"""Deterministic QA gate for one episode (docs/OPERATOR_DESIGN.md 5.6 and 7.2).

usage: python -m pipeline.qa.gate <slug> [--root DIR] [--last-n 10] [--against s1,s2] [--mp4 PATH]
                                  [--source-frames auto|none] [--no-sheets] [--json]

Writes out/<slug>/qa/{gate.json, fingerprint.json, sbs.jpg, stills.jpg, gate.log}.
Exit 0 = PASS (WARNs allowed), 6 = FAIL (any check FAIL), 1 = error (gate.json verdict ERROR).
Runs on the Spark CPU: nice 10, ffmpeg -threads 2, one ffmpeg at a time.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import traceback

from . import fingerprint as fpmod
from . import frames, sameness, textsim
from .util import (REPO, be_nice, episode_file, find_mp4, front_matter, hook_text, narration_paragraphs, now_iso,
                   originality_module, probe_duration, qa_dir, read_json, refs_dir, rel, root, rules, run, sha256,
                   tool, write_json)

# ---- thresholds (rules.json may override hook.max_words and visual.max_hold_s) -----------------------------
DUR_MIN, DUR_WARN = 61.0, 90.0
LUFS_TARGET, LUFS_TOL, TP_FAIL, TP_WARN = -14.0, 1.5, -0.5, -1.0
BLACK_D, BLACK_PIX, BLACK_FAIL_S = 0.25, 0.10, 0.5
FREEZE_N = 0.003
MAGENTA_FAIL = 0.002
SRC_SHARE_FAIL, SRC_RUN_FAIL = 0.01, 6
FIRST_SPEECH_FAIL = 1.0
SAFE_FAIL, SAFE_WARN, EDGE = 0.80, 0.66, 0.05
VARIANT_TOL = 0.20

STOPWORDS = set("a an the and or but so to of in on at by for with from as is are was were be it its this that "
                "then than if you your i my we our they their he she his her".split())
TEXT_LAYER = re.compile(r"/(Headline|Tag|Stat|Options|Timer|RedText|EndCard|SpeedBars|HeightChart|Balance)$")
CREATURE_SKIP = re.compile(r"/(Ocean|Headline|Tag|Stat|Options|Timer|Map|DepthMeter|ScaleBar|HeightChart|SpeedBars|"
                           r"Balance|ECG|Vignette|Flicker|Darkness|Glitch|RedText|EndCard|Heartbeat)$")
DISCLOSURE = re.compile(r"(synthetic|ai)[- ]?(generated )?voice|text[- ]to[- ]speech|\btts\b", re.I)


def chk(status, value=None, threshold=None, detail=""):
    d = {"status": status, "value": value}
    if threshold is not None:
        d["threshold"] = threshold
    if detail:
        d["detail"] = detail
    return d


# ---------------------------------------------------------------------------------------------- media scan

def scan_av(mp4, freeze_d: float, has_audio: bool) -> dict:
    """One decode pass: blackdetect + freezedetect on video, ebur128 (true peak) on audio."""
    fc = f"[0:v]blackdetect=d={BLACK_D}:pix_th={BLACK_PIX},freezedetect=n={FREEZE_N}:d={freeze_d:.2f}[v]"
    maps = ["-map", "[v]", "-f", "null", "-"]
    if has_audio:
        fc += ";[0:a]ebur128=peak=true[a]"
        maps += ["-map", "[a]", "-f", "null", "-"]
    cmd = [tool("ffmpeg"), "-nostdin", "-hide_banner", "-nostats", "-threads", "2", "-filter_threads", "2",
           "-filter_complex_threads", "2", "-i", str(mp4), "-filter_complex", fc, *maps]
    p = run(cmd)
    err = p.stderr
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg scan failed: {err[-400:]}")
    blacks = [{"t0": float(a), "t1": float(b), "d": float(c)} for a, b, c in
              re.findall(r"black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)", err)]
    fs = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", err)]
    fe = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", err)]
    freezes = [{"t0": s, "t1": (fe[i] if i < len(fe) else None)} for i, s in enumerate(fs)]
    loud = {}
    summ = err.rsplit("Summary:", 1)[-1] if "Summary:" in err else ""
    m = re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", summ)
    if m:
        loud["I_lufs"] = float(m.group(1)) if m.group(1) != "-inf" else None
    m = re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf) dBFS", summ, re.S)
    if m:
        loud["true_peak_dbtp"] = float(m.group(1)) if m.group(1) != "-inf" else None
    m = re.search(r"LRA:\s+([\d.]+) LU", summ)
    if m:
        loud["LRA_lu"] = float(m.group(1))
    return {"black": blacks, "freeze": freezes, "loud": loud}


def has_audio_stream(mp4) -> bool:
    p = run([tool("ffprobe"), "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0",
             str(mp4)])
    return bool(p.stdout.strip())


# ---------------------------------------------------------------------------------------------- storyboard

def scene_times(sb: dict) -> list[tuple[float, float, dict]]:
    """Frame-accurate scene starts (F20 rule: start_i = round(cum_i * fps) / fps)."""
    fps = sb.get("fps", 30) or 30
    out, cum = [], 0.0
    for s in sb.get("scenes", []):
        t0 = round(cum * fps) / fps
        cum += float(s.get("duration", 0))
        out.append((t0, round(cum * fps) / fps, s))
    return out


def coord(v, total: float, default: float) -> float:
    if v is None:
        return default
    if isinstance(v, str) and v.strip().endswith("%"):
        return float(v.strip()[:-1]) / 100 * total
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def frame_size(sb: dict) -> tuple[int, int]:
    return (1920, 1080) if sb.get("format") == "16:9" else (1080, 1920)


def layer_box(l: dict, W: int, H: int) -> tuple[float, float, float, float] | None:
    w, h = coord(l.get("width"), W, 0), coord(l.get("height"), H, 0)
    if not w or not h:
        return None
    sc = float(l.get("scale", 1) or 1)
    x, y = coord(l.get("x"), W, W / 2), coord(l.get("y"), H, H / 2)
    ax, ay = float(l.get("anchorX", 0.5)), float(l.get("anchorY", 0.5))
    return (x - ax * w * sc, y - ay * h * sc, x + (1 - ax) * w * sc, y + (1 - ay) * h * sc)


def _zooming(scene: dict) -> bool:
    cam = scene.get("camera") or {}
    if cam.get("preset") not in (None, "static", "none"):
        return True
    return any(abs(float(k.get("zoom", 1)) - 1) > 0.02 for k in cam.get("keyframes", []))


def safe_band(fmt: str) -> dict:
    """SAFE_AREA from studio/src/core/schema.ts (px), with the values at the time of writing as fallback."""
    out = {"9:16": {"top": 230, "bottom": 440}, "16:9": {"top": 60, "bottom": 90}}
    try:
        src = (REPO / "studio/src/core/schema.ts").read_text(encoding="utf-8")
        for f, top, bottom in re.findall(r"'(9:16|16:9)':\s*\{top:\s*(\d+),\s*bottom:\s*(\d+)", src):
            out[f] = {"top": int(top), "bottom": int(bottom)}
    except OSError:
        pass
    return out.get(fmt, out["9:16"])


def caption_ys(scene: dict, style: dict, sb: dict) -> list[float]:
    """Caption centres (fraction of height) as the renderer places them: captionY / captionYAt / style.y,
    clamped into the safe band like captions.tsx (cy <= H - safe.bottom - 0.6 * fontSize)."""
    W, H = frame_size(sb)
    fs = float(style.get("fontSize", 84 if sb.get("format") == "16:9" else 104))
    band = safe_band(sb.get("format", "9:16"))
    base = style.get("y", 0.82 if sb.get("format") == "16:9" else 0.64)
    ys = [scene.get("captionY", base)]
    ys += [c.get("y") for c in scene.get("captionYAt") or [] if isinstance(c.get("y"), (int, float))]
    lo, hi = (band["top"] + fs) / H, (H - band["bottom"] - 0.6 * fs) / H
    return [max(lo, min(hi, float(y))) for y in ys]


def check_safe_area(sb: dict) -> dict:
    W, H = frame_size(sb)
    cap = sb.get("captions") or {}
    style = cap.get("style") or {}
    fsz = float(style.get("fontSize", 84 if sb.get("format") == "16:9" else 104))
    half2, half1 = fsz * 1.15 / H, fsz * 0.6 / H  # bottom of a 2-line page (WARN) / of a 1-line page (FAIL)
    fails, warns = [], []
    caps: dict[float, list] = {}  # caption bottom (% of height) -> scene ids
    for t0, _, s in scene_times(sb):
        if cap.get("words") and cap.get("enabled", True):
            for y in caption_ys(s, style, sb):
                caps.setdefault((round((y + half2) * 100, 1), round((y + half1) * 100, 1)), []).append(s.get("id"))
        for l in s.get("layers", []):
            is_text = l.get("type") == "text" or (l.get("type") == "component" and TEXT_LAYER.search(l.get("name", "")))
            box = layer_box(l, W, H) if is_text else None
            if not box:
                continue
            fixed = float(l.get("depth", 1)) == 0 or not _zooming(s) and not (s.get("camera") or {}).get("keyframes")
            bottom = box[3] / H
            item = {"t": round(t0, 2), "scene_id": s.get("id"), "what": l.get("name") or "text",
                    "bottom_pct": round(bottom * 100, 1), "screen_fixed": fixed}
            if bottom > SAFE_FAIL and fixed:
                fails.append(item)
            elif bottom > SAFE_WARN:
                warns.append(item)
            elif l.get("type") == "text" and fixed and (box[0] < EDGE * W or box[2] > (1 - EDGE) * W):
                # only plain text layers: a component's box is a container wider than the text it draws
                warns.append({**item, "issue": f"text box within {int(EDGE * 100)} % of the edge"})
    for (bottom, bottom1), ids in sorted(caps.items()):
        item = {"what": "captions", "bottom_pct": bottom, "one_line_bottom_pct": bottom1,
                "scenes": ids if len(ids) < len(sb.get("scenes", [])) else "all"}
        if bottom1 > SAFE_FAIL * 100:
            fails.append(item)
        elif bottom > SAFE_WARN * 100:
            warns.append(item)
    st = "FAIL" if fails else "WARN" if warns else "PASS"
    return chk(st, fails + warns, f"FAIL: screen-fixed text, or a 1-line caption page, ending below {int(SAFE_FAIL * 100)} % "
               f"of the height; WARN: anything (2-line captions) below {int(SAFE_WARN * 100)} %, or a text layer within {int(EDGE * 100)} % of an edge",
               f"{len(fails)} fail, {len(warns)} warn (storyboard geometry; camera moves are not modelled)")


def check_captions(sb: dict, bm: dict | None) -> dict:
    W, H = frame_size(sb)
    cap = sb.get("captions") or {}
    style = cap.get("style") or {}
    issues = []
    for w in cap.get("words", []):
        if w.get("emph") and textsim.norm(w.get("text", "")) in STOPWORDS:
            issues.append({"t": w.get("start"), "issue": f"red emphasis on stopword {w.get('text')!r}"})
    for s in (bm or {}).get("scenes", []):
        for pg in s.get("caption_pages", []):
            n = len(str(pg.get("text", "")).split())
            if n > 4:
                issues.append({"t": pg.get("t0"), "scene_id": s.get("scene_id"), "issue": f"caption page of {n} words"})
    ch = float(style.get("fontSize", 84 if sb.get("format") == "16:9" else 104)) * 1.15
    for t0, _, s in scene_times(sb):
        if _zooming(s) or (s.get("camera") or {}).get("keyframes"):
            continue  # camera moves the subject: the reviewer checks these on the sheets
        for y in caption_ys(s, style, sb):
            cb = (0.09 * W, y * H - ch, 0.91 * W, y * H + ch)
            for l in s.get("layers", []):
                if l.get("type") != "component" or CREATURE_SKIP.search(l.get("name", "")):
                    continue
                b = layer_box(l, W, H)
                if not b:
                    continue
                ix = max(0.0, min(cb[2], b[2]) - max(cb[0], b[0]))
                iy = max(0.0, min(cb[3], b[3]) - max(cb[1], b[1]))
                share = ix * iy / ((cb[2] - cb[0]) * (cb[3] - cb[1]))
                if share > 0.4:
                    issues.append({"t": round(t0, 2), "scene_id": s.get("id"),
                                   "issue": f"caption band overlaps {l.get('name')} ({share:.0%})"})
    return chk("WARN" if issues else "PASS", issues[:12], "any (the reviewer decides)",
               f"{len(issues)} issue(s)" + (" (first 12 shown)" if len(issues) > 12 else ""))


def max_hold(sb: dict) -> float | None:
    try:
        from pipeline.episodes.common import visual_events
    except Exception:
        return None
    worst = 0.0
    for s in sb.get("scenes", []):
        ev = visual_events(s)
        worst = max([worst] + [b - a for a, b in zip(ev, ev[1:])])
    return round(worst, 2)


# ---------------------------------------------------------------------------------------------- text checks

def _longest_run(a: list[str], b: list[str], k: int) -> int:
    """Longest run of consecutive words of a that occurs in b (0 if shorter than k)."""
    if len(a) < k or len(b) < k:
        return 0
    grams = {tuple(b[i:i + k]) for i in range(len(b) - k + 1)}
    bj = " " + " ".join(b) + " "
    best, i = 0, 0
    while i + k <= len(a):
        if tuple(a[i:i + k]) in grams:
            n = k
            while i + n < len(a) and " " + " ".join(a[i:i + n + 1]) + " " in bj:
                n += 1
            best = max(best, n)
            i += n
        else:
            i += 1
    return best


def source_transcript(r, slug: str, src: dict, fm: dict, niche: str):
    sid = src.get("source_id") or (fm.get("_references") or [None])[0]
    cands = []
    if src.get("transcript_file"):
        cands.append(r / src["transcript_file"])
    if sid:
        cands += [r / "research/library/transcripts" / f"{sid}.txt",
                  r / "research/corpus" / niche / "raw" / f"{sid}.txt",
                  r / "research/corpus" / niche / "auto/raw" / f"{sid}.txt",
                  r / "research/corpus" / niche / "auto" / f"{sid}.md",
                  r / "research/corpus" / niche / f"{sid}.md"]
    for c in cands:
        if c.is_file():
            return sid, c
    return sid, None


def check_originality(r, slug: str, script, src: dict, fm: dict, niche: str) -> dict:
    mod = originality_module()
    ws = mod.words(mod.script_text(str(script)))
    if not ws:
        return chk("FAIL", None, detail="empty narration")
    grams = mod.ngrams(ws, mod.NGRAM)
    best = {"max_run": 0, "max_5gram_share": 0.0, "worst": None}
    fails = []
    for d in (r / "research/corpus", r / "research/library/transcripts"):
        for p in sorted(d.rglob("*")) if d.is_dir() else []:
            if p.suffix not in (".txt", ".md", ".json") or not p.is_file() or p.resolve() == script.resolve():
                continue
            sw = mod.words(mod.source_text(p))
            if len(sw) < mod.NGRAM:
                continue
            share = len(grams & mod.ngrams(sw, mod.NGRAM)) / max(1, len(grams))
            runlen = _longest_run(ws, sw, 5)
            if (runlen, share) > (best["max_run"], best["max_5gram_share"]):
                best.update(max_run=runlen, max_5gram_share=round(share, 4), worst=rel(r, p))
            if runlen >= mod.RUN_LIMIT or share >= mod.NGRAM_LIMIT:
                fails.append(f"{rel(r, p)}: run {runlen}, {share:.1%} 5-grams")
    sid, tp = source_transcript(r, slug, src, fm, niche)
    val = {**best, "source_id": sid, "source_transcript": rel(r, tp)}
    detail = []
    st = "FAIL" if fails else "PASS"
    if fails:
        detail.append("corpus: " + "; ".join(fails[:5]))
    if tp:
        sw = mod.words(mod.source_text(tp))
        sshare = len(grams & mod.ngrams(sw, mod.NGRAM)) / max(1, len(grams))
        srun = _longest_run(ws, sw, 3)
        val.update(vs_source_5gram_share=round(sshare, 4), vs_source_run=srun)
        if sshare >= SRC_SHARE_FAIL or srun >= SRC_RUN_FAIL:
            st = "FAIL"
            detail.append(f"vs source {sid}: {sshare:.1%} 5-grams, run {srun} words")
    else:
        if st == "PASS":
            st = "WARN"
        detail.append(f"source transcript for {sid} not found: compared with the corpus only")
    thr = (f"corpus: run < {mod.RUN_LIMIT} and 5-gram share < {mod.NGRAM_LIMIT:.0%} per source; "
           f"source: share < {SRC_SHARE_FAIL:.0%} and run < {SRC_RUN_FAIL}")
    return chk(st, val, thr, "; ".join(detail))


def first_speech(r, slug: str, sb: dict) -> float | None:
    cj = read_json(r / "episodes" / slug / "audio" / "captions.json") or {}
    ws = cj.get("words") if isinstance(cj, dict) else cj
    ws = ws or (sb.get("captions") or {}).get("words") or []
    return float(ws[0]["start"]) if ws else None


def speech_words(r, slug: str, sb: dict) -> list[dict]:
    cj = read_json(r / "episodes" / slug / "audio" / "captions.json") or {}
    ws = cj.get("words") if isinstance(cj, dict) else cj
    return ws or (sb.get("captions") or {}).get("words") or []


def check_disclosure(r, slug: str) -> dict:
    pkg = read_json(r / "episodes" / slug / "package.json") or {}
    texts = [("package.json", " ".join(str(pkg.get(k, "")) for k in ("yt_description", "short_caption")))]
    dm = episode_file(r, slug, "description.md")
    if dm:
        texts.append((rel(r, dm), dm.read_text(encoding="utf-8")))
    for where, t in texts:
        m = DISCLOSURE.search(t)
        if m:
            return chk("PASS", where, detail=f"AI-voice line found ({m.group(0)!r})")
    return chk("FAIL", None, "AI-voice disclosure line in package.json or description.md",
               "missing: add 'Narration: synthetic AI voice (Kokoro TTS)...'")


def check_variant(r, slug: str, var: dict, fp: dict, hook_words: int, wpm: float | None, hold: float | None,
                  bm: dict | None, duration: float) -> dict:
    vs = (var or {}).get("variables") or {}
    if not vs:
        return chk("PASS", {}, detail="no variant.json variables")
    measured, off = {}, []

    def num(key, got):
        want = vs.get(key)
        if want is None or got is None:
            return
        measured[key] = round(got, 2)
        if key in ("hook.max_words", "visual.max_hold_s"):
            bad = got > float(want) * (1 + VARIANT_TOL)
        else:
            bad = abs(got - float(want)) > abs(float(want)) * VARIANT_TOL
        if bad:
            off.append(f"{key}: wanted {want}, measured {round(got, 2)}")

    num("hook.max_words", hook_words)
    num("pace.wpm", wpm)
    num("visual.max_hold_s", hold)
    if bm and bm.get("scenes"):
        segs, last = [], None
        for s in bm["scenes"]:
            key = (s.get("beat"), s.get("skeleton_i"))
            if key != last:
                segs.append([s.get("t0", 0), s.get("t1", 0), str(s.get("beat", "")).upper()])
                last = key
            else:
                segs[-1][1] = s.get("t1", segs[-1][1])
        body = [b - a for a, b, lab in segs if lab != "HOOK"]
        if body:
            num("pace.rehook_s", sum(body) / len(body))
        turn = next((a for a, b, lab in segs if lab in ("TURN", "S4", "TURNSTILE")), None)
        if turn is not None and duration:
            num("structure.turnstile_pct", turn / duration * 100)
    if "visual.shot_mix" in vs:
        measured["visual.shot_mix"] = fp.get("shot_mix_class")
        if vs["visual.shot_mix"] != fp.get("shot_mix_class"):
            off.append(f"visual.shot_mix: wanted {vs['visual.shot_mix']}, measured {fp.get('shot_mix_class')}")
    unmeasured = sorted(k for k in vs if k not in measured)
    return chk("WARN" if off else "PASS", measured, f"off by > {int(VARIANT_TOL * 100)} %",
               "; ".join(off) + (("; " if off else "") + f"not measured: {', '.join(unmeasured)}" if unmeasured else ""))


# ---------------------------------------------------------------------------------------------- main

def gate(slug: str, r, last_n=None, against=None, mp4=None, sheets=True, source_frames="auto", log=print) -> dict:
    t_start = time.time()
    ep = r / "episodes" / slug
    mp4 = mp4 or find_mp4(r, slug)
    if not mp4:
        raise FileNotFoundError(f"no MP4 for {slug} (out/{slug}/{slug}_9x16.mp4 or out/pilots/{slug}/)")
    script = ep / "script.md"
    if not script.is_file():
        raise FileNotFoundError(f"no script: {rel(r, script)}")
    sb = read_json(ep / "storyboard.json") or {}
    bm = read_json(ep / "beatmap.json")
    src = read_json(ep / "source.json") or {}
    var = read_json(ep / "variant.json") or {}
    fm = front_matter(script.read_text(encoding="utf-8"))
    niche = fm.get("niche") or "explainer"
    rl = rules(r)
    vv = var.get("variables") or {}
    max_hold_s = float(vv.get("visual.max_hold_s", rl["visual.max_hold_s"]))
    hook_max = int(vv.get("hook.max_words", rl["hook.max_words"]))
    checks = {}

    dur = probe_duration(mp4)
    checks["duration"] = chk("FAIL" if dur < DUR_MIN else "WARN" if dur > DUR_WARN else "PASS", round(dur, 2),
                             f">= {DUR_MIN} (WARN > {DUR_WARN})")
    log(f"duration {dur:.2f} s")

    audio = has_audio_stream(mp4)
    av = scan_av(mp4, max_hold_s + 0.5, audio)
    lo = av["loud"]
    if not audio or lo.get("I_lufs") is None:
        checks["loudness"] = chk("FAIL", lo, detail="no audio stream" if not audio else "ebur128 gave no reading")
    else:
        i, tp = lo["I_lufs"], lo.get("true_peak_dbtp")
        st = "FAIL" if abs(i - LUFS_TARGET) > LUFS_TOL or (tp is not None and tp > TP_FAIL) else \
             "WARN" if tp is not None and tp > TP_WARN else "PASS"
        checks["loudness"] = chk(st, lo, f"I {LUFS_TARGET} +-{LUFS_TOL} LUFS, true peak <= {TP_FAIL} dBTP (WARN > {TP_WARN})")
    log(f"loudness {lo}")

    times = scene_times(sb)
    bad_black, ok_black = [], []
    for b in av["black"]:
        if b["d"] <= BLACK_FAIL_S:
            ok_black.append({**b, "why": "short"})
            continue
        intended = []
        for t0, t1, s in times:
            if t1 <= b["t0"] or t0 >= b["t1"]:
                continue
            names = [l.get("name", "") for l in s.get("layers", [])]
            if s.get("intendedBlack") or s.get("black_ok") or any(re.search(r"/(Darkness|EndCard)$", n) for n in names) \
                    or (s.get("transitionIn") or {}).get("type") == "dipBlack" and abs(t0 - b["t0"]) < 1.0:
                intended.append(s.get("id"))
        (ok_black if intended else bad_black).append({**b, "scenes": intended} if intended else b)
    log("sampling frames at 1 fps")
    samples = frames.sample_video(mp4)
    blanks = [i for i, f in enumerate(samples) if frames.is_blank(f)]
    st = "FAIL" if bad_black else "WARN" if blanks else "PASS"
    checks["black_frames"] = chk(st, bad_black, f"no black run > {BLACK_FAIL_S} s unless the scene marks it intended",
                                 (f"intended/short: {ok_black}; " if ok_black else "") +
                                 (f"near-uniform frames at {blanks} s" if blanks else ""))

    hold = max_hold(sb)
    fr = [{"t0": f["t0"], "t1": f["t1"] if f["t1"] is not None else round(dur, 2)} for f in av["freeze"]]
    checks["frozen"] = chk("FAIL" if fr else "PASS", fr, f"no freeze > visual.max_hold_s + 0.5 = {max_hold_s + 0.5:.1f} s",
                           f"storyboard max hold {hold} s" if hold is not None else "")

    shares = [frames.magenta_share(f) for f in samples]
    worst = max(shares) if shares else 0.0
    worst_t = shares.index(worst) if shares else None
    checks["missing_kit"] = chk("FAIL" if worst > MAGENTA_FAIL else "PASS", round(worst, 5),
                                f"magenta share <= {MAGENTA_FAIL:.1%} in every 1 fps frame",
                                f"worst frame t={worst_t} s" if worst > 0 else "magenta pixel share in sampled frames")

    log("originality")
    checks["originality"] = check_originality(r, slug, script, src, fm, niche)

    log("fingerprint + sameness")
    fp = fpmod.build(slug, r, samples=samples, duration_s=round(dur, 2))
    fpmod.save(r, fp)
    checks["sameness"] = sameness.run(r, slug, fp, last_n, against)

    checks["captions"] = check_captions(sb, bm)
    checks["safe_area"] = check_safe_area(sb)

    paras = narration_paragraphs(script)
    hook = hook_text(paras)
    hw = len(textsim.words(hook))
    fs = first_speech(r, slug, sb)
    hs = "FAIL" if fs is None or fs > FIRST_SPEECH_FAIL else "WARN" if hw > hook_max else "PASS"
    checks["hook"] = chk(hs, {"words": hw, "first_speech_s": fs, "text": hook},
                         f"first speech <= {FIRST_SPEECH_FAIL} s (WARN words > hook.max_words {hook_max})")

    checks["disclosure"] = check_disclosure(r, slug)

    sw = speech_words(r, slug, sb)
    wpm = (len(sw) / (sw[-1]["end"] - sw[0]["start"]) * 60) if len(sw) > 1 and sw[-1]["end"] > sw[0]["start"] else None
    checks["variant"] = check_variant(r, slug, var, fp, hw, wpm, hold, bm, dur)

    out_sheets = {}
    if sheets:
        log("sheets")
        from . import sheet
        out_sheets = sheet.make_all(r, slug, mp4, samples, dur, sb, bm, src, fm, niche,
                                    source_frames=source_frames)
    verdict = "FAIL" if any(c["status"] == "FAIL" for c in checks.values()) else "PASS"
    return {
        "v": 1, "slug": slug, "at": now_iso(), "verdict": verdict,
        "warn_count": sum(c["status"] == "WARN" for c in checks.values()),
        "fail": [k for k, c in checks.items() if c["status"] == "FAIL"],
        "mp4": rel(r, mp4), "mp4_sha256": sha256(mp4), "duration_s": round(dur, 2), "niche": niche,
        "checks": checks, "sheets": {k: rel(r, v) for k, v in out_sheets.items()},
        "gate_s": round(time.time() - t_start, 1),
    }


def summary(g: dict) -> str:
    lines = [f"{g['slug']}: {g['verdict']} ({g.get('warn_count', 0)} warn) {g.get('mp4', '')}"]
    for k, c in g.get("checks", {}).items():
        v = c.get("value")
        if k == "sameness":
            v = (v or {}).get("max")
        s = json.dumps(v, ensure_ascii=False)
        lines.append(f"  {c['status']:4} {k:12} {s[:150]}{'...' if len(s) > 150 else ''}"
                     + (f"  | {c['detail'][:220]}" if c.get("detail") else ""))
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.qa.gate")
    ap.add_argument("slug")
    ap.add_argument("--root")
    ap.add_argument("--last-n", type=int)
    ap.add_argument("--against", help="comma-separated slugs to compare with instead of the posts.jsonl history")
    ap.add_argument("--mp4", help="override the MP4 path")
    ap.add_argument("--source-frames", choices=["auto", "none"], default="auto")
    ap.add_argument("--no-sheets", action="store_true")
    ap.add_argument("--json", action="store_true", help="print gate.json instead of the summary")
    a = ap.parse_args(argv)
    be_nice()
    r = root(a.root)
    qd = qa_dir(r, a.slug)
    qd.mkdir(parents=True, exist_ok=True)
    logf = open(qd / "gate.log", "a", encoding="utf-8")

    def log(msg):
        logf.write(f"{now_iso()} {msg}\n")
        logf.flush()

    log(f"gate {a.slug} root={r}")
    try:
        import pathlib
        g = gate(a.slug, r, a.last_n, a.against.split(",") if a.against is not None else None,
                 pathlib.Path(a.mp4) if a.mp4 else None, not a.no_sheets, a.source_frames, log)
    except Exception as e:  # never leave an older PASS behind for a file we could not check
        log("ERROR " + traceback.format_exc())
        write_json(qd / "gate.json", {"v": 1, "slug": a.slug, "at": now_iso(), "verdict": "ERROR", "error": str(e)})
        print(f"{a.slug}: ERROR {e}", file=sys.stderr)
        return 1
    write_json(qd / "gate.json", g)
    log(f"verdict {g['verdict']} fail={g['fail']} warn={g['warn_count']} in {g['gate_s']} s")
    print(json.dumps(g, indent=1, ensure_ascii=False) if a.json else summary(g))
    return 0 if g["verdict"] == "PASS" else 6


if __name__ == "__main__":
    sys.exit(main())
