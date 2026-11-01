---
id: horror-delivery-photo-inside
niche: horror
title: My Delivery Driver Won't Leave Until I Rate Him 5 Stars
alt_titles: The Delivery Photo Was Taken From Inside My Apartment | "Left At Door" (The Photo Was From Inside)   # ranked list + A/B plan in titles.md
format: 9:16 Short, single (standalone), chat + delivery-app screens
target_runtime_s: 84.1 (window 80-90; never under 61 for Creator Rewards)
measured:                    # every number below is computed by build.py from per-line Kokoro durations measured on the Spark CPU
  timing_source: "Kokoro-82M on the Spark CPU, measured per line (tts_measure.py -> tts_durations.json), 5 voices"
  runtime_s: 84.13           # 66.4 s speech + 11.0 s planned silence + 6.7 s breaths between lines
  words: 276                 # narrator 198, driver 33, support 22, restaurant 17, sister 6
  wpm_speaking: 249          # PLAYBOOK narrated 230-270 / chat 250-275: in band
  wpm_overall: 197           # below band on purpose: 11 s of silence (13% of runtime) is the scare budget
  sentence_median: 5         # narrator 6; narrator punch share (<=4 words) 26%, all voices 41% (chat bubbles)
  you_sentence_share: 0.065  # 3 of 46 sentences (driver, app, timer); first-person narrated band 3-13%
  numbers_distinct: 9        # 9:00, 9:41, fourth, five, 911, 10 ft, six, fifteen, 1,201 = 6.4/min
  line1: "9 words; danger word 'inside' at 1.6 s"
  core_hook: "12 words / 3.4 s"
  first_contradiction_s: 5.4 # support confirms 'inside unit'
  jolts: "37; median gap 2.1 s; longest 5.8 s"
voices:                      # lines.py VOICES; distinct voice per speaker so audio-only viewers can follow
  narrator: af_heart @1.30
  driver_Teo: am_michael @1.15   # also reads the final review (voice swap). am_puck preferred but not cached on the Spark
  support: af_sky @1.25
  sister_Mia: af_nicole @1.25
  restaurant: bm_george @1.20
  app_system_text: on-screen only + UI chime (never spoken)
music: dread
template: pipeline/templates/horror.md (Chat thread + Locked-door siege, standalone)
build: lines.py (source) -> tts_measure.py (Spark) -> build.py -> timeline.json + storyboard.json
references:
  - id: T42u5xhrq-0
    url: https://www.youtube.com/shorts/T42u5xhrq-0
    views: 868500
    outlier_score: 25.54
    why: "TEXT-FIGURE, the corpus's 60 s phone-screen Short and the closest format. Borrowed: the stand-in who voices the viewer's rational denial (0:34-0:35) and the obvious-fix-then-it-fails beat (0:25-0:27), now our sister Mia; the turn into the hero's own space (0:31, 52%); the CAPS rung (0:37) then calm lowercase from the entity (0:50-0:56); the distance countdown (0:38-0:47) run as a live floor-plan icon; the unanswered name-check silence right before the proof image (0:53, 88%); the second-image-as-proof (0:54, 90%; ours is a second proof photo after a silence, not a single held-back image); the voice swap where the victim's own channel speaks as the entity (0:56-0:58). Different danger, cast, wording and ending."
  - id: 7659677578365537569
    url: https://www.tiktok.com/@udhwkz/video/7659677578365537569
    views: 376200
    outlier_score: 10.79
    why: "SIEGE-CHAT. The template for an official channel that sounds reassuring but is the weapon. Borrowed: the official all-clear inside the hook (0:06-0:11); the near-compliance hesitation (0:16); the count match (plant 0:19 -> payoff 0:28), here 1,206 deliveries vs 1,200 ratings paid by support at the turn; authority pushing compliance (0:39-0:52, 1:43-1:51); channel removal where only the enemy channel still works (2:03-2:13); the real authority getting through for a few seconds under a visible clock (3:17-3:41) and killing the fake one (3:58-4:01), here the restaurant: 'no driver named Teo'. No killer, no fake cop, no group chat, no burner."
  - id: Qz-TrB6W2SM
    url: https://www.youtube.com/watch?v=Qz-TrB6W2SM
    views: 1521857
    outlier_score: 9.01
    why: "HOTEL-DOOR, the only corpus hit about a service worker who is not what he claims. Borrowed: the title stating the incident (H12); the polite -> silence -> shouted volume ladder (1:28-1:39); a checkable logical tell (1:42-1:47), here a timeline (chain on at 9:00, photo at 9:41); the retreat to a smaller locked room (1:57); the retro-reveal after a false safety that scales beyond us (2:28-2:30); a silent background plant paid later (0:05/1:15 -> 2:25-2:28), here a delivery-jacket sleeve in the hall mirror that recurs in one review thumbnail; and the bookend return to the opening location with a figure added (2:40-2:48), here the opening door framing that turns into his photo of her."
