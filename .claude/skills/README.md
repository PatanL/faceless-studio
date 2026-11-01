# Project-scoped agent skills

## Remotion official skills (installed 2026-11-01)

- Source: https://github.com/remotion-dev/skills at commit `30d4553ecd46fbc5212fd0ff006ae43af522158b` (2026-10-26). Skill version 4.0.539, the same as our pinned `remotion`. The repo mirrors `packages/skills` in remotion-dev/remotion. remotion.dev/docs/ai/skills documents it.
- Documented install: `npx skills add remotion-dev/skills`. The `skills` CLI is vercel-labs/skills 1.7.4. It installs to the project by default and sends telemetry unless `DISABLE_TELEMETRY=1` is set.
- How we installed: we cloned the repo at that commit into `experiments/vendor/remotion-skills/` and copied the skill folders here unmodified (`diff -r` is clean). That is the same result the CLI gives, without running the CLI on the Mac: BRIEF puts npm installs on the Spark, and the CLI also sends telemetry.
- Installed: `remotion-markup`, `remotion-captions`, `remotion-render`, `remotion-docs`, `remotion-multimedia`.
- Not installed, because each one tells agents to do something BRIEF.md forbids or this pipeline does not use:
  - `remotion-best-practices` and `remotion-studio`: "start Studio and open the preview in the browser" (BRIEF bans Chrome and renders on the Mac).
  - `remotion-upgrade`: upgrades the pinned 4.0.539.
  - `remotion-create`: `npx create-video` scaffolds a new project.
  - `remotion-saas`, `remotion-interactivity`, `remotion-maps` (standalone; markup still nests its copy): out of scope.
  The full set stays in `experiments/vendor/remotion-skills/skills/` for reading.
- BRIEF.md wins over these skills:
  - Render on the Spark only (`scripts/spark_render.sh`, `nice -n 10`, concurrency ≤ 4, swangle, CPU).
  - Never open Studio on the Mac. `remotion-captions` ends with "open the Remotion Studio, unless instructed otherwise", and BRIEF instructs otherwise.
  - Don't run `npx remotion add` or upgrade inside `studio/`. It is the operator's live pipeline. Add packages in an experiment folder first.
- To update: `git -C experiments/vendor/remotion-skills pull`, re-copy the same five folders, and bump the commit above.
