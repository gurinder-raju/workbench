"""Seal calculator for a watch case: O-rings and crystal gaskets.

Works out how hard each seal is squeezed, how far an O-ring is stretched,
and how full its groove is. These are the numbers used to size the three
seals in the current version (see the Seals section of the README).

Run:  python3 seal_calc.py

Rules of thumb used here, for static seals (they don't move in service):
    O-ring squeeze      15-25 %   (under ~10 % may leak, over ~30 % hard to assemble)
    O-ring stretch       0-5 %    (on the groove, so it stays seated)
    groove fill        <= 85 %    (room for the rubber to deform)
    crystal I-ring     0.03-0.07 mm per side (a firm, even press on the glass)
All dimensions in mm.
"""
import math
from dataclasses import dataclass


@dataclass
class RadialORing:
    """O-ring in a groove, sealing sideways against a bore or a shaft."""
    name: str
    ring_id: float          # O-ring inside diameter
    cross_section: float    # O-ring thickness
    groove_d: float         # diameter at the bottom of the groove
    seal_d: float           # diameter of the surface it seals against
    groove_w: float         # groove width

    def gland_depth(self):
        """Radial space the O-ring has to sit in."""
        return abs(self.seal_d - self.groove_d) / 2

    def squeeze(self):
        return (self.cross_section - self.gland_depth()) / self.cross_section

    def stretch(self):
        """Positive when the ring is stretched onto a groove on a spigot or post.
        For a groove inside a bore (the ring seals on a shaft) it is 0."""
        if self.groove_d < self.seal_d:          # groove on the inner part
            return self.groove_d / self.ring_id - 1
        return 0.0

    def fill(self):
        ring_area = math.pi / 4 * self.cross_section ** 2
        return ring_area / (self.groove_w * self.gland_depth())

    def verdict(self):
        notes = []
        if not 0.15 <= self.squeeze() <= 0.25:
            notes.append("squeeze outside 15-25 %")
        if self.stretch() > 0.05:
            notes.append("stretch over 5 %")
        if self.fill() > 0.85:
            notes.append("groove over 85 % full")
        return "OK" if not notes else "; ".join(notes)


@dataclass
class CrystalGasket:
    """Plastic I-ring gasket pressed between a flat crystal and its seat."""
    name: str
    crystal_d: float
    wall: float             # gasket wall thickness
    seat_d: float           # case opening

    def squeeze_per_side(self):
        return (self.crystal_d + 2 * self.wall - self.seat_d) / 2

    def verdict(self):
        s = self.squeeze_per_side()
        return "OK" if 0.03 <= s <= 0.07 else "outside 0.03-0.07 mm per side"


def seat_for(crystal_d, wall, squeeze=0.05):
    """Seat diameter that gives the target squeeze per side."""
    return crystal_d + 2 * wall - 2 * squeeze


def main():
    caseback = RadialORing("Caseback O-ring 32.0 x 0.6", ring_id=32.0, cross_section=0.6,
                           groove_d=32.54, seal_d=33.50, groove_w=0.80)
    crown = RadialORing("Crown O-ring 3.0 x 0.5", ring_id=3.0, cross_section=0.5,
                        groove_d=3.84, seal_d=3.00, groove_w=0.65)
    print("%-28s %8s %8s %8s  %s" % ("O-ring", "squeeze", "stretch", "fill", "verdict"))
    for o in (caseback, crown):
        print("%-28s %7.0f%% %7.1f%% %7.0f%%  %s"
              % (o.name, 100 * o.squeeze(), 100 * o.stretch(), 100 * o.fill(), o.verdict()))

    print()
    print("Crystal gasket, 34.0 mm crystal, seat 34.87 mm, wall measured 0.47-0.50 mm:")
    for wall in (0.47, 0.485, 0.50):
        g = CrystalGasket("I-ring", crystal_d=34.0, wall=wall, seat_d=34.87)
        print("  wall %.3f -> squeeze %.3f mm per side  %s"
              % (wall, g.squeeze_per_side(), g.verdict()))
    print("  seat for a 0.485 wall at 0.05 squeeze: %.2f" % seat_for(34.0, 0.485))


if __name__ == "__main__":
    main()
