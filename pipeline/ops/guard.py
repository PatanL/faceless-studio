#!/usr/bin/env python3
"""Claude Code PreToolUse guard for the operator session, plus the session settings it is installed by.

Stdlib only and self-contained: it runs as `python3 -I <abs path>/pipeline/ops/guard.py hook --approval drafts`
(no imports from the repo, so nothing on sys.path can shadow it). Hooks run in every permission mode, including
bypassPermissions, so this holds even if the human's own settings default to bypass.

  guard.py hook --approval drafts|auto [--app DIR]       # reads the hook JSON on stdin; exit 2 = block (reason on stderr)
  guard.py settings --approval drafts|auto --app DIR [--base allow.json] --out FILE
  guard.py check --approval drafts "<bash command>"      # test a command by hand; prints ALLOW or BLOCK: reason

Always blocked: the human's switches (operator_ctl.sh, state unpause, editing data/operator/config.json or
approval_mode), secrets (~/studio/.env, ~/studio/secrets), crontab, git push, permission bypass flags, direct calls to
Buffer's API, deleting ledgers, and file edits outside the operator's own outputs.
While APPROVAL_MODE is not `auto` (drafts): any `--mode auto`, any APPROVAL_MODE assignment, and any
pipeline.publish.post call that is not explicitly `--mode draft`, `--dry-run` or `--record-manual`.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import sys

ALWAYS = [
    (r"operator_ctl\.sh", "operator_ctl.sh is the human's switch"),
    (r"pipeline[./]ops[./]state(\.py)?\s+unpause", "only the human unpauses (scripts/operator_ctl.sh unpause)"),
    (r"(^|[\s/'\"=])\.env\b|studio/secrets|yt_token|client_secret", "secrets are read by code only, never by the operator"),
    (r"\bcrontab\b|install_operator_cron", "cron changes are a human step (scripts/install_operator_cron.sh)"),
    (r"operator_tmux\.sh\s+(start|resume|rotate|stop|attach)", "the session is started, rotated and stopped from outside (watchdog/human)"),
    (r"\bgit\s+push\b", "never push"),
    (r"dangerously-skip-permissions|bypassPermissions|--permission-mode", "permission settings are the human's"),
    (r"(api|graph)\.buffer(app)?\.com|buffer\.com/(graphql|1/)", "Buffer is reached only through pipeline.publish"),
    (r"\brm\b[^|;&]*\b(data/[\w./*-]*\.jsonl|data/operator|data/learned|data/killrule)", "ledgers and operator state are never deleted"),
    (r">\s*[\w./~-]*data/[\w./-]*\.jsonl\b(?!\.)", "ledgers are append-only through pipeline.common.jsonl (single writer per file)"),
    (r"(>|\btee\b|sed\s+-i|\bmv\b|\bcp\b|\brm\b|\bchmod\b)[^|;&]*data/operator/(config\.json|approval_mode|claude_settings\.json)",
     "the human owns config.json and the approval switch"),
    (r"(>|\btee\b|sed\s+-i|\bmv\b|\bcp\b|\brm\b|\bchmod\b)[^|;&]*pipeline/ops/guard\.py", "the guard is not editable from the session"),
]
DRAFTS = [
    (r"--mode[=\s]+auto\b", "APPROVAL_MODE=drafts: auto posting is off"),
    (r"\bAPPROVAL_MODE\s*=|export\s+APPROVAL_MODE|env\s+[^|;&]*APPROVAL_MODE", "APPROVAL_MODE is set by operator_tmux.sh only"),
    (r"disclosure_ok_auto", "disclosure switches are the human's"),
]
POST_RE = re.compile(r"pipeline[./]publish[./]post\b")
POST_OK_RE = re.compile(r"--mode[=\s]+draft\b|--dry-run\b|--record-manual\b")

# operator outputs it may write with Edit/Write (relative to the app dir; plus temp dirs)
WRITE_OK = [
    "episodes/op-*/review_notes.md", "out/op-*/qa/review.json", "out/op-*/qa/review_notes*.md",
    "data/operator/journal.md", "data/operator/HUMAN.md", "data/operator/notes/*",
    "data/learning/*.md", "data/inbox/tiktok/*.csv",
]
TMP_OK = ["/tmp/*", "/private/tmp/*", "/var/tmp/*"]
SECRET_READ = [re.compile(r"(^|/)\.env$"), re.compile(r"/studio/secrets/"), re.compile(r"yt_token|client_secret")]


def check_bash(cmd: str, approval: str) -> str | None:
    c = " ".join(cmd.split())
    for pat, why in ALWAYS:
        if re.search(pat, c):
            return why
    if approval != "auto":
        for pat, why in DRAFTS:
            if re.search(pat, c):
                return why
        if POST_RE.search(c) and not POST_OK_RE.search(c):
            return ("APPROVAL_MODE=drafts: call pipeline.publish.post only with --mode draft (or --dry-run); "
                    "normally publish jobs go through `python -m pipeline.ops.run start <job>`")
    return None


def check_write(path: str, app: str) -> str | None:
    if not path:
        return None
    p = os.path.abspath(os.path.expanduser(path))
    if any(fnmatch.fnmatch(p, g) for g in TMP_OK):
        return None
    app = os.path.abspath(os.path.expanduser(app))
    if p.startswith(app + os.sep):
        rel = os.path.relpath(p, app)
        if any(fnmatch.fnmatch(rel, g) for g in WRITE_OK):
            return None
        return (f"the operator writes only its own outputs ({', '.join(WRITE_OK)}); code, kits, prompts, docs, "
                f"config and ledgers are changed on the Mac or by the lane CLIs, not here: {rel}")
    return f"outside the app dir: {p}"


def check_read(path: str) -> str | None:
    p = os.path.abspath(os.path.expanduser(path or ""))
    if any(r.search(p) for r in SECRET_READ):
        return "secrets are read by code only, never by the operator"
    return None


def decide(event: dict, approval: str, app: str) -> str | None:
    tool = event.get("tool_name") or ""
    ti = event.get("tool_input") or {}
    if tool == "Bash":
        return check_bash(ti.get("command") or "", approval)
    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        return check_write(ti.get("file_path") or ti.get("notebook_path") or "", app)
    if tool in ("Read",):
        return check_read(ti.get("file_path") or "")
    if tool in ("Grep", "Glob"):
        return check_read(ti.get("path") or "") if ti.get("path") else None
    return None


def build_settings(approval: str, app: str, base: dict | None) -> dict:
    s = {k: v for k, v in (base or {}).items() if not k.startswith("_")}  # unknown keys can fail validation
    perms = dict(s.get("permissions") or {})
    deny = list(perms.get("deny") or [])
    for d in ["Bash(crontab:*)", "Bash(git push:*)", "Bash(scripts/operator_ctl.sh:*)", "Read(~/studio/.env)",
              "Read(~/studio/secrets/**)", "Edit(data/operator/config.json)", "Edit(data/operator/approval_mode)"]:
        if d not in deny:
            deny.append(d)
    if approval != "auto":
        for d in ["Bash(python -m pipeline.publish.post * --mode auto*)", "Bash(python3 -m pipeline.publish.post * --mode auto*)"]:
            if d not in deny:
                deny.append(d)
    perms["deny"] = deny
    perms.pop("defaultMode", None)  # the mode comes from operator_tmux.sh --permission-mode
    s["permissions"] = perms
    me = os.path.join(os.path.abspath(app), "pipeline", "ops", "guard.py")
    hook = {"type": "command", "command": f"python3 -I {me} hook --approval {approval} --app {os.path.abspath(app)}",
            "timeout": 10}
    hooks = dict(s.get("hooks") or {})
    pre = [h for h in (hooks.get("PreToolUse") or []) if "pipeline/ops/guard.py" not in json.dumps(h)]
    pre.append({"matcher": "Bash|Edit|Write|MultiEdit|NotebookEdit|Read|Grep|Glob", "hooks": [hook]})
    hooks["PreToolUse"] = pre
    s["hooks"] = hooks
    s["env"] = {**(s.get("env") or {}), "STUDIO_LOCAL": "1", "TZ": "America/Chicago", "CUDA_VISIBLE_DEVICES": "",
                "APPROVAL_MODE": approval}
    return s


def _arg(argv, name, default=None):
    return argv[argv.index(name) + 1] if name in argv and argv.index(name) + 1 < len(argv) else default


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd = argv[0]
    approval = (_arg(argv, "--approval", "drafts") or "drafts").lower()
    approval = "auto" if approval == "auto" else "drafts"
    app = _arg(argv, "--app", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    if cmd == "hook":
        try:
            event = json.load(sys.stdin)
        except (json.JSONDecodeError, ValueError):
            print("guard: unreadable hook input; blocking to be safe", file=sys.stderr)
            return 2
        why = decide(event, approval, app)
        if why:
            print(f"BLOCKED by operator guard: {why}. See OPERATOR.md section 1 (limits).", file=sys.stderr)
            return 2
        return 0
    if cmd == "check":
        why = check_bash(argv[-1], approval)
        print(f"BLOCK: {why}" if why else "ALLOW")
        return 1 if why else 0
    if cmd == "settings":
        base = None
        bp = _arg(argv, "--base")
        if bp and os.path.exists(os.path.expanduser(bp)):
            with open(os.path.expanduser(bp), encoding="utf-8") as f:
                base = json.load(f)
        out = _arg(argv, "--out")
        s = build_settings(approval, app, base)
        txt = json.dumps(s, indent=1)
        if out:
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            with open(out, "w", encoding="utf-8") as f:
                f.write(txt + "\n")
            print(out)
        else:
            print(txt)
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
