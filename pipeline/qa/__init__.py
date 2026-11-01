"""L2: deterministic QA gate, sameness check and review sheets (docs/OPERATOR_DESIGN.md section 7).

Entry points:
  python -m pipeline.qa.gate <slug>          all checks -> out/<slug>/qa/gate.json (exit 0 PASS, 6 FAIL, 1 error)
  python -m pipeline.qa.fingerprint <slug>   rebuild out/<slug>/qa/fingerprint.json
  python -m pipeline.qa.sameness <slug>      sameness check only (prints JSON)
  python -m pipeline.qa.sheet <slug>         out/<slug>/qa/{sbs,stills}.jpg only
  python -m pipeline.qa.selftest --root DIR  proof run: pilots PASS, near-duplicate FAILs sameness
"""
