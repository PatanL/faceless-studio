"""Scored soundtrack for explainer Shorts: composed in code from the storyboard, rendered from a SoundFont.

Research: research/music/KURZ_MUSIC.md (how Kurzgesagt's music serves the narration, measured on two references, and
which rules transfer to 60-90 s vertical Shorts). The composer reads the storyboard's per-scene settings
(pipeline/episodes/settings.py timeline), the word timings and the script's SFX markers, and writes cues:

  plan       setting runs -> moods (place / light / biome + the words spoken there) -> cues of 4-16 s; a cue turns
             on the narration (a pivot or answer word up to 1.2 s before a setting change moves the boundary to it);
             short map cards become the next cue's intro; a repeated mood escalates (intensity +1, new colour).
  reveals    script impact/stinger markers, pivot sentences ("But / Except / Until ..."), "the answer is X", short
             punch sentences after long ones -> stings (low hit + bell) on the word, 1-3 drop-outs (the music falls
             away 0.25-0.9 s before the word), risers (reverse cymbal + pad swell + arp double-time) into boundaries
             whose intensity rises; the hook plays sparse and lands with a hit on the first setting change.
  loop       `ending: loop`: the last cue returns to the hook's mood and harmony, ends on the chord that leads into
             bar 1, and the rendered tail (sustain + reverb) is wrapped onto the start, so the replay seam is continuous.

Every note is generated here (generic progressions, an episode-seeded motif); instruments are presets of a
licence-cleared SoundFont (config.SOUNDFONTS, pipeline/audio/LICENSES.md), rendered by libfluidsynth (sf2.py); the
sub bass, sub booms and all effects are numpy / pedalboard. Output: score.wav (stereo 48 kHz), stems, score.mid,
score_plan.json (every cue, chord, reveal, drop-out and riser with times, used by the measurements).

usage (Spark, ~/studio/.venv):
  python -m pipeline.audio.score episodes/<slug>/storyboard.json --out /tmp/score [--script episodes/<slug>/script.md]
      [--cues studio/public/episodes/<slug>/cues.json] [--duration 84.63] [--loop]
pipeline.audio.make calls compose() when the music is "score" (config.SCORE) and a storyboard exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from dataclasses import dataclass, field

import numpy as np
import soundfile as sf

from .config import SR

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# ----------------------------------------------------------------------------- theory

QUAL = {"maj": [0, 4, 7], "min": [0, 3, 7], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10], "maj9": [0, 4, 7, 11, 14],
        "min9": [0, 3, 7, 10, 14], "add9": [0, 4, 7, 14], "madd9": [0, 3, 7, 14], "sus2": [0, 2, 7], "sus4": [0, 5, 7],
        "7sus4": [0, 5, 7, 10], "maj7#11": [0, 4, 7, 11, 18], "5": [0, 7]}

# GM presets (bank, program) in the cleared bank (GeneralUser GS names)
P = {"piano": (0, 0), "celesta": (0, 8), "glock": (0, 9), "musicbox": (0, 10), "vibes": (0, 11), "marimba": (0, 12),
     "fingerbass": (0, 33), "synthbass": (0, 39), "cello": (0, 42), "contrabass": (0, 43), "tremolo": (0, 44),
     "pizz": (0, 45), "harp": (0, 46), "timpani": (0, 47), "strings": (0, 48), "slowstrings": (0, 49),
     "synthstrings": (0, 50), "choir": (0, 52), "fantasia": (0, 88), "warmpad": (0, 89), "bowedglass": (0, 92),
     "halopad": (0, 94), "crystal": (0, 98), "atmosphere": (0, 99), "kalimba": (0, 108), "taiko": (0, 116),
     "kit": (128, 48), "stdkit": (128, 0)}

# moods: key offset from the episode tonic, progression [(degree semitones, quality)] one chord per bar, instruments
# per layer, arp pattern / rate, the velocity scale and the base intensity. Layers by intensity:
#   0 pad + sub + motif/sparse arp | 1 + arp + bass | 2 + pulse | 3 + percussion, arp doubled
MOODS = {
    "curious": {"key": 0, "prog": [(0, "maj9"), (2, "add9"), (9, "min7"), (5, "maj7")],
                "pad": ["warmpad", "slowstrings"], "arp": ["celesta", "harp"], "pulse": "harp", "bass": "fingerbass",
                "bells": "glock", "pattern": "rolling", "rate": 2, "base": 1, "perc": "soft"},
    "board": {"key": 0, "prog": [(0, "add9"), (7, "maj"), (9, "min7"), (5, "add9")],
              "pad": ["synthstrings"], "arp": ["marimba", "kalimba"], "pulse": "pizz", "bass": "pizz",
              "bells": "glock", "pattern": "updown", "rate": 2, "base": 1, "staccato": True, "perc": "shaker",
              "prog_alt": [(9, "min7"), (5, "add9"), (0, "add9"), (7, "sus4")]},
    "tense": {"key": 0, "prog": [(0, "min"), (0, "min"), (8, "maj"), (10, "maj")],
              "pad": ["slowstrings"], "arp": ["celesta", "vibes"], "pulse": "strings", "bass": "contrabass",
              "bells": "glock", "pattern": "ostinato", "rate": 2, "base": 2, "perc": "timpani",
              "prog_alt": [(0, "min"), (10, "maj"), (8, "maj"), (7, "maj")]},
    "cold": {"key": 0, "prog": [(0, "madd9"), (10, "add9"), (7, "sus2"), (9, "7sus4")],
             "pad": ["bowedglass", "halopad"], "arp": ["vibes", "crystal"], "pulse": "harp", "bass": "contrabass",
             "bells": "crystal", "pattern": "wide", "rate": 2, "base": 1, "perc": "timpani"},
    "warm": {"key": 3, "prog": [(0, "add9"), (4, "min7"), (9, "min7"), (5, "maj7")],
             "pad": ["slowstrings", "choir"], "arp": ["piano", "harp"], "pulse": "harp", "bass": "cello",
             "bells": "celesta", "pattern": "broken", "rate": 2, "base": 1, "perc": None},
    "question": {"key": 0, "prog": [(5, "maj7"), (7, "sus4"), (5, "maj7"), (7, "7sus4")],
                 "pad": ["halopad", "warmpad"], "arp": ["musicbox", "celesta"], "pulse": "pizz", "bass": None,
                 "bells": "musicbox", "pattern": "sparkle", "rate": 1, "base": 1, "perc": None},
    "deep": {"key": 0, "prog": [(0, "min9"), (5, "min7"), (8, "maj7"), (7, "min")],
             "pad": ["atmosphere", "slowstrings"], "arp": ["vibes", "celesta"], "pulse": "harp", "bass": "contrabass",
             "bells": "vibes", "pattern": "wide", "rate": 1, "base": 1, "perc": None},
}
PATTERNS = {  # chord-tone indexes per arp step (None = rest)
    "rolling": [0, 2, 1, 3, 2, 4, 3, 1], "updown": [0, 1, 2, 3, 4, 3, 2, 1], "ostinato": [0, 0, 2, 0, 1, 0, 2, 3],
    "wide": [0, 3, None, 2, 4, None, 1, 3], "broken": [0, 2, 4, 2, 1, 3, 4, 3], "sparkle": [3, None, 4, None, 2, None, 5, None],
}

TENSION = re.compile(r"\b(hunt\w*|kill\w*|charg\w*|attack\w*|ram|rams|ramm\w*|sunk|sink\w*|sank|fled|flee\w*|chas\w*|"
                     r"brought down|outnumber\w*|teeth|predator\w*|deadly|danger\w*|scared|fear\w*|snap\w*|bite\w*|"
                     r"crush\w*|trap\w*|wash\w*|ambush\w*|strike\w*|struck|dies|die|death|dead|poison\w*|venom\w*)\b", re.I)
WARM = re.compile(r"\b(mother\w*|mum|mom|calf|calves|taught|teach\w*|famil\w*|culture|bab(y|ies)|car(e|es|ing)|"
                  r"together|love\w*|gentle|friend\w*|young|raise\w*|protect\w*|share\w*)\b", re.I)
PIVOT = re.compile(r"^(but|except|until|yet|instead|unless|then|still|now|turns)$", re.I)
ANSWER = re.compile(r"\b(the|our|my)\s+(\w+\s+)?answer\s+(is|was)\b", re.I)

# loudness (LUFS) of each role for a reference phrase at velocity 100 (render_tracks calibrates every preset with the
# same phrase, so presets of different loudness sit at their role level and the velocities keep their dynamics)
ROLE_LUFS = {"pad": -22.0, "arp": -26.0, "pulse": -27.0, "bass": -25.0, "motif": -24.5, "bells": -28.0,
             "perc": -26.0, "stab": -30.0, "shaker": -39.0}
INTENSITY_DB = {0: -3.5, 1: -1.5, 2: 0.0, 3: 1.5}
REF_KEYS = {"pad": [50, 57, 62, 65], "arp": [74, 79, 81, 86], "motif": [74, 79, 81, 86], "bells": [86, 91],
            "pulse": [50, 57], "bass": [38, 45], "perc": [38, 50], "stab": [38, 45, 50], "shaker": [82]}


@dataclass
class Cue:
    t0: float
    t1: float
    mood: str
    intensity: int
    variant: int = 0
    segs: list = field(default_factory=list)   # [(t0, t1, kind)] setting segments inside the cue (kind: map | place)
    text: str = ""
    role: str = ""                              # hook | bookend | ""
    key: int = 0                                # pitch class of the cue's tonic
    chords: list = field(default_factory=list)  # [(t0, t1, root_midi_pc, quality)]


# ----------------------------------------------------------------------------- planning

def _words(sb: dict, words: list | None) -> list[dict]:
    ws = words or (sb.get("captions") or {}).get("words") or []
    out = []
    for w in ws:
        out.append({"w": str(w.get("text", w.get("w", ""))), "s": float(w.get("start", w.get("s", 0))),
                    "e": float(w.get("end", w.get("e", 0))), "emph": bool(w.get("emph"))})
    return out


def sentences(words: list[dict]) -> list[dict]:
    out, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.?!][\"')\]]*$", w["w"]) or w is words[-1]:
            out.append({"words": cur, "s": cur[0]["s"], "e": cur[-1]["e"], "text": " ".join(x["w"] for x in cur)})
            cur = []
    return out


def mood_of(setting: dict, text: str) -> str:
    kind, biome, light = setting.get("kind"), setting.get("biome"), setting.get("light", "day")
    ten, warm, ask = len(TENSION.findall(text)), len(WARM.findall(text)), text.count("?")
    if kind in ("board", "analogy") and ask and ask >= max(ten, warm):
        return "question"
    if warm > ten and warm >= 1:
        return "warm"
    if ten >= 1 and biome != "polar_ice":
        return "tense"
    if biome == "polar_ice":
        return "cold"
    if kind in ("board", "analogy"):
        return "board"
    if biome in ("twilight", "deep") or light in ("night", "dusk"):
        return "deep"
    return "curious"


def find_reveals(words: list[dict], sfx_cues: list[dict]) -> list[dict]:
    """reveal moments with a priority: markers 3, pivot 2.5, answer 2, short punch sentence 1.5, emphasised end word 1"""
    out = []
    starts = np.array([w["s"] for w in words]) if words else np.zeros(0)

    def snap(t):
        if not len(starts):
            return t
        i = int(np.argmin(np.abs(starts - t)))
        return float(starts[i]) if abs(starts[i] - t) <= 0.3 else t

    for c in sfx_cues or []:
        if c.get("source") == "marker" and c.get("cue") in ("impact", "stinger", "boom"):
            out.append({"t": snap(float(c["at"])), "prio": 3.0, "why": f"marker {c['cue']}"})
    sents = sentences(words)
    for i, s in enumerate(sents):
        w0 = s["words"][0]["w"].strip("\"'").lower().rstrip(",")
        if i and PIVOT.match(w0):
            out.append({"t": s["s"], "prio": 2.5, "why": f"pivot '{s['words'][0]['w']}'", "sentence_start": True})
        if ANSWER.search(s["text"]):
            out.append({"t": s["words"][-1]["s"], "prio": 2.0, "why": f"answer '{s['words'][-1]['w']}'"})
        if i and len(s["words"]) <= 3 and len(sents[i - 1]["words"]) >= 6:
            out.append({"t": s["s"], "prio": 1.5, "why": f"punch '{s['text']}'", "sentence_start": True})
        last = s["words"][-1]
        if last["emph"]:
            out.append({"t": last["s"], "prio": 1.0, "why": f"emph '{last['w']}'"})
    # one reveal per moment (highest priority wins within 0.6 s; a sentence opener beats a mid-sentence hit)
    for r in out:
        prev = [w for w in words if w["s"] < r["t"] - 0.01]
        r["prev_end"] = prev[-1]["e"] if prev else 0.0
        r["at_sentence_start"] = bool(prev and re.search(r"[.?!][\"')\]]*$", prev[-1]["w"]))
    out.sort(key=lambda r: (-r["prio"], not r["at_sentence_start"], r["t"]))
    keep = []
    for r in out:
        if all(abs(r["t"] - k["t"]) > 0.6 for k in keep):
            keep.append(r)
    return sorted(keep, key=lambda r: r["t"])


def plan(sb: dict, words: list[dict], total: float, loop: bool, sfx_cues: list[dict] | None = None) -> dict:
    import copy
    from pipeline.episodes import settings as S
    tl = [r for r in S.timeline(sb) if r["t0"] < total - 0.05]
    if not any(sc.get("setting") for sc in sb.get("scenes", [])):
        try:  # a storyboard from before per-scene settings: infer them from the narration (settings.fill)
            tl = [r for r in S.timeline(S.fill(copy.deepcopy(sb))) if r["t0"] < total - 0.05]
        except Exception:  # noqa: BLE001
            tl = []
    if len(tl) < 2 and len(sb.get("scenes", [])) > 1:  # still nothing to follow: one run per scene
        tl, t = [], 0.0
        for sc in sb["scenes"]:
            tl.append({"t0": t, "t1": t + float(sc["duration"]), "setting": dict(S.DEFAULT)})
            t += float(sc["duration"])
        tl = [r for r in tl if r["t0"] < total - 0.05]
    if not tl:
        tl = [{"t0": 0.0, "t1": total, "setting": dict(S.DEFAULT)}]
    tl[-1]["t1"] = total
    reveals = find_reveals(words, sfx_cues or [])
    text_in = lambda a, b: " ".join(w["w"] for w in words if a - 0.05 <= w["s"] < b - 0.05)
    # 1) runs -> moods (a map card takes the mood of the place it names)
    runs = []
    for i, r in enumerate(tl):
        st = r["setting"]
        nxt = tl[i + 1]["setting"] if i + 1 < len(tl) else st
        base = nxt if st.get("kind") == "map" else st
        txt = text_in(r["t0"], r["t1"] if st.get("kind") != "map" else (tl[i + 1]["t1"] if i + 1 < len(tl) else r["t1"]))
        runs.append({"t0": r["t0"], "t1": r["t1"], "kind": st.get("kind"), "mood": mood_of(base, txt), "text": text_in(r["t0"], r["t1"]),
                     "place": st.get("place")})
    # 2) runs -> cues: merge same-mood neighbours up to 16 s; short runs (< 4 s, not the hook) join the next cue
    cues: list[Cue] = []
    for i, r in enumerate(runs):
        seg = (r["t0"], r["t1"], r["kind"])
        if cues and r["kind"] != "map" and (cues[-1].mood == r["mood"] and r["t1"] - cues[-1].t0 <= 16.0 or
                     (cues[-1].t1 - cues[-1].t0 < 4.0 and cues[-1].role != "hook" and i > 0)):
            c = cues[-1]
            if c.t1 - c.t0 < 4.0 and c.mood != r["mood"] and c.role != "hook":
                c.mood = r["mood"]  # a short lead-in (map card) takes the following place's mood
            c.t1 = r["t1"]
            c.segs.append(seg)
            c.text += " " + r["text"]
            continue
        cues.append(Cue(r["t0"], r["t1"], r["mood"], MOODS[r["mood"]]["base"], segs=[seg], text=r["text"],
                        role="hook" if i == 0 else ""))
    # a final short cue (< 3 s) folds into the previous one unless it is the loop bookend
    if len(cues) > 2 and cues[-1].t1 - cues[-1].t0 < 3.0 and not loop:
        cues[-2].t1 = cues[-1].t1
        cues[-2].segs += cues[-1].segs
        cues.pop()
    # 2b) a long run (> 18 s, one place held while the narration moves on) is split into ~12 s sections at sentence
    #     starts: same mood, a new colour, and every other section breathes one intensity step down (Kurz: ~15 s cues)
    sent_starts = [x["s"] for x in sentences(words)]
    split: list[Cue] = []
    for c in cues:
        parts = [c]
        while parts[-1].t1 - parts[-1].t0 > 18.0:
            last = parts[-1]
            cands = [t for t in sent_starts if last.t0 + 9.0 <= t <= last.t1 - 6.0]
            if not cands:
                break
            t = min(cands, key=lambda x: abs(x - (last.t0 + 12.0)))
            nxt = Cue(t, last.t1, last.mood, last.intensity, variant=last.variant + 1,
                      segs=[(t, last.t1, "section")], text=text_in(t, last.t1))
            nxt.role = "section"
            last.t1 = t
            last.text = text_in(last.t0, t)
            parts.append(nxt)
        split += parts
    cues = split
    # 3) the music turns on the word: a strong reveal (>= 2) up to 1.2 s before a boundary moves the boundary to it
    for a, b in zip(cues[:-1], cues[1:]):
        cand = [r for r in reveals if r["prio"] >= 2.0 and b.t0 - 1.2 <= r["t"] < b.t0 - 0.05 and r["t"] - a.t0 > 2.0]
        if cand:
            t = max(cand, key=lambda r: r["prio"])["t"] - 0.03
            a.t1 = b.t0 = round(t, 3)
            b.segs.insert(0, (t, b.segs[0][0], "pivot"))
    # 4) intensity: base by mood, a repeated mood escalates and changes colour, tension past 40 % climbs one more
    for i, c in enumerate(cues):
        if c.role == "section":  # a split section breathes: alternate one step down
            c.intensity = max(1, cues[i - 1].intensity - 1) if cues[i - 1].role != "section" or \
                cues[i - 1].intensity >= c.intensity else min(3, cues[i - 1].intensity + 1)
            c.role = ""
            continue
        if i and cues[i - 1].mood == c.mood:
            c.variant = cues[i - 1].variant + 1
            c.intensity = min(3, cues[i - 1].intensity + 1)
        if c.mood in ("tense",) and c.t0 > 0.4 * total:
            c.intensity = min(3, c.intensity + 1)
        if c.mood == "cold" and TENSION.search(c.text):
            c.intensity = 2
    hook = cues[0]
    hook.role = "hook"
    hook.intensity = 0
    if loop:
        last = cues[-1]
        if last is not hook:
            last.role = "bookend"
            last.mood, last.intensity, last.variant = hook.mood, 0, 0
    # 5) keys and chords (one per bar on a per-cue beat grid that lands every boundary on a downbeat)
    tonic = 2  # D: the house key (moods move relative to it)
    beat0 = 60.0 / 108.0
    for c in cues:
        m = MOODS[c.mood]
        c.key = (tonic + m["key"]) % 12
        dur = c.t1 - c.t0
        nb = max(2, int(round(dur / beat0)))
        beat = dur / nb
        prog = list(m["prog_alt"] if (c.variant % 2 and "prog_alt" in m) else m["prog"])
        if c.role == "bookend":  # end on the chord that leads back into bar 1 of the hook
            n_bars = max(1, int(np.ceil(nb / 4)))
            prog = [prog[(k - n_bars) % len(prog)] for k in range(n_bars)]
        bars = [4] * (nb // 4)
        r = nb % 4
        if r == 1 and bars:
            bars[-1] = 5          # never a 1-beat bar: the last bar stretches
        elif r:
            bars.append(r)
        t = c.t0
        for k, bl in enumerate(bars):
            deg, q = prog[k % len(prog)]
            t1 = c.t1 if k == len(bars) - 1 else t + bl * beat
            c.chords.append((round(t, 4), round(t1, 4), (c.key + deg) % 12, q, beat))
            t = t1
    # 6) drop-outs and stings: priority first, spaced (drop-outs >= 14 s apart, stings >= 4 s)
    drops, stings = [], []
    boundaries = [c.t0 for c in cues[1:]]
    for r in sorted(reveals, key=lambda r: (-r["prio"], not r["at_sentence_start"], r["t"])):
        if r["t"] < 2.5 or r["t"] > total - 0.5:
            continue
        near_b = any(abs(r["t"] - b) < 0.35 for b in boundaries)
        # stings: strong reveals >= 4 s apart; punch lines (1.5) too when >= 8 s from any other sting
        if (r["prio"] >= 2.0 and all(abs(r["t"] - s["t"]) >= 4.0 for s in stings)) or \
                (r["prio"] >= 1.5 and all(abs(r["t"] - s["t"]) >= 8.0 for s in stings)):
            stings.append({"t": r["t"], "why": r["why"], "prio": r["prio"], "on_boundary": near_b})
        # drop-outs (Kurz: 0.3-1.3 s, under the end of the set-up line, 1.6/min): before sentence-opening reveals and
        # answers, >= 14 s apart, never in the hook
        if (r["prio"] >= 2.0 and (r["at_sentence_start"] or r["why"].startswith("answer"))
                and all(abs(r["t"] - d["t1"]) >= 14.0 for d in drops) and r["t"] > 8.0):
            drops.append({"t0": round(r["t"] - 0.6, 3), "t1": round(r["t"] - 0.02, 3), "why": r["why"]})
    stings.sort(key=lambda s: s["t"])
    drops.sort(key=lambda d: d["t0"])
    # 7) risers into boundaries where the intensity rises or the music turns tense, and into the hook landing
    # cymbal risers into a darker / bigger cue (and the hook landing), pad swells into the others; one bar when the
    # jump is big (hook, +2 intensity, into tension), half a bar otherwise (Kurz: 1.5-6 s, peaks on sentence starts)
    risers = []
    for a, b in zip(cues[:-1], cues[1:]):
        jump = b.intensity - a.intensity
        rise = jump > 0 or (b.mood == "tense" and a.mood != "tense") or a.role == "hook"
        if not rise or b.role == "bookend":
            continue
        if any(d["t0"] - 0.1 <= b.t0 <= d["t1"] + 0.3 for d in drops):
            continue  # a drop-out already sets this moment up
        big = a.role == "hook" or jump >= 2 or (b.mood in ("tense", "cold") and a.mood not in ("tense", "cold"))
        beat = a.chords[-1][4]
        L = round(min(0.75 * (a.t1 - a.t0), (4 if big else 2) * beat), 2)
        kind = "cymbal" if (big or b.mood in ("tense", "cold")) else "swell"
        risers.append({"t0": round(b.t0 - L, 3), "t1": b.t0, "len": L, "kind": kind})
    return {"total": round(total, 3), "loop": loop, "tonic": tonic, "cues": [c.__dict__ for c in cues],
            "reveals": reveals, "stings": stings, "drops": drops, "risers": risers,
            "boundaries": boundaries, "settings": [{"t0": r["t0"], "t1": r["t1"], "kind": r["kind"], "mood": r["mood"],
                                                    "place": r["place"]} for r in runs]}


# ----------------------------------------------------------------------------- arrangement (notes)

class Tracks:
    """note lists per (role, preset); each becomes one dry FluidSynth render, normalised to its role level"""

    def __init__(self, seed: int):
        self.notes: dict[tuple, list] = {}
        self.rng = np.random.default_rng(seed)

    def add(self, role: str, preset: str, t: float, dur: float, key: int, vel: float, jitter=0.006):
        if dur <= 0.01 or key < 12 or key > 115:
            return
        tj = t + (self.rng.uniform(-jitter, jitter) if jitter else 0.0)
        v = int(np.clip(vel + self.rng.normal(0, 4), 8, 124))
        self.notes.setdefault((role, preset), []).append((max(0.0, tj), dur, int(key), v))


def voicing(prev: list[int] | None, root_pc: int, q: str, lo=50, hi=74, n=4) -> list[int]:
    ivs = QUAL[q]
    pcs = [(root_pc + i) % 12 for i in ivs]
    pcs = list(dict.fromkeys(pcs))[:n] if len(pcs) > n else pcs
    center = np.mean(prev) if prev else (lo + hi) / 2
    out = []
    for pc in pcs:
        cands = [k for k in range(lo, hi + 1) if k % 12 == pc]
        out.append(min(cands, key=lambda k: abs(k - center)) if cands else lo + (pc - lo) % 12)
    out = sorted(set(out))
    while len(out) < min(n, len(pcs)) and out:
        out.append(out[0] + 12)
    return sorted(out)


def arp_tones(root_pc: int, q: str, lo: int, span: int = 24) -> list[int]:
    ivs = sorted(set(i % 12 for i in QUAL[q]))
    tones = []
    base = lo + ((root_pc - lo) % 12)
    for octv in range(0, span // 12 + 1):
        for i in ivs:
            k = base + i + 12 * octv
            if lo <= k <= lo + span:
                tones.append(k)
    return sorted(set(tones)) or [base]


def motif_for(seed: int) -> list[tuple[float, int]]:
    """an episode motif: (beat offset, chord-tone index) on the first chord, 4-5 notes over two bars"""
    rng = np.random.default_rng(seed)
    shapes = [[(0, 2), (1.5, 3), (2, 4), (4, 3), (6, 1)], [(0, 4), (1, 3), (1.5, 2), (3, 3), (4, 1)],
              [(0, 1), (0.5, 2), (1, 4), (3, 3), (6, 2)], [(0, 3), (1.5, 4), (2, 2), (4, 1), (5, 2)]]
    return shapes[int(rng.integers(len(shapes)))]


def arrange(pl: dict, seed: int) -> tuple[Tracks, dict]:
    tr = Tracks(seed)
    extra = {"sub": [], "booms": [], "risers": pl["risers"]}
    cues = [Cue(**{k: v for k, v in c.items()}) for c in pl["cues"]]
    motif = motif_for(seed)
    prev_pad = None
    for ci, c in enumerate(cues):
        m = MOODS[c.mood]
        inten = c.intensity
        var = c.variant
        pad_p = m["pad"][var % len(m["pad"])]
        arp_p = m["arp"][var % len(m["arp"])]
        stacc = m.get("staccato", False)
        travel_until = c.segs[0][1] if c.segs and c.segs[0][2] == "map" and len(c.segs) > 1 else None
        internal = [s[0] for s in c.segs[1:] if s[0] > c.t0 + 0.5]
        hook = c.role in ("hook", "bookend")
        for bi, (t0, t1, root, q, beat) in enumerate(c.chords):
            n_beats = int(round((t1 - t0) / beat))
            in_travel = travel_until is not None and t0 < travel_until - 0.05
            # sections inside a cue: each internal setting change adds colour (Kurz: texture changes at settings)
            n_int = sum(1 for x in internal if x <= t0 + 0.05)
            lvl = inten + (1 if n_int and inten < 3 else 0)
            # --- pad (legato, voice-led)
            vp = voicing(prev_pad, root, q, 50, 74, 4)
            prev_pad = vp
            pv = 58 + 10 * min(lvl, 3) - (14 if hook else 0) + (6 if c.mood == "question" else 0)
            if not in_travel or ci == 0:
                for k in vp:
                    tr.add("pad", pad_p, t0, t1 - t0 + 0.06, k, pv, jitter=0.0)
                if c.mood == "warm" and lvl >= 1:
                    for k in vp[:2]:
                        tr.add("pad", "choir" if pad_p != "choir" else "slowstrings", t0, t1 - t0 + 0.06, k + 12, pv - 18, 0.0)
            # --- sub (numpy): root in the 40-80 Hz octave
            sub_k = 28 + ((root - 28) % 12)
            if True:
                extra["sub"].append((t0, t1, sub_k, 0.55 if hook else (0.7 if c.mood in ("board", "question") else 1.0)))
            # --- bass
            if m["bass"] and lvl >= 1 and not hook:
                bk = 36 + ((root - 36) % 12)
                if stacc or c.mood == "board":
                    for b in range(0, n_beats, 2):
                        tr.add("bass", m["bass"], t0 + b * beat, beat * 0.8, bk, 84)
                else:
                    tr.add("bass", m["bass"], t0, t1 - t0 + 0.04, bk, 78 + 6 * lvl)
            # --- arp (or travel figure on map cards)
            rate = 2 if lvl >= 1 and m["rate"] == 2 else 1
            if in_travel:
                tones = arp_tones(root, q, 60, 19)
                for s in range(n_beats * 2):
                    t = t0 + s * beat / 2
                    if t >= travel_until - 0.02:
                        break
                    tr.add("arp", "marimba", t, beat * 0.45, tones[[0, 2, 1, 3, 2, 1, 3, 2][s % 8] % len(tones)], 70 + (12 if s % 4 == 0 else 0))
                for b in range(0, n_beats):
                    t = t0 + b * beat
                    if t < travel_until - 0.02:
                        tr.add("bass", "pizz", t, beat * 0.5, 38 + ((root - 38) % 12), 80)
            elif lvl >= 1 or hook or c.mood == "question":
                lo = 72 if arp_p not in ("piano", "harp", "vibes", "marimba", "kalimba") else 62
                if arp_p in ("glock", "crystal", "musicbox"):
                    lo = 79
                tones = arp_tones(root, q, lo + (12 if (var % 2 and lo < 72) else 0), 19)
                pat = PATTERNS[m["pattern"]]
                steps = n_beats * (rate if not hook else 1)
                step_len = beat / (rate if not hook else 1)
                # riser: double-time over the last 2 beats before a riser boundary
                rz = [r for r in pl["risers"] if t0 < r["t1"] <= t1 + 0.01]
                for s in range(steps):
                    t = t0 + s * step_len
                    idx = pat[s % len(pat)]
                    if idx is None or (hook and s % 2 and c.role == "hook" and t < 1.0):
                        continue
                    k = tones[idx % len(tones)]
                    accent = 10 if s % (2 * rate) == 0 else 0
                    v = (54 if hook else 62 + 6 * min(lvl, 3)) + accent
                    dur = step_len * (0.5 if stacc else 1.6)
                    tr.add("arp", arp_p, t, dur, k, v)
                    if lvl >= 3:
                        tr.add("arp", arp_p, t, dur, k + 12, v - 16)
                    for r in rz:
                        if r["t1"] - 2 * beat <= t < r["t1"] - 0.02:
                            tr.add("arp", arp_p, t + step_len / 2, dur * 0.6, tones[(idx + 2) % len(tones)], v - 6)
            # --- pulse (intensity >= 2)
            if lvl >= 2 and not hook and not in_travel:
                pk = 50 + ((root - 50) % 12)
                if c.mood in ("tense", "cold"):
                    acc = [100, 64, 78, 64, 94, 64, 78, 70]
                    for s in range(n_beats * 2):
                        k = pk if s % 4 != 3 else pk + 7
                        tr.add("pulse", m["pulse"] if c.mood == "tense" else "strings", t0 + s * beat / 2, beat * 0.32,
                               k, acc[s % 8] - (6 if lvl == 2 else 0))
                else:
                    tones = arp_tones(root, q, 55, 14)
                    for b in range(n_beats):
                        tr.add("pulse", m["pulse"], t0 + b * beat, beat * 0.6, tones[b % len(tones)], 70 + (10 if b % 4 == 0 else 0))
            # --- percussion (intensity 3 / tense 2)
            perc = m.get("perc")
            if not hook and not in_travel and perc == "timpani" and lvl >= 2:
                tk = 38 + ((root - 38) % 12)
                tr.add("perc", "timpani", t0, beat * 1.5, tk, 92 if lvl >= 3 else 80, 0.0)
                if lvl >= 3:
                    for b in (1.5, 2.0, 3.5):
                        if b < n_beats:
                            tr.add("perc", "taiko", t0 + b * beat, beat, 50, 70 + (12 if b == 2.0 else 0), 0.004)
            if not hook and not in_travel and perc == "shaker" and lvl >= 2:
                for s in range(n_beats * 4):
                    tr.add("shaker", "stdkit", t0 + s * beat / 4, beat / 4, 82, 46 + (16 if s % 2 == 0 else 0))
            if not hook and not in_travel and perc == "soft" and lvl >= 3:
                for s in range(n_beats * 2):
                    tr.add("shaker", "stdkit", t0 + s * beat / 2, beat / 2, 82, 40 + (14 if s % 2 else 0))
            # --- bells on the first downbeat of a cue and on internal setting changes
            if bi == 0 and not hook:
                bt = arp_tones(root, q, 84, 12)
                tr.add("bells", m["bells"], t0, beat * 2, bt[-1], 74)
            for x in internal:
                if t0 - 0.01 <= x < t1 - 0.01 and not hook:
                    bt = arp_tones(root, q, 84, 12)
                    tr.add("bells", m["bells"], x, beat * 2, bt[len(bt) // 2], 66)
                    extra["booms"].append({"t": x, "gain": 0.35})
        # --- motif: hook (bars 1-2), bookend, and the first bar of a warm cue
        if c.role in ("hook", "bookend") or (c.mood == "warm" and c.intensity <= 2):
            t0, t1, root, q, beat = c.chords[0]
            tones = arp_tones(root, q, 74, 14)
            inst = "celesta" if c.role else "piano"
            for off, idx in motif:
                t = c.t0 + off * beat
                if t < c.t1 - 0.1:
                    tr.add("motif", inst, t, beat * 1.4, tones[idx % len(tones)], 66 if c.role else 72)
    # --- stings on reveal words: low hit (timpani + low strings stab + sub boom) + a bell on top
    for s in pl["stings"]:
        c = next((c for c in cues if c.t0 - 0.05 <= s["t"] < c.t1), cues[-1])
        ch = next((x for x in c.chords if x[0] - 0.05 <= s["t"] < x[1]), c.chords[0])
        root, q = ch[2], ch[3]
        t = s["t"] - 0.03
        tr.add("perc", "timpani", t, 1.2, 38 + ((root - 38) % 12), 112, 0.0)
        for k in (38 + ((root - 38) % 12), 45 + ((root + 7 - 45) % 12), 50 + ((root - 50) % 12)):
            tr.add("stab", "strings", t, 0.32, k, 104, 0.0)
        bt = arp_tones(root, q, 86, 12)
        tr.add("bells", MOODS[c.mood]["bells"], t + 0.02, 1.0, bt[-1], 86, 0.0)
        extra["booms"].append({"t": t, "gain": 1.0})
    # boundary landings: a softer low hit on every cue start after the hook (Kurz: low hits at setting changes)
    for c in cues[1:]:
        if c.role == "bookend" or any(abs(s["t"] - c.t0) < 0.4 for s in pl["stings"]):
            continue
        root = c.chords[0][2]
        tr.add("perc", "timpani", c.t0 - 0.02, 1.0, 38 + ((root - 38) % 12), 84 if c.intensity >= 2 else 70, 0.0)
        extra["booms"].append({"t": c.t0 - 0.02, "gain": 0.6 if c.intensity >= 2 else 0.4})
    return tr, extra


# ----------------------------------------------------------------------------- render + mix

def _lufs_active(x: np.ndarray) -> float:
    import pyloudnorm as pyln
    mono = x.mean(1) if x.ndim == 2 else x
    h = int(0.4 * SR)
    n = len(mono) // h
    if n == 0:
        return -70.0
    e = np.sqrt((mono[: n * h].reshape(n, h) ** 2).mean(1) + 1e-12)
    act = e > e.max() * 10 ** (-30 / 20)
    sel = np.concatenate([x[i * h:(i + 1) * h] for i in np.nonzero(act)[0]]) if act.any() else x
    if len(sel) < SR // 2:
        sel = np.pad(sel, [(0, SR // 2 - len(sel))] + [(0, 0)] * (sel.ndim - 1))
    v = pyln.Meter(SR).integrated_loudness(sel)
    return float(v) if np.isfinite(v) else -70.0


def calibrate(r, role: str, preset: str) -> float:
    """active loudness of a preset playing its role's reference phrase at velocity 100 (one note per 0.5 s)"""
    bank, prog = P[preset]
    ch = 9 if bank == 128 else 0
    keys = REF_KEYS.get(role, [60, 67])
    ev = []
    for i in range(8):
        k = keys[i % len(keys)]
        ev += [(i * 0.5, "on", ch, k, 100), (i * 0.5 + (1.0 if role in ("pad", "bass") else 0.4), "off", ch, k)]
    return _lufs_active(r.render(ev, 4.0, {ch: (bank, prog)}, tail=1.0))


