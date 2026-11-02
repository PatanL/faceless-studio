"""House style ("Lantern & Ink") storyboard pass for explainer episodes: the live default look.

build.py runs `apply()` on every explainer storyboard (opt out per module with HOUSE_STYLE = False or per slug with
HOUSE_SKIP), then pipeline/episodes/staging.py checks the result. Everything here is plain storyboard data that the
explainer kit renders (studio/src/kits/explainer/house/), so a builder can also write any of it by hand.

Per scene
  light     scene.light = Lantern setup (one key from the upper left for every shaded figure), a slow key sweep on
            longer scenes (light as an actor, STYLE_BIBLE §9.5). Figures are shaded by the kit by default.
  palette   Ocean backgrounds get a key ramp (bible §2.5): consecutive scenes never share a key, and the colour SHIFT
            lands on the beat a builder marks with scene["_house"]["shift"] = {"at": s, "to": "warm"} (the scale/turn
            beat). With no mark, the first scale beat (a You / ScaleBar / HeightChart / Stat layer) gets it.
  dressing  environment scenes (Ocean background) get a seeded, hazed far school and warm jellies in the upper frame
            band when that band is empty (bible §8 detail density; dressing never counts as a staging collision).
  depth     ONLY for hero wide shots (scene["_house"]["wide"] = True): far ridge + far kelp (depth 0.3), mid reef (warm
            saturated mass, depth 0.6), a cropped ink foreground kelp (depth 1.45, blur 9). polish-2d measured +2.0 s per
            10 s for depth planes with a small visible gain at phone size, so it is opt-in.
  motion    camera pre-roll on the first scene, backOut punch-ins (out-eased zoom-ins <= 0.3 s), never-still drift +
            low hand-held drift (not on the last scene: its last frame is the loop bookend), drop -> dropSquash with a
            landing kick, figure pop -> popSpring (uniform, never thinner than 60 % of rest width), label lag (tags and
            tethers riding a floating figure follow it 0.16 s / 0.07 s late), idle body sway on swimming heroes.
  grade     brightness 1.02, contrast 1.05, saturate 1.12 (free, constant per scene).
Storyboard: overlays.grain = 0 (texture is baked into art; live grain is invisible after x264 and costs ~20 %).
Keys starting with "_house" are removed before the storyboard is written.
"""
from __future__ import annotations

import copy
import math

W, H = 1080, 1920
FIGURES = {"explainer/Orca", "explainer/Diver", "explainer/You", "explainer/Car", "explainer/Bus", "explainer/Seal",
           "explainer/GreatWhite", "explainer/SpermWhale", "explainer/BlueWhale", "explainer/Anglerfish",
           "explainer/Octopus", "explainer/ColossalSquid", "explainer/Crocodile", "explainer/Hippo", "explainer/Grizzly",
           "explainer/Elephant", "explainer/GolfCart", "explainer/Creature", "explainer/Cookiecutter", "explainer/Krill",
           "explainer/Sauropod", "explainer/Jet"}
SWIMMERS = {"explainer/Orca", "explainer/GreatWhite", "explainer/SpermWhale", "explainer/BlueWhale", "explainer/Cookiecutter"}
SCALE_BEAT = {"explainer/You", "explainer/ScaleBar", "explainer/HeightChart", "explainer/Stat"}
# key ramp variants so consecutive scenes never share a key (kit house/oceanBg.tsx KEYS)
VARIANT = {"tide": "sky", "sky": "tide", "mid": "kelp", "kelp": "mid", "deep": "dusk", "dusk": "deep", "warm": "tide"}
# automatic shift target per key: sunlit water lifts warm for the proof beat; the deep sea never turns sunlit, it shifts
# between ink and dusk (a temperature change without inventing daylight at 1,500 m)
AUTO_SHIFT = {"tide": "warm", "sky": "warm", "mid": "tide", "kelp": "tide", "deep": "dusk", "ink": "dusk", "dusk": "deep",
              "warm": "tide"}
GRADE = {"brightness": 1.02, "contrast": 1.05, "saturate": 1.12}
LIGHT = {"setup": "lantern"}


def auto_key(depth) -> str:
    d = depth if isinstance(depth, (int, float)) else (depth[0].get("v", 40) if isinstance(depth, list) and depth else 40)
    return "tide" if d < 30 else "mid" if d < 200 else "deep"


def lag_phase(speed: float, lag_s: float) -> float:
    """phase (rad) that makes an idle follow its parent lag_s seconds late"""
    return -2 * math.pi * speed * lag_s


