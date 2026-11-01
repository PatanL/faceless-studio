# Test 2 setup: cc-blender-skill + mcp-for-blender on Blender 4.3.2 (Mac)

Goal of test 2: build one Zack-style rigid-object shot (a castle gate mechanism, the lane `research/corpus/zackd/PLAYBOOK.md` §"how old things actually worked" recommends) in Blender and score it against the 2D prototype (41/100, `experiments/zackd-proto/NOTES.md` line 166). This file covers only the setup: what runs, what doesn't, and which path the build should take.

Machine: Mac, `/Applications/Blender.app` = **Blender 4.3.2** (built 2024-12-17), GPU backend **Metal**. There's about 16 GB RAM and swap was already ~10.9 GB used during setup, so keep renders small and run one Blender at a time. No other Blender process was running before or after these tests.

## Commits used (pinned)

| Repo | Commit | Notes |
|---|---|---|
| https://github.com/RobLe3/cc-blender-skill | `a2634b588e80265e796aa53f8ab178d75105c2af` (2026-10-12, v1.4.0) | 30 SKILL.md skills + small helper scripts |
| https://github.com/ahujasid/mcp-for-blender | `992233bb258975a05eec8b5691465c50c2831e34` (2026-10-29, package 2.2.6, addon 1.8, protocol 15) | Blender addon (`addon.py`) + stdio MCP server |

`vendor/` is git-ignored because it contains two nested git repos and about 30 MB of images. To recreate it at these exact commits, run `tools/fetch_vendor.sh`.

## What I read before running anything

