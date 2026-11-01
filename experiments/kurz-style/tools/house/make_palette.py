"""Generate house/palette.json: the house-style ramps, defined in OKLCH, gamut-fitted to sRGB.
usage: python3 -I make_palette.py <out.json>
Each ramp is a list of (L, C) at one OKLCH hue. Steps are numbered 0 (darkest) .. n (lightest).
"""
import sys, os, json, colorsys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from oklab import oklch_fit, hexs

RAMPS = {
  # role: cool ambient / darkest darks. Never black: the deepest step is a saturated teal-ink.
  "ink":    (228, [(0.17, 0.040), (0.23, 0.050), (0.29, 0.060), (0.36, 0.070), (0.43, 0.075)]),
  # role: water, glass, cool rim light, cool emitters
  "tide":   (198, [(0.48, 0.085), (0.58, 0.105), (0.68, 0.120), (0.77, 0.120), (0.86, 0.095), (0.93, 0.055)]),
  # role: life, plants, secondary cool subject (Kurzgesagt avoids green; we use it)
  "kelp":   (162, [(0.30, 0.060), (0.40, 0.085), (0.52, 0.110), (0.63, 0.125), (0.75, 0.115)]),
  # role: distance, night sky, space field (kept blue, below the violet band)
  "dusk":   (258, [(0.20, 0.060), (0.28, 0.080), (0.37, 0.100), (0.47, 0.110), (0.58, 0.110)]),
  # role: daylight sky and air
  "sky":    (236, [(0.55, 0.105), (0.65, 0.105), (0.75, 0.090), (0.84, 0.068), (0.93, 0.038)]),
  # role: warm subjects, flesh, coral, danger-adjacent warmth
  "coral":  (34,  [(0.38, 0.110), (0.48, 0.150), (0.58, 0.170), (0.68, 0.160), (0.78, 0.120)]),
  # role: the lantern: key light, emitters, fire, glints of heat
  # hue drifts toward yellow as it brightens (hotter = yellower), like a real flame
  "amber":  (66,  [(0.45, 0.115, 56), (0.58, 0.145, 60), (0.70, 0.160, 66), (0.80, 0.160, 74), (0.88, 0.140, 86), (0.96, 0.070, 96)]),
  # role: earth, sand, rock, wood, paper
  "ochre":  (78,  [(0.40, 0.065), (0.52, 0.085), (0.64, 0.095), (0.76, 0.095), (0.86, 0.075)]),
  # role: our white. Pure #fff is reserved for specular glints (<= 0.3 % of a frame)
  "bone":   (86,  [(0.80, 0.025), (0.88, 0.024), (0.95, 0.018)]),
  # role: brand accent. ONLY the YOU marker, the one key number, and threat
  "signal": (24,  [(0.45, 0.170), (0.58, 0.215)]),
}

out = {"space": "OKLCH (L 0..1, C, h deg); hex is gamut-fitted sRGB", "ramps": {}}
for name, (h, steps) in RAMPS.items():
    lst = []
    for i, st in enumerate(steps):
        L, C = st[0], st[1]
        hs = st[2] if len(st) > 2 else h
        rgb, Cf = oklch_fit(L, C, hs)
        hh, ss, vv = colorsys.rgb_to_hsv(*rgb)
        lst.append({"token": f"{name}-{i}", "hex": hexs(rgb), "oklch": [L, round(Cf, 3), hs],
                    "hsv": [round(hh * 360), round(ss, 2), round(vv, 2)]})
    out["ramps"][name] = lst
json.dump(out, open(sys.argv[1], "w"), indent=1)
for name, lst in out["ramps"].items():
    print(f"{name:7s}", "  ".join(f'{t["hex"]} H{t["hsv"][0]:3d} S{t["hsv"][1]:.2f} V{t["hsv"][2]:.2f}' for t in lst))
