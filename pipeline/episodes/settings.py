"""Per-scene settings for explainer storyboards: where each moment of the video takes place.

Research: research/frame-analysis/REFERENCES_ANALYSIS.md §4 (rules 1-15) and ORCA_V2_AUDIT.md. The references change
setting 5-8x a minute, show a real place only when the narration names it, put abstract facts on a plain board, dress
each place from its own biome list and keep every animal inside its habitat.

A scene's `setting` is one segment or a list of segments (in-scene changes, e.g. a map card that gives way to the
place it names):

  "setting": {"kind": "place", "biome": "polar_ice", "place": "Antarctic Peninsula", "depth": 3, "waterline": 0.33,
              "light": "overcast", "cue": "Antarctica"}
  "setting": [{"at": 0, "kind": "map", "place": "South Africa", "cue": "South Africa"},
              {"at": "@the", "kind": "place", "biome": "kelp_forest", "place": "Gansbaai, South Africa", ...}]

  kind       place (a real place) | board (abstract facts, numbers, comparisons, questions) | analogy ("like a ...") |
             map (a map card names the place)
  biome      BIOMES below (place / analogy); board and map imply biome "board" / "map"
  place      free text, the caption-able name ("open ocean" when the narration names no place)
  depth      metres below the surface of what the camera sees (brightness follows it, rule 6)
  waterline  screen y (0..1) of the water surface, or None when no surface is in view
  light      day | overcast | dusk | night (time of day / light; sky colour, rays, caustics follow it)
  cue        the narration word that motivates the setting (named place / implied place); the segment may start at
             most CUE_EARLY s before that word is spoken (nothing appears before the narration names it)
  at         scene-local start (seconds, or "@word" / "@word#2" / "@word+0.3" resolved against the scene's words)
  board      board field colour (navy | blue | cyan | violet | ink | dusk | kelp | amber | coral | sky); default by fill();
             boards also take surface (0..1 y of a water-surface band), rays, lanes (swim-lane ropes), floor
  key        preferred Ocean key ramp for a place (must be one of the biome's keys)
  coast      {"kind": "cliffs" | "hills" | "rock", "lighthouse": bool} a coastline on the horizon (needs a waterline)

`fill(sb)` runs in build.py / auto.py before the house pass: it resolves "@word" anchors and fills every scene that
declares no setting from its narration (gazetteer: a named place -> that place; numbers, comparisons and questions ->
a board; otherwise the episode default, the hero's habitat). house.py dresses each segment from BIOMES; staging.py
(check_settings) fails a build whose dressing or creatures don't fit the declared setting, whose setting holds longer
than MAX_HOLD, or which changes setting less than MIN_PER_MIN times a minute.
"""
from __future__ import annotations

import re

KINDS = ("place", "board", "analogy", "map")
LIGHTS = ("day", "overcast", "dusk", "night")
MAX_HOLD = 40.0          # s: longest run of one setting (refs: max 34-41.5 s)
MIN_PER_MIN = 5.0        # setting changes per minute (refs: 4.8 / 6.3 / 7.6)
MIN_EPISODE_S = 30.0     # the variety rule needs at least this much runtime
CUE_EARLY = 2.5          # s: a named setting may start at most this long before its cue word
CUE_LATE = 1.5           # s: ... and must start at most this long after it

