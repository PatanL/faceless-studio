#!/usr/bin/env python3
"""Make a 16:9 cut of a 9:16 episode storyboard (same audio, captions and timing).

usage: python3 -m pipeline.episodes.reformat <slug> [--k 0.78]   (use a smaller k, e.g. 0.74, when
  stat boxes sit low in the 9:16 picture zone: text is pushed above the captions, and a smaller k needs less push)
  -> episodes/<slug>/storyboard_16x9.json, render with
     PROPS=episodes/<slug>/storyboard_16x9.json scripts/spark_render.sh Storyboard <slug>_16x9.mp4

The 9:16 builders lay out a picture zone at y ~10-66 % of 1080x1920 with captions at y 0.72.
This maps that zone uniformly (factor k, no distortion, so true-scale comparisons such as
pxPerM rows and scale bars stay aligned) into the upper ~80 % of a 1920x1080 frame, centred,
and moves captions to a bottom band. Full-frame backgrounds simply fill the wider frame;
off-screen keyframe positions (e.g. x "162%") map the same way, so entrances still start
outside the 9:16 column (and mostly outside the 16:9 frame; wide figures keep their crop).
"""
from __future__ import annotations

import argparse
import copy
import json
import os

from .common import ROOT

SW, SH = 1080, 1920          # source 9:16
DW, DH = 1920, 1080          # target 16:9
ZONE_TOP_SRC = 0.10 * SH     # top of the 9:16 picture zone (px)
ZONE_TOP_DST = 0.045 * DH    # where it lands in 16:9 (px)
SCALE_PROPS = ("size", "labelSize", "pxPerM")
# On-screen text reads smaller in a landscape frame: text components get a gentler scale
# (box and font), everything else keeps k so scale comparisons stay exact.
TEXT_COMPONENTS = ("explainer/Headline", "explainer/Tag", "explainer/Stat")
TEXT_BOOST = 1.25
CAPTION_Y = 0.86             # 16:9 caption centre (fraction of DH); core/captions clamps lower values to the safe band anyway
CAPTION_SCALE = 0.8          # 16:9 caption font vs 9:16
TEXT_VISIBLE = 0.32          # visible half-height of a text component as a fraction of its box height


class Map:
    def __init__(self, k: float, text_k: float | None = None):
        self.k = k
        self.ox = (DW - SW * k) / 2
        self.sk = text_k or k  # size factor (positions always use k)

    def x(self, v):
        px = SW * float(v[:-1]) / 100 if isinstance(v, str) else float(v)
        return f"{(px * self.k + self.ox) / DW * 100:.2f}%"

    def y(self, v):
        px = SH * float(v[:-1]) / 100 if isinstance(v, str) else float(v)
        return f"{((px - ZONE_TOP_SRC) * self.k + ZONE_TOP_DST) / DH * 100:.2f}%"

    def s(self, v):
        if isinstance(v, list):
            return [self.s(a) for a in v]
        return round(v * self.sk, 2) if isinstance(v, (int, float)) and not isinstance(v, bool) else v


def _pos(d: dict, m: Map, w_key="width", h_key="height"):
    if "x" in d:
        d["x"] = m.x(d["x"])
    if "y" in d:
        d["y"] = m.y(d["y"])
    for k in (w_key, h_key):
        if isinstance(d.get(k), (int, float)):
            d[k] = m.s(d[k])


def _full_frame(layer: dict) -> bool:
    """A layer that covers the whole 9:16 frame (e.g. a full-bleed Map) fills the whole 16:9 frame instead."""
    w, h = layer.get("width"), layer.get("height")
    return (isinstance(w, (int, float)) and isinstance(h, (int, float)) and w >= SW and h >= SH * 0.95
            and layer.get("x", "50%") == "50%" and layer.get("y", "50%") == "50%" and not layer.get("keyframes"))


def _clear_captions(l: dict, cap_font: float):
    """Keep a text component's visible box above the 16:9 caption line."""
    if not (isinstance(l.get("y"), str) and isinstance(l.get("height"), (int, float))):
        return
    cy = float(l["y"][:-1]) / 100 * DH
    limit = CAPTION_Y * DH - cap_font * 0.75 - 10
    over = cy + l["height"] * TEXT_VISIBLE - limit
    if over > 0:
        l["y"] = f"{(cy - over) / DH * 100:.2f}%"


def layer16(layer: dict, m: Map, cap_font: float = 67) -> dict:
    if _full_frame(layer):
        l = copy.deepcopy(layer)
        l["width"], l["height"] = DW, DH
        return l
    if layer.get("name") in TEXT_COMPONENTS:
        m = Map(m.k, text_k=min(1.0, m.k * TEXT_BOOST))
    l = copy.deepcopy(layer)
    l.setdefault("x", "50%")
    l.setdefault("y", "50%")
    _pos(l, m)
    for kf in l.get("keyframes", []):
        _pos(kf, m)
    if l.get("type") == "particles" and "size" in l:
        l["size"] = m.s(l["size"])
    for k in ("enter", "exit"):
        if isinstance(l.get(k), dict) and "distance" in l[k]:
            l[k]["distance"] = m.s(l[k]["distance"])
    for idl in l.get("idle", []):
        if "amount" in idl and idl.get("type") in ("bob", "float", "drift", "sway"):
            idl["amount"] = m.s(idl["amount"])
    props = l.get("props")
    if isinstance(props, dict):
        for k in SCALE_PROPS:
            if k in props:
                props[k] = m.s(props[k])
    if layer.get("name") in TEXT_COMPONENTS:
        _clear_captions(l, cap_font)
    return l


def camera16(cam: dict, m: Map) -> dict:
    c = copy.deepcopy(cam)
    for kf in c.get("keyframes", []):
        if "x" in kf:
            kf["x"] = m.x(kf["x"])
        if "y" in kf:
            kf["y"] = m.y(kf["y"])
    for sh in c.get("shake", []):
        if "amplitude" in sh:
            sh["amplitude"] = m.s(sh["amplitude"])
    return c


def reformat(sb: dict, k: float = 0.78) -> dict:
    m = Map(k)
    out = copy.deepcopy(sb)
    out["format"] = "16:9"
    out["id"] = f"{sb['id']}-16x9"
    cap_font = round((sb.get("captions") or {}).get("style", {}).get("fontSize", 84) * CAPTION_SCALE)
    for sc in out["scenes"]:
        sc["layers"] = [layer16(l, m, cap_font) for l in sc["layers"]]
        if "camera" in sc:
            sc["camera"] = camera16(sc["camera"], m)
    cap = out.get("captions")
    if cap:
        st = cap.setdefault("style", {})
        st["fontSize"] = cap_font
        st["y"] = CAPTION_Y
        cap["maxChars"] = max(cap.get("maxChars", 16), 22)
        cap["maxWords"] = max(cap.get("maxWords", 3), 4)
    out["_built"] = {**sb.get("_built", {}), "reformat": f"pipeline/episodes/reformat.py k={k} from 9:16"}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--k", type=float, default=0.78)
    a = ap.parse_args()
    ep = os.path.join(ROOT, "episodes", a.slug)
    sb = json.load(open(os.path.join(ep, "storyboard.json")))
    out = os.path.join(ep, "storyboard_16x9.json")
    with open(out, "w") as f:
        json.dump(reformat(sb, a.k), f, indent=1, ensure_ascii=False)
    print(f"{a.slug}: 16:9 cut (k={a.k}) -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
