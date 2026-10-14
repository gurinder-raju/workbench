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