- **cc-blender-skill.** It's almost all Markdown: `plugin/skills/*/SKILL.md` plus references. It has no installer and no addon. The Python helpers under `plugin/skills/*/scripts/` and `tests/` are image analysis and recipe runners, with no network calls and no shell-outs except one `subprocess` call in a host-side test. Recipe code is plain `bpy`. One thing to watch: `blender-rendering` Recipe 8 writes Cycles GPU preferences, so don't run it outside `--factory-startup`. Its README asks you to install the skills into `.claude/skills` and configure an MCP globally. **We do neither**, and agents read the SKILL.md files straight from `vendor/`.
- **mcp-for-blender.**
  - `install.sh` / `uvx mcp-for-blender setup` edit every MCP client config they find (Claude Code's included) and copy the addon into Blender's user addon folder. **Not used.**
  - On register, the addon schedules a GitHub fetch of the latest `addon.py` after 5 s. It only checks; installing needs a button click. Turn the check off with `BLENDERMCP_NO_UPDATE_CHECK=1`.
  - The server sends telemetry to Supabase only with consent (default off). It's also hard-disabled with `DISABLE_TELEMETRY=true`, which `mcp-config.json` sets.
  - Asset and generation tools (Poly Haven, Sketchfab, Hyper3D, Tripo, Meshy, Hunyuan) need API keys and are off by default. **Don't enable them, and don't pass any keys.**
  - `execute_code` runs arbitrary Python in Blender. That's expected, but it means the bridge should only listen on 127.0.0.1, as configured here.

## Question 1: does cc-blender-skill work on Blender 4.3? Yes.

The skills target 5.1.1 and only claim "compat code present, not directly tested" for 4.x. I tested them on 4.3.2 without any MCP (`Blender -b --factory-startup`):

1. **The vendor's own 35-check recipe suite** (`tests/core_recipe_regressions.py`, run via `tools/run_core_suite.py`): **35/35 PASS** on 4.3.2. That covers modeling, materials, lighting, cameras, the EEVEE/Cycles presets, keyframes/F-curves/shape keys, glTF/FBX/OBJ export, decimation, and six small scene fixtures rendered in Cycles CPU. Results are in `compat/core-run1/core-tests.json`, with renders such as `compat/core-run1/sword.png`.
2. **A sweep of every `### Recipe` block** in modeling, materials, lighting, cameras, rendering, animation and pro-workflow (`tools/recipe_sweep.py`; renders stubbed): **52/57 PASS**. None of the 5 failures is a 4.3 API break (`compat/sweep/recipe_sweep.json`):
   - 4 are snippet context: a recipe expects objects it didn't create (`GEO-lamp_shade`, `GEO-leader`, `LGT-key`, `CAM-hero`).
   - `blender-rendering` Recipe 8 hard-codes `OPTIX`. On a Mac the only GPU device type is `METAL`. That's a platform issue, not a version issue.
3. **API probes on 4.3.2** (`tools/eevee_smoke.py`):
   - `BLENDER_EEVEE_NEXT` is the valid EEVEE engine name. The skills' try/except picks it correctly.
   - The disabled BSDF inputs are `Weight` and `Subsurface IOR`, the same as on 5.x, so the `set_input` helper is still needed.
   - `Action.layers` is absent, so the legacy `action.fcurves` path is used. The skills' `get_fcurves_compat` handles both.
   - On EEVEE Next, `use_bloom`, `use_ssr`, `use_ssr_refraction` and `use_volumetric_lights` are gone. The EEVEE preset skips them and logs them as unavailable. For bloom on 4.3, use a compositor Glare node (`glare_type='BLOOM'` exists in 4.3).

Version gotchas to keep in mind when following the skills on 4.3:
- The **5.x notes don't apply to 4.3**: `BLENDER_EEVEE` as the EEVEE name, `scene.compositing_node_group`, Glare options as input sockets, layered-action-only F-curves, `media_type='VIDEO'`. On 4.3:
  - the compositor is `scene.use_nodes = True` + `scene.node_tree`;
  - Glare uses `node.glare_type`;
  - EEVEE is `BLENDER_EEVEE_NEXT`;
  - FFMPEG output is `image_settings.file_format = 'FFMPEG'` directly.

  I verified these four on 4.3.2: `scene.compositing_node_group` is absent and `scene.render.engine = 'BLENDER_EEVEE'` raises TypeError.
- The failure table in `text-to-blender` says "`BLENDER_EEVEE_NEXT` rejected → use `BLENDER_EEVEE`". On 4.3 it's the reverse: `BLENDER_EEVEE` is the legacy name, which 4.2+ rejects.
- Swap OptiX/CUDA for METAL wherever a recipe selects a GPU device.

## Question 2: can mcp-for-blender's addon run headless? No. It needs the GUI.

- **Background fails by design.** `BlenderMCPServer.start()` returns early when `bpy.app.background` is true, and prints "cannot start server in background mode (blender -b) … run Blender with a GUI" (tested: `compat/bridge_bg.json`, `running: false`). Its suggested workaround is `xvfb-run`, which is Linux-only and doesn't apply to the Mac.
- **The GUI works, with no global config.**
  - `tools/mcp_bridge.py` loads the pinned `vendor/mcp-for-blender/addon.py` with importlib inside `Blender --factory-startup`. It isn't installed into Blender's user addons, and the update check is off.
  - The script starts the bridge on `127.0.0.1:9911`. Tested on 4.3.2: raw socket `get_scene_info` and `execute_code` both succeeded (`tools/raw_socket_probe.py`).
- **The MCP server works with a per-invocation config.**
  - The server runs from a project-local venv, built from the repo's `uv.lock`:
    ```
    UV_PROJECT_ENVIRONMENT=experiments/blender-castle/.mcp-venv uv sync --frozen --no-dev --project vendor/mcp-for-blender
    ```
    That's 27 MB, and the folder is git-ignored.
  - `mcp-config.json` points at it with telemetry disabled. An MCP SDK stdio client (`tools/mcp_stdio_probe.py`, using exactly that command and env) listed 9 tools: `get_addon_status`, `disable_telemetry`, `get_scene_info`, `execute_blender_code`, `record_trajectory_feedback`, `look`, `generate_3d`, `search_assets`, `import_asset`.
  - `execute_blender_code` and `get_scene_info` succeeded. `look` (multi-angle material-preview capture) returned an image: `compat/mcp_look_angles.png`.
  - To use it from Claude Code without touching global config:
    ```
    claude --mcp-config experiments/blender-castle/mcp-config.json --strict-mcp-config
    ```
    I did not launch a nested `claude` session itself. The server/command/env path it would spawn is the one tested above.
  - Afterwards: no MCP entry in `~/.claude.json` or `~/.claude/settings.json`, no `blender_mcp` in Blender 4.3's user addons, and `userpref.blend` was unchanged (still dated Jan 2025).
- **Costs of the MCP path on this Mac:**
  - a Blender GUI window opens on the owner's screen, which they need for other Blender work;
  - it uses extra RAM on a machine that is already swapping;
  - a subagent can't attach an MCP server mid-session, so it would have to spawn a nested `claude -p --mcp-config …` process;
  - the scene lives inside the GUI session instead of in a script that can be committed and re-run.

## Chosen path: direct bpy in background Blender, following the skills, with frequent preview renders

The skills' know-how is plain `bpy` recipes plus process rules: real-world dimension lookup, world reset, assembly order, naming, and the render-and-look checkpoint. None of it depends on the MCP transport, and the recipes run on 4.3 as shown above. So:

1. **Scene as code.** Build `experiments/blender-castle/build_scene.py`, run with `Blender -b --factory-startup --python build_scene.py -- <args>`. Each run rebuilds the whole shot from nothing, so it is reproducible and can be committed. Follow `text-to-blender`'s order: block-out → camera lock → light v1 → geometry → materials → light v2 → detail → final render. Use `GEO-/MAT-/LGT-/CAM-` names and the world reset. Read the relevant SKILL.md files from `vendor/cc-blender-skill/plugin/skills/` before each phase: modeling, materials (stone, wood, iron), lighting, cameras, animation (gate, chain, counterweight keyframes), rendering. Also read `blender-pro-workflow` and `animation-quality-gate` (contact-sheet QA).
2. **Render-feedback loop.** Headless EEVEE renders on Metal: a 540×960, 32-sample frame took **3.9 s** (`tools/eevee_smoke.py`, near-empty scene). After each phase:
   - render 3–6 preview stills through the camera at about 540×960 with 16–32 samples, plus a few angle views like the MCP `look` tool's;
   - for motion, render a contact sheet of about 8 frames;
   - Read the PNGs before moving on.

   Final frames are EEVEE at 1080×1920. Use Cycles only for a hero still if it's needed, and keep it short. That serves the same purpose as MCP's `look` and `render`, without a GUI.
3. **Hygiene.**
   - Always pass `--factory-startup`, so user prefs aren't touched.
   - Run under `nice -n 10`, with one Blender process at a time, and check `pgrep -fl Blender.app` first.
   - Write outputs under `experiments/blender-castle/out/` and keep that folder small.
   - Don't use asset downloads. Everything is modeled in code, per BRIEF rule 4 and the "code-rendered" lane.
4. **MCP as a verified fallback only.** If an interactive session is ever worth it (for example to poke at a tricky rig with `look` angles), launch it like this, then close the Blender window afterwards:
   ```
   BLENDERMCP_NO_UPDATE_CHECK=1 Blender --factory-startup --python tools/mcp_bridge.py -- vendor/mcp-for-blender/addon.py 9911 compat/bridge_gui.json
   ```
   Then `claude --mcp-config experiments/blender-castle/mcp-config.json --strict-mcp-config`. Port 9911 is set in both files, so it won't collide with an owner-side addon on the default port 9876.

## Files

- `tools/fetch_vendor.sh`: re-clones `vendor/` at the pinned commits.
- `tools/run_core_suite.py`: runs the vendor's 35-check suite inside background Blender.
- `tools/recipe_sweep.py`: execs every domain recipe on a fresh scene.
- `tools/eevee_smoke.py`: 4.3 API probes, plus headless EEVEE timing and the GPU backend.
- `tools/mcp_bridge.py`: starts the pinned addon's bridge in a GUI Blender without installing it.
- `tools/raw_socket_probe.py`, `tools/mcp_stdio_probe.py`, `tools/mcp_look_probe.py`: bridge and MCP checks.
- `mcp-config.json`: per-invocation MCP config. It uses absolute paths to `.mcp-venv`, so recreate that venv first with the `uv sync` command above.
- `compat/`: evidence (JSON results, logs, small PNGs).
