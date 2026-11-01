"""Build the measured timeline, pacing stats and storyboard.json for horror-two-emergency-alerts.

usage: python3 build.py [--tables]        (stdlib only; safe on the Mac)
inputs : lines.py (the spoken lines), tts_durations.json (Kokoro per-line durations measured on the Spark CPU)
outputs: timeline.json, storyboard.json; --tables prints the markdown tables that script.md carries.

Visuals use only components the horror kit registers today (HandPhone chat, Hallway, FrontDoor, LivingRoom,
Protagonist, Vignette, Glitch, Flicker, Darkness, Heartbeat) plus core layers (rect / circle / text / svg).
Everything the kit cannot do yet is drawn from core layers so no shared kit file is edited:
  - the red emergency-alert cards and the lock / call / home screens sit on a static phone frame (core layers);
  - the peephole with a phone pressed to the lens is one svg with its own circular clipPath;
  - the zoomed sender header (C-O-U-N-T-V), the bubble ECU, the floor plan, the chain and the 4-inch door gap
    are svg / text cards.
Timing is word-anchored: every cue is at("<line>:<word>") on the Kokoro word times, so a re-measure re-times it.
"""
from __future__ import annotations

import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lines as L  # noqa: E402

D = json.load(open(os.path.join(HERE, "tts_durations.json")))["lines"]
EP = "horror-two-emergency-alerts"
TITLE = "Every Phone On My Floor Got An Emergency Alert"
LEAD_IN = 0.12
KNOCK3_SLOW = [0.01, 0.96, 1.91]   # knock transients inside studio/public/sfx/knock3_slow.wav (measured)

# ------------------------------------------------------------------ timeline


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def word_times(lid: str, text: str, start: float) -> list[dict]:
    """Align the script's words to Kokoro tokens by consuming normalised characters."""
    toks = [w for w in D[lid]["words"] if norm(w["w"])]
    say = L_SAY.get(lid)
    words = (say or text).split()
    out, ti = [], 0
    dur = D[lid]["dur"]
    for w in words:
        target = norm(w)
        s = e = None
        acc = ""
        while ti < len(toks) and len(acc) < len(target):
            if s is None:
                s = toks[ti]["s"]
            acc += norm(toks[ti]["w"])
            e = toks[ti]["e"]
            ti += 1
        if s is None:
            s = e = (out[-1]["e"] - start) if out else 0.0
        s = max(0.0, min(s, dur))
        e = max(s + 0.04, min(e, dur + 0.05))
        out.append({"w": w, "s": round(start + s, 3), "e": round(start + e, 3)})
    return out


L_SAY = {e[0]: e[3]["say"] for e in L.V if e[0] not in ("#", "~") and "say" in e[3]}


def build_timeline():
    items, beats, t = [], [], LEAD_IN
    seq = L.V
    for i, e in enumerate(seq):
        if e[0] == "#":
            beats.append({"key": e[1], "title": e[2], "t": round(t, 3)})
            continue
        if e[0] == "~":
            _, sid, secs, opts = e
            items.append({"kind": "silence", "id": sid, "start": round(t, 3), "end": round(t + secs, 3), "dur": secs,
                          "opts": opts, "beat": beats[-1]["key"]})
            t += secs
            continue
        lid, spk, text, opts = e
        dur = D[lid]["dur"]
        words = word_times(lid, text, t)
        items.append({"kind": "line", "id": lid, "spk": spk, "text": text, "start": round(t, 3), "end": round(t + dur, 3),
                      "dur": dur, "words": words, "opts": opts, "beat": beats[-1]["key"]})
        t += dur
        nxt = next((x for x in seq[i + 1:] if x[0] != "#"), None)
        if "gap" in opts:
            g = opts["gap"]
        elif nxt is None or nxt[0] == "~":
            g = 0.1
        else:
            g = L.TURN_GAP if nxt[1] != spk else L.GAP
        t += g
    return items, beats, round(t, 3)


ITEMS, BEATS, RUNTIME = build_timeline()
BY = {it["id"]: it for it in ITEMS}


def at(ref: str, off: float = 0.0) -> float:
    """'n3' = line start, 'n3.end', 'n3:word' = first word starting with it, 'n3:word#2' = 2nd match."""
    if ":" in ref:
        lid, w = ref.split(":", 1)
        n = 1
        if "#" in w:
            w, n = w.split("#")
            n = int(n)
        ws = BY[lid]["words"]
        hits = [x for x in ws if norm(x["w"]) == norm(w)] or [x for x in ws if norm(x["w"]).startswith(norm(w))]
        return round(hits[n - 1]["s"] + off, 3)
    if ref.endswith(".end"):
        return round(BY[ref[:-4]]["end"] + off, 3)
    return round(BY[ref]["start"] + off, 3)


def sfx_cues():
    cues = []
    for it in ITEMS:
        for cue, off, db in it["opts"].get("sfx", []):
            if isinstance(off, str):
                if off.startswith("end"):
                    t = it["end"] + (float(off[4:]) if len(off) > 3 else 0.0)
                elif off.startswith("w:"):
                    t = at(f"{it['id']}:{off[2:]}")
                else:
                    raise ValueError(off)
            else:
                t = it["start"] + off
            cues.append({"cue": cue, "at": round(max(0.0, t), 3), "volume": round(0.8 * 10 ** (db / 20), 3)})
    # the chain keeps straining under the call (the running clock), every ~2.3 s from the hit to the twist
    t, stop = at("n42:hit") + 2.3, at("d6")
    while t < stop - 0.5:
        cues.append({"cue": "chain_strain", "at": round(t, 3), "volume": 0.22})
        t += 2.3
    return sorted(cues, key=lambda c: c["at"])


# ------------------------------------------------------------------ captions

EMPH = {"screamed", "not", "even", "emergency", "services.", "error.", "alone.", "knock.", "fake.", "v.", "word.", "stop.",
        "failed.", "alerts.", "stopped.", "first.", "doors.", "yet.", "three.", "right.", "door.", "josie", "never",
        "lock", "screen.", "open.", "dark.", "rang.", "chain.", "v?", "ours.", "with", "me.", "voice.", "mistake.", "occupant.",
        "open", "door."}


def captions():
    words = []
    for it in ITEMS:
        if it["kind"] != "line":
            continue
        cap = it["opts"].get("cap", {})
        for w in it["words"]:
            shown = cap.get(w["w"], w["w"])
            if it["id"] == "n12" and w["w"] == "County.":
                shown = "County."
            if shown == "":
                if words:
                    words[-1]["end"] = w["e"]
                continue
            d = {"text": shown, "start": w["s"], "end": w["e"]}
            if w["w"].lower() in EMPH or it["spk"] == "A":
                d["emph"] = True
            words.append(d)
    return words


# ------------------------------------------------------------------ stats

NUMBERS = ["nine (minutes)", "three (doors down)", "three (alert three)", "three (slow knocks)", "four (inches)",
           "eleven-F (Tess)", "eleven-F (alert 4)", "one (occupant)"]


def stats():
    lines = [it for it in ITEMS if it["kind"] == "line"]
    words = sum(len(it["text"].split()) for it in lines)
    speech = sum(it["dur"] for it in lines)
    sil = sum(it["dur"] for it in ITEMS if it["kind"] == "silence")
    sents = []
    for it in lines:
        for s in re.split(r"(?<=[.!?])\s+", it["text"].strip()):
            if s:
                sents.append((it["spk"], len(s.split()), s))
    lens = [n for _, n, _ in sents]
    nlens = [n for spk, n, _ in sents if spk == "N"]
    you_s = [s for _, _, s in sents if re.search(r"\b(you|your)\b", s, re.I)]
    you_w = sum(len(re.findall(r"\b(you|your)\b", it["text"], re.I)) for it in lines)
    by_spk = {}
    for it in lines:
        by_spk[it["spk"]] = by_spk.get(it["spk"], 0) + len(it["text"].split())
    return {
        "runtime_s": RUNTIME,
        "speech_s": round(speech, 2),
        "timed_silence_s": round(sil, 2),
        "gaps_s": round(RUNTIME - speech - sil, 2),
        "words": words,
        "words_by_speaker": by_spk,
        "wpm_overall": round(words / (RUNTIME / 60), 1),
        "wpm_speaking": round(words / (speech / 60), 1),
        "wpm_alert_lines": round(sum(len(BY[k]["text"].split()) for k in ("a1", "a2", "a3", "a4")) /
                                 (sum(BY[k]["dur"] for k in ("a1", "a2", "a3", "a4")) / 60), 1),
        "sentences": len(sents),
        "sentence_median_all": statistics.median(lens),
        "sentence_median_narrator": statistics.median(nlens),
        "punch_share_all": round(sum(1 for n in lens if n <= 4) / len(lens), 3),
        "you_sentence_share": round(len(you_s) / len(sents), 3),
        "you_per_100_words": round(100 * you_w / words, 2),
        "spoken_numbers": NUMBERS,
        "numbers_per_min": round(len(NUMBERS) / (RUNTIME / 60), 1),
        "line1_words": len(BY["n1"]["text"].split()),
        "rule_word_s": at("a1:Open"),
        "core_hook_words": len(BY["n1"]["text"].split()) + len(BY["a1"]["text"].split()),
        "core_hook_s": round(BY["a1"]["end"], 2),
        "contradiction_s": at("a2:Previous"),
        "words_first_10s": sum(1 for it in lines for w in it["words"] if w["s"] < 10),
        "timed_silences": [{"id": it["id"], "start": it["start"], "dur": it["dur"]} for it in ITEMS if it["kind"] == "silence"],
    }


