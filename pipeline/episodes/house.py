"""House style ("Lantern & Ink") storyboard pass for explainer episodes: the live default look.

build.py runs `apply()` on every explainer storyboard (opt out per module with HOUSE_STYLE = False or per slug with
HOUSE_SKIP), then pipeline/episodes/staging.py checks the result. Everything here is plain storyboard data that the
explainer kit renders (studio/src/kits/explainer/house/), so a builder can also write any of it by hand.

Per scene
  light     scene.light = Lantern setup (one key from the upper left for every shaded figure), a slow key sweep on
            longer scenes (light as an actor, STYLE_BIBLE §9.5). Figures are shaded by the kit by default.
  palette   Ocean backgrounds get a key ramp from their biome and depth (bible §2.5, analysis rule 6); consecutive
            scenes differ where the biome allows, and the colour SHIFT lands on the beat a builder marks with
            scene["_house"]["shift"] = {"at": s, "to": "warm"} (the scale/turn beat) when the setting has daylight in
            shallow non-polar water (no golden glow in Antarctica). With no mark, the first scale beat gets it.
  setting   scene.setting (pipeline/episodes/settings.py; settings.fill() infers it from the narration when a builder
            declares none) picks the background rig and the set: a Board for abstract beats (no creatures, no props),
            the biome's own dressing for a place (polar ice field, kelp forest, open water specks + a far bait school,
            coast, reef, twilight, deep), placed under the waterline, brightness and key from the depth, sky from the
            light. An in-scene setting change gets a full-frame rig layer (under a map card, or wiping down).
            REFERENCES_ANALYSIS §4 rules 1-13; staging.check_settings fails a build that breaks them.
            scene["_house"]["set"] = False opts a scene out; "fore": False drops its foreground.
            Dressing never counts as a staging collision.
  info      v3 information design (bible §11): Headline = Anton title plate, Tag = lantern tag, ScaleBar = gauge with an
            Anton number (kit defaults); a YOU chip hung under a figure by an svg tether becomes a lantern tag whose
            leader ends in a ring on the figure (the tether layer is dropped).
  motion    camera pre-roll on the first scene, backOut punch-ins (out-eased zoom-ins <= 0.3 s), never-still drift +
            low hand-held drift (not on the last scene: its last frame is the loop bookend), drop -> dropSquash with a
            landing kick, figure pop -> popSpring (uniform, never thinner than 60 % of rest width), label lag (tags and
            tethers riding a floating figure follow it 0.16 s / 0.07 s late), idle body sway on swimming heroes.
  colour    besides the key ramp and shift: every proof/scale beat gets the warm shift where the setting allows it, and a
            builder can re-key a scene with scene["_house"]["key"] when the key fits the biome (settings.BIOMES keys);
            boards carry the other hue families (amber / coral / dusk fields).
  cuts      every hard cut becomes a transition from the library (wipe up/left, iris, fade), so the cut rate stays
            <= 2/min (M5); builder whips become clean wipes (the whip smeared label chips into white bars: orca v2 F721).
  grade     brightness 1.02, contrast 1.04, saturate 0.94 (free, constant per scene): the teal ramp sits at HSV S ~0.95,
            so a saturate boost pushed P3 to 0.96 (target 0.66-0.88).
Storyboard: overlays.grain = 0 (texture is baked into art; live grain is invisible after x264 and costs ~20 %).
Keys starting with "_house" are removed before the storyboard is written.
"""
from __future__ import annotations

import copy
import math
import re

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


# ------------------------------------------------------------------ settings -> rigs + set dressing
# Every scene declares where it takes place (scene.setting, pipeline/episodes/settings.py; settings.fill() infers it
# from the narration when a builder doesn't). The background rig and the set dressing come from that setting: a board
# for abstract beats, the biome's own dressing for a place (REFERENCES_ANALYSIS §4 rules 9-13), placed relative to the
# waterline (nothing marine above it), brightness from depth. An in-scene setting change (a map card giving way to the
# place it names) gets a full-frame rig layer for the new place.

