# usage: python3 kf_plate.py <depth.npy> <public/kf/<id>_plate.json>   (also writes <id>_plate_limits.json: stretch share and frame coverage per camera move)
# 2.5D plate from a key frame + monocular depth (our own code): disparity -> metric depth, a camera-space grid mesh with
# the key frame's UVs (so it is projected from the key camera), and a stretch analysis of camera moves.
import sys, json, base64, numpy as np
disp = np.load(sys.argv[1]); out = sys.argv[2]
H, W = disp.shape; FOV = 40.0; NEAR, FAR = 1.1, 26.0
dn = (disp - np.percentile(disp, 0.5)) / (np.percentile(disp, 99.5) - np.percentile(disp, 0.5)); dn = np.clip(dn, 0, 1)
Z = 1.0 / (dn * (1 / NEAR - 1 / FAR) + 1 / FAR)                                   # metres
GW, GH = 180, 320
ys, xs = np.linspace(0, H - 1, GH).astype(int), np.linspace(0, W - 1, GW).astype(int)
z = Z[np.ix_(ys, xs)]
th = np.tan(np.radians(FOV / 2)); asp = W / H
u, v = np.meshgrid(np.linspace(0, 1, GW), np.linspace(0, 1, GH))
X = (u - 0.5) * 2 * th * asp * z; Y = -(v - 0.5) * 2 * th * z
P = np.stack([X, Y, -z], -1)                                                       # camera space, -z forward
idx = []
for j in range(GH - 1):
    for i in range(GW - 1):
        a = j * GW + i; idx += [a, a + GW, a + 1, a + 1, a + GW, a + GW + 1]
idx = np.array(idx, np.uint32); pos = P.reshape(-1, 3).astype(np.float32); uv = np.stack([u, 1 - v], -1).reshape(-1, 2).astype(np.float32)
b = lambda a: base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()
json.dump({"fov": FOV, "aspect": asp, "grid": [GW, GH], "position": b(pos), "uv": b(uv), "index": b(idx)}, open(out, "w"))

# stretch analysis: per triangle screen area after the move / before; "rubber" triangles span a depth jump (z ratio > 1.25)
tri = idx.reshape(-1, 3); Pv = pos
def project(P3, R, t):
    q = (P3 - t) @ R                                     # into the new camera (R columns = camera axes)
    zz = -q[:, 2]; return np.stack([q[:, 0] / (zz * th * asp), q[:, 1] / (zz * th)], 1), zz
def area(S):
    a, b2, c = S[tri[:, 0]], S[tri[:, 1]], S[tri[:, 2]]
    return 0.5 * np.abs((b2[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b2[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0]))
S0, z0 = project(Pv, np.eye(3), np.zeros(3)); A0 = area(S0)
zt = z0[tri]; rubber = zt.max(1) / zt.min(1) > 1.25
def report(R, t, fov_scale=1.0):
    S1, z1 = project(Pv, R, t); S1 = S1 / fov_scale; A1 = area(S1)
    zc0 = z0[tri].mean(1); zc1 = z1[tri].mean(1)
    front = (z1[tri] > 0.15).all(1)
    inside = front & (np.abs(S1[tri].mean(1)) <= 1).all(1)
    # stretch beyond the rigid magnification a triangle at its depth should get: rubber sheets across depth jumps
    norm = (A1 / np.maximum(A0, 1e-12)) / np.maximum((zc0 / np.maximum(zc1, 1e-3)) ** 2 / fov_scale ** 2, 1e-6)
    stretched = inside & (norm > 1.6)
    share = float(np.clip(A1[stretched].sum() / 4.0, 0, 1))
    # coverage: the share of the new frame the plate still covers (frame corners beyond the key frame show as holes)
    g = np.linspace(-0.98, 0.98, 41); GX, GY = np.meshgrid(g, g)
    # map new-view NDC back to the key view with depth ~ median to test whether it lands inside the key frame
    zm = np.median(z0); dirs = np.stack([GX * th * asp * fov_scale, GY * th * fov_scale, -np.ones_like(GX)], -1)
    Pw = (dirs * zm) @ R.T + t; q, zz = project(Pw.reshape(-1, 3), np.eye(3), np.zeros(3))
    cover = float(((np.abs(q) <= 1).all(1)).mean())
    return round(share, 4), round(cover, 3)
def rotY(a): c, s = np.cos(a), np.sin(a); return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
def rotX(a): c, s = np.cos(a), np.sin(a); return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
res = {"push_m": {}, "orbit_deg_about_3.2m": {}, "tilt_deg": {}, "truck_m": {}}
for d in [0.1, 0.2, 0.35, 0.5, 0.8, 1.2, 1.8]: res["push_m"][d] = report(np.eye(3), np.array([0, 0, -d]))
piv = np.array([0, 0, -3.2])
for a in [1, 2, 4, 6, 10, 15]: R = rotY(np.radians(a)); res["orbit_deg_about_3.2m"][a] = report(R, piv - R @ (piv))
for a in [1, 2, 5, 8]: res["tilt_deg"][a] = report(rotX(np.radians(-a)), np.zeros(3))
res["zoom_x"] = {z: report(np.eye(3), np.zeros(3), 1 / z) for z in [1.2, 1.6, 2.0, 3.0]}
for d in [0.05, 0.1, 0.2, 0.4]: res["truck_m"][d] = report(np.eye(3), np.array([d, 0, 0]))
json.dump(res, open(out.replace(".json", "_limits.json"), "w"), indent=1); print(json.dumps(res))
