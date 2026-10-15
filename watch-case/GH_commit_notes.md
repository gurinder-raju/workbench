# Watch Case STL Version Notes

Commit notes for each iteration of the prototype watch case, one commit per version.

## Suggested Commit 1

File:
- `GH_watch_case_V1_attached_hidden_tunnel.stl`

Commit title:
```text
Add watch case V1 with attached hidden strap tunnel
```

Commit notes:
```text
Adds a complete watch case prototype body with the rear strap bridge included in the STL.

This version establishes the hidden under-case strap-tunnel concept. The bridge attaches at the 3 o'clock and 9 o'clock sides, outside the 22 mm strap lane, so the strap can run from 12 o'clock to 6 o'clock while the visible top remains a smooth case.

Key characteristics:
- 42.0 mm main case width
- 36.0 mm crystal opening
- 33.5 mm visible dial reference
- Crown at 12 o'clock
- Attached hidden underside strap bridge
- Side-cheek attachment geometry at 3 and 9 o'clock

This is a visual/proportion prototype STL, not production-ready CNC CAD.
```

## Suggested Commit 2

File:
- `GH_watch_case_V2_refined_hidden_tunnel.stl`

Commit title:
```text
Refine watch case V2 with smooth hidden tunnel shoulders
```

Commit notes:
```text
Replaces the more rectangular rear bridge attachment with a smoother hidden underside saddle.

This version keeps the 22 mm 12-to-6 strap path while improving the transition from the bridge into the underside of the case. The 3 o'clock and 9 o'clock attachments are modeled as continuous curved shoulders rather than box-like structural cheeks.

Key changes from V1:
- Smoother underside bridge shape
- Curved 3/9 o'clock shoulders
- Better hidden-tunnel design intent
- Case and attached bridge provided as one complete STL body for prototype review

This is design-intent mesh geometry for resin prototyping. A production CNC version should be rebuilt as clean parametric CAD.
```

## Suggested Commit 3

File:
- `GH_watch_case_V3_comfort_back_hidden_tunnel.stl`

Commit title:
```text
Add watch case V3 comfort-back underside contour
```

Commit notes:
```text
Adds the current best version of the watch case prototype with a comfort-contoured underside.

This revision keeps the refined hidden strap tunnel and smooth 3/9 o'clock bridge shoulders, while reshaping the wrist-facing back so the center is the deepest point and the underside gradually lifts toward the perimeter. This better reflects how a wearable watch case should sit on the wrist and reduces abrupt pressure points.

Key changes from V2:
- Comfort-contoured wrist-facing underside
- Center underside sits lowest, with gradual lift toward edges
- Smooth attached hidden saddle retained
- 22 mm 12-to-6 strap path retained
- Complete case-plus-bridge STL prepared for prototype review

This is the preferred current prototype file. It remains a faceted STL design-intent model, not final production CNC CAD.
```

## Suggested Commit 4

File:
- `GH_watch_case_V4_enclosed_case.stl`

Commit title:
```text
Add watch case V4 with enclosed back and rounded top
```

Commit notes:
```text
Adds a revised complete watch case prototype STL based on physical print feedback.

This version improves the case architecture, strap handling, and visual proportions. The rear of the watch is now enclosed before the strap bridge, so the strap path is separated from the internal watch cavity. The underside bridge remains shortened in the 12-to-6 direction to leave future fastening zones, while the usable strap lane is relaxed to approximately 24.0 mm so a 22 mm strap has enough room to be threaded and adjusted without excessive side-to-side looseness.

Key changes from V3:
- Adds an enclosed rear caseback behind the movement cavity
- Keeps the hidden strap bridge below the enclosed caseback
- Sets the usable strap lane to approximately 24.0 mm for a 22 mm strap
- Shortens the underside bridge in the 12-to-6 direction to reserve future screw/fastener space
- Adds subtle rear screw-land pads as layout placeholders
- Further rounds the top case surface to avoid a flat bezel shelf
- Widens the apparent bezel shoulder by reducing the front opening to 35.0 mm
- Raises the top shoulder into a more pronounced continuous dome
- Enlarges and brings the 12 o'clock crown closer to the case
- Adds a stylized faceted crown texture for proportion review
- Rebuilds mesh winding to remove flipped-normal style orientation issues

Mesh validation notes:
- 42.0 mm main case width
- 26,848 triangular facets
- 0 zero-area faces detected
- 0 open boundary edges detected
- 0 nonmanifold edges detected
- 0 same-direction shared-edge conflicts detected after orientation pass

This remains a resin-prototype STL and design-intent mesh. It should be rebuilt as clean parametric CAD before production machining.
```