OVERSCAN = 1.2
BG_DEPTH = 0.12
Z_RIG, Z_SET = -60, -40          # rig layers (a new place inside a scene), then its dressing, all under the content
# sky colours live in the kit (house/oceanBg.tsx SKIES, one place to re-skin): the pass only names the sky
SPECKS = {"open_ocean": 70, "polar_ice": 0, "kelp_forest": 60, "tropical_reef": 60, "coastal_surface": 60,
          "twilight": 0, "deep": 0}


def surface_prop(waterline):
    """screen waterline (0..1) -> Ocean `surface` (fraction of the 1.2x overscanned background box)"""
    return None if waterline is None else round((waterline + (OVERSCAN - 1) / 2) / OVERSCAN, 4)


def choose_key(seg: dict, prev: str | None, want: str | None, prev_seg: dict | None = None) -> str:
    """an Ocean key ramp that fits the biome and depth (rule 6). The same place keeps its key across scenes; a different
    place of the same biome right after it takes another key so the change shows (analysis rule 5)"""
    from .settings import same
    from .settings import BIOMES
    keys = BIOMES[seg["biome"]]["keys"]
    d = float(seg.get("depth", 0))
    if want in keys:
        return want
    if seg["biome"] == "open_ocean":
        k = "royal"                       # the owner's open-ocean look (orca_set_01/04/05 concepts)
    elif seg["biome"] == "coastal_surface":
        k = "tide" if d < 30 else "mid"
    else:
        k = keys[0]
    if k == prev and len(keys) > 1 and not (prev_seg and same(seg, prev_seg)):
        k = next(x for x in keys if x != prev and x != "warm")
    return k


def rig_background(seg: dict, old: dict | None, si: int, layer: bool = False) -> dict:
    """the scene background for a setting segment: Board for boards, Ocean (key, depth, waterline, sky, light) else"""
    if seg["kind"] in ("board", "map"):
        bp = {"field": seg.get("board") or "navy", "seed": f"bd{si}", "floor": seg.get("floor", False)}
        for k in ("surface", "rays", "lanes"):
            if seg.get(k) is not None:
                bp[k] = surface_prop(seg[k]) if k == "surface" else seg[k]
        return {"type": "component", "name": "explainer/Board", "depth": BG_DEPTH, "overscan": OVERSCAN, "props": bp}
    old = old if (old or {}).get("name") == "explainer/Ocean" else {}
    p = dict((old or {}).get("props") or {})
    for k in ("skyTop", "skyBottom", "surface", "bottomColor"):
        p.pop(k, None)
    light = seg.get("light", "day")
    p["depth"] = seg.get("depth", 20)
    sp = surface_prop(seg.get("waterline"))
    if sp is not None:
        p["surface"] = sp
        p["sky"] = f"{'polar' if seg['biome'] == 'polar_ice' else 'temperate'}-{light}"
    d = float(p["depth"])
    if light in ("night",) or d >= 200:
        p["rays"], p["glow"], p["caustics"] = 0, 0, False
    elif light in ("overcast", "dusk"):
        p["rays"] = min(int(p.get("rays", 7)), 4)
        p["rayStrength"] = 0.45
        p["glow"] = min(float(p.get("glow", 1)), 0.35)
    if layer:                          # a rig layer keys itself; the scene background is keyed by _colour()
        p["key"] = choose_key(seg, None, seg.get("key") or p.get("key"))
    if seg["biome"] == "polar_ice":
        p["specks"] = 90                 # cold clear water: thinner marine snow (the krill specks are dressing)
    return {"type": "component", "name": "explainer/Ocean", "depth": BG_DEPTH, "overscan": OVERSCAN, "props": p}


