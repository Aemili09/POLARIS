"""Small-strain, constant-strain triangle (CST) plane-stress finite elements.

mm, N and MPa are consistent units. The hole is a polygonal approximation.
No external FEA executable or proprietary solver is required.
"""
from dataclasses import dataclass
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from matplotlib.tri import Triangulation, LinearTriInterpolator
from .mechanics import Geometry, StressField, grid, validate_force


@dataclass
class FEAResult:
    field: StressField
    nodes_mm: np.ndarray
    triangles: np.ndarray
    displacement_mm: np.ndarray
    element_stress_mpa: np.ndarray
    reaction_n: np.ndarray
    diagnostics: dict


def annular_mesh(geometry, radial=20, angular=96):
    if not isinstance(radial, (int, np.integer)) or not isinstance(angular, (int, np.integer)) or radial < 3 or angular < 16:
        raise ValueError("Mesh needs at least 3 radial layers and 16 angular divisions.")
    corner = np.arctan2(geometry.width_mm, geometry.length_mm)
    angles = np.unique(np.round(np.r_[np.linspace(0, 2*np.pi, angular, endpoint=False),
                                       corner, np.pi-corner, np.pi+corner, 2*np.pi-corner,
                                       0, np.pi/2, np.pi, 3*np.pi/2], 12))
    c, s = np.cos(angles), np.sin(angles)
    outer = np.minimum(geometry.length_mm / (2*np.maximum(np.abs(c), 1e-15)),
                       geometry.width_mm / (2*np.maximum(np.abs(s), 1e-15)))
    # More radial resolution near the stress concentration at the hole.
    fraction = np.linspace(0, 1, radial+1)**1.5
    radii = geometry.hole_radius_mm + fraction[:, None]*(outer-geometry.hole_radius_mm)
    nodes = np.stack((radii*c, radii*s), axis=-1).reshape(-1, 2)
    n = len(angles)
    # Trigonometric construction can put an outer node ~1e-14 mm inside
    # the intended rectangle, causing exact boundary samples to be masked by
    # the triangle locator. Make the known rectangular edges exact.
    outer_nodes = nodes[-n:]
    for axis, half in ((0, geometry.length_mm/2), (1, geometry.width_mm/2)):
        for edge in (-half, half):
            on_edge = np.isclose(outer_nodes[:, axis], edge, atol=1e-10, rtol=0)
            outer_nodes[on_edge, axis] = edge
    triangles = []
    for j in range(radial):
        for k in range(n):
            p, q = j*n+k, j*n+(k+1)%n
            triangles.extend(((p, p+n, q+n), (p, q+n, q)))
    return nodes, np.asarray(triangles)


def element_matrices(nodes, triangles, young_mpa, poisson):
    xy = nodes[triangles]
    x, y = xy[:, :, 0], xy[:, :, 1]
    twice_area = (x[:, 1]-x[:, 0])*(y[:, 2]-y[:, 0]) - (x[:, 2]-x[:, 0])*(y[:, 1]-y[:, 0])
    if np.any(twice_area <= 0):
        raise ValueError("Mesh contains inverted or degenerate elements.")
    b = np.stack((y[:, 1]-y[:, 2], y[:, 2]-y[:, 0], y[:, 0]-y[:, 1]), axis=1)
    c = np.stack((x[:, 2]-x[:, 1], x[:, 0]-x[:, 2], x[:, 1]-x[:, 0]), axis=1)
    B = np.zeros((len(triangles), 3, 6))
    B[:, 0, 0::2] = b
    B[:, 1, 1::2] = c
    B[:, 2, 0::2] = c
    B[:, 2, 1::2] = b
    B /= twice_area[:, None, None]
    D = young_mpa/(1-poisson**2)*np.array([[1, poisson, 0], [poisson, 1, 0], [0, 0, (1-poisson)/2]])
    return B, D, twice_area/2


