"""Buffer GraphQL client and the `channels` / `introspect` CLIs (lane L3, docs/OPERATOR_DESIGN.md 8.1, 8.3).

    python -m pipeline.publish.buffer channels [--dry-run]     # organizations + channel ids for ~/studio/.env
    python -m pipeline.publish.buffer introspect [--dry-run]   # saves data/buffer_schema.json

Credentials come only from ~/studio/.env (BUFFER_API_KEY, optional BUFFER_API_URL, BUFFER_ORG_ID). Without a key every
command runs in dry-run: it prints the exact HTTP request (key shown as ***) and sends nothing. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from pipeline.common import env as cenv
from pipeline.common import timeutil

from . import paths

DEFAULT_URL = "https://api.buffer.com"
QUERIES = Path(__file__).with_name("queries.graphql")
USER_AGENT = "faceless-studio-publisher/1 (+pipeline/publish)"
MAX_TRIES = 4

EXIT_OK, EXIT_FAIL, EXIT_USAGE, EXIT_BUDGET, EXIT_NOTHING, EXIT_DEP, EXIT_GATE = 0, 1, 2, 3, 4, 5, 6


class BufferError(Exception):
    exit_code = EXIT_FAIL


class DependencyDown(BufferError):
    """Auth rejected (401/403, UNAUTHORIZED/FORBIDDEN): exit 5, which can pause the operator loop."""
    exit_code = EXIT_DEP


class Unavailable(BufferError):
    """Buffer 5xx or unreachable after the retries: a transient outage, exit 1 (the next status bucket retries; a
    short blip must never pause an unattended loop)."""
    exit_code = EXIT_FAIL


class NotFound(BufferError):
    pass


class Ambiguous(BufferError):
    """A mutation may or may not have been applied (timeout / 5xx after the request was sent)."""


class MutationFailed(BufferError):
    """Buffer returned a typed MutationError (validation, limits, media fetch)."""


# ---------------------------------------------------------------------------------------------------------------
# queries.graphql loader

_OP_RE = re.compile(r"^(query|mutation|fragment)\s+(\w+)", re.M)


def _blocks(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    ms = list(_OP_RE.finditer(text))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(text)
        body = text[m.start():end]
        body = "\n".join(l for l in body.splitlines() if not l.lstrip().startswith("#")).strip()
        out[m.group(2)] = body
    return out


def load_op(name: str, path: Path = QUERIES) -> str:
    """Operation text plus every fragment it spreads (transitively)."""
    blocks = _blocks(path.read_text(encoding="utf-8"))
    if name not in blocks:
        raise KeyError(f"operation {name!r} not in {path}")
    parts, seen, todo = [blocks[name]], set(), [blocks[name]]
    while todo:
        for frag in re.findall(r"\.\.\.\s*([A-Z]\w*)", todo.pop()):
            if frag not in seen and frag in blocks and blocks[frag].startswith("fragment"):
                seen.add(frag)
                parts.append(blocks[frag])
                todo.append(blocks[frag])
    return "\n\n".join(parts)


def fragment(name: str, path: Path = QUERIES) -> str:
    return _blocks(path.read_text(encoding="utf-8"))[name]


INTROSPECTION = """query IntrospectionQuery {
  __schema {
    queryType { name } mutationType { name }
    types {
      kind name description
      fields(includeDeprecated: true) {
        name description isDeprecated deprecationReason
        args { name description type { ...TypeRef } defaultValue }
        type { ...TypeRef }
      }
      inputFields { name description type { ...TypeRef } defaultValue }
      interfaces { ...TypeRef }
      enumValues(includeDeprecated: true) { name description isDeprecated deprecationReason }
      possibleTypes { ...TypeRef }
    }
  }
}
fragment TypeRef on __Type {
  kind name
  ofType { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } }
}"""


# ---------------------------------------------------------------------------------------------------------------
# client

def credentials() -> tuple[dict, list[str]]:
    """({BUFFER_API_KEY, BUFFER_API_URL, BUFFER_ORG_ID, BUFFER_CHANNEL_*...} that are set, [missing required])."""
    allv = cenv.load_env()
    keys = ["BUFFER_API_KEY", "BUFFER_API_URL", "BUFFER_ORG_ID", "BUFFER_CHANNEL_YOUTUBE", "BUFFER_CHANNEL_TIKTOK",
            "BUFFER_CHANNEL_INSTAGRAM", "BUFFER_YT_CATEGORY_ID", "PUBLIC_HOST_MODE", "PUBLIC_BASE_URL",
            "PUBLIC_MEDIA_DIR", "CLOUDFLARED_BIN"]
    vals = {k: allv[k] for k in keys if allv.get(k)}
    missing = [] if vals.get("BUFFER_API_KEY") else ["BUFFER_API_KEY"]
    return vals, missing


class BufferClient:
    def __init__(self, api_key: str | None, url: str | None = None, dry_run: bool = False, out=None,
                 timeout_s: float = 60, sleep=time.sleep):
        self.api_key = api_key
        self.url = url or DEFAULT_URL
        self.dry_run = dry_run or not api_key
        self.out = out or sys.stdout
        self.timeout_s = timeout_s
        self.sleep = sleep
        self.last_ratelimit: list[str] = []

    # -- request building (also what dry-run prints) --
    def build(self, query: str, variables: dict | None = None, op_name: str | None = None) -> dict:
        body: dict = {"query": query}
        if variables:
            body["variables"] = variables
        if op_name:
            body["operationName"] = op_name
        return {"method": "POST", "url": self.url,
                "headers": {"Content-Type": "application/json", "Authorization": "Bearer ***",
                            "User-Agent": USER_AGENT},
                "body": body}

    def print_request(self, req: dict, label: str = "") -> None:
        print(f"DRY-RUN request{(' ' + label) if label else ''}: {req['method']} {req['url']}", file=self.out)
        for k, v in req["headers"].items():
            print(f"  {k}: {v}", file=self.out)
        print("  body.query:", file=self.out)
        for line in req["body"]["query"].splitlines():
            print("    " + line, file=self.out)
        if "variables" in req["body"]:
            print("  body.variables:", file=self.out)
            for line in json.dumps(req["body"]["variables"], indent=2, ensure_ascii=False).splitlines():
                print("    " + line, file=self.out)

    # -- transport --
    def request(self, query: str, variables: dict | None = None, op_name: str | None = None,
                mutation: bool = False, label: str = "") -> dict | None:
        req = self.build(query, variables, op_name)
        if self.dry_run:
            self.print_request(req, label)
            return None
        data = json.dumps(req["body"]).encode("utf-8")
        headers = dict(req["headers"], Authorization=f"Bearer {self.api_key}")
        for attempt in range(1, MAX_TRIES + 1):
            hreq = urllib.request.Request(self.url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(hreq, timeout=self.timeout_s) as r:
                    self.last_ratelimit = r.headers.get_all("RateLimit") or []
                    payload = json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", "replace")[:2000]
                if e.code in (401, 403):
                    raise DependencyDown(f"Buffer HTTP {e.code}: {cenv.redact(body)}")
                if e.code == 429:
                    wait = _retry_after(e.headers, attempt)
                    if attempt < MAX_TRIES and wait <= 900:
                        self.sleep(wait)
                        continue
                    raise BufferError(f"Buffer rate limit (429), retry-after {wait}s: {cenv.redact(body)}")
                if e.code >= 500:
                    if mutation:
                        raise Ambiguous(f"Buffer HTTP {e.code} on a mutation: {cenv.redact(body)}")
                    if attempt < MAX_TRIES:
                        self.sleep(_backoff(attempt))
                        continue
                    raise Unavailable(f"Buffer HTTP {e.code} after {attempt} tries")
                raise BufferError(f"Buffer HTTP {e.code}: {cenv.redact(body)}")
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
                # refused / DNS failure: the request never reached Buffer, so even a mutation is safe to retry
                not_sent = isinstance(getattr(e, "reason", e), (ConnectionRefusedError, socket.gaierror))
                if mutation and not not_sent:
                    raise Ambiguous(f"Buffer request failed after send: {cenv.redact(str(e))}")
                if attempt < MAX_TRIES:
                    self.sleep(_backoff(attempt))
                    continue
                raise Unavailable(f"Buffer unreachable: {cenv.redact(str(e))}")
            errs = payload.get("errors") or []
            if errs:
                code = ((errs[0].get("extensions") or {}).get("code") or "").upper()
                msg = cenv.redact(errs[0].get("message", ""))
                if code in ("UNAUTHORIZED", "FORBIDDEN"):
                    raise DependencyDown(f"Buffer {code}: {msg}")
                if code == "NOT_FOUND":
                    raise NotFound(msg)
                if code in ("RATE_LIMIT_EXCEEDED", "UNEXPECTED") and attempt < MAX_TRIES and not (
                        mutation and code == "UNEXPECTED"):
                    self.sleep(_backoff(attempt))
                    continue
                if mutation and code == "UNEXPECTED":
                    raise Ambiguous(f"Buffer UNEXPECTED on a mutation: {msg}")
                if payload.get("data") is None:
                    raise BufferError(f"Buffer {code or 'error'}: {msg}")
            return payload.get("data") or {}
        raise BufferError("unreachable")

    # -- operations --
    def organizations(self) -> list[dict] | None:
        d = self.request(load_op("Organizations"), op_name="Organizations", label="Organizations")
        return None if d is None else d["account"]["organizations"]

    def channels(self, org_id: str) -> list[dict] | None:
        d = self.request(load_op("Channels"), {"organizationId": org_id}, "Channels", label="Channels")
        return None if d is None else d["channels"]

    def create_post(self, input_: dict, label: str = "") -> dict | None:
        d = self.request(load_op("CreatePost"), {"input": input_}, "CreatePost", mutation=True, label=label)
        if d is None:
            return None
        res = d.get("createPost") or {}
        if res.get("post"):
            return res["post"]
        raise MutationFailed(f"{res.get('__typename', 'MutationError')}: {cenv.redact(res.get('message', '?'))}")

    def post(self, post_id: str) -> dict | None:
        d = self.request(load_op("Post"), {"id": post_id}, "Post", label=f"Post {post_id}")
        return None if d is None else d.get("post")

    def posts_by_ids(self, ids: list[str]) -> dict[str, dict | None] | None:
        """One request for many posts (GraphQL aliases). Missing/deleted posts map to None."""
        if not ids:
            return {}
        decl = ", ".join(f"$id{i}: PostId!" for i in range(len(ids)))
        sel = "\n".join(f"  p{i}: post(input: {{ id: $id{i} }}) {{ ...PostFields }}" for i in range(len(ids)))
        q = f"query PostStatus({decl}) {{\n{sel}\n}}\n\n{fragment('PostFields')}"
        try:
            d = self.request(q, {f"id{i}": v for i, v in enumerate(ids)}, "PostStatus", label="PostStatus")
        except NotFound:
            # one bad id fails the batch: fall back to one request per id
            out = {}
            for pid in ids:
                try:
                    out[pid] = self.post(pid)
                except NotFound:
                    out[pid] = None
            return out
        if d is None:
            return None
        return {pid: d.get(f"p{i}") for i, pid in enumerate(ids)}

    def recent_channel_posts(self, org_id: str, channel_id: str, since_iso: str) -> list[dict] | None:
        d = self.request(load_op("RecentChannelPosts"),
                         {"organizationId": org_id, "channelId": channel_id, "since": since_iso},
                         "RecentChannelPosts", label="RecentChannelPosts")
        if d is None:
            return None
        return [e["node"] for e in ((d.get("posts") or {}).get("edges") or [])]

    def resolve_org(self, org_id: str | None) -> str | None:
        if org_id:
            return org_id
        orgs = self.organizations()
        if orgs is None:
            return None
        if not orgs:
            raise BufferError("the API key sees no organizations")
        return orgs[0]["id"]


def _backoff(attempt: int) -> float:
    return min(60.0, 2 ** attempt) + random.uniform(0, 0.5)


def _retry_after(headers, attempt: int) -> float:
    try:
        return float(headers.get("Retry-After")) + random.uniform(0, 1)
    except (TypeError, ValueError):
        return _backoff(attempt)


def client_from_env(force_dry_run: bool = False, out=None) -> tuple[BufferClient, dict, list[str]]:
    vals, missing = credentials()
    dry = force_dry_run or bool(missing)
    if missing and not force_dry_run:
        print(cenv.dry_run_notice(missing), file=out or sys.stdout)
    c = BufferClient(vals.get("BUFFER_API_KEY"), vals.get("BUFFER_API_URL"), dry_run=dry, out=out)
    return c, vals, missing


# ---------------------------------------------------------------------------------------------------------------
# CLI

PLATFORM_SERVICE = {"youtube": "youtube", "tiktok": "tiktok", "instagram": "instagram"}


def cmd_channels(a) -> int:
    c, vals, _ = client_from_env(a.dry_run)
    org = vals.get("BUFFER_ORG_ID")
    if c.dry_run:
        c.organizations()
        c.channels(org or "<BUFFER_ORG_ID or the first organization id>")
        return EXIT_OK
    orgs = c.organizations() or []
    print("organizations:")
    for o in orgs:
        print(f"  {o['id']}  {o['name']}  channels={o.get('channelCount')}")
    targets = [org] if org else [o["id"] for o in orgs]
    for oid in targets:
        print(f"channels in {oid}:")
        for ch in c.channels(oid) or []:
            flags = [f for f in ("isDisconnected", "isLocked", "isQueuePaused") if ch.get(f)]
            print(f"  {ch['id']}  {ch['service']:<10} {ch.get('type', ''):<9} {ch['name']}"
                  f"{'  [' + ','.join(flags) + ']' if flags else ''}")
    print("Put the ids in ~/studio/.env as BUFFER_ORG_ID and BUFFER_CHANNEL_YOUTUBE / _TIKTOK / _INSTAGRAM.")
    return EXIT_OK


def cmd_introspect(a) -> int:
    c, _, _ = client_from_env(a.dry_run)
    d = c.request(INTROSPECTION, op_name="IntrospectionQuery", label="IntrospectionQuery")
    if d is None:
        return EXIT_OK
    out = paths.schema_file()
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = {"v": 1, "at": timeutil.iso(), "url": c.url, "schema": d.get("__schema")}
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    tmp.replace(out)
    print(f"saved {out} ({len((d.get('__schema') or {}).get('types') or [])} types)")
    problems = check_schema(doc["schema"])
    for p in problems:
        print("SCHEMA MISMATCH:", p)
    return EXIT_FAIL if problems else EXIT_OK


# fields this lane depends on: type -> fields (input or output)
EXPECTED = {
    "CreatePostInput": ["channelId", "text", "schedulingType", "mode", "dueAt", "saveToDraft", "assets", "metadata",
                        "aiAssisted"],
    "AssetInput": ["video"], "VideoAssetInput": ["url", "metadata"], "VideoMetadataInput": ["thumbnailOffset"],
    "PostInputMetaData": ["youtube", "instagram", "tiktok"],
    "YoutubePostMetadataInput": ["title", "categoryId", "privacy", "madeForKids", "isAiGenerated"],
    "InstagramPostMetadataInput": ["type", "shouldShareToFeed", "isAiGenerated"],
    "TikTokPostMetadataInput": ["isAiGenerated"],
    "Post": ["id", "status", "dueAt", "sentAt", "externalLink", "error", "assets", "metadata"],
    "PostStatus": ["draft", "needs_approval", "scheduled", "sending", "sent", "error"],
    "ShareMode": ["customScheduled", "addToQueue"],
}


def check_schema(schema: dict | None) -> list[str]:
    if not schema:
        return ["no __schema in response (introspection disabled?)"]
    types = {t["name"]: t for t in schema.get("types") or []}
    probs = []
    for tname, fields in EXPECTED.items():
        t = types.get(tname)
        if not t:
            probs.append(f"type {tname} missing")
            continue
        have = {f["name"] for f in (t.get("fields") or []) + (t.get("inputFields") or [])}
        have |= {e["name"] for e in (t.get("enumValues") or [])}
        for f in fields:
            if f not in have:
                probs.append(f"{tname}.{f} missing")
    return probs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.publish.buffer")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("channels", "introspect"):
        p = sub.add_parser(name)
        p.add_argument("--dry-run", action="store_true", help="print the request, send nothing")
    a = ap.parse_args(argv)
    try:
        return {"channels": cmd_channels, "introspect": cmd_introspect}[a.cmd](a)
    except BufferError as e:
        print(f"ERROR: {cenv.redact(str(e))}", file=sys.stderr)
        return e.exit_code


if __name__ == "__main__":
    sys.exit(main())
