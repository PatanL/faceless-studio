"""Per-frame motion metrics. usage: motion.py ffmpeg video fps out.npz [start dur]"""
import sys, subprocess, numpy as np
ff, v, fps, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
W, H = 256, 144
cmd = [ff, "-nostdin", "-loglevel", "error", "-threads", "3"]
if len(sys.argv) > 6: cmd += ["-ss", sys.argv[5], "-t", sys.argv[6]]
cmd += ["-i", v, "-vf", f"fps={fps},scale={W}:{H},format=gray", "-f", "rawvideo", "-"]
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
win = np.outer(np.hanning(H), np.hanning(W)).astype(np.float32)
prev = None; prevF = None
mad, chg, dx, dy, pk, mean = [], [], [], [], [], []
hist = []
while True:
    buf = p.stdout.read(W * H)
    if len(buf) < W * H: break
    a = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.float32)
    mean.append(a.mean()); hist.append(np.histogram(a, 32, (0, 256))[0])
    F = np.fft.fft2((a - a.mean()) * win)
    if prev is not None:
        d = np.abs(a - prev); mad.append(d.mean()); chg.append((d > 6).mean())
        R = F * np.conj(prevF); R /= np.abs(R) + 1e-6
        r = np.real(np.fft.ifft2(R)); i = np.unravel_index(np.argmax(r), r.shape)
        sy = i[0] if i[0] <= H // 2 else i[0] - H; sx = i[1] if i[1] <= W // 2 else i[1] - W
        # subpixel parabolic refine
        def ref(c, n, ax):
            m1 = r[(i[0] - (ax == 0)) % H, (i[1] - (ax == 1)) % W]; p1 = r[(i[0] + (ax == 0)) % H, (i[1] + (ax == 1)) % W]; c0 = r[i]
            den = (m1 - 2 * c0 + p1); return c + (0.5 * (m1 - p1) / den if abs(den) > 1e-9 else 0)
        dx.append(ref(sx, W, 1)); dy.append(ref(sy, H, 0)); pk.append(r[i])
    else:
        mad.append(0); chg.append(0); dx.append(0); dy.append(0); pk.append(0)
    prev, prevF = a, F
np.savez_compressed(out, fps=fps, mad=np.array(mad, np.float32), chg=np.array(chg, np.float32), dx=np.array(dx, np.float32),
                    dy=np.array(dy, np.float32), pk=np.array(pk, np.float32), mean=np.array(mean, np.float32), hist=np.array(hist, np.int32))
print(out, len(mad))
