#!/usr/bin/env python3
"""Build the A/B audio for the first 10.5 s of explainer-orca (run ON THE SPARK, stdlib + ffmpeg).

  base_audio.wav    mix.wav cut to 10.5 s (what the pipeline ships)
  polish_audio.wav  the same mix.wav + designed SFX from cues.json (pitch variants, 90 Hz high-pass,
                    peak-normalised per cue), then a -1.5 dBFS limiter
  sfx_stem.wav      the designed SFX alone (for the phone-body / voice-margin checks)

usage: python3 -I make_audio.py <mix.wav> <sfx_dir> <out_dir>   -> also prints a JSON report
"""
import json
import os
import re
import subprocess
import sys

DUR = 10.5
FF = os.environ.get("FFMPEG", "ffmpeg")


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def probe_sr(path):
    out = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate", "-of", "csv=p=0", path]).stdout
    return int(out.strip())


def levels(path, af=None):
    """(mean_volume, max_volume) in dBFS."""
    args = [FF, "-nostdin", "-hide_banner", "-i", path]
    if af:
        args += ["-af", f"{af},volumedetect"]
    else:
        args += ["-af", "volumedetect"]
    args += ["-f", "null", "-"]
    err = subprocess.run(args, capture_output=True, text=True).stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+) dB", err).group(1))
    peak = float(re.search(r"max_volume: (-?[\d.]+) dB", err).group(1))
    return mean, peak


def loudness(path):
    err = subprocess.run([FF, "-nostdin", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    summ = err[err.rfind("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
    return i, tp


def main():
    mix, sfx_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    here = os.path.dirname(os.path.abspath(__file__))
    plan = json.load(open(os.path.join(here, "cues.json")))
    sr = probe_sr(mix)
    os.makedirs(out, exist_ok=True)
    base = os.path.join(out, "base_audio.wav")
    run([FF, "-nostdin", "-v", "error", "-y", "-i", mix, "-t", str(DUR), "-c:a", "pcm_s16le", base])

    inputs, chains, labels = [], [], []
    # each cue: pitch variant, high-pass, gain to its target peak, delay; first sample at 0, 5 ms fade-in
    for k, c in enumerate(plan["cues"]):
        src = os.path.join(sfx_dir, c["cue"] + ".wav")
        csr = probe_sr(src)
        rate = c.get("rate", 1.0)
        pre = f"asetrate={int(csr * rate)},aresample={sr},highpass=f=90"
        _, pk = levels(src, pre)
        gain = c["peak"] - pk
        inputs += ["-i", src]
        d = int(round(c["at"] * 1000))
        chains.append(f"[{k}:a]{pre},afade=t=in:d=0.005,volume={gain:.2f}dB,adelay={d}:all=1,apad[c{k}]")
        labels.append(f"[c{k}]")
    # bed: loop the rumble, set its RMS, fade in/out
    bed = plan["bed"]
    bsrc = os.path.join(sfx_dir, bed["cue"] + ".wav")
    bmean, _ = levels(bsrc, "highpass=f=40")
    nb = len(plan["cues"])
    inputs += ["-stream_loop", "-1", "-i", bsrc]
    chains.append(
        f"[{nb}:a]aresample={sr},highpass=f=40,volume={bed['rms'] - bmean:.2f}dB,atrim=0:{DUR},"
        f"afade=t=in:d={bed['fadeIn']},afade=t=out:st={DUR - bed['fadeOut']}:d={bed['fadeOut']},apad[bed]"
    )
    labels.append("[bed]")
    n = len(labels)
    fc = ";".join(chains) + f";{''.join(labels)}amix=inputs={n}:normalize=0:duration=longest,atrim=0:{DUR},asetpts=PTS-STARTPTS[sfx]"
    stem = os.path.join(out, "sfx_stem.wav")
    run([FF, "-nostdin", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[sfx]", "-ac", "2", "-c:a", "pcm_f32le", stem])

    pol = os.path.join(out, "polish_audio.wav")
    run([
        FF, "-nostdin", "-v", "error", "-y", "-i", base, "-i", stem, "-filter_complex",
        f"[0:a]aformat=sample_fmts=fltp:channel_layouts=stereo[m];[1:a]aformat=sample_fmts=fltp:channel_layouts=stereo[s];"
        f"[m][s]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false:attack=3:release=60[o]",
        "-map", "[o]", "-c:a", "pcm_s16le", pol,
    ])

    rep = {"sample_rate": sr}
    for name, p in (("base", base), ("polish", pol), ("sfx_stem", stem)):
        i, tp = loudness(p)
        rep[name] = {"I_lufs": i, "peak_dbfs": tp}
    # phone body (ME A4): how much of the SFX survives a 200 Hz high-pass, and its 120-600 Hz share
    full, _ = levels(stem)
    hp, _ = levels(stem, "highpass=f=200")
    body, _ = levels(stem, "bandpass=f=270:width_type=q:w=0.6")
    rep["sfx_body"] = {"mean_full_db": full, "mean_after_hp200_db": hp, "mean_120_600_db": body, "lost_by_hp200_db": round(full - hp, 1)}
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
