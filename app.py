"""Interactive POLARIS-X laboratory: streamlit run app.py."""
from dataclasses import asdict
from io import BytesIO
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from polaris.mechanics import Geometry, StressField, kirsch
from polaris.fea import solve_plate
from polaris.optics import OpticalConfig, optical_images, camera_image
from polaris.plots import main_figure, analyzer_figure, deformation_figure, reconstruction_figure
from polaris.data import stress_csv, read_stress_csv, save_archive
from polaris.calibration import fit_stress_optic, fit_camera, correct_camera
from polaris.inverse import reconstruct
from polaris.validation import physics_checks, held_out_study

st.set_page_config(page_title="POLARIS-X · Stress imaging laboratory", page_icon="◈", layout="wide")
st.markdown("""<style>
.block-container {padding-top: 2rem; max-width: 1500px;}
[data-testid="stMetric"] {background: #142034; border: 1px solid #26384c; border-radius: 10px; padding: 16px;}
h1 {letter-spacing: -.045em;}
</style>""", unsafe_allow_html=True)
st.caption("POLARIS-X / VIRTUAL OPTICS LABORATORY")
st.title("See stress through light.")
st.write("Explore mechanical stress, optical retardation, and polarimetric imaging in one reproducible experiment.")


@st.cache_data(show_spinner=False, max_entries=8)
def mechanics(model, force, geometry, young, poisson, radial, angular, grip, profile):
    if model == "Analytical · Kirsch":
        return kirsch(force, geometry, nx=401, ny=161), None
    result = solve_plate(force, geometry, young, poisson, radial, angular, nx=401, ny=161,
                         grip=grip, load_profile=profile)
    return result.field, result


def show_figure(fig, name):
    st.pyplot(fig)
    data = BytesIO()
    fig.savefig(data, format="png", dpi=155, bbox_inches="tight")
    st.download_button("Download figure", data.getvalue(), file_name=name, mime="image/png", key=name)
    plt.close(fig)


with st.sidebar:
    st.header("Experiment controls")
    model = st.selectbox("Mechanical model", ["Analytical · Kirsch", "Finite plate · FEA", "Import stress CSV"])
    force = st.number_input("Nominal force (N)" if model.startswith("Analytical") else "Applied force (N)", 0.0, 100000.0, 1000.0, 100.0)
    analyzer = st.slider("Analyzer angle (degrees)", 0, 180, 90)
    gamma = st.slider("Display gamma", 0.2, 2.0, 0.65, 0.05)
    with st.expander("Geometry and material"):
        length = st.number_input("Length / display window (mm)", 10.0, 1000.0, 100.0)
        width = st.number_input("Width / display window (mm)", 5.0, 500.0, 40.0)
        radius = st.number_input("Hole radius (mm)", 0.1, 200.0, 5.0)
        thickness = st.number_input("Thickness (mm)", 0.1, 100.0, 5.0)
        reference_width = st.number_input("Kirsch nominal reference width (mm)", 1.0, 500.0, 40.0)
        young = st.number_input("Young's modulus (MPa, assumed)", 1.0, 500000.0, 3000.0)
        poisson = st.number_input("Poisson ratio (assumed)", 0.0, 0.49, 0.35, 0.01)
        coefficient = st.number_input("Stress-optic coefficient (×10⁻¹² Pa⁻¹)", 0.01, 100.0, 3.0, 0.1)
    with st.expander("Finite-element controls"):
        radial = st.select_slider("Radial mesh layers", [8, 12, 20, 32], value=20)
        angular = st.select_slider("Angular mesh divisions", [32, 64, 96, 160], value=96)
        grip = st.selectbox("Left grip", ["roller", "clamped"])
        profile = st.selectbox("Right-edge load distribution", ["uniform", "parabolic"])
    with st.expander("Optical components"):
        red = st.number_input("Red wavelength (nm)", 350.0, 900.0, 630.0)
        green = st.number_input("Green wavelength (nm)", 350.0, 900.0, 525.0)
        blue = st.number_input("Blue wavelength (nm)", 350.0, 900.0, 450.0)
        qwp_on = st.checkbox("Add ideal quarter-wave plate after specimen")
        qwp_angle = st.slider("Quarter-wave plate axis (degrees)", 0, 180, 45) if qwp_on else None
    st.caption("Parameters are illustrative until calibrated against measured data.")

