"""Exportable scientific figures. Gamma is applied only to displayed images."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
from .optics import OpticalConfig, optical_images


def image_on_grid(ax, values, field, **kwargs):
    """Align image pixel centers with the supplied mechanical grid coordinates."""
    x, y = field.x_mm, field.y_mm
    dx, dy = x[1]-x[0], y[1]-y[0]
    if not np.allclose(np.diff(x), dx) or not np.allclose(np.diff(y), dy):
        raise ValueError("Image rendering requires a uniformly spaced stress grid.")
    extent = (x[0]-dx/2, x[-1]+dx/2, y[0]-dy/2, y[-1]+dy/2)
    image = ax.imshow(values, extent=extent, origin="lower", interpolation="nearest", **kwargs)
    ax.set_xlim(field.geometry.extent[:2])
    ax.set_ylim(field.geometry.extent[2:])
    return image


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
        im = image_on_grid(ax, np.ma.masked_where(~field.outside, values), field, cmap=cmap)
        fig.colorbar(im, ax=ax, label=unit, shrink=0.78)
        ax.set_title(title)
    rgb = optical["rgb_linear"]**config.display_gamma
    image_on_grid(axes[2], rgb, field)
    axes[2].set_title(f"Synthetic RGB · analyzer {analyzer_deg:g}°")
    for i, wavelength in enumerate(config.wavelengths_nm):
        image_on_grid(axes[i+3], rgb[..., i], field, cmap="gray", vmin=0, vmax=1)
        axes[i+3].set_title(f"{wavelength:g} nm normalized intensity")
    for ax in axes:
        decorate(ax, field)
    qwp = "" if quarter_wave_deg is None else f" · QWP {quarter_wave_deg:g}°"
    load = f" | {field.metadata['force_n']:g} N" if "force_n" in field.metadata else ""
    fig.suptitle(f"POLARIS-X | {field.metadata['model']}{load} | display γ={config.display_gamma:g}{qwp}\nSynthetic simulation · assumed material unless calibrated")
    return fig


def analyzer_figure(field, config=None, quarter_wave_deg=None):
    config = config or OpticalConfig()
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 6), layout="constrained")
    for ax, angle in zip(axes.ravel(), (0, 45, 90, 135)):
        rgb = optical_images(field, angle, config, quarter_wave_deg)["rgb_linear"]
        image_on_grid(ax, rgb**config.display_gamma, field)
        ax.set_title(f"Analyzer {angle}°" + (" · parallel" if angle == 0 else " · crossed" if angle == 90 else ""))
        decorate(ax, field)
    fig.suptitle(f"Rotating-analyzer virtual camera · same stress field · display γ={config.display_gamma:g}")
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
    accepted = result.valid & field.outside
    values = [truth, np.ma.masked_where(~accepted, result.delta_sigma_mpa),
              np.ma.masked_where(~accepted, 1.96*result.standard_error_mpa)]
    # A common scale must include accepted recovered outliers as well as truth.
    # Otherwise a wrong high-stress fringe branch is silently color-clipped.
    maximum = max(float(truth.max()), float(result.delta_sigma_mpa[accepted].max()) if accepted.any() else 0, 1e-12)
    for ax, value, title in zip(axes, values, ("Reference Δσ", "Recovered Δσ · accepted fits", "Approx. 95% interval half-width")):
        im = image_on_grid(ax, value, field, cmap="viridis", vmin=0,
                          vmax=maximum if ax is not axes[2] else None)
        fig.colorbar(im, ax=ax, label="MPa", shrink=0.7)
        ax.set_title(title)
        decorate(ax, field)
    fraction = accepted.sum()/field.outside.sum()
    error = result.delta_sigma_mpa[accepted]-field.delta_sigma_mpa[accepted]
    rmse = f" · RMSE {np.sqrt(np.mean(error**2)):.2f} MPa" if accepted.any() else ""
    load = f" · {field.metadata['force_n']:g} N" if "force_n" in field.metadata else ""
    fig.suptitle(f"Synthetic constrained inversion{load} · known principal-axis orientation\nAccepted material pixels: {fraction:.1%}{rmse} · local intervals exclude calibration/model error", fontsize=11)
    return fig
