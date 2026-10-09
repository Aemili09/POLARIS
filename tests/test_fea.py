import numpy as np
import pytest
from numpy.testing import assert_allclose
from polaris.fea import solve_plate, element_matrices


def test_linear_displacement_patch():
    nodes = np.array([[0, 0], [2, 0], [2, 1], [0, 1]], float)
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    B, D, area = element_matrices(nodes, triangles, 3000, .35)
    displacement = np.column_stack((.02*nodes[:, 0]+.03*nodes[:, 1]+.1,
                                     -.01*nodes[:, 0]+.04*nodes[:, 1]-.2))
    strain = np.einsum('eij,ej->ei', B, displacement[triangles].reshape(-1, 6))
    assert_allclose(strain, np.tile([.02, .04, .02], (2, 1)), atol=1e-14)
    assert_allclose(area.sum(), 2)


@pytest.mark.parametrize("grip,profile", [("roller", "uniform"), ("clamped", "parabolic")])
def test_force_balance_and_energy(grip, profile):
    result = solve_plate(radial=10, angular=48, nx=51, ny=31, grip=grip, load_profile=profile)
    d = result.diagnostics
    assert_allclose(d["applied_force_n"], 1000, atol=1e-9)
    assert_allclose(d["reaction_x_n"], -1000, atol=1e-7)
    assert_allclose(d["reaction_y_n"], 0, atol=1e-7)
    assert d["relative_free_residual"] < 1e-9
    assert d["strain_energy_n_mm"] > 0
    assert d["maximum_displacement_mm"] > 0
    assert 10 < result.field.delta_sigma_mpa.max() < 25


def test_fea_zero_load_and_linear_scaling():
    opts = dict(radial=6, angular=32, nx=31, ny=21)
    zero, one, two = (solve_plate(f, **opts) for f in (0, 1000, 2000))
    assert_allclose(zero.displacement_mm, 0)
    assert_allclose(two.displacement_mm, 2*one.displacement_mm, atol=1e-12)
    assert_allclose(two.element_stress_mpa, 2*one.element_stress_mpa, atol=1e-10)


def test_mesh_refinement_converges_in_displacement_and_peak():
    results = [solve_plate(radial=r, angular=a, nx=51, ny=31) for r, a in ((8, 32), (16, 64), (32, 128))]
    displacement = np.array([r.diagnostics["maximum_displacement_mm"] for r in results])
    peak = np.array([r.diagnostics["peak_element_principal_difference_mpa"] for r in results])
    assert abs(displacement[2]-displacement[1]) < abs(displacement[1]-displacement[0])
    assert abs(displacement[2]/displacement[1]-1) < .015
    assert abs(peak[2]/peak[1]-1) < .12
