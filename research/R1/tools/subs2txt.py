"""Convert YouTube json3 auto-subs to word list + 10s-chunk transcript."""
import json, sys, os
src, outdir = sys.argv[1], sys.argv[2]
vid = os.path.basename(src).split('.')[0]
d = json.load(open(src))
words = []
for ev in d.get('events', []):
    t0 = ev.get('tStartMs', 0)
    for s in ev.get('segs', []) or []:
        w = s.get('utf8', '').strip()
        if not w or w == '\n':
            continue
        words.append(((t0 + s.get('tOffsetMs', 0)) / 1000.0, w))
words.sort()
json.dump([{'t': round(t, 2), 'w': w} for t, w in words], open(f'{outdir}/{vid}.words.json', 'w'))
lines = []
chunk = 10
cur = 0; buf = []
for t, w in words:
    while t >= cur + chunk:
        if buf: lines.append(f'[{int(cur//60)}:{int(cur%60):02d}] ' + ' '.join(buf))
        buf = []; cur += chunk
    buf.append(w)
if buf: lines.append(f'[{int(cur//60)}:{int(cur%60):02d}] ' + ' '.join(buf))
open(f'{outdir}/{vid}.transcript.txt', 'w').write('\n'.join(lines) + '\n')
dur = words[-1][0] if words else 1
print(vid, 'words', len(words), 'wpm', round(len(words) / (dur / 60), 1))
