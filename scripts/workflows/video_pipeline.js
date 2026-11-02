export const meta = {
  name: 'video-pipeline',
  description: 'One Short through specialist agents: research, script panel, direction, build, every-frame + specialist review, fix loop, caption',
  whenToUse: 'Making any new faceless-studio Short. args: {lane, slug, brief, refs}',
  phases: [
    { title: 'Research' }, { title: 'Script' }, { title: 'Direction' }, { title: 'Build' },
    { title: 'Review' }, { title: 'Fix' }, { title: 'Final' },
  ],
}

// args: {lane: 'kurz'|'zackd'|'story'|..., slug: 'explainer-xyz', brief: 'topic idea or "pick from sources"', refs: 'where the lane references live'}
const A = args || {}
const LANE = A.lane || 'kurz'
const SLUG = A.slug
const BRIEF = A.brief || 'pick the strongest proven viral source for this lane with pipeline.sources pick'
const REFS = A.refs || 'research/references/OWNER_REFERENCES.md and the lane corpus under research/corpus/'
const MAX_ROUNDS = A.rounds || 3

const COMMON = `Repo: /Users/patrickliu/Documents/faceless-studio. Read BRIEF.md, FEEDBACK.md, docs/HOUSE_STYLE.md (style A; the zackd lane uses the realistic variant at the end of it) and docs/FEEDBACK_LOG.md first.
Episode slug: ${SLUG}. Lane: ${LANE}. Lane references: ${REFS}.
Lane principles measured from reference outliers vs their channels' ordinary videos: research/library/LANE_PRINCIPLES.md (topic choice, hook, title); follow them unless the reference brief shows otherwise.
Rules: never publish or schedule anything. Renders, TTS and heavy ffmpeg go through the render dispatcher (scripts/render.sh if present, else scripts/spark_render.sh): Spark CPU only (never its GPU), nice, concurrency 2; the Mac is a second render slot under BRIEF.md rule 2. Never delete files; never spend money or enter credentials. Commit working changes with clear messages ending "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; touch shared kit/core files only with small targeted edits and say so in the commit.`

const TEXT = { type: 'object', properties: { summary: { type: 'string' } }, required: ['summary'] }
const SCORE = {
  type: 'object',
  properties: { scores: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, score: { type: 'number' }, why: { type: 'string' } }, required: ['id', 'score', 'why'] } } },
  required: ['scores'],
}
const ISSUES = {
  type: 'object',
  properties: {
    score: { type: 'number' },
    issues: { type: 'array', items: { type: 'object', properties: {
      t: { type: 'number' }, frame: { type: 'number' }, area: { type: 'string', enum: ['visual', 'audio', 'script'] },
      severity: { type: 'string', enum: ['must', 'nice'] }, issue: { type: 'string' }, fix: { type: 'string' } },
      required: ['t', 'area', 'severity', 'issue', 'fix'] } },
  },
  required: ['score', 'issues'],
}

// ---------------------------------------------------------------- research
phase('Research')
const [refsBrief, commentsBrief, factsBrief] = await parallel([
  () => agent(`${COMMON}\nYou are the reference analyst. Brief: ${BRIEF}. Find the top 3 proven viral videos for this topic/lane (pipeline.sources, yt-dlp on the Spark with --js-runtimes node). Break each down frame by frame at native fps (research/frame-analysis/tools): hook in the first 3 s, cut rate, shot types and angles, how each line is shown on screen, payoff and loop. Save sheets under research/pipeline/${SLUG}/refs/. Return a concise brief a writer and a shot planner can act on (numbers, timestamps, what to copy structurally, what to beat).`, { label: 'research:refs', phase: 'Research', schema: TEXT }),
  () => agent(`${COMMENTS_TASK()}`, { label: 'research:comments', phase: 'Research', schema: TEXT }),
  () => agent(`${COMMON}\nYou are the fact checker and topic scout. Brief: ${BRIEF}. List the facts this topic depends on, each with a reliable source and the safe way to state it (numbers rounded honestly). Flag anything commonly told wrong. Return the fact sheet.`, { label: 'research:facts', phase: 'Research', schema: TEXT }),
])
function COMMENTS_TASK() {
  return `${COMMON}\nYou are the audience researcher. Brief: ${BRIEF}. For the top viral videos on this topic/lane, pull top comments (yt-dlp --write-comments on the Spark, limit 300 per video). Return what viewers react to: the moments they quote, questions they ask, what they share it for, complaints. End with 5 concrete do's for our version.`
}
const RESEARCH = `Reference brief:\n${refsBrief?.summary}\n\nAudience brief:\n${commentsBrief?.summary}\n\nFacts:\n${factsBrief?.summary}`

