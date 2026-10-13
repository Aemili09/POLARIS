# POLARIS — Presentation and Viva Study Guide

Group 18 | Prepared for the presentation on 14 October 2026

Based on the submitted seven-page POLARIS_GROUP 18.pdf, the project repository, the scientific figure audit, and the proposed hardware wiring. This is an editable study guide, not an experimental results report.

**Confirmed presentation plan:** present only the seven submitted slides. You do not plan to show simulation figures or circuit diagrams. No additional diagrams or live demonstration are required by this guide. Detailed numerical results and wiring information are optional background for follow-up questions, not material you must introduce during the talk.

**Confirmed project status:** you have confirmed that the completed work is simulation/software only; hardware and AI remain proposed. Assembly, experimental calibration, a trained defect CNN, and a validated pass/fail system are not completed achievements. A proposed hardware design exists, but that is not an assembled prototype. Never imply that an intended result is an achieved result.

**Literature honesty:** the six citations below are transcribed from your submitted slides. Publisher and bibliographic API access was blocked during preparation. Paper-specific summaries therefore distinguish what the slide explicitly says from interpretation of the cited title. Full texts, author lists, experimental settings, and numerical results have not been independently verified here. Do not memorize invented accuracies or claim to have read a paper that you have not read.

## How to study tonight

- First 30 minutes: sections 1–3. Learn the opening, current status, slide explanations, and seven essential distinctions.
- Next 45 minutes: sections 4 and 6. Understand the light path, five main equations, and why each proposed component exists. Section 5 is optional simulation background; do not prioritize its figure-specific numbers for this presentation.
- Next 35 minutes: section 7. Learn what each literature reference contributes and what it does not establish.
- Next 35 minutes: sections 8–10. Learn AI, validation, drawbacks, applications, and defensible originality.
- Next 45 minutes: section 12. Practise the viva questions aloud; prioritize questions marked CORE.
- Final 20 minutes: sections 11 and 14. Rehearse your seven-slide explanation and rapid revision sheet. Section 13 is optional calculation practice. Then sleep; recall benefits more from rest than another unstructured read-through.

# 1. Your project in plain language

For every answer use: **direct answer → physical reason → project-specific evidence → limitation or next test**. Usually stop after 30–60 seconds and let the examiner choose the follow-up.

## 1.1 The problem and proposed solution

Transparent plastic may look normal under ordinary illumination while containing locked-in manufacturing stress or stress caused by applied forces. In a suitable transparent photoelastic material, stress changes the way two perpendicular components of polarized light propagate. A second polarizing filter converts that change into a visible intensity pattern. POLARIS proposes to capture these patterns reproducibly with a motorized analyzer and camera, process them, and eventually investigate whether validated machine learning can help flag defined anomalies.

The immediate engineering problem is therefore **reliable polarization-dependent image acquisition and interpretation**. Detecting every hidden defect, measuring every stress component, and certifying a part as safe are substantially harder tasks; they are not automatic consequences of seeing fringes.

## 1.2 A 90-second opening you can actually say

“Our project, POLARIS, proposes a low-cost polarimetric inspection setup for transparent photoelastic materials, initially clear polymer specimens. Ordinary images may not reveal internal stress. Stress-induced birefringence changes the polarization of transmitted light, and an analyzer converts that change into a measurable image.

“Our proposed setup uses a stable LED source, a fixed linear polarizer, the specimen, a motorized linear analyzer, and a USB camera. An Arduino controls analyzer rotation, while a laptop captures and processes the images. A load cell is an optional addition for recording the applied force during controlled tests.

“At our present documented stage, we have a physics-based simulation, finite-element stress calculations, synthetic optical images, and a proposed wiring design. Experimental acquisition and calibration are the next milestones. We also propose AI-assisted anomaly analysis, but we are not claiming a trained or validated defect classifier yet.

“Our intended contribution is an accessible, automated student-scale integration, with explicit calibration and uncertainty checks. Photoelasticity itself is established; our work is an engineering implementation and evaluation of this approach.”

## 1.3 The seven distinctions that prevent most viva mistakes

1. **Stress versus defect:** stress is a mechanical state; a defect is a structural or material nonconformity. A stressed specimen is not necessarily defective, and a defect need not generate a detectable stress pattern.
2. **Image brightness versus stress:** intensity depends on stress difference, principal-axis orientation, wavelength, thickness, analyzer angle, and camera response. Bright does not always mean high stress.
3. **Principal stress difference versus complete stress:** the optical model concerns Δσ = σ1 − σ2. It does not directly provide σ1 and σ2 separately or the complete three-dimensional stress tensor.
4. **Simulation versus experiment:** synthetic images show what a chosen model predicts. They do not demonstrate measured material properties or a working physical instrument.
5. **Physics inversion versus AI:** the implemented inverse calculation is a numerical model fit. It is not a trained CNN.
6. **Integration novelty versus new physics:** assembling and validating a useful accessible workflow can be valuable without inventing photoelasticity or proving a world-first system.
7. **Planned output versus validated output:** stress maps, defect localization, and pass/fail are objectives. Each requires its own measurements, labels, thresholds, and validation.

## 1.4 Current evidence you can defend

**Completed in the repository:** an executable simulation notebook; analytical Kirsch stresses; a native finite-plate, plane-stress finite-element solver; stress-to-polarization forward calculations; analyzer-angle and wavelength examples; an interactive application; calibration-fitting utilities using example synthetic data; a constrained inverse demonstration; numerical checks; corrected scientific figures; and proposed hardware connection diagrams.

**Still proposed or unverified physically:** purchased-part selection and assembly; motor-control/camera-acquisition firmware integration; optical alignment; specimen-specific material calibration; real-camera calibration; experimental stress measurements; a physical labelled dataset; trained ML performance; reliable defect localization; and production pass/fail certification.

The earlier numerical audit reported 31 passing software tests. Say “numerically checked under stated assumptions,” not “experimentally validated because the tests passed.” The hardware picture is a design proposal, not a photograph of your assembled instrument.

# 2. Slide-by-slide speaking notes

## Slide 1 — Title and scope

The title is “Development of an AI-Assisted Polarimetric Optoelectronic System for Non-Destructive Detection of Hidden Stress and Defects in Transparent Materials.” Explain **development** as a staged project, **polarimetric** as measuring polarization-dependent light, **optoelectronic** as optical interaction followed by electronic sensing, and **AI-assisted** as a proposed analysis layer rather than the source of the underlying physics.

Suggested explanation: “We are investigating whether a controlled, low-cost polarization imaging system can reveal stress-related optical variations in transparent polymer samples, and whether later data-driven analysis can help categorize defined anomalies.”

Likely follow-up: “Does your title mean you already detect defects?” Answer: “No. It states the project objective. Our completed evidence is currently simulation and design; reliable experimental defect detection is a later validation milestone.”

Do not invent an expansion for POLARIS. It is the project name unless your group has explicitly defined a backronym. Do not confuse it with the technical definition of a polariscope.

## Slide 2 — Six objectives

**Build:** deliver an aligned LED–polarizer–specimen–analyzer–camera setup with a stable mount and controlled background. Success is not simply buying the parts; it includes repeatable images of an unchanged specimen.

**Measure:** record intensity changes at known analyzer angles with fixed exposure, gain, and white balance. At the first stage the measurement is optical intensity, not directly stress in MPa.

**Automate:** home the analyzer, move to selected angles, wait for settling, discard stale frames, and capture tagged images. Rotation does not apply force to the specimen.

**Analyze:** compute normalized images, angular modulation, and spatial pattern features. Quantitative stress needs additional calibration and identifiability checks.

**Classify:** define the labels before choosing an algorithm. “Normal,” “stressed,” and “abnormal” overlap physically. A better initial study may use separate labels for load state and defect state, or narrowly specified mutually exclusive experimental conditions.

**Visualize:** show the image or estimated stress/anomaly field together with a validity mask, scale, acquisition settings, and confidence information where justified. A colored map alone is not a calibrated measurement.

Likely question: “Which objective is already complete?” Answer with the status in section 1.4. Simulation supports design and analysis but does not complete the physical build, measurement, or experimental AI objectives.

## Slide 3 — Literature survey

Explain the slide as four themes: established photoelastic physics; digital image analysis of stress patterns; polarization cues for transparent-object segmentation; and polarization-assisted learning for inspection tasks. The last two motivate possible image features and analysis methods, but they do not prove stress measurement or universal defect detection in your material.

Suggested transition: “The literature motivates the building blocks. Our practical question is whether we can integrate them affordably and validate a narrow transparent-polymer inspection task.” Section 7 gives the paper-by-paper preparation.

## Slide 4 — Proposed methodology

Walk through the light path physically: source → fixed polarizer → specimen → rotating analyzer → camera → laptop processing. The Arduino controls motor and illumination; the USB camera sends frames directly to the laptop.

Resolve the vague alternatives verbally: “Although the slide says LED/laser and glass/plastic, our proposed first prototype uses a diffused white LED and a transparent photoelastic polymer. A laser introduces coherence, speckle, and additional alignment considerations. Glass is a future specimen class requiring its own sensitivity and calibration assessment.”

The lower boxes need qualification: “The CNN and stress/defect/pass-fail outputs are proposed later stages. A classifier does not automatically locate defects, and a color image is not automatically a calibrated stress map.” A localization model needs spatial labels or another specifically validated localization method.

## Slide 5 — Timeline

The submitted slide presents a broad August-to-March development sequence: literature review; hardware design/build; software; AI model development; testing; report. The bars overlap and do not specify precise dates or completion percentages. Explain the dependencies rather than asserting exact dates that are absent.

Say: “We will use stage gates: first repeatable acquisition, then calibration and baseline analysis, then sufficiently documented experimental data, then any trained model and held-out testing. Literature review and testing continue throughout.”

Testing must not wait until the end. Check wiring and power first, then motor motion, then optical images, then mechanical/optical calibration, then algorithms. If delayed, prioritize a demonstrable calibrated acquisition workflow over an unsupported CNN claim. State who owns each task only according to your actual team allocation.

## Slide 6 — Selected references

There are six listed references. In the submitted PDF this page displays the slide number 8, despite being the sixth PDF page; this appears to be retained slide numbering, not evidence of missing experimental results. Be ready to identify which references concern polymers and which concern transparent-object perception or reflective metals.

Never use “a recent paper proved our whole system works.” Explain the narrower relevance of each reference. DOI publication years can differ from the final issue year; verify citation metadata before correcting a year solely from the DOI string.

## Slide 7 — Thank you / questions

Close with one achievement, one limitation, and one next test: “We have developed a model-based simulation and a concrete hardware design. Experimental calibration and defect learning remain future work. Our next test is repeatable angle-resolved imaging of a controlled polymer specimen under independently measured loads.”

# 3. Terminology and full names

