"""V8 42 mm pebble case - parametric build123d model.

Builds four parts and exports STL (printing) + STEP (CAD / CNC):
    case_body       - pebble upper shell, crystal seat, rehaut, movement bore,
                      crown tube at 12, M1.4 tapped holes for the caseback
    caseback_bridge - lower shell that continues the pebble, locating spigot,
                      strap tunnel 12->6 with a short bridge, 4 screw seats
    crown           - clous de Paris crown (2 rows x 16 pyramids)
    movement_ring   - spacer that holds the 26 mm Miyota in the 33.5 mm bore

Run:  python watch.py  [outdir]
"""
import math
import sys
from pathlib import Path

import numpy as np
from build123d import (
    Axis, Box, Cylinder, Edge, Face, Line, Location, Plane, Polyline, Pos, Rot,
    Spline, Vector, Wire, export_step, export_stl, extrude, fillet, revolve, Compound,
)

import params as P
from profile import profile_points

TAG = P.TAG
BIG = 200.0


def revolve_rz(pts_rz):
    """Revolve a closed polygon given in (r, z) about the Z axis."""
    pts = [Vector(r, 0, z) for r, z in pts_rz]
    face = Face(Wire(Polyline(*pts, close=True)))
    return revolve(face, Axis.Z, 360)


def pebble_solid():
    """Whole outer shape: one continuous, curvature-smooth pebble."""
    pts, _ = profile_points(n=110)
    vecs = [Vector(r, 0, z) for r, z in pts]
    # no forced end tangents: they create a hook; the fitted ends are within 0.1 deg
    curve = Spline(*vecs)
    top = Vector(0, 0, P.Z_TOP)
    face = Face(Wire([Line(top, vecs[0]), curve, Line(vecs[-1], top)]))
    return revolve(face, Axis.Z, 360)


def slab(z0, z1):
    return Pos(0, 0, (z0 + z1) / 2) * Box(BIG, BIG, z1 - z0)


def crown_axis_loc(y):
    # local +Z of a part -> global +Y, positioned on the stem axis
    return Location((0, y, P.Z_STEM), (-90, 0, 0))


def build_body(peb):
    body = peb & slab(P.Z_PARTING, P.Z_TOP + 1)
    ch = 0.20  # small chamfer on the crystal-seat edge -> thin bright ring
    inner = revolve_rz([
        (0, P.Z_PARTING - 1),
        (P.R_BORE, P.Z_PARTING - 1),
        (P.R_BORE, P.Z_DIAL_TOP),
        (P.R_REHAUT, P.Z_DIAL_TOP),
        (P.R_REHAUT, P.Z_CRYSTAL_BOT),
        (P.R_CRYSTAL + P.CRYSTAL_SEAT_CLEAR, P.Z_CRYSTAL_BOT),
        (P.R_CRYSTAL + P.CRYSTAL_SEAT_CLEAR, P.Z_TOP - ch),
        (P.R_CRYSTAL + P.CRYSTAL_SEAT_CLEAR + ch, P.Z_TOP),
        (P.R_CRYSTAL + P.CRYSTAL_SEAT_CLEAR + ch, P.Z_TOP + 1),
        (0, P.Z_TOP + 1),
    ])
    body = body - inner
    # crown tube bore + counterbore for the crown collar at 12
    tube = crown_axis_loc(P.R_BORE - 1) * Pos(0, 0, 4) * Cylinder(P.TUBE_HOLE_D / 2, 8)
    spot = crown_axis_loc(P.SPOT_FACE_Y) * Pos(0, 0, 5) * Cylinder(P.SPOT_FACE_R, 10)
    body = body - tube - spot
    # tapped holes for caseback screws
    for sx in (-1, 1):
        for sy in (-1, 1):
            hole = Pos(sx * P.SCREW_X, sy * P.SCREW_Y,
                       P.Z_PARTING + P.SCREW_THREAD_DEPTH / 2 - 0.01) * Cylinder(
                P.SCREW_TAP_D / 2, P.SCREW_THREAD_DEPTH)
            body = body - hole
    return body


def build_caseback(peb):
    lower = peb & slab(-1, P.Z_PARTING)
    # strap channel straight through 12 -> 6, minus a short bridge under the strap.
    # The bridge is carved out of the cutting tool (not fused afterwards) so it
    # shares the pebble's wrist-side surface exactly.
    ceil = P.Z_TUNNEL_CEIL
    lane = Pos(0, 0, (ceil - 2) / 2) * Box(P.LANE_W, BIG, ceil + 2)
    # bridge section in the YZ plane; ends rounded so the strap can drape
    half = P.BRIDGE_L / 2
    rt, rb = 0.9, 1.0
    zt, zb = P.Z_TUNNEL_FLOOR, -0.8
    n = 10
    sec = []
    for k in range(n + 1):  # top corner: round over the strap edge
        a = math.pi / 2 * k / n
        sec.append((half - rt + rt * math.sin(a), zt - rt + rt * math.cos(a)))
    for k in range(n + 1):  # bottom corner
        a = math.pi / 2 * k / n
        sec.append((half - rb + rb * math.cos(a), zb + rb - rb * math.sin(a)))
    sec += [(-y, z) for y, z in reversed(sec)]
    pts = [Vector(0, y, z) for y, z in sec]
    face = Face(Wire(Polyline(*pts, close=True)))
    bridge = extrude(Pos(-(P.LANE_W / 2 + 0.6), 0, 0) * face, amount=P.LANE_W + 1.2, dir=(1, 0, 0))
    lower = lower - (lane - bridge)
    # round the tunnel exits at 12 and 6 where the strap bends over the ceiling edge
    from build123d import GeomType
    exits = [e for e in lower.edges()
             if e.geom_type == GeomType.BSPLINE and abs(e.center().Y) > P.BRIDGE_L / 2
             and abs(e.center().Z - P.Z_TUNNEL_CEIL) < 0.05]
    lower = fillet(exits, 0.8)
    # 4 screws in the channel ceiling past the bridge (2 at 12, 2 at 6):
    # heads sit flush in counterbores, hidden under the strap when worn.
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * P.SCREW_X, sy * P.SCREW_Y
            clr = Pos(x, y, P.Z_PARTING - 1) * Cylinder(P.SCREW_CLEAR_D / 2, 4)
            cb_top = P.Z_TUNNEL_CEIL + P.SCREW_HEAD_DEPTH
            cb = Pos(x, y, cb_top - 1) * Cylinder(P.SCREW_HEAD_D / 2, 2)
            lower = lower - clr - cb
    return lower


