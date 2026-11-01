"""Proof run for the gate in a scratch root (never the live ~/studio/app):

  1. gates the pilots in order, each against the ones before it (fixture rows in <root>/data/posts.jsonl,
     marked "fixture": true, mode "manual"), and expects PASS;
  2. builds a deliberately near-duplicate operator episode of the first pilot (reworded title and hook,
     same topic under another name, same script with a few words changed, the thumbnail re-graded and
     cropped, the MP4 re-encoded with a colour shift) and expects the gate to FAIL on sameness.

usage: python -m pipeline.qa.selftest --root DIR [--pilots explainer-orca,explainer-blue-whale,horror-pinned-rules]
                                      [--neardup-of explainer-orca] [--skip-pilots] [--no-sheets]
DIR must contain episodes/<pilot>/, out/pilots/<pilot>/ and research/ (a copy or symlinks). Exit 0 when every
expectation holds, 1 otherwise. The re-encode runs on 2 threads at nice 10 (about a minute on the Spark).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys

from .util import be_nice, find_mp4, narration_paragraphs, now_iso, qa_dir, read_json, read_jsonl, root, tool, write_json

NEARDUP = "op-20261102-a-killer-whale"
SUBS = [  # (old, new) applied to the narration: a lazy rewrite, the kind the sameness gate must catch
    ("Wild killer whales could kill you easily. They never have.", "A wild killer whale could easily kill you. None ever has."),
    ("Not because they can't.", "It isn't that they can't."),
    ("And you'd never meet just one.", "And you would never meet only one."),
    ("Comforting, right?", "Reassuring, right?"),
    ("Nobody knows why.", "No one knows why."),
]


def _posts(r):
    return r / "data" / "posts.jsonl"


def guard(r) -> None:
    rows = read_jsonl(_posts(r))
    if any(not row.get("fixture") for row in rows):
        sys.exit(f"refusing: {_posts(r)} has real (non-fixture) rows; run the selftest in a scratch root")


def record_fixture_post(r, slug: str) -> None:
    p = _posts(r)
    p.parent.mkdir(parents=True, exist_ok=True)
    row = {"v": 1, "at": now_iso(), "post_key": f"{slug}:youtube", "slug": slug, "platform": "youtube",
           "mode": "manual", "status": "published", "published_at": now_iso(), "fixture": True}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def gate(r, slug: str, sheets: bool) -> tuple[int, dict, str]:
    cmd = [sys.executable, "-m", "pipeline.qa.gate", slug, "--root", str(r)] + ([] if sheets else ["--no-sheets"])
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, read_json(qa_dir(r, slug) / "gate.json") or {}, (p.stdout + p.stderr).strip()


def _ff(args: list[str]) -> None:
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2",
           "-filter_threads", "2", *args]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-400:])


def build_neardup(r, base: str, slug: str = NEARDUP) -> None:
    src_ep, ep, out = r / "episodes" / base, r / "episodes" / slug, r / "out" / slug
    ep.mkdir(parents=True, exist_ok=True)
    (out / "thumbs").mkdir(parents=True, exist_ok=True)

    text = (src_ep / "script.md").read_text(encoding="utf-8")
    for old, new in SUBS:
        text = text.replace(old, new)
    text = re.sub(r"^id: .*$", f"id: {slug}", text, count=1, flags=re.M)
    text = re.sub(r"^title: .*$", "title: Killer Whales Have Never Killed You. Here Is Why.", text, count=1, flags=re.M)
    (ep / "script.md").write_text(text, encoding="utf-8")

    sb = read_json(src_ep / "storyboard.json")
    sb["id"] = slug
    write_json(ep / "storyboard.json", sb)
    (ep / "audio").mkdir(exist_ok=True)
    shutil.copy(src_ep / "audio" / "captions.json", ep / "audio" / "captions.json")

    # beatmap in L1's shape (5.4), so the beatmap paths of the gate run too
    paras = narration_paragraphs(ep / "script.md")
    labels = ["HOOK", "STAKES"] + ["RUNG"] * 6 + ["TURN", "PEAK", "PEAK", "TWIST", "TWIST", "STINGER"]
    skel = {"HOOK": 0, "STAKES": 1, "RUNG": 2, "TURN": 3, "PEAK": 4, "TWIST": 5, "STINGER": 6}
    fps, cum, scenes = sb.get("fps", 30), 0.0, []
    for i, s in enumerate(sb["scenes"]):
        t0 = round(cum * fps) / fps
        cum += s["duration"]
        lab = labels[i] if i < len(labels) else "RUNG"
        scenes.append({"scene_id": s["id"], "p": i + 1, "t0": t0, "t1": round(cum * fps) / fps, "beat": lab,
                       "skeleton_i": skel[lab], "source_beat_i": [], "text": paras[i] if i < len(paras) else "",
                       "components": sorted({l.get("name") for l in s.get("layers", []) if l.get("name")}),
                       "background": (s.get("background") or {}).get("name"), "max_hold_s": None, "caption_pages": []})
    write_json(ep / "beatmap.json", {"v": 1, "slug": slug, "duration_s": round(cum, 3), "fps": fps, "scenes": scenes})

    tr = "research/corpus/explainer/raw/VtrcKTkhDHU.txt"
    write_json(ep / "source.json", {
        "v": 1, "source_id": "VtrcKTkhDHU", "url": "https://www.youtube.com/watch?v=VtrcKTkhDHU", "platform": "youtube",
        "format": "long", "transcript_file": tr if (r / tr).is_file() else None, "angle": "fixture: near-duplicate",
        "hook": {"code": "H6"}, "beats": [], "skeleton": [], "fixture": True})
    write_json(ep / "variant.json", {"v": 1, "experiment_id": None, "arm": None,
                                     "variables": {"hook.max_words": 12, "visual.max_hold_s": 3.0}})

    thumb_src = next(iter(sorted((r / "out" / "pilots" / base / "thumbs").glob(f"{base}_*-eye_9x16.jpg"))), None)
    thumb = out / "thumbs" / f"{slug}_explainer-eye_9x16.jpg"
    if thumb_src:
        _ff(["-i", str(thumb_src), "-vf", "eq=brightness=0.04:saturation=1.15,crop=iw*0.96:ih*0.96,scale=1080:1920",
             "-q:v", "3", str(thumb)])
    write_json(ep / "package.json", {
        "v": 1, "title_pick": 0, "titles": ["Killer Whales Have Never Killed You. Here Is Why.",
                                            "Why A Killer Whale Has Never Hunted You"],
        "yt_title": "Killer Whales Have Never Killed You. Here Is Why.",
        "yt_description": "Wild killer whales could easily kill you. None ever has.\n\n"
                          "Narration: synthetic AI voice (Kokoro TTS). Animation: original 2D vector art.",
        "short_caption": "Killer whales could kill you. They never have.", "hashtags": ["#orca", "#ocean"],
        "thumb_pick": str(thumb.relative_to(r)), "facts_to_verify": [], "fixture": True})

    mp4 = out / f"{slug}_9x16.mp4"
    if not mp4.is_file():
        _ff(["-i", str(find_mp4(r, base)), "-vf", "eq=brightness=0.02:saturation=1.08", "-c:v", "libx264",
             "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "copy", str(mp4)])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa.selftest")
    ap.add_argument("--root", required=True)
    ap.add_argument("--pilots", default="explainer-orca,explainer-blue-whale,horror-pinned-rules")
    ap.add_argument("--neardup-of", default="explainer-orca")
    ap.add_argument("--skip-pilots", action="store_true", help="reuse the fixture history already in --root")
    ap.add_argument("--no-sheets", action="store_true")
    a = ap.parse_args(argv)
    be_nice()
    r = root(a.root)
    if (r / ".git").exists():
        sys.exit("refusing: --root is a git checkout; use a scratch copy")
    guard(r)
    ok, report = True, {}
    if not a.skip_pilots:
        if _posts(r).exists():
            _posts(r).unlink()  # fixture-only file (guard above), rebuilt in order
        for slug in a.pilots.split(","):
            rc, g, txt = gate(r, slug, not a.no_sheets)
            print(txt + "\n")
            report[slug] = {"exit": rc, "verdict": g.get("verdict"), "fail": g.get("fail"),
                            "sameness_vs": (g.get("checks", {}).get("sameness", {}).get("value") or {}).get("vs")}
            ok &= rc == 0 and g.get("verdict") == "PASS"
            if g.get("verdict") == "PASS":
                record_fixture_post(r, slug)
    build_neardup(r, a.neardup_of)
    rc, g, txt = gate(r, NEARDUP, not a.no_sheets)
    print(txt + "\n")
    same = g.get("checks", {}).get("sameness", {})
    report[NEARDUP] = {"exit": rc, "verdict": g.get("verdict"), "fail": g.get("fail"),
                       "sameness_hits": [f"{h['level']} {h['metric']}={h['value']} vs {h['vs']}" for h in same.get("hits", [])]}
    ok &= rc == 6 and same.get("status") == "FAIL"
    print(json.dumps({"expectations_met": ok, "results": report}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
