"""scripts/spark_sync.sh, scripts/spark_render.sh (findings F07, F08/F27, F25, F26, F28, F29) and the slot choice
of scripts/render.sh (Spark first, the Mac when the Spark render lock is held and the Mac has room).

ssh and rsync are replaced by stubs on PATH that only record their argv/stdin, so nothing
touches the network or the Spark. Safe to run anywhere bash exists.
"""
import fcntl
import glob
import os
import platform
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


LOCK_STUB = """#!/usr/bin/env bash
# ssh stub for render.sh: answers the lock probe with $STUB_LOCK_STATE (free | held | empty = unreachable)
cat >/dev/null
[ -n "$STUB_LOCK_STATE" ] && echo "$STUB_LOCK_STATE"
exit 0
"""


class RenderDispatch(unittest.TestCase):
    """RENDER_DRY_RUN=1: only the slot decision, nothing is synced or rendered."""

    def decide(self, lock_state, **env_extra):
        tmp = tempfile.mkdtemp()
        bindir = os.path.join(tmp, "bin")
        os.makedirs(bindir)
        p = os.path.join(bindir, "ssh")
        with open(p, "w") as f:
            f.write(LOCK_STUB)
        os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
        env = {k: v for k, v in os.environ.items() if k not in ("STUDIO_LOCAL", "RENDER_SLOT", "SPARK_LOCK")}
        env.update(PATH=bindir + os.pathsep + env["PATH"], SPARK_HOST="stub-host", RENDER_DRY_RUN="1",
                   STUB_LOCK_STATE=lock_state, MAC_LOCK=os.path.join(tmp, "mac.lock"))
        env.update(env_extra)
        r = subprocess.run(["bash", os.path.join(_util.ROOT, "scripts", "render.sh"), "Storyboard", "x.mp4"], env=env,
                           capture_output=True, text=True, timeout=60)
        return r, r.stdout + r.stderr, env["MAC_LOCK"]

    def test_spark_first_when_its_lock_is_free(self):
        r, out, _ = self.decide("free", MAC_MIN_FREE_GB="0", MAC_MIN_DISK_GB="0")
        self.assertEqual(r.returncode, 0, out)
        self.assertIn("[render] slot: spark", out)

    @unittest.skipUnless(platform.system() == "Darwin", "Mac slot needs macOS")
    def test_mac_when_spark_lock_held_and_mac_has_room(self):
        r, out, _ = self.decide("held", MAC_MIN_FREE_GB="0", MAC_MIN_DISK_GB="0")
        self.assertEqual(r.returncode, 0, out)
        self.assertIn("[render] slot: mac", out)

    @unittest.skipUnless(platform.system() == "Darwin", "Mac slot needs macOS")
    def test_waits_for_spark_when_mac_short_on_ram_or_disk(self):
        for env in ({"MAC_MIN_FREE_GB": "100000", "MAC_MIN_DISK_GB": "0"},
                    {"MAC_MIN_FREE_GB": "0", "MAC_MIN_DISK_GB": "100000000"}):
            r, out, _ = self.decide("held", **env)
            self.assertIn("[render] slot: spark", out)
            self.assertIn("mac not eligible", out)

    @unittest.skipUnless(platform.system() == "Darwin", "Mac slot needs macOS")
    def test_one_mac_render_at_a_time(self):
        tmp = tempfile.mkdtemp()
        lock = os.path.join(tmp, "mac.lock")
        with open(lock, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)  # lockf(1) uses flock(2): same lock
            r, out, _ = self.decide("held", MAC_MIN_FREE_GB="0", MAC_MIN_DISK_GB="0", MAC_LOCK=lock)
        self.assertIn("[render] slot: spark", out)
        self.assertIn("mac render lock held", out)

    def test_operator_on_the_spark_never_uses_the_mac(self):
        r, out, _ = self.decide("held", STUDIO_LOCAL="1", MAC_MIN_FREE_GB="0", MAC_MIN_DISK_GB="0")
        self.assertIn("[render] slot: spark", out)

    def test_forced_mac_refused_when_rules_fail(self):
        r, out, _ = self.decide("free", RENDER_SLOT="mac", MAC_MIN_FREE_GB="100000")
        self.assertEqual(r.returncode, 3, out)
        self.assertNotIn("slot: mac (", out)


if __name__ == "__main__":
    unittest.main()
