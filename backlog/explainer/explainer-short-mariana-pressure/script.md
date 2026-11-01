---
slug: explainer-short-mariana-pressure
niche: explainer
format: short
aspect: "9:16"
title: "What The Mariana Trench Does To Your Body"
title_alternates:
  - "Could Your Body Survive The Mariana Trench?"
  - "What 1,000x Pressure Does To Your Body"
title_formula: "Could you survive [ocean extreme]? / What [extreme] does to your body (PLAYBOOK section 7, Shorts series formula)"
premise: "You hold one breath and sink. We check your body at four depth markers: 10 m, 100 m, 1 km and the bottom (about 11 km). Body only. This is a separate premise from explainer-sinking-every-1000m (creatures + threats per 1,000 m) and shares no lines with it."
variant: "Shorts skeleton PLAYBOOK 1b (S1-S7), depth x10 ladder (fmZfphacPPQ) stretched to 60-90 s by adding the twist beat and a stinger, not by slowing the voice"
target_runtime_s: 85
target_runtime_range_s: [78, 90]
target_words_per_min: 205        # PLAYBOOK Shorts TTS target 180-230; hook read slower (~180)
measured:
  vo_words: 294
  vo_runtime_s: 85.3             # 294 words at 219 wpm body / 180 wpm hook + 0.2 s breath per sentence
  effective_wpm_incl_pauses: 207
  hook_words: 12                 # "Hold your breath and sink. Your body starts losing at ten metres." (PLAYBOOK: <=12 words, <=3 s; ours 4.4 s incl. one breath)
  first_you_word: 2
  sentences: 20
  you_pct_sentences: 80          # target >=60%
  avg_sentence_words: 14.7       # target 12-16
  numbers_per_min: 13            # above the 5-8 target, but every number is paired with a shown object (sky, bottle, motorbike, SUV, jets, Everest); PLAYBOOK 9.3 says comparisons, not density, matter
  first_rung_s: 11.6             # PLAYBOOK <=8 s; the hook already names rung 1 (10 m) at 2 s, and the DepthMeter with all four stops is on screen from frame 1
  turnstile_s: 40.6              # 48% of runtime (target 45-55%)
  peak_s: [59.2, 70.8]           # 69-83%
  twist_s: [70.8, 81.6]          # 83-96%
  stinger_s: [81.6, 85.3]        # 96-100%, cut on "metres"
voice: "Kokoro-82M, calm dry male narrator (same register as the explainer pilots); hook ~180 wpm, body ~215 wpm, 0.2 s breath per sentence; no music-only holds"
references:
  - id: fmZfphacPPQ
    short: PRESSURE
    url: https://www.youtube.com/watch?v=fmZfphacPPQ
    views: 14711279
    outlier_score: 1.84
    why_chosen: "Closest premise and format in the corpus: a second-person dive down a x10 depth ladder where each stop breaks a new part of the body, with a depth meter and a landmark per number. We borrow the ladder (small first number, x10, x10, final big jump), the outside -> inside -> whole-body axis, the conjunction-chained rung bridges, the 'even [thing built for depth]' stakes line, the x-ray cutaway as the pattern interrupt after each number, and the plant-a-word-pay-it-twice device. We do NOT borrow its science: its 'lungs fill with blood', 'toxic blood gas on one breath' and 'you implode' claims are wrong, and our twist corrects the last one on screen."
  - id: XFFjxTllpoA
    short: PUFFER
    url: https://www.youtube.com/watch?v=XFFjxTllpoA
    views: 7931305
    outlier_score: 1.69
    why_chosen: "PLAYBOOK's recommended 60 s Shorts skeleton, and the reason this Short can run 85 s: a title-as-action hook, two stakes numbers by second 8, a timed body ladder where the body is personified as fighting back, a one-clause mechanism aside, the ironic 'it gets worse' turnstile at 46%, death told only through deflating euphemism, then a second act after the peak (reality flip) that keeps the back third from sagging."
  - id: mzeN0BXR4e0
    short: DEEP
    url: https://www.youtube.com/watch?v=mzeN0BXR4e0
    views: 17219766
    outlier_score: 12.86
    why_chosen: "Same place (a descent to the hadal trench) and the biggest views in the explainer corpus. We borrow its 'drop a famous landmark into the place' scale image (Everest in the trench) as our stakes line, its per-stop entry pattern (number + lit band on a cross-section), its 'even life gives up here' hostility line at the deepest rung, and its rule to keep every stat consistent and sourced (it contradicts itself on % explored; we cite every number below)."
