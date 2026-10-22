# watch-case

> The design files for this project are kept private. This repository holds the design notes, version history and section diagrams.

A prototype 42 mm lugless watch case with the crown at 12, and a 22 mm strap that runs under a short bridge. It's for a personal build with a Miyota 9039 movement. Each version is one commit.

## About this project

A personal, non-commercial project: one watch, designed and built by me with AI assistance. I used Claude (Anthropic) as a design and engineering partner, for the parametric CAD, fit checks, sealing design, supplier research and drawings. I directed the design, made the decisions, measured the real parts and iterated it version by version, recorded one commit at a time.

This is my own design and CAD work. It is not affiliated with or endorsed by any watch brand, and it carries no third-party trademarks or logos.

**No warranty.** Everything here is shared as-is, for viewing and learning. The design is untested as a water-resistant watch case, so use it at your own risk.

© 2026 Gurinder Raju. All rights reserved.

## How it was made

The case went through the same loop many times:

1. **Design:** sketch the change, then build it as a precise 3D model.
2. **Check:** before anything is made, test the fit virtually: screws, seals, crown and movement against each other, wall thicknesses and clearances.
3. **Print:** a resin prototype to hold, wear and judge by eye. The first print is what drove V4.
4. **Measure:** once real parts arrived (crown tubes, crystal, gaskets, screws), each was measured with calipers. Where reality differed from the catalogue, the design changed to match. That's V10.
5. **Record:** one commit per version, with what changed and why. See [VERSIONS.md](VERSIONS.md).

AI did much of the heavy lifting: modelling, fit calculations, sourcing parts and suppliers, and drafting quotes and drawings. The direction, taste and final calls were mine.

## Status

- **Now:** V10 is ready to print, waiting on one last measurement from the real movement (where its stem sits).
- **Next:** a final resin prototype to test every fit with real parts, then a metal case (CNC-machined steel, mirror-polished).
- **Dial and hands:** a UV-printed steel dial is on order; custom hands are being quoted.

**Current version: V10.** V10 is V9 (all three seals designed in: a gasketed crystal seat, an O-ring on the caseback, and an O-ring inside the crown) fitted to the measured parts: the 0.61 mm steel dial, the real screw heads and the real crystal gasket. It's the last print before CNC.

![V10 section](GH_watch_case_V10_42mm/GH_watch_case_V10_section.png)

## Design evolution

Every version, cut through the 12-6 axis (crown and strap tunnel) and the 3-9 axis. V5 and V6 were never built. The full story, with what changed in each version, why, and the numbers, is in **[VERSIONS.md](VERSIONS.md)**.

| Version | What changed | Section |
|---|---|---|
| V1 | First concept: a hidden strap tunnel under the case, with the bridge attached at 3 and 9 | [V1](GH_watch_case_V1_section.png) |
| V2 | Smoother shoulders where the strap enters and leaves the tunnel | [V2](GH_watch_case_V2_section.png) |
| V3 | A comfort-back underside contoured to the wrist | [V3](GH_watch_case_V3_section.png) |
| V4 | Enclosed caseback and a rounded top | [V4](GH_watch_case_V4_section.png) |
| V7 | Symmetric roundover: upper curvature matched to the lower shell | [V7](GH_watch_case_V7_section.png) |
| V8 | Rebuilt as a parametric CAD model: one continuous curvature-smooth profile, crown at 12, short 14 mm strap bridge, M1.4 caseback screws, Miyota 9039 stack | [V8](GH_watch_case_V8_42mm/GH_watch_case_V8_section.png) |
| V9 | Sealed for water resistance: gasketed crystal, caseback O-ring and crown O-ring | [V9](GH_watch_case_V9_42mm/GH_watch_case_V9_section.png) |
| V10 | Fitted to measured parts: 0.61 mm dial (thinner caseback, same height), deeper screw seats, crystal seat sized to the real gasket | [V10](GH_watch_case_V10_42mm/GH_watch_case_V10_section.png) |

## Key dimensions

| | V10 |
|---|---|
| Case diameter | **42.0** |
| Bezel inner edge (polished roll starts) | **35.27** (0.840 × diameter; just outside the crystal gasket) |
| Visible dial | **32.4** (0.774 × diameter) |
| Total thickness | **13.75** |
| Thickness / diameter | **0.327** |
| Widest point below the crest | 41 % (crest at z 13.75, widest at z 8.15, level with the crown) |
| Crown diameter / length past the case | **6.2 / 2.75** |
| Strap | **22 mm single-pass strap through a tunnel** |
| Overall | **42.00 wide (3 to 9), 44.75 from 6 to the crown tip** |

