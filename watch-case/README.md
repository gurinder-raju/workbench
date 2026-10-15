# watch-case

A prototype 42 mm lugless pebble watch case with the crown at 12, and a 22 mm strap that runs under a short bridge. It's for a personal build with a Miyota 9039 movement. Each version is one commit; V1 to V7 are single STL files, and from V8 on the case is a parametric CAD model.

## Layout

| Path | What it is |
|---|---|
| `GH_watch_case_V1_…` to `GH_watch_case_V7_….stl` | Earlier versions, one STL each |
| `GH_watch_case_V8_pebble42/`, `GH_watch_case_V9_pebble42/` | Each parametric version's parts as STL, plus its section diagram |
| `step/` | Solid STEP models of every parametric version, for Fusion, Onshape or CAM |
| `cad/` | Parametric source, shared by all versions. Change `params.py` (including `VERSION`), then run `watch.py` |
| `GH_commit_notes.md` | Commit notes for each version |

**Current version: V9.** V9 is V8 with all three seals designed in: a gasketed crystal seat, an O-ring on the caseback, and an O-ring inside the crown. It's the last print before CNC.

![V9 section](GH_watch_case_V9_pebble42/GH_watch_case_V9_section.png)

### V9 parts (`GH_watch_case_V9_pebble42/`)

| File | What it is |
|---|---|
| `…_case_body.stl` | Upper pebble: bezel, I-ring crystal seat, rehaut, movement bore with an O-ring lead-in, crown-tube hole and shoulder pocket at 12, 4 pilot holes for M1.4 screws |
| `…_caseback_bridge.stl` | Lower pebble: 1.6 mm caseback plate, spigot with an O-ring groove, strap tunnel from 12 to 6, 14 mm bridge, 4 flush seats for M1.4 wafer-head screws |
| `…_crown.stl` | Clous de Paris crown, 2 rows × 16 pyramids, smooth collar, bore over the tube with an internal O-ring groove, blind stem hole |
| `…_movement_ring.stl` | Spacer that centres the 26 mm movement in the 33.5 mm bore. It sits on the caseback spigot and has a slot for the stem |
| `…_assembly_preview.stl` | All parts in position, for viewing only |

## Key dimensions

| | V9 |
|---|---|
| Case diameter | **42.0** |
| Bezel inner edge (polished roll starts) | **35.2** (0.838 × diameter; just outside the crystal gasket) |
| Visible dial | **32.4** (0.774 × diameter) |
| Total thickness | **13.75** |
| Thickness / diameter | **0.327** |
| Widest point below the crest | 41 % (crest at z 13.75, widest at z 8.15, level with the crown) |
| Crown diameter / length past the case | **6.2 / 2.75** |
| Strap | **22 mm single-pass strap through a tunnel** |
| Overall | **42.00 wide (3 to 9), 44.75 from 6 to the crown tip** |

Vertical stack, measured from the wrist side upward: bridge 1.1, strap tunnel 2.8, caseback plate 1.6, rotor clearance 0.4, Miyota 9039 movement 3.9, dial 0.5, hands 1.75 plus 0.4 clearance, crystal 1.2, and a 0.1 mm crest above the crystal.

The outer profile is one curvature-continuous curve (`profile.py`), so polished reflections flow without kinks.

## Seals

The goal is about 3 ATM (rain, hand-washing and splashes; no swimming), with the crown pushed in.

| Seal | How it works | Part | Fit (from `check_fits.py`) |
|---|---|---|---|
| **Crystal** | A plastic I-ring gasket around the crystal. A watchmaker presses crystal and gasket into the seat together. | Hytrel "I" gasket, **34.0 mm** inside, **0.45** wall, 0.90 high | Gasket 34.90 free in a **34.80** seat: 0.05 squeeze per side |
| **Caseback** | A spigot on the caseback enters the movement bore. An O-ring in a groove on the spigot seals against the bore wall, so the seal doesn't depend on screw torque. The spigot also centres the caseback, so no dowel pins are needed. A 30° lead-in at the bore mouth keeps the O-ring from being cut. | O-ring **32.0 × 0.6** | Groove Ø32.54, 1.7 % stretch, 20 % squeeze, 74 % groove fill |
| **Crown** | An O-ring sits in a groove inside the crown and seals on the outside of the crown tube's 3.0 mm end. The tube is the wear surface, and a watchmaker can replace it at service. | O-ring **3.0 × 0.5** | Groove Ø3.84, 16 % squeeze, 72 % fill. The tube end engages the crown 1.8 mm |

## Parts to buy

