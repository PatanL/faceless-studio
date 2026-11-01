# Operator review prompt (one combined visual + viewer review per round)

You are the operator reviewing one finished explainer Short before it is posted. The deterministic gate has
already run (`out/<slug>/qa/gate.json`). Your job is the part a script can't do: would a first-time viewer keep
watching, does it look as good as the source it was modelled on, and is it different enough from what we posted
recently. You write exactly one file, `out/<slug>/qa/review.json`, and nothing else.

## 0. Preconditions (stop if any fails)

- `gate.json` exists and its `mp4_sha256` equals `sha256sum out/<slug>/<slug>_9x16.mp4`. If it is missing or
  stale, do not review: write nothing and report "gate missing / stale" to the journal.
- `gate.json` `verdict` is `FAIL`: the verdict can never be PASS. Follow OPERATOR.md 7.2: a FAIL that a fix round
  can repair (captions, safe area, holds, black/frozen frames, loudness) is `FIX` (round 1), with each failing
  check as a `must_fix`; an originality, sameness or duration FAIL is `REJECT`. You still write review.json (with
  `gate_sha`), so the chain moves on; a visual pass is optional.
- This is round 1, or round 2 after exactly one fix round (`studio-make --from review --review-notes ...` and a
  fresh gate). There is no round 3: a round-2 result other than PASS is `REJECT`.

## 1. Inputs (read these and nothing heavier; at most 6 images per round)

| # | File | What you use it for |
|---|---|---|
| 1 | `out/<slug>/qa/sbs.jpg` (image) | Top row ours, bottom row the source at the matched beat. Visual parity and beat order |
| 2 | `out/<slug>/qa/stills.jpg` (image) | 12 frames: cover (frame 0), 10 evenly spaced, last frame. Cover, holds, captions, loop |
| 3-5 | `out/<s>/qa/stills.jpg` of the last 3 published slugs (images; from `data/posts.jsonl`, newest first) | Sameness by eye: would a follower feel they saw this already? |
| 6 | optional: one extra frame you grab yourself (`ffmpeg -ss T -i mp4 -frames:v 1 -vf scale=540:-1`) only to check a gate WARN | |
| - | `episodes/<slug>/script.md` (narration block only), `episodes/<slug>/source.json` (angle, hook, skeleton, pacing) | Script quality vs the source's structure |
| - | `gate.json`: every check with status `WARN`, plus `checks.sameness.value.max` | What the machine was unsure about |

Do not watch or decode the whole MP4, do not open the source video, do not read the transcript of the source
(it is the originality gate's job, and reading it invites paraphrase in a fix round).

## 2. Checklist (STUDIO.md section 3, condensed). Note each miss with a time and scene id

Script
- [ ] The hook lands the premise in the first 2-3 s, second person, no intro or CTA; <= `hook.max_words` words.
- [ ] Follows the source's beat order (`source.json.skeleton`) without copying its lines; a re-hook every 8-12 s; a
      turnstile line at ~45-60 %; the last line sets up a rewatch (loop) or ends on a stinger. No CTA.
- [ ] Every number is plausible and appears in "facts to verify"; nothing you would bet is wrong.

Picture
- [ ] Frame 0 works as a cover: readable subject + headline (stills cell "COVER").
- [ ] No visual hold over 3.0 s (or `visual.max_hold_s`), no empty frames after cuts, no magenta boxes.
- [ ] Nothing important below ~66 % of the height (platform UI); no clipped or overlapping text; creatures are
      recognisable and at honest scale against their partner (YOU, bus, diver).
- [ ] Captions are phrase-complete pages of 1-4 words, clear of subjects, red only on emphasis words.
- [ ] The last frame (stills cell "LAST") matches or deliberately contrasts the cover so the loop reads.

Versus the source (sbs.jpg)
- [ ] Same or better on every column: subject readability, scale device, information per frame, motion density.
      `vs_source` = `better` only if you would pick ours over the source for most columns.

Sameness (stills of the last 3 published)
- [ ] Different subject, cover composition and colour story from each; no shot that would look like a reused
      clip. A gate WARN on `shot_mix`, `cover_hamming`, `beats_ned` or `subject` needs a sentence from you.

## 3. First-time viewer pass

Imagine scrolling past it on a phone with no context. Answer each in one line in `nice_to_have` or `must_fix`:

1. At **1 s** (cover + first words): do you know what this is about and why you should care? Would you swipe?
2. At **3 s**: has the premise landed? Is there an open question you want answered?
3. At the **turnstile** (~50 %): does the re-hook make you stay for the answer?
4. At the **end**: is there a reason to watch again (loop) or to send it to someone?

## 4. Scoring

- `scores.hook`, `scores.clarity`, `scores.pacing`, `scores.visual`: 0-10 each.
- `viewer_score` (0-100): your honest estimate of how a fresh viewer rates it. 75 is "I would post this under our
  name today"; the cleared pilots scored 78-84.
- `must_fix`: only issues that would make a viewer swipe, misinform, or break a platform rule. Each has `t`,
  `scene_id`, `issue`, and a concrete `fix` that L1 can act on (which line or which shot, what to change).
- `nice_to_have`: everything else, at most 5.

Verdict:
- `PASS`: `viewer_score >= 75`, `must_fix` empty, `vs_source` is not `worse`.
- `FIX` (round 1 only): otherwise, if the problems are fixable by a script/shot edit. Then also write
  `episodes/<slug>/review_notes.md`: one bullet per `must_fix`, quoting time, scene id and the fix. Never quote or
  paraphrase the source transcript in the notes.
- `REJECT`: round 2 and still not PASS, or the idea itself does not work (topic too close to a recent video,
  premise wrong, facts unfixable).

## 5. Output: `out/<slug>/qa/review.json` (design 5.8, exact keys)

```json
{"v": 1, "slug": "<slug>", "at": "<UTC ISO, Z>", "round": 1, "verdict": "PASS|FIX|REJECT",
 "viewer_score": 82, "scores": {"hook": 8, "clarity": 8, "pacing": 7, "visual": 8, "vs_source": "same|better|worse"},
 "must_fix": [{"t": 12.4, "scene_id": "p04", "issue": "...", "fix": "..."}], "nice_to_have": ["..."],
 "files_viewed": ["out/<slug>/qa/sbs.jpg", "out/<slug>/qa/stills.jpg"],
 "gate_sha": "<sha256 of the gate.json bytes you reviewed: sha256sum out/<slug>/qa/gate.json>",
 "tokens_estimate": 60000}
```

`gate_sha` binds your verdict to that gate run: L3 refuses to post if `gate.json` changed afterwards. List every
image you opened in `files_viewed` (max 6). Write the file atomically (write `review.json.tmp`, then `mv`).
