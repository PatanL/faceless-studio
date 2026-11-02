"""Contact sheets from grab_frames.py output.

usage:
  sheets.py grid  <frames_dir> <events.json> <out_prefix> [--t0 S --t1 S] [--cols 10 --rows 8 --tw 160]
      every-0.5 s grid; a red bar = a hard cut happened since the previous tile, yellow = transition,
      cyan = composition event. One JPG per cols*rows tiles, <= 1600 px wide.
  sheets.py pairs <frames_dir> <events.json> <out.jpg> <spec>
      frame-pair sheet. spec = comma list of  t_before/t_after[:label]  (seconds), or "cuts" for every cut.
      4 pairs per row, each tile 196 px wide.
  sheets.py stills <frames_dir> <events.json> <out.jpg> <spec> [--cols 4]
      labelled stills, spec = comma list of  t[:label].
"""
import sys, json, os, glob, argparse
from PIL import Image, ImageDraw, ImageFont

def font(sz):
    try: return ImageFont.load_default(size=sz)
    except TypeError: return ImageFont.load_default()

def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"

class Frames:
    def __init__(self, d, ev):
        self.fps = ev["fps"]; self.st = ev.get("start", 0.0)
        self.idx = sorted(int(os.path.basename(p)[2:8]) for p in glob.glob(f"{d}/f_*.jpg")); self.d = d
    def near(self, t):
        i = int(round((t - self.st) * self.fps))
        j = min(self.idx, key=lambda k: abs(k - i))
        return Image.open(f"{self.d}/f_{j:06d}.jpg").convert("RGB"), j / self.fps + self.st

def tile(img, tw, label, bar=None):
    th = round(tw * 9 / 16)
    im = img.resize((tw, th), Image.LANCZOS)
    out = Image.new("RGB", (tw, th + 14), (18, 18, 18)); out.paste(im, (0, 0))
    dr = ImageDraw.Draw(out); dr.text((3, th + 1), label, fill=(235, 235, 235), font=font(11))
    if bar:
        dr.rectangle([0, 0, 4, th], fill=bar)
    return out

def grid(a):
    ev = json.load(open(a.events)); F = Frames(a.frames, ev)
    t0 = a.t0; t1 = a.t1 or ev["duration"] + ev.get("start", 0)
    ts = []; t = t0
    while t < t1 - 1e-6: ts.append(round(t, 3)); t += a.step
    cuts = ev["cuts"]; trs = [x["end"] for x in ev["transitions"]]; comps = [x["t"] for x in ev["comp_events"]]
    per = a.cols * a.rows; k = 0
    for s in range(0, len(ts), per):
        chunk = ts[s:s + per]; tiles = []
        for t in chunk:
            img, _ = F.near(t)
            lo = t - a.step
            bar = (230, 40, 40) if any(lo < c <= t for c in cuts) else \
                  (240, 200, 30) if any(lo < c <= t for c in trs) else \
                  (40, 210, 230) if any(lo < c <= t for c in comps) else None
            tiles.append(tile(img, a.tw, mmss(t), bar))
        tw, th = tiles[0].size
        sheet = Image.new("RGB", (a.cols * (tw + 2), ((len(tiles) - 1) // a.cols + 1) * (th + 2)), (0, 0, 0))
        for n, im in enumerate(tiles):
            sheet.paste(im, ((n % a.cols) * (tw + 2), (n // a.cols) * (th + 2)))
        p = f"{a.out}_{k:02d}_{mmss(chunk[0]).replace(':', 'm')}.jpg"; sheet.save(p, quality=80); k += 1
        print(p)

def parse_spec(spec, ev):
    if spec == "cuts":
        dt = 1.0 / ev["fps"]
        return [(c - dt, c, f"cut {mmss(c)}") for c in ev["cuts"]]
    out = []
    for item in spec.split(","):
        lab = ""
        if ":" in item: item, lab = item.split(":", 1)
        if "/" in item:
            b, c = item.split("/"); out.append((float(b), float(c), lab))
        else:
            out.append((float(item), None, lab))
    return out

def pairs(a):
    ev = json.load(open(a.events)); F = Frames(a.frames, ev); P = parse_spec(a.spec, ev)
    tw = 196; rows = []
    for b, c, lab in P:
        ib, tb = F.near(b); ic, tc = F.near(c)
        t1 = tile(ib, tw, f"{mmss(tb)} {lab}"[:30]); t2 = tile(ic, tw, f"-> {mmss(tc)}")
        pr = Image.new("RGB", (2 * tw + 2, t1.size[1]), (0, 0, 0)); pr.paste(t1, (0, 0)); pr.paste(t2, (tw + 2, 0))
        rows.append(pr)
    cols = 4; pw, ph = rows[0].size
    sheet = Image.new("RGB", (cols * (pw + 6), ((len(rows) - 1) // cols + 1) * (ph + 4)), (60, 60, 60))
    for n, im in enumerate(rows): sheet.paste(im, ((n % cols) * (pw + 6), (n // cols) * (ph + 4)))
    sheet.save(a.out, quality=82); print(a.out, len(rows))

def stills(a):
    ev = json.load(open(a.events)); F = Frames(a.frames, ev); P = parse_spec(a.spec, ev)
    tw = 1600 // a.cols - 4; tiles = []
    for t, _, lab in P:
        im, tt = F.near(t); tiles.append(tile(im, tw, f"{mmss(tt)} {lab}"))
    w, h = tiles[0].size
    sheet = Image.new("RGB", (a.cols * (w + 4), ((len(tiles) - 1) // a.cols + 1) * (h + 4)), (0, 0, 0))
    for n, im in enumerate(tiles): sheet.paste(im, ((n % a.cols) * (w + 4), (n // a.cols) * (h + 4)))
    sheet.save(a.out, quality=84); print(a.out, len(tiles))

ap = argparse.ArgumentParser()
ap.add_argument("mode"); ap.add_argument("frames"); ap.add_argument("events"); ap.add_argument("out")
ap.add_argument("spec", nargs="?", default="")
ap.add_argument("--t0", type=float, default=0.0); ap.add_argument("--t1", type=float, default=0.0)
ap.add_argument("--step", type=float, default=0.5)
ap.add_argument("--cols", type=int, default=10); ap.add_argument("--rows", type=int, default=8)
ap.add_argument("--tw", type=int, default=158)
a = ap.parse_args()
{"grid": grid, "pairs": pairs, "stills": stills}[a.mode](a)
