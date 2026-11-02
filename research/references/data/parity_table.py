"""Markdown table: the 8 RicksClips refs, v4 (key ours) and a v5 key, from the check outputs. usage: parity_table.py <v5key> <v5_pace.json>"""
import json, math, sys
v5, v5pace = sys.argv[1], sys.argv[2]
R = ["7xS87iActkU","VS1Z_Q-Klt8","Mz72MuPgnGY","5WMQhPObNqQ","ZDy3xXA2iHk","GM9UKnZ6JFw","jpFJ8Z_F-qU","0m6G8pDtzNs"]
pace = {e["file"]: e for e in json.load(open("pace.json"))}
def pz(k):
    if k == "ours": return pace["ours_captions.json"]
    if k == v5: return json.load(open(v5pace))[0]
    return next(e for f, e in pace.items() if k in f)
def row(k):
    e = json.load(open(f"out/{k}_events.json")); c = json.load(open(f"out/{k}_cam.json"))
    f = json.load(open(f"f30root/out/r_{k}/qa/frames30.json")); a = json.load(open(f"out/{k}_look.json"))["all"]; p = pz(k)
    sa, sb = a["shadow_a_b_med"][0][0], a["shadow_a_b_med"][1][0]
    return [p["wps"], p["n_gaps_0_8"], e["n_cuts"], f["counts"]["jump"], round(100*c["moving"]), c["speed_pct_25_50_75_90"][1],
            c["moves_per_10s"], round(100*c["quiet_zoom_active"]), a["sat_pct_10_50_90"][1], round(a["colourfulness_med"][0]),
            a["luma_p50_med"][0], a["nonink_p5_pct_10_50_90"][1], round(math.hypot(sa, sb)), round(a["shadow_hue_deg_pct_25_50_75"][1]),
            a["ink_edge_pct_25_50_75"][1], round(100*a["soft_edge_pct_25_50_75"][1], 1), a["acutance_med"][0]]
OURS = "ours"
H = ["wps","pauses>=0.8s","hard cuts","1-frame jumps","moving %","median px/f","moves/10s","quiet zoom %","sat","colourf.","luma p50","non-ink p5","shadow C","shadow hue","ink edge","soft edge %","acutance"]
rows = {k: row(k) for k in R + ["ours", v5]}
print("| Check | " + " | ".join(r[:4] for r in R) + " | refs range | v4 | v5 |")
print("|---|" + "---|"*(len(R)+3))
for i, h in enumerate(H):
    vals = [rows[k][i] for k in R]
    print(f"| {h} | " + " | ".join(str(v) for v in vals) + f" | {min(vals)}-{max(vals)} | {rows[OURS][i]} | **{rows[v5][i]}** |")
