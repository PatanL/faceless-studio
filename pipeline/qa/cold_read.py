"""Cold-reader "makes sense" test: build the prompts, score the answers (see COLD_READ_PROMPT.md).

usage:
  python3 -m pipeline.qa.cold_read prompt <script.md> [--shots FILE] [--pass A|B]
  python3 -m pipeline.qa.cold_read score <reader_A.json> --key KEY.json [--b reader_B.json] [--grade id=0|1 ...] [--out report.md]

Key (written by the author before reading any answer):
  {"slug": "...", "items": [
     {"id": "why-current", "part": "why", "text": "the current reverses and pushes them back",
      "all": [["current", "tide", "water"], ["revers", "turn", "switch", "flip"]]}, ...]}
  part is who | what | why | twist. An item counts as retold when every group in "all" has at least one
  alternative in the reader's retell (who + what_happened + why + twist, lower-cased substring match). Keyword
  matching is lenient on purpose; check the misses by eye and settle them with --grade id=1 (or id=0 for a false hit).

Understanding U = 100 x (0.15 who + 0.35 what + 0.30 why + 0.20 twist coverage).
Friction F = 100 - 8 per reread line marked "lost" - 2 per "slowed" - 6 per jump that blocks understanding
             - 1 per other jump - 2 per "sounds wrong" - 1 per unexplained term (floor 0).
Score = (U + F) / 2.  PASS (required before voicing) = coverage 1.0, no "lost" line, no blocking jump (pass A).
Stdlib only, no network: the reading itself is done by a fresh agent (no repo access, no context).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
PROMPT = REPO / "pipeline" / "qa" / "COLD_READ_PROMPT.md"
W = dict(who=0.15, what=0.35, why=0.30, twist=0.20)


def narration(path) -> list[str]:
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    from pipeline.qa.util import narration_paragraphs
    return narration_paragraphs(path)


def build_prompt(script, shots=None, pas="A") -> str:
    t = PROMPT.read_text()
    body = t.split("## The prompt (cold_read.py fills {NARRATION} and, for pass B, {SHOTS})", 1)[1].strip()
    nar = "\n".join(narration(script))
    sh = ""
    if shots:
        sh = ("SHOT LIST (what is on screen during each line; you now also see the pictures):\n"
              + pathlib.Path(shots).read_text().strip())
    out = body.replace("{NARRATION}", nar).replace("{SHOTS}", sh)
    if pas == "B":
        out = ("Second pass. Same story, but now you also get the shot list, as if you watched the video. Answer again "
               "from scratch with the same JSON keys, and add `fixed_by_pictures` (what the images cleared up) and "
               "`still_confusing`.\n\n" + out)
    return out


def _retell(r: dict) -> dict:
    def flat(x):
        if isinstance(x, str):
            return x
        if isinstance(x, dict):
            return " ".join(flat(v) for v in x.values())
        if isinstance(x, list):
            return " ".join(flat(v) for v in x)
        return str(x)
    return {p: flat(r.get(k, "")).lower() for p, k in (("who", "who"), ("what", "what_happened"), ("why", "why"), ("twist", "twist"))}


def score(reader: dict, key: dict, grades: dict) -> dict:
    rt = _retell(reader)
    alltext = " ".join(rt.values())
    items = []
    for it in key["items"]:
        hit = all(any(alt.lower() in alltext for alt in grp) for grp in it["all"])
        if it["id"] in grades:
            hit = bool(grades[it["id"]])
        items.append(dict(id=it["id"], part=it["part"], text=it["text"], hit=hit, graded=it["id"] in grades))
    cov = {}
    for p in W:
        ps = [i for i in items if i["part"] == p]
        cov[p] = round(sum(i["hit"] for i in ps) / len(ps), 2) if ps else 1.0
    rr = reader.get("reread_lines") or []
    lost = [x for x in rr if isinstance(x, dict) and x.get("level") == "lost"]
    slowed = [x for x in rr if x not in lost]
    jumps = reader.get("logic_jumps") or []
    block = [x for x in jumps if isinstance(x, dict) and x.get("blocks_understanding")]
    wrong = reader.get("sounds_wrong") or []
    terms = reader.get("unexplained_terms") or []
    U = 100 * sum(W[p] * cov[p] for p in W)
    F = max(0.0, 100 - 8 * len(lost) - 2 * len(slowed) - 6 * len(block) - (len(jumps) - len(block)) - 2 * len(wrong) - len(terms))
    flags = dict(reread_lines=rr, logic_jumps=jumps, sounds_wrong=wrong, unexplained_terms=terms)
    return dict(score=round((U + F) / 2, 1), understanding=round(U, 1), friction=round(F, 1), coverage=cov, items=items,
                flags=flags, counts=dict(lost=len(lost), slowed=len(slowed), blocking_jumps=len(block), jumps=len(jumps),
                                         sounds_wrong=len(wrong), terms=len(terms)),
                hook=reader.get("hook"), confidence=reader.get("confidence"),
                passed=all(v == 1.0 for v in cov.values()) and not lost and not block)


def render(name, a, b=None) -> str:
    out = [f"# Cold read: {name}", "",
           f"**Pass A (narration only): {a['score']} / 100, {'PASS' if a['passed'] else 'FAIL'}** "
           f"(coverage who {a['coverage']['who']}, what {a['coverage']['what']}, why {a['coverage']['why']}, "
           f"twist {a['coverage']['twist']}; understanding {a['understanding']}, friction {a['friction']}: {a['counts']}; "
           f"reader confidence {a['confidence']})."]
    if b:
        out.append(f"**Pass B (narration + shot list): {b['score']} / 100** (coverage {b['coverage']}; {b['counts']}).")
    h = a.get("hook") or {}
    out += ["", f"Hook after line 1: keep watching {h.get('keep_watching')}/5; question in the reader's head: "
            f"\"{h.get('question_in_my_head', '')}\"", "", "## Key beats", ""]
    for i in a["items"]:
        mark = "ok" if i["hit"] else "MISSED"
        out.append(f"- [{mark}] {i['part']}: {i['text']}" + (" (graded by hand)" if i["graded"] else ""))
    for lab, k in (("Reread lines (lost / slowed)", "reread_lines"), ("Logic jumps", "logic_jumps"), ("Sounds wrong", "sounds_wrong"),
                   ("Unexplained terms", "unexplained_terms")):
        v = a["flags"][k]
        out += ["", f"## {lab} (pass A): {len(v)}", ""]
        out += [f"- {json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x}" for x in v] or ["- none"]
    if b:
        out += ["", "## Pass B: still flagged with the pictures", ""]
        for k in ("reread_lines", "logic_jumps", "sounds_wrong", "unexplained_terms"):
            for x in b["flags"][k]:
                out.append(f"- {k}: {json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x}")
    return "\n".join(out) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompt")
    p.add_argument("script")
    p.add_argument("--shots")
    p.add_argument("--pass", dest="pas", default="A", choices=["A", "B"])
    s = sub.add_parser("score")
    s.add_argument("reader")
    s.add_argument("--key", required=True)
    s.add_argument("--b")
    s.add_argument("--grade", action="append", default=[])
    s.add_argument("--out")
    s.add_argument("--json")
    a = ap.parse_args(argv)
    if a.cmd == "prompt":
        print(build_prompt(a.script, a.shots, a.pas))
        return 0
    key = json.loads(pathlib.Path(a.key).read_text())
    grades = {g.split("=")[0]: int(g.split("=")[1]) for g in a.grade}
    ra = score(json.loads(pathlib.Path(a.reader).read_text()), key, grades)
    bj = json.loads(pathlib.Path(a.b).read_text()) if a.b else None
    rb = score(bj, key, grades) if bj and "what_happened" in bj else None
    md = render(key.get("slug", a.reader), ra, rb)
    if bj and not rb:  # pass B answered as a delta (fixed_by_pictures / still_confusing / real_jumps)
        md += "\n## Pass B (with the shot list): still confusing\n\n" + "\n".join(f"- {x}" for x in bj.get("still_confusing", []))
        md += "\n\n## Pass B: jumps that still block understanding\n\n" + "\n".join(f"- {x}" for x in bj.get("real_jumps", []))
        md += "\n\n## Pass B: fixed by the pictures\n\n" + "\n".join(f"- {x}" for x in bj.get("fixed_by_pictures", [])) + "\n"
    if a.out:
        pathlib.Path(a.out).write_text(md)
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps(dict(A=ra, B=rb), indent=1))
    print(md if not a.out else f"{key.get('slug')}: A {ra['score']} ({'PASS' if ra['passed'] else 'FAIL'})"
          + (f", B {rb['score']}" if rb else "") + f" -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
