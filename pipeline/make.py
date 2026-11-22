#!/usr/bin/env python3
"""studio-make: one command from a topic, a finished script, or an existing viral source video to a rendered Short +
thumbnails + titles.

  ./studio-make --niche explainer --topic "orca"
  ./studio-make --niche horror --premise "the building chat has one more member than the building has flats"
  ./studio-make --slug explainer-short-cookiecutter-shark --script backlog/explainer/explainer-short-cookiecutter-shark/script.md
  ./studio-make --source auto [--slot a|b] [--date YYYY-MM-DD] [--experiment EXP-003:treatment] [--variant k=v ...]
  ./studio-make --source fGcgWaswMns --budget-tokens 2500000           # an explicit source (id or URL)
  ./studio-make --slug op-20261102-a-sperm-whale --from review --review-notes episodes/op-.../review_notes.md

Modes. On the Mac (default) this is an orchestrator: every heavy step runs on the Spark over ssh (CPU only, niced,
inside the thread budget) and results are pulled back. With STUDIO_LOCAL=1 (or SPARK_HOST=local) it runs ON the
Spark (the operator loop): commands run here in the repo copy, sync/pull do nothing, and every deterministic step
holds a shared ~/studio/locks/code.lock so a Mac sync never lands mid-step.

Steps (in order):
  source      --source only: pick (pipeline.sources), transcript + annotation if the corpus lacks one (claude -p),
              beat skeleton -> episodes/<slug>/source.json, variant.json (experiment arm + learned rules)
  script      claude -p with pipeline/prompts/script_<niche>.md (script_explainer_source.md when source.json exists)
              -> episodes/<slug>/script.md, originality gate (+ a direct check against the source transcript)
              (skipped when episodes/<slug>/script.md exists or --script is given)
  tts         Kokoro voice + word timings + mix (pipeline.audio.make) -> episodes/<slug>/audio/   } run in
  shots       claude -p with pipeline/prompts/shots_<niche>.md -> episodes/<slug>/shots.json         } parallel
  storyboard  pipeline.episodes.auto (anchors -> times, kit/holds/layout checks, zod) -> storyboard.json + beatmap.json
  review      stills contact sheet -> claude -p looks at it and fixes shots.json -> rebuild (--review-rounds N,
              --review-notes FILE); a round that fails is rolled back and the make continues
  render      Remotion via scripts/render.sh: Spark (render lock, --concurrency CONC<=4), or the Mac when the Spark
              lock is held and the Mac has room (--concurrency 2) -> out/<slug>/<slug>_9x16.mp4 + contact sheet
  package     claude -p with pipeline/prompts/package.md -> titles.md, description.md, thumbs.json, package.json
  thumbs      thumbnail stills (thumbs kit) -> out/<slug>/thumbs/ (package.json thumb_pick filled in)
  collect     copies titles/description/package into out/<slug>/, writes out/<slug>/MANIFEST.md

--steps a,b,c runs only those steps; --from STEP runs STEP and everything after it. Each step's log is appended to
episodes/<slug>/make.log; episodes/<slug>/make_status.json is rewritten (atomically) after every step with the
status, steps done, per-claude-call token usage (from `claude -p --output-format json`) and outputs.

Safety (research/CODE_REVIEW_FINDINGS.md): a claude call's exit status is checked and its old outputs are moved aside
first, so a stale file can never count as success (F01); a new script invalidates shots.json (F02); the storyboard is
validated before it replaces the last good one and is pulled only on PASS (F03); a failed review round is rolled
back (F04); pulls are checked, retried once and verified (F06); the episode's own files are pushed explicitly (F07).

Exit codes: 0 ok (also --dry-run-claude), 1 step failed, 2 usage, 3 budget cap, 4 no source candidate,
5 dependency down (claude auth/unavailable, Spark unreachable), 6 blocked by a gate (originality, runtime < 61 s).
Env: SPARK_HOST (default dgx-spark), STUDIO_LOCAL, STUDIO_CLAUDE_MODEL (default opus), CONC (render concurrency,
default 4, cap 4), STUDIO_BUDGET_TOKENS (default per-video budget for --source makes, 2500000).
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import glob
import hashlib
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
LOCAL = os.environ.get("STUDIO_LOCAL") == "1" or HOST == "local"
REMOTE = "~/studio/app"
MODEL = os.environ.get("STUDIO_CLAUDE_MODEL", "opus")
STEPS = ["source", "script", "tts", "shots", "storyboard", "review", "render", "package", "thumbs", "collect"]
CLAUDE_STEPS = {"script", "shots", "review", "package"}  # (source needs claude only to annotate a new source)
THREADS = "export CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=4 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 TTS_THREADS=4 STUDIO_REQUIRE_ZOD=1"
ENV = f"{THREADS}; source ~/studio/app/scripts/spark_env.sh >/dev/null 2>&1; cd ~/studio/app"
TOOLS = ["Read", "Write", "Edit", "Glob", "Grep"]
EXAMPLE_THUMBS = {"explainer": "explainer-blue-whale", "horror": "horror-pinned-rules"}
PILOT = {"explainer": "explainer-orca", "horror": "horror-pinned-rules"}  # out/pilots/<x>/{titles,description}.md
MIN_RUNTIME_S = 61.0
DEFAULT_BUDGET = int(os.environ.get("STUDIO_BUDGET_TOKENS", "2500000"))
# rough weighted-token cost of one claude call per kind (for the "would exceed" budget check); measured on the Spark
EST_TOKENS = {"annotate": 400_000, "script": 600_000, "shots": 900_000, "review": 400_000, "package": 300_000}
# claude's own auth failure strings only (word-bounded): an ordinary failure whose text says "author", or a 401/403
# inside a session UUID or a cost number, must stay exit 1 (exit 5 pauses the whole operator loop)
AUTH_RX = re.compile(r"\bInvalid API key\b|Please run /login\b|\bOAuth token (?:has )?expired\b|"
                     r"\bnot logged in\b|\bauthentication_error\b|\bAPI Error: 40[13]\b|"
                     r"\bOAuth authentication is currently not supported\b", re.I)
EXIT_FAIL, EXIT_USAGE, EXIT_BUDGET, EXIT_NOTHING, EXIT_DEP, EXIT_GATE = 1, 2, 3, 4, 5, 6


class Fail(SystemExit):
    """A step failed. exit_code follows the shared table (1 failed, 3 budget, 4 nothing to do, 5 dependency, 6 gate)."""

    def __init__(self, msg="", exit_code: int = EXIT_FAIL, out: str = "", rc: int | None = None):
        super().__init__(msg)
        self.msg, self.exit_code, self.out, self.rc = str(msg), exit_code, out or "", rc

    def __str__(self):
        return self.msg


class Stop(Exception):
    """Clean stop (e.g. --dry-run-claude before the first claude call)."""


def sha256_file(path: str) -> str | None:
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_json_atomic(path: str, obj) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def spark_argv(cmd: str) -> list[str]:
    """argv that runs `cmd` in the Spark repo copy with the thread budget env (locally in STUDIO_LOCAL mode)."""
    if LOCAL:
        return ["bash", "-c", f"{THREADS}; source {shlex.quote(ROOT)}/scripts/spark_env.sh >/dev/null 2>&1; "
                              f"cd {shlex.quote(ROOT)}; {cmd}"]
    return ["ssh", "-o", "ServerAliveInterval=30", "-o", "ConnectTimeout=20", HOST, f"bash -c {shlex.quote(ENV + '; ' + cmd)}"]


def parse_claude_json(out: str) -> dict:
    """The result object `claude -p --output-format json` prints (last JSON line that has usage/result)."""
    for line in reversed((out or "").strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if isinstance(d, dict) and ("usage" in d or "result" in d or d.get("type") == "result"):
                return d
    return {}


def usage_of(res: dict) -> dict:
    u = res.get("usage") or {}
    d = {"input_tokens": int(u.get("input_tokens") or 0), "output_tokens": int(u.get("output_tokens") or 0),
         "cache_read_tokens": int(u.get("cache_read_input_tokens") or 0),
         "cache_creation_tokens": int(u.get("cache_creation_input_tokens") or 0),
         "cost_usd": round(float(res.get("total_cost_usd") or 0.0), 4)}
    d["weighted_tokens"] = int(d["input_tokens"] + d["output_tokens"] + d["cache_creation_tokens"] + 0.1 * d["cache_read_tokens"])
    return d


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
        self.status = self._load_status()

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
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env={**os.environ, **(env or {})},
                               input=stdin, timeout=timeout)
        except subprocess.TimeoutExpired as e:
            out = ((e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or ""))
            raise Fail(f"command timed out after {timeout}s: {' '.join(cmd)[:200]}", EXIT_FAIL, out, rc=124)
        out = (r.stdout or "") + (r.stderr or "")
        with self.lock:
            self.logf.write(out[-20000:] + ("\n" if out and not out.endswith("\n") else ""))
            self.logf.flush()
        if not quiet and out.strip():
            print("\n".join("    " + l for l in out.strip().splitlines()[-12:]), flush=True)
        if check and r.returncode != 0:
            code = EXIT_DEP if (cmd[:1] == ["ssh"] and r.returncode == 255) else EXIT_FAIL
            raise Fail(f"command failed ({r.returncode}): {' '.join(cmd)[:300]}", code, out, rc=r.returncode)
        return out

    def spark(self, cmd: str, **kw) -> str:
        return self.run(spark_argv(cmd), **kw)

    def local_path(self, rel: str) -> str:
        pre = f"episodes/{self.slug}/"
        if rel.startswith(pre):
            return os.path.join(self.ep, rel[len(pre):])
        return os.path.join(ROOT, rel)

    def sync(self):
        """Mac mode: push code (generic sync) and this episode's own files (op-* episodes are Spark-owned, F07)."""
        if LOCAL:
            return
        self.run(["scripts/spark_sync.sh"], env={"SKIP_NPM": "1"}, quiet=True)
        self.run(["rsync", "-a", "--update", "--exclude", "audio/", "--exclude", "*.prev", "--exclude", "*.tmp",
                  f"{self.ep}/", f"{HOST}:{REMOTE}/episodes/{self.slug}/"], quiet=True)

    def pull(self, *rel, optional=False):
        """Pull files the Spark wrote (repo-relative paths) back to the Mac. Checked, retried once, then verified with
        an rsync checksum dry run (F06). No-op in local mode (the Spark is where we are)."""
        if LOCAL:
            return
        for r in rel:
            dst = self.local_path(r) + ("/" if r.endswith("/") else "")
            os.makedirs(os.path.dirname(dst.rstrip("/")), exist_ok=True)
            src = f"{HOST}:{REMOTE}/{r}"
            try:
                try:
                    self.run(["rsync", "-a", src, dst], check=True, quiet=True)
                except Fail:
                    time.sleep(3)
                    self.run(["rsync", "-a", src, dst], check=True, quiet=True)
                diff = self.run(["rsync", "-a", "-c", "-n", "-i", src, dst], check=True, quiet=True) or ""
            except Fail as e:
                if optional:
                    self.log(f"pull: {r} not pulled ({e})")
                    continue
                raise Fail(f"pull {r} failed: {e}", e.exit_code)
            changed = [l for l in diff.splitlines() if l[:1] in (">", "c") or l.startswith("*deleting")]
            # macOS openrsync lists every file in a -c -n dry run even when it is identical: confirm by sha256
            changed = [l for l in changed if not self._same_bytes(r, l)]
            if changed:
                raise Fail(f"pull {r}: local copy differs from the Spark after pulling ({changed[:3]})")

    def _same_bytes(self, r: str, line: str) -> bool:
        """True when an rsync itemize line names a file whose local and Spark copies have the same sha256"""
        if line.startswith("*deleting") or len(line.split(None, 1)) < 2:
            return False
        name = line.split(None, 1)[1].strip()
        rel = r if not r.endswith("/") else r + name
        if r.endswith("/") is False and os.path.basename(r) != name:
            return False
        loc = sha256_file(self.local_path(rel))
        if loc is None:
            return False
        out = self.run(["ssh", HOST, f"sha256sum {REMOTE}/{shlex.quote(rel)}"], check=False, quiet=True) or ""
        return out.split()[:1] == [loc]

    @contextlib.contextmanager
    def code_lock(self):
        """Local mode: hold ~/studio/locks/code.lock shared for one deterministic step (a Mac sync takes it exclusive)."""
        if not LOCAL:
            yield
            return
        d = os.path.expanduser("~/studio/locks")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "code.lock"), "a") as f:
            t0 = time.time()
            while True:
                try:
                    fcntl.flock(f, fcntl.LOCK_SH | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.time() - t0 > 1800:
                        raise Fail("code.lock held by a sync for 30 min", EXIT_DEP)
                    time.sleep(2)
            try:
                yield
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    # ------------------------------------------------------------------ status + budget
    def _load_status(self) -> dict:
        p = os.path.join(self.ep, "make_status.json")
        try:
            st = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            st = {}
        st.update({"v": 1, "slug": self.slug, "niche": self.niche})
        st.setdefault("steps_done", [])
        st.setdefault("usage", {})
        st.setdefault("usage_total", {"weighted_tokens": 0, "cost_usd": 0.0})
        st.setdefault("outputs", {})
        return st

    def save_status(self, **kw):
        st = getattr(self, "status", None)
        if st is None:
            return
        st.update(kw)
        src = os.path.join(self.ep, "source.json")
        if os.path.exists(src) and not st.get("source_id"):
            try:
                st["source_id"] = json.load(open(src, encoding="utf-8")).get("source_id")
            except ValueError:
                pass
        with self.lock:
            write_json_atomic(os.path.join(self.ep, "make_status.json"), st)

    def record_usage(self, name: str, res: dict, secs: float, rc: int):
        st = getattr(self, "status", None)
        if st is None:
            return
        u = usage_of(res)
        u.update({"duration_s": round(secs), "exit": rc})
        with self.lock:
            cur = st["usage"].get(name)
            if cur:  # the same call again (a rerun): accumulate
                for k in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_creation_tokens",
                          "weighted_tokens", "duration_s"):
                    cur[k] = cur.get(k, 0) + u[k]
                cur["cost_usd"] = round(cur.get("cost_usd", 0) + u["cost_usd"], 4)
                cur["exit"] = rc
                cur["calls"] = cur.get("calls", 1) + 1
            else:
                st["usage"][name] = u
            st["usage_total"] = {"weighted_tokens": sum(v.get("weighted_tokens", 0) for v in st["usage"].values()),
                                 "cost_usd": round(sum(v.get("cost_usd", 0) for v in st["usage"].values()), 4)}
        self.save_status()

    def budget_check(self, name: str):
        cap = getattr(self.a, "budget_tokens", None)
        st = getattr(self, "status", None)
        if not cap or st is None:
            return
        kind = re.sub(r"\d+$", "", name)
        used = st["usage_total"]["weighted_tokens"]
        est = EST_TOKENS.get(kind, 300_000)
        if used + est > cap:
            st["budget_cap"] = "video"  # this per-video cap, never the weekly one (pipeline.ops reads it)
            raise Fail(f"{name}: budget: {used:,} weighted tokens used + ~{est:,} for {kind} > --budget-tokens {cap:,}",
                       EXIT_BUDGET)

    # ------------------------------------------------------------------ claude
    def claude(self, prompt: str, name: str, extra_tools=(), timeout=1800, outputs=(), edits=()) -> str:
        """Run claude -p (on the Spark, or here in local mode) in the repo copy, with file tools + a few allowed
        commands. outputs: repo-relative files the call must (re)create: they are moved aside first and must exist
        afterwards (F01). edits: files it edits in place (pulled afterwards; the caller snapshots them).
        Raises Fail: exit 5 when claude is unavailable or its auth failed, 3 over budget, 1 otherwise."""
        if getattr(self.a, "dry_run_claude", False):
            raise Stop(f"{name}: --dry-run-claude: stopping before the first claude call")
        self.budget_check(name)
        if not self.has_claude():
            raise Fail(f"{name}: claude is not available {'here' if LOCAL else 'on ' + HOST}", EXIT_DEP)
        tools = TOOLS + list(extra_tools)
        moved = []
        for r in outputs:  # F01: a stale output can never count as this call's result
            p = self.local_path(r)
            if os.path.exists(p):
                os.replace(p, p + ".prev")
                moved.append(p)
        if outputs and not LOCAL:
            q = " ".join(shlex.quote(r) for r in outputs)
            self.spark(f'for f in {q}; do [ -e "$f" ] && mv -f "$f" "$f.prev"; done; true', quiet=True)

        def restore():
            for p in moved:
                if not os.path.exists(p) and os.path.exists(p + ".prev"):
                    os.replace(p + ".prev", p)
            if outputs and not LOCAL:
                q = " ".join(shlex.quote(r) for r in outputs)
                try:
                    self.spark(f'for f in {q}; do [ -e "$f.prev" ] && [ ! -e "$f" ] && mv -f "$f.prev" "$f"; done; true',
                               quiet=True)
                except Fail:
                    pass

        pfile = f"/tmp/studio-make-{self.slug}-{name}.md"
        # every step lost turns to refused ad-hoc Bash (awk, python3 -c, heredocs) in the 2026-11-01 operator dry run
        bash_ok = [t[5:-1] for t in extra_tools if t.startswith("Bash(")]
        prompt += ("\n\nTools: the working directory is the repo (no cd needed). Read files with Read/Glob/Grep and "
                   "change them with Edit/Write; Bash is refused except "
                   + (", ".join(f"`{b.rstrip(':*')} ...`" for b in bash_ok) if bash_ok else "nothing") + ".\n")
        if LOCAL:
            with open(pfile, "w", encoding="utf-8") as f:
                f.write(prompt)
        else:
            self.run(["ssh", HOST, f"cat > {pfile}"], stdin=prompt, quiet=True)
        cmd = (f'PATH="$PATH:$HOME/.local/bin" timeout {timeout} nice -n 10 claude -p '
               f"--model {shlex.quote(MODEL)} --output-format json --permission-mode acceptEdits "
               f"--allowedTools {' '.join(shlex.quote(t) for t in tools)} < {pfile}")
        t0 = time.time()
        rc, out = 0, ""
        try:
            out = self.spark(cmd, check=True, timeout=timeout + 60, quiet=True) or ""
        except Fail as e:
            rc, out = (e.rc if e.rc is not None else 1), e.out
        res = parse_claude_json(out)
        self.record_usage(name, res, time.time() - t0, rc)
        text = (res.get("result") or out or "").strip()
        last = text.splitlines()[-1][:200] if text else "(no output)"
        if rc != 0 or res.get("is_error"):
            restore()
            # auth strings are looked for in claude's `result` when it is an error, else (no parseable JSON) in the
            # raw output; never in the agent's normal final text of a run that failed for another reason
            probe = (res.get("result") or "") if res.get("is_error") else ("" if res else out or "")
            code = EXIT_DEP if (AUTH_RX.search(probe[-2000:]) or rc in (126, 127)) else EXIT_FAIL
            self.log(f"{name}: claude -p FAILED (exit {rc}) after {time.time() - t0:.0f}s: {last}")
            raise Fail(f"{name}: claude -p failed (exit {rc}): {last}", code)
        self.log(f"{name}: claude -p done in {time.time() - t0:.0f}s "
                 f"({usage_of(res)['weighted_tokens']:,} weighted tokens, ${usage_of(res)['cost_usd']:.2f}): {last}")
        try:
            self.pull(*outputs, *edits)
        except Fail:
            restore()
            raise
        missing = [r for r in outputs if not os.path.exists(self.local_path(r))]
        if missing:
            restore()
            raise Fail(f"{name}: claude exited 0 but did not write {missing}")
        for p in moved:
            with contextlib.suppress(OSError):
                os.remove(p + ".prev")
        if outputs and not LOCAL:
            q = " ".join(shlex.quote(r + ".prev") for r in outputs)
            self.spark(f"rm -f {q}", check=False, quiet=True)
        return text

    _claude = None

    def has_claude(self) -> bool:
        if Make._claude is None:
            if LOCAL:
                Make._claude = bool(shutil.which("claude") or os.path.exists(os.path.expanduser("~/.local/bin/claude")))
            else:
                r = subprocess.run(["ssh", "-o", "ConnectTimeout=10", HOST, "bash -lc 'command -v claude || ls ~/.local/bin/claude'"],
                                   capture_output=True, text=True)
                Make._claude = r.returncode == 0
        return Make._claude

    # ------------------------------------------------------------------ helpers
    def paragraphs(self) -> list[str]:
        sc = parse(open(os.path.join(self.ep, "script.md"), encoding="utf-8").read())
        return [" ".join(s.words) for s in sc.segments]

    def narration_sha(self) -> str:
        return hashlib.sha256("\n\n".join(self.paragraphs()).encode()).hexdigest()

    def source(self) -> dict | None:
        p = os.path.join(self.ep, "source.json")
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None

    def variant(self) -> dict:
        p = os.path.join(self.ep, "variant.json")
        try:
            return json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            return {}

    def fill(self, name: str, **kw) -> str:
        src = open(os.path.join(ROOT, "pipeline", "prompts", name), encoding="utf-8").read()
        return src.format(slug=self.slug, niche=self.niche, **kw)

    def directives(self, step: str) -> str:
        d = (self.variant().get("directives_by_step") or {}).get(step) or []
        return "\n".join(f"- {x}" for x in d) or "- (none)"

    def stamp_shots(self):
        """Store the narration hash in shots.json so a later script change forces a replan (F02)."""
        p = os.path.join(self.ep, "shots.json")
        try:
            d = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError):
            return
        if isinstance(d, dict) and d.get("_script_sha") != self.narration_sha():
            d["_script_sha"] = self.narration_sha()
            write_json_atomic(p, d)

    # ------------------------------------------------------------------ steps
    def step_source(self):
        a = self.a
        src_path = os.path.join(self.ep, "source.json")
        rel_src = f"episodes/{self.slug}/source.json"
        if not getattr(a, "source", None):
            if os.path.exists(src_path):
                self.log("source: using existing source.json")
            else:
                self.log("source: no --source (topic/script mode), skipped")
            return
        sid = a.source_id
        if os.path.exists(src_path) and json.load(open(src_path)).get("source_id") == sid:
            self.log(f"source: using existing source.json ({sid})")
        else:
            out = self.spark(f"nice -n 10 python3 -m pipeline.sources transcript {shlex.quote(sid)}", check=False, quiet=True)
            tr = out.strip().splitlines()[-1] if out.strip() else ""
            if "sources:" in tr or not tr.endswith(".txt"):
                code = EXIT_NOTHING if "no transcript" in out or "unavailable" in out else EXIT_FAIL
                raise Fail(f"source: no transcript for {sid}: {tr[:200]}", code)
            self.log(f"source: transcript {tr}")
            have = self.spark(f"ls research/corpus/{self.niche}/{sid}.md research/corpus/{self.niche}/auto/{sid}.md "
                              f"2>/dev/null | head -1", check=False, quiet=True).strip()
            if have:
                self.log(f"source: annotation {have}")
            elif getattr(a, "dry_run_claude", False):
                self.log("source: no annotation and --dry-run-claude: skeleton from PLAYBOOK defaults only")
            else:
                prompt = self.spark(f"python3 -m pipeline.sources annotate-prompt {shlex.quote(sid)}", quiet=True)
                auto = f"research/corpus/{self.niche}/auto"
                self.claude(prompt, "annotate", [f"Bash(python3 -m pipeline.sources check-annotation:*)"], timeout=1800,
                            outputs=[f"{auto}/{sid}.md", f"{auto}/{sid}.index.json"])
                chk = self.spark(f"python3 -m pipeline.sources check-annotation {shlex.quote(sid)}", check=False, quiet=True)
                if chk.strip().splitlines()[-1:] != ["PASS"]:
                    raise Fail(f"source: annotation of {sid} is invalid: {chk.strip()[-300:]}")
                self.spark(f"python3 -m pipeline.sources mark {shlex.quote(sid)} annotated --slug {self.slug}", quiet=True)
            topic = f" --topic {shlex.quote(a.topic)}" if a.topic else ""
            mark = "" if getattr(a, "dry_run_claude", False) else f" --slug {self.slug}"  # a dry run never consumes a source
            self.spark(f"python3 -m pipeline.sources skeleton {shlex.quote(sid)} --out {rel_src}{mark}{topic}")
            self.pull(rel_src)
        vargs = "".join(f" --variant {shlex.quote(v)}" for v in (a.variant or []))
        if a.experiment:
            vargs += f" --experiment {shlex.quote(a.experiment)}"
        self.spark(f"python3 -m pipeline.sources variant --out episodes/{self.slug}/variant.json --source-json {rel_src}{vargs}")
        self.pull(f"episodes/{self.slug}/variant.json")
        src = self.source()
        self.log(f"source: {src['source_id']} ({src['format']}, {src.get('views') or 0:,} views, x{src.get('outlier_score')}) "
                 f"hook {src['hook'].get('code')}, {len(src['skeleton'])} skeleton beats; variant "
                 f"{self.variant().get('experiment_id')}:{self.variant().get('arm')} {self.variant().get('variables')}")

    def step_script(self):
        path = os.path.join(self.ep, "script.md")
        rel = f"episodes/{self.slug}/script.md"
        src = self.source()
        if self.a.script:
            shutil.copyfile(os.path.join(ROOT, self.a.script), path)
            self.log(f"script: copied {self.a.script}")
        elif os.path.exists(path) and not self.a.rewrite:
            self.log("script: using existing script.md")
        else:
            if not self.a.topic and not src:
                raise Fail("script: no script.md and no --topic/--premise/--source", EXIT_USAGE)
            self.sync()
            if src:
                prompt = self.fill("script_explainer_source.md", topic=self.a.topic or src.get("topic") or "",
                                   source_json=self.source_summary(src), skeleton_table=self.skeleton_table(src),
                                   hook_directive=self.hook_directive(src), variant_directives=self.directives("script"),
                                   learned_rules=self.learned_notes(), pacing=self.pacing_line(src))
                tools = ["Bash(python3 -m pipeline.sources origcheck:*)", "Bash(python3 scripts/originality_check.py:*)"]
            else:
                prompt = self.fill(f"script_{self.niche}.md", topic=self.a.topic)
                tools = ["Bash(python3 scripts/originality_check.py:*)"]
            self.claude(prompt, "script", tools, timeout=2400, outputs=[rel])
        self.sync()
        with self.code_lock():
            if src:
                out = self.spark(f"nice -n 10 python3 -m pipeline.sources origcheck {rel}", check=False)
            else:
                out = self.spark(f"nice -n 10 python3 scripts/originality_check.py {rel} research/corpus research/library/transcripts",
                                 check=False)
        last = out.strip().splitlines()[-1].strip() if out.strip() else ""
        if last != "PASS" and not (not src and "PASS" in out and "FAIL" not in out):
            raise Fail("script: originality gate did not PASS (see make.log); fix the script and rerun --from script", EXIT_GATE)
        n = len(self.paragraphs())
        words = sum(len(p.split()) for p in self.paragraphs())
        self.log(f"script: originality PASS, {n} paragraphs, {words} words")
        if src and not (180 <= words <= 300):
            raise Fail(f"script: {words} spoken words is outside 180-300 (target {src['target']['words']}); runtime would "
                       f"miss 65-85 s", EXIT_GATE)
        if src:
            plan = self.beat_plan()
            if plan and len(plan) != n:
                self.log(f"script: WARN beat_plan has {len(plan)} entries for {n} paragraphs (beatmap falls back to timing)")

    def step_tts(self):
        self.sync()
        t0 = time.time()
        with self.code_lock():
            self.spark(f"nice -n 10 python -m pipeline.audio.make episodes/{self.slug}/script.md --id {self.slug} "
                       f"--niche {self.niche} --meta-out episodes/{self.slug}/audio", timeout=3600, quiet=True)
        self.pull(f"episodes/{self.slug}/audio/")
        rep = json.load(open(os.path.join(self.ep, "audio", "report.json")))
        dur = rep["mix"]["duration_s"]
        self.log(f"tts: {dur:.1f}s mix in {time.time() - t0:.0f}s")
        if self.source() and dur < MIN_RUNTIME_S:
            raise Fail(f"tts: mix is {dur:.1f}s, under {MIN_RUNTIME_S:.0f}s (Shorts over 60 s only); lengthen the script "
                       f"and rerun --from script --rewrite", EXIT_GATE)

    def step_shots(self):
        path = os.path.join(self.ep, "shots.json")
        rel = f"episodes/{self.slug}/shots.json"
        need = bool(self.a.reshot or self.a.rewrite or self.a.script) or not os.path.exists(path)
        if not need:
            try:
                stored = json.load(open(path, encoding="utf-8")).get("_script_sha")
            except (ValueError, AttributeError):
                stored = "unreadable"
            if stored and stored != self.narration_sha():
                self.log("shots: the narration changed since shots.json was planned: replanning")
                need = True
        if not need:
            self.log("shots: using existing shots.json")
            return
        paras = self.paragraphs()
        listing = "\n".join(f"  {i + 1}. {p}" for i, p in enumerate(paras))
        self.sync()
        prompt = self.fill(f"shots_{self.niche}.md", n_paras=len(paras), paragraphs=listing)
        extra = self.directives("shots")
        if extra != "- (none)":
            prompt += ("\n\nThis episode's variant (an experiment arm or a learned rule; it overrides the defaults above "
                       f"where they differ):\n{extra}\n")
        self.claude(prompt, "shots", ["Bash(python3 -m pipeline.episodes.auto:*)"], timeout=2400, outputs=[rel])
        if not os.path.exists(path):
            raise Fail("shots: claude did not write shots.json")
        self.stamp_shots()

    def step_storyboard(self):
        self.sync()
        with self.code_lock():
            out = self.spark(f"python3 -m pipeline.episodes.auto {self.slug}", check=False)
        last = out.strip().splitlines()[-1] if out.strip() else ""
        if last.strip() != "PASS":
            raise Fail("storyboard: auto build failed (see make.log); fix shots.json and rerun --from storyboard")
        self.pull(f"episodes/{self.slug}/storyboard.json")  # only after PASS (F03)
        self.pull(f"episodes/{self.slug}/beatmap.json", optional=True)
        warns = [l for l in out.splitlines() if l.startswith("WARN")]
        self.log(f"storyboard: PASS ({len(warns)} warnings)")
        self.remix_score()

    def remix_score(self):
        """Explainers score their soundtrack from the storyboard (pipeline.audio.score, music "score"): once the
        storyboard exists, remix with the cached voice (timings unchanged) so the render picks up the composed music.
        The first TTS pass mixed with the fallback bed; a missing FluidSynth/SoundFont keeps that bed (logged)."""
        from pipeline.audio.config import NICHES, SCORE
        meta = open(os.path.join(self.ep, "script.md"), encoding="utf-8").read()
        fm = re.search(r"^music:\s*(\S+)", meta, re.M)
        marker = re.findall(r"\[music:\s*([^\]\s]+)", meta)
        music = marker[-1] if marker else (fm.group(1) if fm else NICHES.get(self.niche, {}).get("music"))
        if music != SCORE:
            return
        extra = f"episodes/{self.slug}/audio/sfx_events.json"
        extra = f" --extra-cues {extra}" if os.path.exists(os.path.join(ROOT, extra)) else ""
        t0 = time.time()
        with self.code_lock():
            self.spark(f"nice -n 10 python -m pipeline.audio.make episodes/{self.slug}/script.md --id {self.slug} "
                       f"--niche {self.niche} --reuse-tts --meta-out episodes/{self.slug}/audio{extra}",
                       timeout=1800, quiet=True)
        self.pull(f"episodes/{self.slug}/audio/")
        rep = json.load(open(os.path.join(self.ep, "audio", "report.json")))["mix"]
        sc = rep.get("score") or {}
        self.log(f"score: music={rep.get('music')} {len(sc.get('cues', []))} cues, {len(sc.get('stings', []))} stings, "
                 f"{len(sc.get('drops', []))} drop-outs, {rep['ffmpeg_ebur128']['I_lufs']} LUFS in {time.time() - t0:.0f}s"
                 + (f" (fallback: {rep['music_fallback_reason']})" if rep.get("music_fallback_reason") else ""))

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
        notes_file = getattr(self.a, "review_notes", None)
        notes = "(none)"
        if notes_file:
            p = notes_file if os.path.isabs(notes_file) else os.path.join(ROOT, notes_file)
            notes = open(p, encoding="utf-8").read().strip() or "(none)"
        shots = os.path.join(self.ep, "shots.json")
        sb = os.path.join(self.ep, "storyboard.json")
        for r in range(done, done + self.a.review_rounds):
            ts = self.stills_times()
            sheet = f"out/{self.slug}/review_r{r + 1}.jpg"
            with self.code_lock():
                self.run(["scripts/spark_stills.sh", f"episodes/{self.slug}/storyboard.json", ",".join(map(str, ts)), sheet],
                         quiet=True)
            remote_sheet = f"studio/out/stills/{self.slug}_storyboard.jpg"
            self.log(f"review {r + 1}: contact sheet {sheet}")
            if not self.has_claude():
                self.log("review: no claude available, skipping the automatic fix pass")
                return
            snap = {p: open(p, "rb").read() for p in (shots, sb) if os.path.exists(p)}  # F04 rollback point
            try:
                self.claude(self.fill("review.md", sheet=remote_sheet, times=", ".join(map(str, ts)), review_notes=notes),
                            f"review{r + 1}", ["Bash(python3 -m pipeline.episodes.auto:*)"], timeout=1500,
                            edits=[f"episodes/{self.slug}/shots.json"])
                self.step_storyboard()
                self.stamp_shots()
            except Stop:
                raise
            except Fail as e:
                self.log(f"review round {r + 1} rejected ({e}); restoring the last good shots.json/storyboard.json")
                for p, b in snap.items():
                    with open(p, "wb") as f:
                        f.write(b)
                if e.exit_code == EXIT_DEP:
                    raise
                self.step_storyboard()  # rebuild the restored plan on the Spark side too
                if e.exit_code == EXIT_BUDGET:
                    self.log("review: budget reached, skipping further review rounds")
                    return

    def step_render(self):
        name = f"{self.slug}/{self.slug}_9x16.mp4"
        t0 = time.time()
        conc = os.environ.get("CONC", "4")
        with self.code_lock():
            # scripts/render.sh: the Spark when its render lock is free, else the Mac if it has room (Mac mode only)
            out = self.run(["scripts/render.sh", "Storyboard", name],
                           env={"CONC": conc, "PROPS": f"episodes/{self.slug}/storyboard.json"}, timeout=3 * 3600,
                           quiet=True)
        slot = next((l.split("slot:", 1)[1].strip() for l in out.splitlines() if l.startswith("[render] slot:")), "?")
        mp4 = os.path.join(self.out, f"{self.slug}_9x16.mp4")
        self.log(f"render: {os.path.relpath(mp4, ROOT)} ({os.path.getsize(mp4) / 1e6:.1f} MB) in {time.time() - t0:.0f}s"
                 f" [slot: {slot}]")
        # contact sheet (Spark ffmpeg): 12 frames across the video
        self.spark(f"cd studio/out/{self.slug} && D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 {self.slug}_9x16.mp4) && "
                   f"nice -n 10 ffmpeg -v error -y -threads 2 -i {self.slug}_9x16.mp4 -vf \"fps=12/$D,scale=270:-2,tile=6x2:padding=4\" "
                   f"-frames:v 1 -q:v 3 {self.slug}_sheet.jpg", check=False, quiet=True)
        if LOCAL:
            sheet = os.path.join(ROOT, "studio", "out", self.slug, f"{self.slug}_sheet.jpg")
            if os.path.exists(sheet):
                shutil.copy2(sheet, self.out + "/")
        else:
            self.run(["rsync", "-a", f"{HOST}:{REMOTE}/studio/out/{self.slug}/{self.slug}_sheet.jpg", self.out + "/"],
                     check=False, quiet=True)
        rel_mp4 = os.path.relpath(mp4, ROOT) if LOCAL else f"studio/out/{name}"
        dur = (self.spark(f"ffprobe -v error -show_entries format=duration -of csv=p=0 {shlex.quote(rel_mp4)} 2>/dev/null || true",
                          check=False, quiet=True) or "").strip()
        try:
            dur = round(float(dur.splitlines()[-1]), 2)
        except (ValueError, IndexError):
            dur = None
        self.status["outputs"].update({"mp4": os.path.relpath(mp4, ROOT), "sheet": f"out/{self.slug}/{self.slug}_sheet.jpg",
                                       "duration_s": dur, "mp4_sha256": sha256_file(mp4)})

    def step_package(self):
        self.sync()
        # out/ is not synced to the Spark: hand the pilot's titles/description to the prompt inline
        pilot = os.path.join(ROOT, "out", "pilots", PILOT[self.niche])
        ex = {k: (open(os.path.join(pilot, f"{k}.md")).read()[:6000] if os.path.exists(os.path.join(pilot, f"{k}.md"))
                  else "(missing)") for k in ("titles", "description")}
        cover = self.directives("package")
        cover = "" if cover == "- (none)" else "\n   Variant: " + cover.lstrip("- ")
        files = ["titles.md", "description.md", "thumbs.json"] + (["package.json"] if self.source() else [])
        self.claude(self.fill("package.md", example=EXAMPLE_THUMBS[self.niche], titles_example=ex["titles"],
                              description_example=ex["description"], cover_directive=cover), "package", timeout=1200,
                    outputs=[f"episodes/{self.slug}/{f}" for f in files])
        if "package.json" not in files:
            self.pull(f"episodes/{self.slug}/package.json", optional=True)
        pj = os.path.join(self.ep, "package.json")
        if os.path.exists(pj):
            try:
                pkg = json.load(open(pj, encoding="utf-8"))
            except ValueError as e:
                raise Fail(f"package: package.json is not valid JSON: {e}")
            bad = [k for k in ("titles", "yt_title", "yt_description", "short_caption", "hashtags") if not pkg.get(k)]
            if bad or len(pkg.get("yt_title", "")) > 100:
                raise Fail(f"package: package.json missing/invalid {bad or ['yt_title > 100 chars']}")
            self.log(f"package: {pkg['yt_title']!r}, {len(pkg['hashtags'])} hashtags")

    def step_thumbs(self):
        with self.code_lock():
            self.run(["scripts/thumbs_render.sh", f"episodes/{self.slug}/thumbs.json"], env={"OUT": f"{self.slug}/thumbs"},
                     timeout=1800, quiet=True)
        tdir = os.path.join(self.out, "thumbs")
        jpgs = sorted(f for f in os.listdir(tdir) if f.endswith(".jpg") and not f.startswith("sheet_"))
        self.log(f"thumbs: {len(jpgs)} images in out/{self.slug}/thumbs/")
        pj = os.path.join(self.ep, "package.json")
        if os.path.exists(pj):
            pkg = json.load(open(pj, encoding="utf-8"))
            if not pkg.get("thumb_pick"):
                prim = (json.load(open(os.path.join(self.ep, "thumbs.json"))) or {}).get("primary") or self.slug
                cand = [f for f in jpgs if f.startswith(f"{prim}_") and f.endswith("_9x16.jpg")] or \
                       [f for f in jpgs if f.endswith("_9x16.jpg")]
                if cand:
                    pkg["thumb_pick"] = f"out/{self.slug}/thumbs/{cand[0]}"
                    write_json_atomic(pj, pkg)
            self.status["outputs"]["thumbs_dir"] = f"out/{self.slug}/thumbs/"

    def step_collect(self):
        for f in ("titles.md", "description.md", "package.json", "source.json", "variant.json", "beatmap.json"):
            if os.path.exists(os.path.join(self.ep, f)):
                shutil.copyfile(os.path.join(self.ep, f), os.path.join(self.out, f))
        files = sorted(os.path.relpath(os.path.join(d, f), self.out) for d, _, fs in os.walk(self.out) for f in fs)
        meta = parse(open(os.path.join(self.ep, "script.md"), encoding="utf-8").read()).meta
        with open(os.path.join(self.out, "MANIFEST.md"), "w") as f:
            f.write(f"# {self.slug}\n\n{meta.get('title', '')}\n\nBuilt by `studio-make` "
                    f"({dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M} UTC). Sources in `episodes/{self.slug}/`.\n\n")
            f.write("\n".join(f"- `{x}`" for x in files) + "\n")
        src = self.source()
        # mark the source used whenever this episode was made from one (source.json), also on a --slug --from retry
        if src and src.get("source_id") and not getattr(self.a, "dry_run_claude", False):
            self.spark(f"python3 -m pipeline.sources mark {shlex.quote(src['source_id'])} used --slug {self.slug}",
                       check=False, quiet=True)
        self.log(f"collect: out/{self.slug}/ ({len(files)} files)")

    # ------------------------------------------------------------------ prompt pieces (source mode)
    def beat_plan(self) -> list[int]:
        meta = parse(open(os.path.join(self.ep, "script.md"), encoding="utf-8").read()).meta
        return [int(x) for x in re.findall(r"\d+", meta.get("beat_plan", ""))]

    @staticmethod
    def source_summary(src: dict) -> str:
        keep = {k: src.get(k) for k in ("source_id", "url", "format", "title", "channel", "views", "outlier_score",
                                         "duration_s", "angle", "hook", "pacing", "corpus_file", "annotation", "topic",
                                         "kit_component")}
        return json.dumps(keep, ensure_ascii=False, indent=1)

    @staticmethod
    def skeleton_table(src: dict) -> str:
        from pipeline.sources import skeleton_table
        return skeleton_table(src)

    def hook_directive(self, src: dict) -> str:
        v = self.variant()
        hook = [d for d in (v.get("directives_by_step") or {}).get("script", []) if d.startswith("Hook:")]
        h = src.get("hook") or {}
        base = (f"the source opens with hook shape {h.get('code') or '?'} ({h.get('shape') or 'see the annotation'}), "
                f"first speech at {h.get('first_speech_s')} s")
        return base + ("; " + " ".join(hook) if hook else "")

    @staticmethod
    def pacing_line(src: dict) -> str:
        p = src.get("pacing") or {}
        wpm = p.get("wpm")
        ours = max(180, min(205, wpm)) if wpm else 190
        return (f"source {wpm or '?'} wpm, re-hook every ~{p.get('rehook_s')} s; ours: about {ours} wpm (explainer "
                f"rubric 180-205), a re-hook every 8-12 s, {src['target']['words'][0]}-{src['target']['words'][1]} words")

    def learned_notes(self) -> str:
        n = self.variant().get("learned_notes") or []
        return "\n".join(f"- {x}" for x in n) or "- (none yet)"

    # ------------------------------------------------------------------ driver
    def go(self, steps: list[str]) -> int:
        self.log(f"=== studio-make {self.slug} ({self.niche}) steps={','.join(steps)}"
                 f"{' LOCAL' if LOCAL else ''}{' DRY-RUN-CLAUDE' if getattr(self.a, 'dry_run_claude', False) else ''}")
        t0 = time.time()
        self.save_status(status="running", started_at=now_iso(), finished_at=None, exit_code=None, error=None,
                         budget_tokens=getattr(self.a, "budget_tokens", None))
        i = 0
        try:
            while i < len(steps):
                st = steps[i]
                self.save_status(step=st)
                if st == "tts" and i + 1 < len(steps) and steps[i + 1] == "shots":
                    # independent: voice on the Spark CPU while claude storyboards (anchors are words, not seconds)
                    err = []
                    th = threading.Thread(target=lambda: self._safe(self.step_tts, err))
                    th.start()
                    self._safe(self.step_shots, err)
                    th.join()
                    if err:
                        raise err[0]
                    self._done("tts", "shots")
                    i += 2
                    continue
                getattr(self, f"step_{st}")()
                self._done(st)
                i += 1
        except Stop as e:
            self.log(f"=== stopped: {e}")
            self.save_status(status="dry_run", finished_at=now_iso(), exit_code=0, error=None)
            return 0
        except Fail as e:
            status = "budget_stop" if e.exit_code == EXIT_BUDGET else "failed"
            self.log(f"=== {status} at {self.status.get('step')}: {e}")
            self.save_status(status=status, finished_at=now_iso(), exit_code=e.exit_code, error=str(e)[:1000])
            raise
        self.log(f"=== done in {(time.time() - t0) / 60:.1f} min -> out/{self.slug}/ "
                 f"({self.status['usage_total']['weighted_tokens']:,} weighted tokens, ${self.status['usage_total']['cost_usd']:.2f})")
        self.save_status(status="done", step=None, finished_at=now_iso(), exit_code=0, error=None)
        return 0

    def _done(self, *names):
        for n in names:
            if n not in self.status["steps_done"]:
                self.status["steps_done"].append(n)
        self.save_status()

    @staticmethod
    def _safe(fn, err):
        try:
            fn()
        except BaseException as e:  # noqa: BLE001
            err.append(e)


