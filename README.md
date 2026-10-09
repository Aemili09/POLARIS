# POLARIS-X

Polarimetric stress imaging laboratory, built from the supplied **POLARIS-X — Simulation V1.1** notebook. Run the original analytical demonstration, explore a finite-plate model, fit calibration data, and reconstruct principal stress differences under explicit assumptions.

## Download the simulation

- [Complete project with generated results (29 MB)](https://github.com/Aemili09/POLARIS/raw/refs/heads/polaris-x-download/downloads/POLARIS-X_Download.zip)
- [Application and original notebook only (57 KB)](https://github.com/Aemili09/POLARIS/raw/refs/heads/polaris-x-download/downloads/POLARIS-X_Source.zip)

Extract either ZIP and open `POLARIS-X/START_HERE.md` for Windows, macOS, Linux and Google Colab instructions. The smaller ZIP excludes pre-generated results; you can generate them by running the application. Checksums are in `downloads/SHA256SUMS`.

If a link displays a GitHub file page, use **Download raw file**. You can also select the `polaris-x-download` branch and choose **Code → Download ZIP** to download this entire branch. Sign in with an account that has repository access if required.

## Run

Python 3.11+ is required (tested on Python 3.12, Linux). No GPU, paid service, account, or external FEA solver is needed.

```bash
bash scripts/setup.sh
bash scripts/start.sh
```

The second command starts the Streamlit laboratory on port 8501. Its tabs provide stress and optical maps, analyzer rotation, shot/read noise, FEA mesh and deformation, calibration uploads, reconstruction, verification, and PNG/CSV/NPZ downloads. Stop it with Ctrl+C. Set `PORT` to change the port.

Generate the complete demonstration without a browser:

```bash
.venv/bin/python scripts/demo.py
```

Results are written to `outputs/`: the two original named figures, analytical and FEA stress grids, lossless arrays, mesh/displacement data, calibration fits, reconstruction comparison, and validation report. `examples/` contains clearly labelled synthetic calibration inputs.

## What is built

| Notebook item | Implementation |
|---|---|
| Original runnable Colab notebook | Preserved verbatim in `notebooks/POLARIS-X_Colab_Simulation_VERIFIED.ipynb` |
| Infinite-plate Kirsch stresses and principal axes | `polaris/mechanics.py` |
| Stress-optic retardance; Jones linear-retarder optics | `polaris/optics.py` |
| Synthetic RGB, 630/525/450 nm channels, configurable analyzer | Interactive laboratory and CLI |
| Main six-panel figure and 0/45/90/135° analyzer comparison | `polaris/plots.py`; original output filenames retained |
| Numerical and physical consistency checks | `polaris/validation.py` and automated tests |
| Finite plate with hole, boundary conditions and distributed loading | Native CST plane-stress FEA in `polaris/fea.py` |
| Mechanical deformation | Nodal displacement export and magnified mesh plot |
| FEA stress export/import | Unit-labelled rectangular-grid CSV; native mesh NPZ |
| Material and camera calibration | Measured phase regression; per-channel linear gain/offset fitting |
| Inverse reconstruction and held-out uncertainty evaluation | Bounded known-orientation inversion, masks, standard errors, independent FEA loads |
| Optional optical/camera extensions | Ideal quarter-wave plate after specimen, photon shot noise and read noise |

The application implements software workflows for the notebook's proposed next stage. Real measurements, fixture/contact modelling, arbitrary geometries and defects, material failure prediction, and a validated hardware digital twin are outside this implementation. The original notebook describes these as future work or limitations; no experimental validation is implied.

## Command-line workflows

```bash
# Original default: nominal 1000 N, crossed analyzer
.venv/bin/polaris simulate --output outputs/kirsch

# Notebook's suggested changes
.venv/bin/polaris simulate --force 1500 --analyzer 45 --output outputs/1500N_45deg

# Finite plate, clamped left grip, parabolic right-edge load
.venv/bin/polaris simulate --model fea --grip clamped --load-profile parabolic --output outputs/fea_clamped

# Refine the finite-element mesh (separate from image resolution)
.venv/bin/polaris simulate --model fea --radial 32 --angular 128 --output outputs/fea_refined

# Imported complete grid; dimensions must match the CSV bounds
.venv/bin/polaris simulate --model csv --input outputs/fea/stress_field.csv --output outputs/imported

# Fit measured unwrapped phase or linear camera reference data
.venv/bin/polaris calibrate stress-optic examples/synthetic_phase_calibration.csv --output outputs/phase_fit.json
.venv/bin/polaris calibrate camera examples/synthetic_camera_calibration.csv --output outputs/camera_fit.json

# Reconstruct an archive using its saved optical metadata
.venv/bin/polaris reconstruct outputs/kirsch/simulation.npz --max-stress 30 --noise 0.002

# Physical checks plus held-out synthetic inverse study
.venv/bin/polaris validate --held-out
```

`polaris simulate --help` lists geometry, material, wavelength, resolution, grip and optical options. Figures apply display gamma; CSV and NPZ preserve physical values. To fit corrected measured images, use the application's optional camera calibration upload, or `polaris.calibration.correct_camera` before creating an input NPZ.

## Physics and interpretation

- **Analytical model:** infinite elastic plate, circular hole, uniform remote x tension. The 100 × 40 mm rectangle is only a viewing window. Nominal force is divided by reference width × thickness; 1000 N / (40 mm × 5 mm) = 5 MPa.
- **Finite model:** finite rectangular plate with one centered circular hole; small-strain isotropic plane stress. Default illustrative modulus is 3000 MPa and Poisson ratio 0.35. The left edge fixes x displacement; `roller` also fixes one y displacement to remove rigid translation, while `clamped` fixes all left-edge y displacements. The right edge receives uniform or parabolic x traction integrated to the requested total force. Remaining boundaries are free. These are idealized grips, without contact or fixture bodies.
- **Optics:** Δσ = √((σx − σy)² + 4τxy²), and δ = 2πdCΔσ/λ. The default C = 3 × 10⁻¹² Pa⁻¹ is assumed, not measured. Incident light is x-polarized. An ideal optional QWP acts after the specimen. The hole is clear air and contributes no retardance.
- **Camera:** three ideal monochromatic channels represent RGB. Optional noise uses Poisson photons and Gaussian read noise before gain/offset and clipping. This is not a spectral or experimentally calibrated camera model.
- **Inverse:** known orientation, coefficient, thickness, wavelengths and analyzer angle are required. Only principal stress difference is reconstructed; individual stress components are not identifiable from these images alone. Dark axes, weak sensitivity, fringe ambiguity and search bounds can prevent recovery. Use the validity mask. See [scientific methods and data formats](docs/METHODS.md).

The default synthetic inverse validation uses independent 600 N and 1400 N FEA fields. It supplies their exact orientation as a prior and adds seeded Gaussian intensity noise. It evaluates numerical inversion under the model assumptions, not physical accuracy. Report valid-pixel coverage alongside RMSE; approximate intervals exclude calibration, mesh and model uncertainty.

The [detailed figure audit](docs/FIGURE_AUDIT.md) records corrected interpolation/display defects and remaining scientific limitations. Image 4 resolves about 34% of material pixels in its synthetic example, and some accepted fits select the wrong fringe branch; acceptance is not proof of correctness. Use the updated figures and report their uncertainty and incomplete coverage.

## Tests and notebook

```bash
MPLCONFIGDIR=/tmp/polaris-matplotlib XDG_CACHE_HOME=/tmp/polaris-cache .venv/bin/python -m pytest -q
.venv/bin/python scripts/execute_notebook.py
```

The tests check the Kirsch traction-free hole boundary, load scaling, far-field limit, Malus/Jones relations, energy conservation, camera noise, FEA constant-strain patch, force balance, mesh refinement, calibration recovery, inverse identifiability and uncertainty, CSV round trips, CLI exports, and interactive app actions.

The notebook runner executes the original notebook with the project's Python interpreter and saves its executed copy and figures in `outputs/notebook/`. You can also upload the preserved notebook to Colab and select **Runtime → Run all**, as in the original instructions.

Dependencies, including development tools, are pinned in `requirements.lock`; `pyproject.toml` specifies the installable package and CLI. Setup is repeatable and cloud startup instructions are in `scripts/start.sh`.
