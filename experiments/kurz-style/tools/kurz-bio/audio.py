"""usage: audio.py ffmpeg video vtt -> prints speech/gap level stats, wpm, onset density"""
import sys, subprocess, re, numpy as np
ff, v, vtt = sys.argv[1:4]
sr = 16000
raw = subprocess.run([ff, "-nostdin", "-loglevel", "error", "-i", v, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
hop = int(0.05 * sr); n = len(x) // hop
fr = x[:n * hop].reshape(n, hop)
rms = 20 * np.log10(np.sqrt((fr ** 2).mean(1)) + 1e-9)
t = np.arange(n) * 0.05
cues = []
for m in re.finditer(r"(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)\n(.*?)\n\n", open(vtt).read() + "\n\n", re.S):
    a = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]); b = int(m[4]) * 3600 + int(m[5]) * 60 + float(m[6])
    cues.append((a, b, m[7].replace("\n", " ")))
sp = np.zeros(n, bool)
words = 0; spoken = 0
for a, b, txt in cues:
    if txt.startswith("("): continue
    sp[(t >= a) & (t < b)] = True; words += len(txt.split()); spoken += b - a
# gaps >= 0.4 s outside cues, ignoring first/last 1 s
gap = ~sp
lab = np.zeros(n, int); k = 0; runs = []
i = 0
while i < n:
    if gap[i]:
        j = i
        while j < n and gap[j]: j += 1
        if (j - i) * 0.05 >= 0.4: runs.append((i, j))
        i = j
    else: i += 1
g = np.concatenate([rms[i + 2:j - 2] for i, j in runs if j - i > 6]) if runs else np.array([])
s = rms[sp]
print("duration_s", round(len(x) / sr, 1), "cues", len(cues), "words", words, "wpm_over_cue_time", round(words / spoken * 60, 1), "wpm_over_total", round(words / (len(x) / sr) * 60, 1))
print("speech_rms_dB p50/p90", np.percentile(s, [50, 90]).round(1))
print("gap(non-speech)_rms_dB p10/p50/p90", np.percentile(g, [10, 50, 90]).round(1) if len(g) else None, "n_gaps", len(runs), "gap_total_s", round(sum(j - i for i, j in runs) * 0.05, 1))
print("pct_frames_below_-50dB(silence)", round(float((rms < -50).mean() * 100), 2), "below -40", round(float((rms < -40).mean() * 100), 2))
# longest true silence
sil = rms < -50; best = 0; cur = 0
for b_ in sil:
    cur = cur + 1 if b_ else 0; best = max(best, cur)
print("longest_silence_s", round(best * 0.05, 2))
# high-band onsets (SFX proxy): energy above 3 kHz via simple diff filter
hp = np.diff(x, prepend=0); hp = np.diff(hp, prepend=0)
fh = hp[:n * hop].reshape(n, hop); eh = 10 * np.log10((fh ** 2).mean(1) + 1e-12)
on = np.where((eh[1:] - eh[:-1] > 9) & (eh[1:] > np.percentile(eh, 60)))[0] + 1
# merge onsets within 0.3 s
m = []
for o in on:
    if not m or o - m[-1] > 6: m.append(o)
m = np.array(m)
print("hf_onsets_total", len(m), "per_min", round(len(m) / (len(x) / sr / 60), 1), "in_gaps", int(sum(gap[o] for o in m)))
np.save(sys.argv[4], np.stack([t, rms, eh, sp.astype(np.float32)]))