# ------------------------------------------------------------------ biomes
# water: underwater picture; floor: a seabed may be in view; depth: allowed metres; keys: Ocean key ramps that fit
# (brightness follows depth: rule 6); dressing: kit components allowed as set dressing (rule 10); ambient: background
# species native to the place (small, low contrast, far plane).
BIOMES: dict[str, dict] = {
    "tropical_reef": {"water": True, "floor": True, "depth": (0, 50), "keys": ("tide", "sky", "warm"),
                      "dressing": {"Reef", "Rocks", "Seabed", "FishSchool", "Jellies", "Specks", "Ridge"},
                      "ambient": {"reefFish", "jelly"}, "lights": ("day", "overcast", "dusk")},
    "kelp_forest": {"water": True, "floor": True, "depth": (0, 40), "keys": ("kelp", "mid", "tide"),
                    "dressing": {"Kelp", "Rocks", "Seabed", "FishSchool", "Specks", "Ridge", "Coast"},
                    "ambient": {"kelpFish"}, "lights": ("day", "overcast", "dusk")},
    "open_ocean": {"water": True, "floor": False, "depth": (0, 200), "keys": ("royal", "tide", "mid", "sky", "warm"),
                   "dressing": {"FishSchool", "Specks", "Pod", "Coast"}, "ambient": {"baitFish", "orca"},
                   "lights": LIGHTS},
    "polar_ice": {"water": True, "floor": False, "depth": (0, 200), "keys": ("polar",),
                  "dressing": {"IceField", "Specks"}, "ambient": {"krill"}, "lights": ("day", "overcast", "dusk", "night")},
    "coastal_surface": {"water": True, "floor": False, "depth": (0, 60), "keys": ("tide", "mid", "sky"),
                        "dressing": {"Coast", "FishSchool", "Specks"}, "ambient": {"baitFish"}, "lights": LIGHTS},
    "twilight": {"water": True, "floor": False, "depth": (200, 1000), "keys": ("dusk", "deep"),
                 "dressing": {"FishSchool", "Specks", "Jellies"}, "ambient": {"lanternfish", "jelly"},
                 "lights": ("night",)},
    "deep": {"water": True, "floor": True, "depth": (1000, 11000), "keys": ("deep", "ink"),
             "dressing": {"Specks", "Seabed", "Rocks"}, "ambient": set(), "lights": ("night",)},
    "board": {"water": False, "floor": False, "depth": (0, 0), "keys": (), "dressing": set(), "ambient": set(),
              "lights": LIGHTS},
    "map": {"water": False, "floor": False, "depth": (0, 0), "keys": (), "dressing": set(), "ambient": set(),
            "lights": LIGHTS},
}
# water boards (blue, navy) are the owner's pick for the orca look (experiments/asset-gen/gen/orca_set_01/02/07)
BOARD_FIELDS = ("navy", "blue", "cyan", "violet", "ink", "dusk", "kelp", "amber", "coral", "sky")

# where a dressing component may sit relative to the waterline: water (fully under it), floor (under it, a seabed
# biome), surface (straddles it, locked to the background plane), sky (above it), any (boards: full frame)
DRESSING_PLACE = {"Reef": "floor", "Rocks": "floor", "Seabed": "floor", "Ridge": "floor", "Kelp": "floor",
                  "FishSchool": "water", "Jellies": "water", "Pod": "water", "Specks": "water",
                  "IceField": "surface", "Coast": "surface", "Board": "any", "Glow": "any", "LightEvent": "any"}
# ambient tints for the FishSchool dressing per biome (a school is drawn as the biome's native fish)
SCHOOL_TINTS = {"tropical_reef": ["sky-2", "tide-3", "sky-3", "amber-3"], "kelp_forest": ["bone-0", "sky-3", "ochre-3"],
                "open_ocean": ["bone-1", "sky-3", "dusk-3"], "coastal_surface": ["bone-1", "sky-3", "dusk-3"],
                "twilight": ["dusk-3", "tide-4"]}

# ------------------------------------------------------------------ habitats (rule 11)
# species (staging.species_of names) -> biomes + depth range (m). Boards, maps and analogies take any species (the
# compared items). Sources: NOAA species profiles; the facts tables in episodes/*/script.md.
HABITAT: dict[str, dict] = {
    "orca": {"biomes": {"open_ocean", "polar_ice", "kelp_forest", "coastal_surface"}, "depth": (0, 400)},
    "greatWhite": {"biomes": {"open_ocean", "kelp_forest", "coastal_surface", "tropical_reef"}, "depth": (0, 1200)},
    "blueWhale": {"biomes": {"open_ocean", "polar_ice", "coastal_surface"}, "depth": (0, 500)},
    "spermWhale": {"biomes": {"open_ocean", "twilight", "deep"}, "depth": (0, 2500)},
    "seal": {"biomes": {"polar_ice", "kelp_forest", "coastal_surface"}, "depth": (0, 500)},
    "colossalSquid": {"biomes": {"twilight", "deep"}, "depth": (300, 2200)},
    "anglerfish": {"biomes": {"twilight", "deep"}, "depth": (200, 4500)},
    "octopus": {"biomes": {"tropical_reef", "kelp_forest"}, "depth": (0, 200)},
    "cookiecutter": {"biomes": {"open_ocean", "twilight"}, "depth": (0, 3700)},
    "krill": {"biomes": {"polar_ice", "open_ocean"}, "depth": (0, 200)},
    "crocodile": {"biomes": {"coastal_surface"}, "depth": (0, 20)},
    # people: scuba (YOU as a diver) stays shallow; on the surface (boats, floes) only where a surface is in view
    "diver": {"biomes": {"open_ocean", "polar_ice", "kelp_forest", "coastal_surface", "tropical_reef"}, "depth": (0, 60)},
    "you": {"biomes": {"open_ocean", "polar_ice", "kelp_forest", "coastal_surface", "tropical_reef"}, "depth": (0, 60)},
    # vehicles / land animals are compared on a board (cars floating in mid-water: ORCA_V2_AUDIT I9)
    "car": {"biomes": set(), "depth": (0, 0)}, "bus": {"biomes": set(), "depth": (0, 0)},
    "golfCart": {"biomes": set(), "depth": (0, 0)}, "jet": {"biomes": set(), "depth": (0, 0)},
    "elephant": {"biomes": set(), "depth": (0, 0)}, "hippo": {"biomes": set(), "depth": (0, 0)},
    "grizzly": {"biomes": set(), "depth": (0, 0)}, "sauropod": {"biomes": set(), "depth": (0, 0)},
}
# kit pieces that only exist in one kind of place
PROP_BIOMES = {"explainer/Sailboat": {"coastal_surface", "open_ocean"}, "explainer/IceFloe": {"polar_ice"}}