def jolts():
    J = [
        ("frame 0: red alert on the lock screen", 0.0), ("every phone screamed", at("n1:screamed")),
        ("rule: not even emergency services", at("a1:Not")), ("second alert", at("n2")),
        ("contradiction: sent in error, let them in", at("a2:Previous")), ("glint on the v (visual)", at("a2:Please")),
        ("one phone goes off down the hall", at("n3:off.")), ("knock", at("n4.end")), ("chat lights up", at("n5")),
        ("they asked how many live here", at("n6:They")), ("which one is real?", at("n7:So")),
        ("my question ignored", at("n10")), ("sender check", at("n11")), ("C-O-U-N-T-V", at("n12:C.")),
        ("fake", at("n13")), ("closer phone + knock", at("n14:off,")), ("Raf: All done. Painless.", at("n15:All")),
        ("Lorna's phone, three doors down", at("n16")), ("Lorna: same words", at("n17:All")),
        ("word for word", at("n18")), ("call failed", at("n19:failed.")), ("only the chat and the alerts work", at("n20:Only")),
        ("Ines: don't open, they're not", at("n21:Don't")), ("that was the whole message", at("n22")),
        ("her phone through my wall + knock", at("n23:screamed,")), ("Ines: All done. Painless.", at("n24:All")),
        ("knocking stops", at("n25")), ("creak in the silence", BY["q1"]["start"] + 1.7),
        ("pattern: phone screams before the knock", at("n26")), ("they were picking doors", at("n27:They#2")),
        ("mine hadn't screamed yet (flash)", at("n28:yet.")), ("phone won't turn off", at("n29:wouldn't")),
        ("mine screams", at("n30")), ("spelled right", at("n31:Spelled")), ("admit county staff", at("a3:Admit")),
        ("three slow knocks at my door", at("n32")), ("the real sender says open", at("n33")),
        ("voice knows Josie", at("d1:Josie")), ("hand sliding the chain (near-miss)", at("n34")),
        ("the call never went through", at("n35:never")), ("peephole", at("n36")), ("my lock screen", at("n37:lock")),
        ("heartbeat in the held silence", BY["q2"]["start"] + 0.8), ("every door stood open", at("n38:Behind")),
        ("number in alert three", at("n40")), ("the only call that rang", at("n41:rang.")),
        ("key in my lock", at("n42:key")), ("door hits the chain", at("n42:hit")), ("'dispatcher' answers", at("d2")),
        ("v alert is fake: good catch", at("d3:Good")), ("'that one's ours'", at("d4")),
        ("screws coming out", at("n43:screws")), ("is anyone with you?", at("d5:anyone")), ("just me", at("t3:Just")),
        ("same voice, phone and door", at("d6")), ("the v was never a mistake", at("n45")),
        ("phone lights up", at("n46")), ("alert 4: my name, one occupant", at("a4")), ("open the door (cut)", at("a4:Open")),
    ]
    ts = sorted(t for _, t in J)
    gaps = [b - a for a, b in zip(ts, ts[1:])] + [RUNTIME - ts[-1]]
    return J, round(statistics.median(gaps), 2), round(max(gaps), 2)


# ------------------------------------------------------------------ storyboard helpers

W, H = 1080, 1920
RED = "#e0262f"
AMBER = "#f2b33d"
GREEN = "#4ade80"
INK = "#0b0d12"
CARD = "#1a0f12"
GREY = "#9a9fa8"

P_CX, P_CY, P_W, P_H = 540, 1120, 800, 1600     # static phone frame (bottom bleeds off frame like a held phone)
S_X0, S_Y0, S_W = 160, 340, 760                 # screen box top-left x/y and width


def rect(x, y, w, h, fill, radius=0, **kw):
    d = {"type": "rect", "x": x, "y": y, "width": w, "height": h, "fill": fill, "radius": radius}
    d.update(kw)
    return d


def circle(x, y, r, fill, **kw):
    d = {"type": "circle", "x": x, "y": y, "width": 2 * r, "height": 2 * r, "fill": fill}
    d.update(kw)
    return d


def text(s, x, y, size=40, color="#ffffff", weight=800, align="center", **kw):
    d = {"type": "text", "text": s, "x": x, "y": y, "fontSize": size, "color": color, "weight": weight, "align": align,
         "font": "body"}
    if align == "left":
        d["anchorX"] = 0
    elif align == "right":
        d["anchorX"] = 1
    d.update(kw)
    return d


def svg(markup, x, y, w, h, **kw):
    d = {"type": "svg", "markup": markup, "x": x, "y": y, "width": w, "height": h}
    d.update(kw)
    return d


def comp(name, props=None, **kw):
    d = {"type": "component", "name": name, "props": props or {}}
    d.update(kw)
    return d


def full(name, props=None, z=0, **kw):
    return comp(name, props, x=540, y=960, width=W, height=H, z=z, **kw)


def timed(layers, start=None, end=None, z=None):
    out = []
    for l in layers:
        l = dict(l)
        if start is not None:
            l["start"] = round(max(0.0, start), 3)
        if end is not None:
            l["end"] = round(end, 3)
        if z is not None:
            l["z"] = l.get("z", 0) + z
        out.append(l)
    return out


def scene(sid, t0, t1, layers, bg=INK, camera=None, trans=None, grade=None, notes=None, captionY=None):
    d = {"id": sid, "duration": round(t1 - t0, 3), "background": {"type": "color", "color": bg}, "layers": layers}
    if camera:
        d["camera"] = camera
    if trans:
        d["transitionIn"] = trans
    if grade:
        d["grade"] = grade
    if notes:
        d["notes"] = notes
    if captionY is not None:
        d["captionY"] = captionY
    return d


def cam(*kf, shake=None):
    c = {"keyframes": [{"t": round(max(0.0, t), 3), "zoom": z, "x": f"{x:.2f}%", "y": f"{y:.2f}%", "ease": e} for t, z, x, y, e in kf]}
    if shake:
        c["shake"] = [{"at": round(max(0.0, a), 3), "duration": d, "amplitude": amp} for a, d, amp in shake]
    return c


NIGHT = {"brightness": 0.95, "contrast": 1.08, "saturate": 0.85, "tint": "#1d3a52", "tintOpacity": 0.18}

# ---- Tess's wallpaper (ownable: it reappears inside the peephole and on the bookend)
WALLPAPER = (
    '<svg viewBox="0 0 760 1560" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#2a2150"/><stop offset="0.55" stop-color="#6b3f6e"/><stop offset="1" stop-color="#14202e"/>'
    '</linearGradient></defs><rect width="760" height="1560" fill="url(#g)"/>'
    '<circle cx="560" cy="430" r="90" fill="#f3e3c3"/><circle cx="600" cy="400" r="86" fill="#4a3166"/>'
    '<path d="M 0 1040 Q 190 960 380 1010 Q 560 1060 760 980 L 760 1560 L 0 1560 Z" fill="#101a26"/>'
    '<path d="M 0 1120 Q 260 1080 520 1130 Q 650 1150 760 1120" stroke="#f3e3c3" stroke-width="5" fill="none" opacity="0.35"/>'
    '<path d="M 300 1180 l 60 0 l -20 26 l -24 0 Z" fill="#f3e3c3" opacity="0.8"/></svg>')

TRI = ('<svg viewBox="0 0 40 36" xmlns="http://www.w3.org/2000/svg"><path d="M 20 2 L 38 34 L 2 34 Z" fill="#ffffff"/>'
       '<rect x="18" y="12" width="4" height="12" fill="#e0262f"/><rect x="18" y="27" width="4" height="4" fill="#e0262f"/></svg>')

ALERTS = {
    "a1": {"sender": "Lindhurst County Emergency Management", "h": 330,
           "body": ["SHELTER IN PLACE.", "Do not open your door for anyone,", "including emergency services."],
           "foot": "Further instructions by alert only."},
    "a2": {"sender": "Lindhurst Countv Emergency Management", "h": 280,
           "body": ["Previous alert sent in error.", "County staff are visiting every", "unit. Please let them in."], "foot": None},
    "a3": {"sender": "Lindhurst County Emergency Management", "h": 280,
           "body": ["Previous alerts sent in error.", "Admit county staff."], "foot": "Questions? Call 555-0148"},
    "a4": {"sender": "Lindhurst County Emergency Management", "h": 280,
           "body": ["TESS AVILA · 11F", "ONE OCCUPANT.", "Open the door."], "foot": None},
}
CARD_W, CARD_GAP, STACK_TOP = 700, 18, 700


def alert_card(key, cx, cy, z=0, scale=1.0, mini=False):
    """Stylised in-world alert card (NOT a pixel copy of iOS/Android WEA): dark card, red header strip with a
    custom triangle, a sender line (in-world UI), body, optional footer. Centre at (cx, cy)."""
    a = ALERTS[key]
    s = scale
    w, h = CARD_W * s, a["h"] * s
    top = cy - h / 2
    left = cx - w / 2
    out = [rect(cx, cy, w, h, CARD, radius=28 * s, stroke="#5a1a20", strokeWidth=3 * s, z=z,
                shadow="0 10px 30px rgba(0,0,0,.55)"),
           rect(cx, top + 30 * s, w, 60 * s, RED, radius=28 * s, z=z + 1),
           rect(cx, top + 48 * s, w, 24 * s, RED, z=z + 1),
           svg(TRI, left + 44 * s, top + 30 * s, 34 * s, 30 * s, z=z + 2),
           text("EMERGENCY ALERT", left + 74 * s, top + 31 * s, 28 * s, "#ffffff", 900, "left", z=z + 2),
           text("now", left + w - 26 * s, top + 31 * s, 24 * s, "#ffd9db", 700, "right", z=z + 2),
           text(a["sender"], left + 28 * s, top + 92 * s, 24 * s, GREY, 700, "left", z=z + 2)]
    y = top + 140 * s
    for ln in a["body"]:
        out.append(text(ln, left + 28 * s, y, 34 * s, "#ffffff", 800, "left", z=z + 2))
        y += 44 * s
    if a["foot"]:
        out.append(text(a["foot"], left + 28 * s, top + h - 34 * s, 24 * s, "#ffb3b8", 700, "left", z=z + 2))
    return out


