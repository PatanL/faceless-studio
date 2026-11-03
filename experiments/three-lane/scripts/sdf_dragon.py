"""Code-sculpted Chinese dragon head (our own code; visual track round 3, owner: "everything in code", the Codex key frame
scratchpad kf/out_1.png as the shape reference). Signed-distance primitives joined by smooth unions, meshed with
marching cubes, exported as a compact JSON mesh the kit loads (kit/codemodels.ts).

usage: python3 sdf_dragon.py <out.json> [--step 0.012]

Shapes (head points +z, y up, ~1.2 m nose to mane): a domed cranium; a long snout ending in a raised nose pad with
round nostrils; a rolled upper lip; heavy brow ridges over deep eye sockets; cheek bulges; a long open lower jaw with a
chin; the mouth cavity cut between the jaws; two long segmented horns sweeping back and curling forward; a mane of
flame-blade fins fanning back from the cheeks and skull; beard fins under the jaw; an S-curved neck with a dorsal crest.
Fine detail (scales, engraving) is a normal map in the material; whiskers, teeth, eyes and the ball are separate
kit geometry placed at the anchors exported here.
"""
import base64, json, sys
import numpy as np
from skimage.measure import marching_cubes

STEP = float(sys.argv[sys.argv.index("--step") + 1]) if "--step" in sys.argv else 0.012
B0, B1 = np.array([-0.62, -1.25, -1.05]), np.array([0.62, 1.15, 1.05])


def grid():
    xs = [np.arange(B0[i], B1[i], STEP) for i in range(3)]
    X, Y, Z = np.meshgrid(*xs, indexing="ij")
    return np.stack([X, Y, Z], -1), xs


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def smax(a, b, k):  # smooth intersection: max(a, b); subtract b from a with smax(a, -b)
    return -smin(-a, -b, k)


def ellipsoid(p, c, r, R=None):
    q = p - c
    if R is not None: q = q @ R
    k0 = np.linalg.norm(q / r, axis=-1); k1 = np.linalg.norm(q / (r * r), axis=-1)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-6)


def sphere(p, c, r): return np.linalg.norm(p - c, axis=-1) - r


def round_cone(p, a, b, ra, rb):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ba = b - a; pa = p - a
    h = np.clip((pa @ ba) / (ba @ ba), 0, 1)
    d = np.linalg.norm(pa - h[..., None] * ba, axis=-1)
    return d - (ra + (rb - ra) * h)


def chain(p, pts, r0, r1, ridge=0.0, k=0.02):
    """a tube through pts with radius r0 -> r1; ridge > 0 adds ring segments (horns)"""
    n = len(pts) - 1; d = None
    for i in range(n):
        ra = r0 + (r1 - r0) * i / n; rb = r0 + (r1 - r0) * (i + 1) / n
        di = round_cone(p, pts[i], pts[i + 1], ra, rb)
        d = di if d is None else smin(d, di, k)
    if ridge:
        # ring bumps along the tube: modulate by the distance from the start along the path
        s = np.linalg.norm(p - np.asarray(pts[0]), axis=-1)
        d = d - ridge * np.maximum(0, np.sin(s * 70))
    return d


def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]); Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]); Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def blade(p, c, length, width, ax, ay, az):
    """a flame-like fin: a thin ellipsoid swept back along its local z, tilted by (ax, ay, az)"""
    return ellipsoid(p, np.asarray(c, float) + rot(ax, ay, az) @ np.array([0, 0, -length * 0.5]), np.array([0.018, width, length * 0.5]), rot(ax, ay, az))


