"""Reproducible physics checks and held-out synthetic reconstruction study."""
import numpy as np
from numpy.testing import assert_allclose
from .mechanics import kirsch, kirsch_at
from .optics import optical_images
from .fea import solve_plate
from .inverse import reconstruct


def physics_checks():
    field = kirsch()
    S = field.metadata["remote_mpa"]
    sx, sy, xy = kirsch_at(0, field.geometry.hole_radius_mm, S, field.geometry.hole_radius_mm)
    assert_allclose([sx, sy, xy], [3*S, 0, 0], atol=1e-12)
    zero = kirsch(0, nx=51, ny=31)
    assert_allclose(zero.delta_sigma_mpa, 0, atol=1e-12)
    assert_allclose(optical_images(zero, 90)["rgb_linear"], 0, atol=1e-12)
    hole = ~field.outside
    cross, parallel = optical_images(field, 90), optical_images(field, 0)
    assert_allclose(cross["rgb_linear"][hole], 0, atol=1e-12)
    assert_allclose(parallel["rgb_linear"][hole], 1, atol=1e-12)
    predicted = np.sin(2*field.phi_rad)[..., None]**2*np.sin(cross["retardances"]/2)**2
    assert_allclose(cross["rgb_linear"], predicted, atol=1e-12)
    assert_allclose(cross["rgb_linear"]+parallel["rgb_linear"], 1, atol=1e-12)
    for angle in (0, 30, 45, 90, 135, 180):
        v = optical_images(field, angle)["rgb_linear"]
        assert np.isfinite(v).all() and v.min() >= 0 and v.max() <= 1
    assert abs(field.sigma_x_mpa[len(field.y_mm)//2, -1]/S-1) < .05
    return ["Kirsch 3σ hole boundary", "Zero-load darkness", "Clear-hole transmission",
            "Jones / closed-form agreement", "Orthogonal analyzer energy conservation",
            "Finite bounded intensities at six angles", "Far-field consistency"]


def held_out_study(forces=(600.0, 1400.0), noise_std=0.001, seed=17):
    """Independent FEA load cases; no material parameters fitted to these cases.

    Known FEA orientation is supplied as a prior. Noise is additive Gaussian on
    linear intensities, without clipping, matching the likelihood used by inverse.
    """
    reports = []
    rng = np.random.default_rng(seed)
    for force in forces:
        result = solve_plate(force, radial=12, angular=64, nx=71, ny=31)
        field = result.field
        image = optical_images(field)["rgb_linear"]
        measured = image + rng.normal(0, noise_std, image.shape)
        recovered = reconstruct(measured, field.phi_rad, noise_std=noise_std)
        valid = recovered.valid & field.outside
        count = int(valid.sum())
        if count == 0:
            raise RuntimeError("No valid reconstructed pixels in held-out study.")
        errors = recovered.delta_sigma_mpa[valid]-field.delta_sigma_mpa[valid]
        coverage = np.mean(np.abs(errors) <= 1.96*recovered.standard_error_mpa[valid])
        reports.append({"force_n": force, "valid_pixels": count,
                        "material_pixels": int(field.outside.sum()),
                        "valid_fraction": float(count/field.outside.sum()),
                        "rmse_mpa": float(np.sqrt(np.mean(errors**2))),
                        "mean_absolute_error_mpa": float(np.mean(np.abs(errors))),
                        "approx_95pct_coverage": float(coverage),
                        "noise_std_linear": noise_std, "known_orientation": True})
    return reports