def _rig_layer(bg: dict, start: float, end: float, z: int, enter: dict | None) -> dict:
    l = {"type": "component", "name": bg["name"], "role": "dressing", "x": "50%", "y": "50%",
         "width": round(W * OVERSCAN), "height": round(H * OVERSCAN), "depth": BG_DEPTH, "z": z,
         "start": round(start, 3), "end": round(end, 3), "props": bg["props"], "setting_rig": True}
    if enter:
        l["enter"] = enter
    return l


def _windows(segs: list[dict], dur: float) -> list[tuple[float, float]]:
    """per segment: the time its rig/dressing is up (starts under a map card that precedes it, runs under the next)"""
    out = []
    for i, s in enumerate(segs):
        a, b = float(s["at"]), float(s["end"])
        if i and segs[i - 1]["kind"] == "map":
            a = max(0.0, a - 0.7)
        if i + 1 < len(segs) and segs[i + 1]["kind"] == "map":
            b = min(dur, b + 0.7)
        out.append((round(a, 3), round(b, 3)))
    return out


def _timed(layers: list[dict], a: float, b: float, dur: float) -> list[dict]:
    for l in layers:
        if a > 0.01:
            l["start"] = a
        if b < dur - 0.01:
            l["end"] = b
    return layers


def biome_set(seg: dict, si: int, k: int, o: dict, fore: bool, notes: str) -> list[dict]:
    """set dressing for one place segment, all role dressing (REFERENCES_ANALYSIS §4 rule 10). k = segment index."""
    from .settings import SCHOOL_TINTS
    b, s = seg["biome"], f"{si}{'abcdefgh'[k % 8]}"
    wl = seg.get("waterline")
    top = (wl if wl is not None else 0.0) + 0.04             # first screen y that is safely under the water
    flip = -1 if si % 2 else 1
    out: list[dict] = []
    z = Z_SET + 2 * k

    def water(h0: float, h1: float):   # a full-width band [h0, h1] of the screen, clipped to the water
        h0 = max(h0, top)
        return {"x": "50%", "y": f"{(h0 + h1) / 2 * 100:.1f}%", "width": 1300, "height": round((h1 - h0) * H)}

    def specks(n, plane, depth, tints, size, op, h0=0.0, name="explainer/Specks"):
        return {"type": "component", "name": name, "role": "dressing", **water(h0, 1.0), "depth": depth, "z": z,
                "props": {"n": n, "seed": f"sp{s}{plane}", "tints": tints, "size": size, "opacity": op, "drift": [3, -4]}}

    coast = seg.get("coast") or ({"kind": "cliffs"} if b == "coastal_surface" else None)
    if wl is not None and (b == "polar_ice" or coast):
        rig = "explainer/IceField" if b == "polar_ice" else "explainer/Coast"
        out.append({"type": "component", "name": rig, "role": "dressing", "x": "50%", "y": "50%",
                    "width": round(W * OVERSCAN), "height": round(H * OVERSCAN), "depth": BG_DEPTH, "z": z,
                    "props": {"waterline": surface_prop(wl), "seed": f"pl{s}", "bergs": 3, "brash": 12, **(coast or {}),
                              **({"sun": 0.8 if b == "polar_ice" else 0.62} if seg.get("light") == "dusk" else {})}})
    if b == "polar_ice":
        # krill: tiny pink specks in the cold water (their native swarm; a warm hue family where it is real)
        out.append(specks(60, "mid", 0.6, ["coral-4", "amber-4", "bone-1"], [2.0, 4.2], [0.25, 0.55]))
    elif b in ("open_ocean", "coastal_surface"):
        out.append(specks(SPECKS[b], "far", 0.3, ["tide-4", "bone-1"], [2.0, 4.0], [0.2, 0.45]))
        if (seg.get("ambient", True) and float(seg.get("depth", 0)) < 200) and si % 2 == 0:
            # a far bait school low in the frame (native, small, low contrast, under the caption band)
            out.append({"type": "component", "name": "explainer/FishSchool", "role": "dressing", **water(0.8, 0.9),
                        "depth": 0.3, "z": z, "opacity": 0.55,
                        "props": {"n": 14, "seed": f"bf{s}", "scale": 0.32, "plane": "far", "dir": flip,
                                  "tints": SCHOOL_TINTS[b]}})
    elif b == "kelp_forest":
        out += [
            {"type": "component", "name": "explainer/Ridge", "role": "dressing", "x": "50%", "y": "82%", "width": 1500,
             "height": 700, "depth": 0.3, "z": z, "props": {"seed": f"rd{s}", "plane": "far", "y": 0.84, "spires": False}},
            {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "50%", "y": "70%", "width": 1500,
             "height": 1100, "depth": 0.3, "z": z, "props": {"seed": f"fk{s}", "n": 7, "plane": "far", "blade": 0.8, "golden": True}},
            {"type": "component", "name": "explainer/FishSchool", "role": "dressing", **water(0.8, 0.9), "depth": 0.35,
             "z": z, "opacity": 0.7, "props": {"n": 16, "seed": f"kf{s}", "scale": 0.4, "plane": "far", "dir": flip,
                                               "tints": SCHOOL_TINTS[b]}},
            {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "5%", "y": "66%", "width": 320,
             "height": 1500, "depth": 0.6, "z": z + 1, "props": {"seed": f"mk{s}", "n": 2, "plane": "mid", "height": [0.8, 1.0], "blade": 1.3, "golden": True}},
            {"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "95%", "y": "68%", "width": 320,
             "height": 1400, "depth": 0.6, "z": z + 1, "props": {"seed": f"mk{s}b", "n": 1, "plane": "mid", "height": [0.65, 0.9], "blade": 1.2, "golden": True}},
            {"type": "component", "name": "explainer/Rocks", "role": "dressing", "x": "50%", "y": "96%", "width": 1300,
             "height": 300, "depth": 0.6, "z": z + 1, "props": {"seed": f"rk{s}", "n": 4, "plane": "mid"}},
            specks(SPECKS[b], "far", 0.3, ["kelp-4", "bone-1"], [2.0, 4.0], [0.2, 0.45]),
        ]
        if fore:
            out += [{"type": "component", "name": "explainer/Kelp", "role": "dressing", "x": "-2%" if flip > 0 else "102%",
                     "y": "80%", "width": 420, "height": 1500, "depth": 1.45, "z": 30, "blur": 9,
                     "props": {"seed": f"ek{s}", "n": 2, "plane": "fore", "height": [0.75, 1.0], "blade": 1.5}}]
    elif b == "tropical_reef":
        out += [
            {"type": "component", "name": "explainer/Ridge", "role": "dressing", "x": "50%", "y": "80%", "width": 1500,
             "height": 700, "depth": 0.3, "z": z, "props": {"seed": f"rd{s}", "plane": "far", "y": 0.82}},
            {"type": "component", "name": "explainer/FishSchool", "role": "dressing", **water(0.5, 0.62), "depth": 0.35,
             "z": z, "props": {"n": 18, "seed": f"s{s}", "scale": 0.5, "plane": "far", "dir": flip, "tints": SCHOOL_TINTS[b]}},
            {"type": "component", "name": "explainer/Jellies", "role": "dressing", **water(0.3, 0.55), "depth": 0.6, "z": z + 1,
             "opacity": 0.85, "props": {"n": 2, "seed": f"j{s}", "size": [22, 38], "plane": "mid", "rise": 2}},
            {"type": "component", "name": "explainer/Reef", "role": "dressing", "x": "50%", "y": "90%", "width": 1400,
             "height": 560, "depth": 0.6, "z": z + 1, "props": {"seed": f"rf{s}", "plane": "mid", "shelf": 0.35}},
            {"type": "component", "name": "explainer/Rocks", "role": "dressing", "x": "50%", "y": "97%", "width": 1300,
             "height": 260, "depth": 0.6, "z": z + 1, "props": {"seed": f"rk{s}", "n": 3, "plane": "mid"}},
        ]
    elif b == "twilight":
        out += [specks(140, "far", 0.3, ["tide-5", "sky-4"], [2.0, 4.5], [0.25, 0.7]),
                {"type": "component", "name": "explainer/FishSchool", "role": "dressing", **water(0.78, 0.9), "depth": 0.3,
                 "z": z, "opacity": 0.5, "props": {"n": 12, "seed": f"lf{s}", "scale": 0.3, "plane": "far", "dir": flip,
                                                   "tints": SCHOOL_TINTS[b]}}]
    elif b == "deep":
        out.append(specks(120, "far", 0.3, ["bone-1", "bone-0"], [2.0, 4.0], [0.15, 0.45]))
    if o.get("pod") and b in ("open_ocean", "polar_ice", "kelp_forest", "coastal_surface") and \
            re.search(r"\b(orcas?|pod|killer whales?)\b", notes, re.I) and not seg.get("counted"):
        out.append({"type": "component", "name": "explainer/Pod", "role": "dressing", **water(0.78, 0.92), "depth": 0.35,
                    "z": z, "props": {"seed": f"pd{s}", "n": 2, "dir": -flip, "plane": "far", "scale": 0.8}})
    return out


