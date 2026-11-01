"""Tiny stdlib HTTP client for the analytics APIs: JSON GET/POST, retries on 429/5xx (max 4 tries, exponential
backoff), no retries on other 4xx, 401/403 -> DependencyError (CLIs exit 5); network errors after the retries ->
TransientError (CLIs exit 1, never a pause); 429/5xx after the retries -> ApiError (exit 1). Secrets never reach logs (redact)."""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request

from ._common import DependencyError, TransientError, redact


class ApiError(RuntimeError):
    def __init__(self, status: int, body: str):
        super().__init__(f"HTTP {status}: {redact(body)[:400]}")
        self.status, self.body = status, body


def request(method: str, url: str, params: dict | None = None, headers: dict | None = None, data: dict | None = None,
            form: bool = False, tries: int = 4, timeout: int = 30) -> dict:
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    body = None
    hdrs = {"Accept": "application/json", **(headers or {})}
    if data is not None:
        if form:
            body = urllib.parse.urlencode(data).encode()
            hdrs["Content-Type"] = "application/x-www-form-urlencoded"
        else:
            body = json.dumps(data).encode()
            hdrs["Content-Type"] = "application/json"
    delay = 2.0
    for attempt in range(1, tries + 1):
        req = urllib.request.Request(url, data=body, method=method, headers=hdrs)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                txt = r.read().decode("utf-8")
                return json.loads(txt) if txt.strip() else {}
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "replace")
            if e.code in (401, 403):
                raise DependencyError(f"HTTP {e.code} from {urllib.parse.urlsplit(url).netloc}: {redact(txt)[:300]}")
            if e.code == 429 or e.code >= 500:
                if attempt < tries:
                    time.sleep(delay)
                    delay *= 2
                    continue
            raise ApiError(e.code, txt)
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < tries:
                time.sleep(delay)
                delay *= 2
                continue
            raise TransientError(f"network: {redact(str(e))}")
    raise TransientError("unreachable")