// ---------------------------------------------------------------- script
phase('Script')
const ANGLES = [
  'a second-person "you" hook that drops the viewer into the situation in the first line',
  'a paradox or absurd-true-outcome hook (the surprising result first, then how)',
  'a concrete number or scale hook that is instantly visual',
]
const drafts = await parallel(ANGLES.map((angle, i) => () => agent(
  `${COMMON}\n${RESEARCH}\n\nYou are writer ${i + 1}. Write a complete ~55-65 s narration script for ${SLUG} using ${angle}, following research/corpus/*/PLAYBOOK.md and the reference brief's structure. Every line must be showable on screen. Save it as research/pipeline/${SLUG}/draft_${i + 1}.md and return the full script text.`,
  { label: `script:writer${i + 1}`, phase: 'Script', schema: TEXT })))
const draftText = drafts.map((d, i) => `--- DRAFT ${i + 1} ---\n${d?.summary || '(missing)'}`).join('\n\n')
const judged = await parallel(['hook and first 3 seconds', 'retention: every line earns the next', 'clarity and payoff on a phone, first-time viewer'].map((lens) => () => agent(
  `${COMMON}\n${RESEARCH}\n\n${draftText}\n\nYou are a script judge. Score each draft 0-10 through one lens only: ${lens}. Be harsh; compare with the reference videos. ids: draft_1, draft_2, draft_3.`,
  { label: `script:judge`, phase: 'Script', schema: SCORE })))
const totals = [1, 2, 3].map((n) => judged.filter(Boolean).reduce((s, j) => s + (j.scores.find((x) => x.id === `draft_${n}`)?.score || 0), 0))
const best = totals.indexOf(Math.max(...totals)) + 1
log(`script totals ${totals.join(' / ')} -> draft ${best}`)
await agent(`${COMMON}\n${RESEARCH}\n\n${draftText}\n\nJudges' notes:\n${JSON.stringify(judged.filter(Boolean))}\n\nYou are the retention critic and editor. Take draft ${best}, graft in the best lines of the others, cut every word that doesn't earn its place, make the hook land within 3 s, and make the ending loop to frame 0. Write the final episodes/${SLUG}/script.md in the pipeline's script format (see existing episodes/*/script.md), run scripts/originality_check.py on it until it passes, and commit.`,
  { label: 'script:editor', phase: 'Script', schema: TEXT })

// ---------------------------------------------------------------- direction
phase('Direction')
const [shotPlan, artPlan] = await parallel([
  () => agent(`${COMMON}\n${refsBrief?.summary}\n\nYou are the shot planner. Read episodes/${SLUG}/script.md. Plan every shot so the cut rate, shot sizes and angles match the reference brief (cut at least as often as the references; close and low angles where they use them; every line literalised on screen). Write research/pipeline/${SLUG}/shot_plan.md: per line, the shot(s), duration, framing, what moves.`, { label: 'direction:shots', phase: 'Direction', schema: TEXT }),
  () => agent(`${COMMON}\n${refsBrief?.summary}\n\nYou are the art director. Read episodes/${SLUG}/script.md. Plan the settings (pipeline/episodes/settings.py: place, kind, biome, depth, light) and the look per setting in the lane's style, and decide where Codex background plates beat code-drawn sets (experiments/asset-gen/NOTES.md; style A or the realistic zackd variant). Generate the plates you need. Write research/pipeline/${SLUG}/art_plan.md.`, { label: 'direction:art', phase: 'Direction', schema: TEXT }),
])

