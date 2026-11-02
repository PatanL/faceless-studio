#!/usr/bin/env python3
"""Old-vs-new sheet matched by NARRATION BEAT (not by timestamp: the house voice re-times the episode).

usage: python3 scripts/old_vs_new_sheet.py out.jpg --beats 12 \
         "old pilot|old.mp4|old_captions.json" "house v1|v1.mp4|old_captions.json" "house v2|v2.mp4|new_captions.json" \
         ["v3 target|v3.mp4|old_captions.json|9.7"]
Each column is label|video|captions.json[|max_seconds]. Beats are evenly spaced words of the narration (the same word
index in every captions file, which must hold the same script); each frame is taken 0.45 s after that word starts.
A column with max_seconds shows an empty cell past its end. Frames are pulled with ffmpeg (a few stills, Mac-safe).
"""
import json
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

CELL_W, CELL_H, PAD, HEAD = 300, 533, 8, 64
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def frame(video, t, path):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1",
                    "-vf", f"scale={CELL_W}:{CELL_H}", path], check=True)
    return Image.open(path).convert("RGB")


def main(argv):
    out = argv[0]
    beats = 12
    if "--beats" in argv:
        i = argv.index("--beats")
        beats = int(argv[i + 1])
        del argv[i:i + 2]
    cols = [c.split("|") for c in argv[1:]]
    words = [json.load(open(c[2]))["words"] for c in cols]
    n = min(len(w) for w in words)
    idx = [round(k * (n - 1) / (beats - 1)) for k in range(beats)]
    idx[0] = 0
    per_row = 2                      # beats side by side per sheet row
    rows = (beats + per_row - 1) // per_row
    block_w = len(cols) * (CELL_W + PAD) + PAD
    W, H = per_row * block_w + PAD, rows * (CELL_H + HEAD + PAD) + 70
    sheet = Image.new("RGB", (W, H), (12, 18, 24))
    d = ImageDraw.Draw(sheet)
    f_big, f_small = ImageFont.truetype(FONT, 30), ImageFont.truetype(FONT, 19)
    d.text((PAD, 18), "explainer-orca: " + "  |  ".join(c[0] for c in cols) + "   (matched by narration word)", fill=(232, 225, 207), font=f_big)
    with tempfile.TemporaryDirectory() as tmp:
        for b, wi in enumerate(idx):
            r, cpos = divmod(b, per_row)
            x0, y0 = PAD + cpos * block_w, 70 + r * (CELL_H + HEAD + PAD)
            word = words[0][wi]["text"]
            for ci, c in enumerate(cols):
                t = words[ci][wi]["start"] + (0.45 if wi else 0.0)
                x = x0 + ci * (CELL_W + PAD)
                lim = float(c[3]) if len(c) > 3 else None
                d.text((x, y0 + 4), f"{c[0]}", fill=(111, 214, 232), font=f_small)
                d.text((x, y0 + 30), f"{t:5.1f}s  “{word}”", fill=(232, 225, 207), font=f_small)
                if lim is not None and t > lim:
                    d.rectangle([x, y0 + HEAD, x + CELL_W, y0 + HEAD + CELL_H], outline=(60, 70, 80), width=2)
                    continue
                im = frame(c[1], t, os.path.join(tmp, f"{b}_{ci}.jpg"))
                sheet.paste(im, (x, y0 + HEAD))
    sheet.save(out, quality=88)
    print(f"{out}: {beats} beats x {len(cols)} columns, {W}x{H}")


if __name__ == "__main__":
    main(sys.argv[1:])