pattern_citations:           # PLAYBOOK patterns cited by tag, not added as references
  - "T3 rule inversion (PLAYBOOK 4B; DORM-RULES 7670495663624408352)"
  - "T11 fake win (PLAYBOOK 4B; TRUCKER-RULES 7692268145888873760)"
  - "T1 fake authority, T2 count match, T6 voice swap, T8 retro-reveal (PLAYBOOK 4B)"
originality_check: PASS      # python3 scripts/originality_check.py on this file, see review.json
---

# My Delivery Driver Won't Leave Until I Rate Him 5 Stars

**Premise.** My food app marks the order "Left at door". The proof photo shows my front door from the
inside, with the chain on. I put that chain on at 9:00, and the photo was taken at 9:41, so whoever took it
was already in my apartment when I locked up. App support calmly confirms the driver's location: "inside
unit". The driver, Teo, says he will head out once I rate him five stars, and the app's own rule says drivers
can't leave until the order is rated. His icon moves across a floor plan of my home. I lock myself in the
bedroom. Then support says the quiet part: six customers never rated him, and he's still delivering to them.
A new proof photo arrives: me on my bed, taken from behind me. Under a 15-second clock the restaurant gets
through: my food is still on their counter, and they have no driver named Teo. I give him five stars anyway.
His icon vanishes. His profile shows 1,201 reviews, every photo a front door from the inside, and the newest
was posted from my account in his voice: "She thinks I left." Down the hall, the chain is still on. Ping: a
new proof photo, me looking at the chain, taken from behind me.

**Ownable rule / signature.** "Drivers can't leave until the order is rated" plus "rate me five stars and I'll
head out". The viewer tracks one question: will rating make him go?
- **Turn (T3, 48%).** Her protective act so far (not rating) is shown to be the trap: the six who never rated
  still have him. Support's line is the count match that pays the header plant (1,206 deliveries, 1,200
  ratings) out loud.
- **Twist (T6 + T8, 95%).** Rating was a trap too. It only makes you think he left.

**Mechanism (settled).** The app is the entity. Support's calm voice, the 911 call that bounces back to the
stars ("The app had taken my phone") and the restaurant's "no driver named Teo" all point the same way. Nobody
"came in" during the story: the chain timeline says he was inside before 9:00 and never left.

**Plants.**
1. Door chain + timestamp. On at 9:00, photo at 9:41 (0:07), paid at 1:21 ("the chain was still on" = he
   never went out).
2. Header stat "1,206 deliveries · 1,200 ratings" (0:12, with a 0.9 s punch-in). Paid as a count match at
   0:40 ("six customers never rated Teo"), then 1,201 reviews at 1:14 (+1 = hers).
3. The proof-photo device. Photo 1 (0:00), photo 2 of me (0:46), a gallery of them (1:14), and the final
   ping (1:23) that turns the bookend shot into his photo.
4. Silent: a green delivery-jacket sleeve in the hall mirror of photo 1. It is in one review thumbnail too.
   No VO, for rewatchers.
5. Wardrobe. Ajar behind her at 0:37 with a hinge creak under the lock click. It is the camera position of
   photo 2 (0:48) and is wider open at 1:13.

**Loops.**
- L1 who took the photo (0:00 -> 0:11 "already inside" -> 0:48 he is behind me).
- L2 is support real (0:05 -> 1:04 the restaurant has no driver named Teo).
- L3 will rating make him leave (0:14 -> 1:10 fake close -> 1:20 "She thinks I left", re-opened).
- L4 where is he (0:21 kitchen -> 0:35 hall -> 0:54 "closer than the map says" -> 1:23 right behind her, open).
- L5 what happened to the six and the 1,201 (0:40 / 1:14, open).

Early loops close before 50%. L4 and L5 are open at the cut: 2, the right count for a standalone.

## Pacing vs PLAYBOOK (measured)

