"""OCR burned-in captions (and in-panel phone text) from sampled frames.

Run on the Spark (CPU only):
  CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=8 python -I ocr_frames.py <frames_dir> <fps> <out.json> [--flip-panel] [--shard=k/n]

Frames are 540x960 (9:16). Caption band is y=180..280; picture panel y=275..685.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageOps
import numpy as np
from rapidocr_onnxruntime import RapidOCR


def main():
    frames_dir, fps, out = Path(sys.argv[1]), float(sys.argv[2]), Path(sys.argv[3])
    flip = "--flip-panel" in sys.argv
    shard = [a for a in sys.argv if a.startswith("--shard=")]
    k, n = (map(int, shard[0][8:].split("/")) if shard else (0, 1))
    panel_every = 2  # OCR the picture panel every Nth frame (1 s at 2 fps)
    ocr = RapidOCR(intra_op_num_threads=2, inter_op_num_threads=1)
    rows = []
    for i, f in enumerate(sorted(frames_dir.glob("f_*.jpg"))):
        if i % n != k:
            continue
        t = i / fps
        im = Image.open(f).convert("RGB")
        cap = im.crop((0, 170, 540, 285)).resize((1080, 230))
        res, _ = ocr(np.array(cap))
        cap_txt = " ".join(r[1] for r in (res or []) if r[2] > 0.5)
        panel_txt = ""
        if i % panel_every == 0:
            pan = im.crop((0, 275, 540, 690))
            if flip:
                pan = ImageOps.mirror(pan)
            pan = pan.resize((1080, 830))
            res2, _ = ocr(np.array(pan))
            panel_txt = " | ".join(r[1] for r in (res2 or []) if r[2] > 0.6)
        rows.append({"t": round(t, 1), "caption": cap_txt, "panel": panel_txt})
        if i % 50 == 0:
            print(i, t, cap_txt, flush=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=0))


if __name__ == "__main__":
    main()
