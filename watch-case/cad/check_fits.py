"""Fit check: drop the chosen M1.4 x 4 wafer-head screw (head 2.5 x 0.5)
into each caseback position and measure the thinnest walls, on the exported meshes."""
import warnings
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Point

import params as P

warnings.filterwarnings("ignore")
body = trimesh.load(P.STL_DIR / f"{P.TAG}_case_body.stl")
back = trimesh.load(P.STL_DIR / f"{P.TAG}_caseback_bridge.stl")

HEAD_D, HEAD_K, SHANK_D, LENGTH = 2.5, 0.5, 1.4, 4.0
seat = P.Z_TUNNEL_CEIL + P.SCREW_HEAD_DEPTH          # head bearing face


def screw(x, y):
    head = trimesh.creation.cylinder(HEAD_D / 2, HEAD_K, sections=64)
    head.apply_translation((x, y, seat - HEAD_K / 2))
    shank = trimesh.creation.cylinder(SHANK_D / 2 - 0.01, LENGTH, sections=64)
    shank.apply_translation((x, y, seat + LENGTH / 2))
    return head, shank


def overlap(a, b):
    try:
        i = trimesh.boolean.intersection([a, b], engine="manifold")
        return 0.0 if i.is_empty else i.volume
    except Exception:
        return float("nan")


def ring_walls(mesh, z, x, y):
    """Min wall from the hole around (x, y) to any other boundary of the slice at z."""
    sec = mesh.section(plane_origin=(0, 0, z), plane_normal=(0, 0, 1))
    T = np.eye(4)
    planar, to3d = sec.to_2D(to_2D=T)
    c = Point(x, y)
    for poly in planar.polygons_full:
        rings = list(poly.interiors)
        for k, hole in enumerate(rings):
            if trimesh.path.polygons.Polygon(hole).contains(c):
                others = [poly.exterior] + [h for j, h in enumerate(rings) if j != k]
                return min(hole.distance(o) for o in others)
    return None


print("standard M1.4 x %.0f: head %.1f x %.1f, shank %.1f" % (LENGTH, HEAD_D, HEAD_K, SHANK_D))
print("head seat z=%.2f, head bottom z=%.2f, tunnel ceiling z=%.2f -> head recessed %.2f mm"
      % (seat, seat - HEAD_K, P.Z_TUNNEL_CEIL, seat - HEAD_K - P.Z_TUNNEL_CEIL))
print("screw tip z=%.2f, pilot hole bottom z=%.2f" % (seat + LENGTH, P.Z_PARTING + P.SCREW_THREAD_DEPTH))
print("thread engagement in body: %.2f mm" % (seat + LENGTH - P.Z_PARTING))
for sx in (-1, 1):
    for sy in (-1, 1):
        x, y = sx * P.SCREW_X, sy * P.SCREW_Y
        head, shank = screw(x, y)
        hv = overlap(head, back)
        sv = overlap(shank, back)
        print("screw at (%5.2f, %6.2f): head hits caseback %.4f mm3, shank hits caseback %.4f mm3"
              % (x, y, hv, sv))
x, y = P.SCREW_X, P.SCREW_Y
for z in (P.Z_TUNNEL_CEIL + 0.05, P.Z_TUNNEL_CEIL + 0.5, seat - 0.05):
    print("  caseback wall around head seat at z=%.2f: %.2f mm" % (z, ring_walls(back, z, x, y)))
for z in (seat + 0.3, P.Z_PARTING - 0.2):
    print("  caseback wall around clearance hole at z=%.2f: %.2f mm" % (z, ring_walls(back, z, x, y)))
for z in (P.Z_PARTING + 0.1, P.Z_PARTING + 1.5, P.Z_PARTING + P.SCREW_THREAD_DEPTH - 0.2):
    print("  body wall around pilot hole at z=%.2f: %.2f mm" % (z, ring_walls(body, z, x, y)))
