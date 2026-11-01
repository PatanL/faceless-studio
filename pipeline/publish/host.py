"""Public URL for one MP4 so Buffer can fetch it (docs/OPERATOR_DESIGN.md 8.4; Buffer has no upload endpoint).

    with hosted(mp4_path, ttl_s=1800) as h:     # h.url = https://<random>.trycloudflare.com/<32-hex>/<slug>.mp4
        ...create posts..., then hold until Buffer has the media (see BUFFER_NOTES.md: Buffer fetches the media
        again when the post goes out, so an ephemeral URL must stay up until every post is sent)

Modes (PUBLIC_HOST_MODE in ~/studio/.env):
  cloudflared (default)  127.0.0.1 server for exactly one file at an unguessable path + a cloudflared quick tunnel
                         (no account). Torn down on exit, including on exceptions, and after ttl_s at the latest.
  static                 copy to PUBLIC_MEDIA_DIR/<token>/<name> and return PUBLIC_BASE_URL/<token>/<name>; the human
                         maps PUBLIC_BASE_URL to that directory (e.g. a named tunnel to `host serve`). The file stays
                         until status.py prunes it after every post using it is terminal.

CLI:
  python -m pipeline.publish.host selftest [--file F]   # acceptance: real quick tunnel, HEAD 200, then unreachable
  python -m pipeline.publish.host serve --dir D --port P  # static-mode file server (token paths only)
"""
from __future__ import annotations

import argparse
import contextlib
import http.server
import os
import re
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from pipeline.common import env as cenv
from pipeline.common import timeutil

TUNNEL_RE = re.compile(r"https://[a-z0-9-]+\.trycloudflare\.com")
TOKEN_PATH_RE = re.compile(r"^/([0-9a-f]{32})/([A-Za-z0-9._-]+\.(?:mp4|jpg|png))$")
CHUNK = 1 << 16


class HostError(Exception):
    exit_code = 5  # dependency unavailable (tunnel failed)


@dataclass
class Hosted:
    mode: str
    url: str
    token: str
    name: str
    opened_at: str
    closed_at: str | None = None
    port: int | None = None
    log: str | None = None
    extra: dict = field(default_factory=dict)

    def record(self) -> dict:
        """What the ledger may keep: never the URL or the token."""
        return {"mode": self.mode, "opened_at": self.opened_at, "closed_at": self.closed_at}


# ---------------------------------------------------------------------------------------------------------------
# local file server: GET/HEAD only, Range support, 404 for anything but the token path(s)

def _make_handler(resolve):
    class H(http.server.BaseHTTPRequestHandler):
        server_version = "studio-media/1"
        sys_version = ""

        def log_message(self, fmt, *args):  # quiet; never log paths (they carry the token)
            pass

        def _target(self):
            path = self.path.split("?", 1)[0]
            return resolve(path)

        def do_HEAD(self):
            self._serve(head=True)

        def do_GET(self):
            self._serve(head=False)

        def _deny(self, code=404):
            self.send_response(code)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def _serve(self, head: bool):
            p = self._target()
            if not p or not p.is_file():
                return self._deny()
            size = p.stat().st_size
            start, end = 0, size - 1
            rng = self.headers.get("Range")
            status = 200
            if rng:
                m = re.match(r"bytes=(\d*)-(\d*)$", rng.strip())
                if not m or (not m.group(1) and not m.group(2)):
                    return self._deny(416)
                if m.group(1):
                    start = int(m.group(1))
                    end = int(m.group(2)) if m.group(2) else size - 1
                else:
                    start = max(0, size - int(m.group(2)))
                end = min(end, size - 1)
                if start > end:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                status = 206
            self.send_response(status)
            ctype = {"mp4": "video/mp4", "jpg": "image/jpeg", "png": "image/png"}.get(p.suffix[1:].lower(),
                                                                                     "application/octet-stream")
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1))
            if status == 206:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if head:
                return
            with open(p, "rb") as f:
                f.seek(start)
                left = end - start + 1
                while left > 0:
                    b = f.read(min(CHUNK, left))
                    if not b:
                        break
                    try:
                        self.wfile.write(b)
                    except (BrokenPipeError, ConnectionResetError):
                        return
                    left -= len(b)

        def _405(self):
            self._deny(405)

        do_POST = do_PUT = do_DELETE = do_PATCH = do_OPTIONS = _405
    return H


class LocalServer:
    def __init__(self, resolve, port: int = 0):
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), _make_handler(resolve))
        self.httpd.daemon_threads = True
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, kwargs={"poll_interval": 0.2}, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.httpd.server_close()


