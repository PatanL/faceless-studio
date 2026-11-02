"""Staging / collision checker for explainer storyboards (house style, FEEDBACK A4 + B8, rubric 2.6 / 2.8 / J9).

Runs on the built storyboard JSON (no rendering): it replays the camera (keyframes, preroll, drift, parallax by layer
depth), every layer's keyframes / enter / exit and the caption pages on a 10 fps grid, estimates screen boxes, and
reports what the orca_open_v3 judge caught by eye:

  hero        a prop (car, diver, YOU, seal...) intersects the hero's body (cars falling through the orca)
  caption     a label touches the caption band while a caption page is up (YOU tag on the caption)
  under       a prop / the hero slides under the caption band while a caption is up (platform under "AND ITS FIN ALONE")
  clipped     a number is covered by a prop drawn above it (the "8" clipped by the platform)
  freeze      a near-freeze longer than 0.6 s (camera still, no visual event) ends in an abrupt push (a move > 0.4 s that
              starts at full speed: ease out / linear / backOut ...) - the 2.25-3.0 s hold + 3.1 s push
  colour      the episode never shifts its colour key (no Ocean `shiftTo` and no key change between scenes)
  cover       a label (tag, stat, text bubble) sits on top of the hero or a prop (orca_full_v1 0:45: "YOU NOT TO SCALE"
              over an orca and the diver)
  safe        a label or text bubble leaves the safe area (orca_full_v1 0:50: the "YUCK?" bubble cut off at the right edge)
  dup         an on-screen headline/tag repeats the caption page under it (same words: fail; most of them: [echo] warning) (regress_bwscale: "BIGGER WINS" headline over
              the caption "BIGGER WINS.")

Roles: a layer's `role` (hero | prop | label | dressing | fx) wins; otherwise animals are hero candidates (the largest one
on screen is the hero), people / vehicles / small figures are props, Tag / Headline / Stat / ScaleBar / text layers are
labels, everything else is dressing. `allowOverlap: true` on a layer waives the hero check for it (contact beats).

usage: python3 -m pipeline.episodes.staging episodes/<slug>/storyboard.json [...]   (exit 1 on violations)
"""
from __future__ import annotations

import json
import math
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KIT = os.path.join(ROOT, "studio", "src", "kits", "explainer")
FPS_CHECK = 10           # samples per second
MIN_RUN = 2              # a violation must hold for this many consecutive samples (0.2 s)
FREEZE_S = 0.6
CAPTION_GAP = 16         # px of clear space a label needs around the caption band (8 let "LIVER: GONE" all but touch it)
COVER_SHARE = 0.22       # share of a label's box on the (inset) body of a hero / prop
SAFE = (0.04, 0.045, 0.96, 0.9)   # safe area (x0, y0, x1, y1) as fractions of the frame: Shorts UI + phone crop
HERO_OVERLAP = 0.25      # share of a prop's (inset) box inside the hero's (inset) box
UNDER_PROP = 0.25        # share of a prop's box under the caption band
UNDER_HERO = 0.45        # share of the hero's box under the caption band
CLIP_SHARE = 0.08        # share of a number's box covered by a prop drawn above it

# ------------------------------------------------------------------ figure metadata (parsed from the kit sources)

HOUSE_BOXES = {"orca": ([14, -58, 990, 470], 8.0, "w"),    # house/figures.tsx (selfShaded engine assets)
               "diver": ([-95, 22, 630, 150], 2.6, "w")}
FIXED = {"SpermWhale": "spermWhale", "ColossalSquid": "colossalSquid", "Orca": "orca", "GreatWhite": "greatWhite",
         "BlueWhale": "blueWhale", "Anglerfish": "anglerfish", "Octopus": "octopus", "Crocodile": "crocodile",
         "Hippo": "hippo", "Grizzly": "grizzly", "Diver": "diver", "You": "you", "Bus": "bus", "Car": "car",
         "Elephant": "elephant", "GolfCart": "golfCart", "WhaleHeart": "whaleHeart", "WhaleTongue": "whaleTongue",
         "WhaleThroat": "whaleThroat", "Sauropod": "sauropod", "Jet": "jet", "Krill": "krill", "Seal": "seal",
         "Liver": "liver", "Cookiecutter": "cookiecutter"}
