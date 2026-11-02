#!/usr/bin/env python3
"""Refresh the Status column of research/library/STORY_TOPIC_QUEUE.md.

A queue topic counts as used once episodes/<slug> exists. Only the Status cell of the
queue table is rewritten; nothing else in the file changes. Run from anywhere:

    python3 research/library/story_queue_status.py          # update in place
    python3 research/library/story_queue_status.py --check  # print only
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "research/library/STORY_TOPIC_QUEUE.md"
EPISODES = REPO / "episodes"

ROW = re.compile(r"^\| (\d+) \| (story-[a-z0-9-]+) \|(.*)\| ([^|]*) \|$")


def main() -> int:
    check_only = "--check" in sys.argv
    lines = QUEUE.read_text().split("\n")
    changed = 0
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if not m:
            continue
        rank, slug, middle, status = m.groups()
        used = (EPISODES / slug).is_dir()
        new = f"used (episodes/{slug})" if used else "open"
        print(f"{rank:>2} {slug:26} {new}")
        if status.strip() != new:
            lines[i] = f"| {rank} | {slug} |{middle}| {new} |"
            changed += 1
    if changed and not check_only:
        QUEUE.write_text("\n".join(lines))
        print(f"updated {changed} row(s)")
    nxt = [l for l in lines if ROW.match(l) and ROW.match(l).group(4).strip() == "open"]
    if nxt:
        print("next open:", ROW.match(nxt[0]).group(2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