def phone_frame(clock="2:47", wallpaper=True, z=0, date="Sunday, November 1"):
    out = [rect(P_CX, P_CY, P_W, P_H, "#15171c", radius=96, stroke="#2c3038", strokeWidth=8, z=z),
           rect(P_CX, P_CY, P_W - 40, P_H - 40, INK, radius=76, z=z + 1)]
    if wallpaper:
        out.append(svg(WALLPAPER, P_CX, P_CY, P_W - 40, P_H - 40, z=z + 2, opacity=0.9))
    out += [text("▮▮▮", S_X0 + 40, S_Y0 + 30, 22, "#e8e8ea", 700, "left", z=z + 3),
            text("23%", S_X0 + S_W - 40, S_Y0 + 30, 24, "#e8e8ea", 700, "right", z=z + 3)]
    return out


def lock_clock(clock, z=0, date="Sunday, November 1"):
    return [text(date, 540, S_Y0 + 120, 34, "#f1eef7", 700, z=z + 3),
            text(clock, 540, S_Y0 + 240, 170, "#f7f3ff", 800, z=z + 3)]


def lock_screen(t0, t1, clock_track, arrivals, z=0, glint_at=None, underline=None):
    """clock_track [(t, '2:47')], arrivals [(key, t_local)] in arrival order (t<0 = already there)."""
    lay = timed(phone_frame(z=z), t0, t1)
    for i, (tt, c) in enumerate(clock_track):
        te = clock_track[i + 1][0] if i + 1 < len(clock_track) else t1
        lay += timed(lock_clock(c, z=z), max(t0, tt), te)
    times = sorted({max(0.0, ta) for _, ta in arrivals})
    for idx, (key, ta) in enumerate(arrivals):
        kf = []
        for tt in times:
            present = [k for k, a in arrivals if max(0.0, a) <= tt]
            if key not in present:
                continue
            order = list(reversed(present))
            y = STACK_TOP
            for k in order:
                h = ALERTS[k]["h"]
                if k == key:
                    break
                y += h + CARD_GAP
            cy = y + ALERTS[key]["h"] / 2
            kf.append((tt, cy))
        cy0 = kf[0][1]
        card = alert_card(key, 540, cy0, z=z + 10 + idx * 10)
        st = max(t0, ta) if ta > 0 else t0
        for l in card:
            l = dict(l)
            dy = l["y"] - cy0
            l["keyframes"] = [{"t": round(tt, 3), "y": round(cy + dy, 1), "ease": "out"} for tt, cy in kf]
            if ta > 0:
                l["enter"] = {"type": "drop", "duration": 0.22, "distance": 120}
                l["start"] = round(st, 3)
            l["end"] = round(t1, 3)
            lay.append(l)
    if glint_at is not None:
        # 0.3 s hairline glint over the 'v' of Countv in alert 2's sender line (no VO): the fair-play plant
        y2 = STACK_TOP + 92 - ALERTS["a2"]["h"] / 2 + ALERTS["a2"]["h"] / 2
        lay.append(rect(540 - CARD_W / 2 + 28 + 203, y2 + 2, 22, 30, "rgba(255,255,255,0.0)", stroke="#fff6c8", strokeWidth=2,
                        radius=4, z=z + 60, start=round(glint_at, 3), end=round(glint_at + 0.3, 3),
                        keyframes=[{"t": round(glint_at, 3), "opacity": 0}, {"t": round(glint_at + 0.1, 3), "opacity": 1},
                                   {"t": round(glint_at + 0.3, 3), "opacity": 0}]))
    if underline is not None:
        ua, key, slot = underline
        yy = STACK_TOP + 92 + 18 + slot
        lay.append(rect(540 - CARD_W / 2 + 28 + 206, yy, 18, 4, GREEN, z=z + 60, start=round(ua, 3), end=round(t1, 3),
                        enter={"type": "wipeRight", "duration": 0.25}))
    return lay


def call_screen(t0, t1, name, sub_track, z=0, end_button=True, clock="2:59"):
    """Outgoing call (no Accept button, one red End button). sub_track [(t, text, colour)]."""
    lay = timed(phone_frame(z=z, wallpaper=False), t0, t1)
    lay += timed([rect(P_CX, P_CY, P_W - 40, P_H - 40, "#11151c", radius=76, z=z + 2),
                  circle(540, S_Y0 + 300, 90, "#2a3240", z=z + 3), text(name[0], 540, S_Y0 + 300, 80, "#c9d2de", 800, z=z + 4),
                  text(name, 540, S_Y0 + 450, 52, "#ffffff", 800, z=z + 3, maxWidth=680)], t0, t1)
    for i, (tt, s, col) in enumerate(sub_track):
        te = sub_track[i + 1][0] if i + 1 < len(sub_track) else t1
        lay += timed([text(s, 540, S_Y0 + 520, 36, col, 700, z=z + 3)], max(t0, tt), te)
    if end_button:
        lay += timed([circle(540, 1640, 62, RED, z=z + 3), text("✕", 540, 1640, 52, "#ffffff", 900, z=z + 4)], t0, t1)
    return lay


def timer_track(t_conn, t_end, start_s=1):
    """Running call timer; t_conn is scene-local (negative when the call connected in an earlier scene)."""
    out, s, t = [], start_s, t_conn
    while t < t_end:
        if t + 1.0 > 0:
            out.append((max(0.0, t), f"00:{s:02d}", "#9fe3b0"))
        s += 1
        t += 1.0
    return out


TESS_COLORS = {"hair": "#6e3420", "top": "#7b6a2e", "topShade": "#5a4d20"}


def tess(expr="scared", exprs=None, pose="phone", lookX=0.0, lookY=0.3, light="phone", z=40, width=1150, talk=None, **kw):
    p = {"pose": pose, "exprs": exprs or [{"t": 0, "e": expr}], "lookX": lookX, "lookY": lookY, "light": light, "blink": True,
         "colors": TESS_COLORS}
    if talk:
        p["talk"] = talk
    p.update(kw.pop("props", {}))
    y = kw.pop("y", "100%")
    x = kw.pop("x", "50%")
    return comp("horror/Protagonist", p, x=x, y=y, anchorY=1, width=width, height=round(width * 1.52), z=z, depth=0, **kw)


MEMBERS = {"Raf": {"color": "#4f7a9a", "initials": "R"}, "Ines": {"color": "#a0607a", "initials": "I"},
           "Lorna": {"color": "#7a8a4f", "initials": "L"}}


def handphone(chat, clock="2:58", tremble=1.5, tilt=-3):
    chat = {"theme": "dark", "scale": 1.25, "clock": clock, "battery": 23, "title": "Ashby Tower · Floor 11", "count": 12, **chat}
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": 0.6, "tilt": tilt, "tremble": tremble, "side": "right",
         "phone": {"members": MEMBERS, "mode": "chat", "chat": chat}, "thumbY": 0.94, "thumbReach": 0.1}
    return comp("horror/HandPhone", p, z=10)


def blurred(name, props, z=0, blur=10, opacity=0.6):
    return comp(name, props, x=540, y=960, width=W, height=H, z=z, blur=blur, opacity=opacity)


def msgs(thread, t0):
    return [{**m, "at": round(m["at"] - t0, 3)} for m in thread]


# ---- custom svg art (storyboard-only, no kit edit)

def red_pulse(x, y, t, z=30, r=120):
    """A red glow that blooms under/through a door when that door's phone screams."""
    return circle(x, y, r, "rgba(255,40,50,0.55)", z=z, blur=40, blend="screen", start=round(max(0.0, t), 3),
                  end=round(t + 1.5, 3), keyframes=[{"t": round(max(0.0, t), 3), "opacity": 0, "scale": 0.6},
                                                   {"t": round(t + 0.2, 3), "opacity": 1, "scale": 1.0},
                                                   {"t": round(t + 1.5, 3), "opacity": 0, "scale": 1.3}])


PEEPHOLE = (
    '<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><defs>'
    '<clipPath id="lens"><circle cx="540" cy="900" r="440"/></clipPath>'
    '<radialGradient id="fish" cx="0.5" cy="0.5" r="0.5"><stop offset="0.6" stop-color="#000" stop-opacity="0"/>'
    '<stop offset="1" stop-color="#000" stop-opacity="0.85"/></radialGradient>'
    '<linearGradient id="hall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3326"/><stop offset="1" stop-color="#15130f"/></linearGradient>'
    '</defs><rect width="1080" height="1920" fill="#030304"/>'
    '<g clip-path="url(#lens)">'
    '<rect x="80" y="440" width="920" height="920" fill="url(#hall)"/>'
    '<ellipse cx="540" cy="520" rx="90" ry="26" fill="#fff1c8" opacity="0.9"/>'
    # open doors down the hall, black inside (left and right walls, fisheye-bent)
    '<g fill="#000" stroke="#5b513f" stroke-width="8">'
    '<path d="M 150 620 Q 175 860 150 1120 L 250 1060 Q 262 860 250 680 Z"/>'
    '<path d="M 300 720 Q 312 870 300 1010 L 360 980 Q 366 870 360 750 Z"/>'
    '<path d="M 930 620 Q 905 860 930 1120 L 830 1060 Q 818 860 830 680 Z"/>'
    '<path d="M 780 720 Q 768 870 780 1010 L 720 980 Q 714 870 720 750 Z"/>'
    '<path d="M 500 790 L 580 790 L 580 930 L 500 930 Z"/></g>'
    # the man: backlit, cap brim, county jacket shoulders
    '<path d="M 250 1400 Q 280 1060 430 1010 Q 540 980 650 1010 Q 800 1060 830 1400 Z" fill="#0b1018"/>'
    '<path d="M 420 1015 Q 540 1060 660 1015" stroke="#c9b37a" stroke-width="10" fill="none" opacity="0.55"/>'
    '<ellipse cx="540" cy="860" rx="120" ry="140" fill="#07090d"/>'
    '<path d="M 410 790 Q 540 700 670 790 L 720 812 Q 540 790 380 812 Z" fill="#0d121a"/>'
    '</g>'
    '<circle cx="540" cy="900" r="440" fill="url(#fish)"/>'
    '<circle cx="540" cy="900" r="446" fill="none" stroke="#2a2a2e" stroke-width="16"/>'
    '<path d="M 300 620 Q 380 520 520 500" stroke="#ffffff" stroke-width="10" fill="none" opacity="0.12"/></svg>')