def set_layers(sc: dict, si: int, o: dict, fore: bool) -> list[dict]:
    """rig layers for in-scene setting changes + the biome dressing of every place segment, timed to its segment"""
    from .settings import normalise, same, segments
    segs = [{**normalise(s), "at": s["at"], "end": s["end"]} for s in segments(sc)]
    dur = sc["duration"]
    if not segs:
        return []
    bgi = next((i for i, s in enumerate(segs) if s["kind"] != "map"), 0)
    wins = _windows(segs, dur)
    out = []
    for i, s in enumerate(segs):
        if s["kind"] == "map":
            continue
        a, b = wins[i]
        if i != bgi and not same(s, segs[bgi]):
            prev_map = i and segs[i - 1]["kind"] == "map"
            enter = None if prev_map else {"type": "wipeDown", "at": round(float(s["at"]), 3), "duration": 0.45}
            out.append(_rig_layer(rig_background(s, sc.get("background"), si * 10 + i, layer=True), a if prev_map else float(s["at"]), b,
                                  Z_RIG + 2 * i, enter))
        if s["kind"] == "place" and o["set"]:
            out += _timed(biome_set(s, si, i, o, fore and i == bgi, sc.get("notes") or ""), a, b, dur)
    return out


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
            # the core whip smears label chips into white bars with a hard seam (orca v2 F721): a clean wipe instead
            sc["transitionIn"] = {"type": "wipe", "duration": 0.5, "direction": tr.get("direction", "left")}
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


