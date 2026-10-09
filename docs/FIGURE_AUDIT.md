# Detailed scientific and presentation audit — 9 October 2026

## Verdict

The four figures are numerical Matplotlib plots produced from the project arrays, not generative image artwork. The numbered PNGs initially matched their source plots byte for byte. That provenance does not guarantee scientific correctness. The audit confirmed the core Kirsch/Jones calculations and added independent mechanical benchmarks, but found and corrected actual numerical/display defects. The model assumptions and incomplete inverse reconstruction prevent any claim of “100% correct” physical predictions.

## Confirmed defects and corrections

1. **Spurious missing material at FEA outer edges.** The trigonometric mesh construction placed some nominally rectangular edge nodes about floating-point precision inside the exact boundary. The triangle locator consequently masked 58 material samples in the original full FEA map and 14 in Image 4's reference grid. These produced white corner/edge slivers and, in optical data, incorrectly clear-space values. Outer nodes are now snapped to the intended rectangle before solving. Rechecks find zero missing material samples for the audited grids. The mechanical solution changes only at floating-point precision.
2. **Grid-to-image coordinate alignment.** The arrays contain nodal samples at both endpoints, while `imshow` previously treated those endpoints as outer pixel edges. Pixel centers were therefore slightly shifted/compressed relative to their physical coordinates. The plotting helper now expands image edges by half a grid step and clips the viewing window to the physical bounds. Nearest-neighbor display avoids additional smoothing. Underlying stress values are unchanged.
3. **Reconstruction color saturation.** Image 4 used the reference maximum (20.086 MPa) as the color limit for both maps, but six accepted reconstructed values exceeded it; the maximum estimate was 26.244 MPa. These wrong high-fringe-branch estimates were color-clipped. Both maps now share a scale that includes the reference AND accepted estimates. The high outliers are no longer hidden by saturation. The estimator is unchanged.
4. **Insufficient context on exported figures.** Updated titles identify load and gamma where relevant. Image 4 now explicitly identifies known orientation, accepted-pixel fraction, RMSE, and the conditional nature of its intervals. Its demonstration uses 1400 N, while Images 1–3 use 1000 N; these should not be presented as a single identical load case.

## Evidence for the equations and solver

- Principal stress differences agree with independent symmetric-tensor eigendecomposition.
- The optical implementation agrees with explicit 2×2 Jones rotation/phase matrix multiplication at five analyzer angles and random stress/axis configurations.
- Orthogonal analyzer intensities add to unity within floating-point error before display gamma. The clear-hole linear intensities are 1, 0.5, 0 and 0.5 at 0°, 45°, 90° and 135°. At gamma 0.65, the displayed mid-gray value is about 0.637, not 0.5.
- Kirsch stresses satisfy the traction-free hole boundary, approach remote uniaxial tension, and pass a finite-difference local force-equilibrium check away from the hole.
- The assembled FEA solver reproduces the exact unperforated rectangular-plate tension solution when given a rectangular benchmark mesh. This independently tests loading, restraints, assembly and solution.
- Element stresses agree with a separate affine-displacement-gradient calculation. Existing checks also verify force balance, elastic load scaling and mesh refinement.
- The inverse grid/refinement routine agrees with independent scalar minimizations over the stress range for representative multiwavelength cases. This verifies minimization, not identifiability under all noise realizations.

## Image 1 — analyzer rotation

**Assessment:** consistent with the stated ideal Jones model. The load and stress are fixed between panels. Changes in brightness and color are expected. The hole is an ideal clear-air path.

**Limits:** an ideal monochromatic-channel model, assumed stress-optic coefficient, uniform x-polarized input, and display gamma are used. No physical camera or specimen has been calibrated. The brightest pixel is not necessarily the highest-stress point. Rendered PNG values are not raw linear sensor intensities.

## Image 2 — mesh and deformation

**Assessment:** mechanically consistent within the native small-strain, isotropic, plane-stress CST model. Default load is 1000 N, modulus 3000 MPa, Poisson ratio 0.35, left roller constraint, right uniform traction. Maximum computed displacement is about 0.177495 mm. The displayed shape is magnified 100×; the color scale retains actual millimetres.

**Limits:** idealized constraints replace real fixture/contact bodies; the hole boundary is polygonal. A visual deformation plot is not a convergence study, and the chosen modulus is illustrative. This is the project's native solver, not ANSYS output.

## Image 3 — stress-to-optics conversion

**Assessment:** the stress-optic units and Jones conversion are consistent. With the default grid, maximum principal stress difference is about 15.3306 MPa and maximum 525 nm retardance about 2.75214 rad. The sampled/recovered grid peak is different from the unsmoothed element peak (15.7115 MPa).

**Mesh dependence at 1000 N:**

| Radial / angular divisions | Peak element stress difference (MPa) | Maximum displacement (mm) |
|---|---:|---:|
| 20 / 96, displayed default | 15.7115 | 0.177495 |
| 32 / 128 | 15.9784 | 0.177569 |
| 48 / 192 | 16.1045 | 0.177583 |
| 64 / 256 | 16.1551 | 0.177579 |

The default element peak is about 2.75% below the finest tested peak; the finest tested mesh is not an exact solution. Stress recovery and image sampling add further differences. Use approximate peak values and report the mesh rather than presenting these as exact measured stresses.

## Image 4 — inverse reconstruction

**Assessment:** a constrained synthetic demonstration, not a general or complete stress-recovery result. The exact FEA principal-axis orientation is supplied to the inverse. Forward and inverse share the same ideal optical model. Calibration/model errors are absent from the synthetic generation and excluded from the uncertainty calculation.

Actual displayed case: 1400 N; 101 × 41 grid; 5 mm thickness; C=3×10⁻¹² Pa⁻¹; crossed analyzer; additive independent Gaussian intensity noise σ=0.001; seed 17; 0–30 MPa search interval.

| Metric after correcting the outer mask | Value |
|---|---:|
| Accepted material pixels | 1395 / 4072 |
| Accepted fraction | 34.26% |
| RMSE on accepted pixels | 1.42136 MPa |
| Median absolute error | 0.29411 MPa |
| Maximum absolute error | 19.30935 MPa |
| Accepted pixels with error exceeding 5 MPa | 6 |
| Empirical coverage of approximate 95% local intervals | 95.84% |

“Accepted” means the heuristic checks passed; it does not mean the stress estimate is correct. The six large outliers select incorrect fringe branches in weak/ambiguous optical data. They are retained and disclosed. Aggregate 95.84% coverage in this one realization is not a guarantee of calibrated intervals in experiments or other parameter regimes. The blank regions mean unresolved or outside material, not zero stress. The large unobserved area is fundamental to this illumination/prior/noise combination and must not be hidden.

## Presentation recommendation

Use Images 1–3 for the forward-simulation demonstration, with the stated idealizations. Use Image 4 as an exploratory inverse-method slide and explicitly report incomplete coverage, the known-orientation prior and the outliers. Do not claim experimental validation, full-field stress recovery, exact FEA peaks, ANSYS validation, failure prediction, or a calibrated physical digital twin.

The repository tests and audit address numerical consistency. Independent experimental data and an independent perforated-plate solver comparison remain useful external validation steps.
