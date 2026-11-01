"""Lane L3 (pipeline/publish): captions limits, preconditions, idempotency, dry-run payloads, status mapping,
GraphQL client error handling and the one-file media server. No network beyond 127.0.0.1, no credentials."""
import contextlib
import hashlib
import io
import json
import os
import shutil
import tempfile
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock

import _util  # noqa: F401  (puts the repo on sys.path)

from pipeline.common import jsonl, timeutil
from pipeline.publish import buffer as B
from pipeline.publish import captions as C
from pipeline.publish import host as H
from pipeline.publish import paths, post, schedule, status

REPO = Path(_util.ROOT)
SLUG = "op-20261102-a-orca"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class Fixture(unittest.TestCase):
    """A throwaway studio root with one gated episode; env file absent, so everything is dry-run."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="l3-"))
        (self.tmp / "pipeline" / "ops").mkdir(parents=True)
        shutil.copy(REPO / "pipeline" / "ops" / "config.default.json", self.tmp / "pipeline" / "ops")
        ep = self.tmp / "episodes" / SLUG
        ep.mkdir(parents=True)
        (ep / "package.json").write_text(json.dumps({
            "v": 1, "title_pick": 1, "titles": ["A", "Orcas Could Hunt You. They Choose Not To.", "C"],
            "short_caption": "Wild orcas could kill you easily.\nThey never have.",
            "hashtags": ["#orca", "ocean", "#shorts"], "yt_description": None}))
        (ep / "variant.json").write_text(json.dumps({"v": 1, "experiment_id": "EXP-001", "arm": "control"}))
        (ep / "source.json").write_text(json.dumps({"v": 1, "source_id": "VtrcKTkhDHU"}))
        out = self.tmp / "out" / SLUG
        (out / "qa").mkdir(parents=True)
        self.mp4 = out / f"{SLUG}_9x16.mp4"
        self.mp4.write_bytes(b"\x00\x00\x00\x18ftypmp42" + b"x" * 1000)
        self.write_gate("PASS")
        self.env = mock.patch.dict(os.environ, {"STUDIO_ENV_FILE": str(self.tmp / "absent.env"),
                                                "STUDIO_DATA_DIR": str(self.tmp / "data")})
        self.env.start()
        self.root = mock.patch.object(paths, "ROOT", self.tmp)
        self.root.start()

    def tearDown(self):
        self.root.stop()
        self.env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_gate(self, verdict, review="PASS", mp4_sha=None, history_mode="default", title="Orcas Could Hunt You"):
        qa = self.tmp / "out" / SLUG / "qa"
        (qa / "fingerprint.json").write_text(json.dumps({"v": 1, "slug": SLUG, "title": title, "hook": "x",
                                                         "topic": "orca"}))
        (qa / "gate.json").write_text(json.dumps({"v": 1, "verdict": verdict,
                                                  "mp4_sha256": mp4_sha or sha(self.mp4),
                                                  "checks": {"sameness": {"status": "PASS",
                                                                          "history_mode": history_mode}}}))
        (qa / "review.json").write_text(json.dumps({"v": 1, "verdict": review, "gate_sha": sha(qa / "gate.json")}))

    def run_post(self, *extra):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = post.main([SLUG, "--slot-at", "2026-11-02T17:30:00Z", *extra])
        return code, buf.getvalue()

    def rows(self):
        return jsonl.read(str(self.tmp / "data" / "posts.jsonl"))


class TestPostDryRun(Fixture):
    def test_dry_run_writes_three_rows_with_payloads(self):
        code, out = self.run_post()
        self.assertEqual(code, 0, out)
        self.assertIn("DRY-RUN: missing BUFFER_API_KEY", out)
        rows = self.rows()
        self.assertEqual([r["platform"] for r in rows], ["youtube", "tiktok", "instagram"])
        for r in rows:
            self.assertEqual((r["status"], r["dry_run"], r["mode"]), ("dry_run", True, "draft"))
            self.assertEqual((r["experiment_id"], r["arm"], r["source_id"]), ("EXP-001", "control", "VtrcKTkhDHU"))
            inp = r["payload"]["variables"]["input"]
            self.assertEqual((inp["mode"], inp["dueAt"], inp["saveToDraft"]),
                             ("customScheduled", "2026-11-02T17:30:00.000Z", True))
            self.assertIn(C.DISCLOSURE, inp["text"])
            self.assertIn("mutation CreatePost", r["payload"]["query"])
            self.assertIn("fragment PostFields on Post", r["payload"]["query"])
            self.assertNotIn("Bearer ", json.dumps(r))
        yt, tt, ig = (r["payload"]["variables"]["input"] for r in rows)
        self.assertEqual(yt["metadata"]["youtube"]["title"], "Orcas Could Hunt You. They Choose Not To.")
        self.assertFalse(yt["metadata"]["youtube"]["madeForKids"])
        self.assertNotIn("metadata", yt["assets"][0]["video"])
        self.assertEqual(ig["metadata"]["instagram"]["type"], "reel")
        self.assertTrue(tt["metadata"]["tiktok"]["isAiGenerated"])
        self.assertIn("#shorts", yt["text"])
        self.assertNotIn("#shorts", tt["text"])
        cap = json.loads((self.tmp / "out" / SLUG / "publish" / "captions.json").read_text())
        self.assertEqual(cap["slug"], SLUG)

    def test_gate_fail_blocks(self):
        self.write_gate("FAIL")
        code, out = self.run_post()
        self.assertEqual(code, 6, out)
        self.assertEqual(self.rows(), [])

    def test_mp4_changed_after_gate_blocks(self):
        self.write_gate("PASS", mp4_sha="0" * 64)
        code, _ = self.run_post()
        self.assertEqual(code, 6)

    def test_review_of_older_gate_blocks(self):
        qa = self.tmp / "out" / SLUG / "qa"
        (qa / "review.json").write_text(json.dumps({"verdict": "PASS", "gate_sha": "f" * 64}))
        self.assertEqual(self.run_post()[0], 6)

    def test_ignore_gates_only_with_dry_run(self):
        self.assertEqual(self.run_post("--ignore-gates")[0], 2)  # needs an explicit --dry-run, even without a key
        self.write_gate("FAIL")
        self.assertEqual(self.run_post("--ignore-gates", "--dry-run")[0], 0)
        self.assertTrue(all(r["gates_ignored"] for r in self.rows()))
        with mock.patch.object(post.cenv, "load_env", return_value={
                "BUFFER_API_KEY": "k" * 20, "BUFFER_CHANNEL_YOUTUBE": "a", "BUFFER_CHANNEL_TIKTOK": "b",
                "BUFFER_CHANNEL_INSTAGRAM": "c"}):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                code = post.main([SLUG, "--slot-at", "2030-01-01T00:00:00Z", "--ignore-gates"])
        self.assertEqual(code, 2)

    def test_idempotent_live_row_blocks_but_dry_run_rows_do_not(self):
        self.assertEqual(self.run_post()[0], 0)
        self.assertEqual(self.run_post()[0], 0)  # dry_run rows never block
        jsonl.append(str(self.tmp / "data" / "posts.jsonl"),
                     {"post_key": f"{SLUG}:tiktok", "slug": SLUG, "platform": "tiktok", "status": "draft",
                      "dry_run": False, "buffer_post_id": "p1"})
        code, out = self.run_post()
        self.assertEqual(code, 6, out)
        self.assertIn("idempotent", out)
        self.assertEqual(self.run_post("--platforms", "youtube")[0], 0)

    def test_non_default_sameness_history_blocks(self):
        self.write_gate("PASS", history_mode="against")  # e.g. `pipeline.qa.gate <slug> --against ""`
        code, out = self.run_post()
        self.assertEqual(code, 6, out)
        self.assertIn("history_mode=against", out)

    def test_sameness_is_rechecked_at_post_time(self):
        other = "op-20261102-b-killer-whale"
        q = self.tmp / "out" / other / "qa"
        q.mkdir(parents=True)
        (q / "fingerprint.json").write_text(json.dumps({"v": 1, "slug": other, "title": "Killer whales", "hook": "y",
                                                        "topic": "killer whale"}))
        jsonl.append(str(self.tmp / "data" / "posts.jsonl"),
                     {"post_key": f"{other}:youtube", "slug": other, "platform": "youtube", "status": "scheduled",
                      "dry_run": False, "buffer_post_id": "p9", "scheduled_at": "2026-11-02T12:00:00Z"})
        code, out = self.run_post()
        self.assertEqual(code, 6, out)  # orca == killer whale: posted since the gate ran
        self.assertIn("sameness_now", out)

    def test_modes_per_platform_in_one_call(self):
        cfg_dir = self.tmp / "data" / "operator"
        cfg_dir.mkdir(parents=True)
        (cfg_dir / "config.json").write_text(json.dumps({"disclosure_ok_auto": {"youtube": True}}))
        code, out = self.run_post("--modes", "youtube=auto,tiktok=draft,instagram=draft")
        self.assertEqual(code, 0, out)
        rows = {r["platform"]: r for r in self.rows()}
        self.assertEqual({p: r["mode"] for p, r in rows.items()},
                         {"youtube": "auto", "tiktok": "draft", "instagram": "draft"})
        self.assertNotIn("saveToDraft", rows["youtube"]["payload"]["variables"]["input"])
        self.assertTrue(rows["tiktok"]["payload"]["variables"]["input"]["saveToDraft"])
        self.assertEqual(self.run_post("--modes", "youtube=sometimes")[0], 2)

    def test_missing_channel_drops_only_that_platform_and_writes_result(self):
        made = []

        class FakeClient:
            dry_run = False

            def __init__(self, *a, **k):
                pass

            def resolve_org(self, org):
                return "org1"

            def channels(self, org):
                return [{"id": "chY", "service": B.PLATFORM_SERVICE["youtube"]},
                        {"id": "chT", "service": B.PLATFORM_SERVICE["tiktok"]}]

            def create_post(self, inp, label=""):
                made.append(inp["channelId"])
                return {"id": f"post-{inp['channelId']}", "status": "draft", "dueAt": inp["dueAt"],
                        "assets": [{"source": "https://cdn.buffer.example/x.mp4"}]}

        @contextlib.contextmanager
        def fake_hosted(path, **k):
            yield H.Hosted("static", "https://media.example/tok/x.mp4", "t" * 32, "x.mp4", "now")

        env = {"BUFFER_API_KEY": "k" * 20, "BUFFER_CHANNEL_YOUTUBE": "chY", "BUFFER_CHANNEL_TIKTOK": "chT"}
        res = self.tmp / "res.json"
        with mock.patch.object(post.cenv, "load_env", return_value=env), \
                mock.patch.object(post.B, "BufferClient", FakeClient), mock.patch.object(post.H, "hosted", fake_hosted):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                code = post.main([SLUG, "--slot-at", "2030-01-01T00:00:00Z", "--result-file", str(res)])
        out = buf.getvalue()
        self.assertEqual(code, 0, out)
        self.assertIn("SKIP: BUFFER_CHANNEL_INSTAGRAM", out)
        self.assertEqual(made, ["chY", "chT"])
        rows = self.rows()
        self.assertEqual([(r["platform"], r["dry_run"], r["status"]) for r in rows],
                         [("youtube", False, "draft"), ("tiktok", False, "draft")])
        r = json.loads(res.read_text())
        self.assertEqual((r["phase"], r["created"], r["skipped_platforms"], r["dry_run"], r["holding"]),
                         ("done", ["youtube", "tiktok"], ["instagram"], False, False))

    def test_sigterm_handler_raises_system_exit(self):
        with self.assertRaises(SystemExit) as cm:
            post._on_signal(15, None)
        self.assertEqual(cm.exception.code, 143)

    def test_failed_ambiguous_row_blocks(self):
        jsonl.append(str(self.tmp / "data" / "posts.jsonl"),
                     {"post_key": f"{SLUG}:youtube", "status": "failed", "ambiguous": True, "dry_run": False})
        self.assertEqual(self.run_post("--platforms", "youtube")[0], 6)

    def test_paused_blocks(self):
        (self.tmp / "data" / "operator").mkdir(parents=True)
        (self.tmp / "data" / "operator" / "config.json").write_text(json.dumps({"paused": True}))
        self.assertEqual(self.run_post()[0], 6)

    def test_auto_needs_disclosure_ok(self):
        cfg = {"mode": {"youtube": "auto", "tiktok": "auto", "instagram": "auto"},
               "disclosure_ok_auto": {"youtube": True, "tiktok": False, "instagram": False}}
        self.assertEqual(post.effective_mode("youtube", cfg, None), ("auto", None))
        self.assertEqual(post.effective_mode("tiktok", cfg, None)[0], "draft")
        self.assertEqual(post.effective_mode("instagram", cfg, "auto")[0], "draft")
        inp = post.build_input("youtube", "c", C.build(SLUG), "https://x/y.mp4", "2026-11-02T17:30:00.000Z",
                               "auto", 1500, "28")
        self.assertNotIn("saveToDraft", inp)

    def test_record_manual(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = post.main(["--record-manual", SLUG, "youtube", "https://youtube.com/shorts/abcdefghijk"])
        self.assertEqual(code, 0)
        r = self.rows()[-1]
        self.assertEqual((r["mode"], r["status"], r["external_id"]), ("manual", "published", "abcdefghijk"))
        self.assertEqual(self.run_post("--platforms", "youtube")[0], 6)  # a manual post blocks a repost


class TestCaptions(unittest.TestCase):
    def pkg(self, **kw):
        base = {"titles": ["T"], "title_pick": 0, "yt_title": "T", "short_caption": "Line one.\nLine two.",
                "hashtags": ["#a", "#b"]}
        base.update(kw)
        return base

    def test_limits_and_disclosure_survive_trimming(self):
        long = " ".join(["word"] * 2000)
        c = C.build("s", self.pkg(short_caption=long, yt_title="<b>" + "x" * 150))
        self.assertLessEqual(C.utf16_len(c["tiktok"]["text"]), 2200)
        self.assertLessEqual(C.ig_len(c["instagram"]["text"]), 2196)
        self.assertLessEqual(C.utf16_len(c["youtube"]["title"]), 100)
        self.assertNotIn("<", c["youtube"]["title"])
        for t in (c["tiktok"]["text"], c["instagram"]["text"], c["youtube"]["description"]):
            self.assertTrue(t.endswith(C.DISCLOSURE))
        self.assertEqual(C.validate(c), [])

    def test_instagram_counts_line_breaks_twice_and_caps_hashtags(self):
        self.assertEqual(C.ig_len("a\nb"), 4)
        self.assertEqual(C.utf16_len("\U0001F40B"), 2)  # emoji = surrogate pair
        c = C.build("s", self.pkg(hashtags=[f"#t{i}" for i in range(40)]))
        self.assertLessEqual(len(C.HASHTAG_RE.findall(c["instagram"]["text"])), 30)

    def test_pilot_titles_and_description_parse(self):
        titles, pick = C.parse_titles_md(_util.read("out/pilots/explainer-orca/titles.md"))
        self.assertEqual(len(titles), 5)
        self.assertEqual(titles[pick], "The Killer Whale Has Never Killed You. Here's Why.")
        d = C.parse_description_md(_util.read("out/pilots/explainer-orca/description.md"))
        self.assertTrue(d["caption"].startswith("Wild killer whales"))
        self.assertIn("#shorts", d["hashtags"])
        self.assertEqual(d["disclosure"], C.DISCLOSURE)


class TestStatus(unittest.TestCase):
    prev = {"post_key": "s:youtube", "slug": "s", "platform": "youtube", "status": "draft", "dry_run": False,
            "buffer_post_id": "p1", "buffer_status": "draft", "scheduled_at": "2026-11-02T17:30:00Z", "at": "x",
            "payload": {"q": 1}}

    def test_sent_maps_to_published_with_external_id(self):
        new = status.updated_row(self.prev, {"status": "sent", "sentAt": "2026-11-02T17:30:05.000Z",
                                             "externalLink": "https://www.youtube.com/shorts/abcdefghijk",
                                             "dueAt": "2026-11-02T17:30:00.000Z"},
                                 timeutil.parse("2026-11-02T18:00:00Z"), 6)
        self.assertEqual((new["status"], new["external_id"]), ("published", "abcdefghijk"))
        self.assertNotIn("at", new)
        self.assertNotIn("payload", new)

    def test_unapproved_draft_becomes_missed_and_unchanged_is_none(self):
        p = {"status": "draft", "dueAt": "2026-11-02T17:30:00.000Z"}
        self.assertIsNone(status.updated_row(self.prev, p, timeutil.parse("2026-11-02T18:00:00Z"), 6))
        self.assertEqual(status.updated_row(self.prev, p, timeutil.parse("2026-11-03T00:00:00Z"), 6)["status"],
                         "missed")
        self.assertEqual(status.updated_row(self.prev, None, timeutil.now_utc(), 6)["status"], "deleted")

    def test_external_ids(self):
        self.assertEqual(post.external_id("tiktok", "https://www.tiktok.com/@x/video/7312345678901234567"),
                         "7312345678901234567")
        self.assertEqual(post.external_id("instagram", "https://www.instagram.com/reel/C1a2B3c4D5e/"), "C1a2B3c4D5e")


class FakeResp:
    def __init__(self, body, headers=None):
        self.body, self.status = json.dumps(body).encode(), 200
        self.headers = mock.Mock(get_all=lambda k: (headers or {}).get(k, []))

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def http_error(code, headers=None):
    return urllib.error.HTTPError("https://api.buffer.com", code, "x", headers or {}, io.BytesIO(b"{}"))


class TestClient(unittest.TestCase):
    def client(self):
        return B.BufferClient("secret-key-123", sleep=lambda s: None, out=io.StringIO())

    def test_load_op_pulls_fragment(self):
        q = B.load_op("CreatePost")
        self.assertIn("fragment PostFields", q)
        self.assertNotIn("query Organizations", q)

    def test_429_retries_then_succeeds(self):
        seq = [http_error(429, {"Retry-After": "1"}),
               FakeResp({"data": {"account": {"organizations": [{"id": "o1", "name": "n"}]}}})]
        with mock.patch.object(urllib.request, "urlopen", side_effect=seq):
            self.assertEqual(self.client().organizations()[0]["id"], "o1")

    def test_mutation_5xx_is_ambiguous_not_retried(self):
        calls = []

        def boom(*a, **k):
            calls.append(1)
            raise http_error(502)
        with mock.patch.object(urllib.request, "urlopen", side_effect=boom):
            with self.assertRaises(B.Ambiguous):
                self.client().create_post({"channelId": "c"})
        self.assertEqual(len(calls), 1)

    def test_unauthorized_is_dependency_down(self):
        with mock.patch.object(urllib.request, "urlopen", return_value=FakeResp(
                {"data": None, "errors": [{"message": "Not authorized", "extensions": {"code": "UNAUTHORIZED"}}]})):
            with self.assertRaises(B.DependencyDown) as cm:
                self.client().organizations()
        self.assertEqual(cm.exception.exit_code, 5)

    def test_typed_mutation_error(self):
        with mock.patch.object(urllib.request, "urlopen", return_value=FakeResp(
                {"data": {"createPost": {"__typename": "InvalidInputError", "message": "Text is required"}}})):
            with self.assertRaises(B.MutationFailed):
                self.client().create_post({"channelId": "c"})

    def test_dry_run_masks_key(self):
        out = io.StringIO()
        c = B.BufferClient("secret-key-123", dry_run=True, out=out)
        self.assertIsNone(c.organizations())
        self.assertIn("Authorization: Bearer ***", out.getvalue())
        self.assertNotIn("secret-key-123", out.getvalue())


class TestHostServer(unittest.TestCase):
    def test_serves_only_the_token_path_with_ranges(self):
        d = Path(tempfile.mkdtemp())
        f = d / "v.mp4"
        f.write_bytes(bytes(range(256)) * 10)
        tok = "a" * 32
        try:
            with H.LocalServer(H.one_file_resolver(tok, "v.mp4", f)) as srv:
                base = f"http://127.0.0.1:{srv.port}"
                self.assertEqual(H.head(f"{base}/{tok}/v.mp4")[0], 200)
                self.assertEqual(H.head(f"{base}/{tok}/v.mp4")[1]["Content-Length"], "2560")
                self.assertEqual(H.head(f"{base}/{'b' * 32}/v.mp4")[0], 404)
                self.assertEqual(H.head(f"{base}/")[0], 404)
                r = urllib.request.urlopen(urllib.request.Request(f"{base}/{tok}/v.mp4",
                                                                  headers={"Range": "bytes=10-19"}))
                self.assertEqual((r.status, r.read()), (206, bytes(range(10, 20))))
                with self.assertRaises(urllib.error.HTTPError) as cm:
                    urllib.request.urlopen(urllib.request.Request(f"{base}/{tok}/v.mp4", data=b"x"))
                self.assertEqual(cm.exception.code, 405)
        finally:
            shutil.rmtree(d)

    def test_dry_run_hosted_opens_nothing(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as t:
            with H.hosted(t.name, dry_run=True, mode="cloudflared") as h:
                self.assertTrue(h.url.startswith("https://DRY-RUN.trycloudflare.com/"))
            self.assertEqual(set(h.record()), {"mode", "opened_at", "closed_at"})


class TestSchedule(unittest.TestCase):
    def test_slots_are_chicago_local(self):
        s = schedule.slots("2026-11-02", {"tz": "America/Chicago", "slots": [
            {"slot": "a", "post_at": "11:30"}, {"slot": "b", "post_at": "18:30"}]})
        self.assertEqual([x["post_at"] for x in s], ["2026-11-02T17:30:00Z", "2026-11-03T00:30:00Z"])


if __name__ == "__main__":
    unittest.main()
