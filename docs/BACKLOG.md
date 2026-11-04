# Backlog (ranked; the loop always takes the top unfinished item)

Priorities (owner): 1) hook, 2) voice, 3) script, 4) visuals and everything else. Mark items done with the commit hash.

## Hook
1. Hook A/B per episode: make 3 frame-0 variants (act close-up, different prop or angle) as stills and have one blind judge pick against 3 RicksClips first frames before building.
2. Dutch v2 hook: the general is readable by 2-4 s (in progress).
3. A first-1.5 s motion rule: something visibly moves in frame 0 (a prop or a character mid-act), checked by a gate.

## Voice
4. The hook boost applies to line 1 only: test a milder boost (1.15) on the "You see" line and the last line.
5. Fix make.py's report.json float32 crash (it forces wrappers).
6. Add a "misheard word" ASR gate to the audio step (faster-whisper medium.en, fail on word mismatches that aren't homophones).

## Script
7. Cold-read every new script with 3 readers (majority) before voicing.
8. Next scripts: Edo firemen (in progress), then storm bells, Fresnel lens.

## Visuals
9. The dragon prow in the Myeongnyang hook kit (never visible in 3 tries); add an in-frame check.
10. Background texture density (65% of the reference): painted wall and window detail.
11. Camera: the jar-orbit study's push and tilt phases (12 frames late, a third of the depth).

## Data
12. Connect YouTube Analytics (owner OAuth) so the loop can read swipe-away and retention itself.
13. A 48 h / 7 d metrics pull for every post (yt-dlp views and likes, IG reel plays) into EXPERIMENTS.md, plus one hypothesis and one test each time.