def slugify(niche: str, text: str) -> str:
    words = re.findall(r"[a-z0-9]+", text.lower())
    stop = {"the", "a", "an", "of", "and", "to", "in", "on", "at", "is", "that", "my", "our", "your"}
    keep = [w for w in words if w not in stop and len(w) > 1][:5] or ["untitled"]
    return f"{niche}-{'-'.join(keep)}"


def pick_source(a) -> dict:
    """Run `pipeline.sources pick` where the data lives (here in local mode, else on the Spark) -> its JSON."""
    args = ["python3", "-m", "pipeline.sources", "pick", "--niche", a.niche, "--json"]
    if a.source != "auto":
        args += ["--id", a.source]
    if a.date:
        args += ["--date", a.date]
    if a.slot:
        args += ["--slot", a.slot]
    cmd = " ".join(shlex.quote(x) for x in args)
    r = subprocess.run(spark_argv(cmd), cwd=ROOT, capture_output=True, text=True, timeout=300)
    if r.returncode == 255 and not LOCAL:
        raise Fail(f"source pick: Spark unreachable: {r.stderr.strip()[-200:]}", EXIT_DEP)
    if r.returncode != 0:
        raise Fail(f"source pick failed: {(r.stderr or r.stdout).strip()[-300:]}", r.returncode if r.returncode in (2, 4) else 1)
    return json.loads(r.stdout.strip().splitlines()[-1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--niche", choices=["explainer", "horror"])
    ap.add_argument("--topic", help="explainer topic (or horror premise); with --source: overrides the derived topic")
    ap.add_argument("--premise", help="horror premise (alias of --topic)")
    ap.add_argument("--source", help="model the episode on this viral source: a video id, URL, or 'auto' (pick one)")
    ap.add_argument("--slot", choices=["a", "b"], help="--source: post slot (default: the next empty one)")
    ap.add_argument("--date", help="--source: local post date YYYY-MM-DD (default: the next empty slot)")
    ap.add_argument("--experiment", help="EXP-NNN:control|treatment (reads data/experiments.jsonl)")
    ap.add_argument("--variant", action="append", default=[], help="key=value, e.g. hook.max_words=9 (repeatable)")
    ap.add_argument("--review-notes", help="file with reviewer notes for the review step (fix round)")
    ap.add_argument("--budget-tokens", type=int, help="per-video cap on weighted claude tokens (exit 3 when reached); "
                                                      f"default {DEFAULT_BUDGET:,} for --source makes")
    ap.add_argument("--dry-run-claude", action="store_true", help="stop cleanly (exit 0) before the first claude call")
    ap.add_argument("--slug", help="episode folder name (default: from niche + topic, or op-<date>-<slot>-<topic>)")
    ap.add_argument("--script", help="use this script.md (repo-relative) instead of writing one")
    ap.add_argument("--steps", help=f"comma list from {','.join(STEPS)}")
    ap.add_argument("--from", dest="start", choices=STEPS, help="run this step and all after it")
    ap.add_argument("--review-rounds", type=int, default=1)
    ap.add_argument("--rewrite", action="store_true", help="rewrite script.md even if it exists (implies a shots replan)")
    ap.add_argument("--reshot", action="store_true", help="regenerate shots.json even if it exists")
    ap.add_argument("--force", action="store_true", help="allow a slug that has a hand-written builder")
    a = ap.parse_args()
    a.topic = a.topic or a.premise
    a.source_id = None
    try:
        if a.source:
            a.niche = a.niche or "explainer"
            if a.niche != "explainer":
                ap.error("--source is wired for --niche explainer only")
            if a.budget_tokens is None:
                a.budget_tokens = DEFAULT_BUDGET
            pk = pick_source(a)
            a.source_id = pk["pick"]["source_id"]
            if not a.slug:
                a.slug = pk["slug"] if not a.topic else (
                    f"op-{pk['slot']['ymd']}-{pk['slot']['slot']}-" + slugify("x", a.topic)[2:])
            print(f"[make] source {a.source_id} (score {pk['pick']['score']}, {', '.join(pk['pick']['reasons'])}) -> {a.slug}",
                  flush=True)
        elif a.slug and a.slug.startswith("op-") and os.path.exists(os.path.join(ROOT, "episodes", a.slug, "source.json")):
            a.niche = a.niche or "explainer"
            if a.budget_tokens is None:
                a.budget_tokens = DEFAULT_BUDGET
    except Fail as e:
        print(f"studio-make: {e}", file=sys.stderr)
        sys.exit(e.exit_code)
    if a.script and not a.slug:
        m = re.search(r"^id:\s*(\S+)", open(os.path.join(ROOT, a.script)).read(), re.M)
        a.slug = m.group(1) if m else os.path.basename(os.path.dirname(a.script))
    if not a.niche:
        a.niche = "horror" if (a.slug or "").startswith("horror") else "explainer"
    if not a.slug:
        if not a.topic:
            ap.error("give --topic/--premise, --source, --slug or --script")
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
    if not a.source and "source" in steps and not a.steps:
        steps = [s for s in steps if s != "source"] if not os.path.exists(os.path.join(ROOT, "episodes", a.slug, "source.json")) else steps
    try:
        sys.exit(Make(a).go(steps))
    except Fail as e:
        print(f"studio-make: {e}", file=sys.stderr)
        sys.exit(e.exit_code)


if __name__ == "__main__":
    main()
