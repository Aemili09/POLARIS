"""Independent benchmarks and regressions from the detailed figure audit."""
import numpy as np
import matplotlib.pyplot as plt
from numpy.testing import assert_allclose
from scipy.optimize import minimize_scalar
from polaris.mechanics import Geometry, StressField, kirsch, kirsch_at
from polaris.optics import optical_images
from polaris.fea import solve_plate
from polaris.inverse import reconstruct, Reconstruction
from polaris.plots import image_on_grid, reconstruction_figure


def test_full_jones_matrix_independent_reference():
    rng = np.random.default_rng(2026)
    phi = rng.uniform(-np.pi/2, np.pi/2, (5, 7))
    ds = rng.uniform(0, 50, phi.shape)
    field = StressField(np.linspace(-50, 50, 7), np.linspace(-20, 20, 5),
                        ds*np.cos(phi)**2, ds*np.sin(phi)**2,
                        ds*np.cos(phi)*np.sin(phi), np.ones(phi.shape, bool), Geometry())
    tensor = np.stack((np.stack((field.sigma_x_mpa, field.tau_xy_mpa), -1),
                       np.stack((field.tau_xy_mpa, field.sigma_y_mpa), -1)), -2)
    eigvals = np.linalg.eigvalsh(tensor)
    assert_allclose(field.delta_sigma_mpa, eigvals[..., 1]-eigvals[..., 0], atol=1e-12)
    # Use explicit 2×2 rotations and a diagonal phase matrix, not the forward
    # implementation's component expressions or the inverse trigonometric formula.
    for angle in (0, 17, 45, 90, 135):
        expected = np.empty(phi.shape+(3,))
        analyzer = np.array([np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))])
        for row, col in np.ndindex(phi.shape):
            c, s = np.cos(phi[row, col]), np.sin(phi[row, col])
            rotation = np.array([[c, -s], [s, c]])
            for k, wave in enumerate((630, 525, 450)):
                phase = 2*np.pi*.005*3e-12*(ds[row, col]*1e6)/(wave*1e-9)
                matrix = rotation @ np.diag(np.exp(1j*np.array([phase/2, -phase/2]))) @ rotation.T
                expected[row, col, k] = abs(analyzer @ matrix @ np.array([1., 0.]))**2
        assert_allclose(optical_images(field, angle)["rgb_linear"], expected, atol=1e-12)


def test_kirsch_local_equilibrium():
    rng = np.random.default_rng(1)
    theta = rng.uniform(0, 2*np.pi, 100)
    radius = rng.uniform(6, 45, 100)
    x, y = radius*np.cos(theta), radius*np.sin(theta)
    h = 1e-4
    xp, xm = kirsch_at(x+h, y, 5, 5), kirsch_at(x-h, y, 5, 5)
    yp, ym = kirsch_at(x, y+h, 5, 5), kirsch_at(x, y-h, 5, 5)
    assert_allclose((xp[0]-xm[0]+yp[2]-ym[2])/(2*h), 0, atol=1e-7)
    assert_allclose((xp[2]-xm[2]+yp[1]-ym[1])/(2*h), 0, atol=1e-7)


def test_solver_matches_exact_unperforated_tension(monkeypatch):
    # Replace only the mesh to benchmark the assembled solver against an exact
    # unperforated rectangle; production geometry remains the perforated plate.
    X, Y = np.meshgrid(np.linspace(-50, 50, 11), np.linspace(-20, 20, 5))
    nodes = np.column_stack((X.ravel(), Y.ravel()))
    triangles = []
    for j in range(4):
        for i in range(10):
            p = j*11+i
            triangles.extend(((p, p+1, p+12), (p, p+12, p+11)))
    monkeypatch.setattr("polaris.fea.annular_mesh", lambda *args: (nodes, np.asarray(triangles)))
    result = solve_plate(nx=31, ny=21)
    exact = np.column_stack((5/3000*(nodes[:, 0]+50), -.35*5/3000*nodes[:, 1]))
    assert_allclose(result.displacement_mm, exact, atol=1e-12)
    assert_allclose(result.element_stress_mpa, np.tile([5., 0, 0], (len(triangles), 1)), atol=1e-10)


def test_fea_stress_from_independent_affine_displacements():
    result = solve_plate(radial=12, angular=64, nx=101, ny=41)
    xy = result.nodes_mm[result.triangles]
    design = np.concatenate((np.ones((*xy.shape[:2], 1)), xy), axis=-1)
    coefficients = np.linalg.solve(design, result.displacement_mm[result.triangles])
    exx, eyy = coefficients[:, 1, 0], coefficients[:, 2, 1]
    gamma = coefficients[:, 2, 0]+coefficients[:, 1, 1]
    independent = np.column_stack((3000/(1-.35**2)*(exx+.35*eyy),
                                   3000/(1-.35**2)*(eyy+.35*exx), 3000/(2*(1+.35))*gamma))
    assert_allclose(result.element_stress_mpa, independent, atol=1e-10)
    X, Y = np.meshgrid(result.field.x_mm, result.field.y_mm)
    assert np.array_equal(result.field.outside, np.hypot(X, Y) >= 5)


def test_image_pixel_centers_match_physical_coordinates():
    field = kirsch(nx=11, ny=5)
    fig, ax = plt.subplots()
    image = image_on_grid(ax, field.delta_sigma_mpa, field)
    left, right, bottom, top = image.get_extent()
    assert_allclose(left+(np.arange(11)+.5)*(right-left)/11, field.x_mm)
    assert_allclose(bottom+(np.arange(5)+.5)*(top-bottom)/5, field.y_mm)
    assert_allclose(ax.get_xlim(), [-50, 50])
    plt.close(fig)


def test_reconstruction_color_scale_keeps_accepted_outliers_visible():
    field = kirsch(nx=11, ny=5)
    shape = field.outside.shape
    estimate = np.full(shape, 29.)
    result = Reconstruction(estimate, np.ones(shape), field.outside.copy(),
                            np.zeros(shape, bool), np.zeros(shape, bool), np.zeros(shape))
    fig = reconstruction_figure(field, result)
    assert fig.axes[0].images[0].get_clim()[1] == 29
    assert fig.axes[1].images[0].get_clim()[1] == 29
    plt.close(fig)


def test_inverse_agrees_with_independent_bounded_optimizer():
    phi = np.array([.4, .8, 1.1])
    stress = np.array([6.3, 14.2, 24.7])
    wavelengths = np.array([630., 525., 450.])*1e-9
    k = 2*np.pi*.005*3e-12*1e6/wavelengths
    measured = np.sin(2*phi[:, None])**2 * np.sin(stress[:, None]*k/2)**2
    measured += np.random.default_rng(42).normal(0, .001, measured.shape)
    result = reconstruct(measured, phi, noise_std=.001)
    for i in range(3):
        def loss(s):
            return np.sum((np.sin(2*phi[i])**2*np.sin(s*k/2)**2-measured[i])**2)
        # Independent scalar optimizations on multiple subintervals, including
        # every endpoint, cover alternative fringe branches across 0–30 MPa.
        candidates = [(loss(v), v) for v in (0., 30.)]
        for lo in range(0, 30, 2):
            fit = minimize_scalar(loss, bounds=(lo, lo+2), method="bounded", options={"xatol": 1e-10})
            candidates.append((fit.fun, fit.x))
        best = min(candidates)[1]
        assert abs(result.delta_sigma_mpa[i]-best) < 1e-3
