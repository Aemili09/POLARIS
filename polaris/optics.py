"""Ideal Jones optics and an optional linear camera with shot/read noise."""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class OpticalConfig:
    stress_optic_pa_inv: float = 3e-12
    wavelengths_nm: tuple = (630.0, 525.0, 450.0)
    display_gamma: float = 0.65

    def __post_init__(self):
        if not np.isfinite(self.stress_optic_pa_inv) or self.stress_optic_pa_inv <= 0:
            raise ValueError("Stress-optic coefficient must be finite and positive.")
        if len(self.wavelengths_nm) != 3 or not all(np.isfinite(w) and w > 0 for w in self.wavelengths_nm):
            raise ValueError("Exactly three positive wavelengths (R, G, B) are required.")
        if not np.isfinite(self.display_gamma) or self.display_gamma <= 0:
            raise ValueError("Display gamma must be finite and positive.")


def retardance(delta_sigma_mpa, thickness_mm, config=None):
    config = config or OpticalConfig()
    if not np.isfinite(thickness_mm) or thickness_mm <= 0:
        raise ValueError("Thickness must be finite and positive.")
    stress = np.asarray(delta_sigma_mpa, float)
    if not np.isfinite(stress).all() or (stress < 0).any():
        raise ValueError("Principal stress differences must be finite and nonnegative.")
    return (2 * np.pi * thickness_mm * 1e-3 * config.stress_optic_pa_inv *
            stress[..., None] * 1e6 / (np.asarray(config.wavelengths_nm) * 1e-9))


def optical_images(field, analyzer_deg=90.0, config=None, quarter_wave_deg=None):
    """Return linear RGB and retardance. Optional ideal QWP sits after specimen."""
    config = config or OpticalConfig()
    if not np.isfinite(analyzer_deg):
        raise ValueError("Analyzer angle must be finite.")
    D = retardance(field.delta_sigma_mpa, field.geometry.thickness_mm, config)
    c = np.cos(field.phi_rad)[..., None]
    s = np.sin(field.phi_rad)[..., None]
    ep, em = np.exp(0.5j * D), np.exp(-0.5j * D)
    ex, ey = c*c*ep + s*s*em, c*s*(ep-em)
    if quarter_wave_deg is not None:
        if not np.isfinite(quarter_wave_deg):
            raise ValueError("Quarter-wave plate angle must be finite.")
        beta = np.deg2rad(quarter_wave_deg)
        cb, sb = np.cos(beta), np.sin(beta)
        p, m = np.exp(0.25j*np.pi), np.exp(-0.25j*np.pi)
        ex, ey = ((cb*cb*p+sb*sb*m)*ex + cb*sb*(p-m)*ey,
                  cb*sb*(p-m)*ex + (sb*sb*p+cb*cb*m)*ey)
    alpha = np.deg2rad(analyzer_deg)
    rgb = np.clip(np.abs(np.cos(alpha)*ex + np.sin(alpha)*ey)**2, 0, 1)
    return {"rgb_linear": rgb, "retardances": D}


def camera_image(rgb_linear, photons=10000.0, read_noise=0.002, gains=(1, 1, 1),
                 offsets=(0, 0, 0), seed=42):
    """Normalized linear camera response; noise is applied before gain/offset."""
    rgb = np.asarray(rgb_linear, float)
    gains, offsets = np.asarray(gains, float), np.asarray(offsets, float)
    if rgb.ndim < 1 or rgb.shape[-1] != 3 or not np.isfinite(rgb).all() or np.any((rgb < 0) | (rgb > 1)):
        raise ValueError("Input must be finite linear RGB in [0, 1].")
    if not np.isfinite(photons) or photons <= 0 or not np.isfinite(read_noise) or read_noise < 0:
        raise ValueError("Photon count must be positive and read noise nonnegative.")
    if gains.shape != (3,) or offsets.shape != (3,) or not np.isfinite(gains).all() or not np.isfinite(offsets).all() or (gains <= 0).any():
        raise ValueError("Provide three positive gains and three finite offsets.")
    rng = np.random.default_rng(seed)
    noisy = rng.poisson(rgb * photons) / photons + rng.normal(0, read_noise, rgb.shape)
    return np.clip(noisy * gains + offsets, 0, 1)
