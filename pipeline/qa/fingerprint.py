"""Per-video fingerprint for the sameness check: out/<slug>/qa/fingerprint.json (design 5.7).

usage: python -m pipeline.qa.fingerprint <slug> [--root DIR] [--no-video]

Fields of 5.7 plus (L2-internal, additive): narration_shingles (crc32 of word 5-grams, so the text itself
is not copied around), frame_dhashes (10 frames at 5 %, 15 % ... 95 %), subject (main kit creature),
mp4_sha256, duration_s, partial (true when built without the video).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

from . import textsim
from .util import (episode_file, find_mp4, front_matter, hook_text, narration_paragraphs, now_iso, qa_dir,
                   read_json, rel, root, sha256, slug_topic, write_json)

# Components that set the scene or give scale; they never count as the subject.
GENERIC = re.compile(r"/(Ocean|You|Diver|Bus|Car|Elephant|GolfCart|Jet|Sauropod|Headline|Tag|Stat|DepthMeter|ScaleBar|"
                     r"HeightChart|Map|Timer|Options|SpeedBars|Balance|ECG|Krill|Vignette|Flicker|Darkness|Glitch|"
                     r"RedText|EndCard|Heartbeat)$")
INFOGRAPHIC = re.compile(r"/(Headline|Tag|Stat|DepthMeter|ScaleBar|HeightChart|Map|Timer|Options|SpeedBars|Balance|ECG)$")

S_CODES = {"S1": "HOOK", "S2": "STAKES", "S3": "RUNG", "S4": "TURN", "S5": "PEAK", "S6": "TWIST", "S7": "STINGER"}
BEAT_WORDS = [  # (label, regex) for the first column of a script's beat-alignment table (pilots have no beatmap)
    ("STINGER", r"bookend|stinger|loop|ending|\bend\b"),  # first: "bookend loop (-> hook)" is the ending
    ("HOOK", r"\bhook\b|rule four on screen"),
    ("TWIST", r"twist"),
    ("PEAK", r"peak|answer|verdict|reveal|payoff|options"),
    ("TURN", r"\?|turnstile|\bturn\b|question"),
    ("STAKES", r"scale|stakes|anchor|length|pinned by"),
]


def norm_beat(label: str) -> str:
    s = str(label or "").strip().upper()
    if s[:2] in S_CODES and (len(s) == 2 or not s[2].isdigit()):
        return S_CODES[s[:2]]
    s = re.sub(r"[^A-Z]+", "_", s).strip("_")
    return {"RUNGS": "RUNG", "LADDER": "RUNG", "ESC": "RUNG", "TURNSTILE": "TURN", "LOOP": "STINGER",
            "BOOKEND": "STINGER", "CTA": "STINGER"}.get(s, s or "?")


def beats_from_beatmap(bm: dict) -> list[str]:
    seq, last = [], None
    for s in bm.get("scenes", []):
        key = (norm_beat(s.get("beat")), s.get("skeleton_i"))
        if key != last:
            seq.append(key[0])
            last = key
    return seq


def beats_from_script(text: str) -> list[str]:
    """Fallback: the 'Our beat (paragraph)' column of the beat-alignment table, mapped to skeleton labels."""
    seq, in_table = [], False
    for line in text.splitlines():
        if line.startswith("| Our beat"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            cell = line.strip("|").split("|")[0].strip().lower()
            if not cell or set(cell) <= set("-: "):
                continue
            seq.append(next((lab for lab, rx in BEAT_WORDS if re.search(rx, cell)), "RUNG"))
    return seq


def shot_mix(sb: dict) -> dict[str, int]:
    """Scenes in which each component appears (background + layers)."""
    c: Counter = Counter()
    for s in sb.get("scenes", []):
        names = set()
        bg = s.get("background") or {}
        if bg.get("type") == "component":
            names.add(bg.get("name"))
        for l in s.get("layers", []):
            if l.get("type") == "component":
                names.add(l.get("name"))
            elif l.get("type") in ("text", "svg", "image"):
                names.add(f"<{l['type']}>")
        c.update(n for n in names if n)
    return dict(sorted(c.items()))


def subject(mix: dict[str, int]) -> str | None:
    cands = [(n, k) for k, n in mix.items() if not GENERIC.search(k) and not k.startswith("<")]
    return max(cands)[1] if cands else None


def shot_mix_class(sb: dict) -> str:
    """creature_heavy | infographic_heavy | balanced, from which kind of layer dominates each scene."""
    cre = inf = 0
    for s in sb.get("scenes", []):
        names = [l.get("name", "") for l in s.get("layers", []) if l.get("type") == "component"]
        i = sum(1 for n in names if INFOGRAPHIC.search(n))
        c = sum(1 for n in names if not GENERIC.search(n))
        cre += c > i
        inf += i > c
    tot = max(1, cre + inf)
    return "creature_heavy" if cre / tot >= 0.65 else "infographic_heavy" if inf / tot >= 0.65 else "balanced"


def _titles_md_pick(path) -> tuple[str | None, str | None]:
    """(picked title, its 'pair with thumbnail' cell) from a pilot-style titles.md."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"\*\*Pick:\*\*\s*#(\d+)", text)
    want = m.group(1) if m else "1"
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0] == want:
            t = re.sub(r"\*\*(.+?)\*\*.*", r"\1", cells[1]).strip()
            return t, (cells[-1] if len(cells) >= 4 else None)
    return None, None


