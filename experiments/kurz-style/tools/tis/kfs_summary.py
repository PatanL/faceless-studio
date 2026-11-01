"""Summarise ../frame_stats.py output (the Kurzgesagt studies' tool) so TIS numbers line up
1:1 with study-kurz-space.md / study-kurz-bio.md §1.
usage: python -I kfs_summary.py <kfs.json> [...]
"""
import sys, json
import numpy as np

for p in sys.argv[1:]:
    r = json.load(open(p))
    med = lambda k, i=None: float(np.median([x[k][i] if i is not None else x[k] for x in r]))
    top1 = [x["palette"][0][1] for x in r]; top3 = [sum(c for _, c in x["palette"][:3]) for x in r]
    hh = np.mean([x["hue_hist"] for x in r], axis=0)
    darkbg = np.mean([max(int(x["border"][i:i + 2], 16) for i in (1, 3, 5)) / 255 < 0.25 for x in r])
    print(f"== {p}  n={len(r)}")
    print(f"  median saturation (all px) {med('sat_p', 1):.2f}; chromatic px {med('sat_chroma_med'):.2f}; median value {med('val_p', 1):.2f}")
    print(f"  dark-background frames (border V<0.25) {darkbg*100:.0f}%")
    fam = [x["hue_families"] for x in r]
    print(f"  hue families/frame median {np.median(fam):.0f} (p10 {np.percentile(fam,10):.0f}, p90 {np.percentile(fam,90):.0f})")
    b80 = [x["n_bins80"] for x in r]; b95 = [x["n_bins95"] for x in r]
    print(f"  4-bit bins covering 80%: median {np.median(b80):.0f}; 95%: median {np.median(b95):.0f} (p10 {np.percentile(b95,10):.0f}-p90 {np.percentile(b95,90):.0f})")
    print(f"  largest cluster coverage median {np.median(top1)*100:.0f}%; top-3 {np.median(top3)*100:.0f}%")
    print(f"  near-white share median {med('near_white_frac')*100:.1f}%; dark (V<0.2) share median {med('dark_frac')*100:.1f}%")
    print("  hue mix of chromatic px (30deg bins from red):", " ".join(f"{i*30}-{i*30+30}:{v*100:.0f}%" for i, v in enumerate(hh)))
