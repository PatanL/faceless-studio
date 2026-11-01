"""Build the measured timeline, pacing stats and storyboard.json for horror-mom-two-chats (final, single cut).

usage: python3 build.py [--tables]        (stdlib only; safe on the Mac)
inputs : lines.py (the spoken lines), tts_durations.json (Kokoro per-line durations measured on the Spark CPU)
outputs: timeline.json, storyboard.json; --tables prints the markdown tables that script.md carries.

Every visual uses components the horror kit registers today plus core layers (rect / circle / text / svg).
The horror kit is locked (BRIEF 11:27), so everything the kit lacks is drawn here as inline SVG or core layers:
the fridge note, the key hook (with / without keys), the red EXIT glow under the door, the peephole figure, the
deadbolt and lever macros, the door gap, the hall closet (door, under-glow, interior, swinging sleeve), the
closet phone with the self-typing draft, the outgoing / connected call screens and the battery chip.
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
EP = "horror-mom-two-chats"
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
        if s is None:
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
    """'n3' = line start, 'n3.end', 'n3:door' = first word starting with 'door', 'n3:the#2' = 2nd match."""
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
                    t = it["end"] + (float(off[3:]) if len(off) > 3 else 0.0)
                elif off.startswith("w:"):
                    t = at(f"{it['id']}:{off[2:]}")
                else:
                    raise ValueError(off)
            else:
                t = it["start"] + off
            cues.append({"cue": cue, "at": round(max(0.0, t), 3), "volume": round(0.8 * 10 ** (db / 20), 3)})
    return sorted(cues, key=lambda c: c["at"])


# ------------------------------------------------------------------ captions

EMPH = {"outside.", "don't", "door.", "even", "key.", "three", "hook.", "deadbolt.", "lock.", "pocket.", "keys.", "marigold.",
        "chain", "never", "lied", "shadow", "slowly.", "behind", "closet.", "typing.", "four", "eight", "two", "empty.", "here.",
        "outside.", "black.", "bathroom.", "dead.", "swinging.", "turn", "click.", "nine.", "kitchen.", "trust.", "412."}


def captions():
    words = []
    for it in ITEMS:
        if it["kind"] != "line":
            continue
        cap = it["opts"].get("cap", {})
        for w in it["words"]:
            shown = cap.get(w["w"], w["w"])
            if shown == "":
                if words:
                    words[-1]["end"] = w["e"]
                continue
            d = {"text": shown, "start": w["s"], "end": w["e"]}
            if w["w"].lower() in EMPH or shown.lower() in EMPH:
                d["emph"] = True
            words.append(d)
    return words


# ------------------------------------------------------------------ stats


def stats():
    lines = [it for it in ITEMS if it["kind"] == "line"]
    words = sum(len(it["text"].split()) for it in lines)
    speech = sum(it["dur"] for it in lines)
    sil = sum(it["dur"] for it in ITEMS if it["kind"] == "silence")
    sents = []
    for it in lines:
        for s in re.split(r"(?<=[.!?:])\s+", it["text"].strip()):
            if s:
                sents.append((it["spk"], len(s.split()), s))
    lens = [n for _, n, _ in sents]
    nlens = [n for spk, n, _ in sents if spk == "N"]
    you_s = [s for _, _, s in sents if re.search(r"\b(you|your)\b", s, re.I)]
    you_w = sum(len(re.findall(r"\b(you|your)\b", it["text"], re.I)) for it in lines)
    by_spk = {}
    for it in lines:
        by_spk[it["spk"]] = by_spk.get(it["spk"], 0) + len(it["text"].split())
    distinct_numbers = ["11:40 (cover)", "nine seconds", "ten", "three percent", "Sunday", "Room 412", "eight minutes",
                        "two percent", "three inches", "nine (o'clock)", "two officers", "Room 412 (again, as the threat)"]
    q = sum(it["text"].count("?") for it in lines)
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
        "questions": q,
        "questions_per_min": round(q / (RUNTIME / 60), 1),
        "distinct_numbers": distinct_numbers,
        "numbers_per_min": round(len(distinct_numbers) / (RUNTIME / 60), 1),
        "line1_words": len(BY["n1"]["text"].split()) + len(BY["f1"]["text"].split()),
        "core_hook_words": sum(len(BY[k]["text"].split()) for k in ("n1", "f1", "n2", "p1")),
        "core_hook_s": round(BY["p1"]["end"], 2),
        "contradiction_s": at("p1:Don't"),
        "danger_at_door_s": at("n3:door"),
        "words_first_10s": sum(1 for it in lines for w in it["words"] if w["s"] < 10),
    }


def jolts():
    """(label, time): each one a new anomaly, rule, sound, notification, number, question or proof."""
    J = [
        ("two Mom banners (frame 0)", 0.0), ("unlock the door", at("f1")), ("nine seconds later", at("n2")),
        ("don't open it (contradiction)", at("p1")), ("one of them is outside our door", at("n3:outside")),
        ("rule: door locked after ten", at("n4:After")), ("loophole: she has her own key", at("n4:She")),
        ("3% battery plea", at("f2:Phone's")), ("rule as a test: use your key", at("n5:Use")),
        ("check the hook", at("f3:Check")), ("keys on the hook", at("n6")), ("hand on the deadbolt", at("n6:hand")),
        ("private: don't touch that lock", at("p2")), ("how did she know?", at("n7")), ("they're in my pocket (lie)", at("p3:They're")),
        ("no typing dots", at("n8")), ("code word asked", at("n9")), ("never typed it", at("n9:never")),
        ("group dodges", at("f4")), ("Marigold", at("p4")), ("chain on", at("n10:slid")), ("doorbell", at("n11:doorbell")),
        ("peephole: scrubs too close", at("n12:blue")), ("motion light rule", at("n13")), ("it never clicked on", at("n13:never")),
        ("Dad never posts", at("n14:Dad#2")), ("silent Dad bubbles", BY["q1"]["start"]), ("never lied", at("n15:never")),
        ("I can see your shadow", at("f5")), ("handle tilts", at("n16")), ("CAPS + knocks", BY["q2"]["start"]),
        ("calls Dad", at("n17:called")), ("ringback", BY["q3"]["start"]), ("ringtone", at("n18")),
        ("behind me, in the closet", at("n18:Behind")), ("4 s ring silence", BY["q4"]["start"]),
        ("Dad is typing", at("n19:Dad")), ("don't turn around", BY["q5"]["start"]), ("Room 412", at("n20:Room")),
        ("real Dad answers", at("d1")), ("cell in the closet", at("d2:closet")), ("who's typing?", at("n22")),
        ("police called", at("d3:front")), ("8 minutes / 2%", at("n23:battery")), ("it hears her", at("f6")),
        ("hook empty", at("n24:Empty")), ("nobody came in", at("n24:Nobody")), ("key in the lock", at("n25:key")),
        ("rule spoken back", at("n26")), ("deadbolt turns / chain", at("n27:slammed")), ("helper: hide in the closet", at("p5")),
        ("Dad: that's where my phone is", at("d4:That's")), ("bathroom", at("d4:bathroom")), ("battery dies", at("n29:black")),
        ("closet opens itself", at("n30:swung")), ("sleeve still swinging", at("n31:sleeve")), ("phone typing", at("n32:typing")),
        ("draft: turn around nora", BY["q8"]["start"] + 0.6), ("I didn't", at("n33:didn't")), ("red/blue light", at("n34")),
        ("gap closes", at("n34:gap")), ("police", at("n35:Police")), ("light test", at("n36:watched")),
        ("light clicks on", at("n37")), ("never for her", at("n37:never")), ("breaks the rule: chain off", at("n38:Chain")),
        ("Mom from the elevator", at("n39:Mom")), ("Mom: phone died at nine", at("r1:died")), ("I never texted you", at("r1:never")),
        ("it knew Marigold", at("n40")), ("only said in our kitchen", at("r2:kitchen")), ("it was in our kitchen", at("n41")),
        ("dead phone lights up", at("n42:lit")), ("first typing dots", at("p6", -0.9)), ("whose voice you trust", at("p6")),
        ("Room 412, in Dad's voice", at("x1")),
    ]
    ts = sorted(t for _, t in J)
    gaps = [b - a for a, b in zip(ts, ts[1:])] + [RUNTIME - ts[-1]]
    return J, round(statistics.median(gaps), 2), round(max(gaps), 2)


# ------------------------------------------------------------------ layer helpers

W, H = 1080, 1920
RED = "#ff3b3b"
EXIT_RED = "#ff2a24"
WARM = "#f1c37c"
INK = "#0f1115"
GREY = "#8a8f99"
MOM_C = "#d9822b"
DAD_C = "#5a6b8f"
ME_C = "#3d7bd9"

P_CX, P_CY, P_W, P_H = 540, 1110, 800, 1620     # static phone frame (call screens)
S_X0, S_Y0, S_W = 160, 320, 760


def rect(x, y, w, h, fill, radius=0, **kw):
    d = {"type": "rect", "x": x, "y": y, "width": w, "height": h, "fill": fill, "radius": radius}
    d.update(kw)
    return d


def circle(x, y, r, fill, **kw):
    d = {"type": "circle", "x": x, "y": y, "width": 2 * r, "height": 2 * r, "fill": fill}
    d.update(kw)
    return d


def text(s, x, y, size=40, color="#ffffff", weight=800, align="center", font="body", **kw):
    d = {"type": "text", "text": s, "x": x, "y": y, "fontSize": size, "color": color, "weight": weight, "align": align, "font": font}
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


def vignette(amount=0.45, color=None, **kw):
    p = {"amount": amount}
    if color:
        p["color"] = color
    p.update(kw)
    return comp("horror/Vignette", p, depth=0, z=50)


def nora(expr="scared", exprs=None, pose="phone", lookX=0.0, lookY=0.4, light="phone", z=40, width=1150, **kw):
    p = {"pose": pose, "exprs": exprs or [{"t": 0, "e": expr}], "lookX": lookX, "lookY": lookY, "light": light, "blink": kw.pop("blink", True)}
    p.update(kw.pop("props", {}))
    return comp("horror/Protagonist", p, x="50%", y="100%", anchorY=1, width=width, height=round(width * 1.52), z=z, depth=0, **kw)


# --- the front door with the red EXIT glow (hall light OFF) and optional feet
def red_strip(z=3, feet=True, warm=None, two_pairs=False):
    """Overlay on a full-frame horror/FrontDoor (hallLight 0): the strip under the door lit only by the red EXIT sign.
    warm=(t) switches it to the warm motion light at scene time t."""
    out = [rect(540, 1671, 500, 10, EXIT_RED, z=z, opacity=0.9),
           rect(540, 1700, 600, 70, EXIT_RED, z=z, opacity=0.28, blur=22)]
    if warm is not None:
        out[0] = dict(out[0], keyframes=[{"t": 0, "opacity": 0.9}, {"t": round(warm, 3), "opacity": 0.9}, {"t": round(warm + 0.06, 3), "opacity": 0.0}])
        out[1] = dict(out[1], keyframes=[{"t": 0, "opacity": 0.28}, {"t": round(warm, 3), "opacity": 0.28}, {"t": round(warm + 0.06, 3), "opacity": 0.0}])
        out += [rect(540, 1671, 500, 10, WARM, z=z, opacity=0.0,
                     keyframes=[{"t": 0, "opacity": 0}, {"t": round(warm, 3), "opacity": 0}, {"t": round(warm + 0.06, 3), "opacity": 1}]),
                rect(540, 1700, 640, 90, WARM, z=z, opacity=0.0, blur=26,
                     keyframes=[{"t": 0, "opacity": 0}, {"t": round(warm, 3), "opacity": 0}, {"t": round(warm + 0.06, 3), "opacity": 0.45}])]
    if feet:
        xs = [(440, 600)] if not two_pairs else [(345, 430), (585, 670)]
        for a, b in xs:
            out += [rect(a, 1670, 70, 14, "#040405", z=z + 1), rect(b, 1670, 70, 14, "#040405", z=z + 1)]
    return out


def door(props=None, feet=True, z=0, warm=None, two_pairs=False, gap=None, **kw):
    p = {"chain": "on", "hallLight": 0.0, "feet": False, "peepholeGlow": 0}
    p.update(props or {})
    lay = [full("horror/FrontDoor", p, z=z, **kw)]
    lay += red_strip(z=z + 3, feet=feet, warm=warm, two_pairs=two_pairs)
    if gap is not None:  # [(t, open 0..1)] the door opened to the chain: black slit at the latch edge
        lay.append(rect(790, 1000, 40, 1340, "#000000", z=z + 4, anchorX=0, scaleX=0.0,
                        keyframes=[{"t": round(t, 3), "scaleX": v, "ease": "out"} for t, v in gap]))
    return lay


# --- inline SVG props (original art, drawn in code)
def key_hook_svg(keys=True):
    k = ""
    if keys:
        k = ('<path d="M 520 742 Q 470 980 520 1180 Q 560 1240 600 1180 Q 650 980 600 742" stroke="#c4202a" stroke-width="26" fill="none"/>'
             '<rect x="540" y="1168" width="40" height="60" rx="8" fill="#9a968d" stroke="#141418" stroke-width="5"/>'
             '<circle cx="560" cy="1268" r="44" fill="none" stroke="#b7b3aa" stroke-width="12"/>'
             '<path d="M 540 1300 l -30 150 l 18 6 l 6 -24 l 12 4 l 6 -24 l -12 -4 l 14 -100 Z" fill="#c9b27a" stroke="#141418" stroke-width="5"/>'
             '<path d="M 580 1302 l 46 140 l -16 8 l -10 -22 l -12 6 l -8 -22 l 12 -6 l -30 -96 Z" fill="#a9a59c" stroke="#141418" stroke-width="5"/>'
             '<path d="M 562 1310 l 4 160 l 18 0 l 0 -24 l 12 0 l 0 -24 l -12 0 l -2 -110 Z" fill="#b8b4aa" stroke="#141418" stroke-width="5"/>')
    return ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="kw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2c3443"/><stop offset="1" stop-color="#1e2430"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#kw)"/>'
            '<rect x="860" y="0" width="220" height="1920" fill="#3a404b" stroke="#141418" stroke-width="10"/>'
            '<rect x="430" y="640" width="260" height="70" rx="14" fill="#4a4f59" stroke="#141418" stroke-width="8"/>'
            '<path d="M 560 700 Q 556 760 520 770 Q 500 772 498 752" stroke="#8d8a83" stroke-width="22" fill="none" stroke-linecap="round"/>'
            '<circle cx="470" cy="676" r="9" fill="#2a2e36"/><circle cx="650" cy="676" r="9" fill="#2a2e36"/>'
            + k + '</svg>')


def note_layers(hl_even=None, hl_key=None, z=10):
    """The fridge note: yellow sticky + Mom's rule in Anton caps + Dad's hotel line. hl_*: scene times to turn red."""
    lay = [rect(540, 960, 1080, 1920, "#1f252d", z=z),
           rect(540, 960, 900, 1920, "#d5d9de", z=z + 1, opacity=0.08),
           rect(1000, 980, 22, 520, "#9aa3ad", radius=10, z=z + 1, opacity=0.5),
           rect(540, 900, 820, 900, "#f1dc6a", radius=6, z=z + 2, rotate=-2.5, shadow="0 24px 40px rgba(0,0,0,.55)"),
           circle(540, 470, 34, "#c4202a", z=z + 3, stroke="#5a0d12", strokeWidth=5)]
    rule = [("AFTER 10", 640), ("THE DOOR STAYS", 750), ("LOCKED.", 860)]
    for s, y in rule:
        lay.append(text(s, 540, y, 80, "#1b1a20", 400, font="display", rotate=-2.5, z=z + 3))
    ev = text("EVEN FOR ME.", 540, 985, 80, "#1b1a20", 400, font="display", rotate=-2.5, z=z + 3)
    ky = text("I HAVE MY KEY. —M", 540, 1105, 72, "#1b1a20", 400, font="display", rotate=-2.5, z=z + 3)
    lay += [ev, ky]
    if hl_even is not None:
        lay.append(rect(290, 1035, 500, 10, RED, z=z + 4, rotate=-2.5, anchorX=0, scaleX=0,
                        keyframes=[{"t": round(hl_even, 3), "scaleX": 0}, {"t": round(hl_even + 0.35, 3), "scaleX": 1, "ease": "out"}]))
    if hl_key is not None:
        lay.append(dict(ky, color="#d0121c", z=z + 5, opacity=0, keyframes=[{"t": round(hl_key, 3), "opacity": 0}, {"t": round(hl_key + 0.12, 3), "opacity": 1}]))
    lay += [rect(540, 1450, 820, 4, "#1b1a20", z=z + 3, rotate=-2.5, opacity=0.25),
            text("Dad: Lakeview Suites, Rm 412 (back Sun)", 540, 1290, 34, "#26303c", 700, font="body", rotate=-2.5, z=z + 3, opacity=0.9)]
    return lay


EXIT_GLOW = '<radialGradient id="eg"><stop offset="0" stop-color="#ff2a24" stop-opacity="0.7"/><stop offset="1" stop-color="#ff2a24" stop-opacity="0"/></radialGradient>'


def peephole_overlay_svg(officers=False):
    """Drawn over horror/Peephole (figure none). The lens is a 994 px circle. Dark corridor, red EXIT glow, and either the
    blue-scrubs figure pressed too close to the lens, head bowed (no face), or two lit officer silhouettes."""
    if not officers:
        body = ('<path d="M -40 994 L -40 640 Q 120 520 330 500 Q 500 486 660 500 Q 880 520 1034 640 L 1034 994 Z" fill="#1f3b57"/>'
                '<path d="M 300 520 Q 497 600 694 520 L 660 620 Q 497 690 334 620 Z" fill="#183049"/>'
                '<path d="M 497 560 L 497 994" stroke="#16293d" stroke-width="10"/>'
                '<ellipse cx="497" cy="360" rx="200" ry="230" fill="#07090c"/>'
                '<path d="M 300 330 Q 497 120 694 330 Q 640 220 497 200 Q 354 220 300 330 Z" fill="#050608"/>'
                '<rect x="0" y="0" width="994" height="994" fill="url(#eg2)" opacity="0.55"/>')
        return ('<svg viewBox="0 0 994 994" xmlns="http://www.w3.org/2000/svg"><defs>' + EXIT_GLOW +
                '<radialGradient id="eg2" cx="0.8" cy="0.2" r="0.9"><stop offset="0" stop-color="#ff2a24" stop-opacity="0.35"/><stop offset="1" stop-color="#ff2a24" stop-opacity="0"/></radialGradient>'
                '<clipPath id="lens"><circle cx="497" cy="497" r="497"/></clipPath></defs>'
                '<g clip-path="url(#lens)"><rect width="994" height="994" fill="#07080b" opacity="0.55"/>'
                '<rect x="760" y="150" width="120" height="44" rx="6" fill="#ff2a24"/><circle cx="820" cy="172" r="160" fill="url(#eg)"/>'
                + body + '</g></svg>')
    fig = ''.join(f'<g transform="translate({x} 0)"><ellipse cx="0" cy="430" rx="62" ry="74" fill="#0b0d12"/>'
                  f'<path d="M -150 994 L -150 640 Q -120 540 0 520 Q 120 540 150 640 L 150 994 Z" fill="#141a26"/>'
                  f'<rect x="-40" y="600" width="26" height="18" fill="#c9b27a"/></g>' for x in (330, 670))
    return ('<svg viewBox="0 0 994 994" xmlns="http://www.w3.org/2000/svg"><defs><clipPath id="lens"><circle cx="497" cy="497" r="497"/></clipPath>'
            '<radialGradient id="wl" cx="0.5" cy="0.1" r="0.8"><stop offset="0" stop-color="#f1c37c" stop-opacity="0.55"/><stop offset="1" stop-color="#f1c37c" stop-opacity="0"/></radialGradient></defs>'
            '<g clip-path="url(#lens)"><rect width="994" height="994" fill="url(#wl)"/>' + fig + '</g></svg>')


def deadbolt_svg():
    return ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
            '<defs><linearGradient id="dd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4d3d35"/><stop offset="1" stop-color="#33282a"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#dd)"/>'
            '<rect x="880" y="0" width="200" height="1920" fill="#3a404b" stroke="#141418" stroke-width="10"/>'
            '<rect x="120" y="300" width="640" height="560" fill="none" stroke="#2a211d" stroke-width="14" opacity="0.6"/>'
            '<circle cx="540" cy="1000" r="230" fill="#a9a59c" stroke="#141418" stroke-width="14"/>'
            '<circle cx="540" cy="1000" r="170" fill="#bdb9b0" opacity="0.5"/></svg>')


THUMB = ('<svg viewBox="0 0 120 460" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="10" width="100" height="440" rx="34" '
         'fill="#7f7b73" stroke="#141418" stroke-width="12"/><rect x="40" y="40" width="40" height="380" rx="14" fill="#9a968d"/></svg>')
LEVER_PLATE = ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><rect width="1080" height="1920" fill="#43352f"/>'
               '<rect x="880" y="0" width="200" height="1920" fill="#3a404b" stroke="#141418" stroke-width="10"/>'
               '<rect x="160" y="1180" width="640" height="560" fill="none" stroke="#2a211d" stroke-width="14" opacity="0.6"/>'
               '<circle cx="700" cy="960" r="120" fill="#a9a59c" stroke="#141418" stroke-width="14"/></svg>')
LEVER = ('<svg viewBox="0 0 600 120" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="20" width="560" height="80" rx="38" '
         'fill="#bdb9b0" stroke="#141418" stroke-width="12"/><circle cx="540" cy="60" r="58" fill="#a9a59c" stroke="#141418" stroke-width="12"/></svg>')

WALL = ('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
        '<defs><linearGradient id="hw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1c2129"/><stop offset="1" stop-color="#272d38"/></linearGradient></defs>'
        '<rect width="1080" height="1920" fill="url(#hw)"/><rect y="1700" width="1080" height="220" fill="#17151a"/>'
        '<rect y="1680" width="1080" height="28" fill="#13161c"/>'
        '<rect x="160" y="300" width="560" height="1400" fill="#30353f" stroke="#0f1014" stroke-width="12"/>'
        '<rect x="840" y="880" width="70" height="110" rx="10" fill="#c9c4b8" opacity="0.5"/></svg>')
CLOSET_DOOR = ('<svg viewBox="0 0 520 1360" xmlns="http://www.w3.org/2000/svg"><rect x="0" y="0" width="520" height="1360" fill="#3b3f48" '
               'stroke="#0f1014" stroke-width="12"/>' + ''.join(f'<rect x="70" y="{y}" width="380" height="16" rx="4" fill="#2a2d34"/>' for y in range(110, 600, 44)) +
               ''.join(f'<rect x="70" y="{y}" width="380" height="16" rx="4" fill="#2a2d34"/>' for y in range(760, 1250, 44)) +
               '<circle cx="450" cy="690" r="22" fill="#9a968d" stroke="#0f1014" stroke-width="6"/></svg>')
CLOSET_INSIDE = (
    '<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="1080" height="1920" fill="#060708"/>'
    '<rect x="60" y="420" width="960" height="18" rx="8" fill="#5d6570"/>'
    '<path d="M 150 440 Q 110 900 140 1500 L 330 1500 Q 350 900 300 440 Z" fill="#20262e"/>'
    '<path d="M 800 440 Q 760 900 780 1460 L 960 1460 Q 990 900 940 440 Z" fill="#2a1f22"/>'
    '<path d="M 330 450 Q 250 1000 300 1660 L 780 1660 Q 830 1000 750 450 Q 640 400 540 420 Q 440 400 330 450 Z" fill="#5b616b" stroke="#0b0c0f" stroke-width="10"/>'
    '<path d="M 540 430 L 540 1650" stroke="#383c43" stroke-width="10"/>'
    '<path d="M 470 440 L 540 640 L 610 440" fill="#3e434b" stroke="#0b0c0f" stroke-width="8"/>'
    '<rect x="580" y="1080" width="170" height="150" rx="16" fill="#3e434b" stroke="#0b0c0f" stroke-width="8"/>'
    '<path d="M 540 420 L 540 380 Q 540 350 570 350" stroke="#7d828c" stroke-width="8" fill="none"/>'
    '</svg>')
SLEEVE = ('<svg viewBox="0 0 200 900" xmlns="http://www.w3.org/2000/svg"><path d="M 40 0 Q 0 400 50 860 L 170 880 Q 190 420 150 0 Z" '
          'fill="#565c66" stroke="#0b0c0f" stroke-width="10"/><rect x="48" y="820" width="122" height="60" rx="10" fill="#3a3e45"/></svg>')
SILHOUETTE_BACK = (
    '<svg viewBox="0 0 600 760" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M 20 760 Q 40 470 190 430 Q 250 410 300 412 Q 350 410 410 430 Q 560 470 580 760 Z" fill="#14171c"/>'
    '<path d="M 200 440 Q 300 486 400 440 Q 380 404 300 400 Q 220 404 200 440 Z" fill="#1d2128"/>'
    '<path d="M 300 70 Q 175 72 168 200 Q 162 300 150 392 Q 196 420 240 404 Q 270 416 300 412 Q 330 416 360 404 '
    'Q 404 420 450 392 Q 438 300 432 200 Q 425 72 300 70 Z" fill="#0c0d10"/>'
    '<path d="M 432 210 Q 440 300 450 390" stroke="#9cc2ff" stroke-width="6" fill="none" opacity="0.45"/>'
    '<path d="M 168 210 Q 160 300 150 390" stroke="#9cc2ff" stroke-width="6" fill="none" opacity="0.45"/></svg>')


def hall_wall(closet_x=440, glow=None, open_kf=None, z=0, inside=False):
    """Our apartment's inner hallway, front-on: the hall closet door (louvered) with a phone glow under it.
    glow: list of (t, opacity) keys for the under-door glow; open_kf: [(t, scaleX)] the door swinging open (hinge left)."""
    lay = [svg(WALL, 540, 960, 1080, 1920, z=z)]
    if inside:
        lay.append(svg(CLOSET_INSIDE, 440, 1000, 560, 1400, z=z + 1))
    else:
        lay.append(rect(440, 1000, 560, 1400, "#050506", z=z + 1))
    lay.append(rect(440, 1702, 520, 12, "#7fb4ff", z=z + 2, opacity=0.0, blur=6,
                    keyframes=[{"t": round(t, 3), "opacity": v, "ease": "linear"} for t, v in (glow or [(0, 0.0)])]))
    d = svg(CLOSET_DOOR, 180, 1000, 520, 1360, z=z + 3, anchorX=0)
    if open_kf:
        d["keyframes"] = [{"t": round(t, 3), "scaleX": v, "ease": "inOut"} for t, v in open_kf]
    lay.append(d)
    return lay


def ring_glow(t0, n_rings, period=2.0):
    """Under-door glow keys that pulse with the desk bell (two 0.4 s bursts per 2.0 s cycle)."""
    keys = [(0, 0.0)]
    for c in range(n_rings):
        b = t0 + c * period
        keys += [(b, 0.0), (b + 0.05, 0.85), (b + 0.4, 0.3), (b + 0.6, 0.85), (b + 1.0, 0.25), (b + 1.9, 0.12)]
    return keys


# --- phone helpers
MEMBERS = {"Mom": {"color": MOM_C, "initials": "M"}, "Dad": {"color": DAD_C, "initials": "D"}}


def handphone(chat=None, mode="chat", lock=None, banners=None, vibrate=None, tremble=1.5, tilt=-3, glitch=None, screens=None,
              clock="11:41", battery=6, cy=0.6):
    phone = {"members": MEMBERS, "mode": mode}
    if chat:
        phone["chat"] = {"theme": "dark", "scale": 1.25, "clock": clock, "battery": battery, **chat}
    if lock:
        phone["lock"] = {"battery": battery, **lock}
    if banners:
        phone["banners"] = banners
    if vibrate:
        phone["vibrate"] = vibrate
    if screens:
        phone["screens"] = screens
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": cy, "tilt": tilt, "tremble": tremble, "side": "right", "phone": phone,
         "thumbY": 0.94, "thumbReach": 0.1}
    if glitch:
        p["glitch"] = glitch
    return comp("horror/HandPhone", p, z=10)


def msgs(thread, scene_start):
    return [{**m, "at": round(m["at"] - scene_start, 3)} for m in thread]


def typing(spans, scene_start):
    return [{"from": f, "at": round(a - scene_start, 3), "until": round(b - scene_start, 3)} for f, a, b in spans]


def family(t0, upto=None, typing_spans=(), clock="11:41", battery=6, **kw):
    th = [m for m in FAMILY if upto is None or m["at"] <= upto]
    return {"title": "Family", "count": 3, "subtitle": "Mom, Dad, you", "accent": ME_C, "messages": msgs(th, t0),
            "typing": typing(typing_spans, t0), **kw}


def private(t0, upto=None, typing_spans=(), **kw):
    th = [m for m in PRIVATE if upto is None or m["at"] <= upto]
    return {"title": "Mom", "dm": "Mom", "subtitle": "mobile", "accent": ME_C, "messages": msgs(th, t0),
            "typing": typing(typing_spans, t0), **kw}


def phone_frame(clock="11:47", battery="2%", bat_red=True):
    return [rect(P_CX, P_CY, P_W, P_H, "#15171c", radius=96, stroke="#2c3038", strokeWidth=8, z=1),
            rect(P_CX, P_CY, P_W - 40, P_H - 40, "#16131c", radius=76, z=2),
            text(clock, S_X0 + 40, S_Y0 + 40, 30, "#e8e8ea", 700, "left", z=3),
            text(battery, S_X0 + S_W - 40, S_Y0 + 40, 30, RED if bat_red else "#e8e8ea", 900, "right", z=3)]


def call_screen(t0, t1, name, sub, initials, color, connected_at=None, label="calling…", ended_at=None, clock="11:47",
                battery="2%", z=0):
    """Outgoing / connected call drawn from core layers (one red End button, no Accept), on a static phone frame.
    Times are scene-local. connected_at starts a per-second timer."""
    lay = timed(phone_frame(clock, battery, battery.endswith("%") and int(battery[:-1]) < 20), t0, t1, z)
    lay += timed([text(sub, 540, 470, 32, "#aab0bb", 700, z=4), text(name, 540, 540, 60, "#ffffff", 900, z=4, maxWidth=680),
                  circle(540, 860, 130, color, z=4), text(initials, 540, 860, 110, "#ffffff", 900, z=5),
                  circle(540, 1640, 70, "#d23a3f", z=4), text("End", 540, 1745, 28, "#c9ced6", 700, z=4)], t0, t1, z)
    ce = connected_at if connected_at is not None else t1
    lay += timed([text(label, 540, 610, 34, "#aab0bb", 700, z=4)], t0, min(ce, t1), z)
    if connected_at is None:
        for i in range(3):
            lay += timed([circle(540, 860, 130, "rgba(0,0,0,0)", stroke="rgba(220,200,255,0.5)", strokeWidth=5, z=3,
                                 idle=[{"type": "pulse", "amount": 0.45, "speed": 0.8, "phase": i / 3}])], t0, t1, z)
    else:
        end = ended_at if ended_at is not None else t1
        n = int((end - connected_at) // 1) + 1
        for k in range(n):
            ts, te = max(t0, connected_at + k), min(connected_at + k + 1, end)
            if connected_at + k >= end:
                break
            if te <= ts:
                continue
            lay += timed([text(f"00:{k:02d}", 540, 610, 34, "#7fd1a0", 800, z=4)], ts, te, z)
        if ended_at is not None and ended_at < t1:
            lay += timed([text("Call ended", 540, 610, 34, RED, 800, z=4)], ended_at, t1, z)
    return lay


def closet_phone(t0, t1, draft_at, z=0):
    """The peak macro: Dad's phone half out of the grey coat pocket, Family thread, the draft typing itself."""
    cx, cy = 540, 840
    lay = [rect(540, 960, 1080, 1920, "#2f3339", z=z),
           svg('<svg viewBox="0 0 1080 1920" xmlns="http://www.w3.org/2000/svg"><path d="M 0 1480 Q 540 1380 1080 1500 L 1080 1920 L 0 1920 Z" '
               'fill="#3e434b" stroke="#0b0c0f" stroke-width="12"/><path d="M 0 1520 Q 540 1430 1080 1540" stroke="#2a2e34" stroke-width="10" fill="none"/></svg>',
               540, 960, 1080, 1920, z=z + 6),
           rect(cx, cy, 640, 1240, "#0d0e12", radius=70, rotate=12, z=z + 2, stroke="#3a3e47", strokeWidth=8),
           rect(cx, cy, 590, 1190, "#12141a", radius=54, rotate=12, z=z + 3),
           circle(cx, cy, 520, "rgba(127,180,255,0.20)", z=z + 1, blur=80),
           text("Family", cx + 30, cy - 470, 44, "#ffffff", 900, rotate=12, z=z + 4),
           text("3 members", cx + 40, cy - 420, 26, GREY, 700, rotate=12, z=z + 4),
           text("Just open the front door.", cx - 60, cy - 120, 32, "#eef0f3", 700, rotate=12, z=z + 4, background="#262b34", padding=18, radius=24),
           rect(cx - 44, cy + 270, 470, 74, "#1d2129", radius=37, rotate=12, z=z + 4, stroke="#3a3e47", strokeWidth=3),
           text("turn around nora", cx - 230, cy + 225, 50, "#ffffff", 800, "left", rotate=12, z=z + 5,
                typewriter={"at": round(draft_at, 3), "cps": 5.0}),
           rect(cx + 260, cy + 250, 6, 46, "#7fb4ff", rotate=12, z=z + 5, idle=[{"type": "pulse", "amount": 0.9, "speed": 2.0}]),
           vignette(0.7)]
    return timed(lay, t0, t1)