| Term | Full name / meaning | What it means in this project |
| --- | --- | --- |
| NDT | Non-Destructive Testing | Inspection intended not to impair the specimen’s future usefulness; loading and gripping must still stay within safe limits. |
| LED | Light-Emitting Diode | Solid-state illumination; use a panel with current limiting, not a bare power LED directly on 12 V. |
| LASER | Light Amplification by Stimulated Emission of Radiation | An alternative source on the slide, not selected for the proposed V1. |
| PMMA | Poly(methyl methacrylate) | Acrylic; a candidate transparent polymer, with specimen-specific properties. |
| PC | Polycarbonate, or personal computer depending on context | Say “polycarbonate specimen” and “laptop” to avoid ambiguity. |
| RGB | Red, Green, Blue | Camera channels or synthetic channels; a camera’s broad bands are not ideal monochromatic wavelengths. |
| UVC / USB | USB Video Class / Universal Serial Bus | Standard camera interface to the laptop. |
| MCU / GPIO | Microcontroller Unit / General-Purpose Input/Output | Arduino logic and control pins. |
| PWM | Pulse-Width Modulation | Duty-cycle switching; avoid illumination PWM during capture in the simple prototype. |
| MOSFET | Metal-Oxide-Semiconductor Field-Effect Transistor | Electronic LED switch; gate, drain, source are G, D, S. |
| ADC | Analog-to-Digital Converter | HX711 converts a small bridge signal to digital data. |
| PGA | Programmable-Gain Amplifier | HX711’s front-end amplification; gain is not the same thing as accuracy. |
| NC / NO / COM | Normally Closed / Normally Open / Common | Microswitch terminals; “normal” means mechanically unactuated. |
| NEMA | National Electrical Manufacturers Association | NEMA 17 identifies a nominal mounting/frame size, not a motor’s current or torque. |
| FEA / FEM | Finite-Element Analysis / Finite-Element Method | Numerical mechanics used for the finite plate. |
| CST | Constant-Strain Triangle | A three-node linear triangular finite element. |
| AI / ML / DL | Artificial Intelligence / Machine Learning / Deep Learning | Related categories; DL uses multilayer neural networks. |
| CNN | Convolutional Neural Network | A proposed image-learning model family; no trained defect CNN is presently demonstrated. |
| SVM | Support Vector Machine | A possible simpler classifier for engineered image features. |
| YOLO | You Only Look Once | An object-detection model family cited in a reference title, not the implemented POLARIS model. |
| ROI / SNR | Region of Interest / Signal-to-Noise Ratio | Selected specimen region and useful signal relative to noise. |
| RMSE / MAE | Root-Mean-Square Error / Mean Absolute Error | Regression-error metrics; RMSE penalizes large errors more strongly. |
| IoU | Intersection over Union | Spatial overlap metric for localization/segmentation. |
| QWP | Quarter-Wave Plate | Adds a quarter-cycle phase difference at its design wavelength; optional advanced optics, absent from the proposed basic circuit. |
| MPa / nm / rad | Megapascal / nanometre / radian | Stress, wavelength, and phase units. 1 MPa = 10⁶ Pa = 1 N/mm². |

Arduino Uno R3 is a board name and revision. ATmega328P, A4988, HX711, and FQP30N06L are device identifiers; do not manufacture “full forms” for their part numbers. GT2 in the proposed belt drive refers to the selected belt/tooth system; purchase matching 2 mm pitch pulleys and belt, rather than mixing tooth profiles.

# 4. Physics you must understand

## 4.1 Polarization, polarizer, and analyzer

Light is an electromagnetic wave. Polarization describes how its electric-field direction evolves. An ideal linear polarizer passes the component along its transmission axis. The first polarizer prepares a known state. The analyzer is another polarizer after the specimen; its name describes its measurement role, not a fundamentally different material.

For already linearly polarized light passing through an ideal analyzer at relative angle θ, Malus’s law is I = Iin cos²θ. This does not by itself describe a birefringent specimen between the filters. An ideal first polarizer transmits half the average intensity of unpolarized light; real filters also have losses. In our normalized optical equations I0 refers to intensity after the input polarizer.

Parallel axes (0°) transmit the clear-path input; crossed axes (90°) ideally extinguish it. Real filters have a finite extinction ratio, misalignment, stray light, camera offset, and scattering, so a real crossed image is not perfectly black.

## 4.2 Stress, strain, and principal stresses

Stress is internal force per area. Normal stress acts normal to a plane; shear stress acts along it. Strain measures deformation relative to initial dimensions and is dimensionless. Elastic modulus relates stress to strain in a specified regime. Young’s modulus E describes axial stiffness; Poisson’s ratio ν relates lateral contraction to axial extension in simple uniaxial loading.

For a 2D symmetric stress tensor with σx, σy, and τxy:

**σ1,2 = (σx + σy)/2 ± sqrt[((σx − σy)/2)² + τxy²]**

**Δσ = σ1 − σ2 = sqrt[(σx − σy)² + 4τxy²]**

**φ = 0.5 atan2(2τxy, σx − σy)**

Principal directions have zero in-plane shear stress. φ is the principal-axis angle relative to the x-polarization direction. When Δσ = 0, the principal direction is not uniquely defined. If only Δσ is measured, the mean stress (σ1 + σ2)/2 remains unknown: many stress states yield the same difference.

## 4.3 Birefringence and the stress-optic law

Birefringence means two orthogonal polarization components experience different refractive indices. Stress can induce this in initially isotropic transparent photoelastic materials. Molecular orientation, processing history, temperature, and material composition can also affect the optical response; a real specimen may already be birefringent before loading.

In the simplest calibrated linear stress-optic model:

**Δn = C Δσ**

Here C is the stress-optic coefficient, with units Pa⁻¹ if stress is in Pa. More generally signs and principal optical-axis conventions must be handled consistently; the project uses a nonnegative stress difference and an assumed positive coefficient. C is not Young’s modulus, is not universal across plastics, and may depend on wavelength and temperature.

Optical path difference is Γ = d Δn, measured in metres. Phase retardation is:

**δ = 2π Γ / λ = (2π/λ) C d Δσ**

δ is a phase delay, not a mechanical displacement. If stress and principal axes vary significantly through thickness, a simple uniform-retarder model may be inadequate. A transmitted measurement can mix information along the light path and generally does not locate a defect’s depth.

## 4.4 Why fringes appear

The input field splits into components along the specimen’s principal optical axes. They acquire different phases. Recombination at the analyzer produces an intensity depending on their relative phase and orientation. For ideal crossed linear polarizers:

**I / I0 = sin²(2φ) sin²(δ/2)**

Two independent reasons can make the image dark: alignment with a principal axis, where sin(2φ) = 0; or an integer-wave phase difference, where δ = 2πm. Low intensity can also result from genuinely low retardance. Therefore darkness does not uniquely mean zero stress.

Isochromatic fringes are associated with constant retardation, and with principal-stress difference under appropriate uniform material/thickness assumptions. Isoclinic patterns are associated with principal-axis alignment. A plane polariscope mixes orientation and retardation effects. An ideal circular polariscope uses suitable quarter-wave plates to remove the orientation factor from its isochromatic response, but it still has phase periodicity and calibration requirements.

Fringe order is N = δ/(2π) = C d Δσ / λ. A stress-fringe value fσ can be defined so Δσ = N fσ/d, with fσ = λ/C under compatible units. You cannot infer an arbitrary absolute fringe order from one wrapped intensity measurement without additional information.

## 4.5 Analyzer rotation: what it adds and what it cannot add

Changing the analyzer angle changes intensity even while the stress field remains fixed. Four useful angles are 0°, 45°, 90°, and 135°. Orthogonal analyzer intensities add to the same total intensity in the ideal lossless normalized model, before gamma rendering.

For linear-analyzer measurements, S0 = I0° + I90°, S1 = I0° − I90°, and S2 = I45° − I135°. Here the angle-labelled I0° is a measured analyzer image, not the earlier normalization symbol I0. Degree of linear polarization is sqrt(S1² + S2²)/S0 where S0 is nonzero; the linear polarization angle is 0.5 atan2(S2,S1).

These four measurements do **not** measure S3, the circular-polarization component. A rotating linear analyzer alone is not a complete Stokes polarimeter. Additional polarization preparation/analysis, such as appropriate QWP states, is required for a more complete measurement. Nor do four analyzer angles automatically resolve absolute phase, principal-axis ambiguity, and complete stress.

This is why a good answer is “more informative angular data and repeatability,” not “four images fully recover every stress component.” The present inverse demonstration separately assumes that φ is known from FEA.

## 4.6 White light, wavelengths, and camera response

The synthetic demonstration uses ideal channels at 630, 525, and 450 nm. A white LED and ordinary RGB camera instead integrate over broad spectral bands. A more realistic channel model is a wavelength integral of source spectrum × optical transmission × sensor sensitivity × the wavelength-dependent polarization response, followed by camera gain/offset and other processing.

Consequently, assigning exactly 630/525/450 nm to uncalibrated webcam RGB values is not quantitatively justified. Start with qualitative patterns; for quantitative work consider characterized narrow-band LEDs/filters or a calibrated spectral forward model. Even a narrow-band LED has nonzero bandwidth.

Gamma, auto-exposure, auto-white-balance, compression, clipping, and denoising can change pixel values. Lock settings, avoid saturation, characterize camera linearity, and use linearized intensities for fitting. PNG screenshots are suitable for presentation, not automatically suitable for quantitative inversion.

## 4.7 Limits of “hidden stress and defects”

Residual stress remains after external loads are removed; it may arise from moulding, cooling gradients, machining, or assembly. Applied stress arises from current loading. Initial and loaded images can be compared, but subtracting intensities is not equivalent to subtracting stresses because the optical relation is nonlinear and axis orientation can change.

A hole or crack can redistribute stress and produce a local optical signature. But scratches, thickness changes, illumination gradients, scattering, and inherent anisotropy may also change the image. The system must distinguish causes using controlled specimens and independent ground truth. Stress can be beneficial in some applications, such as intentionally compressive surface stress; “high stress” is not universally “bad.”

# 5. Optional backup: simulation and numerical examples

**Not part of your planned slide presentation.** You are not showing these figures. Read this section only if time permits or if you want preparation for questions about the completed software. Do not volunteer exact inverse-error statistics in an opening or methodology explanation. If asked what the software does, begin with a simple forward-model description and state its assumptions.

## 5.1 Why there is a hole in the specimen

A circular hole creates a recognizable stress concentration and has an analytical benchmark. The Kirsch solution describes a circular hole in an ideal infinite elastic plate under remote loading. Under uniaxial tension the hole-edge hoop stress has a maximum of three times the remote nominal stress. This factor of three is not universally exact for a finite-width plate, different loading, a crack, or nonlinear material behavior.

The finite-element model handles our finite rectangle and specified constraints. The geometry is still intentionally simple: one centred circular hole, homogeneous isotropic material, linear elasticity, and small strain. The hole is a known geometric feature used to test the physics, not proof that an AI system discovered an unknown defect.

## 5.2 FEA in enough detail for a mechanics examiner

The mesh divides the plate into three-node triangular elements. Within each CST element displacement varies linearly, so strain is constant. For plane stress, the constitutive matrix uses E and ν to relate in-plane stress to strain. Each element stiffness is Ke = d A Bᵀ D B. Element matrices are assembled into the global system K u = f; restraints remove rigid-body motion; the solution gives displacements, then strains and stresses.

Plane stress approximates a thin plate with negligible out-of-plane stress components away from local disturbances. It is not the same as plane strain, which constrains out-of-plane strain. Thickness and geometry determine whether the approximation is reasonable; local grips and three-dimensional effects can violate it.

Default constraints are ux = 0 along the left edge, with uy = 0 at the left middle node to remove rigid translation. Uniform right-edge traction gives the requested total load. The hole and top/bottom edges are traction-free. This roller-type model allows transverse contraction and differs from rigid clamping.

Stress changes rapidly near the hole, so the mesh is denser there. More plotted pixels do not refine the mechanical mesh. Recovered nodal/grid stresses are smoothed/interpolated from element stresses; their maxima need not equal the unsmoothed element maximum.

Checks include force balance, a constant-strain patch check, an unperforated tension benchmark, load scaling, and mesh refinement. These support numerical consistency, but independent perforated-plate solver comparison and experiments remain useful validation steps. This is a native Python solver, not ANSYS output.

## 5.3 Parameters and calculations worth memorizing

| Quantity | Demonstration value | Qualification |
| --- | --- | --- |
| Plate length × width × thickness | 100 × 40 × 5 mm | Illustrative simulated geometry. |
| Hole radius / diameter | 5 mm / 10 mm | One central circular hole. |
| Load, main forward figures | 1000 N | A simulation input, not a command to load the real prototype. |
| Young’s modulus / Poisson ratio | 3000 MPa / 0.35 | Assumed material values, not measured specimen properties. |
| Stress-optic coefficient C | 3 × 10⁻¹² Pa⁻¹ | Illustrative, requires material/wavelength calibration. |
| Optical channel wavelengths | 630 / 525 / 450 nm | Ideal monochromatic model channels. |
| Display gamma | 0.65 | Rendering choice; not included in stored linear-intensity arrays. |

**Nominal gross stress:** A = 40 × 5 = 200 mm². At 1000 N, σnom = 1000/200 = 5 N/mm² = 5 MPa. The ideal infinite-plate benchmark predicts a 15 MPa maximum hoop stress. The finite-plate calculation is not required to match this exactly.

**Net-section distinction:** through a 10 mm hole, the remaining nominal section is (40 − 10) × 5 = 150 mm², giving 6.67 MPa average net-section stress. Never mix gross- and net-section definitions when quoting stress-concentration factors.

