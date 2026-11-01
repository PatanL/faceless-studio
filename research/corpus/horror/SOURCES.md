# Horror corpus: sources

Niche: phone and group-chat apartment horror. These are short 2D or chat-screen stories, mostly 60 to 200 s, built from rules or warnings, an authority figure who turns out to be fake, and a cliffhanger. Some run as 2-part series.

Built 2026-11-01, about 09:05 to 09:25 UTC. All downloads, transcription and frame sampling ran on the Spark CPU, never the GPU. Only text and small JPGs are on the Mac.

## Selection method

- **Pool.** I started with everything in `research/library/candidates-horror.json` and R2's metadata (`dgx-spark:~/studio/refs/R2/meta`). That covers full listings for @mraevq, @udhwkz, @lehwh7, @melovebz and @topscaryclips, plus about 20 YouTube searches and channel tabs. I added four new YouTube searches, each run both as a normal search and with a Shorts/under-4-min filter: "apartment group chat horror animation", "rules horror story animated", "scary text story animation" and "killer in my building story". I also pulled channel listings for WrONG Rules, Dusk Broadcast and Wansee. Raw listings are in `dgx-spark:~/studio/refs/corpus_horror/meta/`.
- **Outlier score.** `views / median views of that channel's recent uploads`. Each file header says which median was used. For @mraevq I kept the library's basis: 10,750, the median of its horror-cartoon era. Its latest 40 uploads are a different format with a median of 7,018, which would put the seed at 102x.
- **Filter.**
  - The video has to fit the niche: apartment, door, phone, chat, rules or warnings, or a fake authority.
  - It has to be short. The target is 60 to 180 s, and I allowed up to about 250 s, plus the one 357 s seed.
  - We have to be able to rebuild its structure in code-only 2D: flat cartoon panels, chat UIs, text cards and pictograms.
  - Anything over 400 s was dropped, even with a high score: @lehwh7 "teeth grinding monster", 1.9M views, 11x, 585 s; @mraevq 7664930759395888416, 428K, 40x, 918 s.
- **Transcripts.**
  - Every video was downloaded once to `dgx-spark:~/studio/refs/corpus_horror/vid/`. TikTok needed `--impersonate chrome`, so the `~/.local/bin/yt-dlp` script was run under `~/studio/venvs/r2/bin/python`, which has curl_cffi, with `PYTHONPATH` set to the user site-packages.
  - Narrated videos were transcribed with faster-whisper `small` (int8, CPU, 4 threads, VAD, `CUDA_VISIBLE_DEVICES=""`) in `~/studio/.venv`. Audio is passed as a numpy array, because that venv's PyAV breaks the file loader.
  - YouTube auto-subs (VTT) were pulled for every YouTube video and cleaned with `tools/vtt2lines.py`.
  - The chat-only Shorts were transcribed by reading 1 fps contact sheets, bubble by bubble, with speaker labels.
  - Scripts are in `tools/` here, mirrored on the Spark at `~/studio/refs/corpus_horror/tools/`.
- **Overview sheets.** `sheets/<id>.jpg` has one frame every few seconds (40 tiles) for each chosen video, so visual beats can be matched to the transcript.

## The 12

