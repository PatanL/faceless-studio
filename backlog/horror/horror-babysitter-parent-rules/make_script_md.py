#!/usr/bin/env python3
"""Writes script.md for horror-babysitter-parent-rules from script_head.md (hand-written prose) + measured timing.

The timed script table, the narration block and the shot list are generated from lines.py, timing.json and
storyboard.json, so script.md never drifts from the measured Kokoro timings.
usage: python3 gen_storyboard.py && python3 make_script_md.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lines as L  # noqa: E402

T = json.load(open(os.path.join(HERE, "timing.json")))
SB = json.load(open(os.path.join(HERE, "storyboard.json")))
HEAD = open(os.path.join(HERE, "script_head.md")).read()
TAIL = open(os.path.join(HERE, "script_tail.md")).read()


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


starts = {ln["id"]: ln for ln in T["lines"]}
sil = T["silences"]
rows = ["| t | beat | voice | VO (word for word) | on screen |", "|---|---|---|---|---|"]
beat = ""
for e in L.V:
    if e[0] == "#":
        beat = e[1]
        continue
    if e[0] == "~":
        a, b = sil[e[1]]
        rows.append(f"| {mmss(a)}-{mmss(b)} | {beat} | (silence {e[2]:.1f} s) | | {e[3].get('screen', '')} |")
        continue
    lid, spk, text, opts = e
    ln = starts[lid]
    who = "Ivy (narr.)" if spk == "N" else L.SPEAKER_NAME[spk]
    rows.append(f"| {mmss(ln['start'])}-{mmss(ln['end'])} | {beat} | {who} | {text} | {opts.get('screen', '')} |")
timed = "\n".join(rows)

# Narration block: parser-valid for pipeline/audio/script.py (the single-voice fallback). One [music:] only; the two
# dropouts are hush= on cues; no [cut]; SFX names that exist in studio/public/sfx. The real build is multi-voice
# (lines.VOICES/FX) with the storyboard's _sfx_cues; see "Voice and audio".
MARK = {
    "n1": ("[music: dread] ", " [sfx: phone_buzz_long vol=-10]"),
    "c1": ("", " [sfx: glitch vol=-12]"),
    "n4": ("", " [sfx: click]"),
    "k1": ("", " [sfx: stinger @0.1 vol=-10]"),
    "n6": ("", " [sfx: click]"),
    "n12": ("", " [sfx: glitch]"),
    "n13": ("", ""),
    "n14": ("", " [sfx: ding] [pause: 0.7]"),
    "n15": ("", " [sfx: knock3 hush=1.6 wait]"),
    "n17": ("", " [sfx: click]"),
    "n18": ("", " [sfx: message_send]"),
    "n21": ("", " [sfx: static vol=-14]"),
    "n23": ("", " [sfx: heartbeat_slow hush=3.0] [pause: 3.0]"),
    "n27": ("[sfx: phone_buzz] ", ""),
    "n29": ("", " [sfx: message_pop]"),
    "n30": ("[sfx: phone_buzz_long] ", ""),
    "n31": ("", " [sfx: breath vol=-16 hush=1.2] [pause: 1.2]"),
}
paras, cur = [], []
for e in L.V:
    if e[0] == "#":
        if cur:
            paras.append(" ".join(cur))
            cur = []
        continue
    if e[0] == "~":
        continue
    lid, spk, text, opts = e
    pre, post = MARK.get(lid, ("", ""))
    cur.append(pre + text + post)
if cur:
    paras.append(" ".join(cur))
narr = "```narration\n" + "\n\n".join(paras) + "\n```"

shots = ["| # | t_start | dur | beat | layers (kit names; svg = inline art in gen_storyboard.py) |", "|---|---|---|---|---|"]
for i, (sc, meta) in enumerate(zip(SB["scenes"], T["scenes"])):
    names = []
    bg = sc["background"]
    if bg.get("type") == "component":
        names.append(bg["name"].replace("horror/", "") + " (bg)")
    for l_ in sc["layers"]:
        if l_["type"] == "component":
            names.append(l_["name"].replace("horror/", ""))
        elif l_["type"] == "svg":
            names.append("svg")
        elif l_["type"] in ("text", "circle", "rect"):
            names.append(l_["type"])
    compact = []
    for n in names:
        if compact and compact[-1][0] == n:
            compact[-1][1] += 1
        else:
            compact.append([n, 1])
    lay = ", ".join(f"{n}x{k}" if k > 1 else n for n, k in compact)
    shots.append(f"| {sc['id']} | {meta['start']:.2f} | {sc['duration']:.2f} | {meta['beat']} | {lay} |")
shot_md = "\n".join(shots)

out = (HEAD.replace("{{TIMED}}", timed).replace("{{NARRATION}}", narr).replace("{{SHOTS}}", shot_md)
       + TAIL)
open(os.path.join(HERE, "script.md"), "w").write(out)
print("script.md written", len(out), "chars")
