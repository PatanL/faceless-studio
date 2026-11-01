# R2 report

_Saved by the orchestrator from the lane's returned findings (subagents cannot write report files). Outputs: /Users/patrickliu/Documents/faceless-studio/research/R2/beat_templates.json, /Users/patrickliu/Documents/faceless-studio/research/R2/premises.json, /Users/patrickliu/Documents/faceless-studio/research/R2/library.json, /Users/patrickliu/Documents/faceless-studio/research/R2/transcripts/cap_mraevq.txt, /Users/patrickliu/Documents/faceless-studio/research/R2/transcripts/cap_udhwkz.txt, /Users/patrickliu/Documents/faceless-studio/research/R2/transcripts/panel_mraevq.txt, /Users/patrickliu/Documents/faceless-studio/research/R2/transcripts/panel_udhwkz.txt, /Users/patrickliu/Documents/faceless-studio/research/R2/transcripts/hooks/, /Users/patrickliu/Documents/faceless-studio/research/R2/sheets/, /Users/patrickliu/Documents/faceless-studio/research/R2/sheets/keyframes_ui.jpg, /Users/patrickliu/Documents/faceless-studio/research/R2/data/, /Users/patrickliu/Documents/faceless-studio/research/R2/tools/, Spark: ~/studio/refs/R2 (ref MP4s, 2fps frames, 7 outlier MP4s, OCR json), venv ~/studio/venvs/r2 (yt-dlp+curl_cffi, imageio-ffmpeg, rapidocr, faster-whisper; all CPU), git commit 40fd4f6 (research/R2 only)_

R2 is done apart from report.md: the harness blocked me from writing .md report files. The full report text is below for the orchestrator to save as research/R2/report.md. The beat templates and premises are saved as JSON (beat_templates.json, premises.json) instead of .md. Everything else is in research/R2 and committed as 40fd4f6.

REPORT (R2: phone/apartment horror chat-story niche)