evidence: "Insider Tech 'How Deep The Ocean Really Is' 83.6M; atomic marvel 'Human Body vs Implosion' 10.3M; The Infographics Show 1.2M (backlog/explainer/TOPICS.md #12, backlog/explainer/evidence/mariana_trench_pressure_human_shorts.jsonl)"
fact_file: "section 'Fact sheet' below; every number and mechanism has a source; hedged claims are worded as hedges in the VO"
safety: "No gore. Death is said only as 'extremely not alive'. 'Coughing blood' is a real, mild freediving injury stated plainly, with no image of blood beyond a red tint in the x-ray lungs. The rib beat is a hedge ('something gives') over a flat x-ray crack line, with no body damage on the YOU figure. No self-harm framing: it is a thought experiment, and the hook rule (one breath, no gear) is stated as a hypothetical (R5)."
cta: none   # PLAYBOOK 6: 6 of 6 outlier Shorts end with no CTA
post_caption: "Which ocean extreme should we put your body through next?"
---

# What The Mariana Trench Does To Your Body

## Beat alignment table

| Our beat | Our timestamp | Reference id + timestamp | Device borrowed | How we adapt it |
|---|---|---|---|---|
| S1 Hook | 0:00-0:04.4 | fmZfphacPPQ 0:00-0:03; XFFjxTllpoA 0:00-0:03 | H4: second person in word 1-2 + a deliberately small first number that says damage starts early; subject on screen in frame 1 | An imperative instead of a conditional ("Hold your breath and sink"), which also sets the honest rule for the whole Short: one breath, no gear, no compressed gas. "Ten metres" is said as the place the losing starts. Frame 1 already shows the DepthMeter with all four stops and the trench floor label |
| S2 Stakes / anchor | 0:04.4-0:11.6 | XFFjxTllpoA 0:03-0:07; mzeN0BXR4e0 12:52-13:07 | Two numbers by second 8; a famous landmark dropped into the place for scale | Endpoint first (almost 11 km), then Everest dropped into the trench with ~2 km to spare. Gives the ladder a visible finish line before rung 1 |
| Progress device | 0:00-1:25 | fmZfphacPPQ (visual depth number per rung); mzeN0BXR4e0 1:40, 6:06 (lit band per zone) | Visible shape of the video; a new band lit at every stop | Right-edge `DepthMeter` with 4 grey stop pins (10 M, 100 M, 1 KM, 10,935 M); each pin turns red and stamps a pressure multiple (x2, x11, x101, x1,072) when we arrive |
| R1 10 m: format-teaching rung | 0:11.6-0:25.5 | fmZfphacPPQ 0:03-0:08; XFFjxTllpoA 0:07-0:11 | Rung entry by number; a mild, felt first symptom (ears); a one-clause mechanism paired with an everyday comparison | Comparison: 10 m of water weighs as much as the whole sky. Mechanism: Boyle's halving in plain verbs ("shrinks to half"). Felt symptom: ear ache, plus the honest eardrum risk shallower than 10 m. Plants "squeeze"/"half" for the stinger |
| R2 100 m | 0:25.5-0:40.6 | fmZfphacPPQ 0:08-0:14; XFFjxTllpoA 0:14-0:21 | x10 number as re-hook; organ change + one-clause reason; the body personified as fighting back | The real mechanism replaces the reference's error: dive reflex (heart slows) and blood shift (blood fills the chest to stand in for the air). Water-bottle prop for the breath. One authority/reality line: freedivers train for years for this, and some still come up coughing blood |
| S4 Turnstile | 0:40.6-0:43.3 | XFFjxTllpoA 0:27-0:28 | Ironic false reassurance at ~46-48%, with a background change on the next word | "Enjoy it, because you just did the easy part" lands at 48%; on "Stop three" the ocean drops from twilight blue to midnight black |
| R3 1 km | 0:43.3-0:59.2 | fmZfphacPPQ 0:14-0:20; XFFjxTllpoA 0:52-0:55 | "Even [a thing built for depth]" stakes line; x10 jump; a pointed scale object | The machine becomes an animal that really does this on one breath (sperm whale), turned into a you-vs-it contrast ("and yours aren't"). Scale object: a motorbike on your thumbnail. Honest hedge once per video: "something gives" |
| S5 Peak 11 km | 0:59.2-1:10.8 | fmZfphacPPQ 0:26-0:32; mzeN0BXR4e0 13:01-13:47 | Final number + biggest landmark; a "nothing lives here" hostility line | The thumbnail callback escalates (motorbike -> SUV), then the whole-body figure (fifty jumbo jets across your skin). "Even fish give up" uses the real deepest-fish record, 2.6 km above the floor |
| S6 Twist / second axis | 1:10.8-1:21.6 | fmZfphacPPQ 0:30-0:32 (its payoff, inverted); XFFjxTllpoA 0:43-0:47 (second act after the peak) | Change axis after the peak; myth-bust of the famous version | The genre's (and PRESSURE's) payoff is "you implode". We flip it: hollow air-filled things implode, a mostly-water body only shrinks ~4%. Relief with a sting, told as a deflation ("extremely not alive") |
| S7 Stinger | 1:21.6-1:25.3 | fmZfphacPPQ 0:13 / 0:26 / 0:31 (plant, partial, total payoff); XFFjxTllpoA 0:55-0:59 (end on a fact, no CTA) | Planted word paid off; question answered in 3-4 words; last frame matches the first so the loop restarts | "Squeeze" and "half", planted at 0:12, return as the counterintuitive fact that half of all the air squeeze happened in the first ten metres. Cut on "metres" to the 10 m frame, which is one second from the opening frame |