def _first_at(layer: dict) -> float:
    for k in ("start",):
        if isinstance(layer.get(k), (int, float)):
            return layer[k]
    en = layer.get("enter") or {}
    if isinstance(en.get("at"), (int, float)):
        return en["at"]
    p = layer.get("props") or {}
    return p["at"] if isinstance(p.get("at"), (int, float)) else 0.0


def _upper_band_empty(scene: dict) -> bool:
    """no picture-carrying layer (figures, labels) sits mostly in the top 12-40 % of the frame"""
    from .staging import layer_box, role_of
    for l in scene.get("layers", []):
        if role_of(l) == "dressing" or l.get("depth", 1) == 0 and l.get("name") == "explainer/Headline":
            continue
        try:
            x0, y0, x1, y1 = layer_box(l, min(scene["duration"] * 0.5, 1.0), W, H)
        except Exception:  # noqa: BLE001 - a layer the estimator can't read never blocks the dressing
            continue
        if y1 > 0.12 * H and y0 < 0.4 * H and (x1 - x0) * (y1 - y0) < 0.6 * W * H:
            if (min(y1, 0.4 * H) - max(y0, 0.12 * H)) > 0.5 * (y1 - y0):
                return False
    return True


def dressing(scene: dict, si: int) -> list[dict]:
    """far school + warm jellies for the upper frame (bible §8), all role dressing"""
    return [
        {"type": "component", "name": "explainer/FishSchool", "role": "dressing", "x": "50%", "y": "27%", "width": 1300,
         "height": 260, "depth": 0.35, "z": -6, "props": {"n": 18, "seed": f"s{si}", "scale": 0.5, "plane": "far",
                                                           "dir": -1 if si % 2 else 1}},
        {"type": "component", "name": "explainer/Jellies", "role": "dressing", "x": "50%", "y": "30%", "width": 1200,
         "height": 520, "depth": 0.6, "z": -5, "opacity": 0.85,
         "props": {"n": 2, "seed": f"j{si}", "size": [26, 46], "plane": "mid", "colors": ["amber-3", "coral-3", "tide-3"]}},
    ]


def wide_planes(scene: dict, si: int) -> list[dict]:
    """opt-in depth planes for a hero wide shot (bible §6)"""
    return [
        {"type": "component", "name": "explainer/Ridge", "role": "dressing", "x": "50%", "y": "72%", "width": 1500, "height": 900,
         "depth": 0.3, "z": -9, "props": {"seed": f"rd{si}", "plane": "far", "y": 0.8}},
        {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "50%", "y": "70%", "width": 1500, "height": 1000,
         "depth": 0.3, "z": -8, "props": {"seed": f"fk{si}", "n": 4, "plane": "far", "blade": 0.6}},
        {"type": "component", "name": "explainer/Reef", "role": "dressing", "x": "50%", "y": "88%", "width": 1400, "height": 560,
         "depth": 0.6, "z": -7, "props": {"seed": f"rf{si}", "plane": "mid", "shelf": 0.35}},
        {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "-1%", "y": "78%", "width": 420, "height": 1500,
         "depth": 1.45, "z": 30, "blur": 9, "props": {"seed": f"ek{si}", "n": 2, "plane": "fore", "height": [0.75, 1.0], "blade": 1.5}},
        {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "102%", "y": "80%", "width": 380, "height": 1400,
         "depth": 1.45, "z": 30, "blur": 9, "props": {"seed": f"ek{si}b", "n": 1, "plane": "fore", "height": [0.7, 0.9], "blade": 1.6}},
    ]


