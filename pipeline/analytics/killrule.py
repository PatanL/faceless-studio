"""Kill rule (OPERATOR_DESIGN 5.17).

  python -m pipeline.analytics.killrule [--dry-run]

Only YouTube rows with window 7d count, one per published video (latest real row per post_key), in publish order.
n < after_videos (30) -> insufficient. median >= target (10k) -> continue. Else if the last-10 median >= target/2
and the Theil-Sen slope > 0 and the rule has not been extended yet -> extend (re-check after 15 more videos; until
then the verdict stays extend). Else -> stop. L5 acts on the verdict (stop pauses the loop and writes HUMAN.md).
"""
from __future__ import annotations

import argparse
import json
import sys

from ._common import EXIT_OK, config, dpath, iso, is_real, jsonl_read, median, now_utc, read_json, write_json_atomic

EXTEND_BY = 15


def theil_sen(ys: list[float]) -> float | None:
    sl = [(ys[j] - ys[i]) / (j - i) for i in range(len(ys)) for j in range(i + 1, len(ys))]
    return median(sl)


def series() -> list[dict]:
    latest: dict[str, dict] = {}
    for r in jsonl_read(dpath("metrics.jsonl")):
        if r.get("platform") == "youtube" and r.get("window") == "7d" and is_real(r) and r.get("views") is not None:
            latest[r["post_key"]] = r
    pub = {p["post_key"]: p.get("published_at") for p in jsonl_read(dpath("posts.jsonl")) if p.get("published_at")}
    return sorted(latest.values(), key=lambda r: (pub.get(r["post_key"]) or r.get("at") or "", r["post_key"]))


def evaluate(views: list[float], prev: dict | None = None, after: int = 30, target: float = 10000,
             extend_min: float | None = None, extend_by: int = EXTEND_BY) -> dict:
    extend_min = target / 2 if extend_min is None else extend_min
    prev = prev or {}
    n = len(views)
    out = {"v": 1, "at": iso(now_utc()), "n_videos": n, "target_views_7d": target,
           "median_views_7d": median(views), "first10_median": median(views[:10]),
           "last10_median": median(views[-10:]), "theil_sen_slope_per_video": None,
           "extended_once": bool(prev.get("extended_once")), "n_at_extend": prev.get("n_at_extend")}
    if n >= 2:
        s = theil_sen(views)
        out["theil_sen_slope_per_video"] = None if s is None else round(s, 2)
    med, last10, slope = out["median_views_7d"], out["last10_median"], out["theil_sen_slope_per_video"]
    if n < after:
        out["verdict"] = "insufficient"
        out["explanation"] = f"{n} of {after} YouTube videos have 7-day numbers"
    elif med >= target:
        out["verdict"] = "continue"
        out["explanation"] = f"median 7-day views {med:.0f} >= {target:.0f}"
    elif out["extended_once"] and n < (out["n_at_extend"] or 0) + extend_by:
        out["verdict"] = "extend"
        out["explanation"] = (f"extended at n={out['n_at_extend']}; re-check at n={(out['n_at_extend'] or 0) + extend_by} "
                              f"(median {med:.0f}, last-10 {last10:.0f}, slope {slope})")
    elif not out["extended_once"] and last10 >= extend_min and (slope or 0) > 0:
        out["verdict"] = "extend"
        out["extended_once"] = True
        out["n_at_extend"] = n
        out["explanation"] = (f"median {med:.0f} < {target:.0f} but last-10 median {last10:.0f} >= {extend_min:.0f} and "
                              f"slope {slope:+.1f}/video > 0: extend once by {extend_by} videos")
    else:
        out["verdict"] = "stop"
        out["explanation"] = (f"median {med:.0f} < {target:.0f}; last-10 median {last10:.0f}, slope {slope}"
                              + ("; already extended once" if out["extended_once"] else ""))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.analytics.killrule")
    ap.add_argument("--dry-run", action="store_true", help="print only")
    a = ap.parse_args(argv)
    kr = config().get("kill_rule", {})
    rows = series()
    prev = read_json(dpath("killrule.json"))
    out = evaluate([float(r["views"]) for r in rows], prev, int(kr.get("after_videos", 30)),
                   float(kr.get("target_views_7d", 10000)), kr.get("extend_last10_min"),
                   int(kr.get("extend_videos", EXTEND_BY)))
    out["post_keys"] = [r["post_key"] for r in rows]
    print(json.dumps({k: v for k, v in out.items() if k != "post_keys"}, indent=1))
    if not a.dry_run:
        write_json_atomic(dpath("killrule.json"), out)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