def render_tracks(tr: Tracks, total: float, tail: float, log=print) -> dict[str, np.ndarray]:
    from .sf2 import Renderer
    r = Renderer()
    n = int((total + tail) * SR)
    stems: dict[str, np.ndarray] = {}
    for (role, preset), notes in sorted(tr.notes.items()):
        bank, prog = P[preset]
        ch = 9 if bank == 128 else 0
        ev = []
        for t, d, k, v in notes:
            ev.append((t, "on", ch, k, v))
            ev.append((t + d, "off", ch, k))
        a = r.render(ev, total, {ch: (bank, prog)}, tail=tail)[:n]
        a = np.pad(a, ((0, n - len(a)), (0, 0)))
        lv = calibrate(r, role, preset)
        if lv <= -69 or not np.abs(a).max() > 0:
            continue
        a *= 10 ** ((ROLE_LUFS.get(role, -28.0) - lv) / 20)
        stem = {"pad": "pad", "arp": "keys", "motif": "keys", "bells": "keys", "pulse": "pulse", "bass": "bass",
                "perc": "perc", "stab": "perc", "shaker": "perc"}[role]
        stems[stem] = stems.get(stem, np.zeros((n, 2), np.float32)) + a.astype(np.float32)
        log(f"[score] track {role:6s} {preset:12s} {len(notes):4d} notes  ref {lv:6.1f} -> {ROLE_LUFS.get(role, -28):.1f} LUFS, "
            f"track {_lufs_active(a):6.1f}")
    return stems