ANIMALS = {"spermWhale", "colossalSquid", "orca", "greatWhite", "blueWhale", "anglerfish", "octopus", "crocodile", "hippo",
           "grizzly", "elephant", "sauropod", "seal", "cookiecutter"}
POSE_CONSTS = {"orcaTop": ("orca", "top"), "orcaHead": ("orca", "head")}
LABELS = {"explainer/Tag", "explainer/Headline", "explainer/Stat", "explainer/ScaleBar", "explainer/Timer",
          "explainer/SpeedBars", "explainer/Options", "explainer/DepthMeter", "explainer/HeightChart"}
NUMBER_LABELS = LABELS | {"text"}
_FIG = None


def figures() -> dict:
    """species (and 'species:pose') -> (box, size_m, axis)"""
    global _FIG
    if _FIG is not None:
        return _FIG
    out = {}
    rx = re.compile(r"const (\w+): (?:Figure|Omit<Figure[^>]*>) = \{(.{0,300}?)box: \[([^\]]+)\],\s*size: ([\d.]+),\s*axis: '(\w)'", re.S)
    for fn in os.listdir(KIT):
        if not fn.endswith(".tsx"):
            continue
        src = open(os.path.join(KIT, fn), encoding="utf-8").read()
        for name, _, box, size, axis in rx.findall(src):
            val = ([float(v) for v in box.split(",")], float(size), axis)
            if name in POSE_CONSTS:
                sp, pose = POSE_CONSTS[name]
                out[f"{sp}:{pose}"] = val
            else:
                out[name] = val
        for m in re.finditer(r"(\w+): \{box: \[([^\]]+)\], size: ([\d.]+), axis: '(\w)'", src):  # inline poses
            if "grizzly" in src[max(0, m.start() - 300):m.start()]:
                out[f"grizzly:{m.group(1)}"] = ([float(v) for v in m.group(2).split(",")], float(m.group(3)), m.group(4))
    out["orca:flat"] = out.get("orca", ([20, 2, 974, 356], 8.0, "w"))
    out["diver:flat"] = out.get("diver", ([-115, 50, 690, 120], 2.6, "w"))
    out.update(HOUSE_BOXES)
    _FIG = out
    return out


def species_of(layer: dict) -> str | None:
    if layer.get("type") != "component":
        return None
    name = layer.get("name", "")
    p = layer.get("props") or {}
    if name == "explainer/Creature":
        sp = str(p.get("species", ""))
        return {"killerwhale": "orca", "shark": "greatWhite", "squid": "colossalSquid"}.get(sp.lower(), sp)
    if name.startswith("explainer/") and name.split("/", 1)[1] in FIXED:
        return p.get("species") or FIXED[name.split("/", 1)[1]]
    return None


# ------------------------------------------------------------------ easing / sampling (core/anim.ts, core/camera.ts)

def _back(t, s=1.7):
    return t * t * ((s + 1) * t - s)


EASES = {
    "linear": lambda t: t,
    "in": lambda t: t ** 3,
    "out": lambda t: 1 - (1 - t) ** 3,
    "inOut": lambda t: 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2,
    "backIn": lambda t: _back(t),
    "backOut": lambda t: 1 - _back(1 - t),
    "elastic": lambda t: 1 - (1 - t) ** 3,
    "bounce": lambda t: 1 - (1 - t) ** 2,
    "step": lambda t: 1.0 if t >= 1 else 0.0,
}
FAST_START = {"out", "linear", "backOut", "elastic", "bounce"}


def ease(name, t):
    return EASES.get(name or "inOut", EASES["inOut"])(max(0.0, min(1.0, t)))