# ------------------------------------------------------------------ threads (absolute times)

FAMILY: list = []
PRIVATE: list = []


def threads():
    FAMILY[:] = [
        {"from": "Mom", "text": "night shift tonight. love you. lock up 🔒", "at": -500},
        {"from": "Dad", "text": "ok", "at": -499},
        {"from": "Mom", "text": "I'm outside. Unlock the door.", "at": 0.01},
        {"from": "Mom", "text": "hands full honey", "at": at("f2")},
        {"from": "Mom", "text": "phone's on 3%", "at": at("f2:Phone's")},
        {"from": "Mom", "text": "please", "at": at("f2:Please")},
        {"me": True, "text": "Rule. Use your key.", "at": at("n5:Use")},
        {"from": "Mom", "text": "forgot them this morning", "at": at("f3")},
        {"from": "Mom", "text": "check the hook", "at": at("f3:Check")},
        {"me": True, "text": "what's our word?", "at": at("n9:both")},
        {"from": "Mom", "text": "Nora I'm not doing this in the hallway", "at": at("f4")},
        {"from": "Mom", "text": "open up", "at": at("f4:Open")},
        {"from": "Dad", "text": "It's really her, kiddo.", "at": BY["q1"]["start"] + 0.1},
        {"from": "Dad", "text": "I just talked to her.", "at": BY["q1"]["start"] + 0.95},
        {"from": "Dad", "text": "Let your mother in.", "at": BY["q1"]["start"] + 1.8},
        {"from": "Mom", "text": "I can see your shadow under the door, Nora.", "at": at("f5")},
        {"from": "Mom", "kind": "alert", "text": "NORA. OPEN. THE DOOR.", "at": BY["q2"]["start"]},
        {"from": "Dad", "text": "Don't turn around, kiddo.", "at": BY["q5"]["start"] + 0.1},
        {"from": "Dad", "text": "Just open the front door.", "at": BY["q5"]["start"] + 1.0},
    ]
    PRIVATE[:] = [
        {"from": "Mom", "text": "be safe tonight ❤️", "at": -900},
        {"from": "Mom", "text": "Don't open it. I'm still at work.", "at": 0.02},
        {"from": "Mom", "text": "Don't touch that lock.", "at": at("p2")},
        {"me": True, "text": "ur keys are right here on the hook??", "at": at("n7.end", -0.35)},
        {"from": "Mom", "text": "No they're not.", "at": at("p3")},
        {"from": "Mom", "text": "They're in my pocket.", "at": at("p3", 0.25)},
        {"me": True, "text": "what's our word?", "at": at("n9:asked")},
        {"from": "Mom", "text": "Marigold.", "at": at("p4")},
        {"from": "Mom", "text": "Now put the chain on.", "at": at("p4:Now")},
        {"from": "Mom", "text": "Now I know whose voice you trust.", "at": at("p6")},
        {"from": "Mom", "text": "Next time, I'll call from Room 412.", "at": at("x1")},
    ]


