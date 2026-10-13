"""Design parameters for the V8 42 mm pebble case.

Coordinate system (all mm):
    +X -> 3 o'clock, +Y -> 12 o'clock (crown + strap axis), +Z -> up (crystal).
    Z = 0 is the lowest point of the case (centre of the wrist-side bridge).

Plan-view proportions are fractions of the case diameter.
Vertical stack is built bottom-up from a Miyota 9039 (26.0 mm x 3.90 mm).
"""

from pathlib import Path

# ---- Version and output layout (watch-case/ stays flat) --------------------
VERSION = "V8"
TAG = f"GH_watch_case_{VERSION}_pebble42"
CASE_DIR = Path(__file__).resolve().parent.parent   # watch-case/
STL_DIR = CASE_DIR / TAG                            # one folder of STL parts per version
STEP_DIR = CASE_DIR / "step"                        # STEP solids for every version
PREVIEW_DIR = CASE_DIR / ".renders"                 # local preview images, never committed

# ---- Size ----------------------------------------------------------------
DIAMETER = 42.0

R_MAX = DIAMETER / 2                     # 21.00  widest point of the pebble

# ---- Plan-view proportions (fractions of the case diameter) ---------------
# polished bezel inner edge  : 0.826 x D   -> 34.7 mm
# visible dial               : 0.774 x D   -> 32.4 mm
R_BEZEL_IN = 0.8256 * R_MAX              # 17.34  where the polished roll starts
R_CRYSTAL = 17.00                        # crystal 34.0 mm dia (flat sapphire)
R_REHAUT = 16.20                         # visible dial opening 32.4 mm
R_DIAL = 16.70                           # dial 33.4 mm dia (sits under rehaut)
R_BORE = 16.75                           # movement/dial bore 33.5 mm (back loaded)

# ---- Vertical stack (bottom -> top) ---------------------------------------
# One continuous pebble.  The strap tunnel runs 12 -> 6 through the bottom of it,
# under a 1.6 mm caseback plate; a short bridge closes the tunnel in the middle.
BRIDGE_T = 1.10                          # bridge thickness at centre
TUNNEL_H = 2.80                          # strap tunnel height (single-pass strap <= 2.6 mm)
Z_TUNNEL_FLOOR = BRIDGE_T                # 1.10
Z_TUNNEL_CEIL = Z_TUNNEL_FLOOR + TUNNEL_H  # 3.90
BACK_PLATE_T = 1.60                      # caseback plate: room for a flush standard M1.4 head
Z_PARTING = Z_TUNNEL_CEIL + BACK_PLATE_T   # 5.50  caseback <-> case body joint
Z_FLOOR = Z_PARTING                      # caseback top = floor under the movement
# (no centring ring: the 4 screws locate the caseback; add 2 dowel pins for CNC)

MOVT_CLEAR = 0.40                        # Miyota min clearance rotor -> caseback
MOVT_H = 3.90                            # Miyota 9039 height
Z_MOVT_BOT = Z_FLOOR + MOVT_CLEAR        # 5.90
Z_MOVT_TOP = Z_MOVT_BOT + MOVT_H         # 9.80  (dial side of movement)
DIAL_T = 0.50
Z_DIAL_TOP = Z_MOVT_TOP + DIAL_T         # 10.30
HAND_STACK = 1.75                        # 9039: 0.90 + 0.40 + 0.45
HAND_CLEAR = 0.40                        # Miyota min hand -> crystal
Z_CRYSTAL_BOT = Z_DIAL_TOP + HAND_STACK + HAND_CLEAR  # 12.45
CRYSTAL_T = 1.20
Z_CRYSTAL_TOP = Z_CRYSTAL_BOT + CRYSTAL_T  # 13.65
Z_TOP = Z_CRYSTAL_TOP + 0.10             # 13.75  bezel crest (crystal sits 0.1 below)

# Widest point ~41 % down from the crest, level with the crown axis
Z_MAX = 8.15

# ---- Crown at 12 ----------------------------------------------------------
STEM_FROM_DIAL_SIDE = 1.55               # ESTIMATE - verify on the real movement
Z_STEM = Z_MOVT_TOP - STEM_FROM_DIAL_SIDE  # 8.25
TUBE_HOLE_D = 2.70                       # print: glue a 2.5 mm tube in (CNC: 2.50 press fit)
SPOT_FACE_Y = 20.35                      # floor of the crown counterbore (collar tucks in)
SPOT_FACE_R = 3.05                       # counterbore 6.1 mm for the 5.7 mm collar
CROWN_D = 6.18                           # 0.147 x case diameter
CROWN_GAP = 0.20                         # crown face -> counterbore floor
CROWN_KNURL_ROWS = 2
CROWN_ROW_H = 1.30
CROWN_PYRAMIDS = 16                      # clous de Paris studs per row
CROWN_SKIRT_H = 0.60                     # smooth collar on the case side
CROWN_SKIRT_D = 5.70

# ---- Strap tunnel / bridge -------------------------------------------------
STRAP_W = 22.0
LANE_W = 23.0                            # 0.5 mm per side: snug, no side-to-side flop
BRIDGE_L = 14.0                          # length along 12-6: short so the strap drapes

# ---- Caseback screws: 2 at 12, 2 at 6, in the strap channel past the bridge --
# Standard M1.4 x 4 cheese head (ISO 1207 / DIN 84: head <= 2.6 dia x 0.9) or pan head.
SCREW_R = 17.85                          # >= 0.5 mm wall to the movement bore
SCREW_X = 9.00                           # inside the 23 mm strap lane, clear of the exit fillet
SCREW_Y = (SCREW_R ** 2 - SCREW_X ** 2) ** 0.5   # 15.41
SCREW_TAP_D = 1.15                       # print: pilot, screw cuts its thread (CNC: 1.10 + M1.4 tap)
SCREW_CLEAR_D = 1.60                     # clearance through the caseback plate
SCREW_HEAD_D = 2.90                      # head seat: 0.15 mm room around a 2.6 mm head
SCREW_HEAD_DEPTH = 1.00                  # 0.9 mm head sits 0.1 below the tunnel ceiling
SCREW_THREAD_DEPTH = 3.80                # 4 mm screw: 0.6 mm plate + 3.4 mm in the body

# ---- Movement holder ring --------------------------------------------------
RING_OD = 2 * R_BORE - 0.20              # 33.30  (0.1 mm clearance per side for printing)
RING_ID = 26.20                          # Miyota 9039 dia 26.00 (0.1 per side)

# ---- Print fits (Foundry I/O advised ~0.2 mm on pin/hole fits) -------------
CRYSTAL_SEAT_CLEAR = 0.05                # seat 34.1 for a 34.0 crystal; glue it
