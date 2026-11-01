"""Build the measured timeline, pacing stats and storyboard.json for horror-delivery-photo-inside.

usage: python3 build.py [--tables]        (stdlib only; safe on the Mac)
inputs : lines.py (the spoken lines), tts_durations.json (Kokoro per-line durations measured on the Spark CPU)
outputs: timeline.json, storyboard.json; --tables prints the markdown tables that script.md carries.

Every visual in storyboard.json uses components the horror kit registers today plus core layers
(rect / circle / text / svg). The delivery-app screens (order card, map + floor plan, rating sheet,
profile + review) are drawn from core layers on a static phone frame, so no kit edit is needed.
"""
from __future__ import annotations

import json
import math
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lines as L  # noqa: E402

D = json.load(open(os.path.join(HERE, "tts_durations.json")))["lines"]
EP = "horror-delivery-photo-inside"
LEAD_IN = 0.12

# ------------------------------------------------------------------ timeline

def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def word_times(lid: str, text: str, start: float) -> list[dict]:
    """Align the script's words to Kokoro tokens by consuming normalised characters."""
    toks = [w for w in D[lid]["words"] if norm(w["w"])]
    out, ti = [], 0
    dur = D[lid]["dur"]
    for w in text.split():
        target = norm(w)
        s = e = None
        acc = ""
        while ti < len(toks) and len(acc) < len(target):
            if s is None:
                s = toks[ti]["s"]
            acc += norm(toks[ti]["w"])
            e = toks[ti]["e"]
            ti += 1
        if s is None:  # fallback: spread evenly at the end
            s = e = out[-1]["e"] - start if out else 0.0
        s = max(0.0, min(s, dur))
        e = max(s + 0.04, min(e, dur + 0.05))
        out.append({"w": w, "s": round(start + s, 3), "e": round(start + e, 3)})
    return out


def build_timeline():
    items, beats, t = [], [], LEAD_IN
    seq = L.V
    for i, e in enumerate(seq):
        if e[0] == "#":
            beats.append({"key": e[1], "title": e[2], "t": round(t, 3)})
            continue
        if e[0] == "~":
            _, sid, secs, opts = e
            items.append({"kind": "silence", "id": sid, "start": round(t, 3), "end": round(t + secs, 3), "dur": secs, "opts": opts,
                          "beat": beats[-1]["key"]})
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
    """'n3' = line start, 'n3.end', 'n3:nine' = first word starting with 'nine', 'n3:nine#2' = 2nd match."""
    if ":" in ref:
        lid, w = ref.split(":", 1)
        n = 1
        if "#" in w:
            w, n = w.split("#")
            n = int(n)
        hits = [x for x in BY[lid]["words"] if norm(x["w"]) == norm(w)] or \
            [x for x in BY[lid]["words"] if norm(x["w"]).startswith(norm(w))]
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
    return sorted(cues, key=lambda c: c["at"])


# ------------------------------------------------------------------ captions

EMPH = {"inside", "alone.", "verified!", "nine.", "forty-one.", "already", "five", "fourth", "kitchen.", "glitch.", "nine",
        "stars.", "rate", "me!", "hallway.", "ten", "feet.", "locked", "six", "still", "behind", "closer", "fifteen",
        "teo.", "twelve", "inside.", "account.", "left.", "on."}


def captions():
    words = []
    for it in ITEMS:
        if it["kind"] != "line":
            continue
        cap = it["opts"].get("cap", {})
        for i, w in enumerate(it["words"]):
            shown = cap.get(w["w"], w["w"])
            if shown == "":
                if words:
                    words[-1]["end"] = w["e"]
                continue
            d = {"text": shown, "start": w["s"], "end": w["e"]}
            if w["w"].lower() in EMPH and it["id"] not in ("r2", "r3"):
                d["emph"] = True
            words.append(d)
        prev_spk = it["spk"]
    # no explicit br: the core pager (maxWords/maxChars/gapBreak) splits pages; br would disable it
    return words


prev_spk = None

# ------------------------------------------------------------------ stats

NUMWORDS = {"nine", "forty-one", "five", "fourth", "one", "ten", "six", "fifteen", "twelve", "hundred"}


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
        by_spk.setdefault(it["spk"], 0)
        by_spk[it["spk"]] += len(it["text"].split())
    distinct_numbers = ["9:00", "9:41", "five (stars)", "fourth (star)", "911", "10 ft", "six", "fifteen", "1,201"]
    hook_end = at("n2.end")
    return {
        "runtime_s": RUNTIME,
        "speech_s": round(speech, 2),
        "silence_s": round(sil, 2),
        "gaps_s": round(RUNTIME - speech - sil, 2),
        "words": words,
        "words_by_speaker": by_spk,
        "wpm_overall": round(words / (RUNTIME / 60), 1),
        "wpm_speaking": round(words / (speech / 60), 1),
        "sentences": len(sents),
        "sentence_median_all": statistics.median(lens),
        "sentence_mean_all": round(statistics.mean(lens), 2),
        "sentence_median_narrator": statistics.median(nlens),
        "punch_share_all": round(sum(1 for n in lens if n <= 4) / len(lens), 3),
        "punch_share_narrator": round(sum(1 for n in nlens if n <= 4) / len(nlens), 3),
        "you_sentence_share": round(len(you_s) / len(sents), 3),
        "you_per_100_words": round(100 * you_w / words, 2),
        "distinct_numbers": distinct_numbers,
        "numbers_per_min": round(len(distinct_numbers) / (RUNTIME / 60), 1),
        "line1_words": len(BY["n1"]["text"].split()),
        "danger_word_s": at("n1:inside"),
        "core_hook_words": len(BY["n1"]["text"].split()) + len(BY["n2"]["text"].split()),
        "core_hook_s": round(hook_end, 2),
        "contradiction_s": at("s1:inside"),
        "words_first_10s": sum(1 for it in lines for w in it["words"] if w["s"] < 10),
    }


# jolts: (label, time) - each one a new anomaly, rule, sound, notification, number or proof
def jolts():
    J = [
        ("proof photo from inside (frame 0)", 0.0), ("I live alone", at("n2")), ("support: inside unit", at("s1:inside")),
        ("chain on at nine", at("n3:nine")), ("photo says 9:41", at("n3:nine#2")), ("already inside (impact)", at("n4")),
        ("driver: rate me five stars", at("r1:Rate")), ("app rule: drivers can't leave", at("r1.end", 0.15)),
        ("fridge thump", at("n5.end")), ("map = my apartment", at("n6")), ("icon in kitchen", at("n6:kitchen")),
        ("Mia: just rate him", at("m1")), ("Not delivered", at("n8:Not")), ("911 bounces to the stars", at("n9:bounced")),
        ("the app had taken my phone", at("n9:app")), ("just one tap", at("r2")), ("RATE ME (caps)", at("r4")),
        ("icon in hallway, 10 ft", at("n10")), ("bedroom lock click + wardrobe creak", at("n11:locked")),
        ("support: six never rated", at("s2:Six")), ("still delivering to them", at("s2:still")),
        ("hello? / HELLO?? silence", BY["q2"]["start"]), ("proof of delivery updated", at("n12")),
        ("photo 2: taken from behind me", at("n12:Taken")), ("map still said hallway", at("n13")),
        ("calm lowercase: closer than the map", at("r5")), ("15 s timer", at("n14")), ("restaurant calls", at("c1")),
        ("no driver named Teo", at("c1:We")), ("silent ticks", BY["q4"]["start"]), ("five stars tapped", at("n15.end")),
        ("fake win: icon vanished", at("n16")), ("1,201 reviews, all doors from inside", at("n17:Every")),
        ("newest from my account", at("n18")), ("She thinks I left (voice swap)", at("r6")),
        ("chain still on", at("n19")), ("final ping: new proof photo", at("n19.end", 0.35)),
    ]
    ts = sorted(t for _, t in J)
    gaps = [b - a for a, b in zip(ts, ts[1:])] + [RUNTIME - ts[-1]]
    return J, round(statistics.median(gaps), 2), round(max(gaps), 2)