// ---------------------------------------------------------------- build
phase('Build')
await agent(`${COMMON}\nShot plan:\n${shotPlan?.summary}\n\nArt plan:\n${artPlan?.summary}\n\nYou are the builder. Make ${SLUG} with the pipeline end to end (studio-make: voice, storyboard from shots.json, staging check PASS, render through the dispatcher). Follow the shot and art plans; build any new kit components you need. Then run python3 -m pipeline.qa.frames30 ${SLUG} --mp4 <final mp4>. Return the MP4 path and duration.`,
  { label: 'build:visuals', phase: 'Build', schema: TEXT })
await agent(`${COMMON}\nYou are the audio specialist for ${SLUG}. Check the narration (natural pacing, no robotic seams), the scored soundtrack at the approved level (pipeline/audio/config.py), and that every sound effect lands within 2 frames of its visual event in the latest render. Fix by remixing (pipeline.audio.make --reuse-tts) and re-muxing onto the latest MP4; never change the narration timing. Return what you changed and the final MP4 path.`,
  { label: 'build:audio', phase: 'Build', schema: TEXT })

// ---------------------------------------------------------------- review + fix loop
const CRITICS = [
  ['hook', 'the first 3 seconds and the cover frame: would a scrolling viewer stop? Compare with the references\' first 3 s'],
  ['logic', 'does everything on screen make sense for where we are and what is being said (place, depth, scale, era, physics)?'],
  ['motion', 'is motion smooth and motivated: no pops, snaps, frozen holds, ghosting fades; does the cut rate match the references?'],
  ['readability', 'captions, labels and subjects on a phone: collisions, safe area, split phrases, things too small to read'],
  ['sound', 'voice naturalness, music level under the voice, SFX timing against the picture, the loop seam'],
]
let round = 0, verdict = null, history = []
while (round < MAX_ROUNDS) {
  round++
  phase('Review')
  const prep = await agent(`${COMMON}\nList the every-frame sheets for ${SLUG}: run python3 -m pipeline.qa.frames30 on the latest final MP4 if out/${SLUG}/qa/f30/ is older than it. Return JSON in summary: {"mp4": path, "duration": seconds, "sheets": [paths in order]}.`, { label: `review:prep r${round}`, phase: 'Review', schema: TEXT })
  let info = {}
  try { info = JSON.parse(prep?.summary || '{}') } catch (e) { info = {} }
  const sheets = info.sheets || []
  const spans = []
  for (let i = 0; i < sheets.length; i += 5) spans.push(sheets.slice(i, i + 5))
  const reviews = await parallel([
    ...spans.map((s, i) => () => agent(`${COMMON}\nYou are a frame reviewer (round ${round}). Follow pipeline/qa/REVIEW_PROMPT.md section 3. Read EVERY one of these every-frame sheets in order: ${s.join(', ')} (video ${info.mp4}). Report every unintended pop, snap, vanish, ghost, nonsense element or unreadable moment with time and frame.`, { label: `review:frames ${i + 1}`, phase: 'Review', schema: ISSUES })),
    ...CRITICS.map(([id, q]) => () => agent(`${COMMON}\nYou are the ${id} critic (round ${round}) for ${info.mp4}. Judge only this: ${q}. Use frames (ffmpeg on the Spark or Mac), the every-frame sheets in out/${SLUG}/qa/f30/ and the reference sheets in research/pipeline/${SLUG}/refs/. Score 0-10 and list issues.`, { label: `review:${id}`, phase: 'Review', schema: ISSUES })),
  ])
  const all = reviews.filter(Boolean)
  const must = all.flatMap((r) => r.issues.filter((x) => x.severity === 'must'))
  verdict = await agent(`${COMMON}\nYou are the final judge (round ${round}). Put ${info.mp4} side by side with the lane references (research/pipeline/${SLUG}/refs/). Your job is to find why it is NOT as good as them, not to approve it. Reviewer findings: ${JSON.stringify(all).slice(0, 12000)}\nScore it 0-10 overall (8 = same tier as the references; FEEDBACK.md ship bar: every principle >= 7, hook >= 8). Put the 8 most important fixes first in issues.`, { label: `review:judge r${round}`, phase: 'Review', schema: ISSUES })
  const hook = reviews[spans.length]?.score ?? 0  // CRITICS[0] is the hook critic, right after the frame reviewers
  history.push({ round, judge: verdict?.score, hook, must: must.length })
  log(`round ${round}: judge ${verdict?.score}, hook ${hook}, must-fix ${must.length}`)
  if ((verdict?.score || 0) >= 8 && hook >= 8 && must.length === 0) break
  if (round >= MAX_ROUNDS) break

  phase('Fix')
  const todo = [...(verdict?.issues || []), ...must]
  const byArea = (a) => todo.filter((x) => x.area === a)
  if (byArea('script').length) {
    await agent(`${COMMON}\nYou are the script fixer. Apply these script issues to episodes/${SLUG}/script.md without breaking timing more than needed, keep originality PASS, then regenerate the voice and storyboard (studio-make from the voice step). Issues: ${JSON.stringify(byArea('script'))}`, { label: `fix:script r${round}`, phase: 'Fix', schema: TEXT })
  }
  await agent(`${COMMON}\nYou are the visual fixer (round ${round}). Fix these issues in the shots/storyboard/kit for ${SLUG}, re-render through the dispatcher, re-run frames30, and check each fix in the new sheets yourself. Issues: ${JSON.stringify(byArea('visual'))}`, { label: `fix:visual r${round}`, phase: 'Fix', schema: TEXT })
  await agent(`${COMMON}\nYou are the audio fixer (round ${round}). Remix and re-mux onto the newest render of ${SLUG} (pipeline.audio.make --reuse-tts), fixing: ${JSON.stringify(byArea('audio'))}. Also re-check that SFX still land on the new picture.`, { label: `fix:audio r${round}`, phase: 'Fix', schema: TEXT })
}

