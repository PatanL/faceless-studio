"""Ratio of each composition's render time to the Base runs that bracket it.

usage: python3 -I summarize.py results/results_run*.tsv
Prints one markdown row per (run, composition): seconds, bracketing Base mean, ratio, load at start.
"""
import csv
import sys


def rows(path):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main(paths):
    print("| run | composition | s (450 f) | Base s | ratio | load1 |")
    print("|---|---|---|---|---|---|")
    for p in paths:
        rs = rows(p)
        run = p.rsplit("/", 1)[-1].replace("results_", "").replace(".tsv", "")
        for i, r in enumerate(rs):
            if r["comp"] == "Base":
                continue
            prev = next((rs[j] for j in range(i - 1, -1, -1) if rs[j]["comp"] == "Base"), None)
            nxt = next((rs[j] for j in range(i + 1, len(rs)) if rs[j]["comp"] == "Base"), None)
            bases = [float(b["seconds"]) for b in (prev, nxt) if b]
            status = r.get("status", "ok")
            load = r.get("load1_start") or r.get("load1")
            if status != "ok" or not bases:
                print(f"| {run} | {r['comp']} | {r['seconds']} | - | {status} | {load} |")
                continue
            base = sum(bases) / len(bases)
            print(f"| {run} | {r['comp']} | {r['seconds']} | {base:.1f} | {float(r['seconds']) / base:.2f} | {load} |")


if __name__ == "__main__":
    main(sys.argv[1:])
