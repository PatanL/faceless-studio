# Word-highlight caption cards (VISUAL_GRAMMAR section 9 geometry) as transparent PNG bands + an ffmpeg concat list.
#   python3 tools/captions.py audio/captions.json out/captions [--plain] [--dur 11.2]
# One PNG per (card, active word). Band is 1080x260, placed so the text centre sits at y=1503 (78.3% of 1920).
import json, sys, os, re, argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('words'); ap.add_argument('out')
ap.add_argument('--plain', action='store_true', help='no word highlight (grammar default)')
ap.add_argument('--dur', type=float, required=True)
A = ap.parse_args()
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = ImageFont.truetype(os.path.join(HERE, 'fonts', 'Montserrat-ExtraBold.woff2'), 68)
W, BH, CY = 1080, 260, 130          # band size, text centre inside the band
BAND_Y = 1503 - CY                  # overlay y on the 1920 frame
HI = (255, 214, 74)                 # active word
CHUNKS = [2, 3, 2, 3, 3, 2, 2, 2, 4, 3, 2, 2]   # phrase-boundary cards (sum = 30 words)

words = json.load(open(A.words))['words']
assert sum(CHUNKS) == len(words), (sum(CHUNKS), len(words))
def clean(t): return re.sub(r"[^\w'\-]", '', t)

def card(ws, active):
    toks = [clean(w['text']) for w in ws]
    space = FONT.getlength(' ')
    widths = [FONT.getlength(t) for t in toks]
    total = sum(widths) + space * (len(toks) - 1)
    assert total <= 0.72 * W, ('card too wide', toks, total)
    x0 = (W - total) / 2
    txt = Image.new('L', (W, BH), 0); d = ImageDraw.Draw(txt)
    colour = Image.new('RGBA', (W, BH), (0, 0, 0, 0)); dc = ImageDraw.Draw(colour)
    x = x0
    for i, (t, w) in enumerate(zip(toks, widths)):
        d.text((x, CY), t, font=FONT, fill=255, anchor='lm')
        fill = HI if (i == active and not A.plain) else (255, 255, 255)
        dc.text((x, CY), t, font=FONT, fill=fill + (255,), anchor='lm')
        x += w + space
    # soft drop shadow, no box: 0 3px 8px rgba(0,0,0,.6) + 0 0 2px rgba(0,0,0,.35)
    sh1 = Image.new('L', (W, BH), 0); sh1.paste(txt, (0, 3)); sh1 = sh1.filter(ImageFilter.GaussianBlur(4)).point(lambda v: int(v * 0.6))
    sh2 = txt.filter(ImageFilter.GaussianBlur(1)).point(lambda v: int(v * 0.35))
    sh = Image.fromarray(np.maximum(np.array(sh1), np.array(sh2)))
    base = Image.new('RGBA', (W, BH), (8, 14, 28, 0)); base.putalpha(sh)
    return Image.alpha_composite(base, colour)

os.makedirs(A.out, exist_ok=True)
segs = []          # (png, start, end)
i = 0
cards = []
for n in CHUNKS:
    cards.append(words[i:i + n]); i += n
blank = os.path.join(A.out, 'blank.png'); Image.new('RGBA', (W, BH), (0, 0, 0, 0)).save(blank)
for ci, ws in enumerate(cards):
    for wi, w in enumerate(ws):
        png = os.path.join(A.out, f'c{ci:02d}_w{wi}.png')
        card(ws, wi).save(png)
        start = 0.0 if (ci == 0 and wi == 0) else w['start']
        if wi + 1 < len(ws): end = ws[wi + 1]['start']
        elif ci + 1 < len(cards): end = cards[ci + 1][0]['start']
        else: end = w['end'] + 0.1          # caption-free tail after the last word
        segs.append((png, start, end))
segs.append((blank, segs[-1][2], A.dur))
with open(os.path.join(A.out, 'list.txt'), 'w') as f:
    f.write('ffconcat version 1.0\n')
    for png, s, e in segs:
        f.write(f"file '{os.path.basename(png)}'\nduration {e - s:.3f}\n")
    f.write(f"file '{os.path.basename(segs[-1][0])}'\n")
json.dump({'band_y': BAND_Y, 'segments': [(os.path.basename(p), round(s, 3), round(e, 3)) for p, s, e in segs]},
          open(os.path.join(A.out, 'segments.json'), 'w'), indent=1)
print('cards', len(cards), 'segments', len(segs), 'band_y', BAND_Y)