def bg_segment(sc: dict) -> dict | None:
    """the setting segment the scene background draws (the first one that is not a map card)"""
    from .settings import normalise, segments
    segs = [normalise(s) for s in segments(sc)]
    return next((s for s in segs if s["kind"] != "map"), segs[0] if segs else None)


def shift_ok(seg: dict | None) -> bool:
    """a warm lift is daylight in shallow non-polar water only (no golden glow in Antarctica or at 500 m)"""
    return bool(seg) and seg["kind"] == "place" and seg.get("light", "day") == "day" and seg["biome"] not in \
        ("polar_ice", "twilight", "deep") and float(seg.get("depth", 0)) < 50


def _colour(sb: dict, mark_default: bool) -> None:
    """key ramps from each scene's setting (biome + depth: rule 6), neighbouring scenes differ where the biome allows,
    one colour shift on the scale/turn beat where the setting allows a warm lift"""
    prev, prev_seg = None, None
    shifted = any((s.get("_house") or {}).get("shift") for s in sb["scenes"])
    for si, sc in enumerate(sb["scenes"]):
        bg = sc.get("background") or {}
        seg = bg_segment(sc)
        if bg.get("name") != "explainer/Ocean":
            prev, prev_seg = None, None
            continue
        p = bg.setdefault("props", {})
        if p.get("look") == "legacy":
            return
        hk = (sc.get("_house") or {}).get("key") or p.get("key")
        want = (sc.get("_house") or {}).get("key") or (seg or {}).get("key") or p.get("key")
        key = choose_key(seg, prev, want, prev_seg) if seg and seg.get("biome") in _biomes() else (hk or auto_key(p.get("depth", 40)))
        p["key"] = key
        p.pop("bottomColor", None) if (sc.get("_house") or {}).get("key") else None
        sh = (sc.get("_house") or {}).get("shift")
        if sh and not shift_ok(seg):
            sh = None                     # the builder's mark lands on a setting without daylight: no warm lift
        beat = [_first_at(l) for l in sc.get("layers", []) if l.get("name") in SCALE_BEAT]
        if not sh and not shifted and mark_default and beat and shift_ok(seg) and (sc.get("_house") or {}).get("proof", True):
            sh = {"at": round(max(0.0, min(beat) - 0.2), 3), "to": AUTO_SHIFT.get(key, "warm")}
            shifted = True
        elif not sh and mark_default and beat and key in ("tide", "sky", "mid") and shift_ok(seg) and \
                (sc.get("_house") or {}).get("proof", True):
            sh = {"at": round(max(0.0, min(beat) - 0.2), 3), "to": "warm"}
        sc.setdefault("light", dict(LIGHT))
        sc["light"].setdefault("haze", HAZE.get(key, "tide-1"))
        if sh:
            p["shiftTo"] = sh.get("to", "warm")
            p["shiftAt"] = sh["at"]
            p["shiftDur"] = sh.get("dur", 0.8)
            key = p["shiftTo"]
        prev, prev_seg = key, seg


