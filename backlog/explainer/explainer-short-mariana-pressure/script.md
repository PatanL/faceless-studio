---
slug: explainer-short-mariana-pressure
niche: explainer
format: short
aspect: "9:16"
title: "You Wouldn't Implode In The Mariana Trench"
title_alternates:
  - "What Happens To One Breath On The Way To The Mariana Trench"
  - "Your Breath vs The Mariana Trench"
title_formula: "Myth-bust title that names the expected outcome and denies it (PLAYBOOK section 5 'myth-bust on the famous one'); full ranked list in titles.md"
premise: "You take one breath and go straight down. Your air (shown as a bubble on screen) is the measuring stick: half at 10 m, a quarter at 30 m, a water bottle at 100 m, a shot glass at 1 km, a teaspoon at the bottom. Everyone expects you to implode. You don't: hollow, air-filled things implode, and you're mostly water. Separate from explainer-sinking-every-1000m (creatures and threats every 1,000 m) and from episodes/explainer-pressure-ladder (weight-on-your-thumbnail ladder, sky's-weight hook, Titanic/scuba-record rungs, fish-at-8 km twist). This script uses none of those beats: no thumbnail gag, no fish beat, no sky line in the VO, no Titanic, no scuba record."
variant: "Shorts skeleton PLAYBOOK 1b (S1-S7). PRESSURE's depth ladder extended by adding rungs (6 stops: 10 / 30 / 100 / 250 / 1,000 / 10,935 m), not by stretching each rung; PUFFER's turnstile, joke death and second act after the peak; DEEP's Everest-in-the-trench reveal at ~71% and its 'And yet' turn."
target_runtime_s: 75
target_runtime_range_s: [70, 78]
target_words_per_min: 195
measured:               # gen_storyboard.py --timeline (per-word estimate calibrated to the shipped am_michael voice; rerun on real captions after TTS)
  vo_words: 242
  vo_runtime_s: 74.9
  effective_wpm_incl_pauses: 194
  hook_words: 10        # "Hold your breath. Just ten metres down, your ears ache," spoken 0:00.1-0:03.1
  hook_s: 3.0
  first_you_word: 2
  first_rung_s: 1.4     # "ten metres" (the number); its mechanism and the x2 stamp land 0:03.5-0:06.7
  stops_s: [1.4, 11.7, 17.2, 26.3, 37.0, 50.2]   # 10 / 30 / 100 / 250 / 1,000 / 10,935 m
  sentences: 12         # chained clauses; avg 20 words (PLAYBOOK allows chained Shorts sentences)
  you_pct_sentences: 67 # target >= 60
  you_pct_words: 9.5    # target >= 5
  numbers_per_min: 7.2  # 9 spoken numerals; 8.8/min if "half" and "quarter" are counted (target 5-8)
  spoken_comparisons: 4 # water bottle, shot glass, teaspoon, Everest; every other scale image is on screen only
  turnstile_s: 34.4     # 46%
  peak_s: [48.1, 58.9]  # 64-79%
  twist_s: [59.7, 70.5] # 80-94%
  stinger_s: [71.1, 74.9]
voice: "Kokoro-82M am_michael (explainer default). Per-paragraph [speed:] markers (supported by pipeline/audio/script.py): 1.02 for the hook, rung 1 and the stakes line, 1.06 from 30 m, 1.0 for the stinger. Re-time every shot from the TTS word timings by rerunning gen_storyboard.py on captions.json; the shot times below are estimates."
music: "deep_ocean bed 0:00 to the turnstile, cut dead on 'part.'; underwater_rumble loop + dread bed from 1 km to the twist; deep_ocean again from the twist to the end (declared in storyboard.json audio.music)"
references:
  - id: fmZfphacPPQ
    short: PRESSURE
    url: https://www.youtube.com/watch?v=fmZfphacPPQ
    views: 14711279
    outlier_score: 1.84
    why_chosen: "Closest premise and format: a second-person descent down a depth ladder where each stop breaks a new part of the body. Borrowed: the H4 hook (small first number with 'just', 0:00-0:03) chained into a felt ear symptom (0:03-0:07); conjunction bridges between rungs ('and by the time', 0:07; 'and if you', 0:12; 'at around', 0:25); the 'somehow' hedge that concedes the premise (0:15); x-ray cutaways right after a number (0:12, 0:21); landmarks shown but not spoken (0:10, 0:27); the plant / partial / total payoff of one word (0:13, 0:26, 0:31). Not borrowed: its science ('lungs fill with blood', toxic gases on one breath, 'you implode'), which our twist corrects."
  - id: XFFjxTllpoA
    short: PUFFER
    url: https://www.youtube.com/watch?v=XFFjxTllpoA
    views: 7931305
    outlier_score: 1.69
    why_chosen: "PLAYBOOK's recommended Shorts skeleton for the 60-90 s slot. Borrowed: the body personified as fighting back (0:14); the one-clause mechanism with a plain verb (0:17-0:21); the 6-word ironic turnstile at 46% (0:27); death told only as a joke tied to an everyday object (0:36-0:39); a second act after the peak so the back third does not sag (0:43-0:52); ending on a fact with no CTA (0:55-0:59)."
  - id: mzeN0BXR4e0
    short: DEEP
    url: https://www.youtube.com/watch?v=mzeN0BXR4e0
    views: 17219766
    outlier_score: 12.86
    why_chosen: "Same place and the biggest views in the explainer corpus. Borrowed: the Everest-dropped-into-the-trench image as the peak scale reveal, at the same point in the runtime (13:02-13:07, 72% of 17:57; ours 0:52.9, 71%); the order 'maximum stakes, fatal to a human' (13:10-13:21) then the 'And yet' turn (13:21; DEEP uses 'And yet' about 7 times as its core engine), which here turns 'you're dead' into 'but you never imploded'. Not borrowed: DEEP's 'life thrives here' payoff (that snailfish beat belongs to pressure-ladder)."