# ------------------------------------------------------------------ narration -> setting (fill)
# a place named in the narration -> its setting (extend with a source for new places)
GAZETTEER: list[tuple[str, dict]] = [
    (r"\bantarctic(a)?\b|\bsouthern ocean\b|\bpack ice\b|\bice floe", {"biome": "polar_ice", "place": "Antarctic Peninsula",
                                                                     "depth": 3, "waterline": 0.33, "light": "overcast"}),
    (r"\barctic\b|\bgreenland\b|\bsvalbard\b", {"biome": "polar_ice", "place": "Arctic sea ice", "depth": 3,
                                                "waterline": 0.33, "light": "overcast"}),
    (r"\bsouth africa\b|\bgansbaai\b|\bcape town\b", {"biome": "kelp_forest", "place": "Gansbaai, South Africa",
                                                      "depth": 12, "waterline": None, "light": "day"}),
    (r"\bkelp\b|\bcalifornia\b", {"biome": "kelp_forest", "place": "kelp forest", "depth": 12, "waterline": None,
                                  "light": "day"}),
    (r"\bwestern australia\b|\bbremer bay\b", {"biome": "open_ocean", "place": "Bremer Bay, Western Australia",
                                               "depth": 10, "waterline": 0.1, "light": "day"}),
    (r"\bspain\b|\bportugal\b|\bgibraltar\b|\biberia", {"biome": "coastal_surface", "place": "Iberian Atlantic coast",
                                                        "depth": 0, "waterline": 0.26, "light": "day"}),
    (r"\bcoral\b|\breefs?\b|\btropical\b", {"biome": "tropical_reef", "place": "coral reef", "depth": 10,
                                           "waterline": None, "light": "day"}),
    (r"\btwilight zone\b|\bmesopelagic\b", {"biome": "twilight", "place": "twilight zone", "depth": 500,
                                           "waterline": None, "light": "night"}),
    (r"\babyss|\btrench\b|\bmidnight zone\b|\bdeep sea\b|\bseafloor\b", {"biome": "deep", "place": "deep sea",
                                                                       "depth": 3000, "waterline": None,
                                                                       "light": "night"}),
]
# abstract beats (numbers, comparisons, questions, lists) -> a board (rule 13)
ABSTRACT = re.compile(r"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|twenty|thirty|fifty|hundred|thousand|"
                      r"million|metres?|meters?|tonnes?|tons?|kilometres?|km|times|as heavy|as tall|as big|bigger|"
                      r"heavier|faster|smaller|why|maybe|answer|percent)\b", re.I)
ANALOGY = re.compile(r"\b(like a|that's like|imagine|as if)\b", re.I)
DEFAULT = {"kind": "place", "biome": "open_ocean", "place": "open ocean", "depth": 20, "waterline": None, "light": "day"}


def segments(scene: dict) -> list[dict]:
    """the scene's setting as a list of segments with numeric scene-local `at` (first at 0) and `end`"""
    st = scene.get("setting")
    if not st:
        return []
    segs = [dict(s) for s in (st if isinstance(st, list) else [st])]
    segs[0]["at"] = 0.0
    for a, b in zip(segs, segs[1:]):
        a["end"] = float(b["at"])
    segs[-1]["end"] = float(scene["duration"])
    return segs


