"""Fill script.tmpl.md with the measured numbers and tables from build.py -> script.md.
usage: python3 render_script.py [ORIGINALITY_RESULT]"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402

st = B.stats()
J, jmed, jmax = B.jolts()
lines = []
for it in B.ITEMS:
    if it["kind"] == "line":
        lines.append(f"| {B.mmss(it['start'])} | {it['dur']:.2f} | {it['spk']} | {it['text']} | {it['opts'].get('screen', '')} |")
    else:
        lines.append(f"| {B.mmss(it['start'])} | {it['dur']:.2f} | — | *[timed silence {it['dur']} s]* | {it['opts'].get('screen', '')} |")
scenes, t = [], 0.0
sc = B.build_scenes()
for i, s in enumerate(sc, 1):
    scenes.append(f"| {i} | {s['id']} | {B.mmss(t)} | {B.mmss(t + s['duration'])} | {s.get('notes', '')} |")
    t += s["duration"]
rep = {
    "RUNTIME": f"{B.RUNTIME:.1f}", "WORDS": str(st["words"]), "WPM": f"{st['wpm_overall']:.0f}", "WPMS": f"{st['wpm_speaking']:.0f}",
    "WPMA": f"{st['wpm_alert_lines']:.0f}", "HOOK_S": f"{st['core_hook_s']:.1f}", "RULE_S": f"{st['rule_word_s']:.1f}",
    "CONTRA_S": f"{st['contradiction_s']:.1f}", "JMED": f"{jmed:.1f}", "JMAX": f"{jmax:.1f}", "JN": str(len(J)),
    "NUMS": f"{st['numbers_per_min']:.1f}", "YOU": f"{100 * st['you_sentence_share']:.0f}", "SMED": str(st["sentence_median_all"]),
    "SMEDN": str(st["sentence_median_narrator"]), "PUNCH": f"{100 * st['punch_share_all']:.0f}",
    "GLINT": f"{B.at('a2:Please'):.1f}", "YET": B.mmss(B.at("n28:yet.")), "NSCENES": str(len(sc)),
    "LINES": "\n".join(lines),
    "SPOKEN": "\n".join(f"{B.L.SPEAKER_NAME[it['spk']].split(' (')[0]}: {it['text']}" if it["kind"] == "line"
                        else f"[timed silence {it['dur']} s]" for it in B.ITEMS), "SCENES": "\n".join(scenes),
    "ORIG": sys.argv[1] if len(sys.argv) > 1 else "PENDING",
}
s = open(os.path.join(HERE, "script.tmpl.md")).read()
for k, v in rep.items():
    s = s.replace("{{" + k + "}}", v)
assert "{{" not in s, s[s.index("{{"):s.index("{{") + 40]
open(os.path.join(HERE, "script.md"), "w").write(s)
print("script.md written", len(s.split()), "words")