| # | id | channel | views | outlier | dur | transcript source |
|---|---|---|---|---|---|---|
| 1 | [7702661541224566049](https://www.tiktok.com/@udhwkz/video/7702661541224566049) | udhwkz | 2,200,000 | **63.1x** | 3:21 | whisper |
| 2 | [7702661471641128224](https://www.tiktok.com/@udhwkz/video/7702661471641128224) | udhwkz | 343,100 | 9.8x | 3:11 | whisper |
| 3 | [7654526047005723937](https://www.tiktok.com/@mraevq/video/7654526047005723937) (seed) | mraevq | 716,900 | **66.7x** | 5:57 | whisper |
| 4 | [7659677578365537569](https://www.tiktok.com/@udhwkz/video/7659677578365537569) (seed) | udhwkz | 376,200 | 10.8x | 4:09 | whisper |
| 5 | [7692268145888873760](https://www.tiktok.com/@udhwkz/video/7692268145888873760) | udhwkz | 694,900 | 19.9x | 2:46 | whisper |
| 6 | [7694996216505060641](https://www.tiktok.com/@udhwkz/video/7694996216505060641) | udhwkz | 613,300 | 17.6x | 2:45 | whisper |
| 7 | [7670495663624408352](https://www.tiktok.com/@mraevq/video/7670495663624408352) | mraevq | 193,600 | 18.0x | 2:55 | whisper |
| 8 | [cVUJmsVkUW4](https://www.youtube.com/watch?v=cVUJmsVkUW4) | WrONG Rules | 290,919 | **30.9x** | 2:15 | whisper + VTT + burned-in captions |
| 9 | [omuJBFs2L6c](https://www.youtube.com/watch?v=omuJBFs2L6c) | Dusk Broadcast | 762,944 | 18.6x | 1:37 | VTT (whisper-checked) |
| 10 | [T42u5xhrq-0](https://www.youtube.com/shorts/T42u5xhrq-0) | Textify | 868,500 | **25.5x** | 1:00 | on-screen chat (visual) |
| 11 | [gzXY52lcAcI](https://www.youtube.com/shorts/gzXY52lcAcI) | Textify | 352,848 | 10.4x | 0:59 | on-screen chat (visual) |
| 12 | [Qz-TrB6W2SM](https://www.youtube.com/watch?v=Qz-TrB6W2SM) | Wansee Entertainment | 1,521,857 | 9.0x | 2:48 | whisper |

### Why each was chosen

1. **7702661541224566049: funeral procession, Part 1.** This is the biggest spike in the niche: 2.2M views in about a day, 63x the channel median, 164K likes and 12.9K saves.
   - It opens on an unwritten rule ("you never pass a hearse"), then adds a second rule ("never roll down the window at night").
   - A stranger performs a ritual and then the companion repeats it, which builds the dread.
   - It ends mid-scene, so it's the model for a Part-1 cliffhanger.
   - The rules-in-the-first-5-seconds hook carries over directly to building or chat rules.
2. **7702661471641128224: funeral procession, Part 2.** This is the same story continued. It was posted **9 seconds before Part 1** (03:00:57 vs 03:01:06 UTC), so Part 1 sits on top of the profile grid. It's the only clean 2-part pair in the pool.
   - Part 2 got 16% of Part 1's views, which tells us how far views fall off for a second part.
   - The structure: a reveal from an earlier plant (the license plate "1574" turns up in a crash), then a phone call to the family that **disproves the companion's story** ("What uncle?").
   - It ends on a fresh hook ("the fingerprint of a wandering evil spirit").
3. **7654526047005723937: seed, killer in the complex.** This is the exact target format.
   - Management's group-chat warning is followed by "he was caught".
   - A fake cop knocks at the door.
   - **Floating "viewer comment" text** tells the hero he's being watched, and the group chat erupts. It turns out exactly N residents confirmed the arrest, which reveals the chat itself is compromised.
   - There's a call to the real police with the battery running out, and it ends on "tap the story below to watch the full ending".
   - Chat panels, a peephole and a phone are all easy to build in code. On-screen chat OCR with timings is in `research/R2/transcripts/panel_mraevq.txt` and `cap_mraevq.txt`.
4. **7659677578365537569: seed, hallway-song killer.** A sister telling of the same premise, useful for comparing the beats.
   - A building rule (a song plays when the killer strikes), then the group-text "caught" update.
   - A cop who works alone, with 4 smiley stickers on his chest, matches exactly 4 confirmations in the chat.
   - Admin deletes a message and mutes the group. An earlier tenant left something behind.
   - A real-police call with "don't open that door". The final push notification reads "Don't let them find you. Get out of the building."
   - On-screen chat OCR is in `research/R2/transcripts/panel_udhwkz.txt`.
5. **7692268145888873760: night-shift trucker rules.** 695K views, 19.9x.
   - The opener is literally "Do you know the unspoken rules for…?", followed by the rule list and "tonight I broke them".
   - The narrator breaks his own rule by picking up a stranded family, and their story doesn't add up. The radio reports a red-car crash on this same road, which turns out to be a "flashback" to a crash 3 years ago. That hints the passengers aren't who they seem.
   - A red car chases them on a mountain road.
   - It's the cleanest example of opening on a rule list.
6. **7694996216505060641: apartment elevator.** 613K views, 17.6x, set in a residential high-rise.
   - An innocent question ("what floor are you going to?") makes every neighbor panic, and each reaction escalates.
   - Two phone screens appear: an AI-assistant chat asks the hero to share their location, and then Mom calls ("Don't you ever come home again").
   - The mechanic of one taboo phrase plus escalating reactions transfers directly.
   - The original relies on a Chinese wordplay, so we copy the mechanic, not the joke.
7. **7670495663624408352: dorm curtains and the supervisor's rules.** 18x.
   - A trusted authority (the dorm supervisor) gives rules: shoes pointing opposite ways, keep your eyes shut, blessed incense ash.
   - The twist is that the authority is the villain: the ash is her dead daughter's ashes and she wants a replacement.
   - A roommate shows a news article on her phone as proof.
   - It ends on a new rule ("a lightning-struck branch under your pillow").
   - It's the best example of the fake-authority twist through rules.
8. **cVUJmsVkUW4: "Mom's Note, Day 1".** 31x, 135 s. The whole video is a numbered list of house rules, read as a note from Mom.
   - Full-screen title cards ("ONLY THEN", "NOW", "REMEMBER") act as punctuation.
   - Color rules (blue or white objects, a red doll) and conditional branches ("if they are… stay put / if not…").
   - It ends with a setup for the series ("you'll find the second note… don't read it early").
   - Rules text cards are pure code.
9. **omuJBFs2L6c: Dusk Broadcast, "One of Your Classmates Is Not Real".** 763K views, 18.6x, 97 s.
   - An official-broadcast voice gives numbered guidelines ("First, do not sit next to them…"), ending "signing off, stay tuned, stay safe".
   - The visuals are flat white pictograms on black, with one red figure as the anomaly and caption text. This is the most code-friendly look in the corpus.
   - It's the model for an authority-warning format, and we can turn it into building-management notices.
10. **T42u5xhrq-0: Textify "so scary".** 868K views, 25.5x, 60 s. A two-person iMessage thread over game footage.
    - The pacing: about 56 bubbles in 60 s, roughly one per second.
    - Escalation: a creepy channel, then a noise in the room, then a figure, then ALL-CAPS panic.
    - A silence beat ("Ava?", "AVA??"), then a photo bubble.
    - The killer texts from the victim's phone: "Ava can't come to the phone right now… And soon, you will too…"
    - This is the chat-screen kit's reference for timing and the beats where the reply comes from the wrong person.
11. **gzXY52lcAcI: Textify "Creepiest Farmer Text Chat, PART 1".** 10.4x.
    - It cold-opens on a flash-forward: Dad texting "SHOOT THEM FOR GOD'S SAKE".
    - Then it cuts back in time to the family group chat "Roots Farm" and slowly builds normal tension (a crash outside, Mom goes to check).
    - It ends on a blurred "Full Story" card, a Part-1 cliffhanger.
    - It shows the 1:1 chat versus group-chat switch, sender names over the bubbles, and a flash-forward hook in 13 s.
12. **Qz-TrB6W2SM: Wansee, "Someone Broke Into Our Hotel Room".** 1.52M views, 9x on a large channel (169K median), 168 s.
    - Kids alone at 1 a.m. hear a knock, and the man claims to be "room service".
    - The fake-authority tell is that he spoke English instead of Turkish. They hide in the bathroom and call a parent on a phone that was left behind.
    - Footage proves it was real.
    - It's the plainest version of "someone at the door claims to be staff", told in first person over simple 2D.

## Alternates (transcribed, in `raw/_alt/`)

- `7668625939458182422`, TopScaryClips "True water park horror story (part 2/3)". It has the highest outlier in the pool at **121x** (498K views on a 4.1K median). Part 3 (`7668626589122399510`) got only 41K.
  - It's useful for series mechanics: it cuts mid-rescue, and the numbered part label is in the title.
  - The premise (a water-park drowning played for mockery) is off-niche, so it isn't in the 12.
- `7694491037988818208`, udhwkz, 623K views, 17.9x. A family-disaster continuation part that starts mid-story. Off-niche.
- `BciSW_2VMZg`, WrONG Rules "New Household Rules (Pt3?)", 104K views, 11x, 50 s. A short rules list. A good micro-format (under 60 s), but there was too little text to make the 12.

## Caveats

- Every TikTok source is a **translated repost of Chinese 2D animated series**. The narration is machine-translated English with TTS, so whisper renders names phonetically (Xiaowu/Shaowu, Zhang Bo, Du Mei).
  - Use them for structure and devices only. Never reuse their stories, names or lines; BRIEF hard rule 5 applies.
  - Run the originality gate against this folder.
- Whisper segment timestamps are the start of each spoken segment, accurate to about ±0.5 s. Chat-video timestamps are the second each bubble first appears in the 1 fps sampling.
- The WrONG Rules channel tags some uploads with stablediffusion and midjourney. Only the script structure is used here.

## Expansion (12:08 UTC)

Added 2026-11-01, about 12:08 to 12:20 UTC: 13 more transcripts (12 outliers plus 1 marked control), all from channels that are not among the first 12 sources except two Wansee/Shorts-format picks noted below. Same rules as above: every listing, download, subtitle pull, whisper run and frame sample ran on the Spark CPU (`CUDA_VISIBLE_DEVICES=""`, `nice -n 10`, whisper `cpu_threads=4`, ffmpeg `-threads 2`). Only text is on the Mac.

- **Pool.** The library (`research/library/library.json`, `candidates-horror.json`), `research/daily/latest.md` (11:08 UTC run), R2's channel listings (`dgx-spark:~/studio/refs/R2/meta/`) and the corpus search listings, plus two new YouTube searches ("scary text message story #shorts", "horror rules animated #shorts") and fresh channel listings for Luke Davidson, Mr. Nightmare, Llama Arts, Lighthouse Horror, Texty Stories, NightProtocol and Wansee Shorts. Working folder: `dgx-spark:~/studio/refs/corpus_horror/x2/` (`meta/`, `subs/`, `wh/`, `vid/`, `frames/wh9/`, scripts `dl.sh`, `subs.sh`, `whisper_np.py`).
- **Outlier score.** Same definition: views / median views of that channel's recent uploads in the same tab (Videos, Shorts or TikTok). Each header names the median used.
- **Transcripts.** YouTube auto-subs (`en-orig` VTT, cleaned with `tools/vtt2lines.py`, HTML entities and `>>` speaker marks stripped) for every YouTube video that had them; creator-uploaded captions for the Llama Arts video; faster-whisper `small` on CPU (int8, 4 threads, VAD, audio passed as a numpy array) for the TikToks and the no-subs YouTube video; bubble-by-bubble reading of 2 s contact sheets for the silent Texty Stories chat. Builder: `dgx-spark:~/studio/refs/corpus_horror/x2/build_x2.py` (with the hand-read chat in `manual_wh9ESTS69Dk.txt` next to it; it reuses `tools/vtt2lines.py` and writes the same two header lines as `tools/build_raw.py`).
- **Not done here.** No `sheets/` overview JPGs, no INDEX.json entries and no line-by-line annotation for these yet.

| # | id | channel | role | views | outlier | dur | transcript source |
|---|---|---|---|---|---|---|---|
| 13 | [wh9ESTS69Dk](https://www.youtube.com/watch?v=wh9ESTS69Dk) | Texty Stories | outlier | 248,728 | **165.8x** | 6:18 | on-screen chat (visual, 2 s frames) |
| 14 | [8bo9yZvedUM](https://www.youtube.com/watch?v=8bo9yZvedUM) | Luke Davidson | outlier | 16,247,875 | **34.1x** | 10:21 | VTT |
| 15 | [7650872317119057168](https://www.tiktok.com/@melovebz/video/7650872317119057168) | melovebz | outlier | 134,400 | **23.8x** | 9:26 | whisper |
| 16 | [gDNMSoGSZgQ](https://www.youtube.com/shorts/gDNMSoGSZgQ) | The Story Vault | outlier (Short) | 19,845 | **19.8x** | 0:59 | VTT (whisper-checked) |
| 17 | [kJCVK8xTkPk](https://www.youtube.com/watch?v=kJCVK8xTkPk) | Resident Guidance | outlier | 13,473 | **17.4x** | 5:14 | VTT |
| 18 | [7659482056656735521](https://www.tiktok.com/@lehwh7/video/7659482056656735521) | lehwh7 | outlier | 1,900,000 | 11.2x | 9:45 | whisper |
| 19 | [x--ui6_mAxE](https://www.youtube.com/shorts/x--ui6_mAxE) | Wansee Entertainment | outlier (Short) | 141,758 | 9.5x | 0:15 | VTT |
| 20 | [shTJ7_kRNJ8](https://www.youtube.com/watch?v=shTJ7_kRNJ8) | NightProtocol | outlier (1 day old) | 3,201 | 7.6x | 10:33 | VTT |
| 21 | [02nCBx8WqW0](https://www.youtube.com/watch?v=02nCBx8WqW0) | Llama Arts | outlier | 11,900,854 | 6.4x | 4:46 | creator captions |
| 22 | [6WfCF7KsLaQ](https://www.youtube.com/watch?v=6WfCF7KsLaQ) | Horror Shorts Party | outlier | 1,282,475 | 5.1x | 5:25 | whisper (no subs) |
| 23 | [hPWu7UAovxk](https://www.youtube.com/watch?v=hPWu7UAovxk) | Mr. Nightmare | outlier | 5,034,624 | 5.0x | 9:21 | VTT |
| 24 | [cWgSgd-QcOY](https://www.youtube.com/watch?v=cWgSgd-QcOY) | Lighthouse Horror | outlier | 505,355 | 2.6x | 22:06 | VTT |
| C1 | [FDLk6TlVTq0](https://www.youtube.com/watch?v=FDLk6TlVTq0) | Resident Guidance | **CONTROL** | 1,088 | 1.4x | 5:35 | VTT |

### Why each was chosen

13. **wh9ESTS69Dk: "My DEAD DAUGHTER Texted Me".** The biggest ratio in the pool. The score is against a quiet recent window (1,500 median, 2026 uploads); this 2023 upload is still the channel's top video by far.
    - A silent iMessage recording, about 116 bubbles in 6:18, so roughly one bubble every 3 s with the typing animation shown. Slower than Textify (one per second) and still a hit.
    - Beats: lock-screen notification "Hello mommy", denial ("My daughter died two years ago"), escalating ALL-CAPS warnings, "Please open the door", "I'm outside" while the door is empty, a photo bubble of the empty doorway, a chat-switch to the husband ("Not this again"), and the payoff that the whole Unknown thread has vanished.
    - The vanishing-thread ending and the switch to a second chat are pure chat-UI devices our chat kit can do.
14. **8bo9yZvedUM: Luke Davidson, "THE SCARIEST TEXT CHAT EVER!!!"** 16.2M views, 34x. A creator reads a 3 a.m. home-alone text chat aloud (little brother home alone, older brother at a party, someone in the house) and stops to react.
    - Useful for which chat lines a narrator chooses to dwell on, and for the "don't tell Mom" guilt lever that keeps the victim from calling for help.
    - The reaction asides are not part of the story; skip them when measuring pacing.
15. **7650872317119057168: melovebz, fake-human roommate.** 23.8x. A 2 a.m. noise (pages turning) leads to an online stranger ("Exorcist") who says the roommate is a fake human cramming language before eating him.
    - The online helper is the authority figure. The hero blocks him, unblocks him at the next scare, and the tells (clothes inside out, wrong words) build the case.
    - It shares a template with #18, which suggests the format travels across reposting accounts.
16. **gDNMSoGSZgQ: The Story Vault Short, "Never kill your own dog".** 19.8x on the Shorts tab, 59 s.
    - It opens on a rule in the first 2 s ("we kill a dog every New Year's... never kill your own dog"), breaks it by 0:05, has a dying-whisper prophecy, then a hide-in-the-stove instruction from Grandma.
    - The ending is a "Dad" voice at the door ("open the door, it's Dad"), which is our fake-authority-at-the-door beat squeezed into under a minute.
17. **kJCVK8xTkPk: Resident Guidance, "If Your Neighbour Waves from Two Different Windows… Only Wave Once".** 17.4x. The closest match to our building-rules premise in the whole pool.
    - A cold-open scene (two windows, same neighbor, both waving) and then "There are five rules", each one tied to a mundane chore (keys, shopping, the milk in the fridge).
    - Calm second-person narration over still illustrations, which is exactly our code-only look. It ends on a softer re-hook ("They may not be waving at you").
18. **7659482056656735521: lehwh7, "teeth grinding monster".** 1.9M views, 11.2x. It was dropped from the first 12 for running 9:45; it's here as the long-form TikTok example.
    - A 2 a.m. sound outside the door for three nights, then an online stranger ("TimeHunter") explains the rules (seven days of grinding, then it eats you; it disguises itself as someone close).
    - Trust flips between Grandpa and Dad ("he doesn't have a shadow"), and a neighbor in apartment 503 hands over a protective pendant.
19. **x--ui6_mAxE: Wansee Short, "I gave her a ride, but she was....."** 9.5x on Wansee's Shorts tab. It's on an existing channel but in a format the first 12 lack: a 15 s, 4-line micro-story that ends on a smile. It shows the minimum viable horror Short.
20. **shTJ7_kRNJ8: NightProtocol, "If Everyone On The Night Bus Stands Up At Your Stop… STAY SEATED".** 7.6x, uploaded the day before collection, so the score is still rising.
    - The cold open states the rule and then three don'ts in 10 s. It promises "seven rules, and remember rule number four, it's the one almost everyone breaks" (an explicit open loop), and it's labeled "Night protocol file 015" (series framing).
    - It ends with a text message from the friend who got off ("Same bus tonight. I told them you're coming").
21. **02nCBx8WqW0: Llama Arts, "Disturbing True Snapchat Stories Animated".** 11.9M views, 6.4x on a 1.85M-median channel.
    - A gym stranger gets the narrator's Snapchat. Each removal or block is answered by a new snap ("why did you remove me?", then a re-add from a new account), so the phone escalates on every beat.
    - It ends with an unresolved worry ("any time somebody new adds me... I'll never know").
22. **6WfCF7KsLaQ: Horror Shorts Party, "TRUE OMEGLE CHAT ROOM HORROR STORY".** 1.28M views, 5.1x. No subs, so whisper.
    - A stranger on video chat says he is deaf, types in the chat box, then switches to a whiteboard because "my hands will be occupied" ("wanna play a game?").
    - It's the best example in the pool of a chat-box UI as the main stage inside a narrated 2D story.
23. **hPWu7UAovxk: Mr. Nightmare, "3 Text Conversations with Creepy Backstories".** 5M views, 5.0x on a 1M-median channel.
    - The structure is to read the real-looking texts first (a girl hiding in a closet texting Mom) and then tell the backstory that makes them scary. One story ends with texts sent from a family member's phone by someone else.
    - It's the clearest model for a screenshots-then-reveal format, and it's three stories in one.
24. **cWgSgd-QcOY: Lighthouse Horror, "11 Rules For Idiots Who Bought A Haunted House".** 2.6x on a 192K-median channel. It's long (22 min) and is here as the long-form rules example.
    - A sarcastic second-person host gives a numbered list framed as advice to the viewer. A friend ("Nathan") is the cautionary example, and it ends with a threat to the viewer ("I have a really good software for tracing IPs").
- **C1. FDLk6TlVTq0: CONTROL.** Resident Guidance, "If the Pigeons Outside Your Building Stop Moving… Don't Feed Them", 1,088 views (1.4x). It uses the same narrator, the same five-rules template and the same length as #17.
    - Compare the two to see what the outlier does differently: a human double rather than an animal, a cold open that puts the viewer in the act (waving), and a title that names an action to take.

### Caveats (expansion)

- #15, #16 and #18 are translated Chinese animation reposts like the TikTok seeds. BRIEF rule 5 applies: borrow structure and devices only.
- #14 includes the creator's reaction asides mixed into the chat reading, and #24 includes channel intro and outro talk. #17, #20 and C1 auto-subs contain `[music]` tags.
- The TikTok view counts are yt-dlp's rounded figures (1.9M, 134.4K). The melovebz account's display name is "mystoriess".
- The #13 timings are the first 2 s frame where each bubble appears (+-2 s). Speaker labels: MOM = blue bubbles (phone owner), UNKNOWN and BABE = grey bubbles.