def px(v, ref, fb=0.0):
    if v is None:
        return fb
    if isinstance(v, (int, float)):
        return float(v)
    return float(str(v).rstrip("%")) / 100 * ref


def sample(kfs, prop, t, base, res=lambda v: v):
    prev = None
    for k in kfs:
        if prop not in k or k[prop] is None:
            continue
        if k["t"] <= t:
            prev = k
            continue
        if prev is None:
            return res(k[prop])
        span = k["t"] - prev["t"]
        p = 1 if span <= 0 else (t - prev["t"]) / span
        a, b = res(prev[prop]), res(k[prop])
        return a + (b - a) * ease(k.get("ease"), p)
    return res(prev[prop]) if prev is not None else base


def preset_keys(cam, W, H, dur):
    a = cam.get("amount", 1)
    cx, cy, pan = W / 2, H / 2, min(W, H) * 0.12 * a
    P = cam.get("preset", "none")
    L = "linear"
    table = {
        "pushIn": [(0, cx, cy, 1), (dur, cx, cy, 1 + 0.18 * a)],
        "pullOut": [(0, cx, cy, 1 + 0.18 * a), (dur, cx, cy, 1)],
        "panLeft": [(0, cx + pan, cy, 1.08), (dur, cx - pan, cy, 1.08)],
        "panRight": [(0, cx - pan, cy, 1.08), (dur, cx + pan, cy, 1.08)],
        "panUp": [(0, cx, cy + pan, 1.08), (dur, cx, cy - pan, 1.08)],
        "panDown": [(0, cx, cy - pan, 1.08), (dur, cx, cy + pan, 1.08)],
        "drift": [(0, cx - pan * 0.3, cy + pan * 0.15, 1.04), (dur, cx + pan * 0.3, cy - pan * 0.15, 1.1)],
    }
    return [{"t": t, "x": x, "y": y, "zoom": z, "ease": L} for t, x, y, z in table.get(P, [])]


def camera_at(cam, t, W, H, dur, drift=True):
    if not cam:
        return W / 2, H / 2, 1.0
    kfs = sorted(cam.get("keyframes") or preset_keys(cam, W, H, dur), key=lambda k: k["t"])
    pre = cam.get("preroll") or 0

    def get(prop, d, res):
        if pre > 0 and len(kfs) >= 2:
            k0, k1 = kfs[0], kfs[1]
            if prop in k0 and prop in k1 and k0["t"] <= t < k1["t"] and k1["t"] > k0["t"]:
                span = k1["t"] - k0["t"] + pre
                p0 = ease(k1.get("ease"), pre / span)
                if p0 < 0.999:
                    a, b = res(k0[prop]), res(k1[prop])
                    v0 = (a - p0 * b) / (1 - p0)
                    return v0 + (b - v0) * ease(k1.get("ease"), (t - k0["t"] + pre) / span)
        return sample(kfs, prop, t, d, res)

    x = get("x", W / 2, lambda v: px(v, W))
    y = get("y", H / 2, lambda v: px(v, H))
    z = get("zoom", 1.0, float)
    dr = cam.get("drift")
    if drift and dr:
        z *= 1 + dr.get("zoom", 0) * t
        x += dr.get("x", 0) * t
        y += dr.get("y", 0) * t
    return x, y, z


def to_screen(cam_xyz, d, x, y, W, H):
    cx, cy, zoom = cam_xyz
    pcx = W / 2 + (cx - W / 2) * d
    pcy = H / 2 + (cy - H / 2) * d
    z = max(0.01, 1 + (zoom - 1) * d)
    return (x - pcx) * z + W / 2, (y - pcy) * z + H / 2, z


# ------------------------------------------------------------------ layers -> screen boxes

