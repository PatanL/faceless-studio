"""Story-lane camera grammar: glide and never stop (RicksClips3000 measurements).

Source: research/references/STORY_LANE_TUTORIAL_CHECK.md (camera table, plan step 1). The references are moving in
96-100 % of frames, median 5.8-11 px/frame at 720p, 0-3 hard cuts per Short, scene changes as 6-8 frame dissolves,
eased moves of ~24-40 frames, slow push-ins on 69-89 % of quiet frames and no hand-held float. Our v4 cut 20 times and
sat still in 30 % of its frames (median 0.58 px/f).

auto.py runs `apply()` after the house pass when shots.json has a top-level "story_camera": {...} (options below; {}
takes the defaults). It rewrites each scene's camera from the framings the shots author wrote:

  framings   every authored camera key is a framing the camera arrives at near that key's time. Two keys under 2
             frames apart (the old in-scene "cut" idiom) collapse into the later framing, so they become a glide.
  glides     sine-eased moves of glide_s (default 1.0 s = 30 f, FWHM ~20 f; never under min_glide_s), landing
             land_frac of the glide after the anchor word, so the move carries into the word. A glide blends from the
             hold path it leaves into the hold path it joins, so velocity is continuous (no stop at either end).
  holds      between glides the camera pushes in (push per frame on the zoom, at most hold_max_push per hold) and
             drifts sideways (drift_px per frame on screen at 1080 wide), so it never stops. drift_mode "toward" (the
             safe one, used by story-chess-turk v5): the drift heads for the next framing and covers at most
             hold_drift_frac of the way, so the camera never leaves the span between two checked framings; "free":
             toward the next framing or alternating, any distance up to hold_max_drift (subjects can leave the frame).
  output     the path is sampled every 2 frames as linear keyframes (camera.ts interpolates between them).
  shake      removed (house float and kicks); camera.drift and preroll removed (the holds replace them).
  depth      the background and every stick/Set layer move at set_depth (default 0.9), so the whole set travels with
             the camera (the old 0.3 left 70 % of the frame nearly still); framings are clamped so the overscanned
             set always covers the frame.
  lens blur  set_blur > 0 (px at 1080): a stick/Set background becomes a full-frame layer under everything with that
             blur (backgrounds take no filter), and stick/Set layers get it too; characters and props stay sharp. The
             blur scales with the camera zoom, so close-ups get the softer background the references show.
  cuts       a scene starts with a xfade_s crossfade (default 7 frames) unless its 1-based index is in "cuts"
             (at most 3: kept as hard cuts, for the big punches).
  swaps      layers that start after the scene start or end before its end (shot changes inside a scene) get
             swap_s fades; the outgoing layer is held swap_s longer, so the swap reads as a dissolve, not a cut.

per framing (an authored camera key): "drift": -1 | 0 | 1 sideways direction of the hold after it (0 = push only),
"push": the most that hold may push in (zoom fraction), "cont": true on the first key = start where the previous
scene's camera ended (same set on both sides of a crossfade: the dissolve then shows no double image).
options: cuts [ints], glide_s 1.0, min_glide_s 0.8, land_frac 0.3, push 0.003, hold_max_push 0.18, drift_px 3.3, hold_max_drift 130 (screen px per hold), min_push 0.0011, drift_mode free|toward, hold_drift_frac 0.6,
         set_depth 0.9, xfade_s 0.233, swap_s 0.233, min_zoom 1.0, overscan 1.2, set_blur 0

`speed_report(sb)` estimates the camera_motion.py numbers (moving share, median px/frame at 720 wide) from the
storyboard without rendering (set plane only; characters ride at depth 1 and move a little more).
"""
from __future__ import annotations

import copy
import math

W, H, FPS = 1080, 1920, 30
DEFAULTS = {"cuts": [], "glide_s": 1.0, "min_glide_s": 0.8, "land_frac": 0.3, "push": 0.003, "hold_max_push": 0.18,
            "drift_px": 3.3, "hold_max_drift": 130, "min_push": 0.0011, "drift_mode": "free", "hold_drift_frac": 0.6, "set_depth": 0.9, "xfade_s": 0.233, "swap_s": 0.233, "min_zoom": 1.0, "overscan": 1.2,
            "set_blur": 0.0}
SWAP_LAYERS = {"stick/Person", "stick/Turk", "stick/Chess", "stick/Set", "stick/Paper", "explainer/Map"}