**Retardation example:** at Δσ = 10 MPa, d = 0.005 m, C = 3 × 10⁻¹² Pa⁻¹, Δn = 3 × 10⁻⁵ and Γ = 150 nm. At λ = 525 nm, δ ≈ 1.795 rad and N ≈ 0.286. If φ = 45° and the analyzer is crossed, I/I0 ≈ sin²(0.8976) ≈ 0.611. If φ = 0°, the same stress difference gives zero ideal crossed intensity.

**One fringe period in stress:** λ/(Cd) ≈ 35 MPa at 525 nm for the assumed C and d. Because intensity contains a sine squared, multiple stresses can yield similar measurements; multiple wavelengths help but do not eliminate all ambiguities under noise.

## 5.4 What to say about each of your four figures

**Figure 1 — Analyzer rotation:** one fixed stress field, four analyzer orientations. The changing brightness is optical modulation, not four different loads. For an ideal clear hole the linear normalized intensities are 1, 0.5, 0, 0.5. Display gamma changes the visible middle gray to about 0.637. Do not use displayed brightness as a direct stress scale.

**Figure 2 — Mesh and deformation:** the denser mesh resolves the region near the hole. The shape deformation is magnified 100 times so it can be seen; the color scale reports actual displacement. The default maximum displacement is about 0.1775 mm. It is not a 17.75 mm measured motion.

**Figure 3 — Stress and optics:** this is the forward chain from mechanics to principal stress difference, phase retardation, and synthetic intensity. At 1000 N the sampled grid maximum Δσ is approximately 15.33 MPa, while the default unsmoothed element maximum is approximately 15.71 MPa. The maximum 525 nm grid retardation is about 2.75 rad. Different recovery/sampling operations explain the different maxima.

**Figure 4 — Constrained inverse example:** this is a different, 1400 N synthetic case. The inverse is supplied the exact FEA principal orientation. It fits three ideal channels with known thickness and coefficient. This is a deliberately limited test of model consistency, not experimental recovery or a learned AI model.

For the audited 101 × 41 reconstruction figure: 1395 of 4072 material pixels were accepted (34.26%). Accepted-pixel RMSE was about 1.421 MPa, median absolute error 0.294 MPa, maximum absolute error 19.31 MPa, with six accepted errors exceeding 5 MPa. The approximate local 95% intervals covered the truth for 95.84% of accepted pixels in that single synthetic realization.

Interpretation: the reconstruction is incomplete, some accepted results are wrong, and local uncertainty intervals omit calibration/model uncertainty. White or missing regions mean unresolved or outside material, not zero stress. Do not call 95.84% coverage “95.84% accuracy.” Other validation grids in the repository have different counts; do not attach their metrics to this figure.

## 5.5 What the earlier audit corrected

The plots were numerical outputs, not generative artwork. The audit nevertheless found real issues: interpolation masks left small artificial gaps at outer boundaries; image coordinates had half-pixel alignment errors; and a reconstruction color scale hid high outliers by saturation. These were corrected, and figure descriptions now disclose load, gamma, accepted coverage, and inverse assumptions.

Use the audited repository figures. If asked whether they are “100% correct,” say: “They are consistent with the tested model and corrected plotting procedures, but the model is idealized and the inverse is incomplete. We do not claim exact physical predictions without experiments.”

# 6. Components, specifications, and connections

## 6.1 What is on the slide versus what we selected later

The submitted PDF names source, polarizer, sample, analyzer, sensor, and AI analysis at block level. It does not specify Uno, A4988, HX711, or a precise camera model. The following parts are **proposed engineering choices developed after the slide**, not components claimed to have already been purchased or specified in the submitted deck.

The general optical path is: diffused LED → fixed LINEAR polarizer P1 → polymer specimen → rotating LINEAR analyzer P2 → camera lens/sensor. Use transmission geometry. The specimen has a separate manual fixture. The motor rotates P2, not the specimen and not the load mechanism.

## 6.2 Arduino Uno R3 and laptop

The Uno R3 is based on the ATmega328P microcontroller: nominal 5 V logic, 16 MHz clock, 32 KB flash, 2 KB SRAM, 1 KB EEPROM, 14 digital I/O pins including six PWM-capable pins, and six analogue inputs. Some flash is occupied by the bootloader. These are standard board specifications; verify a purchased compatible board’s actual configuration.

Its role is deterministic low-rate control: STEP/DIR pulses, driver enable, homing, LED switching, and optional HX711 readout. It does not have the memory or conventional interface to run this RGB-image CNN or ingest an ordinary USB webcam. The laptop is the USB host, image processor, and future ML platform. A Raspberry Pi could later replace it after confirming camera compatibility and performance.

The Uno is powered from laptop USB. The external 12 V supply is for motor/LED loads. Join grounds for a common signal reference; never connect 12 V to Uno 5V or GPIO. GPIO drives logic, not motor coils or the LED panel’s load current. Keep D0/D1 available for USB serial in this design.

## 6.3 Camera and illumination

**Camera requirement:** a UVC USB camera with controllable exposure, gain, and white balance, fixed mounting, adequate field of view, and a lens that resolves the desired feature. An exact camera model/resolution has not been selected; do not invent one in the viva. Prefer a camera with documented linear/raw output or characterize its processing if quantitative measurements are required.

Spatial sampling depends on object-plane field of view and pixel count. Example: 100 mm spanning 1920 pixels corresponds to about 0.052 mm/pixel. This is only sampling, not verified defect resolution: lens blur, focus, contrast, aberrations, noise, and the number of pixels per feature matter.

**LED requirement:** a uniform diffused 12 V white panel with built-in current limiting, drawing no more than 0.5 A in the proposed design. At the upper limit this is 6 W electrical input, not 6 W measured optical power. Warm it up and control ambient illumination. Use DC on/off, not PWM, during exposure to avoid rolling-shutter bands or timing-dependent intensity changes.

LED rather than laser is a practical first choice: inexpensive area illumination, easier diffusion, and less coherent speckle. A laser is not inherently more quantitative; it introduces different measurement problems. A laser is not part of the proposed V1 circuit.

## 6.4 Polarizers, sample, and mechanical alignment

Use two linear polarizing films/filters with clear aperture covering the optical beam, adequate extinction, and useful visible-band transmission. Photographic circular/CPL filters are not equivalent drop-in replacements. Align P1 as the reference 0° axis; define P2 angles relative to P1, not relative to the laboratory table.

Start with a transparent, reasonably uniform polymer coupon. PMMA and polycarbonate are candidate classes, not interchangeable calibrated materials. Actual batch, thickness, manufacturing stress, surface condition, elastic constants, and stress-optic response must be measured or independently characterized.

Mounts must not unintentionally bend or squeeze the sample in the viewing area. Keep camera, light, and specimen fixed while only P2 rotates. Positioning P2 near the camera may reduce required filter area, but check vignetting, beam coverage, and alignment. An 80-tooth pulley pitch circumference with a 2 mm pitch is 160 mm, giving a pitch diameter of about 50.9 mm; clear aperture is smaller and depends on the mechanical design.

## 6.5 NEMA 17 stepper, A4988 driver, and belt

NEMA 17 describes a roughly 42 mm square mounting frame. It does not specify a universal torque, step angle, rated current, coil resistance, or speed. The proposal assumes a four-wire bipolar motor with 200 full steps/revolution (1.8° per full step), rated for at least 0.60 A/phase. Select sufficient torque for the analyzer’s inertia and friction; a torque requirement has not yet been experimentally measured.

The A4988 is a chopper-current-regulated bipolar stepper driver. The IC supports a motor-supply range commonly specified as 8–35 V and logic supply around 3–5.5 V; the selected 12 V motor and 5 V logic supplies are within that range. Carrier layout, cooling, current sense resistors, and current capacity must be checked. “Up to 2 A” advertising is not a guarantee of sustainable uncooled carrier current.

STEP advances the microstep translator; DIR selects direction; ENABLE is active low. RESET and SLEEP are held high in this design. MS1/MS2/MS3 all high selects 1/16 stepping. Keep STEP and DIR low at startup with pull-downs; an ENABLE pull-up makes the initial state disabled.

Initial proposed current limit is ITRIP = 0.60 A/phase, without exceeding the actual motor rating. For the A4988, VREF = 8 ITRIP Rs. If Rs = 0.068 Ω, VREF ≈ 0.326 V; if Rs = 0.10 Ω, VREF ≈ 0.480 V. Read the actual carrier resistor value; do not turn the potentiometer blindly or equate supply current with phase current.

Connect one coil to 1A/1B and the other to 2A/2B. Identify coil pairs by resistance/continuity with power off; motor lead colors are not standardized. Mixing coils causes vibration, missed motion, or malfunction. Do not connect/disconnect motor leads while the driver is powered.

With a 20T motor pulley and an 80T analyzer ring, reduction is 4:1. Commands per analyzer revolution = 200 × 16 × 4 = 12,800. Commands per degree ≈ 35.556; one command increment is 0.028125°. Absolute targets for 0°, 45°, 90°, 135° are 0, 1600, 3200, and 4800 steps from a calibrated zero. This is commanded resolution, not demonstrated angular accuracy. Microstep nonlinearity, belt compliance, backlash, missed steps, and homing repeatability remain errors.

## 6.6 Homing microswitch

A normally closed microswitch provides a mechanical reference on the analyzer ring. Connect COM to ground, NC to D7, with a 4.7 kΩ pull-up to 5 V and a 100 nF filter capacitor to ground. Away from the home index the closed contact reads low; at the index it opens and reads high. A broken wire also reads high, so require a back-off/release transition, debounce, travel/time limits, and a fault response.

The home switch supplies a reference, not continuous angular feedback. Optical zero must be calibrated separately: use the actual parallel/crossed transmission relation. A future encoder would directly measure angle and help detect missed motion.

## 6.7 MOSFET, resistors, and capacitors

The FQP30N06L is a logic-level N-channel MOSFET used as a low-side LED switch. With the TO-220 marked face toward you, the proposed pin convention is 1 gate, 2 drain/tab, 3 source; confirm the manufacturer package drawing when buying. Gate is driven from D9 through 100 Ω; a 10 kΩ gate-to-ground resistor holds it off during startup. LED negative goes to drain, source to ground, and LED positive to switched 12 V.

“Logic level” concerns useful low on-resistance at a specified gate voltage. Threshold voltage only indicates the onset of conduction at a small test current; it does not mean the transistor is fully on. The resistor limits brief gate-charging current and can reduce ringing. The pull-down prevents a floating gate.

Use a 100 µF, 35 V electrolytic close to A4988 VMOT/ground, positive to VMOT. It provides local energy storage and helps limit supply transients. A 100 nF ceramic decouples VDD/ground. The capacitor voltage rating is a maximum working rating, not the voltage it produces. Reversed electrolytic polarity is incorrect.

External 10 kΩ resistors pull ENABLE high and STEP/DIR low. At 5 V, a 10 kΩ resistor draws 0.5 mA when the opposite state is driven. The 4.7 kΩ home pull-up draws approximately 1.06 mA while the switch is closed. The nominal 4.7 kΩ × 100 nF time constant is 0.47 ms; software debounce is still needed.

## 6.8 Optional load cell and HX711

A strain-gauge load cell converts elastic deformation into small resistance changes, usually connected as a Wheatstone bridge. Excitation powers the bridge; its differential output is often specified in mV/V at rated load. The HX711 is a nominal 24-bit ADC with a programmable-gain front end designed for bridge measurements. Typical supported sample rates are 10 or 80 samples/s, depending on module configuration; nominal 24-bit code width is not 24-bit effective force accuracy.

The proposed generic module uses 5 V VCC and common ground; DT goes to D5 and SCK to D6. Match load-cell excitation E+/E− and signal A+/A− to the actual module labels. Leave unused channel B unconnected according to module documentation. Do not infer electrical roles from wire colors.

Choose a full-bridge load cell rated for the fixture; 2 kN is an example, not a purchased component or approved working load. Tare the unloaded system, apply known traceable forces, fit and check calibration, repeat loading/unloading, and assess hysteresis, creep, and mounting effects. A 2 mV/V cell excited at 5 V would produce about 10 mV differential at its rated load; this is an example calculation, not our measured sensor sensitivity.

