#!/usr/bin/env python3
"""Multi-voice audio for horror-roommate-texts-from-room (Spark CPU only).

pipeline/audio (locked by the horror closeout lane) reads ONE voice per script. This episode needs four
(Maya, both Danis in the same voice, Dani's mom) plus a muffled low-pass on the kitchen voice. So this script
reuses the pipeline's own pieces read-only (Kokoro wrapper, word alignment, trims, voice chain, mix) and adds
only the per-line voice and FX on top. Nothing in pipeline/ is modified.

Input:  the ```cast block in script.md (one utterance per line, see the block's header comment).
Output: --out (default studio/public/episodes/horror-roommate-texts-from-room/): mix.wav + stems + sfx/*.wav
        --meta (default <this folder>/audio/): lines.json, captions.json, cues.json, report.json

usage (Spark):
  source ~/studio/app/scripts/spark_env.sh && cd ~/studio/app
  nice -n 10 env TTS_THREADS=4 OMP_NUM_THREADS=4 python3 backlog/horror/horror-roommate-texts-from-room/gen_audio.py
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time

os.environ["CUDA_VISIBLE_DEVICES"] = ""  # never the GPU (BRIEF hard rule 1)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)

import numpy as np  # noqa: E402

from pipeline.audio.config import NICHES, SR  # noqa: E402
from pipeline.audio.mix import PUBLIC, mix  # noqa: E402
from pipeline.audio.tts import _kokoro, _to48, align, trim_head, trim_tail, voice_chain  # noqa: E402

EP = "horror-roommate-texts-from-room"
HORROR_CHAIN = NICHES["horror"]["voice_chain"]

# speaker -> (kokoro voice, speed, ffmpeg chain, gain dB, captioned?)
# Both Danis use the SAME voice (af_sky) so the ear cannot tell them apart; only the room changes.
VOICES = {
    "NARR":    ("af_heart", 1.40, HORROR_CHAIN, 0.0, True),
    "ME":      ("af_heart", 1.40, HORROR_CHAIN, -1.0, False),   # Maya reading her own blue bubble
    "TXT":     ("af_sky", 1.32, "highpass=f=120,equalizer=f=3000:t=q:w=1:g=1.5", -2.5, False),  # Dani thread, read close and flat
    "CALM":    ("af_sky", 1.00, "highpass=f=120,equalizer=f=3000:t=q:w=1:g=1.5", -2.0, False),  # the last two bubbles, slower
    "KITCHEN": ("af_sky", 1.08, "highpass=f=220,lowpass=f=1800,aecho=0.8:0.55:38|61:0.16|0.08", -4.5, True),  # through a wall (1.8 kHz low-pass keeps the words, loses the air)
    "DOOR":    ("af_sky", 1.04, "highpass=f=90,equalizer=f=220:t=q:w=1:g=2.5,acompressor=threshold=-24dB:ratio=3:attack=5:release=90", -1.0, True),
    "MOM":     ("af_nicole", 1.35, "highpass=f=120", -2.0, False),
}
DEFAULT_GAP = 0.12

MARK = re.compile(r"\[(sfx|gap|hold)\s*:\s*([^\]]+)\]")
ALT = re.compile(r"\{([^|}]+)\|([^}]+)\}")   # {display|spoken}


def cast_lines(md: str):
    m = re.search(r"```cast\n(.*?)```", md, re.S)
    if not m:
        sys.exit("no ```cast block in script.md")
    out = []
    for raw in m.group(1).splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lid, rest = s.split(" ", 1)
        spk, text = rest.split(":", 1)
        out.append((lid.strip(), spk.strip(), text.strip()))
    return out


def tokenize(text: str):
    """-> display tokens [(display, [spoken words])], markers [(kind, arg, token_index)]"""
    toks, marks = [], []
    pos = 0
    work = ALT.sub(lambda m: m.group(1).replace(" ", " ") + "\u0001" + m.group(2).replace(" ", "_"), text)
    for piece in re.split(r"(\[[^\]]+\])", work):
        mm = MARK.fullmatch(piece.strip()) if piece.strip().startswith("[") else None
        if mm:
            marks.append((mm.group(1), mm.group(2).strip(), len(toks)))
            continue
        for w in piece.split():
            if "\u0001" in w:
                disp, spoken = w.split("\u0001")
                toks.append((disp.replace(" ", " "), spoken.split("_")))
            else:
                toks.append((w, [w]))
        pos += 1
    return toks, marks


def sfx_args(arg: str):
    parts = arg.split()
    d = {"cue": parts[0], "off": 0.0, "db": 0.0}
    for p in parts[1:]:
        if p.startswith("@"):
            d["off"] = float(p[1:])
        elif p.startswith("vol="):
            d["db"] = float(p[4:])
        elif p.startswith("hush="):
            d["hush"] = float(p[5:])
    return d


# ------------------------------------------------------------------ procedural SFX (episode-local, CC0, original)
def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(d, 1e-4))


def _noise(n, seed):
    return np.random.default_rng(seed).standard_normal(n).astype(np.float32)


def _bp(x, lo, hi):
    from scipy.signal import butter, sosfilt
    sos = butter(2, [lo, hi], btype="band", fs=SR, output="sos")
    return sosfilt(sos, x).astype(np.float32)


def _lp(x, f):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(2, f, btype="low", fs=SR, output="sos"), x).astype(np.float32)


def latch_click(seed=0):
    """One sticky door latch: a dry metal tick, a short spring ring and a low wood thunk."""
    n = int(0.22 * SR)
    t = np.arange(n) / SR
    tick = _bp(_noise(n, seed), 1800, 6000) * _env(n, 0.0005, 0.006)
    ring = (np.sin(2 * np.pi * 2350 * t) + 0.5 * np.sin(2 * np.pi * 3710 * t)) * _env(n, 0.0005, 0.035) * 0.25
    thunk = np.sin(2 * np.pi * 140 * t) * _env(n, 0.001, 0.03) * 0.6
    return (tick + ring + thunk).astype(np.float32)


def latch2():
    """The ownable signature: Dani's door clicks twice (0.38 s apart). Same file at the plant and the payoff."""
    a, b = latch_click(1), latch_click(2) * 0.9
    out = np.zeros(int(0.75 * SR), np.float32)
    out[: len(a)] += a
    i = int(0.38 * SR)
    out[i:i + len(b)] += b
    return out