# ------------------------------------------------------------------ storyboard helpers

W, H = 1080, 1920
BRAND = "#8b6cff"   # fictional "Bites" violet (not DoorDash red, not Uber Eats green/black)
GREEN = "#4ade80"
RED = "#ff3b3b"
GOLD = "#ffc83d"
INK = "#0f1115"
CARD = "#1a1d24"
GREY = "#8a8f99"

P_CX, P_CY, P_W, P_H = 540, 1110, 800, 1620          # static phone frame for the app screens
S_X0, S_Y0, S_W = 160, 320, 760                      # screen box (top-left x/y, width)


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


def timed(layers, start=None, end=None, z=None):
    """Give a group of layers the same start/end (a cut insert) and lift them above the base."""
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


def slice_xy(box_cx, box_cy, bw, bh, ax, ay):
    """Map a point in 1080x1920 set art to screen coords inside a box (xMidYMid slice)."""
    s = max(bw / 1080, bh / 1920)
    ox = (1080 * s - bw) / 2
    oy = (1920 * s - bh) / 2
    return round(box_cx - bw / 2 + ax * s - ox, 1), round(box_cy - bh / 2 + ay * s - oy, 1)


def phone_frame(clock="9:43"):
    return [
        rect(P_CX, P_CY, P_W, P_H, "#15171c", radius=96, stroke="#2c3038", strokeWidth=8, z=1),
        rect(P_CX, P_CY, P_W - 40, P_H - 40, INK, radius=76, z=2),
        text(clock, S_X0 + 40, S_Y0 + 40, 30, "#e8e8ea", 700, "left", z=3),
        text("▮▮▮  31%", S_X0 + S_W - 40, S_Y0 + 40, 26, "#e8e8ea", 700, "right", z=3),
    ]


def app_header(title, sub=None):
    out = [text("bites", S_X0 + 40, S_Y0 + 120, 34, BRAND, 900, "left", z=3),
           text(title, S_X0 + 40, S_Y0 + 185, 48, "#ffffff", 900, "left", z=3)]
    if sub:
        out.append(text(sub, S_X0 + 40, S_Y0 + 240, 28, GREY, 600, "left", z=3))
    return out


MIRROR = ('<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"><circle cx="60" cy="60" r="54" fill="#1b2029" '
          'stroke="#7d828c" stroke-width="8"/><path d="M 70 30 Q 96 46 92 92 L 78 98 Q 80 60 62 40 Z" fill="#2f6b4c" opacity="0.85"/>'
          '<path d="M 30 40 Q 44 28 60 26" stroke="#c9d2de" stroke-width="5" fill="none" opacity="0.5"/></svg>')


def door_photo(cx, cy, bw, bh, stamp="9:41 PM", border=True, mirror=True, door_props=None, z=4, tick=None):
    """A proof photo of the front door from inside: white border, FrontDoor set, timestamp, mirror plant."""
    props = {"chain": "on", "hallLight": 0.9, "feet": False, "exposure": 1.35, "lift": 0.25, "liftColor": "#8a7a64"}
    props.update(door_props or {})
    pad = 22 if border else 0
    out = []
    if border:
        out.append(rect(cx, cy + 18, bw + 2 * pad, bh + 2 * pad + 36, "#f4f1ea", radius=6, z=z, shadow="0 18px 40px rgba(0,0,0,.6)"))
    out.append(comp("horror/FrontDoor", props, x=cx, y=cy, width=bw, height=bh, z=z + 1))
    if mirror:
        mx, my = slice_xy(cx, cy, bw, bh, 960, 640)
        r = 55 * max(bw / 1080, bh / 1920)
        out.append(svg(MIRROR, mx, my, 2 * r, 2 * r, z=z + 2))
    if border:
        out.append(text(stamp, cx + bw / 2, cy + bh / 2 + 34, max(22, round(bw / 22)), "#3b3b3b", 700, "right", z=z + 2))
        if tick:
            out.append(text(tick, cx - bw / 2, cy + bh / 2 + 34, max(22, round(bw / 22)), "#1f8f4e", 900, "left", z=z + 2))
    return out


# floor plan (svg 680x820 placed at FP_CX/FP_CY) and icon positions in screen space
FP_CX, FP_CY, FP_W, FP_H = 540, 1000, 680, 820
FLOORPLAN = (
    '<svg viewBox="0 0 680 820" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="0" y="0" width="680" height="820" rx="24" fill="#12151b"/>'
    '<g fill="none" stroke="#c9d2de" stroke-width="6">'
    '<rect x="20" y="20" width="640" height="780"/>'
    '<line x1="330" y1="20" x2="330" y2="300"/><line x1="20" y1="300" x2="250" y2="300"/><line x1="430" y1="300" x2="660" y2="300"/>'
    '<line x1="250" y1="300" x2="250" y2="800"/><line x1="430" y1="300" x2="430" y2="590"/><line x1="430" y1="690" x2="430" y2="800"/>'
    '</g>'
    '<rect x="520" y="12" width="90" height="16" fill="#12151b"/><path d="M 520 20 L 610 20" stroke="#ffb347" stroke-width="8"/>'
    '<g font-family="Montserrat, sans-serif" font-weight="800" font-size="30" fill="#8a8f99" text-anchor="middle">'
    '<text x="175" y="170">KITCHEN</text><text x="495" y="170">ENTRY</text><text x="340" y="460">HALL</text>'
    '<text x="135" y="560">BATH</text><text x="545" y="470">BEDROOM</text><text x="565" y="58" font-size="20" fill="#ffb347">FRONT DOOR</text>'
    '</g></svg>')
STREETMAP = (
    '<svg viewBox="0 0 680 820" xmlns="http://www.w3.org/2000/svg"><rect width="680" height="820" rx="24" fill="#1a2027"/>'
    '<g stroke="#2f3a46" stroke-width="34"><line x1="0" y1="180" x2="680" y2="140"/><line x1="0" y1="520" x2="680" y2="560"/>'
    '<line x1="160" y1="0" x2="200" y2="820"/><line x1="470" y1="0" x2="430" y2="820"/></g>'
    '<rect x="230" y="230" width="170" height="250" fill="#26303b"/><circle cx="315" cy="355" r="22" fill="#8b6cff"/>'
    '<circle cx="315" cy="355" r="44" fill="none" stroke="#8b6cff" stroke-width="4" opacity="0.5"/></svg>')


def fp_xy(px, py):
    return round(FP_CX - FP_W / 2 + px, 1), round(FP_CY - FP_H / 2 + py, 1)


