# tests/

Regression tests for the code-review findings in `research/CODE_REVIEW_FINDINGS.md` (ids F01-F29).
Nothing here renders, runs TTS, uses the network or touches the Spark GPU. The shell-script tests put
stub `ssh`/`rsync` binaries first on `PATH`, so they only record arguments and never connect.

Each confirmed bug has a test marked as an **expected failure**: `@unittest.expectedFailure` in Python
(pytest reports it as `xfail`) and the `xfail()` wrapper in `core_ts.test.mjs`. The wrapper is strict: if the
bug gets fixed, the test reports `XPASS` / "unexpected success". When that happens, remove the marker so
the test guards the fix. Tests whose names have no `F` id are plain regression guards that pass today.

| File | Covers | Needs |
|---|---|---|
| `test_audio_script.py` | F09-F13 (`pipeline/audio/script.py` markers, front matter) | python3 only |
| `test_auto_resolve.py` | F05 anchor resolution, F03 write-before-zod (static order check) | python3 only |
| `test_make.py` | F01, F02, F04, F06 (`pipeline/make.py` steps, ssh/claude stubbed) | python3 only |
| `test_originality.py` | F22-F24 (runs `scripts/originality_check.py` on temp files) | python3 only |
| `test_reformat_camera.py` | F16 (`reformat.camera16`) | python3 only |
| `test_spark_scripts.py` | F07, F08/F27, F25, F26, F28, F29 (`spark_sync.sh`, `spark_render.sh`) | bash |
| `test_mix.py` | F14, F15 (`pipeline/audio/mix.py`) | numpy, scipy, soundfile, pyloudnorm: skipped on the Mac, runs in the Spark venv |
| `core_ts.test.mjs` | F17-F21 (`studio/src/core` captions pager, `sceneTimings`, `SvgMarkup`) | Node >= 23.2 (`module.stripTypeScriptTypes`), no `node_modules` |

`core_ts.test.mjs` slices the JSX-free functions out of the current `.ts`/`.tsx` sources, strips the types and
evaluates them, so it always tests the live code. F19 and the informational F21 check read the real
`episodes/horror-elevator-maintenance` and `episodes/explainer-orca` storyboards.

## Run on the Mac (light: about 2 s, no installs)

```bash
cd ~/Documents/faceless-studio
python3 -m unittest discover -s tests -p 'test_*.py'          # or: python3 -m pytest tests  (if pytest is installed)
node --test tests/core_ts.test.mjs                              # XFAIL_VERBOSE=1 prints why each xfail fails
```

## Run on the Spark (adds the two mix tests)

Use the venv's python. Prefer a scratch copy so you don't need a full `spark_sync.sh` (see F07/F26):

```bash
ssh dgx-spark 'mkdir -p /tmp/crtests/tests && ln -sfn ~/studio/app/pipeline /tmp/crtests/pipeline'
for f in _util.py test_mix.py; do ssh dgx-spark "cat > /tmp/crtests/tests/$f" < tests/$f; done
ssh dgx-spark 'cd /tmp/crtests && CUDA_VISIBLE_DEVICES="" OMP_NUM_THREADS=2 nice -n 10 \
  ~/studio/.venv/bin/python -m unittest discover -s tests -p "test_mix.py" -v; rm -rf /tmp/crtests'
```

After a normal sync, the whole suite also runs in place:
`cd ~/studio/app && ~/studio/.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`, plus
`node --test tests/core_ts.test.mjs` (with nvm node 22.7+ add `--experimental-strip-types`; node 22 may not export
`stripTypeScriptTypes`, so run the node file on the Mac if it errors).

Expected result today: Python `OK (expected failures=26, skipped=2)` on the Mac (the 2 skipped are mix);
node `pass 8, fail 0` (6 of them are xfails); Spark mix `expected failures=2`.
