#!/usr/bin/env python3
"""horror-new-building-rules: one generator for the measured timeline, script.md and both storyboards.

Inputs (same folder)
  lines.py             spoken lines, silences, SFX, caption emphasis (single source of the narration)
  tts_durations.json   Kokoro-82M af_heart timings measured on the Spark CPU (tts_measure.py), with word timestamps
  script.tmpl.md       script.md template: {t:id} / {e:id} time tokens and <!--P1_SCRIPT--> style blocks

usage
  python3 build.py              writes script.md, storyboard.json (Part 1), storyboard_p2.json, narration_p1.md, narration_p2.md
  python3 build.py --stats      prints the pacing numbers only
  python3 build.py --voice DIR  (Spark) joins the line wavs in DIR into studio/public/episodes/<id>/p{1,2}_voice.wav

Every shot starts LEAD s before the word that names it, and every bubble, lamp, knock and card lands on a measured
word, so the picture stays in sync with the real TTS. Re-snap after the final mix by re-measuring (tts_measure.py).
Only registered horror kit components plus core rect/text/svg layers are used: the kit is locked (BRIEF 11:27 UTC),
so the three kit gaps (door lamps, a paper note, the spare-room door) are inline SVG here (tier S).
"""
from __future__ import annotations

import difflib
import json
import math
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lines as L  # noqa: E402

EP = "horror-new-building-rules"
TTS = json.load(open(os.path.join(HERE, "tts_durations.json")))["lines"]
START = {"p1": 0.15, "p2": 0.12}
LEAD = 0.1
W, H = 1080, 1920
RED = "#ff4b55"
INK = "#1d2a55"
PAPER = "#e9dfc4"
AMBER = "#f2b35a"


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def fmt(t: float) -> str:
    m = int(t // 60)
    return f"{m}:{t - 60 * m:04.1f}"


def vol(db: float) -> float:
    return round(min(2.0, 0.8 * 10 ** (db / 20)), 3)


# ============================================================== timeline
class Item:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def align(display: list[str], tts: list[tuple[str, float, float]]) -> list[tuple[str, float, float]]:
    """Map caption words (display text) onto measured TTS word times."""
    dn = [norm(w) for w in display]
    tn = [norm(w) for w, _, _ in tts]
    out: list = [None] * len(display)
    sm = difflib.SequenceMatcher(None, dn, tn, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                out[i1 + k] = (display[i1 + k], tts[j1 + k][1], tts[j1 + k][2])
        elif i2 > i1:
            if j2 > j1:
                s, e = tts[j1][1], tts[j2 - 1][2]
            else:
                s = tts[j1 - 1][2] if j1 > 0 else (tts[0][1] if tts else 0)
                e = tts[j1][1] if j1 < len(tts) else s + 0.3
            span = display[i1:i2]
            tot = sum(max(1, len(norm(x))) for x in span)
            c = s
            for k, w in enumerate(span):
                d = (e - s) * max(1, len(norm(w))) / tot
                out[i1 + k] = (w, c, c + d)
                c += d
    return out


def build_timeline(part: str):
    t = START[part]
    items, beat = [], None
    for e in L.PARTS[part]:
        if e[0] == "#":
            beat = (e[1], e[2])
            continue
        if e[0] == "~":
            _, sid, secs, opts = e
            items.append(Item(id=sid, kind="sil", start=t, end=t + secs, opts=opts, beat=beat, text="", words=[]))
            t += secs
            continue
        lid, text, opts = e
        m = TTS[lid]
        assert m["text"] == text and m["say"] == opts.get("say", text), f"tts_durations.json is stale for {lid}: rerun tts_measure.py on the Spark"
        dur = m["dur"]
        tw = [(w["w"], max(0.0, w["s"]), min(dur, w["e"])) for w in m["words"] if re.search(r"[A-Za-z0-9]", w["w"])]
        words = [(w, t + s, t + e2) for w, s, e2 in align(text.split(), tw)]
        items.append(Item(id=lid, kind="line", start=t, end=t + dur, opts=opts, beat=beat, text=text, words=words, dur=dur))
        t = t + dur + opts.get("gap", L.GAP)
    cut = items[-1].end
    return items, cut, cut + L.END_CARD


TL, CUT, TOTAL, BYID = {}, {}, {}, {}
for _p in L.PARTS:
    TL[_p], CUT[_p], TOTAL[_p] = build_timeline(_p)
    for _it in TL[_p]:
        BYID[_it.id] = _it


def at(anchor: str, off: float = 0.0) -> float:
    """'a01' line start, 'a01$' line end, 'a01@3' start of caption word 3, 'k3' silence start."""
    if "@" in anchor:
        lid, k = anchor.split("@")
        return BYID[lid].words[int(k)][1] + off
    if anchor.endswith("$"):
        return BYID[anchor[:-1]].end + off
    return BYID[anchor].start + off


def part_of(anchor: str) -> str:
    lid = re.split(r"[@$]", anchor)[0]
    for p, its in TL.items():
        if any(i.id == lid for i in its):
            return p
    raise KeyError(anchor)


# ============================================================== SVG art (kit gaps, tier S)
def wrap(text: str, n: int) -> list[str]:
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + ([cur] if cur else [])


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


NOTE_HEAD = "For whoever lives in 7C next. - D. Rowe"
NOTE_RULES = [
    ("1", "Never give anyone your unit number. Not even the building."),
    ("2", "No stairs after midnight."),
    ("3", "If your hall light goes out, stay inside until sunrise."),
    ("4", "If someone you know asks your unit, it isn't them."),
]


def torn(x0, x1, y, amp=14, step=36, seed=3):
    """Ragged edge from x0 to x1 (either direction)."""
    n = max(2, int(abs(x1 - x0) / step) + 1)
    pts, k = [], seed
    for i in range(n + 1):
        k = (k * 1103515245 + 12345) % 2 ** 31
        x = x0 + (x1 - x0) * i / n
        pts.append(f"{x:.0f},{y + (k % (2 * amp)) - amp:.0f}")
    return " ".join(pts)


def note_svg(focus: int | None = None) -> str:
    """The last tenant's note, taped under the kitchen sink, lit by the phone torch. focus = rule index to ink red."""
    rows, y = [], 640
    rows.append(f'<text x="240" y="{y}" font-family="Montserrat" font-weight="800" font-size="27" fill="{INK}">{esc(NOTE_HEAD)}</text>')
    y += 70
    for i, (n, txt) in enumerate(NOTE_RULES):
        col = "#b3121f" if (i == 0 or focus == i) else INK
        wt = 900 if focus == i else 700
        for j, ln in enumerate(wrap(txt, 27)):
            lab = f"{n}. " if j == 0 else "    "
            rows.append(f'<text x="240" y="{y}" font-family="Montserrat" font-weight="{wt}" font-size="36" fill="{col}">{esc(lab + ln)}</text>')
            y += 54
        y += 18
    paper_bottom = y + 10
    lines_svg = "".join(f'<line x1="230" x2="850" y1="{yy}" y2="{yy}" stroke="#9fb3d1" stroke-width="2" opacity="0.6"/>' for yy in range(660, paper_bottom, 54))
    return (
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
        '<defs><radialGradient id="torch" cx="0.5" cy="0.42" r="0.6"><stop offset="0" stop-color="#fff6dc" stop-opacity="0.22"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
        f'<rect width="{W}" height="{H}" fill="#1b1512"/>'
        '<rect x="0" y="0" width="1080" height="420" fill="#2b211b"/>'
        '<rect x="120" y="1250" width="70" height="680" fill="#5c6168"/><rect x="120" y="1240" width="300" height="70" rx="30" fill="#6b7078"/>'
        '<rect x="760" y="1300" width="60" height="640" fill="#4c5157"/>'
        f'<g transform="rotate(-2 540 900)">'
        f'<polygon points="210,560 870,560 870,{paper_bottom} {torn(870, 210, paper_bottom, seed=7)}" fill="{PAPER}"/>'
        f'<polygon points="{torn(210, 870, paper_bottom, seed=7)} 870,{paper_bottom + 40} 210,{paper_bottom + 40}" fill="#1b1512" opacity="0"/>'
        + lines_svg + "".join(rows)
        + '<rect x="420" y="530" width="240" height="60" fill="#d8d3b8" opacity="0.75" transform="rotate(3 540 560)"/>'
        '</g>'
        f'<rect width="{W}" height="{H}" fill="url(#torch)"/>'
        '</svg>'
    )


def rule_card_svg(n: str, txt: str, torn_only: bool = False) -> str:
    """Close-up strip of the note: one rule, big (replaces the black rule cards; no hand-lettered font is installed)."""
    body = ""
    if torn_only:
        body = (f'<text x="140" y="905" font-family="Montserrat" font-weight="700" font-size="58" fill="{INK}" opacity="0.9">5. If</text>'
                f'<rect x="300" y="860" width="420" height="44" fill="{INK}" opacity="0.18"/>')
        bottom = 960
    else:
        ys = 820
        body += f'<text x="90" y="{ys + 10}" font-family="Montserrat" font-weight="900" font-size="120" fill="#b3121f">{n}.</text>'
        for j, ln in enumerate(wrap(txt, 19)):
            body += f'<text x="250" y="{ys + j * 84}" font-family="Montserrat" font-weight="800" font-size="62" fill="{INK}">{esc(ln)}</text>'
        bottom = ys + 84 * len(wrap(txt, 19)) + 40
    return (
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
        f'<rect width="{W}" height="{H}" fill="#0d0b0a"/>'
        f'<polygon points="{torn(40, 1040, 700, amp=10, seed=2)} 1040,{bottom} {torn(1040, 40, bottom, amp=22 if torn_only else 10, seed=5)}" fill="{PAPER}"/>'
        + "".join(f'<line x1="40" x2="1040" y1="{yy}" y2="{yy}" stroke="#9fb3d1" stroke-width="3" opacity="0.5"/>' for yy in range(780, bottom - 20, 84))
        + body + '</svg>'
    )


def slip_svg() -> str:
    return (
        f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="#0b0a0a"/>'
        f'<polygon points="{torn(110, 970, 700, amp=20, seed=11)} 970,1180 110,1180" fill="{PAPER}" transform="rotate(2 540 940)"/>'
        '<line x1="110" x2="970" y1="840" y2="840" stroke="#9fb3d1" stroke-width="3" opacity="0.5"/>'
        '<line x1="110" x2="970" y1="960" y2="960" stroke="#9fb3d1" stroke-width="3" opacity="0.5"/>'
        '<line x1="110" x2="970" y1="1080" y2="1080" stroke="#9fb3d1" stroke-width="3" opacity="0.5"/></svg>'
    )


# hallway geometry, copied from kit HallArt (studio/src/kits/horror/backgrounds.tsx) so the overlays sit on its doors
def hall_at(d):
    return dict(xl=420 * d, xr=1080 - 420 * d, yc=700 * d, yf=1920 - 910 * d)


DOORS = {  # unit -> (depth pair index, side). The near pair sits outside the lens ring, so the visible four are the apartments.
    "7A": (1, 0), "7D": (1, 1), "7B": (2, 0), "7E": (2, 1),
}
DOOR_D = [(0.08, 0.3), (0.48, 0.62), (0.74, 0.82)]


def door_geom(unit):
    i, side = DOORS[unit]
    d0, d1 = DOOR_D[i]
    a, b = hall_at(d0), hall_at(d1)
    ha, hb = a["yf"] - a["yc"], b["yf"] - b["yc"]
    x0 = a["xr"] if side else a["xl"]
    x1 = b["xr"] if side else b["xl"]
    top0, top1 = a["yc"] + ha * 0.28, b["yc"] + hb * 0.28
    return dict(x0=x0, x1=x1, top0=top0, top1=top1, bot0=a["yf"], bot1=b["yf"], scale=1 - d0, xm=(x0 + x1) / 2, topm=(top0 + top1) / 2)


def lamp_svg(unit, on=True) -> str:
    g = door_geom(unit)
    s = g["scale"]
    cx, cy = g["xm"], g["topm"] - 38 * s
    r = 30 * s + 7
    glow = ""
    if on:
        glow = (f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * 6:.0f}" fill="url(#lg)"/>'
                f'<polygon points="{g["x0"]:.0f},{g["top0"]:.0f} {g["x1"]:.0f},{g["top1"]:.0f} {g["x1"]:.0f},{g["bot1"]:.0f} {g["x0"]:.0f},{g["bot0"]:.0f}" fill="{AMBER}" opacity="0.13"/>')
    fix = f'<rect x="{cx - r:.0f}" y="{cy - r * 0.55:.0f}" width="{2 * r:.0f}" height="{r * 1.1:.0f}" rx="{r * 0.4:.0f}" fill="{"#ffd58a" if on else "#2a2722"}" stroke="#0c0b0d" stroke-width="{max(2, 5 * s):.0f}"/>'
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="lg"><stop offset="0" stop-color="{AMBER}" stop-opacity="0.55"/>'
            f'<stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient></defs>{glow}{fix}</svg>')


def hall_static_svg() -> str:
    """Unit plates on the four visible doors, and a green EXIT sign over the end door (the stairwell)."""
    out = []
    for unit in ("7A", "7B", "7D", "7E"):
        g = door_geom(unit)
        s = g["scale"]
        out.append(f'<text x="{g["xm"]:.0f}" y="{g["topm"] + 70 * s:.0f}" text-anchor="middle" font-family="Montserrat" font-weight="800" font-size="{40 * s + 10:.0f}" fill="#cbbf9f" opacity="0.8">{unit}</text>')
    out.append('<rect x="508" y="752" width="64" height="24" rx="3" fill="#2fbf71"/><text x="540" y="770" text-anchor="middle" font-family="Montserrat" font-weight="900" font-size="17" fill="#06210f">EXIT</text>')
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{"".join(out)}</svg>'


def ajar_svg(unit="7A") -> str:
    """The door swung inward a crack: a black gap along its far edge with the lit edge of the door leaf beside it."""
    g = door_geom(unit)
    f = 0.55
    xa = g["x0"] + (g["x1"] - g["x0"]) * f
    ta = g["top0"] + (g["top1"] - g["top0"]) * f
    ba = g["bot0"] + (g["bot1"] - g["bot0"]) * f
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'<polygon points="{xa:.0f},{ta:.0f} {g["x1"]:.0f},{g["top1"]:.0f} {g["x1"]:.0f},{g["bot1"]:.0f} {xa:.0f},{ba:.0f}" fill="#000000"/>'
            f'<polygon points="{xa - 9:.0f},{ta - 3:.0f} {xa + 3:.0f},{ta:.0f} {xa + 3:.0f},{ba:.0f} {xa - 9:.0f},{ba + 3:.0f}" fill="#b49a7c"/>'
            f'<polygon points="{xa:.0f},{ba:.0f} {g["x1"]:.0f},{g["bot1"]:.0f} {g["x1"] + 30:.0f},{g["bot1"] + 40:.0f} {xa - 40:.0f},{ba + 60:.0f}" fill="#000000" opacity="0.6"/></svg>')


