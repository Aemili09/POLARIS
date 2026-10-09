"""Analytical mechanics and a common, explicitly unit-labelled field format."""
from dataclasses import dataclass, field
import numpy as np


@dataclass(frozen=True)
class Geometry:
    length_mm: float = 100.0
    width_mm: float = 40.0
    hole_radius_mm: float = 5.0
    thickness_mm: float = 5.0
    reference_width_mm: float = 40.0

    def __post_init__(self):
        values = tuple(vars(self).values())
        if not all(np.isfinite(v) and v > 0 for v in values):
            raise ValueError("All geometry dimensions must be finite and positive.")
        if 2 * self.hole_radius_mm >= min(self.length_mm, self.width_mm):
            raise ValueError("The circular hole must fit strictly inside the plate.")

    @property
    def extent(self):
        return (-self.length_mm / 2, self.length_mm / 2, -self.width_mm / 2, self.width_mm / 2)


@dataclass
class StressField:
    x_mm: np.ndarray
    y_mm: np.ndarray
    sigma_x_mpa: np.ndarray
    sigma_y_mpa: np.ndarray
    tau_xy_mpa: np.ndarray
    outside: np.ndarray
    geometry: Geometry
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        self.x_mm = np.asarray(self.x_mm, dtype=float)
        self.y_mm = np.asarray(self.y_mm, dtype=float)
        for coords in (self.x_mm, self.y_mm):
            if coords.ndim != 1 or len(coords) < 2 or not np.isfinite(coords).all() or not (np.diff(coords) > 0).all():
                raise ValueError("Coordinates must be finite, strictly increasing 1D arrays.")
        shape = (len(self.y_mm), len(self.x_mm))
        self.outside = np.asarray(self.outside, dtype=bool)
        if self.outside.shape != shape or not self.outside.any():
            raise ValueError("Material mask must match the grid and contain material points.")
        for name in ("sigma_x_mpa", "sigma_y_mpa", "tau_xy_mpa"):
            value = np.asarray(getattr(self, name), dtype=float)
            if value.shape != shape or not np.isfinite(value[self.outside]).all():
                raise ValueError("Stress arrays must match the grid and be finite in material.")
            setattr(self, name, np.where(self.outside, value, 0.0))

    @property
    def delta_sigma_mpa(self):
        return np.hypot(self.sigma_x_mpa - self.sigma_y_mpa, 2 * self.tau_xy_mpa)

    @property
    def phi_rad(self):
        return 0.5 * np.arctan2(2 * self.tau_xy_mpa, self.sigma_x_mpa - self.sigma_y_mpa)


def grid(geometry, nx, ny):
    if any(not isinstance(n, (int, np.integer)) or isinstance(n, bool) or n < 3 for n in (nx, ny)):
        raise ValueError("Grid dimensions must be integers of at least 3.")
    x = np.linspace(-geometry.length_mm / 2, geometry.length_mm / 2, nx)
    y = np.linspace(-geometry.width_mm / 2, geometry.width_mm / 2, ny)
    return x, y, np.meshgrid(x, y)


def validate_force(force_n):
    if not np.isfinite(force_n) or force_n < 0:
        raise ValueError("Force must be finite and nonnegative.")


def kirsch_at(x_mm, y_mm, remote_mpa, hole_radius_mm):
    """Kirsch stresses at arbitrary points; the clear hole is assigned zero stress."""
    if not np.isfinite(remote_mpa) or remote_mpa < 0 or not np.isfinite(hole_radius_mm) or hole_radius_mm <= 0:
        raise ValueError("Remote tension must be nonnegative and hole radius positive.")
    x, y = np.broadcast_arrays(np.asarray(x_mm, float), np.asarray(y_mm, float))
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Coordinates must be finite.")
    r = np.hypot(x, y)
    theta = np.arctan2(y, x)
    q = (hole_radius_mm / np.maximum(r, hole_radius_mm)) ** 2
    s = remote_mpa
    rr = s / 2 * (1 - q) + s / 2 * (1 - 4*q + 3*q*q) * np.cos(2*theta)
    tt = s / 2 * (1 + q) - s / 2 * (1 + 3*q*q) * np.cos(2*theta)
    rt = -s / 2 * (1 + 2*q - 3*q*q) * np.sin(2*theta)
    c, t = np.cos(theta), np.sin(theta)
    outside = r >= hole_radius_mm * (1 - 1e-12)
    sx = rr*c*c + tt*t*t - 2*rt*t*c
    sy = rr*t*t + tt*c*c + 2*rt*t*c
    xy = (rr-tt)*t*c + rt*(c*c-t*t)
    return tuple(np.where(outside, a, 0.0) for a in (sx, sy, xy))


def kirsch(force_n=1000.0, geometry=None, nx=551, ny=241):
    geometry = geometry or Geometry()
    validate_force(force_n)
    x, y, (X, Y) = grid(geometry, nx, ny)
    remote = force_n / (geometry.reference_width_mm * geometry.thickness_mm)
    stresses = kirsch_at(X, Y, remote, geometry.hole_radius_mm)
    return StressField(x, y, *stresses, np.hypot(X, Y) >= geometry.hole_radius_mm,
                       geometry, {"model": "Kirsch infinite plate", "force_n": force_n,
                                  "remote_mpa": remote, "force_is_nominal_reference": True})