ROOM = {"kitchen": fp_xy(175, 225), "entry": fp_xy(565, 110), "hall": fp_xy(340, 560), "hall_door": fp_xy(400, 640)}
YOU = fp_xy(560, 640)
SCOOTER = ('<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="46" fill="#8b6cff" stroke="#fff" stroke-width="6"/>'
           '<g fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round"><circle cx="30" cy="66" r="9"/><circle cx="72" cy="66" r="9"/>'
           '<path d="M 30 66 L 58 66 L 64 34 L 74 34"/></g></svg>')


def map_screen(t0, t1, icon_kf, label_track, street_until=None, z=0, you=True, pulse=False):
    """Floor plan inside the app; icon_kf: [(t, room|None)] scene-local; label_track: [(t, text)]."""
    lay = timed(phone_frame() + app_header("Track your order", "Teo is on the way"), t0, t1, z)
    fp = svg(FLOORPLAN, FP_CX, FP_CY, FP_W, FP_H, z=4)
    if street_until is not None:
        fp["keyframes"] = [{"t": t0, "opacity": 0, "scale": 0.7}, {"t": street_until, "opacity": 1, "scale": 1, "ease": "out"}]
        st = svg(STREETMAP, FP_CX, FP_CY, FP_W, FP_H, z=5,
                 keyframes=[{"t": t0, "opacity": 1, "scale": 1}, {"t": street_until, "opacity": 0, "scale": 1.6, "ease": "in"}])
        lay += timed([st], t0, t1, z)
    lay += timed([fp], t0, t1, z)
    if you:
        lay += timed([circle(YOU[0], YOU[1], 16, "#4aa3ff", stroke="#ffffff", strokeWidth=5, z=6,
                             idle=[{"type": "pulse", "amount": 0.15, "speed": 1.2}]),
                      text("you", YOU[0], YOU[1] + 42, 24, "#4aa3ff", 800, z=6)], t0, t1, z)
    kf = []
    for tt, room in icon_kf:
        if room is None:
            kf.append({"t": tt, "opacity": 0, "scale": 0.2, "ease": "in"})
        else:
            x, y = ROOM[room]
            kf.append({"t": tt, "x": x, "y": y, "opacity": 1, "scale": 1, "ease": "inOut"})
    x0, y0 = ROOM[next(r for _, r in icon_kf if r)]
    icon = svg(SCOOTER, x0, y0, 92, 92, z=8, keyframes=kf)
    if pulse:
        icon["idle"] = [{"type": "pulse", "amount": 0.18, "speed": 2.0}]
    lay += timed([icon], t0, t1, z)
    for i, (tt, s) in enumerate(label_track):
        te = label_track[i + 1][0] if i + 1 < len(label_track) else t1
        lay += timed([text(s, 540, 1500, 40, "#ffffff", 900, background="#2a2440", padding=18, radius=40, z=7)], max(t0, tt), te, z)
    return lay


def rating_sheet(t0, t1, filled_at=(), z=0, title="Rate Teo", sub="How was your delivery?", timer=None, cond=None,
                 tap_at=None, under=None):
    """Bottom-sheet rating UI. filled_at: per-star fill times (scene-local) for stars 1..n."""
    lay = timed(phone_frame() + app_header("Your order", "Lucky Noodle · #4471"), t0, t1, z)
    if under:
        lay += timed(under, t0, t1, z)
    lay += timed([rect(P_CX, 1450, S_W, 860, CARD, radius=44, z=10, shadow="0 -20px 50px rgba(0,0,0,.6)"),
                  rect(P_CX, 1048, 120, 10, "#3a3d46", radius=5, z=11),
                  text(title, 540, 1150, 56, "#ffffff", 900, z=11), text(sub, 540, 1215, 30, GREY, 600, z=11)], t0, t1, z)
    for i in range(5):
        x = 540 + (i - 2) * 132
        lay += timed([text("★", x, 1360, 118, "#3a3d46", 900, z=11)], t0, t1, z)
        if i < len(filled_at):
            lay += timed([text("★", x, 1360, 118, GOLD, 900, z=12, enter={"type": "pop", "duration": 0.18})], filled_at[i], t1, z)
    if cond:
        lay += timed([text(cond, 540, 1660, 30, "#e8e8ea", 700, maxWidth=640, lineHeight=1.2, z=11)], t0, t1, z)
    if timer:
        for (ts, te, s) in timer:
            lay += timed([text(s, 540, 1530, 72, RED, 900, z=12)], ts, te, z)
    if tap_at is not None:
        x = 540 + (len(filled_at) - 1 - 2) * 132 if filled_at else 540 + 132
        lay += timed([circle(x, 1360, 60, "rgba(255,255,255,0.25)", z=13,
                             keyframes=[{"t": tap_at, "scale": 0.4, "opacity": 0.9}, {"t": tap_at + 0.35, "scale": 1.6, "opacity": 0}])],
                     tap_at, min(t1, tap_at + 0.4), z)
    return lay


SILHOUETTE_BACK = (
    '<svg viewBox="0 0 600 760" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M 20 760 Q 40 470 190 430 Q 250 410 300 412 Q 350 410 410 430 Q 560 470 580 760 Z" fill="#14171c"/>'
    '<path d="M 200 440 Q 300 486 400 440 Q 380 404 300 400 Q 220 404 200 440 Z" fill="#1d2128"/>'
    '<path d="M 300 70 Q 175 72 168 200 Q 162 300 150 392 Q 196 420 240 404 Q 270 416 300 412 Q 330 416 360 404 '
    'Q 404 420 450 392 Q 438 300 432 200 Q 425 72 300 70 Z" fill="#0c0d10"/>'
    '<path d="M 432 210 Q 440 300 450 390" stroke="#9cc2ff" stroke-width="6" fill="none" opacity="0.45"/>'
    '<path d="M 168 210 Q 160 300 150 390" stroke="#9cc2ff" stroke-width="6" fill="none" opacity="0.45"/></svg>')
BEDROOM_DOOR = (
    '<svg viewBox="0 0 400 900" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="10" width="380" height="880" fill="#23262d" stroke="#08090b" stroke-width="10"/>'
    '<rect x="40" y="40" width="320" height="850" fill="#2c2a2c" stroke="#08090b" stroke-width="8"/>'
    '<rect x="80" y="90" width="240" height="300" fill="none" stroke="#1b1a1c" stroke-width="8"/><rect x="80" y="450" width="240" height="380" fill="none" stroke="#1b1a1c" stroke-width="8"/>'
    '<circle cx="320" cy="480" r="16" fill="#9a968d"/><rect x="250" y="472" width="72" height="16" rx="6" fill="#aaa69c"/>'
    '<rect x="320" y="440" width="14" height="22" rx="3" fill="#6f6c66"/>'
    '<rect x="40" y="884" width="320" height="6" fill="#e7b46a" opacity="0.5"/></svg>')
DUVET = ('<svg viewBox="0 0 1080 600" xmlns="http://www.w3.org/2000/svg"><path d="M 0 140 Q 260 40 540 120 Q 820 200 1080 90 L 1080 600 L 0 600 Z" '
         'fill="#34405c" stroke="#0b0d12" stroke-width="10"/><path d="M 80 260 Q 380 180 640 260 Q 880 330 1040 250" stroke="#2a3349" stroke-width="12" fill="none"/></svg>')
