"""Dimensioned cross-section diagram (matplotlib), saved next to the version's STL files."""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.patches import Rectangle

import params as P

TAG = P.TAG
GOLD, BACK, CROWN = "#d4b25f", "#b8954a", "#e0c070"


def load(name):
    return trimesh.load(P.STL_DIR / f"{TAG}_{name}.stl")


def crown_mesh():
    m = load("crown")
    T = trimesh.transformations
    m.apply_transform(T.translation_matrix((0, P.SPOT_FACE_Y + P.CROWN_GAP, P.Z_STEM))
                      @ T.rotation_matrix(math.radians(-90), (1, 0, 0)))
    return m


def draw_section(ax, x0, title):
    for m, col in [(load("case_body"), GOLD), (load("caseback_bridge"), BACK),
                   (crown_mesh(), CROWN), (load("movement_ring"), "#9aa3ad")]:
        sec = m.section(plane_origin=(x0, 0, 0), plane_normal=(1, 0, 0))
        if sec is None:
            continue
        T = np.eye(4)
        T[:3, :3] = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]   # world (y, z) -> plot (x, y)
        planar, _ = sec.to_2D(to_2D=T)
        for poly in planar.polygons_full:
            xs, ys = poly.exterior.xy
            ax.fill(xs, ys, color=col, ec="#4a3a10", lw=0.5)
            for hole in poly.interiors:
                hx, hy = hole.xy
                ax.fill(hx, hy, color="white", ec="#4a3a10", lw=0.5)
    # non-case parts for context
    ax.add_patch(Rectangle((-13.0, P.Z_MOVT_BOT), 26.0, P.MOVT_H, fc="#cfd5db", ec="#6b7480", lw=0.6))
    ax.text(0, P.Z_MOVT_BOT + P.MOVT_H / 2, "Miyota 9039  26.0 x 3.90", ha="center", va="center", fontsize=7)
    ax.add_patch(Rectangle((-P.R_DIAL, P.Z_MOVT_TOP), 2 * P.R_DIAL, P.DIAL_T, fc="white", ec="#555", lw=0.6))
    ax.add_patch(Rectangle((-P.R_CRYSTAL, P.Z_CRYSTAL_BOT), 2 * P.R_CRYSTAL, P.CRYSTAL_T,
                           fc="#d8ecf7", ec="#6aa0c0", lw=0.6, alpha=0.8))
    ax.plot([-0.4, -0.4], [P.Z_DIAL_TOP, P.Z_DIAL_TOP + P.HAND_STACK], color="#c33", lw=2)
    st = 2.4
    if abs(x0) < P.STRAP_W / 2:
        ax.add_patch(Rectangle((-24, P.Z_TUNNEL_FLOOR + 0.2), 48, st, fc="#222", ec="#000", lw=0.5, alpha=0.85))
        ax.text(-23.5, P.Z_TUNNEL_FLOOR + 0.2 + st / 2, "22 mm strap", color="w", fontsize=6, va="center")
    ax.set_title(title, fontsize=9)
    ax.set_aspect("equal")
    ax.set_xlim(-25, 27)
    ax.set_ylim(-2.5, 16.5)
    ax.axhline(0, color="#bbb", lw=0.4)
    ax.set_xlabel("mm  (6 o'clock  <-   ->  12 o'clock)", fontsize=7)
    ax.tick_params(labelsize=6)


def dim(ax, x, z0, z1, text, side=1):
    ax.annotate("", (x, z0), (x, z1), arrowprops=dict(arrowstyle="<->", lw=0.6, color="#333"))
    ax.text(x + 0.3 * side, (z0 + z1) / 2, text, fontsize=6, va="center", ha="left" if side > 0 else "right")


def main():
    fig, axs = plt.subplots(2, 1, figsize=(10, 8.4), dpi=170)
    draw_section(axs[0], 0.0, "Section through 12-6 axis (crown, strap tunnel, bridge)")
    a = axs[0]
    dim(a, -22.5, 0, P.Z_TOP, "%.2f total" % P.Z_TOP, -1)
    dim(a, 2.0, 0, P.Z_TUNNEL_FLOOR, "bridge %.1f" % P.BRIDGE_T)
    dim(a, 9.0, P.Z_TUNNEL_FLOOR, P.Z_TUNNEL_CEIL, "tunnel %.1f" % P.TUNNEL_H)
    dim(a, 9.0, P.Z_TUNNEL_CEIL, P.Z_PARTING, "caseback %.1f" % P.BACK_PLATE_T)
    dim(a, 15.0, P.Z_DIAL_TOP, P.Z_CRYSTAL_BOT, "hands+gap %.2f" % (P.HAND_STACK + P.HAND_CLEAR))
    a.annotate("", (-P.BRIDGE_L / 2, -1.6), (P.BRIDGE_L / 2, -1.6), arrowprops=dict(arrowstyle="<->", lw=0.6))
    a.text(0, -2.2, "bridge %.0f mm long (12-6)" % P.BRIDGE_L, ha="center", fontsize=6)
    a.text(24.6, P.Z_STEM + 3.6, "crown at 12\nstem axis z=%.2f" % P.Z_STEM, fontsize=6, ha="center")

    draw_section(axs[1], P.SCREW_X, "Section at x = %.1f mm (caseback screws, 2 at 12 + 2 at 6)" % P.SCREW_X)
    b = axs[1]
    for sy in (-1, 1):
        b.annotate("M1.4 screw\nhidden under strap", (sy * P.SCREW_Y, P.Z_TUNNEL_CEIL + 0.3),
                   (sy * 13.5, -1.8), fontsize=6, ha="center",
                   arrowprops=dict(arrowstyle="->", lw=0.6))
    fig.tight_layout()
    out = P.STL_DIR / f"GH_watch_case_{P.VERSION}_section.png"
    fig.savefig(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