Pacing against PLAYBOOK sections 1b, 3 and 8:

| Check | Target | Ours |
|---|---|---|
| Hook | <=12 words, <=3 s, "you" in first 10 words, subject on screen in frame 1 | 12 words, 4.4 s (one breath), "your" at word 2, trench label + DepthMeter on frame 1 |
| Words/min | 180-230 (TTS) | ~207 incl. pauses |
| Rung spacing | a new rung or number every 3-8 s | new number at 2, 5, 9, 12, 26, 44, 59, 61, 65, 69, 78 s; stops at 12 / 26 / 43 / 59 s |
| Attention reset | every 3-6 s | a visual state change every 1.5-4 s (shot list); a caption card per clause |
| Explicit verbal re-hook | ~10 s | 11.6 "Stop one", 25.5 "Stop two", 40.6 turnstile, 43.3 "Stop three", 59.2 "Last stop", 70.8 "And yet", 81.6 question |
| Turnstile | 45-55% | 48% |
| Spine loop | opens at 0 s, closes ~64-100% | "how much of you survives the bottom?" opens 0:00, closes 1:21 (95%) |
| Micro loops | one every 8-12 s | "your body improvises" -> how (0:30-0:36); "so something gives" -> whales can, you can't (0:52-0:59); "And yet you don't implode" -> why (1:11-1:21); "biggest squeeze?" -> answer (1:22-1:25) |
| Plant -> payoff | 1 word paid twice | "squeeze/shrinks to half" 0:12 -> "a hundredth" 0:48 -> "biggest squeeze... first ten metres" 1:25; thumbnail 0:44 -> 1:03 |
| "You" sentences | >=60% | 80% |
| CTA | none | none; comment prompt goes in the post caption only |

## Fact sheet

