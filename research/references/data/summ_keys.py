import json
import sys; K=sys.argv[1:]
print("key | dur | cuts | flashes | trans | f30 jumps | hold drift move moving moving_any | speed p50 p90 | moves/10s peak50 fwhm50 leneq25/50/75 snaps | quiet zoom act pushin rate | unfit tileonly")
for k in K:
    e=json.load(open(f"out/{k}_events.json")); c=json.load(open(f"out/{k}_cam.json"))
    f=json.load(open(f"f30root/out/r_{k}/qa/frames30.json"))
    print(k, e["duration"], e["n_cuts"], e["n_flashes"], e["n_transitions"], f["counts"]["jump"], "|", c["hold"],c["drift"],c["move"],c["moving"],c["moving_any"],"|",c["speed_pct_25_50_75_90"][1],c["speed_pct_25_50_75_90"][3],"|",c["moves_per_10s"],c["move_peak_pct_25_50_75_90"][1:2],c["move_fwhm_pct_25_50_75"][1:2],c["move_len_eq_pct_25_50_75"],c["snaps_attack_le3_peak_ge25"],"|",c["quiet_zoom_active"],c["quiet_pushin_share"],c["quiet_zoom_rate_pct_med"],"|",c["unfit_frames"],c["tile_only_frames"])
print()
print("cuts at:"); 
for k in K:
    e=json.load(open(f"out/{k}_events.json")); print(k, e["cuts"], "flashes", e["flashes"], "trans", [(t["start"],t["dur"]) for t in e["transitions"]][:30])
print()
for k in K:
    L=json.load(open(f"out/{k}_look.json")); a=L["all"]
    print(k, "luma50",a["luma_p50_med"],"mean",a["luma_mean_pct_10_50_90"],"p1",a["luma_p1_med"],"np5",a["nonink_p5_pct_10_50_90"],"blk",a["black_area_share_med"],a["frames_black_area_over_1pct"],"sat",a["sat_pct_10_50_90"],"colf",a["colourfulness_med"])
    print("    shadow ab",a["shadow_a_b_med"],"bneg",a["shadow_b_negative_share"],"hue",a["shadow_hue_deg_pct_25_50_75"],"| hi ab",a["highlight_a_b_med"],"bpos",a["highlight_b_positive_share"],"| ink_edge",a["ink_edge_pct_25_50_75"],"inkpx",a["ink_px_share_med"],"| soft",a["soft_edge_pct_25_50_75"],a["frames_soft_edge_over_40pct"],"acu",a["acutance_med"])
    if "before" in L:
        for s in ("before","after"):
            b=L[s]; print("   ",s,L["split_t"],"luma",b["luma_mean_pct_10_50_90"][1],"frame_b",b["frame_b_med"],"sat",b["sat_pct_10_50_90"][1],"shadow b",b["shadow_a_b_med"][1])