def _biomes():
    from .settings import BIOMES
    return BIOMES


def _rigs(sb: dict) -> None:
    """scene background from its setting (Board for boards, Ocean keyed to the place); legacy looks are left alone"""
    for si, sc in enumerate(sb["scenes"]):
        bg = sc.get("background") or {}
        if ((bg.get("props") or {}).get("look")) == "legacy":
            continue
        seg = bg_segment(sc)
        if seg is None or (bg.get("name") not in ("explainer/Ocean", "explainer/Board", None) and seg["kind"] == "place"):
            continue                      # a builder's own non-ocean background (land kit, horror sets) stays
        sc["background"] = rig_background(seg, bg, si)


def apply(sb: dict, opts: dict | None = None) -> dict:
    """storyboard -> house-style storyboard (pure; returns a new dict)"""
    from .settings import fill
    o = {"dressing": True, "set": True, "info": True, "cuts": True, "motion": True, "auto_shift": True, **(opts or {})}
    sb = copy.deepcopy(sb)
    fill(sb)
    sb["overlays"] = {**sb.get("overlays", {}), "grain": 0}
    _rigs(sb)
    _colour(sb, o["auto_shift"])
    n = len(sb["scenes"])
    for si, sc in enumerate(sb["scenes"]):
        hs = sc.get("_house") or {}
        sc.setdefault("light", dict(LIGHT))
        if sc["duration"] >= 4:
            sc["light"].setdefault("sweep", 8)
        sc.setdefault("grade", dict(GRADE))
        add = []
        if hs.get("set", True) and o["dressing"]:
            # foreground in 4 of every 5 scenes where the biome has one, never on the cover/bookend (the loop seam)
            fore = hs.get("fore", si % 5 != 2 and si not in (0, n - 1))
            add += set_layers(sc, si, {**o, "set": o["set"]}, fore)
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
