#!/usr/bin/env python3
"""studio-make: one command from a topic (or a finished script) to a rendered Short + thumbnails + titles.

  ./studio-make --niche explainer --topic "orca"
  ./studio-make --niche horror --premise "the building chat has one more member than the building has flats"
  ./studio-make --slug explainer-short-cookiecutter-shark --script backlog/explainer/explainer-short-cookiecutter-shark/script.md

Runs on the Mac as an orchestrator only; every heavy step runs on the Spark (CPU only, niced, inside the thread budget):

  script      claude -p (Spark) with pipeline/prompts/script_<niche>.md -> episodes/<slug>/script.md, originality gate
              (skipped when episodes/<slug>/script.md exists or --script is given)
  tts         Kokoro voice + word timings + mix (pipeline.audio.make) -> episodes/<slug>/audio/   } run in
  shots       claude -p with pipeline/prompts/shots_<niche>.md -> episodes/<slug>/shots.json         } parallel
  storyboard  pipeline.episodes.auto (anchors -> times, kit/holds/layout checks, zod) -> storyboard.json
  review      stills contact sheet -> claude -p looks at it and fixes shots.json -> rebuild (--review-rounds N)
  render      Remotion on the Spark (render lock, --concurrency 4) -> out/<slug>/<slug>_9x16.mp4 + contact sheet
  package     claude -p with pipeline/prompts/package.md -> titles.md, description.md, thumbs.json
  thumbs      thumbnail stills (thumbs kit) -> out/<slug>/thumbs/
  collect     copies titles/description into out/<slug>/ and writes out/<slug>/MANIFEST.md

--steps a,b,c runs only those steps; --from STEP runs STEP and everything after it. Each step's log is appended to
episodes/<slug>/make.log. Without claude on the Spark, the script step needs an existing script.md and the shots step an
existing shots.json (written by hand or by any agent); everything else is deterministic.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from pipeline.audio.script import parse  # noqa: E402

HOST = os.environ.get("SPARK_HOST", "dgx-spark")
REMOTE = "~/studio/app"
MODEL = os.environ.get("STUDIO_CLAUDE_MODEL", "opus")
STEPS = ["script", "tts", "shots", "storyboard", "review", "render", "package", "thumbs", "collect"]
ENV = ("export CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=4 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 TTS_THREADS=4; "
       "source ~/studio/app/scripts/spark_env.sh >/dev/null 2>&1; cd ~/studio/app")
TOOLS = ["Read", "Write", "Edit", "Glob", "Grep"]
EXAMPLE_THUMBS = {"explainer": "explainer-blue-whale", "horror": "horror-pinned-rules"}
PILOT = {"explainer": "explainer-orca", "horror": "horror-pinned-rules"}  # out/pilots/<x>/{titles,description}.md


class Fail(SystemExit):
    pass


class Make:
    def __init__(self, a):
        self.a = a
        self.niche = a.niche
        self.slug = a.slug
        self.ep = os.path.join(ROOT, "episodes", self.slug)
        self.out = os.path.join(ROOT, "out", self.slug)
        os.makedirs(self.ep, exist_ok=True)
        os.makedirs(self.out, exist_ok=True)
        self.logf = open(os.path.join(self.ep, "make.log"), "a")
        self.lock = threading.Lock()

    # ------------------------------------------------------------------ plumbing
    def log(self, msg: str):
        line = f"[{dt.datetime.now(dt.timezone.utc):%H:%M:%S}] {msg}"
        with self.lock:
            print(line, flush=True)
            self.logf.write(line + "\n")
            self.logf.flush()

    def run(self, cmd, check=True, env=None, stdin=None, timeout=None, quiet=False) -> str:
        if isinstance(cmd, str):
            cmd = ["bash", "-c", cmd]
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env={**os.environ, **(env or {})},
                           input=stdin, timeout=timeout)
        out = (r.stdout or "") + (r.stderr or "")
        with self.lock:
            self.logf.write(out[-20000:] + ("\n" if out and not out.endswith("\n") else ""))
            self.logf.flush()
        if not quiet and out.strip():
            print("\n".join("    " + l for l in out.strip().splitlines()[-12:]), flush=True)
        if check and r.returncode != 0:
            raise Fail(f"command failed ({r.returncode}): {' '.join(cmd)[:300]}")
        return out

    def spark(self, cmd: str, **kw) -> str:
        return self.run(["ssh", "-o", "ServerAliveInterval=30", HOST, f"bash -c {shlex.quote(ENV + '; ' + cmd)}"], **kw)

    def sync(self):
        self.run(["scripts/spark_sync.sh"], env={"SKIP_NPM": "1"}, quiet=True)

    def pull(self, *rel):
        """Pull files the Spark wrote (repo-relative paths) back to the Mac (source of truth)."""
        for r in rel:
            dst = os.path.join(ROOT, r)
            os.makedirs(os.path.dirname(dst.rstrip("/")), exist_ok=True)
            self.run(["rsync", "-a", f"{HOST}:{REMOTE}/{r}", dst], check=False, quiet=True)

    def claude(self, prompt: str, name: str, extra_tools=(), timeout=1800) -> str:
        """Run claude -p on the Spark in ~/studio/app with file tools + a few allowed commands."""
        if not self.has_claude():
            raise Fail(f"{name}: claude is not available on {HOST}")
        tools = TOOLS + list(extra_tools)
        pfile = f"/tmp/studio-make-{self.slug}-{name}.md"
        self.run(["ssh", HOST, f"cat > {pfile}"], stdin=prompt, quiet=True)
        cmd = (f"timeout {timeout} claude -p --model {shlex.quote(MODEL)} --permission-mode acceptEdits "
               f"--allowedTools {' '.join(shlex.quote(t) for t in tools)} < {pfile}")
        t0 = time.time()
        out = self.spark(cmd, check=False, timeout=timeout + 60, quiet=True)
        self.log(f"{name}: claude -p done in {time.time() - t0:.0f}s: {out.strip().splitlines()[-1][:200] if out.strip() else '(no output)'}")
        return out

    _claude = None

    def has_claude(self) -> bool:
        if Make._claude is None:
            r = subprocess.run(["ssh", "-o", "ConnectTimeout=10", HOST, "bash -lc 'command -v claude || ls ~/.local/bin/claude'"],
                               capture_output=True, text=True)
            Make._claude = r.returncode == 0
        return Make._claude

    def paragraphs(self) -> list[str]:
        sc = parse(open(os.path.join(self.ep, "script.md"), encoding="utf-8").read())
        return [" ".join(s.words) for s in sc.segments]

    def fill(self, name: str, **kw) -> str:
        src = open(os.path.join(ROOT, "pipeline", "prompts", name), encoding="utf-8").read()
        return src.format(slug=self.slug, niche=self.niche, **kw)

    # ------------------------------------------------------------------ steps
    def step_script(self):
        path = os.path.join(self.ep, "script.md")
        rel = f"episodes/{self.slug}/script.md"
        if self.a.script:
            shutil.copyfile(os.path.join(ROOT, self.a.script), path)
            self.log(f"script: copied {self.a.script}")
        elif os.path.exists(path) and not self.a.rewrite:
            self.log("script: using existing script.md")
        else:
            if not self.a.topic:
                raise Fail("script: no script.md and no --topic/--premise")
            self.sync()
            self.claude(self.fill(f"script_{self.niche}.md", topic=self.a.topic), "script",
                        ["Bash(python3 scripts/originality_check.py:*)"], timeout=2400)
            self.pull(rel)
            if not os.path.exists(path):
                raise Fail("script: claude did not write script.md")
        self.sync()
        out = self.spark(f"nice -n 10 python3 scripts/originality_check.py {rel} research/corpus research/library/transcripts",
                         check=False)
        if "PASS" not in out:
            raise Fail("script: originality gate did not PASS (see make.log); fix the script and rerun --from script")
        n = len(self.paragraphs())
        words = sum(len(p.split()) for p in self.paragraphs())
        self.log(f"script: originality PASS, {n} paragraphs, {words} words")

    def step_tts(self):
        self.sync()
        t0 = time.time()
        self.spark(f"nice -n 10 python -m pipeline.audio.make episodes/{self.slug}/script.md --id {self.slug} "
                   f"--niche {self.niche} --meta-out episodes/{self.slug}/audio", timeout=3600, quiet=True)
        self.pull(f"episodes/{self.slug}/audio/")
        rep = json.load(open(os.path.join(self.ep, "audio", "report.json")))
        self.log(f"tts: {rep['mix']['duration_s']:.1f}s mix in {time.time() - t0:.0f}s")

    def step_shots(self):
        path = os.path.join(self.ep, "shots.json")
        if os.path.exists(path) and not self.a.reshot:
            self.log("shots: using existing shots.json")
            return
        paras = self.paragraphs()
        listing = "\n".join(f"  {i + 1}. {p}" for i, p in enumerate(paras))
        self.sync()
        self.claude(self.fill(f"shots_{self.niche}.md", n_paras=len(paras), paragraphs=listing), "shots",
                    ["Bash(python3 -m pipeline.episodes.auto:*)"], timeout=2400)
        self.pull(f"episodes/{self.slug}/shots.json")
        if not os.path.exists(path):
            raise Fail("shots: claude did not write shots.json")

    def step_storyboard(self):
        self.sync()
        out = self.spark(f"python3 -m pipeline.episodes.auto {self.slug}", check=False)
        self.pull(f"episodes/{self.slug}/storyboard.json")
        last = out.strip().splitlines()[-1] if out.strip() else ""
        if last.strip() != "PASS":
            raise Fail("storyboard: auto build failed (see make.log); fix shots.json and rerun --from storyboard")
        warns = [l for l in out.splitlines() if l.startswith("WARN")]
        self.log(f"storyboard: PASS ({len(warns)} warnings)")

    def stills_times(self) -> list[float]:
        sb = json.load(open(os.path.join(self.ep, "storyboard.json")))
        ts, t = [0.0], 0.0
        for s in sb["scenes"]:  # two stills per scene: after its first beat and near its end
            ts += [round(t + s["duration"] * 0.35, 2), round(t + s["duration"] * 0.85, 2)]
            t += s["duration"]
        ts.append(round(t - 0.1, 2))
        return ts

    def step_review(self):
        done = len([f for f in os.listdir(self.out) if f.startswith("review_r")])
        for r in range(done, done + self.a.review_rounds):
            ts = self.stills_times()
            sheet = f"out/{self.slug}/review_r{r + 1}.jpg"
            self.run(["scripts/spark_stills.sh", f"episodes/{self.slug}/storyboard.json", ",".join(map(str, ts)), sheet],
                     quiet=True)
            remote_sheet = f"studio/out/stills/{self.slug}_storyboard.jpg"
            self.log(f"review {r + 1}: contact sheet {sheet}")
            if not self.has_claude():
                self.log("review: no claude on the Spark, skipping the automatic fix pass")
                return
            self.claude(self.fill("review.md", sheet=remote_sheet, times=", ".join(map(str, ts))), f"review{r + 1}",
                        ["Bash(python3 -m pipeline.episodes.auto:*)"], timeout=1500)
            self.pull(f"episodes/{self.slug}/shots.json")
            self.step_storyboard()

    def step_render(self):
        name = f"{self.slug}/{self.slug}_9x16.mp4"
        t0 = time.time()
        self.run(["scripts/spark_render.sh", "Storyboard", name],
                 env={"CONC": "4", "PROPS": f"episodes/{self.slug}/storyboard.json"}, timeout=3 * 3600, quiet=True)
        mp4 = os.path.join(self.out, f"{self.slug}_9x16.mp4")
        self.log(f"render: {os.path.relpath(mp4, ROOT)} ({os.path.getsize(mp4) / 1e6:.1f} MB) in {time.time() - t0:.0f}s")
        # contact sheet (Spark ffmpeg): 12 frames across the video
        self.spark(f"cd studio/out/{self.slug} && D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 {self.slug}_9x16.mp4) && "
                   f"nice -n 10 ffmpeg -v error -y -threads 2 -i {self.slug}_9x16.mp4 -vf \"fps=12/$D,scale=270:-2,tile=6x2:padding=4\" "
                   f"-frames:v 1 -q:v 3 {self.slug}_sheet.jpg", check=False, quiet=True)
        self.run(["rsync", "-a", f"{HOST}:{REMOTE}/studio/out/{self.slug}/{self.slug}_sheet.jpg", self.out + "/"],
                 check=False, quiet=True)

    def step_package(self):
        self.sync()
        # out/ is not synced to the Spark: hand the pilot's titles/description to the prompt inline
        pilot = os.path.join(ROOT, "out", "pilots", PILOT[self.niche])
        ex = {k: (open(os.path.join(pilot, f"{k}.md")).read()[:6000] if os.path.exists(os.path.join(pilot, f"{k}.md"))
                  else "(missing)") for k in ("titles", "description")}
        self.claude(self.fill("package.md", example=EXAMPLE_THUMBS[self.niche], titles_example=ex["titles"],
                              description_example=ex["description"]), "package", timeout=1200)
        self.pull(*(f"episodes/{self.slug}/{f}" for f in ("titles.md", "description.md", "thumbs.json")))
        missing = [f for f in ("titles.md", "description.md", "thumbs.json") if not os.path.exists(os.path.join(self.ep, f))]
        if missing:
            raise Fail(f"package: missing {missing}")

    def step_thumbs(self):
        self.run(["scripts/thumbs_render.sh", f"episodes/{self.slug}/thumbs.json"], env={"OUT": f"{self.slug}/thumbs"},
                 timeout=1800, quiet=True)
        n = len([f for f in os.listdir(os.path.join(self.out, "thumbs")) if f.endswith(".jpg")])
        self.log(f"thumbs: {n} images in out/{self.slug}/thumbs/")

    def step_collect(self):
        for f in ("titles.md", "description.md"):
            if os.path.exists(os.path.join(self.ep, f)):
                shutil.copyfile(os.path.join(self.ep, f), os.path.join(self.out, f))
        files = sorted(os.path.relpath(os.path.join(d, f), self.out) for d, _, fs in os.walk(self.out) for f in fs)
        meta = parse(open(os.path.join(self.ep, "script.md"), encoding="utf-8").read()).meta
        with open(os.path.join(self.out, "MANIFEST.md"), "w") as f:
            f.write(f"# {self.slug}\n\n{meta.get('title', '')}\n\nBuilt by `studio-make` "
                    f"({dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC). Sources in `episodes/{self.slug}/`.\n\n")
            f.write("\n".join(f"- `{x}`" for x in files) + "\n")
        self.log(f"collect: out/{self.slug}/ ({len(files)} files)")

    # ------------------------------------------------------------------ driver
    def go(self, steps: list[str]):
        self.log(f"=== studio-make {self.slug} ({self.niche}) steps={','.join(steps)}")
        t0 = time.time()
        i = 0
        while i < len(steps):
            st = steps[i]
            if st == "tts" and i + 1 < len(steps) and steps[i + 1] == "shots":
                # independent: voice on the Spark CPU while claude storyboards (anchors are words, not seconds)
                err = []
                th = threading.Thread(target=lambda: self._safe(self.step_tts, err))
                th.start()
                self._safe(self.step_shots, err)
                th.join()
                if err:
                    raise err[0]
                i += 2
                continue
            getattr(self, f"step_{st}")()
            i += 1
        self.log(f"=== done in {(time.time() - t0) / 60:.1f} min -> out/{self.slug}/")

    @staticmethod
    def _safe(fn, err):
        try:
            fn()
        except BaseException as e:  # noqa: BLE001
            err.append(e)


def slugify(niche: str, text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"the", "a", "an", "of", "and", "to", "in", "on", "at", "is", "that", "my", "our", "your"}
    keep = [w for w in words if w not in stop][:5] or ["untitled"]
    return f"{niche}-{'-'.join(keep)}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--niche", choices=["explainer", "horror"])
    ap.add_argument("--topic", help="explainer topic (or horror premise)")
    ap.add_argument("--premise", help="horror premise (alias of --topic)")
    ap.add_argument("--slug", help="episode folder name (default: from niche + topic)")
    ap.add_argument("--script", help="use this script.md (repo-relative) instead of writing one")
    ap.add_argument("--steps", help=f"comma list from {','.join(STEPS)}")
    ap.add_argument("--from", dest="start", choices=STEPS, help="run this step and all after it")
    ap.add_argument("--review-rounds", type=int, default=1)
    ap.add_argument("--rewrite", action="store_true", help="rewrite script.md even if it exists")
    ap.add_argument("--reshot", action="store_true", help="regenerate shots.json even if it exists")
    ap.add_argument("--force", action="store_true", help="allow a slug that has a hand-written builder")
    a = ap.parse_args()
    a.topic = a.topic or a.premise
    if a.script and not a.slug:
        m = re.search(r"^id:\s*(\S+)", open(os.path.join(ROOT, a.script)).read(), re.M)
        a.slug = m.group(1) if m else os.path.basename(os.path.dirname(a.script))
    if not a.niche:
        a.niche = "horror" if (a.slug or "").startswith("horror") else "explainer"
    if not a.slug:
        if not a.topic:
            ap.error("give --topic/--premise, --slug or --script")
        a.slug = slugify(a.niche, a.topic)
        base, k = a.slug, 2
        # never take over a hand-built episode (pilots): a derived slug that exists without a make.log gets a suffix
        while (os.path.isdir(os.path.join(ROOT, "episodes", a.slug))
               and not os.path.exists(os.path.join(ROOT, "episodes", a.slug, "make.log"))):
            a.slug = f"{base}-v{k}"
            k += 1
    from pipeline.episodes.build import BUILDERS
    if a.slug in BUILDERS and not a.force:
        ap.error(f"{a.slug} has a hand-written builder (pipeline/episodes/*_eps.py); studio-make would overwrite its "
                 f"storyboard. Pick another --slug or pass --force")
    steps = STEPS
    if a.steps:
        steps = [s.strip() for s in a.steps.split(",")]
        bad = [s for s in steps if s not in STEPS]
        if bad:
            ap.error(f"unknown steps {bad}")
    elif a.start:
        steps = STEPS[STEPS.index(a.start):]
    try:
        Make(a).go(steps)
    except Fail as e:
        print(f"studio-make: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