Vertical stack, measured from the wrist side upward: bridge 1.1, strap tunnel 2.8, caseback plate 1.49, rotor clearance 0.4, Miyota 9039 movement 3.9, dial 0.61, hands 1.75 plus 0.4 clearance, crystal 1.2, and a 0.1 mm crest above the crystal.

The outer profile is one curvature-continuous curve, so polished reflections flow without kinks.

## Seals

The goal is about 3 ATM (rain, hand-washing and splashes; no swimming), with the crown pushed in.

| Seal | How it works | Part | Fit (checked in CAD) |
|---|---|---|---|
| **Crystal** | A plastic I-ring gasket around the crystal. A watchmaker presses crystal and gasket into the seat together. | Hytrel "I" gasket, **34.0 mm** inside, 0.90 high. Listed as a 0.45 wall; measured **0.47–0.50** | Gasket about 34.97 free in a **34.87** seat: 0.05 squeeze per side (0.035–0.065 across the measured range) |
| **Caseback** | A spigot on the caseback enters the movement bore. An O-ring in a groove on the spigot seals against the bore wall, so the seal doesn't depend on screw torque. The spigot also centres the caseback, so no dowel pins are needed. A 30° lead-in at the bore mouth keeps the O-ring from being cut. | O-ring **32.0 × 0.6** | Groove Ø32.54, 1.7 % stretch, 20 % squeeze, 74 % groove fill |
| **Crown** | An O-ring sits in a groove inside the crown and seals on the outside of the crown tube's 3.0 mm end. The tube is the wear surface, and a watchmaker can replace it at service. | O-ring **3.0 × 0.5** | Groove Ø3.84, 16 % squeeze, 72 % fill. The tube end engages the crown 1.8 mm |

## Parts to buy

- **Movement**: Miyota 9039 (no date, 3 hands, 26.0 × 3.90 mm). Mount it rotated 90° so the stem exits at 12, and print the dial with 12 at the crown.
- **Crystal**: flat, Ø34.0 × 1.2 mm (mineral for the prototype, sapphire later).
- **Dial**: Ø33.4 × 0.61 mm (0.024" UV-printed stainless steel, laser-cut with a 2.0 mm centre hole), with Ø32.4 visible. It's clamped between the rehaut and the movement ring. It has no dial feet, so fix it to the movement with dial dots (thin adhesive pads). The caseback plate was thinned from 1.60 to 1.49 mm for this dial, so the case stays 13.75 mm. If a 0.50 mm dial is used instead, the caseback plate goes back to 1.60 mm. Don't shim or raise the ring: that lifts the movement and puts the stem off-centre in the crown tube.
- **Crown tube**: **80.135.42**: 2.5 mm case end, 3.0 mm crown end that's 2.5 mm long, 5.5 mm overall (Esslinger/Ofrei 80.135 series). The tube's shoulder sits in a 0.5 mm pocket, so 2.0 mm of the crown end stands proud and no filing is needed. The print hole is 2.7 mm, so glue the tube in.
- **Caseback screws**: 4 × **M1.4 × 4 mm** stainless, flat round (wafer) head, flat underneath, 0.3 mm pitch. Measured on the screws in hand: head Ø2.4 × 0.66 mm, 3.89 mm under the head, thread 1.35 mm. The head sits 0.04 mm below the tunnel ceiling in a Ø2.9 × 0.70 mm seat. There are two at 12 and two at 6, in the strap channel just past the bridge. Each screw grips 3.1 mm into the case.
- **Crystal gasket**: Esslinger individual Hytrel "I" gasket, 34.0 mm (series 84.045, about $6).
- **Caseback O-ring**: 32.0 × 0.6 mm, Esslinger .60 mm thickness O-ring gaskets (84.314.60), size 32 mm, pack of 3.
- **Crown O-ring**: 3.0 × 0.5 mm (OD 4.0), nitrile 70: Polymax (UK) part 3X0.5N70. It's only needed for final assembly, not for the print.
- **Strap**: 22 mm single-pass strap (one piece, no spring bars), **2.6 mm thick or less** at the case. The tunnel is 23.0 × 2.8 mm.