A load cell measures total applied force. It does not directly give local stress near a hole, nor residual stress in an unloaded specimen. For a uniform uniaxial calibration coupon, F/A can establish a reference stress under appropriate assumptions; a nonuniform field needs additional mechanics and validation.

## 6.9 Power and exact pin map

Use an enclosed isolated regulated 12 V / 3 A adapter, a 2 A inline fuse, and a switch rated for the DC load. This gives 36 W nameplate capacity; it does not mean the circuit always consumes 36 W. The 0.60 A motor phase setting is not simply 1.20 A at the 12 V supply because the chopper driver converts voltage/current and recirculates coil current. Confirm real supply demand and heating experimentally.

Route motor/LED return currents directly to the external supply ground. Join the Uno signal ground there or through a sensible common-ground arrangement, minimizing high-current paths through sensitive HX711 wiring. Keep bridge leads short/twisted where practical. Do not drive power loads through GPIO or rely on loose high-current breadboard contacts.

| Uno / component terminal | Connect to | Purpose |
| --- | --- | --- |
| Uno USB-B | Laptop USB | Board power and serial commands. |
| Camera USB | Separate laptop USB port / adequate powered hub | Camera data and power; not Uno GPIO. |
| D2 | A4988 STEP | Motion pulses. |
| D3 | A4988 DIR | Direction. |
| D4 | A4988 ENABLE | Low enables motor output; external 10 kΩ pull-up. |
| D5 | HX711 DT | Optional force data input. |
| D6 | HX711 SCK | Optional force clock output. |
| D7 | Home switch NC | Pull-up and filter described above. |
| D9 | 100 Ω → MOSFET gate | LED on/off. |
| Uno 5V | A4988 VDD; MS1/2/3; RESET/SLEEP; HX711 VCC; pull-ups | Logic power only. |
| Common ground | Uno GND; both A4988 GNDs; adapter negative; MOSFET source; HX711 GND; switch COM | Shared reference and correctly routed returns. |
| Switched +12 V | A4988 VMOT; LED positive | Motor and illumination power. |

## 6.10 Intended acquisition sequence

1. Boot with motor disabled, STEP low, and LED off. Check the switch state and establish communication.
2. Home slowly, verify switch opening and release on back-off, and apply the calibrated optical-zero offset.
3. Warm the LED, lock camera settings, focus, check saturation, and capture dark/flat references.
4. Move to each target angle using a consistent approach direction; report motion completion, then allow mechanical settling. An initial 300–500 ms wait is a starting setting to test, not a measured requirement.
5. Discard old buffered frames; capture multiple fresh images with angle, exposure, load, timestamp, sample ID, and calibration ID.
6. Check image quality and repeatability before interpretation. When the specimen moves or load changes during a sequence, four frames may no longer represent one mechanical state.

The protocol is proposed; do not claim synchronized hardware firmware already exists solely because the wiring drawing includes these connections.

# 7. Literature survey: explain each reference accurately

## 7.1 How to answer a paper question

For each paper state: problem → measurement modality → general method → what it contributes to POLARIS → what it does not prove. If asked for architecture, dataset size, accuracy, material coefficient, or an experimental parameter absent from your reading, say: “I have not verified that detail; I would need to check the paper. Its relevance to our design is …”

A reference title supports a research topic; it does not establish its precise results. The following summaries deliberately avoid unverified numerical claims.

## Reference 1 — Wang et al. (2023), polycarbonate goggles

**Slide citation:** “Qualitative characterization of residual stress of injection molded polycarbonate goggles based on photoelasticity and digital image processing technique.” Frontiers in Materials, 10, 1242721. The publisher article route used for checking was https://www.frontiersin.org/journals/materials/articles/10.3389/fmats.2023.1242721/full ; full text was not accessible here.

**What your slide explicitly reports:** photoelasticity and digital image processing were combined for residual-stress quality assessment of injection-moulded polycarbonate goggles, with image features linked to simulated stress.

**Why this is physically plausible:** moulding can leave nonuniform cooling and molecular orientation, leading to residual optical/mechanical anisotropy. Polarization images can reveal patterns not obvious in ordinary images. Digital features can make comparisons more repeatable than purely visual judgment.

**What to say:** “This is the most directly relevant cited application for our initial transparent-polymer scope. It motivates using photoelastic image features for residual-stress assessment.”

**Limit:** the word “qualitative” matters. Do not turn an image-feature/stress association into a claim of universal absolute stress measurement. Goggles also have curvature and thickness variation; transfer to our flat plate requires its own geometry and calibration treatment. Do not assume the paper used a CNN unless verified.

**Likely cross-question:** “Are image features a direct stress measurement?” Answer: “They can be indicators under controlled conditions, but the relation depends on thickness, optics, material, orientation, and image processing. A quantitative measurement needs calibrated modelling and independent validation.”

## Reference 2 — Verma, Torgal, and Agarwal (listed as 2024)

**Slide citation:** “Experimental stress analysis on polycarbonate material using photoelasticity.” Materials Today: Proceedings. DOI: https://doi.org/10.1016/j.matpr.2023.08.270 .

**What can safely be taken from the cited title:** the work concerns experimental photoelastic stress analysis of polycarbonate. The slide gives no sample geometry, loading arrangement, material coefficient, or numerical results; none is asserted here.

**Relevance:** it motivates experimentally testing a suitable transparent polymer and emphasizes that the optical response must be tied to actual mechanics. It is closer to our physical specimen/load problem than a general transparent-object segmentation paper.

**What to say:** “This reference supports our choice to investigate photoelastic polymer specimens experimentally. We still need to determine the properties and optical response of our own batch rather than copy a coefficient without checking conditions.”

**Likely cross-question:** “Why does a 2024 reference have 2023 in the DOI?” Answer: “The DOI string may reflect an earlier publication/registration stage than the final issue date. I would verify the publisher metadata rather than infer an error from the DOI alone.” The complete bibliographic metadata remains to be checked.

## Reference 3 — Yu et al. (2024), transparent-object segmentation

**Slide citation:** “Transparent objects segmentation based on polarization imaging and deep learning.” Optics Communications, 555, 130246. DOI: https://doi.org/10.1016/j.optcom.2023.130246 .

**What your slide reports:** polarization imaging and deep learning were used for transparent-object segmentation; polarization cues can supply information that ordinary RGB images may miss.

**Explain segmentation:** assign a category to pixels, such as object versus background. Transparent objects are difficult for ordinary appearance-based methods because background texture is visible through them, boundaries can be weak, and reflections vary. Polarization can provide additional contrast or material/geometry cues.

**Relevance:** suggests that polarization-dependent features could improve specimen masking or support a later image-analysis pipeline. It motivates testing whether angle-resolved inputs add information beyond RGB.

**Limit:** finding a transparent object’s silhouette is not measuring internal principal stress, detecting a crack, or assigning a safety rating. Do not cite segmentation performance as defect-detection or MPa accuracy. Architecture, dataset, and performance numbers were not verified here.

**Likely cross-question:** “How does segmentation help your project?” Answer: “It can isolate the specimen from background so analysis is performed on a meaningful ROI. That is an upstream processing aid; stress inference still requires separate physics and validation.”

## Reference 4 — Li et al. (2025), porosity in reflective metal parts

**Slide citation:** “Automated Detection of Micro-Scale Porosity Defects in Reflective Metal Parts via Deep Learning and Polarization Imaging.” Nanomaterials, 15(11), 795. Listed article route: https://www.mdpi.com/2079-4991/15/11/795 .

**What the title supports:** an application of polarization imaging and deep learning to a specifically named defect type in reflective metal parts. The provided slide contains no independently verified minimum defect size, learning architecture, dataset, or accuracy.

**Relevance:** methodological motivation for combining polarization-dependent appearance with labelled learning for a narrowly defined inspection task. It may help frame an experimental comparison against ordinary intensity images.

**Critical difference:** opaque reflective-metal inspection uses reflected-light effects and surface appearance, whereas our basic photoelastic arrangement uses transmission through a transparent specimen. Similar use of “polarization” does not imply the same forward physics or transferable thresholds.

**Likely cross-question:** “Does this prove you can inspect metals?” Answer: “No. A reflection-mode redesign and a separate validation study would be needed. We cite it as an example of polarization-assisted inspection, not as proof that our transmission system measures metal stress.”

## Reference 5 — Fan et al. (2025), intensity/spectral/polarization fusion

**Slide citation:** “Joint intensity-spectral polarization hierarchical fusion guided efficient transparent object detection.” Optics and Laser Technology. DOI: https://doi.org/10.1016/j.optlastec.2025.113429 .

**What can safely be inferred from the title:** the work addresses transparent-object detection using a fusion of multiple optical information types. “Hierarchical fusion” suggests combining information at more than one representation level, but the actual mechanism must be checked in the full paper; it is not established by the title alone.

**Relevance:** motivates testing whether intensity plus polarization-derived features outperform intensity alone. This should be an ablation experiment, not an assumption that more channels always improve results.

**Limit:** our V1 does not contain a spectral imager, and three broad webcam channels are not the same as a characterized spectral-polarization system. Transparent-object detection also differs from internal stress reconstruction. Do not promise to reproduce this paper’s architecture without confirming its sensors and data requirements.

**Likely cross-question:** “Why not use all those modalities?” Answer: “Additional modalities may help, but they increase cost, calibration burden, alignment requirements, and data demand. Our first prototype tests a simpler polarization acquisition setup before adding complexity.”

## Reference 6 — Reflective surfaces with polarization and modified YOLO (2025)

**Slide citation:** “Highly reflective metal industrial parts surface detection with polarization vision and modified YOLO.” Digital Signal Processing. DOI: https://doi.org/10.1016/j.dsp.2025.105238 . Your slide does not list authors; retrieve the full publisher citation before a final report submission.

**What the title supports:** reflection-based surface inspection and a modified object detector. YOLO is a model family; the word “modified” does not identify the exact change. Do not invent an attention module, backbone, training set, or improvement percentage.

**Relevance:** shows why polarization-assisted image contrast can be considered alongside a detection pipeline. It may motivate a future localization baseline if bounding-box ground truth is available.

**Limit:** surface detection in highly reflective metal is a different material and optical regime. A standard bounding-box detector does not automatically deliver pixel-level segmentation or stress in MPa. For thin cracks, a segmentation approach might ultimately be more appropriate, but that remains a task-specific design decision.

## 7.2 Comparison and defensible research gap

| Reference group | Direct contribution to our reasoning | What must not be claimed |
| --- | --- | --- |
| Wang / Verma | Transparent polymer photoelasticity and experimental/image-analysis motivation. | A universal uncalibrated stress coefficient or validated POLARIS performance. |
| Yu / Fan | Polarization information for transparent-object perception and possible ROI/features. | Internal stress recovery merely because objects were detected/segmented. |
| Li / reflective-metal YOLO paper | Polarization-assisted labelled inspection in another optical regime. | Transmission through opaque metal or direct cross-material generalization. |

Safe gap statement: “These references motivate a student-scale integration of motorized polarization acquisition, physics-based interpretation, and later anomaly analysis for a specified transparent-polymer task. Our proposed study is about accessibility, repeatability, and validation of that integration.”

Unsafe gap statement: “Nobody has combined polarization and AI before.” Your own references already indicate otherwise. Establishing a publication-level novelty claim needs a systematic search including phase-stepping photoelasticity, digital polariscopes, low-cost motorized systems, and photoelastic inverse learning. The current six references are not an exhaustive prior-art review.

Before presenting, open at least the abstract/conclusion of the references you plan to discuss in detail. Record actual sensor geometry, material, target task, experimental ground truth, and limitation. If inaccessible, be honest about the extent of your reading.

# 8. AI, image processing, and a credible development plan

## 8.1 Define the task before the network

Classification assigns a label to an image/specimen. Detection finds objects/regions, often as boxes. Segmentation assigns pixel labels. Regression predicts a continuous value such as Δσ. Anomaly detection flags deviation from a learned or defined reference. These require different ground truth and metrics.

The slide’s “normal, stressed and abnormal” classes are not inherently disjoint: a good part can be intentionally stressed; a defective unloaded part may show weak contrast. A more defensible protocol separates defect state from load state or specifies exact conditions, such as intact/known-notch coupons tested at prescribed loads. Cosmetic marks and structural flaws should not share one vague label without justification.

