"""Per-platform captions (docs/OPERATOR_DESIGN.md 5.9, 8.5) -> out/<slug>/publish/captions.json.

Sources, in order: episodes/<slug>/package.json (5.5); else titles.md + description.md from episodes/<slug>/ or
out/pilots/<slug>/ (the pilot format). The disclosure line is appended to every platform's text if missing.

Limits are the ones Buffer validates (https://developers.buffer.com/guides/character-limits.md, read 2026-11-01),
counted in UTF-16 code units; Instagram counts each line break as 2:
  YouTube title 100, description 5000 | TikTok with video 2200 | Instagram 2196 and 30 hashtags.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from pipeline.common import timeutil

from . import paths

DISCLOSURE = "Narration: synthetic AI voice (Kokoro TTS). Animation: original 2D vector art."
LIMITS = {"youtube_title": 100, "youtube_description": 5000, "tiktok": 2200, "instagram": 2196}
IG_MAX_HASHTAGS = 30
HASHTAG_RE = re.compile(r"(?<![\w&])#[\w]+", re.U)


def utf16_len(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2


def ig_len(s: str) -> int:
    return utf16_len(s) + s.count("\n")  # each line break counts 2


def _fit(body: str, tail: str, limit: int, measure=utf16_len) -> str:
    """body + tail within limit, trimming body at a word boundary (tail is never cut)."""
    sep = "\n\n" if body and tail else ""
    full = body + sep + tail
    if measure(full) <= limit:
        return full
    room = limit - measure(sep + tail) - 1
    if room <= 0:
        raise ValueError(f"disclosure/hashtags alone exceed the {limit} limit")
    cut = body
    while measure(cut) > room:
        cut = cut[: max(0, len(cut) - max(1, len(cut) // 20))]
    cut = cut.rsplit(" ", 1)[0] if " " in cut else cut
    return cut.rstrip(" ,;:-") + "…" + sep + tail


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def clean_title(t: str) -> str:
    t = re.sub(r"[*_`]", "", t).replace("<", "").replace(">", "").strip()  # YouTube rejects < and > in titles
    if utf16_len(t) > LIMITS["youtube_title"]:
        t = t[: LIMITS["youtube_title"] - 1].rsplit(" ", 1)[0] + "…"
    return t


# ---------------------------------------------------------------------------------------------------------------
# readers

def parse_titles_md(text: str) -> tuple[list[str], int]:
    """(titles in table order, picked index). Rows look like `| 2 | **Title** | ... |`; pick from `**Pick:** #2`."""
    rows: dict[int, str] = {}
    for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*\*\*(.+?)\*\*", text, re.M):
        rows[int(m.group(1))] = m.group(2).strip()
    titles = [rows[k] for k in sorted(rows)]
    pick = 0
    m = re.search(r"\*\*Pick:?\*\*:?\s*#?(\d+)", text) or re.search(r"Pick:?\s*\**\s*#(\d+)", text)
    if m and int(m.group(1)) in rows:
        pick = sorted(rows).index(int(m.group(1)))
    return titles, pick


def parse_description_md(text: str) -> dict:
    """First `## ` section (the 9:16 Shorts/TikTok caption): caption lines, hashtags, disclosure present?"""
    secs = re.split(r"^##\s+", text, flags=re.M)
    first = secs[1] if len(secs) > 1 else text
    body = first.split("\n", 1)[1] if "\n" in first else ""
    caption, tags, disclosure = [], [], None
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if _norm(s) == _norm(DISCLOSURE) or s.lower().startswith("narration:"):
            disclosure = s
            continue
        toks = s.split()
        if toks and all(t.startswith("#") for t in toks):
            tags += toks
            continue
        caption.append(s)
    return {"caption": "\n".join(caption), "hashtags": tags, "disclosure": disclosure}


def load_package(slug: str) -> tuple[dict, list[str]]:
    """Normalized package (5.5 shape) and the source files used."""
    ep, pil = paths.episode_dir(slug), paths.pilot_dir(slug)
    pkg = paths.read_json(ep / "package.json")
    if pkg:
        titles = pkg.get("titles") or []
        pick = int(pkg.get("title_pick") or 0)
        pkg = dict(pkg)
        pkg.setdefault("yt_title", titles[pick] if titles else "")
        return pkg, [str(ep / "package.json")]
    tf = paths.first_existing(ep / "titles.md", pil / "titles.md")
    df = paths.first_existing(ep / "description.md", pil / "description.md")
    if not tf or not df:
        raise FileNotFoundError(f"{slug}: no package.json and no titles.md/description.md "
                                f"in {ep} or {pil}")
    titles, pick = parse_titles_md(tf.read_text(encoding="utf-8"))
    if not titles:
        raise ValueError(f"{tf}: no title rows found")
    d = parse_description_md(df.read_text(encoding="utf-8"))
    return {"v": 1, "title_pick": pick, "titles": titles, "yt_title": titles[pick],
            "yt_description": None, "short_caption": d["caption"], "hashtags": d["hashtags"],
            "disclosure_line": d["disclosure"]}, [str(tf), str(df)]


# ---------------------------------------------------------------------------------------------------------------
# builder

def build(slug: str, pkg: dict | None = None) -> dict:
    sources = []
    if pkg is None:
        pkg, sources = load_package(slug)
    disclosure = pkg.get("disclosure_line") or DISCLOSURE
    tags = []
    for t in pkg.get("hashtags") or []:
        t = t if t.startswith("#") else "#" + t
        if t.lower() not in {x.lower() for x in tags}:
            tags.append(t)
    social_tags = [t for t in tags if t.lower() != "#shorts"]
    yt_tags = social_tags + ["#shorts"]

    caption = (pkg.get("short_caption") or "").strip()
    # caption text may already carry hashtags inline; don't repeat them
    inline = {t.lower() for t in HASHTAG_RE.findall(caption)}

    def tail(ts):
        line = " ".join(t for t in ts if t.lower() not in inline)
        return (line + "\n\n" + disclosure) if line else disclosure

    yt_desc_src = (pkg.get("yt_description") or "").strip()
    if yt_desc_src:
        body = "\n".join(l for l in yt_desc_src.splitlines() if _norm(l) != _norm(disclosure)).strip()
        tl = ("#shorts\n\n" if "#shorts" not in body.lower() else "") + disclosure
        yt_desc = _fit(body, tl, LIMITS["youtube_description"])
    else:
        yt_desc = _fit(caption, tail(yt_tags), LIMITS["youtube_description"])

    ig_tags = social_tags[:IG_MAX_HASHTAGS - len(inline)] if len(inline) < IG_MAX_HASHTAGS else []
    out = {
        "v": 1, "slug": slug, "at": timeutil.iso(),
        "youtube": {"title": clean_title(pkg.get("yt_title") or ""), "description": yt_desc,
                    "tags": [t.lstrip("#") for t in social_tags]},
        "tiktok": {"text": _fit(caption, tail(social_tags), LIMITS["tiktok"])},
        "instagram": {"text": _fit(caption, tail(ig_tags), LIMITS["instagram"], ig_len)},
        "disclosure_line": disclosure,
        "sources": [str(Path(s).relative_to(paths.ROOT)) if Path(s).is_relative_to(paths.ROOT) else s for s in sources],
        "cover_offset_ms": pkg.get("cover_offset_ms"),
    }
    problems = validate(out)
    if problems:
        raise ValueError("; ".join(problems))
    return out


def validate(c: dict) -> list[str]:
    p = []
    t = c["youtube"]["title"]
    if not t:
        p.append("youtube title empty")
    if utf16_len(t) > LIMITS["youtube_title"]:
        p.append("youtube title > 100")
    if utf16_len(c["youtube"]["description"]) > LIMITS["youtube_description"]:
        p.append("youtube description > 5000")
    if utf16_len(c["tiktok"]["text"]) > LIMITS["tiktok"]:
        p.append("tiktok text > 2200")
    if ig_len(c["instagram"]["text"]) > LIMITS["instagram"]:
        p.append("instagram text > 2196")
    if len(HASHTAG_RE.findall(c["instagram"]["text"])) > IG_MAX_HASHTAGS:
        p.append("instagram > 30 hashtags")
    d = _norm(c["disclosure_line"])
    for k in ("tiktok", "instagram"):
        if d not in _norm(c[k]["text"]):
            p.append(f"{k} text lacks the disclosure line")
    if d not in _norm(c["youtube"]["description"]):
        p.append("youtube description lacks the disclosure line")
    return p


def write(slug: str, captions: dict, out_path: Path | None = None) -> Path:
    out_path = out_path or paths.publish_dir(slug) / "captions.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(captions, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(out_path)
    return out_path


if __name__ == "__main__":
    import sys
    print(json.dumps(build(sys.argv[1]), indent=1, ensure_ascii=False))
