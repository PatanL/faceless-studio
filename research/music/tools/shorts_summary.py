"""Shorts-specific measures on top of analyze.py: how fast the music lands, how sections fit ~60 s, how it ends/loops.

usage (music venv): python research/music/tools/shorts_summary.py work/kurz-shorts out.json
  expects <dir>/<id>/{vocals,music}.flac, <id>/words.json, <id>.cuts.json and analyze.py's
  research/music/data/shorts/<id>_music.json
"""
import glob
import json
import os
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(__file__))
from analyze import loudness_track, HOP  # noqa: E402


def chroma(y, sr):
    import librosa
    return librosa.feature.chroma_cqt(y=librosa.effects.harmonic(y), sr=sr, hop_length=512).mean(1)


def main():
    base, out = sys.argv[1], sys.argv[2]
    adir = os.path.join(os.path.dirname(__file__), "..", "data", "shorts")
    rows = []
    for d in sorted(glob.glob(os.path.join(base, "*/"))):
        k = os.path.basename(d.rstrip("/"))
        ap = os.path.join(adir, f"{k}_music.json")
        if not os.path.exists(ap):
            continue
        a = json.load(open(ap))
        m, sr = sf.read(os.path.join(d, "music.flac"), dtype="float32", always_2d=True)
        v, _ = sf.read(os.path.join(d, "vocals.flac"), dtype="float32", always_2d=True)
        T = len(m) / sr
        mS = loudness_track(m, 1.0, sr)
        vS = loudness_track(v, 0.4, sr)
        med = float(np.median(mS[int(2 / HOP):]))
        t = (np.arange(len(mS)) + 0.5) * HOP
        land = next((float(t[i]) for i in range(len(mS)) if mS[i] >= med - 6), None)
        words = json.load(open(os.path.join(d, "words.json")))["words"]
        first_sent = next((w["e"] for w in words if w["w"].rstrip('"').endswith((".", "?", "!"))), None)
        cuts = json.load(open(os.path.join(base, f"{k}.cuts.json")))
        first_cut = cuts[1]["t0"] if len(cuts) > 1 else None
        hits = [h["t"] for h in a["hits"]]
        last_word = words[-1]["e"] if words else T
        y = m.mean(1)
        c0, c1 = chroma(y[: int(3 * sr)], sr), chroma(y[-int(3 * sr):], sr)
        cos = float(c0 @ c1 / (np.linalg.norm(c0) * np.linalg.norm(c1) + 1e-9))
        end_lvl = float(np.median(mS[-int(1 / HOP):]))
        start_lvl = float(np.median(mS[: int(1 / HOP)]))
        tail = mS[-int(4 / HOP):]
        fade = float(tail[0] - tail[-1])
        mins = (a["analysed"][1] - a["analysed"][0]) / 60
        info = {}
        ij = os.path.join(base, "..", "..", "refs", "kurz-shorts", f"{k}.info.json")
        if os.path.exists(ij):
            j = json.load(open(ij))
            info = {"title": j.get("title"), "views": j.get("view_count")}
        rows.append({
            "id": k, **info, "dur_s": round(T, 1), "wpm": round(len(words) / (T / 60), 0),
            "visual_changes_per_min": round((len(cuts) - 1) / (T / 60), 1),
            "music_first_above_-45_s": a["starts_ends"]["first_music_above_-45_lufs_s"],
            "music_lands_s (1 s level within 6 dB of median)": land,
            "first_hit_s": hits[0] if hits else None, "first_sentence_end_s": first_sent, "first_visual_change_s": first_cut,
            "start_level_vs_median_db": round(start_lvl - med, 1),
            "voice_minus_music": a["loudness"]["voice_minus_music_under_speech_db"],
            "gaps_ge_0p5": a["loudness"]["gaps_ge_0p5s"], "gap_swell_db": a["loudness"].get("music_gap_minus_speech_db"),
            "music_range_db": round(a["loudness"]["music_LRA_like_p10_p95_short_term"][1] -
                                    a["loudness"]["music_LRA_like_p10_p95_short_term"][0], 1),
            "sections_per_min": a["boundaries"]["coarse_per_min"], "n_sections": len(a["boundaries"]["coarse"]) + 1,
            "tempo": a["tempo"]["global_bpm_librosa"], "pulse_clarity": a["tempo"]["pulse_clarity_median"],
            "risers_per_min": round(len(a["risers"]) / mins, 1), "hits_per_min": round(len(a["hits"]) / mins, 1),
            "dropouts_per_min": round(len(a["dropouts"]) / mins, 1),
            "hits_at_visual_changes": a["alignment"].get("hits_vs_setting_changes", {}),
            "texture_at_changes_vs_random": [a["setting_change_steps"]["texture_dist_median_at_changes"],
                                             a["setting_change_steps"]["texture_dist_median_random"]],
            "last_word_to_end_s": round(T - last_word, 2), "end_level_vs_median_db": round(end_lvl - med, 1),
            "fade_last_4s_db": round(fade, 1), "chroma_end_vs_start_cos": round(cos, 2),
            "minor_sections_share": round(np.mean(["min" in s["key"] for s in a["sections"]]), 2) if a["sections"] else None,
            "drums_within_10db_share": round(np.mean([s.get("drums_minus_music_db", -99) > -10 for s in a["sections"]]), 2)
            if a["sections"] else None,
        })
    json.dump(rows, open(out, "w"), indent=1)
    keys = ["id", "dur_s", "wpm", "visual_changes_per_min", "music_first_above_-45_s",
            "music_lands_s (1 s level within 6 dB of median)", "first_hit_s", "first_sentence_end_s",
            "first_visual_change_s", "start_level_vs_median_db", "sections_per_min", "n_sections", "risers_per_min",
            "hits_per_min", "dropouts_per_min", "last_word_to_end_s", "end_level_vs_median_db", "fade_last_4s_db",
            "chroma_end_vs_start_cos", "music_range_db", "gaps_ge_0p5", "gap_swell_db", "tempo", "pulse_clarity",
            "minor_sections_share", "drums_within_10db_share"]
    for r in rows:
        print({k: r.get(k) for k in keys}, r["voice_minus_music"], r["texture_at_changes_vs_random"],
              {x: r["hits_at_visual_changes"].get(x) for x in ("share", "null_mean", "p_value")})


if __name__ == "__main__":
    main()
