"""Portable CSV stress interchange and lossless simulation archives."""
from dataclasses import asdict
import json
import numpy as np
import pandas as pd
from .mechanics import Geometry, StressField

COLUMNS = ["x_mm", "y_mm", "sigma_x_mpa", "sigma_y_mpa", "tau_xy_mpa"]


def stress_csv(field):
    X, Y = np.meshgrid(field.x_mm, field.y_mm)
    return pd.DataFrame({"x_mm": X.ravel(), "y_mm": Y.ravel(),
                         "sigma_x_mpa": field.sigma_x_mpa.ravel(),
                         "sigma_y_mpa": field.sigma_y_mpa.ravel(),
                         "tau_xy_mpa": field.tau_xy_mpa.ravel(),
                         "material": field.outside.astype(int).ravel()}).to_csv(index=False)


def read_stress_csv(source, geometry=None):
    """Import a complete rectangular grid, optionally with material=0/1 masks.

    A solver's scattered element/nodal output must first be sampled to this grid.
    MPa is required explicitly; Pa must be converted by the exporter.
    """
    geometry = geometry or Geometry()
    df = pd.read_csv(source)
    if not set(COLUMNS).issubset(df.columns):
        raise ValueError("Stress CSV requires columns: " + ", ".join(COLUMNS))
    if df.duplicated(["x_mm", "y_mm"]).any():
        raise ValueError("Duplicate coordinate pairs are not allowed.")
    try:
        df[COLUMNS] = df[COLUMNS].apply(pd.to_numeric, errors="raise")
    except (ValueError, TypeError) as exc:
        raise ValueError("Stress CSV columns must be numeric.") from exc
    if not np.isfinite(df[COLUMNS].to_numpy()).all():
        raise ValueError("Stress CSV values must be finite, including zero values in holes.")
    x, y = np.sort(df.x_mm.unique()), np.sort(df.y_mm.unique())
    if len(df) != len(x)*len(y) or len(x) < 2 or len(y) < 2:
        raise ValueError("CSV must contain a complete rectangular grid with at least 2 × 2 points.")
    if any(not np.allclose(np.diff(axis), np.diff(axis)[0], rtol=1e-6, atol=1e-10) for axis in (x, y)):
        raise ValueError("CSV coordinates must be uniformly spaced for image rendering.")
    if not np.allclose([x[0], x[-1], y[0], y[-1]], geometry.extent):
        raise ValueError("CSV bounds must match the configured centered display window dimensions.")
    df = df.sort_values(["y_mm", "x_mm"])
    shape = (len(y), len(x))
    if "material" in df:
        if not df.material.isin([0, 1]).all():
            raise ValueError("The material mask must contain only 0 or 1.")
        outside = df.material.to_numpy().reshape(shape).astype(bool)
    else:
        X, Y = np.meshgrid(x, y)
        outside = np.hypot(X, Y) >= geometry.hole_radius_mm
    return StressField(x, y, *(df[name].to_numpy().reshape(shape) for name in COLUMNS[2:]),
                       outside, geometry, {"model": "Imported stress grid"})


def save_archive(path, field, optical, config):
    metadata = {"geometry": asdict(field.geometry), "optics": asdict(config), **field.metadata}
    np.savez_compressed(path, x_mm=field.x_mm, y_mm=field.y_mm,
                        sigma_x_mpa=field.sigma_x_mpa, sigma_y_mpa=field.sigma_y_mpa,
                        tau_xy_mpa=field.tau_xy_mpa, material=field.outside,
                        delta_sigma_mpa=field.delta_sigma_mpa, phi_rad=field.phi_rad,
                        rgb_linear=optical["rgb_linear"], retardance_rad=optical["retardances"],
                        metadata_json=json.dumps(metadata))
