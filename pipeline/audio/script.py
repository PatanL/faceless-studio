"""Turn a script file into narration segments + timed markers.

Accepted input (.md or .txt):
- Optional YAML-ish front matter between `---` lines. Keys read here (all optional):
  niche, voice, speed, music. Everything else is ignored.
- Narration source, first match wins:
  1. a fenced block ```narration ... ``` (or ```vo```),
  2. a section headed `## Narration` / `## Script` / `## VO` / `## Voiceover` (until the next `## `),
  3. lines that start with `VO:` or `NARRATOR:`,
  4. otherwise the whole body.
  Markdown headings, tables, HTML comments, list bullets that look like notes (`- note:`),
  and **bold** / _italic_ markers are stripped.
- Blank lines separate paragraphs (a pause is inserted between them).
- Inline markers (case-insensitive), placed where they should happen:
    [sfx: knock3]            cue at the next spoken word (or end of segment)
    [sfx: knock3 @+0.3 vol=-2]  offset seconds, level dB relative to the default
    [sfx: knock3_slow wait]  play it, and hold the narration until it has finished
    [pause: 0.8]             silence in seconds
    [music: dread]           choose the music bed (anywhere; last one wins)
    [music: none]            no music bed
    [vox: -4]                voice gain (dB) for this paragraph (quiet, close passages: gives the mix dynamics)
    [speed: 1.15]            TTS speed from this paragraph on (e.g. slow the last 20 s down)
    [sfx: knock3_slow hush=0.5]  also pull the music bed to near silence for 0.5 s before the cue
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

MARK = re.compile(r"\[(sfx|pause|music|vox|speed)\s*:\s*([^\]]+)\]", re.I)


@dataclass
class Marker:
    kind: str                # sfx | pause
    word_index: int          # index into the segment's word list where it fires
    name: str = ""
    seconds: float = 0.0     # pause length or sfx offset
    db: float = 0.0          # sfx level offset
    hush: float = 0.0        # sfx: seconds of near-silent music bed before the cue


@dataclass
class Segment:
    text: str                # narration text with markers removed
    words: list[str]
    markers: list[Marker] = field(default_factory=list)
    gain_db: float = 0.0     # [vox: dB]
    speed: float | None = None  # [speed: x] (sticky: applies to later paragraphs too)


@dataclass
class Script:
    meta: dict
    segments: list[Segment]
    music: str | None = None   # None = niche default, "" = none


def _front_matter(src: str):
    meta = {}
    if src.startswith("---"):
        end = src.find("\n---", 3)
        if end != -1:
            for line in src[3:end].splitlines():
                m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", line)
                if m and not line.startswith((" ", "\t")):
                    meta[m.group(1).lower()] = m.group(2).strip("'\"")
            src = src[end + 4:]
    return meta, src


def _narration(body: str) -> str:
    m = re.search(r"```(?:narration|vo)\s*\n(.*?)```", body, re.S | re.I)
    if m:
        return m.group(1)
    m = re.search(r"^##+\s*(narration|script|vo|voice ?over)\b.*?$\n(.*?)(?=^##\s|\Z)", body, re.S | re.I | re.M)
    if m:
        return m.group(2)
    vo = re.findall(r"^\s*(?:VO|NARRATOR)\s*:\s*(.*)$", body, re.M)
    if vo:
        return "\n\n".join(vo)
    return body


def _clean(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    keep = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("#", "|", "```")) or re.match(r"^[-*]\s*\w+\s*:", s):
            keep.append("")
            continue
        s = re.sub(r"^[-*>]\s+", "", s)
        s = re.sub(r"(\*\*|__|\*|`)", "", s)
        keep.append(s)
    return "\n".join(keep)


def parse(src: str) -> Script:
    meta, body = _front_matter(src)
    text = _clean(_narration(body))
    music = meta.get("music")
    segments = []
    speed = None
    for para in re.split(r"\n\s*\n", text):
        para = " ".join(para.split())
        if not para:
            continue
        words, markers, plain = [], [], []
        gain = 0.0
        pos = 0
        for m in MARK.finditer(para):
            chunk = para[pos:m.start()]
            plain.append(chunk)
            words += chunk.split()
            kind, arg = m.group(1).lower(), m.group(2).strip()
            if kind == "music":
                music = "" if arg.lower() in ("none", "off") else arg
            elif kind == "vox":
                gain = float(re.findall(r"[-+]?[\d.]+", arg)[0])
            elif kind == "speed":
                speed = float(re.findall(r"[\d.]+", arg)[0])
            elif kind == "pause":
                markers.append(Marker("pause", len(words), seconds=float(re.findall(r"[\d.]+", arg)[0])))
            else:
                parts = arg.split()
                mk = Marker("sfx", len(words), name=parts[0])
                wait = False
                for p in parts[1:]:
                    if p.startswith("@"):
                        mk.seconds = float(p[1:])
                    elif p.lower().startswith("vol="):
                        mk.db = float(p[4:])
                    elif p.lower() == "wait":
                        wait = True
                    elif p.lower().startswith("hush="):
                        mk.hush = float(p[5:])
                markers.append(mk)
                if wait:  # hold the narration until the sound has played (length resolved at synth time)
                    markers.append(Marker("pause", len(words), name=parts[0], seconds=-1.0))
            pos = m.end()
        plain.append(para[pos:])
        words += para[pos:].split()
        seg_text = " ".join("".join(plain).split())
        if words or markers:
            segments.append(Segment(seg_text, words, markers, gain_db=gain, speed=speed))
    return Script(meta, segments, music)


def split_on_pauses(seg: Segment) -> list[tuple[Segment, float]]:
    """Split a segment at pause markers -> [(sub_segment, pause_after_seconds)]."""
    out, start, cur_markers = [], 0, []
    for mk in seg.markers:
        if mk.kind == "pause":
            sub = seg.words[start:mk.word_index]
            out.append((Segment(" ".join(sub), sub, [
                Marker(m.kind, m.word_index - start, m.name, m.seconds, m.db, m.hush) for m in cur_markers]), mk.seconds))
            start, cur_markers = mk.word_index, []
        else:
            cur_markers.append(mk)
    sub = seg.words[start:]
    out.append((Segment(" ".join(sub), sub, [
        Marker(m.kind, m.word_index - start, m.name, m.seconds, m.db, m.hush) for m in cur_markers]), 0.0))
    return out