def dragon(p):
    d = ellipsoid(p, np.array([0, 0.13, -0.08]), np.array([0.29, 0.27, 0.33]))                    # cranium
    d = smin(d, round_cone(p, [0, 0.12, 0.08], [0, 0.13, 0.6], 0.2, 0.13), 0.09)                  # snout: shorter, rising (key frame)
    d = smin(d, ellipsoid(p, np.array([0, 0.21, 0.63]), np.array([0.18, 0.14, 0.13])), 0.07)      # nose pad: a big curled bulb
    for s in (-1, 1):
        d = smin(d, round_cone(p, [s * 0.15, -0.01, 0.06], [s * 0.12, 0.02, 0.64], 0.065, 0.05), 0.05)     # rolled upper lip
        d = smin(d, round_cone(p, [s * 0.11, 0.30, 0.16], [s * 0.21, 0.37, -0.12], 0.075, 0.05), 0.06)     # brow ridge
        d = smin(d, ellipsoid(p, np.array([s * 0.2, 0.0, -0.08]), np.array([0.13, 0.16, 0.19])), 0.07)     # cheek
        d = smin(d, round_cone(p, [s * 0.06, 0.27, 0.3], [s * 0.06, 0.3, 0.52], 0.045, 0.035), 0.04)       # snout ridge
    for s in (-1, 1):
        d = smax(d, -sphere(p, np.array([s * 0.08, 0.28, 0.72]), 0.05), 0.015)                    # nostrils
        d = smax(d, -sphere(p, np.array([s * 0.19, 0.22, 0.16]), 0.075), 0.02)                     # eye sockets
    # lower jaw, open, with a chin; then the mouth cavity between the jaws
    jaw = round_cone(p, [0, -0.13, -0.06], [0, -0.48, 0.5], 0.14, 0.08)
    jaw = smin(jaw, ellipsoid(p, np.array([0, -0.5, 0.49]), np.array([0.1, 0.07, 0.08])), 0.04)
    d = smin(d, jaw, 0.05)
    cav = round_cone(p, [0, -0.1, 0.0], [0, -0.27, 0.62], 0.12, 0.1)
    d = smax(d, -cav, 0.03)
    # horns: long, segmented, sweeping back and up, curling forward at the tips
    for s in (-1, 1):
        pts = [[s * 0.10, 0.34, -0.14], [s * 0.16, 0.56, -0.34], [s * 0.21, 0.80, -0.46], [s * 0.20, 1.0, -0.38], [s * 0.15, 1.08, -0.26]]
        d = smin(d, chain(p, pts, 0.07, 0.012, ridge=0.006), 0.04)
    # mane: flame blades fanning back from the skull and cheeks, beard fins under the jaw
    for s in (-1, 1):
        for k in range(8):
            a = -0.2 + k * 0.32
            c = [s * (0.2 + 0.05 * np.cos(a)), 0.05 + 0.3 * np.sin(a) * 0.9, -0.22 - 0.05 * k]
            d = smin(d, blade(p, c, 0.42 + 0.06 * (k % 3), 0.05, -0.35 - 0.15 * np.sin(a), s * (0.55 + 0.05 * k), s * 0.25), 0.03)
        for k in range(3):
            d = smin(d, blade(p, [s * 0.06, -0.42, 0.42 - k * 0.12], 0.26, 0.035, 1.2, s * 0.15, 0), 0.03)
    for k in range(5):                                                                             # crest along the top
        d = smin(d, blade(p, [0, 0.36 - 0.02 * k, -0.12 - 0.12 * k], 0.28, 0.06, -0.55, 0, 0), 0.03)
    # neck: an S-curve back and down into the wall, a dorsal crest
    neck = chain(p, [[0, 0.02, -0.25], [0, -0.22, -0.58], [0, -0.66, -0.62], [0, -1.05, -0.78]], 0.22, 0.2, k=0.06)
    d = smin(d, neck, 0.08)
    for k in range(6):
        y = -0.12 - k * 0.17; z = -0.62 - 0.05 * np.sin(k)
        d = smin(d, blade(p, [0, y, z - 0.18], 0.24, 0.05, -0.2 - 0.12 * k, 0, 0), 0.03)
    return d


def main():
    out = sys.argv[1]
    P, xs = grid()
    D = dragon(P.reshape(-1, 3)).reshape(P.shape[:3])
    v, f, _, _ = marching_cubes(D, 0.0, spacing=(STEP, STEP, STEP))
    v = v + B0
    # smooth normals from the field's gradient
    g = np.stack(np.gradient(D, STEP), -1)
    idx = np.clip(np.round((v - B0) / STEP).astype(int), 0, np.array(D.shape) - 1)
    n = g[idx[:, 0], idx[:, 1], idx[:, 2]]; n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    # cylindrical UVs round the head/neck axis for the scale and engraving maps
    u = (np.arctan2(v[:, 1], v[:, 0]) / (2 * np.pi) + 0.5); w = (v[:, 2] - v[:, 1]) * 1.6
    uv = np.stack([u * 6, w * 3], 1)
    b64 = lambda a, t: base64.b64encode(np.ascontiguousarray(a, t).tobytes()).decode()
    anchors = {
        "eyes": [[s * 0.19, 0.22, 0.17] for s in (-1, 1)],
        "nostrils": [[s * 0.08, 0.28, 0.73] for s in (-1, 1)],
        "upperTeeth": [[s * (0.14 - 0.012 * k), -0.06, 0.12 + 0.075 * k] for s in (-1, 1) for k in range(7)],
        "lowerTeeth": [[s * (0.11 - 0.008 * k), -0.22 - 0.035 * k, 0.1 + 0.06 * k] for s in (-1, 1) for k in range(7)],
        "mouth": [0, -0.2, 0.42], "whiskerRoots": [[s * 0.16, 0.16, 0.68] for s in (-1, 1)], "tongue": [0, -0.24, 0.3],
    }
    json.dump({"generator": "experiments/three-lane/scripts/sdf_dragon.py", "step": STEP, "count": int(len(v)), "tris": int(len(f)),
               "position": b64(v, np.float32), "normal": b64(n, np.float32), "uv": b64(uv, np.float32), "index": b64(f, np.uint32), "anchors": anchors}, open(out, "w"))
    print(f"vertices {len(v)} triangles {len(f)} -> {out}")


if __name__ == "__main__":
    main()
