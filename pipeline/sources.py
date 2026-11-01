#!/usr/bin/env python3
"""Viral source videos for the operator loop: pick one, get its transcript + beat annotation, compress its beats
onto a 65-85 s Shorts skeleton, and check our script against it. Deterministic except `annotate` (claude -p).

  python -m pipeline.sources pick [--niche explainer] [--id ID|URL] [--exclude id,...] [--json] [--top N]
        ranked candidates; prints the pick (and the next empty slot); writes nothing
  python -m pipeline.sources transcript <id>          ensure a timestamped transcript (library, corpus or auto/raw);
        else yt-dlp subtitles (flock ytdlp), else audio + faster-whisper -t 4 (flock render). Prints its path.
  python -m pipeline.sources annotate-prompt <id>     print the filled annotate prompt (make.py runs claude on it)
  python -m pipeline.sources annotate <id> [--dry-run]  transcript + claude -p annotation -> research/corpus/<niche>/auto/
  python -m pipeline.sources skeleton <id> --out episodes/<slug>/source.json [--slug S]   (+ a `picked` row)
  python -m pipeline.sources variant --out episodes/<slug>/variant.json [--experiment EXP-003:treatment] [--variant k=v ...]
  python -m pipeline.sources origcheck <script.md> [--source-json path]   general gate + direct check vs the source
  python -m pipeline.sources mark <id> used|rejected|unavailable|picked|annotated [--slug S] [--reason R]

Data (repo-relative; on the Spark these are Spark-owned, see scripts/spark_owned.txt):
  reads  research/library/videos/*.json, research/library.jsonl, research/corpus/<niche>/{INDEX.json,<id>.md,raw/},
         research/corpus/<niche>/auto/, research/library/transcripts/, data/sources.jsonl, data/posts.jsonl,
         out/<slug>/qa/fingerprint.json, data/learned/rules.json, data/experiments.jsonl, pipeline/sources_kit_fit.json
  writes data/sources.jsonl (append-only), research/corpus/<niche>/auto/{raw/<id>.txt,<id>.md,<id>.index.json},
         episodes/<slug>/source.json, episodes/<slug>/variant.json
Never edits research/corpus/<niche>/INDEX.json or the hand-made corpus files.
Exit codes: 0 ok, 1 failed, 2 usage, 4 no candidate / source unavailable, 6 originality FAIL.
Env (optional, from the process env or ~/studio/.env): YTDLP_COOKIES_FILE (cookies for yt-dlp when YouTube
bot-blocks the Spark), STUDIO_CLAUDE_MODEL (default opus).
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import fcntl
import glob
import importlib.util
import json
import math
import os
import re
import shlex
import subprocess
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:  # shared helpers (lane L5); fall back to minimal local copies until they land
    from pipeline.common import jsonl as _jsonl  # type: ignore
except Exception:  # noqa: BLE001
    _jsonl = None
try:
    from pipeline.common import env as _env  # type: ignore
except Exception:  # noqa: BLE001
    _env = None

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("America/Chicago")
except Exception:  # noqa: BLE001
    TZ = dt.timezone(dt.timedelta(hours=-6))

PLAYBOOK_ORDER = ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]
SKELETON_NAME = {"S1": "HOOK", "S2": "STAKES", "S3": "RUNG", "S4": "TURN", "S5": "PEAK", "S6": "TWIST", "S7": "STINGER"}
# PLAYBOOK 1b defaults when a source lacks a beat we need (device text = the PLAYBOOK's own words, abridged)
DEFAULT_DEVICE = {
    "S1": "title as a second-person scenario; subject on screen in frame 1",
    "S2": "two numbers (a count and a multiple of something feared) or you as rung 0",
    "S3": "one notch worse per rung, one new number or landmark each, joined with and/then/so",
    "S4": "4-7 word false reassurance or 'not the worst part' line, background change on the next word",
    "S5": "the worst outcome or the big reveal, through a joke or a euphemism",
    "S6": "change axis after the peak: hypothetical becomes real, outside becomes inside",
    "S7": "end on the strongest word; last frame matches the first so it loops; no CTA",
}
# long-form sources are compressed onto these PLAYBOOK 1b ranges (% of our runtime)
LONG_RANGES = {"S1": (0, 5), "S2": (5, 18), "S3": (18, 48), "S4": (48, 54), "S5": (54, 75), "S6": (75, 92), "S7": (92, 100)}
MAX_ENTRIES = {"S1": 1, "S2": 2, "S3": 4, "S4": 1, "S5": 2, "S6": 2, "S7": 1}
DROP_LABELS = re.compile(r"^(CTA|END[- ]SCREEN|HOST INTRO|MID-ROLL|CHAPTER CARD)\b")
CATEGORY_RULES = [  # (regex on the beat label, PLAYBOOK code); first match wins
    (r"^(HOOK|COLD OPEN|SPECTACLE|SILENT)", "S1"),
    (r"^(STINGER|BOOKEND|BUTTON|KICKER|OUTRO|CLOSE|RECAP|RELIEF WITH STING|REFLECTION|FINAL BOARD|SYNTHESIS)", "S7"),
    (r"^(REHOOK|TURNSTILE|TURN\b|TIME JUMP|PIVOT|PATTERN BREAK|WAIVER|MICRO-CLIFFHANGER|FALSE RESOLUTION|FAKE-OUT)", "S4"),
    (r"(TWIST|REVERSAL|^FLIP|^REALITY|SPECIES SWITCH|PURPOSE REVEAL)", "S6"),
    (r"^(CLIMAX|PEAK|VERDICT|FINALE|CONSEQUENCE|UNDERDOG FINALE|STEP-OUT VERDICT|CASE)\b|PAYOFF", "S5"),
    (r"^(STAKES|REFRAME|PROMISE|SETUP|RULES|THESIS|ROADMAP|Q\d|MISDIRECT|FORMAT REVEAL|RELATE|BREATH|CAVEAT|RUNG 0|EVIDENCE)", "S2"),
]
# hook codes of the hand corpus (PLAYBOOK section 2, "Used by" column; nickname -> id from SOURCES/INDEX)
HOOK_BY_ID = {
    "fGcgWaswMns": "H1", "JkAcCdqYJN0": "H2", "6mRR91AbxjQ": "H2", "XFFjxTllpoA": "H3", "fmZfphacPPQ": "H4",
    "nAWpLtG-kNs": "H5", "qrfhhZ-Wvmk": "H5", "VtrcKTkhDHU": "H6", "mzeN0BXR4e0": "H7", "jw6bS-WL4F4": "H8",
    "Ky0XPonYDcc": "H9", "4QGQhaRv4Dw": "H10", "QxM2Hu70tVk": "H11", "2cK8l5Yg5w8": "H12", "2d6Ciu3INeA": "H13",
    "ZZf1KBnH5iI": "H14", "LpUzg3Dc-m0": "H15", "V15wrmD5VFs": "H16", "UNPK8PNCCmQ": "H17", "lVV5ztC3CtI": "H18",
    "SDs41Ke3v4Q": "H19", "thtoMGvpWIU": "H20", "UfbYyHuVx5M": "H21",
}
TARGET_RUNTIME = (65, 85)
TARGET_WORDS = (210, 260)
KOKORO_WPM_AT_1 = 172  # am_michael at speed 1.0 measured on explainer-giant-pacific-octopus (247 words / 86.1 s)
VS_SOURCE_RUN = 6       # FAIL if a 6-word run is shared with the source transcript (stricter than the general 8)
VS_SOURCE_SHARE = 0.01  # FAIL if >= 1 % of our 5-grams are in the source transcript


class SourceError(Exception):
    def __init__(self, msg, code=1):
        super().__init__(msg)
        self.code = code


# ------------------------------------------------------------------ small shared helpers

def rel(*p) -> str:
    return os.path.join(ROOT, *p)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jsonl_read(path: str) -> list[dict]:
    if _jsonl is not None:
        return _jsonl.read(path)
    out = []
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except ValueError:
                        print(f"[sources] skipping a bad line in {path}", file=sys.stderr)
    except FileNotFoundError:
        pass
    return out


def jsonl_append(path: str, row: dict) -> None:
    row = {"v": 1, "at": now_iso(), **row}
    if _jsonl is not None:
        return _jsonl.append(path, row)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path + ".lock", "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())


def load_env() -> dict:
    """KEY=VALUE from ~/studio/.env (values never printed), overlaid by the process env for the keys we use."""
    vals = {}
    if _env is not None:
        try:
            vals = dict(_env.load_env())
        except Exception:  # noqa: BLE001
            vals = {}
    else:
        try:
            for line in open(os.path.expanduser("~/studio/.env"), encoding="utf-8"):
                m = re.match(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*$", line)
                if m and not line.lstrip().startswith("#"):
                    vals[m.group(1)] = m.group(2).strip("'\"")
        except OSError:
            pass
    for k in ("YTDLP_COOKIES_FILE", "STUDIO_CLAUDE_MODEL"):
        if os.environ.get(k):
            vals[k] = os.environ[k]
    return vals


try:
    from pipeline.common import locks as _locks  # type: ignore
except Exception:  # noqa: BLE001
    _locks = None


@contextlib.contextmanager
def flock(name: str, timeout_s: int = 5400):
    if _locks is not None:
        try:
            with _locks.flock(name, timeout_s=timeout_s):
                yield
            return
        except _locks.LockTimeout as e:
            raise SourceError(str(e), 1)
    d = os.path.expanduser("~/studio/locks")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, f"{name}.lock"), "a") as f:
        t0 = time.time()
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.time() - t0 > timeout_s:
                    raise SourceError(f"timed out waiting for ~/studio/locks/{name}.lock", 1)
                time.sleep(5)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def write_json(path: str, obj) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


def slugify(text: str, max_words: int = 5) -> str:
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    stop = {"the", "a", "an", "of", "and", "to", "in", "on", "at", "is", "that", "my", "our", "your", "you", "why",
            "what", "how", "this", "it", "s", "if", "would", "could", "never", "want", "meet", "d", "every"}
    keep = [w for w in words if w not in stop and len(w) > 1][:max_words] or ["untitled"]
    return "-".join(keep)


def video_id(s: str) -> str:
    s = s.strip()
    for rx in (r"[?&]v=([\w-]{11})", r"youtu\.be/([\w-]{11})", r"/shorts/([\w-]{11})", r"/video/(\d{15,})"):
        m = re.search(rx, s)
        if m:
            return m.group(1)
    return s


# ------------------------------------------------------------------ candidates

def kit_rules() -> dict:
    return json.load(open(rel("pipeline", "sources_kit_fit.json"), encoding="utf-8"))


def kit_fit(title: str, rules: dict | None = None) -> dict:
    rules = rules or kit_rules()
    t = (title or "").lower()
    best = {"weight": 0.0, "component": None, "topic": None, "match": None}
    for r in rules["rules"]:
        for kw in r["kw"]:
            m = re.search(rf"\b(?:{kw})\b", t)
            if m and r["weight"] > best["weight"]:
                best = {"weight": r["weight"], "component": r["component"], "topic": r["topic"] or m.group(0),
                        "match": m.group(0)}
    pen = 0.0
    for r in rules.get("avoid", []):
        if any(re.search(rf"\b(?:{kw})\b", t) for kw in r["kw"]):
            pen = max(pen, r["penalty"])
    best["penalty"] = pen
    return best


def _fmt(platform: str, fmt: str | None, duration) -> str:
    if platform == "tiktok":
        return "tiktok"
    if platform == "youtube_shorts" or (fmt or "").lower().startswith("short"):
        return "short"
    if isinstance(duration, (int, float)) and duration and duration <= 180:
        return "short"
    return "long"


def load_candidates(niche: str = "explainer") -> dict[str, dict]:
    """-> {source_id: record}. Library outlier JSONs, daily-pull rows that clear the outlier bar, and corpus outliers."""
    cands: dict[str, dict] = {}

    def put(rec, origin):
        sid = rec["source_id"]
        cur = cands.get(sid)
        if cur is None:
            rec["origins"] = [origin]
            cands[sid] = rec
            return
        cur["origins"].append(origin)
        for k, v in rec.items():  # fresher numbers win for views/outlier; fill gaps otherwise
            if k in ("views", "outlier_score") and origin == "library.jsonl" and v:
                cur[k] = v
            elif cur.get(k) in (None, "", 0) and v not in (None, ""):
                cur[k] = v

    for f in sorted(glob.glob(rel("research", "library", "videos", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except ValueError:
            continue
        sid = d.get("id") or d.get("video_id") or os.path.splitext(os.path.basename(f))[0]
        if d.get("niche") != niche or d.get("role") != "outlier":
            continue
        put({"source_id": sid, "url": d.get("url"), "platform": "tiktok" if d.get("platform") == "tiktok" else "youtube",
             "format": _fmt(d.get("platform", ""), None, d.get("duration")), "title": d.get("title"),
             "channel": d.get("channel"), "views": d.get("views"), "outlier_score": d.get("outlier_score"),
             "duration_s": d.get("duration")}, "library/videos")
    latest = {}
    for r in jsonl_read(rel("research", "library.jsonl")):
        if r.get("type") == "video" and r.get("niche") == niche and r.get("id"):
            latest[r["id"]] = r
    for sid, r in latest.items():
        fmt = _fmt(r.get("platform", ""), r.get("format"), r.get("duration_s"))
        bar = 3.0 if fmt == "long" else 1.5
        if (r.get("outlier_score") or 0) >= bar and (r.get("views") or 0) >= 300000:
            put({"source_id": sid, "url": r.get("url"), "platform": r.get("platform"), "format": fmt,
                 "title": r.get("title"), "channel": r.get("channel"), "views": r.get("views"),
                 "outlier_score": r.get("outlier_score"), "duration_s": r.get("duration_s")}, "library.jsonl")
    for e in corpus_index(niche).values():
        if e.get("role", "outlier") != "outlier":
            continue
        put({"source_id": e["id"], "url": e.get("url"), "platform": "youtube", "format": _fmt("", e.get("format"), e.get("duration_s")),
             "title": e.get("title"), "channel": e.get("channel"), "views": e.get("views"),
             "outlier_score": e.get("outlier_score"), "duration_s": e.get("duration_s"),
             "premise": e.get("angle") or e.get("premise_one_line")}, "corpus")
    return cands


def corpus_index(niche: str = "explainer") -> dict[str, dict]:
    """Hand INDEX.json entries plus auto/<id>.index.json entries (auto never overrides a hand entry)."""
    out = {}
    for f in sorted(glob.glob(rel("research", "corpus", niche, "auto", "*.index.json"))):
        try:
            e = json.load(open(f, encoding="utf-8"))
            if isinstance(e, list):
                e = e[0]
            e["_file"] = os.path.relpath(f, ROOT)
            out[e["id"]] = e
        except (ValueError, KeyError, IndexError):
            continue
    try:
        for e in json.load(open(rel("research", "corpus", niche, "INDEX.json"), encoding="utf-8")):
            e["_file"] = f"research/corpus/{niche}/INDEX.json"
            out[e["id"]] = e
    except (OSError, ValueError):
        pass
    return out


def corpus_file(sid: str, niche: str = "explainer") -> str | None:
    for p in (rel("research", "corpus", niche, f"{sid}.md"), rel("research", "corpus", niche, "auto", f"{sid}.md")):
        if os.path.exists(p):
            return os.path.relpath(p, ROOT)
    return None


def transcript_file(sid: str, niche: str = "explainer") -> str | None:
    for p in (rel("research", "library", "transcripts", f"{sid}.txt"), rel("research", "corpus", niche, "raw", f"{sid}.txt"),
              rel("research", "corpus", niche, "auto", "raw", f"{sid}.txt")):
        if os.path.exists(p) and os.path.getsize(p) > 200:
            return os.path.relpath(p, ROOT)
    return None


def source_state() -> dict[str, dict]:
    return {r["source_id"]: r for r in jsonl_read(rel("data", "sources.jsonl")) if r.get("source_id")}


def is_unused(row: dict | None, now: dt.datetime | None = None) -> bool:
    if not row:
        return True
    st = row.get("status")
    if st in ("used", "rejected", "unavailable"):
        return False
    if st == "picked":
        try:
            at = dt.datetime.strptime(row["at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        except (KeyError, ValueError):
            return True
        return ((now or dt.datetime.now(dt.timezone.utc)) - at).total_seconds() > 24 * 3600
    return True


def recent_topics(n: int = 10) -> list[dict]:
    """Topics/titles of the last n published (or scheduled/draft) videos, plus the last n operator episodes."""
    seen, out = set(), []
    posts = [r for r in jsonl_read(rel("data", "posts.jsonl")) if r.get("status") in ("published", "scheduled", "draft", "sending")]
    slugs = []
    for r in sorted(posts, key=lambda r: r.get("at", ""), reverse=True):
        if r.get("slug") and r["slug"] not in slugs:
            slugs.append(r["slug"])
    eps = sorted(glob.glob(rel("episodes", "op-*", "source.json")), reverse=True)
    for s in slugs[:n]:
        fp = rel("out", s, "qa", "fingerprint.json")
        if os.path.exists(fp) and s not in seen:
            d = json.load(open(fp, encoding="utf-8"))
            out.append({"slug": s, "topic": d.get("topic"), "title": d.get("title"), "source_id": d.get("source_id")})
            seen.add(s)
    for f in eps[:n]:
        s = os.path.basename(os.path.dirname(f))
        if s in seen:
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except ValueError:
            continue
        out.append({"slug": s, "topic": d.get("topic"), "title": d.get("title"), "source_id": d.get("source_id")})
        seen.add(s)
    return out


def _jaccard(a: str, b: str) -> float:
    A, B = set(slugify(a, 99).split("-")), set(slugify(b, 99).split("-"))
    return len(A & B) / max(1, len(A | B))


def score(c: dict, rules: dict) -> dict:
    fit = kit_fit(c.get("title") or "", rules)
    if fit["weight"] < 0.6 and c.get("premise"):  # unnamed subject in the title ("the ocean's deadliest predator")
        alt = kit_fit(c["premise"], rules)
        if alt["weight"] > fit["weight"]:
            fit = {**alt, "penalty": max(fit["penalty"], alt["penalty"])}
    views = max(1, c.get("views") or 1)
    outl = max(0.01, c.get("outlier_score") or 0.01)
    is_short = 1 if c.get("format") in ("short", "tiktok") else 0
    has_tr = 1 if transcript_file(c["source_id"]) else 0
    has_co = 1 if corpus_file(c["source_id"]) else 0
    s = (math.log10(views) + 1.5 * math.log10(outl) + fit["weight"] + 0.5 * is_short + 0.3 * has_tr + 0.3 * has_co
         - fit["penalty"])
    reasons = [f"views {views:,}", f"outlier {outl:g}"]
    if fit["component"]:
        reasons.append(f"kit_fit:{fit['component'].split('/')[-1]} {fit['weight']:g}")
    if fit["penalty"]:
        reasons.append(f"off-kit penalty -{fit['penalty']:g}")
    if is_short:
        reasons.append("short")
    if has_tr:
        reasons.append("transcript")
    if has_co:
        reasons.append("corpus")
    topic = fit["topic"] or slugify(c.get("title") or "", 3).replace("-", " ")
    return {**c, "score": round(s, 3), "reasons": reasons, "kit_component": fit["component"], "topic": topic,
            "has_transcript": bool(has_tr), "has_corpus": bool(has_co)}


def rank(niche: str = "explainer", exclude=(), only_id: str | None = None) -> tuple[list[dict], list[dict]]:
    """-> (eligible ranked, dropped with reasons)."""
    rules = kit_rules()
    meme = re.compile(rules.get("meme_title", r"$^"), re.I)
    state = source_state()
    recent = recent_topics(10)
    cands = load_candidates(niche)
    ranked, dropped = [], []
    for sid, c in cands.items():
        c = score(c, rules)
        why = None
        if only_id is None:
            if sid in exclude:
                why = "excluded"
            elif not is_unused(state.get(sid)):
                why = f"already {state[sid]['status']}"
            elif not c.get("title") or meme.search(c["title"]):
                why = "meme/hashtag title"
            else:
                for r in recent:
                    if r.get("source_id") == sid:
                        why = f"source used by {r['slug']}"
                    elif r.get("topic") and c["topic"] and r["topic"] == c["topic"]:
                        why = f"same topic as {r['slug']}"
                    elif r.get("title") and _jaccard(r["title"], c["title"]) >= 0.5:
                        why = f"title too close to {r['slug']}"
                    if why:
                        break
        elif sid != only_id:
            continue
        (dropped if why else ranked).append({**c, "dropped": why} if why else c)
    ranked.sort(key=lambda c: (-c["score"], c["source_id"]))
    for i, c in enumerate(ranked):
        c["rank"] = i + 1
    return ranked, dropped


def next_slot(date: str | None = None, slot: str | None = None) -> dict:
    """The next local (America/Chicago) date/slot with no episodes/op-<date>-<slot>-* folder."""
    d = dt.date.fromisoformat(date) if date else dt.datetime.now(TZ).date()
    for _ in range(60):
        ymd = d.strftime("%Y%m%d")
        for s in ([slot] if slot else ["a", "b"]):
            if not glob.glob(rel("episodes", f"op-{ymd}-{s}-*")):
                return {"date": d.isoformat(), "ymd": ymd, "slot": s}
        if date and slot:
            return {"date": d.isoformat(), "ymd": ymd, "slot": slot, "taken": True}
        d += dt.timedelta(days=1)
    raise SourceError("no free slot in the next 60 days", 4)


def make_slug(ymd: str, slot: str, topic: str) -> str:
    return f"op-{ymd}-{slot}-{slugify(topic, 5)}"


# ------------------------------------------------------------------ transcripts

TS_LINE = re.compile(r"^\[(\d{1,2}):(\d{2})(?::(\d{2}))?(?:\.(\d+))?\]\s*(.*)$")


def read_transcript(path: str) -> list[tuple[float, str]]:
    out = []
    for line in open(rel(path) if not os.path.isabs(path) else path, encoding="utf-8", errors="ignore"):
        m = TS_LINE.match(line.strip())
        if not m:
            continue
        a, b, c, frac, text = m.groups()
        t = int(a) * 60 + int(b) if c is None else int(a) * 3600 + int(b) * 60 + int(c)
        if frac:
            t += float("0." + frac)
        if text.strip():
            out.append((float(t), text.strip()))
    return out


def _vtt_to_lines(vtt: str) -> list[tuple[float, str]]:
    """YouTube auto-sub VTT -> de-duplicated [(start s, text)] (rolling captions repeat the previous line)."""
    out, last = [], ""
    cue = None
    for line in vtt.splitlines():
        m = re.match(r"^(\d+):(\d{2}):(\d{2})\.(\d{3}) -->", line) or re.match(r"^(\d{2}):(\d{2})\.(\d{3}) -->", line)
        if m:
            g = m.groups()
            cue = (int(g[0]) * 3600 + int(g[1]) * 60 + int(g[2]) + int(g[3]) / 1000) if len(g) == 4 else (int(g[0]) * 60 + int(g[1]) + int(g[2]) / 1000)
            continue
        if cue is None or not line.strip() or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        text = re.sub(r"<[^>]+>", "", line).strip()
        if text and text != last:
            out.append((cue, text))
            last = text
    return out


def _fmt_ts(t: float) -> str:
    return f"[{int(t // 60):02d}:{t % 60:05.2f}]"


def ensure_transcript(sid: str, niche: str = "explainer", rec: dict | None = None) -> str:
    """-> repo-relative transcript path. Downloads only when no transcript exists anywhere (Spark only)."""
    have = transcript_file(sid, niche)
    if have:
        return have
    rec = rec or load_candidates(niche).get(sid) or {"source_id": sid, "url": f"https://www.youtube.com/watch?v={sid}"}
    url = rec.get("url") or f"https://www.youtube.com/watch?v={sid}"
    env = load_env()
    ytdlp = os.path.expanduser("~/studio/bin/yt-dlp")
    if not os.path.exists(ytdlp):
        ytdlp = os.path.expanduser("~/.local/bin/yt-dlp")
    if not os.path.exists(ytdlp):
        raise SourceError("yt-dlp not found (~/studio/bin or ~/.local/bin): run this on the Spark", 5)
    work = os.path.expanduser(f"~/studio/refs/{niche}/auto")
    os.makedirs(work, exist_ok=True)
    cookies = ["--cookies", env["YTDLP_COOKIES_FILE"]] if env.get("YTDLP_COOKIES_FILE") else []
    base = [ytdlp, "--no-warnings", "--no-playlist", *cookies]
    lines, how = [], ""
    with flock("ytdlp"):
        r = subprocess.run(["nice", "-n", "10", *base, "--skip-download", "--write-auto-subs", "--write-subs",
                            "--sub-langs", "en,en-orig,en-US,en.*", "--sub-format", "vtt", "-o", f"{work}/%(id)s.%(ext)s", url],
                           capture_output=True, text=True, timeout=600)
        vtts = sorted(glob.glob(f"{work}/{sid}*.vtt"), key=lambda p: ("orig" in p, p))
        if vtts:
            lines, how = _vtt_to_lines(open(vtts[0], encoding="utf-8", errors="ignore").read()), "yt-dlp auto-subs"
        if not lines:
            r2 = subprocess.run(["nice", "-n", "10", *base, "-f", "bestaudio[ext=m4a]/bestaudio", "-o", f"{work}/{sid}.%(ext)s", url],
                                capture_output=True, text=True, timeout=1800)
            audio = [p for p in glob.glob(f"{work}/{sid}.*") if not p.endswith((".vtt", ".json", ".txt"))]
            if r2.returncode != 0 or not audio:
                msg = (r.stderr + r2.stderr).strip().splitlines()[-1:] or ["no subtitles and no audio"]
                jsonl_append(rel("data", "sources.jsonl"), {"source_id": sid, "url": url, "status": "unavailable",
                                                            "reason": msg[0][:300]})
                raise SourceError(f"{sid}: no transcript available ({msg[0][:200]})", 4)
    if not lines:
        with flock("render"):  # whisper never runs during a render (thread budget)
            lines, how = _whisper(audio[0]), "faster-whisper small (CPU int8, 4 threads, VAD)"
    if not lines:
        raise SourceError(f"{sid}: transcription produced no text", 1)
    out = rel("research", "corpus", niche, "auto", "raw", f"{sid}.txt")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    head = (f"# {url} | {rec.get('title', '')} | {rec.get('channel', '')} | {rec.get('views', '')} | "
            f"{rec.get('outlier_score', '')} | {rec.get('duration_s', '')}\n# transcript: {how}; fetched {now_iso()}\n")
    with open(out, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(f"{_fmt_ts(t)} {x}" for t, x in lines) + "\n")
    return os.path.relpath(out, ROOT)


def _whisper(audio: str) -> list[tuple[float, str]]:
    py = os.path.expanduser("~/studio/.venv/bin/python")
    code = ("import json,sys\nfrom faster_whisper import WhisperModel\n"
            "m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=4)\n"
            "segs,_=m.transcribe(sys.argv[1],language='en',vad_filter=True)\n"
            "print(json.dumps([[s.start,s.text.strip()] for s in segs]))\n")
    env = {**os.environ, "CUDA_VISIBLE_DEVICES": "", "OMP_NUM_THREADS": "4"}
    r = subprocess.run(["nice", "-n", "10", py, "-c", code, audio], capture_output=True, text=True, env=env, timeout=3600)
    if r.returncode != 0:
        raise SourceError(f"whisper failed: {r.stderr.strip()[-300:]}", 1)
    return [(float(a), b) for a, b in json.loads(r.stdout.strip().splitlines()[-1])]


# ------------------------------------------------------------------ annotation

def annotation(sid: str, niche: str = "explainer") -> dict | None:
    return corpus_index(niche).get(sid)


def annotate_prompt(sid: str, niche: str = "explainer") -> str:
    rec = load_candidates(niche).get(sid) or {"source_id": sid}
    tr = transcript_file(sid, niche)
    if not tr:
        raise SourceError(f"{sid}: no transcript yet (run: python -m pipeline.sources transcript {sid})", 1)
    src = open(rel("pipeline", "prompts", f"annotate_{niche}.md"), encoding="utf-8").read()
    return src.format(id=sid, url=rec.get("url") or "", title=rec.get("title") or "", channel=rec.get("channel") or "",
                      views=rec.get("views") or "", outlier=rec.get("outlier_score") or "", duration=rec.get("duration_s") or "",
                      format=rec.get("format") or "", transcript=tr, niche=niche,
                      out_md=f"research/corpus/{niche}/auto/{sid}.md", out_index=f"research/corpus/{niche}/auto/{sid}.index.json")


def check_annotation(sid: str, niche: str = "explainer") -> list[str]:
    errs = []
    p = rel("research", "corpus", niche, "auto", f"{sid}.index.json")
    try:
        e = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        return [f"{os.path.relpath(p, ROOT)}: {ex}"]
    if isinstance(e, list):
        e = e[0] if e else {}
    if e.get("id") != sid:
        errs.append(f"index id {e.get('id')!r} != {sid}")
    beats = e.get("beat_sequence") or []
    if len(beats) < 4:
        errs.append("beat_sequence has fewer than 4 beats")
    parsed = [parse_beat(b, e.get("duration_s")) for b in beats]
    if sum(1 for b in parsed if b["t0"] is not None) < len(parsed) * 0.75:
        errs.append("most beats lack a '(m:ss-m:ss, x%)' time range")
    if e.get("hook_code") and not re.match(r"^H([1-9]|1\d|2[01])$", str(e["hook_code"])):
        errs.append(f"hook_code {e['hook_code']!r} is not H1-H21")
    if not os.path.exists(rel("research", "corpus", niche, "auto", f"{sid}.md")):
        errs.append("auto .md missing")
    return errs


# ------------------------------------------------------------------ skeleton

BEAT_RX = re.compile(r"^(?P<label>[A-Z][A-Z0-9/+\-]*(?: [A-Z0-9][A-Z0-9/+\-]*)*)\b\s*(?P<rest>.*)$")
RANGE_RX = re.compile(r"\((?P<a>\d+:\d{2})\s*-\s*(?P<b>\d+:\d{2})(?:,\s*(?P<pct>[\d.]+)\s*%[^)]*)?\)")
PCT_RX = re.compile(r"\((?P<a>[\d.]+)\s*-\s*(?P<b>[\d.]+)\s*%\)")


def _mmss(s: str) -> float:
    m, sec = s.split(":")
    return int(m) * 60 + int(sec)


def parse_beat(text: str, duration: float | None) -> dict:
    m = BEAT_RX.match(text.strip())
    label, rest = (m.group("label"), m.group("rest")) if m else ("BEAT", text)
    label = re.sub(r"\s+(\d+-|N-|T)$", "", label).strip()
    t0 = t1 = None
    r = RANGE_RX.search(text)
    if r:
        t0, t1 = _mmss(r.group("a")), _mmss(r.group("b"))
    elif duration:
        p = PCT_RX.search(text)
        if p:
            t0, t1 = float(p.group("a")) / 100 * duration, float(p.group("b")) / 100 * duration
    device = RANGE_RX.sub("", PCT_RX.sub("", rest)).strip(" ,;")
    return {"label": label, "t0": t0, "t1": t1, "device": device[:200]}


def category(label: str, pct_mid: float | None) -> str | None:
    if DROP_LABELS.match(label):
        return None
    if label == "REVEAL" or label.startswith("REVEAL"):
        return "S6" if (pct_mid or 0) > 60 else "S5"
    for rx, code in CATEGORY_RULES:
        if re.search(rx, label):
            return code
    if pct_mid is not None:
        if pct_mid < 6:
            return "S1"
        if pct_mid > 92:
            return "S7"
    return "S3"


def hook_shapes() -> dict[str, str]:
    try:
        pb = open(rel("research", "corpus", "explainer", "PLAYBOOK.md"), encoding="utf-8").read()
    except OSError:
        return {}
    return {f"H{n}": name for n, name in re.findall(r"^\|\s*H(\d+)\s*\|\s*\*\*(.+?)\*\*", pb, re.M)}


def _merge(entries: list[dict], code: str, cap: int) -> list[dict]:
    """Merge a run of same-code entries down to `cap` entries, evenly, keeping order."""
    if len(entries) <= cap:
        return entries
    out, n = [], len(entries)
    for k in range(cap):
        grp = entries[k * n // cap:(k + 1) * n // cap]
        out.append({"code": code, "from_beats": [i for g in grp for i in g["from_beats"]],
                    "src_s": sum(g["src_s"] for g in grp), "device": " + ".join(g["device"] for g in grp if g["device"])[:300]})
    return out


def build_skeleton(beats: list[dict], fmt: str, runtime: float = 75.0) -> list[dict]:
    """beats: source beats with code (S1..S7 or None=dropped), pct0/pct1. -> skeleton entries for our Short."""
    seq = []
    prev = 0
    for b in beats:
        if not b.get("playbook"):
            continue
        c = max(PLAYBOOK_ORDER.index(b["playbook"]), prev)  # keep the PLAYBOOK order: a late PAYOFF is second-axis
        prev = c
        seq.append({"code": PLAYBOOK_ORDER[c], "from_beats": [b["i"]], "src_s": max(0.5, (b["t1"] or 0) - (b["t0"] or 0)),
                    "device": b.get("device", "")})
    groups: list[list[dict]] = []
    for e in seq:
        if groups and groups[-1][0]["code"] == e["code"]:
            groups[-1].append(e)
        else:
            groups.append([e])
    entries = []
    for g in groups:
        code = g[0]["code"]
        cap = MAX_ENTRIES[code]
        if code == "S1":  # one hook; extra hook-ish beats fold into it
            g = [{"code": code, "from_beats": [i for x in g for i in x["from_beats"]], "src_s": sum(x["src_s"] for x in g),
                  "device": " + ".join(x["device"] for x in g if x["device"])[:300]}]
        entries += _merge(g, code, cap)
    have = {e["code"] for e in entries}
    for code in ("S1", "S2", "S3", "S4", "S5", "S7"):  # mandatory beats the source lacks: PLAYBOOK defaults
        if code not in have:
            pos = next((k for k, e in enumerate(entries) if PLAYBOOK_ORDER.index(e["code"]) > PLAYBOOK_ORDER.index(code)), len(entries))
            entries.insert(pos, {"code": code, "from_beats": [], "src_s": 0.0, "device": DEFAULT_DEVICE[code] + " (PLAYBOOK default)"})
    if "S3" in have and sum(1 for e in entries if e["code"] == "S3") < 2:  # at least 2 rungs for a 65-85 s Short
        k = next(k for k, e in enumerate(entries) if e["code"] == "S3")
        entries.insert(k + 1, {**entries[k], "device": entries[k]["device"] + " (second rung, one notch worse)"})
    # target % of our runtime
    if fmt == "long" or not any(e["src_s"] for e in entries):
        ranges = dict(LONG_RANGES)
        if not any(e["code"] == "S6" for e in entries):
            ranges["S5"] = (54, 92)
        by = {}
        for e in entries:
            by.setdefault(e["code"], []).append(e)
        for code, es in by.items():
            a, b = ranges[code]
            tot = sum(max(1.0, x["src_s"]) for x in es)
            t = a
            for x in es:
                w = (b - a) * max(1.0, x["src_s"]) / tot if code == "S3" else (b - a) / len(es)
                x["pct0"], x["pct1"] = round(t, 1), round(t + w, 1)
                t += w
    else:  # a Short: keep the source's own proportions, hook <= 6 %, stinger >= 3 %
        tot = sum(max(0.5, e["src_s"]) if e["src_s"] else 0.06 * 60 for e in entries)
        t = 0.0
        for e in entries:
            w = 100 * (max(0.5, e["src_s"]) if e["src_s"] else 3.6) / tot
            e["pct0"], e["pct1"] = round(t, 1), round(t + w, 1)
            t += w
        h = entries[0]
        if h["code"] == "S1" and h["pct1"] > 6:
            extra = h["pct1"] - 6
            h["pct1"] = 6.0
            rest = entries[1:]
            span = 100 - 6
            old_span = 100 - (6 + extra)
            for e in rest:  # stretch the rest to fill
                e["pct0"] = round(6 + (e["pct0"] - 6 - extra) * span / old_span, 1)
                e["pct1"] = round(6 + (e["pct1"] - 6 - extra) * span / old_span, 1)
        entries[-1]["pct1"] = 100.0
    out = []
    rung = 0
    for i, e in enumerate(entries):
        name = SKELETON_NAME[e["code"]]
        if e["code"] == "S3":
            rung += 1
            name = f"RUNG{rung}"
        out.append({"i": i, "label": name, "playbook": e["code"], "from_beats": e["from_beats"],
                    "target_pct0": e["pct0"], "target_pct1": e["pct1"],
                    "target_s": [round(e["pct0"] * runtime / 100, 1), round(e["pct1"] * runtime / 100, 1)],
                    "device": e["device"] or DEFAULT_DEVICE[e["code"]]})
    return out


def skeleton(sid: str, niche: str = "explainer", topic: str | None = None) -> dict:
    cands = load_candidates(niche)
    rec = cands.get(sid)
    ann = annotation(sid, niche)
    if rec is None and ann is None:
        raise SourceError(f"{sid} is not in research/library or the {niche} corpus", 4)
    rec = score(rec or {"source_id": sid, "url": ann.get("url"), "platform": "youtube", "format": _fmt("", ann.get("format"), ann.get("duration_s")),
                        "title": ann.get("title"), "channel": ann.get("channel"), "views": ann.get("views"),
                        "outlier_score": ann.get("outlier_score"), "duration_s": ann.get("duration_s")}, kit_rules())
    tr = transcript_file(sid, niche)
    lines = read_transcript(tr) if tr else []
    duration = rec.get("duration_s") or (ann or {}).get("duration_s") or (lines[-1][0] + 3 if lines else None)
    beats = []
    for i, txt in enumerate((ann or {}).get("beat_sequence") or []):
        b = parse_beat(txt, duration)
        beats.append(b)
    for k, b in enumerate(beats):  # fill missing times from neighbours
        if b["t0"] is None:
            b["t0"] = beats[k - 1]["t1"] if k and beats[k - 1]["t1"] is not None else 0.0
        if b["t1"] is None:
            b["t1"] = next((x["t0"] for x in beats[k + 1:] if x["t0"] is not None), duration or b["t0"])
    D = float(duration or (beats[-1]["t1"] if beats else 60) or 60)
    for i, b in enumerate(beats):
        b["i"] = i
        b["pct0"], b["pct1"] = round(100 * b["t0"] / D, 1), round(100 * b["t1"] / D, 1)
        b["playbook"] = category(b["label"], (b["pct0"] + b["pct1"]) / 2)
    words = sum(len(x.split()) for _, x in lines)
    span = (lines[-1][0] - lines[0][0] + 3.0) if len(lines) > 1 else None
    wpm = round(60 * words / span) if span and words > 30 else None
    hook_code = (ann or {}).get("hook_code") or HOOK_BY_ID.get(sid)
    first = " ".join(x for _, x in lines[:4])
    first_sentence = re.split(r"(?<=[.!?])\s", first)[0] if first else ""
    pacing = dict((ann or {}).get("pacing") or {})
    pacing.setdefault("wpm", wpm)
    pacing.setdefault("avg_shot_s", None)
    pacing.setdefault("rehook_s", 9.0 if rec["format"] != "long" else 30.0)
    fmt = rec["format"]
    skel = build_skeleton(beats, "long" if fmt == "long" else "short")
    return {
        "v": 1, "source_id": sid, "url": rec.get("url"), "platform": rec.get("platform") or "youtube", "format": fmt,
        "title": rec.get("title"), "channel": rec.get("channel"), "views": rec.get("views"),
        "outlier_score": rec.get("outlier_score"), "duration_s": duration, "picked_at": now_iso(),
        "pick": {"rank": rec.get("rank"), "score": rec["score"], "reasons": rec["reasons"],
                 "candidates_considered": len(cands)},
        "topic": topic or rec["topic"], "kit_component": rec.get("kit_component"),
        "corpus_file": corpus_file(sid, niche), "transcript_file": tr,
        "annotation": (ann or {}).get("_file"),
        "angle": (ann or {}).get("angle") or (ann or {}).get("premise_one_line") or "",
        "hook": {"code": hook_code, "shape": hook_shapes().get(hook_code or "", None),
                 "first_speech_s": lines[0][0] if lines else None, "words": len(first_sentence.split()) or None,
                 "source_first_line_words": len(first_sentence.split()) or None},
        "beats": [{k: b[k] for k in ("i", "label", "playbook", "t0", "t1", "pct0", "pct1", "device")} | {"purpose": ""}
                  for b in beats],
        "pacing": pacing,
        "skeleton": skel,
        "target": {"runtime_s": list(TARGET_RUNTIME), "words": list(TARGET_WORDS)},
        "heatmap_file": (f"data/heatmaps/{sid}.json" if os.path.exists(rel("data", "heatmaps", f"{sid}.json")) else None),
    }


def skeleton_table(src: dict) -> str:
    rows = ["| # | Our beat | PLAYBOOK | Target % | Target s | Source beats (label @ time) | Device to borrow |",
            "|---|---|---|---|---|---|---|"]
    beats = {b["i"]: b for b in src["beats"]}
    for e in src["skeleton"]:
        fb = ", ".join(f"{beats[i]['label']} @ {int(beats[i]['t0'] // 60)}:{int(beats[i]['t0'] % 60):02d}" for i in e["from_beats"]
                       if i in beats) or "(none: PLAYBOOK default)"
        rows.append(f"| {e['i']} | {e['label']} | {e['playbook']} | {e['target_pct0']:g}-{e['target_pct1']:g} | "
                    f"{e['target_s'][0]:g}-{e['target_s'][1]:g} | {fb} | {e['device']} |")
    return "\n".join(rows)


# ------------------------------------------------------------------ variants (experiments + learned rules)

VARIABLES = {
    "hook.type": ("enum", ["source"] + [f"H{i}" for i in range(1, 22)]),
    "hook.max_words": ("int", (5, 14)),
    "hook.visual": ("enum", ["subject_full", "subject_eye", "you_vs_subject", "headline_only"]),
    "structure.skeleton": ("enum", ["source", "playbook_list", "playbook_ladder"]),
    "structure.turnstile_pct": ("int", (40, 70)),
    "structure.ending": ("enum", ["loop_callback", "stinger_fact", "twist_question"]),
    "pace.wpm": ("int", (170, 215)),
    "pace.rehook_s": ("float", (6, 12)),
    "visual.max_hold_s": ("float", (1.5, 3.0)),
    "visual.cover": ("enum", ["scale", "eye", "abyss", "headline"]),
    "visual.shot_mix": ("enum", ["creature_heavy", "infographic_heavy", "balanced"]),
    "visual.caption_style": ("enum", ["pill", "page"]),
}
DEFAULTS = {"hook.type": "source", "hook.max_words": 12, "structure.skeleton": "source", "pace.rehook_s": 9,
            "visual.max_hold_s": 3.0, "visual.cover": "scale", "visual.shot_mix": "balanced"}


def coerce(key: str, val):
    if key not in VARIABLES:
        raise SourceError(f"unknown variable {key!r}; known: {', '.join(VARIABLES)}", 2)
    kind, spec = VARIABLES[key]
    if kind == "enum":
        v = str(val)
        if v.upper() in spec:
            v = v.upper()
        if v not in spec:
            raise SourceError(f"{key}={val!r}: must be one of {spec}", 2)
        return v
    try:
        v = int(val) if kind == "int" else float(val)
    except (TypeError, ValueError):
        raise SourceError(f"{key}={val!r}: must be a {kind}", 2)
    if not spec[0] <= v <= spec[1]:
        raise SourceError(f"{key}={val!r}: must be within {spec[0]}-{spec[1]}", 2)
    return v


def learned_rules() -> dict:
    try:
        return json.load(open(rel("data", "learned", "rules.json"), encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def directive(key: str, v, src: dict | None = None) -> str | None:
    hook = (src or {}).get("hook") or {}
    shapes = hook_shapes()
    if key == "hook.type":
        code = hook.get("code") if v == "source" else v
        if not code:
            return "Hook: use the source's hook shape as described in the skeleton (no PLAYBOOK code known)."
        return f"Hook: use hook shape {code} ({shapes.get(code, '?')}) from research/corpus/explainer/PLAYBOOK.md section 2, in fresh words."
    if key == "hook.max_words":
        return f"Hook: the first sentence has at most {v} words."
    if key == "hook.visual":
        return {"subject_full": "Frame 0 (cover): the whole subject, fully visible, plus a 1-3 word headline.",
                "subject_eye": "Frame 0 (cover): an extreme close-up on the subject's eye or face, plus a headline.",
                "you_vs_subject": "Frame 0 (cover): YOU (stick figure) next to the subject at true scale, plus a headline.",
                "headline_only": "Frame 0 (cover): a big headline over the dark ocean; the subject enters on the first word."}[v]
    if key == "structure.skeleton":
        return {"source": "Structure: follow the source skeleton table exactly (beat order and target %).",
                "playbook_list": "Structure: a PLAYBOOK 1b 60-90 s list Short (4-8 rungs of 7-15 s, turn at 58-66 %, answer at 66-91 %).",
                "playbook_ladder": "Structure: a PLAYBOOK 1b ladder (S1-S7, a new rung every 8-10 s)."}[v]
    if key == "structure.turnstile_pct":
        return f"Structure: put the turnstile re-hook line at about {v} % of the runtime."
    if key == "structure.ending":
        return {"loop_callback": "Ending: the last line calls back to the hook so the Short loops.",
                "stinger_fact": "Ending: end on one hard, true stinger fact (a number or a recurrence), cut within 1 s.",
                "twist_question": "Ending: end on a short twist question that reframes the hook."}[v]
    if key == "pace.wpm":
        speed = max(0.9, min(1.25, round(v / KOKORO_WPM_AT_1, 2)))
        return (f"Pace: about {v} words per minute: set the front matter `speed: {speed}` and write about "
                f"{int(v * 75 / 60)} spoken words for a 75 s runtime.")
    if key == "pace.rehook_s":
        return f"Pace: a re-hook (new number, landmark, question or 'it gets worse' line) at least every {v:g} s of speech."
    if key == "visual.max_hold_s":
        return f"Visuals: no picture hold longer than {v:g} s (a new layer, keyframe or camera key at least that often)."
    if key == "visual.cover":
        return f"Thumbnail/cover: use the thumbs template '{v}' as the primary thumbnail."
    if key == "visual.shot_mix":
        return {"creature_heavy": "Visuals: most scenes show a creature or figure at true scale; infographics only as small overlays.",
                "infographic_heavy": "Visuals: most scenes lead with an infographic (Stat, ScaleBar, DepthMeter, Timer, Options, SpeedBars).",
                "balanced": "Visuals: alternate creature/figure scenes and infographic scenes."}[v]
    if key == "visual.caption_style":
        return f"Captions: '{v}' style (recorded; the caption renderer is not switched per episode yet)."
    return None


SCRIPT_KEYS = ("hook.type", "hook.max_words", "structure.skeleton", "structure.turnstile_pct", "structure.ending",
               "pace.wpm", "pace.rehook_s")
SHOTS_KEYS = ("hook.visual", "visual.max_hold_s", "visual.shot_mix", "visual.caption_style")
PACKAGE_KEYS = ("visual.cover",)


def build_variant(experiment: str | None = None, overrides: list[str] | None = None, src: dict | None = None) -> dict:
    rules = learned_rules()
    values = {**DEFAULTS, **(rules.get("defaults") or {})}
    exp_id, arm, exp_vars = None, None, {}
    if experiment:
        if ":" not in experiment:
            raise SourceError("--experiment wants EXP-NNN:control|treatment", 2)
        exp_id, arm = experiment.split(":", 1)
        rows = [r for r in jsonl_read(rel("data", "experiments.jsonl")) if r.get("type") == "experiment" and r.get("experiment_id") == exp_id]
        if not rows:
            raise SourceError(f"{exp_id} not found in data/experiments.jsonl", 2)
        e = rows[-1]
        if arm not in ("control", "treatment"):
            raise SourceError(f"arm {arm!r} must be control or treatment", 2)
        exp_vars[e["variable"]] = coerce(e["variable"], e[arm])
    over = {}
    for kv in overrides or []:
        if "=" not in kv:
            raise SourceError(f"--variant {kv!r}: want key=value", 2)
        k, v = kv.split("=", 1)
        over[k.strip()] = coerce(k.strip(), v.strip())
    values = {k: coerce(k, v) for k, v in {**values, **exp_vars, **over}.items() if k in VARIABLES}
    dirs = {k: directive(k, v, src) for k, v in values.items()}
    return {"v": 1, "experiment_id": exp_id, "arm": arm, "variables": {**exp_vars, **over},
            "values": values, "rules_version": rules.get("updated_at"),
            "directives": [d for d in dirs.values() if d],
            "directives_by_step": {"script": [dirs[k] for k in SCRIPT_KEYS if dirs.get(k)],
                                   "shots": [dirs[k] for k in SHOTS_KEYS if dirs.get(k)],
                                   "package": [dirs[k] for k in PACKAGE_KEYS if dirs.get(k)]},
            "learned_notes": (rules.get("notes") or [])[:12]}


# ------------------------------------------------------------------ originality vs the source

def _orig_module():
    spec = importlib.util.spec_from_file_location("originality_check", rel("scripts", "originality_check.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def vs_source(script_path: str, transcript_path: str) -> dict:
    oc = _orig_module()
    ours = oc.words(oc.script_text(script_path))
    src = oc.words(oc.source_text(__import__("pathlib").Path(rel(transcript_path) if not os.path.isabs(transcript_path) else transcript_path)))
    grams = oc.ngrams(ours, 5)
    share = len(grams & oc.ngrams(src, 5)) / max(1, len(grams))
    # longest shared run of consecutive words (longest common substring over word lists)
    pos: dict[str, list[int]] = {}
    for j, w in enumerate(src):
        pos.setdefault(w, []).append(j)
    best, prev = 0, {}
    for w in ours:
        cur = {}
        for j in pos.get(w, ()):
            cur[j] = prev.get(j - 1, 0) + 1
            if cur[j] > best:
                best = cur[j]
        prev = cur
    return {"max_run": best, "share_5gram": round(share, 4), "words": len(ours),
            "pass": best < VS_SOURCE_RUN and share < VS_SOURCE_SHARE}


def origcheck(script: str, source_json: str | None = None) -> int:
    r = subprocess.run([sys.executable, rel("scripts", "originality_check.py"), script, rel("research", "corpus"),
                        rel("research", "library", "transcripts")], capture_output=True, text=True)
    general = r.stdout.strip()
    ok = r.returncode == 0 and "PASS" in general.splitlines()[0:1]
    print("general:", general.splitlines()[0] if general else "(no output)")
    for line in general.splitlines()[1:]:
        print("  " + line)
    sj = source_json or os.path.join(os.path.dirname(os.path.abspath(script)), "source.json")
    if os.path.exists(sj):
        src = json.load(open(sj, encoding="utf-8"))
        tr = src.get("transcript_file")
        if tr and os.path.exists(rel(tr)):
            v = vs_source(script, tr)
            print(f"vs source {src['source_id']}: longest shared run {v['max_run']} words (FAIL at {VS_SOURCE_RUN}), "
                  f"{v['share_5gram']:.2%} shared 5-grams (FAIL at {VS_SOURCE_SHARE:.0%}) -> {'PASS' if v['pass'] else 'FAIL'}")
            ok = ok and v["pass"]
        else:
            print(f"vs source: no transcript for {src.get('source_id')} (general check only)")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 6


# ------------------------------------------------------------------ CLI

def _local_claude(prompt: str, name: str, tools: list[str], timeout: int = 1800) -> dict:
    model = load_env().get("STUDIO_CLAUDE_MODEL") or "opus"
    claude = os.path.expanduser("~/.local/bin/claude") if not shutil_which("claude") else shutil_which("claude")
    r = subprocess.run(["timeout", str(timeout), claude, "-p", "--model", model, "--output-format", "json",
                        "--permission-mode", "acceptEdits", "--allowedTools", *tools], input=prompt, cwd=ROOT,
                       capture_output=True, text=True)
    res = {}
    for line in reversed(r.stdout.strip().splitlines()):
        if line.startswith("{"):
            try:
                res = json.loads(line)
                break
            except ValueError:
                pass
    if r.returncode != 0 or res.get("is_error"):
        raise SourceError(f"{name}: claude -p failed (exit {r.returncode}): {(res.get('result') or r.stderr)[-300:]}",
                          5 if re.search(r"auth|login|401|403|credential|expired", r.stdout + r.stderr, re.I) else 1)
    return res


def shutil_which(x):
    import shutil
    return shutil.which(x)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.sources", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pick")
    p.add_argument("--niche", default="explainer")
    p.add_argument("--id", help="resolve this source id or URL instead of ranking")
    p.add_argument("--exclude", default="")
    p.add_argument("--json", action="store_true")
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--date")
    p.add_argument("--slot", choices=["a", "b"])
    for name in ("transcript", "annotate-prompt"):
        q = sub.add_parser(name)
        q.add_argument("id")
        q.add_argument("--niche", default="explainer")
    q = sub.add_parser("annotate")
    q.add_argument("id")
    q.add_argument("--niche", default="explainer")
    q.add_argument("--dry-run", action="store_true", help="transcript only, no claude")
    q.add_argument("--force", action="store_true", help="re-annotate even if an annotation exists")
    q = sub.add_parser("check-annotation")
    q.add_argument("id")
    q.add_argument("--niche", default="explainer")
    q = sub.add_parser("skeleton")
    q.add_argument("id")
    q.add_argument("--niche", default="explainer")
    q.add_argument("--out", required=True)
    q.add_argument("--slug")
    q.add_argument("--topic")
    q = sub.add_parser("variant")
    q.add_argument("--out", required=True)
    q.add_argument("--experiment")
    q.add_argument("--variant", action="append", default=[])
    q.add_argument("--source-json")
    q = sub.add_parser("origcheck")
    q.add_argument("script")
    q.add_argument("--source-json")
    q = sub.add_parser("mark")
    q.add_argument("id")
    q.add_argument("status", choices=["picked", "annotated", "used", "rejected", "unavailable"])
    q.add_argument("--slug")
    q.add_argument("--reason")
    q.add_argument("--url")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "pick":
            only = video_id(a.id) if a.id else None
            ranked, dropped = rank(a.niche, exclude=set(filter(None, a.exclude.split(","))), only_id=only)
            if only and not ranked:
                if only in corpus_index(a.niche):
                    e = corpus_index(a.niche)[only]
                    ranked = [score({"source_id": only, "url": e.get("url"), "platform": "youtube",
                                     "format": _fmt("", e.get("format"), e.get("duration_s")), "title": e.get("title"),
                                     "channel": e.get("channel"), "views": e.get("views"),
                                     "outlier_score": e.get("outlier_score"), "duration_s": e.get("duration_s")}, kit_rules())]
                    ranked[0]["rank"] = None
                else:
                    raise SourceError(f"{only} is not in research/library or the {a.niche} corpus", 4)
            if not ranked:
                raise SourceError("no unused candidate source", 4)
            slot = next_slot(a.date, a.slot)
            pick = ranked[0]
            out = {"pick": pick, "slot": slot, "slug": make_slug(slot["ymd"], slot["slot"], pick["topic"]),
                   "candidates": len(ranked) + len(dropped), "eligible": len(ranked),
                   "top": [{k: c.get(k) for k in ("rank", "source_id", "score", "format", "views", "outlier_score", "topic", "title")}
                           for c in ranked[:a.top]],
                   "dropped": [{k: c.get(k) for k in ("source_id", "dropped", "title")} for c in dropped][:20]}
            if a.json:
                print(json.dumps(out, ensure_ascii=False))
            else:
                for c in out["top"]:
                    print(f"{c['rank'] or '-':>3} {c['score']:6.2f} {c['source_id']:<20} {c['format']:<6} {c['views'] or 0:>11,} "
                          f"x{c['outlier_score']:<7} {c['topic']!s:<18} {c['title']}")
                print(f"pick: {pick['source_id']} -> {out['slug']} ({', '.join(pick['reasons'])}); "
                      f"{len(dropped)} dropped, e.g. {[d['dropped'] for d in dropped[:3]]}")
            return 0
        if a.cmd == "transcript":
            print(ensure_transcript(video_id(a.id), a.niche))
            return 0
        if a.cmd == "annotate-prompt":
            print(annotate_prompt(video_id(a.id), a.niche))
            return 0
        if a.cmd == "check-annotation":
            errs = check_annotation(video_id(a.id), a.niche)
            print("\n".join(errs) or "PASS")
            return 0 if not errs else 1
        if a.cmd == "annotate":
            sid = video_id(a.id)
            tr = ensure_transcript(sid, a.niche)
            print(f"transcript: {tr}")
            if corpus_file(sid, a.niche) and not a.force:
                print(f"annotation exists: {corpus_file(sid, a.niche)}")
                return 0
            if a.dry_run:
                print("DRY-RUN: transcript only, no claude annotation")
                return 0
            res = _local_claude(annotate_prompt(sid, a.niche), "annotate", ["Read", "Write", "Edit", "Glob", "Grep",
                                                                           "Bash(python3 -m pipeline.sources check-annotation:*)"])
            errs = check_annotation(sid, a.niche)
            if errs:
                raise SourceError(f"annotation invalid: {errs}", 1)
            jsonl_append(rel("data", "sources.jsonl"), {"source_id": sid, "status": "annotated"})
            print(f"annotated: research/corpus/{a.niche}/auto/{sid}.md ({res.get('total_cost_usd', 0):.2f} USD)")
            return 0
        if a.cmd == "skeleton":
            sid = video_id(a.id)
            src = skeleton(sid, a.niche, a.topic)
            out = a.out if os.path.isabs(a.out) else rel(a.out)
            write_json(out, src)
            if a.slug:
                jsonl_append(rel("data", "sources.jsonl"), {"source_id": sid, "url": src.get("url"), "status": "picked",
                                                            "slug": a.slug, "score": src["pick"]["score"]})
            print(f"source.json: {os.path.relpath(out, ROOT)}: {len(src['beats'])} source beats -> {len(src['skeleton'])} "
                  f"skeleton beats, hook {src['hook']['code']}, wpm {src['pacing'].get('wpm')}")
            return 0
        if a.cmd == "variant":
            src = json.load(open(rel(a.source_json) if a.source_json and not os.path.isabs(a.source_json) else a.source_json,
                                 encoding="utf-8")) if a.source_json else None
            v = build_variant(a.experiment, a.variant, src)
            out = a.out if os.path.isabs(a.out) else rel(a.out)
            write_json(out, v)
            print(f"variant.json: {os.path.relpath(out, ROOT)}: experiment {v['experiment_id']}:{v['arm']} "
                  f"vars {v['variables']}")
            return 0
        if a.cmd == "origcheck":
            return origcheck(a.script, a.source_json)
        if a.cmd == "mark":
            jsonl_append(rel("data", "sources.jsonl"), {"source_id": video_id(a.id), "status": a.status, "slug": a.slug,
                                                        "reason": a.reason, "url": a.url})
            print(f"{a.id}: {a.status}")
            return 0
    except SourceError as e:
        print(f"sources: {e}", file=sys.stderr)
        return e.code
    return 2


if __name__ == "__main__":
    sys.exit(main())
