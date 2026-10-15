"""Design parameters for the 42 mm pebble case (V9: sealed, gasketed).

Coordinate system (all mm):
    +X -> 3 o'clock, +Y -> 12 o'clock (crown + strap axis), +Z -> up (crystal).
    Z = 0 is the lowest point of the case (centre of the wrist-side bridge).

Plan-view proportions are fractions of the case diameter.
Vertical stack is built bottom-up from a Miyota 9039 (26.0 mm x 3.90 mm).
"""

from pathlib import Path

# ---- Version and output layout (watch-case/ stays flat) --------------------
VERSION = "V9"
TAG = f"GH_watch_case_{VERSION}_pebble42"
CASE_DIR = Path(__file__).resolve().parent.parent   # watch-case/
STL_DIR = CASE_DIR / TAG                            # one folder of STL parts per version
STEP_DIR = CASE_DIR / "step"                        # STEP solids for every version
PREVIEW_DIR = CASE_DIR / ".renders"                 # local preview images, never committed

# ---- Size ----------------------------------------------------------------
DIAMETER = 42.0

R_MAX = DIAMETER / 2                     # 21.00  widest point of the pebble

# ---- Plan-view proportions (fractions of the case diameter) ---------------
# polished bezel inner edge  : 0.838 x D   -> 35.2 mm (outside the crystal gasket)
# visible dial               : 0.774 x D   -> 32.4 mm
R_CRYSTAL = 17.00                        # crystal 34.0 mm dia x 1.2 (flat mineral; sapphire later)
# Crystal seal: I-ring gasket (Hytrel, 0.45 wall x 0.90 high); the watchmaker
# presses crystal + gasket into the seat.
CRYSTAL_GASKET_WALL = 0.45
CRYSTAL_GASKET_H = 0.90
CRYSTAL_GASKET_SQUEEZE = 0.05            # per side: seat 34.80 for a 34.90 gasket
R_CRYSTAL_SEAT = R_CRYSTAL + CRYSTAL_GASKET_WALL - CRYSTAL_GASKET_SQUEEZE   # 17.40
# polished roll starts just outside the gasket seat (0.1 chamfer + 0.1 flat land)
R_BEZEL_IN = R_CRYSTAL_SEAT + 0.20       # 17.60  (0.838 x D)
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
SPOT_FACE_Y = 20.35                      # floor of the crown counterbore (collar tucks in)
SPOT_FACE_R = 3.05                       # counterbore 6.1 mm for the 5.7 mm collar
# Tube 80.135.42: case end 2.5 dia, crown end 3.0 dia x 2.5 long, 5.5 overall.
# The tube is the replaceable wear surface for the crown seal.
TUBE_HOLE_D = 2.70                       # print: glue a 2.5 mm tube in (CNC: 2.50 press fit)
TUBE_SHOULDER_D = 3.20                   # pocket for the 3.0 crown end (CNC: 3.05)
TUBE_SHOULDER_DEPTH = 0.50               # tube shoulder sits 0.5 below the counterbore floor:
                                         # 2.0 of the crown end stands proud, no filing
CROWN_D = 6.18                           # 0.147 x case diameter
CROWN_GAP = 0.20                         # crown face -> counterbore floor
CROWN_KNURL_ROWS = 2
CROWN_ROW_H = 1.30
CROWN_PYRAMIDS = 16                      # clous de Paris studs per row
CROWN_SKIRT_H = 0.60                     # smooth collar on the case side
CROWN_SKIRT_D = 5.70
# Crown seal: a 3.0 x 0.5 O-ring in a groove inside the crown, sealing on the
# tube's 3.0 crown end. Water resistant with the crown pushed in.
CROWN_BORE_D = 3.20                      # slides over the 3.0 tube end (CNC: 3.10)
CROWN_BORE_DEPTH = 2.00                  # tube engages 1.8, 0.2 end clearance
CROWN_ORING_ID = 3.00
CROWN_ORING_CS = 0.50
CROWN_GROOVE_D = 3.84                    # 16 % squeeze on the tube
CROWN_GROOVE_W = 0.65
CROWN_GROOVE_Z = 0.30                    # groove starts 0.3 in from the crown mouth
CROWN_STEM_HOLE_D = 0.80                 # print: stem screws in (CNC: tap 10 = 0.90 thread)
CROWN_STEM_HOLE_DEPTH = 0.95             # past the bore; leaves a 0.25 floor

# ---- Strap tunnel / bridge -------------------------------------------------
STRAP_W = 22.0
LANE_W = 23.0                            # 0.5 mm per side: snug, no side-to-side flop
BRIDGE_L = 14.0                          # length along 12-6: short so the strap drapes

# ---- Caseback screws: 2 at 12, 2 at 6, in the strap channel past the bridge --
# M1.4 x 4 wafer (flat round) head screw: head 2.5 dia x 0.5, pitch 0.3.
SCREW_R = 17.85                          # >= 0.5 mm wall to the movement bore
SCREW_X = 9.00                           # inside the 23 mm strap lane, clear of the exit fillet
SCREW_Y = (SCREW_R ** 2 - SCREW_X ** 2) ** 0.5   # 15.41
SCREW_TAP_D = 1.15                       # print: pilot, screw cuts its thread (CNC: 1.10 + M1.4 tap)
SCREW_CLEAR_D = 1.60                     # clearance through the caseback plate
SCREW_HEAD_D = 2.90                      # head seat: 0.2 mm room around a 2.5 mm wafer head
SCREW_HEAD_DEPTH = 0.50                  # 0.5 mm wafer head sits flush with the tunnel ceiling
SCREW_THREAD_DEPTH = 3.30                # 4 mm screw: 1.1 mm plate + 2.9 mm in the body

# ---- Caseback seal: spigot + radial O-ring --------------------------------
# A spigot on the caseback enters the movement bore and carries a 32.0 x 0.6
# O-ring that seals radially against the bore wall (independent of screw torque).
# The spigot also centres the caseback, so no dowel pins are needed.
SPIGOT_OD = 33.30                        # print: 0.1 per side in the 33.5 bore (CNC: 33.40)
SPIGOT_H = 1.30                          # rises above the parting line; the ring sits on it
BACK_ORING_ID = 32.00
BACK_ORING_CS = 0.60
BACK_GROOVE_D = 2 * R_BORE - 2 * 0.48    # 32.54: 20 % squeeze against the bore
BACK_GROOVE_W = 0.80
BACK_GROOVE_Z = 0.25                     # groove starts 0.25 above the parting line
BORE_LEAD_R = 0.20                       # 30 deg lead-in chamfer at the bore mouth
BORE_LEAD_H = 0.35

# ---- Movement holder ring --------------------------------------------------
RING_OD = 2 * R_BORE - 0.20              # 33.30  (0.1 mm clearance per side for printing)
RING_ID = 26.20                          # Miyota 9039 dia 26.00 (0.1 per side)

# Print fits follow Foundry I/O advice (~0.2 mm on pin/hole fits); CNC values in comments.
