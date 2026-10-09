"""POLARIS-X scientific simulation tools. Coordinates: mm; stresses: MPa."""

from .mechanics import Geometry, StressField, kirsch
from .optics import OpticalConfig, optical_images

__all__ = ["Geometry", "StressField", "kirsch", "OpticalConfig", "optical_images"]