def one_file_resolver(token: str, name: str, path: Path):
    want = f"/{token}/{name}"
    return lambda p: path if secrets.compare_digest(p, want) else None


def dir_resolver(root: Path):
    root = root.resolve()

    def r(p):
        m = TOKEN_PATH_RE.match(p)
        if not m:
            return None
        f = (root / m.group(1) / m.group(2)).resolve()
        return f if f.parent.parent == root else None
    return r


# ---------------------------------------------------------------------------------------------------------------
# cloudflared quick tunnel

class Tunnel:
    def __init__(self, port: int, bin_path: str | None = None, log_dir: str | None = None, start_timeout_s=60):
        self.port = port
        self.bin = os.path.expanduser(bin_path or "~/.local/bin/cloudflared")
        fd, self.log = tempfile.mkstemp(prefix="cloudflared-", suffix=".log", dir=log_dir)
        os.close(fd)
        self.start_timeout_s = start_timeout_s
        self.proc: subprocess.Popen | None = None
        self.url: str | None = None

    def start(self) -> str:
        if not os.path.exists(self.bin):
            raise HostError(f"cloudflared not found at {self.bin} (set CLOUDFLARED_BIN)")
        logf = open(self.log, "ab")
        self.proc = subprocess.Popen(
            [self.bin, "tunnel", "--no-autoupdate", "--url", f"http://127.0.0.1:{self.port}"],
            stdout=logf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
        logf.close()
        deadline = time.monotonic() + self.start_timeout_s
        while time.monotonic() < deadline:
            if self.proc.poll() is not None:
                raise HostError(f"cloudflared exited {self.proc.returncode}; log {self.log}")
            m = TUNNEL_RE.search(Path(self.log).read_text(errors="replace"))
            if m:
                self.url = m.group(0)
                return self.url
            time.sleep(0.5)
        self.stop()
        raise HostError(f"no trycloudflare URL within {self.start_timeout_s}s; log {self.log}")

    def stop(self):
        if self.proc and self.proc.poll() is None:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(self.proc.pid, signal.SIGTERM)
            try:
                self.proc.wait(10)
            except subprocess.TimeoutExpired:
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(self.proc.pid, signal.SIGKILL)
                self.proc.wait(5)


def head(url: str, timeout_s: float = 15) -> tuple[int | None, dict]:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "studio-media-check/1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as r:
            return r.status, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {})
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return None, {"error": str(e)}


def wait_head_ok(url: str, size: int, timeout_s: float = 90) -> dict:
    deadline, last = time.monotonic() + timeout_s, None
    while time.monotonic() < deadline:
        code, h = head(url)
        last = (code, h.get("error") or h.get("Content-Length"))
        if code == 200 and str(h.get("Content-Length")) == str(size):
            return h
        time.sleep(2)
    raise HostError(f"public URL not serving the file after {timeout_s:.0f}s (last {last})")


# ---------------------------------------------------------------------------------------------------------------
# the context manager

def _settings() -> dict:
    e = cenv.load_env()
    return {"mode": (e.get("PUBLIC_HOST_MODE") or "cloudflared").strip().lower(),
            "base": e.get("PUBLIC_BASE_URL"), "media_dir": e.get("PUBLIC_MEDIA_DIR"),
            "bin": e.get("CLOUDFLARED_BIN")}