PEEP_C, PEEP_R = (540, 900), 470


def ring_svg() -> str:
    cx, cy = PEEP_C
    r = PEEP_R
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="pv" cx="0.5" cy="0.5" r="0.5">'
            '<stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.85"/></radialGradient></defs>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#pv)"/>'
            f'<path fill-rule="evenodd" fill="#050506" d="M0,0H{W}V{H}H0Z M{cx - r},{cy} a{r},{r} 0 1,0 {2 * r},0 a{r},{r} 0 1,0 -{2 * r},0Z"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 8}" fill="none" stroke="#141215" stroke-width="22"/>'
            f'<ellipse cx="{cx - 150}" cy="{cy - 250}" rx="120" ry="50" fill="#fff" opacity="0.06" transform="rotate(-25 {cx - 150} {cy - 250})"/></svg>')


def crouch_svg() -> str:
    """Head and shoulders pressed to the door, ear first, rising into the bottom of the lens."""
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            '<path d="M250 1420 Q300 1210 470 1180 Q520 1060 640 1080 Q760 1100 760 1230 Q850 1260 880 1420 Z" fill="#040405"/>'
            '<path d="M600 1150 Q640 1120 668 1160 Q676 1200 640 1215" fill="none" stroke="#2a2a30" stroke-width="10"/>'
            '<path d="M470 1180 Q520 1070 640 1082" fill="none" stroke="#3b3326" stroke-width="5" opacity="0.7"/></svg>')


def spare_door_svg(light: bool) -> str:
    """Interior door of the locked spare room: no peephole, no chain, a keyed knob, a light gap at the floor."""
    gap = ('<rect x="300" y="1648" width="480" height="12" fill="#ffe2a8"/>'
           '<polygon points="300,1660 780,1660 900,1920 180,1920" fill="#ffd27a" opacity="0.16"/>') if light else '<rect x="300" y="1648" width="480" height="12" fill="#07070a"/>'
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="#1e222b"/>'
            '<rect y="1660" width="1080" height="260" fill="#171416"/>'
            '<rect x="270" y="300" width="540" height="1365" fill="#c9c2b2" opacity="0.18"/>'
            '<rect x="300" y="330" width="480" height="1318" fill="#3d3330" stroke="#0c0b0d" stroke-width="7"/>'
            '<rect x="350" y="400" width="380" height="520" fill="none" stroke="#2a221f" stroke-width="10"/>'
            '<rect x="350" y="1010" width="380" height="560" fill="none" stroke="#2a221f" stroke-width="10"/>'
            '<circle cx="720" cy="1000" r="26" fill="#a9a59c" stroke="#0c0b0d" stroke-width="5"/><rect x="714" y="992" width="12" height="18" rx="3" fill="#2a2722"/>'
            f'{gap}</svg>')


def paper_slip_svg() -> str:
    return '<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg"><polygon points="0,10 200,0 196,110 6,120" fill="#e9dfc4"/><line x1="20" x2="170" y1="50" y2="48" stroke="#1d2a55" stroke-width="6"/><line x1="20" x2="130" y1="78" y2="77" stroke="#1d2a55" stroke-width="6"/></svg>'


