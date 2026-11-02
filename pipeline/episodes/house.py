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
  set       EVERY environment scene (Ocean background) gets the orca_open_v3 set, so the look persists through the
            whole video (judge, orca_full_v1: a reef strip only at 3-10 s scored depth 3/12): far ridge + spires, far kelp
            and an optional background pod (HOUSE_OPTS "pod": "orca", depth 0.3-0.35); mid side kelp with node rings, a
            warm saturated reef + rocks across the bottom, seeded jellies and a school in the upper/middle water (depth
            0.6); a cropped, blurred ink foreground (kelp silhouettes at the frame edges, depth 1.45) in >= 60 % of the
            scenes (bible §6/§8). scene["_house"]["set"] = False opts a scene out; "fore": False drops its foreground.
            Dressing never counts as a staging collision.
  info      v3 information design (bible §11): Headline = Anton title plate, Tag = lantern tag, ScaleBar = gauge with an
            Anton number (kit defaults); a YOU chip hung under a figure by an svg tether becomes a lantern tag whose
            leader ends in a ring on the figure (the tether layer is dropped).
  motion    camera pre-roll on the first scene, backOut punch-ins (out-eased zoom-ins <= 0.3 s), never-still drift +
            low hand-held drift (not on the last scene: its last frame is the loop bookend), drop -> dropSquash with a
            landing kick, figure pop -> popSpring (uniform, never thinner than 60 % of rest width), label lag (tags and
            tethers riding a floating figure follow it 0.16 s / 0.07 s late), idle body sway on swimming heroes.
  colour    besides the key ramp and shift: every proof/scale beat gets the warm shift (sunlit keys) and a builder can re-key
            a scene with scene["_house"]["key"] (e.g. "danger" for the shark/kill beats), so the video has a second and
            third hue family per beat (judge: one teal key for the whole video, P5 = 1).
  cuts      every hard cut becomes a transition from the library (wipe up/left, iris, fade; builder whips kept and slowed
            to >= 0.45 s), so the cut rate stays <= 2/min (M5) and the transitions are motivated (water wipe, light iris).
  grade     brightness 1.02, contrast 1.04, saturate 0.94 (free, constant per scene): the teal ramp sits at HSV S ~0.95,
            so a saturate boost pushed P3 to 0.96 (target 0.66-0.88).
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
GRADE = {"brightness": 1.02, "contrast": 1.04, "saturate": 0.94}
LIGHT = {"setup": "lantern"}
# plane haze per key ramp (dressing.tsx far/mid planes mix toward it)
HAZE = {"tide": "tide-1", "sky": "tide-1", "warm": "tide-1", "mid": "tide-0", "kelp": "kelp-1", "deep": "ink-3",
        "ink": "ink-3", "dusk": "dusk-1", "danger": "coral-0"}


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


def env_set(scene: dict, si: int, o: dict, fore: bool) -> list[dict]:
    """the persistent orca_open_v3 set for an environment scene (bible §6/§8), all role dressing"""
    flip = -1 if si % 2 else 1
    out = [
        {"type": "component", "name": "explainer/Ridge", "role": "dressing", "x": "50%", "y": "80%", "width": 1500, "height": 700,
         "depth": 0.3, "z": -12, "props": {"seed": f"rd{si}", "plane": "far", "y": 0.82}},
        {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "50%", "y": "72%", "width": 1500, "height": 1000,
         "depth": 0.3, "z": -11, "props": {"seed": f"fk{si}", "n": 4, "plane": "far", "blade": 0.6}},
    ]
    if o.get("pod"):
        out.append({"type": "component", "name": "explainer/Pod", "role": "dressing", "x": "50%", "y": "24%", "width": 1300,
                    "height": 420, "depth": 0.35, "z": -10, "props": {"seed": f"pd{si}", "n": 3, "dir": -flip, "plane": "far"}})
    out += [
        {"type": "component", "name": "explainer/FishSchool", "role": "dressing", "x": "50%", "y": "27%" if si % 2 else "58%",
         "width": 1300, "height": 260, "depth": 0.35, "z": -9,
         "props": {"n": 18, "seed": f"s{si}", "scale": 0.5, "plane": "far", "dir": flip}},
        {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "5%", "y": "66%", "width": 320, "height": 1500,
         "depth": 0.6, "z": -8, "props": {"seed": f"mk{si}", "n": 1, "plane": "mid", "height": [0.8, 1.0], "blade": 1.1}},
        {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "95%", "y": "68%", "width": 320, "height": 1400,
         "depth": 0.6, "z": -8, "props": {"seed": f"mk{si}b", "n": 1, "plane": "mid", "height": [0.65, 0.9], "blade": 1.0}},
        {"type": "component", "name": "explainer/Jellies", "role": "dressing", "x": "50%", "y": "30%", "width": 1200,
         "height": 620, "depth": 0.6, "z": -7, "opacity": 0.9,
         "props": {"n": 3, "seed": f"j{si}", "size": [24, 44], "plane": "mid", "colors": ["amber-3", "coral-3", "tide-3"]}},
        {"type": "component", "name": "explainer/Reef", "role": "dressing", "x": "50%", "y": "90%", "width": 1400, "height": 560,
         "depth": 0.6, "z": -6, "props": {"seed": f"rf{si}", "plane": "mid", "shelf": 0.35}},
        {"type": "component", "name": "explainer/Rocks", "role": "dressing", "x": "50%", "y": "97%", "width": 1300, "height": 260,
         "depth": 0.6, "z": -5, "props": {"seed": f"rk{si}", "n": 3, "plane": "mid"}},
    ]
    if fore:
        out += [
            {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "-2%" if flip > 0 else "102%", "y": "80%",
             "width": 420, "height": 1500, "depth": 1.45, "z": 30, "blur": 9,
             "props": {"seed": f"ek{si}", "n": 2, "plane": "fore", "height": [0.75, 1.0], "blade": 1.5}},
            {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "103%" if flip > 0 else "-3%", "y": "84%",
             "width": 360, "height": 1300, "depth": 1.45, "z": 30, "blur": 9,
             "props": {"seed": f"ek{si}b", "n": 1, "plane": "fore", "height": [0.6, 0.85], "blade": 1.6}},
        ]
    return out


