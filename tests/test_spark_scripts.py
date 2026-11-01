"""scripts/spark_sync.sh and scripts/spark_render.sh (findings F07, F08/F27, F25, F26, F28, F29).

ssh and rsync are replaced by stubs on PATH that only record their argv/stdin, so nothing
touches the network or the Spark. Safe to run anywhere bash exists.
"""
import glob
import os
import shlex
import stat
import subprocess
import tempfile
import unittest

import _util

STUB = """#!/usr/bin/env bash
n=$(ls "$LOGDIR" | wc -l | tr -d ' ')
printf '%s\\n' "$@" > "$LOGDIR/$n.$(basename "$0").args"
if [ "$(basename "$0")" = ssh ]; then cat > "$LOGDIR/$n.ssh.stdin"; fi
exit 0
"""


def run(script, env_extra, *args):
    tmp = tempfile.mkdtemp()
    bindir, logdir = os.path.join(tmp, "bin"), os.path.join(tmp, "log")
    os.makedirs(bindir), os.makedirs(logdir)
    for name in ("ssh", "rsync"):
        p = os.path.join(bindir, name)
        with open(p, "w") as f:
            f.write(STUB)
        os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
    env = {k: v for k, v in os.environ.items() if k not in ("CONC", "PROPS", "SYNC_DELETE", "SKIP_NPM", "NO_SYNC")}
    env.update(PATH=bindir + os.pathsep + env["PATH"], LOGDIR=logdir, SPARK_HOST="stub-host", NO_PULL="1")
    env.update(env_extra)
    r = subprocess.run(["bash", os.path.join(_util.ROOT, "scripts", script), *args], env=env,
                       capture_output=True, text=True, timeout=60)
    calls = []
    for p in sorted(glob.glob(os.path.join(logdir, "*.args")), key=lambda x: int(os.path.basename(x).split(".")[0])):
        n, tool = os.path.basename(p).split(".")[:2]
        stdin_p = os.path.join(logdir, f"{n}.ssh.stdin")
        calls.append((tool, open(p).read().split("\n"), open(stdin_p).read() if os.path.exists(stdin_p) else ""))
    return r, calls


def rsync_push(calls):
    return next(a for t, a, _ in calls if t == "rsync")


class SparkSync(unittest.TestCase):
    def test_plain_sync_excludes_node_modules(self):
        """Regression guard (passes today)."""
        r, calls = run("spark_sync.sh", {"SKIP_NPM": "1"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("node_modules", rsync_push(calls))

    def test_F25_sync_delete_protects_spark_only_outputs(self):
        """F25: with SYNC_DELETE=1 the Spark-only mix.wav / music / episodes/*/audio must be protected."""
        r, calls = run("spark_sync.sh", {"SKIP_NPM": "1", "SYNC_DELETE": "1"})
        a = " ".join(rsync_push(calls))
        self.assertIn("--delete", a)
        for p in ("studio/public/episodes", "studio/public/music", "audio"):
            self.assertIn(p, a, f"--delete without protecting {p}")

    def test_F26_push_does_not_overwrite_newer_spark_files(self):
        """F26: the push needs --update (or must exclude episodes/*/audio/) so stale Mac copies don't win."""
        r, calls = run("spark_sync.sh", {"SKIP_NPM": "1"})
        a = rsync_push(calls)
        self.assertTrue("--update" in a or "-u" in a or any("audio" in x for x in a), a)

    def test_F07_push_does_not_clobber_files_claude_is_editing(self):
        """F07: files make.py's claude steps edit on the Spark (shots.json, script.md, titles.md) must not be
        overwritten by another lane's sync mid-edit (--update, per-lane workspace, or excluded from the push)."""
        r, calls = run("spark_sync.sh", {"SKIP_NPM": "1"})
        a = rsync_push(calls)
        self.assertTrue("--update" in a or any("shots.json" in x for x in a), a)


class SparkRender(unittest.TestCase):
    def remote(self, env):
        r, calls = run("spark_render.sh", dict(NO_SYNC="1", **env), "Storyboard", "x.mp4")
        self.assertEqual(r.returncode, 0, r.stderr)
        ssh = [c for c in calls if c[0] == "ssh"]
        self.assertTrue(ssh)
        return ssh[-1]

    def conc(self, env):
        _, args, _ = self.remote(env)
        cmd = shlex.split(next(a for a in args if a.startswith("bash -s")))
        return int(cmd[7])  # bash -s -- PROJ ENTRY COMP NAME CONC PROPS

    def test_render_is_locked(self):
        """Regression guard (passes today): the render itself runs under flock."""
        _, _, stdin = self.remote({})
        self.assertLess(stdin.index("flock"), stdin.index("remotion render"))

    def test_F28_default_concurrency_within_budget(self):
        """F28: BRIEF says Remotion --concurrency=4 (~10 cores). Default and cap must be <= 4."""
        self.assertLessEqual(self.conc({}), 4)

    def test_F28_concurrency_cap(self):
        self.assertLessEqual(self.conc({"CONC": "12"}), 4)

    def test_F29_remote_render_dies_with_the_ssh_session(self):
        """F29: ssh -tt (SIGHUP on disconnect) or a trap that kills the process group."""
        _, args, stdin = self.remote({})
        self.assertTrue("-tt" in args or "trap " in stdin, args)

    def test_F08_F27_npm_ci_runs_under_the_render_lock(self):
        """F08/F27: spark_render's sync must not run npm ci outside render.lock
        (either SKIP_NPM=1 for the sync, or flock around npm ci)."""
        r, calls = run("spark_render.sh", {}, "Storyboard", "x.mp4")
        npm = [s for t, _, s in calls if t == "ssh" and "npm ci" in s]
        for s in npm:
            self.assertTrue("flock" in s and s.index("flock") < s.index("npm ci"), "npm ci outside the lock")


if __name__ == "__main__":
    unittest.main()
