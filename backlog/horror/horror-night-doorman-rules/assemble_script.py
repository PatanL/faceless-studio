"""Fill script.tmpl.md with the measured numbers and tables from build.py -> script.md (stdlib, Mac-safe)."""
import io
import json
import os
import re
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402

tl = json.load(open(os.path.join(HERE, "timeline.json")))
buf = io.StringIO()
with redirect_stdout(buf):
    B.tables()
out = buf.getvalue()


def section(part, name):
    blk = out.split(f"# {part.upper()}  runtime")[1]
    blk = blk.split("\n# P")[0]
    s = blk.split(f"## {name}\n")[1]
    return s.split("\n## ")[0].strip()


def narr(seq):
    rows = []
    for e in seq:
        if e[0] == "#":
            continue
        if e[0] == "~":
            rows.append(f"[pause: {e[2]}]")
            continue
        rows.append(("VOICE: " if e[1] == "V" else "") + e[2])
    return "\n\n".join(rows)


v = {}
for k in ("p1", "p2"):
    s = tl[k]["stats"]
    K = k.upper()
    v.update({f"{K}_RT": round(s["runtime_s"], 1), f"{K}_W": s["words"], f"{K}_WPM": s["wpm_overall"], f"{K}_WPMS": s["wpm_speaking"],
              f"{K}_HOOKW": s["core_hook_words"], f"{K}_HOOKS": s["core_hook_s"], f"{K}_CONTRA": round(s["contradiction_s"], 1),
              f"{K}_W10": s["words_first_10s"], f"{K}_JMED": s["jolt_median_s"], f"{K}_JMAX": s["jolt_max_gap_s"], f"{K}_JN": s["jolts"],
              f"{K}_NPM": s["numbers_per_min"], f"{K}_NUMS": ", ".join(s["distinct_numbers"]), f"{K}_SMED": s["sentence_median"],
              f"{K}_PUNCH": round(100 * s["punch_share_le4"]), f"{K}_Q": s["questions"], f"{K}_QPM": s["questions_per_min"],
              f"{K}_LINES": section(k, "LINES"), f"{K}_SCENES": section(k, "SCENES")})
v["P1_NARR"] = narr(B.L.P1)
v["P2_NARR"] = narr(B.L.P2)
t = open(os.path.join(HERE, "script.tmpl.md")).read()
t = re.sub(r"\{([A-Z0-9_]+)\}", lambda m: str(v[m.group(1)]) if m.group(1) in v else m.group(0), t)
open(os.path.join(HERE, "script.md"), "w").write(t)
left = re.findall(r"\{[A-Z0-9_]+\}", t)
print("script.md written", len(t), "chars; unfilled:", left)