def _covered(scene: dict) -> bool:
    """a full-frame card (Map) is up for the whole scene: no set behind it"""
    dur = scene["duration"]
    for l in scene.get("layers", []):
        if l.get("name") == "explainer/Map" and (l.get("end") or dur) - (l.get("start") or 0) >= 0.9 * dur:
            return True
    return False


TETHER = 'x1="5" y1="0" x2="5" y2="100"'


def _info(sc: dict) -> None:
    """YOU chip + svg tether -> one lantern tag with a ring leader on the figure (bible §11)"""
    layers = sc.get("layers", [])
    drop = set()
    for i, l in enumerate(layers):
        if l.get("type") != "svg" or TETHER not in str(l.get("svg") or l.get("src") or l.get("markup") or ""):
            continue
        tag = next((t for t in layers[i + 1:i + 3] if t.get("name") == "explainer/Tag" and t.get("x") == l.get("x")
                    and str((t.get("props") or {}).get("text", "")).upper().startswith("YOU")), None)
        if not tag:
            continue
        ly, lh = float(str(l["y"]).rstrip("%")) / 100 * H, float(l.get("height", 40))
        ty = float(str(tag["y"]).rstrip("%")) / 100 * H
        top = ly - lh / 2
        p = tag.setdefault("props", {})
        p["leader"] = [0, round(top - ty, 1)]
        p["accent"] = "red"
        for k in ("bg", "color"):
            p.pop(k, None)
        drop.add(i)
    if drop:
        sc["layers"] = [l for i, l in enumerate(layers) if i not in drop]


def _transitions(sb: dict) -> None:
    """hard cuts -> library transitions (M5 <= 2 cuts/min, bible §9.6); builder whips are kept, never faster than 0.45 s"""
    lib = [{"type": "wipe", "duration": 0.55, "direction": "up"}, {"type": "fade", "duration": 0.5},
           {"type": "iris", "duration": 0.55}, {"type": "wipe", "duration": 0.55, "direction": "left"}]
    k = 0
    n = len(sb["scenes"])
    for i, sc in enumerate(sb["scenes"]):
        if i == 0:
            continue
        tr = sc.get("transitionIn") or {}
        typ = tr.get("type", "cut")
        if typ == "whip":
            tr["duration"] = max(0.45, tr.get("duration", 0.3))
            continue
        if typ == "dipBlack":
            # the dip to black read as a hard cut (M5); a slow crossfade keeps the beat without the black frame
            sc["transitionIn"] = {"type": "fade", "duration": 0.6}
            continue
        if typ != "cut":
            continue
        if i == n - 1:
            sc["transitionIn"] = {"type": "fade", "duration": 0.5}
            continue
        bg = (sc.get("background") or {}).get("props") or {}
        prev = (sb["scenes"][i - 1].get("background") or {}).get("props") or {}
        dark = lambda p: p.get("key") in ("deep", "ink", "dusk", "danger")
        if dark(prev) and not dark(bg):
            sc["transitionIn"] = {"type": "iris", "duration": 0.55}   # light opening out of the dark
            continue
        sc["transitionIn"] = dict(lib[k % len(lib)])
        k += 1


