"""Narration -> 48 kHz mono voice track + word timings + SFX cue times.

Kokoro-82M (CPU) gives per-token timestamps; tokens are merged into words and aligned to the
script's own words, so captions show exactly the script text. If the engine gives no usable
timings (Piper, or Kokoro coverage < 60 %), faster-whisper (CPU, int8) aligns instead.
"""
from __future__ import annotations

import difflib
import os
import re
import subprocess
import tempfile
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # never the GPU

import numpy as np
from scipy.signal import resample_poly

from .config import SR
from .script import Script, Segment, split_on_pauses

LEAD_IN = 0.25   # silence before the first word
TAIL = 0.6       # silence after the last word
TRIM_DB = -40.0  # trailing audio quieter than this (dBFS) counts as silence when trimming a chunk
TRIM_KEEP = 0.12 # keep at most this much trailing silence per chunk (Kokoro leaves ~0.7 s)


def trim_tail(a48, keep=TRIM_KEEP, thresh_db=TRIM_DB):
    """Cut a chunk's trailing silence to <= keep seconds (20 ms windows below thresh_db)."""
    win = int(0.02 * SR)
    if len(a48) < win * 4:
        return a48
    th = 10 ** (thresh_db / 20)
    n = len(a48) // win
    rms = np.sqrt(np.mean(a48[: n * win].reshape(n, win) ** 2, axis=1))
    loud = np.nonzero(rms > th)[0]
    if not len(loud):
        return a48
    end = min(len(a48), (loud[-1] + 1) * win + int(keep * SR))
    return a48[:end]

def trim_head(a48, keep=0.03, thresh_db=TRIM_DB):
    """Cut a chunk's leading silence to <= keep seconds (so the voice starts right after the lead-in)."""
    win = int(0.02 * SR)
    if len(a48) < win * 4:
        return a48
    th = 10 ** (thresh_db / 20)
    n = len(a48) // win
    rms = np.sqrt(np.mean(a48[: n * win].reshape(n, win) ** 2, axis=1))
    loud = np.nonzero(rms > th)[0]
    if not len(loud):
        return a48
    return a48[max(0, loud[0] * win - int(keep * SR)):]


_PIPES: dict = {}


def _norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def _kokoro(text: str, voice: str, lang: str, speed: float):
    """-> (audio float32 @24k, [(word_text, start, end)])"""
    import torch
    torch.set_num_threads(int(os.environ.get("TTS_THREADS", "6")))
    from kokoro import KPipeline
    if lang not in _PIPES:
        _PIPES[lang] = KPipeline(lang_code=lang, device="cpu")
    pipe = _PIPES[lang]
    chunks, words, offset = [], [], 0.0
    for r in pipe(text, voice=voice, speed=speed, split_pattern=None):
        audio = r.audio.numpy() if hasattr(r.audio, "numpy") else np.asarray(r.audio)
        cur = None
        for tok in (r.tokens or []):
            if cur is None:
                cur = {"t": "", "s": None, "e": None}
            cur["t"] += tok.text
            if tok.start_ts is not None and tok.end_ts is not None and _norm(tok.text):
                s, e = offset + tok.start_ts, offset + tok.end_ts
                cur["s"] = s if cur["s"] is None else min(cur["s"], s)
                cur["e"] = e if cur["e"] is None else max(cur["e"], e)
            if tok.whitespace:
                words.append(cur)
                cur = None
        if cur is not None:
            words.append(cur)
        chunks.append(audio.astype(np.float32))
        offset += len(audio) / 24000
    audio = np.concatenate(chunks) if chunks else np.zeros(0, np.float32)
    return audio, 24000, [(w["t"], w["s"], w["e"]) for w in words if _norm(w["t"])]


_SENT_END = re.compile(r"(?<=[.!?…])[\"”’)]*\s+")


def _kokoro_sentences(text: str, voice: str, lang: str, speed: float, gap: float):
    """Natural-pause mode: one Kokoro call per sentence, each trimmed, joined by `gap` s of silence.
    Whole-paragraph calls run sentences together and sound read-out (owner's blind test, 2026-11-01).
    -> (audio float32 @48k, [(word_text, start, end)])"""
    parts = [p.strip() for p in _SENT_END.split(text.strip()) if p.strip()]
    if len(parts) <= 1:
        a, sr, timed = _kokoro(text, voice, lang, speed)
        return _to48(a, sr), SR, timed
    pieces, timed_all, cur = [], [], 0.0
    for i, part in enumerate(parts):
        a, sr, timed = _kokoro(part, voice, lang, speed)
        a48 = _to48(a, sr)
        n0 = len(a48)
        a48 = trim_head(a48, keep=0.03)
        cut = (n0 - len(a48)) / SR
        a48 = trim_tail(a48)
        for w_, s_, e_ in timed:
            timed_all.append((w_, None if s_ is None else cur + max(0.0, s_ - cut),
                              None if e_ is None else cur + max(0.0, e_ - cut)))
        pieces.append(a48)
        cur += len(a48) / SR
        if i < len(parts) - 1:
            pieces.append(np.zeros(int(gap * SR), np.float32))
            cur += int(gap * SR) / SR
    return np.concatenate(pieces), SR, timed_all


