"""Fit measured unwrapped phase and linear camera reference data."""
from dataclasses import asdict, dataclass
import numpy as np


@dataclass
class StressOpticFit:
    coefficient_pa_inv: float
    standard_error_pa_inv: float
    phase_offset_rad: float
    residual_rms_rad: float
    samples: int

    def to_dict(self):
        return asdict(self)


def fit_stress_optic(delta_sigma_mpa, retardance_rad, thickness_mm=5.0, wavelength_nm=525.0):
    """Fit phase = C * 2π d Δσ/λ + offset with ordinary least squares.

    Phase must already be unwrapped; intensity alone does not supply phase.
    Standard error assumes independent, homoscedastic phase errors.
    """
    s, phase = np.asarray(delta_sigma_mpa, float), np.asarray(retardance_rad, float)
    if s.ndim != 1 or phase.shape != s.shape or len(s) < 3 or not np.isfinite(s).all() or not np.isfinite(phase).all() or (s < 0).any():
        raise ValueError("Provide at least three finite, nonnegative stress differences and matching phases.")
    if not np.isfinite(thickness_mm) or thickness_mm <= 0 or not np.isfinite(wavelength_nm) or wavelength_nm <= 0:
        raise ValueError("Thickness and wavelength must be positive.")
    if np.ptp(s) <= np.finfo(float).eps * max(1.0, np.max(s)):
        raise ValueError("Calibration needs distinct stress levels.")
    # Fit slope in rad/MPa to avoid an ill-conditioned SI design matrix.
    design = np.column_stack((s, np.ones_like(s)))
    slope, offset = np.linalg.lstsq(design, phase, rcond=None)[0]
    factor = 2*np.pi*(thickness_mm*1e-3)*1e6/(wavelength_nm*1e-9)
    if slope <= 0:
        raise ValueError("Measured phase must increase with principal stress difference.")
    residual = phase - design @ [slope, offset]
    variance = np.sum(residual**2)/(len(s)-2)
    se = np.sqrt(variance/np.sum((s-s.mean())**2))/factor
    return StressOpticFit(float(slope/factor), float(se), float(offset),
                          float(np.sqrt(np.mean(residual**2))), len(s))


def fit_camera(reference_linear, measured_rgb):
    """Fit measured RGB = gain * reference RGB + offset, excluding saturation."""
    x, y = np.asarray(reference_linear, float), np.asarray(measured_rgb, float)
    if x.ndim != 2 or x.shape[1] != 3 or x.shape != y.shape or len(x) < 3 or not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Camera calibration requires matching finite N × 3 reference and measured arrays.")
    if ((x < 0) | (x > 1) | (y < 0) | (y > 1)).any():
        raise ValueError("Camera references and measurements must be normalized to [0, 1].")
    gains, offsets, residuals = [], [], []
    for k in range(3):
        usable = (y[:, k] > 0) & (y[:, k] < 1)
        xx, yy = x[usable, k], y[usable, k]
        if len(xx) < 3 or np.ptp(xx) < 1e-8:
            raise ValueError("Each channel needs at least three unsaturated samples with varying intensity.")
        design = np.column_stack((xx, np.ones_like(xx)))
        gain, offset = np.linalg.lstsq(design, yy, rcond=None)[0]
        if gain <= 0:
            raise ValueError("Camera channel gain must be positive.")
        gains.append(float(gain))
        offsets.append(float(offset))
        residuals.append(float(np.sqrt(np.mean((yy-design @ [gain, offset])**2))))
    return {"gains": gains, "offsets": offsets, "residual_rms": residuals,
            "model": "linear per-channel gain and offset; clipped samples excluded"}


def correct_camera(measured_rgb, gains, offsets):
    rgb, g, o = np.asarray(measured_rgb, float), np.asarray(gains, float), np.asarray(offsets, float)
    if rgb.ndim < 1 or rgb.shape[-1] != 3 or g.shape != (3,) or o.shape != (3,) or (g <= 0).any() or not all(np.isfinite(v).all() for v in (rgb, g, o)):
        raise ValueError("Finite RGB values, positive gains and finite offsets are required.")
    # Do not clip: clipping would hide calibration errors and bias inverse fits.
    return (rgb-o)/g
