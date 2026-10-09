import numpy as np
import pytest
from numpy.testing import assert_allclose
from polaris.calibration import fit_stress_optic, fit_camera, correct_camera
from polaris.optics import retardance
from polaris.inverse import reconstruct


def test_coefficient_and_camera_recovery():
    stress = np.linspace(0, 20, 21)
    phase = retardance(stress, 5)[:, 1] + .07
    fit = fit_stress_optic(stress, phase)
    assert_allclose(fit.coefficient_pa_inv/3e-12, 1, atol=1e-12)
    assert_allclose(fit.phase_offset_rad, .07, atol=1e-12)
    assert fit.standard_error_pa_inv < 1e-25
    reference = np.tile(np.linspace(.1, .8, 10)[:, None], (1, 3))
    gains, offsets = [1.05, .93, 1.1], [.01, .02, .03]
    measured = reference*gains+offsets
    fit = fit_camera(reference, measured)
    assert_allclose(fit["gains"], gains)
    assert_allclose(fit["offsets"], offsets)
    assert_allclose(correct_camera(measured, fit["gains"], fit["offsets"]), reference)


def test_inverse_recovers_held_out_known_phases_and_rejects_dark_axes():
    stress = np.array([3.2, 7.6, 14.5, 22.3])
    phi = np.array([.35, .6, .85, 1.0])
    rgb = np.sin(2*phi[:, None])**2*np.sin(retardance(stress, 5)/2)**2
    recovered = reconstruct(rgb, phi, noise_std=.0001)
    assert recovered.valid.all()
    assert_allclose(recovered.delta_sigma_mpa, stress, atol=.001)
    dark = reconstruct(np.zeros((4, 3)), np.zeros(4))
    assert not dark.valid.any()
    assert np.isinf(dark.standard_error_mpa).all()


def test_noise_uncertainty_and_phase_ambiguity():
    rng = np.random.default_rng(12)
    phi = np.full(1000, np.pi/4)
    true_stress = np.full(1000, 7.1)
    rgb = np.sin(retardance(true_stress, 5)/2)**2 + rng.normal(0, .002, (1000, 3))
    fit = reconstruct(rgb, phi, noise_std=.002)
    assert fit.valid.all()
    coverage = np.mean(abs(fit.delta_sigma_mpa-true_stress) < 1.96*fit.standard_error_mpa)
    assert .92 < coverage < .98
    from polaris.optics import OpticalConfig
    monochrome = OpticalConfig(wavelengths_nm=(525, 525, 525))
    image = np.sin(retardance(np.array([7.1]), 5, monochrome)/2)**2
    ambiguous = reconstruct(image, np.array([np.pi/4]), config=monochrome, max_stress_mpa=100)
    assert ambiguous.ambiguous[0] and not ambiguous.valid[0]


def test_invalid_calibration_and_bounds():
    with pytest.raises(ValueError):
        fit_stress_optic([1, 1, 1], [1, 2, 3])
    with pytest.raises(ValueError):
        fit_camera(np.ones((3, 3)), np.ones((3, 3)))
    with pytest.raises(ValueError):
        reconstruct(np.zeros((3, 3)), np.zeros(3), noise_std=0)