def role_of(layer: dict) -> str:
    if layer.get("role"):
        return layer["role"]
    sp = species_of(layer)
    if sp:
        base = sp.split(":")[0]
        if (layer.get("props") or {}).get("silhouette"):
            return "dressing"
        if abs(layer.get("depth", 1) - 1) > 0.15:
            return "dressing"
        return "animal" if base in ANIMALS else "prop"
    if layer.get("type") == "text" or layer.get("name") in LABELS:
        return "label"
    if layer.get("type") == "svg" and "<text" in str(layer.get("markup", "")):
        return "label"            # a drawn bubble / card with words in it ("YUCK?") stages like a label
    return "dressing"


def _norm_words(s: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("\n", " ")).split() if w]


def _text_of(layer):
    p = layer.get("props") or {}
    if layer.get("type") == "text":
        return str(layer.get("text", ""))
    for k in ("text", "value", "label"):
        if p.get(k) is not None:
            return str(p.get(k))
    return ""


def visible(layer, t, dur):
    s = layer.get("start")
    e = layer.get("end")
    if s is not None and t < s:
        return 0.0
    if e is not None and t >= e:
        return 0.0
    op = sample(sorted(layer.get("keyframes", []), key=lambda k: k["t"]), "opacity", t, layer.get("opacity", 1))
    en = layer.get("enter")
    if en:
        at = en.get("at", s if s is not None else 0)
        d = en.get("duration", 0.4)
        if t < at:
            return 0.0
        if t < at + d * 0.5:
            op *= 0.5
    ex = layer.get("exit")
    if ex:
        end = e if e is not None else dur
        at = ex.get("at", end - ex.get("duration", 0.4))
        if t >= at + ex.get("duration", 0.4) * 0.5:
            return 0.0
    p = layer.get("props") or {}
    if layer.get("name") in LABELS:   # kit labels time themselves with props.at / props.out
        if isinstance(p.get("at"), (int, float)) and t < p["at"] + 0.15:
            return 0.0
        if isinstance(p.get("out"), (int, float)) and t >= p["out"]:
            return 0.0
    return op


def layer_box(layer, t, W, H):
    """world-space content box (x0, y0, x1, y1) of the visible drawing, before the camera"""
    kfs = sorted(layer.get("keyframes", []), key=lambda k: k["t"])
    x = sample(kfs, "x", t, px(layer.get("x", "50%"), W, W / 2), lambda v: px(v, W))
    y = sample(kfs, "y", t, px(layer.get("y", "50%"), H, H / 2), lambda v: px(v, H))
    sc = sample(kfs, "scale", t, layer.get("scale", 1))
    sx = sample(kfs, "scaleX", t, 1) * sc
    sy = sample(kfs, "scaleY", t, 1) * sc
    full = layer.get("type") == "component"
    w = px(layer.get("width"), W, W if full else 0)
    h = px(layer.get("height"), H, H if full else 0)
    ax, ay = layer.get("anchorX", 0.5), layer.get("anchorY", 0.5)
    bx0, by0 = x - ax * w * sx, y - ay * h * sy           # layer box (scaled about the anchor)
    bw, bh = w * sx, h * sy
    p = layer.get("props") or {}
    sp = species_of(layer)
    if sp:
        key = f"{sp}:{p['pose']}" if p.get("pose") and f"{sp}:{p['pose']}" in figures() else sp
        fig = figures().get(key)
        if fig:
            (fx, fy, fw, fh), size, axis = fig
            if isinstance(p.get("pxPerM"), (int, float)):
                m = size / (fw if axis == "w" else fh)
                dw, dh = fw * m * p["pxPerM"] * sx, fh * m * p["pxPerM"] * sy
            else:
                k = min(bw / fw, bh / fh) if fw and fh else 1
                dw, dh = fw * k, fh * k
            cx = bx0 + bw / 2
            top = by0 + bh - dh if p.get("align") == "bottom" else by0 + (bh - dh) / 2
            return cx - dw / 2, top, cx + dw / 2, top + dh
    if layer.get("name") in LABELS or layer.get("type") == "text":
        txt = _text_of(layer)
        size = p.get("size") or layer.get("fontSize") or 48
        lines = max(1, txt.count("\n") + 1)
        longest = max((len(s) for s in txt.split("\n")), default=1)
        if layer.get("name") == "explainer/Stat":
            tw, th = min(bw, max(longest * 0.62 * size, 0.62 * size * len(str(p.get("label", ""))) * 0.4)), size * 1.9
        elif layer.get("name") == "explainer/Tag" and p.get("look") != "legacy":     # lantern pill (+ dot)
            tw = min(bw or 1e9, longest * 0.68 * size + 1.6 * size)
            th = lines * size * 1.1 + 0.6 * size
        elif layer.get("name") == "explainer/Headline" and p.get("look") != "legacy":  # Anton title plate
            fs = size * 1.12
            sub = str(p.get("sub") or "")
            tw = min(bw or 1e9, max(longest * 0.5 * fs, len(sub) * 0.75 * max(30, fs * 0.36)) + 0.8 * fs)
            th = lines * fs * 1.06 + 0.4 * fs + (max(30, fs * 0.36) * 1.3 if sub else 0)
        elif layer.get("name") in ("explainer/Tag", "explainer/Headline") or layer.get("type") == "text":
            tw = min(bw or 1e9, longest * 0.6 * size + size)
            th = lines * size * 1.2 + (size * 0.7 if p.get("sub") else 0)
        else:
            return bx0, by0, bx0 + bw, by0 + bh
        cx, cy = bx0 + bw / 2, by0 + bh / 2
        return cx - tw / 2, cy - th / 2, cx + tw / 2, cy + th / 2
    return bx0, by0, bx0 + bw, by0 + bh