// ---------------------------------------------------------------- final
phase('Final')
const final = await agent(`${COMMON}\n${commentsBrief?.summary}\n\nYou are the caption writer and closer for ${SLUG}. 1) Make a phone-sized copy (< 30 MB) of the final MP4 in out/. 2) Write a caption for Instagram and a title + description for YouTube Shorts modelled on the proven viral references (hook line, share prompt, 3-6 hashtags; no clickbait the video doesn't pay off); save as out/${SLUG}/caption.md. 3) Append 3-5 lines to docs/OVERNIGHT_LOG.md: rounds ${JSON.stringify(history)}, what's still wrong, paths. Do not publish. Return JSON in summary: {"phone_mp4": path, "caption_file": path, "judge": score, "still_wrong": [..]}.`,
  { label: 'final:caption', phase: 'Final', schema: TEXT })
const parity = await agent(`${COMMON}\nYou run the parity check for ${SLUG} exactly as docs/PARITY.md defines it: (1) the measured checks for ours and 3 lane references (research/pipeline/${SLUG}/refs/), (2) a blind side-by-side panel of three judges given unlabeled matched-moment pairs (order from a coin derived from the file hashes), (3) leave the owner check open. Append the results to docs/PARITY_LOG.md. Return JSON in summary: {"pass": true|false, "failed_checks": [..], "panel": {...}}.`,
  { label: 'final:parity', phase: 'Final', schema: TEXT })
return { slug: SLUG, lane: LANE, rounds: history, final: final?.summary, parity: parity?.summary }