@contextlib.contextmanager
def hosted(path: str | Path, ttl_s: float = 1800, mode: str | None = None, dry_run: bool = False,
           name: str | None = None, verify: bool = True):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(path)
    s = _settings()
    mode = (mode or s["mode"]).lower()
    token = secrets.token_hex(16)
    name = name or path.name
    if dry_run:
        base = {"static": (s["base"] or "https://PUBLIC_BASE_URL").rstrip("/")}.get(mode,
                                                                                     "https://DRY-RUN.trycloudflare.com")
        h = Hosted(mode, f"{base}/{token}/{name}", token, name, timeutil.iso(), extra={"dry_run": True})
        try:
            yield h
        finally:
            h.closed_at = timeutil.iso()
        return
    size = path.stat().st_size
    if mode == "static":
        if not s["base"] or not s["media_dir"]:
            raise HostError("PUBLIC_HOST_MODE=static needs PUBLIC_BASE_URL and PUBLIC_MEDIA_DIR in ~/studio/.env")
        d = Path(os.path.expanduser(s["media_dir"])) / token
        d.mkdir(parents=True, exist_ok=False)
        dst = d / name
        try:
            os.link(path, dst)
        except OSError:
            shutil.copy2(path, dst)
        h = Hosted("static", f"{s['base'].rstrip('/')}/{token}/{name}", token, name, timeutil.iso())
        if verify:
            wait_head_ok(h.url, size)
        try:
            yield h
        finally:
            h.closed_at = timeutil.iso()  # the file stays: Buffer fetches again at publish time
        return
    if mode != "cloudflared":
        raise HostError(f"unknown PUBLIC_HOST_MODE {mode!r}")
    with LocalServer(one_file_resolver(token, name, path)) as srv:
        tun = Tunnel(srv.port, s["bin"])
        killer = threading.Timer(ttl_s, tun.stop)
        killer.daemon = True
        try:
            base = tun.start()
            killer.start()
            h = Hosted("cloudflared", f"{base}/{token}/{name}", token, name, timeutil.iso(), port=srv.port,
                       log=tun.log)
            if verify:
                wait_head_ok(h.url, size)
            yield h
        finally:
            killer.cancel()
            tun.stop()
            with contextlib.suppress(OSError):
                os.unlink(tun.log)
            if "h" in locals():
                h.closed_at = timeutil.iso()


def prune_static(slug_file: str, keep_tokens: set[str] | None = None) -> list[str]:
    """Remove PUBLIC_MEDIA_DIR/<token>/<slug_file> copies (called by status.py once every post is terminal)."""
    s = _settings()
    if not s["media_dir"]:
        return []
    root = Path(os.path.expanduser(s["media_dir"]))
    gone = []
    for f in root.glob(f"*/{slug_file}"):
        if keep_tokens and f.parent.name in keep_tokens:
            continue
        f.unlink()
        with contextlib.suppress(OSError):
            f.parent.rmdir()
        gone.append(f.parent.name[:6] + "...")
    return gone


# ---------------------------------------------------------------------------------------------------------------
# CLI

def cmd_selftest(a) -> int:
    tmpdir = None
    if a.file:
        f = Path(a.file)
    else:
        tmpdir = tempfile.mkdtemp(prefix="host-selftest-")
        f = Path(tmpdir) / "selftest.mp4"
        f.write_bytes(b"\x00\x00\x00\x18ftypmp42" + secrets.token_bytes(200_000))
    size = f.stat().st_size
    ok = True
    try:
        with hosted(f, ttl_s=300, mode="cloudflared") as h:
            host_only = h.url.split("/")[2]
            code, hd = head(h.url)
            print(f"HEAD via tunnel: {code} Content-Length={hd.get('Content-Length')} "
                  f"Content-Type={hd.get('Content-Type')} (file {size} bytes) host={host_only}")
            ok &= code == 200 and str(hd.get("Content-Length")) == str(size)
            req = urllib.request.Request(h.url, headers={"Range": "bytes=0-15", "User-Agent": "studio-media-check/1"})
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read()
                print(f"GET Range 0-15: {r.status} Content-Range={r.headers.get('Content-Range')} {len(body)} bytes")
                ok &= r.status == 206 and len(body) == 16
            wrong = f"https://{host_only}/{'0' * 32}/{h.name}"
            code2, _ = head(wrong)
            code3, _ = head(f"https://{host_only}/")
            print(f"HEAD wrong token: {code2}; HEAD /: {code3}")
            ok &= code2 == 404 and code3 == 404
            closed_url = h.url
        time.sleep(3)
        code4, hd4 = head(closed_url, timeout_s=10)
        print(f"HEAD after close: {code4 if code4 is not None else 'unreachable'} "
              f"{'' if code4 is not None else hd4.get('error', '')[:80]}")
        ok &= code4 != 200
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)
    print("SELFTEST", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def cmd_serve(a) -> int:
    root = Path(os.path.expanduser(a.dir))
    root.mkdir(parents=True, exist_ok=True)
    with LocalServer(dir_resolver(root), port=a.port) as srv:
        print(f"serving token paths under {root} on http://127.0.0.1:{srv.port} (GET/HEAD only)", flush=True)
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                time.sleep(3600)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m pipeline.publish.host")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("selftest")
    p.add_argument("--file")
    p = sub.add_parser("serve")
    p.add_argument("--dir", required=True)
    p.add_argument("--port", type=int, default=8787)
    a = ap.parse_args(argv)
    try:
        return {"selftest": cmd_selftest, "serve": cmd_serve}[a.cmd](a)
    except HostError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return e.exit_code


if __name__ == "__main__":
    sys.exit(main())
