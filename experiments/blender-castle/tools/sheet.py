# Contact sheet of preview PNGs with frame labels (Pillow only).
import sys, math
from PIL import Image, ImageDraw
out, cols, files = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
ims = [Image.open(f).convert('RGB') for f in files]
w = 270; h = int(ims[0].height * w / ims[0].width)
rows = math.ceil(len(ims) / cols)
sheet = Image.new('RGB', (cols * w, rows * h), (0, 0, 0))
for i, (f, im) in enumerate(zip(files, ims)):
    th = im.resize((w, h), Image.LANCZOS); d = ImageDraw.Draw(th)
    d.rectangle((0, 0, 60, 14), fill=(0, 0, 0)); d.text((3, 2), f.split('/')[-1][:9], fill=(255, 255, 0))
    sheet.paste(th, ((i % cols) * w, (i // cols) * h))
sheet.save(out, quality=88)
