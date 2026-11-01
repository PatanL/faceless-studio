"""Summarise frame_metrics.py output per video and per scene type.
usage: python -I aggregate.py <metrics.json> [more.json ...]
Scene types (automatic, by luminance/saturation of the frame):
  dark   meanL < 30 (space, night, title cards on navy)
  mid    30 <= meanL < 70 (most character/environment scenes)
  light  meanL >= 70 (cream infographic boards, white labs, sky)
"""
import sys, json
import numpy as np


def q(a, ps=(10, 50, 90)):
    return [round(float(np.percentile(a, p)), 3) for p in ps]


for path in sys.argv[1:]:
    m = json.load(open(path))
    print("=" * 70, "\n", path, len(m), "frames")
    groups = {"all": list(m.values())}
    for v in m.values():
        k = "dark" if v["meanL"] < 30 else ("light" if v["meanL"] >= 70 else "mid")
        groups.setdefault(k, []).append(v)
    for k, vs in groups.items():
        print(f"-- {k}: {len(vs)} frames ({len(vs)/len(m)*100:.0f}%)")
        for key in ("n_colours", "n_flat", "dark_frac", "outline", "edge_den", "grad_frac", "grain", "vignette", "blur_frac", "meanL"):
            print(f"   {key:10s} p10/p50/p90 = {q([v[key] for v in vs])}")
        print(f"   sat p50 (p10/p50/p90 of frame medians) = {q([v['sat'][1] for v in vs])}; frame sat p90 median = {q([v['sat'][2] for v in vs])[1]}")
        print(f"   val p50 (p10/p50/p90 of frame medians) = {q([v['val'][1] for v in vs])}; frame val p10 median = {q([v['val'][0] for v in vs])[1]}")
        # most common palette anchors: dominant cluster hex of each frame, binned to 3 bits/channel
        from collections import Counter
        c = Counter()
        for v in vs:
            for p in v["palette"][:3]:
                h = p["hex"]; r, g, b = int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)
                c["#%02x%02x%02x" % ((r // 32) * 32 + 16, (g // 32) * 32 + 16, (b // 32) * 32 + 16)] += p["cov"]
        print("   top colour bins (top-3 clusters, coverage-weighted):", [(h, round(w / len(vs), 3)) for h, w in c.most_common(10)])