def held_phone_svg(clock="3:09"):
    """Her own lock screen on the man's phone, pressed flat to the lens (wallpaper + three red cards + clock)."""
    return (
        '<svg viewBox="0 0 300 600" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="w" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#2a2150"/><stop offset="0.55" stop-color="#6b3f6e"/><stop offset="1" stop-color="#14202e"/></linearGradient></defs>'
        '<rect x="0" y="0" width="300" height="600" rx="40" fill="#111"/>'
        '<rect x="12" y="12" width="276" height="576" rx="32" fill="url(#w)"/>'
        '<circle cx="215" cy="150" r="34" fill="#f3e3c3"/><circle cx="230" cy="139" r="32" fill="#4a3166"/>'
        '<path d="M 12 410 Q 90 380 150 398 Q 220 418 288 388 L 288 588 L 12 588 Z" fill="#101a26"/>'
        f'<text x="150" y="110" font-family="Montserrat, sans-serif" font-weight="800" font-size="62" fill="#f7f3ff" text-anchor="middle">{clock}</text>'
        '<g><rect x="28" y="230" width="244" height="64" rx="12" fill="#1a0f12"/><rect x="28" y="230" width="244" height="18" rx="9" fill="#e0262f"/>'
        '<rect x="28" y="306" width="244" height="64" rx="12" fill="#1a0f12"/><rect x="28" y="306" width="244" height="18" rx="9" fill="#e0262f"/>'
        '<rect x="28" y="382" width="244" height="64" rx="12" fill="#1a0f12"/><rect x="28" y="382" width="244" height="18" rx="9" fill="#e0262f"/>'
        '<g fill="#ffffff" opacity="0.8"><rect x="40" y="260" width="170" height="8" rx="4"/><rect x="40" y="276" width="120" height="8" rx="4"/>'
        '<rect x="40" y="336" width="180" height="8" rx="4"/><rect x="40" y="352" width="100" height="8" rx="4"/>'
        '<rect x="40" y="412" width="160" height="8" rx="4"/><rect x="40" y="428" width="130" height="8" rx="4"/></g></g>'
        '<path d="M 30 40 L 120 40" stroke="#ffffff" stroke-width="6" opacity="0.15"/></svg>')


DOOR_GAP = (
    '<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><rect width="1080" height="1920" fill="#0a0c10"/>'
    '<rect x="120" y="180" width="760" height="1740" fill="#1c1f26" stroke="#050608" stroke-width="14"/>'
    '<rect x="880" y="180" width="70" height="1740" fill="#f2d79a"/>'
    '<rect x="880" y="180" width="70" height="1740" fill="#fff4d6" opacity="0.5"/>'
    '<rect x="950" y="160" width="130" height="1760" fill="#14161b"/>'
    '<rect x="800" y="820" width="60" height="130" rx="10" fill="#8f8a80"/>'
    '<rect x="990" y="820" width="50" height="130" rx="10" fill="#8f8a80"/>'
    '<path d="M 830 860 Q 915 890 1010 860" stroke="#cfc8b8" stroke-width="14" fill="none" stroke-dasharray="22 10"/>'
    '<rect x="760" y="1060" width="56" height="150" rx="14" fill="#a8a296"/></svg>')

CHAIN_ECU = (
    '<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><rect width="1080" height="1920" fill="#1b1e25"/>'
    '<rect x="0" y="0" width="300" height="1920" fill="#121419"/><rect x="290" y="0" width="16" height="1920" fill="#050608"/>'
    '<rect x="560" y="860" width="420" height="80" rx="14" fill="#8f8a80" stroke="#3a3833" stroke-width="6"/>'
    '<rect x="580" y="886" width="380" height="28" rx="12" fill="#2b2a27"/>'
    '<rect x="160" y="840" width="90" height="140" rx="14" fill="#8f8a80" stroke="#3a3833" stroke-width="6"/>'
    '<circle cx="205" cy="870" r="10" fill="#3a3833"/><circle cx="205" cy="950" r="10" fill="#3a3833"/>'
    '<circle cx="600" cy="900" r="10" fill="#3a3833"/><circle cx="940" cy="900" r="10" fill="#3a3833"/></svg>')
CHAIN_LINKS = ('<svg viewBox="0 0 500 120" xmlns="http://www.w3.org/2000/svg"><path d="M 0 60 Q 250 120 500 60" '
               'stroke="#cfc8b8" stroke-width="18" fill="none" stroke-dasharray="34 12"/><circle cx="500" cy="60" r="26" fill="#cfc8b8"/></svg>')
HAND = ('<svg viewBox="0 0 300 260" xmlns="http://www.w3.org/2000/svg"><path d="M 20 260 Q 0 120 70 70 Q 120 40 170 60 L 250 40 '
        'Q 290 40 280 80 L 200 110 Q 230 140 210 190 Q 190 250 160 260 Z" fill="#e2b896" stroke="#3a2a22" stroke-width="8"/>'
        '<path d="M 60 260 L 70 190" stroke="#7b6a2e" stroke-width="60"/></svg>')

FLOORPLAN = (
    '<svg viewBox="0 0 900 1300" xmlns="http://www.w3.org/2000/svg"><rect width="900" height="1300" rx="30" fill="#10141b"/>'
    '<rect x="360" y="60" width="180" height="1180" fill="#1b212b"/>'
    '<g fill="#232a35" stroke="#3b4554" stroke-width="6">'
    '<rect x="80" y="90" width="260" height="240"/><rect x="560" y="90" width="260" height="240"/>'
    '<rect x="80" y="370" width="260" height="240"/><rect x="560" y="370" width="260" height="240"/>'
    '<rect x="80" y="650" width="260" height="240"/><rect x="560" y="650" width="260" height="240"/>'
    '<rect x="80" y="930" width="260" height="240"/><rect x="560" y="930" width="260" height="240"/></g>'
    '<g font-family="Montserrat, sans-serif" font-weight="800" font-size="40" fill="#8a93a3" text-anchor="middle">'
    '<text x="210" y="225">RAF</text><text x="690" y="505">LORNA</text><text x="210" y="785">INES</text>'
    '<text x="690" y="225">11B</text><text x="210" y="505">11C</text><text x="690" y="785">11E</text>'
    '<text x="690" y="1065">11G</text><text x="210" y="1065" fill="#f7f3ff">ME</text></g></svg>')
FP = {"x": 540, "y": 1040, "w": 900, "h": 1300}


def fp_xy(px, py):
    return round(FP["x"] - FP["w"] / 2 + px, 1), round(FP["y"] - FP["h"] / 2 + py, 1)


ROOMS = {"raf": fp_xy(210, 210), "lorna": fp_xy(690, 490), "ines": fp_xy(210, 770), "me": fp_xy(210, 1050)}

FRAME_ART = ('<svg viewBox="0 0 300 380" xmlns="http://www.w3.org/2000/svg"><rect x="8" y="8" width="284" height="364" fill="#3a2c22" '
             'stroke="#120c08" stroke-width="10"/><rect x="34" y="34" width="232" height="312" fill="#5c6f7a"/>'
             '<circle cx="190" cy="120" r="40" fill="#e8d9b0"/><path d="M 34 260 Q 120 200 266 250 L 266 346 L 34 346 Z" fill="#33424a"/></svg>')


# ------------------------------------------------------------------ scenes

