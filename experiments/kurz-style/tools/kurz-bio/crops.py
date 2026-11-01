import sys, os
from PIL import Image
# lines: still x0 y0 x1 y1 name
os.makedirs("crops", exist_ok=True)
for line in open(sys.argv[1]):
    p = line.split()
    if len(p) < 6: continue
    im = Image.open("stills/" + p[0]).crop(tuple(int(v) for v in p[1:5]))
    im.save("crops/" + p[5] + ".png"); print(p[5], im.size)
