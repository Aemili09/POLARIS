# Scientific methods and data contracts

## Finite-element mechanics

The native solver uses three-node constant-strain triangles in 2D plane stress, consistent N/mm/MPa units, and direct sparse solution. Radial rings connect the polygonal hole to the rectangle. Rays include rectangle corners, and spacing is refined near the hole. Mesh dimensions control mechanics; `nx`/`ny` only control output sampling.

For each element, Kₑ = d A Bᵀ D B. Nodal stress recovery uses area-weighted adjacent element stresses followed by linear interpolation over the actual triangulation. `fea_mesh.npz` preserves unsmoothed element stresses and nodal displacements. Grid peak stress can differ from element peak stress because of recovery and sampling. Refine the mesh to assess local peak error. The geometry is limited to one centered circular hole.

Boundary conditions:

- Left roller: ux = 0 on the left edge; uy = 0 at its middle node.
- Left clamped: ux = uy = 0 on the left edge.
- Right edge: x traction, uniform or proportional to 1 − (2y/W)², normalized to the requested total force.
- Hole, top and bottom: traction-free.

Reference width only affects the Kirsch force conversion. Finite-plate nominal stress uses actual width × thickness. Thickness multiplies element stiffness. Plane stress, linear material and small deformation are assumptions, not a general PMMA model. No ANSYS or FreeCAD execution is claimed.

## Stress interchange

UTF-8 CSV header:

```text
x_mm,y_mm,sigma_x_mpa,sigma_y_mpa,tau_xy_mpa,material
```

Rows may be unordered. Include every point of a complete, uniformly spaced rectangular Cartesian grid, including clear-space points with finite zero stresses. Coordinates must span the centered configured length/width. `material` is optional: 1 for material, 0 for clear space. If absent, the configured circle supplies the mask. Duplicate coordinates, missing grid points, non-finite values, invalid masks, mismatched bounds and missing columns are rejected. Convert solver Pa values to MPa before import. For an external FEA mesh, interpolate its stress field onto this grid using the solver's domain mask before export. The importer does not infer boundaries from scattered nodes.

Simulation NPZ contains `x_mm`, `y_mm`, three Cartesian stresses, `material`, `delta_sigma_mpa`, `phi_rad`, `rgb_linear`, `retardance_rad`, and a JSON metadata string with geometry, optics, model and analyzer settings. Array axes are (y, x), with the last axis R/G/B for optical arrays. The first y row is the bottom of the image; gamma never enters these arrays. Load NPZ with `allow_pickle=False`.

## Calibration

For material calibration, independently determine principal stress differences and unwrapped optical retardance at a known wavelength and thickness. Supply `delta_sigma_mpa,retardance_rad`. At least three measurements and distinct stress levels are required. Fit:

```text
retardance_rad = phase_offset_rad + coefficient_pa_inv × 2π × d_m × delta_sigma_pa / wavelength_m
```

The intercept can expose a fixed phase offset. The forward model assumes zero specimen/background phase offset; account for the measured offset in experimental preprocessing. It is not automatically added to spatial birefringence. Coefficient standard error uses ordinary least squares with independent equal-variance phase errors, excluding force, geometry and unwrapping uncertainty. Enter the coefficient into the application or pass `--coefficient` to simulation. Do not fit wrapped phase as unwrapped phase.

For camera calibration, acquire multiple known linear intensity references with unchanged exposure, illumination and processing. Supply:

```text
reference_r,reference_g,reference_b,measured_r,measured_g,measured_b
```

Normalize all values to [0,1]. Each channel needs at least three unsaturated, varying reference levels. Fit `measured = gain × reference + offset`; saturated measured values (0 or 1) are excluded. Correction is `(measured − offset) / gain` without clipping. This assumes linear response with no channel mixing; it does not measure a full spectral response. Saturation destroys information; avoid clipped images for quantitative inversion.

`examples/synthetic_*` are deterministic generated data for software demonstration, not measurements of any specimen or camera.

## Inverse reconstruction

For known principal angle φ, analyzer α and wavelength λ:

```text
Iλ = cos² α + sin(2φ) sin(2α − 2φ) sin²(kλ Δσ / 2)
kλ = 2π d C × 10⁶ / λ  (Δσ in MPa)
```

The inverse searches a nonnegative stress interval with all three channels, refines its minimum locally, and compares competing minima. It assumes independent equal-variance Gaussian intensity errors. Search resolution is checked against phase sampling. The QWP forward extension is excluded from this inverse model.

| Output array | Meaning |
|---|---|
| `delta_sigma_mpa` | Best candidate, including unresolved pixels; always consult `valid` |
| `standard_error_mpa` | Local Fisher standard error from intensity derivatives |
| `valid` | Sufficient sensitivity, acceptable residual, no rival minimum, away from bounds |
| `ambiguous` | Competing local minima within Δχ² ≤ 3.84 |
| `boundary` | Fit or its approximate 95% interval reaches a search bound |
| `residual_rms` | RMS residual in normalized linear intensity |

Dark axes have zero information; small derivatives imply large uncertainty. Pixels are rejected when local standard error exceeds 10% of the search range or RMS residual exceeds four noise standard deviations. Approximate 95% intervals use ±1.96 standard errors, conditional on known orientation and exact optical parameters. The normal approximation can be inaccurate near low-sensitivity regions. Invalid estimates remain available for diagnosis and are never labelled as recovered data.

Input NPZ requires `rgb_linear` and `phi_rad`, optionally `material`. The CLI uses geometry/optics/analyzer metadata if present; otherwise flags supply them. The application checks metadata against its sidebar. PNG RGB is unsuitable because gamma, color processing and clipping break the linear-intensity assumption. Inversion from the noisy camera extension needs its heteroscedastic shot noise accounted for; the constant-noise approximation does not provide calibrated shot-noise intervals.

The held-out study solves FEA at 600 N and 1400 N, supplies exact principal orientation, adds seeded Gaussian noise (σ=0.001), and reconstructs over 0–30 MPa. These loads differ from the 1000 N demonstration. No parameters are trained on them. Accuracy and empirical interval coverage are evaluated only over valid material pixels; valid-pixel fractions are reported. This tests algorithm consistency; independent measurements are needed to validate the optical model and material assumptions.