def members_svg(highlight: bool) -> str:
    rows = [("Building Office", "", "#3a3f4a", False), ("Dale", "8A", "#8f6a4a", False), ("Mrs. Kowal", "7A", "#7a5c8f", False),
            ("Odette", "3B", "#4f7a73", False), ("Priya", "7B", "#4a628f", False), ("Tess", "7E", "#8f4a55", False),
            ("June (you)", "7C", "#5a6f8f", True), ("D. Rowe", "7C", "#2b2b2b", True)]
    out = ['<rect x="120" y="360" width="840" height="1280" rx="40" fill="#14171d" stroke="#2b3240" stroke-width="4"/>',
           '<text x="180" y="450" font-family="Montserrat" font-weight="800" font-size="40" fill="#e8eaee">Members</text>',
           '<text x="900" y="450" text-anchor="end" font-family="Montserrat" font-weight="700" font-size="30" fill="#8b93a3">38</text>']
    y = 540
    for name, unit, col, seven_c in rows:
        out.append(f'<circle cx="215" cy="{y}" r="42" fill="{col}"/>')
        out.append(f'<text x="290" y="{y + 12}" font-family="Montserrat" font-weight="800" font-size="38" fill="#e8eaee">{esc(name)}</text>')
        if unit:
            out.append(f'<text x="900" y="{y + 12}" text-anchor="end" font-family="Montserrat" font-weight="900" font-size="38" fill="{RED if (highlight and seven_c) else "#8b93a3"}">{unit}</text>')
        if name == "D. Rowe":
            out.append(f'<circle cx="245" cy="{y + 30}" r="13" fill="#2fbf71" stroke="#14171d" stroke-width="5"/>')
            out.append(f'<text x="290" y="{y + 52}" font-family="Montserrat" font-weight="700" font-size="26" fill="#2fbf71">online</text>')
        if highlight and seven_c:
            out.append(f'<rect x="150" y="{y - 58}" width="780" height="118" rx="22" fill="none" stroke="{RED}" stroke-width="6"/>')
        y += 132
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{"".join(out)}</svg>'


def photo_frame_svg(label: str) -> str:
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
            f'<path fill-rule="evenodd" fill="#f1f1ee" d="M90,330H990V1610H90Z M120,360H960V1520H120Z"/>'
            f'<text x="130" y="1580" font-family="Montserrat" font-weight="800" font-size="38" fill="#3a3a3a">{esc(label)}</text></svg>')


# ============================================================== layer helpers
def full(name, props=None, **kw):
    lay = {"type": "component", "name": name, "props": props or {}}
    lay.update(kw)
    return lay


def ov(name, z=50, **props):
    return {"type": "component", "name": name, "depth": 0, "z": z, "props": props}


def svgl(markup, z=10, **kw):
    lay = {"type": "svg", "markup": markup, "x": "50%", "y": "50%", "width": W, "height": H, "z": z}
    lay.update(kw)
    return lay


def protagonist(exprs, pose="phone", x="50%", w=1000, look=(0, 0.5), light="phone", **kw):
    p = {"pose": pose, "exprs": exprs, "lookX": look[0], "lookY": look[1]}
    if light:
        p["light"] = light
    lay = {"type": "component", "name": "horror/Protagonist", "x": x, "y": "100%", "anchorY": 1, "width": w, "height": round(w * 1.52), "props": p}
    lay.update(kw)
    return lay


VIG = ov("horror/Vignette", 50, amount=0.4)


# ============================================================== chats
MEMBERS = {
    "Building Office": {"color": "#3a3f4a", "initials": "BO"},
    "Odette 3B": {"color": "#4f7a73", "initials": "O"},
    "Odette": {"color": "#4f7a73", "initials": "O"},
    "Dale 8A": {"color": "#8f6a4a", "initials": "D"},
    "Mrs. Kowal 7A": {"color": "#7a5c8f", "initials": "K"},
    "Priya 7B": {"color": "#4a628f", "initials": "P"},
    "Sam 7D": {"color": "#6b7a4a", "initials": "S"},
    "Tess 7E": {"color": "#8f4a55", "initials": "T"},
    "Marco 2F": {"color": "#5a5a7a", "initials": "M"},
    "D. Rowe": {"color": "#2b2b2b", "initials": "DR"},
}

CHATS = {
    "res": {"title": "Harrow Court Residents", "count": 38, "dayLabel": "Today 5:12 AM", "msgs": [
        ("a01", -60, {"from": "Marco 2F", "text": "whoever keeps propping the lobby door open, please stop"}),
        ("a01", -59, {"from": "Odette 3B", "text": "Package room opens at 9 tomorrow."}),
        ("a01", -0.6, {"from": "Building Office", "kind": "alert", "text": "Night check. Please reply with your unit number so we know you're home."}),
        ("a04@4", 0, {"from": "Odette 3B", "text": "We don't have a building office. The super lives in 1A."}),
        ("a10@0", 0, {"from": "Dale 8A", "text": "taking the stairs down to find this \"office\" lol"}),
        ("a10@0", 0.6, {"from": "Marco 2F", "text": "😂"}),
        ("a10@0", 1.0, {"from": "Priya 7B", "text": "prank??"}),
        ("a10@0", 1.45, {"from": "Sam 7D", "text": "who even is this"}),
        ("a12", 0.05, {"from": "Building Office", "text": "Dale. Your lease renews in 11 days. The stairs are fine."}),
        ("a16", 0.0, {"from": "Building Office", "kind": "alert", "text": "Reminder: the note under the sink is out of date. Please reply."}),
        ("a18@1", 0, {"from": "Odette 3B", "text": "Nobody answer it."}),
        ("a19@4", 0, {"from": "Mrs. Kowal 7A", "text": "7A. sorry i like rules"}),
        ("a21@1", 0, {"from": "Priya 7B", "text": "7B"}),
        ("a21@2", 0, {"from": "Sam 7D", "text": "7D"}),
        ("a21@3", 0, {"from": "Tess 7E", "text": "7E"}),
        ("a24", 0.1, {"from": "Mrs. Kowal 7A", "text": "June, please reply. It's fine."}),
        ("a26", 0.0, {"from": "Priya 7B", "text": "June, please reply. It's fine."}),
    ], "typing": [("a11", "a12", "Building Office")]},
    "dm": {"title": "Building Office", "dm": "Building Office", "dayLabel": "Today 5:38 AM", "msgs": [
        ("a29", -0.15, {"from": "Building Office", "text": "Every unit on floor 7 has replied except one."}),
    ], "typing": []},
    "odette": {"title": "Odette", "dm": "Odette", "subtitle": "text message", "dayLabel": "Today 5:45 AM", "msgs": [
        ("b04$", -0.1, {"me": True, "text": "Are you outside my door?"}),
        ("b05", 0.0, {"from": "Odette", "text": "Bathtub. Floor 3. That's not me."}),
        ("b06", 0.0, {"from": "Odette", "text": "Typing it marks you. Saying it opens."}),
    ], "typing": [("b04$", "b05", "Odette")]},
    "rowe": {"title": "D. Rowe", "dm": "D. Rowe", "subtitle": "online", "dayLabel": "Today 5:57 AM", "msgs": [
        ("b21@4", 0.0, {"me": True, "text": "Are you in my spare room?"}),
        ("b22@3", 0.0, {"from": "D. Rowe", "text": "Don't answer it. Not even to me."}),
    ], "typing": [("b22", "b22@3", "D. Rowe")]},
}


def chat_state(key, s0, s1):
    c = CHATS[key]
    msgs = []
    for anc, off, m in c["msgs"]:
        t = at(anc, off) if not (isinstance(off, (int, float)) and off < -30) else at(anc) + off
        if t <= s1 - 0.05:
            mm = dict(m)
            mm["at"] = round(t - s0, 3)
            msgs.append(mm)
    typing = [{"from": f, "at": round(at(a) - s0, 3), "until": round(at(b) - s0, 3)} for a, b, f in c["typing"] if at(a) < s1 and at(b) > s0]
    return msgs, typing


def phone_chat(key, s0, s1, clock, tremble=1.5, glitch=None, unread=None):
    c = CHATS[key]
    msgs, typing = chat_state(key, s0, s1)
    chat = {"title": c["title"], "messages": msgs, "dayLabel": c["dayLabel"], "accent": "#3d5a80", "clock": clock,
            "battery": 23, "theme": "dark", "scale": 1.25}
    if "count" in c:
        chat["count"] = c["count"]
    if c.get("dm"):
        chat["dm"] = c["dm"]
        chat["subtitle"] = c.get("subtitle", "private message")
    if typing:
        chat["typing"] = typing
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": 0.61, "tilt": -3, "tremble": tremble, "side": "right",
         "phone": {"members": MEMBERS, "mode": "chat", "chat": chat}, "thumbY": 0.94, "thumbReach": 0.1}
    if glitch:
        p["glitch"] = glitch
    return {"type": "component", "name": "horror/HandPhone", "props": p}


def phone_lock(time, notifs, s0, vibrate=None):
    p = {"phoneWidth": 0.68, "cx": 0.53, "cy": 0.61, "tilt": -3, "tremble": 2, "side": "right", "thumbY": 0.94, "thumbReach": 0.1,
         "phone": {"members": MEMBERS, "mode": "lock", "lock": {"time": time, "date": "Sunday",
                                                                 "notifications": [{"at": round(at(a, o) - s0, 3), "app": app, "title": ti, "text": tx} for a, o, app, ti, tx in notifs]}}}
    if vibrate:
        p["phone"]["vibrate"] = [{"at": round(at(vibrate) - s0, 3), "duration": 0.5, "amount": 1}]
    return {"type": "component", "name": "horror/HandPhone", "props": p}


