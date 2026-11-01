#!/usr/bin/env python3
"""Extract review-ref frames on the Spark (never on the Mac: the source MP4s live in ~/studio/refs).

    ssh dgx-spark 'cd ~/studio/app && nice -n 10 python3 research/library/review-refs/extract_refs.py'
    rsync -a dgx-spark:~/studio/refs/review-refs/ research/library/review-refs/   # pull JPGs back

Reads frames_spec.json next to this file. Writes ~/studio/refs/review-refs/<niche>/<id>/NN_<qa_class>.jpg
at 1080 px wide (height follows the source aspect). The thumbnail frame is copied from the source
cover JPG next to the MP4 (or, failing that, research/library/thumbs/<id>.jpg) and scaled to 1080 wide.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFS = os.path.expanduser("~/studio/refs")
OUT = os.path.join(REFS, "review-refs")
FFMPEG = next((p for p in [os.path.expanduser("~/studio/bin/ffmpeg"), "/opt/homebrew/bin/ffmpeg", "ffmpeg"]
               if p == "ffmpeg" or os.path.exists(p)), "ffmpeg")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", " ".join(cmd), r.stderr[-400:], file=sys.stderr)
    return r.returncode == 0


def main():
    spec = json.load(open(os.path.join(HERE, "frames_spec.json")))
    for niche in ("explainer", "horror"):
        classes = spec[niche]["classes"]
        for vid, ref in spec[niche]["refs"].items():
            src = os.path.join(REFS, ref["src"])
            od = os.path.join(OUT, niche, vid)
            os.makedirs(od, exist_ok=True)
            for idx, cls in enumerate(classes, 1):
                dst = os.path.join(od, f"{idx:02d}_{cls}.jpg")
                if cls == "thumbnail":
                    cands = [os.path.splitext(src)[0] + ".jpg",
                             os.path.join(REFS, niche, vid + ".jpg"),
                             os.path.join(HERE, "..", "thumbs", vid + ".jpg")]
                    cover = next((c for c in cands if os.path.exists(c)), None)
                    if cover:
                        # Shorts covers come pillarboxed in a 16:9 JPG: crop back to the 9:16 picture.
                        vf = "scale=1080:-2:flags=lanczos"
                        if ref.get("thumb_crop_9x16"):
                            vf = "crop=trunc(ih*9/16/2)*2:ih," + vf
                        run([FFMPEG, "-y", "-v", "error", "-threads", "2", "-i", cover,
                             "-vf", vf, "-q:v", "3", dst])
                    else:
                        print("no cover for", vid, file=sys.stderr)
                    continue
                t = ref["frames"][cls][0]
                run([FFMPEG, "-y", "-v", "error", "-threads", "2", "-ss", str(t), "-i", src,
                     "-frames:v", "1", "-vf", "scale=1080:-2:flags=lanczos", "-q:v", "3", dst])
            print("done", niche, vid)


if __name__ == "__main__":
    main()
