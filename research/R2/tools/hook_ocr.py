"""Caption-band OCR of first N and last M seconds of a 9:16 video (frames pre-extracted at 1 fps, 540 wide).
python -I hook_ocr.py <frames_dir> <out.json> [y0 y1]
Auto-detects the caption band if y0/y1 not given by OCRing the full frame and keeping Latin text lines."""
import json, sys, re
from pathlib import Path
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

d, out = Path(sys.argv[1]), Path(sys.argv[2])
ocr = RapidOCR(intra_op_num_threads=3, inter_op_num_threads=1)
rows = []
for f in sorted(d.glob("*.jpg")):
    im = Image.open(f).convert("RGB")
    res, _ = ocr(np.array(im))
    lines = []
    for box, txt, conf in (res or []):
        if conf < 0.6: continue
        latin = sum(c.isascii() and c.isalpha() for c in txt)
        if latin >= max(3, 0.6 * len(txt.replace(" ", ""))):
            y = int(sum(p[1] for p in box) / 4)
            lines.append((y, txt))
    lines.sort()
    rows.append({"frame": f.name, "lines": [f"{y}:{t}" for y, t in lines]})
out.write_text(json.dumps(rows, ensure_ascii=False, indent=0))