print("plate under the head: %.2f mm" % (P.Z_PARTING - seat))

# ---- V9 seals ---------------------------------------------------------------
print()
print("seals:")
cg = P.CRYSTAL_GASKET_WALL
print("  crystal: 34.0 crystal + %.2f I-ring -> %.2f free, seat %.2f, squeeze %.2f/side (%.0f %%)"
      % (cg, 2 * (P.R_CRYSTAL + cg), 2 * P.R_CRYSTAL_SEAT, P.CRYSTAL_GASKET_SQUEEZE,
         100 * P.CRYSTAL_GASKET_SQUEEZE / cg))
sq = (P.BACK_ORING_CS - (2 * P.R_BORE - P.BACK_GROOVE_D) / 2)
print("  caseback: %.1f x %.1f O-ring on a %.2f groove (stretch %.1f %%), bore %.2f, squeeze %.0f %%,"
      " groove fill %.0f %%" % (P.BACK_ORING_ID, P.BACK_ORING_CS, P.BACK_GROOVE_D,
         100 * (P.BACK_GROOVE_D / P.BACK_ORING_ID - 1), 2 * P.R_BORE, 100 * sq / P.BACK_ORING_CS,
         100 * (3.1416 / 4 * P.BACK_ORING_CS ** 2) / (P.BACK_GROOVE_W * (2 * P.R_BORE - P.BACK_GROOVE_D) / 2)))
sq = (P.CROWN_ORING_CS - (P.CROWN_GROOVE_D - 3.0) / 2)
print("  crown: %.1f x %.1f O-ring in a %.2f groove on the 3.0 tube end, squeeze %.0f %%,"
      " groove fill %.0f %%" % (P.CROWN_ORING_ID, P.CROWN_ORING_CS, P.CROWN_GROOVE_D,
         100 * sq / P.CROWN_ORING_CS,
         100 * (3.1416 / 4 * P.CROWN_ORING_CS ** 2) / (P.CROWN_GROOVE_W * (P.CROWN_GROOVE_D - 3.0) / 2)))
proud = 2.5 - P.TUBE_SHOULDER_DEPTH
print("  tube crown end proud of the counterbore floor %.2f; crown face gap %.2f -> engagement %.2f,"
      " end clearance %.2f" % (proud, P.CROWN_GAP, proud - P.CROWN_GAP,
                                P.CROWN_BORE_DEPTH - (proud - P.CROWN_GAP)))
print("  tube case end %.2f long in a %.2f hole (stops %.2f short of the bore)"
      % (5.5 - 2.5, P.SPOT_FACE_Y - P.TUBE_SHOULDER_DEPTH - P.R_BORE,
         P.SPOT_FACE_Y - P.TUBE_SHOULDER_DEPTH - P.R_BORE - 3.0))
ring = trimesh.load(P.STL_DIR / f"{P.TAG}_movement_ring.stl")
for a, b, na, nb in ((body, back, "body", "caseback"), (body, ring, "body", "ring"),
                     (back, ring, "caseback", "ring")):
    print("  overlap %s / %s: %.4f mm3" % (na, nb, overlap(a, b)))
crown = trimesh.load(P.STL_DIR / f"{P.TAG}_crown.stl")
sec = crown.section(plane_origin=(0, 0, P.CROWN_GROOVE_Z + P.CROWN_GROOVE_W / 2), plane_normal=(0, 0, 1))
pl, _ = sec.to_2D(to_2D=np.eye(4))
poly = max(pl.polygons_full, key=lambda p: p.area)
print("  crown wall outside the O-ring groove: %.2f mm" % poly.exterior.distance(poly.interiors[0]))
sec = crown.section(plane_origin=(0, 0, P.CROWN_BORE_DEPTH + P.CROWN_STEM_HOLE_DEPTH + 0.1),
                    plane_normal=(0, 0, 1))
print("  crown top above the stem hole: solid=%s" % (sec is not None))