def sub_bass(segs: list, n: int) -> np.ndarray:
    """sine sub with a touch of 2nd/3rd harmonic (so phone speakers imply it), legato between bars"""
    f = np.zeros(n)
    g = np.zeros(n)
    for t0, t1, k, gain in segs:
        i0, i1 = int(t0 * SR), min(n, int(t1 * SR))
        f[i0:i1] = 440 * 2 ** ((k - 69) / 12)
        g[i0:i1] = gain
    # glide 40 ms, gain smooth 60 ms
    from scipy.ndimage import uniform_filter1d
    f = uniform_filter1d(np.where(f > 0, f, np.nan_to_num(f)), size=int(0.04 * SR))
    g = uniform_filter1d(g, size=int(0.06 * SR))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    y = np.tanh(1.2 * y) / np.tanh(1.2)
    return (y * g).astype(np.float32)


def boom(n_len: float = 0.8) -> np.ndarray:
    t = np.arange(int(n_len * SR)) / SR
    f = 38 + 42 * np.exp(-t / 0.07)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.28) * np.clip(t / 0.004, 0, 1)
    return (np.tanh(1.5 * y) / np.tanh(1.5)).astype(np.float32)


def reverse_cymbal(seconds: float) -> np.ndarray:
    from .sf2 import Renderer
    a = Renderer().render([(0.0, "on", 9, 49, 112), (0.05, "on", 9, 57, 90)], 0.1, {9: P["kit"]}, tail=5.0)
    a = a[::-1]
    nz = np.nonzero(np.abs(a).max(1) > np.abs(a).max() * 1e-3)[0]
    a = a[nz[0]:] if len(nz) else a
    L = int(seconds * SR)
    if len(a) >= L:
        a = a[-L:]
    else:
        a = np.pad(a, ((L - len(a), 0), (0, 0)))
    fade = np.clip(np.arange(L) / (0.3 * L), 0, 1)[:, None]
    return (a * fade).astype(np.float32)


