"""Beat maps for retention alignment (read-only over L1's files).

Own episodes: `episodes/<slug>/beatmap.json` (OPERATOR_DESIGN 5.4, written by L1). For episodes made before L1's
beatmap step existed (the pilots), `derive_from_storyboard` builds the same shape from `storyboard.json`
(scene durations with the F20 frame-accurate cumulative rounding, caption words) and the beat-alignment table of
`script.md`. Caption pages are approximated with a simple greedy pager (sentence end, pause, maxWords/maxChars,
explicit `br`); L1's beatmap carries the real pages and wins when present.

Source videos: `research/library/videos/<id>.json` beats (t_start/t_end/beat_type) or the line tables of
`research/corpus/explainer/[auto/]<id>.md` give scene-like segments; lines come from the corpus line table or
the transcript (`research/library/transcripts/<id>.txt`, `[mm:ss.xx] text`). Internal use only (BRIEF rule 5:
structure study, never reuse wording).
"""
from __future__ import annotations

import json
import os
import re

from ._common import ROOT, read_json, rpath

SENT_END = re.compile(r"[.!?…]+[\"')\]]*$")


def _episode_dir(slug: str, episode_dir: str | None = None) -> str:
    return episode_dir or rpath("episodes", slug)


# ---------------------------------------------------------------- own episodes
def load(slug: str, episode_dir: str | None = None) -> dict:
    d = _episode_dir(slug, episode_dir)
    bm = read_json(os.path.join(d, "beatmap.json"))
    if bm and bm.get("scenes"):
        bm.setdefault("derived", False)
        for s in bm["scenes"]:
            s.setdefault("sentences", split_sentences_text(s.get("text", ""), s["t0"], s["t1"]))
        return bm
    sb_path = os.path.join(d, "storyboard.json")
    if not os.path.exists(sb_path):
        raise FileNotFoundError(f"no beatmap.json or storyboard.json in {d}")
    return derive_from_storyboard(sb_path, os.path.join(d, "script.md"))


def scene_bounds(durations: list[float], fps: int) -> list[tuple[float, float]]:
    """F20: start_i = round(cum_i * fps) / fps (no per-scene rounding drift)."""
    out, cum = [], 0.0
    for d in durations:
        a = round(cum * fps) / fps
        cum += d
        b = round(cum * fps) / fps
        out.append((a, b))
    return out


