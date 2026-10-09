import numpy as np
import pytest
from numpy.testing import assert_allclose
from polaris.mechanics import Geometry, kirsch, kirsch_at
from polaris.optics import OpticalConfig, optical_images, camera_image
from polaris.validation import physics_checks


def test_notebook_physics():
    assert len(physics_checks()) == 7


def test_entire_hole_boundary_is_traction_free():
    theta = np.linspace(0, 2*np.pi, 97)
    c, s = np.cos(theta), np.sin(theta)
    sx, sy, t = kirsch_at(5*c, 5*s, 5, 5)
    assert_allclose(sx*c+t*s, 0, atol=1e-12)
    assert_allclose(t*c+sy*s, 0, atol=1e-12)


def test_load_scaling_symmetry_and_far_field():
    one, two = kirsch(1000, nx=51, ny=31), kirsch(2000, nx=51, ny=31)
    assert_allclose(two.delta_sigma_mpa, 2*one.delta_sigma_mpa)
    assert_allclose(one.sigma_x_mpa, one.sigma_x_mpa[::-1], atol=1e-12)
    assert_allclose(one.tau_xy_mpa, -one.tau_xy_mpa[::-1], atol=1e-12)
    assert_allclose(kirsch_at(50000, 10000, 5, 5), (5, 0, 0), atol=1e-6)


def test_malus_law_and_qwp_energy():
    field = kirsch(0, nx=21, ny=11)
    for alpha in (0, 30, 45, 90):
        assert_allclose(optical_images(field, alpha)["rgb_linear"], np.cos(np.deg2rad(alpha))**2, atol=1e-12)
    # 45° ideal QWP converts x-polarized light into circular polarization.
    for alpha in (0, 30, 90, 135):
        assert_allclose(optical_images(field, alpha, quarter_wave_deg=45)["rgb_linear"], 0.5, atol=1e-12)
    loaded = kirsch(1000, nx=31, ny=21)
    a = optical_images(loaded, 23, quarter_wave_deg=17)["rgb_linear"]
    b = optical_images(loaded, 113, quarter_wave_deg=17)["rgb_linear"]
    assert_allclose(a+b, 1, atol=1e-12)


def test_gamma_never_changes_physical_arrays():
    field = kirsch(nx=21, ny=11)
    a = optical_images(field, config=OpticalConfig(display_gamma=.4))
    b = optical_images(field, config=OpticalConfig(display_gamma=1.5))
    assert_allclose(a["rgb_linear"], b["rgb_linear"])
    assert_allclose(a["retardances"], b["retardances"])


def test_camera_noise_is_seeded_and_has_expected_scale():
    ideal = np.full((300, 300, 3), 0.4)
    image = camera_image(ideal, photons=10000, read_noise=.002)
    assert_allclose(image, camera_image(ideal, photons=10000, read_noise=.002))
    assert abs(image.mean()-.4) < 1e-4
    assert abs(image.var()-(.4/10000+.002**2)) < 1e-6


@pytest.mark.parametrize("kwargs", [{"force_n": -1}, {"force_n": np.nan}, {"nx": 1}, {"ny": 3.5}])
def test_bad_mechanical_inputs(kwargs):
    with pytest.raises(ValueError):
        kirsch(**kwargs)


def test_bad_geometry_and_optics():
    with pytest.raises(ValueError):
        Geometry(hole_radius_mm=30)
    with pytest.raises(ValueError):
        OpticalConfig(wavelengths_nm=(630, 0, 450))