def screen_box(layer, t, cam_xyz, W, H):
    x0, y0, x1, y1 = layer_box(layer, t, W, H)
    d = layer.get("depth", 1)
    a = to_screen(cam_xyz, d, x0, y0, W, H)
    b = to_screen(cam_xyz, d, x1, y1, W, H)
    return min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])


def inset(b, k):
    w, h = b[2] - b[0], b[3] - b[1]
    return b[0] + w * k, b[1] + h * k, b[2] - w * k, b[3] - h * k


def area(b):
    return max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])


def inter(a, b):
    return area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


def clip(b, W, H):
    return max(0, b[0]), max(0, b[1]), min(W, b[2]), min(H, b[3])


def on_screen(b, W, H):
    return inter(b, (0, 0, W, H)) > 0.05 * max(1.0, area(b))


# ------------------------------------------------------------------ captions

def caption_band(sb, scene, t_local, t_global, W, H, want_page=False):
    cap = sb.get("captions") or {}
    if not cap or cap.get("enabled") is False:
        return None
    words = cap.get("words") or []
    style = cap.get("style") or {}
    linger = cap.get("linger", 0.35)
    act = [w for w in words if w["start"] - 0.05 <= t_global <= w["end"] + linger]
    if not act:
        return None
    i = words.index(act[0])
    if any(w.get("br") for w in words):      # explicit pages: from the last br at/before i to the next br
        a = max(j for j in range(i + 1) if words[j].get("br") or j == 0)
        b = next((j for j in range(i + 1, len(words)) if words[j].get("br")), len(words))
        page = words[a:b]
    else:                                     # pager estimate: up to maxWords / maxChars from this word
        page, n = [], 0
        for w in words[i:i + cap.get("maxWords", 3)]:
            if page and n + len(w["text"]) > cap.get("maxChars", 16) + 4:
                break
            page.append(w)
            n += len(w["text"]) + 1
            if w["text"].rstrip("\"'”’)").endswith((".", "?", "!")):
                break                             # the pager never carries a sentence end onto the next words
    if want_page:
        return page
    chars = sum(len(w["text"]) + 1 for w in page) - 1
    fs = style.get("fontSize") or (104 if sb.get("format", "9:16") == "9:16" else 84)
    maxw = style.get("maxWidth") or 0.82 * W
    tw = chars * (0.7 if style.get("uppercase", True) else 0.58) * fs   # Montserrat 900 caps ~0.7 em per char
    lines = max(1, min(2, math.ceil(tw / maxw)))
    bw = min(maxw, tw)
    y = style.get("y", 0.64)
    if scene.get("captionY") is not None:
        y = scene["captionY"]
    for c in scene.get("captionYAt") or []:
        if t_local >= c["at"]:
            y = c["y"]
    cy = y * H
    hh = lines * fs * 1.08 / 2 + style.get("strokeWidth", 14) / 2
    return W / 2 - bw / 2, cy - hh, W / 2 + bw / 2, cy + hh