WARDROBE_EDGE = ('<svg viewBox="0 0 200 1920" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="160" height="1920" fill="#060607"/>'
                 '<rect x="150" y="0" width="20" height="1920" fill="#1a1517"/></svg>')


def photo2(cx, cy, bw, bh, z=0, border=True, stamp="9:52 PM"):
    """Nora from behind on her bed, facing her locked door, shot from the wardrobe corner."""
    s = bw / 1080
    out = []
    if border:
        out.append(rect(cx, cy + 18 * s, bw + 44 * s, bh + 80 * s, "#f4f1ea", radius=6, z=z))
    out += [
        rect(cx, cy, bw, bh, "#07080a", z=z + 1),
        comp("horror/Bedroom", {"lamp": 0.0, "wardrobeOpen": 0.3, "phoneGlow": True, "exposure": 0.8, "lift": 0.12},
             x=cx, y=cy, width=bw, height=bh, z=z + 2, blur=round(3 * s, 1), opacity=0.55),
        svg(BEDROOM_DOOR, cx, cy - bh * 0.12, 400 * s * 1.1, 900 * s * 1.1, z=z + 3),
        circle(cx, cy + bh * 0.16, 260 * s, "rgba(150,190,255,0.22)", z=z + 4, blur=round(60 * s, 1)),
        svg(SILHOUETTE_BACK, cx, cy + bh / 2 - 380 * s * 1.25, 600 * s * 1.25, 760 * s * 1.25, z=z + 5),
        svg(DUVET, cx, cy + bh / 2 - 170 * s, bw, 340 * s, z=z + 6),
        svg(WARDROBE_EDGE, cx - bw / 2 + 90 * s, cy, 200 * s, bh, z=z + 7),
        comp("horror/Vignette", {"amount": 0.7}, x=cx, y=cy, width=bw, height=bh, z=z + 8),
    ]
    if border:
        out.append(text(stamp, cx + bw / 2, cy + bh / 2 + 40 * s, max(22, round(44 * s)), "#3b3b3b", 700, "right", z=z + 9))
    return out


def full(name, props=None, z=0, **kw):
    return comp(name, props, x=540, y=960, width=W, height=H, z=z, **kw)


def nora(expr="scared", exprs=None, pose="phone", lookX=0.0, lookY=0.4, light="phone", z=40, width=1150, flip=False, **kw):
    p = {"pose": pose, "exprs": exprs or [{"t": 0, "e": expr}], "lookX": lookX, "lookY": lookY, "light": light, "blink": True}
    p.update(kw.pop("props", {}))
    return comp("horror/Protagonist", p, x="50%", y="100%", anchorY=1, width=width, height=round(width * 1.52), z=z,
                depth=0, flipX=flip, **kw)


MEMBERS = {"Bites Support": {"color": BRAND, "initials": "B"}, "Teo": {"color": "#5a6b8f", "initials": "T"},
           "Mia": {"color": "#b0607a", "initials": "M"}, "Bites": {"color": "#3a3f4a", "initials": "b"}}


def handphone(chat=None, mode="chat", call=None, lock=None, banners=None, vibrate=None, tremble=1.5, tilt=-3, glitch=None,
              screens=None, clock="9:44"):
    phone = {"members": MEMBERS, "mode": mode}
    if chat:
        chat = {"theme": "dark", "scale": 1.25, "clock": clock, "battery": 31, "dm": True, **chat}
        phone["chat"] = chat
    if call:
        phone["call"] = call
    if lock:
        phone["lock"] = lock
    if banners:
        phone["banners"] = banners
    if vibrate:
        phone["vibrate"] = vibrate
    if screens:
        phone["screens"] = screens
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": 0.6, "tilt": tilt, "tremble": tremble, "side": "right", "phone": phone,
         "thumbY": 0.94, "thumbReach": 0.1}
    if glitch:
        p["glitch"] = glitch
    return comp("horror/HandPhone", p, z=10)


def msgs(thread, scene_start):
    return [{**m, "at": round(m["at"] - scene_start, 3)} for m in thread]


# ------------------------------------------------------------------ scenes

def scene(sid, t0, t1, layers, bg="#07080b", camera=None, trans=None, grade=None, notes=None, captionY=None):
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
    c = {"keyframes": [{"t": round(t, 3), "zoom": z, "x": f"{x:.2f}%", "y": f"{y:.2f}%", "ease": e} for t, z, x, y, e in kf]}
    if shake:
        c["shake"] = [{"at": round(a, 3), "duration": d, "amplitude": amp} for a, d, amp in shake]
    return c