def _soften(sc: dict) -> None:
    """in-scene hard changes the cut detector counts (M5): full-frame cards pop in/out -> fades; white hit flashes dimmed"""
    dur = sc["duration"]
    for l in sc.get("layers", []):
        if l.get("name") == "explainer/Map":
            s0, e0 = l.get("start"), l.get("end")
            if isinstance(s0, (int, float)) and s0 > 0.05 and not l.get("enter"):
                l["enter"] = {"type": "fade", "at": s0, "duration": 0.6}
            if isinstance(e0, (int, float)) and e0 < dur - 0.05 and not l.get("exit"):
                l["exit"] = {"type": "fade", "at": max(0.0, e0 - 0.6), "duration": 0.6}
        if l.get("type") == "rect" and str(l.get("fill", "")).lower() in ("#fff", "#ffffff"):
            for k in l.get("keyframes", []):
                if isinstance(k.get("opacity"), (int, float)):
                    k["opacity"] = round(k["opacity"] * 0.3, 3)   # the shake + SFX carry the hit


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
        hk = (sc.get("_house") or {}).get("key")
        if hk:
            # a builder re-key is a colour statement: it replaces the depth darkening / bottom override it would fight
            p["key"] = hk
            p.pop("bottomColor", None)
            if isinstance(p.get("depth"), (int, float)):
                p["depth"] = min(p["depth"], 60)
        key = p.get("key") or auto_key(p.get("depth", 40))
        if key == prev and "key" not in p:
            key = VARIANT.get(key, key)
        p["key"] = key
        sh = (sc.get("_house") or {}).get("shift")
        beat = [_first_at(l) for l in sc.get("layers", []) if l.get("name") in SCALE_BEAT]
        if not sh and not shifted and mark_default and beat:
            sh = {"at": round(max(0.0, min(beat) - 0.2), 3), "to": AUTO_SHIFT.get(key, "warm")}
            shifted = True
        elif not sh and mark_default and beat and key in ("tide", "sky", "mid") and (sc.get("_house") or {}).get("proof", True):
            # every later proof beat warms too (a second hue family where the numbers land)
            sh = {"at": round(max(0.0, min(beat) - 0.2), 3), "to": "warm"}
        # far planes haze toward the water they sit in (a teal haze in a dark scene drew pale spires)
        sc.setdefault("light", dict(LIGHT))
        sc["light"].setdefault("haze", HAZE.get(key, "tide-1"))
        if sh:
            p["shiftTo"] = sh.get("to", "warm")
            p["shiftAt"] = sh["at"]
            p["shiftDur"] = sh.get("dur", 0.8)
            key = p["shiftTo"]
        prev = key


def apply(sb: dict, opts: dict | None = None) -> dict:
    """storyboard -> house-style storyboard (pure; returns a new dict)"""
    o = {"dressing": True, "set": True, "info": True, "cuts": True, "motion": True, "auto_shift": True, **(opts or {})}
    sb = copy.deepcopy(sb)
    sb["overlays"] = {**sb.get("overlays", {}), "grain": 0}
    _colour(sb, o["auto_shift"])
    n = len(sb["scenes"])
    for si, sc in enumerate(sb["scenes"]):
        hs = sc.get("_house") or {}
        sc.setdefault("light", dict(LIGHT))
        if sc["duration"] >= 4:
            sc["light"].setdefault("sweep", 8)
        sc.setdefault("grade", dict(GRADE))
        env = (sc.get("background") or {}).get("name") == "explainer/Ocean" and \
            ((sc.get("background") or {}).get("props") or {}).get("look") != "legacy"
        add = []
        if env and o["set"] and hs.get("set", True) and not _covered(sc):
            # foreground in 4 of every 5 scenes (>= 60 %, bible §6), never on the cover/bookend (frame 0 = the loop seam)
            fore = hs.get("fore", si % 5 != 2 and si not in (0, n - 1))
            # the last scene is the loop bookend: it reuses scene 0's set so the replay seam matches frame 0
            add += env_set(sc, 0 if si == n - 1 and n > 1 else si, o, fore)
        elif env and o["dressing"] and hs.get("dressing", True) and _upper_band_empty(sc):
            add += dressing(sc, si)
        sc["layers"] = add + sc.get("layers", [])
        if o["info"]:
            _info(sc)
        if o["cuts"]:
            _soften(sc)
        if o["motion"]:
            _motion(sc, si, si == n - 1)
    if o["cuts"]:
        _transitions(sb)
    for sc in sb["scenes"]:
        sc.pop("_house", None)
    return sb