def title_and_thumb(r, slug: str) -> tuple[str, str | None, str]:
    """(title, thumbnail path or None, where the title came from)."""
    pkg = read_json(r / "episodes" / slug / "package.json") or {}
    thumb = pkg.get("thumb_pick")
    thumb = str(r / thumb) if thumb and not str(thumb).startswith("/") else thumb
    if pkg.get("titles") or pkg.get("yt_title"):
        titles = pkg.get("titles") or []
        i = pkg.get("title_pick", 0) or 0
        t = titles[i] if 0 <= i < len(titles) else pkg.get("yt_title")
        return t or pkg.get("yt_title") or "", thumb, "package.json"
    title, pair = None, None
    tm = episode_file(r, slug, "titles.md")
    if tm:
        title, pair = _titles_md_pick(tm)
    if not thumb:
        thumb = _thumb_from_pair(r, slug, pair)
    if title:
        return title, thumb, rel(r, tm)
    script = r / "episodes" / slug / "script.md"
    fm = front_matter(script.read_text(encoding="utf-8")) if script.is_file() else {}
    return fm.get("title", ""), thumb, "script.md"


def _thumb_from_pair(r, slug: str, pair: str | None) -> str | None:
    thumbs = [d / "thumbs" for d in (r / "out" / slug, r / "out" / "pilots" / slug)]
    files = sorted(p for d in thumbs if d.is_dir() for p in d.glob("*_9x16.jpg") if not p.name.startswith("sheet"))
    if not files:
        return None
    spec = read_json(r / "episodes" / slug / "thumbs.json") or {}
    if pair and ":" in pair:
        tmpl, text = (x.strip() for x in pair.split(":", 1))
        niche = spec.get("niche") or slug.split("-")[0]
        for v in spec.get("variants", []):
            if v.get("template") == tmpl and v.get("text", "").strip().upper() == text.upper():
                want = f"{v.get('id', slug)}_{niche}-{tmpl}_9x16.jpg"
                hit = [p for p in files if p.name == want]
                if hit:
                    return str(hit[0])
        hit = [p for p in files if f"-{tmpl}_9x16" in p.name and p.name.startswith(f"{slug}_")]
        if hit:
            return str(hit[0])
    return str(files[0])


def build(slug: str, r=None, samples=None, duration_s: float | None = None, video: bool = True) -> dict:
    """samples: optional (N, h, w, 3) frames at 1 fps from the gate, so the video is decoded once."""
    r = root(r) if not hasattr(r, "joinpath") else r
    ep = r / "episodes" / slug
    script = ep / "script.md"
    text = script.read_text(encoding="utf-8") if script.is_file() else ""
    paras = narration_paragraphs(script) if script.is_file() else []
    fm = front_matter(text)
    src = read_json(ep / "source.json") or {}
    var = read_json(ep / "variant.json") or {}
    sb = read_json(ep / "storyboard.json") or {}
    bm = read_json(ep / "beatmap.json")
    title, thumb, title_from = title_and_thumb(r, slug)
    mix = shot_mix(sb)
    fp = {
        "v": 1, "slug": slug, "at": now_iso(), "title": title, "title_from": title_from,
        "hook": hook_text(paras), "topic": fm.get("topic") or src.get("topic") or slug_topic(slug),
        "niche": fm.get("niche") or (slug.split("-")[0] if not slug.startswith("op-") else "explainer"),
        "beat_seq": beats_from_beatmap(bm) if bm else beats_from_script(text),
        "beat_seq_from": "beatmap.json" if bm else "script.md beat table",
        "shot_mix": mix, "shot_mix_class": shot_mix_class(sb), "subject": subject(mix),
        "thumb": rel(r, thumb), "thumb_dhash": None, "cover_dhash": None, "frame_dhashes": [],
        "source_id": src.get("source_id") or (fm.get("_references") or [None])[0],
        "hook_code": (src.get("hook") or {}).get("code") or (var.get("variables") or {}).get("hook.type"),
        "narration_shingles": textsim.shingles(" ".join(paras)),
        "mp4_sha256": None, "duration_s": duration_s, "partial": True,
    }
    if not video:
        return fp
    from . import frames
    mp4 = find_mp4(r, slug)
    if thumb:
        fp["thumb_dhash"] = frames.dhash(frames.load_image(thumb, 216, 384))
    if mp4:
        fp["mp4_sha256"] = sha256(mp4)
        if samples is None:
            samples = frames.sample_video(mp4)
        if len(samples):
            fp["cover_dhash"] = frames.dhash(samples[0])
            n = len(samples)
            fp["frame_dhashes"] = [frames.dhash(samples[min(n - 1, int(n * (k + 0.5) / 10))]) for k in range(10)]
            fp["partial"] = False
    return fp


def load(r, slug: str) -> dict | None:
    return read_json(qa_dir(r, slug) / "fingerprint.json")


def save(r, fp: dict) -> None:
    write_json(qa_dir(r, fp["slug"]) / "fingerprint.json", fp)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa.fingerprint")
    ap.add_argument("slug")
    ap.add_argument("--root")
    ap.add_argument("--no-video", action="store_true", help="text + storyboard only (no ffmpeg)")
    a = ap.parse_args(argv)
    r = root(a.root)
    fp = build(a.slug, r, video=not a.no_video)
    save(r, fp)
    show = {k: v for k, v in fp.items() if k != "narration_shingles"}
    show["narration_shingles"] = f"{len(fp['narration_shingles'])} hashes"
    print(json.dumps(show, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