def _px(v, full: float) -> float:
    if isinstance(v, str) and v.endswith("%"):
        return float(v[:-1]) / 100 * full
    return float(v)


def _framings(cam: dict | None, dur: float) -> list[dict]:
    """authored keys -> [{t, x, y, z}] with instant jumps collapsed (the later framing wins)"""
    keys = sorted((cam or {}).get("keyframes") or [], key=lambda k: k["t"])
    out: list[dict] = []
    last = {"x": W / 2, "y": H / 2, "z": 1.0}
    for k in keys:
        f = {"t": max(0.0, min(dur, float(k["t"]))),
             "x": _px(k["x"], W) if "x" in k else last["x"],
             "y": _px(k["y"], H) if "y" in k else last["y"],
             "z": float(k.get("zoom", last["z"]))}
        for opt in ("drift", "push", "cont"):          # per-framing hold overrides (see module doc)
            if opt in k:
                f[opt] = k[opt]
        last = f
        if out and f["t"] - out[-1]["t"] < 2 / FPS:
            out[-1] = {**f, "t": out[-1]["t"]} if len(out) == 1 and out[-1]["t"] == 0 else f
            continue
        out.append(f)
    if not out:
        out = [{"t": 0.0, "x": W / 2, "y": H / 2, "z": 1.05}]
    if out[0]["t"] > 0:
        out.insert(0, {**out[0], "t": 0.0})
    # drop framings that do not move (a hold continues through them)
    slim = [out[0]]
    for f in out[1:]:
        p = slim[-1]
        if abs(f["x"] - p["x"]) < 4 and abs(f["y"] - p["y"]) < 4 and abs(f["z"] / p["z"] - 1) < 0.015:
            continue
        slim.append(f)
    return slim


def _clamp(f: dict, o: dict) -> dict:
    d, ov = o["set_depth"], o["overscan"]
    z = max(o["min_zoom"], f["z"])
    ze = 1 + (z - 1) * d
    mx = max(0.0, (W * ov / 2 - W / (2 * ze)) / d)
    my = max(0.0, (H * ov / 2 - H / (2 * ze)) / d)
    return {**f, "z": z, "x": min(W / 2 + mx, max(W / 2 - mx, f["x"])), "y": min(H / 2 + my, max(H / 2 - my, f["y"]))}