def normalise(seg: dict) -> dict:
    """defaults per kind: board / map carry their own biome, place segments fall back to DEFAULT fields"""
    s = dict(seg)
    k = s.setdefault("kind", "place")
    if k in ("board", "map"):
        s["biome"] = k
        s.setdefault("place", k)
        s["depth"] = 0
        s["waterline"] = None
        s.setdefault("light", "day")
        return s
    for f, v in DEFAULT.items():
        s.setdefault(f, v)
    return s


def same(a: dict, b: dict) -> bool:
    """two segments are one setting (no visible change): same kind, biome, place, board field and depth band"""
    f = lambda s: (s.get("kind"), s.get("biome"), s.get("place"), s.get("board"), s.get("lanes"), s.get("light"),
                   depth_band(s.get("depth", 0)))
    return f(a) == f(b)


def depth_band(d) -> int:
    d = float(d or 0)
    return 0 if d < 200 else 1 if d < 1000 else 2


def timeline(sb: dict) -> list[dict]:
    """global setting runs [{t0, t1, setting}] with consecutive identical segments merged"""
    out, t0 = [], 0.0
    for sc in sb["scenes"]:
        for s in segments(sc):
            seg = normalise(s)
            a, b = t0 + float(s["at"]), t0 + float(s["end"])
            if b - a <= 1e-6:
                continue
            if out and same(out[-1]["setting"], seg):
                out[-1]["t1"] = b
            else:
                out.append({"t0": a, "t1": b, "setting": seg})
        t0 += sc["duration"]
    return out


def stats(sb: dict) -> dict:
    tl = timeline(sb)
    total = sum(s["duration"] for s in sb["scenes"])
    holds = [r["t1"] - r["t0"] for r in tl]
    distinct = {(r["setting"]["kind"], r["setting"]["biome"], r["setting"].get("place"), r["setting"].get("board"))
                for r in tl}
    changes = max(0, len(tl) - 1)
    return {"runs": len(tl), "distinct": len(distinct), "changes": changes,
            "per_min": round(changes / (total / 60), 2) if total else 0.0,
            "max_hold": round(max(holds), 2) if holds else 0.0, "total": round(total, 2),
            "world_share": round(sum(h for h, r in zip(holds, tl) if r["setting"]["kind"] in ("place",)) / total, 3) if total else 0}


# ------------------------------------------------------------------ fill: narration -> setting

def _scene_words(sb: dict) -> list[tuple[dict, float, list[dict]]]:
    """[(scene, t0, words spoken inside it with scene-local times)]"""
    words = (sb.get("captions") or {}).get("words") or []
    out, t0 = [], 0.0
    for sc in sb["scenes"]:
        t1 = t0 + sc["duration"]
        ws = [{**w, "start": w["start"] - t0, "end": w["end"] - t0} for w in words if t0 - 0.01 <= w["start"] < t1]
        out.append((sc, t0, ws))
        t0 = t1
    return out


def _norm(w: str) -> str:
    return re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))


def anchor(ws: list[dict], a, dur: float) -> float:
    """"@word", "@word#2", "@word+0.3", "@word.end" -> scene-local seconds (numbers pass through)"""
    if isinstance(a, (int, float)):
        return float(a)
    m = re.match(r"^@([\w'*-]+)(?:#(\d+))?(\.end)?([+-][\d.]+)?$", str(a))
    if not m:
        raise ValueError(f"setting anchor {a!r}: use a number or '@word[#n][.end][+-s]'")
    tok, nth, end, off = m.group(1), int(m.group(2) or 1) - 1, bool(m.group(3)), float(m.group(4) or 0)
    pre = tok.endswith("*")
    tok = _norm(tok.rstrip("*"))
    subs = lambda w: [_norm(x) for x in w["text"].replace("-", " ").split()]   # joined caption tokens split back
    hits = [w for w in ws if any((x.startswith(tok) if pre else x == tok) for x in subs(w))]
    if len(hits) <= nth:
        raise ValueError(f"setting anchor {a!r}: word not in the scene")
    t = hits[nth]["end" if end else "start"] + off
    return round(max(0.0, min(dur - 0.05, t)), 3)


