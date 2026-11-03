# usage: python kf_depth.py <key_frame.png> <out.npy>   (needs torch + transformers; Depth Anything V2 small, official weights)
# Depth Anything V2 (small), official weights from the depth-anything organisation on Hugging Face; MPS on the Mac
import sys, numpy as np, torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForDepthEstimation
src, out = sys.argv[1:3]
dev = "mps" if torch.backends.mps.is_available() else "cpu"
proc = AutoImageProcessor.from_pretrained("depth-anything/Depth-Anything-V2-Small-hf")
model = AutoModelForDepthEstimation.from_pretrained("depth-anything/Depth-Anything-V2-Small-hf").to(dev).eval()
im = Image.open(src).convert("RGB")
with torch.no_grad():
    o = model(**{k: v.to(dev) for k, v in proc(images=im, return_tensors="pt").items()})
d = torch.nn.functional.interpolate(o.predicted_depth[:, None], size=im.size[::-1], mode="bicubic", align_corners=False)[0, 0].cpu().numpy()
np.save(out, d.astype(np.float32)); v = (d - d.min()) / (d.max() - d.min())
Image.fromarray((v * 255).astype(np.uint8)).save(out.replace(".npy", ".png")); print(d.shape, float(d.min()), float(d.max()), dev)
