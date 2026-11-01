"""Shared helpers for episode storyboard builders (lane S1).

Contract (see pipeline/templates/*.md): one narration paragraph = one scene. Scene i starts just before the
first word of paragraph i, using real word timings from episodes/<slug>/audio/captions.json (written by
pipeline.audio.make --meta-out) or, before TTS has run, a words-per-minute estimate. Layers inside a scene
are anchored to words with Scene.at("word").
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
from pipeline.audio.script import parse  # noqa: E402

LEAD = 0.15          # cut this many seconds before the paragraph's first word
TAIL = 1.2           # seconds after the last word when no mix duration is known
EST_WPM = {"explainer": 205, "horror": 230}
EST_PAUSE = {"explainer": 0.38, "horror": 0.55}


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


class Scene:
    def __init__(self, idx, start, dur, words, text):
        self.i, self.start, self.dur, self.words, self.text = idx, start, dur, words, text

    def at(self, token: str, nth: int = 0, end: bool = False, off: float = 0.0) -> float:
        """Scene-local time of the nth word matching token ('word' exact, 'wor*' prefix)."""
        tok = norm(token.rstrip("*"))
        prefix = token.endswith("*")
        hits = [w for w in self.words if (norm(w["text"]).startswith(tok) if prefix else norm(w["text"]) == tok)]
        if len(hits) <= nth:
            raise KeyError(f"scene {self.i}: no word {token!r} (#{nth}) in: {self.text[:80]}")
        w = hits[nth]
        t = (w["end"] if end else w["start"]) - self.start + off
        return round(max(0.0, min(self.dur - 0.05, t)), 3)

    def first(self) -> float:
        return round(self.words[0]["start"] - self.start, 3) if self.words else 0.0

    def last(self) -> float:
        return round(self.words[-1]["end"] - self.start, 3) if self.words else self.dur

    def frac(self, f: float) -> float:
        return round(self.dur * f, 3)


def load(slug: str):
    """-> meta, scenes[list[Scene]], words (global), total_dur, timing_source"""
    ep = os.path.join(ROOT, "episodes", slug)
    src = open(os.path.join(ep, "script.md"), encoding="utf-8").read()
    sc = parse(src)
    meta = sc.meta
    niche = meta.get("niche", "explainer")
    paras = [seg.words for seg in sc.segments]
    cap_path = os.path.join(ep, "audio", "captions.json")
    rep_path = os.path.join(ep, "audio", "report.json")
    total = None
    if os.path.exists(cap_path):
        words = json.load(open(cap_path))["words"]
        source = "kokoro captions.json"
        if os.path.exists(rep_path):
            total = json.load(open(rep_path))["mix"]["duration_s"]
    else:
        words, t = [], 0.4
        spw = 60.0 / EST_WPM[niche]
        for p in paras:
            for w in p:
                d = spw * (0.55 + 0.09 * len(w))
                words.append({"text": w, "start": round(t, 3), "end": round(t + d * 0.9, 3)})
                t += d
            t += EST_PAUSE[niche]
        source = f"estimate {EST_WPM[niche]} wpm (run pipeline.audio.make for real timings)"
    n_script = sum(len(p) for p in paras)
    if len(words) != n_script:
        raise SystemExit(f"{slug}: captions have {len(words)} words, script has {n_script}; rerun TTS")
    if total is None:
        total = words[-1]["end"] + TAIL
    # split global words into paragraphs
    groups, k = [], 0
    for p in paras:
        groups.append(words[k:k + len(p)])
        k += len(p)
    starts = [0.0]
    for g in groups[1:]:
        starts.append(round(max(starts[-1] + 0.6, g[0]["start"] - LEAD), 3))
    ends = starts[1:] + [round(total, 3)]
    scenes = [Scene(i, s, round(e - s, 3), g, " ".join(paras[i])) for i, (s, e, g) in enumerate(zip(starts, ends, groups))]
    return meta, scenes, words, total, source


def visual_events(scene: dict) -> list[float]:
    """Scene-local times where the picture changes (besides idle motion and captions)."""
    ev = [0.0, scene["duration"]]
    for l in scene.get("layers", []):
        for k in ("start", "end"):
            if isinstance(l.get(k), (int, float)):
                ev.append(l[k])
        for k in ("enter", "exit"):
            if isinstance(l.get(k), dict) and isinstance(l[k].get("at"), (int, float)):
                ev.append(l[k]["at"])
        ev += [k["t"] for k in l.get("keyframes", []) if isinstance(k.get("t"), (int, float))]
        p = l.get("props") or {}
        for k in ("at", "out"):
            if isinstance(p.get(k), (int, float)) and p[k] > 0:
                ev.append(p[k])
        for v in p.values():  # value tracks ([{t, v}]) and nested side props with "at"
            if isinstance(v, list):
                ev += [k["t"] for k in v if isinstance(k, dict) and isinstance(k.get("t"), (int, float))]
                ev += [k for k in v if isinstance(k, (int, float)) and k > 0] if p.get("beats") is v else []
            if isinstance(v, dict) and isinstance(v.get("at"), (int, float)):
                ev.append(v["at"])
        ev += _nested_cues(p)  # cue lists ({at}) and nested phone chats: bubbles, typing, banners, vibrate, glitches
    cam = scene.get("camera") or {}
    ev += [k["t"] for k in cam.get("keyframes", [])]
    ev += [s["at"] for s in cam.get("shake", [])]
    return sorted(t for t in ev if 0 <= t <= scene["duration"])


def _nested_cues(obj) -> list[float]:
    """Every positive at/editAt/connectedAt inside a nested props object (a phone's chat, banners, vibrate...)."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("at", "editAt", "connectedAt") and isinstance(v, (int, float)) and v > 0:
                out.append(v)
            elif isinstance(v, (dict, list)):
                out += _nested_cues(v)
    elif isinstance(obj, list):
        for v in obj:
            out += _nested_cues(v)
    return out


# ------------------------------------------------------------------ generic layer helpers

def comp(name, x, y, w, h, props=None, **kw):
    layer = {"type": "component", "name": name, "x": x, "y": y, "width": w, "height": h, "props": props or {}}
    layer.update(kw)
    return layer


def ov(name, z=50, **props):
    """Full-frame overlay component (fixed to screen)."""
    return {"type": "component", "name": name, "depth": 0, "z": z, "props": props}


def svg(markup, x, y, w, h, **kw):
    layer = {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h}
    layer.update(kw)
    return layer


def text(t, x, y, size=64, **kw):
    layer = {"type": "text", "text": t, "x": x, "y": y, "fontSize": size}
    layer.update(kw)
    return layer


def pop(at, d=0.35):
    return {"type": "pop", "at": at, "duration": d}


def fade(at, d=0.4):
    return {"type": "fade", "at": at, "duration": d}


def storyboard(slug, meta, scenes, words, total, captions_style, overlays, notes_source):
    return {
        "version": 1,
        "id": slug,
        "title": meta.get("title", slug),
        "format": "9:16",
        "fps": 30,
        "scenes": scenes,
        "captions": {"words": [{"text": w["text"], "start": w["start"], "end": w["end"], **({"emph": True} if w.get("emph") else {})}
                               for w in words],
                     "maxWords": 3, "maxChars": 16, "style": captions_style},
        "audio": {"voice": [{"src": f"episodes/{slug}/mix.wav", "start": 0, "volume": 1, "duration": round(total, 3)}],
                  "music": [], "sfx": [], "duckOn": "none"},
        "overlays": overlays,
        "_built": {"by": "pipeline/episodes/build.py", "timing": notes_source,
                   "audio": f"studio/public/episodes/{slug}/mix.wav (Spark; rebuild with pipeline.audio.make)"},
    }