| # | Claim in VO | Value used | Source / note |
|---|---|---|---|
| F1 | Bottom of the Mariana Trench "almost eleven kilometres down" | Challenger Deep ~10,935 m (on screen "10,935 M") | Greenaway et al. 2021 (Earth and Space Science) ~10,935 m; Vescovo/Five Deeps 2019 sonar ~10,925 m. Both round to "almost 11 km" |
| F2 | Everest's peak would still be "two kilometres underwater" | 8,849 m; 10,935 - 8,849 = 2,086 m | Nepal-China joint survey 2020 (8,848.86 m) |
| F3 | Ten metres of seawater weighs as much as the whole sky above you; pressure doubles at 10 m | 1 atm per ~10.06 m seawater; 2 atm absolute at 10 m | NOAA Diving Manual (33 fsw = 1 atm) |
| F4 | Every air pocket shrinks to half at 10 m; a hundredth at 1 km | Boyle's law: V = V0 / P(atm abs): 1/2 at 10 m, 1/11 at 100 m, 1/101 at 1 km, ~1/1,072 at the bottom | Standard gas law; applies to a breath-hold diver's lungs, middle ear, sinuses and gut gas |
| F5 | Ears go first; an unequalised eardrum can tear before 10 m | Ear pain from ~1-2 m; rupture reported at pressure differences reached around 1.5-5 m | DAN (Divers Alert Network) ear barotrauma guidance; NOAA Diving Manual. Worded "can tear" |
| F6 | A full breath becomes a small water bottle at 100 m | ~6 L total lung capacity / 11 = ~0.55 L | Typical adult male TLC ~6 L (respiratory physiology texts); bottle on screen labelled "~0.5 L" |
| F7 | Your heart slows | Diving bradycardia (dive reflex) | Lindholm & Lundgren 2009, J Appl Physiol 106:284-292, "The physiology and pathophysiology of human breath-hold diving" |
| F8 | Blood rushes into your chest to fill the gap the air left | Thoracic blood shift at depth | Same review (F7); this replaces the reference's incorrect "lungs fill with blood" |
| F9 | Freedivers train for years to reach 100 m; some still come up coughing blood | Pulmonary barotrauma of descent ("lung squeeze"), haemoptysis after deep dives | Mijacika & Dujic 2016, Eur Respir Rev 25:506-512; Lindholm 2009. 100 m+ is elite depth (AIDA/CMAS records are in the 100-130 m range for constant weight). Worded "some" |
| F10 | 1 km: a hundred times the pressure, like a motorbike on your thumbnail | 101 atm = ~104 kg per cm²; thumbnail ~2 cm² -> ~210 kg; road motorbike ~150-250 kg | Arithmetic from F3; on screen "~100x" and "~200 KG" |
| F11 | Your ribs can't bend that far, so something gives | Hedged on purpose | The lungs cannot shrink to 1/101 of total capacity (far below residual volume, ~1.2 L); what fails first in a human at that depth has never been measured. The VO admits that ("something gives"), the PLAYBOOK's once-per-video honest hedge |
| F12 | Sperm whales hunt down here on one breath; their ribs are built to fold | Foraging dives typically 400-1,200 m, some deeper than 2,000 m; flexible ribcage, lungs collapse at depth | Watwood et al. 2006, J Anim Ecol 75:814-825; Fahlman et al. 2017 on lung collapse in deep-diving cetaceans. "Built to fold" is a simplification of a compliant chest wall |
| F13 | The bottom: nearly eleven hundred times the pressure | ~1,086 bar = ~1,072 atm | Commonly cited Challenger Deep pressure (TOPICS #12); on screen "x1,072" |
| F14 | Over a tonne on every square centimetre; an SUV on your thumbnail | 1,086 bar = ~1,107 kg per cm²; x 2 cm² = ~2.2 t; mid-size SUV ~1.9-2.5 t | Arithmetic |
| F15 | Fifty loaded jumbo jets spread across your skin | Body surface ~1.8 m² x 1.086e8 Pa = ~1.95e8 N = ~19,900 t-force; Boeing 747-400 max take-off ~397 t -> ~50 | Arithmetic; Boeing 747-400 airport planning document |
| F16 | Even fish give up more than two kilometres above you | Deepest fish filmed: snailfish (Pseudoliparis) at 8,336 m, Izu-Ogasawara Trench, 2022; 10,935 - 8,336 = 2.6 km | Minderoo-UWA Deep Sea Research Centre / Tokyo Univ. of Marine Science, announced April 2023; physiological fish limit ~8,200-8,400 m (Yancey et al. 2014, PNAS 111:4461) |
| F17 | You don't implode; implosion happens to hollow, air-filled things like a sealed can | Implosion = sudden collapse of a gas-filled hollow structure | Engineering definition; a sealed can of air on screen. Corrects fmZfphacPPQ's "you implode" payoff |
| F18 | You're mostly water and water barely squeezes; ~4% smaller | Water compressibility ~4.6e-10 per Pa -> ~4% volume loss at ~1,000 bar; adult body ~55-60% water, other soft tissue of similar order | Standard water property tables (IAPWS); worded "about four percent" |
| F19 | The biggest squeeze of the whole trip is the first ten metres | By Boyle's law the air keeps 50% of its volume at 10 m and ~0.09% at the bottom, so half of all the shrinking happens in the first 10 m (and the pressure ratio changes fastest at the surface) | Arithmetic from F4. This is also why divers are taught that the shallow metres are where barotrauma is most likely (NOAA, DAN) |

## The script

Layers: KICKER = `Headline` ALL-CAPS white, top third; PUNCH = red `Headline` word, lower-middle; TAG = small white `Tag` pinned to an object; METER = `DepthMeter` on the right edge for the whole Short, with four stop pins; XRAY = NEW `explainer/BodyCutaway` (YOU outline with lungs, middle ears, sinuses, heart, ribcage and chest vessels). Burned-in word captions (core `captions`, 2-3 words per card, white bold, lower-middle third, red highlight on numbers) follow the VO throughout.

Hook first line: "Hold your breath and sink."
Hook first visual: 9:16, bright surface split; the stick-figure YOU floats at the waterline, cheeks puffed, one big breath bubble on screen labelled "YOUR AIR 100%". On the right edge the DepthMeter reads 0 M with four grey pins below (10 M, 100 M, 1 KM, 10,935 M); far below, the water goes black and a faint trench floor line is tagged "MARIANA TRENCH". YOU tips head-down on "sink".

### [0:00] S1 HOOK (12 words, ~180 wpm)

[0:00.0] Hold your breath and sink.
  on-screen: TAG "1 BREATH. NO GEAR." beside YOU; METER "0 M"
[0:01.9] Your body starts losing at ten metres.
  on-screen: METER pin "10 M" pulses red; caption highlights "TEN METRES"

### [0:04.4] S2 STAKES (two numbers + landmark)

[0:04.4] You're heading for the bottom of the Mariana Trench, almost eleven kilometres down.
  on-screen: KICKER "MARIANA TRENCH"; `Stat` "10,935 M" counts up; METER bottom pin "10,935 M" lights
[0:08.2] Drop Mount Everest in, and its peak still sits two kilometres underwater.
  on-screen: Everest silhouette drops into the trench cross-section; TAG "EVEREST 8,849 M"; bracket above the peak "~2 KM OF WATER"

### [0:11.6] R1 STOP ONE: 10 M (format-teaching rung)

[0:11.6] Stop one, ten metres: that much seawater weighs as much as the entire sky above you, so the pressure doubles and every pocket of air inside you shrinks to half.
  on-screen: METER pin "10 M" stamps red "x2"; split card: sky column labelled "THE WHOLE SKY" = water column labelled "10 M OF WATER"; breath bubble shrinks to "50%"; PUNCH "HALF"
[0:20.1] Your ears go first, and if you don't pop them, an eardrum can tear before you even get here.
  on-screen: XRAY head close-up, eardrum bows inward; TAG "EARDRUM"; small red "TEAR RISK: < 10 M"

### [0:25.5] R2 STOP TWO: 100 M (organ change + body fights back)

[0:25.5] Stop two, a hundred metres: eleven times the pressure, and your full breath is now a small water bottle, so your body improvises.
  on-screen: METER pin "100 M" stamps "x11"; 6 L breath balloon shrinks beside a 0.5 L bottle until they match; TAG "~0.5 L"
[0:32.0] Your heart slows, and blood rushes into your chest to fill the gap the air left.
  on-screen: XRAY chest: heart pulse slows (`Stat` "BPM" ticks down); red blood fills the vessels around the shrunken lungs; TAG "BLOOD SHIFT"
[0:36.6] Freedivers train for years to get here, and some still come up coughing blood.
  on-screen: TAG "TRAINED FREEDIVERS"; small red "LUNG SQUEEZE"

### [0:40.6] S4 TURNSTILE (48%)

[0:40.6] Enjoy it, because you just did the easy part.
  on-screen: PUNCH "THE EASY PART" in white, then the background drops to black on the next word

### [0:43.3] R3 STOP THREE: 1 KM ("even" contrast + honest hedge)

[0:43.3] Stop three, one kilometre: a hundred times the pressure, like a motorbike parked on your thumbnail.
  on-screen: METER pin "1 KM" stamps "x101"; macro thumb with a motorbike balanced on the nail; TAG "~200 KG"
[0:47.8] Your lungs would have to shrink to a hundredth of their size, and your ribs can't bend that far, so something gives.
  on-screen: XRAY lungs shrink to a sliver, `Stat` "1/100"; ribcage flexes, one flat white crack line; TAG "SOMETHING GIVES"
[0:54.1] Sperm whales hunt down here on one breath because their ribs are built to fold, and yours aren't.
  on-screen: `SpermWhale` glides past YOU at true scale; split XRAY: whale ribcage folds flat (green tick) vs your ribcage (red cross); PUNCH "YOURS AREN'T"

### [0:59.2] S5 PEAK: THE BOTTOM, 10,935 M

[0:59.2] Last stop, the bottom: nearly eleven hundred times the pressure, over a tonne on every square centimetre, an SUV on your thumbnail and fifty loaded jumbo jets spread across your skin.
  on-screen: METER bottom pin stamps "x1,072"; `Stat` "1 TONNE / CM²"; thumb again, the motorbike swaps for a `Car` (SUV); pull out to YOU under a stack of jet silhouettes, `Stat` "x50"
[1:07.9] Even fish give up more than two kilometres above you.
  on-screen: NEW snailfish at a dashed line "DEEPEST FISH 8,336 M"; bracket down to YOU "2.6 KM"

### [1:10.8] S6 TWIST (myth-bust)

[1:10.8] And yet you don't implode.
  on-screen: KICKER "YOU DON'T IMPLODE" with "IMPLODE" struck through in red
[1:12.4] That only happens to hollow things full of air, like a sealed can.
  on-screen: sealed can crumples flat in one frame; TAG "HOLLOW + AIR"
[1:16.2] You're mostly water, and water barely squeezes, so you'd arrive about four percent smaller, airless, and extremely not alive.
  on-screen: YOU outline vs dashed original outline, `Stat` "-4%"; breath bubble gone, TAG "AIR: 0%"; YOU drifts flat to the trench floor, eyes as X marks

### [1:21.6] S7 STINGER (callback, cut on the last word)

[1:21.6] And the biggest squeeze of your whole trip?
  on-screen: METER whips back up to the surface
[1:24.0] The first ten metres.
  on-screen: back at 10 m, bright water; breath bubble "50%" and PUNCH "HALF"; the METER pin "10 M" glows; hard cut on "metres" (the next loop opens on the same water)

## Shot list

Kit vocabulary: core layers (`rect`, `circle`, `text`, `svg`, `particles`, `component`), camera (`pushIn`, `pullOut`, `panUp`, `panDown`, `drift`, keyframes, `shake`), transitions (`cut`, `fade`, `dipBlack`, `whip`), `grade`, core `captions`; explainer kit `explainer/Ocean` (`depth` track, `surface`, `rays`, `snow`, `falloff`), `DepthMeter` (`depth` track, `max`, `zones`, `side`), `You` (`pose`), `SpermWhale`, `Car`, `HeightChart`, `ScaleBar`, `Stat`, `Headline`, `Tag`. Kit gaps marked NEW (flat SVG, code only, no generated imagery): `explainer/BodyCutaway` (YOU outline as x-ray; props `lungs` 0..1 volume track, `eardrum` 0..1 bow, `heartBpm` track, `blood` 0..1 chest-vessel fill, `ribs` normal|flex|crack, `focus` head|chest|full), `explainer/Thumb` (macro thumb with nail, `load` slot for a figure), `explainer/Motorbike`, `explainer/Jet` (747 silhouette), `explainer/Bottle` (`liters`), `explainer/Can` (`crush` 0..1), `explainer/Snailfish` (pale translucent, `idle`), `explainer/TrenchSection` (cross-section with water column and floor; `mountain` overlay with `heightM`), `You` NEW prop `cheeks` (puffed breath-hold) and `pose: limp`, `DepthMeter` NEW prop `pins` [{depth, label, at, stamp}]. SFX from `studio/public/sfx`.

| t_start | t_end | shot type | visual description (kit vocabulary) | camera move | SFX |
|---|---|---|---|---|---|
| 0:00.0 | 0:01.9 | wide, surface split | `Ocean` `surface: 0.22`, bright sky, `rays: 7`, `depth: 0`; `You` `pose: stand` NEW `cheeks: true` at the waterline; `circle` breath bubble beside YOU, `Tag` "YOUR AIR 100%"; `DepthMeter` `side: right`, NEW `pins` 10 M / 100 M / 1 KM / 10,935 M grey; faint floor line far below, `Tag` "MARIANA TRENCH"; `Tag` "1 BREATH. NO GEAR." | hold, YOU tips head-down on "sink" | `breath` (inhale), `bubbles` |
| 0:01.9 | 0:04.4 | medium, descending | YOU sinks; `Ocean` `depth` 0 -> 8; `DepthMeter` `depth` 0 -> 8; pin "10 M" pulses red | `panDown` follow | `underwater_rumble` bed starts low |
| 0:04.4 | 0:08.2 | graphic, full column | NEW `TrenchSection` full height, tiny YOU dot near the top; `Headline` "MARIANA TRENCH"; `Stat` "10,935 M" count-up 0 -> 10,935; bottom pin lights | `pullOut` from YOU to full column | `whoosh_long` |
| 0:08.2 | 0:11.6 | graphic, scale drop | `TrenchSection` `mountain` Everest silhouette drops in from the top, `Tag` "EVEREST 8,849 M"; bracket above the peak "~2 KM OF WATER" | small `shake` on landing | `impact` (soft) |
| 0:11.6 | 0:14.5 | medium, 10 m | cut back to YOU at 10 m, `Ocean` `depth: 10`; `DepthMeter` pin "10 M" stamps red "x2" | `cut`, slight `pushIn` | `tick`, stamp `click` |
| 0:14.5 | 0:17.5 | split graphic | left: `rect` sky column, `Tag` "THE WHOLE SKY"; right: `rect` water column, `Tag` "10 M OF WATER"; a `=` sign between, both columns on one scale pan level | `whip` in | `whoosh` |
| 0:17.5 | 0:20.1 | close | breath bubble `circle` `r` track 100% -> 50%, `Stat` "50%"; red `Headline` "HALF" | `pushIn` on bubble | `pop` (deflating) |
| 0:20.1 | 0:23.0 | x-ray close, head | NEW `BodyCutaway` `focus: head`, `eardrum` 0 -> 0.8 bow inward, sinus cavities outlined; `Tag` "EARDRUM" | `pushIn` to ear | `drone` thin, rising |
| 0:23.0 | 0:25.5 | x-ray close | eardrum flashes red, `Tag` red "TEAR RISK: < 10 M"; YOU (inset) pinches nose and pops, small ring pulse | `shake` 0.2 s on the flash | `click` (pop) |
| 0:25.5 | 0:28.5 | medium, 100 m | `Ocean` `depth: 100`, rays thin; `DepthMeter` pin "100 M" stamps "x11" | `cut`, `drift` down | stamp `click`, `sonar_ping` |
| 0:28.5 | 0:32.0 | scale gag | breath balloon `circle` labelled "6 L" shrinks beside NEW `Bottle` `liters: 0.5` until they match; `Tag` "~0.5 L" | hold | `pop` |
| 0:32.0 | 0:36.6 | x-ray, chest | `BodyCutaway` `focus: chest`, `lungs` 0.5 -> 0.09, `heartBpm` track 75 -> 40 (pulse visibly slows), `blood` 0 -> 0.7 red fill in chest vessels; `Stat` "BPM" ticking down; `Tag` "BLOOD SHIFT" | slow `pushIn` | `heartbeat_slow` |
| 0:36.6 | 0:40.6 | medium | YOU in profile, `Tag` "TRAINED FREEDIVERS"; lungs in the x-ray inset tint red, `Tag` red "LUNG SQUEEZE" | `drift` | `heartbeat_slow` continues |
| 0:40.6 | 0:43.3 | medium, ironic beat | white `Headline` "THE EASY PART"; YOU `pose: shrug`; on the last word `grade` crushes to black | hold, then `dipBlack` | music bed cuts out, `stinger` |
| 0:43.3 | 0:45.5 | wide, 1 km | `Ocean` `depth: 1000`, `rays: 0`, `snow: 120`; `DepthMeter` pin "1 KM" stamps "x101" | `cut` in from black | `boom` low, stamp |
| 0:45.5 | 0:47.8 | macro | NEW `Thumb` fills frame; NEW `Motorbike` lowers onto the nail; `Tag` "~200 KG"; nail flexes | `pushIn` | `impact` |
| 0:47.8 | 0:51.0 | x-ray, chest | `BodyCutaway` `lungs` -> 0.01 (a sliver), `Stat` "1/100" | `pushIn` | `drone` |
| 0:51.0 | 0:54.1 | x-ray close | `ribs: flex` then `ribs: crack`: one flat white crack line on one rib, no gore; `Tag` "SOMETHING GIVES" | `shake` 0.3 s | `impact` (dull) |
| 0:54.1 | 0:57.0 | wide, true scale | `SpermWhale` (`pxPerM` matched with `You`) glides past left to right above YOU | `drift` with whale | `sonar_ping` x2 (clicks) |
| 0:57.0 | 0:59.2 | split x-ray | left: whale ribcage folding flat, green tick; right: YOUR ribcage, red cross; red `Headline` "YOURS AREN'T" | `whip` left -> right | `ding` then `glitch` |
| 0:59.2 | 1:01.5 | wide, the bottom | `Ocean` `depth: 10935`, black, sparse `snow`; flat trench floor; `DepthMeter` bottom pin stamps "x1,072"; YOU arrives at the floor | `panDown` to floor, stop hard | `boom`, stamp |
| 1:01.5 | 1:03.5 | graphic | `Stat` "1 TONNE / CM²" with a 1 cm² square drawn on YOU's palm | hold | `tick` |
| 1:03.5 | 1:05.5 | macro | `Thumb` again; `Motorbike` swaps out for `Car` `color` dark grey (SUV), nail bends further; `Tag` "~2.2 T" | `cut`, `pushIn` | `impact` |
| 1:05.5 | 1:07.9 | wide gag | `pullOut` to YOU on the floor under a stacked tower of NEW `Jet` silhouettes; `Stat` "x50" counts up | `pullOut` | `whoosh_long` |
| 1:07.9 | 1:10.8 | cross-section | NEW `Snailfish` at a dashed line "DEEPEST FISH 8,336 M"; bracket down to YOU "2.6 KM"; `Tag` "NO FISH BELOW HERE" | `panDown` from fish to YOU | `sonar_ping` (distant) |
| 1:10.8 | 1:12.4 | title card | white `Headline` "YOU DON'T IMPLODE", red strike-through draws across "IMPLODE" | `whip` in | `riser` (short), stop |
| 1:12.4 | 1:16.2 | prop | NEW `Can` sealed, `Tag` "HOLLOW + AIR"; `crush` 0 -> 1 in 3 frames | `shake` 0.2 s on crush | `impact` (sharp) |
| 1:16.2 | 1:19.0 | medium | YOU outline inside a dashed original outline, `Stat` "-4%"; breath bubble gone, `Tag` "AIR: 0%" | slow `pushIn` | `underwater_rumble` |
| 1:19.0 | 1:21.6 | medium | YOU NEW `pose: limp`, drifting flat to the floor, eyes as X marks (cartoon) | `drift` | silence beat |
| 1:21.6 | 1:24.0 | fast travel | `DepthMeter` `depth` 10,935 -> 10 with motion streaks; `Ocean` `depth` track back to 10, rays return | `panUp` very fast (`whip` feel) | `whoosh_long` reversed feel |
| 1:24.0 | 1:25.3 | medium, 10 m (matches 0:01.9) | YOU at 10 m, bright water; breath bubble "50%"; red `Headline` "HALF"; pin "10 M" glows; hard `cut` on "metres" | hold | `bubbles`, cut to silence |