# ------------------------------------------------------------------ checks

def _runs(flags):
    """[(i0, i1)] runs of True of length >= MIN_RUN"""
    out, s = [], None
    for i, f in enumerate(flags + [False]):
        if f and s is None:
            s = i
        elif not f and s is not None:
            if i - s >= MIN_RUN:
                out.append((s, i - 1))
            s = None
    return out


def _name(layer, i):
    return f"{layer.get('id') or layer.get('name') or layer.get('type')}#{i}"


def check_scene(sb, scene, t0, W, H) -> list[str]:
    dur = scene["duration"]
    n = max(1, int(dur * FPS_CHECK))
    ts = [min(dur - 1e-3, k / FPS_CHECK) for k in range(n)]
    layers = scene.get("layers", [])
    roles = [role_of(l) for l in layers]
    order = {i: (l.get("z", 0), i) for i, l in enumerate(layers)}
    cams = [camera_at(scene.get("camera"), t, W, H, dur) for t in ts]
    out = []
    flags: dict[tuple, list[bool]] = {}

    def flag(key, k):
        flags.setdefault(key, [False] * n)[k] = True

    for k, t in enumerate(ts):
        vis = {i: visible(l, t, dur) for i, l in enumerate(layers)}
        boxes = {i: screen_box(l, t, cams[k], W, H) for i, l in enumerate(layers) if vis[i] > 0.3 and roles[i] != "dressing"}
        boxes = {i: b for i, b in boxes.items() if on_screen(b, W, H)}
        animals = [i for i in boxes if roles[i] in ("animal", "hero")]
        hero = None
        explicit = [i for i in animals if roles[i] == "hero"]
        if explicit:
            hero = max(explicit, key=lambda i: area(boxes[i]))
        elif animals:
            cand = max(animals, key=lambda i: area(clip(boxes[i], W, H)))
            if area(clip(boxes[cand], W, H)) > 0.06 * W * H:
                hero = cand
        props = [i for i in boxes if roles[i] in ("prop", "animal") and i != hero]
        labels = [i for i in boxes if roles[i] == "label"]
        band = caption_band(sb, scene, t, t0 + t, W, H)
        if hero is not None:
            hb = inset(boxes[hero], 0.14)
            for i in props:
                if layers[i].get("allowOverlap") or abs(layers[i].get("depth", 1) - layers[hero].get("depth", 1)) > 0.15:
                    continue
                pb = inset(boxes[i], 0.1)
                if area(pb) and inter(pb, hb) / area(pb) > HERO_OVERLAP:
                    flag(("hero", i, hero), k)
        if band:
            gb = (band[0] - CAPTION_GAP, band[1] - CAPTION_GAP, band[2] + CAPTION_GAP, band[3] + CAPTION_GAP)
            for i in labels:
                if layers[i].get("name") == "explainer/DepthMeter":
                    continue
                if inter(boxes[i], gb) > 0:
                    flag(("caption", i), k)
            for i in props + ([hero] if hero is not None else []):
                b = inset(boxes[i], 0.1)
                share = inter(b, band) / max(1.0, area(b))
                if share > (UNDER_HERO if i == hero else UNDER_PROP):
                    flag(("under", i), k)
        # labels on top of a subject (a label drawn over a hero / prop it is not attached to)
        subj = props + ([hero] if hero is not None else [])
        for i in labels:
            if layers[i].get("allowOverlap") or layers[i].get("name") in ("explainer/DepthMeter", "explainer/SpeedBars",
                                                                           "explainer/HeightChart", "explainer/ScaleBar"):
                continue
            lb = boxes[i]
            for j in subj:
                sb_ = inset(boxes[j], 0.2 if j == hero else 0.1)
                if area(lb) and inter(lb, sb_) / area(lb) > COVER_SHARE:
                    flag(("cover", i, j), k)
        # safe area: labels and text bubbles stay inside it (headlines may sit high: top margin only)
        sx0, sy0, sx1, sy1 = SAFE[0] * W, SAFE[1] * H, SAFE[2] * W, SAFE[3] * H
        for i in labels:
            b = boxes[i]
            if layers[i].get("name") in ("explainer/DepthMeter", "explainer/HeightChart", "explainer/ScaleBar"):
                continue      # gauges measure the subject and may run past the frame on a punch-in (the number stays centred)
            if layers[i].get("type") == "svg" and (px(layers[i].get("height"), H) >= 0.4 * H or px(layers[i].get("width"), W) >= 0.6 * W):
                continue      # rulers / full cards drawn as svg measure the set like a gauge
            if b[0] < sx0 - 2 or b[2] > sx1 + 2 or b[1] < sy0 - 2 or b[3] > sy1 + 2:
                flag(("safe", i), k)
        # a headline / tag that repeats the caption page under it reads twice (dup)
        page = caption_band(sb, scene, t, t0 + t, W, H, want_page=True) if band else None
        if page:
            cw = _norm_words(" ".join(w["text"] for w in page))
            for i in labels:
                if layers[i].get("name") not in ("explainer/Headline", "explainer/Tag") and layers[i].get("type") != "text":
                    continue
                lw = _norm_words(_text_of(layers[i]))
                if len(lw) >= 2 and len(set(lw) & set(cw)) >= 0.8 * len(set(lw)) and len(set(lw)) >= 0.6 * len(set(cw)):
                    # the same words as the page = a hard fail; a near restatement = a warning (echo)
                    flag(("dup" if set(lw) == set(cw) else "echo", i), k)
        for i in labels:
            if not re.search(r"\d", _text_of(layers[i])):
                continue
            for j in props + ([hero] if hero is not None else []):
                above = order[j] > order[i]   # SceneView stacks by z, then array order (depth is parallax only)
                if above and inter(inset(boxes[j], 0.08), boxes[i]) / max(1.0, area(boxes[i])) > CLIP_SHARE:
                    flag(("clipped", i, j), k)

    for key, fl in flags.items():
        for a, b in _runs(fl):
            ta, tb = t0 + ts[a], t0 + ts[b] + 1 / FPS_CHECK
            kind = key[0]
            L = lambda i: _name(layers[i], i)
            if kind == "hero":
                msg = f"{L(key[1])} intersects the hero {L(key[2])}: block it clear of the body or set allowOverlap"
            elif kind == "caption":
                msg = f"label {L(key[1])} touches the caption band: move it or set scene captionY/captionYAt"
            elif kind == "under":
                msg = f"{L(key[1])} slides under the caption band: keep props above it while captions are up"
            elif kind == "cover":
                msg = f"label {L(key[1])} sits on top of {L(key[2])}: move it clear of the subject (or tie it with a leader)"
            elif kind == "safe":
                msg = f"label {L(key[1])} leaves the safe area: keep labels and bubbles inside the frame margins"
            elif kind == "dup":
                msg = f"label {L(key[1])} repeats the caption under it: drop it or say something the caption doesn't"
            elif kind == "echo":
                msg = f"label {L(key[1])} echoes most of the caption under it (warning): prefer a number or a new fact"
            else:
                msg = f"number in {L(key[1])} is clipped by {L(key[2])} drawn above it"
            out.append(f"{scene['id']} {ta:.1f}-{tb:.1f}s [{kind}] {msg}")
    out += check_freeze(scene, t0, W, H)
    return out


