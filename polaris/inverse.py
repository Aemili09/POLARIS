"""Bounded stress-difference reconstruction with known principal-axis orientation.

This is a constrained inverse problem, not recovery of a full stress tensor.
Uses raw linear monochromatic RGB and independent Gaussian intensity errors.
"""
from dataclasses import dataclass
import numpy as np
from .optics import OpticalConfig, retardance


@dataclass
class Reconstruction:
    delta_sigma_mpa: np.ndarray
    standard_error_mpa: np.ndarray
    valid: np.ndarray
    ambiguous: np.ndarray
    boundary: np.ndarray
    residual_rms: np.ndarray


def reconstruct(rgb_linear, phi_rad, thickness_mm=5.0, config=None, analyzer_deg=90.0,
                max_stress_mpa=30.0, noise_std=0.002, samples=2001):
    """Global discrete search, sub-grid refinement, local Fisher uncertainty.

    Mark unresolved pixels (dark axes, rival minima, bound hits, poor fits,
    or large uncertainty) invalid. Standard errors exclude material/model error.
    """
    config = config or OpticalConfig()
    rgb, phi = np.asarray(rgb_linear, float), np.asarray(phi_rad, float)
    if rgb.shape != phi.shape + (3,) or not np.isfinite(rgb).all() or not np.isfinite(phi).all():
        raise ValueError("Finite linear RGB must have shape phi.shape + (3,).")
    if not np.isfinite(max_stress_mpa) or max_stress_mpa <= 0 or not np.isfinite(noise_std) or noise_std <= 0 or not isinstance(samples, int) or samples < 101:
        raise ValueError("Use a positive stress bound/noise and at least 101 search samples.")
    if not np.isfinite(analyzer_deg):
        raise ValueError("Analyzer angle must be finite.")
    stress_grid = np.linspace(0, max_stress_mpa, samples)
    step = stress_grid[1]
    k = retardance(np.array(1.0), thickness_mm, config)
    if np.max(k)*step > 0.1:
        raise ValueError("Search spacing is too coarse to resolve optical fringes; increase samples.")
    basis = np.sin(stress_grid[:, None]*k/2)**2
    alpha = np.deg2rad(analyzer_deg)
    baseline = np.cos(alpha)**2
    amplitude = np.sin(2*phi.ravel())*np.sin(2*alpha-2*phi.ravel())
    observed = rgb.reshape(-1, 3)
    estimate = np.empty(len(observed))
    ambiguous = np.zeros(len(observed), bool)
    boundary = np.zeros(len(observed), bool)
    for begin in range(0, len(observed), 128):
        end = min(begin+128, len(observed))
        amp = amplitude[begin:end]
        pred = baseline + amp[:, None, None]*basis[None, :, :]
        cost = np.sum((pred-observed[begin:end, None, :])**2, axis=2)
        index = cost.argmin(axis=1)
        row = np.arange(end-begin)
        bounded = (index == 0) | (index == samples-1)
        center = np.clip(index, 1, samples-2)
        low, mid, high = cost[row, center-1], cost[row, center], cost[row, center+1]
        denom = low-2*mid+high
        shift = np.divide(0.5*(low-high), denom, out=np.zeros_like(mid), where=denom > 1e-30)
        fitted = (center+np.clip(shift, -1, 1))*step
        estimate[begin:end] = np.where(bounded, stress_grid[index], fitted)
        boundary[begin:end] = bounded
        # Competing local minima within Δχ² <= 3.84 indicate phase ambiguity.
        minima = np.zeros_like(cost, bool)
        minima[:, 1:-1] = (cost[:, 1:-1] <= cost[:, :-2]) & (cost[:, 1:-1] < cost[:, 2:])
        minima[:, 0] = cost[:, 0] < cost[:, 1]
        minima[:, -1] = cost[:, -1] < cost[:, -2]
        minima[row, index] = False
        rivals = np.where(minima, cost, np.inf).min(axis=1)
        ambiguous[begin:end] = rivals-cost[row, index] <= 3.84*noise_std**2
    prediction = baseline + amplitude[:, None]*np.sin(estimate[:, None]*k/2)**2
    derivative = amplitude[:, None]*k/2*np.sin(estimate[:, None]*k)
    information = np.sum(derivative**2, axis=1)/noise_std**2
    se = np.divide(1.0, np.sqrt(information), out=np.full_like(information, np.inf), where=information > 1e-20)
    residual = np.sqrt(np.mean((prediction-observed)**2, axis=1))
    boundary |= (estimate < 1.96*se) | (estimate > max_stress_mpa-1.96*se)
    valid = (np.abs(amplitude) > 1e-6) & ~ambiguous & ~boundary & (se < max_stress_mpa/10) & (residual < 4*noise_std)
    shape = phi.shape
    return Reconstruction(*(a.reshape(shape) for a in (estimate, se, valid, ambiguous, boundary, residual)))
