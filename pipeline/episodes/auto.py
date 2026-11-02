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
    "pages": ["What would", "a sperm whale's click", ...],  # optional: the whole narration as caption pages, in order
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
Anchors resolve only under those time keys and time lists (F05). Anywhere else a string starting with "@" is
text (chat handles such as "@Mom", "@Admin who is member #41?") and is left alone.
Anchor grammar: ^@[\\w'*-]+(#\\d+)?(\\.end)?([+-][\\d.]+)?$ or the specials above; anything else is an error.

House style (explainers): every explainer storyboard built here goes through the Lantern & Ink pass
(pipeline/episodes/house.py, the live look) and then the staging/collision checker (pipeline/episodes/staging.py); a
staging violation is an ERROR (also with --check), an [echo] (headline nearly repeating the caption) a WARN. The pass
adds by itself: scene light + key sweep, the background rig and set dressing of each scene's setting (a board, or the
biome's own dressing under its waterline; pipeline/episodes/settings.py), the palette key ramp and a colour SHIFT where
the setting allows it, title plate / lantern tag info design, popSpring / dropSquash motion, camera pre-roll + drift,
cuts -> wipe/iris/fade. The shots vocabulary to steer it (all optional):
  scene      "setting": {...} or [{...}, {"at": "@word", ...}]   where the scene takes place (settings.py docstring:
                                          kind place|board|map|analogy, biome, place, depth, waterline, light, cue);
                                          inferred from the narration when absent. staging fails a build whose
                                          dressing / animals don't fit it, a setting held > 40 s, < 5 changes a minute
  top level  "house": {"pod": "orca"}      pass options: pod (far silhouettes in every set: "orca"), dressing, set,
                                          info, cuts, motion, auto_shift (true/false)
  scene      "_house": {...}               "shift": {"at": "@word", "to": "warm", "dur": 0.8}  the colour shift beat
                                          (default: the first scale beat: a You / ScaleBar / HeightChart / Stat layer)
                                          "key": "danger"   re-key this scene (colour script: threat beats)
                                          "set": false      no set (a diagram card); "fore": false  no foreground
                                          "proof": false    no warm lift on this proof beat
             "light": {"setup": "lantern|daylight|cold|stellar", "sweep": 8, ...}   (default lantern, sweep on >= 4 s)
  keys       royal, tide, mid, deep, kelp, dusk, sky, warm, danger, ink, polar (Ocean "key" / "shiftTo"; must fit the biome)
  layer      "shade": false | {"core", "hi", "rim", "marks", "cast", "glint", "lod"}  kit figures are shaded by default
                                          (inline svg is NOT shaded: it reads flat next to the house figures)
             "role": hero|prop|label|dressing|fx, "allowOverlap": true (contact beats: a bite, a hand on the fin)
             enter "popSpring" / "dropSquash" ("pop" / "drop" are upgraded to them)
  dressing   explainer/Kelp, FishSchool, Jellies, Rocks, Reef, Seabed, Ridge, Pod, Specks, Glow, LightEvent, Board,
             IceField, IceFloe, Coast (each only in its biome: settings.BIOMES): give each a
             distinct props.seed (two identical seeds draw identical kelp / fish: an ERROR)
  colours    house palette tokens (ink-0..4, tide-0..5, kelp-, dusk-, sky-, coral-, ochre-, amber-, bone-, signal-;
             studio/src/kits/explainer/house/palette.ts) or #hex; "red" stays the signal accent for one word per beat
  never      "look": "legacy" (the old flat style) in an operator episode: an ERROR

The new storyboard is written to storyboard.json.tmp, zod-validated, and only then moved over storyboard.json, so a
failed build always leaves the last good storyboard in place (F03). On the Spark (STUDIO_LOCAL=1, or
STUDIO_REQUIRE_ZOD=1, or a checkout at ~/studio/app) a missing zod/node is a failure, not a skip (F08).
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

TIME_KEYS = {"at", "t", "start", "end", "out", "until", "editAt", "connectedAt", "readAt", "seenAt", "from_t", "stampAt"}
TIME_LISTS = {"itemAt", "hits", "beats", "taps", "times", "talk"}
# keys that are a time in some components (Heartbeat/Flicker "from") and text in others (EndCard "from": "June (3B)",
# chat messages): an anchor there resolves only if it is well-formed, spoken, and not inside a dict with "text"
AMBIGUOUS_TIME_KEYS = {"from"}
ANCHOR = re.compile(r"^@(?P<body>.+?)(?P<off>[+-]\d+(?:\.\d+)?)?$")
WORD_ANCHOR = re.compile(r"^@[\w'*-]+(#\d+)?(\.end)?([+-][\d.]+)?$")
SPECIAL_ANCHOR = re.compile(r"^@:(start|end|first|last|\d+(\.\d+)?%)([+-][\d.]+)?$")
NICHE_DEFAULT_BG = {
    "explainer": {"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2,
                  "props": {"depth": 30, "rays": 7, "snow": 60}},
    "horror": {"type": "color", "color": "#0b0d12"},
}


class AnchorError(Exception):
    pass


def resolve_anchor(s: Scene, a: str) -> float:
    a = a.strip()
    if not (WORD_ANCHOR.match(a) or SPECIAL_ANCHOR.match(a)):
        raise AnchorError(f"bad anchor {a!r} (grammar: @word[#n][.end][+-s] or @:start|end|first|last|NN%)")
    m = ANCHOR.match(a)
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
        if not n.isdigit() or int(n) < 1:
            raise AnchorError(f"anchor {a!r}: '#{n}' is not a 1-based occurrence number")
        nth = int(n)
    try:
        return s.at(body, nth=nth - 1, end=end, off=off)
    except KeyError:
        words = " ".join(norm(w["text"]) for w in s.words)
        raise AnchorError(f"anchor {a!r}: word {body!r} #{nth} not spoken in paragraph {s.i + 1} ({words[:160]})")


def resolve(obj, s: Scene, errors: list, path: str, key: str | None = None, in_time_list: bool = False):
    """Recursively replace anchor strings with numbers. Errors on unresolved anchors under time keys."""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if k in AMBIGUOUS_TIME_KEYS and isinstance(v, str):
                out[k] = v
                if v.startswith("@") and "text" not in obj:
                    try:
                        out[k] = resolve_anchor(s, v)
                    except AnchorError:
                        pass
                continue
            out[k] = resolve(v, s, errors, f"{path}.{k}", k, k in TIME_LISTS)
        return out
    if isinstance(obj, list):
        return [resolve(v, s, errors, f"{path}[{i}]", key, in_time_list) for i, v in enumerate(obj)]
    timey = key in TIME_KEYS or in_time_list
    if timey and isinstance(obj, str) and obj.startswith("@") and len(obj) > 1:
        try:
            return resolve_anchor(s, obj)
        except AnchorError as e:
            errors.append(f"{path}: {e}")
            return obj
    if timey and isinstance(obj, str):
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


HOUSE_SCENE_KEYS = {"shift", "key", "set", "fore", "proof", "dressing"}
HOUSE_OPTS = {"pod", "dressing", "set", "info", "cuts", "motion", "auto_shift"}
DRESSING = {f"explainer/{n}" for n in
            "Kelp FishSchool Jellies Rocks Reef Seabed Ridge Pod Specks Glow LightEvent IceField Coast".split()}


def house_keys() -> set:
    """palette key ramps the Ocean background knows (studio/src/kits/explainer/house/oceanBg.tsx KEYS)"""
    try:
        src = open(os.path.join(ROOT, "studio", "src", "kits", "explainer", "house", "oceanBg.tsx"), encoding="utf-8").read()
    except OSError:
        return {"tide", "mid", "deep", "kelp", "dusk", "sky", "warm", "danger", "ink"}
    block = re.search(r"export const KEYS[^{]*\{(.*?)\n\};", src, re.S)
    keys = set(re.findall(r"^\s+(\w+):\s*\[", block.group(1), re.M)) if block else set()
    return keys | set(re.findall(r"^KEYS\.(\w+)\s*=", src, re.M))


def house_vocab(shots: dict, scenes: list[dict]) -> tuple[list[str], list[str]]:
    """the house-style shots vocabulary (module docstring): -> (errors, warnings)"""
    errs, warns = [], []
    keys = house_keys()
    for k in (shots.get("house") or {}):
        if k not in HOUSE_OPTS:
            errs.append(f"house.{k}: unknown house option (known: {', '.join(sorted(HOUSE_OPTS))})")
    seeds: dict = {}
    for i, s in enumerate(scenes):
        hs = s.get("_house") or {}
        if not isinstance(hs, dict):
            errs.append(f"scenes[{i}]._house must be an object")
            hs = {}
        for k in hs:
            if k not in HOUSE_SCENE_KEYS:
                errs.append(f"scenes[{i}]._house.{k}: unknown key (known: {', '.join(sorted(HOUSE_SCENE_KEYS))})")
        sh = hs.get("shift")
        if sh is not None and not (isinstance(sh, dict) and isinstance(sh.get("at"), (int, float))):
            errs.append(f"scenes[{i}]._house.shift needs an 'at' time (\"@word\")")
        for what, v in (("_house.key", hs.get("key")), ("_house.shift.to", (sh or {}).get("to") if isinstance(sh, dict) else None)):
            if v is not None and v not in keys:
                errs.append(f"scenes[{i}].{what} {v!r}: not a palette key ({', '.join(sorted(keys))})")
        bg = s.get("background") or {}
        bp = bg.get("props") or {}
        for k in ("key", "shiftTo"):
            if bp.get(k) is not None and bp[k] not in keys:
                errs.append(f"scenes[{i}].background.props.{k} {bp[k]!r}: not a palette key ({', '.join(sorted(keys))})")
        if bp.get("look") == "legacy":
            errs.append(f"scenes[{i}].background: look 'legacy' is the old flat style; operator episodes use the house look")
        for j, l in enumerate(s.get("layers", [])):
            where = f"scenes[{i}].layers[{j}]"
            p = l.get("props") or {}
            if p.get("look") == "legacy":
                errs.append(f"{where}: look 'legacy' is the old flat style; operator episodes use the house look")
            if l.get("shade") is False and l.get("name") in FIGURE_NAMES:
                warns.append(f"{where} {l.get('name')}: shade false draws the figure flat next to shaded ones")
            if l.get("name") in DRESSING:
                l.setdefault("role", "dressing")
                sk = (l["name"], str(p.get("seed")))
                if sk in seeds:
                    errs.append(f"{where} {l['name']} seed {p.get('seed')!r} repeats {seeds[sk]}: identical set dressing "
                                f"(give every dressing layer its own props.seed)")
                seeds.setdefault(sk, where)
            if l.get("type") == "svg" and l.get("role") not in ("dressing", "fx"):
                w, h = l.get("width") or 0, l.get("height") or 0
                if isinstance(w, (int, float)) and isinstance(h, (int, float)) and w * h * float(l.get("scale", 1) or 1) ** 2 > 0.08 * 1080 * 1920:
                    warns.append(f"{where}: a large inline svg is not house-shaded and reads flat; use a kit figure "
                                 f"(explainer/Creature species) or keep it small / a silhouette")
    return errs, warns


def house_pass(sb: dict, opts: dict | None) -> tuple[dict, list[str], list[str]]:
    """house look + caption-dup drop + staging check -> (storyboard, errors, warnings)"""
    from . import house, staging
    for sc in sb["scenes"]:
        for j, l in enumerate(sc.get("layers", [])):
            l["_src"] = j            # shots.json layer index, so staging messages point at the layer to fix
    sb = house.apply(sb, opts)
    sb["_built"]["style"] = "house (Lantern & Ink): pipeline/episodes/house.py"
    warnings = []
    dropped = drop_caption_dups(sb)
    if dropped:
        warnings.append(f"dropped {len(dropped)} on-screen label(s) that repeated the caption under them: {dropped}")
    msgs = staging.check(sb)
    by_id = {sc["id"]: (i, sc) for i, sc in enumerate(sb["scenes"])}

    def where(m: str) -> str:
        sid = m.split(" ", 1)[0]
        if sid not in by_id:
            return m
        i, sc = by_id[sid]

        def sub(x):
            k = int(x.group(2))
            ls = sc.get("layers", [])
            src = ls[k].get("_src") if k < len(ls) else None
            return f"{x.group(1)} (shots scenes[{i}].layers[{src}])" if src is not None else f"{x.group(1)} (house set)"
        return re.sub(r"([\w/]+)#(\d+)", sub, m)

    warnings += [f"staging: {where(m)}" for m in msgs if staging.is_warning(m)]
    errors = [f"staging: {where(m)}" for m in msgs if not staging.is_warning(m)]
    for sc in sb["scenes"]:
        for l in sc.get("layers", []):
            l.pop("_src", None)
    return sb, errors, warnings


FIGURE_NAMES = {f"explainer/{n}" for n in ("SpermWhale ColossalSquid Orca GreatWhite BlueWhale Anglerfish Octopus Crocodile "
                                           "Hippo Grizzly Diver You Bus Car Elephant GolfCart Sauropod Jet Seal Cookiecutter").split()}


def zod_required() -> bool:
    """True on the Spark: a missing zod must fail the build there instead of silently skipping (F08)."""
    if os.environ.get("STUDIO_REQUIRE_ZOD") == "0":
        return False
    if os.environ.get("STUDIO_REQUIRE_ZOD") == "1" or os.environ.get("STUDIO_LOCAL") == "1":
        return True
    return os.path.realpath(ROOT) == os.path.realpath(os.path.expanduser("~/studio/app"))


def zod_validate(path: str) -> tuple[bool, str]:
    """Run studio/src/cli/validate.ts when node + node_modules exist (the Spark). -> (ok, message)."""
    studio = os.path.join(ROOT, "studio")
    required = zod_required()
    if not os.path.isdir(os.path.join(studio, "node_modules", "zod")):
        if required:
            return False, "zod required here but studio/node_modules/zod is missing (npm ci running or failed?)"
        return True, "zod skipped (no studio/node_modules here)"
    node = os.environ.get("STUDIO_NODE") or shutil.which("node")
    if not node:
        cands = sorted(glob.glob(os.path.expanduser("~/.nvm/versions/node/v22*/bin/node")))
        node = cands[-1] if cands else None
    if not node:
        return (False, "zod required here but no node found") if required else (True, "zod skipped (no node)")
    r = subprocess.run([node, "--experimental-strip-types", "--no-warnings", "src/cli/validate.ts", path],
                       cwd=studio, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


# ------------------------------------------------------------------ build

def niche_module(niche: str):
    from . import explainer_eps, horror_eps
    return {"explainer": explainer_eps, "horror": horror_eps}[niche]


def drop_caption_dups(sb: dict) -> list[str]:
    """remove headlines / tags that say exactly what the caption under them says (regress_bwscale: a "BIGGER WINS"
    headline stacked over the caption "BIGGER WINS."); staging.py [dup] finds them"""
    import re as _re
    from . import staging
    hits = {}
    for m in staging.check(sb):
        x = _re.match(r"(\S+) \S+ \[dup\] label \S+#(\d+) ", m)
        if x:
            hits.setdefault(x.group(1), set()).add(int(x.group(2)))
    out = []
    for sc in sb["scenes"]:
        idx = hits.get(sc["id"])
        if idx:
            out += [f"{sc['id']}:{(sc['layers'][i].get('props') or {}).get('text')}" for i in sorted(idx)]
            sc["layers"] = [l for i, l in enumerate(sc["layers"]) if i not in idx]
    return out


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
    if niche == "explainer":
        e, w = house_vocab(shots, built)
        errors += e
        warnings += w
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
    if shots.get("pages"):   # hand-checked whole-phrase caption pages (like the hand builders' CAPTION_PAGES) win
        from .build import mark_pages
        try:
            mark_pages(words, shots["pages"], slug)
        except SystemExit as e:
            errors.append(f"pages: {e}")
    variant = _read_json(os.path.join(ep, "variant.json")) or {}
    limit = float((variant.get("values") or {}).get("visual.max_hold_s") or 3.0)
    holds = check_holds(slug, built, limit) if limit != 3.0 else check_holds(slug, built)
    if holds:
        warnings.append(f"visual holds over {limit:g} s (add a layer/keyframe/camera key in that window): " + "; ".join(holds))
    if errors:
        return errors, warnings
    paging = dict(getattr(mod, "CAPTION_PAGING", None) or {})
    if shots.get("glue") and niche != "explainer":
        paging["glue"] = shots["glue"]
    sb = storyboard(slug, meta, built, words, total, mod.CAPTIONS, mod.OVERLAYS, source, paging)
    sb["_built"]["by"] = "pipeline/episodes/auto.py (shots.json)"
    if niche == "explainer":
        # the live look (Lantern & Ink) + the staging/collision checker; --check runs it too, so collisions surface
        # while shots.json is being written
        sb, e, w = house_pass(sb, shots.get("house"))
        errors += e
        warnings += w
        if shots.get("story_camera") is not None:   # story lane: glide, never stop (pipeline/episodes/story_camera.py)
            from .story_camera import apply as story_camera
            sb = story_camera(sb, shots["story_camera"])
    else:
        for s in sb["scenes"]:
            s.pop("_house", None)
    if errors or check_only:
        return errors, warnings
    path = os.path.join(ep, "storyboard.json")
    tmp = path + ".tmp"  # validate first, replace only on PASS (F03): a failed build keeps the last good file
    with open(tmp, "w") as f:
        json.dump(sb, f, indent=1, ensure_ascii=False)
    dur = sum(s["duration"] for s in built)
    if zod:
        ok, msg = zod_validate(tmp)
        print(msg)
        if not ok:
            errors.append("zod schema: " + msg)
            print(f"{slug}: storyboard NOT written (zod failed); the previous storyboard.json is unchanged, "
                  f"the rejected build is {os.path.relpath(tmp, ROOT)}")
            return errors, warnings
    os.replace(tmp, path)
    print(f"{slug}: {len(built)} scenes, {dur:.1f}s, {len(words)} words, timing={source.split()[0]} -> "
          f"{os.path.relpath(path, ROOT)}")
    bm = beatmap(slug, sb, specs, meta, _read_json(os.path.join(ep, "source.json")))
    bpath = os.path.join(ep, "beatmap.json")
    with open(bpath + ".tmp", "w") as f:
        json.dump(bm, f, indent=1, ensure_ascii=False)
    os.replace(bpath + ".tmp", bpath)
    print(f"{slug}: beatmap.json ({len(bm['scenes'])} scenes, beats from {bm['beats_from']})")
    return errors, warnings


def _read_json(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def caption_pages(words: list[dict], linger: float = 0.3) -> list[dict]:
    """Caption pages as the explainer pager marks them (word "br" = first word of a page; else one page per word run)."""
    pages, cur = [], []
    for w in words:
        if (w.get("br") and cur) or (cur and w["start"] - cur[-1]["end"] > 0.45):
            pages.append(cur)
            cur = []
        cur.append(w)
    if cur:
        pages.append(cur)
    out = []
    for k, p in enumerate(pages):
        t1 = pages[k + 1][0]["start"] if k + 1 < len(pages) else p[-1]["end"] + linger
        out.append({"t0": round(p[0]["start"], 3), "t1": round(min(t1, p[-1]["end"] + linger), 3),
                    "text": " ".join(w["text"] for w in p)})
    return out


def beatmap(slug: str, sb: dict, specs: list[dict], meta: dict, source: dict | None) -> dict:
    """episodes/<slug>/beatmap.json: one row per scene (time range, beat, skeleton/source beat, narration, components,
    longest hold, caption pages), the bridge from script and shots to video time and retention curves.
    Times use frame-accurate cumulative rounding (start_i = round(cum_i * fps) / fps, F20)."""
    from .common import visual_events
    fps = sb.get("fps", 30)
    scenes = sb["scenes"]
    total = sum(s["duration"] for s in scenes)
    skel = (source or {}).get("skeleton") or []
    plan = [int(x) for x in re.findall(r"\d+", str(meta.get("beat_plan", "")))]
    beats_from = "beat_plan" if skel and len(plan) == len(scenes) and all(0 <= x < len(skel) for x in plan) else (
        "timing" if skel else "shots")
    pages = caption_pages(sb.get("captions", {}).get("words", []))
    rows, cum = [], 0.0
    for i, s in enumerate(scenes):
        t0 = round(cum * fps) / fps
        cum += s["duration"]
        t1 = round(cum * fps) / fps
        if beats_from == "beat_plan":
            k = plan[i]
        elif skel:
            mid = 100 * (t0 + t1) / 2 / max(total, 1e-6)
            k = next((e["i"] for e in skel if e["target_pct0"] <= mid < e["target_pct1"]), skel[-1]["i"])
        else:
            k = None
        sk = skel[k] if k is not None and k < len(skel) else None
        spec_beat = (specs[i] if i < len(specs) else {}).get("beat")
        comps = []
        for l in s.get("layers", []):
            if l.get("type") == "component" and l.get("name") not in comps:
                comps.append(l["name"])
        ev = visual_events(s)
        hold = max((b - a for a, b in zip(ev, ev[1:])), default=s["duration"])
        bg = s.get("background") or {}
        rows.append({"scene_id": s.get("id", f"p{i + 1:02d}"), "p": i + 1, "t0": round(t0, 3), "t1": round(t1, 3),
                     "beat": (sk or {}).get("label") or (str(spec_beat).upper() if spec_beat else None),
                     "shots_beat": spec_beat, "skeleton_i": k, "playbook": (sk or {}).get("playbook"),
                     "source_beat_i": (sk or {}).get("from_beats", []), "text": s.get("notes", ""),
                     "components": comps, "background": bg.get("name") or bg.get("type"),
                     "max_hold_s": round(hold, 2),
                     "caption_pages": [p for p in pages if t0 <= p["t0"] < t1]})
    return {"v": 1, "slug": slug, "duration_s": round(round(total * fps) / fps, 3), "fps": fps,
            "source_id": (source or {}).get("source_id"), "beats_from": beats_from, "scenes": rows}


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
