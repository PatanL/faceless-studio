"""Collect story_sound.py + analyze.py + motion_spikes.py results into one numbers-only JSON (no audio, no words).

Adds: SFX onsets vs on-screen motion onsets (circular-shift null), music-track identity across the references
(chroma cross-correlation of the Demucs music stems: same recording -> r >= 0.8), and top-by-views vs the rest.

usage (Mac sound venv): python -I story_sound_summary.py WORK_DIR ricks24_metrics.json out.json
  WORK_DIR has meas/<key>.json, an/<id>_music.json, vis/<key>_motion.json, stems/<id>/music.flac
"""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import align  # noqa: E402

OURS = {"turk_v4": "story-chess-turk v4 (out/story-chess-turk/story-chess-turk_v4.mp4, Demucs)",
        "turk_v6": "story-chess-turk v6 (Demucs)", "turk_v7": "story-chess-turk v7 = current mix (Demucs)",
        "turk_v7_true": "story-chess-turk current mix, our own stems", "vasa_v1": "story-vasa v1 mix (Demucs)",
        "vasa_v1_true": "story-vasa v1 mix, our own stems",
        "ab_B": "A/B side B: Turk voice + audio profile story_ricks (Demucs); side A = turk_v7 (bit-identical remix)",
        "ab_B_true": "A/B side B, our own stems",
        "ab_B_tight": "side B with the profile's pause tightening applied to the cached voice (Demucs)",
        "ab_B_tight_true": "side B tightened, our own stems"}


def med(xs):
    xs = [x for x in xs if x is not None and np.isfinite(x)]
    return round(float(np.median(xs)), 2) if xs else None


def rng(xs):
    xs = [x for x in xs if x is not None and np.isfinite(x)]
    return [round(float(min(xs)), 2), round(float(max(xs)), 2)] if xs else None