# ------------------------------------------------------------------ scenes


def scene(sid, t0, t1, layers, bg="#07080b", camera=None, trans=None, notes=None, captionY=None, hold_ok=False):
    d = {"id": sid, "duration": round(t1 - t0, 3), "background": {"type": "color", "color": bg}, "layers": layers}
    if camera:
        d["camera"] = camera
    if trans:
        d["transitionIn"] = trans
    if notes:
        d["notes"] = notes
    if captionY is not None:
        d["captionY"] = captionY
    if hold_ok:
        d["_hold_ok"] = True
    return d


def cam(*kf, shake=None):
    c = {"keyframes": [{"t": round(t, 3), "zoom": z, "x": f"{x:.2f}%", "y": f"{y:.2f}%", "ease": e} for t, z, x, y, e in kf]}
    if shake:
        c["shake"] = [{"at": round(a, 3), "duration": d, "amplitude": amp} for a, d, amp in shake]
    return c


def step(t, z, x, y):
    """A hard punch: keyframe pair so the camera jumps at t (an in-scene cut)."""
    return [(max(0.0, t - 0.01), None, None, None, "linear"), (t, z, x, y, "step")]


def cut_cam(segs, end, shake=None):
    """segs: [(t, zoom_start, zoom_end, x, y)] - each segment holds a framing with a slow push, hard cut to the next."""
    kf = []
    for i, (t, z0, z1, x, y) in enumerate(segs):
        te = segs[i + 1][0] if i + 1 < len(segs) else end
        kf.append((t, z0, x, y, "step" if i else "linear"))
        kf.append((max(t + 0.02, te - 0.01), z1, x, y, "linear"))
    return cam(*kf, shake=shake)