def sizzle(dur):
    """Muffled frying-pan sizzle heard through a wall: band noise plus random fat crackles, low-passed."""
    n = int(dur * SR)
    base = _bp(_noise(n, 7), 2500, 9000) * 0.25
    rng = np.random.default_rng(8)
    crack = np.zeros(n, np.float32)
    for i in rng.integers(0, n - 2000, size=int(dur * 38)):
        crack[i:i + 400] += _noise(400, int(i)) * _env(400, 0.0002, 0.002) * rng.uniform(0.3, 1.0)
    x = _lp(base + _bp(crack, 1500, 7000), 1400)
    fade = int(0.4 * SR)
    x[:fade] *= np.linspace(0, 1, fade)
    x[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))  # it cuts dead when she stops cooking
    return x


def plate():
    n = int(0.5 * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * g for f, g in ((1830, 1), (2960, .6), (4410, .35))) * _env(n, 0.0005, 0.09)
    x += _bp(_noise(n, 3), 2000, 7000) * _env(n, 0.0003, 0.01)
    return _lp(x.astype(np.float32), 3000) * 0.5  # one wall away


def handle_jolt(seed=0):
    """A lever handle forced against a hand: metal clack plus the latch rattling in the strike plate."""
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    clack = _bp(_noise(n, 20 + seed), 900, 5000) * _env(n, 0.0005, 0.02)
    rattle = _bp(_noise(n, 40 + seed), 1500, 4000) * _env(n, 0.002, 0.08) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 34 * t))) * 0.5
    body = np.sin(2 * np.pi * 95 * t) * _env(n, 0.001, 0.05) * 0.7
    return (clack + rattle + body).astype(np.float32)


