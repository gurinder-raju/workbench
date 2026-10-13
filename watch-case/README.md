# watch-case

A prototype 42 mm lugless pebble watch case with the crown at 12, and a 22 mm strap that runs under a short bridge. It's for a personal build with a Miyota 9039 movement. Each version is one commit; V1 to V7 are single STL files, and from V8 on the case is a parametric CAD model.

## Layout

| Path | What it is |
|---|---|
| `GH_watch_case_V1_…` to `GH_watch_case_V7_….stl` | Earlier versions, one STL each |
| `GH_watch_case_V8_pebble42/` | V8 parts as STL, plus its section diagram. Each new version gets a folder like this |
| `step/` | Solid STEP models of every parametric version, for Fusion, Onshape or CAM |
| `cad/` | Parametric source, shared by all versions. Change `params.py` (including `VERSION`), then run `watch.py` |
| `GH_commit_notes.md` | Commit notes for each version |

**Current version: V8**

![V8 section](GH_watch_case_V8_pebble42/GH_watch_case_V8_section.png)

### V8 parts (`GH_watch_case_V8_pebble42/`)

| File | What it is |
|---|---|
| `…_case_body.stl` | Upper pebble: bezel, crystal seat, rehaut, movement bore, crown-tube hole at 12, 4 pilot holes for M1.4 screws |
| `…_caseback_bridge.stl` | Lower pebble: 1.6 mm caseback plate, strap tunnel from 12 to 6, 14 mm bridge, 4 flush seats for standard M1.4 heads |
| `…_crown.stl` | Clous de Paris crown, 2 rows × 16 pyramids, smooth collar, tube recess |
| `…_movement_ring.stl` | Spacer that centres the 26 mm movement in the 33.5 mm bore, with a slot for the stem |
| `…_assembly_preview.stl` | All parts in position, for viewing only |

## Key dimensions

| | V8 |
|---|---|
| Case diameter | **42.0** |
| Bezel inner edge (polished roll starts) | **34.7** (0.826 × diameter) |
| Visible dial | **32.4** (0.774 × diameter) |
| Total thickness | **13.75** |
| Thickness / diameter | **0.327** |
| Widest point below the crest | 41 % (crest at z 13.75, widest at z 8.15, level with the crown) |
| Crown diameter / length past the case | **6.2 / 2.75** |
| Strap | **22 mm single-pass strap through a tunnel** |
| Overall | **42.00 wide (3 to 9), 44.75 from 6 to the crown tip** |

Vertical stack, measured from the wrist side upward: bridge 1.1, strap tunnel 2.8, caseback plate 1.6, rotor clearance 0.4, Miyota 9039 movement 3.9, dial 0.5, hands 1.75 plus 0.4 clearance, crystal 1.2, and a 0.1 mm crest above the crystal.

The outer profile is one curvature-continuous curve (`profile.py`), so polished reflections flow without kinks. Its radius of curvature runs from 2.7 mm at the crest to about 10 mm at the widest point.

## Parts to buy

- **Movement**: Miyota 9039 (no date, 3 hands, 26.0 × 3.90 mm). Mount it rotated 90° so the stem exits at 12, and print the dial with 12 at the crown.
- **Crystal**: flat sapphire, Ø34.0 × 1.2 mm. The printed seat is 34.1 mm, so glue it in.
- **Dial**: Ø33.4 × 0.5 mm, with Ø32.4 visible. It's clamped between the rehaut and the movement ring.
- **Crown tube**: OD 2.5 mm, about 4.6 mm long. That's 3.6 mm through the case wall plus about 1 mm into the crown's 1.8 mm recess. The printed hole is 2.7 mm, so glue the tube in. The stem runs through it into the crown. A printed crown can't hold the stem's 0.9 mm thread, so glue the stem in once it's cut to length, or use a metal crown for test fits.
- **Caseback screws**: 4 × **M1.4 × 4 mm**, standard stainless cheese head (ISO 1207 / DIN 84) or pan head (DIN 7985). Any head up to Ø2.6 × 0.9 mm sits flush. There are two at 12 and two at 6, in the strap channel just past the bridge. They sit under the strap when worn and are reached from underneath with the strap out. Each screw grips 3.4 mm into the case.
- **Strap**: 22 mm single-pass strap (one piece, no spring bars), **2.6 mm thick or less** at the case. The tunnel is 23.0 × 2.8 mm.

## Printing notes

- Print the body with the flat joint face (z = 5.5) on the bed. Print the caseback with its flat top on the bed. The tunnel ceiling then bridges about 23 mm, so either add supports inside the tunnel or print in resin.
- The case STLs are fine meshes (0.002 mm chord tolerance) and are watertight.
- **Fits for printing.** Foundry I/O advised about 0.2 mm on pin/hole fits, so the print version uses:
  - 1.15 mm pilot holes: drive the screws in slowly, or run an M1.4 tap first.
  - 1.6 mm clearance holes in the caseback.
  - A 2.9 mm head seat, 1.0 mm deep.
  - 0.1 mm per side on the movement ring.
  - A 2.7 mm crown-tube hole.
  - A 34.1 mm crystal seat.
  The four screws also centre the caseback; there's no separate centring ring.
- **Thinnest walls on the print** (from `check_fits.py`): 0.46 mm at the screw-head seat edge, 0.53 mm between each pilot hole and the movement bore, and 0.6 mm of plate under each screw head.
- In steel the case weighs about 56 g (7.0 cm³). In titanium it would be about 31 g.

## Before CNC

- [ ] **Stem height**: the crown axis assumes the Miyota stem sits 1.55 mm below the movement's dial side (an estimate). Measure the real movement, then update `STEM_FROM_DIAL_SIDE` and rebuild.
- [ ] Add casing clamps or screws between the movement and the ring. The prototype holds the movement by clamping the dial.
- [ ] Add a seal if you want water resistance: an O-ring on the caseback joint, plus crown and crystal gaskets.
- [ ] Switch the print fits back to machining fits:
  - a 2.50 mm press fit for the crown tube;
  - 1.10 mm drilled and tapped M1.4 holes;
  - a crystal gasket seat;
  - two dowel pins to centre the caseback.
- [ ] Optional: hollow out the solid lower cheeks to save weight.

## Rebuilding

```bash
pip install build123d trimesh manifold3d scipy moderngl matplotlib shapely
cd cad
python watch.py        # STL parts -> GH_watch_case_<VERSION>_pebble42/, STEP -> step/
python section.py      # section diagram, next to the STL parts
python check_fits.py   # test-fits a standard M1.4 x 4 screw and measures walls
python render.py       # optional local previews in .renders/ (git-ignored, never committed)
```

The repo doesn't hold any images apart from the section diagrams. `.gitignore` blocks image files, except ones named `*_section.png`.