# ============================================================== shot builders
# each returns (background, layers, camera_extra, desc, kit) given scene start s0 and end s1
def B_chat(s0, s1, key, clock, set_="door", tremble=1.5, glitch_at=None, desc="", feet=False):
    bg_layer = (full("horror/FrontDoor", {"hallLight": 0.85, "chain": "on", "feet": feet}, depth=0.2, blur=5) if set_ == "door"
                else full("horror/LivingRoom", {"lamp": 0.35, "tv": "off"}, depth=0.2, blur=5))
    g = [{"at": round(at(glitch_at) - s0, 3), "duration": 0.22, "amount": 0.8}] if glitch_at else None
    layers = [bg_layer, phone_chat(key, s0, s1, clock, tremble, g), VIG]
    if g:
        layers.append(ov("horror/Glitch", 60, cues=[{"at": g[0]["at"], "duration": 0.25, "amount": 0.9}], seed=f"g{int(s0 * 10)}"))
    return {"type": "color", "color": "#0b0d12"}, layers, {}, desc, "HandPhone chat over a blurred set"


def B_lock(s0, s1, time, notifs, vibrate=None, set_="living", desc=""):
    bg_layer = full("horror/LivingRoom", {"lamp": 0.2, "tv": "off"}, depth=0.2, blur=6) if set_ == "living" else full("horror/FrontDoor", {"hallLight": 0.6, "chain": "on"}, depth=0.2, blur=6)
    return {"type": "color", "color": "#0b0d12"}, [bg_layer, phone_lock(time, notifs, s0, vibrate), VIG], {}, desc, "HandPhone lock screen"


def B_note(s0, s1, desc=""):
    return {"type": "color", "color": "#1b1512"}, [svgl(note_svg(0), z=1), ov("horror/Darkness", 50, x=0.5, y=0.45, radius=0.62, darkness=0.35)], {}, desc, "inline SVG note (kit gap) under a torch pool"


def B_rule(s0, s1, n, txt, faint=None, desc="", torn_only=False):
    layers = [svgl(rule_card_svg(n, txt, torn_only), z=1)]
    if faint:
        layers.insert(0, full(faint[0], faint[1], opacity=0.12, depth=0.1))
    layers.append(ov("horror/Vignette", 50, amount=0.55))
    return {"type": "color", "color": "#0d0b0a"}, layers, {"punch": True}, desc, "note close-up strip (inline SVG)"


def B_char(s0, s1, exprs, pose="phone", set_="living", look=(0, 0.5), light="phone", dark=0.3, glitch_at=None, desc="", w=1000):
    ex = [{"t": round(max(0.0, at(a) - s0), 3), "e": e} for a, e in exprs]
    bg = ({"type": "component", "name": "horror/LivingRoom", "depth": 0.25, "props": {"lamp": 0.3, "tv": "off"}} if set_ == "living"
          else {"type": "component", "name": "horror/FrontDoor", "depth": 0.25, "props": {"hallLight": 0.7, "chain": "on", "dark": 0.35}})
    layers = [protagonist(ex, pose, look=look, light=light, w=w), ov("horror/Darkness", 50, x=0.5, y=0.55, radius=0.55, darkness=dark), VIG]
    if glitch_at:
        layers.append(ov("horror/Glitch", 60, cues=[{"at": round(at(glitch_at) - s0, 3), "duration": 0.25, "amount": 0.9}], seed=f"c{int(s0 * 10)}"))
    return bg, layers, {}, desc, "Protagonist (June) over a set"


def B_peep(s0, s1, lamps, extra=None, chips=None, dark_steps=None, desc="", figure_svg=None, zoom_to=None):
    """Fake peephole: kit Hallway + inline lamp/plate overlays at the same scale, then a ring mask (the kit Peephole hardcodes its hall)."""
    sc = 1.1
    layers = [full("horror/Hallway", {"flicker": 0.05, "lights": 2, "endDoor": True}, x="50%", y="50%", width=W, height=H, scale=sc, depth=1, z=0),
              svgl(hall_static_svg(), z=2, scale=sc)]
    for unit, off_t, on_t in lamps:   # off_t / on_t absolute (None = never)
        a = None if off_t is None else round(off_t - s0, 3)
        b = None if on_t is None else round(on_t - s0, 3)
        if a is not None and a <= 0 and (b is None or b <= 0):
            layers.append(svgl(lamp_svg(unit, False), z=3, scale=sc))
            continue
        lay_on = svgl(lamp_svg(unit, True), z=3, scale=sc)
        lay_off = svgl(lamp_svg(unit, False), z=3, scale=sc)
        if a is not None and a > 0:
            lay_on["end"] = a
            lay_off["start"] = a
            layers += [lay_on, lay_off]
        elif b is not None and b > 0:
            lay_off["end"] = b
            lay_on["start"] = b
            layers += [lay_off, lay_on]
        else:
            layers.append(lay_on)
    for mk, start in (extra or []):
        lay = svgl(mk, z=4, scale=sc)
        if start is not None:
            lay["start"] = round(max(0.0, start - s0), 3)
        layers.append(lay)
    if dark_steps:
        kf = [{"t": 0, "opacity": dark_steps[0][1]}]
        for t, o in dark_steps[1:]:
            tt = round(max(0.05, t - s0), 3)
            kf += [{"t": max(0.0, tt - 0.05), "opacity": kf[-1]["opacity"]}, {"t": tt, "opacity": o, "ease": "step"}]
        layers.append({"type": "rect", "x": "50%", "y": "50%", "width": W, "height": H, "fill": "#000000", "opacity": dark_steps[0][1], "z": 5, "keyframes": kf})
    if figure_svg:
        layers.append(svgl(figure_svg, z=6))
    layers.append(svgl(ring_svg(), z=20, depth=0))
    for text, t in (chips or []):
        layers.append({"type": "text", "text": text, "x": "50%", "y": 1260, "fontSize": 64, "color": "#e8eaee", "background": "#2b3a55", "padding": 18, "radius": 26,
                       "depth": 0, "z": 30, "start": round(t - s0, 3), "end": round(min(s1 - s0, t - s0 + 0.7), 3), "enter": {"type": "pop", "duration": 0.18}})
    layers.append(ov("horror/Flicker", 40, strength=0.12, seed=f"p{int(s0 * 10)}"))
    cam = {"zoom_to": zoom_to} if zoom_to else {}
    return {"type": "color", "color": "#050506"}, layers, cam, desc, "fake peephole: kit Hallway + inline lamp overlays + ring mask"


def B_door(s0, s1, knocks=(), chain="on", hall=0.8, feet=False, handle=None, dark=0.2, sit=None, desc="", knock_y=1160, extra=None, hall_track=None):
    p = {"hallLight": hall_track if hall_track else hall, "chain": chain, "dark": dark, "knocks": [round(at(a, o) - s0, 3) for a, o in knocks], "knockY": knock_y}
    if feet:
        p["feet"] = feet if not isinstance(feet, tuple) else [round(at(feet[0]) - s0, 3), 99]
    if handle:
        p["handle"] = [{"at": round(at(handle) - s0, 3), "duration": 0.5}]
    layers = []
    if sit:
        layers.append(protagonist([{"t": 0, "e": sit}], "sit", look=(0.5, 0), light=None, w=1000))
    layers += [ov("horror/Darkness", 50, x=0.5, y=0.6, radius=0.6, darkness=0.3), VIG]
    for lay in extra or []:
        layers.append(lay)
    cam = {"shake": [{"at": round(at(a, o) - s0, 3), "duration": 0.16, "amplitude": 12} for a, o in knocks]}
    return {"type": "component", "name": "horror/FrontDoor", "depth": 0.25, "props": p}, layers, cam, desc, "FrontDoor"


def B_spare(s0, s1, light_on=None, light_off=None, slip=None, knocks=(), desc="", zoom=None):
    layers = []
    on_t = None if light_on is None else at(light_on) - s0
    off_t = None if light_off is None else at(light_off[0], light_off[1]) - s0
    if on_t is None or on_t <= 0:
        lay = svgl(spare_door_svg(True), z=1)
        if off_t is not None:
            lay["end"] = round(off_t, 3)
            l2 = svgl(spare_door_svg(False), z=1, start=round(off_t, 3))
            layers += [lay, l2]
        else:
            layers.append(lay)
    else:
        layers += [svgl(spare_door_svg(False), z=1, end=round(on_t, 3)), svgl(spare_door_svg(True), z=1, start=round(on_t, 3))]
    if slip:
        t0 = round(at(slip) - s0, 3)
        layers.append({"type": "svg", "markup": paper_slip_svg(), "x": 540, "y": 1650, "width": 220, "height": 132, "z": 3, "start": t0, "opacity": 1,
                       "keyframes": [{"t": t0, "x": 560, "y": 1655, "rotate": 0}, {"t": t0 + 1.1, "x": 470, "y": 1790, "rotate": -9, "ease": "out"}]})
    layers += [ov("horror/Darkness", 50, x=0.5, y=0.8, radius=0.6, darkness=0.35), VIG]
    cam = {"shake": [{"at": round(at(a, o) - s0, 3), "duration": 0.18, "amplitude": 16} for a, o in knocks]}
    if zoom:
        cam["zoom"] = zoom
    return {"type": "color", "color": "#1e222b"}, layers, cam, desc, "spare-room door (inline SVG, kit gap)"