def build_scenes():
    S = []
    # chat thread (absolute times); the read-out speaks each bubble as it pops
    thread = [
        {"from": "Lorna", "text": "anyone else's phone just scream??", "at": -40},
        {"from": "Raf", "text": "county jackets. super polite. they asked how many live here", "at": at("n6:County")},
        {"from": "Ines", "text": "so which one is real??", "at": at("n7:So")},
        {"from": "Lorna", "text": "the second obviously. first was a glitch", "at": at("n8:The")},
        {"me": True, "text": "then why did the first one say not even emergency services?", "at": at("n9.end")},
        {"from": "Raf", "text": "All done. Painless. Open up when they knock.", "at": at("n15:All")},
        {"from": "Lorna", "text": "All done. Painless. Open up when they knock.", "at": at("n17:All")},
        {"from": "Ines", "text": "don't open. they're not", "at": at("n21:Don't")},
        {"from": "Ines", "text": "All done. Painless. Open up when they knock.", "at": at("n24:All")},
    ]

    def chat_scene(sid, t0, t1, cam_=None, typing=None, notes=None, draft=None, unread=None):
        m = [x for x in thread if x["at"] < t1 - 0.05]
        chat = {"messages": msgs(m, t0)}
        if typing:
            chat["typing"] = [{"from": f, "at": round(a - t0, 3), "until": round(u - t0, 3)} for f, a, u in typing]
        if draft:
            chat["draft"] = draft
        lay = [blurred("horror/Bedroom", {"lamp": 0.0, "phoneGlow": True}, z=0, blur=12, opacity=0.5),
               handphone(chat), comp("horror/Vignette", {"amount": 0.5}, depth=0, z=50)]
        S.append(scene(sid, t0, t1, lay, camera=cam_, grade=NIGHT, notes=notes))

    # 01 COVER + hook: lock screen, alert 1 live at frame 0 ------------------------------------------
    t0, t1 = 0.0, at("n2")
    lay = [blurred("horror/Bedroom", {"lamp": 0.0, "phoneGlow": True}, z=0, blur=14, opacity=0.5)]
    lay += lock_screen(0, t1 - t0, [(0, "2:47")], [("a1", -1)], z=5)
    lay += [comp("horror/Vignette", {"amount": 0.55, "color": "120,0,0"}, depth=0, z=80)]
    a1s = at("a1") - t0
    S.append(scene("s01_cover_alert1", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (a1s, 1.06, 50, 52, "out"), (t1 - t0, 1.32, 50, 47, "out"),
                              shake=[(0.05, 0.35, 14)]),
                   notes="COVER FRAME = frame 0: lock screen 2:47 with the red alert card already up; phone glow on a dark bedroom. "
                         "During a1 the camera pushes onto the body so 'including emergency services' and 'Further instructions by "
                         "alert only' read; caption card NOT EVEN EMERGENCY SERVICES sits in the top band ~3-5 s."))

    # 02 alert 2 drops on top (Countv; 0.3 s glint on the v at ~3 s into the scene, no VO) ------------
    t0, t1 = at("n2"), at("n3")
    lay = [blurred("horror/Bedroom", {"lamp": 0.0, "phoneGlow": True}, z=0, blur=14, opacity=0.5)]
    lay += lock_screen(0, t1 - t0, [(0, "2:56")], [("a1", -1), ("a2", 0.15)], z=5, glint_at=at("a2:Please") - t0)
    lay += [comp("horror/Vignette", {"amount": 0.55, "color": "120,0,0"}, depth=0, z=80)]
    S.append(scene("s02_alert2_stacks", t0, t1, lay, grade=NIGHT, trans={"type": "whip", "duration": 0.25, "direction": "up"},
                   camera=cam((0, 1.0, 50, 50, "linear"), (1.0, 1.12, 50, 45, "out"), (t1 - t0, 1.2, 50, 44, "linear"),
                              shake=[(0.15, 0.3, 12)]),
                   notes="Alert 2 stacks over alert 1 (clock 2:56). Sender line reads 'Lindhurst Countv Emergency Management'. "
                         "A 0.3 s hairline glint on the v (fair-play plant, no VO)."))

    # 03 hallway: one phone screams at the far end, then a knock --------------------------------------
    t0, t1 = at("n3"), at("n5")
    tone, kn = at("n3:off.") - t0, at("n4.end") - t0
    lay = [full("horror/Hallway", {"lights": 2, "flicker": 0.15, "endDoor": True, "runner": True, "figure": 0.6, "figureDepth": 0.95}),
           red_pulse(540, 1010, tone, r=90), comp("horror/Vignette", {"amount": 0.6}, depth=0, z=50)]
    S.append(scene("s03_hall_far_phone", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.12, 50, 48, "linear"), shake=[(kn, 0.2, 6)]),
                   notes="The far door glows red for a beat (its phone screaming through the hall), then a tiny figure knocks there. "
                         "Rung 1 of the ladder: phone first, then the knock. (Check the red pulse sits on Hallway's end door on a still.)"))

    # 04 floor chat: Raf / Ines / Lorna / me, then nobody answers ---------------------------------------
    chat_scene("s04_floor_chat", at("n5"), at("n11"), typing=[("Lorna", at("n10") + 0.1, at("n10") + 1.0)],
               cam_=cam((0, 1.0, 50, 50, "linear"), (at("n11") - at("n5"), 1.08, 50, 55, "linear")),
               notes="Chat 'Ashby Tower · Floor 11' (12 members). Raf's plant ('they asked how many live here'), Ines's viewer-proxy "
                     "question, Lorna defends the fake alert, my question sends, typing dots under Lorna start and stop.")

    # 05 the sender card: C-O-U-N-T-V letter by letter, then FAKE -----------------------------------
    t0, t1 = at("n11"), at("n14")
    lay = [rect(540, 960, 1080, 1920, "#0e0a0c"),
           text("SENT BY", 540, 520, 34, GREY, 800),
           text("Lindhurst County", 540, 640, 82, "#d9dde4", 800),
           rect(540, 690, 620, 2, "#2a2f38"),
           text("Lindhurst", 540, 900, 82, "#f7f3ff", 800)]
    letters = ["C", "O", "U", "N", "T", "V"]
    for i, ch in enumerate(letters):
        x = 190 + i * 140
        tt = at(f"n12:{ch}.") - t0
        lay.append(text(ch, x, 1080, 150, "#3a3f48", 900))
        lay.append(text(ch, x, 1080, 150, RED if ch == "V" else "#ffffff", 900, start=round(tt, 3), z=2,
                        enter={"type": "pop", "duration": 0.16}))
    tv = at("n12:V.") - t0
    lay.append(circle(190 + 5 * 140, 1080, 105, "rgba(0,0,0,0)", stroke=RED, strokeWidth=8, start=round(tv, 3), z=3,
                      enter={"type": "zoomIn", "duration": 0.2}))
    t13 = at("n13") - t0
    lay += timed([rect(540, 1420, 760, 150, "rgba(0,0,0,0)", stroke=RED, strokeWidth=10, radius=18, rotate=-6, z=4),
                  text("FAKE", 540, 1420, 110, RED, 900, rotate=-6, z=5)], t13, None)
    lay.append(comp("horror/Glitch", {"cues": [{"at": round(tv, 3), "duration": 0.15, "amount": 0.4}], "seed": "v1"}, depth=0, z=60))
    S.append(scene("s05_countv_card", t0, t1, lay, trans={"type": "glitch", "duration": 0.2},
                   camera=cam((0, 1.0, 50, 50, "linear"), (tv, 1.06, 62, 52, "out"), (t1 - t0, 1.0, 50, 55, "out")),
                   notes="Zoomed sender header built from core text layers (kit has no per-glyph highlight): each letter lights on "
                         "its tick (word-anchored to the Kokoro letter times), the V lights red and gets a ring, FAKE stamps on n13."))

    # 06 hallway rung 2 ----------------------------------------------------------------------------
    t0, t1 = at("n14"), at("n15")
    lay = [full("horror/Hallway", {"lights": 2, "flicker": 0.2, "endDoor": True, "runner": True, "figure": 0.7, "figureDepth": 0.75}),
           red_pulse(380, 1060, at("n14:off,") - t0, r=110), comp("horror/Vignette", {"amount": 0.6}, depth=0, z=50)]
    S.append(scene("s06_hall_rung2", t0, t1, lay, grade=NIGHT, camera=cam((0, 1.04, 50, 50, "linear"), (t1 - t0, 1.1, 50, 50, "linear"),
                   shake=[(at("n14:Knock.") - t0, 0.2, 8)]), notes="Rung 2: a closer door glows red, then the knock."))

    chat_scene("s07_chat_raf_painless", at("n15"), at("n16"),
               cam_=cam((0, 1.0, 50, 50, "linear"), (at("n16") - at("n15"), 1.1, 50, 58, "out")),
               notes="Raf's second post: 'All done. Painless. Open up when they knock.'")

    t0, t1 = at("n16"), at("n17")
    lay = [full("horror/Hallway", {"lights": 1, "flicker": 0.25, "endDoor": True, "runner": True, "figure": 0.8, "figureDepth": 0.55}),
           red_pulse(760, 1100, 0.05, r=130), comp("horror/Vignette", {"amount": 0.65}, depth=0, z=50)]
    S.append(scene("s08_hall_rung3_lorna", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.06, 50, 50, "linear"), (t1 - t0, 1.12, 50, 50, "linear"), shake=[(at("n16:Knock.") - t0, 0.2, 10)]),
                   notes="Rung 3: Lorna's door, three doors down, glows red; knock."))

    chat_scene("s09_chat_lorna_painless", at("n17"), at("n18"),
               cam_=cam((0, 1.0, 50, 50, "linear"), (at("n18") - at("n17"), 1.18, 50, 60, "out")),
               notes="Lorna's identical post stacks under Raf's.")

    # 10 bubble ECU: word for word, even the full stop -----------------------------------------------
    t0, t1 = at("n18"), at("n19")
    lay = [rect(540, 960, 1080, 1920, "#0d1016")]
    for k, (who, col, y) in enumerate((("Raf", "#4f7a9a", 760), ("Lorna", "#7a8a4f", 1120))):
        lay += [circle(140, y - 40, 40, col), text(who[0], 140, y - 40, 36, "#fff", 900),
                text(who, 210, y - 160, 30, GREY, 800, "left"),
                rect(560, y + 10, 760, 270, "#232a35", radius=36),
                text("All done.", 210, y - 60, 46, "#f1f3f6", 800, "left"),
                text("Painless.", 210, y + 0, 46, "#f1f3f6", 800, "left"),
                text("Open up when they knock.", 210, y + 60, 46, "#f1f3f6", 800, "left"),
                circle(848, y + 74, 22, "rgba(0,0,0,0)", stroke=RED, strokeWidth=4, start=round(0.5 + 0.25 * k, 3),
                       enter={"type": "zoomIn", "duration": 0.15})]
    S.append(scene("s10_bubbles_ecu", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.1, 52, 52, "out")),
                   notes="Bubble replicas as core layers (positions are ours, so the rings land): both full stops ringed red. "
                         "Verify the ring x (806) against Montserrat 800 46 px on a still."))

    # 11 isolation: outgoing call fails, SMS stuck, only chat + alerts alive ------------------------------
    t0, t1 = at("n19"), at("n21")
    tf, ts = at("n19:failed.") - t0, at("n19:My") - t0
    tn = at("n20") - t0
    lay = call_screen(0, ts, "Josie", [(0, "Calling…", "#c9d2de"), (tf, "Call Failed", "#ff6b6b")], z=5)
    lay += timed(phone_frame(z=5, wallpaper=False) +
                 [rect(P_CX, P_CY, P_W - 40, P_H - 40, "#0f1218", radius=76, z=7), text("Josie", 540, S_Y0 + 120, 44, "#fff", 800, z=8),
                  rect(700, 900, 300, 90, "#2f6fe0", radius=40, z=8), text("pick up pls", 700, 900, 34, "#fff", 800, z=9),
                  text("Sending…", 840, 965, 26, GREY, 700, "right", z=9)], ts, tn)
    home = phone_frame(z=5) + [rect(P_CX, P_CY, P_W - 40, P_H - 40, "rgba(5,6,9,0.55)", radius=76, z=7)]
    for i in range(12):
        x, y = 255 + (i % 4) * 190, 640 + (i // 4) * 210
        live = i in (5, 6)
        home.append(rect(x, y, 130, 130, ("#2a9d5c" if i == 5 else RED) if live else "#3a3f48", radius=32, z=8,
                         opacity=1 if live else 0.35))
    home += [text("Floor chat", 255 + 190, 640 + 210 + 100, 24, "#e8e8ea", 700, z=9),
             text("Alerts", 255 + 2 * 190, 640 + 210 + 100, 24, "#e8e8ea", 700, z=9),
             text("No Service", 540, S_Y0 + 80, 30, "#ff8a8a", 800, z=9)]
    lay += timed(home, tn, t1 - t0)
    S.append(scene("s11_isolation", t0, t1, lay, grade=NIGHT, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.06, 50, 50, "linear")),
                   notes="Outgoing-call screen drawn from core layers (kit CallScreen is incoming-only): 'Calling…' -> 'Call Failed', "
                         "then the SMS stuck on 'Sending…', then the home screen greyed except two icons: Floor chat and Alerts."))

    chat_scene("s12_ines_cut_off", at("n21"), at("n23"),
               cam_=cam((0, 1.0, 50, 50, "linear"), (at("n23") - at("n21"), 1.2, 50, 62, "linear")),
               notes="The lone ally: Ines (next door) posts 'don't open. they're not' and the bubble ends mid-line. Hold on it.")

    # 13 the shared wall: her phone screams through it, then the knock next door ----------------------------
    t0, t1 = at("n23"), at("n24")
    tt, kk = at("n23:screamed,") - t0, at("n23.end", 0.15) - t0
    lay = [full("horror/LivingRoom", {"lamp": 0.1, "tv": "off"}),
           svg(FRAME_ART, 540, 760, 300, 380, z=5, keyframes=[{"t": round(kk, 3), "rotate": 0}, {"t": round(kk + 0.08, 3), "rotate": -5},
                                                              {"t": round(kk + 0.18, 3), "rotate": 4}, {"t": round(kk + 0.3, 3), "rotate": -2},
                                                              {"t": round(kk + 0.5, 3), "rotate": 0}]),
           red_pulse(120, 900, tt, z=6, r=260), comp("horror/Vignette", {"amount": 0.6}, depth=0, z=50)]
    S.append(scene("s13_shared_wall", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.08, 50, 46, "linear"), shake=[(kk, 0.5, 18)]),
                   notes="Her shared wall: red glow bleeds through on Ines's alert, the framed print rattles on the knock next door."))

    chat_scene("s14_ines_painless", at("n24"), at("n25"),
               cam_=cam((0, 1.16, 50, 60, "linear"), (at("n25") - at("n24"), 1.0, 50, 50, "out")),
               notes="Third identical post, from the ally who warned her. Pull out so all three identical bubbles show.")

    # 15 the lull: knocking stops, 3 s of silence ----------------------------------------------------------
    t0, t1 = at("n25"), at("n26")
    lay = [full("horror/FrontDoor", {"chain": "on", "hallLight": 0.0}),
           tess("terrified", pose="phone", lookX=0.3, y="112%", width=1100, props={"blink": False}),
           comp("horror/Darkness", {"x": 0.52, "y": 0.78, "radius": 0.28, "darkness": 0.85}, depth=0, z=45),
           comp("horror/Vignette", {"amount": 0.6}, depth=0, z=50)]
    S.append(scene("s15_silence", t0, t1, lay, grade=NIGHT, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.04, 50, 52, "linear")),
                   notes="TIMED SILENCE 3.0 s after 'Then the knocking stopped.' Music hard-muted (music track ends here), room tone, "
                         "one breath, one floor creak at +1.7 s. Tess low on the floor, back to her chained door, phone glow only."))

    # 16 the midpoint turn: floor plan, doors light in order, then the amber flash on "yet" ------------------------
    t0, t1 = at("n26"), at("n29")
    lay = [rect(540, 960, 1080, 1920, "#0b0e13"), svg(FLOORPLAN, FP["x"], FP["y"], FP["w"], FP["h"], z=1)]
    seqs = [("raf", 0.2), ("lorna", 0.75), ("ines", 1.3)]
    for room, tt in seqs:
        x, y = ROOMS[room]
        lay += [rect(x, y, 240, 220, "rgba(224,38,47,0.55)", z=2, start=tt, enter={"type": "fade", "duration": 0.15}),
                text("✆", x - 80, y - 60, 44, "#ffffff", 900, z=3, start=tt),
                text("KNOCK", x, y + 70, 30, "#ffffff", 900, z=3, start=round(tt + 0.35, 3), enter={"type": "pop", "duration": 0.15})]
    yet = at("n28:yet.") - t0
    mx, my = ROOMS["me"]
    lay += [rect(mx, my, 240, 220, "rgba(0,0,0,0)", stroke="#f7f3ff", strokeWidth=6, z=3,
                 idle=[{"type": "pulse", "amount": 0.04, "speed": 1.0}]),
            rect(mx, my, 240, 220, "rgba(224,38,47,0.7)", z=4, start=round(yet + 0.3, 3),
                 keyframes=[{"t": round(yet + 0.3, 3), "opacity": 0}, {"t": round(yet + 0.6, 3), "opacity": 1},
                            {"t": round(yet + 0.9, 3), "opacity": 0.3}, {"t": round(yet + 1.2, 3), "opacity": 1}]),
            rect(540, 960, 1080, 1920, AMBER, z=70, depth=0, start=round(yet, 3), end=round(yet + 0.3, 3),
                 keyframes=[{"t": round(yet, 3), "opacity": 1}, {"t": round(yet + 0.3, 3), "opacity": 0}]),
            comp("horror/Glitch", {"cues": [{"at": round(yet + 0.28, 3), "duration": 0.4, "amount": 0.6}], "seed": "m1"}, depth=0, z=71)]
    S.append(scene("s16_midpoint_plan", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 42, "linear"), (yet, 1.05, 50, 48, "inOut"), (t1 - t0, 1.35, 40, 68, "out"),
                              shake=[(yet, 0.3, 22)]),
                   notes="MIDPOINT TURN (B8 / S6 'in your place'): top-down floor plan; Raf, Lorna, Ines light red in order with a "
                         "phone glyph, then KNOCK. The pattern says the alerts were choosing doors. THE ONLY FULL-FRAME COLOUR FLASH: "
                         "amber 0.3 s on 'yet', then her door ('ME') pulses red. Camera pushes onto her door."))

    # 17 the power button: it won't turn off ---------------------------------------------------------------
    t0, t1 = at("n29"), at("n30")
    tw = at("n29:wouldn't") - t0
    lay = timed(phone_frame(z=5), 0, t1 - t0)
    lay += timed([rect(P_CX, P_CY, P_W - 40, P_H - 40, "rgba(10,12,16,0.75)", radius=76, z=8),
                  rect(540, 700, 620, 120, "#2a2f38", radius=60, z=9), circle(250, 700, 52, "#ffffff", z=10,
                  keyframes=[{"t": 0.2, "x": 250}, {"t": round(tw, 3), "x": 520, "ease": "out"}, {"t": round(tw + 0.05, 3), "x": 250, "ease": "step"}]),
                  text("slide to power off", 600, 700, 30, "#c9d2de", 700, z=9)], 0, tw + 0.3)
    lay += timed(lock_clock("3:07", z=5), tw + 0.3, t1 - t0)
    lay.append(comp("horror/Glitch", {"cues": [{"at": round(tw, 3), "duration": 0.3, "amount": 0.7}], "seed": "p1"}, depth=0, z=60))
    S.append(scene("s17_power_button", t0, t1, lay, grade=NIGHT, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.05, 50, 45, "linear")),
                   notes="Power-off slider: the knob slides, glitches and snaps back to the lock screen. They're inside the phone."))

    # 18 PEAK CONTACT: my phone screams, alert 3 spelled right --------------------------------------------
    t0, t1 = at("n30"), at("n32")
    lay = [blurred("horror/FrontDoor", {"chain": "on", "hallLight": 0.4}, z=0, blur=14, opacity=0.45)]
    lay += lock_screen(0, t1 - t0, [(0, "3:08")], [("a1", -1), ("a2", -1), ("a3", 0.08)], z=5,
                       underline=(at("n31:Spelled") - t0, "a3", 0))
    lay += [comp("horror/Vignette", {"amount": 0.6, "color": "140,0,0", "pulse": 1.4}, depth=0, z=80)]
    S.append(scene("s18_my_phone_screams", t0, t1, lay, grade=NIGHT, trans={"type": "whip", "duration": 0.2, "direction": "down"},
                   camera=cam((0, 1.0, 50, 50, "linear"), (1.0, 1.1, 50, 42, "out"), (t1 - t0, 1.18, 50, 40, "linear"),
                              shake=[(0.08, 0.6, 18)]),
                   notes="PEAK CONTACT (the pattern pays): her own phone screams. Alert 3 lands from the correctly spelled sender "
                         "(green underline under the y): 'Previous alerts sent in error. Admit county staff.' Footer: 'Questions? "
                         "Call 555-0148' (fictional 555-01xx range)."))

    # 19 three slow knocks at my door + the dilemma line ----------------------------------------------------
    t0, t1 = at("n32"), at("d1")
    lay = [full("horror/FrontDoor", {"knocks": KNOCK3_SLOW, "chain": "on", "feet": True, "hallLight": 0.8, "peepholeGlow": True}),
           comp("horror/Vignette", {"amount": 0.55}, depth=0, z=50)]
    S.append(scene("s19_my_door_knocks", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.08, 50, 46, "linear"),
                              shake=[(k, 0.2, 12) for k in KNOCK3_SLOW]),
                   notes="Three slow knocks timed to the transients inside knock3_slow.wav (0.01/0.96/1.91 s); feet shadow under the door."))

    # 20 the voice at the door (persuasive, specific) -----------------------------------------------------
    t0, t1 = at("d1"), at("n34")
    lay = [full("horror/FrontDoor", {"chain": "on", "feet": True, "hallLight": 0.8, "peepholeGlow": True}),
           tess("worried", exprs=[{"t": 0, "e": "worried"}, {"t": round(at("d1:Josie") - t0, 3), "e": "shocked"}], pose="idle",
                lookX=0.7, light="none", width=900, x="22%", y="104%"),
           comp("horror/Vignette", {"amount": 0.5}, depth=0, z=50)]
    S.append(scene("s20_door_voice", t0, t1, lay, grade=NIGHT, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.06, 46, 50, "linear")),
                   notes="Door voice (am_michael, door fx: lowpass 1.3 kHz): warm, specific, names her sister Josie. Tess in the "
                         "lower left, turns shocked on 'Josie'."))

    # 21 near-miss: her hand slides the chain ----------------------------------------------------------------
    t0, t1 = at("n34"), at("n35")
    lay = [svg(CHAIN_ECU, 540, 960, 1080, 1920),
           svg(CHAIN_LINKS, 430, 905, 520, 125, z=2, keyframes=[{"t": 0.1, "x": 430}, {"t": round(t1 - t0, 3), "x": 560, "ease": "out"}]),
           svg(HAND, 760, 1010, 300, 260, z=3, keyframes=[{"t": 0.1, "x": 760}, {"t": round(t1 - t0, 3), "x": 860, "ease": "out"}]),
           comp("horror/Vignette", {"amount": 0.6}, depth=0, z=50)]
    S.append(scene("s21_chain_slide", t0, t1, lay, camera=cam((0, 1.1, 60, 50, "linear"), (t1 - t0, 1.18, 64, 50, "linear")),
                   notes="NEAR-MISS: ECU on the chain track; her hand slides the chain knob halfway toward the open end."))

    # 22 the tell: the call never went through -----------------------------------------------------------------
    t0, t1 = at("n35"), at("n36")
    tn = at("n35:My") - t0
    lay = [rect(540, 960, 1080, 1920, INK)]
    lay += call_screen(tn, t1 - t0, "Josie", [(tn, "Call Failed", "#ff6b6b")], z=5)
    lay += timed([svg(CHAIN_ECU, 540, 960, 1080, 1920, z=1),
                  svg(CHAIN_LINKS, 560, 905, 520, 125, z=2), svg(HAND, 860, 1010, 300, 260, z=3)], 0, tn)
    lay.append(comp("horror/Glitch", {"cues": [{"at": round(tn, 3), "duration": 0.2, "amount": 0.5}], "seed": "t1"}, depth=0, z=60))
    S.append(scene("s22_call_never_went_through", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.18, 64, 50, "linear"), (tn, 1.0, 50, 50, "step"), (t1 - t0, 1.08, 50, 40, "out")),
                   notes="The tell: a flash insert of the 'Call Failed' screen from s11. Josie never heard from her, so how do they know Josie?"))

    # 23 PEEPHOLE: the phone pressed to the lens; then the 4 s held silence (SCARIEST IMAGE) -------------------------
    t0, t1 = at("n36"), at("n39")
    hold0 = BY["q2"]["start"] - t0
    hold1 = BY["q2"]["end"] - t0
    tl = at("n37:lock") - t0
    lay = [svg(PEEPHOLE, 540, 960, 1080, 1920, z=0),
           svg(held_phone_svg("3:09"), 540, 1000, 300, 600, z=2,
               keyframes=[{"t": 0.0, "scale": 0.5, "y": 1080}, {"t": round(at("n37:pressing") - t0, 3), "scale": 0.55, "y": 1080},
                          {"t": round(tl, 3), "scale": 1.0, "y": 960, "ease": "out"}]),
           circle(540, 900, 440, "rgba(0,0,0,0)", stroke="#000", strokeWidth=40, z=3, blur=18),
           comp("horror/Flicker", {"strength": 0.08, "from": round(hold0, 3)}, depth=0, z=40),
           comp("horror/Vignette", {"amount": 0.5}, depth=0, z=50)]
    S.append(scene("s23_peephole_held_phone", t0, t1, lay, trans={"type": "dipBlack", "duration": 0.2},
                   camera=cam((0, 1.0, 50, 47, "linear"), (tl, 1.05, 50, 50, "out"), (hold0, 1.42, 50, 50, "out"),
                              (hold1, 1.46, 50, 50, "linear"), (hold1 + 0.6, 1.0, 50, 47, "out"), (t1 - t0, 1.0, 50, 47, "linear")),
                   notes="Peephole as ONE svg with its own clipPath (the kit Peephole can't hold a prop): a backlit man in a cap "
                         "(not the recurring Mr. Hale puppet), every hall door open and black behind him. He presses a phone flat to "
                         "the lens: HER lock screen (same wallpaper as frame 0, three red cards, 3:09). SCARIEST IMAGE: the 4.0 s "
                         "timed silence holds ~1.45x on the phone (one heartbeat at +0.8 s, faint flicker, no VO, music muted), then "
                         "pulls back on n38 to show the open doors. Clock 3:09 matches her own phone."))

    # 24 chain back on --------------------------------------------------------------------------------------
    t0, t1 = at("n39"), at("n40")
    lay = [svg(CHAIN_ECU, 540, 960, 1080, 1920),
           svg(CHAIN_LINKS, 560, 905, 520, 125, z=2, keyframes=[{"t": 0.0, "x": 560}, {"t": round(t1 - t0 - 0.1, 3), "x": 430, "ease": "in"}]),
           svg(HAND, 860, 1010, 300, 260, z=3, keyframes=[{"t": 0.0, "x": 860}, {"t": round(t1 - t0 - 0.1, 3), "x": 760, "ease": "in"}])]
    S.append(scene("s24_chain_back", t0, t1, lay, camera=cam((0, 1.18, 60, 50, "linear"), (t1 - t0, 1.1, 58, 50, "linear"),
                   shake=[(t1 - t0 - 0.1, 0.15, 8)]), notes="Chain slammed back to the locked end (click)."))

    # 25 the number in alert three: the only call that rings ---------------------------------------------------
    t0, t1 = at("n40"), at("n42")
    tc = at("n40:I") - t0
    lay = lock_screen(0, tc, [(0, "3:09")], [("a1", -1), ("a2", -1), ("a3", -1)], z=5)
    lay += timed([circle(540 - CARD_W / 2 + 200, STACK_TOP + ALERTS["a3"]["h"] - 34, 40, "rgba(255,255,255,0.3)", z=90,
                         keyframes=[{"t": round(tc - 0.3, 3), "scale": 0.4, "opacity": 0.9}, {"t": round(tc, 3), "scale": 1.6, "opacity": 0}])],
                 tc - 0.3, tc)
    lay += call_screen(tc, t1 - t0, "555-0148", [(tc, "Calling…", "#c9d2de"), (at("n41:rang.") - t0, "Ringing…", "#9fe3b0")], z=5)
    S.append(scene("s25_call_the_number", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.25, 50, 30, "linear"), (tc, 1.0, 50, 50, "step"), (t1 - t0, 1.06, 50, 48, "linear")),
                   notes="Push onto alert 3's footer, tap '555-0148', outgoing call. Everything else failed all night; this rings."))

    # 26 key in the lock, door to the chain -------------------------------------------------------------------
    t0, t1 = at("n42"), at("d2")
    th = at("n42:hit") - t0
    lay = [full("horror/FrontDoor", {"chain": "on", "hallLight": 0.9, "feet": True}, z=0, end=round(at("n42:swung") - t0, 3)),
           svg(DOOR_GAP, 540, 960, 1080, 1920, z=1, start=round(at("n42:swung") - t0, 3), enter={"type": "fade", "duration": 0.12}),
           comp("horror/Vignette", {"amount": 0.55}, depth=0, z=50)]
    S.append(scene("s26_key_door_hits_chain", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (th, 1.05, 70, 50, "out"), (t1 - t0, 1.1, 74, 50, "linear"),
                              shake=[(at("n42:turned") - t0, 0.1, 4), (th, 0.35, 24)]),
                   notes="A key turns (they have keys), the door swings in four inches and slams against the chain. DOOR_GAP svg: "
                         "a 4-inch strip of hall light, the chain taut across it. From here the chain strains every ~2.3 s (the clock)."))

    # 27-35 the call under the clock: dispatcher on the call screen, Tess whispering, the chain giving way ----------------
    conn = at("d2")
    tess_ear = lambda t0_, t1_, expr, lookX: [  # noqa: E731
        blurred("horror/FrontDoor", {"chain": "on", "hallLight": 0.9}, z=0, blur=10, opacity=0.5),
        tess(expr, pose="ear", lookX=lookX, light="phone", width=1150, talk=[[0.0, round(t1_ - t0_ - 0.2, 3)]]),
        comp("horror/Vignette", {"amount": 0.55}, depth=0, z=50)]
    for sid, a, b, kind, extra in [
        ("s27_dispatch_door_shut", "d2", "t1", "call", "'Lindhurst County. Is your door shut?' (phone fx band-pass)"),
        ("s28_tess_v_question", "t1", "d3", "tess", "Whisper: 'Did you send the alert with the v?' Looking away from the door."),
        ("s29_dispatch_good_catch", "d3", "t2", "call", "'No, ma'am. That one's fake. Good catch.' (sells trust; reframed at n45)"),
        ("s30_tess_let_them_in", "t2", "d4", "tess", "Whisper: 'And the one telling me to let them in?' Looking at the door."),
        ("s31_dispatch_ours", "d4", "n43", "call", "'That one's ours. Our staff are outside your door.'"),
        ("s32_chain_screws", "n43", "d5", "chain", "ECU: the chain plate, screws backing out of the frame (clock rung)."),
        ("s33_dispatch_anyone", "d5", "t3", "call", "'Quickly now. Your name, your unit, and is anyone with you?' (= Raf's 'how many live here')"),
        ("s34_tess_just_me", "t3", "d6", "tess", "Whisper: 'Tess Avila. Eleven F. Just me.'"),
    ]:
        t0, t1 = at(a), at(b)
        if kind == "call":
            lay = call_screen(0, t1 - t0, "Lindhurst County EM", timer_track(conn - t0, t1 - t0, 1), z=5)
            lay.append(comp("horror/Vignette", {"amount": 0.45}, depth=0, z=50))
            camk = cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.05, 50, 46, "linear"))
        elif kind == "tess":
            expr = {"t1": "terrified", "t2": "suspicious", "t3": "terrified"}[a]
            lay = tess_ear(t0, t1, expr, {"t1": -0.6, "t2": 0.8, "t3": -0.2}[a])
            camk = cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.08, 50, 44, "linear"))
        else:
            lay = [svg(CHAIN_ECU, 540, 960, 1080, 1920),
                   svg(CHAIN_LINKS, 430, 905, 520, 125, z=2, idle=[{"type": "jitter", "amount": 6, "speed": 9}]),
                   circle(205, 870, 14, "#8f8a80", z=3, keyframes=[{"t": 0.0, "x": 205}, {"t": round(t1 - t0, 3), "x": 236, "ease": "in"}]),
                   circle(205, 950, 14, "#8f8a80", z=3, keyframes=[{"t": 0.0, "x": 205}, {"t": round(t1 - t0, 3), "x": 230, "ease": "in"}])]
            camk = cam((0, 1.25, 25, 50, "linear"), (t1 - t0, 1.35, 22, 50, "linear"), shake=[(0.0, 0.4, 20)])
        S.append(scene(sid, t0, t1, lay, grade=NIGHT, camera=camk, notes=extra))

    # 36 TRUTH TWIST: "Thank you, Tess." on the phone and through the gap at once --------------------------------
    t0, t1 = at("d6"), at("n45")
    lay = [svg(DOOR_GAP, 540, 960, 1080, 1920, z=0),
           rect(540, 600, 760, 230, "#11151c", radius=40, z=5, shadow="0 20px 40px rgba(0,0,0,.6)"),
           text("Lindhurst County EM", 540, 560, 44, "#ffffff", 800, z=6),
           text(f"00:{int(at('d6') - at('d2')) + 1:02d}", 540, 630, 34, "#9fe3b0", 700, z=6),
           tess("shocked", exprs=[{"t": 0, "e": "terrified"}, {"t": round(at("n44") - t0, 3), "e": "shocked"}], pose="ear",
                lookX=0.9, light="phone", width=820, x="24%", y="104%"),
           comp("horror/Glitch", {"cues": [{"at": round(at("n44:same") - t0, 3), "duration": 0.25, "amount": 0.5}], "seed": "tw"}, depth=0, z=60),
           comp("horror/Vignette", {"amount": 0.55}, depth=0, z=50)]
    S.append(scene("s35_twist_same_voice", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.12, 62, 50, "linear")),
                   notes="TRUTH TWIST: d6 'Thank you, Tess.' plays twice, d6_phone (band-pass) and d6_door (lowpass) 0.06 s apart: "
                         "the 'dispatcher' is the man at the door. Call card top, the 4-inch gap right, Tess bottom-left turning to it."))

    # 37 reframe: the v was never a mistake --------------------------------------------------------------------
    t0, t1 = at("n45"), at("n46")
    lay = [rect(540, 960, 1080, 1920, "#0e0a0c"), text("Lindhurst", 540, 820, 82, "#f7f3ff", 800)]
    for i, ch in enumerate("COUNTV"):
        lay.append(text(ch, 190 + i * 140, 1000, 150, RED if ch == "V" else "#ffffff", 900))
    lay += [circle(890, 1000, 105, "rgba(0,0,0,0)", stroke=RED, strokeWidth=8),
            text("Good catch.", 540, 1280, 60, "#9fe3b0", 800, typewriter={"at": 0.15, "cps": 22}),
            comp("horror/Glitch", {"amount": 0.15}, depth=0, z=60)]
    S.append(scene("s36_v_never_a_mistake", t0, t1, lay, trans={"type": "glitch", "duration": 0.2},
                   camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.1, 70, 52, "linear")),
                   notes="Reframe of the midpoint proof: the Countv card returns with 'Good catch.' typed under it. The typo was bait "
                         "so she'd trust the alerts that were spelled right."))

    # 38 BOOKEND + CLIFF: same framing as the cover, alert 4 names her, hard cut --------------------------------------
    t0, t1 = at("n46"), RUNTIME
    a4 = at("n46.end") - t0
    lay = [blurred("horror/Bedroom", {"lamp": 0.0, "phoneGlow": True}, z=0, blur=14, opacity=0.5)]
    lay += lock_screen(0, t1 - t0, [(0, "3:10")], [("a1", -1), ("a2", -1), ("a3", -1), ("a4", a4)], z=5)
    lay += [comp("horror/Vignette", {"amount": 0.55, "color": "120,0,0"}, depth=0, z=80)]
    S.append(scene("s37_bookend_alert4", t0, t1, lay, grade=NIGHT,
                   camera=cam((0, 1.0, 50, 50, "linear"), (a4, 1.0, 50, 50, "linear"), (t1 - t0, 1.32, 50, 47, "out"),
                              shake=[(a4, 0.4, 16)]),
                   notes="BOOKEND of s01 (same framing, push and blur). Alert 4 drops on top of the stack: 'TESS AVILA · 11F · ONE "
                         "OCCUPANT. Open the door.' Hold 0.9 s, then HARD CUT to black (no card, no music tail)."))
    return S