| Metric | PLAYBOOK target | This script (Kokoro-measured) |
|---|---|---|
| Runtime | Shorts 50-100 s; chat hits peak ~60 s (§6) | **84.1 s** (trimmed from 89 s planned / ~111 s real for the last draft); over 61 s for Creator Rewards |
| Words / wpm | narrated 230-270, chat 250-275 (§7) | 276 words; **249 wpm speaking** (in band); 197 wpm overall because of 11 s of planned silence |
| Line 1 | <=12 words, place/object + danger | 9 words, "My delivery photo was taken from inside my apartment." Danger word at 1.6 s |
| Core hook | <=30 words, <=6 s; threat in frame 0 | 12 words / 3.4 s. Frame 0 = order card + inside-out door photo + red ring + burned "taken from INSIDE →" label |
| Trusted source contradicted | <=11 s | Support confirms "inside unit" at 5.4 s; the chain timeline proves it at 10.2-11.2 s |
| Jolt interval | median 6 s (Shorts 2.5-3.5), never >8 s | 37 jolts, median 2.1 s, longest gap 5.8 s |
| Viewer-proxy voice | required (§8) | Mia: "It's a glitch. Just rate him." (0:23), then her channel dies |
| Turn | 45-60% | Count match at 0:40 (**48%**) |
| Scariest image | once, 60-80% (corpus 47-82%), held ~4 s | Photo 2 lands at 0:48 (57%), then **held still 4.0 s** in silence, 0:49-0:53 (58-63%). It sits 2 points early so the clock and twist keep their slots |
| Lifeline under a clock | 70-90% | Real-time 15 s clock 0:56-1:10 (67-83%); restaurant line gets through 1:00-1:05 (72-77%) |
| Truth twist | 85-95% | Identity twist at 1:04 (76%, "no driver named Teo"); retro-reveal + voice swap 1:14-1:21 (88-96%) |
| Ending | hard cut at greatest need / threat turned on "you"; bookend first shot | Present-tense threat "She thinks I left." (95%), chain bookend (97%), final ping turns the opening framing into his photo of her (98%); hard cut, no CTA |
| Numbers / min | narrated 3-5, chat 0-1 | 9 distinct numbers = 6.4/min (counted once each, not per repeat) |
| Sentence median | 6-9 narrated, 4-5 chat; punches at spikes | 5 overall (narrator 6). Narrator punch share 26%, over the 13-22% narration band: punches kept at spikes ("I live alone." "So he was already inside." "Ten feet." "Taken from behind me.") |
| "You" share | first-person narrated 3-13% | 6.5% of sentences, all in the driver's, app's and timer's words |
| Silences | 1-3 timed with SFX, 3-8 s | 0.6 s fridge; 1.3 s unanswered "hello?/HELLO??"; **4.0 s** photo hold (heartbeat); **2.6 s** clock ticks; 0.9 s fake-win quiet; 1.6 s end hold = 11.0 s |

## Beat alignment (both sides as % of runtime)