def _motion(sc: dict, si: int, last: bool) -> None:
    dur = sc["duration"]
    cam = sc.get("camera")
    kicks = []
    for l in sc.get("layers", []):
        if l.get("type") != "component" or l.get("name") not in FIGURES:
            continue
        en = l.get("enter") or {}
        if en.get("type") == "drop":
            en["type"] = "dropSquash"
            en["duration"] = max(en.get("duration", 0.4), 0.5)
            en["distance"] = max(en.get("distance", 160), 90)
            kicks.append({"at": round(en.get("at", l.get("start", 0)) + min(0.22, en["duration"] * 0.4), 3), "duration": 0.3,
                          "amplitude": 3.5, "frequency": 11, "rotate": 0.12, "decay": True})
        elif en.get("type") == "pop":
            en["type"] = "popSpring"
            en["duration"] = max(en.get("duration", 0.35), 0.5)
        if l.get("name") in SWIMMERS and not l.get("idle") and not (l.get("props") or {}).get("silhouette"):
            l["idle"] = [{"type": "sway", "amount": 0.7, "speed": 0.22, "phase": 0.8 + si}]
    # label lag: tags / tethers that ride a floating figure (same x, float idle) follow it late
    for f in sc.get("layers", []):
        fl = next((i for i in f.get("idle", []) if i.get("type") == "float"), None)
        if not fl or f.get("name") not in FIGURES:
            continue
        for l in sc["layers"]:
            if l is f or l.get("x") != f.get("x"):
                continue
            lag = 0.16 if l.get("name") == "explainer/Tag" else 0.07 if l.get("type") == "svg" else None
            if lag and any(i.get("type") == "float" for i in l.get("idle", [])) or (lag and not l.get("idle")):
                l["idle"] = [{**fl, "phase": round(fl.get("phase", 0) + lag_phase(fl.get("speed", 0.5), lag), 4)}]
    if cam is None:
        cam = sc["camera"] = {"keyframes": []}
    kfs = cam.get("keyframes") or []
    if si == 0 and len(kfs) > 1 and kfs[0]["t"] == 0:
        cam["preroll"] = 0.3
    for a, b in zip(kfs, kfs[1:]):
        if b.get("ease") == "out" and isinstance(a.get("zoom"), (int, float)) and isinstance(b.get("zoom"), (int, float)) \
                and b["zoom"] - a["zoom"] > 0.08 and b["t"] - a["t"] <= 0.3:
            b["ease"] = "backOut"
    if not last:
        cam.setdefault("drift", {"zoom": 0.006, "x": 5 if si % 2 == 0 else -5, "y": 0})
        cam["shake"] = list(cam.get("shake", [])) + [{"at": 0, "duration": dur, "amplitude": 3, "frequency": 0.22,
                                                       "rotate": 0, "decay": False}]
    if kicks:
        cam["shake"] = list(cam.get("shake", [])) + kicks


def _colour(sb: dict, mark_default: bool) -> None:
    prev = None
    shifted = any((s.get("_house") or {}).get("shift") for s in sb["scenes"])
    for si, sc in enumerate(sb["scenes"]):
        bg = sc.get("background") or {}
        if bg.get("name") != "explainer/Ocean":
            prev = None
            continue
        p = bg.setdefault("props", {})
        if p.get("look") == "legacy":
            return
        key = p.get("key") or auto_key(p.get("depth", 40))
        if key == prev and "key" not in p:
            key = VARIANT.get(key, key)
        p["key"] = key
        sh = (sc.get("_house") or {}).get("shift")
        if not sh and not shifted and mark_default:
            beat = [_first_at(l) for l in sc.get("layers", []) if l.get("name") in SCALE_BEAT]
            if beat:
                sh = {"at": round(max(0.0, min(beat) - 0.2), 3), "to": AUTO_SHIFT.get(key, "warm")}
                shifted = True
        if sh:
            p["shiftTo"] = sh.get("to", "warm")
            p["shiftAt"] = sh["at"]
            p["shiftDur"] = sh.get("dur", 0.8)
            key = p["shiftTo"]
        prev = key


def apply(sb: dict, opts: dict | None = None) -> dict:
    """storyboard -> house-style storyboard (pure; returns a new dict)"""
    o = {"dressing": True, "motion": True, "auto_shift": True, **(opts or {})}
    sb = copy.deepcopy(sb)
    sb["overlays"] = {**sb.get("overlays", {}), "grain": 0}
    _colour(sb, o["auto_shift"])
    n = len(sb["scenes"])
    for si, sc in enumerate(sb["scenes"]):
        hs = sc.get("_house") or {}
        sc.setdefault("light", {**LIGHT, **({"sweep": 8} if sc["duration"] >= 4 else {})})
        sc.setdefault("grade", dict(GRADE))
        env = (sc.get("background") or {}).get("name") == "explainer/Ocean"
        add = []
        if hs.get("wide"):
            add += wide_planes(sc, si)
        if env and o["dressing"] and hs.get("dressing", True) and _upper_band_empty(sc):
            add += dressing(sc, si)
        sc["layers"] = add + sc.get("layers", [])
        if o["motion"]:
            _motion(sc, si, si == n - 1)
    for sc in sb["scenes"]:
        sc.pop("_house", None)
    return sb