def build_crown():
    R = P.CROWN_D / 2
    H = P.CROWN_SKIRT_H + P.CROWN_KNURL_ROWS * P.CROWN_ROW_H
    z0 = P.CROWN_SKIRT_H
    skirt = Pos(0, 0, z0 / 2) * Cylinder(P.CROWN_SKIRT_D / 2, z0)
    knurl = Pos(0, 0, z0 + (H - z0) / 2) * Cylinder(R, H - z0)
    crown = skirt + knurl
    depth = 0.60
    # axial V grooves (90 deg) between the pyramid columns
    for i in range(P.CROWN_PYRAMIDS):
        ang = 360.0 * (i + 0.5) / P.CROWN_PYRAMIDS
        w = 2.0
        tri = [Vector(R - depth, 0, z0 - 0.5), Vector(R - depth + w, w, z0 - 0.5),
               Vector(R - depth + w, -w, z0 - 0.5)]
        prism = extrude(Face(Wire(Polyline(*tri, close=True))), amount=H - z0 + 1.0, dir=(0, 0, 1))
        crown = crown - Rot(0, 0, ang) * prism
    # circumferential V grooves at the row boundaries (ends become chamfers)
    for k in range(P.CROWN_KNURL_ROWS + 1):
        zc = z0 + k * P.CROWN_ROW_H
        w = 2.0
        groove = revolve_rz([(R - depth, zc), (R - depth + w, zc + w), (R - depth + w, zc - w)])
        crown = crown - groove
    # restore a clean skirt under the first row (it was nicked by the first groove)
    crown = crown + Pos(0, 0, z0 / 2) * Cylinder(P.CROWN_SKIRT_D / 2, z0)
    # case-side recess for the crown tube, stem tap hole
    crown = crown - Pos(0, 0, 0.65) * Cylinder(1.55, 2.3)        # tube recess, open at the face
    crown = crown - Pos(0, 0, 1.8 + 0.5) * Cylinder(0.40, 1.0)   # blind, 0.4 mm floor
    return crown


def build_ring():
    od = P.RING_OD
    h = P.Z_MOVT_TOP - P.Z_FLOOR
    ring = Pos(0, 0, P.Z_FLOOR + h / 2) * (Cylinder(od / 2, h) - Cylinder(P.RING_ID / 2, h + 1))
    slot_z0 = P.Z_STEM - 1.4
    slot = Pos(0, 15, (slot_z0 + P.Z_MOVT_TOP + 1) / 2) * Box(2.8, 10, P.Z_MOVT_TOP + 1 - slot_z0)
    return ring - slot


def export_clean_stl(shape, path):
    """Tessellate finely, then weld + drop degenerate slivers (revolve poles)."""
    import tempfile
    import trimesh
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.stl"
        export_stl(shape, str(raw), tolerance=0.002, angular_tolerance=0.03)
        m = trimesh.load(str(raw))
    m.merge_vertices(digits_vertex=5)
    m.update_faces(m.nondegenerate_faces(height=1e-6))
    m.update_faces(m.unique_faces())
    comps = m.split(only_watertight=False)
    comps = [c for c in comps if len(c.faces) > 4]
    m = trimesh.util.concatenate(comps)
    if not m.is_winding_consistent:
        trimesh.repair.fix_winding(m)
    m.export(str(path))
    return m


def main():
    P.STL_DIR.mkdir(parents=True, exist_ok=True)
    P.STEP_DIR.mkdir(parents=True, exist_ok=True)
    peb = pebble_solid()
    print("pebble volume %.1f mm3" % peb.volume)
    body = build_body(peb)
    print("body ok", body.is_valid, "%.1f mm3" % body.volume)
    back = build_caseback(peb)
    print("caseback ok", back.is_valid, "%.1f mm3" % back.volume)
    crown = build_crown()
    print("crown ok", crown.is_valid, "%.1f mm3" % crown.volume)
    crown_placed = crown_axis_loc(P.SPOT_FACE_Y + P.CROWN_GAP) * crown
    ring = build_ring()
    print("ring ok", ring.is_valid)
    parts = {
        "case_body": body,
        "caseback_bridge": back,
        "crown": crown,
        "movement_ring": ring,
    }
    for name, part in parts.items():
        m = export_clean_stl(part, P.STL_DIR / f"{TAG}_{name}.stl")
        print("  %-16s %7d tris  watertight=%s  vol=%.1f" % (name, len(m.faces), m.is_watertight, m.volume))
        export_step(part, str(P.STEP_DIR / f"{TAG}_{name}.step"))
    asm = Compound([body, back, crown_placed, ring])
    export_clean_stl(asm, P.STL_DIR / f"{TAG}_assembly_preview.stl")
    export_step(asm, str(P.STEP_DIR / f"{TAG}_assembly.step"))
    print("exported to", P.STL_DIR, "and", P.STEP_DIR)


if __name__ == "__main__":
    main()