def scene_camera(cam: dict | None, dur: float, si: int, o: dict, prev_end: dict | None = None) -> dict:
    fr = [_clamp(f, o) for f in _framings(cam, dur)]
    if prev_end is not None and fr[0].get("cont"):
        fr[0] = {**fr[0], **prev_end}               # same set as the scene before: start where its camera ended
    # glide windows
    glides = []
    prev_end = 0.0
    for i in range(1, len(fr)):
        L = o["glide_s"]
        s = fr[i]["t"] - (1 - o["land_frac"]) * L
        s = max(s, prev_end + 2 / FPS)
        e = s + L
        if e > dur + 0.1:                      # land before the scene ends
            e = dur + 0.1
            s = max(prev_end + 2 / FPS, e - L)
        if e - s < o["min_glide_s"]:
            e = s + o["min_glide_s"]
        glides.append((s, e, fr[i]))
        prev_end = e
    # hold velocities (per frame): push-in on log zoom, sideways drift toward the next framing (screen px / zoom)
    end_t = dur + 0.3                          # keep moving through the outgoing crossfade
    bounds = [0.0] + [g[1] for g in glides]    # hold i runs from bounds[i] to the next glide start (or end_t)
    sign = 1 if si % 2 == 0 else -1
    vel = []
    for i in range(len(glides) + 1):
        h0 = bounds[i]
        h1 = glides[i][0] if i < len(glides) else end_t
        here = fr[0] if i == 0 else glides[i - 1][2]
        nxt = glides[i][2] if i < len(glides) else None
        n = max(1.0, (h1 - h0) * FPS)
        # a capped hold still pushes at >= min_push per frame (the references' quiet frames zoom in 69-89 % of the time)
        dz = math.log1p(max(o["min_push"], min(o["push"], here.get("push", o["hold_max_push"]) / n)))
        if o["drift_mode"] == "toward":
            # the push also saturates at the framing's cap (+ the min_push floor over the hold), so a glide that
            # extrapolates the hold never zooms past what was checked
            zcap = math.log1p(max(here.get("push", o["hold_max_push"]), o["min_push"] * n))
            dz = (dz, zcap)
            # safe drift: only toward the next framing and at most hold_drift_frac of the way there, so the camera stays
            # between two authored (checked) framings; no sideways drift on the last hold or where "drift": 0
            if nxt is None or here.get("drift") == 0:
                vel.append((0.0, 0.0, dz, None))
                continue
            ddx, ddy = (nxt["x"] - here["x"]) * here["z"], (nxt["y"] - here["y"]) * here["z"]   # screen px
            dist = math.hypot(ddx, ddy)
            if dist < 1:
                vel.append((0.0, 0.0, dz, None))
                continue
            reach = min(o["hold_max_drift"], o["hold_drift_frac"] * dist)       # screen px
            vd = min(o["drift_px"], 2 * reach / n)
            # saturating: starts at vd and eases toward `reach`, never past it (also while a glide extrapolates it)
            vel.append((vd * ddx / dist, vd * ddy / dist, dz, reach))
            continue
        if "drift" in here:
            dirx = here["drift"]                    # authored: -1 left, 1 right, 0 push only
        elif nxt is not None and abs(nxt["x"] - here["x"]) > 6:
            dirx = 1 if nxt["x"] > here["x"] else -1
        else:
            dirx, sign = sign, -sign
        dy = 0.0 if nxt is None or abs(nxt["y"] - here["y"]) <= 6 else (0.35 if nxt["y"] > here["y"] else -0.35)
        vd = min(o["drift_px"], o["hold_max_drift"] / n)   # long holds drift slower: the subject stays in frame
        vel.append((dirx * vd, dy * vd, dz, None))

    def hold_state(i: int, base: dict, tau: float) -> tuple[float, float, float]:
        vx, vy, dz, reach = vel[i]
        n = tau * FPS
        if isinstance(dz, tuple):
            r, cap = dz
            z = base["z"] * math.exp(cap * (1 - math.exp(-r * max(0.0, n) / cap)) if n > 0 else r * n)
        else:
            z = base["z"] * math.exp(dz * n)
        if reach:                                   # toward mode: travel reach * (1 - e^(-v n / reach)) screen px
            v = math.hypot(vx, vy)
            k = reach * (1 - math.exp(-v * max(0.0, n) / reach)) / v if n > 0 else n
            return base["x"] + vx * k / z, base["y"] + vy * k / z, z
        return base["x"] + vx * n / z, base["y"] + vy * n / z, z

    def sine(p: float) -> float:
        p = min(1.0, max(0.0, p))
        return 0.5 - 0.5 * math.cos(math.pi * p)

    states = []
    nf = int(math.ceil(end_t * FPS))
    gi = 0
    for fi in range(nf + 1):
        t = fi / FPS
        while gi < len(glides) and t >= glides[gi][1]:
            gi += 1
        base = fr[0] if gi == 0 else glides[gi - 1][2]
        hb = bounds[gi]
        if gi < len(glides) and t >= glides[gi][0]:
            gs, ge, tgt = glides[gi]
            a = hold_state(gi, base, t - hb)                   # where the hold would have drifted to
            b = hold_state(gi + 1, tgt, t - ge)                # the next hold's path, extended back in time
            e = sine((t - gs) / (ge - gs))
            x, y, z = (a[0] + (b[0] - a[0]) * e, a[1] + (b[1] - a[1]) * e, math.exp(math.log(a[2]) + (math.log(b[2]) - math.log(a[2])) * e))
        else:
            x, y, z = hold_state(gi, base, t - hb)
        c = _clamp({"x": x, "y": y, "z": z}, o)
        states.append((t, c["x"], c["y"], c["z"]))
    step = 2
    clean = [{"t": round(t, 4), "x": round(x, 2), "y": round(y, 2), "zoom": round(z, 5), "ease": "linear"}
             for k, (t, x, y, z) in enumerate(states) if k % step == 0 or k == len(states) - 1]
    last = states[min(len(states) - 1, int(round(dur * FPS)))]
    return {"keyframes": clean, "shake": [], "_end": {"x": last[1], "y": last[2], "z": last[3]}}