def build_scenes():
    threads()
    S = []
    END = RUNTIME

    # 1 HOOK ------------------------------------------------------------------------------------
    t0, t1 = 0.0, at("n3")
    b1, b2 = at("f1") - t0, at("n2") - t0
    lock = {"time": "11:40", "date": "Friday, October 30",
            "notifications": [{"at": -2, "app": "Messages", "title": "Family · Mom", "text": "I'm outside. Unlock the door."},
                              {"at": -1, "app": "Messages", "title": "Mom", "text": "Don't open it. I'm still at work."}]}
    hp = comp("horror/Phone", {"members": MEMBERS, "mode": "lock", "lock": {"battery": 6, **lock}}, x=540, y=760, width=640, height=1320,
              z=10, rotate=-3, shadow="0 30px 60px rgba(0,0,0,.7)")
    lay = door(feet=True, z=0) + [hp, vignette(0.5, "120,0,10"),
                                            rect(700, 1740, 360, 140, EXIT_RED, z=4, opacity=0.18, blur=40)]
    stl = at("p1:still") - t0
    S.append(scene("s01_hook", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.03, 50, 50), (b1, 1.75, 1.8, 50, 45.5), (b2, 1.75, 1.82, 50, 39),
                                   (stl, 1.2, 1.25, 50, 62)], t1 - t0, shake=[(b2 + 0.05, 0.18, 6)]),
                   notes="FRAME 0 = COVER: both Mom banners fully readable on the lock screen (11:40), the front door sharp behind the "
                         "phone with the red EXIT strip under it broken by two feet. Punch-ins: banner 1 on 'I'm outside', banner 2 on "
                         "'Nine seconds later'."))

    # 2 DOOR ------------------------------------------------------------------------------------
    t0, t1 = at("n3"), at("n4")
    o = at("n3:outside") - t0
    lay = door(feet=True) + [comp("horror/Darkness", {"x": 0.5, "y": 0.7, "radius": 0.55, "darkness": 0.7}, depth=0, z=20), vignette(0.5, "120,0,10")]
    S.append(scene("s02_door", t0, t1, lay, trans={"type": "whip", "duration": 0.22, "direction": "left"},
                   camera=cam((0, 1.0, 50, 55, "linear"), (o, 1.12, 50, 70, "linear"), (o + 0.01, 1.9, 50, 86, "step"),
                              (t1 - t0, 2.0, 50, 86, "linear")),
                   notes="Premise paid: the feet in the red EXIT glow. Hall light OFF (the motion sensor never fires for her)."))

    # 3 RULE NOTE -------------------------------------------------------------------------------
    t0, t1 = at("n4"), at("f2")
    ev, key = at("n4:Even") - t0, at("n4:She") - t0
    lay = note_layers(hl_even=ev, hl_key=None, z=0)
    S.append(scene("s03_rule", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.03, 50, 48), (at("n4:After") - t0, 1.12, 1.15, 50, 40), (ev, 1.15, 1.18, 50, 52),
                                   (key, 1.15, 1.2, 50, 60)], t1 - t0),
                   notes="Ownable rule + loophole on one prop. The small second line plants Lakeview Suites Rm 412 (paid at 1:35 and in the last line)."))

    # 4 GROUP PRESSURE --------------------------------------------------------------------------
    t0, t1 = at("f2"), at("n6")
    lay = [full("horror/LivingRoom", {"lamp": 0.25, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
           handphone(family(t0, typing_spans=[("Mom", t0 - 0.5, t0)]), battery=6), vignette(0.4)]
    S.append(scene("s04_group", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 50, 52), (at("f2:Phone's") - t0, 1.22, 1.25, 50, 50), (at("n5") - t0, 1.05, 1.08, 50, 56),
                                   (at("f3") - t0, 1.25, 1.28, 50, 52)], t1 - t0),
                   notes="Warm Mom: plausible details. Nora turns the rule into a test ('Rule. Use your key.'); the group Mom overrules it by pointing at the hook."))

    # 5 KEYS + NEAR-OPEN ------------------------------------------------------------------------
    t0, t1 = at("n6"), at("p2")
    hd = at("n6:hand") - t0
    lay = timed([svg(key_hook_svg(True), 540, 960, 1080, 1920, z=0),
                 comp("horror/Darkness", {"x": 0.52, "y": 0.5, "radius": 0.45, "darkness": 0.75}, depth=0, z=20)], 0, hd)
    lay += timed([svg(deadbolt_svg(), 540, 960, 1080, 1920, z=0),
                  svg(THUMB, 540, 1000, 120, 460, z=2),
                  comp("horror/Darkness", {"x": 0.5, "y": 0.52, "radius": 0.5, "darkness": 0.6}, depth=0, z=20)], hd, t1 - t0)
    lay.append(vignette(0.45))
    S.append(scene("s05_hook_near_open", t0, t1, lay,
                   camera=cam((0, 1.0, 50, 50, "linear"), (hd - 0.01, 1.14, 52, 60, "linear"), (hd, 1.0, 50, 52, "step"),
                              (t1 - t0, 1.2, 50, 52, "linear")),
                   notes="The hook confirms the group Mom (keys on a plain red lanyard). Then the near-open: the deadbolt thumb-turn, close."))

    # 6 PRIVATE LIE -----------------------------------------------------------------------------
    t0, t1 = at("p2"), at("n9")
    st = at("n8:staring") - t0
    lay = timed([full("horror/FrontDoor", {"chain": "off", "hallLight": 0.0}, blur=9, opacity=0.75, depth=0.2),
                 handphone(private(t0), vibrate=[{"at": 0.0, "duration": 0.4, "amount": 1}], battery=6, clock="11:42")], 0, st)
    lay += timed([svg(key_hook_svg(True), 540, 960, 1080, 1920, z=0),
                  comp("horror/Darkness", {"x": 0.52, "y": 0.55, "radius": 0.4, "darkness": 0.8}, depth=0, z=20)], st, t1 - t0)
    lay.append(vignette(0.45))
    nd = at("n8") - t0
    S.append(scene("s06_private_lie", t0, t1, lay,
                   camera=cut_cam([(0, 1.25, 1.28, 50, 47), (at("n7") - t0, 1.0, 1.03, 50, 55), (at("p3") - t0, 1.22, 1.25, 50, 58),
                                   (nd, 1.55, 1.6, 52, 66), (st, 1.25, 1.35, 52, 62)], t1 - t0, shake=[(0.0, 0.3, 8)]),
                   notes="The private Mom knows her hand is on the lock, then lies instantly (no typing dots): the clean catchable lie."))

    # 7 CODE WORD -------------------------------------------------------------------------------
    t0, t1 = at("n9"), at("n11")
    kt = at("n9:kitchen") - t0
    f4 = at("f4") - t0
    p4 = at("p4") - t0
    sl = at("n10:slid") - t0
    lay = timed([full("horror/LivingRoom", {"lamp": 0.25, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
                 handphone(private(t0), battery=6, clock="11:43")], 0, kt)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.3, "tv": "off"}), nora("suspicious", lookX=-0.4, lookY=0.2)], kt, f4)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.25, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
                  handphone(family(t0), battery=6, clock="11:43")], f4, p4)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.25, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
                  handphone(private(t0), battery=6, clock="11:43")], p4, sl)
    lay += timed([full("horror/FrontDoor", {"chain": "off", "hallLight": 0.0})], sl, sl + 0.25)
    lay += timed([full("horror/FrontDoor", {"chain": "on", "hallLight": 0.0})], sl + 0.25, t1 - t0)
    lay.append(vignette(0.45))
    S.append(scene("s07_codeword", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 50, 55), (at("n9:both") - t0, 1.2, 1.24, 50, 55), (kt, 1.0, 1.06, 50, 50),
                                   (f4, 1.15, 1.2, 50, 52), (p4, 1.3, 1.36, 50, 52), (sl, 2.6, 2.7, 72.5, 43.5)], t1 - t0,
                                  shake=[(sl + 0.25, 0.15, 6)]),
                   notes="Micro loop: the group dodges, the private chat answers the never-typed word and adds an order (chain on)."))

    # 8 DOORBELL + PEEPHOLE + LIGHT -------------------------------------------------------------
    t0, t1 = at("n11"), at("n14")
    pe = at("n12") - t0
    nv = at("n13:never") - t0
    lay = timed(door(feet=True), 0, pe)
    lay += timed([full("horror/Peephole", {"figure": "none", "exposure": 0.4, "flicker": 0, "vignette": 0.85}),
                  svg(peephole_overlay_svg(False), 540, 902, 994, 994, z=5)], pe, nv)
    lay += timed(door(feet=True), nv, t1 - t0)
    lay.append(vignette(0.5, "120,0,10"))
    db = at("n11:doorbell") - t0
    S.append(scene("s08_bell_peephole", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 50, 50), (pe, 1.0, 1.05, 50, 47), (at("n12:Head") - t0, 1.12, 1.16, 50, 52),
                                   (at("n13") - t0, 1.05, 1.1, 50, 47), (at("n13:even") - t0, 1.18, 1.22, 50, 45), (nv, 1.9, 2.0, 50, 87)],
                                  t1 - t0, shake=[(db, 0.22, 12)]),
                   notes="Peephole: dark corridor, red EXIT sign, blue scrubs pressed too close to the lens. The motion light rule is "
                         "stated as history (it clicks on for anyone); it never fires. No on-screen flicker (real PIR lights hold 30 s+)."))

    # 9 DAD POSTS (silent bubbles) + NEVER LIED ------------------------------------------------
    t0, t1 = at("n14"), at("f5")
    q1s, q1e = BY["q1"]["start"] - t0, BY["q1"]["end"] - t0
    lay = timed([full("horror/LivingRoom", {"lamp": 0.2, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
                 handphone(family(t0, typing_spans=[("Dad", at("n14:Dad#2"), BY["q1"]["start"])]), battery=5, clock="11:44")], 0, q1e)
    lay += timed(hall_wall(glow=[(0, 0.0)]) + [svg(SILHOUETTE_BACK, 540, 1560, 760, 960, z=30, depth=0, opacity=0.0)], q1e, t1 - t0)
    lay += timed([nora("worried", lookX=0.2, lookY=0.3, width=1050, z=40)], q1e, t1 - t0)
    lay.append(vignette(0.45))
    S.append(scene("s09_dad_vouches", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 50, 52), (q1s, 1.32, 1.34, 50, 55), (q1s + 0.95, 1.38, 1.4, 50, 58),
                                   (q1s + 1.8, 1.44, 1.46, 50, 61), (q1e, 1.0, 1.06, 50, 50)], t1 - t0),
                   notes="Dad's three bubbles land SILENT (no VO): the TEXT-FIGURE bubble rhythm, so his first heard voice is the landline. "
                         "Behind Nora: the hall closet door."))

    # 10 SHADOW + HANDLE + CAPS -----------------------------------------------------------------
    t0, t1 = at("f5"), at("n17")
    fl = at("f5:shadow") - t0
    hn = at("n16") - t0
    q2 = BY["q2"]["start"] - t0
    lay = timed([full("horror/LivingRoom", {"lamp": 0.2, "tv": "off"}, blur=8, opacity=0.8, depth=0.2),
                 handphone(family(t0), battery=5, clock="11:44")], 0, fl)
    lay += timed(door(feet=True) + [rect(540, 1655, 500, 10, "#0a0b0e", z=6, opacity=0.6)], fl, hn)
    sl, su = at("n16:Slowly") - t0, at("n16:up") - t0
    lay += timed([svg(LEVER_PLATE, 540, 960, 1080, 1920, z=0),
                  svg(LEVER, 700, 960, 600, 120, z=2, anchorX=0.9, anchorY=0.5,
                      keyframes=[{"t": round(hn, 3), "rotate": 0}, {"t": round(sl + 0.6, 3), "rotate": -28, "ease": "inOut"},
                                 {"t": round(su, 3), "rotate": -28}, {"t": round(su + 0.5, 3), "rotate": 0, "ease": "inOut"}]),
                  comp("horror/Darkness", {"x": 0.62, "y": 0.5, "radius": 0.45, "darkness": 0.7}, depth=0, z=20)], hn, q2)
    lay += timed([full("horror/FrontDoor", {"chain": "on", "hallLight": 0.0}, blur=9, opacity=0.75, depth=0.2),
                  handphone(family(t0), battery=5, clock="11:45", vibrate=[{"at": round(q2, 3), "duration": 0.6, "amount": 1}])], q2, t1 - t0)
    lay.append(vignette(0.5, "120,0,10"))
    S.append(scene("s10_shadow_handle", t0, t1, lay,
                   camera=cut_cam([(0, 1.25, 1.3, 50, 56), (fl, 2.1, 2.2, 50, 87), (hn, 1.0, 1.08, 60, 50), (q2, 1.3, 1.34, 50, 58)],
                                  t1 - t0, shake=[(q2 + 0.25, 0.4, 16)]),
                   notes="Proximity: it sees her shadow; the lever tilts down slowly and back up (drawn insert, not the kit's fast jiggle). "
                         "Typography ladder: the group Mom breaks into CAPS (silent alert bubble) with knocks."))

    # 11 CALL + RINGTONE IN THE CLOSET (B8 turn) ------------------------------------------------
    t0, t1 = at("n17"), at("n19")
    cl = at("n17:called") - t0
    r0 = at("n18") - t0
    bh = at("n18:Behind") - t0
    q4s = BY["q4"]["start"] - t0
    lay = timed([full("horror/LivingRoom", {"lamp": 0.15, "tv": "off"}, blur=10, opacity=0.6, depth=0.2)], 0, r0)
    lay += timed([handphone(family(t0), battery=5, clock="11:45")], 0, cl)
    lay += call_screen(cl, r0, "Dad", "mobile", "D", DAD_C, clock="11:45", battery="5%")
    lay += timed([full("horror/LivingRoom", {"lamp": 0.15, "tv": "off"}), nora("shocked", pose="ear", lookX=0.0, lookY=0.2, light="phone", blink=False)], r0, bh)
    glow = ring_glow(r0, 1) + ring_glow(r0 + 2.0, 1)[1:] + ring_glow(q4s, 2)[1:] + [(q4s + 3.95, 0.0)]
    lay += timed(hall_wall(glow=[(bh, 0.6)] + [(t, v) for t, v in glow if t > bh]) +
                 [svg(SILHOUETTE_BACK, 760, 1600, 860, 1090, z=30, depth=0)], bh, t1 - t0)
    lay.append(comp("horror/Heartbeat", {"bpm": 90, "bpmTo": 130, "intensity": 0.55, "from": round(bh, 3)}, depth=0, z=55))
    lay.append(vignette(0.5))
    S.append(scene("s11_ring_in_closet", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 50, 50), (r0, 1.0, 1.06, 50, 45), (at("n18:Dad's") - t0, 1.25, 1.3, 50, 40),
                                   (bh, 1.0, 1.06, 40, 55), (at("n18:closet") - t0, 1.12, 1.16, 41, 60), (q4s, 1.16, 1.22, 41, 62),
                                   (q4s + 2.0, 1.3, 1.38, 41, 70)], t1 - t0, shake=[(r0 + 0.05, 0.2, 5)]),
                   notes="TURN (personal link): the voucher's phone rings in OUR hall closet. 4.0 s silence beat: two full ring cycles, the "
                         "under-door glow pulses with each ring, music out."))

    # 12 DAD TYPING -----------------------------------------------------------------------------
    t0, t1 = at("n19"), at("n20")
    q5 = BY["q5"]["start"] - t0
    lay = [full("horror/FrontDoor", {"chain": "on", "hallLight": 0.0}, blur=9, opacity=0.75, depth=0.2),
           handphone(family(t0, typing_spans=[("Dad", at("n19:Dad"), BY["q5"]["start"])]), battery=4, clock="11:46"),
           comp("horror/Glitch", {"cues": [{"at": round(at("n19:Dad") - t0, 3), "duration": 0.2, "amount": 0.35}], "seed": "g1"}, depth=0, z=60),
           vignette(0.5)]
    S.append(scene("s12_dad_typing", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 50, 52), (at("n19:family") - t0, 1.35, 1.38, 50, 33), (q5, 1.3, 1.33, 50, 58),
                                   (q5 + 1.0, 1.42, 1.45, 50, 62)], t1 - t0),
                   notes="Isolation: the only channel answering is the enemy's. Dad's calm sentence-case bubbles land silent."))

    # 13 HOTEL LANDLINE + BATTERY CLOCK ----------------------------------------------------------
    t0, t1 = at("n20"), at("f6")
    nf = at("n20:fridge") - t0
    rm = at("n20:Room") - t0
    d1 = at("d1") - t0
    n21 = at("n21:Where's") - t0
    d2 = at("d2") - t0
    dc = at("d2:closet") - t0
    n22 = at("n22") - t0
    d3 = at("d3") - t0
    n23 = at("n23") - t0
    bt = at("n23:battery") - t0
    lay = timed(hall_wall(glow=[(0, 0.1)]) + [nora("scared", lookX=-0.5, lookY=0.3, width=980, z=40,
                                                    keyframes=[{"t": 0, "scale": 0.92}, {"t": round(nf, 3), "scale": 1.04, "ease": "linear"}])], 0, nf)
    lay += timed(note_layers(z=0), nf, rm + 0.9)
    lay += call_screen(rm + 0.9, n21, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=d1, clock="11:46", battery="3%")
    lay += timed([full("horror/LivingRoom", {"lamp": 0.12, "tv": "off"}), nora("scared", pose="ear", lookX=0.3, lookY=0.1)], n21, d2)
    lay += call_screen(d2, dc, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=d1, clock="11:47", battery="3%")
    lay += timed(hall_wall(glow=[(0, 0.15)]), dc, n22)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.12, "tv": "off"}), nora("terrified", pose="ear", lookX=0.5, lookY=0.1, blink=False)], n22, d3)
    lay += call_screen(d3, n23, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=d1, clock="11:47", battery="2%")
    lay += call_screen(n23, t1 - t0, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=d1, clock="11:47", battery="2%")
    lay += timed([text("2%", 540, 1250, 220, RED, 900, font="display", z=30, enter={"type": "pop", "duration": 0.2}),
                  text("police · 8 min", 540, 1440, 54, "#ffffff", 800, z=30, background="#2a2440", padding=18, radius=40)], bt, t1 - t0)
    lay.append(vignette(0.45))
    S.append(scene("s13_hotel_landline", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.03, 50, 50), (nf, 1.35, 1.4, 50, 66), (rm + 0.9, 1.0, 1.03, 50, 50), (n21, 1.0, 1.05, 50, 50),
                                   (d2, 1.0, 1.03, 50, 50), (dc, 1.0, 1.06, 41, 52), (n22, 1.1, 1.14, 50, 45), (d3, 1.0, 1.03, 50, 50),
                                   (n23, 1.0, 1.03, 50, 50), (bt, 1.06, 1.1, 50, 62)], t1 - t0),
                   notes="Lifeline: the hotel landline from the fridge note (Room 412). Real Dad: his cell is in his coat in the closet. "
                         "Clock: police 8 min, her battery 2%. Call screen = one red End button (outgoing, then connected)."))

    # 14 BARRIER LADDER -------------------------------------------------------------------------
    t0, t1 = at("f6"), at("p5")
    em = at("n24:Empty") - t0
    nb = at("n24:Nobody") - t0
    ky = at("n25") - t0
    rl = at("n26") - t0
    dbt = at("n27") - t0
    sm = at("n27:slammed") - t0
    th3 = at("n27:Three") - t0
    lay = call_screen(0, at("n24") - t0, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=d1 - (t0 - at("n20")),
                      clock="11:48", battery="2%")
    lay += timed([rect(540, 360, 760, 150, "rgba(38,43,53,0.97)", radius=30, z=20, shadow="0 18px 40px rgba(0,0,0,.55)", enter={"type": "slideDown", "duration": 0.25}),
                  text("FAMILY · MOM", 230, 320, 22, "#aab2bf", 700, "left", z=21),
                  text("who are you whispering to, honey?", 230, 375, 34, "#ffffff", 800, "left", z=21)], 0, at("n24") - t0)
    lay += timed([svg(key_hook_svg(False), 540, 960, 1080, 1920, z=0),
                  comp("horror/Darkness", {"x": 0.52, "y": 0.45, "radius": 0.38, "darkness": 0.8}, depth=0, z=20)], at("n24") - t0, nb)
    lay += timed(hall_wall(glow=[(0, 0.12)]) + [nora("terrified", lookX=-0.7, lookY=0.1, light="none", width=1000, z=40,
                                                      props={"exprs": [{"t": 0, "e": "terrified"}]})], nb, ky)
    lay += timed([svg(deadbolt_svg(), 540, 960, 1080, 1920, z=0), svg(THUMB, 540, 1000, 120, 460, z=2),
                  comp("horror/Darkness", {"x": 0.5, "y": 0.52, "radius": 0.45, "darkness": 0.65}, depth=0, z=20)], ky, rl)
    lay += timed(note_layers(hl_key=rl, z=0), rl, dbt)
    lay += timed([svg(deadbolt_svg(), 540, 960, 1080, 1920, z=0),
                  svg(THUMB, 540, 1000, 120, 460, z=2, keyframes=[{"t": round(dbt, 3), "rotate": 0}, {"t": round(dbt + 0.45, 3), "rotate": -90, "ease": "inOut"}]),
                  comp("horror/Darkness", {"x": 0.5, "y": 0.52, "radius": 0.45, "darkness": 0.65}, depth=0, z=20)], dbt, sm)
    lay += timed(door(feet=False, gap=[(0.0, 0.0), (sm, 0.0), (sm + 0.12, 1.0)], props={"knocks": [round(sm, 3)]}) +
                 [comp("horror/Darkness", {"x": 0.62, "y": 0.5, "radius": 0.5, "darkness": 0.6}, depth=0, z=20),
                  {"type": "particles", "preset": "dust", "count": 40, "color": "#9fb6cf", "speed": 0.6, "seed": 3, "x": 850, "y": 1000,
                   "width": 300, "height": 1300, "z": 25, "opacity": 0.5}], sm, t1 - t0)
    lay.append(vignette(0.5))
    S.append(scene("s14_barrier", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.03, 50, 50), (at("n24") - t0, 1.0, 1.1, 52, 50), (em, 1.25, 1.3, 52, 45), (nb, 1.0, 1.06, 50, 50),
                                   (ky, 1.0, 1.1, 50, 52), (rl, 1.15, 1.2, 50, 58), (dbt, 1.0, 1.06, 50, 52), (sm, 1.2, 1.25, 66, 50),
                                   (th3, 1.6, 1.7, 73, 50)], t1 - t0, shake=[(sm, 0.35, 22)]),
                   notes="Barrier ladder: hook empty (nobody came in) -> a key from outside -> the rule spoken back as dread "
                         "(the fridge note's 'I HAVE MY KEY' turns red) -> the deadbolt turns -> the door slams to the chain; three inches of black."))

    # 15 RULE INVERSION + BATTERY DIES ------------------------------------------------------------
    t0, t1 = at("p5"), at("n30")
    n28 = at("n28") - t0
    d4 = at("d4") - t0
    ti = at("d4:in#2") - t0 if len([w for w in BY["d4"]["words"] if norm(w["w"]) == "in"]) > 1 else at("d4:there") - t0
    n29 = at("n29") - t0
    bk = at("n29:black") - t0
    q7 = BY["q7"]["start"] - t0
    base_call = d1 - (t0 - at("n20"))
    lay = call_screen(0, n28, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=base_call, clock="11:49", battery="1%")
    for i, (s, ts) in enumerate([("Get in the hall closet.", 0.0), ("Shut the door.", at("p5:Shut") - t0), ("Don't make a sound.", at("p5:Don't") - t0)]):
        y = 360 + i * 150
        lay += timed([rect(540, y, 760, 130, "rgba(38,43,53,0.97)", radius=30, z=20, enter={"type": "slideDown", "duration": 0.22}),
                      text("MOM", 230, y - 32, 22, "#aab2bf", 700, "left", z=21), text(s, 230, y + 18, 36, "#ffffff", 800, "left", z=21)], ts, n28)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.1, "tv": "off"}), nora("scared", pose="ear", lookX=0.4, lookY=0.1)], n28, d4)
    lay += call_screen(d4, ti, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=base_call, clock="11:49", battery="1%")
    lay += timed(hall_wall(glow=[(0, 0.18)]), ti, ti + 0.7)
    lay += call_screen(ti + 0.7, n29, "Lakeview Suites", "Columbus · Room 412", "LS", "#4a6b5a", connected_at=base_call, clock="11:49", battery="1%")
    lay += timed(hall_wall(glow=[(0, 0.18)]) + [nora("terrified", pose="phone", lookX=-0.2, lookY=0.4, width=1000, z=40,
                                                      keyframes=[{"t": round(n29, 3), "x": 760}, {"t": round(bk, 3), "x": 540, "ease": "out"}])], n29, t1 - t0)
    lay += timed([rect(540, 960, 1080, 1920, "#000000", z=45, opacity=0.0,
                       keyframes=[{"t": round(bk, 3), "opacity": 0}, {"t": round(bk + 0.08, 3), "opacity": 0.55}])], n29, t1 - t0)
    lay += timed([comp("horror/Glitch", {"cues": [{"at": round(bk, 3), "duration": 0.25, "amount": 0.8}], "seed": "g2"}, depth=0, z=60)], 0, t1 - t0)
    lay.append(vignette(0.55))
    S.append(scene("s15_inversion", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.03, 50, 40), (at("p5:Shut") - t0, 1.05, 1.07, 50, 42), (n28, 1.08, 1.12, 50, 45),
                                   (d4, 1.0, 1.03, 50, 50), (ti, 1.1, 1.15, 41, 55), (ti + 0.7, 1.0, 1.03, 50, 50), (n29, 1.0, 1.04, 50, 52),
                                   (q7, 1.1, 1.16, 45, 55)], t1 - t0, shake=[(bk, 0.25, 8)]),
                   notes="T3 rule inversion: the helper's protective order (hide in the closet) is the trap; the real authority names it "
                         "('that's where my phone is') and gives the opposite. She obeys him. Then the battery dies: the landline is gone."))

    # 16 PEAK: the closet opens itself -------------------------------------------------------------
    t0, t1 = at("n30"), at("n34")
    sw = at("n30:swung") - t0
    n31 = at("n31") - t0
    slv = at("n31:sleeve") - t0
    n32 = at("n32") - t0
    q8 = BY["q8"]["start"] - t0
    n33 = at("n33") - t0
    lay = timed(hall_wall(glow=[(0, 0.2), (sw, 0.5)], open_kf=[(0, 1.0), (sw, 1.0), (sw + 1.1, 0.12)], inside=True), 0, n31)
    inside = [svg(CLOSET_INSIDE, 540, 960, 1080, 1920, z=0),
              svg(SLEEVE, 380, 470, 200, 900, z=2, anchorX=0.5, anchorY=0.0,
                  keyframes=[{"t": round(n31, 3), "rotate": 9}, {"t": round(n31 + 0.8, 3), "rotate": -6, "ease": "inOut"},
                             {"t": round(n31 + 1.6, 3), "rotate": 4, "ease": "inOut"}, {"t": round(n31 + 2.4, 3), "rotate": -2.5, "ease": "inOut"},
                             {"t": round(n31 + 3.2, 3), "rotate": 1.5, "ease": "inOut"}, {"t": round(n31 + 4.0, 3), "rotate": 0, "ease": "inOut"}]),
              rect(665, 1150, 120, 90, "#7fb4ff", z=3, opacity=0.55, blur=18, idle=[{"type": "pulse", "amount": 0.25, "speed": 1.2}]),
              rect(540, 900, 700, 1300, "#9fb6cf", z=1, opacity=0.10, blur=90),
              comp("horror/Darkness", {"x": 0.5, "y": 0.55, "radius": 0.5, "darkness": 0.6}, depth=0, z=20)]
    lay += timed(inside, n31, q8)
    lay += closet_phone(q8, n33, draft_at=q8 + 0.6)
    lay += timed([full("horror/FrontDoor", {"chain": "on", "hallLight": 0.0}, blur=10, opacity=0.8, depth=0.2),
                  rect(790 - 10, 1000, 40, 1340, "#000000", z=2, blur=6),
                  nora("terrified", pose="idle", lookX=0.0, lookY=0.0, light="none", blink=False, width=1100, z=40)], n33, t1 - t0)
    lay.append(vignette(0.6))
    S.append(scene("s16_peak_closet", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 41, 52), (n31, 1.0, 1.05, 50, 45), (slv, 1.35, 1.4, 36, 40), (n32, 1.6, 1.75, 62, 61),
                                   (q8, 1.0, 1.0, 50, 50), (n33, 1.0, 1.05, 50, 48)], t1 - t0),
                   hold_ok=True,
                   notes="THE scariest image, once (~71%): the closet opens itself; Dad's coat, nobody in it, the sleeve still swinging; "
                         "the phone in the pocket types a draft that addresses her ('turn around nora'), held still ~4 s with no music "
                         "(the one intended hold over 3 s). Then her face, eyes forward; behind her the door's black gap."))

    # 17 RESCUE + LIGHT TEST --------------------------------------------------------------------
    t0, t1 = at("n34"), at("n38")
    gp = at("n34:gap") - t0
    n35 = at("n35") - t0
    n36 = at("n36") - t0
    ck = at("n37") - t0
    fr = at("n37:for") - t0
    pol = [comp("horror/Vignette", {"amount": 0.6, "color": "255,40,60", "pulse": 1.6}, depth=0, z=51),
           comp("horror/Vignette", {"amount": 0.6, "color": "40,90,255", "pulse": 1.6, "inner": 0.3}, depth=0, z=52)]
    lay = timed(door(feet=False, gap=[(0.0, 1.0), (gp, 1.0), (gp + 0.9, 0.0)]) + pol, 0, n35)
    lay += timed(door(feet=False, props={"knocks": [round(n35, 3), round(n35 + 0.3, 3), round(n35 + 0.6, 3)]}) + pol, n35, n36)
    lay += timed(door(feet=True, two_pairs=True, warm=ck) + pol, n36, fr)
    lay += timed([full("horror/Peephole", {"figure": "none", "exposure": 1.3, "flicker": 0, "vignette": 0.6}),
                  svg(peephole_overlay_svg(True), 540, 902, 994, 994, z=5)] + pol, fr, t1 - t0)
    S.append(scene("s17_rescue_light", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.04, 55, 50), (gp, 1.15, 1.2, 70, 50), (n35, 1.0, 1.04, 50, 50), (n36, 1.9, 1.95, 50, 87),
                                   (fr, 1.0, 1.05, 50, 47)], t1 - t0, shake=[(n35, 0.2, 6), (n35 + 0.3, 0.2, 6), (n35 + 0.6, 0.2, 6)]),
                   notes="Rescue under red/blue. The gap closes by itself (latch click). The planted rule decides: on 'Click' the strip "
                         "under the door turns from EXIT red to warm motion light, with two pairs of feet; peephole: two lit officers."))

    # 18 CHAIN OFF + MOM ------------------------------------------------------------------------
    t0, t1 = at("n38"), at("r1")
    ch = at("n38:Chain") - t0
    n39 = at("n39") - t0
    mm = at("n39:Mom") - t0
    lay = timed([full("horror/FrontDoor", {"chain": "on", "hallLight": 1.0})], 0, ch + 0.1)
    lay += timed([full("horror/FrontDoor", {"chain": "off", "hallLight": 1.0})], ch + 0.1, n39)
    lay += timed([full("horror/Hallway", {"lights": 3, "flicker": 0, "endDoor": True, "figure": 0.9, "figureDepth": 0.35})], n39, mm)
    lay += timed([full("horror/ElevatorPanel", {"from": 3, "to": 6, "at": 0.0, "perFloor": 0.25, "floors": 12, "flicker": 0})], mm, t1 - t0)
    S.append(scene("s18_chain_off", t0, t1, lay,
                   camera=cut_cam([(0, 2.6, 2.7, 72.5, 43.5), (n39, 1.0, 1.06, 50, 50), (mm, 1.0, 1.08, 50, 50)], t1 - t0),
                   notes="She breaks Mom's rule because the light test passed. Two officers in the lit corridor; the elevator reaches 6: Mom."))

    # 19 TWIST ----------------------------------------------------------------------------------
    t0, t1 = at("r1"), at("n42")
    n40 = at("n40") - t0
    r2 = at("r2") - t0
    n41 = at("n41") - t0
    lay = timed([full("horror/Hallway", {"lights": 3, "flicker": 0, "endDoor": True}, blur=10, opacity=0.7, depth=0.2),
                 comp("horror/HandPhone", {"phoneWidth": 0.6, "cx": 0.5, "cy": 0.62, "tilt": 6, "tremble": 2.5, "side": "left",
                                           "skin": "#d9b99a", "phone": {"mode": "off"}}, z=10)], 0, n40)
    lay += timed([full("horror/Hallway", {"lights": 3, "flicker": 0}, blur=8, opacity=0.8, depth=0.2),
                  nora("relieved", exprs=[{"t": 0, "e": "relieved"}, {"t": round(0.6, 3), "e": "worried"}], pose="idle", lookX=0.2, lookY=0.1, light="none")], n40, r2)
    lay += timed([full("horror/LivingRoom", {"lamp": 0.0, "tv": "off", "flicker": 0.2}),
                  comp("horror/Darkness", {"x": 0.5, "y": 0.5, "radius": 0.28, "darkness": 0.92}, depth=0, z=20)], r2, n41)
    lay += timed([full("horror/Hallway", {"lights": 3, "flicker": 0}, blur=8, opacity=0.8, depth=0.2),
                  nora("terrified", pose="idle", lookX=-0.8, lookY=0.1, light="none", blink=False)], n41, t1 - t0)
    lay.append(vignette(0.45))
    S.append(scene("s19_twist", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.06, 50, 55), (at("r1:never") - t0, 1.2, 1.25, 50, 60), (n40, 1.0, 1.05, 50, 50),
                                   (r2, 1.0, 1.12, 50, 50), (n41, 1.05, 1.1, 50, 48)], t1 - t0),
                   notes="T8 after safety, NEW information: Mom's phone died at nine, so neither chat was ever her; and Marigold was only "
                         "ever said out loud in our kitchen, so whatever answered had been inside our home."))

    # 20 VOICE SWAP + BOOKEND -------------------------------------------------------------------
    t0, t1 = at("n42"), END
    lt = at("n42:lit") - t0
    pc = at("n42:private") - t0
    p6 = at("p6") - t0
    x1 = at("x1") - t0
    lock = {"time": "11:58", "date": "Friday, October 30",
            "notifications": [{"at": round(lt + 0.15, 3), "app": "Messages", "title": "Mom", "text": "typing…"}]}
    ph_lock = handphone(mode="lock", lock=lock, battery=0, tremble=2.0, cy=0.6)
    ph_lock["props"]["phone"]["screens"] = [{"t": 0, "mode": "off"}, {"t": round(lt, 3), "mode": "lock"}]
    lay = door(props={"chain": "off", "hallLight": 1.0}, feet=False, blur=2.5)
    lay += timed([ph_lock], 0, pc + 0.5)
    lay += timed([handphone(private(t0, typing_spans=[("Mom", at("p6", -0.9), at("p6"))]), battery=0, clock="11:58", tremble=2.0,
                            glitch=[{"at": round(x1, 3), "duration": 0.25, "amount": 0.7}])], pc + 0.5, t1 - t0)
    lay += [comp("horror/Glitch", {"cues": [{"at": round(x1, 3), "duration": 0.22, "amount": 0.6}], "seed": "g3"}, depth=0, z=60),
            vignette(0.55, "120,0,10")]
    S.append(scene("s20_voice_swap", t0, t1, lay,
                   camera=cut_cam([(0, 1.0, 1.03, 50, 50), (lt, 1.08, 1.1, 50, 52), (pc + 0.5, 1.0, 1.04, 50, 52), (p6, 1.3, 1.34, 50, 60),
                                   (x1, 1.4, 1.45, 50, 64), (BY["q9"]["start"] - t0, 1.0, 1.0, 50, 50)], t1 - t0, shake=[(x1, 0.2, 6)]),
                   notes="Her dead phone wakes. The private thread shows typing dots for the first time (the tell breaks), then the threat "
                         "aimed at what she actually trusted: the Room 412 landline, read in Dad's voice. Last frame = frame 0's "
                         "composition (phone over the front door). Hard cut, no CTA."))
    # drop the zero-length placeholder layers
    for s in S:
        s["layers"] = [l for l in s["layers"] if not (isinstance(l.get("start"), (int, float)) and isinstance(l.get("end"), (int, float))
                                                       and l["end"] - l["start"] < 0.01)]
    return S


