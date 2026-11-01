#!/usr/bin/env python3
"""Rebuild script.md's generated sections (VO with timestamps, shot table) after a new TTS pass.
usage: python3 assemble_script.py   (reads script.md, replaces between the GENERATED markers)"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
def run(*a):
    return subprocess.run([sys.executable, *a], cwd=HERE, capture_output=True, text=True, check=True).stdout
vo = run("timing.py", "--md").split("\n#### ", 1)
vo = "#### " + vo[1].strip() + "\n"
shots = run("gen_storyboard.py", "--md").strip() + "\n"
p = os.path.join(HERE, "script.md")
s = open(p).read()
for tag, body in (("VO", vo), ("SHOTS", shots)):
    s = re.sub(rf"<!-- GENERATED:{tag} -->.*?<!-- /GENERATED:{tag} -->", lambda m: f"<!-- GENERATED:{tag} -->\n{body}<!-- /GENERATED:{tag} -->", s, flags=re.S)
open(p, "w").write(s)
print("script.md regenerated")