def build_scenes():
    S = []
    # threads (absolute times)
    support = [
        {"from": "Bites Support", "text": "Hi Nora! How can we help with order #4471?", "at": -30},
        {"me": True, "text": "who took this photo?? I live alone", "at": at("n1:inside")},
        {"from": "Bites Support", "text": "Driver verified ✓ Location: INSIDE UNIT. Anything else today? 🙂", "at": at("s1")},
        {"from": "Bites Support", "text": "Sorry for the wait! 6 customers never rated Teo. He's still delivering to them 🙂", "at": at("s2")},
        {"me": True, "text": "hello?", "at": BY["q2"]["start"] + 0.1},
        {"me": True, "text": "HELLO??", "at": BY["q2"]["start"] + 0.7},
    ]
    teo = [
        {"from": "Teo", "text": "Hi! Your order's by the door 🙂 Rate me ★★★★★ and I'll head out", "at": at("r1")},
        {"kind": "system", "text": "Drivers can't leave until the order is rated.", "at": at("r1.end", 0.15)},
        {"from": "Teo", "text": "just one tap :)", "at": at("r2")},
        {"from": "Teo", "text": "I've been very patient.", "at": at("r3")},
        {"from": "Teo", "kind": "alert", "text": "RATE ME", "at": at("r4")},
        {"from": "Teo", "text": "i'm closer than the map says.", "at": at("r5")},
    ]
    mia = [
        {"from": "Mia", "text": "u up? lol", "at": -400},
        {"me": True, "text": "someone took a photo INSIDE my place", "at": at("n7", 0.2)},
        {"from": "Mia", "text": "it's a glitch lol. just rate him", "at": at("m1")},
        {"me": True, "text": "HE'S INSIDE", "at": at("n8:he's")},
        {"kind": "system", "text": "! Not delivered", "at": at("n8:Not")},
    ]

    # 1 HOOK ------------------------------------------------------------------------------------
    t0, t1 = 0.0, at("s1")
    tp = at("n2")
    ring = slice_xy(540, 990, 600, 700, 780, 840)
    card = (phone_frame("9:43") + app_header("Your order", "Lucky Noodle · #4471")
            + [rect(540, 1010, 700, 1060, CARD, radius=36, z=3),
               text("✓ Left at door · 9:41 PM", 220, 600, 40, GREEN, 900, "left", z=4)]
            + door_photo(540, 990, 600, 700, "9:41 PM", z=5)
            + [circle(ring[0], ring[1], 78, "rgba(0,0,0,0)", stroke=RED, strokeWidth=9, z=12,
                      idle=[{"type": "pulse", "amount": 0.12, "speed": 1.6}]),
               text("taken from INSIDE →", ring[0] - 300, ring[1] - 4, 50, "#ffffff", 900, background=RED, padding=14, radius=10,
                    rotate=-4, z=13),
               text("Proof of delivery", 220, 1470, 30, GREY, 700, "left", z=4)])
    lay = timed(card, None, tp)
    lay += timed(door_photo(540, 900, 940, 1500, "9:41 PM", z=20), tp, t1)
    lay += timed([comp("horror/Vignette", {"amount": 0.45}, depth=0, z=60)], tp, t1)
    S.append(scene("s01_hook", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (tp - 0.01, 1.05, 50, 50, "linear"), (tp, 1.0, 50, 50, "step"),
                              (t1, 1.14, 58, 46, "linear")),
                   notes="FRAME 0 = COVER: the order card, the inside-out door photo, red ring + 'taken from INSIDE ->' label on the chain. "
                         "Hard cut to the photo full-frame on 'I live alone'. A green delivery-jacket sleeve shows in the hall mirror (silent plant)."))

    # 2 SUPPORT --------------------------------------------------------------------------------
    t0, t1 = at("s1"), at("n3")
    gi = at("s1:inside") - t0
    lay = [full("horror/LivingRoom", {"lamp": 0.4, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
           handphone({"title": "Bites Support", "subtitle": "Typically replies instantly", "accent": BRAND,
                      "messages": msgs(support[:3], t0), "typing": [{"from": "Bites Support", "at": -0.6, "until": 0.0}]},
                     glitch=[{"at": round(gi, 3), "duration": 0.2, "amount": 0.9}]),
           comp("horror/Glitch", {"cues": [{"at": round(gi, 3), "duration": 0.18, "amount": 0.8}], "seed": "g1"}, depth=0, z=60),
           comp("horror/Vignette", {"amount": 0.4}, depth=0, z=50)]
    S.append(scene("s02_support", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (gi, 1.04, 50, 52, "linear"),
                                                         (gi + 0.2, 1.22, 52, 60, "out"), (t1 - t0, 1.25, 52, 60, "linear"),
                                                         shake=[(gi, 0.22, 10)]),
                   notes="Support's calm all-clear IS the contradiction: 'inside unit' at ~6 s."))

    # 3 TELL -----------------------------------------------------------------------------------
    t0, t1 = at("n3"), at("r1")
    a, b, c = at("n3:I") - t0, at("n3:The#2") - t0, at("n4") - t0
    lay = timed(door_photo(540, 900, 940, 1500, "9:41 PM", z=0), 0, a)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.3, "tv": "off"}), nora("suspicious", lookX=0.5, lookY=0.1, light="none")], a, b, 0)
    lay += timed(door_photo(540, 900, 940, 1500, "9:41 PM", z=0) +
                 [text("9:41 PM", 540, 1610, 120, RED, 900, background="#f4f1ea", padding=16, radius=8, z=30,
                       enter={"type": "pop", "duration": 0.2})], b, c)
    lay += timed([full("horror/FrontDoor", {"chain": "on", "hallLight": 0.25, "feet": False}),
                  comp("horror/Darkness", {"x": 0.68, "y": 0.44, "radius": 0.42, "darkness": 0.85}, depth=0, z=20),
                  comp("horror/RedText", {"text": "ALREADY INSIDE", "style": "scrawl", "at": round(c + 0.05, 3), "duration": 1.1,
                                          "fontSize": 120, "y": 0.3}, depth=0, z=70)], c, t1 - t0)
    lay.append(comp("horror/Vignette", {"amount": 0.5}, depth=0, z=50))
    S.append(scene("s03_tell", t0, t1, lay,
                   camera=cam((0, 1.6, 66, 46, "linear"), (a - 0.01, 1.75, 67, 45, "linear"), (a, 1.0, 50, 50, "step"),
                              (b - 0.01, 1.04, 50, 50, "linear"), (b, 1.25, 50, 72, "step"), (c - 0.01, 1.32, 50, 74, "linear"),
                              (c, 1.0, 50, 50, "step"), (t1 - t0, 1.08, 62, 44, "linear"), shake=[(c, 0.25, 14)]),
                   notes="The chain is a timeline: on at 9:00, photo at 9:41, so he was inside before she locked up."))

    # 4 DRIVER CHAT + APP RULE -----------------------------------------------------------------
    t0, t1 = at("r1"), at("n5")
    lay = [full("horror/LivingRoom", {"lamp": 0.35, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
           handphone({"title": "Teo", "subtitle": "★5.0 · 1,206 deliveries · 1,200 ratings", "accent": "#3d4a6b",
                      "messages": msgs(teo[:2], t0)}),
           comp("horror/Vignette", {"amount": 0.4}, depth=0, z=50)]
    S.append(scene("s04_rules", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (1.2, 1.0, 50, 50, "linear"), (1.5, 1.35, 50, 30, "out"),
                              (2.4, 1.36, 50, 30, "linear"), (2.6, 1.08, 50, 52, "out"), (t1 - t0, 1.1, 50, 54, "linear")),
                   notes="Plant: the header stat (1,206 deliveries vs 1,200 ratings) gets a 0.9 s punch-in. App rule is on-screen only, with a UI chime."))

    # 5 NEAR-COMPLIANCE + KITCHEN ---------------------------------------------------------------
    t0, t1 = at("n5"), at("n7")
    thump = BY["n5"]["end"] - t0
    q1e = BY["q1"]["end"] - t0
    s4 = at("n5:fourth") - t0
    lay = rating_sheet(0, thump, filled_at=[0.05, 0.25, 0.45, s4], tap_at=None)
    lay += timed([circle(540 + 132, 1360, 64, "rgba(255,255,255,0.18)", z=14, idle=[{"type": "pulse", "amount": 0.2, "speed": 3}])], s4, thump)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.2, "tv": "off"}),
                  nora("shocked", lookX=-0.7, lookY=0.0, light="phone", blink=False)], thump, q1e, 0)
    k = at("n6:kitchen") - t0
    lay += map_screen(q1e, t1 - t0, [(q1e, "kitchen")], [(q1e, "Teo · 30 ft away")], street_until=q1e + 0.9, z=0)
    S.append(scene("s05_kitchen", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (thump - 0.01, 1.08, 56, 70, "linear"), (thump, 1.0, 50, 50, "step"),
                              (q1e, 1.0, 50, 50, "step"), (k, 1.0, 50, 50, "linear"), (t1 - t0, 1.2, 38, 40, "out"),
                              shake=[(thump, 0.3, 16)]),
                   notes="Near-compliance: four stars filled, thumb on the fourth; the fridge thump stops her. Then the map is my apartment."))

    # 6 MIA ------------------------------------------------------------------------------------
    t0, t1 = at("n7"), at("n9")
    nd = at("n8:Not") - t0
    lay = [full("horror/LivingRoom", {"lamp": 0.2, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
           handphone({"title": "Mia", "subtitle": "sister", "accent": "#b0607a", "messages": msgs(mia, t0),
                      "typing": [{"from": "Mia", "at": round(at("m1") - t0 - 0.6, 3), "until": round(at("m1") - t0, 3)}]},
                     tremble=2.5),
           comp("horror/RedText", {"text": "! NOT DELIVERED", "style": "flash", "at": round(nd, 3), "duration": 0.7, "fontSize": 96,
                                   "y": 0.3}, depth=0, z=70),
           comp("horror/Vignette", {"amount": 0.45}, depth=0, z=50)]
    S.append(scene("s06_mia", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (1.4, 1.06, 50, 54, "linear"),
                                                     (nd, 1.1, 50, 56, "linear"), (t1 - t0, 1.14, 50, 58, "linear"), shake=[(nd, 0.2, 8)]),
                   notes="Viewer-proxy voice: Mia says what the viewer is thinking (just rate him), then the channel dies."))

    # 7 911 ------------------------------------------------------------------------------------
    t0, t1 = at("n9"), at("r2")
    bounce = at("n9:bounced") - t0
    lay = [full("horror/LivingRoom", {"lamp": 0.2, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
           handphone(mode="call", call={"name": "911", "sub": "Emergency", "label": "Calling…", "at": -0.2}, tremble=3,
                     glitch=[{"at": round(bounce - 0.15, 3), "duration": 0.3, "amount": 1.0}])]
    lay = timed(lay, 0, bounce)
    lay += rating_sheet(bounce, t1 - t0, title="Rate your driver", sub="Rate Teo to continue", z=0)
    lay += [comp("horror/Glitch", {"cues": [{"at": round(bounce - 0.1, 3), "duration": 0.3, "amount": 1.0},
                                            {"at": round(at("n9:app") - t0, 3), "duration": 0.15, "amount": 0.6}], "seed": "g2"},
                 depth=0, z=60),
            comp("horror/Vignette", {"amount": 0.45}, depth=0, z=50)]
    S.append(scene("s07_911", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (bounce, 1.04, 50, 50, "linear"),
                                                     (bounce + 0.01, 1.0, 50, 50, "step"), (t1 - t0, 1.12, 50, 66, "linear"),
                                                     shake=[(bounce, 0.25, 12)]),
                   trans={"type": "glitch", "duration": 0.2},
                   notes="Channel removal: 911 bounces back to five empty stars. 'The app had taken my phone' makes it a rule, not a glitch."))

    # 8 VOLUME LADDER + HALLWAY ----------------------------------------------------------------
    t0, t1 = at("r2"), at("n11")
    r4 = at("r4") - t0
    h = at("n10") - t0
    lay = timed([full("horror/LivingRoom", {"lamp": 0.15, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
                 handphone({"title": "Teo", "subtitle": "★5.0 · 1,206 deliveries · 1,200 ratings", "accent": "#3d4a6b",
                            "messages": msgs(teo[:5], t0)}, vibrate=[{"at": round(r4, 3), "duration": 0.5, "amount": 1}], tremble=3)], 0, h)
    lay += map_screen(h, t1 - t0, [(h, "kitchen"), (h + 1.2, "hall")], [(h, "Teo · 30 ft away"), (h + 1.0, "Teo · 10 ft away")])
    lay.append(comp("horror/Vignette", {"amount": 0.5}, depth=0, z=50))
    S.append(scene("s08_ladder", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (r4, 1.05, 50, 52, "linear"),
                                                        (r4 + 0.15, 1.18, 50, 58, "out"), (h - 0.01, 1.2, 50, 58, "linear"),
                                                        (h, 1.0, 50, 50, "step"), (t1 - t0, 1.12, 50, 56, "linear"),
                                                        shake=[(r4, 0.3, 20)]),
                   notes="Typography ladder: polite, curt, CAPS. Proximity ladder: kitchen 30 ft -> hall 10 ft."))

    # 9 BEDROOM RETREAT ------------------------------------------------------------------------
    t0, t1 = at("n11"), at("s2")
    lk = at("n11:locked") - t0
    lay = timed([full("horror/Hallway", {"lights": 1, "flicker": 0.3, "endDoor": True, "figure": 0})], 0, lk + 0.5)
    lay += timed([full("horror/Bedroom", {"lamp": 0.15, "wardrobeOpen": 0.22, "phoneGlow": True}),
                  nora("scared", lookX=0.0, lookY=0.2, width=1000),
                  svg(DUVET, 540, 1700, 1080, 600, z=45, depth=0)], lk + 0.5, t1 - t0)
    lay.append(comp("horror/Vignette", {"amount": 0.55}, depth=0, z=50))
    S.append(scene("s09_bedroom", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (lk + 0.49, 1.15, 50, 45, "linear"),
                                                         (lk + 0.5, 1.0, 50, 50, "step"), (t1 - t0, 1.05, 54, 50, "linear"),
                                                         shake=[(lk + 0.4, 0.15, 6)]),
                   trans={"type": "whip", "duration": 0.25, "direction": "left"},
                   notes="She faces the camera = faces the bedroom door. The wardrobe (ajar) is behind her; its hinge creaks under the lock click."))

    # 10 TURN + SILENCE BEAT -------------------------------------------------------------------
    t0, t1 = at("s2"), at("n12")
    six = at("s2:Six") - t0
    lay = [full("horror/Bedroom", {"lamp": 0.1, "wardrobeOpen": 0.25}, blur=8, opacity=0.8, depth=0.2),
           handphone({"title": "Bites Support", "subtitle": "Typically replies instantly", "accent": BRAND,
                      "messages": msgs(support, t0)}, tremble=2.5),
           comp("horror/Heartbeat", {"bpm": 70, "intensity": 0.5, "from": round(six, 3)}, depth=0, z=55),
           comp("horror/Vignette", {"amount": 0.5}, depth=0, z=50)]
    stat = [rect(540, 960, 1080, 1920, "#07080b", z=80),
            text("Teo", 540, 700, 64, "#ffffff", 900, z=81),
            text("1,206 deliveries", 540, 860, 92, "#ffffff", 900, z=81),
            text("1,200 ratings", 540, 990, 92, "#ffffff", 900, z=81),
            text("6 never rated him", 540, 1170, 84, RED, 900, z=81, enter={"type": "pop", "duration": 0.2})]
    lay += timed(stat, six, six + 1.1)
    S.append(scene("s10_turn", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (six + 1.1, 1.06, 50, 54, "linear"),
                                                      (t1 - t0, 1.16, 50, 60, "linear")),
                   notes="TURN (T3): her protective act (not rating) is the trap. Count-match pays the header plant out loud. "
                         "Then two unanswered name checks ('hello?' 'HELLO??') = the silence beat before the proof."))

    # 11 SCARIEST IMAGE ------------------------------------------------------------------------
    t0, t1 = at("n12"), at("n13")
    me = at("n12:Me") - t0
    tk = at("n12:Taken") - t0
    lay = timed([full("horror/Bedroom", {"lamp": 0.1}, blur=8, opacity=0.8, depth=0.2),
                 handphone(mode="lock", lock={"time": "9:52", "date": "Friday"},
                           banners=[{"at": 0.05, "duration": 3, "app": "bites", "title": "Proof of delivery updated", "text": "Tap to view photo"}])],
                0, me)
    lay += timed(photo2(540, 930, 960, 1500, z=0), me, t1 - t0)
    lay += timed([comp("horror/Heartbeat", {"bpm": 70, "bpmTo": 92, "intensity": 0.7}, depth=0, z=55)], me, t1 - t0)
    S.append(scene("s11_photo2", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (me - 0.01, 1.03, 50, 50, "linear"), (me, 1.3, 52, 62, "step"),
                              (tk - 0.01, 1.36, 52, 63, "linear"), (tk, 1.0, 50, 50, "step")),
                   notes="THE scariest image, once: held perfectly still for the 4.0 s silence (q3) - the only still hold. "
                         "Composition: wardrobe-door edge at left (camera position), her silhouette from behind, her locked door ahead."))

    # 12 MAP LIES + CALM LOWERCASE -------------------------------------------------------------
    t0, t1 = at("n13"), at("n14")
    r5 = at("r5") - t0
    lay = map_screen(0, r5, [(0, "hall")], [(0, "Teo · 10 ft away")], pulse=True)
    lay += timed([full("horror/Bedroom", {"lamp": 0.1}, blur=8, opacity=0.8, depth=0.2),
                  handphone({"title": "Teo", "subtitle": "★5.0 · 1,206 deliveries · 1,200 ratings", "accent": "#3d4a6b",
                             "messages": msgs(teo, t0)}, tremble=1)], r5, t1 - t0)
    S.append(scene("s12_closer", t0, t1, lay, camera=cam((0, 1.25, 50, 38, "linear"), (r5 - 0.01, 1.3, 50, 38, "linear"),
                                                        (r5, 1.0, 50, 50, "step"), (t1 - t0, 1.06, 50, 52, "linear")),
                   notes="The tracker lies (said out loud now), and Teo drops from CAPS to calm lowercase: the scariest register."))

    # 13 CLOCK + RESTAURANT LIFELINE -----------------------------------------------------------
    t0, t1 = at("n14"), at("n16")
    tap = BY["n15"]["end"] - t0
    timer = [(float(i), float(i + 1), f"0:{15 - i:02d}") for i in range(15) if i < tap + 1]
    timer[-1] = (timer[-1][0], t1 - t0, timer[-1][2])
    c1s, c1e = at("c1") - t0, BY["c1"]["end"] - t0
    nta = at("n15") - t0
    callcard = [rect(540, 560, 720, 170, "#22252c", radius=34, z=30, shadow="0 18px 40px rgba(0,0,0,.6)"),
                circle(250, 560, 46, "#d9822b", z=31), text("LN", 250, 560, 34, "#ffffff", 900, z=32),
                text("Lucky Noodle", 320, 535, 40, "#ffffff", 900, "left", z=31),
                text("restaurant · in-app call", 320, 590, 28, GREY, 600, "left", z=31)]
    lay = rating_sheet(0, t1 - t0, filled_at=[tap - 0.32, tap - 0.24, tap - 0.16, tap - 0.08, tap], timer=timer,
                       cond="Rate within 0:15 or your driver will hand you the order in person.", tap_at=tap)
    lay += timed(callcard + [circle(870, 560, 40, GREEN, z=31), text("☎", 870, 560, 40, "#ffffff", 900, z=32)], c1s - 0.35, c1s + 0.3)
    lay += timed(callcard + [text("0:03", 860, 535, 30, GREEN, 800, "right", z=31)], c1s + 0.3, c1e)
    lay += timed(callcard + [text("Call ended", 860, 535, 30, RED, 800, "right", z=31)], c1e, c1e + 0.9)
    lay += timed([full("horror/Bedroom", {"lamp": 0.05, "wardrobeOpen": 0.35, "phoneGlow": True}, z=40),
                  svg(SILHOUETTE_BACK, 540, 1560, 750, 950, z=41, depth=0), svg(WARDROBE_EDGE, 90, 960, 200, 1920, z=42, depth=0),
                  comp("horror/Vignette", {"amount": 0.75}, depth=0, z=43)], nta, nta + 1.1)
    lay += [comp("horror/Heartbeat", {"bpm": 92, "bpmTo": 120, "intensity": 0.7}, depth=0, z=55),
            comp("horror/Vignette", {"amount": 0.45}, depth=0, z=50)]
    S.append(scene("s13_clock", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (c1s, 1.04, 50, 48, "linear"), (c1e, 1.1, 50, 40, "linear"),
                              (c1e + 0.3, 1.45, 50, 80, "out"), (nta - 0.01, 1.5, 50, 80, "linear"), (nta, 1.0, 50, 50, "step"),
                              (nta + 1.1, 1.0, 50, 50, "linear"), (nta + 1.11, 1.25, 50, 72, "step"), (t1 - t0, 1.3, 50, 72, "linear"),
                              shake=[(tap, 0.2, 8)]),
                   notes="Real-time 15 s clock (one label per second). The restaurant gets through for 5 s: no driver named Teo "
                         "(kills the app and support as authority). Silent ticks, then 'I didn't turn around' over the wardrobe-corner view."))

    # 14 FAKE WIN ------------------------------------------------------------------------------
    t0, t1 = at("n16"), at("n17")
    q5 = BY["q5"]["start"] - t0
    lay = map_screen(0, q5, [(0, "hall"), (0.6, None)], [(0, "Delivery complete. Thank you!")])
    lay += timed([rect(540, 1500, 640, 120, "#123d26", radius=30, z=20),
                  text("✓ Delivery complete. Thank you!", 540, 1500, 36, GREEN, 900, z=21)], 0.5, q5)
    lay += timed([full("horror/Bedroom", {"lamp": 0.3, "wardrobeOpen": 0.35}), nora("relieved", lookY=0.5, width=1000),
                  svg(DUVET, 540, 1700, 1080, 600, z=45, depth=0)], q5, t1 - t0)
    S.append(scene("s14_fakewin", t0, t1, lay, camera=cam((0, 1.08, 50, 50, "linear"), (q5, 1.0, 50, 50, "linear"),
                                                         (q5 + 0.01, 1.0, 50, 50, "step"), (t1 - t0, 1.03, 50, 50, "linear")),
                   notes="Fake win (T11). Relief face; the wardrobe behind her is a little wider open than before (no VO)."))

    # 15 PROFILE + REVIEW + VOICE SWAP ---------------------------------------------------------
    t0, t1 = at("n17"), at("n19")
    ev = at("n17:Every") - t0
    n18 = at("n18") - t0
    r6 = at("r6") - t0
    base = phone_frame("9:58") + [circle(S_X0 + 100, S_Y0 + 170, 56, "#5a6b8f", z=3), text("T", S_X0 + 100, S_Y0 + 170, 52, "#fff", 900, z=4),
                                  text("Teo", S_X0 + 180, S_Y0 + 140, 52, "#ffffff", 900, "left", z=3),
                                  text("★5.0 · 1,201 reviews", S_X0 + 180, S_Y0 + 200, 34, GOLD, 800, "left", z=3)]
    lay = timed(base, 0, t1 - t0)
    grid = []
    looks = ["#8a7a64", "#5f7a94", "#7a5c8f", "#6f8a64", "#946a5f", "#64808a"]
    for i in range(6):
        cx = 360 + (i % 2) * 360
        cy = 850 + (i // 2) * 420
        grid += door_photo(cx, cy, 300, 360, ["9:12 PM", "11:40 PM", "8:03 PM", "10:27 PM", "1:15 AM", "9:49 PM"][i], z=5,
                           door_props={"liftColor": looks[i], "hallLight": 0.5 + 0.1 * (i % 3)}, mirror=(i == 4))
    for l in grid:
        if isinstance(l.get("y"), (int, float)):
            y = l["y"]
            l["keyframes"] = [{"t": round(ev, 3), "y": y + 260}, {"t": round(n18, 3), "y": y - 120, "ease": "out"}]
    lay += timed(grid, 0, n18)
    review = [rect(540, 1050, 700, 560, CARD, radius=34, z=20),
              circle(250, 860, 46, "#c97a5a", z=21), text("N", 250, 860, 40, "#ffffff", 900, z=22),
              text("Nora R. · just now", 320, 840, 36, "#ffffff", 900, "left", z=21),
              text("★★★★★", 320, 895, 40, GOLD, 900, "left", z=21)]
    lay += timed(review, n18, t1 - t0)
    lay += timed(door_photo(540, 1130, 300, 260, "9:52 PM", z=21, mirror=False), n18, r6)
    lay += timed([text("She thinks I left.", 540, 1100, 64, "#ffffff", 900, z=23, typewriter={"at": round(r6, 3), "cps": 18})], r6, t1 - t0)
    lay += [comp("horror/Glitch", {"cues": [{"at": round(r6, 3), "duration": 0.22, "amount": 0.9}], "seed": "g3"}, depth=0, z=60),
            comp("horror/Vignette", {"amount": 0.4}, depth=0, z=50)]
    S.append(scene("s15_reviews", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (ev, 1.0, 50, 50, "linear"), (n18 - 0.01, 1.05, 50, 52, "linear"),
                              (n18, 1.0, 50, 50, "step"), (r6, 1.12, 50, 55, "out"), (t1 - t0, 1.2, 50, 57, "linear")),
                   notes="Retro-reveal + scale-up: 1,201 reviews, every photo a door from inside. The newest is from her account, "
                         "read in HIS voice (am_michael): 'She thinks I left.' One thumbnail has the green sleeve in its mirror."))

    # 16 BOOKEND -------------------------------------------------------------------------------
    t0, t1 = at("n19"), RUNTIME
    ping = BY["n19"]["end"] + 0.35 - t0
    lay = [full("horror/FrontDoor", {"chain": "on", "hallLight": 0.5, "feet": False}),
           svg(MIRROR, 960, 640, 110, 110, z=2),
           comp("horror/Darkness", {"x": 0.62, "y": 0.45, "radius": 0.5, "darkness": 0.8}, depth=0, z=20),
           comp("horror/Flicker", {"strength": 0.15, "from": 1.0}, depth=0, z=30)]
    lay += timed([svg(SILHOUETTE_BACK, 540, 1640, 820, 1040, z=35, depth=0),
                  rect(540, 960, 1080, 1920, "rgba(0,0,0,0)", stroke="#f4f1ea", strokeWidth=44, z=40, depth=0),
                  rect(540, 1860, 1080, 120, "#f4f1ea", z=41, depth=0),
                  text("✓ Delivered to customer", 60, 1858, 40, "#1f8f4e", 900, "left", z=42, depth=0),
                  text("9:58 PM", 1020, 1858, 40, "#3b3b3b", 700, "right", z=42, depth=0),
                  rect(540, 960, 1080, 1920, "#ffffff", z=45, depth=0,
                       keyframes=[{"t": round(ping, 3), "opacity": 0.85}, {"t": round(ping + 0.18, 3), "opacity": 0}])], ping, t1 - t0)
    S.append(scene("s16_bookend", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (ping, 1.06, 58, 46, "linear"), (ping + 0.01, 1.0, 50, 50, "step"),
                              (t1 - t0, 1.0, 50, 50, "linear")),
                   notes="Bookend = the 0:02 photo framing (same camera). On the ping it becomes a NEW proof photo with her in it, "
                         "taken from behind her. Hard cut, no CTA."))
    return S