def row(m, an, motion):
    v, s, r, b, g = m["voice"], m["sfx"], m["room"], m["bed"], m["gap"]
    T = m["duration_s"]
    out = {
        "duration_s": T,
        "mix_I_lufs": m["mix"]["I_lufs"], "mix_true_peak_dbtp": m["mix"]["true_peak_dbtp"], "mix_LRA_lu": m["mix"]["LRA_lu"],
        "voice_I_lufs": m["integrated"]["voice_lufs"], "nonvoice_I_lufs": m["integrated"]["nonvoice_lufs"],
        "voice_minus_nonvoice_I_lu": g["voice_minus_nonvoice_integrated_lu"],
        "voice_minus_bed_M_speech_p10": g["voice_minus_bed_M_under_speech_p10_p50_p90"][0],
        "voice_minus_bed_M_speech_p50": g["voice_minus_bed_M_under_speech_p10_p50_p90"][1],
        "voice_minus_bed_M_speech_p90": g["voice_minus_bed_M_under_speech_p10_p50_p90"][2],
        "speech_share": g["speech_share"],
        "bed_entry_s": b["bed_entry_s"], "bed_present_share": b["bed_present_share"],
        "bed_S_range_p10_p95_db": b["bed_S_range_p10_p95_db"], "bed_dropouts": len(b["bed_dropouts"]),
        "bed_level_steps_ge_4db": b["bed_level_steps_ge_4db"],
        "sfx_per_min": s["per_min"], "sfx_kinds_per_min": s["kinds_per_min"],
        "sfx_level_vs_voice_lu_p10_p50_p90": s["level_vs_voice_lu_p10_p50_p90"],
        "sfx_level_by_kind_median_lu": s["level_by_kind_median"], "sfx_share_in_speech": s["share_in_speech"],
        "sfx_interval_s_p50": s["interval_s_p50"],
        "sfx_on_visual_change_0p3s": {k: s["sync"].get("sfx_on_a_visual_change_within_0p3s", {}).get(k)
                                      for k in ("share", "null_mean", "p_value")},
        "visual_changes_with_sfx_0p3s": {k: s["sync"].get("visual_changes_with_sfx_within_0p3s", {}).get(k)
                                         for k in ("share", "null_mean", "p_value")},
        "nonvoice_harmonic_share_p50": m["nonvoice_texture"]["harmonic_share_p10_p50_p90"][1],
        "ambience_like_share": m["nonvoice_texture"]["ambience_like_windows_share"],
        "speech_gaps_ge_0p12s_per_min": round(r["speech_gaps_ge_0p12s"] / (T / 60), 1),
        "speech_gap_len_s_p50": (r["gap_len_s_p50_p90"] or [None])[0],
        "room_vocals_in_gaps_db_rel_speech_p50": (r["vocals_stem_in_gaps_db_rel_speech_p10_p50_p90"] or [None, None])[1],
        "room_mix_in_gaps_db_rel_speech_p50": (r["mix_in_gaps_db_rel_speech_p10_p50_p90"] or [None, None])[1],
        "mix_digital_silence_share": r["mix_digital_silence_share_50ms_below_-60dbfs"],
        "breaths_per_min": r["breaths_per_min"],
        "voice_f0_median_hz": v.get("f0_median_hz"), "voice_f0_p5_p95_hz": v.get("f0_p5_p95_hz"),
        "voice_f0_range_p5_p95_st": v.get("f0_range_p5_p95_st"), "voice_f0_std_st": v.get("f0_std_st"),
        "voice_f0_1s_spread_st": v.get("f0_1s_median_spread_st_p10_p90"),
        "voice_M_spread_p10_p90_lu": v.get("voice_M_spread_p10_p90_lu"), "voice_S_spread_p10_p95_lu": v.get("voice_S_spread_p10_p95_lu"),
        "voice_crest_db_p50": (v.get("crest_db_p10_p50_p90") or [None, None])[1],
        "voice_crest_db_p10_p50_p90": v.get("crest_db_p10_p50_p90"),
        "voice_ltas_db_rel_total": v.get("ltas_db_rel_total"),
        "voice_brightness_db": v.get("brightness_db_4k_8k_minus_300_1k"), "voice_presence_db": v.get("presence_db_1k_4k_minus_300_1k"),
        "voice_centroid_hz": v.get("spectral_centroid_hz"),
        "wps": v.get("wps"), "wps_3s_cv": v.get("wps_3s_cv"), "wps_3s_p10_p50_p90": v.get("wps_3s_p10_p50_p90"),
    }
    if b.get("you_see"):
        out["you_see_bed_step_db"] = [y["bed_step_db"] for y in b["you_see"]]
        out["you_see_dropout_within_1s"] = [int(y["drop_within_1s"]) for y in b["you_see"]]
    if motion is not None:
        on = [e["t"] for e in s["events"]]
        sp = [x["t"] for x in motion["spikes"]]
        out["motion_onsets_per_min"] = round(len(sp) / (T / 60), 1)
        if on and sp:
            a = align(on, sp, 0.2, T, [])
            out["sfx_on_motion_onset_0p2s"] = {k: a.get(k) for k in ("share", "null_mean", "p_value", "matched_offset_median_s")}
            a2 = align(sp, on, 0.2, T, [])
            out["motion_onsets_with_sfx_0p2s"] = {k: a2.get(k) for k in ("share", "null_mean", "p_value")}
    out["sfx_events"] = [{"t": e["t"], "dur": e["dur"], "kind": e["kind"], "level_vs_voice_lu": e["level_vs_voice_lu"]}
                         for e in s["events"]]
    if an:
        t = an["tempo"]
        secs = an["sections"]
        out["music"] = {
            "tempo_bpm_librosa": t["global_bpm_librosa"], "tempo_window_p25_p75": t["window_bpm_p25_p75"],
            "pulse_clarity_median": t["pulse_clarity_median"], "share_windows_clear_pulse": t["share_windows_clear_pulse_gt_0p3"],
            "sections": len(secs), "section_len_s_median": med([x["dur"] for x in secs]),
            "boundaries_per_min": an["boundaries"]["coarse_per_min"],
            "keys": [x["key"] for x in secs], "minor_share": round(float(np.mean([x["key"].endswith("min") for x in secs])), 2),
            "harmonic_share_median": med([x["harmonic_share"] for x in secs]),
            "centroid_hz_median": med([x["centroid_hz"] for x in secs]),
            "hi_tonal_onsets_per_s_median": med([x["hi_tonal_onsets_per_s"] for x in secs]),
            "onsets_per_s_median": med([x["onsets_per_s"] for x in secs]),
            "drums_minus_music_db_median": med([x.get("drums_minus_music_db") for x in secs]),
            "bass_minus_music_db_median": med([x.get("bass_minus_music_db") for x in secs]),
            "other_minus_music_db_median": med([x.get("other_minus_music_db") for x in secs]),
            "band_dBA_rel_total_median": {k: med([x["band_dBA_rel_total"][k] for x in secs]) for k in secs[0]["band_dBA_rel_total"]},
            "octave_db_rel_max_median": {k: med([x["octave_db_rel_max"][k] for x in secs]) for k in secs[0]["octave_db_rel_max"]},
            "risers": len(an["risers"]), "hits": len(an["hits"]), "dropouts": len(an["dropouts"]),
            "boundaries_vs_visual_changes": {k: an["alignment"]["coarse_boundaries_vs_setting_changes"].get(k)
                                             for k in ("share", "null_mean", "p_value")},
            "first_music_s": an["starts_ends"]["first_music_above_-45_lufs_s"],
        }
        if out.get("you_see_bed_step_db") is not None:
            pass
    return out


