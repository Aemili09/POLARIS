"""Command-line entry points for repeatable simulation and calibration."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .mechanics import Geometry, kirsch
from .fea import solve_plate
from .optics import OpticalConfig, optical_images
from .data import stress_csv, read_stress_csv, save_archive
from .plots import main_figure, analyzer_figure, deformation_figure
from .calibration import fit_stress_optic, fit_camera
from .inverse import reconstruct
from .validation import physics_checks, held_out_study


def parser():
    p = argparse.ArgumentParser(description="POLARIS-X polarimetric stress imaging")
    sub = p.add_subparsers(dest="command", required=True)
    sim = sub.add_parser("simulate", help="Generate maps, analyzer sweep, CSV and raw NPZ")
    sim.add_argument("--model", choices=("kirsch", "fea", "csv"), default="kirsch")
    sim.add_argument("--input", type=Path, help="Stress CSV for --model csv")
    sim.add_argument("--force", type=float, default=1000)
    sim.add_argument("--analyzer", type=float, default=90)
    sim.add_argument("--length", type=float, default=100)
    sim.add_argument("--width", type=float, default=40)
    sim.add_argument("--radius", type=float, default=5)
    sim.add_argument("--thickness", type=float, default=5)
    sim.add_argument("--reference-width", type=float, default=40)
    sim.add_argument("--coefficient", type=float, default=3e-12)
    sim.add_argument("--wavelengths", type=float, nargs=3, default=[630, 525, 450])
    sim.add_argument("--gamma", type=float, default=0.65)
    sim.add_argument("--nx", type=int, default=551)
    sim.add_argument("--ny", type=int, default=241)
    sim.add_argument("--young", type=float, default=3000)
    sim.add_argument("--poisson", type=float, default=0.35)
    sim.add_argument("--radial", type=int, default=20)
    sim.add_argument("--angular", type=int, default=96)
    sim.add_argument("--grip", choices=("roller", "clamped"), default="roller")
    sim.add_argument("--load-profile", choices=("uniform", "parabolic"), default="uniform")
    sim.add_argument("--quarter-wave", type=float, default=None, help="Optional ideal QWP axis after specimen, degrees")
    sim.add_argument("--output", type=Path, default=Path("outputs/kirsch"))
    check = sub.add_parser("validate", help="Notebook physics checks and optional held-out FEA inverse study")
    check.add_argument("--held-out", action="store_true")
    check.add_argument("--output", type=Path, default=Path("outputs/validation.json"))
    cal = sub.add_parser("calibrate", help="Fit measured unwrapped retardance or linear camera references")
    cal.add_argument("kind", choices=("stress-optic", "camera"))
    cal.add_argument("input", type=Path)
    cal.add_argument("--thickness", type=float, default=5)
    cal.add_argument("--wavelength", type=float, default=525)
    cal.add_argument("--output", type=Path, default=Path("outputs/calibration.json"))
    inv = sub.add_parser("reconstruct", help="Fit an NPZ containing rgb_linear and phi_rad; no QWP")
    inv.add_argument("input", type=Path)
    inv.add_argument("--thickness", type=float, default=5)
    inv.add_argument("--coefficient", type=float, default=3e-12)
    inv.add_argument("--analyzer", type=float, default=90)
    inv.add_argument("--max-stress", type=float, default=30)
    inv.add_argument("--noise", type=float, default=0.002)
    inv.add_argument("--output", type=Path, default=Path("outputs/reconstruction.npz"))
    return p


def main(argv=None):
    p = parser()
    args = p.parse_args(argv)
    try:
        if args.command == "simulate":
            geometry = Geometry(args.length, args.width, args.radius, args.thickness, args.reference_width)
            config = OpticalConfig(args.coefficient, tuple(args.wavelengths), args.gamma)
            fea = None
            if args.model == "kirsch":
                field = kirsch(args.force, geometry, args.nx, args.ny)
            elif args.model == "fea":
                fea = solve_plate(args.force, geometry, args.young, args.poisson, args.radial,
                                  args.angular, args.nx, args.ny, args.grip, args.load_profile)
                field = fea.field
            else:
                if args.input is None:
                    p.error("--model csv requires --input")
                field = read_stress_csv(args.input, geometry)
            field.metadata.update(analyzer_deg=args.analyzer, quarter_wave_deg=args.quarter_wave)
            optical = optical_images(field, args.analyzer, config, args.quarter_wave)
            args.output.mkdir(parents=True, exist_ok=True)
            for name, fig in (("POLARIS_X_Main_Results.png", main_figure(field, args.analyzer, config, args.quarter_wave)),
                              ("POLARIS_X_Analyzer_Sweep.png", analyzer_figure(field, config, args.quarter_wave))):
                fig.savefig(args.output/name, dpi=155, bbox_inches="tight")
                plt.close(fig)
            (args.output/"stress_field.csv").write_text(stress_csv(field))
            save_archive(args.output/"simulation.npz", field, optical, config)
            summary = {**field.metadata, "geometry": asdict(geometry), "optics": asdict(config),
                       "peak_grid_delta_sigma_mpa": float(field.delta_sigma_mpa.max())}
            if fea is not None:
                fig = deformation_figure(fea)
                fig.savefig(args.output/"POLARIS_X_Deformation.png", dpi=155, bbox_inches="tight")
                plt.close(fig)
                np.savez_compressed(args.output/"fea_mesh.npz", nodes_mm=fea.nodes_mm,
                                    triangles=fea.triangles, displacement_mm=fea.displacement_mm,
                                    element_stress_mpa=fea.element_stress_mpa, reaction_n=fea.reaction_n)
            (args.output/"summary.json").write_text(json.dumps(summary, indent=2))
            print(json.dumps(summary, indent=2))
            print(f"Saved results to {args.output.resolve()}")
        elif args.command == "validate":
            checks = physics_checks()
            report = {"physics_checks_passed": checks}
            if args.held_out:
                report["held_out_fea_reconstruction"] = held_out_study()
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(report, indent=2))
            print(json.dumps(report, indent=2))
        elif args.command == "calibrate":
            df = pd.read_csv(args.input)
            if args.kind == "stress-optic":
                result = fit_stress_optic(df.delta_sigma_mpa, df.retardance_rad, args.thickness, args.wavelength).to_dict()
            else:
                result = fit_camera(df[[f"reference_{c}" for c in "rgb"]], df[[f"measured_{c}" for c in "rgb"]])
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2))
            print(json.dumps(result, indent=2))
        else:
            with np.load(args.input, allow_pickle=False) as archive:
                config = OpticalConfig(args.coefficient)
                thickness, analyzer = args.thickness, args.analyzer
                if "metadata_json" in archive:
                    metadata = json.loads(str(archive["metadata_json"]))
                    if metadata.get("quarter_wave_deg") is not None:
                        raise ValueError("Reconstruction does not support quarter-wave-plate images.")
                    config = OpticalConfig(**metadata.get("optics", asdict(config)))
                    thickness = metadata.get("geometry", {}).get("thickness_mm", thickness)
                    analyzer = metadata.get("analyzer_deg", analyzer)
                result = reconstruct(archive["rgb_linear"], archive["phi_rad"], thickness,
                                     config, analyzer, args.max_stress, args.noise)
                if "material" in archive:
                    result.valid &= archive["material"].astype(bool)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            np.savez_compressed(args.output, **vars(result))
            print(f"Saved {args.output}: {result.valid.sum()} / {result.valid.size} valid pixels")
    except (ValueError, OSError, KeyError, AttributeError) as exc:
        p.error(str(exc))


if __name__ == "__main__":
    main()
