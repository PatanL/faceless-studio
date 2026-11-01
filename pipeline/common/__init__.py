"""Shared helpers for every operator lane (owned by L5; see docs/OPERATOR_DESIGN.md section 4.4).

Stdlib only, so any lane (and any python, venv or system) can import it:

    from pipeline.common import jsonl, env, timeutil, locks
"""
