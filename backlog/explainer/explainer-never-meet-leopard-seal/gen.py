#!/usr/bin/env python3
"""Build script.md and storyboard.json for explainer-never-meet-leopard-seal from vo.py + measured Kokoro timings.

usage: python3 gen.py            (reads tts_durations.json if present, else a 177 wpm estimate)
Timeline: each VO line starts after the previous line's measured duration + its gap (vo.GAP / PUNCH_GAP / explicit),
silence entries add their seconds, END_HOLD closes the video. Every timestamp in script.md comes from this.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vo  # noqa: E402
from shots import SHOTS, KIT_GAPS  # noqa: E402
from doc import FRONT, BODY_BEFORE_SCRIPT, AFTER_SCRIPT, REHOOKS, JOKES  # noqa: E402

SLUG = "explainer-never-meet-leopard-seal"
YOU = re.compile(r"\b(you|your|you're|you'd|you've|you'll|yours|yourself)\b")

# ------------------------------------------------------------------ timeline
tts_path = os.path.join(HERE, "tts_durations.json")
TTS = json.load(open(tts_path)) if os.path.exists(tts_path) else None


def est(text, speed):
    return len(text.split()) / (177.0 * speed / vo.BODY_SPEED) * 60


LINE = {}      # id -> dict(start, end, text, on, sec)
ORDER = []
SECS = []      # (key, heading, start)
t = 0.0
cur = None
words = []
for e in vo.V:
    if e[0] == "#":
        cur = e[1]
        SECS.append([e[1], e[2], None])
        continue
    if e[0] == "~":
        _, lid, secs, on = e
        LINE[lid] = dict(start=round(t, 3), end=round(t + secs, 3), text=None, on=on, sec=cur, silence=secs)
        ORDER.append(lid)
        if SECS[-1][2] is None:
            SECS[-1][2] = t
        t += secs
        continue
    lid, text, on, gap = e
    speed = vo.HOOK_SPEED if lid.startswith("h") else vo.BODY_SPEED
    if TTS and lid in TTS["lines"]:
        d = TTS["lines"][lid]["dur"]
        for w in TTS["lines"][lid]["words"]:
            if re.search(r"[A-Za-z0-9]", w["w"]):
                words.append({"text": w["w"], "start": round(t + max(0, w["s"]), 3), "end": round(t + max(0.05, w["e"]), 3), "lid": lid})
    else:
        d = est(text, speed)
        ws = text.split()
        for i, w in enumerate(ws):
            words.append({"text": w.strip(".,:;?!\"'"), "start": round(t + d * i / len(ws), 3),
                          "end": round(t + d * (i + 0.9) / len(ws), 3), "lid": lid})
    LINE[lid] = dict(start=round(t, 3), end=round(t + d, 3), text=text, on=on, sec=cur, speed=speed, gap=gap if gap is not None else vo.GAP)
    ORDER.append(lid)
    if SECS[-1][2] is None:
        SECS[-1][2] = t
    t += d + (gap if gap is not None else vo.GAP)
VO_END = LINE[ORDER[-1]]["end"]
TOTAL = round(VO_END + vo.END_HOLD, 2)


def fmt(s, dec=False):
    m, r = divmod(max(0.0, s), 60)
    return f"{int(m)}:{r:04.1f}" if dec else f"{int(m)}:{int(r):02d}"


def pct(s):
    return f"{100 * s / TOTAL:.0f}%"


def T(lid):
    return LINE[lid]["start"]


# ------------------------------------------------------------------ stats
spoken = [LINE[i] for i in ORDER if LINE[i]["text"]]
all_words = sum(len(x["text"].split()) for x in spoken)
hook = [LINE[i] for i in ORDER if i.startswith("h")]
hook_words = sum(len(x["text"].split()) for x in hook)
sentences = []
for x in spoken:
    sentences += [s for s in re.split(r"(?<=[.?!])\s+", x["text"]) if s.strip()]
you_words = sum(len(YOU.findall(x["text"].lower())) for x in spoken)
you_sent = sum(1 for s in sentences if YOU.search(s.lower()))
num_re = re.compile(r"\b(\d[\d,.]*|one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|twenty-eight|forty|seventy|half)\b")
nums = sum(len(num_re.findall(x["text"].lower())) for x in spoken)
speech = sum(x["end"] - x["start"] for x in spoken)
STATS = dict(
    vo_words=all_words, hook_words=hook_words, hook_s=round(LINE["h10"]["end"], 1), name_s=round(T("h9"), 1),
    turn_s=round(T("h5"), 1), rule_s=round(T("h4"), 1),
    vo_span=round(VO_END, 1), total=TOTAL, eff_wpm=round(all_words / VO_END * 60, 1),
    speech_wpm=round(all_words / speech * 60, 1), hook_wpm=round(hook_words / LINE["h10"]["end"] * 60, 1),
    body_speech_wpm=round((all_words - hook_words) / (speech - sum(x["end"] - x["start"] for x in hook)) * 60, 1),
    avg_sentence=round(all_words / len(sentences), 1), sentences=len(sentences),
    you_pct_words=round(100 * you_words / all_words, 2), you_pct_sentences=round(100 * you_sent / len(sentences), 1),
    you_per_min=round(you_words / (VO_END / 60), 1), numbers_per_min=round(nums / (VO_END / 60), 1),
    first_rung=round(T("r1a"), 1), setup_pct=round(100 * T("r1a") / TOTAL, 1), promise=round(T("s4"), 1),
    exhibit7=round(T("s6"), 1), timing="Kokoro-82M am_michael on the Spark CPU, measured per line" if TTS else "estimate (177 wpm)",
    hook_speed=vo.HOOK_SPEED, body_speed=vo.BODY_SPEED,
)


import statistics  # noqa: E402
_rh = [T(i) for i in REHOOKS]
_rg = [b - a for a, b in zip([0.0] + _rh, _rh)]
_jk = [T(i) for i in JOKES]
_jg = [b - a for a, b in zip([0.0] + _jk, _jk + [VO_END])]
STATS.update(rehooks=", ".join(fmt(x) for x in _rh), rehook_median=round(statistics.median(_rg), 1), rehook_max=round(max(_rg), 1),
             jokes=", ".join(fmt(x) for x in _jk), joke_max=round(max(_jg), 1))


# ------------------------------------------------------------------ placeholder substitution
def subst(s):
    def rep(m):
        k, a = m.group(1), m.group(2)
        if k == "T":
            return fmt(T(a))
        if k == "D":
            return fmt(T(a), True)
        if k == "E":
            return fmt(LINE[a]["end"])
        if k == "P":
            return pct(T(a))
        if k == "S":
            return str(STATS[a])
        raise KeyError(m.group(0))
    return re.sub(r"\{([TDEPS]):([A-Za-z0-9_]+)\}", rep, s)


# ------------------------------------------------------------------ shots -> scene windows
def shot_start(sh):
    a = sh["at"]
    off = sh.get("off", 0.0)
    if a == "0":
        return 0.0
    base = LINE[a]["start"] if a in LINE else None
    lead = 0.0 if LINE[a].get("silence") else 0.15
    return round(max(0.0, base - lead + off), 3)


WIN = []
for i, sh in enumerate(SHOTS):
    s = 0.0 if i == 0 else shot_start(sh)
    WIN.append(s)
WIN.append(TOTAL)
for i in range(len(SHOTS)):
    assert WIN[i + 1] > WIN[i] + 0.5, (SHOTS[i]["id"], WIN[i], WIN[i + 1])

TIME_KEYS = {"at", "start", "end", "out", "t", "until"}


def resolve(obj, s0, dur, key=None):
    if isinstance(obj, dict):
        return {k: resolve(v, s0, dur, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolve(v, s0, dur, key) for v in obj]
    if isinstance(obj, str) and obj.startswith("@"):
        m = re.match(r"^@([A-Za-z0-9_]+)(\.end)?([+-]\d+(?:\.\d+)?)?$", obj)
        if not m:
            return obj
        lid, end, off = m.group(1), m.group(2), float(m.group(3) or 0)
        if lid == "end":
            g = s0 + dur
        elif lid == "start":
            g = s0
        else:
            g = LINE[lid]["end"] if end else LINE[lid]["start"]
        return round(max(0.0, min(dur - 0.05, g + off - s0)), 3)
    return obj


scenes = []
for i, sh in enumerate(SHOTS):
    s0, s1 = WIN[i], WIN[i + 1]
    dur = round(s1 - s0, 3)
    sc = {"id": sh["id"], "duration": dur, "background": sh["bg"], "layers": sh.get("layers", []),
          "notes": " ".join(LINE[l]["text"] for l in ORDER if LINE[l]["text"] and s0 - 0.01 <= LINE[l]["start"] < s1 - 0.01)}
    if sh.get("camera"):
        sc["camera"] = sh["camera"]
    if sh.get("trans"):
        sc["transitionIn"] = sh["trans"]
    if sh.get("grade"):
        sc["grade"] = sh["grade"]
    if sh.get("cues"):
        sc["sfx"] = [{"cue": c, "at": a, "volume": v} for c, a, v in sh["cues"]]
    if sh.get("captionY"):
        sc["captionY"] = sh["captionY"]
    scenes.append(resolve(sc, s0, dur))

EMPH_LINES = {"h6", "h10", "r1k", "r2b", "r3l", "r5k", "ri5", "p3", "p8", "t7", "b5"}
cap_words = []
for w in words:
    d = {"text": w["text"], "start": w["start"], "end": w["end"]}
    if w["lid"] in EMPH_LINES:
        d["emph"] = True
    cap_words.append(d)
for a, b in zip(cap_words, cap_words[1:]):
    if a["end"] > b["start"]:
        a["end"] = round(max(a["start"] + 0.02, b["start"] - 0.01), 3)

storyboard = {
    "version": 1, "id": SLUG, "title": "Why You'd Never Want To Meet A Leopard Seal", "format": "16:9", "fps": 30,
    "scenes": scenes,
    "captions": {"words": cap_words, "maxWords": 4, "maxChars": 22, "gapBreak": 0.45, "linger": 0.35,
                 "glue": ["leopard seal", "leopard seals", "sea ice", "Kirsty Brown", "Paul Nicklen", "Frank Wild", "Gareth Wood"],
                 "style": {"font": "display", "fontSize": 67, "color": "#ffffff", "highlight": "#ff5a4a",
                           "highlightMode": "none", "strokeWidth": 12, "uppercase": True, "y": 0.86}},
    "audio": {"voice": [{"src": f"episodes/{SLUG}/mix.wav", "start": 0, "volume": 1, "duration": round(VO_END + 0.5, 2)}],
              "music": [
                  {"src": "music/deep_ocean.m4a", "start": 0, "end": round(T("pause1"), 2), "volume": 0.3, "duckTo": 0.1, "fadeIn": 0.6, "fadeOut": 2.5},
                  {"src": "music/tension_pulse.m4a", "start": round(T("c1"), 2), "end": round(T("t1"), 2), "volume": 0.28, "duckTo": 0.1, "fadeIn": 1.5, "fadeOut": 1.0},
                  {"src": "music/documentary_pulse.m4a", "start": round(T("t1"), 2), "end": TOTAL, "volume": 0.28, "duckTo": 0.1, "fadeIn": 2.0, "fadeOut": 3.0},
              ],
              "sfx": [], "duckOn": "voice"},
    "overlays": {"grain": 0.04, "vignette": 0.2, "fadeIn": 0, "fadeOut": 1.0},
    "_built": {"by": f"backlog/explainer/{SLUG}/gen.py", "timing": STATS["timing"],
               "audio": f"studio/public/episodes/{SLUG}/mix.wav (Spark; build with pipeline.audio.make from the narration block in script.md)",
               "unbuilt_components": sorted({l["name"] for s in scenes for l in s["layers"] if l.get("type") == "component" and l["name"] in KIT_GAPS} |
                                            {s["background"]["name"] for s in scenes if s["background"].get("type") == "component" and s["background"]["name"] in KIT_GAPS})},
}
json.dump(storyboard, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1)

# ------------------------------------------------------------------ script.md
out = [subst(FRONT), subst(BODY_BEFORE_SCRIPT)]
out.append("## The script\n")
out.append(subst(
    "Layers: KICKER = ALL-CAPS white title top-centre; PUNCH = red caption for the beat's punch word only; TAG = small white label "
    "pinned to an object; CASE FILE = dossier board (NEW `explainer/CaseFile`, 7 slots) shown as a 2-3 s insert each time a slot is stamped. "
    "Burned-in word captions follow the VO (core `captions`). Timestamps are line starts on the measured Kokoro timeline "
    f"(hook speed {vo.HOOK_SPEED}, body {vo.BODY_SPEED}); `(SILENCE n s)` lines hold the picture with no VO.\n\n"
    "Hook first line: \"You're kneeling on Antarctic sea ice, camera up.\"\n"
    "Hook first visual: wide surface split, low sun; YOU kneels on a white floe with a camera to the eye; under the waterline a long spotted "
    "silhouette slides beneath the ice keel, left to right. The viewer sees it; YOU does not. Sound: ice creak + the sub-bass trill.\n"))
for key, heading, start in SECS:
    out.append(f"\n### [{fmt(start)}] {subst(heading)}\n")
    for lid in ORDER:
        x = LINE[lid]
        if x["sec"] != key:
            continue
        if x["text"] is None:
            out.append(f"[{fmt(x['start'], True)}] (SILENCE {x['silence']:.1f} s)\nON SCREEN: {subst(x['on'])}")
        else:
            out.append(f"[{fmt(x['start'], True)}] {x['text']}" + (f"\nON SCREEN: {subst(x['on'])}" if x["on"] else ""))
out.append("")
out.append(subst(AFTER_SCRIPT))
out.append("\n## Shot list\n")
out.append(subst(KIT_GAPS["_intro"]))
out.append("\n| # | t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX (existing `studio/public/sfx` names) |\n|---|---|---|---|---|---|---|")
for i, sh in enumerate(SHOTS):
    out.append(f"| {i + 1} | {fmt(WIN[i], True)} | {fmt(WIN[i + 1], True)} | {sh['type']} | {subst(sh['desc'])} | {sh['cam']} | {sh['sfx']} |")
out.append("")
out.append("## Narration (TTS source)\n")
out.append("Read by `pipeline.audio.make` (Kokoro am_michael). One paragraph per shot so scene cuts land just before each paragraph's first word.\n")
out.append("```narration")
out.append(f"[speed: {vo.HOOK_SPEED}]")
para = []
for i, sh in enumerate(SHOTS):
    s0, s1 = WIN[i], WIN[i + 1]
    seg = []
    for lid in ORDER:
        x = LINE[lid]
        if s0 - 0.01 <= x["start"] < s1 - 0.01:
            if x["text"] is None:
                seg.append(f"[pause: {x['silence']:.1f}]")
            else:
                if lid == "s1":
                    seg.insert(0, f"[speed: {vo.BODY_SPEED}]")
                seg.append(x["text"])
    if seg:
        para.append(" ".join(seg))
out.append("\n\n".join(para))
out.append("```\n")
open(os.path.join(HERE, "script.md"), "w").write("\n".join(out))

json.dump({"stats": STATS, "lines": {k: {"start": v["start"], "end": v["end"]} for k, v in LINE.items()},
           "shots": [{"id": sh["id"], "start": WIN[i], "end": WIN[i + 1]} for i, sh in enumerate(SHOTS)]},
          open(os.path.join(HERE, "timeline.json"), "w"), indent=1)
print(json.dumps(STATS, indent=1))
print("shots", len(SHOTS), "scenes", len(scenes), "total", TOTAL)