def beat_labels_from_script(script_md: str, n: int) -> list[str | None]:
    """Paragraph -> beat label from the script's beat alignment table ('| 4-8 Pod, wave ... |').
    The label is the first word of the first cell after the paragraph number(s), upper-cased."""
    labels: list[str | None] = [None] * n
    if not os.path.exists(script_md):
        return labels
    with open(script_md, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\|\s*(\d+)(?:\s*[-–]\s*(\d+))?\s+([^|]+)\|", line)
            if not m:
                continue
            a, b = int(m.group(1)), int(m.group(2) or m.group(1))
            word = re.findall(r"[A-Za-z][A-Za-z'-]*", m.group(3))
            if not word:
                continue
            lab = word[0].upper()
            for p in range(a, b + 1):
                if 1 <= p <= n:
                    labels[p - 1] = lab
    return labels


def caption_pages(words: list[dict], max_words: int = 4, max_chars: int = 20, gap_break: float = 0.45) -> list[dict]:
    """Greedy approximation of the core pager (captions.tsx): new page on `br`, after a sentence end, after a
    pause >= gap_break, or when maxWords/maxChars would be exceeded. Good enough to say which words were on
    screen at time t; it is not frame-exact."""
    pages: list[dict] = []
    cur: list[dict] = []

    def flush():
        if cur:
            pages.append({"t0": cur[0]["start"], "t1": cur[-1]["end"], "text": " ".join(w["text"] for w in cur)})
            cur.clear()

    for i, w in enumerate(words):
        if cur:
            prev = cur[-1]
            chars = len(" ".join(x["text"] for x in cur)) + 1 + len(w["text"])
            if (w.get("br") or SENT_END.search(prev["text"]) or w["start"] - prev["end"] >= gap_break
                    or len(cur) >= max_words or chars > max_chars + 6):
                flush()
        cur.append(w)
    flush()
    for a, b in zip(pages, pages[1:]):
        a["t1"] = max(a["t1"], min(b["t0"], a["t1"] + 0.4))
    return pages


def split_sentences(words: list[dict]) -> list[dict]:
    out, cur = [], []
    for w in words:
        cur.append(w)
        if SENT_END.search(w["text"]):
            out.append({"t0": cur[0]["start"], "t1": cur[-1]["end"], "text": " ".join(x["text"] for x in cur)})
            cur = []
    if cur:
        out.append({"t0": cur[0]["start"], "t1": cur[-1]["end"], "text": " ".join(x["text"] for x in cur)})
    return out


def split_sentences_text(text: str, t0: float, t1: float) -> list[dict]:
    """Sentences of a scene's narration with times spread by word count (when no word timings are given)."""
    parts = [p.strip() for p in re.split(r"(?<=[.!?…])\s+", text or "") if p.strip()]
    if not parts:
        return []
    n = sum(len(p.split()) for p in parts)
    out, k = [], 0
    for p in parts:
        a = t0 + (t1 - t0) * k / n
        k += len(p.split())
        out.append({"t0": round(a, 3), "t1": round(t0 + (t1 - t0) * k / n, 3), "text": p})
    return out


def derive_from_storyboard(sb_path: str, script_md: str | None = None) -> dict:
    sb = read_json(sb_path)
    fps = int(sb.get("fps", 30))
    scenes = sb["scenes"]
    bounds = scene_bounds([float(s["duration"]) for s in scenes], fps)
    cap = sb.get("captions") or {}
    words = [w for w in cap.get("words", []) if "start" in w]
    pages = caption_pages(words, int(cap.get("maxWords", 4)), int(cap.get("maxChars", 20)), float(cap.get("gapBreak", 0.45)))
    labels = beat_labels_from_script(script_md or "", len(scenes))
    out = []
    for i, (s, (t0, t1)) in enumerate(zip(scenes, bounds)):
        ws = [w for w in words if t0 <= (w["start"] + w["end"]) / 2 < t1]
        comps = []
        for L in s.get("layers", []):
            if L.get("type") == "component" and L.get("name") and L["name"] not in comps:
                comps.append(L["name"])
        bg = (s.get("background") or {}).get("name")
        text = " ".join(w["text"] for w in ws) or s.get("notes", "")
        out.append({
            "scene_id": s.get("id", f"p{i:02d}"), "p": i + 1, "t0": t0, "t1": t1,
            "beat": labels[i] or s.get("beat") or "?", "skeleton_i": None, "source_beat_i": [],
            "text": text, "components": comps, "background": bg,
            "caption_pages": [p for p in pages if t0 <= p["t0"] < t1],
            "sentences": split_sentences(ws) if ws else split_sentences_text(text, t0, t1),
        })
    return {"v": 1, "slug": sb.get("id"), "duration_s": bounds[-1][1] if bounds else 0.0, "fps": fps,
            "scenes": out, "derived": True, "derived_from": os.path.relpath(sb_path, ROOT)}


# ---------------------------------------------------------------- source videos
def _mmss(s: str) -> float | None:
    m = re.match(r"^\s*(?:(\d+):)?(\d{1,2}):(\d{2}(?:\.\d+)?)\s*$", s)
    if not m:
        return None
    h = int(m.group(1) or 0)
    return h * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def corpus_lines(video_id: str) -> list[dict]:
    """Rows of the line-by-line table: {t, text, beat}. Looks in the hand-made corpus, then auto/."""
    for p in (rpath("research", "corpus", "explainer", f"{video_id}.md"),
              rpath("research", "corpus", "explainer", "auto", f"{video_id}.md")):
        if not os.path.exists(p):
            continue
        rows, cols = [], None
        with open(p, encoding="utf-8") as f:
            for line in f:
                if not line.startswith("|"):
                    cols = None if not line.strip() else cols
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                low = [c.lower() for c in cells]
                if "time" in low and "beat" in low and any(c.startswith("line") for c in low):
                    cols = (low.index("time"), next(i for i, c in enumerate(low) if c.startswith("line")), low.index("beat"))
                    continue
                if cols and len(cells) > max(cols):
                    t = _mmss(cells[cols[0]])
                    if t is not None:
                        rows.append({"t": t, "text": cells[cols[1]], "beat": re.sub(r"[*`]", "", cells[cols[2]])})
        if rows:
            return rows
    return []


def transcript_lines(video_id: str) -> list[dict]:
    for p in (rpath("research", "library", "transcripts", f"{video_id}.txt"),
              rpath("research", "corpus", "explainer", "raw", f"{video_id}.txt"),
              rpath("research", "corpus", "explainer", "auto", "raw", f"{video_id}.txt")):
        if not os.path.exists(p):
            continue
        rows = []
        with open(p, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^\[(\d+):(\d+(?:\.\d+)?)\]\s*(.*)$", line.strip())
                if m:
                    rows.append({"t": int(m.group(1)) * 60 + float(m.group(2)), "text": m.group(3)})
        if rows:
            return rows
    return []


def source_beatmap(video_id: str, duration_s: float | None = None) -> dict:
    """Segments of a source video: library beats if present, else runs of the corpus line table's beat column."""
    lib = read_json(rpath("research", "library", "videos", f"{video_id}.json")) or {}
    auto_idx = read_json(rpath("research", "corpus", "explainer", "auto", f"{video_id}.index.json")) or {}
    dur = float(duration_s or lib.get("duration") or auto_idx.get("duration_s") or 0) or None
    lines = corpus_lines(video_id)
    tlines = transcript_lines(video_id)
    segs = []
    if lib.get("beats"):
        for i, b in enumerate(lib["beats"]):
            segs.append({"i": i, "label": str(b.get("beat_type", "?")).split("/")[0].strip().upper(),
                         "t0": float(b["t_start"]), "t1": float(b["t_end"]), "summary": b.get("summary", "")})
    elif lines:
        cur = None
        for r in lines:
            lab = r["beat"].split("/")[0].strip().upper() or "?"
            if cur is None or lab != cur["label"]:
                if cur:
                    cur["t1"] = r["t"]
                cur = {"i": len(segs), "label": lab, "t0": r["t"], "t1": None, "summary": ""}
                segs.append(cur)
        if cur:
            cur["t1"] = dur or (lines[-1]["t"] + 3)
    if not segs:
        raise FileNotFoundError(f"no beats for source {video_id} (library json, corpus or auto/ annotation)")
    dur = dur or segs[-1]["t1"]
    src_lines = lines or tlines
    scenes = []
    for s in segs:
        ls = [x for x in src_lines if s["t0"] <= x["t"] < s["t1"]]
        sents = []
        for j, x in enumerate(ls):
            nxt = ls[j + 1]["t"] if j + 1 < len(ls) else s["t1"]
            sents.append({"t0": x["t"], "t1": nxt, "text": x["text"]})
        scenes.append({"scene_id": f"b{s['i']:02d}", "p": s["i"] + 1, "t0": s["t0"], "t1": s["t1"],
                       "beat": s["label"], "skeleton_i": None, "source_beat_i": [s["i"]],
                       "text": s["summary"], "components": [], "caption_pages": [], "sentences": sents})
    return {"v": 1, "slug": None, "video_id": video_id, "duration_s": dur, "scenes": scenes, "derived": True,
            "derived_from": "library beats" if lib.get("beats") else "corpus line table",
            "lines_from": "corpus" if lines else ("transcript" if tlines else None)}


def at(bm: dict, t: float) -> tuple[dict | None, dict | None, dict | None, dict | None]:
    """(scene, sentence, previous sentence, caption page) on screen at time t."""
    scene = None
    for s in bm["scenes"]:
        if s["t0"] <= t < s["t1"]:
            scene = s
            break
    if scene is None and bm["scenes"]:
        scene = bm["scenes"][-1] if t >= bm["scenes"][-1]["t0"] else bm["scenes"][0]
    sents = [x for s in bm["scenes"] for x in s.get("sentences", [])]
    sent = prev = None
    for k, x in enumerate(sents):
        if x["t0"] <= t:
            sent, prev = x, (sents[k - 1] if k else None)
        else:
            break
    page = None
    for s in bm["scenes"]:
        for p in s.get("caption_pages", []):
            if p["t0"] <= t:
                page = p
    if page and t > page["t1"] + 0.6:
        page = None
    return scene, sent, prev, page


if __name__ == "__main__":  # quick look: python -m pipeline.analytics.beatmap <slug>
    import sys

    bm = load(sys.argv[1])
    print(json.dumps({k: v for k, v in bm.items() if k != "scenes"}, indent=1))
    for s in bm["scenes"]:
        print(f"{s['scene_id']} {s['t0']:6.2f}-{s['t1']:6.2f} {s['beat']:<8} {s['text'][:70]}")