def check_freeze(scene, t0, W, H) -> list[str]:
    """near-freeze > FREEZE_S (camera still, no visual event) that ends in a fast-start camera move longer than 0.4 s"""
    from .common import visual_events
    cam = scene.get("camera")
    if not cam or not cam.get("keyframes"):
        return []
    dur = scene["duration"]
    # picture events from the layers (camera keys that change nothing are not events; the camera speed is measured below)
    ev = [e for e in visual_events({**scene, "camera": {"keyframes": [], "shake": (scene.get("camera") or {}).get("shake", [])}}) if 0 < e < dur]
    kfs = sorted(cam["keyframes"], key=lambda k: k["t"])
    out = []
    for a, b in zip(kfs, kfs[1:]):
        d = b["t"] - a["t"]
        if d <= 0.4 or b.get("ease", "inOut") not in FAST_START:
            continue
        mag = abs((b.get("zoom") or 1) - (a.get("zoom") or 1)) * W / 2 + abs(px(b.get("x"), W, 0) - px(a.get("x"), W, 0)) + abs(px(b.get("y"), H, 0) - px(a.get("y"), H, 0))
        if "zoom" not in a or "zoom" not in b:
            mag = abs(px(b.get("x"), W, 0) - px(a.get("x"), W, 0)) + abs(px(b.get("y"), H, 0) - px(a.get("y"), H, 0))
        if mag < 40:
            continue
        start = a["t"]
        # how long was the camera still before this move?
        s = start
        step = 1 / 30
        prev = camera_at(cam, s, W, H, dur, drift=False)
        while s - step >= 0:
            cur = camera_at(cam, s - step, W, H, dur, drift=False)
            v = math.hypot(cur[0] - prev[0], cur[1] - prev[1]) + abs(cur[2] - prev[2]) * W / 2
            if v > 0.5:
                break
            prev, s = cur, s - step
        still = start - s
        if s <= step:                         # held since the scene start: the cut itself is the event
            still = min(still, start)
        quiet = [e for e in ev if s + 0.05 < e < start - 0.05]
        if still > FREEZE_S and not quiet:
            out.append(f"{scene['id']} {t0 + s:.1f}-{t0 + start:.1f}s [freeze] {still:.1f}s near-freeze, then an abrupt "
                       f"{b.get('ease', 'inOut')} push ({d:.1f}s): keep the camera drifting through the hold or ease the push in")
    return out