def music_segments():
    """dread bed with hard mutes at the two timed silences and the end (no other mute mechanism needed)."""
    q1, q2, q3 = BY["q1"], BY["q2"], BY["q3"]
    segs = [(0.0, q1["start"]), (q1["end"], q2["start"]), (q2["end"], q3["start"])]
    return [{"src": "music/dread.m4a", "start": round(a, 3), "end": round(b, 3), "volume": 0.3, "duckTo": 0.12,
             "fadeIn": 0.3 if i else 0.0, "fadeOut": 0.05} for i, (a, b) in enumerate(segs)]


def storyboard():
    scenes = build_scenes()
    total = round(sum(s["duration"] for s in scenes), 3)
    assert abs(total - RUNTIME) < 0.05, (total, RUNTIME)
    voice = []
    for it in ITEMS:
        if it["kind"] != "line":
            continue
        if it["id"] == "d6":
            voice.append({"src": f"episodes/{EP}/vo/d6_phone.wav", "start": it["start"], "volume": 1, "duration": round(it["dur"], 3)})
            voice.append({"src": f"episodes/{EP}/vo/d6_door.wav", "start": round(it["start"] + 0.06, 3), "volume": 0.85,
                          "duration": round(it["dur"], 3)})
        else:
            voice.append({"src": f"episodes/{EP}/vo/{it['id']}.wav", "start": it["start"], "volume": 1, "duration": round(it["dur"], 3)})
    return {
        "version": 1, "id": EP, "title": TITLE, "format": "9:16", "fps": 30,
        "scenes": scenes,
        "captions": {"words": captions(), "maxWords": 3, "maxChars": 16, "gapBreak": 0.25, "linger": 0.25,
                     "glue": ["NOT EVEN", "EMERGENCY SERVICES.", "Open up", "Just me."],
                     "style": {"font": "display", "fontSize": 72, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "none",
                               "strokeWidth": 12, "uppercase": False, "y": 0.13, "backing": 0.8}},
        "audio": {"voice": voice, "music": music_segments(), "sfx": sfx_cues(), "duckOn": "voice"},
        "overlays": {"grain": 0.4, "vignette": 0.3, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{EP}/build.py",
                   "timing": "Kokoro-82M on the Spark CPU, measured per line: af_heart 1.36 (narrator), af_heart 1.12 (Tess spoken), "
                             "bf_emma 1.12 (alerts), am_michael 1.08 (door voice = dispatcher)",
                   "audio": f"per-line wavs + fx: ~/studio/tts/{EP}/*.wav on the Spark (tts_measure.py, then vo_fx.sh); copy them to "
                            f"studio/public/episodes/{EP}/vo/. New SFX alert_tone / alert_tone_wall / chain_strain are in "
                            f"backlog/horror/{EP}/sfx/ (gen_sfx.py) and must be copied to studio/public/sfx/ at promotion.",
                   "components": "registered horror kit components + core layers only (no unbuilt components, no kit edits)"},
    }


