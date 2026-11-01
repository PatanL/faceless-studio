"""Build a plain B2 storyboard around a pipeline audio folder, to prove captions + mix + cue sync.

usage: python -m pipeline.audio.demo_storyboard studio/public/episodes/<id> studio/storyboards/<name>.json [--format 9:16]

Scenes are cut at paragraph-sized pauses in the narration; each SFX cue gets a camera shake
(impacts/knocks/stingers) or a callout flash, so a render shows whether cue times line up.
Visuals are deliberately simple (gradients, a title, a cue label): this is an audio test card.
"""
from __future__ import annotations

import argparse
import json
import os

PALETTE = [["#0b0d12", "#1b1f2b"], ["#120b0d", "#2a1418"], ["#0b1210", "#14261f"], ["#0d0b12", "#221a30"]]
SHAKE = {"knock", "knock3", "knock3_slow", "impact", "boom", "stinger", "heartbeat", "heartbeat_slow", "heartbeat_fast"}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("episode_dir")
    ap.add_argument("out_json")
    ap.add_argument("--format", default="9:16")
    ap.add_argument("--title", default="B5 audio test")
    a = ap.parse_args(argv)
    d = a.episode_dir.rstrip("/")
    frag = json.load(open(os.path.join(d, "audio.storyboard.json")))
    words = json.load(open(os.path.join(d, "captions.json")))["words"]
    cues = json.load(open(os.path.join(d, "cues.json")))
    dur = frag["duration_s"]
    # cut points: gaps > 0.9 s between words
    cuts = [0.0]
    for w0, w1 in zip(words, words[1:]):
        if w1["start"] - w0["end"] > 0.9 and w1["start"] - cuts[-1] > 2.5:
            cuts.append(round(w1["start"] - 0.25, 3))
    cuts.append(dur)
    scenes = []
    for i, (s, e) in enumerate(zip(cuts, cuts[1:])):
        local = [c for c in cues if s <= c["at"] < e]
        scenes.append({
            "id": f"s{i}",
            "duration": round(e - s, 3),
            "background": {"type": "gradient", "kind": "radial", "colors": PALETTE[i % len(PALETTE)][::-1]},
            "transitionIn": {"type": "fade" if i else "cut", "duration": 0.3},
            "camera": {"preset": "pushIn", "amount": 0.6,
                       "shake": [{"at": round(c["at"] - s, 3), "duration": 0.35 if "knock" in c["cue"] else 0.6,
                                  "amplitude": 14} for c in local if c["cue"] in SHAKE]},
            "layers": [
                {"type": "text", "text": a.title.upper(), "y": "17%", "fontSize": 54, "color": "#8a93a6",
                 "letterSpacing": 0.12, "depth": 0},
                {"type": "particles", "preset": "dust", "count": 40, "color": "rgba(220,220,255,0.35)"},
            ],
            "callouts": [{"style": "label", "text": f"SFX: {c['cue']}", "at": round(c["at"] - s, 3), "duration": 1.0,
                          "x": "50%", "y": "30%", "background": "#ff3b5c", "color": "#ffffff", "fontSize": 40}
                         for c in local],
            "grade": {"vignette": 0.5, "flicker": 0.08},
        })
    sb = {
        "version": 1, "id": os.path.splitext(os.path.basename(a.out_json))[0], "title": a.title, "format": a.format,
        "fps": 30, "scenes": scenes,
        "captions": {"src": frag["captions"]["src"], "style": {"highlight": "#ff3b5c"}},
        "audio": {k: v for k, v in frag["audio"].items()},
        "overlays": {"grain": 0.06, "vignette": 0.3, "fadeIn": 0.2, "fadeOut": 0.6},
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out_json)), exist_ok=True)
    json.dump(sb, open(a.out_json, "w"), indent=1)
    print(f"[demo] {len(scenes)} scenes, {dur}s -> {a.out_json}")


if __name__ == "__main__":
    main()