def check_colour(sb) -> list[str]:
    """house rule: an episode on the Ocean background shifts its colour key at least once (scale/turn beat)"""
    oceans = [((s.get("background") or {}).get("props") or {}) for s in sb["scenes"]
              if (s.get("background") or {}).get("name") == "explainer/Ocean"]
    if not oceans or any(p.get("look") == "legacy" for p in oceans):
        return []
    if any(p.get("shiftTo") for p in oceans):
        return []
    return ["[colour] no colour shift: the scale/turn beat needs an Ocean `shiftTo` (STYLE_BIBLE §2.5; house.py adds one "
            "when a builder marks the beat with scene _house.shift)"]


WARN_KINDS = ("[echo]",)


def is_warning(msg: str) -> bool:
    return any(k in msg for k in WARN_KINDS)


def check(sb: dict) -> list[str]:
    W, H = (1080, 1920) if sb.get("format", "9:16") == "9:16" else (1920, 1080)
    out, t0 = [], 0.0
    for s in sb["scenes"]:
        out += check_scene(sb, s, t0, W, H)
        t0 += s["duration"]
    return out + check_colour(sb)


def main(argv):
    bad = 0
    for p in argv or []:
        sb = json.load(open(p))
        v = check(sb)
        print(f"{p}: {len(v)} staging violation(s)")
        for m in v:
            print("  " + m)
        bad += bool(v)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    sys.exit(main(sys.argv[1:]))
