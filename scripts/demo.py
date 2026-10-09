"""Generate all demonstrations, including synthetic calibration examples."""
from pathlib import Path
import os
import numpy as np
import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", "/tmp/polaris-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/polaris-cache")
from polaris.cli import main
from polaris.fea import solve_plate
from polaris.optics import optical_images, retardance
from polaris.inverse import reconstruct
from polaris.plots import reconstruction_figure
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
output, examples = root / "outputs", root / "examples"
examples.mkdir(exist_ok=True)
rng = np.random.default_rng(123)
stress = np.linspace(0, 20, 21)
phase = retardance(stress, 5)[:, 1] + .02 + rng.normal(0, .003, len(stress))
pd.DataFrame({"delta_sigma_mpa": stress, "retardance_rad": phase}).to_csv(examples/"synthetic_phase_calibration.csv", index=False)
reference = np.tile(np.linspace(.05, .85, 17)[:, None], (1, 3))
measured = reference*np.array([1.03, .95, 1.08])+np.array([.01, .02, .015])
data = {f"reference_{c}": reference[:, k] for k, c in enumerate("rgb")}
data.update({f"measured_{c}": measured[:, k] for k, c in enumerate("rgb")})
pd.DataFrame(data).to_csv(examples/"synthetic_camera_calibration.csv", index=False)
main(["simulate", "--output", str(output/"kirsch")])
main(["simulate", "--model", "fea", "--output", str(output/"fea")])
main(["calibrate", "stress-optic", str(examples/"synthetic_phase_calibration.csv"), "--output", str(output/"phase_fit.json")])
main(["calibrate", "camera", str(examples/"synthetic_camera_calibration.csv"), "--output", str(output/"camera_fit.json")])
main(["validate", "--held-out", "--output", str(output/"validation.json")])
field = solve_plate(1400, radial=12, angular=64, nx=101, ny=41).field
measured = optical_images(field)["rgb_linear"]+np.random.default_rng(17).normal(0, .001, (*field.outside.shape, 3))
result = reconstruct(measured, field.phi_rad, noise_std=.001)
result.valid &= field.outside
np.savez_compressed(output/"reconstruction.npz", **vars(result), reference_delta_sigma_mpa=field.delta_sigma_mpa)
fig = reconstruction_figure(field, result)
fig.savefig(output/"POLARIS_X_Reconstruction.png", dpi=155, bbox_inches="tight")
plt.close(fig)
print(f"Complete demonstration: {output}")