def B_stairs(s0, s1, label, desc=""):
    return ({"type": "component", "name": "horror/Stairwell", "depth": 0.2, "props": {"floor": "6", "flicker": 0.2, "exit": True}},
            [svgl(photo_frame_svg(label), z=10, depth=0), ov("horror/Vignette", 50, amount=0.3)], {}, desc, "Stairwell floor 6 inside a photo frame")


def B_members(s0, s1, hl_at, desc=""):
    t = round(at(hl_at) - s0, 3)
    return ({"type": "color", "color": "#07080b"},
            [svgl(members_svg(False), z=1, end=t), svgl(members_svg(True), z=1, start=t), VIG], {}, desc, "member list (inline SVG panel)")


def B_slip(s0, s1, red_at, desc=""):
    t1 = round(at("b28") - s0, 3)
    layers = [svgl(slip_svg(), z=1),
              {"type": "text", "text": "I never left 7C.", "x": "50%", "y": 820, "fontSize": 78, "font": "body", "weight": 800, "color": INK, "z": 5,
               "typewriter": {"at": t1, "cps": 26}, "start": 0},
              {"type": "text", "text": "Whatever knocks, it isn't me.", "x": "50%", "y": 960, "fontSize": 66, "font": "body", "weight": 800, "color": INK, "z": 5, "maxWidth": 860,
               "typewriter": {"at": round(at("b28@4") - s0, 3), "cps": 30}, "start": 0},
              ov("horror/RedText", 60, text="IT ISN'T ME", at=round(at(red_at) - s0, 3), style="scrawl", fontSize=150, y=0.3),
              ov("horror/Vignette", 50, amount=0.5)]
    return {"type": "color", "color": "#0b0a0a"}, layers, {"punch": True}, desc, "slip close-up (inline SVG + text typewriter) + RedText"


def B_black(s0, s1, desc="", text=None):
    layers = [ov("horror/Flicker", 40, strength=0.0, seed="bk")]
    if text:
        layers.append({"type": "text", "text": text, "x": "50%", "y": "50%", "fontSize": 60, "color": "#8b93a3", "z": 5})
    return {"type": "color", "color": "#000000"}, layers, {}, desc, "black"


def B_hall_dark(s0, s1, desc=""):
    return ({"type": "component", "name": "horror/Hallway", "depth": 0.2, "props": {"flicker": 0.6, "lights": 1, "endDoor": True}},
            [ov("horror/Darkness", 50, x=0.5, y=0.45, radius=0.3, darkness=0.85), VIG], {}, desc, "Hallway, lights 1, Darkness")


def B_end(s0, s1, rule, frm, label, desc=""):
    return ({"type": "color", "color": "#07070a"},
            [ov("horror/EndCard", 80, rule=rule, sub="is typing…", label=label, at=0, stampAt=0.6, **{"from": frm})], {}, desc, "EndCard (bookend)")


# ============================================================== shot lists
def lamps_p1():
    off = {"7A": at("a20$", -0.05), "7B": at("a21@1"), "7D": at("a21@2"), "7E": at("a21@3")}
    return off


def P1_SHOTS():
    off = lamps_p1()
    lamp_rows = lambda: [(u, off[u], None) for u in ("7A", "7B", "7D", "7E")]
    return [
        ("a01", B_chat, dict(key="res", clock="5:12", feet=True, desc="COVER. Residents chat, red Building Office alert 'Night check. Please reply with your unit number...'; blurred front door with a feet shadow under it"), True),
        ("a02", B_note, dict(desc="The last tenant's note taped under the sink in the phone torch: header 'For whoever lives in 7C next. - D. Rowe', rules 1-4, torn bottom; rule 1 in red"), True),
        ("a03", B_rule, dict(n="1", txt=NOTE_RULES[0][1], desc="Close-up strip: '1. Never give anyone your unit number. Not even the building.'"), True),
        ("a04", B_chat, dict(key="res", clock="5:13", glitch_at="a04$", desc="Odette 3B: 'We don't have a building office. The super lives in 1A.' Glitch on the line end"), True),
        ("a05", B_char, dict(exprs=[("a05", "suspicious")], desc="June on the sofa, phone light, suspicious"), True),
        ("a06", B_rule, dict(n="2", txt=NOTE_RULES[1][1], faint=("horror/Stairwell", {"floor": "7"}), desc="Strip: '2. No stairs after midnight.' (stairwell ghosted behind)"), True),
        ("a07", B_rule, dict(n="3", txt=NOTE_RULES[2][1], faint=("horror/Hallway", {"lights": 3}), desc="Strip: '3. If your hall light goes out, stay inside until sunrise.'"), True),
        ("a08", B_rule, dict(n="4", txt=NOTE_RULES[3][1], desc="Strip: '4. If someone you know asks your unit, it isn't them.'"), True),
        ("a09", B_rule, dict(n="5", txt="", torn_only=True, desc="Strip: the ragged torn bottom edge, the top of a '5. If' just visible"), True),
        ("a10", B_chat, dict(key="res", clock="5:14", desc="Dale 8A: 'taking the stairs down to find this \"office\" lol', then 3 quick reactions (😂 / prank?? / who even is this)"), True),
        ("a11", B_chat, dict(key="res", clock="5:14", tremble=2, desc="Header: 'Building Office is typing…'"), False),
        ("a12", B_chat, dict(key="res", clock="5:14", tremble=2.5, glitch_at="a12@1", desc="Building Office: 'Dale. Your lease renews in 11 days. The stairs are fine.'"), True),
        ("a13", B_char, dict(exprs=[("a13", "worried")], look=(0.5, 0.3), desc="June, worried, eyes toward the door"), True),
        ("a14", B_peep, dict(lamps=[(u, None, None) for u in ("7A", "7B", "7D", "7E")], desc="Peephole: corridor, four apartment doors (7A 7B 7D 7E) each with a lit amber lamp; far pair = EXIT stairwell + TRASH, no lamps"), True),
        ("a15", B_lock, dict(time="5:25", notifs=[("a15", 0.2, "Harrow Court Residents", "Building Office", "New message")], vibrate="a15", desc="Lock screen 5:25, banner 'Building Office · New message'"), True),
        ("a16", B_chat, dict(key="res", clock="5:25", tremble=2, desc="Building Office alert: 'Reminder: the note under the sink is out of date. Please reply.'"), True),
        ("a17", B_char, dict(exprs=[("a17", "scared"), ("a17@7", "shocked")], glitch_at="a17@7", desc="June: scared, then shocked on 'me' (glitch)"), True),
        ("a18", B_chat, dict(key="res", clock="5:26", desc="Odette 3B: 'Nobody answer it.'"), True),
        ("a19", B_chat, dict(key="res", clock="5:26", desc="Mrs. Kowal 7A: '7A. sorry i like rules' (lowercase)"), True),
        ("a20", B_peep, dict(lamps=lamp_rows(), dark_steps=[(0, 0.0), (off["7A"], 0.12)], desc="Peephole: the lamp over 7A (nearest left) clicks out on 'out'"), True),
        ("a21", B_peep, dict(lamps=lamp_rows(), dark_steps=[(0, 0.12), (off["7B"], 0.22), (off["7D"], 0.32), (off["7E"], 0.42)],
                             chips=[("7B", off["7B"]), ("7D", off["7D"]), ("7E", off["7E"])], desc="Peephole: lamps 7B, 7D, 7E die on each spoken unit; a reply chip pops for each"), True),
        ("a23", B_hall_dark, dict(desc="Dark hall, one flickering ceiling light; knocking (three at a time) from the far end"), True),
        ("a24", B_chat, dict(key="res", clock="5:33", tremble=2.5, desc="Mrs. Kowal 7A, now in sentence case: 'June, please reply. It's fine.'"), True),
        ("a26", B_chat, dict(key="res", clock="5:33", tremble=3, glitch_at="a26", desc="Priya 7B: 'June, please reply. It's fine.' word for word"), True),
        ("a27", B_peep, dict(lamps=lamp_rows(), dark_steps=[(0, 0.42)], extra=[(ajar_svg("7A"), at("a27@4"))], zoom_to=("30%", "52%", 1.6),
                             desc="P1 PEAK (held ~4 s, slow push into the lens): every lamp dark; 7A's door stands open a crack, black inside"), True),
        ("a28", B_lock, dict(time="5:38", notifs=[("a28", 0.15, "Harrow Court Residents", "Building Office (private)", "Message")], vibrate="a28", desc="Lock screen 5:38, private message banner, buzz"), True),
        ("a29", B_chat, dict(key="dm", clock="5:38", tremble=3, desc="DM from Building Office: 'Every unit on floor 7 has replied except one.'"), True),
        ("a30", B_spare, dict(light_on="a30@9", desc="Behind her: the locked spare-room door; the gap under it lights up on 'light'"), True),
        ("a31", B_door, dict(sit="scared", hall=0.6, desc="June on the floor at the front door, chain on, hands on the chain"), True),
        ("k1", B_door, dict(knocks=[("k1", 0.0)], hall=0.5, feet=True, knock_y=820, desc="Close door: knock 1, feet shadow, rattle"), True),
        ("k2", B_char, dict(exprs=[("k2", "terrified")], pose="cover", set_="door", light=None, desc="June, hands over mouth"), True),
        ("k3", B_door, dict(knocks=[("k3", 0.0)], hall=0.5, feet=True, handle="k3", knock_y=820, desc="Knock 3, handle jiggle; HARD CUT on the knock"), True),
    ]