def fx_chain(name: str, x: np.ndarray, beat: float) -> np.ndarray:
    import pedalboard as pb
    chains = {
        "pad": [pb.HighpassFilter(110), pb.PeakFilter(2800, -3.0, 0.9), pb.Chorus(rate_hz=0.25, depth=0.12, mix=0.18),
                pb.Reverb(room_size=0.82, damping=0.45, wet_level=0.30, dry_level=0.80, width=1.0)],
        "keys": [pb.HighpassFilter(260), pb.PeakFilter(2800, -4.0, 1.0),
                 pb.Delay(delay_seconds=min(1.5, 0.75 * beat), feedback=0.22, mix=0.14),
                 pb.Reverb(room_size=0.72, damping=0.4, wet_level=0.28, dry_level=0.82, width=1.0)],
        "pulse": [pb.HighpassFilter(90), pb.PeakFilter(2800, -3.0, 0.9),
                  pb.Reverb(room_size=0.5, damping=0.5, wet_level=0.16, dry_level=0.9, width=0.8)],
        "bass": [pb.HighpassFilter(35), pb.LowpassFilter(2600),
                 pb.Compressor(threshold_db=-24, ratio=3.0, attack_ms=12, release_ms=140)],
        "perc": [pb.HighpassFilter(32), pb.Reverb(room_size=0.62, damping=0.5, wet_level=0.20, dry_level=0.9, width=1.0)],
        "fx": [pb.HighpassFilter(320), pb.PeakFilter(3000, -4.0, 0.8),
               pb.Reverb(room_size=0.6, damping=0.4, wet_level=0.22, dry_level=0.9, width=1.0)],
        "sub": [pb.LowpassFilter(160)],
    }
    board = pb.Pedalboard(chains[name])
    return board(x.T.astype(np.float32), SR).T