secondary_device_citations:
  - "fGcgWaswMns (SPERM) ESC-3 'where it goes that you can't' (2:42-2:58), via PLAYBOOK section 4 capability dossier: the sperm-whale ribs line at 0:45.1"
evidence: "Insider Tech 'How Deep The Ocean Really Is' 83.6M; atomic marvel 'Human Body vs Implosion' 10.3M; BRIGHT SIDE 'What Happens to Your Body at the Mariana Trench Bottom?' 0.89M (backlog/explainer/TOPICS.md #12, backlog/explainer/evidence/mariana_trench_pressure_human_shorts.jsonl)"
fact_file: "section 'Fact sheet' below; every number and mechanism has a source; hedged claims are worded as hedges in the VO"
safety: "Framed as a thought experiment on screen from frame 0 (Tag 'THOUGHT EXPERIMENT: 1 BREATH, NO GEAR') and in the VO ('pretend you somehow still have air'). No gore: death is said only as 'extremely not alive', and the figure turns grey and lies down. 'Coughing blood' is a real freediving injury, said as 'can'; the x-ray shows a red tint, nothing else. The rib beat is a hedge ('something gives') over one flat white crack line in an x-ray card. No self-harm framing (PLAYBOOK section 10 safety box). Note: research/R5 is still empty, so there is no policy file to cite yet."
cta: none   # PLAYBOOK 6: 6 of 6 outlier Shorts end with no CTA
post_caption: "Which ocean myth should we bust next?"
---

# You Wouldn't Implode In The Mariana Trench

## Beat alignment table

Percentages are of our 74.9 s runtime and of each reference's runtime (PRESSURE 33 s, PUFFER 59 s, DEEP 1077 s).