| Our beat | Ours (s, %) | Reference id + timestamp (%) | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Hook: proof photo from inside | 0:00-0:03 (0-4%) | Qz-TrB6W2SM title + 0:00 (0%); T42u5xhrq-0 0:00-0:03 (0-5%) | The title states the incident; threat in frame 0, no intro | The title states the rule; line 1 states the photo; the cover label points at the chain |
| S2 Trusted source answers | 0:04-0:07 (4-8%) | 7659677578365537569 0:06-0:11 (2-4%) | The official channel's all-clear sits inside the hook | Support doesn't deny anything. It cheerfully confirms "inside unit", so the reassurance is the contradiction |
| S3 Tell | 0:07-0:12 (9-15%) | Qz-TrB6W2SM 1:42-1:47 (61-63%) | A checkable clue proves he is not what he claims | **Moved early.** The chain timeline (on at 9:00, photo at 9:41) proves he was inside before she locked up |
| S4 Rules | 0:12-0:16 (15-19%) | T42u5xhrq-0 0:15 (25%); 7659677578365537569 0:31-0:39 (12-16%) | A rule is stated, then authority pushes compliance | Driver: "rate me five stars and I'll head out"; app system line (on screen only): drivers can't leave until rated. The header stat is planted |
| B3 Near-compliance | 0:16-0:19 (19-22%) | 7659677578365537569 0:16 (6%); PLAYBOOK B3 | The hero nearly complies | Thumb on the fourth star; the fridge thump stops it |
| S5/S6 Threat crosses into my space | 0:19-0:22 (23-26%) | T42u5xhrq-0 0:31-0:33 (52-55%) | A sound, then "in my room" | **Moved early** (a Short with a second act): the map is my floor plan, the icon is in my kitchen |
| B6 Channel removal + proxy voice | 0:22-0:31 (26-37%) | T42u5xhrq-0 0:25-0:27, 0:34-0:35 (42-58%); 7659677578365537569 2:03-2:13 (49-53%) | The stand-in voices the rational fix; familiar UI failure; only the enemy channel works | Mia's "just rate him" (the viewer's own thought), then "Not delivered"; 911 bounces to the stars; "The app had taken my phone" makes it a rule |
| S7 Volume + proximity ladders | 0:31-0:37 (37-44%) | Qz-TrB6W2SM 1:28-1:39 (52-59%); T42u5xhrq-0 0:37-0:47 (62-78%) | Polite -> curt -> CAPS; distance shrinks rung by rung | "just one tap :)" -> "I've been very patient." -> "RATE ME"; icon kitchen 30 ft -> hall 10 ft |
| B5 Barrier retreat | 0:37-0:39 (44-47%) | Qz-TrB6W2SM 1:57 (70%) | Retreat to a smaller locked room | Bedroom door locked; the wardrobe behind her creaks (plant for photo 2) |
| B8 Turn: rule inversion + count match | 0:39-0:43 (47-52%) | PLAYBOOK T3; 7659677578365537569 0:19 -> 0:28 (8-11%) count match; 1:43-1:51 (41-44%) authority | The protective act is the trap; a planted count pays off; the top authority pushes compliance | "Six customers never rated Teo. He's still delivering to them." Not rating = he stays. 1,206 - 1,200 = 6 flashes on screen |
| S8 Silence beat | 0:43-0:45 (52-53%) | T42u5xhrq-0 0:53 (88%) | Two unanswered name checks before the proof | "hello?" "HELLO??" to support, no typing dots, 1.3 s |
| S9/B9 Scariest image, held | 0:45-0:53 (53-63%) | T42u5xhrq-0 0:54 (90%); PLAYBOOK B9 (~4 s held) | Image used as proof after a silence | A second proof photo: me on the bed, from the wardrobe corner. Tight on "Me, on my bed", snaps wide on "Taken from behind me", then **4.0 s** perfectly still |
| B9b Tracker lie + calm register | 0:53-0:56 (63-67%) | T42u5xhrq-0 0:50-0:56 (83-93%) typography ladder | After CAPS, calm lowercase from the entity is the scariest register | "The map still said hallway." (said aloud, so audio-only viewers get it) + "i'm closer than the map says." |
| B10 Lifeline under a clock | 0:56-1:10 (67-83%) | 7659677578365537569 3:17-3:41 (79-89%), identity twist 3:58-4:01 (96%) | A real authority gets through on a failing line under a visible countdown and kills the fake authority | The 15 s clock ticks in real time; the restaurant gets 5 s: food still on the counter, "no driver named Teo"; call ends; 2.6 s of ticks; she rates at 0:02 without turning around |
| B12-style fake win | 1:10-1:14 (84-88%) | PLAYBOOK T11 (TRUCKER-RULES 7692268145888873760) | Relief beat | Icon vanishes, "Delivery complete. Thank you!", 0.9 s quiet, relieved face (the wardrobe is wider open) |
| B11 Retro-reveal + voice swap | 1:14-1:21 (88-96%) | Qz-TrB6W2SM 2:28-2:30 (88-89%); T42u5xhrq-0 0:56-0:58 (93-97%) | After safety it was worse and not just us; the victim's own channel speaks calmly as the entity, turned on the listener | 1,201 reviews, every photo a door from inside; the newest from my account, read in **his** voice: "She thinks I left." |
| B12 Bookend + cut | 1:21-1:24 (97-100%) | Qz-TrB6W2SM 2:40-2:48 (95-100%); 7659677578365537569 4:00 (96%) | Return to the opening location with a figure added; the planted identifier pays off | The 0:03 door framing, chain still on; a ping turns it into a new proof photo ("✓ Delivered to customer · 9:58 PM") with her silhouette in the foreground: his photo, taken from behind her. Hard cut |

Restructure note: S3 and S5/S6 run earlier than in their sources (12% and 23% vs 61% and 52%). A Short
that has a lifeline act needs its first proof and its "inside my space" rung in the first quarter. The turn
(48%), image (57-63%), clock (67-83%) and twist (88-96%) stay inside the PLAYBOOK bands.

## Script

