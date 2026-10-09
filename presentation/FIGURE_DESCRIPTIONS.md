# POLARIS-X: numbered figures and slide descriptions

Figures are numbered in the order supplied for this presentation. Each number refers to the complete composite figure, not an individual panel.

## Overall description slide

**Title: POLARIS-X — From mechanical stress to polarized-light images**

**Objective:** Demonstrate how stress around a circular hole changes the optical response of an ideal birefringent specimen, and explore where stress differences can be reconstructed from synthetic images.

- Mechanical models calculate the stress field and principal-axis orientation around the hole.
- The stress-optic law converts principal stress difference into phase retardation; the Jones model predicts intensity through a rotating analyzer.
- Finite-element results show the mesh, displacement and finite-plate stress-to-light calculation.
- Inverse fitting estimates principal stress differences in optically informative regions and reports uncertainty and unresolved pixels.

**Workflow:** Mechanical loading → Stress field → Optical retardation → Synthetic images → Constrained reconstruction

**Scope:** Synthetic, numerically checked results using illustrative material parameters. Experimental calibration and validation are still required.

## Image 1 — Effect of analyzer rotation on the optical image

**File:** `Image_1_Analyzer_Rotation.png`

**Slide description:**

- The same stress field is viewed with the analyzer at 0°, 45°, 90° and 135° relative to the input polarization.
- Parallel polarizers (0°) give a bright background; crossed polarizers (90°) suppress the background and reveal stress-induced optical contrast around the hole.
- The 45° and 135° views produce complementary intensity variations. The ideal clear hole is bright at 0°, dark at 90° and intermediate at 45°/135°.

**Caption:** Rotating-analyzer images of an unchanged mechanical stress field, illustrating the dependence of optical intensity on analyzer orientation.

**What to say:** “We have not changed the load between these panels. The image changes because the analyzer selects a different component of the emerging polarized light.”

**Interpretation note:** Display gamma modifies brightness. Optical intensity depends on retardation and principal-axis orientation, so brightness is not a direct stress scale.

## Image 2 — Finite-element mesh and specimen deformation

**File:** `Image_2_FEA_Mesh_and_Deformation.png`

**Slide description:**

- The left panel shows the triangular finite-element mesh, refined near the circular hole where stress varies rapidly.
- The right panel shows the deformed shape, with displacement magnified 100× for visibility.
- The color scale represents actual displacement magnitude in millimetres; it is not multiplied by the visual magnification factor.

**Caption:** Finite-element mesh and calculated displacement of the finite plate under tension; deformed coordinates are displayed at 100× magnification.

**What to say:** “The plate is supported on its left edge and loaded on its right edge in this example. The mesh resolves the region near the hole, and the exaggerated shape helps us see the calculated deformation.”

**Interpretation note:** This is a simplified linear-elastic plane-stress model. Deformation magnitude is not the same quantity as stress, and the plotted shape is visually exaggerated.

## Image 3 — Finite-plate stress, retardation and synthetic optical images

**File:** `Image_3_FEA_Stress_and_Optics.png`

**Slide description:**

- The top-left panel shows the principal stress difference in MPa, with elevated values near the upper and lower parts of the hole boundary.
- The top-middle panel converts that stress difference into phase retardation at 525 nm; the top-right panel combines three ideal channels into synthetic RGB at a 90° analyzer angle.
- The lower panels show the individual 630, 525 and 450 nm intensities. Their responses differ because retardation depends on wavelength.

**Caption:** Finite-element stress field converted into phase retardation and ideal polarized-light images using the stress-optic law and Jones optics.

**What to say:** “This figure connects the mechanical and optical calculations. The stress field supplies both stress difference and principal-axis orientation to the optical model, which predicts the images.”

**Interpretation note:** The hole is masked in the stress/phase maps and acts as clear air in the optical model. High stress need not coincide with maximum image brightness. The assumed stress-optic coefficient has not been experimentally calibrated.

## Image 4 — Stress reconstruction and uncertainty

**File:** `Image_4_Reconstruction_and_Uncertainty.png`

**Slide description:**

- The left panel is the reference principal stress difference from the mechanical simulation; the middle panel shows the recovered values only at pixels passing the reconstruction validity checks.
- White regions in the reconstruction include the hole and unresolved pixels; they must not be interpreted as zero stress.
- The right panel shows the approximate 95% interval half-width in MPa. Smaller values indicate tighter local uncertainty intervals under the model assumptions.

**Caption:** Comparison of reference and reconstructed principal stress differences, with approximate uncertainty intervals shown for valid reconstructed pixels.

**What to say:** “The method reconstructs stress differences only where the optical measurements provide enough information. It explicitly leaves unresolved regions blank and estimates uncertainty for the retained values.”

**Interpretation note:** The reconstruction uses known principal-axis orientation, thickness and optical coefficient. Intervals are conditional local approximations and exclude calibration and model uncertainty. This figure does not demonstrate complete stress-tensor recovery or experimental accuracy.

## Presentation sequence

Use the overall description first, then Images 1–4 in the numbered order. For a mechanics-first explanation, present Image 2 → Image 3 → Image 1 → Image 4 while keeping the figure numbers unchanged.
