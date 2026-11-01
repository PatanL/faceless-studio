"""Build the measured timelines, pacing stats and storyboards for horror-night-doorman-rules (2 parts).

usage: python3 build.py [--tables]        (stdlib only; safe on the Mac)
inputs : lines.py (the spoken lines), tts_durations.json (Kokoro per-line durations measured on the Spark CPU)
outputs: timeline.json (both parts), storyboard.json (Part 1), storyboard_p2.json (Part 2);
         --tables prints the markdown tables that script.md carries.

The horror kit is locked (BRIEF Update 11:27), so nothing here needs a kit edit. Every visual is a
registered horror component (HandPhone, Protagonist, Hallway, ElevatorPanel, Stairwell, Flicker, Vignette,
Heartbeat, Glitch, RedText, Darkness) or a core layer (rect / circle / text / svg). The lobby, the desk phone,
the key board, the elevator doors, the CCTV grid, the paper sheets and the back-view figure are inline SVG
drawn below. They are written so they can be lifted into a horror/LobbyDesk + horror/Paper component later.
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
EP = "horror-night-doorman-rules"
LEAD_IN = 0.12

# ------------------------------------------------------------------ timeline


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def word_times(lid: str, text: str, start: float) -> list[dict]:
    """Align the script's words to Kokoro tokens by consuming normalised characters. When the TTS text differs
    (opts.say: "Mister" for "Mr.", "A M" for "a.m."), align on the TTS words and map back by position."""
    toks = [w for w in D[lid]["words"] if norm(w["w"])]
    dur = D[lid]["dur"]
    words = text.split()
    say = L_SAY.get(lid)
    if not say:
        st = word_times_raw(toks, words, dur)
        return [{"w": w, "s": round(start + s, 3), "e": round(start + e, 3)} for w, (s, e) in zip(words, st)]
    sw = say.split()
    stimes = word_times_raw(toks, sw, dur)
    res, j = [], 0
    for w in words:
        take = 2 if norm(w) == "am" and j + 1 < len(sw) and norm(sw[j]) == "a" else 1
        s, e = stimes[min(j, len(sw) - 1)][0], stimes[min(j + take - 1, len(sw) - 1)][1]
        j += take
        res.append({"w": w, "s": round(start + s, 3), "e": round(start + e, 3)})
    return res


def word_times_raw(toks, words, dur):
    out, ti, last = [], 0, 0.0
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
            s = e = last
        s = max(0.0, min(s, dur))
        e = max(s + 0.04, min(e, dur + 0.05))
        last = e
        out.append((s, e))
    return out


L_SAY = {e[0]: e[3]["say"] for e in L.spoken() if "say" in e[3]}


def build_timeline(seq):
    items, beats, t = [], [], LEAD_IN
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
        items.append({"kind": "line", "id": lid, "spk": spk, "text": text, "start": round(t, 3), "end": round(t + dur, 3),
                      "dur": dur, "words": word_times(lid, text, t), "opts": opts, "beat": beats[-1]["key"]})
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


class Part:
    def __init__(self, key, seq):
        self.key = key
        self.items, self.beats, self.runtime = build_timeline(seq)
        self.by = {it["id"]: it for it in self.items}

    def at(self, ref: str, off: float = 0.0) -> float:
        """'n3' = start, 'n3.end', 'n3:word' = first word starting with 'word', 'n3:word#2' = 2nd match."""
        if ":" in ref:
            lid, w = ref.split(":", 1)
            n = 1
            if "#" in w:
                w, n = w.split("#")
                n = int(n)
            ws = self.by[lid]["words"]
            hits = [x for x in ws if norm(x["w"]) == norm(w)] or [x for x in ws if norm(x["w"]).startswith(norm(w))]
            return round(hits[n - 1]["s"] + off, 3)
        if ref.endswith(".end"):
            return round(self.by[ref[:-4]]["end"] + off, 3)
        return round(self.by[ref]["start"] + off, 3)

    def sfx_cues(self):
        cues = []
        for it in self.items:
            for cue, off, db in it["opts"].get("sfx", []):
                if isinstance(off, str):
                    if off.startswith("end"):
                        t = it["end"] + (float(off[4:]) if len(off) > 3 else 0.0)
                    elif off.startswith("w:"):
                        t = self.at(f"{it['id']}:{off[2:]}")
                    else:
                        raise ValueError(off)
                else:
                    t = it["start"] + off
                cues.append({"cue": cue, "at": round(max(0.0, t), 3), "volume": round(0.8 * 10 ** (db / 20), 3)})
        return sorted(cues, key=lambda c: c["at"])

    def captions(self):
        words = []
        for it in self.items:
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
                if norm(w["w"]) in EMPH:
                    d["emph"] = True
                words.append(d)
        return words


EMPH = {"nineteenohthree", "empty", "broke", "never", "nobody", "wrong", "his", "number", "blazer", "wall", "red", "ring",
        "lying", "lied", "paper", "ninetysix", "up", "himself", "me", "kid", "shift", "sounds", "dead", "grey", "green",
        "fortyone", "inbed", "isnt", "failed", "out"}

P1 = Part("p1", L.P1)
P2 = Part("p2", L.P2)

# ------------------------------------------------------------------ stats

NUMS = {"p1": ["1903", "31 years", "six rules", "1 AM", "19", "95", "96th", "2:41", "24 hours", "6 AM"]}
NUMS["p2"] = ["1903", "3 AM", "95", "96th", "93-94-95 count", "19", "2:41", "five (minutes)", "5-9-13-16 floors", "4%", "911", "seven"]


def stats(P: Part, hook_ids, contra_ref, line1="n1"):
    lines = [it for it in P.items if it["kind"] == "line"]
    words = sum(len(it["text"].split()) for it in lines)
    speech = sum(it["dur"] for it in lines)
    sil = sum(it["dur"] for it in P.items if it["kind"] == "silence")
    sents = []
    for it in lines:
        for s in re.split(r"(?<=[.!?])\s+", it["text"].strip()):
            if s:
                sents.append(len(s.split()))
    qs = sum(it["text"].count("?") for it in lines if it["spk"] == "N")
    hook_end = P.at(hook_ids[-1] + ".end")
    return {
        "runtime_s": P.runtime,
        "speech_s": round(speech, 2),
        "timed_silence_s": round(sil, 2),
        "words": words,
        "wpm_overall": round(words / (P.runtime / 60), 1),
        "wpm_speaking": round(words / (speech / 60), 1),
        "sentences": len(sents),
        "sentence_median": statistics.median(sents),
        "sentence_mean": round(statistics.mean(sents), 2),
        "punch_share_le4": round(sum(1 for n in sents if n <= 4) / len(sents), 3),
        "questions": qs,
        "questions_per_min": round(qs / (P.runtime / 60), 1),
        "distinct_numbers": NUMS[P.key],
        "numbers_per_min": round(len(NUMS[P.key]) / (P.runtime / 60), 1),
        "line1_words": len(P.by[line1]["text"].split()),
        "core_hook_words": sum(len(P.by[i]["text"].split()) for i in hook_ids),
        "core_hook_s": round(hook_end, 2),
        "contradiction_s": P.at(contra_ref),
        "words_first_10s": sum(1 for it in lines for w in it["words"] if w["s"] < 10),
    }


def jolts(P: Part, J):
    ts = sorted(t for _, t in J)
    gaps = [b - a for a, b in zip(ts, ts[1:])] + [P.runtime - ts[-1]]
    return J, round(statistics.median(gaps), 2), round(max(gaps), 2)


def jolts_p1():
    a = P1.at
    return [("frame 0: red light through the tape + rule 3", 0.0), ("1903 is empty", a("n1:Nineteen-oh-three#2")),
            ("I broke rule three", a("n2:broke")), ("the owner ordered me (banner)", a("n2:text")),
            ("31 years, never met", a("n3:thirty-one")), ("six rules", a("n4:six")), ("door propped at 1 AM", a("n5:propped")),
            ("elevator comes down by itself, from 19", a("n6")), ("Gus: shut the door (he knows)", a("g1")),
            ("he wasn't in the building", a("n7:wasn't")), ("empty car", a("n8:nobody")), ("rule 2", a("g2")),
            ("19 already lit inside", a("n9:already")), ("doors wait until I look away", a("n10:until")),
            ("climbs back to 19", a("n10:climbed")), ("verdict: the building answered", a("n11:building")),
            ("rule 4: 95, never a 96th", a("n12:ninety-five,")), ("tape over 1903", a("n13:tape")),
            ("2:41 text from 'Mr. Pell'", a("n14")), ("Go up now", a("p1:Go")), ("rule 5: obey him", a("n15")),
            ("rules collide", a("n16:wrong.")), ("typing / silence", a("n17:typing.")), ("what number?", a("g3")),
            ("never his", a("g4")), ("the number was", a("n19:number")), ("don't go up", a("g5")),
            ("and if 1903 calls? no answer", a("n20:answer.")), ("camera monitor", a("n21")),
            ("door open a crack + man in a blazer", a("n21:blazer")), ("held: the gap widens", P1.by["h1"]["start"] + 1.8),
            ("Pell: ask him why he left at 2:41", a("p2:Ask")), ("same minute, 24 h ago", a("n22")),
            ("security: next patrol 6 AM", a("n23:Next")), ("dot goes grey", a("n24:grey.")),
            ("a sound I'd never heard", a("n25:sound")), ("red light under the tape", a("n25:red.")),
            ("LINE 1903 rings", P1.by["h2"]["start"]), ("dot back to green", a("n26:green.")), ("Let it ring.", a("g6"))]


def jolts_p2():
    a = P2.at
    return [("frame 0: 1903 calling", 0.0), ("rules swore it was empty", a("q1:My")), ("Gus said let it ring / I picked up", a("q2:picked")),
            ("the voice: it isn't me", a("v1:Whatever's")), ("line dead", a("q3:dead.")), ("chat Gus: home in bed", a("q4:Gus:")),
            ("Pell: Gus never came home", a("q5:Gus")), ("which Gus? (question)", a("q6:So")), ("paper", a("q7:paper,")),
            ("Pell's real number doesn't match", a("q8:wasn't")), ("dial Gus", a("q9:dialed")),
            ("1903 lights up in sync", a("q10:lit")), ("chat Gus lied too", a("q11:lied")), ("3 AM rule 4", a("q12")),
            ("count 93-95", a("q13")), ("96", a("q14")), ("brass tag 1903", a("q15:nineteen-oh-three.")),
            ("elevator came down empty, waiting", a("q16:chimed.")), ("everything points up", a("q17:Everything")),
            ("Gus's last entry", a("q18:last")), ("Going up myself", a("q19:Going")), ("never signed back in", a("q20")),
            ("rule 3 inverted: he went himself", a("q21:went")), ("nobody went after him", a("q22:nobody")),
            ("somebody had to go up", a("q23:Somebody")), ("4 X key", a("q24:four.")), ("2 X elevator", a("q24:two.")),
            ("6 X desk", a("q25:six.")), ("3 X me", a("q25:three.")), ("Gus: nobody means you too", a("q26:Nobody")),
            ("lights dip at 13", a("q27:thirteen")), ("signal dies at 16", a("q27:sixteen")), ("how is the chat working?", a("q27:How?")),
            ("if I'm standing up there, it isn't me", a("q28")), ("19, doors open", a("q29:doors")),
            ("the man in the blazer", a("q30:blazer")), ("held", P2.by["ph1"]["start"] + 2.0), ("4% / 911 fails", a("q31:failed.")),
            ("in Gus's voice", a("q32:voice:")), ("Thanks, kid. Your shift now.", a("v2")), ("light out", a("q33:out.")),
            ("Gus: I lied so you wouldn't come", a("q34:lied")), ("Marcus added", a("q35:Marcus")), ("sending from me", a("q35:from#2")),
            ("rule 3 rewritten", a("q36:Even"))]


# ------------------------------------------------------------------ storyboard helpers

W, H = 1080, 1920
RED = "#ff3b30"
INK = "#07080b"
GREY = "#8a8f99"
BRASS = "#c9a24a"
NAVY, NAVY_SH, SHIRT = "#1d2740", "#141b2e", "#e9e4d8"


def rect(x, y, w, h, fill, radius=0, **kw):
    d = {"type": "rect", "x": x, "y": y, "width": w, "height": h, "fill": fill, "radius": radius}
    d.update(kw)
    return d


def circle(x, y, r, fill, **kw):
    d = {"type": "circle", "x": x, "y": y, "width": 2 * r, "height": 2 * r, "fill": fill}
    d.update(kw)
    return d


def text(s, x, y, size=40, color="#ffffff", weight=800, align="center", **kw):
    d = {"type": "text", "text": s, "x": x, "y": y, "fontSize": size, "color": color, "weight": weight, "align": align, "font": "body"}
    if align == "left":
        d["anchorX"] = 0
    elif align == "right":
        d["anchorX"] = 1
    d.update(kw)
    return d


def svg(markup, x=540, y=960, w=W, h=H, **kw):
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


def lena(expr="scared", exprs=None, pose="phone", lookX=0.0, lookY=0.4, light="phone", z=40, width=1150, x="50%", y="100%", depth=0, **kw):
    p = {"pose": pose, "exprs": exprs or [{"t": 0, "e": expr}], "lookX": lookX, "lookY": lookY, "light": light, "blink": True,
         "colors": {"top": NAVY, "topShade": NAVY_SH, "shirt": SHIRT}}
    p.update(kw.pop("props", {}))
    if "blink" in kw:
        p["blink"] = kw.pop("blink")
    return comp("horror/Protagonist", p, x=x, y=y, anchorY=1, width=width, height=round(width * 1.52), z=z, depth=depth, **kw)


def vig(a=0.45, z=50):
    return comp("horror/Vignette", {"amount": a}, depth=0, z=z)


def glitch(cues, seed="g", z=60):
    return comp("horror/Glitch", {"cues": [{"at": round(t, 3), "duration": d, "amount": a} for t, d, a in cues], "seed": seed}, depth=0, z=z)


MEMBERS = {"Gus": {"color": "#7a6142", "initials": "GB"}, "Mr. Pell (Owner)": {"color": "#3d4a6b", "initials": "P"},
           "Marcus": {"color": "#2f6b5a", "initials": "M"}, "Lena": {"color": "#8a4b5c", "initials": "L"}}


def handphone(chat=None, mode="chat", call=None, lock=None, banners=None, vibrate=None, tremble=1.5, tilt=-3, glitch_=None,
              clock="1:04", battery=41, z=10, cy=0.6):
    phone = {"members": MEMBERS, "mode": mode}
    if chat:
        phone["chat"] = {"theme": "dark", "scale": 1.25, "clock": clock, "battery": battery, **chat}
    if call:
        phone["call"] = {"battery": battery, **call}
    if lock:
        phone["lock"] = lock
    if banners:
        phone["banners"] = banners
    if vibrate:
        phone["vibrate"] = vibrate
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": cy, "tilt": tilt, "tremble": tremble, "side": "right", "phone": phone,
         "thumbY": 0.94, "thumbReach": 0.1}
    if glitch_:
        p["glitch"] = glitch_
    return comp("horror/HandPhone", p, z=z)


def msgs(thread, t0, upto=None):
    return [{**m, "at": round(m["at"] - t0, 3)} for m in thread if upto is None or m["at"] <= upto]


def cam(*kf, shake=None):
    c = {"keyframes": [{"t": round(t, 3), "zoom": zz, "x": f"{x:.2f}%", "y": f"{y:.2f}%", "ease": e} for t, zz, x, y, e in kf]}
    if shake:
        c["shake"] = [{"at": round(a, 3), "duration": d, "amplitude": amp} for a, d, amp in shake]
    return c


def push(d, z0=1.0, z1=1.06, x=50, y=50, x1=None, y1=None):
    return cam((0, z0, x, y, "linear"), (d, z1, x if x1 is None else x1, y if y1 is None else y1, "linear"))


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


def stamp(s, x, y, at, size=110, rot=-7, color="#ffffff", bg=RED, z=70):
    return text(s, x, y, size, color, 900, background=bg, padding=22, radius=14, rotate=rot, z=z, depth=0, start=round(at, 3),
                enter={"type": "pop", "duration": 0.18}, font="display")


def card(s, y, at=None, color="#ffffff", bg="#1f232b", size=46, z=30, border=None, width=880):
    d = text(s, 540, y, size, color, 800, maxWidth=width, lineHeight=1.2, background=bg, padding=30, radius=30, z=z, depth=0,
             shadow="0 18px 40px rgba(0,0,0,.6)")
    if at is not None:
        d["start"] = round(at, 3)
        d["enter"] = {"type": "pop", "duration": 0.18}
    return d


# ------------------------------------------------------------------ set art (inline SVG, 1080x1920 art boxes)

SVGNS = 'xmlns="http://www.w3.org/2000/svg"'
FONT = 'font-family="Montserrat, sans-serif" font-weight="800"'

# desk phone close-up: unit buttons 1901-1908 in 2 columns; 1903 = column 0, row 1 at (300, 1010)
BTN = {f"190{i + 1}": (300 + (i % 2) * 400, 860 + (i // 2) * 150) for i in range(8)}
T1903 = BTN["1903"]


def desk_phone_svg():
    btns = []
    for u, (x, y) in BTN.items():
        btns.append(f'<rect x="{x - 150}" y="{y - 55}" width="300" height="110" rx="16" fill="#e9e5da" stroke="#5b5649" stroke-width="5"/>'
                    f'<circle cx="{x - 112}" cy="{y}" r="15" fill="#3a1416" stroke="#1a0a0b" stroke-width="3"/>'
                    f'<text x="{x + 20}" y="{y + 17}" text-anchor="middle" {FONT} font-size="48" fill="#34312a">{u}</text>')
    return (f'<svg viewBox="0 0 1080 1920" {SVGNS}><defs><linearGradient id="dk" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#1c1e24"/><stop offset="1" stop-color="#0b0c0f"/></linearGradient>'
            '<linearGradient id="bd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfc8b8"/><stop offset="1" stop-color="#a39c8b"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="url(#dk)"/>'
            '<path d="M0 1700 Q 300 1640 540 1660 Q 800 1680 1080 1620 L1080 1920 L0 1920Z" fill="#14161b" opacity="0.8"/>'
            '<rect x="70" y="330" width="940" height="1330" rx="70" fill="url(#bd)" stroke="#2a2822" stroke-width="10"/>'
            '<rect x="110" y="360" width="860" height="160" rx="80" fill="#2a2b2f" stroke="#111" stroke-width="8"/>'
            '<rect x="160" y="395" width="200" height="90" rx="40" fill="#35363b"/><rect x="720" y="395" width="200" height="90" rx="40" fill="#35363b"/>'
            '<rect x="230" y="580" width="620" height="170" rx="18" fill="#26332a" stroke="#1a1a16" stroke-width="8"/>'
            f'<text x="540" y="810" text-anchor="middle" {FONT} font-size="30" fill="#6b6556" letter-spacing="6">CALLOWAY · FRONT DESK · FLOOR 19</text>'
            + "".join(btns) +
            '<g fill="#bdb6a6" stroke="#5b5649" stroke-width="4">' +
            "".join(f'<rect x="{220 + c * 230}" y="{1440 + r * 0 }" width="180" height="90" rx="14"/>' for c in range(3) for r in range(1)) +
            '</g></svg>')


TAPE = (f'<svg viewBox="0 0 360 160" {SVGNS}><path d="M 8 18 L 352 4 L 356 142 L 4 156 Z" fill="#e8c547" opacity="0.80"/>'
        '<path d="M 300 6 L 352 4 L 354 52 Z" fill="#f6e9a8" opacity="0.95"/><path d="M 300 6 L 354 52 L 322 40 Z" fill="#b8962e" opacity="0.7"/>'
        '<path d="M 20 40 L 330 30" stroke="#fff6c8" stroke-width="5" opacity="0.35"/></svg>')


def desk_phone(lit=None, lcd="", lcd_color="#9fe0a6", pulses=None, cover=False, z=0, lcd_track=None):
    """Desk phone ECU. lit: None | 'dim' | 'red'. pulses: [t] scene-local ring pulses (red light flares)."""
    x, y = T1903
    out = [svg(desk_phone_svg(), z=z)]
    if lit:
        a = 0.95 if lit == "red" else 0.45
        kf = []
        for p in pulses or []:
            kf += [{"t": round(max(0, p - 0.05), 3), "opacity": a * 0.55}, {"t": round(p + 0.1, 3), "opacity": 1.0, "ease": "out"},
                   {"t": round(p + 1.6, 3), "opacity": a * 0.55, "ease": "in"}]
        out.append(circle(x, y, 120, "rgba(255,40,30,0.95)", blur=22, opacity=a, z=z + 1, keyframes=kf,
                          idle=[] if kf else [{"type": "pulse", "amount": 0.08, "speed": 0.8}]))
        out.append(circle(x - 112, y, 18, "#ff5a4a", z=z + 1, opacity=a))
    out.append(svg(TAPE, x, y, 360, 160, rotate=-3, z=z + 2))
    if lit:
        halo = 0.55 if cover else (0.4 if lit == "red" else 0.18)
        out.append(circle(x, y, 260, "rgba(255,50,35,0.55)", blur=60, opacity=halo, z=z + 3))
    if lcd_track:
        for i, (t0, s, col) in enumerate(lcd_track):
            t1 = lcd_track[i + 1][0] if i + 1 < len(lcd_track) else None
            l = text(s, 540, 665, 64, col, 900, z=z + 4, font="condensed", letterSpacing=0.06)
            l["start"] = round(t0, 3)
            if t1 is not None:
                l["end"] = round(t1, 3)
            out.append(l)
    elif lcd:
        out.append(text(lcd, 540, 665, 64, lcd_color, 900, z=z + 4, font="condensed", letterSpacing=0.06))
    return out


# key board: 96 hooks = 24 floors x 4 units; 12 rows (two floors per row, top = floor 24), 8 columns
def hook_xy(unit: int):
    f, u = unit // 100, unit % 100
    row = (24 - f) // 2
    col = ((24 - f) % 2) * 4 + (u - 1)
    return 155 + col * 110, 420 + row * 105


KEY = ('<g transform="translate({x},{y})"><circle cx="0" cy="0" r="7" fill="#d9d4c7"/>'
       '<path d="M -9 6 L 9 6 L 6 64 L -6 64 Z" fill="{c}" stroke="#5a4520" stroke-width="2"/>'
       '<circle cx="0" cy="18" r="9" fill="#1b140c"/><rect x="-14" y="38" width="28" height="22" rx="4" fill="#efe6cf" opacity="0.9"/></g>')


def keyboard_svg(extra=False):
    units = [f * 100 + u for f in range(1, 25) for u in range(1, 5)]
    g = []
    for un in units:
        x, y = hook_xy(un)
        g.append(f'<text x="{x}" y="{y - 14}" text-anchor="middle" {FONT} font-size="17" fill="#8f8270">{un}</text>'
                 f'<circle cx="{x}" cy="{y}" r="6" fill="#a19a8a"/>')
        if un != 1903:
            g.append(KEY.format(x=x, y=y, c="#a9894a"))
    return (f'<svg viewBox="0 0 1080 1920" {SVGNS}><rect width="1080" height="1920" fill="#120f0d"/>'
            '<rect x="60" y="300" width="960" height="1380" rx="20" fill="#2c2119" stroke="#0c0907" stroke-width="12"/>'
            '<rect x="90" y="330" width="900" height="1320" rx="12" fill="#3a2b20"/>'
            f'<text x="540" y="1630" text-anchor="middle" {FONT} font-size="34" fill="#c9b48a" letter-spacing="8">KEYS · 96 UNITS</text>'
            + "".join(g) + '</svg>')


def keyboard(extra_at=None, z=0, highlight=None):
    out = [svg(keyboard_svg(), z=z)]
    x, y = hook_xy(1903)
    out.append(circle(x, y + 30, 46, "rgba(255,59,48,0)", stroke=RED, strokeWidth=5, z=z + 1, opacity=0.9,
                      idle=[{"type": "pulse", "amount": 0.1, "speed": 1.2}]) if highlight else None)
    if extra_at is not None:
        k = svg(f'<svg viewBox="-30 -10 60 90" {SVGNS}>' + KEY.format(x=0, y=0, c="#d6b25a") + '</svg>', x, y + 35, 60, 90, z=z + 2,
                start=round(extra_at, 3), idle=[{"type": "sway", "amount": 5, "speed": 0.6}], anchorY=0.1)
        out.append(k)
    return [o for o in out if o]


def lobby_svg():
    return (f'<svg viewBox="0 0 1080 1920" {SVGNS}><defs>'
            '<radialGradient id="lamp" cx="0.5" cy="0.62" r="0.5"><stop offset="0" stop-color="#f0d9a0" stop-opacity="0.32"/>'
            '<stop offset="1" stop-color="#f0d9a0" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1626"/><stop offset="1" stop-color="#14263b"/></linearGradient>'
            '<linearGradient id="mb" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8d4cc"/><stop offset="1" stop-color="#9c978d"/></linearGradient></defs>'
            '<rect width="1080" height="1920" fill="#15181e"/>'
            '<rect x="0" y="1350" width="1080" height="570" fill="#202329"/>'
            '<path d="M0 1350 L1080 1350" stroke="#2c3038" stroke-width="6"/>'
            # glass doors (left), street outside
            '<rect x="50" y="520" width="380" height="830" fill="url(#st)" stroke="#9aa3ad" stroke-width="10"/>'
            '<circle cx="150" cy="640" r="70" fill="#f5d38a" opacity="0.25"/><rect x="140" y="640" width="10" height="700" fill="#2b3442"/>'
            '<line x1="240" y1="520" x2="240" y2="1350" stroke="#9aa3ad" stroke-width="10"/>'
            # elevator (right)
            '<rect x="670" y="600" width="340" height="750" fill="#2a2e35" stroke="#9aa3ad" stroke-width="10"/>'
            '<rect x="690" y="620" width="148" height="720" fill="#5d646e"/><rect x="842" y="620" width="148" height="720" fill="#58606a"/>'
            '<rect x="780" y="520" width="120" height="60" rx="8" fill="#0b0909" stroke="#3a3d44" stroke-width="4"/>'
            # key board on the back wall
            '<rect x="455" y="640" width="190" height="300" rx="8" fill="#2c2119" stroke="#0c0907" stroke-width="6"/>'
            + "".join(f'<circle cx="{475 + c * 21}" cy="{665 + r * 23}" r="4" fill="#a9894a"/>' for c in range(8) for r in range(12)) +
            '<rect width="1080" height="1920" fill="url(#lamp)"/>'
            '</svg>')


DESK_FRONT = (f'<svg viewBox="0 0 1080 700" {SVGNS}><defs><linearGradient id="mb2" x1="0" y1="0" x2="1" y2="1">'
              '<stop offset="0" stop-color="#d8d4cc"/><stop offset="1" stop-color="#8e897f"/></linearGradient></defs>'
              '<path d="M 150 80 L 930 80 L 980 160 L 100 160 Z" fill="#e9e5dc" stroke="#2a2a2a" stroke-width="6"/>'
              '<rect x="100" y="160" width="880" height="420" fill="url(#mb2)" stroke="#2a2a2a" stroke-width="6"/>'
              '<path d="M 180 230 Q 400 300 520 260 T 900 330" stroke="#ffffff" stroke-width="4" fill="none" opacity="0.35"/>'
              '<path d="M 200 420 Q 380 380 600 450 T 940 400" stroke="#6f6a61" stroke-width="3" fill="none" opacity="0.5"/>'
              # monitor + desk phone + log on the desk top
              '<rect x="700" y="-40" width="210" height="140" rx="10" fill="#111" stroke="#444" stroke-width="6"/>'
              + "".join(f'<rect x="{712 + c * 64}" y="{-28 + r * 62}" width="58" height="56" fill="#3b3f45"/>' for c in range(3) for r in range(2)) +
              '<rect x="230" y="40" width="170" height="60" rx="12" fill="#bfb8a8" stroke="#333" stroke-width="5"/>'
              '<rect x="450" y="60" width="160" height="34" fill="#efe9da" stroke="#333" stroke-width="4"/>'
              '</svg>')


GLASS_DOOR = (f'<svg viewBox="0 0 180 830" {SVGNS}><rect x="5" y="5" width="170" height="820" fill="#9fc3e6" opacity="0.10" '
              'stroke="#c9d2de" stroke-width="10"/><path d="M 30 80 L 150 30" stroke="#ffffff" stroke-width="6" opacity="0.25"/>'
              '<rect x="140" y="380" width="14" height="90" rx="6" fill="#c9d2de"/></svg>')


def lobby(door_open_at=None, door_shut_at=None, lena_props=None, elevator_display=None, z=0, dim=None, flicker=None):
    """Lobby wide. The right-hand glass door (x 240..430) swings open (scaleX) at door_open_at."""
    out = [svg(lobby_svg(), z=z)]
    gd = svg(GLASS_DOOR, 240, 935, 190, 830, anchorX=0, z=z + 1)
    kf = []
    if door_open_at is not None:
        kf += [{"t": round(door_open_at, 3), "scaleX": 1.0}, {"t": round(door_open_at + 0.6, 3), "scaleX": 0.25, "ease": "out"}]
    if door_shut_at is not None:
        kf += [{"t": round(door_shut_at, 3), "scaleX": 0.25}, {"t": round(door_shut_at + 0.25, 3), "scaleX": 1.0, "ease": "in"}]
    if kf:
        gd["keyframes"] = kf
    out.append(gd)
    if elevator_display:
        for i, (t0, s) in enumerate(elevator_display):
            t1 = elevator_display[i + 1][0] if i + 1 < len(elevator_display) else None
            l = text(s, 840, 551, 44, RED, 900, z=z + 2, font="condensed", start=round(t0, 3))
            if t1 is not None:
                l["end"] = round(t1, 3)
            out.append(l)
    lp = {"expr": "neutral", "pose": "phone", "lookX": 0.0, "lookY": 0.5, "light": "phone"}
    lp.update(lena_props or {})
    out.append(lena(width=330, x=540, y=1330, z=z + 3, depth=1, **{k: v for k, v in lp.items()}))
    out.append(svg(DESK_FRONT, 540, 1600, 1080, 700, z=z + 4))
    if flicker:
        out.append(comp("horror/Flicker", {"strength": flicker, "from": 0}, depth=0, z=z + 20))
    if dim:
        out.append(rect(540, 960, W, H, "#000", opacity=dim, z=z + 19, depth=0))
    return out


def elevator_view(open_at=None, close_at=None, display=None, z=0, lit19=True):
    """Elevator doors full frame; doors slide apart at open_at and close at close_at; display track [(t, text)]."""
    car = (f'<svg viewBox="0 0 1080 1920" {SVGNS}><rect width="1080" height="1920" fill="#17191e"/>'
           '<rect x="140" y="420" width="800" height="1300" fill="#e9d9a6"/><rect x="200" y="470" width="680" height="1200" fill="#cbb984"/>'
           '<rect x="200" y="1160" width="680" height="24" rx="12" fill="#8a7b52"/><rect x="760" y="760" width="90" height="300" rx="8" fill="#9d9a8e"/>'
           + (f'<circle cx="805" cy="800" r="16" fill="#ffb35c"/>' if lit19 else '') +
           '<rect x="200" y="1500" width="680" height="170" fill="#9c8a5c"/></svg>')
    frame = (f'<svg viewBox="0 0 1080 1920" {SVGNS}><path d="M0 0 H1080 V1920 H0 Z M140 420 V1720 H940 V420 Z" fill="#2a2e35" fill-rule="evenodd"/>'
             '<rect x="140" y="420" width="800" height="1300" fill="none" stroke="#9aa3ad" stroke-width="16"/>'
             '<rect x="420" y="250" width="240" height="120" rx="10" fill="#0b0909" stroke="#3a3d44" stroke-width="6"/>'
             '<rect x="0" y="1720" width="1080" height="200" fill="#202329"/></svg>')
    out = [svg(car, z=z)]
    for side in (0, 1):
        x0 = 340 if side == 0 else 740
        dx = -390 if side == 0 else 390
        kf = []
        if open_at is not None:
            kf += [{"t": round(open_at, 3), "x": x0}, {"t": round(open_at + 0.7, 3), "x": x0 + dx, "ease": "inOut"}]
        if close_at is not None:
            kf += [{"t": round(close_at, 3), "x": x0 + dx}, {"t": round(close_at + 0.7, 3), "x": x0, "ease": "inOut"}]
        out.append(rect(x0, 1070, 400, 1300, "#6b7280" if side == 0 else "#646b76", stroke="#3b3f46", strokeWidth=6, z=z + 1, keyframes=kf))
    out.append(svg(frame, z=z + 2))
    for i, (t0, s) in enumerate(display or []):
        t1 = display[i + 1][0] if i + 1 < len(display) else None
        l = text(s, 540, 312, 92, RED, 900, z=z + 3, font="condensed", start=round(t0, 3))
        if t1 is not None:
            l["end"] = round(t1, 3)
        out.append(l)
    return out


def count_track(t0, frm, to, per, label=None):
    n = abs(to - frm)
    step = 1 if to >= frm else -1
    tr = [(round(t0 + i * per, 3), str(frm + step * i) if (frm + step * i) > 1 else (label or "1")) for i in range(n + 1)]
    return tr


# back-view man in a concierge blazer (viewBox 200 x 520): no face, collar line, navy blazer
FIGURE = (f'<svg viewBox="0 0 200 520" {SVGNS}>'
          '<ellipse cx="100" cy="62" rx="36" ry="44" fill="#3d3833"/><path d="M 66 70 Q 100 108 134 70 L 132 96 Q 100 116 68 96 Z" fill="#2c2824"/>'
          '<rect x="84" y="96" width="32" height="22" fill="#b89a82"/><path d="M 80 112 L 120 112 L 116 126 L 84 126 Z" fill="#e9e4d8"/>'
          '<path d="M 30 136 Q 40 118 84 116 L 116 116 Q 160 118 170 136 L 178 330 L 22 330 Z" fill="#1d2740" stroke="#0b0f1a" stroke-width="4"/>'
          '<path d="M 100 120 L 100 330" stroke="#141b2e" stroke-width="5"/>'
          '<path d="M 26 150 L 12 320 Q 18 336 32 330 L 44 168 Z" fill="#18213a"/><path d="M 174 150 L 188 320 Q 182 336 168 330 L 156 168 Z" fill="#18213a"/>'
          '<ellipse cx="22" cy="334" rx="12" ry="16" fill="#b89a82"/><ellipse cx="178" cy="334" rx="12" ry="16" fill="#b89a82"/>'
          '<path d="M 46 330 L 154 330 L 150 500 L 108 500 L 100 360 L 92 500 L 50 500 Z" fill="#15171b"/>'
          '<rect x="44" y="498" width="50" height="16" rx="6" fill="#0a0a0a"/><rect x="106" y="498" width="50" height="16" rx="6" fill="#0a0a0a"/></svg>')

# end door of the Hallway art: x 490..590, y 790..1010; end wall x 420..660, y 700..1010


def hallway_1903(gap_kf=None, gap0=0.18, figure=True, plate=True, z=0, lights=1, flicker=0.15, cctv=False):
    out = [full("horror/Hallway", {"lights": lights, "flicker": flicker, "endDoor": True, "figure": 0, "runner": "#3a1f22"}, z=z)]
    g = rect(590, 900, 100, 220, "#000000", anchorX=1, z=z + 1, scaleX=gap0)
    if gap_kf:
        g["keyframes"] = gap_kf
    out.append(g)
    if plate:
        out.append(text("1903", 540, 832, 15, "#2a241c", 900, background="#c8bb98", padding=3, radius=2, z=z + 2))
    if figure:
        out.append(svg(FIGURE, 626, 1010, 74, 192, anchorY=1, z=z + 3))
    if cctv:
        out.append(text("CAM 19-E", 70, 260, 44, "#e8e8e8", 800, "left", z=z + 5, depth=0, font="condensed"))
        out.append(text("02:44:07", 1010, 260, 44, "#e8e8e8", 800, "right", z=z + 5, depth=0, font="condensed"))
        out.append(circle(1010, 330, 12, RED, z=z + 5, depth=0, idle=[{"type": "pulse", "amount": 0.3, "speed": 1}]))
        out.append(comp("horror/Glitch", {"amount": 0.08, "seed": "cctv"}, depth=0, z=z + 4))
    return out


def cctv_grid(z=0):
    """Monitor with a 2x3 grid; tile (1,0) = CAM 19-E is at (780, 760) size 460x340."""
    out = [rect(540, 960, 1000, 1200, "#0d0e10", radius=30, stroke="#3a3d44", strokeWidth=14, z=z)]
    tiles = [("CAM L-1", 300, 760), ("CAM 19-E", 780, 760), ("ELEV A", 300, 1120), ("CAM 07-W", 780, 1120), ("STAIR B", 300, 1480),
             ("GARAGE", 780, 1480)]
    for name, x, y in tiles:
        out.append(rect(x, y, 460, 340, "#22252a", z=z + 1))
        if name == "CAM 19-E":
            out += [comp("horror/Hallway", {"lights": 1, "flicker": 0.1, "endDoor": True, "figure": 0}, x=x, y=y, width=460, height=340, z=z + 2),
                    rect(x + (590 - 540) * 460 / 1080 * 1.0, y, 6, 30, "#000", z=z + 3)]
        elif name == "CAM 07-W":
            out.append(comp("horror/Hallway", {"lights": 2, "flicker": 0.05, "endDoor": True, "figure": 0}, x=x, y=y, width=460, height=340, z=z + 2))
        elif name == "STAIR B":
            out.append(comp("horror/Stairwell", {"floor": "B"}, x=x, y=y, width=460, height=340, z=z + 2))
        elif name == "ELEV A":
            out.append(comp("horror/ElevatorPanel", {"from": 19, "to": 19, "at": 0, "floors": 20}, x=x, y=y, width=460, height=340, z=z + 2))
        else:
            out.append(svg(lobby_svg(), x, y, 460, 340, z=z + 2, opacity=0.8))
        out.append(text(name, x - 215, y - 145, 24, "#e8e8e8", 800, "left", z=z + 4, font="condensed"))
    out.append(text("CALLOWAY CCTV · 02:44", 540, 420, 34, "#9aa0a8", 800, z=z + 4, font="condensed"))
    return out


def paper(lines_, title, z=0, y0=520, ruled=True, cols=None):
    """A laminated or ruled sheet with rows of text. lines_: [(text, color, start or None)]."""
    out = [rect(540, 980, 900, 1300, "#efeadf", radius=14, z=z, shadow="0 30px 60px rgba(0,0,0,.7)"),
           rect(540, 980, 900, 1300, "rgba(255,255,255,0.10)", radius=14, z=z + 6),
           text(title, 140, y0 - 80, 36, "#2a2a2a", 900, "left", z=z + 1)]
    if ruled:
        out += [rect(540, y0 - 40 + i * 92, 820, 3, "#c9c2b1", z=z + 1) for i in range(12)]
    for i, (s, col, st) in enumerate(lines_):
        l = text(s, 140, y0 + i * 92, 34, col, 700, "left", z=z + 2)
        if st is not None:
            l["start"] = round(st, 3)
        out.append(l)
    return out


def phone_glow_dark(x=0.5, y=0.55, r=0.38, dark=0.82, z=55):
    return comp("horror/Darkness", {"x": x, "y": y, "radius": r, "darkness": dark}, depth=0, z=z)


# ------------------------------------------------------------------ Part 1 scenes


def p1_scenes():
    a, BY = P1.at, P1.by
    S = []
    handover = [{"from": "Gus", "text": "6 rules. Read them twice.", "at": a("n4:Desk")}]
    for i in range(1, 7):
        m = {"from": "Gus", "text": L.RULES[i], "at": round(a("n4:Desk") + 0.5 + 0.28 * i, 3)}
        if i == 3:
            m["kind"] = "alert"
        handover.append(m)
    handover += [
        {"from": "Gus", "text": "Shut the door. Rule 1, never open the glass doors after 1.", "at": a("g1:Shut")},
        {"from": "Gus", "text": "Rule 2. If the elevator comes down empty, don't get in.", "at": a("g2:Rule")},
        {"me": True, "text": "The owner says go up. Which rule wins?", "at": a("n17:asked")},
        {"from": "Gus", "text": "What number texted you?", "at": a("g3:What")},
        {"me": True, "text": "[screenshot] Mr. Pell (Owner) · 555-0143", "at": a("n18:sent")},
        {"from": "Gus", "text": "That number was never his.", "at": a("g4")},
        {"from": "Gus", "text": "Don't go up. Don't send anyone.", "at": a("g5:Don't")},
        {"me": True, "text": "and if 1903 calls?", "at": a("n20:and")},
        {"me": True, "text": "why did you leave?", "at": a("n24:why")},
        {"from": "Gus", "text": "Let it ring.", "at": a("g6")},
    ]
    pell = [{"kind": "system", "text": "Mr. Pell (Owner) · saved contact", "at": a("n14") - 5},
            {"from": "Mr. Pell (Owner)", "text": "1903 needs help. Go up now.", "at": a("p1")},
            {"from": "Mr. Pell (Owner)", "text": "Gus doesn't work here anymore. Ask him why he left at 2:41 last night.", "at": a("p2:Gus")}]
    gus_chat = {"title": "Desk Handover", "subtitle": "Gus · online", "accent": "#7a6142"}
    pell_chat = {"title": "Mr. Pell (Owner)", "subtitle": "Owner · Calloway", "accent": "#3d4a6b", "dm": "Mr. Pell (Owner)"}

    def hp(t0, upto=None, clock="1:04", **kw):
        chat = {**gus_chat, **kw.pop("chat", {}), "messages": msgs(handover, t0, upto)}
        return handphone(chat, clock=clock, **kw)

    def blurred(z=0, **lp):
        return [svg(lobby_svg(), z=z, blur=10, opacity=0.6, depth=0.2)]

    # s01 HOOK / COVER ---------------------------------------------------------------------------
    t0, t1 = 0.0, a("n2:text")
    e = a("n1:Nineteen-oh-three#2")
    lay = desk_phone(lit="red", lcd="LINE 1903", lcd_color="#ff6a5a", cover=True)
    lay += [card(L.RULES[3], 500, color="#ffffff", bg="#b3261e", size=50, z=30)]
    lay += [vig(0.4)]
    S.append(scene("s01_cover", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (e, 1.06, 50, 50, "linear"), (e + 0.01, 1.22, 32, 52, "step"),
                                                         (t1, 1.3, 30, 53, "linear")),
                   notes="FRAME 0 = COVER: the red light glows bright through the yellow tape on 1903's button (brighter than the story "
                         "has it, for the grid); the rule-3 bubble as a red card. Punch-in on the tape on 'Nineteen-oh-three is empty'."))
    # s02 owner's banner -------------------------------------------------------------------------
    t0, t1 = a("n2:text"), a("n3")
    lay = [svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2),
           handphone(mode="lock", lock={"time": "2:41", "date": "Tuesday"}, clock="2:41",
                     banners=[{"at": 0.05, "duration": 4, "app": "Messages", "title": "Mr. Pell (Owner)", "text": "1903 needs help. Go up now."}],
                     vibrate=[{"at": 0.05, "duration": 0.5, "amount": 1}], glitch_=[{"at": 0.35, "duration": 0.2, "amount": 0.8}]),
           glitch([(0.35, 0.18, 0.7)], "g1"), vig(0.45)]
    S.append(scene("s02_order", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (0.3, 1.22, 50, 36, "out"), (t1 - t0, 1.25, 50, 36, "linear"),
                                                        shake=[(0.3, 0.2, 10)]), trans={"type": "glitch", "duration": 0.15},
                   notes="Flash-forward contradiction by 6 s: the owner's text orders rule 3 broken."))
    # s03 lobby + Gus card ------------------------------------------------------------------------
    t0, t1 = a("n3"), a("n4")
    g = a("n3:Gus,") - t0
    lay = timed(lobby(lena_props={"expr": "neutral", "lookY": 0.5}), 0, g)
    lay += timed([svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2),
                  hp(t0, upto=-1, chat={"messages": [{"kind": "system", "text": "Gus Brandt · Night Desk · 31 yrs", "at": 0.0}]}, clock="11:02")], g, t1 - t0)
    S.append(scene("s03_setup", t0, t1, lay, camera=cam((0, 1.0, 46, 52, "linear"), (g - 0.01, 1.05, 52, 52, "linear"), (g, 1.0, 50, 50, "step"),
                                                        (t1 - t0, 1.04, 50, 50, "linear")),
                   notes="The Calloway lobby (glass doors, desk, elevator, key board); then the only contact: a system card for Gus."))
    # s04 the handover chat + 6 rules -------------------------------------------------------------
    t0, t1 = a("n4"), a("n5")
    lay = blurred() + [handphone({**gus_chat, "messages": msgs(handover, t0, a("n4:six") + 1)}, clock="11:02",
                                 banners=[{"at": 0.0, "duration": 1.4, "app": "Desk Handover", "title": "Gus added you", "text": "Desk Handover"}]),
                       vig(0.4)]
    S.append(scene("s04_rules", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.08, 50, 46, "linear")),
                   notes="Six bubbles stack in fast on 'six rules' (one pop each); rule 3 is the red alert bubble."))
    # s05 rule 1 broken ---------------------------------------------------------------------------
    t0, t1 = a("n5"), a("n6")
    pr = a("n5:propped") - t0
    lay = lobby(door_open_at=pr, lena_props={"expr": "relieved", "pose": "idle", "lookX": -0.6, "light": "none"})
    lay += [text("1:04 AM", 950, 430, 48, "#9fe0a6", 900, "right", depth=0, z=60, font="condensed", background="#0b0d10", padding=12, radius=8)]
    S.append(scene("s05_break", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (pr, 1.08, 38, 52, "linear"), (t1 - t0, 1.12, 34, 52, "linear")),
                   notes="B3 at ~13%: a minor rule broken before she has read it (HEARSE-P1 0:31). The glass door swings open on 'propped'."))
    # s06 the elevator answers --------------------------------------------------------------------
    t0, t1 = a("n6"), a("g1")
    ln = BY["n6"]["end"] - t0 + 0.3
    lay = elevator_view(display=[(0, "19")] + [(round(0.55 + 0.32 * i, 3), str(19 - i)) for i in range(1, 8)])
    lay += [vig(0.4)]
    S.append(scene("s06_answer", t0, t1, lay, camera=push(t1 - t0, 1.35, 1.45, 50, 22, None, 20),
                   notes="Something visibly answers: the display counts down from 19 with nobody pressing it."))
    # s07 Gus knows -------------------------------------------------------------------------------
    t0, t1 = a("g1"), a("n7")
    lay = blurred() + [hp(t0, upto=a("g1:Shut") + 0.01, clock="1:04", chat={"pinned": {"text": L.RULES[1], "label": "RULE 1", "at": round(a("g1:Rule") - t0, 3)}}),
                       vig(0.4)]
    S.append(scene("s07_gus_knows", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (0.2, 1.12, 50, 56, "out"), (t1 - t0, 1.14, 50, 56, "linear"))))
    # s08 how did he know -------------------------------------------------------------------------
    t0, t1 = a("n7"), a("n8")
    lay = [svg(lobby_svg(), blur=6, opacity=0.7, depth=0.2), lena(exprs=[{"t": 0, "e": "suspicious"}], lookY=-0.6, lookX=0.2, light="phone"), vig(0.5)]
    S.append(scene("s08_how", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.08, 50, 40),
                   notes="Plant: Gus knew. He is in the building (Part 2: his phone is in 1903)."))
    # s09 door shut, empty car --------------------------------------------------------------------
    t0, t1 = a("n8"), a("g2")
    sh = a("n8:shut.") - t0
    op = a("n8:opened") - t0
    lay = timed(lobby(door_open_at=None, door_shut_at=None, lena_props={"expr": "scared", "pose": "idle", "lookX": 0.7, "light": "none"}) +
                [rect(335, 935, 190, 830, "#ffffff", opacity=0, z=8, keyframes=[{"t": sh, "opacity": 0.6}, {"t": sh + 0.15, "opacity": 0}])], 0, op)
    lay += timed(elevator_view(open_at=op + 0.05, display=[(0, "1")]), op, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("s09_empty", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (op - 0.01, 1.04, 56, 50, "linear"), (op, 1.0, 50, 55, "step"),
                                                        (t1 - t0, 1.08, 50, 58, "linear"), shake=[(sh, 0.2, 10)])))
    # s10 rule 2 ----------------------------------------------------------------------------------
    t0, t1 = a("g2"), a("n9")
    lay = blurred() + [hp(t0, upto=a("g2:Rule") + 0.01, chat={"pinned": {"text": L.RULES[2], "label": "RULE 2", "at": 0.1}}), vig(0.4)]
    S.append(scene("s10_rule2", t0, t1, lay, camera=push(t1 - t0, 1.08, 1.12, 50, 56)))
    # s11 19 already lit ---------------------------------------------------------------------------
    t0, t1 = a("n9"), a("n10")
    al = a("n9:already") - t0
    # doors already open: draw the open state (doors parked aside)
    lay = timed([l for l in elevator_view(open_at=0.0, display=[(0, "1")])], 0, al - 0.3)
    lay += timed([comp("horror/ElevatorPanel", {"from": 1, "to": 1, "at": 0, "floors": 20, "target": 19, "pressed": [{"at": 0, "floor": 19}]},
                       x=540, y=960, width=W, height=H)], al - 0.3, t1 - t0)
    lay.append(vig(0.5))
    S.append(scene("s11_lit", t0, t1, lay, camera=cam((0, 1.0, 50, 55, "linear"), (al - 0.31, 1.06, 50, 52, "linear"), (al - 0.3, 1.9, 50, 34, "step"),
                                                      (t1 - t0, 2.0, 50, 34, "linear")),
                   notes="Rule 2 earns 'true': the car's panel already has 19 lit (wrong detail)."))
    # s12 waiting doors + climb -------------------------------------------------------------------
    t0, t1 = a("n10"), a("n11")
    lk = a("n10:looked") - t0
    cl = a("n10:climbed") - t0
    lay = timed(elevator_view(open_at=0.0, display=[(0, "1")]), 0, lk)
    lay += timed([svg(lobby_svg(), blur=6, opacity=0.7, depth=0.2), lena(exprs=[{"t": 0, "e": "scared"}], lookY=0.9, lookX=0.0, light="phone")], lk, cl)
    lay += timed(elevator_view(open_at=None, display=count_track(0, 1, 19, 0.09)), cl, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("s12_waits", t0, t1, lay, camera=cam((0, 1.0, 50, 55, "linear"), (lk - 0.01, 1.1, 50, 58, "linear"), (lk, 1.0, 50, 45, "step"),
                                                       (cl - 0.01, 1.05, 50, 45, "linear"), (cl, 1.35, 50, 22, "step"), (t1 - t0, 1.4, 50, 20, "linear")),
                   notes="The doors hold open until she looks down; the cut back finds them closed and the display climbing to 19."))
    # s13 verdict: read every rule twice ----------------------------------------------------------
    t0, t1 = a("n11"), a("n12")
    tw = a("n11:twice.") - t0
    lay = blurred() + [hp(t0, upto=a("n4:six") + 1, clock="1:06"),
                       text("✓", 900, 1215, 70, "#4ade80", 900, z=30, depth=0, start=0.4, enter={"type": "pop", "duration": 0.2}),
                       text("✓", 900, 1355, 70, "#4ade80", 900, z=30, depth=0, start=0.7, enter={"type": "pop", "duration": 0.2}), vig(0.4)]
    S.append(scene("s13_twice", t0, t1, lay, camera=cam((0, 1.12, 50, 60, "linear"), (tw, 1.0, 50, 52, "out"), (t1 - t0, 1.0, 50, 52, "linear")),
                   notes="Verdict line; the pull-out shows all six rules on screen (rules 4-6 are read just in time later)."))
    # s14 rule 4: the key board -------------------------------------------------------------------
    t0, t1 = a("n12"), a("n13")
    r4 = a("n12:At") - t0
    lay = keyboard(highlight=True) + [card(L.RULES[4], 1780, at=r4, size=40, z=30), vig(0.45)]
    kx, ky = hook_xy(1903)
    S.append(scene("s14_keys", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (r4, 1.05, 50, 48, "linear"),
                                                      (t1 - t0, 1.5, 100 * kx / W, 100 * (ky + 30) / H, "inOut")),
                   notes="Plant: 96 hooks (24 floors x 4), 95 keys; the empty hook is 1903's. The push ends on it."))
    # s15 the tape --------------------------------------------------------------------------------
    t0, t1 = a("n13"), a("n14")
    tp = a("n13:tape") - t0
    lay = desk_phone(lit=None, lcd="FRONT DESK", lcd_color="#9fe0a6") + [vig(0.45)]
    S.append(scene("s15_tape", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (tp, 1.1, 40, 52, "linear"),
                                                      (t1 - t0, 1.45, 100 * T1903[0] / W + 3, 100 * T1903[1] / H, "inOut")),
                   notes="Plant: the yellow tape, old, curling at one corner. No light yet."))
    # s16 2:41 text arrives ------------------------------------------------------------------------
    t0, t1 = a("n14"), a("p1")
    bz = a("n14:buzzed.") - t0
    lay = [svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2),
           text("2:41", 540, 560, 150, "#9fe0a6", 900, depth=0, z=20, font="condensed", background="#0b0d10", padding=16, radius=12, end=round(bz, 3)),
           timed([handphone({**pell_chat, "messages": msgs(pell, t0, a("n14"))}, clock="2:41",
                            vibrate=[{"at": 0.0, "duration": 0.4, "amount": 1}])], bz, None)[0], vig(0.45)]
    S.append(scene("s16_pell", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (bz - 0.01, 1.05, 50, 40, "linear"), (bz, 1.0, 50, 52, "step"),
                                                      (t1 - t0, 1.06, 50, 52, "linear"), shake=[(bz, 0.2, 10)]),
                   notes="MIDPOINT ~49%: a contact already saved as the owner."))
    # s17 Go up now -------------------------------------------------------------------------------
    t0, t1 = a("p1"), a("n15")
    lay = [svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2), handphone({**pell_chat, "messages": msgs(pell, t0, a("p1") + 0.01)}, clock="2:41"), vig(0.45)]
    S.append(scene("s17_goup", t0, t1, lay, camera=cam((0, 1.0, 50, 52, "linear"), (0.15, 1.2, 50, 60, "out"), (t1 - t0, 1.22, 50, 60, "linear"))))
    # s18 rule 5 (just in time) -------------------------------------------------------------------
    t0, t1 = a("n15"), a("n16")
    lay = blurred() + [hp(t0, upto=a("g2:Rule") + 0.01, clock="2:41", chat={"pinned": {"text": L.RULES[5], "label": "RULE 5", "at": 0.05}}), vig(0.4)]
    S.append(scene("s18_rule5", t0, t1, lay, camera=push(t1 - t0, 1.12, 1.16, 50, 34), trans={"type": "whip", "duration": 0.2, "direction": "up"}))
    # s19 collision -------------------------------------------------------------------------------
    t0, t1 = a("n16"), a("n17")
    th = a("n16:three") - t0
    wr = a("n16:wrong.") - t0
    lay = [svg(lobby_svg(), blur=12, opacity=0.5, depth=0.2),
           card(L.RULES[5], 720, size=46, z=30, bg="#1f3a2a"), card(L.RULES[3], 1180, at=th, size=46, z=30, bg="#7a1d18"),
           text("VS", 540, 950, 90, "#ffffff", 900, z=31, depth=0, start=round(th, 3), enter={"type": "pop", "duration": 0.2}, font="display"),
           vig(0.5)]
    S.append(scene("s19_collide", t0, t1, lay, camera=cam((0, 1.0, 50, 40, "linear"), (th, 1.05, 50, 48, "linear"), (wr, 1.12, 50, 50, "out"),
                                                         (t1 - t0, 1.14, 50, 50, "linear"), shake=[(wr, 0.2, 8)]),
                   notes="Two rival authorities in one list (DORM-RULES engine): obey the owner vs send nobody."))
    # s20 which rule wins + typing silence ---------------------------------------------------------
    t0, t1 = a("n17"), a("g3")
    ty = a("n17:typing.") - t0
    lay = blurred() + [hp(t0, upto=a("n17:asked") + 0.01, clock="2:42",
                          chat={"typing": [{"from": "Gus", "at": round(ty, 3), "until": round(ty + 0.7, 3)},
                                           {"from": "Gus", "at": round(ty + 1.4, 3), "until": round(t1 - t0, 3)}]}), vig(0.4)]
    S.append(scene("s20_typing", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.1, 50, 52, None, 46)))
    # s21 what number / screenshot ----------------------------------------------------------------
    t0, t1 = a("g3"), a("g4")
    lay = blurred() + [hp(t0, upto=a("n18:sent") + 0.01, clock="2:42"), vig(0.4)]
    S.append(scene("s21_number", t0, t1, lay, camera=push(t1 - t0, 1.08, 1.12, 50, 58)))
    # s22 never his -------------------------------------------------------------------------------
    t0, t1 = a("g4"), a("n19")
    lay = blurred() + [hp(t0, upto=a("g4") + 0.01, clock="2:42", glitch_=[{"at": 0.2, "duration": 0.25, "amount": 0.9}]),
                       glitch([(0.2, 0.2, 0.8)], "g2"), vig(0.45)]
    S.append(scene("s22_never", t0, t1, lay, camera=cam((0, 1.0, 50, 52, "linear"), (0.2, 1.25, 50, 62, "out"), (t1 - t0, 1.27, 50, 62, "linear"),
                                                       shake=[(0.2, 0.2, 12)])))
    # s23 the number was --------------------------------------------------------------------------
    t0, t1 = a("n19"), a("g5")
    lay = [svg(lobby_svg(), blur=6, opacity=0.7, depth=0.2), lena(exprs=[{"t": 0, "e": "shocked"}], lookY=0.3), vig(0.5)]
    S.append(scene("s23_numberwas", t0, t1, lay, camera=push(t1 - t0, 1.05, 1.15, 50, 40)))
    # s24 don't go up / and if 1903 calls ----------------------------------------------------------
    t0, t1 = a("g5"), a("n21")
    lay = blurred() + [hp(t0, upto=a("n20:and") + 0.01, clock="2:43"), vig(0.4)]
    S.append(scene("s24_dontgo", t0, t1, lay, camera=push(t1 - t0, 1.08, 1.14, 50, 58)))
    # s25 monitor grid ---------------------------------------------------------------------------
    nineteen = a("n21:On")
    t0, t1 = a("n21"), nineteen
    lay = cctv_grid() + [vig(0.4)]
    S.append(scene("s25_monitor", t0, t1, lay, grade={"saturate": 0.15, "contrast": 1.1},
                   camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 2.2, 72.2, 39.6, "in")),
                   notes="Monitor: 2x3 CCTV grid; digital zoom into CAM 19-E."))
    # s26 PEAK (held) ----------------------------------------------------------------------------
    t0, t1 = nineteen, a("p2")
    h0, h1 = BY["h1"]["start"] - t0, BY["h1"]["end"] - t0
    bl = a("n21:blazer") - t0
    gap = [{"t": 0.0, "scaleX": 0.14}, {"t": round(h0, 3), "scaleX": 0.18}, {"t": round(h1, 3), "scaleX": 0.55, "ease": "inOut"}]
    lay = hallway_1903(gap_kf=gap, gap0=0.14, figure=True, cctv=True, flicker=0.05)
    lay += [timed([rect(626, 920, 10, 10, "#000", opacity=0)], 0, bl)[0], vig(0.65)]
    S.append(scene("s26_peak", t0, t1, lay, grade={"saturate": 0.0, "contrast": 1.15, "brightness": 1.05},
                   camera=cam((0, 2.0, 50, 46, "linear"), (bl, 2.35, 53, 45.5, "linear"), (h0, 2.45, 53.5, 45.5, "out"), (h1, 2.47, 53.5, 45.5, "linear"),
                              (t1 - t0, 2.47, 53.5, 45.5, "linear")),
                   notes=f"B9 HELD IMAGE ({h1 - h0:.1f} s still, music out): 1903 open a crack, a back-view man in a concierge blazer "
                         "facing the wall beside it. During the hold the dark gap of the door widens (the one change in frame)."))
    # s27 Pell taunt -----------------------------------------------------------------------------
    t0, t1 = a("p2"), a("n22")
    lay = [svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2), handphone({**pell_chat, "messages": msgs(pell, t0)}, clock="2:44",
                                                                       vibrate=[{"at": 0.0, "duration": 0.4, "amount": 1}]), vig(0.45)]
    S.append(scene("s27_taunt", t0, t1, lay, camera=cam((0, 1.0, 50, 52, "linear"), (a("p2:two") - t0, 1.1, 50, 62, "linear"),
                                                       (t1 - t0, 1.2, 50, 64, "out"))))
    # s28 2:41 match -----------------------------------------------------------------------------
    t0, t1 = a("n22"), a("n23")
    tf = a("n22:twenty-four") - t0
    lay = [rect(540, 960, W, H, "#050506", depth=0), text("2:41", 540, 900, 300, RED, 900, font="condensed", z=5),
           text("- 24 h", 540, 1150, 110, "#ffffff", 900, font="condensed", z=5, start=round(tf, 3), enter={"type": "pop", "duration": 0.2}),
           comp("horror/Heartbeat", {"bpm": 72, "intensity": 0.5}, depth=0, z=55), vig(0.6)]
    S.append(scene("s28_match", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.12)))
    # s29 lifeline: security ---------------------------------------------------------------------
    t0, t1 = a("n23"), a("n24")
    nx = a("n23:Next") - t0
    lay = [svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2),
           handphone(mode="call", call={"name": "Calloway Security", "sub": "24 h line", "label": "recording…", "at": -0.3}, clock="2:45", tremble=2.5),
           card("Next patrol: 6:00 AM", 1560, at=nx, size=52, bg="#2a2e36", z=30), vig(0.45)]
    S.append(scene("s29_security", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.06)))
    # s30 isolation: dot grey --------------------------------------------------------------------
    t0, t1 = a("n24"), a("n25")
    gr = a("n24:grey.") - t0
    lay = blurred() + timed([hp(t0, upto=a("n24:why") + 0.01, clock="2:45")], 0, gr)
    lay += timed([hp(t0, upto=a("n24:why") + 0.01, clock="2:45", chat={"subtitle": "Gus · last seen 2:38"})], gr, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("s30_grey", t0, t1, lay, camera=cam((0, 1.0, 50, 52, "linear"), (gr, 1.15, 50, 34, "out"), (t1 - t0, 1.18, 50, 34, "linear")),
                   notes="B6 isolation: the presence line goes from 'online' to 'last seen 2:38'."))
    # s31 the sound ------------------------------------------------------------------------------
    t0, t1 = a("n25"), a("n25:Under")
    snd = a("n25:sound") - t0
    lay = lobby(lena_props={"expr": "terrified", "pose": "idle", "lookX": -0.2, "light": "none", "blink": False}, flicker=0.25)
    S.append(scene("s31_sound", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (t1 - t0, 1.15, 40, 78, "linear"), shake=[(snd, 0.25, 6)]),
                   notes="Sound before visual (TRUCKER 1:45): one distorted ring; lights dip."))
    # s32 red light + ring (held prop) ------------------------------------------------------------
    t0, t1 = a("n25:Under"), a("n26:and")
    h2 = BY["h2"]["start"] - t0
    lay = desk_phone(lit="red", pulses=[h2, h2 + 2.0], lcd_track=[(0, "LINE 1903", "#ff6a5a"), (h2, "LINE 1903 · RING", "#ff6a5a")]) + [
        comp("horror/Heartbeat", {"bpm": 70, "bpmTo": 95, "intensity": 0.6}, depth=0, z=55), vig(0.5)]
    S.append(scene("s32_redlight", t0, t1, lay, camera=cam((0, 1.25, 100 * T1903[0] / W + 4, 100 * T1903[1] / H - 4, "linear"),
                                                          (t1 - t0, 1.3, 100 * T1903[0] / W + 4, 100 * T1903[1] / H - 4, "linear")),
                   notes="The red light through the tape (pays the P1-7 plant), ring on the silence."))
    # s33 dot back to green ----------------------------------------------------------------------
    t0, t1 = a("n26:and"), a("g6")
    lay = blurred() + [hp(t0, upto=a("n24:why") + 0.01, clock="2:46", chat={"typing": [{"from": "Gus", "at": 0.5, "until": round(t1 - t0, 3)}]}), vig(0.45)]
    S.append(scene("s33_green", t0, t1, lay, camera=push(t1 - t0, 1.15, 1.18, 50, 34)))
    # s34 CLIFF + bookend ------------------------------------------------------------------------
    t0, t1 = a("g6"), P1.runtime
    bk = BY["g6"]["end"] - t0 + 0.05
    lay = timed(blurred() + [hp(t0, upto=a("g6") + 0.01, clock="2:46", tremble=3)], 0, bk)
    lay += timed(desk_phone(lit="red", pulses=[0.1], lcd="LINE 1903", lcd_color="#ff6a5a") +
                 [card(L.RULES[3], 500, color="#ffffff", bg="#b3261e", size=50, z=30),
                  text("PART 1/2", 540, 1500, 120, "#ffffff", 900, background=RED, padding=26, radius=16, rotate=-4, z=80, depth=0,
                       start=round(bk + 0.35, 3), enter={"type": "pop", "duration": 0.2}, font="display")], bk, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("s34_cliff", t0, t1, lay, camera=cam((0, 1.15, 50, 56, "linear"), (bk - 0.01, 1.2, 50, 56, "linear"), (bk, 1.0, 50, 50, "step"),
                                                       (t1 - t0, 1.12, 50, 50, "linear")),
                   notes="B12: a fresh imperative ('Let it ring.' was never said before), then the frame-0 framing as the bookend + PART 1/2."))
    return S


# ------------------------------------------------------------------ Part 2 scenes


def p2_scenes():
    a, BY = P2.at, P2.by
    S = []
    handover = [{"from": "Gus", "text": L.RULES[3], "at": -900, "kind": "alert"},
                {"from": "Gus", "text": "Let it ring.", "at": -30},
                {"from": "Gus", "text": "That wasn't me on the phone. I'm home in bed. Don't pick up again.", "at": a("q4:Gus:")},
                {"from": "Gus", "text": "Put the key back, please. Nobody means you too.", "at": a("q26:Gus:")},
                {"from": "Gus", "text": "If I'm standing up there, it isn't me.", "at": a("q28")},
                {"from": "Gus", "text": "I'm sorry. I lied so you wouldn't come.", "at": a("q34:Gus:")}]
    pell = [{"from": "Mr. Pell (Owner)", "text": "1903 needs help. Go up now.", "at": -400},
            {"from": "Mr. Pell (Owner)", "text": "Gus never came home last night. Go up.", "at": a("q5:Pell:")}]
    gus_chat = {"title": "Desk Handover", "subtitle": "Gus · online", "accent": "#7a6142"}
    pell_chat = {"title": "Mr. Pell (Owner)", "subtitle": "Owner · Calloway", "accent": "#3d4a6b", "dm": "Mr. Pell (Owner)"}

    def hp(t0, upto=None, clock="2:46", battery=11, **kw):
        chat = {**gus_chat, **kw.pop("chat", {}), "messages": msgs(handover, t0, upto)}
        return handphone(chat, clock=clock, battery=battery, **kw)

    def blurred():
        return [svg(lobby_svg(), blur=10, opacity=0.6, depth=0.2)]

    # t01 COLD OPEN / COVER --------------------------------------------------------------------
    t0, t1 = 0.0, a("q1:My")
    lay = desk_phone(lit="red", pulses=[0.0, 2.0], lcd="LINE 1903 · CALLING", lcd_color="#ff6a5a", cover=True) + [vig(0.45)]
    S.append(scene("t01_cover", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.06, 50, 50),
                   notes="FRAME 0 = COVER: the desk phone ringing from 1903, red light through the yellow tape, LCD 'LINE 1903 · CALLING'."))
    # t02 rules swore it was empty --------------------------------------------------------------
    t0, t1 = a("q1:My"), a("q2")
    lay = desk_phone(lit="red", pulses=[0.6], lcd="LINE 1903 · CALLING", lcd_color="#ff6a5a") + [card(L.RULES[3], 500, at=0.05, bg="#b3261e", size=50), vig(0.45)]
    S.append(scene("t02_rule", t0, t1, lay, camera=push(t1 - t0, 1.12, 1.18, 30, 52)))
    # t03 let it ring / picked up ---------------------------------------------------------------
    t0, t1 = a("q2"), a("v1")
    pk = a("q2:picked") - t0
    lay = timed(blurred() + [hp(t0, upto=-29, clock="2:46")], 0, pk)
    lay += timed([svg(lobby_svg(), blur=6, opacity=0.7, depth=0.2), lena(exprs=[{"t": 0, "e": "suspicious"}], pose="ear", light="red", lookX=0.3)], pk, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("t03_pickup", t0, t1, lay, camera=cam((0, 1.1, 50, 58, "linear"), (pk - 0.01, 1.14, 50, 58, "linear"), (pk, 1.0, 50, 44, "step"),
                                                        (t1 - t0, 1.06, 50, 42, "linear")),
                   notes="She defies Gus's last order: 'Let it ring.' -> picked up."))
    # t04 the voice -----------------------------------------------------------------------------
    t0, t1 = a("v1"), a("q3")
    wh = a("v1:Whatever's") - t0
    lay = [svg(lobby_svg(), blur=8, opacity=0.6, depth=0.2), lena(exprs=[{"t": 0, "e": "scared"}, {"t": round(wh, 3), "e": "shocked"}], pose="ear", light="red"),
           text("1903 · 00:04", 800, 560, 54, "#ff6a5a", 900, font="condensed", background="#0b0d10", padding=14, radius=10, depth=0, z=60),
           glitch([(wh, 0.15, 0.4)], "v1"), vig(0.5)]
    S.append(scene("t04_voice", t0, t1, lay, camera=cam((0, 1.0, 50, 44, "linear"), (wh, 1.08, 50, 40, "linear"), (t1 - t0, 1.14, 50, 38, "linear")),
                   notes="Contradiction at ~8 s: the voice (bm_george) says the chat isn't him. Re-watch clue: only this voice says 'kid'."))
    # t05 line dead -----------------------------------------------------------------------------
    t0, t1 = a("q3"), a("q4")
    lay = desk_phone(lit=None, lcd="LINE DROPPED", lcd_color="#9fe0a6") + [vig(0.5)]
    S.append(scene("t05_dead", t0, t1, lay, camera=push(t1 - t0, 1.25, 1.28, 50, 36), trans={"type": "glitch", "duration": 0.12}))
    # t06 chat Gus ------------------------------------------------------------------------------
    t0, t1 = a("q4"), a("q5")
    lay = blurred() + [hp(t0, upto=a("q4:Gus:") + 0.01, vibrate=[{"at": 0.0, "duration": 0.4, "amount": 1}]), vig(0.4)]
    S.append(scene("t06_chat", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.12, 50, 52, None, 58)))
    # t07 Pell ----------------------------------------------------------------------------------
    t0, t1 = a("q5"), a("q6")
    lay = blurred() + [handphone({**pell_chat, "messages": msgs(pell, t0)}, clock="2:47", battery=11), vig(0.4)]
    S.append(scene("t07_pell", t0, t1, lay, camera=push(t1 - t0, 1.1, 1.16, 50, 58), trans={"type": "whip", "duration": 0.2, "direction": "left"}))
    # t08 which Gus? ----------------------------------------------------------------------------
    t0, t1 = a("q6"), a("q7")
    lay = [svg(lobby_svg(), blur=6, opacity=0.7, depth=0.2),
           lena(exprs=[{"t": 0, "e": "suspicious"}], lookX=-0.6, props={}), vig(0.5)]
    sw = a("q6:So") - t0
    lay[1]["props"]["lookX"] = -0.6
    lay.insert(2, timed([lena(exprs=[{"t": 0, "e": "angry"}], lookX=0.6)], sw, t1 - t0)[0])
    lay[1]["end"] = round(sw, 3)
    S.append(scene("t08_which", t0, t1, lay, camera=cam((0, 1.05, 46, 42, "linear"), (sw, 1.08, 54, 42, "linear"), (t1 - t0, 1.12, 50, 40, "linear"))))
    # t09 staff sheet ---------------------------------------------------------------------------
    sheet_rows = [("R. Pell (Owner) ........ 555-0178", "#1f1f1f", None), ("G. Brandt (Night) · cell ... 555-0122", "#1f1f1f", None),
                  ("Day desk ............... 555-0150", "#1f1f1f", None), ("Calloway Security ...... 555-0100", "#1f1f1f", None),
                  ("Elevator service ....... 555-0190", "#1f1f1f", None)]
    t0, t1 = a("q7"), a("q8")
    lay = paper(sheet_rows, "CALLOWAY STAFF · EMERGENCY CONTACTS", y0=640, ruled=False) + [phone_glow_dark(0.5, 0.45, 0.42, 0.8)]
    S.append(scene("t09_sheet", t0, t1, lay, camera=cam((0, 1.0, 50, 30, "linear"), (t1 - t0, 1.1, 50, 40, "out")),
                   notes="B4 outside check (HEARSE-P2 1:36): paper nobody can edit."))
    # t10 Pell's real number ---------------------------------------------------------------------
    t0, t1 = a("q8"), a("q9")
    wn = a("q8:wasn't") - t0
    lay = paper(sheet_rows, "CALLOWAY STAFF · EMERGENCY CONTACTS", y0=640, ruled=False)
    lay += [rect(540, 640, 830, 70, "rgba(255,225,77,0.45)", z=3),
            card("Texting me: Mr. Pell (Owner) · 555-0143", 1520, at=wn, size=42, bg="#2a2e36"),
            rect(540, 1520, 840, 8, RED, z=40, depth=0, start=round(wn + 0.4, 3), enter={"type": "wipeRight", "duration": 0.3}),
            phone_glow_dark(0.5, 0.55, 0.55, 0.7)]
    S.append(scene("t10_mismatch", t0, t1, lay, camera=push(t1 - t0, 1.2, 1.25, 50, 36, None, 40),
                   notes="Pays rule 5: the rule was real, the contact was swapped (555-0178 on paper vs 555-0143 texting)."))
    # t11 dial Gus ------------------------------------------------------------------------------
    t0, t1 = a("q9"), a("q10")
    dl = a("q9:dialed") - t0
    lay = timed(paper(sheet_rows, "CALLOWAY STAFF · EMERGENCY CONTACTS", y0=640, ruled=False) + [rect(540, 732, 830, 70, "rgba(255,225,77,0.45)", z=3),
                                                                                              phone_glow_dark(0.5, 0.42, 0.5, 0.7)], 0, dl)
    lay += timed(blurred() + [handphone(mode="call", call={"name": "Gus Brandt", "sub": "mobile", "label": "calling…", "at": 0.0}, clock="2:48", battery=10)], dl, t1 - t0)
    S.append(scene("t11_dial", t0, t1, lay, camera=cam((0, 1.25, 50, 40, "linear"), (dl - 0.01, 1.28, 50, 40, "linear"), (dl, 1.0, 50, 52, "step"),
                                                      (t1 - t0, 1.04, 50, 52, "linear"))))
    # t12 sync lights (split) -------------------------------------------------------------------
    t0, t1 = a("q10"), a("q11")
    lit = a("q10:lit") - t0
    left = handphone(mode="call", call={"name": "Gus Brandt", "sub": "mobile", "label": "calling…", "at": -1.0}, clock="2:48", battery=10)
    left.update({"x": 270, "y": 960, "width": 540, "height": H})
    dp = [dict(l) for l in desk_phone(lit="red", pulses=[lit, lit + 1.6], lcd="LINE 1903", lcd_color="#ff6a5a")]
    lay = [left]
    for l in dp:
        l = dict(l)
        l["x"] = 810 + (l["x"] - 540) * 0.5 if isinstance(l["x"], (int, float)) else l["x"]
        l["y"] = 960 + (l["y"] - 960) * 0.5
        for k in ("width", "height"):
            if isinstance(l.get(k), (int, float)):
                l[k] = l[k] * 0.5
        if l.get("type") == "text":
            l["fontSize"] = l["fontSize"] * 0.5
        if l.get("blur"):
            l["blur"] = l["blur"] * 0.5
        l["z"] = l.get("z", 0) + 2
        l["start"] = round(lit - 0.2, 3)
        lay.append(l)
    lay += [rect(540, 960, 8, H, "#000", z=20, depth=0), vig(0.4)]
    S.append(scene("t12_sync", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.05),
                   notes="Two lights flash together: Gus's cell rings in 1903."))
    # t13 chat lied -----------------------------------------------------------------------------
    t0, t1 = a("q11"), a("q12")
    ld = a("q11:lied") - t0
    lay = blurred() + [hp(t0, upto=a("q4:Gus:") + 0.01, clock="2:48", battery=10), stamp("NOT HOME", 560, 1140, ld, size=96), vig(0.4)]
    S.append(scene("t13_lied", t0, t1, lay, camera=push(t1 - t0, 1.05, 1.12, 50, 58)))
    # t14 rule 4 (restated for cold viewers) -----------------------------------------------------
    t0, t1 = a("q12"), a("q13")
    r4 = a("q12:Rule") - t0
    lay = keyboard() + [text("3:00 AM", 950, 430, 48, "#9fe0a6", 900, "right", depth=0, z=60, font="condensed", background="#0b0d10", padding=12, radius=8),
                        card(L.RULES[4], 1780, at=r4, size=40, z=30), vig(0.45)]
    S.append(scene("t14_rule4", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.08)))
    # t15 count + black beat ---------------------------------------------------------------------
    t0, t1 = a("q13"), a("q14")
    cts = [a("q13:Ninety-three.") - t0, a("q13:Ninety-four.") - t0, a("q13:Ninety-five.") - t0]
    bl = BY["ps1"]["start"] - t0
    lay = timed(keyboard() + [rect(540, 960, W, H, "#000", opacity=0.35, depth=0, z=20)], 0, bl)
    spots = [hook_xy(2403), hook_xy(2402), hook_xy(2401)][::-1]
    for i, (tt, n) in enumerate(zip(cts, (93, 94, 95))):
        x, y = hook_xy(101 + i)
        lay += timed([circle(x, y + 30, 40, "rgba(255,225,120,0.35)", blur=8, z=5), text(str(n), 540, 1000, 240, "#ffffff", 900, font="condensed", z=40, depth=0, strokeColor="#000", strokeWidth=8)],
                     tt, cts[i + 1] if i < 2 else bl)
    lay += timed([rect(540, 960, W, H, "#030304", depth=0, z=50), circle(700, 900, 6, "#e6c766", blur=3, z=51, depth=0)], bl, t1 - t0)
    S.append(scene("t15_count", t0, t1, lay, camera=cam((0, 1.5, 24, 78, "linear"), (bl, 1.5, 34, 78, "linear"))))
    # t16 96 + brass tag -------------------------------------------------------------------------
    t0, t1 = a("q14"), a("q16")
    tg = a("q15:nineteen-oh-three.") - t0
    kx, ky = hook_xy(1903)
    lay = keyboard(extra_at=0.0) + [text("96", 540, 1450, 260, RED, 900, font="condensed", z=40, depth=0, end=round(tg, 3), strokeColor="#000", strokeWidth=8),
                                    text("1903", kx, ky + 95, 30, "#3b2a10", 900, z=6, background=BRASS, padding=6, radius=6, start=round(tg - 0.1, 3)),
                                    vig(0.5)]
    S.append(scene("t16_96", t0, t1, lay, camera=cam((0, 1.4, 100 * kx / W, 100 * ky / H + 2, "linear"), (tg, 2.6, 100 * kx / W, 100 * (ky + 90) / H, "out"),
                                                    (t1 - t0, 2.7, 100 * kx / W, 100 * (ky + 90) / H, "linear"), shake=[(0.0, 0.2, 8)]),
                   notes="Part-1 plant paid at ~33% (key 96 on the empty hook, tag 1903)."))
    # t17 elevator waiting -----------------------------------------------------------------------
    t0, t1 = a("q16"), a("q17")
    ch = a("q16:chimed.") - t0
    lay = timed([svg(lobby_svg(), blur=4, opacity=0.8, depth=0.2), lena(exprs=[{"t": 0, "e": "terrified"}], pose="idle", lookX=0.8, light="none")], 0, ch + 0.35)
    lay += timed(elevator_view(open_at=ch + 0.4, display=[(0, "1")]), ch + 0.35, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("t17_elevator", t0, t1, lay, camera=cam((0, 1.0, 50, 44, "linear"), (ch + 0.34, 1.05, 60, 44, "linear"), (ch + 0.35, 1.0, 50, 55, "step"),
                                                          (t1 - t0, 1.1, 50, 58, "linear"))))
    # t18 triptych -------------------------------------------------------------------------------
    t0, t1 = a("q17"), a("q18")
    k1, k2, k3 = a("q17:key,") - t0, a("q17:elevator,") - t0, a("q17:owner.") - t0
    lay = [rect(540, 960, W, H, "#0a0b0e", depth=0),
           card("key 96 · tag 1903", 560, at=k1, bg="#3b2a10", size=52), card("the elevator · came down from 19", 960, at=k2, size=52),
           card("Mr. Pell: Go up now.", 1360, at=k3, bg="#2b3654", size=52),
           text("↑", 540, 1650, 200, RED, 900, z=40, depth=0, start=round(a("q17:Everything") - t0, 3), enter={"type": "slideUp", "duration": 0.3}), vig(0.4)]
    S.append(scene("t18_up", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.05)))
    # t19 visitor log ----------------------------------------------------------------------------
    log_rows = [("MON  11:40  0704  pizza", "#3b3b3b", None), ("MON  12:15  1210  locksmith", "#3b3b3b", None),
                ("MON   1:58  2302  cab", "#3b3b3b", None)]
    t0, t1 = a("q18"), a("q19")
    lay = paper(log_rows, "VISITOR LOG · NIGHT DESK", y0=560) + [phone_glow_dark(0.5, 0.5, 0.55, 0.6)]
    S.append(scene("t19_log", t0, t1, lay, camera=cam((0, 1.0, 50, 46, "linear"), (t1 - t0, 1.12, 50, 52, "linear")), trans={"type": "whip", "duration": 0.2, "direction": "up"}))
    # t20 handwriting -----------------------------------------------------------------------------
    t0, t1 = a("q19"), a("q20")
    lay = paper(log_rows, "VISITOR LOG · NIGHT DESK", y0=560)
    lay.append(text("MON   2:41  1903  called. Going up myself. Back in five. –G", 140, 836, 34, "#1b2a6b", 800, "left", z=4, maxWidth=820,
                    lineHeight=1.3, typewriter={"at": 0.1, "cps": 22}))
    lay.append(phone_glow_dark(0.5, 0.48, 0.5, 0.6))
    S.append(scene("t20_entry", t0, t1, lay, camera=push(t1 - t0, 1.35, 1.4, 50, 45, 56, 45),
                   notes="B7 paper plant: Gus went up at 2:41 (pays the Part-1 2:41 match)."))
    # t21 never signed back in --------------------------------------------------------------------
    t0, t1 = a("q20"), a("q21")
    lay = paper(log_rows + [("", "#000", None)], "VISITOR LOG · NIGHT DESK", y0=560)
    lay += [text("MON   2:41  1903  called. Going up myself. Back in five. –G", 140, 836, 34, "#1b2a6b", 800, "left", z=4, maxWidth=820, lineHeight=1.3),
            text("TIME IN:", 560, 1010, 36, "#3b3b3b", 900, "left", z=4), rect(880, 1010, 180, 60, "rgba(255,59,48,0)", stroke=RED, strokeWidth=5, z=5,
                                                                               idle=[{"type": "pulse", "amount": 0.08, "speed": 1.4}]),
            phone_glow_dark(0.6, 0.53, 0.4, 0.75)]
    S.append(scene("t21_timein", t0, t1, lay, camera=push(t1 - t0, 1.6, 1.65, 66, 53)))
    # t22 reframe ---------------------------------------------------------------------------------
    t0, t1 = a("q21"), a("q22")
    wt = a("q21:went") - t0
    lay = [svg(lobby_svg(), blur=6, opacity=0.7, depth=0.2), lena(exprs=[{"t": 0, "e": "shocked"}, {"t": round(wt, 3), "e": "angry"}], lookY=0.2),
           card(L.RULES[3], 540, at=0.2, bg="#7a1d18", size=44), vig(0.5)]
    S.append(scene("t22_reframe", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.1, 50, 44),
                   notes="B8 MIDPOINT ~51%: rule 3 inverted. 'Send nobody up' is why Gus went himself, and why nobody followed."))
    # t23 nobody ever went up ---------------------------------------------------------------------
    t0, t1 = a("q22"), a("q23")
    nb = a("q22:nobody") - t0
    lay = [rect(540, 960, W, H, "#0a0b0e", depth=0), card(L.RULES[3], 900, size=56, bg="#7a1d18"),
           comp("horror/RedText", {"text": "SEND NOBODY UP", "style": "neon", "at": round(nb, 3), "duration": 2.0, "fontSize": 96, "y": 0.68}, depth=0, z=70), vig(0.5)]
    S.append(scene("t23_nobody", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.08)))
    # t24 somebody had to go up -------------------------------------------------------------------
    t0, t1 = a("q23"), a("q24")
    sb = a("q23:Somebody") - t0
    lay = timed(blurred() + [handphone({**pell_chat, "messages": msgs(pell, t0)}, clock="2:58", battery=8)], 0, sb)
    lay += timed([svg(lobby_svg(), blur=4, opacity=0.8, depth=0.2), lena(exprs=[{"t": 0, "e": "angry"}], pose="idle", lookY=-0.2, light="none")], sb, t1 - t0)
    lay.append(vig(0.45))
    S.append(scene("t24_somebody", t0, t1, lay, camera=cam((0, 1.08, 50, 56, "linear"), (sb - 0.01, 1.12, 50, 56, "linear"), (sb, 1.0, 50, 42, "step"),
                                                          (t1 - t0, 1.05, 50, 40, "linear")),
                   notes="Ties the ascent to the owner's order (the hook's promise)."))
    # t25 4 X / 2 X ---------------------------------------------------------------------------------
    t0, t1 = a("q24"), a("q25")
    f4, el, f2 = a("q24:four.") - t0, a("q24:got") - t0, a("q24:two.") - t0
    lay = timed(keyboard(), 0, el)
    lay += [stamp("4 ✕  the 96th key", 540, 1500, f4, size=78)]
    lay += timed(elevator_view(open_at=0.0, display=[(0, "1")]), el, t1 - t0)
    lay += [stamp("2 ✕  rode it empty", 540, 1640, f2, size=78, rot=5)]
    kx, ky = hook_xy(1903)
    S.append(scene("t25_breaks", t0, t1, lay, camera=cam((0, 2.2, 100 * kx / W, 100 * ky / H + 2, "linear"), (el - 0.01, 2.2, 100 * kx / W, 100 * ky / H + 2, "linear"),
                                                        (el, 1.0, 50, 55, "step"), (t1 - t0, 1.08, 50, 58, "linear"), shake=[(f4, 0.15, 8), (f2, 0.15, 8)]),
                   notes="Rule-break ladder: each rule named with its content as it breaks."))
    # t26 6 X / 3 X ---------------------------------------------------------------------------------
    t0, t1 = a("q25"), a("q26")
    f6, f3 = a("q25:six.") - t0, a("q25:three.") - t0
    lay = lobby(lena_props={"expr": "neutral", "pose": "idle", "light": "none", "props": {}}, flicker=0.1)
    lay = [l for l in lay if l.get("name") != "horror/Protagonist"]
    lay += [stamp("6 ✕  left the desk", 540, 640, f6, size=78),
            rect(540, 960, W, H, "#000", opacity=0, depth=0, z=65, keyframes=[{"t": round(f3 - 0.05, 3), "opacity": 0}, {"t": round(f3, 3), "opacity": 0.6}]),
            stamp("3 ✕", 540, 900, f3, size=300, rot=-8), stamp("sent somebody up: me", 540, 1180, f3 + 0.15, size=64, rot=-8)]
    S.append(scene("t26_rule3", t0, t1, lay, camera=cam((0, 1.0, 50, 50, "linear"), (f3, 1.04, 50, 50, "linear"), (f3 + 0.2, 1.12, 50, 50, "out"),
                                                       (t1 - t0, 1.14, 50, 50, "linear"), shake=[(f6, 0.15, 6), (f3, 0.35, 22)]),
                   notes="The title rule is named as it breaks, biggest stamp of the ladder (the loudest hit)."))
    # t27 put the key back ---------------------------------------------------------------------------
    t0, t1 = a("q26"), a("q27")
    lay = [svg(elevator_view()[0]["markup"], blur=8, opacity=0.6, depth=0.2), hp(t0, upto=a("q26:Gus:") + 0.01, clock="3:01", battery=6, tremble=3,
                                                                                vibrate=[{"at": 0.0, "duration": 0.4, "amount": 1}]), vig(0.4)]
    S.append(scene("t27_putback", t0, t1, lay, camera=push(t1 - t0, 1.05, 1.12, 50, 58)))
    # t28 floors ------------------------------------------------------------------------------------
    t0, t1 = a("q27"), a("q28")
    f5, f9, f13, f16 = (a("q27:Five,") - t0, a("q27:nine,") - t0, a("q27:thirteen") - t0, a("q27:sixteen") - t0)
    per = (f16 - f5) / 11
    lay = [full("horror/ElevatorPanel", {"from": 5, "to": 16, "at": round(f5, 3), "perFloor": round(per, 3), "floors": 20, "target": 19,
                                         "pressed": [{"at": 0, "floor": 19}], "flicker": 0.0}),
           comp("horror/Flicker", {"strength": 0.0, "blackouts": [{"at": round(f13, 3), "duration": 0.35}]}, depth=0, z=30),
           text("No Service", 540, 1500, 64, "#ffffff", 900, background="#b3261e", padding=18, radius=14, z=40, depth=0, start=round(f16 + 0.2, 3),
                enter={"type": "pop", "duration": 0.2}),
           text("chat: delivered", 540, 1640, 44, "#9fe0a6", 800, z=40, depth=0, start=round(a("q27:chat") - t0, 3), enter={"type": "fade", "duration": 0.2}),
           vig(0.5)]
    S.append(scene("t28_floors", t0, t1, lay, camera=push(t1 - t0, 1.9, 1.95, 50, 22),
                   notes="Channel removal: lights dip at 13, signal dies at 16, only the chat still works (SIEGE-CHAT 2:03-2:11)."))
    # t29 if I'm standing up there -------------------------------------------------------------------
    t0, t1 = a("q28"), a("q29")
    lay = [svg(elevator_view()[0]["markup"], blur=8, opacity=0.6, depth=0.2), hp(t0, upto=a("q28") + 0.01, clock="3:02", battery=5, tremble=3), vig(0.45)]
    S.append(scene("t29_notme", t0, t1, lay, camera=push(t1 - t0, 1.1, 1.18, 50, 58)))
    # t30 19, doors open ------------------------------------------------------------------------------
    t0, t1 = a("q29"), a("q30")
    op = a("q29:doors") - t0
    lay = timed([full("horror/ElevatorPanel", {"from": 19, "to": 19, "at": 0, "floors": 20, "target": 19})], 0, op)
    lay += timed(hallway_1903(figure=False, gap0=0.14, flicker=0.12), op, t1 - t0)
    lay += timed([rect(270 - 0, 960, 540, H, "#646b76", depth=0, z=30, keyframes=[{"t": round(op, 3), "x": 270}, {"t": round(op + 0.7, 3), "x": -280, "ease": "inOut"}]),
                  rect(810, 960, 540, H, "#6b7280", depth=0, z=30, keyframes=[{"t": round(op, 3), "x": 810}, {"t": round(op + 0.7, 3), "x": 1360, "ease": "inOut"}])],
                 op, t1 - t0)
    lay.append(vig(0.5))
    S.append(scene("t30_nineteen", t0, t1, lay, camera=cam((0, 1.9, 50, 22, "linear"), (op - 0.01, 1.9, 50, 22, "linear"), (op, 1.0, 50, 50, "step"),
                                                          (t1 - t0, 1.15, 50, 47, "linear"))))
    # t31 PEAK (held) ----------------------------------------------------------------------------------
    t0, t1 = a("q30"), a("q31")
    h0, h1 = BY["ph1"]["start"] - t0, BY["ph1"]["end"] - t0
    bz = a("q30:blazer") - t0
    lay = hallway_1903(gap0=0.3, figure=True, flicker=0.06)
    lay[0]["props"]["flicker"] = 0.06
    lay += [comp("horror/Heartbeat", {"bpm": 60, "bpmTo": 82, "intensity": 0.6, "from": round(h0, 3)}, depth=0, z=55), vig(0.75)]
    S.append(scene("t31_peak", t0, t1, lay, camera=cam((0, 1.2, 50, 48, "linear"), (bz, 1.9, 53, 46.5, "inOut"), (h0, 2.05, 53.5, 46.5, "out"),
                                                      (h1, 2.13, 53.5, 46.5, "linear"), (t1 - t0, 2.13, 53.5, 46.5, "linear")),
                   notes=f"B9 HELD IMAGE ({h1 - h0:.1f} s, music out): the same composition as Part 1's CCTV peak, now in colour, in person, closer."))
    # t32 911 fails ------------------------------------------------------------------------------------
    t0, t1 = a("q31"), a("q32")
    fl = a("q31:failed.") - t0
    lay = [svg(elevator_view()[0]["markup"], blur=10, opacity=0.4, depth=0.2),
           handphone(mode="call", call={"name": "911", "sub": "Emergency", "label": "calling…", "at": -0.2}, clock="3:03", battery=4, tremble=4,
                     glitch_=[{"at": round(fl, 3), "duration": 0.3, "amount": 1.0}]),
           card("Call failed · No Service", 1560, at=fl, size=50, bg="#b3261e"), vig(0.5)]
    S.append(scene("t32_911", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.06), notes="B10: the outside lifeline, 4% battery, fails."))
    # t33 twist: Gus's voice -----------------------------------------------------------------------------
    t0, t1 = a("q32"), a("q33")
    lay = hallway_1903(gap0=0.3, figure=True, flicker=0.04) + [vig(0.8)]
    S.append(scene("t33_kid", t0, t1, lay, camera=push(t1 - t0, 2.13, 2.3, 53.5, 46.5),
                   notes="B11 TWIST ~86%: 'Thanks, kid. Your shift now.' in the line voice (bm_george); he never turns, no lip flap."))
    # t34 light out --------------------------------------------------------------------------------------
    t0, t1 = a("q33"), a("q34")
    ot = a("q33:out.") - t0
    lay = timed(hallway_1903(gap0=0.3, figure=True, flicker=0.04), 0, ot)
    lay += timed([rect(540, 960, W, H, "#000", depth=0, z=50), lena(exprs=[{"t": 0, "e": "terrified"}], light="phone", lookY=0.6, z=60, blink=False)], ot, t1 - t0)
    S.append(scene("t34_out", t0, t1, lay, camera=cam((0, 2.3, 53.5, 46.5, "linear"), (ot - 0.01, 2.32, 53.5, 46.5, "linear"), (ot, 1.0, 50, 50, "step"),
                                                     (t1 - t0, 1.05, 50, 48, "linear"))))
    # t35 I lied so you wouldn't come -------------------------------------------------------------------
    t0, t1 = a("q34"), a("q35")
    lay = [rect(540, 960, W, H, "#000", depth=0), hp(t0, upto=a("q34:Gus:") + 0.01, clock="3:04", battery=3, tremble=2,
                                                       vibrate=[{"at": 0.0, "duration": 0.4, "amount": 1}]), vig(0.6)]
    S.append(scene("t35_sorry", t0, t1, lay, camera=push(t1 - t0, 1.05, 1.12, 50, 58),
                   notes="Resolves the identity knot: the chat was the real Gus, lying to keep her away."))
    # t36 Marcus added, sending from me ------------------------------------------------------------------
    t0, t1 = a("q35"), a("q36")
    snd = a("q35:from#2") - t0
    ch3 = {**gus_chat, "subtitle": "3 members", "messages": msgs(handover, t0, a("q34:Gus:") + 0.01) +
           [{"kind": "system", "text": "Marcus (Day Desk) joined", "at": 0.1}]}
    lay = [rect(540, 960, W, H, "#000", depth=0),
           handphone(ch3, clock="3:04", battery=3, banners=[{"at": 0.0, "duration": 1.6, "app": "Desk Handover", "title": "Marcus joined", "text": "Desk Handover · 3 members"}]),
           comp("horror/RedText", {"text": "sending… from me", "style": "flash", "at": round(snd, 3), "duration": 1.2, "fontSize": 70, "y": 0.78}, depth=0, z=70),
           vig(0.55)]
    S.append(scene("t36_marcus", t0, t1, lay, camera=push(t1 - t0, 1.0, 1.08)))
    # t37 bookend: the rules, from Lena ------------------------------------------------------------------
    t0, t1 = a("q36"), P2.runtime
    ev = a("q36:Even") - t0
    mine = [{"me": True, "text": L.RULES[i], "at": round(0.15 * k, 3)} for k, i in enumerate((1, 2, 4, 5, 6))]
    mine.append({"me": True, "kind": "alert", "text": L.RULE3_NEW, "at": round(a("q36:If") - t0, 3)})
    ch4 = {**gus_chat, "subtitle": "3 members", "messages": mine, "draft": ""}
    lay = [rect(540, 960, W, H, "#000", depth=0), handphone(ch4, clock="3:05", battery=2),
           text("END · PART 2/2", 540, 1640, 92, "#ffffff", 900, background=RED, padding=24, radius=16, rotate=-4, z=80, depth=0,
                start=round(BY["pe1"]["start"] - t0, 3), enter={"type": "pop", "duration": 0.2}, font="display"), vig(0.5)]
    S.append(scene("t37_bookend", t0, t1, lay, camera=cam((0, 1.0, 50, 52, "linear"), (ev, 1.1, 50, 60, "linear"), (t1 - t0, 1.16, 50, 62, "linear")),
                   notes="B12 new rule from a new authority: the same six rules, sent from Lena; rule 3 rewritten. Bookends Part 1's frame-0 rule."))
    return S


# ------------------------------------------------------------------ storyboards


def storyboard(P: Part, scenes, title, holds):
    total = round(sum(s["duration"] for s in scenes), 3)
    assert abs(total - P.runtime) < 0.05, (P.key, total, P.runtime)
    voice = [{"src": f"episodes/{EP}/{P.key}/vo/{it['id']}.wav", "start": it["start"], "volume": 1, "duration": round(it["dur"], 3)}
             for it in P.items if it["kind"] == "line"]
    music, t = [], 0.0
    for hs, he in holds:
        music.append({"src": "music/dread.m4a", "start": round(t, 2), "end": round(hs, 2), "volume": 0.3, "duckTo": 0.12,
                      "fadeIn": 0.4 if t == 0 else 0.8, "fadeOut": 0.4})
        t = he
    music.append({"src": "music/dread.m4a", "start": round(t, 2), "end": round(P.runtime - 0.3, 2), "volume": 0.3, "duckTo": 0.12,
                  "fadeIn": 0.8, "fadeOut": 1.0})
    return {
        "version": 1, "id": f"{EP}-{P.key}", "title": title, "format": "9:16", "fps": 30, "scenes": scenes,
        "captions": {"words": P.captions(), "maxWords": 5, "maxChars": 18, "gapBreak": 0.25, "linger": 0.3,
                     "glue": ["Mr. Pell", "Desk Handover", "Rule three", "rule three", "Let it ring.", "Your shift now."],
                     "style": {"font": "display", "fontSize": 58, "color": "#ffffff", "highlight": "#ff4b55", "highlightMode": "none",
                               "strokeWidth": 10, "uppercase": False, "y": 0.12, "backing": 0.85}},
        "audio": {"voice": voice, "music": music, "sfx": P.sfx_cues(), "duckOn": "voice"},
        "overlays": {"grain": 0.45, "vignette": 0.3, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{EP}/build.py",
                   "timing": "Kokoro-82M on the Spark CPU, measured per line (lines.VOICES: af_heart 1.35 narrator, bm_george 1.05 the voice)",
                   "audio": f"per-line wavs: copy ~/studio/tts/{EP}/<id>.wav to studio/public/episodes/{EP}/{P.key}/vo/ on the Spark "
                            "(tts_measure.py writes them); music + sfx from studio/public (desk_ring.wav added by this episode)",
                   "components": "registered horror kit components + core layers only (the kit is locked; no unbuilt components)"},
    }


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def tables():
    for P, scenes, J, hook, contra in ((P1, p1_scenes(), jolts_p1(), ["n1", "n2"], "n2:text"), (P2, p2_scenes(), jolts_p2(), ["q1", "q2", "v1"], "v1:Whatever's")):
        st = stats(P, hook, contra, "n1" if P is P1 else "q1")
        J, jmed, jmax = jolts(P, J)
        print(f"\n# {P.key.upper()}  runtime {P.runtime}")
        print("## STATS\n" + json.dumps(st, indent=1))
        print(f"jolts {len(J)} median {jmed} max {jmax}")
        print("\n## BEATS")
        for b in P.beats:
            print(f"| {b['key']} | {mmss(b['t'])} | {100 * b['t'] / P.runtime:.0f}% | {b['title']} |")
        print("\n## LINES")
        for it in P.items:
            if it["kind"] == "line":
                who = "" if it["spk"] == "N" else "**VOICE:** "
                print(f"| {mmss(it['start'])} | {it['dur']:.2f} | {who}{it['text']} | {it['beat']} | {it['opts'].get('screen', '')} |")
            else:
                print(f"| {mmss(it['start'])} | {it['dur']:.2f} | *[silence {it['dur']} s]* | {it['beat']} | {it['opts'].get('screen', '')} |")
        print("\n## SCENES")
        t = 0
        for s in scenes:
            print(f"| {s['id']} | {t:.2f} | {t + s['duration']:.2f} | {s.get('notes', '')} |")
            t += s["duration"]
        print("\n## JOLTS")
        print(", ".join(f"{mmss(tt)} {lab}" for lab, tt in sorted(J, key=lambda x: x[1])))


if __name__ == "__main__":
    s1, s2 = p1_scenes(), p2_scenes()
    sb1 = storyboard(P1, s1, "I Broke Rule 3 of the Night Desk Handover (Part 1/2)", [(P1.by["h1"]["start"] - 0.2, P1.by["h1"]["end"] + 0.1)])
    sb2 = storyboard(P2, s2, "The Desk Phone Rang From the Empty Apartment (Part 2/2)", [(P2.by["ph1"]["start"] - 0.2, P2.by["ph1"]["end"] + 0.1)])
    tl = {}
    for P, J, hook, contra in ((P1, jolts_p1(), ["n1", "n2"], "n2:text"), (P2, jolts_p2(), ["q1", "q2", "v1"], "v1:Whatever's")):
        J, jmed, jmax = jolts(P, J)
        tl[P.key] = {"runtime": P.runtime, "beats": P.beats,
                     "items": [{k: v for k, v in it.items() if k != "opts"} | {"screen": it["opts"].get("screen", "")} for it in P.items],
                     "stats": stats(P, hook, contra, "n1" if P is P1 else "q1") | {"jolts": len(J), "jolt_median_s": jmed, "jolt_max_gap_s": jmax}}
    json.dump(tl, open(os.path.join(HERE, "timeline.json"), "w"), indent=1)
    json.dump(sb1, open(os.path.join(HERE, "storyboard.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(sb2, open(os.path.join(HERE, "storyboard_p2.json"), "w"), indent=1, ensure_ascii=False)
    if "--tables" in sys.argv:
        tables()
    print(f"p1 {P1.runtime} s {len(s1)} scenes; p2 {P2.runtime} s {len(s2)} scenes", file=sys.stderr)