def solve_plate(force_n=1000.0, geometry=None, young_mpa=3000.0, poisson=0.35,
                radial=20, angular=96, nx=301, ny=121, grip="roller", load_profile="uniform"):
    """Left ux fixed; roller grip anchors one uy, clamped fixes all left uy.

    Right-edge x traction is uniform or parabolic, normalized to force_n.
    The top, bottom and hole boundaries are traction-free.
    """
    geometry = geometry or Geometry()
    validate_force(force_n)
    if not np.isfinite(young_mpa) or young_mpa <= 0 or not np.isfinite(poisson) or not -1 < poisson < 0.5:
        raise ValueError("Young's modulus must be positive; Poisson ratio must lie in (-1, 0.5).")
    if grip not in ("roller", "clamped") or load_profile not in ("uniform", "parabolic"):
        raise ValueError("Unsupported grip or load profile.")
    nodes, tri = annular_mesh(geometry, radial, angular)
    B, D, areas = element_matrices(nodes, tri, young_mpa, poisson)
    local = np.einsum('eji,jk,ekl->eil', B, D, B) * (areas*geometry.thickness_mm)[:, None, None]
    dofs = np.stack((2*tri, 2*tri+1), axis=-1).reshape(-1, 6)
    rows = np.broadcast_to(dofs[:, :, None], local.shape).ravel()
    cols = np.broadcast_to(dofs[:, None, :], local.shape).ravel()
    ndof = 2*len(nodes)
    K = coo_matrix((local.ravel(), (rows, cols)), shape=(ndof, ndof)).tocsr()
    left = np.flatnonzero(np.isclose(nodes[:, 0], -geometry.length_mm/2, atol=1e-8, rtol=0))
    right = np.flatnonzero(np.isclose(nodes[:, 0], geometry.length_mm/2, atol=1e-8, rtol=0))
    right = right[np.argsort(nodes[right, 1])]
    f = np.zeros(ndof)
    # Two-point Gauss integration of linearly interpolated nodal edge forces.
    for p, q in zip(right[:-1], right[1:]):
        length = nodes[q, 1]-nodes[p, 1]
        for xi in (-1/np.sqrt(3), 1/np.sqrt(3)):
            N = np.array([(1-xi)/2, (1+xi)/2])
            ypos = N @ nodes[[p, q], 1]
            weight = 1.0 if load_profile == "uniform" else 1-(2*ypos/geometry.width_mm)**2
            f[2*np.array([p, q])] += N*length/2*weight
    f *= force_n/f.sum()
    fixed = np.r_[2*left, 2*left+1 if grip == "clamped" else [2*left[np.argmin(np.abs(nodes[left, 1]))]+1]]
    free = np.setdiff1d(np.arange(ndof), fixed)
    u = np.zeros(ndof)
    u[free] = spsolve(K[free][:, free], f[free])
    if not np.isfinite(u).all():
        raise RuntimeError("FEA failed: non-finite displacement solution.")
    reaction = K @ u - f
    stresses = np.einsum('ij,ejk,ek->ei', D, B, u[dofs])
    # Area-weighted nodal stress recovery, then interpolation over the actual mesh.
    nodal = np.zeros((len(nodes), 3))
    weights = np.zeros(len(nodes))
    for k in range(3):
        np.add.at(nodal, tri[:, k], stresses*areas[:, None])
        np.add.at(weights, tri[:, k], areas)
    nodal /= weights[:, None]
    x, y, (X, Y) = grid(geometry, nx, ny)
    triangulation = Triangulation(nodes[:, 0], nodes[:, 1], tri)
    values = [LinearTriInterpolator(triangulation, nodal[:, k])(X, Y).filled(np.nan) for k in range(3)]
    outside = (np.hypot(X, Y) >= geometry.hole_radius_mm) & np.logical_and.reduce([np.isfinite(a) for a in values])
    diagnostics = {"nodes": len(nodes), "elements": len(tri), "applied_force_n": float(f[0::2].sum()),
                   "reaction_x_n": float(reaction[0::2].sum()), "reaction_y_n": float(reaction[1::2].sum()),
                   "relative_free_residual": float(np.linalg.norm(reaction[free])/max(force_n, 1)),
                   "strain_energy_n_mm": float(0.5*u @ (K@u)),
                   "maximum_displacement_mm": float(np.linalg.norm(u.reshape(-1, 2), axis=1).max()),
                   "peak_element_principal_difference_mpa": float(np.hypot(stresses[:, 0]-stresses[:, 1], 2*stresses[:, 2]).max())}
    field = StressField(x, y, *values, outside, geometry,
                        {"model": "Finite plate CST plane stress", "force_n": force_n,
                         "remote_mpa": force_n/(geometry.width_mm*geometry.thickness_mm),
                         "young_mpa": young_mpa, "poisson": poisson, "grip": grip,
                         "load_profile": load_profile, "stress_recovery": "area-weighted nodal averaging",
                         **diagnostics})
    return FEAResult(field, nodes, tri, u.reshape(-1, 2), stresses, reaction.reshape(-1, 2), diagnostics)