try:
    geometry = Geometry(length, width, radius, thickness, reference_width)
    config = OpticalConfig(coefficient*1e-12, (red, green, blue), gamma)
    if model == "Import stress CSV":
        upload = st.file_uploader("Stress grid CSV", type="csv")
        st.caption("Columns: x_mm, y_mm, sigma_x_mpa, sigma_y_mpa, tau_xy_mpa; optional material (0/1). Complete centered rectangular grid; set matching dimensions in the sidebar.")
        if upload is None:
            st.info("Upload a stress grid exported from POLARIS-X or resampled from your FEA solver.")
            st.stop()
        field, fea = read_stress_csv(upload, geometry), None
    else:
        with st.spinner("Solving mechanical field…"):
            field, fea = mechanics(model, force, geometry, young, poisson, radial, angular, grip, profile)
    optical = optical_images(field, analyzer, config, qwp_angle)
except (ValueError, RuntimeError) as exc:
    st.error(str(exc))
    st.stop()

field.metadata.update(analyzer_deg=analyzer, quarter_wave_deg=qwp_angle)
cols = st.columns(4)
cols[0].metric("Reference stress", f"{field.metadata.get('remote_mpa', 0):.2f} MPa" if "remote_mpa" in field.metadata else "Imported")
cols[1].metric("Peak principal difference", f"{field.delta_sigma_mpa.max():.2f} MPa")
cols[2].metric(f"Peak phase · {green:g} nm", f"{optical['retardances'][..., 1].max():.2f} rad")
cols[3].metric("Analyzer", f"{analyzer}°", "Crossed" if analyzer == 90 else "Parallel" if analyzer == 0 else "Rotated", delta_color="off")
if model.startswith("Analytical"):
    st.info("Kirsch models an infinite plate. The rectangle is a display window; force is a nominal conversion using reference width × thickness.")
elif fea is not None:
    st.info("Finite plate: linear elastic plane stress with a polygonal circular hole. Check mesh convergence before interpreting local peak stresses.")

forward, sweep, mech, calibration, inverse, verification = st.tabs(
    ["Stress & light", "Analyzer & camera", "Mechanics & exports", "Calibration", "Reconstruction", "Verification"])

with forward:
    show_figure(main_figure(field, analyzer, config, qwp_angle), "POLARIS_X_Main_Results.png")
    st.caption("Three ideal monochromatic channels form synthetic RGB. Gamma affects display only. Stress and phase are masked in the clear hole.")

with sweep:
    show_figure(analyzer_figure(field, config, qwp_angle), "POLARIS_X_Analyzer_Sweep.png")
    st.subheader("Simulated camera")
    c1, c2 = st.columns(2)
    photons = c1.number_input("Full-scale photon count", 100.0, 1000000.0, 10000.0, 1000.0)
    read_noise = c2.number_input("Read noise (normalized standard deviation)", 0.0, 0.1, 0.002, 0.001, format="%.3f")
    noisy = camera_image(optical["rgb_linear"], photons, read_noise)
    st.image(noisy**gamma, caption="Seeded shot + read noise · display gamma applied", clamp=True)
    buffer = BytesIO()
    np.savez_compressed(buffer, rgb_linear=noisy, phi_rad=field.phi_rad, material=field.outside,
                        metadata_json=json.dumps({**field.metadata, "geometry": asdict(geometry), "optics": asdict(config),
                                                  "camera": {"photons": photons, "read_noise": read_noise, "seed": 42}}))
    st.download_button("Download raw camera simulation", buffer.getvalue(), "camera_simulation.npz")