The initial non-AI baseline should be repeatable acquisition, specimen masking, normalized angle images, and a simple rule or classical model. Only then test whether learning adds measurable value.

## 8.2 A proposed processing pipeline

1. Assign independent specimen IDs and record material/batch, dimensions, load, angle, illumination, exposure, and session.
2. Reject blurred/saturated frames; subtract a measured dark background and use an appropriate flat-field correction. A typical correction resembles (I − Idark)/(Iflat − Idark), excluding near-zero denominators; record how normalization is defined.
3. Register frames only when justified, without altering the physical angular signal. Use a specimen/material mask to exclude clear holes and background where appropriate.
4. Extract intensity, angular modulation, texture, local gradients, or calibrated polarization features. Do not interpret edges from illumination or holder shadows as defects.
5. Compare an intensity-only baseline with angle-resolved features under identical train/test splits. This ablation tests whether polarization is actually useful.
6. If enough independent data exist, train a simple classifier first. A CNN is a candidate, not a requirement. Report failures and uncertainty rather than only successful examples.

## 8.3 Explain a CNN simply but accurately

A convolutional layer applies learned local filters across the image. Early filters can respond to edges or textures; later layers combine patterns into task-dependent features. Nonlinear activations such as ReLU allow nonlinear mappings. Pooling or strided convolutions may reduce spatial resolution; a classifier head produces class scores. A segmentation model preserves or reconstructs spatial detail to produce masks.

Training adjusts weights to reduce a loss on labelled examples, commonly with gradient-based optimization and backpropagation. Classification might use cross-entropy; segmentation can use cross-entropy and overlap-based losses; stress regression needs physically meaningful continuous targets. Hyperparameters are tuned using validation data, not the final held-out test set.

There is no confirmed POLARIS architecture, layer count, parameter count, dataset size, epoch count, training accuracy, or inference latency at the documented stage. If asked to propose one, say so explicitly: “I would first benchmark a compact transfer-learning classifier or a feature-based model, choosing segmentation only when spatial labels exist.”

## 8.4 Ground truth and data leakage

A simulator provides exact labels for its own assumed model, not for a physical specimen. A load cell provides force, not a complete local stress image. A known manufactured notch establishes that geometric feature, but does not establish detection of all natural defects. Local physical stress validation needs an independent suitable reference and uncertainty analysis.

Split by **specimen**, and where practical batch and acquisition session. Adjacent frames, repeated angles, and repeated loads of the same specimen must not leak between train and test sets in a way that lets the model recognize the specimen rather than generalize. An 80/20 image split is not enough if the images are correlated.

Augmentation also needs physics awareness: rotating an image can change the interpretation of polarization axes unless angle labels/features are transformed consistently. Arbitrary color jitter may destroy a stress-related optical signal. Synthetic-to-real transfer needs real held-out evaluation; matching the simulator does not solve the domain gap.

## 8.5 Metrics and pass/fail

For defect detection define the positive class first. Precision = TP/(TP+FP); recall/sensitivity = TP/(TP+FN); specificity = TN/(TN+FP); F1 is the harmonic mean of precision and recall. Accuracy can be misleading in an imbalanced dataset. Also report confusion matrices, per-class performance, uncertainty, and results on new specimens.

For localization use IoU/Dice or suitable detection metrics, and examine errors on small defects. For stress regression use MAE/RMSE in MPa, bias, calibration uncertainty, and spatial coverage. Reporting low error only on a small accepted subset without coverage is misleading.

A neural-network score is not automatically a calibrated probability. Choose thresholds using the application’s costs of false rejection and missed defects, then validate on held-out data. A pass/fail result requires an agreed acceptance criterion and traceable reference. Until then, label output as an inspection aid or anomaly indication, not certification of structural safety.

# 9. Calibration, validation, and experiments beyond the slides

## 9.1 A staged experiment you can propose tomorrow

**Stage A: empty optical path.** Capture analyzer sweeps without a specimen. Verify approximate Malus behavior, crossed leakage, LED stability, exposure repeatability, and no saturation. This checks the instrument, not stress sensitivity.

**Stage B: unloaded specimen.** Record baseline patterns and mounting repeatability. Baseline birefringence may reflect residual stress, material anisotropy, or thickness/optical variation; do not automatically label it defective.

**Stage C: controlled loading.** Use an independently calibrated force measurement and a suitable coupon/fixture, staying in the intended reversible regime. Repeat loading/unloading and measure hysteresis or time dependence. Assess whether acquisition time is short relative to creep/load drift.

**Stage D: material/camera calibration.** Establish thickness, optical zero, response linearity, and stress-optic behavior using an appropriate reference. If phase must be unwrapped, verify the unwrapping. Calibrating a model against its own synthetic output does not establish physical calibration.

**Stage E: known anomalies and controls.** Compare intact and specifically characterized specimens at matched loads, thickness, illumination, and processing. Randomize test order where feasible. Include nuisance changes such as remounting and session variation to reveal fragile algorithms.

**Stage F: independent validation.** Keep new specimens/batches held out. Report misses, false positives, unresolved areas, resolution limits, and uncertainty. Add learning only after the baseline measurement is stable.

## 9.2 Verification versus validation

Verification asks whether the equations and code have been implemented correctly: unit checks, benchmark solutions, conservation/force balance, numerical convergence. Validation asks whether the model adequately describes the physical system for its intended use. Calibration estimates model or instrument parameters from reference data. Testing the same data used to fit parameters is not independent validation.

Mesh convergence shows how a numerical result changes with refinement; it does not prove the material law is correct. A close camera fit to simulated images is not experimental truth. Confidence in a whole instrument comes from the combination of physics, calibration, independent evidence, and defined operating limits.

## 9.3 Important error sources and their consequences

| Error source | Consequence | Mitigation / test |
| --- | --- | --- |
| Unknown C or thickness | Wrong stress scale. | Measure thickness and calibrate material/spectral conditions. |
| Analyzer angle error/backlash | Intensity mismatch; poor repeatability. | Optical zero, same-direction approach, repeat cycles, possible encoder. |
| LED drift / ambient light | Apparent change mistaken for specimen response. | Warm-up, enclosure, reference monitoring, dark/flat checks. |
| Auto camera processing / clipping | Invalid quantitative intensity model. | Fixed controls, linearity testing, unsaturated images. |
| Broad spectral channels | Difference from ideal wavelength model. | Characterized spectral model or narrow-band acquisition. |
| Weak optical sensitivity / phase branches | Large uncertainty or wrong inverse solution. | Additional independent states/prior information; reject unresolved estimates. |
| Out-of-plane stress / varying axes through thickness | Simple 2D uniform-retarder model fails. | Restrict geometry or develop a more complete model. |
| Fixture stress / creep / vibration | Nonrepeatable field during capture. | Better mounts, controlled load timing, settling and repeatability tests. |
| Dataset leakage / bias | Overoptimistic AI performance. | Independent specimens/sessions, realistic controls, blinded test set. |

For Δσ = δλ/(2πCd), first-order relative uncertainty, away from problematic zero/branch regions, can be approximated by adding independent relative variances in δ, λ, C, and d. This is only a local approximation; correlated calibration errors and fringe-order mistakes require more careful treatment. Reducing camera noise alone cannot remove an incorrect stress-optic coefficient.

## 9.4 Resolution, accuracy, repeatability, sensitivity

Resolution is the smallest distinguishable increment under a specified definition; a command step or pixel pitch is only one contributor. Accuracy concerns closeness to the true/reference value. Precision is spread of repeated results; repeatability is precision under stated similar conditions. Sensitivity describes how much the measured signal changes for a change in the measurand. A highly repeatable biased instrument is still inaccurate.

Define performance before measuring it: angle repeatability in degrees, intensity repeatability at fixed settings, force error in newtons, stress error in MPa, accepted spatial fraction, and defect detection probability at a specified feature size/material/load. None of these experimental performance numbers has been established merely by drawing the circuit.

# 10. Benefits, drawbacks, applications, and originality

## 10.1 Benefits you can reasonably propose

- Full-field optical imaging can reveal spatial variation rather than only one sensor location, within the field of view and sensitivity limits.
- Polarization can add contrast to stress-related effects that ordinary intensity images miss.
- Motorized acquisition can improve consistency and reduce manual angle-setting effort if homing, settling, and alignment are verified.
- A laptop/USB-camera/microcontroller architecture is accessible for student development and allows transparent software inspection.
- Reusable simulations help understand expected trends, select experiments, and test algorithms before committing to hardware.
- A validated future analysis pipeline could aid repeatable screening, while maintaining human review and explicit uncertainty.

“Low-cost,” “faster,” and “more accurate” are design aims until compared with a named baseline using actual purchase costs and measured performance. Do not invent a total rupee budget; the camera, mounts, load fixture, and calibration equipment may dominate cost more than the Arduino.

## 10.2 Current drawbacks you should volunteer

The physical instrument is not yet experimentally demonstrated in the documented work. Quantitative calibration is absent. The inverse assumes known principal-axis orientation and only recovers a subset of synthetic pixels reliably. The simple optical model neglects real spectral response and several physical imperfections. A labelled experimental dataset and trained classifier are absent. A transmission design does not inspect opaque interiors or provide depth localization. Slow sequential acquisition is sensitive to movement and load changes. Material properties, geometry, and fixture conditions limit generalization.

These are not reasons to abandon the project. They define the next experiments and the scope of a defensible first prototype: **repeatable qualitative polarization imaging of specified transparent polymers, followed by calibrated measurements where supported**.

## 10.3 Where it might be useful—and where it is not yet suitable

Potential research/teaching applications include clear polymer coupons, moulded transparent parts, stress visualization around holes, assembly-induced stress studies, and comparative process-quality research. Extending to goggles, lenses, or complex mouldings requires handling curvature, thickness, surface coatings, and manufacturing anisotropy.

It is not currently a certified industrial acceptance tool, a universal crack detector, a replacement for all NDT, or a way to measure internal stress in opaque metals by transmission. Medical, aerospace, and safety-critical deployment would require substantially stronger qualification and application-specific standards.

## 10.4 Compare with alternatives without overselling

| Method | Main advantage | Difference from our proposal |
| --- | --- | --- |
| Ordinary RGB inspection | Simple, inexpensive appearance imaging. | May miss polarization-dependent stress cues; still an essential baseline. |
| Strain gauges | Local calibrated strain measurement. | Contact/local measurement; stress requires material/mechanical assumptions. |
| Digital Image Correlation | Full-field surface displacement/strain from texture tracking. | Usually needs trackable texture; measures surface kinematics rather than birefringence. |
| Ultrasonic testing | Can inspect many opaque materials and internal discontinuities. | Coupling, geometry, transducers, and interpretation differ; broader material applicability in many cases. |
| X-ray / CT | Internal structural imaging, potentially 3D. | Different contrast mechanism, cost and infrastructure; not a routine direct measurement of our optical stress difference. |
| Reflection polarization imaging | Useful for surface/reflection contrast, including opaque parts. | Requires a different optical arrangement and task-specific interpretation. |
| Digital photoelastic/polarimetric instruments | Established quantitative workflows under suitable conditions. | Our intended distinction is accessible integration and explicit evaluation, not invention of the method. |

## 10.5 What is unique in our work?

Say: “Our present contribution is a coherent student-scale workflow: analytical and finite-element mechanics, polarization-image simulation, an auditable inverse demonstration, and a concrete low-cost motorized hardware design. We propose to test its repeatability and usefulness for a defined transparent-polymer task.”

The repository’s uncertainty/validity masks and disclosure of failure regions are useful engineering features. They show an effort not to mistake every colored pixel for a valid measurement. They are not evidence that no prior instrument does this.

Future evidence of added value would include a reproducible bill of materials and cost, repeatable acquisition, calibration, performance against an intensity-only baseline, and independent specimen tests. A claim of worldwide research novelty or patentability needs a broader prior-art review.

# 11. Presentation plan — submitted slides only

## 11.1 A sensible five-minute structure