# ------------------------------------------------------------------ tables for script.md

def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def tables():
    st = stats()
    J, jmed, jmax = jolts()
    print("## STATS\n" + json.dumps(st, indent=1))
    print(f"jolts {len(J)} median {jmed} max {jmax}")
    print("\n## BEATS")
    for b in BEATS:
        print(f"| {b['key']} | {mmss(b['t'])} | {100 * b['t'] / RUNTIME:.0f}% | {b['title']} |")
    print("\n## LINES")
    for it in ITEMS:
        if it["kind"] == "line":
            print(f"| {mmss(it['start'])} | {it['dur']:.2f} | {it['spk']} | {it['text']} | {it['opts'].get('screen', '')} |")
        else:
            print(f"| {mmss(it['start'])} | {it['dur']:.2f} | — | *[silence {it['dur']} s]* | {it['opts'].get('screen', '')} |")
    print("\n## SCENES")
    t = 0
    for i, s in enumerate(build_scenes(), 1):
        print(f"| {i} | {s['id']} | {mmss(t)} | {mmss(t + s['duration'])} | {s.get('notes', '')} |")
        t += s["duration"]
    print("\n## KEY TIMES")
    for ref in ["n1:screamed", "a1:Open", "a1:Not", "a1.end", "a2:Previous", "a2:Please", "n3:off.", "n6:They", "n12:C.", "n13",
                "n16", "n21", "n25", "n26", "n28:yet.", "n30", "a3", "n32", "d1:Josie", "n34", "n37:lock", "n38", "n40", "n41:rang.",
                "n42:hit", "d2", "d5:anyone", "t3:Just", "d6", "n45", "a4", "a4:Open", "a4.end"]:
        tt = at(ref)
        print(f"{ref}: {tt:.2f} ({100 * tt / RUNTIME:.0f}%)")
    print("q1", BY["q1"]["start"], "q2", BY["q2"]["start"], "q3", BY["q3"]["start"])


if __name__ == "__main__":
    sb = storyboard()
    json.dump({"runtime": RUNTIME, "beats": BEATS,
               "items": [{k: v for k, v in it.items() if k != "opts"} | {"screen": it["opts"].get("screen", "")} for it in ITEMS],
               "stats": stats()}, open(os.path.join(HERE, "timeline.json"), "w"), indent=1)
    json.dump(sb, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1, ensure_ascii=False)
    if "--tables" in sys.argv:
        tables()
    print(f"runtime {RUNTIME} s, scenes {len(sb['scenes'])}", file=sys.stderr)