with mech:
    if fea is not None:
        scale = st.slider("Deformation magnification", 1, 500, 100)
        show_figure(deformation_figure(fea, scale), "POLARIS_X_Deformation.png")
        st.json(fea.diagnostics)
        buffer = BytesIO()
        np.savez_compressed(buffer, nodes_mm=fea.nodes_mm, triangles=fea.triangles,
                            displacement_mm=fea.displacement_mm, element_stress_mpa=fea.element_stress_mpa)
        st.download_button("Download FEA mesh, displacements and stresses", buffer.getvalue(), "fea_mesh.npz")
    else:
        st.write("Select Finite plate · FEA for mesh, displacement and force-balance diagnostics.")
    st.download_button("Export stress grid CSV", stress_csv(field), "stress_field.csv", "text/csv")
    buffer = BytesIO()
    save_archive(buffer, field, optical, config)
    st.download_button("Export raw simulation NPZ", buffer.getvalue(), "simulation.npz")
    st.download_button("Export experiment settings", json.dumps({**field.metadata, "geometry": asdict(geometry), "optics": asdict(config)}, indent=2), "experiment.json", "application/json")

with calibration:
    st.subheader("Measure, fit, then apply")
    st.write("Fit the specimen coefficient from independently measured, unwrapped retardance at known stress differences. A separate linear camera fit estimates channel gains and offsets.")
    st.caption("Synthetic example files in examples/ demonstrate the formats; they are not experimental measurements.")
    phase_file = st.file_uploader("Phase calibration CSV · delta_sigma_mpa, retardance_rad", type="csv", key="phase")
    cal_wavelength = st.number_input("Calibration wavelength (nm)", 350.0, 900.0, 525.0)
    if phase_file is not None:
        try:
            df = pd.read_csv(phase_file)
            fit = fit_stress_optic(df["delta_sigma_mpa"], df["retardance_rad"], thickness, cal_wavelength)
            st.json(fit.to_dict())
            st.success(f"Fitted coefficient: {fit.coefficient_pa_inv/1e-12:.4f} ×10⁻¹² Pa⁻¹. Enter this value in Geometry and material to apply it.")
            st.download_button("Download coefficient fit", json.dumps(fit.to_dict(), indent=2), "stress_optic_calibration.json")
        except (ValueError, KeyError) as exc:
            st.error(str(exc))
    camera_file = st.file_uploader("Camera calibration CSV · reference_r/g/b, measured_r/g/b", type="csv", key="camera")
    if camera_file is not None:
        try:
            df = pd.read_csv(camera_file)
            fit = fit_camera(df[[f"reference_{c}" for c in "rgb"]], df[[f"measured_{c}" for c in "rgb"]])
            st.json(fit)
            st.download_button("Download camera fit", json.dumps(fit, indent=2), "camera_calibration.json")
        except (ValueError, KeyError) as exc:
            st.error(str(exc))

