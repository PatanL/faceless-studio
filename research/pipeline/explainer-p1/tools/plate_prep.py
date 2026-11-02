"""explainer-p1 plates: Codex PNG -> crisp 1296x2304 JPG for studio/public/plates/explainer-p1/, plus measurements.

For each plate: vectorize with vtracer (experiments/asset-gen "medium" preset, NOTES.md Path A), rasterize the SVG at
the 1.2x overscan size the plate layer uses (1296x2304) so flat edges stay crisp under camera push-ins (a Lanczos
upscale of the 941x1672 PNG goes soft), and report:
  waterline  screen y (0..1) of the water surface in a cut-away plate (largest row-to-row colour jump in the top half)
  L*         mean CIELAB lightness of the whole plate and of its water band (the lightness ladder, analysis rule 6)
  dE         mean-colour CIEDE76 to the previous plate in ladder order (analysis rule 5: a setting change must show, >= 10)

usage (from experiments/asset-gen, its venv has vtracer + cv2):
  .venv/bin/python ../../research/pipeline/explainer-p1/tools/plate_prep.py
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np
import vtracer

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
GEN = os.path.join(ROOT, "experiments/asset-gen/gen")
OUT = os.path.join(ROOT, "studio/public/plates/explainer-p1")
VEC = os.path.join(ROOT, "experiments/asset-gen/vec")
W, H = 1296, 2304
MEDIUM = dict(colormode="color", hierarchical="stacked", mode="spline", filter_speckle=6, color_precision=6,
              layer_difference=16, corner_threshold=60, length_threshold=4.0, splice_threshold=45, path_precision=3)
# ladder order (the story's order): (name, split = has a waterline with sky above, chosen Codex version)
PLATES = [("cambrian_split", True, "A2"), ("cambrian_under", False, "A2"), ("devonian", False, "A"),
          ("cretaceous_dusk", True, "A"), ("miocene", False, "A"), ("today_coast", True, "A"),
          ("today_below", False, "A")]


def waterline(img):
    """y (0..1) of the strongest full-width horizontal colour edge in the top 60 % (the surface line)"""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(float)
    rows = lab.mean(axis=1)
    d = np.linalg.norm(np.diff(rows, axis=0), axis=1)
    top = int(len(d) * 0.6)
    y = int(np.argmax(d[int(len(d) * 0.1):top])) + int(len(d) * 0.1)
    return round((y + 1) / img.shape[0], 3)


def lab_mean(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(float)
    m = lab.reshape(-1, 3).mean(axis=0)
    return np.array([m[0] * 100 / 255, m[1] - 128, m[2] - 128])


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(VEC, exist_ok=True)
    stats, prev = {}, None
    names = sys.argv[1:] or [p[0] for p in PLATES]
    for name, split, ver in PLATES:
        if name not in names:
            continue
        src = os.path.join(GEN, f"p1_plate_{name}_{ver}.png")
        if not os.path.exists(src):
            print("missing", src)
            continue
        img = cv2.imread(src)
        svg = os.path.join(VEC, f"p1_{name}_medium.svg")
        vtracer.convert_image_to_svg_py(src, svg, **MEDIUM)
        png = os.path.join(VEC, f"p1_{name}_{W}.png")
        subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), svg, "-o", png], check=True)
        big = cv2.imread(png)
        cv2.imwrite(os.path.join(OUT, f"{name}.jpg"), big, [cv2.IMWRITE_JPEG_QUALITY, 90])
        back = cv2.resize(big, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)
        mse = ((back.astype(float) - img.astype(float)) ** 2).mean()
        wl = waterline(img) if split else None
        lab = lab_mean(img)
        water = img[int(img.shape[0] * (wl or 0)):] if split else img
        s = {"src": os.path.relpath(src, ROOT), "jpg": f"plates/explainer-p1/{name}.jpg", "native": list(img.shape[1::-1]),
             "paths": open(svg).read().count("<path"), "psnr": float(round(10 * np.log10(255 ** 2 / max(mse, 1e-6)), 1)),
             "waterline": wl, "L": float(round(lab[0], 1)), "L_water": float(round(lab_mean(water)[0], 1)),
             "dE_prev": None if prev is None else round(float(np.linalg.norm(lab - prev)), 1)}
        prev = lab
        stats[name] = s
        print(name, s, flush=True)
    path = os.path.join(ROOT, "research/pipeline/explainer-p1/plates.json")
    old = json.load(open(path)) if os.path.exists(path) else {}
    old.update(stats)
    json.dump(old, open(path, "w"), indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()