# ------------------------------------------------------------------ holds: auto punch-ins in any gap > 2.9 s


def _events(s):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
    from pipeline.episodes.common import visual_events
    return visual_events(s)


def _zoom_at(kf, t):
    pts = [(k["t"], k["zoom"], k["x"], k["y"]) for k in kf]
    prev = pts[0]
    for p in pts:
        if p[0] <= t:
            prev = p
        else:
            frac = (t - prev[0]) / max(1e-6, p[0] - prev[0])
            return prev[1] + (p[1] - prev[1]) * frac, prev[2], prev[3]
    return prev[1], prev[2], prev[3]


def fix_holds(scenes, limit=2.9):
    for s in scenes:
        if s.get("_hold_ok"):
            continue
        for _ in range(12):
            ev = _events(s)
            gaps = [(b - a, a, b) for a, b in zip(ev, ev[1:]) if b - a > limit]
            if not gaps:
                break
            g, a, b = max(gaps)
            tm = round(a + g / 2, 3)
            kf = s.setdefault("camera", {}).setdefault("keyframes", [])
            if not kf:
                kf += [{"t": 0, "zoom": 1.0, "x": "50%", "y": "50%", "ease": "linear"}]
            z, x, y = _zoom_at(sorted(kf, key=lambda k: k["t"]), tm)
            kf += [{"t": round(tm - 0.01, 3), "zoom": round(z, 3), "x": x, "y": y, "ease": "linear"},
                   {"t": tm, "zoom": round(z * 1.07, 3), "x": x, "y": y, "ease": "step"}]
            later = [k for k in kf if k["t"] > tm]
            for k in later:
                k["zoom"] = round(k["zoom"] * 1.07, 3) if k["t"] < b + 1e-6 and k is not later[-1] else k["zoom"]
            kf.sort(key=lambda k: k["t"])
    for s in scenes:
        s.pop("_hold_ok", None)
    return scenes


