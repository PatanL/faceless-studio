"""Where the operator's files live. Override the data root with STUDIO_DATA (tests) and logs with OPERATOR_LOG_DIR."""
from __future__ import annotations

import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def data_dir() -> str:
    return os.path.abspath(os.environ.get("STUDIO_DATA") or os.path.join(ROOT, "data"))


def ops_dir() -> str:
    return os.path.join(data_dir(), "operator")


def state_file() -> str:
    return os.path.join(ops_dir(), "state.json")


def config_file() -> str:
    return os.path.join(ops_dir(), "config.json")


def default_config_file() -> str:
    return os.path.join(ROOT, "pipeline", "ops", "config.default.json")


def journal_file() -> str:
    return os.path.join(ops_dir(), "journal.md")


def human_file() -> str:
    return os.path.join(ops_dir(), "HUMAN.md")


def stopped_flag() -> str:
    """Present after `operator_tmux.sh stop`: the watchdog does not resurrect a deliberately stopped operator."""
    return os.path.join(ops_dir(), "STOPPED")


def approval_file() -> str:
    """Written by operator_tmux.sh at session start (drafts|auto); the most restrictive of it and $APPROVAL_MODE wins."""
    return os.path.join(ops_dir(), "approval_mode")


def ledger(name: str) -> str:
    return os.path.join(data_dir(), name)


def episodes_dir() -> str:
    return os.path.abspath(os.environ.get("STUDIO_EPISODES") or os.path.join(ROOT, "episodes"))


def out_dir() -> str:
    return os.path.abspath(os.environ.get("STUDIO_OUT") or os.path.join(ROOT, "out"))


def log_dir() -> str:
    d = os.environ.get("OPERATOR_LOG_DIR")
    if not d:
        studio = os.path.expanduser("~/studio")
        d = os.path.join(studio, "logs", "operator") if os.path.isdir(studio) else os.path.join(ops_dir(), "logs")
    os.makedirs(d, exist_ok=True)
    return d