def handle_turn(dur=1.6):
    """Slow lever turn: a dry rising squeak with a ratchet of tiny ticks."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 600 + 500 * t / dur
    sq = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.08 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t))
    ticks = np.zeros(n, np.float32)
    for k in range(int(dur * 9)):
        i = int(k / 9 * SR)
        ticks[i:i + 300] += _bp(_noise(300, 90 + k), 2000, 6000) * _env(300, 0.0002, 0.003)
    x = (sq + ticks).astype(np.float32)
    x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return x


def steps(count=6, span=2.1):
    """Barefoot-ish steps on a wooden floor, getting closer (louder, brighter)."""
    out = np.zeros(int((span + 0.4) * SR), np.float32)
    for k in range(count):
        n = int(0.25 * SR)
        t = np.arange(n) / SR
        g = 0.35 + 0.65 * k / max(1, count - 1)
        x = (np.sin(2 * np.pi * (80 + 6 * k) * t) * _env(n, 0.002, 0.04) +
             _lp(_noise(n, 60 + k), 900 + 250 * k) * _env(n, 0.001, 0.02) * 0.8) * g
        i = int(k * span / max(1, count - 1) * SR)
        out[i:i + n] += x.astype(np.float32)
    return out


def floor_creak():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    f = 210 - 60 * t
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.6 + 0.4 * np.sin(2 * np.pi * 23 * t)) * _env(n, 0.08, 0.35)
    return _lp((x + _bp(_noise(n, 77), 300, 1200) * 0.15 * _env(n, 0.05, 0.3)).astype(np.float32), 1500)


def silence(dur):
    return np.zeros(int(dur * SR), np.float32)


def write_sfx(out_dir, sizzle_dur):
    import soundfile as sf
    d = os.path.join(out_dir, "sfx")
    os.makedirs(d, exist_ok=True)
    made = {
        "latch2": latch2(), "sizzle": sizzle(sizzle_dur), "plate": plate(), "jolt_a": handle_jolt(0),
        "jolt_b": handle_jolt(1), "jolt_c": handle_jolt(2), "handle_turn": handle_turn(), "steps6": steps(),
        "floor_creak": floor_creak(), "hush4": silence(4.0),
    }
    rel = {}
    for k, x in made.items():
        x = x / (np.abs(x).max() + 1e-9) * 0.7 if np.abs(x).max() > 0 else x
        p = os.path.join(d, f"{k}.wav")
        sf.write(p, x.astype(np.float32), SR, subtype="PCM_16")
        rel[k] = os.path.relpath(p, PUBLIC)
    return rel


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", default=os.path.join(HERE, "script.md"))
    ap.add_argument("--out", default=os.path.join(PUBLIC, "episodes", EP))
    ap.add_argument("--meta", default=os.path.join(HERE, "audio"))
    ap.add_argument("--music", default="tension_pulse")
    a = ap.parse_args()
    t_wall = time.time()
    lines = cast_lines(open(a.script, encoding="utf-8").read())

    pieces, t = [np.zeros(int(0.12 * SR), np.float32)], 0.12
    out_lines, words, cues = [], [], []
    for lid, spk, text in lines:
        toks, marks = tokenize(text)
        gap = DEFAULT_GAP
        hold = None
        for kind, arg, _ in marks:
            if kind == "gap":
                gap = float(arg)
            if kind == "hold":
                hold = float(arg)
        rec = {"id": lid, "speaker": spk, "text": " ".join(d for d, _ in toks)}
        if spk.startswith("BUBBLE") or hold is not None:   # on-screen only: a silent bubble / held beat
            dur = hold or 0.0
            rec.update(start=round(t, 3), end=round(t + dur, 3), words=[], voiced=False)
            for kind, arg, ti in marks:
                if kind == "sfx":
                    c = sfx_args(arg)
                    cues.append({**{k: v for k, v in c.items() if k != "off"}, "at": round(t + c["off"], 3), "line": lid})
            if dur:
                pieces.append(np.zeros(int(dur * SR), np.float32))
            t += dur
            out_lines.append(rec)
            continue
        voice, speed, chain, gain, cap = VOICES[spk]
        spoken = [w for _, sp in toks for w in sp]
        text_say = " ".join(spoken)
        audio, sr, timed = _kokoro(text_say, voice, "a", speed)
        a48 = trim_tail(_to48(audio, sr))
        n0 = len(a48)
        a48 = trim_head(a48, keep=0.03)
        cut = (n0 - len(a48)) / SR
        timed = [(w, None if s is None else max(0.0, s - cut), None if e is None else max(0.0, e - cut)) for w, s, e in timed]
        if chain:
            a48 = voice_chain(a48, chain)
        a48 = a48 * (10 ** (gain / 20))
        dur = len(a48) / SR
        times, cov = align(spoken, timed, dur)
        # spoken word times -> display tokens
        tw, k = [], 0
        for disp, sp in toks:
            s0, e0 = times[k][0], times[k + len(sp) - 1][1]
            k += len(sp)
            tw.append({"text": disp, "start": round(t + min(s0, dur), 3), "end": round(t + min(e0, dur), 3)})
        for kind, arg, ti in marks:
            if kind != "sfx":
                continue
            c = sfx_args(arg)
            base = tw[ti]["start"] if ti < len(tw) else t + dur
            cues.append({**{kk: v for kk, v in c.items() if kk != "off"}, "at": round(max(0.0, base + c["off"]), 3), "line": lid})
        rec.update(start=round(t, 3), end=round(t + dur, 3), words=tw, voiced=True, voice=voice, speed=speed,
                   coverage=round(cov, 3), caption=cap)
        out_lines.append(rec)
        if cap:
            words += [{**w, "spk": spk} for w in tw]
        pieces.append(a48.astype(np.float32))
        t += dur
        if gap:
            pieces.append(np.zeros(int(gap * SR), np.float32))
            t += gap
    pieces.append(np.zeros(int(0.35 * SR), np.float32))
    voice_track = np.concatenate(pieces)

    # resolve episode-local cue names (procedural) to their files under studio/public
    by_id = {r["id"]: r for r in out_lines}
    sizzle_end = next((c["at"] for c in cues if c["cue"] == "sizzle_stop"), 20.0)
    sizzle_start = next((c["at"] for c in cues if c["cue"] == "sizzle"), 1.0)
    rel = write_sfx(a.out, max(1.0, sizzle_end - sizzle_start))
    final = []
    for c in cues:
        if c["cue"] == "sizzle_stop":
            continue
        name = rel.get(c["cue"], c["cue"])
        final.append({**c, "cue": name, "name": c["cue"]})
    final.sort(key=lambda c: c["at"])
    cfg = dict(NICHES["horror"])
    cfg.update({"hush": {}, "music_db": -9.0, "max_tail": 0.6, "music_fade_out": 0.6, "end_fade": 0.25})
    mx = mix(voice_track, [{k: v for k, v in c.items() if k in ("cue", "at", "db", "hush")} for c in final], cfg, a.music, a.out)

    os.makedirs(a.meta, exist_ok=True)
    spoken_words = sum(len(r["words"]) for r in out_lines)
    speech_s = sum(r["end"] - r["start"] for r in out_lines if r["voiced"])
    total = mx["report"]["duration_s"]
    report = {
        "episode": EP, "built_utc": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()),
        "voices": {k: {"voice": v[0], "speed": v[1], "chain": v[2], "gain_db": v[3]} for k, v in VOICES.items()},
        "duration_s": total, "voice_end_s": round(t, 3), "words": spoken_words,
        "speech_s": round(speech_s, 2), "wpm_speech": round(spoken_words / speech_s * 60, 1),
        "wpm_overall": round(spoken_words / t * 60, 1),
        "min_coverage": min((r["coverage"] for r in out_lines if r["voiced"]), default=1.0),
        "mix": {k: mx["report"][k] for k in ("pyloudnorm_lufs", "true_peak_dbtp_4x", "ffmpeg_ebur128", "music")},
        "wall_s": round(time.time() - t_wall, 1),
    }
    json.dump(out_lines, open(os.path.join(a.meta, "lines.json"), "w"), indent=1)
    json.dump({"words": [{k: w[k] for k in ("text", "start", "end")} for w in words]},
              open(os.path.join(a.meta, "captions.json"), "w"), indent=1)
    json.dump(final, open(os.path.join(a.meta, "cues.json"), "w"), indent=1)
    json.dump(report, open(os.path.join(a.meta, "report.json"), "w"), indent=1)
    print(json.dumps({k: report[k] for k in ("duration_s", "words", "wpm_speech", "wpm_overall", "min_coverage", "wall_s")}))
    for r in out_lines:
        print(f"{r['id']:>4} {r['speaker']:<8} {r['start']:6.2f}-{r['end']:6.2f}  {r['text'][:70]}")


if __name__ == "__main__":
    main()
