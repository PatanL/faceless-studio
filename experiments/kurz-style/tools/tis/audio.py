"""Sound-design measurements from audio.sh envelopes + the video's subtitle cues.
usage: python -I audio.py <audio_outdir> <subs.vtt> [scores_events.json]
Reports:
  - voice vs non-voice RMS (inside vs outside subtitle cues; manual subs only are reliable)
  - music bed: low-band (<150 Hz) level in non-voice gaps, and share of 0.1 s windows where
    the full band never falls below -45 dBFS (no true silence = continuous bed)
  - gaps: share of cue gaps >= 0.4 s and their median length
  - SFX transients: high-band (>5 kHz) jumps >= 12 dB above the local 3 s median, per minute,
    and share that land within 0.35 s of a detected scene transition
"""
import sys, re, json
import numpy as np


def load(p):
    a = np.loadtxt(p, dtype=str)
    t = a[:, 0].astype(float)
    v = np.array([float(x) if x not in ("-inf", "inf", "") else -120.0 for x in a[:, 1]])
    return t, v


d = sys.argv[1]
t, full = load(f"{d}/rms_full.txt"); _, low = load(f"{d}/rms_low.txt"); _, voice = load(f"{d}/rms_voice.txt"); _, high = load(f"{d}/rms_high.txt")
n = min(len(t), len(low), len(voice), len(high)); t, full, low, voice, high = t[:n], full[:n], low[:n], voice[:n], high[:n]

def sec(x):
    h, m, s = x.split(":"); return int(h) * 3600 + int(m) * 60 + float(s)
cues = [(sec(a), sec(b)) for a, b in re.findall(r"(\d\d:\d\d:\d\d\.\d\d\d) --> (\d\d:\d\d:\d\d\.\d\d\d)", open(sys.argv[2]).read())]
inside = np.zeros(n, bool)
for a, b in cues:
    inside[(t >= a) & (t < b)] = True
gaps = [cues[i + 1][0] - cues[i][1] for i in range(len(cues) - 1)]
gaps = np.array([g for g in gaps if g > 0.05])
outside = ~inside
# shrink "outside" to windows at least 0.15 s from any cue edge
med = lambda x: round(float(np.median(x)), 1) if len(x) else None
res = {
    "rms_full_dB voice/gap": [med(full[inside]), med(full[outside])],
    "rms_low<150Hz_dB voice/gap": [med(low[inside]), med(low[outside])],
    "rms_voiceband_dB voice/gap": [med(voice[inside]), med(voice[outside])],
    "rms_high>5k_dB voice/gap": [med(high[inside]), med(high[outside])],
    "windows_below_-45dB_full": round(float((full < -45).mean()), 3),
    "windows_below_-60dB_full": round(float((full < -60).mean()), 3),
    "cue_gaps>=0.4s_share": round(float((gaps >= 0.4).mean()), 3) if len(gaps) else None,
    "cue_gap_median_s": med(gaps),
    "cues": len(cues),
}
# pauses from the voice band itself (subtitle cues are often contiguous)
quiet = voice < (np.median(voice[inside]) - 20 if inside.any() else -45)
runs, r = [], 0
for q in quiet:
    if q: r += 1
    else:
        if r: runs.append(r * 0.1)
        r = 0
runs = np.array(runs)
res["voice_pauses>=0.3s_per_min"] = round(float((runs >= 0.3).sum() / (t[-1] / 60)), 1)
res["voice_pause_median_s(>=0.3)"] = med(runs[runs >= 0.3])
res["bed_level_in_pauses_dB(full,low)"] = [med(full[quiet]), med(low[quiet])]


def rise(sig, e):
    i0, i1 = np.searchsorted(t, [e - 0.3, e + 0.3]); b0, b1 = np.searchsorted(t, [e - 1.5, e - 0.5])
    if i1 <= i0 or b1 <= b0: return None
    return float(sig[i0:i1].max() - np.median(sig[b0:b1]))


if len(sys.argv) > 3:
    st = [e[0] for e in json.load(open(sys.argv[3]))["events"] if 2 < e[0] < t[-1] - 2]
    rng = np.random.default_rng(0); rnd = rng.uniform(2, t[-1] - 2, 600)
    for name, sig in (("high>5k", high), ("low<150", low), ("full", full)):
        a = np.array([x for x in (rise(sig, e) for e in st) if x is not None])
        b = np.array([x for x in (rise(sig, e) for e in rnd) if x is not None])
        res[f"{name}: rise at transitions vs random (median dB, share>=8dB)"] = [
            round(float(np.median(a)), 1), round(float(np.median(b)), 1), round(float((a >= 8).mean()), 2), round(float((b >= 8).mean()), 2)]
print(json.dumps(res, indent=1))
