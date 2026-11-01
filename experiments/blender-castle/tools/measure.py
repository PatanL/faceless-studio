# VISUAL_GRAMMAR section 12 colour checks on rendered frames (numpy only; same definitions as section 4.1).
import sys, json, colorsys
import numpy as np
from PIL import Image
lum, sat, blue, warm, ccl = [], [], 0, 0, []
tot = 0
for p in sys.argv[1:]:
    a = np.asarray(Image.open(p).convert('RGB').resize((270, 480)), dtype=np.float32) / 255
    y = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    mx, mn = a.max(-1), a.min(-1); s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    lum.append(np.median(y) * 255); sat.append(np.median(s))
    h = np.zeros_like(mx); d = np.maximum(mx - mn, 1e-6)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    m = (s > 0.25) & (mx > 0.15); tot += m.sum()
    blue += ((h >= 180) & (h < 240) & m).sum(); warm += (((h < 60)) & m).sum()
    H, Wd = y.shape; c = y[H // 3:2 * H // 3, Wd // 3:2 * Wd // 3].mean(); k = np.concatenate([y[:H // 6, :Wd // 6].ravel(), y[:H // 6, -Wd // 6:].ravel(), y[-H // 6:, :Wd // 6].ravel(), y[-H // 6:, -Wd // 6:].ravel()]).mean()
    ccl.append((c - k) * 255)
print(json.dumps({'frames': len(sys.argv) - 1, 'median_luma': round(float(np.median(lum)), 1), 'median_sat': round(float(np.median(sat)), 3),
                  'blue_share': round(blue / tot, 3), 'warm_share': round(warm / tot, 3), 'centre_minus_corner': round(float(np.median(ccl)), 1)}))