def cue_time(ws: list[dict], cue: str) -> float | None:
    """scene-local start of the first spoken run matching cue (one or more words), None if absent"""
    toks = [_norm(t) for t in cue.split() if _norm(t)]
    flat = []
    for w in ws:                         # joined caption tokens ("2019,", "fifty-six kilometres") split back to words
        for t in w["text"].replace("-", " ").split():
            flat.append((_norm(t), w["start"]))
    for i in range(len(flat) - len(toks) + 1):
        if all(flat[i + k][0] == toks[k] or flat[i + k][0].rstrip("s") == toks[k].rstrip("s") for k in range(len(toks))):
            return flat[i][1]
    return None


def infer(text: str, prev: dict | None, default: dict) -> dict:
    """one scene's setting from its narration: named place > analogy > abstract (board) > previous place > default"""
    low = text.lower()
    for rx, st in GAZETTEER:
        m = re.search(rx, low)
        if m:
            return {"kind": "place", **st, "cue": m.group(0)}
    if ANALOGY.search(text):
        return {"kind": "analogy", "biome": (prev or default).get("biome", "open_ocean"), "place": "analogy",
                "depth": 0, "waterline": None, "light": "day"}
    if len(ABSTRACT.findall(text)) + text.count("?") >= 2:
        return {"kind": "board"}
    if prev and prev.get("kind") == "place":
        return {k: v for k, v in prev.items() if k not in ("cue", "at", "end")}   # the story stays where it was
    return dict(default)


def fill(sb: dict, default: dict | None = None) -> dict:
    """resolve anchors and fill missing settings in place (returns sb). Builders that declare settings win."""
    d = {**DEFAULT, **(default or {})}
    prev = None
    boards = 0
    for sc, _t0, ws in _scene_words(sb):
        st = sc.get("setting")
        if not st:
            st = infer(sc.get("notes") or " ".join(w["text"] for w in ws), prev, d)
        segs = [dict(s) for s in (st if isinstance(st, list) else [st])]
        for i, s in enumerate(segs):
            s["at"] = 0.0 if i == 0 else anchor(ws, s.get("at", 0), sc["duration"])
            if s.get("kind") == "board" and not s.get("board"):
                s["board"] = BOARD_FIELDS[boards % 3]       # navy / blue / ink: neighbouring boards differ
                boards += 1
        sc["setting"] = segs[0] if len(segs) == 1 else segs
        last = normalise(segs[-1])
        if last["kind"] == "place":
            prev = last                 # boards and maps don't move the story: the next unnamed beat returns here
    return sb


def validate(sb: dict) -> list[str]:
    """schema-level errors in the declared settings (kinds, biomes, lights, depth inside the biome's band)"""
    out = []
    for sc in sb["scenes"]:
        segs = segments(sc)
        if not segs:
            out.append(f"{sc['id']} [setting] no setting declared (scene.setting; pipeline/episodes/settings.py)")
            continue
        last = -1.0
        for s in segs:
            n = normalise(s)
            where = f"{sc['id']} @{float(s['at']):.2f}s"
            if n["kind"] not in KINDS:
                out.append(f"{where} [setting] kind {n['kind']!r} (known: {', '.join(KINDS)})")
            if n["biome"] not in BIOMES:
                out.append(f"{where} [setting] biome {n['biome']!r} (known: {', '.join(BIOMES)})")
                continue
            if n.get("light") not in LIGHTS:
                out.append(f"{where} [setting] light {n.get('light')!r} (known: {', '.join(LIGHTS)})")
            elif n["light"] not in BIOMES[n["biome"]]["lights"]:
                out.append(f"{where} [setting] light {n['light']!r} does not exist in {n['biome']} "
                           f"({', '.join(BIOMES[n['biome']]['lights'])})")
            lo, hi = BIOMES[n["biome"]]["depth"]
            if n["kind"] == "place" and not lo <= float(n.get("depth", 0)) <= hi:
                out.append(f"{where} [setting] depth {n.get('depth')} m is outside {n['biome']} ({lo}-{hi} m)")
            if float(s["at"]) <= last:
                out.append(f"{where} [setting] segments must start in order")
            last = float(s["at"])
            if n["kind"] == "board" and n.get("board") and n["board"] not in BOARD_FIELDS:
                out.append(f"{where} [setting] board field {n['board']!r} (known: {', '.join(BOARD_FIELDS)})")
    return out