- 0:00–0:40: problem, specimen scope, and present status.
- 0:40–1:20: six objectives, grouped into acquire → analyze → validate.
- 1:20–2:10: literature themes and the distinction between polymer stress papers and perception/metal papers.
- 2:10–3:25: light path, component roles, and planned automation. Explain that the laptop handles the camera/processing.
- 3:25–4:20: explain planned validation, expected benefits, and current limitations verbally; show no additional simulation or circuit image.
- 4:20–5:00: stage-gated timeline, next experiment, and expected contribution.

Adjust to the actual allotted time. Do not rush through every equation in the oral presentation; keep the detail ready for questions.

## 11.2 How to answer without extra diagrams

Use the methodology block diagram already in the submitted PDF. Point to the source, then explain: “The first filter prepares light; the specimen changes its polarization; the analyzer converts that change to intensity; the camera records it; the computer processes the data.” This is sufficient for the main physical explanation. You do not need a component-level circuit or simulation plot to describe the proposal.

If asked where the circuit or simulation figures are, say: “This presentation is focused on the proposed methodology and literature. We have completed simulation/software preparation and a proposed hardware design, but are not presenting those diagrams in this deck. Hardware implementation and AI training remain future work.” Do not imply a live hardware demonstration is available.

If asked what the simulation contributes, explain verbally: “It models a stress field, converts it through the stress-optic law into phase delay, and predicts analyzer-dependent intensity. It helps us understand parameter effects and design experiments; it does not replace physical calibration.” Detailed figures and numerical values are background, not required talking points.

## 11.3 What each teammate should know

Everyone should know the aim, light path, present status, and central limitation. Allocate deeper ownership of optics/mechanics, hardware/control, software/AI, and literature/validation according to actual work; do not invent individual contributions. Practise handovers such as: “The optical principle is …; my teammate can explain the detailed circuit implementation.”

If asked who wrote the code or whether AI tools were used, answer accurately according to your actual process and institutional rules. Be able to explain the equations, assumptions, and checks yourself. Generated assistance is not experimental evidence or a substitute for understanding.

# 12. Viva question bank — short answer, then deeper reasoning

These questions cover plausible optics, instrumentation, mechanics, electronics, computing, and research-methods perspectives. They are preparation for likely directions, not a promise that every examiner question can be predicted.

## A. Aim, status, and scope

**Q1 [CORE]. What exactly does POLARIS measure?**

Initially, polarization-dependent transmitted intensity at known analyzer angles. With validated material, thickness, camera, and optical modelling, suitable data may support principal-stress-difference estimation. Defect classification is a separate proposed task. Say “intensity is measured; stress is inferred,” which makes the measurement chain clear.

**Q2 [CORE]. What have you actually completed?**

The documented work includes simulation, analytical and finite-element mechanics, synthetic optics, a limited numerical inverse, an interactive software application, checked figures, and a proposed wiring design. As confirmed by the team, hardware and AI remain proposed; experimental calibration and a trained defect CNN are not completed achievements.

**Q3 [CORE]. Where is the AI in your current result?**

AI is a proposed future assistance layer. The present stress-to-image model and inverse fitting are physics-based numerical calculations, not learned weights. We should evaluate whether learning improves a clear baseline once independent physical data exist, rather than relabel the simulator as a CNN.

**Q4. Why use the term optoelectronic?**

The specimen changes an optical signal, the camera converts photons into electronic data, and electronics/software acquire and interpret that data. The term describes the measurement chain; it does not imply a special new sensor has been invented.

**Q5 [CORE]. Is stressed material necessarily defective?**

No. Stress may be an intended operating state, and residual stress can be beneficial or harmful depending on its distribution and application. We need separately defined defect labels and acceptance criteria. This is why the slide’s simple normal/stressed/abnormal classes need refinement before training.

**Q6. Why is the method non-destructive if you apply load?**

Inspection is non-destructive only if the chosen load, gripping, and environment do not impair future use. We would stay within a justified reversible test regime and check for residual deformation or damage. A simulation load of 1000 N is not permission to apply that force to an unqualified specimen or fixture.

**Q7. Why begin with polymers instead of all transparent materials?**

We need a narrow, controllable experimental scope. Suitable transparent polymers can display accessible photoelastic effects, but their coefficients and residual anisotropy still need characterization. Glass, coatings, curved optics, and other materials require separate calibration and may have different sensitivity.

**Q8. What is your minimum successful project?**

A working and documented optical/mechanical setup that captures repeatable angle-resolved polymer images, demonstrates controlled response to known conditions, and states its limits. A calibrated subset of measurements is more defensible than an unsupported universal defect classifier.

## B. Optics and measurement physics

**Q9 [CORE]. Why do you need two polarizers?**

The first prepares a known input polarization. The specimen changes the relationship between its orthogonal components; the analyzer projects the output into a measurable intensity. Without a controlled input and output analysis, changes are harder to interpret quantitatively.

**Q10 [CORE]. State Malus’s law and its limitation here.**

I = Iin cos²θ for an ideal analyzer acting on linearly polarized input. A stressed birefringent specimen introduces phase and orientation effects, so the full specimen/analyzer model is needed. Simply applying cos²θ to every stressed pixel would miss the physics.

**Q11 [CORE]. What is birefringence?**

It is a difference in refractive index for two orthogonal polarization components. Stress-induced birefringence can make an initially isotropic photoelastic material behave as an optical retarder. Not all birefringence is caused by the current applied stress; fabrication and intrinsic anisotropy can contribute.

**Q12 [CORE]. What is the stress-optic law?**

In the simple model, Δn = C(σ1 − σ2), and δ = 2πCd(σ1 − σ2)/λ. It relates a stress difference to an optical phase delay under stated material and thickness assumptions. C must be calibrated for the relevant material and optical conditions.

**Q13. Why can high stress appear dark?**

For crossed polarizers the intensity includes sin²(2φ) and sin²(δ/2). A principal axis aligned with the input gives zero orientation factor, and integer-wave retardation also yields a dark response. Intensity is periodic and orientation-sensitive, not a monotonic stress meter.

**Q14 [CORE]. Can you find σ1 and σ2 individually?**

Not from their difference alone. Adding the same value to both leaves Δσ unchanged. Additional mechanical constraints, equilibrium information, boundary conditions, or independent measurements are needed to separate the stresses. The present model does not claim recovery of a complete 3D tensor.

**Q15. What happens under equal biaxial in-plane stress?**

σ1 = σ2 gives zero in-plane principal stress difference, so the ideal stress-induced birefringence term vanishes even though nonzero stress exists. This illustrates the method’s inability to measure an arbitrary mean stress using this observable alone.

**Q16. What are isochromatics and isoclinics?**

Isochromatics correspond to retardation/fringe-order contours under suitable material/thickness conditions. Isoclinics relate to principal-axis alignment with the polarizer/analyzer. Their superposition in a plane polariscope can complicate interpretation; circular arrangements can suppress the orientation term ideally.

**Q17. Why does wavelength matter?**

Phase delay scales as 1/λ for a fixed optical path difference, and real material/source/sensor behavior can also vary spectrally. Therefore different wavelengths give different intensities at the same stress. Multiple spectral measurements can constrain ambiguities but require correct spectral modelling.

**Q18 [CORE]. Are your webcam RGB channels exactly the three simulated wavelengths?**

No. Webcam channels have broad, overlapping responses and may undergo processing. The simulation uses ideal monochromatic channels. Quantitative transfer requires spectral/camera calibration or a redesigned narrow-band acquisition scheme; qualitative patterns are the honest first output.

**Q19. Why not use a laser for better precision?**

A laser offers spectral and coherence properties, but can also create speckle and additional alignment problems. Precision depends on the entire measurement chain, not the label “laser.” A diffused LED is a practical first source for stable area imaging.

**Q20. Do four analyzer angles measure the full polarization state?**

No. They can estimate the linear Stokes components S0, S1, S2 under suitable conditions, but not S3. A rotating linear analyzer alone cannot fully distinguish all elliptical polarization states. Extra polarization optics/states are needed for full polarimetry.

**Q21. If you rotate the analyzer, are you changing the stress?**

Ideally no: only the output polarization projection changes. The sample and load stay fixed. If the mount mechanically disturbs the sample or the load drifts during capture, that would be an experimental artifact to control.

**Q22. Can you determine defect depth?**

Not from a single transmission intensity map. The light interacts through the specimen thickness, and different three-dimensional distributions may generate similar projected signals. Depth localization requires additional measurement diversity and a more complete inverse model.

**Q23. What is a quarter-wave plate and why is it absent?**

A QWP produces a π/2 phase delay at its design wavelength and orientation conditions. It can prepare/analyze circular or elliptical states and support a circular polariscope. Our initial circuit uses linear polarizers for simplicity; a broadband QWP extension needs its own calibration and is not automatically handled by the current inverse.

**Q24. Can the unloaded sample still show a pattern?**

Yes: residual stress, molecular orientation, inherent anisotropy, thickness variation, or mounting may contribute. Record baseline images and investigate their origin; do not conclude that every unloaded pattern is a crack or that a uniform intensity proves an unstressed specimen.

## C. Mechanics and numerical modelling

**Q25 [CORE]. Why choose a circular hole?**

It generates a well-understood stress concentration and admits an analytical infinite-plate solution for comparison. It is a controlled geometry for understanding the measurement chain. It does not by itself establish detection of unknown defects in arbitrary parts.

**Q26 [CORE]. Why use both Kirsch and FEA?**

Kirsch gives a transparent analytical benchmark under infinite-plate assumptions. FEA lets us represent a finite boundary and specified restraints. Agreement in a relevant limit is useful, while differences can arise from finite width, mesh approximation, and boundary conditions.

**Q27. What is the stress-concentration factor?**

It is a ratio of a defined local maximum stress to a defined nominal stress. For an ideal infinite plate with a circular hole in uniaxial tension it reaches three at the appropriate hole-edge locations. State whether nominal stress uses gross or net section; different definitions produce different quoted factors.

**Q28. Why is 1000 N not 1000 MPa?**

Force and stress are different quantities. Stress requires force divided by area. For our 40 mm × 5 mm gross section, 1000 N corresponds to 5 MPa nominal stress, before the local concentration is considered.

**Q29. What is plane stress, and when can it fail?**

It assumes out-of-plane stress components are negligible, commonly for an appropriately thin plate under in-plane loading away from local effects. Thick geometry, complex gripping, out-of-plane loads, and through-thickness gradients can make it inadequate. We must assess the physical specimen, not assume every transparent object is plane stress.

**Q30. Why is a single node restrained vertically?**

With a left-edge horizontal restraint, the plate could still translate vertically as a rigid body. Fixing one suitable vertical displacement removes that mode without clamping the entire edge transversely. This choice changes what physical fixture the model approximates.

**Q31. Why use small-strain linear elasticity?**

It is a tractable first model when deformations and strains are sufficiently small and the material response is approximately elastic. Polymers can show creep, viscoelasticity, plasticity, and temperature dependence; those effects require a more complete model if the experiment enters that regime.

**Q32. Why does finer mesh change peak stress?**

A coarse mesh cannot fully resolve steep gradients near the hole, and the polygonal boundary approximates a circle. Peak stress often converges more slowly than global displacement. We report mesh dependence and avoid presenting a single peak as an exact measured value.

**Q33. What is the difference between mesh density and image resolution?**

Mesh density controls the mechanical discretization. Image-grid resolution controls sampling/visualization of the computed field. Increasing image pixels can make a plot smoother-looking without improving the underlying mechanical solution.

**Q34 [OPTIONAL SOFTWARE BACKUP]. How good is your inverse stress result?**

It is limited: in the audited 1400 N figure, only 34.26% of material pixels were accepted and accepted-pixel RMSE was about 1.42 MPa, with some large wrong-branch errors. It assumes exact orientation and optical parameters. It is evidence of a constrained numerical experiment, not full-field experimental accuracy.

**Q35. Why are parts of the inverse map blank?**

They are outside material or fail sensitivity/ambiguity/fit checks. An unresolved pixel is not a zero-stress pixel. Reporting a validity mask is essential because apparently plausible estimates can be unreliable where the optical signal carries little information.

**Q36. Why is 95% interval coverage not 95% accuracy?**

Coverage measures how often an interval contains a reference truth under a defined experiment, not how close each point estimate is. The reported intervals are local approximations conditional on exact model parameters, and the observed coverage comes from a synthetic realization. Large errors and unresolved areas can coexist with that coverage statistic.