def compose(sb: dict, words: list | None, total: float, loop: bool, out_dir: str, sfx_cues: list | None = None,
            seed_key: str = "", log=print) -> dict:
    """plan + arrange + render the score for `total` seconds; writes score.wav, stems/, score.mid, score_plan.json"""
    import pedalboard as pb
    ws = _words(sb, words)
    pl = plan(sb, ws, total, loop, sfx_cues)
    seed = int(hashlib.sha256((seed_key or sb.get("id", "score")).encode()).hexdigest()[:8], 16)
    tr, extra = arrange(pl, seed)
    tail = 4.0
    n = int((total + tail) * SR)
    stems = render_tracks(tr, total, tail, log)
    beat = 60 / 108
    sub = sub_bass(extra["sub"], n)
    sub_st = np.stack([sub, sub], 1) * 10 ** ((-27.0 - _lufs_active(np.stack([sub, sub], 1))) / 20)
    bm = boom()
    booms = np.zeros(n, np.float32)
    for b in extra["booms"]:
        i = int(max(0, b["t"]) * SR)
        j = min(n, i + len(bm))
        booms[i:j] += bm[: j - i] * b["gain"]
    sub_st += np.stack([booms, booms], 1) * 10 ** ((-24.0 - _lufs_active(np.stack([bm, bm], 1))) / 20)
    stems["sub"] = sub_st.astype(np.float32)
    fx = np.zeros((n, 2), np.float32)
    for r in pl["risers"]:
        if r.get("kind") == "swell":
            continue
        rc = reverse_cymbal(r["len"])
        i = int(r["t0"] * SR)
        j = min(n, i + len(rc))
        if i >= 0:
            fx[i:j] += rc[: j - i]
    if np.abs(fx).max() > 0:
        fx *= 10 ** ((-24.0 - _lufs_active(fx)) / 20)
        stems["fx"] = fx
    # --- dynamics: hook level, cue intensity, swell into risers, drop-outs (pre-FX so tails ring naturally)
    t = np.arange(n) / SR
    g_db = np.zeros(n, np.float32)
    for c in pl["cues"]:
        sel = (t >= c["t0"]) & (t < c["t1"])
        g_db[sel] = INTENSITY_DB[c["intensity"]] + (-1.0 if c["role"] in ("hook", "bookend") else 0.0)
    g_db[t >= pl["total"]] = g_db[min(n - 1, int(pl["total"] * SR) - 1)]
    from scipy.ndimage import uniform_filter1d
    g_db = uniform_filter1d(g_db, size=int(0.25 * SR))  # 250 ms cross-fades between cue levels
    for r in pl["risers"]:  # pad/keys swell +4 dB across the riser
        sel = (t >= r["t0"]) & (t < r["t1"])
        g_db[sel] += 6.0 * ((t[sel] - r["t0"]) / max(1e-3, r["len"])) ** 2
    drop_db = np.zeros(n, np.float32)
    for d in pl["drops"]:
        a0, a1 = d["t0"], d["t1"]
        ramp_down = np.clip((t - a0) / 0.06, 0, 1)
        ramp_up = np.clip((a1 - t) / 0.012, 0, 1)
        drop_db = np.minimum(drop_db, np.where((t >= a0) & (t < a1 + 0.02), -24.0 * np.minimum(ramp_down, ramp_up), 0))
    gain = 10 ** ((g_db + drop_db) / 20)
    out = np.zeros((n, 2), np.float32)
    wet = {}
    for name, x in stems.items():
        y = x * (gain[:, None] if name != "fx" else 10 ** (drop_db / 20)[:, None])
        y = fx_chain(name, y, beat)
        # drop-outs also pull the reverb tails down 12 dB (Kurz drop-outs are 12-20 dB deep)
        y *= 10 ** (np.maximum(drop_db, -12.0) / 20)[:, None]
        wet[name] = y
        out += y
    bus = pb.Pedalboard([pb.Compressor(threshold_db=-18, ratio=2.0, attack_ms=25, release_ms=220),
                         pb.PeakFilter(3000, -2.5, 0.7), pb.HighShelfFilter(9000, 1.5, 0.7)])
    out = bus(out.T.astype(np.float32), SR).T
    # --- length: loop endings wrap the rendered tail onto the start (continuous replay seam)
    N = int(round(total * SR))
    if loop:
        tail_part = out[N:]
        out = out[:N].copy()
        out[: len(tail_part)] += tail_part
        for k in wet:
            tp = wet[k][N:]
            wet[k] = wet[k][:N].copy()
            wet[k][: len(tp)] += tp
    else:
        out = out[: N + int(2.0 * SR)]
        for k in wet:
            wet[k] = wet[k][: len(out)]
    # --- level: -20 LUFS integrated, peaks under -3 dBFS (the mix sets the final level against the voice)
    import pyloudnorm as pyln
    lv = pyln.Meter(SR).integrated_loudness(out)
    g = 10 ** ((-20.0 - lv) / 20)
    pk = np.abs(out).max() * g
    if pk > 10 ** (-3 / 20):
        g *= 10 ** (-3 / 20) / pk
    out *= g
    os.makedirs(os.path.join(out_dir, "score_stems"), exist_ok=True)
    sf.write(os.path.join(out_dir, "score.wav"), out, SR, subtype="PCM_24")
    for k, y in wet.items():
        sf.write(os.path.join(out_dir, "score_stems", f"{k}.wav"), y * g, SR, subtype="PCM_24")
    write_midi(tr, os.path.join(out_dir, "score.mid"))
    from .sf2 import soundfont
    sfm = soundfont()
    prov = {"generator": "pipeline.audio.score", "soundfont": sfm["name"], "soundfont_sha256": sfm["sha256"],
            "soundfont_licence": sfm["licence"], "seed": seed}
    pl["provenance"] = prov
    pl["n_notes"] = sum(len(v) for v in tr.notes.values())
    pl["tracks"] = sorted(f"{r}:{p}" for r, p in tr.notes)
    json.dump(pl, open(os.path.join(out_dir, "score_plan.json"), "w"), indent=1)
    log(f"[score] {len(pl['cues'])} cues ({', '.join(c['mood'] + str(c['intensity']) for c in pl['cues'])}), "
        f"{len(pl['stings'])} stings, {len(pl['drops'])} drop-outs, {len(pl['risers'])} risers, {pl['n_notes']} notes")
    return {"audio": out.astype(np.float32), "plan": pl, "provenance": prov, "path": os.path.join(out_dir, "score.wav")}