def identity(work, ids):
    """max chroma cross-correlation between the references' music stems (10 s windows of A slid over B)"""
    import librosa
    import soundfile as sf
    from scipy.signal import resample_poly
    ch = {}
    for i in ids:
        x, sr = sf.read(os.path.join(work, "stems", i, "music.flac"), dtype="float32", always_2d=True)
        y = resample_poly(x.mean(1), 1, 2)
        c = librosa.feature.chroma_cqt(y=y, sr=sr // 2, hop_length=2205)  # 0.1 s
        c = (c - c.mean(1, keepdims=True)) / (c.std(1, keepdims=True) + 1e-9)
        ch[i] = c
    res = {}
    for a in ids:
        for b in ids:
            if a >= b:
                continue
            A, B = ch[a], ch[b]
            best = -1
            for w0 in range(0, A.shape[1] - 100, 50):
                win = A[:, w0:w0 + 100]
                for l in range(0, B.shape[1] - 100, 2):
                    r = float((win * B[:, l:l + 100]).mean())
                    best = max(best, r)
            res[f"{a}|{b}"] = round(best, 2)
    # self-similarity baseline: same video, windows >= 10 s apart
    selfr = []
    for a in ids:
        A = ch[a]
        best = -1
        for w0 in range(0, A.shape[1] - 100, 50):
            win = A[:, w0:w0 + 100]
            for l in range(0, A.shape[1] - 100, 2):
                if abs(l - w0) < 100:
                    continue
                best = max(best, float((win * A[:, l:l + 100]).mean()))
        selfr.append(round(best, 2))
    return res, dict(zip(ids, selfr))


def main():
    work, metrics, out = sys.argv[1], sys.argv[2], sys.argv[3]
    vids = json.load(open(metrics))["videos"]
    ranked = sorted(vids, key=lambda k: -vids[k]["views"])
    rank = {k: i + 1 for i, k in enumerate(ranked)}
    refs, ours = {}, {}
    for f in sorted(glob.glob(os.path.join(work, "meas", "*.json"))):
        m = json.load(open(f))
        k = m["key"]
        anp = os.path.join(work, "an", f"{k}_music.json")
        an = json.load(open(anp)) if os.path.exists(anp) else None
        mk = k.replace("_true", "")
        mp = os.path.join(work, "vis", f"{mk}_motion.json")
        motion = json.load(open(mp)) if os.path.exists(mp) else None
        r = row(m, an, motion)
        if k in vids:
            r["views"] = vids[k]["views"]
            r["views_rank_of_24"] = rank[k]
            r["you_see_t"] = vids[k]["pace"].get("you_see_t", [])
            refs[k] = r
        else:
            ours[k] = r
    top = [k for k in refs if refs[k]["views_rank_of_24"] <= 8]
    rest = [k for k in refs if refs[k]["views_rank_of_24"] > 8]
    keys = [k for k, v in next(iter(refs.values())).items() if isinstance(v, (int, float)) and k not in ("views", "views_rank_of_24")]
    mkeys = [k for k, v in next(iter(refs.values()))["music"].items() if isinstance(v, (int, float))]

    def group(ks):
        g = {k: {"median": med([refs[i][k] for i in ks]), "range": rng([refs[i][k] for i in ks])} for k in keys}
        g.update({f"music.{k}": {"median": med([refs[i]["music"][k] for i in ks]), "range": rng([refs[i]["music"][k] for i in ks])}
                  for k in mkeys})
        for kind in ("whoosh", "impact", "pop_click", "foley", "tonal", "riser"):
            g[f"sfx_{kind}_per_min"] = {"median": med([refs[i]["sfx_kinds_per_min"].get(kind, 0) for i in ks]),
                                        "range": rng([refs[i]["sfx_kinds_per_min"].get(kind, 0) for i in ks])}
            lv = [refs[i]["sfx_level_by_kind_median_lu"].get(kind) for i in ks]
            g[f"sfx_{kind}_level_vs_voice_lu"] = {"median": med(lv), "range": rng(lv)}
        g["sfx_on_motion_onset_share"] = {"median": med([refs[i].get("sfx_on_motion_onset_0p2s", {}).get("share") for i in ks]),
                                          "null_median": med([refs[i].get("sfx_on_motion_onset_0p2s", {}).get("null_mean") for i in ks])}
        g["sfx_on_visual_change_share"] = {"median": med([refs[i]["sfx_on_visual_change_0p3s"]["share"] for i in ks]),
                                           "null_median": med([refs[i]["sfx_on_visual_change_0p3s"]["null_mean"] for i in ks])}
        g["n"] = len(ks)
        return g

    ident, selfr = identity(work, sorted(refs))
    res = {
        "note": "RicksClips3000 story Shorts, audio measured 2026-11-02 on the Mac (Demucs htdemucs_ft stems, "
                "research/music/tools/story_sound.py + analyze.py + motion_spikes.py + story_sound_summary.py). Only the 8 "
                "references with an audio track on the Spark (refs/ig/ricks720_*.webm, the PARITY 8) are measured: the 16 "
                "others in refs/lanes/ricks/vid are video-only downloads. Numbers only; no audio, words or stems leave "
                "~/faceless-work/ricks-sound.",
        "method": {
            "gap": "momentary (0.4 s) loudness, voice stem minus music bed (non-voice stem with detected SFX frames "
                   "interpolated over), under speech (analyze.py speech mask)",
            "sfx": "events in the Demucs drums stem rising >= 6 dB over their 2.5 s rolling median in >= 25 % of the "
                   "audible mel bands (or >= 8 dB in half the bands < 300 Hz); kinds by duration/attack/centroid/"
                   "harmonicity. Validated on our Turk mix against its cue list: crisp SFX found, soft long swells and "
                   "quiet ticks missed, so ref counts are lower bounds; tonal SFX that Demucs files under 'other' are missed",
            "level_vs_voice": "peak 100 ms loudness of the event minus the voice's median momentary loudness in speech",
            "sync": "share of SFX onsets within 0.3 s of a visual change (frame_metrics transitions + cuts, 240p) or "
                    "0.2 s of a motion onset (motion_spikes.py), vs a 2000-shift circular null",
            "room": "speech gaps >= 120 ms from a 20 ms voice mask; vocals stem and full mix RMS in the gaps re speech RMS",
            "voice": "pYIN f0 60-400 Hz; crest = peak/RMS per 0.5 s speech window; LTAS bands re total 50 Hz-16 kHz",
            "groups": "top = views rank <= 8 of the 24 RicksClips Shorts; rest = the other measured refs",
        },
        "refs": refs,
        "groups": {"all8": group(sorted(refs)), "top_by_views": group(top), "rest": group(rest),
                   "top_ids": top, "rest_ids": rest},
        "music_identity": {"pairwise_max_chroma_r": ident, "self_repeat_max_chroma_r": selfr,
                           "pairs_r_ge_0p8": [k for k, v in ident.items() if v >= 0.8]},
        "ours": ours,
        "ours_labels": {k: OURS.get(k, k) for k in ours},
    }
    json.dump(res, open(out, "w"), indent=1)
    print("refs", len(refs), "ours", len(ours), "top", top, "rest", rest)


if __name__ == "__main__":
    main()