def _piper(text: str, voice: str):
    from piper import PiperVoice
    path = voice if voice.endswith(".onnx") else os.path.join(
        os.environ.get("STUDIO_PIPER_VOICES", os.path.expanduser("~/studio/models/piper")), voice + ".onnx")
    key = ("piper", path)
    if key not in _PIPES:
        _PIPES[key] = PiperVoice.load(path)
    pv = _PIPES[key]
    parts = [c.audio_float_array for c in pv.synthesize(text)]
    return np.concatenate(parts).astype(np.float32), pv.config.sample_rate, []


_WHISPER = None


def whisper_words(audio48: np.ndarray):
    """faster-whisper word timings on a 48 kHz mono array -> [(text, start, end)]."""
    global _WHISPER
    from faster_whisper import WhisperModel
    if _WHISPER is None:
        _WHISPER = WhisperModel(os.environ.get("WHISPER_MODEL", "base.en"), device="cpu",
                                compute_type="int8", cpu_threads=int(os.environ.get("TTS_THREADS", "6")))
    a16 = resample_poly(audio48, 1, 3).astype(np.float32)
    segs, _ = _WHISPER.transcribe(a16, word_timestamps=True, beam_size=1)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]


def align(script_words: list[str], timed: list[tuple], seg_dur: float):
    """Give every script word a (start, end) using the timed words of the engine/whisper."""
    a = [_norm(w) for w in script_words]
    b = [_norm(t[0]) for t in timed]
    times: list = [None] * len(a)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                s, e = timed[j1 + k][1], timed[j1 + k][2]
                if s is not None and e is not None:
                    times[i1 + k] = (s, e)
        elif tag == "replace":  # e.g. "2,000" vs "two thousand": spread the span evenly
            ss = [timed[j][1] for j in range(j1, j2) if timed[j][1] is not None]
            ee = [timed[j][2] for j in range(j1, j2) if timed[j][2] is not None]
            if ss and ee:
                s0, e0 = min(ss), max(ee)
                n = i2 - i1
                for k in range(n):
                    times[i1 + k] = (s0 + (e0 - s0) * k / n, s0 + (e0 - s0) * (k + 1) / n)
    matched = sum(t is not None for t in times)
    # interpolate the gaps
    i = 0
    while i < len(times):
        if times[i] is None:
            j = i
            while j < len(times) and times[j] is None:
                j += 1
            lo = times[i - 1][1] if i > 0 else 0.0
            hi = times[j][0] if j < len(times) else seg_dur
            n = j - i
            for k in range(n):
                times[i + k] = (lo + (hi - lo) * k / n, lo + (hi - lo) * (k + 1) / n)
            i = j
        else:
            i += 1
    return times, (matched / len(a) if a else 1.0)


def _to48(audio, sr):
    if sr == SR:
        return audio
    from math import gcd
    g = gcd(SR, sr)
    return resample_poly(audio, SR // g, sr // g).astype(np.float32)


def voice_chain(audio48: np.ndarray, chain: str) -> np.ndarray:
    """Run an ffmpeg -af chain over the voice (EQ / compression / room). Length is preserved."""
    if not chain:
        return audio48
    import soundfile as sf
    with tempfile.TemporaryDirectory() as d:
        src, dst = os.path.join(d, "in.wav"), os.path.join(d, "out.wav")
        sf.write(src, audio48, SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", chain, "-ar", str(SR),
                        "-ac", "1", "-c:a", "pcm_f32le", dst], check=True)
        out, _ = sf.read(dst, dtype="float32")
    out = out[: len(audio48)]
    return np.pad(out, (0, len(audio48) - len(out)))


