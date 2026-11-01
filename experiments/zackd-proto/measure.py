"""Run the zackd reference palette/caption measurement (VISUAL_GRAMMAR 4.1 / 12) on our render.
Spark only, CPU:  CUDA_VISIBLE_DEVICES="" nice -n 10 python -I measure.py out/zackd-proto.mp4
Reuses ~/studio/tmp_zackd_palette/palette.py (not in the repo)."""
import json, os, shutil, sys, tempfile
sys.path.insert(0, os.path.expanduser("~/studio/tmp_zackd_palette"))
import palette  # noqa: E402

mp4 = os.path.abspath(sys.argv[1])
d = tempfile.mkdtemp()
os.makedirs(os.path.join(d, "proto"))
os.symlink(mp4, os.path.join(d, "proto", "proto.mp4"))
palette.IDS = ["proto"]
out = os.path.join(d, "m.json")
palette.main(d, out)
r = json.load(open(out))["proto"]
h = r["hue_share_30deg"]
blue = h["180-210"] + h["210-240"]
warm = h["0-30"] + h["30-60"]
print(json.dumps({k: r[k] for k in ("luma_median", "luma_p10_p90", "sat_median", "center_minus_corner_luma",
                                    "caption_center_y", "caption_band_h", "caption_width_p90")}
                 | {"blue_share": round(blue, 3), "warm_share": round(warm, 3), "palette_top5": r["palette"][:5]}, indent=1))
shutil.rmtree(d)
