"""Fair (curvature-continuous) outer profile of the pebble case.

The profile is built intrinsically: curvature k(s) = exp(g(s)) along arc length,
with g a smooth cubic B-spline.  Integrating the tangent angle gives a curve whose
curvature never jumps, so polished reflections flow without kinks.

The curve runs from the bezel crest at the crystal edge (tangent horizontal,
pointing outward), over the widest point (tangent vertical), along the belly and
under the case to the axis (tangent horizontal, pointing inward).

Targets describe the intended pebble shape of the 42 mm case.
"""
import numpy as np
from scipy.interpolate import BSpline
from scipy.optimize import least_squares

import params as P

N_COEF = 12
M = 4000


def _basis(n_coef, u):
    k = 3
    inner = np.linspace(0, 1, n_coef - k + 1)
    t = np.r_[[0] * k, inner, [1] * k]
    B = np.zeros((len(u), n_coef))
    for i in range(n_coef):
        c = np.zeros(n_coef)
        c[i] = 1
        B[:, i] = BSpline(t, c, k)(u)
    return B


U = np.linspace(0, 1, M)
BASIS = _basis(N_COEF, U)


def build(x):
    L = x[0]
    g = BASIS @ x[1:]
    kappa = np.exp(g)
    s = U * L
    ds = np.diff(s)
    phi = np.r_[0, np.cumsum(0.5 * (kappa[1:] + kappa[:-1]) * ds)]
    c, sn = np.cos(phi), np.sin(phi)
    r = P.R_BEZEL_IN + np.r_[0, np.cumsum(0.5 * (c[1:] + c[:-1]) * ds)]
    z = P.Z_TOP - np.r_[0, np.cumsum(0.5 * (sn[1:] + sn[:-1]) * ds)]
    return s, r, z, phi, kappa


# Upper roll: quarter ellipse from crest to widest point.
_t = np.linspace(0.15, 1.45, 7)
UPPER_TARGETS = np.c_[P.R_BEZEL_IN + (P.R_MAX - P.R_BEZEL_IN) * np.cos(_t),
                      P.Z_MAX + (P.Z_TOP - P.Z_MAX) * np.sin(_t)]
# Lower belly: long and full (r at depth below the widest point), turning softly
# onto a nearly flat wrist face under the bridge.
LOWER_TARGETS = np.array([
    [20.86, P.Z_MAX - 1.55],
    [20.55, P.Z_MAX - 2.85],
    [20.05, P.Z_MAX - 4.15],
    [19.30, P.Z_MAX - 5.45],
    [18.00, P.Z_MAX - 6.65],
])
BOTTOM_FLAT_R = 13.6       # bridge corners reach r = 13.5
BOTTOM_FLAT_Z = 0.32


def residuals(x):
    s, r, z, phi, kappa = build(x)
    res = []
    W = 60.0
    res += [8 * W * (phi[-1] - np.pi), W * r[-1], W * z[-1]]
    # widest point: phi = pi/2 at (R_MAX, Z_MAX)
    i = np.searchsorted(phi, np.pi / 2)
    res += [W * (r[i] - P.R_MAX), W * (z[i] - P.Z_MAX)]
    pts = np.c_[r, z]
    for tgt in np.r_[UPPER_TARGETS, LOWER_TARGETS]:
        d = np.min(np.hypot(*(pts - tgt).T))
        res.append(6.0 * d)
    # nearly flat wrist face under the bridge
    j = np.argmin(np.abs(r[i:] - BOTTOM_FLAT_R)) + i
    res.append(20.0 * max(0.0, z[j] - BOTTOM_FLAT_Z))
    # monotone tangent angle is automatic (kappa > 0); keep g smooth
    g = x[1:]
    res += list(1.2 * np.diff(g, 2))
    return np.array(res)


def fit():
    x0 = np.r_[34.0, np.log(np.linspace(0.12, 0.05, N_COEF))]
    sol = least_squares(residuals, x0, method="trf", max_nfev=4000)
    return sol.x


def profile_points(n=160):
    """Return (r, z) samples of the fitted profile from crest to axis."""
    x = fit()
    s, r, z, phi, kappa = build(x)
    # resample with denser spacing where curvature is high
    w = np.sqrt(kappa) + 0.05
    cum = np.r_[0, np.cumsum(0.5 * (w[1:] + w[:-1]) * np.diff(s))]
    q = np.interp(np.linspace(0, cum[-1], n), cum, np.arange(len(s)))
    idx = np.unique(np.round(q).astype(int))
    r_s, z_s = r[idx], z[idx]
    r_s[-1], z_s[-1] = 0.0, 0.0
    return np.c_[r_s, z_s], (s, r, z, phi, kappa)


if __name__ == "__main__":
    pts, (s, r, z, phi, kappa) = profile_points()
    i = np.searchsorted(phi, np.pi / 2)
    print("arc length %.2f  end r %.3f z %.3f phi_end %.4f" % (s[-1], r[-1], z[-1], phi[-1]))
    print("widest r %.3f at z %.3f  (target %.2f @ %.2f)" % (r.max(), z[np.argmax(r)], P.R_MAX, P.Z_MAX))
    for zz in [13, 12, 11, 10, 9, 8, 7, 6, 5.2, 3.9, 2.5, 1.1, 0.5, 0.3]:
        j = i + np.argmin(np.abs(z[i:] - zz)) if zz < P.Z_MAX else np.argmin(np.abs(z[:i] - zz))
        print("  z %5.2f  r %6.3f   radius of curvature %6.2f" % (zz, r[j], 1 / kappa[j]))
    print("bottom z at r=13.5: %.3f" % z[i + np.argmin(np.abs(r[i:] - 13.5))])
    print("min/max radius of curvature: %.2f / %.1f" % (1 / kappa.max(), 1 / kappa.min()))