def synthesize(script: Script, cfg: dict, force_whisper: bool = False, log=print):
    """-> dict(audio=np 48k mono, words=[{text,start,end}], cues=[{cue,at,db,source}], stats)"""
    engine, voice, lang, speed = cfg["engine"], cfg["voice"], cfg["lang"], cfg["speed"]
    lead = float(cfg.get("lead_in", LEAD_IN))
    pieces = [np.zeros(int(lead * SR), np.float32)]
    t = lead
    words, cues, coverage, synth_s = [], [], [], 0.0
    plan = []
    def sfx_len(name):
        import soundfile as sf
        from .mix import find_asset
        try:
            return sf.info(find_asset("sfx", name)).duration
        except Exception:
            return 1.0

    for si, seg in enumerate(script.segments):
        for mk in seg.markers:
            if mk.kind == "pause" and mk.seconds < 0:
                off = max([m.seconds for m in seg.markers if m.kind == "sfx" and m.name == mk.name
                           and m.word_index == mk.word_index] or [0.0])
                mk.seconds = sfx_len(mk.name) + max(0.0, off) + 0.15
        subs = split_on_pauses(seg)
        for k, (sub, pause_after) in enumerate(subs):
            last_of_seg = k == len(subs) - 1
            gap = pause_after + (cfg["paragraph_pause"] if last_of_seg and si < len(script.segments) - 1 else 0)
            plan.append((sub, gap, seg.gain_db, seg.speed or speed))
    gains = []  # (start sample, end sample, dB) from [vox: dB], applied after the voice chain
    speeds = set()
    for sub, gap, gain_db, sp in plan:
        if sub.words:
            t0 = time.time()
            speeds.add(sp)
            if engine == "piper":
                a, sr, timed = _piper(sub.text, voice)
            elif cfg.get("sentence_mode"):
                a, sr, timed = _kokoro_sentences(sub.text, voice, lang, sp, float(cfg.get("sentence_gap", 0.26)) / sp)
            else:
                a, sr, timed = _kokoro(sub.text, voice, lang, sp)
            synth_s += time.time() - t0
            a48 = trim_tail(_to48(a, sr)) if cfg.get("trim_tail") else _to48(a, sr)
            # first spoken chunk: cut Kokoro's lead silence (trim_head); later chunks only with trim_head_every
            head_keep = cfg.get("trim_head") if not pieces[1:] else cfg.get("trim_head_every")
            if head_keep is not None:
                n0 = len(a48)
                a48 = trim_head(a48, keep=float(head_keep))
                cut = (n0 - len(a48)) / SR
                if cut and timed:
                    timed = [(w_, None if s_ is None else max(0.0, s_ - cut), None if e_ is None else max(0.0, e_ - cut))
                             for w_, s_, e_ in timed]
            dur = len(a48) / SR
            times, cov = align(sub.words, timed, dur) if timed and not force_whisper else (None, 0.0)
            if times:
                times = [(min(s_, dur), min(e_, dur)) for s_, e_ in times]
            if times is None or cov < 0.6:
                wt = whisper_words(a48)
                times, cov = align(sub.words, wt, dur)
                src = "whisper"
            else:
                src = engine
            coverage.append((len(sub.words), cov, src))
            for w, (s, e) in zip(sub.words, times):
                words.append({"text": w, "start": round(t + s, 3), "end": round(t + e, 3)})
            for mk in sub.markers:
                if mk.kind != "sfx":
                    continue
                at = t + (times[mk.word_index][0] if mk.word_index < len(times) else dur) + mk.seconds
                cues.append({"cue": mk.name, "at": round(max(0.0, at), 3), "db": mk.db, "source": "marker",
                             **({"hush": mk.hush} if mk.hush else {})})
            if gain_db:
                gains.append((int(round(t * SR)), int(round((t + dur) * SR)), gain_db))
            pieces.append(a48)
            t += dur
        else:  # markers only (e.g. a line that is just "[sfx: knock3] [pause: 1.2]")
            for mk in sub.markers:
                if mk.kind == "sfx":
                    cues.append({"cue": mk.name, "at": round(t + mk.seconds, 3), "db": mk.db, "source": "marker",
                                 **({"hush": mk.hush} if mk.hush else {})})
        if gap > 0:
            pieces.append(np.zeros(int(gap * SR), np.float32))
            t += int(gap * SR) / SR
    pieces.append(np.zeros(int(TAIL * SR), np.float32))
    audio = np.concatenate(pieces)
    audio = voice_chain(audio, cfg.get("voice_chain", ""))
    fadeN = int(0.03 * SR)
    for i, j, db in gains:  # after the compressor, so a quiet passage stays quiet
        g = np.full(j - i, 10 ** (db / 20), np.float32)
        ramp = np.linspace(1, 10 ** (db / 20), min(fadeN, len(g)), dtype=np.float32)
        g[: len(ramp)] = ramp
        audio[i:j] *= g[: max(0, min(j, len(audio)) - i)]
    n_words = sum(c[0] for c in coverage) or 1
    stats = {
        "engine": engine, "voice": voice, "speed": speed if len(speeds) <= 1 else sorted(speeds), "synth_s": round(synth_s, 2),
        "duration_s": round(len(audio) / SR, 3),
        "timing_source": sorted({c[2] for c in coverage}),
        "timing_coverage": round(sum(c[0] * c[1] for c in coverage) / n_words, 3),
    }
    log(f"[tts] {voice} {stats['duration_s']}s audio in {stats['synth_s']}s, timings {stats['timing_source']} "
        f"coverage {stats['timing_coverage']}")
    return {"audio": audio, "words": words, "cues": cues, "stats": stats}


def auto_cues(words: list[dict], rules: dict, existing: list[dict], min_gap=1.5, in_speech_db: dict | None = None):
    """Keyword-triggered SFX: fire at the word's start, never within min_gap of another cue.
    in_speech_db: extra dB per cue name (auto cues always land inside speech, e.g. knock3 -6 -> -9 dB under voice)."""
    in_speech_db = in_speech_db or {}
    out = []
    taken = [c["at"] for c in existing]
    for w in words:
        for pat, cue in rules.items():
            if re.search(pat, w["text"], re.I):
                at = w["start"]
                if all(abs(at - x) >= min_gap for x in taken):
                    out.append({"cue": cue, "at": round(at, 3), "db": float(in_speech_db.get(cue, 0.0)), "source": f"auto:{w['text']}"})
                    taken.append(at)
                break
    return out
