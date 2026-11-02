"""Path A: auto-vectorize a generated PNG with vtracer at several presets, rasterize back with rsvg-convert,
and record path count, SVG size and fidelity (PSNR + mean abs error vs source).
usage: .venv/bin/python scripts/vectorize.py gen/a_orca_side_v2.png orca"""
import sys, os, re, subprocess, json
import vtracer, numpy as np, cv2
src, tag = sys.argv[1], sys.argv[2]
G = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = os.path.join(G, 'vec'); os.makedirs(out, exist_ok=True)
PRESETS = {
  # coarse: few big flat regions (animator-friendly, loses marks)
  'coarse':  dict(colormode='color', hierarchical='stacked', mode='spline', filter_speckle=24, color_precision=5,
                  layer_difference=32, corner_threshold=60, length_threshold=4.0, splice_threshold=45, path_precision=2),
  # medium: vtracer defaults-ish
  'medium':  dict(colormode='color', hierarchical='stacked', mode='spline', filter_speckle=6, color_precision=6,
                  layer_difference=16, corner_threshold=60, length_threshold=4.0, splice_threshold=45, path_precision=3),
  # fine: keeps micro-marks
  'fine':    dict(colormode='color', hierarchical='stacked', mode='spline', filter_speckle=2, color_precision=7,
                  layer_difference=8, corner_threshold=45, length_threshold=3.5, splice_threshold=45, path_precision=3),
}
img = cv2.imread(src)
H, W = img.shape[:2]
res = {}
for name, kw in PRESETS.items():
    svg = os.path.join(out, f'{tag}_{name}.svg')
    vtracer.convert_image_to_svg_py(src, svg, **kw)
    txt = open(svg).read()
    npath = len(re.findall(r'<path', txt))
    png = os.path.join(out, f'{tag}_{name}.png')
    subprocess.run(['rsvg-convert', '-w', str(W), '-h', str(H), '-b', 'white', svg, '-o', png], check=True)
    r = cv2.imread(png)
    diff = np.abs(r.astype(float) - img.astype(float))
    mse = (diff ** 2).mean()
    psnr = 10 * np.log10(255 ** 2 / mse)
    res[name] = dict(paths=npath, kb=round(os.path.getsize(svg) / 1024), psnr=round(psnr, 2), mae=round(diff.mean(), 2))
    print(name, res[name], flush=True)
json.dump(res, open(os.path.join(out, f'{tag}_stats.json'), 'w'), indent=1)
