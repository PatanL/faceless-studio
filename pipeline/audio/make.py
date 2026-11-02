"""One command: script -> voice (TTS) -> word timings -> captions JSON -> ducked, -14 LUFS mix.

usage (Spark, from ~/studio/app):
  source scripts/spark_env.sh
  python -m pipeline.audio.make stories/x/script.md --niche horror --id ep-x
      [--out studio/public/episodes/ep-x] [--music dread|none] [--voice bm_george] [--speed 1.0]
      [--no-auto-sfx] [--whisper] [--meta-out episodes/ep-x/audio]
      [--extra-cues episodes/ep-x/audio/sfx_events.json] [--reuse-tts]

  --extra-cues  JSON list [{cue, at, db?, rate?}] added to the mix (e.g. the storyboard's action SFX from
                pipeline.episodes.sfx_events: drops, pops, punches, light events, transitions). rate = pitch variant.
  --reuse-tts   reuse the voice + word timings cached by the previous run in --out (tts_cache.npz / tts_cache.json),
                so a remix with new cues never changes the timings the storyboard was built on.

Writes to --out (default studio/public/episodes/<id>/, so Remotion can load it):
  mix.wav                 final stereo mix, 48 kHz, -14 LUFS integrated, <= -1 dBTP
  voice.wav music.wav sfx.wav   stems at mix gain (sum ~= mix before limiting)
  captions.json           {"words":[{text,start,end}...]} -> storyboard captions.src (B2 schema Word)
  cues.json               [{cue, at, db, source, dur, level_db}] global seconds (for visual sync: shake on impact...)
  audio.storyboard.json   {"captions": {...}, "audio": {...}} fragments to paste into a storyboard
  report.json             TTS speed, timing source/coverage, LUFS (pyloudnorm + ffmpeg ebur128), duck depth
  waveform.png            stacked voice / music / sfx / mix waveforms (visual check of ducking + cues)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""

from .config import NICHES
from .mix import PUBLIC, ROOT, mix
from .script import parse
from .tts import auto_cues, synthesize


def waveform_png(paths: dict, out_png: str, cues: list[dict], dur: float):
    """Stacked waveforms (top to bottom: voice, music, sfx, mix), red ticks at cues, white ticks each second."""
    w, h = 1800, 180
    inputs, filt = [], []
    order = [("voice", "0x7fd3ff"), ("music", "0xffb347"), ("sfx", "0xff5c7a"), ("mix", "0xe8e8e8")]
    for i, (k, col) in enumerate(order):
        inputs += ["-i", paths[k]]
        filt.append(f"[{i}:a]aformat=channel_layouts=mono,showwavespic=s={w}x{h}:colors={col}:scale=sqrt,"
                    f"drawbox=x=0:y=0:w={w}:h={h}:color=0x333333:t=1[w{i}]")
    filt.append("".join(f"[w{i}]" for i in range(len(order))) + f"vstack=inputs={len(order)}[st]")
    ticks = "".join(f",drawbox=x={int(c['at'] / dur * w)}:y=0:w=2:h={h * 4}:color=0xff5c7a@0.6:t=fill" for c in cues)
    secs = "".join(f",drawbox=x={int(t / dur * w)}:y={h * 4 - 12}:w=1:h=12:color=white:t=fill" for t in range(int(dur) + 1))
    filt.append(f"color=c=0x14161b:s={w}x{h * len(order)}[bg];[bg][st]overlay=shortest=1{ticks}{secs}[out]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
                    "-map", "[out]", "-frames:v", "1", out_png], check=True)


def cut_cues(sc, words: list[dict], cfg: dict, existing: list[dict]) -> list[dict]:
    """Transition SFX on scene cuts (one narration paragraph = one scene, cut ~0.15 s before its first word).
    cfg["cut_sfx"] = {"cues": [names, rotated], "lead": s before the first word, "db": level offset}; a cut that
    already has a marker cue within 0.6 s gets none (impacts/stingers carry their own cut)."""
    spec = cfg.get("cut_sfx")
    if not spec:
        return []
    names, lead, db = spec["cues"], float(spec.get("lead", 0.35)), float(spec.get("db", 0.0))
    out, idx, k = [], 0, 0
    for si, seg in enumerate(sc.segments):
        n = len(seg.words)
        if si > 0 and n and idx < len(words):
            t = round(max(0.0, words[idx]["start"] - lead), 3)
            if not any(abs(c["at"] - t) < 0.6 for c in existing):
                out.append({"cue": names[k % len(names)], "at": t, "db": db, "source": "cut"})
                k += 1
        idx += n
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script")
    ap.add_argument("--niche", choices=sorted(NICHES))
    ap.add_argument("--id")
    ap.add_argument("--out")
    ap.add_argument("--music", help="bed name in studio/public/music, a path, or 'none'")
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--engine", choices=["kokoro", "piper"])
    ap.add_argument("--no-auto-sfx", action="store_true")
    ap.add_argument("--whisper", action="store_true", help="force faster-whisper alignment")
    ap.add_argument("--meta-out", help="also copy the small JSON outputs here (e.g. episodes/<id>/audio)")
    ap.add_argument("--extra-cues", help="JSON list of extra SFX cues [{cue, at, db?, rate?}] (storyboard action SFX)")
    ap.add_argument("--reuse-tts", action="store_true", help="reuse the cached voice/timings from the previous run in --out")
    a = ap.parse_args(argv)

    t0 = time.time()
    src = open(a.script, encoding="utf-8").read()
    sc = parse(src)
    niche = a.niche or sc.meta.get("niche") or "explainer"
    cfg = dict(NICHES[niche])
    for k in ("voice", "speed", "engine"):
        v = getattr(a, k) or sc.meta.get(k)
        if v:
            cfg[k] = float(v) if k == "speed" else v
    for k in ("paragraph_pause", "music_db", "duck_db"):  # per-script overrides (front matter)
        if sc.meta.get(k) not in (None, ""):
            cfg[k] = float(sc.meta[k])
    if str(sc.meta.get("ending", "")).lower() == "loop":  # Shorts loop: cut ~0.3 s after the last word, bed not faded
        cfg.update(cfg.get("loop_ending", {}))
    if cfg["voice"].startswith("b") and cfg["engine"] == "kokoro":
        cfg["lang"] = "b"
    elif cfg["engine"] == "kokoro":
        cfg["lang"] = "a"
    ep = a.id or sc.meta.get("id") or os.path.splitext(os.path.basename(a.script))[0]
    out = a.out or os.path.join(PUBLIC, "episodes", ep)
    os.makedirs(out, exist_ok=True)

    music = a.music if a.music is not None else (sc.music if sc.music is not None else cfg["music"])
    if music in ("none", "off"):
        music = ""

    cache_a, cache_j = os.path.join(out, "tts_cache.npz"), os.path.join(out, "tts_cache.json")
    if a.reuse_tts:
        import numpy as np
        if not (os.path.exists(cache_a) and os.path.exists(cache_j)):
            raise SystemExit(f"--reuse-tts: no cached voice in {out} (run once without --reuse-tts)")
        tts = {**json.load(open(cache_j)), "audio": np.load(cache_a)["audio"]}
        print(f"[make] reusing cached voice ({len(tts['words'])} words) from {out}")
    else:
        tts = synthesize(sc, cfg, force_whisper=a.whisper)
        import numpy as np
        np.savez_compressed(cache_a, audio=tts["audio"])
        json.dump({k: tts[k] for k in ("words", "cues", "stats")}, open(cache_j, "w"))
    cues = sorted(tts["cues"], key=lambda c: c["at"])
    if not a.no_auto_sfx:
        cues = sorted(cues + auto_cues(tts["words"], cfg.get("auto_sfx", {}), cues, in_speech_db=cfg.get("auto_sfx_db")), key=lambda c: c["at"])
    if not a.no_auto_sfx:
        cues = sorted(cues + cut_cues(sc, tts["words"], cfg, cues), key=lambda c: c["at"])
    if a.extra_cues:
        extra = [c for c in json.load(open(a.extra_cues)) if c.get("cue")]
        # an action cue never doubles a script/auto cue already within 0.25 s
        extra = [c for c in extra if not any(abs(c["at"] - o["at"]) < 0.25 for o in cues)]
        cues = sorted(cues + [{**c, "source": c.get("source", "storyboard")} for c in extra], key=lambda c: c["at"])
    mx = mix(tts["audio"], cues, cfg, music, out)
    dur = mx["report"]["duration_s"]

    rel = os.path.relpath(out, PUBLIC) if os.path.abspath(out).startswith(PUBLIC + os.sep) else None
    json.dump({"words": tts["words"], "source": tts["stats"]["timing_source"], "voice": cfg["voice"]},
              open(os.path.join(out, "captions.json"), "w"), indent=1)
    json.dump(mx["report"]["sfx_placed"], open(os.path.join(out, "cues.json"), "w"), indent=1)
    frag = {
        "_note": "paths are relative to studio/public. 'audio' plays the finished mix (music+sfx baked in, "
                 "so duckOn none); 'audio_stems' lets Remotion mix the stems instead.",
        "duration_s": dur,
        "captions": {"src": f"{rel}/captions.json" if rel else None},
        "audio": {"voice": [{"src": f"{rel}/mix.wav" if rel else None, "start": 0, "volume": 1, "duration": dur}],
                  "music": [], "sfx": [], "duckOn": "none"},
        "audio_stems": {
            "voice": [{"src": f"{rel}/voice.wav", "start": 0, "volume": 1, "duration": dur}],
            "music": [{"src": f"{rel}/music.wav", "start": 0, "volume": 1, "duckTo": 1, "loop": False, "fadeIn": 0, "fadeOut": 0}],
            "sfx": [{"src": f"{rel}/sfx.wav", "at": 0, "volume": 1}],
            "duckOn": "none",
        } if rel else None,
        "cues": [{"cue": c["cue"], "at": c["at"]} for c in mx["report"]["sfx_placed"]],
    }
    json.dump(frag, open(os.path.join(out, "audio.storyboard.json"), "w"), indent=1)
    try:
        waveform_png(mx["paths"], os.path.join(out, "waveform.png"), mx["report"]["sfx_placed"], dur)
    except subprocess.CalledProcessError as e:
        print("[make] waveform.png failed:", e, file=sys.stderr)
    report = {"id": ep, "niche": niche, "script": os.path.relpath(os.path.abspath(a.script), ROOT),
              "tts": tts["stats"], "mix": mx["report"], "words": len(tts["words"]),
              "wall_s": round(time.time() - t0, 1)}
    json.dump(report, open(os.path.join(out, "report.json"), "w"), indent=1)
    if a.meta_out:
        os.makedirs(a.meta_out, exist_ok=True)
        for f in ("captions.json", "cues.json", "audio.storyboard.json", "report.json", "waveform.png"):
            if os.path.exists(os.path.join(out, f)):
                shutil.copy(os.path.join(out, f), a.meta_out)
    print(f"[make] {ep}: {dur}s, {len(tts['words'])} words, {len(cues)} cues -> {out} ({report['wall_s']}s)")


if __name__ == "__main__":
    main(sys.argv[1:])
