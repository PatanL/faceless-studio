"""Lane L1: make.py claude accounting, budget cap, F01 output checks, and the local mode of the Spark scripts.
Everything is stubbed: no ssh, no claude, no render."""
import argparse
import json
import os
import stat
import subprocess
import tempfile
import unittest

import _util
from pipeline import make as mk

RESULT = json.dumps({"type": "result", "is_error": False, "result": "done: 12 scenes", "total_cost_usd": 0.5,
                     "usage": {"input_tokens": 1000, "output_tokens": 2000, "cache_read_input_tokens": 100000,
                               "cache_creation_input_tokens": 5000}})


def fake(tmp, **args):
    m = mk.Make.__new__(mk.Make)
    m.slug, m.niche = "t-ep", "explainer"
    m.ep, m.out = os.path.join(tmp, "ep"), os.path.join(tmp, "out")
    os.makedirs(m.ep), os.makedirs(m.out)
    a = dict(script=None, rewrite=False, reshot=False, topic="x", review_rounds=1, budget_tokens=None, dry_run_claude=False)
    a.update(args)
    m.a = argparse.Namespace(**a)
    m.logs = []
    m.log = m.logs.append
    m.lock = __import__("threading").Lock()
    m.status = {"v": 1, "slug": m.slug, "steps_done": [], "usage": {}, "usage_total": {"weighted_tokens": 0, "cost_usd": 0.0},
                "outputs": {}}
    m.run = lambda *x, **k: ""
    m.pull = lambda *x, **k: None
    m.has_claude = lambda: True
    return m


class Claude(unittest.TestCase):
    def test_usage_is_recorded_and_weighted(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp)

            def spark(cmd, **k):
                if "claude -p" in cmd:
                    open(os.path.join(m.ep, "shots.json"), "w").write("{}")
                    return RESULT + "\n"
                return ""
            m.spark = spark
            m.claude("p", "shots", outputs=["episodes/t-ep/shots.json"])
            u = m.status["usage"]["shots"]
            self.assertEqual(u["weighted_tokens"], 1000 + 2000 + 5000 + 10000)
            self.assertEqual(m.status["usage_total"]["weighted_tokens"], 18000)
            self.assertTrue(os.path.exists(os.path.join(m.ep, "make_status.json")))

    def test_exit_zero_without_output_is_a_failure_and_restores(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp)
            p = os.path.join(m.ep, "titles.md")
            open(p, "w").write("OLD")
            m.spark = lambda cmd, **k: (RESULT + "\n") if "claude -p" in cmd else ""
            with self.assertRaises(mk.Fail):
                m.claude("p", "package", outputs=["episodes/t-ep/titles.md"])
            self.assertEqual(open(p).read(), "OLD")

    def test_auth_failure_is_exit_5(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp)

            def spark(cmd, check=True, **k):
                if "claude -p" in cmd:
                    raise mk.Fail("x", out='{"type":"result","is_error":true,"result":"Invalid API key · Please run /login"}', rc=1)
                return ""
            m.spark = spark
            with self.assertRaises(mk.Fail) as cm:
                m.claude("p", "script")
            self.assertEqual(cm.exception.exit_code, 5)

    def test_budget_cap_is_exit_3_before_the_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp, budget_tokens=1_000_000)
            m.status["usage_total"]["weighted_tokens"] = 900_000
            m.spark = lambda *x, **k: self.fail("claude must not run over budget")
            with self.assertRaises(mk.Fail) as cm:
                m.claude("p", "shots")
            self.assertEqual(cm.exception.exit_code, 3)

    def test_dry_run_claude_stops_cleanly(self):
        with tempfile.TemporaryDirectory() as tmp:
            m = fake(tmp, dry_run_claude=True)
            with self.assertRaises(mk.Stop):
                m.claude("p", "script")


class LocalScripts(unittest.TestCase):
    """STUDIO_LOCAL=1: the Spark scripts never call ssh or rsync."""

    def run_script(self, script, env, *args):
        tmp = tempfile.mkdtemp()
        bindir, log = os.path.join(tmp, "bin"), os.path.join(tmp, "calls")
        os.makedirs(bindir)
        for name in ("ssh", "rsync"):
            p = os.path.join(bindir, name)
            open(p, "w").write(f"#!/usr/bin/env bash\necho {name} >> {log}\nexit 0\n")
            os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)
        e = {**os.environ, "PATH": bindir + os.pathsep + os.environ["PATH"], "STUDIO_LOCAL": "1", **env}
        r = subprocess.run(["bash", os.path.join(_util.ROOT, "scripts", script), *args], env=e, capture_output=True,
                           text=True, timeout=60)
        return r, (open(log).read().split() if os.path.exists(log) else [])

    def test_sync_is_a_noop_locally(self):
        r, calls = self.run_script("spark_sync.sh", {"SKIP_NPM": "1"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(calls, [])
        self.assertIn("local mode", r.stdout)

    def test_owned_paths_are_protected_in_the_push(self):
        owned = [l.strip() for l in open(os.path.join(_util.ROOT, "scripts", "spark_owned.txt"))
                 if l.strip() and not l.startswith("#")]
        for p in ("/data/", "/episodes/op-*/", "/research/corpus/*/auto/", "/out/"):
            self.assertIn(p, owned)


if __name__ == "__main__":
    unittest.main()
