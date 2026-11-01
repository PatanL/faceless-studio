"""Run on Spark (CPU only). For each video: scene-cut detection, 5s frame sampling, labelled contact sheets, cut stats JSON."""
import os, sys, json, re, subprocess, glob
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from PIL import Image, ImageDraw
FF = sys.argv[1]; refdir = sys.argv[2]; outdir = sys.argv[3]; ids = sys.argv[4:]
os.makedirs(outdir, exist_ok=True)
def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)
for vid in ids:
    src = f"{refdir}/{vid}.mp4"
    vdir = f"{outdir}/{vid}"; os.makedirs(f"{vdir}/f5", exist_ok=True); os.makedirs(f"{vdir}/cuts", exist_ok=True)
    # scene scores for every frame (downscaled), keep score per frame
    r = run([FF, "-hide_banner", "-threads", "6", "-i", src, "-vf", "scale=320:-2,select='gte(scene,0)',metadata=print:file=-", "-an", "-f", "null", "-"])
    scores = []
    t = None
    for line in r.stdout.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m: t = float(m.group(1)); continue
        m = re.search(r"lavfi.scene_score=([\d.]+)", line)
        if m and t is not None: scores.append((t, float(m.group(1))))
    dur = scores[-1][0] if scores else 0
    stats = {"id": vid, "duration": dur}
    for th in (0.2, 0.3, 0.4):
        cuts = [round(t, 2) for t, s in scores if s >= th]
        # merge cuts within 0.3s (dissolves)
        merged = []
        for c in cuts:
            if not merged or c - merged[-1] > 0.3: merged.append(c)
        stats[f"cuts_{th}"] = merged
        stats[f"n_cuts_{th}"] = len(merged)
        stats[f"cuts_per_min_{th}"] = round(len(merged) / (dur / 60), 2) if dur else 0
        stats[f"mean_shot_s_{th}"] = round(dur / (len(merged) + 1), 2) if dur else 0
    # motion proxy: mean scene score per 5 s window (continuous animation vs static)
    win = {}
    for t, s in scores: win.setdefault(int(t // 5), []).append(s)
    stats["motion_5s"] = [round(sum(v) / len(v), 4) for k, v in sorted(win.items())]
    json.dump(stats, open(f"{vdir}/cuts.json", "w"))
    # 5 s sampled frames (offset 2.5 s so we land mid-window)
    run([FF, "-hide_banner", "-loglevel", "error", "-threads", "6", "-ss", "2.5", "-i", src, "-vf", "fps=1/5,scale=384:-2", "-q:v", "4", f"{vdir}/f5/%04d.jpg"])
    # one frame just after each cut at 0.3
    for i, c in enumerate(stats["cuts_0.3"]):
        run([FF, "-hide_banner", "-loglevel", "error", "-ss", str(c + 0.25), "-i", src, "-frames:v", "1", "-vf", "scale=384:-2", "-q:v", "4", f"{vdir}/cuts/{i:04d}_{c:07.2f}.jpg"])
    # contact sheets: 6 cols x 5 rows = 30 frames = 150 s per sheet
    frames = sorted(glob.glob(f"{vdir}/f5/*.jpg"))
    cols, rows = 6, 5
    for si in range(0, len(frames), cols * rows):
        batch = frames[si:si + cols * rows]
        w, h = Image.open(batch[0]).size
        sheet = Image.new("RGB", (cols * w, rows * (h + 18)), (20, 20, 20))
        d = ImageDraw.Draw(sheet)
        for j, fp in enumerate(batch):
            idx = int(os.path.basename(fp)[:4]) - 1
            ts = 2.5 + idx * 5
            x, y = (j % cols) * w, (j // cols) * (h + 18)
            sheet.paste(Image.open(fp), (x, y + 18))
            d.text((x + 4, y + 3), f"{int(ts//60)}:{int(ts%60):02d}", fill=(255, 220, 0))
        sheet.save(f"{outdir}/{vid}_sheet{si // (cols*rows) + 1:02d}.jpg", quality=72)
    print(vid, "dur", round(dur, 1), {k: v for k, v in stats.items() if k.startswith(("n_cuts", "cuts_per_min", "mean_shot"))}, flush=True)
