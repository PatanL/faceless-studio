#!/usr/bin/env python3
"""Generic storyboard builder: episodes/<slug>/shots.json (word-anchored scene specs) -> storyboard.json.

No per-episode Python or TSX. A shots file is written by `studio-make` (claude -p with
pipeline/prompts/shots_<niche>.md) or by hand, and this module turns it into a B2 storyboard using the same
contract as the hand builders (pipeline/episodes/common.py): one narration paragraph = one scene, scene i starts
just before the first word of paragraph i (Kokoro timings from audio/captions.json, else a wpm estimate).

usage: python3 -m pipeline.episodes.auto <slug> [--check] [--no-zod]
  --check   resolve + check only, do not write storyboard.json (exit 1 on errors)
  --no-zod  skip the zod schema check (needs node + studio/node_modules, i.e. the Spark)

shots.json
  {
    "niche": "explainer" | "horror",
    "emphasis": ["circles", ["forget", 2]],      # optional red caption words (content words; [word, nth] 1-based)
    "glue": ["great whites", "blue whale"],      # optional phrases a caption card never splits
    "scenes": [                                   # exactly one per narration paragraph, in order
      {"p": 1, "beat": "hook",                    # p and beat are informational
       "background": {...},                       # optional; niche default (explainer: Ocean depth 30)
       "layers": [...], "camera": {...}, "transitionIn": {...}, "grade": {...}, "callouts": [...]}
    ]
  }

Time anchors. Anywhere a time is expected (at, t, start, end, out, until, editAt, connectedAt, and the items of
itemAt / hits / beats / taps lists), a string anchor may replace the number; it resolves to scene-local seconds:
  "@bus"          start of the first spoken word "bus" in this scene's paragraph (case/punctuation-insensitive)
  "@bus#2"        start of the 2nd "bus" (1-based)
  "@bus.end"      end of that word          "@fif*"   prefix match ("fifty-six" -> "@fifty-six" also works)
  "@bus+0.3"      offset in seconds (also -0.2), combinable: "@bus#2.end-0.1"
  "@:start" 0     "@:end" scene duration    "@:first" first word    "@:last" end of the last word
  "@:40%"         a fraction of the scene duration
Anchors on non-time keys are resolved too when they match a spoken word, and otherwise left as text.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys

from .common import ROOT, Scene, load, norm, storyboard

TIME_KEYS = {"at", "t", "start", "end", "out", "until", "editAt", "connectedAt", "readAt", "seenAt", "from_t"}
TIME_LISTS = {"itemAt", "hits", "beats", "taps", "times"}
ANCHOR = re.compile(r"^@(?P<body>.+?)(?P<off>[+-]\d+(?:\.\d+)?)?$")
NICHE_DEFAULT_BG = {
    "explainer": {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2,
                  "props": {"depth": 30, "rays": 7, "snow": 60}},
    "horror": {"type": "color", "color": "#0b0d12"},
}


class AnchorError(Exception):
    pass


def resolve_anchor(s: Scene, a: str) -> float:
    m = ANCHOR.match(a.strip())
    if not m:
        raise AnchorError(f"bad anchor {a!r}")
    body, off = m.group("body"), float(m.group("off") or 0)
    if body.startswith(":"):
        k = body[1:]
        if k == "start":
            t = 0.0
        elif k == "end":
            t = s.dur
        elif k == "first":
            t = s.first()
        elif k == "last":
            t = s.last()
        elif k.endswith("%"):
            t = s.dur * float(k[:-1]) / 100
        else:
            raise AnchorError(f"unknown special anchor {a!r}")
        return round(max(-1.0, min(s.dur, t + off)), 3)
    end = body.endswith(".end")
    if end:
        body = body[:-4]
    nth = 1
    if "#" in body:
        body, n = body.rsplit("#", 1)
        nth = int(n)
    try:
        return s.at(body, nth=nth - 1, end=end, off=off)
    except KeyError:
        words = " ".join(norm(w["text"]) for w in s.words)
        raise AnchorError(f"anchor {a!r}: word {body!r} #{nth} not spoken in paragraph {s.i + 1} ({words[:160]})")


def resolve(obj, s: Scene, errors: list, path: str, key: str | None = None, in_time_list: bool = False):
    """Recursively replace anchor strings with numbers. Errors on unresolved anchors under time keys."""
    if isinstance(obj, dict):
        return {k: resolve(v, s, errors, f"{path}.{k}", k, k in TIME_LISTS) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve(v, s, errors, f"{path}[{i}]", key, in_time_list) for i, v in enumerate(obj)]
    if isinstance(obj, str) and obj.startswith("@") and len(obj) > 1:
        timey = key in TIME_KEYS or in_time_list
        try:
            return resolve_anchor(s, obj)
        except AnchorError as e:
            if timey:
                errors.append(f"{path}: {e}")
            return obj
    if (key in TIME_KEYS or in_time_list) and isinstance(obj, str):
        errors.append(f"{path}: time value {obj!r} is not a number or an @anchor")
    return obj


# ------------------------------------------------------------------ kit checks

def kit_components() -> tuple[set, set]:
    """-> (registered component names, explainer figure species/keys) by scanning studio/src/kits."""
    names, species = set(), set()
    for f in glob.glob(os.path.join(ROOT, "studio", "src", "kits", "**", "*.tsx"), recursive=True):
        src = open(f, encoding="utf-8").read()
        names |= set(re.findall(r"registerComponent\(\s*['\"]([^'\"]+)['\"]", src))
        if f.endswith(os.path.join("explainer", "index.tsx")):
            block = re.search(r"const FIXED[^{]*\{(.*?)\n\};", src, re.S)
            if block:
                for nm, sp in re.findall(r"(\w+):\s*'(\w+)'", block.group(1)):
                    names.add(f"explainer/{nm}")
                    species.add(sp)
        if "/explainer/" in f.replace(os.sep, "/"):
            # figure dictionaries: `export const MARINE = {spermWhale, ...}` and `name: {` figure entries
            for blk in re.findall(r"export const [A-Z_]+(?:: Record<string, Figure>)? = \{(.*?)\};", src, re.S):
                species |= set(re.findall(r"\b([a-z][A-Za-z0-9]+)\b(?=\s*[,:}\n])", blk))
    return names, species


def check_components(scenes: list[dict], names: set, species: set) -> list[str]:
    errs = []

    def walk(o, path):
        if isinstance(o, dict):
            if o.get("type") == "component":
                n = o.get("name")
                if n not in names:
                    errs.append(f"{path}: unknown component {n!r} (renders a magenta 'missing' box)")
                if n == "explainer/Creature":
                    sp = (o.get("props") or {}).get("species")
                    key = lambda x: re.sub(r"[^a-z0-9]", "", str(x).lower())
                    if sp and key(sp) not in {key(x) for x in species}:
                        errs.append(f"{path}: unknown species {sp!r}; known: {', '.join(sorted(species))}")
            for k, v in o.items():
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")

    for i, s in enumerate(scenes):
        walk(s.get("background"), f"scenes[{i}].background")
        walk(s.get("layers"), f"scenes[{i}].layers")
    return errs


def layout_warnings(scenes: list[dict], fmt: str = "9:16") -> list[str]:
    """Text-like layers in the 9:16 platform UI zone (y > 77 %) or off screen."""
    out = []
    if fmt != "9:16":
        return out
    for i, s in enumerate(scenes):
        for j, l in enumerate(s.get("layers", [])):
            y = l.get("y")
            if isinstance(y, str) and y.endswith("%"):
                y = float(y[:-1]) / 100 * 1920
            if not isinstance(y, (int, float)):
                continue
            nm = l.get("name", l.get("type"))
            if nm in ("explainer/Headline", "explainer/Tag", "explainer/Stat", "text", "explainer/Options") and y > 0.77 * 1920:
                out.append(f"scenes[{i}].layers[{j}] {nm} at y={y:.0f}px sits under the platform UI (keep text above 77 %)")
            if y < -200 or y > 2120:
                out.append(f"scenes[{i}].layers[{j}] {nm} is off screen (y={y:.0f})")
        # scale partners: two or more figures in one scene should share pxPerM (honest "you vs. X" comparison)
        figs = [(l.get("name"), (l.get("props") or {}).get("pxPerM")) for l in s.get("layers", [])
                if l.get("type") == "component" and l.get("name") in FIGURE_NAMES]
        if len(figs) >= 2 and len({p for _, p in figs}) > 1:
            out.append(f"scenes[{i}]: figures {', '.join(f'{n}(pxPerM={p})' for n, p in figs)} do not share one pxPerM, "
                       f"so their sizes are not comparable (give every figure the same pxPerM, or drop the comparison)")
    return out


FIGURE_NAMES = {f"explainer/{n}" for n in ("SpermWhale ColossalSquid Orca GreatWhite BlueWhale Anglerfish Octopus Crocodile "
                                           "Hippo Grizzly Diver You Bus Car Elephant GolfCart Sauropod Jet Seal").split()}


def zod_validate(path: str) -> tuple[bool, str]:
    """Run studio/src/cli/validate.ts when node + node_modules exist (the Spark). -> (ok, message)."""
    studio = os.path.join(ROOT, "studio")
    if not os.path.isdir(os.path.join(studio, "node_modules", "zod")):
        return True, "zod skipped (no studio/node_modules here)"
    node = os.environ.get("STUDIO_NODE") or shutil.which("node")
    if not node:
        cands = sorted(glob.glob(os.path.expanduser("~/.nvm/versions/node/v22*/bin/node")))
        node = cands[-1] if cands else None
    if not node:
        return True, "zod skipped (no node)"
    r = subprocess.run([node, "--experimental-strip-types", "--no-warnings", "src/cli/validate.ts", path],
                       cwd=studio, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


# ------------------------------------------------------------------ build

def niche_module(niche: str):
    from . import explainer_eps, horror_eps
    return {"explainer": explainer_eps, "horror": horror_eps}[niche]


def build(slug: str, check_only: bool = False, zod: bool = True) -> tuple[list, list]:
    """-> (errors, warnings). Writes episodes/<slug>/storyboard.json unless check_only or errors."""
    from .build import STOPWORDS, auto_emphasis, check_holds, mark_emphasis
    ep = os.path.join(ROOT, "episodes", slug)
    shots_path = os.path.join(ep, "shots.json")
    try:
        shots = json.load(open(shots_path, encoding="utf-8"))
    except FileNotFoundError:
        return [f"{shots_path} missing"], []
    except json.JSONDecodeError as e:
        return [f"shots.json is not valid JSON: {e}"], []
    meta, scenes, words, total, source = load(slug)
    niche = shots.get("niche") or meta.get("niche") or "explainer"
    niche = "horror" if "horror" in niche else "explainer"
    mod = niche_module(niche)
    errors, warnings = [], []
    specs = shots.get("scenes") or []
    if len(specs) != len(scenes):
        errors.append(f"shots.json has {len(specs)} scenes but the narration has {len(scenes)} paragraphs "
                      f"(one scene per paragraph, in order)")
    built = []
    for i, (sc, spec) in enumerate(zip(scenes, specs)):
        spec = dict(spec)
        for k in ("p", "beat", "id", "duration", "notes"):
            spec.pop(k, None)
        spec = resolve(spec, sc, errors, f"scenes[{i}]")
        out = {"id": f"p{i + 1:02d}", "duration": sc.dur,
               "background": spec.pop("background", None) or NICHE_DEFAULT_BG[niche],
               "layers": spec.pop("layers", []), "notes": sc.text}
        out.update(spec)
        built.append(out)
    names, species = kit_components()
    errors += check_components(built, names, species)
    warnings += layout_warnings(built)
    # captions: emphasis (explicit list, else the niche's auto rule) + phrase-boundary pages
    for w in words:
        w.pop("emph", None)
        w.pop("br", None)
    emph = shots.get("emphasis")
    if emph:
        try:
            mark_emphasis(words, [(e[0], max(0, int(e[1]) - 1)) if isinstance(e, list) else e for e in emph])
        except SystemExit as e:
            errors.append(f"emphasis: {e}")
    elif getattr(mod, "EMPH_AUTO", None):
        auto_emphasis(words, mod.EMPH_AUTO)
    stray = [w["text"] for w in words if w.get("emph") and norm(w["text"]) in STOPWORDS]
    if stray:
        errors.append(f"emphasis on stopwords {stray}: red is for content words only")
    if niche == "explainer":
        from .phrases import phrase_pages
        phrase_pages(words, glue=shots.get("glue", []))
    holds = check_holds(slug, built)
    if holds:
        warnings.append("visual holds over 3 s (add a layer/keyframe/camera key in that window): " + "; ".join(holds))
    if errors or check_only:
        return errors, warnings
    paging = dict(getattr(mod, "CAPTION_PAGING", None) or {})
    if shots.get("glue") and niche != "explainer":
        paging["glue"] = shots["glue"]
    sb = storyboard(slug, meta, built, words, total, mod.CAPTIONS, mod.OVERLAYS, source, paging)
    sb["_built"]["by"] = "pipeline/episodes/auto.py (shots.json)"
    path = os.path.join(ep, "storyboard.json")
    with open(path, "w") as f:
        json.dump(sb, f, indent=1, ensure_ascii=False)
    dur = sum(s["duration"] for s in built)
    print(f"{slug}: {len(built)} scenes, {dur:.1f}s, {len(words)} words, timing={source.split()[0]} -> "
          f"{os.path.relpath(path, ROOT)}")
    if zod:
        ok, msg = zod_validate(path)
        print(msg)
        if not ok:
            errors.append("zod schema: " + msg)
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--no-zod", action="store_true")
    a = ap.parse_args()
    errors, warnings = build(a.slug, check_only=a.check, zod=not a.no_zod)
    for w in warnings:
        print("WARN", w)
    for e in errors:
        print("ERROR", e)
    print("PASS" if not errors else f"FAIL ({len(errors)} errors)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