**Hook.**
- First line (VO + caption, 0:00.1): "My delivery photo was taken from inside my apartment."
- First visual (frame 0, also the cover): a static phone with the fictional "bites" app (violet, not any real
  brand's colours). The order card shows a green "✓ Left at door · 9:41 PM" and a big white-bordered proof
  photo: the inside of a front door, warm hall light, coat hook, and the chain hooked across. A pulsing red
  ring sits on the chain, with a burned-in red label "taken from INSIDE →".

Voice markup: `[voice: x]` marks the speaker for the multi-voice build. `pipeline.audio.make` is single-voice
today, so the shipping audio is the per-line Kokoro wavs from `tts_measure.py`, which `storyboard.json` places
directly (`audio.voice`, one clip per line, `duckOn: voice`). `||` = timed silence.

```narration
[0:00.1 | S1 HOOK] [music: dread]
[voice: af_heart] My delivery photo was taken from inside my apartment. [sfx: notify]
I live alone. [sfx: stinger @0.05 vol=-8]

[0:03.8 | S2 TRUSTED SOURCE ANSWERS]
[voice: af_sky] Driver verified! Location: inside unit. Anything else today? [sfx: message_pop] [sfx: glitch @1.15 vol=-4]

[0:07.2 | S3 TELL: THE CHAIN IS A TIMELINE]
[voice: af_heart] In the photo my chain is on, and I put it on at nine. The photo says nine forty-one.
So he was already inside. [sfx: impact vol=-10]

[0:12.5 | S4 RULES]
[voice: am_michael] Hi! Your order's by the door. Rate me five stars and I'll head out. [sfx: message_pop]
(on screen only, UI chime: "Drivers can't leave until the order is rated.")

[0:16.1 | B3 NEAR-COMPLIANCE + PROXIMITY RUNG 1]
[voice: af_heart] My thumb was on the fourth star when my fridge door thumped shut. [sfx: impact vol=-3] [pause: 0.6]
The map showed my apartment, and his icon was in the kitchen. [sfx: sonar_ping @0.9 vol=-6]

[0:21.9 | B6 CHANNEL REMOVAL + VIEWER-PROXY VOICE]
I texted my sister. [sfx: message_send]
[voice: af_nicole] It's a glitch. Just rate him. [sfx: message_pop]
[voice: af_heart] I typed, he's inside. Not delivered. [sfx: glitch @1.0 vol=-6]
I called nine one one, and it bounced me back to the stars. The app had taken my phone. [sfx: glitch @1.25 vol=-2]

[0:31.5 | S7 VOLUME LADDER]
[voice: am_michael] Just one tap. [sfx: message_pop]
I've been very patient. [sfx: message_pop]
Rate me! [sfx: phone_buzz]
[voice: af_heart] His icon slid into the hallway. Ten feet. [sfx: footsteps @0.3 vol=-12]
I locked my bedroom door and sat on the bed, facing it. [sfx: click @0.9] [sfx: door_creak @1.0 vol=-20]

[0:39.5 | B8 TURN]
[voice: af_sky] Sorry for the wait! Six customers never rated Teo. He's still delivering to them. [sfx: drone @2.0 vol=-6]
[pause: 1.3] (on screen: "hello?" ... "HELLO??", no reply) [sfx: message_send x2]

[0:44.8 | B9 SCARIEST IMAGE]
[voice: af_heart] Then a new proof photo. Me, on my bed, staring at my locked door. Taken from behind me. [sfx: notify] [sfx: stinger @"Taken"]
[pause: 4.0] [sfx: heartbeat_slow]
The map still said hallway.
[voice: am_michael] I'm closer than the map says.

[0:56.2 | B10 LIFELINE UNDER A CLOCK]
[voice: af_heart] Then a timer: rate in fifteen seconds, or your driver hands you the order in person. [sfx: clock_ticking vol=-8]
[voice: bm_george] Hi, it's Lucky Noodle. Your food's still on our counter. We don't have a driver named Teo. [sfx: phone_buzz @-0.35]
[pause: 2.6] [sfx: tick x3]
[voice: af_heart] I didn't turn around. I gave him five stars. [sfx: ding @end]

[1:10.3 | FAKE WIN]
His icon vanished, and the app said delivery complete. [pause: 0.9]

[1:13.7 | B11 RETRO-REVEAL + VOICE SWAP]
His profile had twelve hundred and one reviews. Every photo was a front door, from the inside. [sfx: whoosh @"Every"]
The newest came from my account.
[voice: am_michael] She thinks I left. [sfx: stinger]

[1:21.2 | B12 BOOKEND + CUT]
[voice: af_heart] Down the hall, the chain was still on. [sfx: notify @end+0.35] [pause: 1.6]
```

### Line-by-line timing and on-screen text (Kokoro-measured; start of each line)

| t | dur | Voice | VO / caption line | Beat | On screen |
|---|---|---|---|---|---|
| 0:00.1 | 2.54 | N | My delivery photo was taken from inside my apartment. | S1 | Order card: green "✓ Left at door · 9:41 PM"; proof photo of my front door from INSIDE, chain on; red ring on the chain; burned label "taken from INSIDE →" |
| 0:02.8 | 0.58 | N | I live alone. | S1 | Photo insert full-frame (white proof border, "9:41 PM"); sleeve in the hall mirror |
| 0:03.8 | 3.15 | Support | Driver verified! Location: inside unit. Anything else today? | S2 | Support chat. Me: "who took this photo?? I live alone". Support: "Driver verified ✓ Location: INSIDE UNIT. Anything else today? 🙂"; glitch + shake on "inside" |
| 0:07.2 | 3.71 | N | In the photo my chain is on, and I put it on at nine. The photo says nine forty-one. | S3 | Macro on the chain; Nora's suspicious glance; "9:41 PM" stamp punched in red. Captions show "9:00" and "9:41" |
| 0:11.2 | 1.04 | N | So he was already inside. | S3 | The real front door in the dark, chain on; RedText scrawl "ALREADY INSIDE" |
| 0:12.5 | 3.31 | Teo | Hi! Your order's by the door. Rate me five stars and I'll head out. | S4 | Driver chat header "Teo · ★5.0 · 1,206 deliveries · 1,200 ratings" (0.9 s punch-in); bubble; then system line (on screen only, UI chime) "Drivers can't leave until the order is rated." |
| 0:16.1 | 2.36 | N | My thumb was on the fourth star when my fridge door thumped shut. | B3 | Rating sheet ★★★★☆, touch ring on star 4; shake on the thump |
| 0:18.5 | 0.60 | — | *[silence 0.6 s]* | B3 | Nora frozen, looking toward the kitchen |
| 0:19.1 | 2.54 | N | The map showed my apartment, and his icon was in the kitchen. | B3 | Street map zooms into a floor plan (Kitchen / Entry / Hall / Bath / Bedroom, "you" dot in Bedroom); scooter icon in Kitchen; "Teo · 30 ft away" |
| 0:21.9 | 0.97 | N | I texted my sister. | B6 | Chat "Mia". Me: "someone took a photo INSIDE my place" |
| 0:23.2 | 1.76 | Mia | It's a glitch. Just rate him. | B6 | Mia: "it's a glitch lol. just rate him" |
| 0:25.2 | 1.69 | N | I typed, he's inside. Not delivered. | B6 | Me: "HE'S INSIDE" + "! Not delivered"; RedText flash "! NOT DELIVERED" |
| 0:27.1 | 3.99 | N | I called nine one one, and it bounced me back to the stars. The app had taken my phone. | B6 | Call screen "911 · Calling…" glitches into the rating sheet "Rate your driver ☆☆☆☆☆". Caption shows "911" |
| 0:31.5 | 0.92 | Teo | Just one tap. | S7 | Teo: "just one tap :)" |
| 0:32.5 | 1.07 | Teo | I've been very patient. | S7 | Teo: "I've been very patient." |
| 0:33.7 | 0.56 | Teo | Rate me! | S7 | Teo: "RATE ME" (red alert bubble); phone vibrates, shake. Caption "RATE ME." |
| 0:34.6 | 2.10 | N | His icon slid into the hallway. Ten feet. | S7 | Floor plan: icon slides Kitchen -> Hall, "Teo · 10 ft away" |
| 0:36.9 | 2.25 | N | I locked my bedroom door and sat on the bed, facing it. | B5 | Dark hallway (whip), then the bedroom: Nora on the bed, duvet over her lap, facing camera = facing her door; wardrobe ajar behind her (hinge creak under the lock click) |
| 0:39.5 | 3.96 | Support | Sorry for the wait! Six customers never rated Teo. He's still delivering to them. | B8 | Support bubble; on "Six" a 1.1 s card: "1,206 deliveries / 1,200 ratings / 6 never rated him" (red); heartbeat starts |
| 0:43.5 | 1.30 | — | *[silence 1.3 s]* | S8 | Me: "hello?" ... "HELLO??" (no reply, no typing dots) |
| 0:44.8 | 4.21 | N | Then a new proof photo. Me, on my bed, staring at my locked door. Taken from behind me. | B9 | Lock-screen banner "Proof of delivery updated"; photo 2, tight on her silhouette, snaps wide on "Taken": wardrobe-door edge at left, her back, her locked door ahead, "9:52 PM" |
| 0:49.1 | 4.00 | — | *[silence 4.0 s]* | B9 | Photo 2 held perfectly still; heartbeat 70 -> 92 bpm |
| 0:53.1 | 1.03 | N | The map still said hallway. | B9 | Floor plan: icon pulsing in Hall, "10 ft away" |
| 0:54.5 | 1.38 | Teo | I'm closer than the map says. | B9 | Teo, calm lowercase: "i'm closer than the map says." |
| 0:56.2 | 4.04 | N | Then a timer: rate in fifteen seconds, or your driver hands you the order in person. | B10 | Rating sheet: "Rate within 0:15 or your driver will hand you the order in person." Red timer drops one label per real second (0:15 at 56.2 ... 0:01 at 70.2) |
| 1:00.5 | 4.87 | Restaurant | Hi, it's Lucky Noodle. Your food's still on our counter. We don't have a driver named Teo. | B10 | In-app call card "Lucky Noodle · restaurant" over the sheet, timer still running under it; then "Call ended" |
| 1:05.5 | 2.60 | — | *[silence 2.6 s]* | B10 | Push-in on the timer; ticks only (0:06 -> 0:04) |
| 1:08.1 | 2.00 | N | I didn't turn around. I gave him five stars. | B10 | "I didn't turn around": the wardrobe-corner view of her back, live; then all five stars fill gold at 0:02, tap ripple, ding |
| 1:10.3 | 2.32 | N | His icon vanished, and the app said delivery complete. | T11 | Floor plan: icon shrinks away; green "✓ Delivery complete. Thank you!" |
| 1:12.8 | 0.90 | — | *[silence 0.9 s]* | T11 | Relieved face; the wardrobe behind her is wider open (no VO) |
| 1:13.7 | 4.58 | N | His profile had twelve hundred and one reviews. Every photo was a front door, from the inside. | B11 | Profile "Teo · ★5.0 · 1,201 reviews"; 2x3 grid of door photos from inside (6 tints, chains on, one with the mirror sleeve) scrolls up |
| 1:18.5 | 1.17 | N | The newest came from my account. | B11 | Top review card: "Nora R. · just now · ★★★★★" with my door photo |
| 1:19.9 | 0.96 | Teo | She thinks I left. | B11 | Review text types out in my account: "She thinks I left."; glitch, stinger |
| 1:21.2 | 1.30 | N | Down the hall, the chain was still on. | B12 | The 0:03 door framing, chain on, flicker |
| 1:22.5 | 1.60 | — | *[silence 1.6 s]* | B12 | Ping at 1:22.9: a camera flash and the frame becomes a proof photo, white border, "✓ Delivered to customer · 9:58 PM", her silhouette in the foreground. Hard cut at 1:24.1 |

## Shot list (storyboard.json, 16 scenes, all renderable today)

Every scene uses only components the horror kit registers now, plus core `rect` / `circle` / `text` / `svg`
layers. The delivery-app screens (order card with photo inset, street map -> floor plan with a keyframed
scooter icon, rating sheet with a per-second timer, profile grid, review card) are drawn from core layers on a
**static** phone frame, so the photo inset never drifts against HandPhone tilt or tremble. Chats and calls use
`horror/HandPhone`. The from-behind figure, bedroom door, duvet and wardrobe edge are inline SVG layers in the
storyboard. Holds: every shot is 3 s or less except photo 2 (the planned 4 s still; `check_storyboards.py`
max hold 5.1 s, from "Taken" to the cut). Spark stills checked: `out/stills/horror-delivery-photo-inside_v1.jpg`,
`_v2.jpg`, `_v3.jpg`.

| Scene | t | Visual | Camera / cut | SFX |
|---|---|---|---|---|
| s01_hook | 0.0-3.75 | Frame 0 = cover: static phone, bites order card, white-bordered FrontDoor photo inset (chain on, hall light, mirror with green sleeve), pulsing red ring on the chain, red "taken from INSIDE →" label. Hard cut at 2.85 to the photo full-frame | push 1.00 -> 1.05; after the cut, push 1.0 -> 1.14 toward the chain | notify, stinger |
| s02_support | 3.75-7.22 | HandPhone "Bites Support" chat over a blurred LivingRoom; Glitch on "inside" | punch to the bubble 1.04 -> 1.22, shake | message_pop, glitch |
| s03_tell | 7.22-12.51 | Photo macro on the chain (zoom 1.6-1.75) -> Nora suspicious (LivingRoom) -> photo with a red "9:41 PM" stamp -> the real FrontDoor in Darkness + RedText "ALREADY INSIDE" | three step cuts, shake on "So" | impact |
| s04_rules | 12.51-16.15 | HandPhone "Teo" DM, header "★5.0 · 1,206 deliveries · 1,200 ratings"; bubble; system line | punch-in on the header 1.2-2.6 s (plant) | message_pop |
| s05_kitchen | 16.15-21.87 | Rating sheet ★★★★☆ with a touch ring on star 4 -> thump: Nora shocked (LivingRoom) -> street map zooms into the floor plan, icon in Kitchen, "Teo · 30 ft away" | shake on the thump; drift toward the kitchen | impact, sonar_ping |
| s06_mia | 21.87-27.15 | HandPhone "Mia" chat; typing dots; "HE'S INSIDE"; "! Not delivered"; RedText flash | slow push, shake | message_send, message_pop, glitch |
| s07_911 | 27.15-31.46 | HandPhone call "911 · Calling…" -> glitch -> rating sheet "Rate your driver" | glitch transition in, shake on "bounced" | glitch x2 |
| s08_ladder | 31.46-36.90 | Teo chat: "just one tap :)", "I've been very patient.", red "RATE ME" (vibrate) -> floor plan, icon Kitchen -> Hall, "10 ft away" | shake 20 px on RATE ME | message_pop x3, phone_buzz, footsteps |
| s09_bedroom | 36.90-39.46 | Hallway (lights 1, flicker) -> Bedroom (lamp 0.15, wardrobeOpen 0.22) + Nora scared, phone light + duvet foreground | whip in; small shake on the lock | click, door_creak (-20 dB) |
| s10_turn | 39.46-44.82 | Support chat; 1.1 s stat card on "Six" (1,206 / 1,200 / red "6 never rated him"); "hello?", "HELLO??"; Heartbeat from "Six" | slow push 1.0 -> 1.16 | message_pop, drone, message_send x2 |
| s11_photo2 | 44.82-53.13 | HandPhone lock screen + banner "Proof of delivery updated" -> photo 2: dimmed Bedroom, SVG bedroom door, phone-glow pool, SVG back-view silhouette, duvet, wardrobe-door edge at left, white border "9:52 PM", Vignette, Heartbeat | tight 1.3 on her back, **snap wide on "Taken"**, then no move for 5 s | notify, stinger, heartbeat_slow |
| s12_closer | 53.13-56.18 | Floor plan, icon pulsing in Hall -> Teo chat, calm lowercase bubble | step cut | message_pop |
| s13_clock | 56.18-70.33 | Rating sheet + red timer (one text layer per real second) + condition text; Lucky Noodle call card (ringing -> "0:03" -> "Call ended"); push-in on the timer during the ticks; 1.1 s cut to the wardrobe-corner view of her back on "I didn't turn around"; stars fill, tap ripple | push to the timer 1.45-1.5; step cuts; shake on the tap | clock_ticking, phone_buzz, tick x3, ding |
| s14_fakewin | 70.33-73.66 | Floor plan, icon shrinks out; green "Delivery complete" card -> Nora relieved, wardrobe wider (0.35) | slow pull-out | (music dip in the mix) |
| s15_reviews | 73.66-81.23 | Profile header "★5.0 · 1,201 reviews"; 2x3 door-photo grid (FrontDoor x6, liftColor tints, one with the mirror sleeve) scrolls up -> review card "Nora R. · just now" with a door photo -> typewriter "She thinks I left." + Glitch | push 1.0 -> 1.2 on the review | whoosh, stinger |
| s16_bookend | 81.23-84.13 | FrontDoor full-frame (same framing as the 0:03 insert), Darkness, Flicker, mirror; ping at 82.88: white flash, white border, "✓ Delivered to customer · 9:58 PM", back-view silhouette in the foreground | slow push, reset on the ping; hard cut | notify |

## Kit and pipeline needs

Nothing blocks a render. `npm run validate` (zod) passes on the Spark: 16 scenes, 84.17 s, 270 caption words.
`check_storyboards.py` on the Spark reports no missing components and no missing audio, because the per-line
wavs are in `studio/public/episodes/horror-delivery-photo-inside/vo/`. Nice-to-haves for reuse across episodes:
- `horror/DeliveryApp` as a kit component, a port of the core-layer screens in `build.py`, if a second
  delivery episode is made.
- Multi-voice support in `pipeline.audio.make` (`[voice: x]` markers), so this script could go through the
  standard mix and loudness chain instead of per-line clips plus `duckOn: voice`. Before posting, run the
  final render's audio through `pipeline.audio.mix` loudness normalisation (-14 LUFS).
- A red failed-send state for chat bubbles. A RedText flash covers it today.
- `am_puck` voice download (HF Kokoro-82M `voices/am_puck.pt`) if we want a lighter driver voice than
  am_michael.

## Originality notes

- No corpus premise reused: no killer, cop, building chat, taboo, cursed channel, hotel or children. The
  driver, support, the chain timeline, the floor plan, the rating rule, the six unrated homes, the restaurant
  call and the review gallery are ours.
- Devices borrowed (structure only): official reassurance in the hook, a checkable tell, near-compliance,
  count match, viewer-proxy denial, channel removal, the volume and distance ladders, the silence before the
  proof, the held image, a real authority under a clock, a fake win, the retro-reveal scale-up, the voice swap
  and the bookend with a figure added.
- Gate: `python3 scripts/originality_check.py backlog/horror/horror-delivery-photo-inside/script.md research/corpus research/library/transcripts` -> PASS (see review.json).
- Disclosure: this is fiction told in first person. Never call it true or real. On TikTok, turn on the
  AI-generated content label (synthetic voices). In the YouTube description: "Fictional story. Synthetic
  voices. All animation is original and drawn in code." "bites" and "Lucky Noodle" are invented, and the app
  UI avoids DoorDash red and the Uber Eats green/black card layout. Vary the kit's tints per episode so
  repeated template shots don't read as mass-produced.