# ------------------------------------------------------------------ storyboard


def storyboard():
    scenes = build_scenes()
    holds_ok = [s["id"] for s in scenes if s.get("_hold_ok")]
    scenes = fix_holds(scenes)
    total = round(sum(s["duration"] for s in scenes), 3)
    assert abs(total - RUNTIME) < 0.05, (total, RUNTIME)
    voice = [{"src": f"episodes/{EP}/vo/{it['id']}.wav", "start": it["start"], "volume": 1, "duration": round(it["dur"], 3)}
             for it in ITEMS if it["kind"] == "line"]
    q4, q4e = BY["q4"]["start"], BY["n19"]["start"]
    q7 = BY["q7"]["start"]
    resc = BY["n34"]["start"]
    music = [{"src": "music/dread.m4a", "start": 0, "end": round(q4, 2), "volume": 0.3, "duckTo": 0.12, "fadeIn": 0.4, "fadeOut": 0.25},
             {"src": "music/dread.m4a", "start": round(q4e, 2), "end": round(q7, 2), "volume": 0.3, "duckTo": 0.12, "fadeIn": 0.8, "fadeOut": 0.4},
             {"src": "music/tension_pulse.m4a", "start": round(resc, 2), "end": round(RUNTIME - 0.3, 2), "volume": 0.22, "duckTo": 0.09,
              "fadeIn": 1.0, "fadeOut": 0.2}]
    sb = {
        "version": 1, "id": EP, "title": "My Mom Texted Me Twice. Only One Said Don't Open The Door.", "format": "9:16", "fps": 30,
        "scenes": scenes,
        "captions": {"words": captions(), "maxWords": 4, "maxChars": 18, "gapBreak": 0.25, "linger": 0.3,
                     "glue": ["front door", "hall closet", "code word", "Room 412.", "the chain", "motion sensor"],
                     "style": {"font": "display", "fontSize": 62, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "none",
                               "strokeWidth": 10, "uppercase": False, "y": 0.13, "backing": 0.85}},
        "audio": {"voice": voice, "music": music, "sfx": sfx_cues(), "duckOn": "voice"},
        "overlays": {"grain": 0.45, "vignette": 0.3, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{EP}/build.py",
                   "timing": "Kokoro-82M on the Spark CPU, measured per line, 4 voices (lines.VOICES)",
                   "audio": f"per-line wavs: copy ~/studio/tts/{EP}/*.wav to studio/public/episodes/{EP}/vo/ on the Spark "
                            "(tts_measure.py writes them); music + sfx from studio/public (desk_bell_ring, key_scrape, siren, relay_click "
                            "made by sfx_synth.py)",
                   "music_drops": "three music segments: out for the closet ring (silence beat) and from the battery death through the peak",
                   "intended_holds": holds_ok,
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
    for s in storyboard()["scenes"]:
        print(f"| {s['id']} | {mmss(t)} | {mmss(t + s['duration'])} | {s.get('notes', '')} |")
        t += s["duration"]
    print("\n## JOLTS")
    print(", ".join(f"{mmss(tt)} {lab}" for lab, tt in sorted(J, key=lambda x: x[1])))
    ts = sorted(t for _, t in J)
    gaps = sorted(((b - a), mmss(a)) for a, b in zip(ts, ts[1:]))[-5:]
    print("largest jolt gaps:", gaps)
    print("\n## KEY TIMES")
    for ref in ["f1", "p1:Don't", "n3:door", "n4", "n5:Use", "n6:hand", "p3", "p4", "n11:doorbell", "n13:never", "n14", "f5", "n17",
                "n18:Behind", "n19", "n20:Room", "d2:closet", "n23", "n24:Empty", "n25", "n26", "n27:slammed", "p5", "d4", "n29:black",
                "n30", "n33", "n34", "n37", "n38", "r1", "r2", "n42", "p6", "x1"]:
        tt = at(ref)
        print(f"{ref}: {mmss(tt)} ({100 * tt / RUNTIME:.0f}%)")


if __name__ == "__main__":
    sb = storyboard()
    json.dump({"runtime": RUNTIME, "beats": BEATS,
               "items": [{k: v for k, v in it.items() if k != "opts"} | {"screen": it["opts"].get("screen", "")} for it in ITEMS],
               "stats": stats()}, open(os.path.join(HERE, "timeline.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(sb, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1, ensure_ascii=False)
    if "--tables" in sys.argv:
        tables()
    print(f"runtime {RUNTIME} s, scenes {len(sb['scenes'])}", file=sys.stderr)