## D. Electronics, components, and power

**Q37 [CORE]. Why use an Arduino and a laptop?**

The Arduino is suitable for simple timed control and sensor I/O. The laptop supplies USB-host functionality, camera capture, visualization, and future model computation. Separating those roles avoids trying to process full camera frames within the Uno’s very small memory.

**Q38. What are the Uno’s key specifications?**

ATmega328P, 5 V logic, 16 MHz, 32 KB flash, 2 KB SRAM, and 1 KB EEPROM, with 14 digital I/O and six analogue inputs on the standard board. State these as board specifications, not claims about image-processing capability.

**Q39 [CORE]. Why can’t the stepper connect directly to Arduino pins?**

Motor coils require substantially more current and a controlled bipolar drive with inductive-current handling. GPIO provides logic signals. The A4988 supplies and regulates coil current from the external motor supply while receiving STEP/DIR/ENABLE logic.

**Q40. What does NEMA 17 tell you?**

Primarily the mounting/frame standard. It does not guarantee a particular current, torque, step angle, or winding resistance. Our proposal separately assumes a 200-step/revolution motor and a suitable current rating.

**Q41 [CORE]. How do you set motor current?**

Read the A4988 carrier’s actual sense-resistor value, choose a phase-current limit within the motor/driver/cooling capability, and use VREF = 8 I Rs. For the proposed 0.60 A setting and Rs = 0.068 Ω, the target is approximately 0.326 V. Verify actual behavior and heating rather than relying on potentiometer position.

**Q42. Why do all grounds connect?**

Logic voltages need a common reference between Arduino, driver, MOSFET, and sensors. However, routing matters: high motor/LED currents should not flow through sensitive signal-return paths. Common reference does not mean connecting 12 V and 5 V together.

**Q43. Why use a MOSFET for the LED?**

The LED panel’s load current should not come from a GPIO. A logic-level N-MOSFET lets D9 control a separate power path with low conduction loss when properly driven. Current limiting is provided by the chosen LED panel/driver, not by the MOSFET alone.

**Q44. What do gate, drain, and source do?**

Gate voltage relative to source controls the channel. In our low-side arrangement the source is at ground, the drain connects to LED negative, and the gate receives the control signal through a resistor. The TO-220 tab is drain for the selected FQP30N06L package convention.

**Q45. Why add a gate pull-down?**

During reset a microcontroller pin may be high impedance. A pull-down discharges/defines the MOSFET gate so the LED does not turn on unpredictably. The series resistor limits brief charging current; neither resistor replaces LED current regulation.

**Q46. Why is a capacitor placed near VMOT?**

The driver switches current rapidly and wiring has inductance. Local bulk capacitance helps supply transient current and reduce voltage excursions. It must have correct polarity and adequate voltage rating; it does not replace correct grounding or a suitable supply.

**Q47. Why no separate flyback diode across each stepper coil?**

The integrated bipolar driver provides controlled current paths and recirculation as part of its H-bridge design. Arbitrarily adding diodes across bidirectionally driven coils is not the same as protecting a simple one-direction relay switch. Follow the driver’s application circuit and supply-decoupling requirements.

**Q48. Can you power everything from the Uno USB cable?**

No. The proposal reserves USB for the Uno’s logic and uses a separately powered camera connection and external 12 V supply for motor/LED loads. USB and board power paths have limits, and the motor should not be supplied through the Uno’s 5 V pin.

**Q49. Is a 24-bit HX711 accurate to one part in 2²⁴?**

No. Nominal code width does not establish effective noise-free resolution or calibrated force accuracy. Bridge sensitivity, noise, gain, temperature, drift, mounting, and calibration all matter. We would report measured repeatability and calibration residuals in newtons.

**Q50. Is the HX711 using ordinary I²C?**

No. Its DT and SCK use a device-specific serial clock/data interface. That is why the design assigns two digital pins and a suitable HX711 library/protocol rather than assuming an I²C device address.

## E. Control, acquisition, and metrology

**Q51 [CORE]. How do you command a 45° analyzer movement?**

With 200 full steps/revolution, 1/16 microstepping, and 4:1 reduction, there are 12,800 command steps per analyzer revolution. A 45° change requires 1600 steps. This calculation assumes no lost steps and a correctly calibrated mechanical setup.

**Q52. Is 0.028125° your measured angular accuracy?**

No. It is the command increment calculated from gearing and microstepping. Actual accuracy depends on the motor, belt, load, microstep behavior, homing and alignment. We need a physical angle-reference/repeatability test to claim accuracy.

**Q53. Why use a home switch if the motor counts steps?**

Step counts only describe motion relative to a known starting state and can be wrong after missed steps or power loss. Homing establishes a reference. It does not continuously measure the angle, so optical-zero calibration and repeatability testing are still needed.

**Q54. Why use normally closed contacts?**

The circuit can notice an open circuit as a high level, including the home actuation or a broken wire. That is useful but not uniquely diagnostic. A back-off/release check and timeout are needed to distinguish a valid homing sequence from a fault.

**Q55. What is backlash and how do you reduce it?**

It is lost motion when reversing direction due to mechanical clearance/compliance. Approach measurement angles consistently, maintain appropriate belt tension, and test repeatability. An encoder could measure actual position rather than relying only on commanded motion.

**Q56. Why wait before capturing an image?**

Motor motion, vibration, exposure timing, and camera buffering can otherwise produce a blurred or stale frame. Wait for motion completion and verified settling, then discard buffered frames. The correct delay must be measured for the assembled system, not assumed from a diagram.

**Q57. Why lock exposure and white balance?**

Automatic adjustments can change pixel values even if the specimen is unchanged, confusing optical effects with camera compensation. Locked settings are necessary for comparable angular images; linearity, offset, spectral response, and saturation must still be characterized.

**Q58. Why avoid LED PWM during imaging?**

Unsynchronized modulation can interact with frame exposure and rolling shutters, producing brightness fluctuations or stripes. Continuous illumination simplifies quantitative acquisition. PWM could be used only with a designed and validated synchronization/averaging scheme.

**Q59. What is the first calibration you would perform?**

Start with basic instrument behavior: dark offset, stable illumination, unsaturated camera response, and an empty-path analyzer sweep. Then establish optical zero and repeated-angle consistency. Material stress calibration follows after the acquisition chain is reliable.

**Q60. Can the load cell calibrate the stress around the hole directly?**

It supplies the total force. Dividing by gross area gives nominal stress, not the nonuniform local field. A uniform coupon can support stress-optic calibration under suitable assumptions; a hole field needs mechanical modelling and independent validation.

## F. AI, data, and software

**Q61 [CORE]. Why use a CNN rather than a threshold?**

A CNN may learn complex spatial patterns if enough independent labelled data exist. But a calibrated threshold or classical feature model may be simpler and more interpretable. We should compare them on the same held-out specimens and keep the simplest method that meets the actual task.

**Q62. What dataset have you trained on?**

No physical trained-model dataset is established in the documented project. Synthetic data support numerical demonstrations, not an experimentally validated CNN. Our next steps are labelled acquisition, independent specimen splits, baseline models, and then training if justified.

**Q63. What would your input and output be?**

For a proposed classifier, inputs could be registered angle-resolved images or calibrated features; outputs would be narrowly defined class labels. For segmentation, outputs are masks and require spatial labels. For stress regression, outputs are continuous calibrated values with uncertainty and valid-region information. We must choose rather than confuse these tasks.

**Q64 [CORE]. How will you prevent data leakage?**

Keep all correlated views/loads of a specimen within an appropriate split and evaluate on genuinely new specimens, preferably new sessions/batches as well. Randomly splitting nearly identical frames can make performance look excellent while only testing memorization.

**Q65. Why not train entirely on simulation?**

It may help pretraining and controlled testing, but simulated optics omit physical effects such as spectrum, sensor processing, mounting, residual anisotropy, and real defects. Physical held-out data are needed to demonstrate transfer. Domain randomization can help but is not itself validation.

**Q66. What is overfitting?**

A model fits training-specific patterns rather than the intended general relationship. Symptoms include strong training performance and weaker independent performance. Use meaningful splits, simpler models, regularization, suitable augmentation, and honest validation; more epochs do not guarantee improvement.

**Q67. Which metric matters most for defective parts?**

It depends on the consequences of misses and false rejects. Defect recall is important when misses are costly, but precision and false-positive rate also affect usability. Report the confusion matrix and per-class performance; raw accuracy alone can hide poor minority-defect detection.

**Q68. Does softmax confidence tell you the probability the part is safe?**

No. A model score can be miscalibrated, especially outside its training distribution. Safety requires a validated acceptance criterion and uncertainty management. At the proposed stage our output should be an inspection aid, not an unsupported guarantee.

**Q69. How would you prove polarization helps the AI?**

Use a controlled ablation: same specimens, splits, task, and evaluation; compare an intensity-only baseline with polarization-angle/features added. Report differences on held-out data and include failure cases. Do not attribute improvement to polarization if the comparison also changes data or training conditions unfairly.

**Q70. Does a heat map explain why a network detected a crack?**

It may indicate influential regions, but an attention/saliency visualization is not proof of causal physical reasoning or correct localization. Validate against independently marked defects and nuisance controls. Interpretability graphics complement, rather than replace, accuracy and robustness testing.

## G. Literature and research reasoning

**Q71 [CORE]. Which reference is most directly relevant to your specimen?**

The Wang polycarbonate-goggle paper and Verma polycarbonate-photoelasticity paper are closest to transparent-polymer stress investigation. The transparent-object and reflective-metal references motivate polarization/image-learning methods but address different measurement tasks.

**Q72. What exactly did Wang et al. demonstrate?**

Our slide describes qualitative residual-stress characterization of moulded polycarbonate goggles using photoelasticity and digital image processing, with image features linked to simulated stress. I would not quote a numerical accuracy, a CNN architecture, or a universal absolute-stress capability without checking the full paper.

**Q73. How is Yu’s segmentation different from your stress map?**

Segmentation identifies which pixels belong to an object or category. A stress map assigns a mechanically meaningful quantity to material points. Good object masking can assist our pipeline, but it does not supply stress calibration or an inverse mechanical solution.

**Q74. Why cite a metal-inspection paper for a transparent-polymer project?**

It is relevant as a methodological example of polarization-assisted inspection and learning, not as identical physics. We must explicitly acknowledge reflection versus transmission and different defects/materials. It cannot validate our measurement on transparent polymers.

**Q75 [CORE]. What is your research gap?**

A practical, student-scale integration and evaluation for a clearly specified polymer task: affordable automated acquisition, interpretable modelling, and explicit validation. We cannot claim nobody has combined AI and polarization; our own bibliography contradicts that broader assertion.

**Q76. What was the exact accuracy in the Fan or Li paper?**

I have not verified the exact metric and experimental split, so I should not quote a number. The relevant contribution to our proposal is the use of complementary polarization information for a defined perception/inspection task. I would consult the full paper before making a numerical comparison.

**Q77. Are six papers sufficient to prove novelty?**

No. They support a preliminary motivation, not an exhaustive prior-art search. A stronger review needs established digital photoelasticity, phase stepping, low-cost motorized polariscopes, quantitative inverse methods, and comparable implementations, including their costs and limitations.

**Q78. What is the difference between a literature takeaway and your own finding?**

A literature takeaway summarizes a cited author’s evidence within its scope. Our finding must arise from our own documented analysis or experiment. We should identify provenance explicitly and not present a paper’s result or a simulator’s assumed truth as our measured achievement.

## H. Validation, usefulness, and difficult challenges

**Q79 [CORE]. What is your biggest current limitation?**

The lack of physical calibration and independent experimental validation. In addition, the present inverse has a strong known-orientation prior and incomplete coverage. A reliable first hardware acquisition/calibration experiment is more urgent than claiming general AI defect detection.

**Q80. How will you establish ground truth for a defect?**

Define a specific defect class and independently characterize its location/size using an appropriate reference method or controlled manufactured feature. Keep load/material conditions documented. A hand-drawn label based only on the same ambiguous polarization image is not strong independent ground truth.

**Q81. Can a crack be missed?**