def storyboard():
    scenes = build_scenes()
    total = round(sum(s["duration"] for s in scenes), 3)
    assert abs(total - RUNTIME) < 0.05, (total, RUNTIME)
    voice = []
    for it in ITEMS:
        if it["kind"] == "line":
            voice.append({"src": f"episodes/{EP}/vo/{it['id']}.wav", "start": it["start"], "volume": 1, "duration": round(it["dur"], 3)})
    sb = {
        "version": 1, "id": EP, "title": "My Delivery Driver Won't Leave Until I Rate Him 5 Stars", "format": "9:16", "fps": 30,
        "scenes": scenes,
        "captions": {"words": captions(), "maxWords": 5, "maxChars": 18, "gapBreak": 0.25, "linger": 0.3,
                     "glue": ["five stars", "front door", "inside unit", "Lucky Noodle", "10 FEET."],
                     "style": {"font": "display", "fontSize": 58, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "none",
                               "strokeWidth": 10, "uppercase": False, "y": 0.12, "backing": 0.85}},
        "audio": {"voice": voice,
                  "music": [{"src": "music/dread.m4a", "start": 0, "end": round(RUNTIME - 0.4, 2), "volume": 0.3, "duckTo": 0.12,
                             "fadeIn": 0.4, "fadeOut": 1.2}],
                  "sfx": sfx_cues(), "duckOn": "voice"},
        "overlays": {"grain": 0.45, "vignette": 0.3, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{EP}/build.py",
                   "timing": "Kokoro-82M on the Spark CPU, measured per line, five voices (lines.VOICES)",
                   "audio": f"per-line wavs: copy ~/studio/tts/{EP}/*.wav to studio/public/episodes/{EP}/vo/ on the Spark "
                            "(tts_measure.py writes them); music + sfx from studio/public",
                   "components": "registered horror kit components + core layers only (no unbuilt components)"},
    }
    return sb


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
            print(f"| {mmss(it['start'])} | {it['dur']:.2f} | {it['spk']} | {it['text']} | {it['beat']} | {it['opts'].get('screen', '')} |")
        else:
            print(f"| {mmss(it['start'])} | {it['dur']:.2f} | — | *[silence {it['dur']} s]* | {it['beat']} | {it['opts'].get('screen', '')} |")
    print("\n## SCENES")
    t = 0
    for s in build_scenes():
        print(f"| {s['id']} | {t:.2f} | {t + s['duration']:.2f} | {s.get('notes', '')} |")
        t += s["duration"]
    print("\n## JOLTS")
    print(", ".join(f"{mmss(tt)} {lab}" for lab, tt in sorted(J, key=lambda x: x[1])))
    print("\n## KEY TIMES")
    for ref in ["n1:inside", "s1:inside", "n4", "r1", "n5.end", "n6:kitchen", "n9:bounced", "r4", "n10", "s2:Six", "n12", "n12:Taken",
                "n13", "r5", "n14", "c1", "c1:We", "n15.end", "n16", "n17", "n18", "r6", "n19", "n19.end"]:
        tt = at(ref)
        print(f"{ref}: {tt:.2f} ({100 * tt / RUNTIME:.0f}%)")


if __name__ == "__main__":
    sb = storyboard()
    json.dump({"runtime": RUNTIME, "beats": BEATS,
               "items": [{k: v for k, v in it.items() if k != "opts"} | {"screen": it["opts"].get("screen", "")} for it in ITEMS],
               "stats": stats()}, open(os.path.join(HERE, "timeline.json"), "w"), indent=1)
    json.dump(sb, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1, ensure_ascii=False)
    if "--tables" in sys.argv:
        tables()
    print(f"runtime {RUNTIME} s, scenes {len(sb['scenes'])}", file=sys.stderr)