def write_midi(tr: Tracks, path: str):
    try:
        import pretty_midi
    except ImportError:
        return
    pm = pretty_midi.PrettyMIDI(initial_tempo=108)
    for (role, preset), notes in sorted(tr.notes.items()):
        bank, prog = P[preset]
        inst = pretty_midi.Instrument(program=prog, is_drum=bank == 128, name=f"{role}:{preset}")
        for t, d, k, v in notes:
            inst.notes.append(pretty_midi.Note(velocity=v, pitch=k, start=t, end=t + d))
        pm.instruments.append(inst)
    pm.write(path)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("storyboard")
    ap.add_argument("--out", required=True)
    ap.add_argument("--captions", help="captions.json (default: the storyboard's captions.words)")
    ap.add_argument("--cues", help="cues.json of the mix (script markers become reveals)")
    ap.add_argument("--duration", type=float, help="default: the storyboard's length")
    ap.add_argument("--loop", action="store_true")
    a = ap.parse_args(argv)
    sb = json.load(open(a.storyboard))
    words = json.load(open(a.captions))["words"] if a.captions else None
    total = a.duration or sum(s["duration"] for s in sb["scenes"])
    cues = json.load(open(a.cues)) if a.cues else None
    compose(sb, words, total, a.loop, a.out, cues)


if __name__ == "__main__":
    main()