| Our beat | Our time (%) | Reference id + timestamp (%) | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Hook | 0:00.1-0:03.1 (0-4%) | fmZfphacPPQ 0:00-0:07 (0-21%) | H4: a small first number with a minimiser ("just"), then a mild symptom almost everyone has felt (ears) | 10 words in ~3.0 s. "Hold your breath" sets the rule (one breath, no gear); the thought-experiment Tag is on screen from frame 0. Ends on a felt word ("ache"), and the head x-ray card shows the eardrum bowing |
| R1 10 m + mechanism | 0:03.5-0:06.7 (5-9%) | fmZfphacPPQ 0:07 (21%) conjunction bridge; XFFjxTllpoA 0:17-0:21 (29-36%) one-clause mechanism | No full stop between hook and rung; one 3-4 s mechanism in plain verbs | "because the pressure's doubled and squeezed your one breath to half" (11 words, 3.2 s). Plants "squeeze". The sky comparison is dropped (it is pressure-ladder's hook) |
| S2 Stakes / endpoint | 0:07.1-0:11.0 (9-15%) | XFFjxTllpoA 0:03-0:07 (5-12%) | A stakes number by ~10 s | One chained clause with the endpoint ("almost eleven kilometres below you"). The implode myth is planted on screen at 0:10.5 (Tag "EVERYONE SAYS YOU'D IMPLODE..."), the hook's contract (PLAYBOOK section 2). Everest is held back for the peak |
| Progress device | 0:00-1:14.9 | fmZfphacPPQ (a number per rung); mzeN0BXR4e0 1:40, 6:06 (lit band per zone) | Visible shape of the video | Log-scale depth meter on the left edge with 6 pins; each pin turns red and stamps the pressure multiple (x2, x4, x11, x26, x101, x1,072) on arrival. Breath bubble shrinks with the air volume |
| R2 30 m | 0:11.5-0:16.3 (15-22%) | XFFjxTllpoA 0:14 (24%) body personified | The body reacting, one notch worse | A quarter; the dive reflex slows the heart (ECG beats spread out); you stop floating and start falling. Ends on a comma into R3 |
| R3 100 m | 0:16.7-0:25.6 (22-34%) | fmZfphacPPQ 0:10-0:14 (30-42%) x10 number, organ change, x-ray after the number; fmZfphacPPQ 0:10 landmark shown, not said; fmZfphacPPQ 0:18 (55%) "even [something built for depth]" | Number re-hook, chest x-ray, visual-only landmark, an "even" authority line | Water bottle (spoken comparison 1). Blood shift replaces PRESSURE's wrong "lungs fill with blood". A ~96 m clock-tower silhouette stands beside YOU, never named. "even trained freedivers can come up from here coughing blood" |
| R4 250 m + hedge | 0:26.0-0:33.8 (35-45%) | fmZfphacPPQ 0:12-0:15 (36-45%) "and if you somehow kept going" | The "somehow" hedge that concedes the premise is impossible | Reality line: about the deepest anyone has gone on one breath (~253 m, 2012). Then "pretend you somehow still have air", so the viewer plays along instead of typing "you'd drown first" |
| S4 Turnstile | 0:34.4-0:36.0 (46-48%) | XFFjxTllpoA 0:27 (46%) | 6-word ironic false reassurance, background change on the next word | "Relax. That was the easy part." The music bed cuts on "part."; dipBlack into the black 1 km water |
| R5 1 km | 0:37.0-0:44.4 (49-59%) | fmZfphacPPQ 0:21 (64%) second x-ray; fmZfphacPPQ 0:26 (79%) planted word paid partly; fmZfphacPPQ 0:27 (82%) landmark shown, not said | x10 number, x-ray, honest hedge, partial payoff | "squeezed into a shot glass" (comparison 2, and the partial payoff of "squeeze"); ribs can't fold that small, "so something gives" (hedge); "you still haven't imploded" plants the twist word in the VO. Three stacked ~330 m lattice towers (~1 km) are shown, not named |
| R5b Sperm whale | 0:45.1-0:47.6 (60-64%) | fGcgWaswMns 2:42-2:58 (27-30%) "where it goes that you can't" (PLAYBOOK section 4 capability dossier) | You-vs-it contrast with an animal that really does this | "Sperm whales hunt down here with ribs built to fold." No "because": a folding chest is one adaptation among several (fact F12). This is a contrast line, not PRESSURE's "even" line |
| S5 Peak, the bottom | 0:48.1-0:58.9 (64-79%) | mzeN0BXR4e0 13:02-13:07 (72%) Everest in the trench; mzeN0BXR4e0 13:10-13:21 (73-74%) maximum stakes, "fatal to a human"; XFFjxTllpoA 0:36-0:39 (61-66%) death as a joke tied to an everyday object | Final number, the biggest landmark, the worst outcome as a joke | Bridged in with "Yours aren't, so by the time you reach the bottom". Your whole breath is one teaspoon (comparison 3). Everest dropped in beside you, peak still underwater (comparison 4, at 71%). The death is a callback joke: "extremely not alive since roughly the shot glass". Tonnes per cm² and x1,072 are on screen only |
| S6 Twist, myth-bust | 0:59.7-1:10.5 (80-94%) | mzeN0BXR4e0 13:21 (74%) the "And yet" turn from hostility to survival; fmZfphacPPQ 0:30-0:32 (91-97%) its "implode" payoff, inverted; XFFjxTllpoA 0:43-0:52 (73-88%) second act after the peak | Change axis after the peak; myth-bust of the famous version | Chained in: "...shot glass, and yet you never imploded." Pays off the 0:10.5 Tag and the 0:44 plant. Hollow + air implodes (a sealed can); you're basically a water balloon, so your flesh is only ~4% smaller |
| S7 Stinger | 1:11.1-1:14.9 (95-100%) | fmZfphacPPQ 0:13 / 0:26 / 0:31 plant, partial, total; XFFjxTllpoA 0:55-0:59 end on a fact, no CTA | The planted word paid off in full; a question answered in 4 words; cut on the last word | "And the biggest squeeze on your air? The first ten metres." The bar card makes clear it is about air volume (50% lost in the first 10 m, ~0.09% left at the bottom). The last frame is frame 0's layout (surface, YOUR AIR 100%), so the loop restarts on the same picture |

Pacing against PLAYBOOK sections 1b, 3 and 8:

| Check | Target | Ours |
|---|---|---|
| Hook | <=12 words, <=3 s, "you" in the first 10 words, subject on screen in frame 1 | 10 words, ~3.0 s, "your" at word 2; YOU, breath bubble, meter and thought-experiment Tag in frame 0 |
| First rung | <=8 s | number at 1.4 s, mechanism and x2 stamp by 6.7 s |
| Words/min | 180-230 (TTS) | ~194 incl. pauses |
| Rungs | add rungs, not length per rung; a new rung or number every 3-8 s | 6 stops (was 4); stops at 1.4 / 11.7 / 17.2 / 26.3 / 37.0 / 50.2 s; a spoken number or comparison at 1.4, 4.5, 6.4, 9.7, 11.7, 12.7, 17.2, 19.0, 26.3, 37.0, 39.5, 50.2, 51.9, 52.9, 69.6, 74.0 s |
| Explicit verbal re-hook | ~10 s | longest gap 6.2 s (re-hooks at 1.4, 3.5, 9.7, 11.7, 17.2, 22.7, 26.3, 32.2, 34.4, 37.0, 42.4, 45.1, 48.1, 50.2, 52.9, 56.6, 59.7, 65.2, 71.1, 73.7) |
| Conjunction chain | no full stop before the payoff | hook -> R1 -> stakes ("because", "and"); R2 -> R3 -> R4 ("and at a hundred", "and by two hundred and fifty"); R5 -> peak ("so by the time"); peak -> twist ("and yet"). Full stops only at the turnstile, the whale punch and the stinger question |
| Turnstile | 45-55%, 4-7 words | 46%, 6 words |
| Peak / spine | 55-75% / spine closes ~70% | peak 64-79%; spine ("do you implode?") closes at 80% |
| Numbers | 5-8/min | 7.2/min (9 numerals); 4 spoken comparisons, every other scale image on screen only |
| Plant -> payoff | 1 word paid twice | "squeeze": 0:05.1 planted -> 0:38.7 partial (shot glass) -> 1:11.9 total (stinger). "implode": 0:10.5 on screen -> 0:44.1 spoken plant -> 1:00.4 paid. "shot glass": 0:39.5 -> 0:58.4 callback joke |
| Comic deflation after the midpoint | every 4-6 s (comedy Shorts) | "pretend" 32.2, "Relax" 34.4, "Yours aren't" 48.1, "still underwater" 55.0, "extremely not alive" 56.6, MYTH stamp 60.6, "water balloon" 66.3 |
| "You" | >=60% of sentences, >=5% of words | 67%, 9.5% |
| CTA | none | none; the comment prompt is in the post caption only |

## Fact sheet

| # | Claim in VO / on screen | Value used | Source / note |
|---|---|---|---|
| F1 | Floor of the Mariana Trench "almost eleven kilometres" down | Challenger Deep ~10,935 m (on screen "10,935 M") | Greenaway et al. 2021 (Earth and Space Science) ~10,935 m; Five Deeps 2019 sonar ~10,925 m |
| F2 | Everest dropped in beside you, peak still underwater | 8,848.86 m; 10,935 - 8,849 = ~2,086 m of water above the peak (on screen "~2 KM") | Nepal-China joint survey 2020 |
| F3 | Pressure doubles at 10 m; multiples on the meter | ~1 atm per 10.06 m of seawater; x2 at 10 m, x4 at 30 m, x11 at 100 m, x26 at 250 m, x101 at 1 km, ~x1,072 at the bottom | NOAA Diving Manual (33 fsw = 1 atm) |
| F4 | Your breath: half at 10 m, a quarter at 30 m | Boyle's law V = V0 / P(atm abs) | Standard gas law; applies to the gas in a breath-hold diver's lungs, middle ear, sinuses |
| F5 | Ears ache by ten metres | Ear pain from ~1-3 m without equalising; eardrum rupture reported at pressure differences reached around 1.5-5 m | DAN ear barotrauma guidance; NOAA Diving Manual. "ache" is the mild claim |
| F6 | Breath = water bottle at 100 m; shot glass at 1 km; teaspoon at the bottom | ~6 L total lung capacity: /11 = ~0.55 L (bottle 0.5 L); /101 = ~59 mL (shot glass 44-60 mL); /1,072 = ~5.6 mL (teaspoon ~5 mL). Bubble on screen: 4% at 250 m (1/26 = 3.8%), ~0.09% at the bottom | Typical adult male TLC ~6 L (respiratory physiology texts). The comparisons describe the gas volume, which is exact by Boyle's law wherever the gas sits |
| F7 | Your heart's slowing | Diving bradycardia (dive reflex) starts with face immersion and deepens with the dive | Lindholm & Lundgren 2009, J Appl Physiol 106:284-292 |
| F8 | You stop floating and start falling by 30 m | With a full breath most people float at the surface, are near neutral around ~10-15 m and sink below (freedivers' "freefall") | Freediving physics (buoyancy shrinks with lung volume, F4). Worded as 30 m, safely past the crossover |
| F9 | At 100 m blood rushes into your chest to fill the space | Thoracic blood shift at depth, mostly from ~30-50 m down | Lindholm & Lundgren 2009 (F7). Replaces PRESSURE's incorrect "lungs fill with blood" |
| F10 | Even trained freedivers can come up from here coughing blood | Pulmonary barotrauma of descent ("lung squeeze"), haemoptysis after deep dives | Mijacika & Dujic 2016, Eur Respir Rev 25:506-512. Worded "can". Record note (updated per the 2026-11-01 originality review, re-check on aidainternational.org before publishing): constant-weight records are now about 100-136 m depending on discipline (Molchanov CWT 136 m, 2023; CWTB ~126-127 m, 2025; CNF 103 m, 2025), so 100 m is elite depth |
| F11 | By 250 m you're about as deep as anyone has gone on a single breath | Herbert Nitsch, ~253 m no-limits dive, Santorini, June 2012 (not a ratified AIDA record; the ratified no-limits record is 214 m, Nitsch 2007) | Widely reported (AIDA, press 2012). Worded "about as deep", on screen "~253 M (2012)", no name |
| F12 | Sperm whales hunt down here with ribs built to fold | Foraging dives typically 400-1,200 m, some deeper than 2,000 m; compliant chest wall and lung collapse at depth, plus large oxygen stores and strong bradycardia | Watwood et al. 2006, J Anim Ecol 75:814-825; Fahlman et al. 2017 on lung collapse in deep-diving cetaceans. "Built to fold" simplifies a compliant chest; no "because" in the VO, since the ribs are one adaptation among several |
| F13 | Your ribs can't fold that small, so something gives | Hedged on purpose | The lungs cannot shrink to 1/101 of total capacity (far below residual volume, ~1.2 L, even with blood shift; human freedivers have reached ~1/22 at 214 m). What fails first at 1 km has never been measured, and the VO says so ("something gives") |
| F14 | On screen at the bottom: "~1.1 TONNES ON EVERY CM²", "x1,072" | ~1,086 bar = ~1,107 kgf per cm² = ~1,072 atm | Commonly cited Challenger Deep pressure (TOPICS #12); arithmetic |
| F15 | "extremely not alive since roughly the shot glass" | Joke, not a claim of a cause of death | Inside the stated hypothetical: in reality a one-breath diver blacks out long before 1 km (the VO's "pretend you somehow still have air" concedes this) |
| F16 | You never imploded; implosion happens to hollow, air-filled things like a sealed can | Implosion = sudden collapse of a gas-filled hollow structure | Engineering definition. Corrects fmZfphacPPQ's "you implode" payoff. No reference to any real submersible accident |
| F17 | You're basically a water balloon; water barely squeezes; your flesh is only about four percent smaller | Water compressibility ~4.6e-10 per Pa -> ~4-5% volume loss at ~1,086 bar; adult body ~55-60% water, other soft tissue similar | IAPWS water property tables. "Flesh", not "you": losing ~6 L of lung gas from a ~70 L body would take off another ~8%, so the -4% Stat sits on a tissue block, not on the whole YOU outline |
| F18 | The biggest squeeze on your air is the first ten metres | Air keeps 50% of its volume at 10 m and ~0.09% at the bottom, so half of all the shrinking happens in the first 10 m | Arithmetic from F4. Said as "on your air" because every 10 m adds the same pressure; on screen "LOST IN THE FIRST 10 M: 50%" vs "LEFT AT THE BOTTOM: ~0.09%" |
| L1 | Landmarks on screen, never spoken | Clock tower ~96 m at the 100 m stop; 3 stacked lattice towers ~330 m each (~1 km) at the 1 km stop; Everest at the bottom | Tower heights from public records; drawn as flat silhouettes, labelled "~96 M CLOCK TOWER" and "~3 EIFFEL TOWERS" |

## Script

### Timed voiceover, beats and on-screen text

Layers: KICKER = `explainer/Headline` (white, red underline), PUNCH = red `Headline`, TAG = `explainer/Tag`, STAT = `explainer/Stat`. METER = the log-scale depth meter on the left edge (core `rect` / `circle` / `text` layers, built in gen_storyboard.py). BUBBLE = the breath bubble (core `circle`, area proportional to air volume). XRAY = flat svg x-ray cards (head, chest) with separate lung, blood and crack layers. Burned-in word captions (core `captions`, max 3 words, white, red on emphasis words, y 0.71) run throughout. Times are generator estimates; anchors are words.

Hook first line: "Hold your breath."
Hook first visual (frame 0, identical to the last frame): bright surface; YOU stands at the waterline; BUBBLE "YOUR AIR 100%" beside it; Tag "THOUGHT EXPERIMENT: 1 BREATH, NO GEAR"; METER on the left with six grey pins (10 M, 30 M, 100 M, 250 M, 1 KM, 10,935 M) and the red marker at 0 M.

**[0:00.1] S1 HOOK (10 words, ~3.0 s)**
- VO: "Hold your breath. Just ten metres down, your ears ache,"
- On screen: YOU tips head-down after "breath" and sinks; the METER marker slides to 10 M on "ten"; a red bracket 0-10 M with Tag "JUST 10 M"; on "ears" the head XRAY card pops in and the eardrum bows inward; Tag "EARS ACHE".

**[0:03.5] R1, 10 M (mechanism, 11 words)**
- VO: "because the pressure's doubled and squeezed your one breath to half,"
- On screen: METER pin 10 M turns red and stamps "x2" on "doubled"; STAT "x2 THE PRESSURE"; BUBBLE shrinks 100% -> 50% on "half"; PUNCH "HALF".

**[0:07.1] S2 STAKES (endpoint, one chained clause)**
- VO: "and the floor of the Mariana Trench is still almost eleven kilometres below you."
- On screen: whip up to the trench cross-section, a white dot labelled "YOU (10 M)" at the top; KICKER "MARIANA TRENCH"; STAT counts to "10,935 M"; on "below", Tag "EVERYONE SAYS YOU'D IMPLODE..." (the contract the twist pays).

**[0:11.5] R2, 30 M (16 words)**
- VO: "By thirty metres it's a quarter, your heart's slowing, and you're not floating anymore, you're falling,"
- On screen: pin 30 M stamps "x4"; BUBBLE 50% -> 25%, Tag "A QUARTER"; `explainer/ECG` with beats spreading apart, Tag "HEART SLOWING (DIVE REFLEX)"; on "falling", Tag "NOT FLOATING. FALLING." and YOU accelerates down.

**[0:16.7] R3, 100 M (32 words)**
- VO: "and at a hundred, your whole breath fits in a water bottle, so blood rushes into your chest to fill the space,"
- VO: "and even trained freedivers can come up from here coughing blood,"
- On screen: pin 100 M stamps "x11"; a ~96 m clock-tower silhouette next to a tiny YOU (Tag "~96 M CLOCK TOWER", never spoken); BUBBLE shrinks beside a 0.5 L bottle, Tag "YOUR BREATH ~0.5 L"; on "blood", the chest XRAY card zooms in, lungs shrink, red blood fills the vessels, Tag "BLOOD SHIFT"; Tags "TRAINED FREEDIVERS", "LUNG SQUEEZE".

**[0:26.0] R4, 250 M + the hedge (30 words)**
- VO: "and by two hundred and fifty metres, you're about as deep as anyone has ever gone on a single breath,"
- VO: "so from here on, pretend you somehow still have air."
- On screen: pin 250 M stamps "x26"; BUBBLE "4%"; a green line wipes across, Tag "DEEPEST BREATH-HOLD DIVE: ~253 M (2012)", then Tag "HUMANS STOP HERE"; on "pretend", KICKER "PRETEND YOU STILL HAVE AIR" and YOU shrugs.

**[0:34.4] S4 TURNSTILE (46%, 6 words)**
- VO: "Relax. That was the easy part."
- On screen: KICKER "THAT WAS THE EASY PART" over a shrugging YOU; music cuts on "part."; dipBlack.

**[0:37.0] R5, 1 KM (26 words)**
- VO: "One kilometre down, your breath is squeezed into a shot glass, and your ribs can't fold that small,"
- VO: "so something gives, and you still haven't imploded."
- On screen: black water, marine snow; pin 1 KM stamps "x101"; three stacked lattice-tower silhouettes (Tag "~3 EIFFEL TOWERS", never spoken); BUBBLE 4% -> 1% beside a shot glass, Tag "YOUR BREATH ~60 ML"; on "ribs", the chest XRAY card, lungs a sliver; on "gives", one white crack line on a rib, camera shake, Tag "SOMETHING GIVES"; Tag "STILL NOT IMPLODED".

**[0:45.1] R5b, the sperm whale (10 words)**
- VO: "Sperm whales hunt down here with ribs built to fold."
- On screen: `explainer/SpermWhale` glides across above a tiny YOU; Tag "RIBS BUILT TO FOLD ✓" in green.

**[0:48.1] S5 PEAK, THE BOTTOM (38 words over three lines)**
- VO: "Yours aren't, so by the time you reach the bottom, your whole breath is one teaspoon,"
- On screen: PUNCH "YOURS AREN'T"; whip down; YOU drops to the trench floor; pin 10,935 M stamps "x1,072"; STAT "~1.1 TONNES ON EVERY CM²" and Tag "x1,072 THE SURFACE PRESSURE" (on screen only); a teaspoon, Tag "YOUR WHOLE BREATH: ~5 ML".
- VO: "drop Everest in beside you and its peak is still underwater,"
- On screen: trench cross-section; Everest (drawn at its true 81% of the water column) drops in beside the YOU dot and shakes the frame; Tag "EVEREST 8,849 M"; a red bracket above the peak, Tag "~2 KM OF WATER ABOVE THE PEAK".
- VO: "and you've been extremely not alive since roughly the shot glass,"
- On screen: YOU turns grey and tips over onto the floor; Tag "STATUS: EXTREMELY NOT ALIVE", then "(SINCE ~1 KM)".

**[0:59.7] S6 TWIST, THE MYTH-BUST (37 words)**
- VO: "and yet you never imploded."
- On screen: whip to a title card: Tag "'YOU'D IMPLODE'" is struck through in red on "never"; text "YOU NEVER IMPLODED"; Tag "MYTH".
- VO: "That only happens to hollow things full of air, like a sealed can,"
- On screen: a sealed can labelled "AIR"; Tag "HOLLOW + AIR"; on "can" it swaps to the crushed drawing with a shake; Tag "= IMPLODES".
- VO: "and you're basically a water balloon, and water barely squeezes, so your flesh is only about four percent smaller."
- On screen: grey YOU next to a water balloon, Tag "= WATER BALLOON"; Tag "WATER BARELY SQUEEZES"; a pink tissue block inside a dashed outline, Tag "YOUR FLESH", STAT "-4% SMALLER".

**[1:11.1] S7 STINGER (callback, cut on the last word)**
- VO: "And the biggest squeeze on your air?"
- On screen: whip to a dark card; KICKER "YOUR AIR"; red bar "LOST IN THE FIRST 10 M: 50%", grey bar "LOST IN THE NEXT 10,925 M: ~50%", Tag "LEFT AT THE BOTTOM: ~0.09%".
- VO: "The first ten metres."
- On screen: whip back to frame 0's layout (surface, YOU, "YOUR AIR 100%", meter at 0 M); the red 0-10 M bracket wipes down, Tag "HALF YOUR AIR GOES HERE". Hard cut 0.35 s after "metres" into the loop.

### Narration (builder input: one paragraph = one beat; scenes are grouped in gen_storyboard.py)

```narration
[music: deep_ocean] [speed: 1.02] Hold your breath. Just ten metres down, your ears ache,

because the pressure's doubled and squeezed your one breath to half,

and the floor of the Mariana Trench is still almost eleven kilometres below you.

[speed: 1.06] By thirty metres it's a quarter, your heart's slowing, and you're not floating anymore, you're falling,

and at a hundred, your whole breath fits in a water bottle, so blood rushes into your chest to fill the space,

and even trained freedivers can come up from here coughing blood,

and by two hundred and fifty metres, you're about as deep as anyone has ever gone on a single breath,

so from here on, pretend you somehow still have air.

Relax. That was the easy part.

One kilometre down, your breath is squeezed into a shot glass, and your ribs can't fold that small,

so something gives, and you still haven't imploded.

Sperm whales hunt down here with ribs built to fold.

Yours aren't, so by the time you reach the bottom, your whole breath is one teaspoon,

drop Everest in beside you and its peak is still underwater,

and you've been extremely not alive since roughly the shot glass,

and yet you never imploded.

That only happens to hollow things full of air, like a sealed can,

and you're basically a water balloon, and water barely squeezes, so your flesh is only about four percent smaller.

[speed: 1.0] And the biggest squeeze on your air?

The first ten metres.
```

Optional ~60 s A/B cut (retention nice-to-have; no corpus outlier Short runs past 59 s): drop "and even trained freedivers can come up from here coughing blood," and "Sperm whales hunt down here with ribs built to fold." (then open the peak line with "So by the time..."), and shorten the flesh line to "and you're basically a water balloon, so your flesh is only about four percent smaller." That removes ~33 words (~10 s) and keeps every stop, the turnstile, the twist and the stinger.

## Shot list

Kit vocabulary used: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), camera (`pushIn`, `panDown`, `drift`, keyframes, `shake`), scene transitions (`cut`, `whip`, `dipBlack`; `whip` is only ever a transition, never a camera move), core `captions`; explainer kit `explainer/Ocean` (`depth`, `surface`, `rays`, `snow`), `explainer/You` (`pose` stand / shrug, `silhouette`, `idle`, layer `rotate`), `explainer/SpermWhale`, `explainer/ECG`, `explainer/Stat`, `explainer/Headline`, `explainer/Tag`. Everything else is inline svg markup in `gen_storyboard.py` (head card, chest card, lung, blood overlay, crack line, bottle, shot glass, teaspoon, can upright + crushed, water balloon, tissue block, clock tower, lattice tower, trench section, Everest). Kit gaps: `explainer/DepthMeter` is linear, so the meter is built from core layers on a log scale; a `scale: 'log'` + `pins` [{depth, label, at, stamp}] extension to DepthMeter would replace those ~20 layers. No other kit change is needed. SFX are all in `studio/public/sfx`.

| t_start | t_end | shot | visual (kit vocabulary) | camera / transition | SFX |
|---|---|---|---|---|---|
| 0:00.0 | 0:03.4 | wide, surface | `Ocean` depth 0 surface 0.22 rays 7; `You` stand at the waterline, rotate 0 -> 180 after "breath" and sinks; BUBBLE `circle` + text "YOUR AIR 100%"; Tag "THOUGHT EXPERIMENT: 1 BREATH, NO GEAR"; METER, marker 0 -> 10 M on "ten", red 0-10 M bracket + Tag "JUST 10 M"; head XRAY svg pops on "ears", eardrum svg scaleX bow; Tag "EARS ACHE" | slow zoom 1.0 -> 1.04 | `breath`, `bubbles` |
| 0:03.4 | 0:07.0 | medium, 10 m | `Ocean` depth 10; `You` head-down; BUBBLE scale 1.41 -> 1.0 (100% -> 50%) on "half", text "YOUR AIR"; pin 10 M stamps "x2" on "doubled"; `Stat` "x2 THE PRESSURE"; PUNCH "HALF" | `pushIn` 0.3 | `click` stamp, `pop` |
| 0:07.0 | 0:11.4 | graphic, full column | trench-section svg; white dot "YOU (10 M)"; KICKER "MARIANA TRENCH"; `Stat` 0 -> 10,935 "METRES TO THE FLOOR"; Tag "EVERYONE SAYS YOU'D IMPLODE..." on "below" | transition `whip` up; camera keyframes zoom 1.15 -> 1.0 (pull out) | `whoosh_long`, `tick` |
| 0:11.4 | 0:16.6 | medium, 30 m | `Ocean` depth 30; pin 30 M stamps "x4"; BUBBLE 50% -> 25%, text "25%", Tag "A QUARTER"; `ECG` beats spreading (prefill); Tag "HEART SLOWING (DIVE REFLEX)"; Tag "NOT FLOATING. FALLING." + bubbles stream, YOU y keyframes accelerate | `panDown` 0.4 | `click`, `heartbeat_slow`, `whoosh` |
| 0:16.6 | 0:19.8 | wide, 100 m + landmark | `Ocean` depth 100; pin 100 M stamps "x11"; clock-tower svg (~96 m) beside a small YOU, Tag "~96 M CLOCK TOWER"; BUBBLE 25% -> 9% next to the bottle svg, Tag "YOUR BREATH ~0.5 L" | camera keyframes, zoom 1.0 -> 1.05 | `click`, `sonar_ping`, `pop` |
| 0:19.8 | 0:25.8 | x-ray, chest | chest card svg zooms in on "blood"; two lung svgs scale 0.55 -> 0.32; blood svg opacity 0 -> 0.9; Tag "BLOOD SHIFT"; Tags "TRAINED FREEDIVERS", "LUNG SQUEEZE" | zoom 1.05 -> 1.12, `shake` 0.3 s on "coughing" | `heartbeat_slow` |
| 0:25.8 | 0:34.3 | medium, 250 m | `Ocean` depth 250 rays 0; pin 250 M stamps "x26"; BUBBLE "4%"; green `rect` wipeRight + Tag "DEEPEST BREATH-HOLD DIVE: ~253 M (2012)"; Tag "HUMANS STOP HERE" on "single"; on "pretend", KICKER "PRETEND YOU STILL HAVE AIR" and `You` swaps to pose shrug | `drift` 0.4 | `click`, `ding` |
| 0:34.3 | 0:36.9 | medium, ironic | KICKER "THAT WAS THE EASY PART"; `You` shrug | `pushIn` 0.4 | `stinger`; music bed cuts on "part." |
| 0:36.9 | 0:40.5 | wide, 1 km + landmark | transition `dipBlack`; `Ocean` depth 1000 snow 120; pin 1 KM stamps "x101"; 3 stacked lattice-tower svgs, Tag "~3 EIFFEL TOWERS"; BUBBLE 4% -> 1% beside the shot-glass svg, Tag "YOUR BREATH ~60 ML" | `pushIn` 0.3 | `boom`, `pop`; `underwater_rumble` + `dread` beds start |
| 0:40.5 | 0:45.0 | x-ray, chest | chest card; lungs 0.3 -> 0.1; blood overlay; crack svg pops on "gives", Tag "SOMETHING GIVES"; Tag "STILL NOT IMPLODED" | `shake` 0.35 s on "gives" | `impact` |
| 0:45.0 | 0:48.0 | wide, you vs it | `SpermWhale` x 95% -> 50% across the frame above a small head-down `You`; Tag "RIBS BUILT TO FOLD ✓" green | `drift` 0.5 | `sonar_ping` x2 |
| 0:48.0 | 0:52.5 | wide, the bottom | transition `whip` down; PUNCH "YOURS AREN'T"; floor `rect`; `You` drops y 400 -> 1090; pin 10,935 M stamps "x1,072"; `Stat` "~1.1 TONNES ON EVERY CM²"; Tag "x1,072 THE SURFACE PRESSURE"; teaspoon svg, Tag "YOUR WHOLE BREATH: ~5 ML" | hold, then zoom 1.0 -> 1.08; `shake` on landing | `glitch`, `boom`, `pop` |
| 0:52.5 | 0:55.8 | graphic, scale drop | trench-section svg; Everest svg (81% of the column) drops from above on "Everest"; YOU dot on the floor; Tag "EVEREST 8,849 M"; red bracket + Tag "~2 KM OF WATER ABOVE THE PEAK" | `shake` on landing | `whoosh`, `impact` |
| 0:55.8 | 0:59.6 | medium, deflation | floor `rect`; `You` silhouette grey, idle off, rotate 180 -> 270 (lying down); Tag "STATUS: EXTREMELY NOT ALIVE"; Tag "(SINCE ~1 KM)" | `pushIn` 0.3 | `ding` |
| 0:59.6 | 1:01.5 | title card | transition `whip` left; Tag "'YOU'D IMPLODE'" struck by a red `rect` wipeRight on "never"; text "YOU NEVER IMPLODED"; Tag "MYTH" | `pushIn` 0.4 | `riser`, `glitch` |
| 1:01.5 | 1:05.1 | prop | can svg (AIR label) swaps to the crushed-can svg on "can"; Tags "HOLLOW + AIR", "= IMPLODES" | `shake` 0.3 s on the swap | `impact` |
| 1:05.1 | 1:11.0 | medium | grey `You` + water-balloon svg, Tag "= WATER BALLOON"; Tag "WATER BARELY SQUEEZES"; tissue-block svg (dashed original outline) scale 1.0 -> 0.987 on "four"; Tag "YOUR FLESH"; `Stat` "-4% SMALLER" | `pushIn` 0.3 | `pop`, `tick` |
| 1:11.0 | 1:13.4 | graphic | transition `whip` up; KICKER "YOUR AIR"; red bar "LOST IN THE FIRST 10 M: 50%"; grey bar "LOST IN THE NEXT 10,925 M: ~50%" on "air"; Tag "LEFT AT THE BOTTOM: ~0.09%" | hold | `whoosh_long` |
| 1:13.4 | 1:14.9 | wide, surface (= frame 0) | transition `whip` down; frame 0's layers verbatim with no motion; red 0-10 M bracket wipeDown + Tag "HALF YOUR AIR GOES HERE" on "first"; hard cut 0.35 s after "metres" | zoom 1.03 -> 1.0, ending on frame 0's framing | `bubbles` |

Storyboard: `storyboard.json` is generated by `python3 gen_storyboard.py storyboard.json` (17 scenes, 74.9 s, 242 caption words). It validates against `studio/src/core/schema.ts` (`src/cli/validate.ts` with Node 22 on the Spark: ok). `scripts/check_storyboards.py` finds every component registered and a longest visual hold of 2.4 s; the only flag is the missing `mix.wav`, which doesn't exist until TTS runs. Stills were rendered on the Spark CPU (`scripts/spark_stills.sh`, contact sheet `out/stills/mariana-pressure.jpg`), and the overlaps they showed (x2 Stat over HALF, a turnstile headline over YOU, landmark tags over the meter, the final bracket tag over the thought-experiment tag) are fixed.

## Originality

- `python3 scripts/originality_check.py backlog/explainer/explainer-short-mariana-pressure/script.md research/corpus research/library/transcripts` -> PASS (result recorded in review.json).
- Also checked against our own `episodes/` and `backlog/` (the duplicate risk): see review.json for the max 5-gram share with `episodes/explainer-pressure-ladder/script.md`.
- Structure borrowed from fmZfphacPPQ / XFFjxTllpoA / mzeN0BXR4e0 (table above). All wording is new.