- **Movement**: Miyota 9039 (no date, 3 hands, 26.0 × 3.90 mm). Mount it rotated 90° so the stem exits at 12, and print the dial with 12 at the crown.
- **Crystal**: flat, Ø34.0 × 1.2 mm (mineral for the prototype, sapphire later).
- **Dial**: Ø33.4 × 0.5 mm, with Ø32.4 visible. It's clamped between the rehaut and the movement ring.
- **Crown tube**: **80.135.42**: 2.5 mm case end, 3.0 mm crown end that's 2.5 mm long, 5.5 mm overall (Esslinger/Ofrei 80.135 series). The tube's shoulder sits in a 0.5 mm pocket, so 2.0 mm of the crown end stands proud and no filing is needed. The print hole is 2.7 mm, so glue the tube in.
- **Caseback screws**: 4 × **M1.4 × 4 mm** stainless, flat round (wafer) head, Ø2.5 × 0.5 mm, flat underneath, 0.3 mm pitch. The head sits flush in a Ø2.9 × 0.5 mm seat. There are two at 12 and two at 6, in the strap channel just past the bridge. Each screw grips 2.9 mm into the case.
- **Crystal gasket**: Esslinger individual Hytrel "I" gasket, 34.0 mm (series 84.045, about $6).
- **Caseback O-ring**: 32.0 × 0.6 mm, Esslinger .60 mm thickness O-ring gaskets (84.314.60), size 32 mm, pack of 3.
- **Crown O-ring**: 3.0 × 0.5 mm (OD 4.0), nitrile 70: Polymax (UK) part 3X0.5N70. It's only needed for final assembly, not for the print.
- **Strap**: 22 mm single-pass strap (one piece, no spring bars), **2.6 mm thick or less** at the case. The tunnel is 23.0 × 2.8 mm.

## Printing notes

- Print the body with the flat joint face (z = 5.5) on the bed. The caseback no longer has a flat face, because the spigot stands on top. Let Foundry I/O orient it, and ask them to keep supports off the spigot, its O-ring groove and the screw seats. The tunnel ceiling bridges about 23 mm.
- The case STLs are fine meshes (0.002 mm chord tolerance) and are watertight.
- **Fits for printing.** Foundry I/O advised about 0.2 mm on pin/hole fits. Print values, with the CNC value in brackets:

  | Feature | Print | CNC |
  |---|---|---|
  | Screw holes in the body | 1.15 pilot; the screw cuts its own thread | 1.10 drilled, tapped M1.4 × 0.3, 2.5 deep |
  | Caseback spigot | Ø33.30 in the 33.50 bore | Ø33.40 |
  | Crown-tube hole / shoulder pocket | 2.70 / 3.20; glue the tube | 2.50 press fit / 3.05 |
  | Crown bore over the tube | 3.20 | 3.10 |
  | Crown stem hole | 0.80; screw the stem in | Tap 10 (0.90 thread) |
  | Movement ring | 0.1 per side | 0.05 per side |

  The crystal seat (34.80), the O-ring grooves and the screw seats are the same for print and CNC.
- **Thinnest walls on the print** (from `check_fits.py`): 0.38 mm at the mouth of each pilot hole, where the bore lead-in passes; 0.53 mm higher up; 0.48 mm at the screw-head seat edge; and 0.57 mm between the crown's O-ring groove and its pyramids.
- A printed crown won't hold the stem's thread for long. For test fits, glue the stem in once it's cut to length.

## Before CNC

- [ ] **Stem height**: the crown axis assumes the Miyota stem sits 1.55 mm below the movement's dial side (an estimate). Measure the real movement, then update `STEM_FROM_DIAL_SIDE` and rebuild.
- [ ] Measure the real crystal, crown tube and gaskets, and update `params.py` if they differ.
- [ ] Add casing clamps or screws between the movement and the ring. The prototype holds the movement by clamping the dial.
- [ ] Switch the print fits to the CNC values above, and send a 2D drawing with the thread callouts alongside the STEP (STEP files don't carry threads).
- [ ] Confirm with the CNC shop that they can tap M1.4 in the chosen metal and cut the 3.84 mm groove inside the crown.
- [ ] Optional: hollow out the solid lower cheeks to save weight.

## Rebuilding

```bash
pip install build123d trimesh manifold3d scipy moderngl matplotlib shapely
cd cad
python watch.py        # STL parts -> GH_watch_case_<VERSION>_pebble42/, STEP -> step/
python section.py      # section diagram, next to the STL parts
python check_fits.py   # screw test-fit, wall thicknesses, seal squeeze and part overlaps
python render.py       # optional local previews in .renders/ (git-ignored, never committed)
```

The repo doesn't hold any images apart from the section diagrams. `.gitignore` blocks image files, except ones named `*_section.png`.