with inverse:
    st.subheader("Recover principal stress difference")
    st.write("Bounded multiwavelength fitting uses known principal-axis orientation, thickness and stress-optic coefficient. Dark axes, competing phase solutions and bounds can make a pixel unresolved.")
    source = st.radio("Reconstruction source", ["Synthetic demonstration", "Measured NPZ"], horizontal=True)
    max_stress = st.number_input("Upper stress bound (MPa)", 1.0, 200.0, 30.0)
    noise = st.number_input("Intensity noise standard deviation", 0.0001, 0.1, 0.002, 0.001, format="%.4f")
    measured_file = st.file_uploader("NPZ with rgb_linear and phi_rad; optional material mask", type="npz") if source == "Measured NPZ" else None
    camera_fit_file = st.file_uploader("Optional camera calibration JSON", type="json") if source == "Measured NPZ" else None
    st.caption("Measured arrays use the sidebar's wavelengths, coefficient, thickness and analyzer angle. Supply raw linear intensities, never gamma-adjusted PNGs. If using an archive with metadata, the settings must match. QWP reconstruction is not supported.")
    if st.button("Run reconstruction", disabled=qwp_on):
        try:
            target = None
            if source == "Synthetic demonstration":
                sl = (slice(None, None, 5), slice(None, None, 5))
                target = StressField(field.x_mm[::5], field.y_mm[::5], field.sigma_x_mpa[sl], field.sigma_y_mpa[sl],
                                     field.tau_xy_mpa[sl], field.outside[sl], geometry, field.metadata)
                image = optical_images(target, analyzer, config)["rgb_linear"]
                image += np.random.default_rng(42).normal(0, noise, image.shape)
                phi, material = target.phi_rad, target.outside
            else:
                if measured_file is None:
                    raise ValueError("Upload the measured NPZ first.")
                with np.load(measured_file, allow_pickle=False) as archive:
                    image, phi = archive["rgb_linear"], archive["phi_rad"]
                    material = archive["material"].astype(bool) if "material" in archive else np.ones(phi.shape, bool)
                    if "metadata_json" in archive:
                        meta = json.loads(str(archive["metadata_json"]))
                        if meta.get("quarter_wave_deg") is not None:
                            raise ValueError("This archive uses a quarter-wave plate; inverse model does not support it.")
                        oc = meta.get("optics", {})
                        if not np.isclose(meta.get("analyzer_deg", analyzer), analyzer) or not np.isclose(meta.get("geometry", {}).get("thickness_mm", thickness), thickness) or not np.isclose(oc.get("stress_optic_pa_inv", config.stress_optic_pa_inv)/config.stress_optic_pa_inv, 1) or not np.allclose(oc.get("wavelengths_nm", config.wavelengths_nm), config.wavelengths_nm):
                            raise ValueError("Archive optical settings differ from the sidebar. Set matching parameters first.")
                if camera_fit_file is not None:
                    fit = json.load(camera_fit_file)
                    image = correct_camera(image, fit["gains"], fit["offsets"])
            with st.spinner("Searching stress and estimating uncertainty…"):
                result = reconstruct(image, phi, thickness, config, analyzer, max_stress, noise)
            if material.shape != phi.shape:
                raise ValueError("Material mask must match phi_rad.")
            result.valid &= material
            st.write(f"Resolved {result.valid.sum():,} of {material.sum():,} material pixels.")
            if target is not None:
                show_figure(reconstruction_figure(target, result), "POLARIS_X_Reconstruction.png")
                if result.valid.any():
                    error = result.delta_sigma_mpa[result.valid]-target.delta_sigma_mpa[result.valid]
                    st.metric("RMSE on resolved pixels", f"{np.sqrt(np.mean(error**2)):.3f} MPa")
            else:
                st.write("Reconstruction complete. Download the array results and masks below.")
            buffer = BytesIO()
            np.savez_compressed(buffer, **vars(result))
            st.download_button("Download reconstruction and uncertainty", buffer.getvalue(), "reconstruction.npz")
            st.caption("Intervals are local Gaussian approximations conditional on known orientation, coefficient and thickness. They exclude model error and calibration uncertainty. Unresolved pixels must not be treated as recovered stress.")
        except (ValueError, KeyError, OSError) as exc:
            st.error(str(exc))

with verification:
    st.subheader("Check the physics")
    st.write("Run the notebook's consistency checks, or test reconstruction on two independent finite-plate load cases with seeded synthetic noise.")
    if st.button("Run physics checks"):
        for check in physics_checks():
            st.success(check)
    if st.button("Run held-out FEA study"):
        with st.spinner("Solving held-out loads and reconstructing…"):
            report = held_out_study()
        st.dataframe(pd.DataFrame(report), hide_index=True)
        st.download_button("Download validation report", json.dumps(report, indent=2), "held_out_validation.json")
    st.markdown("""**Scope of this laboratory**

- Kirsch: infinite plate, circular hole, uniform remote tension.
- FEA: finite rectangular plate, one centered hole, small-strain isotropic elasticity, plane stress.
- Optics: ideal retarder and monochromatic channels; optional ideal quarter-wave plate and synthetic camera noise.
- Calibration: tools for measured phase and linear camera references; examples are synthetic.
- Inverse: stress difference with known orientation and bounded search; explicit unresolved-pixel masks.

Complex fixtures/contact, arbitrary defects, failure prediction, real hardware acquisition and a validated physical digital twin require additional models and experimental data.
""")