Yes. It may be too small, poorly oriented, weakly stressed, outside optical sensitivity, obscured by scattering, or outside the validated material domain. Detection probability must be measured against defect size and conditions; we cannot claim every hidden defect is visible.

**Q82. Can thickness variation mimic stress?**

Yes. Retardation depends on the product C d Δσ, so unknown thickness changes confound stress interpretation. Curved parts also alter paths and interfaces. Measure geometry or include it in the model; a flat uniform coupon is a sensible first scope.

**Q83. How would temperature affect the result?**

It can change source output, sensor behavior, refractive properties, elastic response, stress-optic coefficient, and specimen stress. Record/control temperature and test drift. A calibration is only transferable over the conditions for which it remains valid.

**Q84. Is the project real time?**

Not established. Sequential rotation, settling, camera frames, and processing impose latency. Measure end-to-end acquisition time before claiming real-time operation. A snapshot polarization camera might reduce temporal mismatch but changes cost and calibration and is not the chosen V1.

**Q85. How much does the whole instrument cost?**

We have a proposed component architecture, not a verified purchased bill of materials. I would obtain quotations for optics, camera, motion parts, mounts, fixture, load sensor, and power supply, and include calibration costs and an explicit laptop-included/excluded comparison. A guessed total would be misleading.

**Q86. Why not simply use an existing industrial instrument?**

Existing instruments are appropriate benchmarks. Our educational objective is an accessible, documented implementation that lets us understand acquisition, modelling, and validation. We must demonstrate a cost/performance/usefulness advantage rather than assume a custom build is inherently better.

**Q87 [CORE]. What experiment comes next?**

Assemble and verify the low-voltage control circuit, establish motor homing, and collect a repeatable empty-path analyzer sweep. Then test an unloaded polymer and controlled loading with reference measurements. This sequence isolates instrument problems before interpreting every image variation as stress.

**Q88. If the CNN never works, does the project fail?**

Not necessarily. A reproducible polarimetric acquisition system with well-characterized qualitative or calibrated measurement capability is a meaningful result. We should narrow the claim and report that AI did not add validated value, rather than force an unreliable classifier into the output.

**Q89. How will you make a pass/fail threshold?**

Start from an application-specific acceptance criterion, independent ground truth, and the costs of missed defects versus false rejection. Set the decision rule on development data, then evaluate independently and define an inconclusive region. Without that foundation, output should remain an anomaly indicator.

**Q90. How do you know the model is not just detecting the hole or background?**

Use controls, masks, changed backgrounds, matched intact/anomaly specimens, and held-out shapes or sessions as appropriate. Examine performance under nuisance changes. A model that only recognizes the known simulated hole has not established general hidden-defect detection.

**Q91. What would make you reject a stress estimate?**

Low sensitivity, competing phase solutions, fit at a search boundary, poor residuals, saturation, uncertain calibration, or an invalid material region. Report a validity mask and why estimates were rejected. A full-color output is less valuable than a smaller defensible set of estimates.

**Q92. Can the same calibration be used for any material?**

No. Material coefficient, dispersion, thickness, residual anisotropy, and mechanical response vary. Even the same polymer name can hide batch and manufacturing differences. Recalibration and domain checks are needed before transfer.

**Q93. Why is your model called a simulation rather than a digital twin?**

A validated physical twin would require demonstrated correspondence with a specific physical system and appropriately maintained parameters/data. Our current model uses illustrative assumptions without experimental calibration. “Simulation” is the more accurate description.

**Q94. What if an examiner points out a genuine mistake?**

Acknowledge it specifically, separate its effect from unaffected conclusions, and state the corrective test. For example: “You are right that webcam bands are not monochromatic. Our quantitative simulation uses ideal channels; the physical prototype therefore needs spectral calibration before those values can be compared.”

**Q95. What should you say when you do not know a detail?**

Say exactly what is known and where the gap is: “I know the role and governing relationship, but I have not verified that component/paper parameter. I would check the datasheet/reference before finalizing it.” Do not guess a number just because several examiners are present.

**Q96 [CORE]. Summarize your achievement, limitation, and contribution in three sentences.**

“We have developed a physics-based simulation and a concrete design for motorized polarization imaging of transparent polymers. The documented work has not yet established experimental stress accuracy or a trained defect classifier. Our intended contribution is a reproducible student-scale integration with explicit calibration, validation, and honest reporting of unresolved regions.”

# 13. Rapid numerical drills and examiner traps

## Calculations to practise without reading

**1000 N through 40 × 5 mm:** 5 MPa gross nominal stress. **1400 N through the same section:** 7 MPa. Do not apply these as local hole-edge stresses.

**200 steps/rev and 1/16 stepping:** 3200 motor pulses/rev. **4:1 belt reduction:** 12,800 analyzer pulses/rev. **45° analyzer move:** 1600 pulses. **90°:** 3200. **135°:** 4800. **1.8° full motor step:** 0.45° analyzer full step after 4:1 reduction, before microstepping.

**A4988 at 0.60 A, Rs = 0.10 Ω:** VREF = 8 × 0.60 × 0.10 = 0.48 V. Do not reuse this on a 0.068 Ω carrier.

**12 V panel at 0.5 A:** 6 W electrical input. **12 V, 3 A adapter:** 36 W nameplate capacity. **5 V across 10 kΩ:** 0.5 mA.

**2 kN load rating in kg-force equivalents:** about 204 kgf using g ≈ 9.81 m/s². Force capacity does not authorize hanging that mass from an unqualified frame; the unit conversion is not a fixture design.

**Δσ = 10 MPa with assumed C and d:** Δn = 3 × 10⁻⁵; optical path difference = 150 nm; δ ≈ 1.795 rad at 525 nm. Convert MPa to Pa and mm to metres before using the optical formula.

## Replace these unsafe phrases

| Do not say | Say instead |
| --- | --- |
| “We detect all hidden defects.” | “We propose to evaluate defined anomalies in specified transparent specimens.” |
| “This bright region has the maximum stress.” | “Brightness depends on orientation and phase; the simulated stress map identifies the model’s maximum.” |
| “Our accuracy is 95.84%.” | “That is synthetic local interval coverage for an accepted subset, not experimental accuracy.” |
| “We have a trained CNN.” | “CNN analysis is planned; the current inverse is physics-based.” |
| “NEMA 17 means a 17-step motor.” | “It specifies a mounting frame; our proposed motor separately has 200 full steps/rev.” |
| “The motor loads the specimen.” | “The motor rotates the analyzer; a separate fixture loads the specimen.” |
| “A 24-bit ADC gives 24-bit measurement accuracy.” | “Effective resolution and accuracy require noise and calibration tests.” |
| “The circuit picture proves hardware works.” | “It is a proposed connection diagram; assembly and bench tests remain necessary.” |
| “The simulation is ANSYS validated.” | “The project uses a native solver and numerical benchmarks; no ANSYS result is claimed.” |
| “Polarization plus AI is completely new.” | “Our intended contribution is an accessible, validated integration for a narrow task.” |
| “A zero-load image means zero stress.” | “Residual stress and other optical anisotropy may remain without external load.” |
| “This part passes, so it cannot fail.” | “Any acceptance result is conditional on a validated criterion and operating scope.” |

# 14. Final revision sheet

**Aim:** controlled polarization imaging for transparent-polymer stress/anomaly investigation; AI is a proposed later assistance layer.

**Present evidence:** simulation, analytical/FEA mechanics, synthetic optics, limited inverse, software interface, corrected figures, and proposed hardware. No experimentally validated stress instrument or trained CNN established in this guide.

**Light path:** LED + diffuser → fixed linear polarizer → specimen → rotating linear analyzer → USB camera → laptop.

**Control:** Uno → A4988 → stepper → belt → analyzer; home switch gives reference; laptop handles camera; optional load cell → HX711 → Uno. Specimen loading is separate.

**Five formulas:** σnom = F/A; Δσ = sqrt[(σx − σy)² + 4τxy²]; Δn = CΔσ; δ = 2πCdΔσ/λ; crossed I/I0 = sin²(2φ)sin²(δ/2).

**Core caution:** intensity is not stress, stress is not necessarily a defect, simulation is not experiment, inverse fitting is not CNN learning, and integration is not automatically new physics.

**Pins:** D2 STEP; D3 DIR; D4 ENABLE; D5 HX711 DT; D6 SCK; D7 home NC; D9 MOSFET gate via 100 Ω. Uno USB power, external 12 V motor/LED supply, common ground.

**Motion:** 200 × 16 × 4 = 12,800 pulses/analyzer revolution; 45° = 1600 pulses. Command resolution is not measured accuracy.

**Optional software backup:** 100 × 40 × 5 mm plate, 5 mm hole radius, 1000 N, 5 MPa gross stress, assumed E = 3000 MPa and ν = 0.35, assumed C = 3 × 10⁻¹² Pa⁻¹, ideal 630/525/450 nm channels.

**Optional inverse detail, not a slide talking point:** analyzer rotation; mesh/deformation magnified 100×; stress-to-optics; constrained inverse at a different 1400 N load. Inverse accepts about 34% of material pixels, with about 1.42 MPa accepted-pixel RMSE and some large errors.

**Literature map:** Wang/Verma = polymer photoelasticity. Yu/Fan = transparent-object perception and polarization information. Li/YOLO metal paper = reflection-based inspection, a different optical/material domain. Do not invent paper metrics.

**Next experiment:** empty-path analyzer sweep → repeatable unloaded-polymer imaging → controlled load measurements → calibration → independent specimens → only then justified learning and pass/fail evaluation.

**If challenged:** “That is a proposed capability, not a completed measurement. Our present evidence is …; the experiment needed to establish it is …”

**Closing line:** “We aim to build an accessible and interpretable measurement workflow, and to quantify where it works and where it does not.”

# 15. Sources, provenance, and files to keep available

## Submitted document

POLARIS_GROUP 18.pdf, seven pages, supplied by the team. Group members: Moumita Namasudra, Aemili Das, Antarlina Datta, Aishi Kesh. Supervisor: Dr. Aparupa Kar. The guide follows the submitted slide claims while explicitly distinguishing later proposed component choices.

## Project evidence

- Project repository: https://github.com/Aemili09/POLARIS
- Methods: https://github.com/Aemili09/POLARIS/blob/main/docs/METHODS.md
- Numerical validation: https://github.com/Aemili09/POLARIS/blob/main/docs/VALIDATION.md
- Scientific figure audit: https://github.com/Aemili09/POLARIS/blob/main/docs/FIGURE_AUDIT.md
- Audited presentation assets: https://github.com/Aemili09/POLARIS/tree/main/presentation
- Pictorial wiring: https://github.com/Aemili09/POLARIS/blob/main/hardware/POLARIS_Pictorial_Wiring.png

Numerical statements in this guide come from the repository’s documented audit and methods; no new physical measurement is claimed. Hardware remains a proposed design. Standard component specifications are starting references to confirm against purchased-part manufacturer documents; clone modules and cameras can differ.

## Manufacturer / technical references to consult

- Arduino Uno Rev3: https://docs.arduino.cc/hardware/uno-rev3/
- Pololu A4988 carrier information and application guidance: https://www.pololu.com/product/1182
- A4988 manufacturer datasheet: https://www.allegromicro.com/-/media/files/datasheets/a4988-datasheet.pdf
- FQP30N06L manufacturer datasheet: https://www.onsemi.com/pdf/datasheet/fqp30n06l-d.pdf
- HX711 protocol/library background: https://github.com/bogde/HX711 ; consult the actual module schematic and IC datasheet for power, RATE, and pin details.

These are reference destinations, not a claim that every web page or manufacturer document was retrievable during preparation. Publisher reference details in section 7 remain slide-sourced pending full-text/metadata checking.

## Final practical checklist

- Save the submitted PDF, this Word guide, and the PDF reading copy locally. You do not need to show or open the extra simulation/circuit images for this presentation.
- Open each file before leaving; check that the presentation laptop can display it offline.
- Know which results are synthetic and which, if any, your team has physically measured since this guide was prepared.
- Practise the opening once, the optical explanation once, and the CORE questions twice aloud.
- Carry a short note with the five formulas, pin map, motion calculation, and limitations; understand them rather than memorizing unexplained numbers.
- If a claim is not supported, narrow it clearly. A technically honest answer is stronger than an impressive but indefensible one.