def _swaps(sc: dict, o: dict) -> None:
    dur = sc["duration"]
    D = o["swap_s"]
    for l in sc.get("layers", []):
        if l.get("name") not in SWAP_LAYERS and l.get("type") != "rect":
            continue
        s0, e0 = l.get("start"), l.get("end")
        if isinstance(s0, (int, float)) and 0.05 < s0 < dur - 0.05 and not l.get("enter"):
            l["enter"] = {"type": "fade", "at": round(s0, 3), "duration": D}
        if isinstance(e0, (int, float)) and 0.05 < e0 < dur - 0.05 and not l.get("exit"):
            l["end"] = round(min(dur, e0 + D), 3)
            l["exit"] = {"type": "fade", "at": round(e0, 3), "duration": D}


def apply(sb: dict, opts: dict | None = None) -> dict:
    o = {**DEFAULTS, **(opts or {})}
    cuts = set(int(c) for c in o["cuts"])
    if len(cuts) > 3:
        raise ValueError(f"story_camera: {len(cuts)} hard cuts listed; the story lane allows at most 3")
    sb = copy.deepcopy(sb)
    prev_end = None
    for si, sc in enumerate(sb["scenes"]):
        sc["camera"] = scene_camera(sc.get("camera"), sc["duration"], si, o, prev_end)
        prev_end = sc["camera"].pop("_end")
        bg = sc.get("background") or {}
        if bg.get("type") == "component" and str(bg.get("name", "")).startswith("stick/"):
            bg["depth"] = o["set_depth"]
            if o["set_blur"] > 0 and bg.get("name") == "stick/Set":
                ov = bg.get("overscan", o["overscan"])
                sc["layers"].insert(0, {"type": "component", "name": "stick/Set", "x": W / 2, "y": H / 2,
                                        "width": round(W * ov), "height": round(H * ov), "z": -50, "role": "dressing",
                                        "props": copy.deepcopy(bg.get("props") or {})})
                sc["background"] = {"type": "color", "color": "#2a2350", "depth": o["set_depth"], "overscan": ov}
        for l in sc.get("layers", []):
            if l.get("name") == "stick/Set":
                l["depth"] = o["set_depth"]
                if o["set_blur"] > 0:
                    l["blur"] = o["set_blur"]
        _swaps(sc, o)
        if si > 0:
            sc["transitionIn"] = {"type": "cut", "duration": 0} if si + 1 in cuts else \
                {"type": "fade", "duration": o["xfade_s"]}
    sb.setdefault("_built", {})["camera"] = "pipeline/episodes/story_camera.py (story lane grammar)"
    return sb


# ------------------------------------------------------------------------------------------------ offline estimate
def _ease(name: str, p: float) -> float:
    p = min(1.0, max(0.0, p))
    if name == "linear":
        return p
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2      # cubic inOut (core default)


def _cam_at(keys: list[dict], t: float) -> tuple[float, float, float]:
    prev = None
    for k in keys:
        if k["t"] <= t:
            prev = k
            continue
        if prev is None:
            return k["x"], k["y"], k["zoom"]
        p = _ease(k.get("ease", "inOut"), (t - prev["t"]) / (k["t"] - prev["t"]))
        return tuple(a + (b - a) * p for a, b in ((prev["x"], k["x"]), (prev["y"], k["y"]), (prev["zoom"], k["zoom"])))
    return prev["x"], prev["y"], prev["zoom"]


def speed_report(sb: dict, depth: float | None = None) -> dict:
    """per-frame speed of the set plane, camera_motion.py units (px/frame at 720 wide: |translation| + |zoom| * 734)"""
    sp = []
    for sc in sb["scenes"]:
        keys = [{**k, "x": _px(k["x"], W), "y": _px(k["y"], H)} for k in sc["camera"]["keyframes"]]
        d = depth if depth is not None else (sc.get("background") or {}).get("depth", 1.0)
        n = round(sc["duration"] * FPS)
        last = None
        for f in range(n):
            x, y, z = _cam_at(keys, f / FPS)
            cx, cy, ze = W / 2 + (x - W / 2) * d, H / 2 + (y - H / 2) * d, 1 + (z - 1) * d
            if last is not None:
                lx, ly, lz = last
                tr = math.hypot(cx - lx, cy - ly) * ze * 720 / W
                sp.append(tr + abs(ze / lz - 1) * 734)
            last = (cx, cy, ze)
    s = sorted(sp)
    q = lambda p: round(s[min(len(s) - 1, int(p * len(s)))], 2)
    return {"frames": len(sp), "moving_0_3": round(sum(v >= 0.3 for v in sp) / len(sp), 3),
            "ge_2": round(sum(v >= 2 for v in sp) / len(sp), 3), "p25": q(0.25), "p50": q(0.5), "p90": q(0.9)}