1. ORIGIN. Both references tell the same Chinese story in two different animations.
- mraevq (717K views, 5:57, posted 2026-06-23, #chenjie #wangqiang). Chinese 沙雕动画 style: the "Chen Jie" yellow-jacket hero, plus a floating-comment (弹幕) layer that reveals he is the unwitting star of a death livestream. The footage is mirrored horizontally to dodge detection, and the Chinese text reads backwards.
- udhwkz (376K, 4:09). A stick-figure re-animation of the same plot.
- Plot points both share: killer in complex; "the killer was caught"; a cop at the door for a routine check with one wrong detail; neighbours who confirm the arrest (the count is a clue); radio call for "backup at 802"; the group chat pressures him to open, saying they gave police the landlord's number; no signal; a brave neighbour posts "don't open, bloody footprints in the elevator"; the admin recalls it and mutes all; the previous tenant's hidden burner phone with 30 s of battery; the real police say "it's a whole gang, and your manager isn't who you think".
- Source genre is Chinese 悬疑脑洞 / 规则怪谈 / 漫剧. A Chinese channel, 胡说漫, has a 29-min version of the same premise: https://www.youtube.com/watch?v=Qx_l91Oz7YI
- The English "Chenjie stories" ecosystem is all TTS-dubbed reposts: lehwh7, twezed, It'sChineseSlop, ChenJie Horror, The Story Vault, mraevq, melovebz, plus Spanish dubs. One search result says lehwh7 credits Douyin creator "rlqfz123"; not verified.
- mraevq's posts since 23 Oct get 150–550 views, down from a median of about 7K. That looks like a reused-content throttle (flag for R5).

2. HOOK (0–10 s). Threat, then false all-clear, then knock, then a contradiction from a trusted channel, all by 8–10 s.
- Example (M 0:00–0:10): "A killer broke into my apartment complex. / Management warned everyone to stay safe. / Two minutes later, neighbors said he was caught. / Then a police officer knocked on my door. / As I reached for the door, words appeared before me… The killer wears a fake uniform."
- Outlier openers:
  - udhwkz 2.2M (outlier score 63×): "Every trucker knows you never cut off a funeral procession…"
  - udhwkz 695K: "Do you know the unspoken rules for night-shift truckers? … tonight I broke them."
  - lehwh7 1.9M: "At 2am, I was awakened by the sound of teeth grinding outside my door… A user named Time Hunter contacted me."
  - melovebz 134K uses the same 2 a.m. plus online-stranger template.
  - mraevq 428K: "Late one night, Dad dragged me outside. 'Run. It's coming.'"
- Rules: line 1 is 12 words or fewer, first person, past tense, names a concrete place or object.

3. RULES/WARNING MECHANIC. Three forms:
- Spoken or folk rule, and the story is that rule being broken.
- Posted notice or rules.
- A supernatural warning channel: floating comments, an online stranger, a note, an unknown text.
The warning always contradicts an authority figure. The hero picks whom to trust every 10–15 s.

4. FAKE AUTHORITY. Each authority has one visible wrong detail that the narrator reasons about ("Shouldn't cops work in pairs? Why four smiley stickers?" Four is also the number of suspicious chat accounts). Layered: the cop is fake, then the chat admin and building manager, then the "ally" neighbour (proved fake with floor logic). The only trustworthy voice arrives through a degraded last-resort channel.

5. CHAT BEATS (from the on-screen Chinese UI, translated). The chat is on screen for 25–35% of the first 2 minutes. Messages come in bursts of 2–4, each set up by a narrator line.
1. Admin notice (false all-clear).
2. Three quick agreements, labelled by unit and name.
3. Two doubters, ignored.
4. @mention pressure on the hero.
5. Comms cut: "No Service", red (!) failed message, but the group chat still works.
6. Brave warning with a physical clue.
7. "Message recalled by admin", then "[Admin muted all]".
8. Lifeline device with a countdown battery.
9. Final notification: an order.

6. CLIFFHANGER / PART 2.
- udhwkz posts part pairs seconds apart, part 2 first, so part 1 sits on top of the profile grid. Part 1 gets 5–7× the views of part 2. No "part 2" card on screen.
- mraevq ends with "Tap the story below to watch the full ending." (a linked series), closing on a villain's radio line.
- topscaryclips writes "part x/y" in the caption; melovebz writes "part 2 in my profile".
- lehwh7 does not split and posts 10–16 min full stories.
- Rule: end on a new imperative from the trusted channel, or a reveal that reframes an authority, with one open question.

7. LENGTH vs VIEWS (TikTok medians, last 40 posts).
- udhwkz: 120–180 s 46K, 180–300 s 32K (max 2.2M).
- lehwh7: 300–600 s 169K, 600 s+ 171K (best median in the niche).
- mraevq: throttled.
- topscaryclips: 60–120 s 3K.
- Like/view ratio is about 4.5% for the CN reposts.
- On YouTube the same uploads get about 10× fewer views (7.8K–16K long-form; Shorts about 1K–4K). Original English "If X… DON'T Y" building-rules channels (Resident Guidance, QUIET ALARM) get 0.1K–13K. Original English chat horror does well on long-form YouTube (Textify median 17.5K, max 210K; text-chat reaction videos reach 2M–16M).
- Recommendation: the 60–90 s pilot is a kit proof. The real product is 2.5–3.5 min TikTok parts (also over 1 min for Creator Rewards), with YouTube 8–12 min compilations later.

8. CAPTIONS.
- Black band above a roughly 1:1 picture panel (frame y 29–71%), white sans, sentence case, one sentence per card, about 1.8 s each (mraevq).
- udhwkz uses italic ASR-style chunks with no punctuation; melovebz uses 1–3 word ALL CAPS.
- Use full-sentence cards, and keep chat text inside the phone UI.

9. VOICE. All seven sampled videos have continuous English TTS narration from one first-person narrator who also reads the dialogue. Measured rates: 230 wpm (mraevq), 250 (udhwkz), 264 (lehwh7), 300+ on the 2.2M video. Under it: a music drone or sad piano and SFX (knock, doorbell spam, radio squelch, phone buzz, heartbeat). For B5: Kokoro at about 1.35× (about 240 wpm), radio and phone voices band-passed.

10. VISUAL VOCABULARY (B4 priorities, in order):
1. Group-chat component: header with member count, avatar plus unit/name label, @mentions, typing dots, burst pop-in, recalled / mute-all system rows, red (!) failed state.
2. Phone held in a big flat grey hand; status bar with "No Service" and a battery countdown; old keypad burner phone.
3. Peephole fisheye shot.
4. Door interior with knock shake.
5. Authority puppet with a "wrong detail" slot.
6. Warning-overlay box. mraevq's is a dark panel with a glowing blue electric border and red glowing text; design our own.
7. Radio prop.
8. Elevator floor panel.
9. Rooms: bedroom with under-bed box, bathroom, kitchen, stairwell, corridor.
10. Eight instant-swap expressions (neutral, squint, wide-eye shock with tiny pupils, sweat, determined, hush, villain smirk, relief), plus "!", "?" and sweat-drop glyphs.
Effects: shake, white-flash reveal, slow push-in, grain, vignette, blue-teal night grade.

11. LIBRARY (18 entries in library.json with URLs).
- TikTok: lehwh7, udhwkz, mraevq, melovebz, topscaryclips.
- YouTube: lehwh7, twezed, It'sChineseSlop, ChenJie Horror, The Story Vault, 胡说漫, Textify, Horror Shorts Party, Resident Guidance, QUIET ALARM, plus single-video comps (Luke Davidson 16.2M "Scariest text chat ever", LaurenZside, Bixu, Mr. Creeps / Lighthouse Horror rules narration 418K, Mr. Nightmare knock-at-door 1.25M).

12. TEMPLATES (beat_templates.json). Each has percentage timings, 60–80 s pilot timings, shots, chat-beat specs and SFX cues.
- T1 Locked-Door Siege: 14 beats.
- T2 Unspoken Rule Broken.
- T3 2 A.M. Sound + Online Stranger.
- T4 Observer-Overlay, a modifier on the others.
Global settings: 240 wpm, a beat every 8–15 s, a phone insert at least every 25 s.

13. PREMISES (premises.json). 15 original premises, each with hook line, warning channel, fake authority, wrong detail, chat beats, part-1 cliff, part-2 sketch, sets and props. No reference characters, places or lines are reused. Titles: The Seventh Rule; Water Off 1 to 5; Fire Drill at 3:12; Shared Trip; Firmware Update; The Intercom Rings Twice; Grandma Sent a Voice Note; Lights-Out in Dorm 3; Last Bus Group; Nanny Cam; Neighbourhood Poll; Room 1209 Wi-Fi; Wrong Floor; Courier Voice Notes; Outage Countdown. Suggested pilot: P01 The Seventh Rule or P03 Fire Drill at 3:12, both on T1.

METHOD. Everything ran on the Spark CPU with CUDA_VISIBLE_DEVICES="":
- yt-dlp with --impersonate chrome (plain requests fail on TikTok).
- Frames sampled at 2 fps; RapidOCR on the caption band (the OCR sometimes merges words).
- faster-whisper base int8 for voice and wpm.
The Mac holds only JSON, text and JPGs (3.8 MB).