def P2_SHOTS():
    return [
        ("b01", B_door, dict(knocks=[("b01", 0.02)], hall=0.8, feet=True, knock_y=820, desc="COVER. Front door, hall light on, a feet shadow, impact marks of the third knock still settling"), True),
        ("b02", B_door, dict(hall=0.8, feet=True, knock_y=820, handle="b02@1", desc="Closer on the door; the lever jiggles on 'Which unit'"), True),
        ("b04", B_chat, dict(key="odette", clock="5:45", set_="door", tremble=2.5, desc="Texts to Odette (not the chat): 'Are you outside my door?' then typing dots 0.5 s"), True),
        ("b05", B_chat, dict(key="odette", clock="5:45", set_="door", tremble=3, glitch_at="b05@4", desc="Odette: 'Bathtub. Floor 3. That's not me.' then 'Typing it marks you. Saying it opens.'"), True),
        ("b07", B_peep, dict(lamps=[(u, 0.0, None) for u in ("7A", "7B", "7D", "7E")], dark_steps=[(0, 0.42)], desc="Peephole: the four dark lamps (7A 7B 7D 7E)"), True),
        ("b03", B_rule, dict(n="4", txt=NOTE_RULES[3][1], desc="Strip: '4. If someone you know asks your unit, it isn't them.'"), True),
        ("b08", B_door, dict(knocks=[("b08", 0.0), ("b08", 0.32), ("b08", 0.64)], hall=0.8, feet=True, knock_y=820, desc="Three knocks, the voice changes"), True),
        ("b09", B_char, dict(exprs=[("b09", "scared")], pose="sit", set_="door", look=(0.7, 0), light=None, desc="June on the floor, staring at the door"), True),
        ("b10", B_stairs, dict(label="Dale 8A · 5:16 AM", desc="Dale's photo 1: stairwell landing '6'"), True),
        ("b10@8", B_stairs, dict(label="Dale 8A · 5:19 AM", desc="Photo 2: the same landing '6'"), True),
        ("b10@10", B_stairs, dict(label="Dale 8A · 5:23 AM", desc="Photo 3: the same landing '6'"), True),
        ("b11", B_rule, dict(n="2", txt=NOTE_RULES[1][1], faint=("horror/Stairwell", {"floor": "6"}), desc="Strip: '2. No stairs after midnight.'"), True),
        ("b12", B_spare, dict(desc="The spare-room door behind her, light on underneath; slow push"), True),
        ("b13", B_spare, dict(zoom=True, desc="Closer on the keyed knob: locked, owner's storage"), False),
        ("b14", B_members, dict(hl_at="b14@6", desc="Chat member list: two rows read 7C, both ringed red: 'June (you)' and 'D. Rowe · online'"), True),
        ("b16", B_char, dict(exprs=[("b16", "shocked")], glitch_at="b16", desc="June, shocked"), True),
        ("b19", B_lock, dict(time="5:55", notifs=[], set_="door", desc="Lock screen 5:55, no notifications"), True),
        ("b20", B_door, dict(knocks=[("b20", 0.0), ("b20", 0.3), ("b20", 0.6), ("b20@5", 0.0), ("b20@5", 0.3), ("b20@5", 0.6), ("b20@7", 0.0), ("b20@7", 0.3), ("b20@7", 0.6)],
                             hall_track=[{"t": 0, "v": 0.8}], feet=True, knock_y=820, desc="Three bursts of three knocks: Kowal's voice, the super's, my mother's"), True),
        ("b21", B_chat, dict(key="rowe", clock="5:57", set_="door", tremble=3, desc="DM to D. Rowe: 'Are you in my spare room?'"), True),
        ("b22", B_chat, dict(key="rowe", clock="5:57", set_="door", tremble=3, desc="D. Rowe, instantly: 'Don't answer it. Not even to me.'"), True),
        ("b17", B_peep, dict(lamps=[(u, 0.0, None) for u in ("7A", "7B", "7D", "7E")], dark_steps=[(0, 0.5)], desc="Peephole: the dark hall, nobody standing"), True),
        ("b18", B_peep, dict(lamps=[(u, 0.0, None) for u in ("7A", "7B", "7D", "7E")], dark_steps=[(0, 0.5)], figure_svg=crouch_svg(),
                             desc="P2 PEAK (held ~4.8 s): low in the lens, a head pressed ear-first to the door; heartbeat, no VO for 2 s"), True),
        ("b23", B_door, dict(hall=0.8, feet=True, desc="Front door, handle still, feet shadow; captions '7C? 7C?'"), True),
        ("b24", B_char, dict(exprs=[("b24", "terrified")], pose="cover", set_="door", light=None, desc="June biting her sleeve, hands over mouth"), True),
        ("b25", B_lock, dict(time="6:01", notifs=[], set_="door", desc="Lock 6:01"), True),
        ("b25@3", B_lock, dict(time="6:02", notifs=[], set_="door", desc="Lock 6:02"), False),
        ("b25@8", B_lock, dict(time="6:04", notifs=[], set_="door", desc="Lock 6:04"), True),
        ("b26", B_door, dict(hall=1.0, feet=False, dark=0.0, desc="Front door: warm light under it, the shadow gone"), True),
        ("b26@3", B_peep, dict(lamps=[("7A", None, None), ("7B", 0.0, None), ("7D", 0.0, None), ("7E", 0.0, None)], dark_steps=[(0, 0.3)], extra=[(ajar_svg("7A"), None)], zoom_to=("30%", "45%", 1.4),
                               desc="Peephole: 7A's lamp back on (door still ajar), 7B 7D 7E dark"), True),
        ("b27", B_spare, dict(slip="b27@5", desc="Spare-room door: a slip of paper slides out from the lit gap on 'slid'"), True),
        ("b28", B_slip, dict(red_at="b28@7", desc="The slip: 'I never left 7C.' / 'Whatever knocks, it isn't me.' typed on; RedText 'IT ISN'T ME' (the episode's one red scrawl)"), True),
        ("q2", B_black, dict(desc="Black, 0.7 s silence"), False),
        ("b29", B_spare, dict(knocks=[("k4", 0.0), ("k4", 0.45), ("k4", 0.9)], light_off=("k4", 0.9), desc="Spare-room door from her side: three knocks from inside, the gap goes dark on the third; HARD CUT"), True),
    ]


ENDS = {
    "p1": ("REPLY.", "Building Office", "PART 2", "End card (bookend of frame 0): Building Office bubble 'REPLY.' + 'is typing…', stamp PART 2"),
    "p2": ("7C?", "Building Office", "2/2", "End card (bookend of the cold open's question): Building Office bubble '7C?' + 'is typing…', stamp 2/2"),
}


# ============================================================== scenes, captions, audio
def ensure_holds(scene, maxgap=2.8):
    """Slow linear push with intermediate keyframes, so no stretch is > maxgap s without a visual event."""
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
    from pipeline.episodes.common import visual_events  # noqa: E402
    d = scene["duration"]
    cam = scene.setdefault("camera", {})
    if not cam.get("keyframes"):
        z1 = 1.0 + min(0.06, 0.012 * d)
        cam["keyframes"] = [{"t": 0.0, "zoom": 1.0, "ease": "linear"}, {"t": round(d, 3), "zoom": round(z1, 4), "ease": "linear"}]
    for _ in range(20):
        ev = visual_events(scene)
        gaps = [(b - a, a, b) for a, b in zip(ev, ev[1:])]
        g, a, b = max(gaps)
        if g <= maxgap:
            break
        t = round((a + b) / 2, 3)
        kf = cam["keyframes"]
        k0 = max((k for k in kf if k["t"] <= t), key=lambda k: k["t"])
        k1 = min((k for k in kf if k["t"] >= t), key=lambda k: k["t"])
        z = k0["zoom"] + (k1["zoom"] - k0["zoom"]) * ((t - k0["t"]) / max(1e-6, k1["t"] - k0["t"]))
        kf.append({"t": t, "zoom": round(z, 4), "ease": "linear"})
        kf.sort(key=lambda k: k["t"])