## Suggested Commit 5 (V7)

File:
- `GH_watch_case_V7_symmetric_roundover.stl`

Commit title:
```text
Add watch case V7 with symmetric roundover
```

Commit notes:
```text
Adds a follow-up surface refinement to make the upper case curvature match the lower roundover more closely.

This version keeps the enclosed back, hidden strap bridge, approximately 24.0 mm strap lane, enlarged crown, and future screw-land layout. The main change is the outer case cross-section: the upper side now starts tapering inward earlier, with a larger-radius top roundover instead of a mostly vertical side wall ending in a small top corner.
```

## Suggested Commit 6 (V8)

Files:
- `GH_watch_case_V8_42mm/` (STL parts and section diagram)
- `step/` (STEP solids)
- `cad/` (parametric build123d source, shared by future versions)
- `README.md`

Commit title:
```text
Add watch case V8: parametric 42 mm case with crown at 12 and short strap bridge
```

Commit notes:
```text
Rebuilds the case from scratch as a parametric CAD model (build123d) instead of a hand-made mesh.

- One continuous, curvature-smooth outer profile (no kinks in polished reflections)
- Bezel inner edge 34.7 mm, visible dial 32.4 mm
- 42.00 mm wide, 13.75 mm total, thickness/diameter 0.327
- Stack built around a Miyota 9039: 0.4 rotor clearance, 1.75 hand stack + 0.4, 34.0 x 1.2 flat crystal
- Crown at 12: clous de Paris, 2 rows x 16 pyramids, collar tucked into a counterbore
- 22 mm strap through a 23.0 x 2.8 mm tunnel; bridge only 14 mm long so the strap drapes
- 4 x standard M1.4 x 4 caseback screws, 2 at 12 and 2 at 6, heads flush in the strap channel past the bridge
- Print fits per Foundry I/O's 0.2 mm advice (pilot holes, tube hole, crystal seat, movement ring); fit-checked with a virtual standard screw
- Separate parts: case body, caseback+bridge, crown, movement ring (STL + STEP)

Stem height (1.55 mm below the movement dial side) is an estimate and must be verified before CNC.

## Suggested Commit 7 (V9)

Files:
- `GH_watch_case_V9_42mm/` (STL parts and section diagram)
- `step/` (V9 STEP solids)
- `cad/` (seal parameters, fit checks, section drawing)
- `README.md`

Commit title:
```text
Add watch case V9: sealed for water resistance (crystal gasket, caseback O-ring, crown O-ring)
```

Commit notes:
```text
Moves the case from a display prototype toward a wearable, water-resistant watch.
Each of the three ways water gets in now has a standard watch seal, sized to
off-the-shelf gaskets, so this last print tests the same sealing geometry that goes to CNC.
Target: about 3 ATM (rain, hand-washing, splashes) with the crown pushed in.

Crystal
- Seat 34.80 for a 34.0 x 1.2 crystal in a Hytrel I-ring gasket (0.45 wall x 0.90 high), 0.05 squeeze per side
- Pressed in by a watchmaker with a crystal press, so it can be serviced (no glue)
- Bezel crest moved out to 35.2 mm (0.838 x D) so the seat doesn't leave a knife edge

Caseback
- Spigot into the movement bore carries a 32.0 x 0.6 O-ring sealing radially against the bore (20 % squeeze, 74 % groove fill)
- The seal doesn't depend on screw torque; the 4 M1.4 screws only retain the back
- The spigot also centres the caseback, so no dowel pins are needed
- 30 deg lead-in at the bore mouth so the O-ring isn't cut on assembly
- Movement ring now sits on the spigot (3.0 mm tall)

Crown
- Standard tube design: 80.135.42 tube (2.5 case end, 3.0 crown end) is the replaceable wear surface
- 3.0 x 0.5 O-ring in a groove inside the crown, sealing on the tube's 3.0 end (16 % squeeze); bore 2.0 deep, tube engages 1.8
- Tube shoulder sits in a 0.5 mm pocket, so the tube fits as supplied (no filing)
- A tubeless variant (O-ring on a crown post sealing straight in the case) was tried and rejected:
  it makes the case the wear surface, leaves a 0.33 mm wall and needs a larger, draggier O-ring

Checks and drawings
- check_fits.py reports seal squeeze, stretch and groove fill, and checks the parts for overlaps
- Section diagram shows the three seals and the crown tube
- Print fits are kept per Foundry I/O's advice; README lists the CNC value for each

Still to verify on the real parts before printing: stem height (1.55 mm below the dial side is an
estimate), crystal size, tube crown-end diameter and the crystal gasket wall.
```
