import sys, numpy as np
from PIL import Image
def load(p): return np.asarray(Image.open(p).convert("L"), np.float32)
def shift(a, b):
    H, W = a.shape; w = np.outer(np.hanning(H), np.hanning(W))
    A = np.fft.fft2((a - a.mean()) * w); B = np.fft.fft2((b - b.mean()) * w)
    R = A * np.conj(B); R /= np.abs(R) + 1e-6; r = np.real(np.fft.ifft2(R)); i = np.unravel_index(np.argmax(r), r.shape)
    sy = i[0] if i[0] <= H // 2 else i[0] - H; sx = i[1] if i[1] <= W // 2 else i[1] - W
    return sx, sy, round(float(r[i]), 3)
d = sys.argv[1]; f0, f1 = sys.argv[2], sys.argv[3]
a = load(f"{d}/{f0}"); b = load(f"{d}/{f1}")
for spec in sys.argv[4:]:
    name, y0, y1, x0, x1 = spec.split(":"); y0, y1, x0, x1 = map(int, (y0, y1, x0, x1))
    print(name, shift(b[y0:y1, x0:x1], a[y0:y1, x0:x1]))