def build_scenes(part):
    shots = P1_SHOTS() if part == "p1" else P2_SHOTS()
    starts = []
    for i, (anc, *_r) in enumerate(shots):
        s = 0.0 if i == 0 else max(starts[-1] + 0.3, at(anc) - LEAD)
        assert i == 0 or at(anc) - LEAD > starts[-1] - 0.01, f"{part}: shot {anc} is out of order"
        starts.append(round(s, 3))
    cut = CUT[part]
    bounds = starts + [round(cut, 3)]
    scenes, rows = [], []
    for i, (anc, fn, kw, jolt) in enumerate(shots):
        s0, s1 = bounds[i], bounds[i + 1]
        kw = dict(kw)
        desc = kw.pop("desc", "")
        zoom = kw.pop("zoom", None) if fn is B_spare else None
        res = fn(s0, s1, **kw) if fn is not B_spare else fn(s0, s1, zoom=zoom, **kw)
        bg, layers, cam_extra, desc2, kit = res
        sc = {"id": f"{part}_{i:02d}", "duration": round(s1 - s0, 3), "background": bg, "layers": layers, "notes": desc or desc2}
        cam = {}
        if cam_extra.get("shake"):
            cam["shake"] = cam_extra["shake"]
        if cam_extra.get("punch"):
            d = s1 - s0
            cam["keyframes"] = [{"t": 0.0, "zoom": 1.08, "ease": "linear"}, {"t": 0.12, "zoom": 1.0, "ease": "out"}, {"t": round(d, 3), "zoom": round(1.0 + 0.015 * d, 4), "ease": "linear"}]
        if cam_extra.get("zoom"):
            d = s1 - s0
            cam["keyframes"] = [{"t": 0.0, "zoom": 1.0, "x": "50%", "y": "50%", "ease": "linear"}, {"t": round(d, 3), "zoom": 1.35, "x": "64%", "y": "52%", "ease": "inOut"}]
        if cam_extra.get("zoom_to"):
            zx, zy, zz = cam_extra["zoom_to"]
            d = s1 - s0
            cam["keyframes"] = [{"t": 0.0, "zoom": 1.0, "x": "50%", "y": "50%", "ease": "linear"},
                                {"t": round(min(d, 2.4), 3), "zoom": zz, "x": zx, "y": zy, "ease": "inOut"},
                                {"t": round(d, 3), "zoom": round(zz * 1.02, 3), "x": zx, "y": zy, "ease": "linear"}]
        if cam:
            sc["camera"] = cam
        if fn in (B_rule, B_slip, B_members) or (i > 0 and fn is not shots[i - 1][1] and fn in (B_peep,)):
            sc["transitionIn"] = {"type": "cut", "duration": 0.0}
        if fn is B_black or anc in ("a30", "b12", "b27"):
            sc["transitionIn"] = {"type": "dipBlack", "duration": 0.24}
        ensure_holds(sc)
        scenes.append(sc)
        rows.append((s0, s1, fn.__name__[2:], desc or desc2, kit, jolt, sc))
    rule, frm, label, desc = ENDS[part]
    bg, layers, _c, _d, kit = B_end(cut, TOTAL[part], rule, frm, label)
    sc = {"id": f"{part}_end", "duration": round(TOTAL[part] - cut, 3), "background": bg, "layers": layers, "notes": desc}
    ensure_holds(sc)
    scenes.append(sc)
    rows.append((cut, TOTAL[part], "end", desc, kit, True, sc))
    return scenes, rows


def captions(part):
    words = []
    for it in TL[part]:
        if it.kind != "line":
            continue
        emph = {norm(w) for w in it.opts.get("emph", [])}
        for w, s, e in it.words:
            d = {"text": w, "start": round(s, 3), "end": round(max(e, s + 0.05), 3)}
            if norm(w) in emph:
                d["emph"] = True
            words.append(d)
    return {"enabled": True, "words": words, "maxWords": 6, "maxChars": 20, "gapBreak": 0.25,
            "glue": ["building office", "unit number", "spare room", "hall light", "member list", "lease date"],
            "style": {"font": "display", "fontSize": 58, "color": "#ffffff", "highlight": RED, "highlightMode": "none",
                      "strokeWidth": 10, "uppercase": False, "y": 0.12, "backing": 0.85}}


def sfx_cues(part):
    cues = []
    for it in TL[part]:
        for cue, off, db in it.opts.get("sfx", []):
            if off == "end":
                t = it.end
            elif isinstance(off, str) and off.startswith("@"):
                t = it.words[int(off[1:])][1]
            else:
                t = it.start + off
            cues.append({"cue": cue, "at": round(max(0.0, t), 3), "volume": vol(db)})
    return sorted(cues, key=lambda c: c["at"])


def music_end(part):
    for it in TL[part]:
        if it.kind == "sil" and it.opts.get("music_stop"):
            return it.start
    return CUT[part]


def storyboard(part):
    scenes, rows = build_scenes(part)
    sb = {
        "version": 1, "id": f"{EP}-{part}",
        "title": {"p1": "Never Give Anyone Your Unit Number (Part 1/2)", "p2": "Someone Else Lives In My Apartment (Part 2/2)"}[part],
        "format": "9:16", "fps": 30, "scenes": scenes, "captions": captions(part),
        "audio": {"voice": [{"src": f"episodes/{EP}/{part}_voice.wav", "start": 0, "volume": 1, "duration": round(CUT[part], 3)}],
                  "music": [{"src": "music/dread.m4a", "start": 0, "end": round(music_end(part), 3), "volume": 0.3, "duckTo": 0.12, "fadeOut": 0.4}],
                  "sfx": sfx_cues(part), "duckOn": "voice"},
        "overlays": {"grain": 0.5, "vignette": 0.35, "fadeIn": 0, "fadeOut": 0},
        "_built": {"by": f"backlog/horror/{EP}/build.py", "timing": "Kokoro-82M af_heart measured on the Spark CPU (tts_durations.json)",
                   "audio": f"studio/public/episodes/{EP}/{part}_voice.wav is built on the Spark by build.py --voice (line wavs laid on this timeline)"},
    }
    return sb, rows


# ============================================================== stats + script.md
NUM_RE = re.compile(r"\d")


def stats(part):
    its = TL[part]
    lines_ = [i for i in its if i.kind == "line"]
    words = sum(len(i.text.split()) for i in lines_)
    speech = sum(i.dur for i in lines_)
    total = TOTAL[part]
    first10 = sum(1 for i in lines_ for w, s, e in i.words if s < 10)
    nums = sum(1 for i in lines_ for w in i.text.split() if NUM_RE.search(w))
    _, rows = storyboard(part)
    jolts = [r[0] for r in rows if r[5]]
    gaps = [b - a for a, b in zip(jolts, jolts[1:])]
    return dict(words=words, speech=speech, total=total, cut=CUT[part], wpm_spoken=words / speech * 60, wpm_overall=words / total * 60,
                first10=first10, nums_per_min=nums / total * 60, jolts=jolts, jolt_median=statistics.median(gaps), jolt_max=max(gaps),
                scenes=len(rows))


def narration_block(part):
    """Narration in pipeline/audio/script.py syntax. [speed] is sticky there, so every override is reset;
    a short silence that carries a knock becomes `[sfx: knock wait]` (the cue holds the narration)."""
    out, para = [], []
    cur_speed = L.SPEED
    first = True

    def flush():
        if para:
            out.append(" ".join(para))
            para.clear()

    def tag(c, of, db, wait=False):
        o = f" @{of}" if isinstance(of, (int, float)) and of else ""
        return f"[sfx: {c}{o}{' vol=' + str(db) if db else ''}{' wait' if wait else ''}]"

    for it in TL[part]:
        if it.kind == "sil":
            secs = it.end - it.start
            if it.opts.get("music_stop"):
                para.append("[music: stop]")
            sfx = it.opts.get("sfx", [])
            if sfx and secs <= 0.7 and len(sfx) == 1:
                para.append(tag(sfx[0][0], 0, sfx[0][2], wait=True))
            else:
                para += [tag(c, of, db) for c, of, db in sfx] + [f"[pause: {secs:.2f}]"]
            continue
        o = it.opts
        tags = []
        if first:
            tags.append("[music: dread]")
            first = False
        sp = o.get("speed", L.SPEED)
        special = sp != L.SPEED or "vox" in o
        if special or sp != cur_speed:
            flush()
        if sp != cur_speed:
            tags.append(f"[speed: {sp}]")
            cur_speed = sp
        if "vox" in o:
            tags.append(f"[vox: {o['vox']}]")
        words = o.get("say", it.text).split()
        inline = {}
        pre = []
        for c, of, db in o.get("sfx", []):
            if of == "end":
                continue
            if isinstance(of, str) and of.startswith("@"):
                k = int(of[1:]) if "say" not in o else round(int(of[1:]) * len(words) / max(1, len(it.text.split())))
                inline.setdefault(min(k, len(words) - 1), []).append(tag(c, 0, db))
            else:
                pre.append(tag(c, of, db))
        body = " ".join((" ".join(inline[k]) + " " if k in inline else "") + w for k, w in enumerate(words))
        post = " ".join(tag(c, 0, db) for c, of, db in o.get("sfx", []) if of == "end")
        para.append(" ".join(x for x in [" ".join(tags), " ".join(pre), body, post] if x))
        if special or o.get("gap", L.GAP) >= 0.2:
            flush()
            if special and sp != L.SPEED and False:
                pass
    flush()
    return "\n\n".join(out) + " [cut]"


