"""Exportable scientific figures. Gamma is applied only to displayed images."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from .optics import OpticalConfig, optical_images


def decorate(ax, field):
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.add_patch(Circle((0, 0), field.geometry.hole_radius_mm, fill=False,
                        linestyle="--", linewidth=1, edgecolor="white", alpha=0.8))


def main_figure(field, analyzer_deg=90, config=None, quarter_wave_deg=None):
    config = config or OpticalConfig()
    optical = optical_images(field, analyzer_deg, config, quarter_wave_deg)
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), layout="constrained")
    axes = axes.ravel()
    for ax, values, title, unit, cmap in (
        (axes[0], field.delta_sigma_mpa, "Principal stress difference", "MPa", "inferno"),
        (axes[1], optical["retardances"][..., 1], f"Phase retardation ({config.wavelengths_nm[1]:g} nm)", "rad", "viridis"),
    ):
        im = ax.imshow(np.ma.masked_where(~field.outside, values), extent=field.geometry.extent, origin="lower", cmap=cmap)
        fig.colorbar(im, ax=ax, label=unit, shrink=0.78)
        ax.set_title(title)
    rgb = optical["rgb_linear"]**config.display_gamma
    axes[2].imshow(rgb, extent=field.geometry.extent, origin="lower")
    axes[2].set_title(f"Synthetic RGB · analyzer {analyzer_deg:g}°")
    for i, wavelength in enumerate(config.wavelengths_nm):
        axes[i+3].imshow(rgb[..., i], extent=field.geometry.extent, origin="lower", cmap="gray", vmin=0, vmax=1)
        axes[i+3].set_title(f"{wavelength:g} nm normalized intensity")
    for ax in axes:
        decorate(ax, field)
    qwp = "" if quarter_wave_deg is None else f" · QWP {quarter_wave_deg:g}°"
    fig.suptitle(f"POLARIS-X | {field.metadata['model']} | display γ={config.display_gamma:g}{qwp}\nSynthetic simulation · assumed material unless calibrated")
    return fig


def analyzer_figure(field, config=None, quarter_wave_deg=None):
    config = config or OpticalConfig()
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 6), layout="constrained")
    for ax, angle in zip(axes.ravel(), (0, 45, 90, 135)):
        rgb = optical_images(field, angle, config, quarter_wave_deg)["rgb_linear"]
        ax.imshow(rgb**config.display_gamma, extent=field.geometry.extent, origin="lower")
        ax.set_title(f"Analyzer {angle}°" + (" · parallel" if angle == 0 else " · crossed" if angle == 90 else ""))
        decorate(ax, field)
    fig.suptitle("Rotating-analyzer virtual camera · same stress field")
    return fig


def deformation_figure(result, scale=100.0):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), layout="constrained")
    nodes = result.nodes_mm
    axes[0].triplot(nodes[:, 0], nodes[:, 1], result.triangles, color="#8697a8", linewidth=0.3)
    axes[0].set_title("Finite-element mesh")
    shifted = nodes + scale*result.displacement_mm
    image = axes[1].tripcolor(shifted[:, 0], shifted[:, 1], result.triangles,
                              np.linalg.norm(result.displacement_mm, axis=1), shading="gouraud", cmap="viridis")
    fig.colorbar(image, ax=axes[1], label="Displacement magnitude (mm)")
    axes[1].set_title(f"Deformation · displacement magnified {scale:g}×")
    for ax in axes:
        ax.set_aspect("equal")
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
    return fig


def reconstruction_figure(field, result):
    fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")
    truth = np.ma.masked_where(~field.outside, field.delta_sigma_mpa)
    values = [truth, np.ma.masked_where(~result.valid | ~field.outside, result.delta_sigma_mpa),
              np.ma.masked_where(~result.valid | ~field.outside, 1.96*result.standard_error_mpa)]
    for ax, value, title in zip(axes, values, ("Reference Δσ", "Recovered Δσ · valid pixels", "Approx. 95% interval half-width")):
        im = ax.imshow(value, extent=field.geometry.extent, origin="lower", cmap="viridis", vmin=0,
                       vmax=float(truth.max()) if ax is not axes[2] else None)
        fig.colorbar(im, ax=ax, label="MPa", shrink=0.7)
        ax.set_title(title)
        decorate(ax, field)
    return fig