def timed_script(part):
    out, beat = [], None
    shots = {round(r[0], 2): r for r in storyboard(part)[1]}
    for it in TL[part]:
        if it.beat != beat:
            beat = it.beat
            out.append(f"\n**[{beat[1]}]**\n")
        if it.kind == "sil":
            what = ", ".join(c for c, _, _ in it.opts.get("sfx", [])) or "room tone"
            extra = " Music out." if it.opts.get("music_stop") else ""
            extra += " HARD CUT at the end." if it.opts.get("cut") else ""
            out.append(f"- `{fmt(it.start)}-{fmt(it.end)}` silence ({it.end - it.start:.2f} s): {what}.{extra}")
            continue
        say = f" (TTS: \"{it.opts['say']}\")" if "say" in it.opts else ""
        out.append(f"- `{fmt(it.start)}-{fmt(it.end)}` VO: {it.text}{say}")
    return "\n".join(out)


def shot_table(part):
    _, rows = storyboard(part)
    out = ["| # | t_start | t_end | shot | visual (kit vocabulary) | camera | SFX in window |", "|---|---|---|---|---|---|---|"]
    cues = sfx_cues(part)
    for k, (s0, s1, kind, desc, kit, jolt, sc) in enumerate(rows):
        cam = sc.get("camera", {})
        cm = []
        if cam.get("shake"):
            cm.append(f"shake x{len(cam['shake'])}")
        kf = cam.get("keyframes", [])
        if kf:
            cm.append(f"zoom {kf[0].get('zoom', 1):.2f}->{kf[-1].get('zoom', 1):.2f}")
        sf = ", ".join(f"{c['cue']} {c['at']:.1f}" for c in cues if s0 <= c["at"] < s1)
        out.append(f"| {k + 1} | {s0:.2f} | {s1:.2f} | {kind}{' (jolt)' if jolt else ''} | {desc} [{kit}] | {', '.join(cm) or 'static'} | {sf or '-'} |")
    return "\n".join(out)


def pacing(part):
    s = stats(part)
    pct = lambda t: f"{t / s['total'] * 100:.0f}%"
    if part == "p1":
        extra = [
            f"- Hook: line 1 is {len(BYID['a01'].text.split())} words / {BYID['a01'].end - BYID['a01'].start:.1f} s with the threat in frame 0 (Building Office alert + feet shadow under the door). The trusted source is contradicted by the note at {at('a02@9'):.1f} s ('never') and again by Odette at {at('a04@4'):.1f} s (PLAYBOOK cap 11 s).",
            f"- Words in the first 10 s: {s['first10']} (PLAYBOOK median 43.5).",
            f"- Rules list: {at('a06'):.1f}-{BYID['a09'].end:.1f} s = {BYID['a09'].end - at('a06'):.1f} s ({(BYID['a09'].end - at('a06')) / s['total'] * 100:.0f}% of runtime; target <= 10 s). Rule 1 is already stated in the hook.",
            f"- Midpoint turn ('It meant me.') at {at('a17'):.1f} s ({pct(at('a17'))}). Peak image (7A ajar, held {BYID['h1'].end - at('a27'):.1f} s) at {at('a27'):.1f} s ({pct(at('a27'))}). Target narrowed at {at('a29'):.1f} s ({pct(at('a29'))}); the inside threat (spare-room light) at {at('a30'):.1f} s; hard cut at {s['cut']:.1f} s ({pct(s['cut'])}).",
        ]
    else:
        extra = [
            f"- Cold hook: a knock on frame 0, Odette's voice by {at('b01@5'):.1f} s, the forbidden question 'Which unit is this?' at {at('b02'):.1f} s. Her own text falsifies the voice at {at('b05'):.1f} s ('Bathtub. Floor 3. That's not me.'). The mechanic is stated in 7 words by {BYID['b06'].end:.1f} s, and the premise for cold viewers (four units gave the number, four lights out; rule four) by {BYID['b03'].end:.1f} s.",
            f"- Words in the first 10 s: {s['first10']}.",
            f"- Part 1 plant paid (Dale on the stairs, rule two) at {at('b10'):.1f} s ({pct(at('b10'))}). Turn (7C twice in the member list) at {at('b14'):.1f} s ({pct(at('b14'))}). Peak image held {BYID['h2'].end - at('b18'):.1f} s from {at('b18'):.1f} s ({pct(at('b18'))}). Clock {at('b19'):.1f}-{BYID['b25'].end:.1f} s. Twist (the torn-off end slides out at sunrise) at {at('b27'):.1f} s ({pct(at('b27'))}); cut at {s['cut']:.1f} s ({pct(s['cut'])}).",
        ]
    return "\n".join([
        f"- {s['words']} words; {s['speech']:.1f} s of speech -> {s['wpm_spoken']:.0f} wpm spoken (PLAYBOOK narrated band 230-270); {s['wpm_overall']:.0f} wpm over the full {s['total']:.1f} s including timed silences and the {L.END_CARD:.1f} s end card. Kokoro af_heart speed {L.SPEED} (1.0-1.2 on the knock lines), measured on the Spark CPU, not estimated.",
        f"- Runtime {s['total']:.1f} s (cut at {s['cut']:.1f} s): above the 61 s Creator Rewards floor and inside the PLAYBOOK Shorts band (50-100 s).",
        *extra,
        f"- Jolts (shot changes that carry a new anomaly, rule, number or notification): {len(s['jolts'])}; median gap {s['jolt_median']:.1f} s, longest {s['jolt_max']:.1f} s (Shorts target 2.5-3.5 s, never > 8 s). {s['scenes']} shots.",
        f"- Numbers per minute: {s['nums_per_min']:.1f} (clock times and unit codes; above the 3-5 target, which the unit-number mechanic needs; spoken times are spelled out for Kokoro).",
    ])


def write_all():
    tmpl = open(os.path.join(HERE, "script.tmpl.md")).read()
    rep = {
        "<!--P1_SCRIPT-->": timed_script("p1"), "<!--P2_SCRIPT-->": timed_script("p2"),
        "<!--P1_NARR-->": "```narration\n" + narration_block("p1") + "\n```", "<!--P2_NARR-->": "```narration\n" + narration_block("p2") + "\n```",
        "<!--P1_SHOTS-->": shot_table("p1"), "<!--P2_SHOTS-->": shot_table("p2"),
        "<!--P1_PACING-->": pacing("p1"), "<!--P2_PACING-->": pacing("p2"),
    }
    for k, v in rep.items():
        tmpl = tmpl.replace(k, v)
    s1, s2 = stats("p1"), stats("p2")
    tmpl = tmpl.replace("{W1}", str(s1["words"])).replace("{W2}", str(s2["words"]))
    tmpl = tmpl.replace("{R1}", f"{s1['total']:.1f}").replace("{R2}", f"{s2['total']:.1f}")
    tmpl = tmpl.replace("{WPM1}", f"{s1['wpm_spoken']:.0f}").replace("{WPM2}", f"{s2['wpm_spoken']:.0f}")
    tmpl = tmpl.replace("{WPMO1}", f"{s1['wpm_overall']:.0f}").replace("{WPMO2}", f"{s2['wpm_overall']:.0f}")
    tmpl = re.sub(r"\{t:([A-Za-z0-9@$]+)\}", lambda m: fmt(at(m.group(1))), tmpl)
    tmpl = re.sub(r"\{e:([A-Za-z0-9]+)\}", lambda m: fmt(BYID[m.group(1)].end), tmpl)
    open(os.path.join(HERE, "script.md"), "w").write(tmpl)
    for part in ("p1", "p2"):
        sb, _ = storyboard(part)
        name = "storyboard.json" if part == "p1" else f"storyboard_{part}.json"
        json.dump(sb, open(os.path.join(HERE, name), "w"), ensure_ascii=False)
        open(os.path.join(HERE, f"narration_{part}.md"), "w").write(
            f"---\nid: {EP}-{part}\nniche: horror\nvoice: {L.VOICE}\nspeed: {L.SPEED}\nmusic: dread\n---\n\n"
            f"Pipeline input for pipeline/audio (it reads only the first narration block of a file, so each part has its own).\n\n```narration\n{narration_block(part)}\n```\n")
    print("wrote script.md, storyboard.json (Part 1), storyboard_p2.json, narration_p1.md, narration_p2.md")


def build_voice(wav_dir):
    import wave
    import numpy as np
    root = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
    dst_dir = os.path.join(root, "studio", "public", "episodes", EP)
    os.makedirs(dst_dir, exist_ok=True)
    SR = 24000
    for part in ("p1", "p2"):
        buf = np.zeros(int((TOTAL[part] + 0.5) * SR), dtype=np.float32)
        for it in TL[part]:
            if it.kind != "line":
                continue
            with wave.open(os.path.join(wav_dir, f"{it.id}.wav")) as w:
                a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
            g = 10 ** (it.opts.get("vox", 0) / 20)
            i0 = int(it.start * SR)
            buf[i0:i0 + len(a)] += a[: len(buf) - i0] * g
        out = os.path.join(dst_dir, f"{part}_voice.wav")
        with wave.open(out, "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((np.clip(buf, -1, 1) * 32767).astype("<i2").tobytes())
        print("wrote", out, f"{len(buf) / SR:.1f} s")


if __name__ == "__main__":
    if "--stats" in sys.argv:
        for p in ("p1", "p2"):
            s = stats(p)
            print(p, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in s.items() if k != "jolts"})
    elif "--voice" in sys.argv:
        build_voice(sys.argv[sys.argv.index("--voice") + 1])
    else:
        write_all()
