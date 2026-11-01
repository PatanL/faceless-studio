---
series: horror-new-building-rules
title: Never Give Anyone Your Unit Number
parts: 5
format: 9:16 narrated phone/door horror, horror kit (studio/src/kits/horror), Kokoro af_heart at speed 1.3
runtime_target_s: {p1: 78.8 (measured), p2: 82.8 (est.), p3: 85, p4: 85, p5: 90}
status: writing only (BRIEF hard rules: no renders, no TTS, no kit / pipeline / episodes / out/pilots edits; horror-pinned-rules paths untouched)
written_utc: 2026-11-01 ~12:55-13:30
canon_sources:
  - backlog/horror/horror-new-building-rules/script.md (Part 1 as written and measured: canon, unchanged)
  - backlog/horror/horror-new-building-rules/narration_p2.md (old 2-part ending: SUPERSEDED; its beats are redistributed to Parts 3 and 5 below)
playbook: research/corpus/horror/PLAYBOOK.md (revised 12:40 UTC, 24 outliers + 8 controls)
primary_references:
  - id: 7659677578365537569   # SIEGE-CHAT, @udhwkz, 376K, 10.79x: residents' chat run by a fake authority, unit labels, count match, clock lifeline
  - id: 7702661541224566049   # HEARSE-P1, @udhwkz, 2.2M, 63.1x: full skeleton, bookend shot, part label
  - id: 7702661471641128224   # HEARSE-P2, @udhwkz, 343K, 9.85x: sequel variant P2 and the 16% sequel decay
  - id: cVUJmsVkUW4           # MOM-NOTE, WrONG Rules, 291K, 31.0x: the rules note, withheld part of the document
  - id: 7670495663624408352   # DORM-RULES, @mraevq, 194K, 18.0x: two rival authorities, rule inversion
  - id: 7694996216505060641   # FLOOR-PHRASE, @udhwkz, 613K, 17.6x: reactor-closeness ladder ending on the mother
  - id: kJCVK8xTkPk           # TWO-WINDOWS, Resident Guidance, 13K, 17.4x: the impossible double, perspective inversion
  - id: gDNMSoGSZgQ           # DOG-RULE, The Story Vault, 20K, 19.8x: the protector named, then that voice used as the lure
  - id: Qz-TrB6W2SM           # HOTEL-DOOR, Wansee, 1.52M, 9.0x: door volume ladder, retro-reveal after safety
  - id: 7659482056656735521   # TWO-SUSPECTS, @lehwh7, 1.9M, 11.2x: the helper's knowledge slip, "full story" compile
  - id: 7650872317119057168   # FAKE-ROOMMATE, @melovebz, 134K, 23.8x: the tell that fires on the narrator last
  - id: BciSW_2VMZg           # WrONG Rules Pt3, 104K, 11.0x (vs its hookless Pt2 xKgepVHATm4, 1.0x): every part hooks cold
---

# Never Give Anyone Your Unit Number: series bible (5 parts)

## 1. Logline

At 5:12 a.m. the "Building Office" of Harrow Court asks every tenant to reply with their unit number. Harrow Court has no building office. June, two weeks into apartment 7C, has the last tenant's handwritten rules taped under her sink, and rule one forbids exactly that. Over two nights the thing behind the account asks, then borrows the voices of people she trusts, then issues rules of its own, and finally stops asking June at all: it starts asking the other resident of 7C, the one behind the locked spare-room door.

**Series promise (the one line every part restates within 15 s):** *Typing it marks you. Saying it opens.* Only the resident of a unit can give its number away.

**Why this premise (PLAYBOOK §8 premise box).** An ownable, countable rule (one number you must never give, a hall light per door as the cost); a barrier everyone knows (the front door, the residents' chat); a human-shaped threat (it borrows neighbours, a mother, and finally June herself: TWO-WINDOWS kJCVK8xTkPk 0:10 vs PIGEONS FDLk6TlVTq0); two rival authorities (the paper note vs the chat account, DORM-RULES 7670495663624408352). Demand: WrONG Rules BciSW_2VMZg 11.0x, Mr. Creeps apartment rules 873K, Lighthouse apartment rules 340K (backlog/horror/TOPICS.md #3).

## 2. Canon and what changed

- **Part 1 is canon as written and measured** in `backlog/horror/horror-new-building-rules/script.md` (78.8 s, 274 words, storyboard validated). Nothing in this bible requires a Part 1 change.
- The old 2-part Part 2 (`narration_p2.md`) packed the whole night into 83 s. In five parts its beats are spread out: the member-list "7C twice", the sunrise clock, the torn-off end of the note and the knocks from inside the spare room move to **Part 3**; the crouched listener image is retired (Part 3 gets a new held image). The new **Part 2** (script in `part2/script.md`) is the borrowed-voice siege and ends on June's double in the peephole.
- Clock, continuous across nights: P1 5:12-5:38 a.m. · P2 5:38-5:44 (as scripted: 5:41 on screen) · P3 5:44-6:04 (sunrise 6:04) · P4 the same day 11:40 a.m.-11:59 p.m. · P5 night two, 12:00-5:12 a.m. (ring back to the hook hour).

## 3. The building (fixed map, never contradict)

Harrow Court, 9 floors, one elevator, one stairwell. Floor 7, left to right down the corridor: 7A (Mrs. Kowal), 7B (Priya), 7C (June, end of the corridor, opposite the trash room), 7D (Sam), 7E (Tess), EXIT door to the stairwell. 3B is Odette. 8A is Dale. 1A is Walt, the super, the only staff. There is no building office. The residents' chat ("Harrow Court Residents") has one member per unit **plus one** "Building Office" account with a grey house avatar, plus (revealed P3) a second 7C member: **D. Rowe**.

Inside 7C: front door with chain and peephole, kitchen with the note under the sink, bedroom, and a **spare room** the letting agent called "owner's storage, key lost". The spare-room bolt is on June's side (P2 plant). The building's floor plan shows a wall where that door is (P4 payoff).

## 4. Recurring characters and puppet sets

The kit has two rigs (`studio/src/kits/horror/characters.tsx`): **Protagonist** ("Nora" art: dark bob, olive hoodie) and **Neighbour** ("Hale" art: gaunt, grey comb-over, moustache, maroon cardigan; alias Stranger). Both take any expression from `EXPRESSIONS`, poses `idle | phone | ear | cover | sit`, `light none | phone | red`, `silhouette`, `blink`, `lookX/lookY`, `tilt` and `colors {hair, top, topShade, skin, shirt}`. Every character below is built from those props only (no kit edits; the kit is locked to the horror closeout lane). Mr. Hale's own look is the fake-management face in the locked pilot, so this series always recolours the Neighbour rig.

| Character | Role / arc | Rig + colours | Expression set (kit names) | Poses / light | Never |
|---|---|---|---|---|---|
| **June** (7C) narrator, late 20s | New tenant; keeps rule one for two nights; P5 decides who 7C belongs to | Protagonist, default colours (her olive hoodie is the identity tell for her double) | `neutral` (baseline, P4 daylight), `worried`, `scared`, `terrified` (one use per part, at the peak), `suspicious` (reading the Office), `shocked` (twists), `relieved` (false relief only), `angry` (P4 confronting Walt), `sad` (P5 ending) | `phone` with `light: phone` for every chat beat; `cover` at each silence beat; `sit` (back to the cabinet under the sink) in P3 and P5; `ear` on calls | never smiles on screen before the P5 ending |
| **June's double** (the Office wearing June) | Appears once in P2 (peephole), once in P5 (spare-room doorway) | Protagonist, same colours, `blink: false` | `stare` (talks with barely moving lips), `grin` (one frame max, P5 only), `blank` | `phone` with `light: red`; `lookX 0, lookY 0` locked to the lens | never blinks, never in daylight |
| **Odette** (3B) ally, 30s | The voice of reason in the chat; the viewer-proxy who speaks objections; Alt ending B makes her the first one taken | Protagonist recoloured: `hair #8a4b2a` (copper), `top #2f5d62`, `topShade #244a4e` | `worried`, `suspicious`, `scared`, `relieved`, `sad`; Alt B only: `sly`, `stare` | chat-only in P1-P3 (avatar initial "O"); on screen P4 (`idle`, `ear`) | never says or types her own unit after P1's "3B" label |
| **Dale** (8A) joker | Breaks rule two in P1, lost on "floor six" in P2, comes back polite in P4 | Neighbour recoloured: `hair #5a3b22`, `top #c4622d`, `topShade #9c4c22` | before: `smile`, `sly`, `surprised`; taken: `smile` with `blink: false`, `blank` | `idle`; P4 `phone` | never seen on the stairs (photos only) |
| **Mrs. Kowal** (7A) rule-lover | First to reply ("sorry, I like rules"); her light is the one that comes back at sunrise (P3), and she is the P3 cut: the first taken to knock, quoting rule three; P4 opens with her leading the four | Protagonist recoloured: `hair #b9b6ae`, `top #6c5a86`, `topShade #574873`, `skin #e2d3c2` | before: `worried`, `smile`; taken: `smile` + `blink: false`, `stare` | `idle`, `cover` | — |
| **The taken** (7B Priya, 7D Sam, 7E Tess) | Lights out in P1; back in daylight in P4, polite, in reply order | Neighbour (Sam) and Protagonist (Priya, Tess) recoloured in muted greys, `pale` comes with `blank` | `smile` + `blink: false`, `blank`, `grin` (P4 peak only) | `idle` in a doorway | never speak in contractions (the "taken" register: full sentences, full stops, from P1's Mrs. Kowal posts) |
| **Walt** (1A) the super | The only real staff; P4 outside check; installed the bolt for D. Rowe two years ago | Neighbour recoloured: `hair #8d8d92`, `top #2b3a55` (navy work jacket), `topShade #22304a` | `neutral`, `suspicious`, `surprised`, `sad`, `angry` | `idle`, `ear` (on a call in P3's voice ladder: voice only) | his voice at a door in P2 is the Office, never Walt |
| **D. Rowe** (7C, "the last tenant") protector or not | Wrote the note; lives in the spare room; online in the chat; the P5 question | Neighbour, `silhouette: true` (eye glints only) through P4; lit only in the P5 ending: default colours greyed (`top #3c3c42`) | silhouette has no face; P5 lit: `sad`, `blank`, `relieved` (Ending A, as he leaves) | `idle`, `sit` | never shown lit before 75% of Part 5 (the Ending A exit at 68-78 s) |
| **The Building Office** | The thing; speaks only through the chat and borrowed voices | no puppet: chat account, grey house avatar, `kind: 'alert'` bubbles | — | — | never has a face of its own; never explains itself |
| **June's mother** | Voice only (P2 the door; P2 the real call) | — | — | — | never on screen |

Speech registers (cheap to track, PLAYBOOK §4A typography ladder, T42u5xhrq-0 0:50-0:51): living people text in lowercase with no full stops; the Office and the taken write in sentence case with full stops. A living person's account switching to full stops is always a casualty proof.

## 5. The rule system

### 5A. The hidden laws (writers only; never stated in full on screen)

1. **Typing it marks you.** A resident who types their own unit number to anyone loses the light over their door (countable, P1).
2. **Saying it opens.** A resident who says their unit number aloud, inside the unit, opens it to the Office: the hall light goes out (as with typing) and the Office occupies the person; by noon they come back polite (P4). Opening the physical door does nothing by itself, which is why every voice asks for the number and never just to be let in (P2 editor fix).
2a. **It hears the unit.** Once it has asked a unit, it hears anything said aloud inside it (that is how law 2 works). This is where the pet name "Junie" comes from in P2: two weeks of June's calls with her mother, before the door ever used it. It cannot hear typing, and it cannot hear inside the unnumbered room (law 4).
3. **Only the resident can give it.** The Office can start the sentence in any voice, even June's, but it cannot finish it (P2 cliff). That is why it borrows trusted voices: it needs the resident to complete the line.
4. **The Office can only ask for rooms on the plan.** The spare room was built into a wall cavity after the plan was filed. It has no number, so it is the one place the Office cannot ask for. D. Rowe has hidden there for two years.
5. **Sunrise pauses it.** From sunrise to midnight it cannot knock; it can still post in the chat and send the taken.
6. **A unit with two residents can be given by either one.** Night two (P4-P5) it stops working on June and works on D. Rowe.
7. **A resident can only leave by handing the unit over.** Someone else must say "this is mine" aloud with the number. This is the law D. Rowe has been waiting for (Ending A). Writers' backstory (never stated in full): Rowe said "7C" aloud two years ago, survived only because he had already had Walt build the unnumbered room and bolt it from the outside, and has lived there since; the bolt is on the outside because the room's only safety is that nobody inside it can be talked into opening it.
8. **Nothing breaks these laws on screen.** No object moves by itself and no knock happens between sunrise and midnight except from the taken (law 5). Every scare is a person (living, taken, or borrowed) doing something the laws allow. (Editor pass: the old P4 cliff had the bolt slide on its own, which no law allowed.)

### 5B. The two rulebooks (what the viewer counts against)

**The note (D. Rowe, paper, taped under the sink)** — shown on paper close-ups, white text, red only on the verb:

| # | Rule | Stated | Paid |
|---|---|---|---|
| 1 | Never give anyone your unit number. Not even the building. | P1 0:06.6 | every part; P5 is the only time June says it |
| 2 | No stairs after midnight. | P1 0:13.5 | P2 (Dale's floor-six photos) |
| 3 | If your hall light goes out, stay inside until sunrise. | P1 0:14.9 | P3 (sunrise 6:04; only 7A's light returns) |
| 4 | If someone you know asks your unit, it isn't them. | P1 0:17.9 | P2 (Odette's voice, Walt's, her mother's, her own) |
| torn end, front | I never left 7C. Whatever knocks, it isn't me. | P3 end (slides out under the spare-room door) | P5 (both readings: he never moved out / he never stopped being the resident) |
| torn end, back | 5. If it says two residents, it means the room. Keep the bolt shut. | P4 (June turns the slip over in daylight) | P4 cliff (the note's own author asks her to open it) and P5 0:00 (she has) |
| 6 | (June's own, written in P5 Ending A) Never give anyone your unit number. Not even me. | P5 last shot | ring to P1 line 1 |

**The Office's rules (chat + an elevator notice)** — each one mirrors a note rule inverted (T3 rule inversion, DORM-RULES 7670495663624408352 50-63%; the two-rival-authorities engine, PLAYBOOK §1D):

| Part | Office says | Inverts |
|---|---|---|
| P1 | Please reply with your unit number. / The stairs are fine. / The note under the sink is out of date. | rules 1, 2 and the note itself |
| P2 | (no posts; it speaks through voices at the door) | rule 4 |
| P3 | Every unit on seven has replied except one. / 7C? | rule 1 as a question |
| P4 | REVISED HOUSE RULES (elevator notice + pinned post): 1. The note under the sink is void. 2. The stairs are open. 3. Hall lights belong to the building. 4. If someone you know asks your unit, help them. 5. Unit 7C has two residents. Tonight, one will reply. | rules 1-4 one for one, then a fifth that answers the torn back |
| P5 | @7C @7C (tagging both members); finally: Thank you. Unit 7C is complete. | — |

### 5C. Escalation by part (two ladders always running, PLAYBOOK §4A)

| Part | Office's method (tier) | Proximity ladder | Channel-removal ladder | Cost the viewer counts |
|---|---|---|---|---|
| P1 | **Ask** (chat request, roll call) | corridor → one door closer per reply → June's door | building office → neighbours → the note "out of date" | 4 lights out on floor 7 |
| P2 | **Borrow** (voices of people she knows, then her own) | Odette's voice → Dale → Walt → her mother → June herself | Odette's chat (alive) → the call to her mother (drops) → battery 9% | the double starts "this is June, from Seven…" |
| P3 | **Wait** (sunrise clock, bare unit as a question) | the door → the spare room behind her | Odette goes quiet → D. Rowe's DM is the last channel | 3 of 4 lights stay dark at sunrise |
| P4 | **Rule** (daylight notice, the taken come visiting) | the taken in the corridor → at her door with a casserole → Walt's own office | Walt's records → the floor plan → the slip's back | 5 Office rules vs 4 note rules |
| P5 | **Trade** (it works on the other resident) | the spare-room bolt → the spare-room door → the threshold | chat tags both 7C members → Odette's line → D. Rowe's voice | one sentence: "This is mine. Seven-C." |

## 6. Cliffhanger chain

Every part cuts at the point of greatest need with one new imperative or reveal (PLAYBOOK §4C ending 1; SIEGE-CHAT 7659677578365537569 4:05-4:08) and opens the next part with a frame-0 jolt that a cold viewer understands in 3 s (PLAYBOOK §5, a cold hook inside 3 s for every part: BciSW_2VMZg Pt3 11.0x vs xKgepVHATm4 mid-list Pt2 1.0x; HEARSE-P2 7702661471641128224 took until 0:20 for its hard hook and got 16% of Part 1). No recap narration; the premise line comes back in fresh words by 15 s instead.

| Cut | Last line (spoken) | Last image (held, then part card) | Next part, first 3 s (frame 0 = cover) | PLAYBOOK mechanic + reference |
|---|---|---|---|---|
| **P1 → P2** | "Two." (the third knock lands on the cut) | FrontDoor, chain on, knock 3 shakes the frame; end card bookends frame 0's request "Reply with your unit number." + PART 2 | knock 3 on frame 0, then Odette's voice through the door: "June? What's your unit again?" as the first words (~1.6 s; was 3.6 s), rule 1 on screen from frame 0 | cut on a counted beat with a part label (HEARSE-P1 7702661541224566049 3:16-3:21.9 bookend + label); cold hook ≤3 s fixes HEARSE-P2's 0:20 hook (7702661471641128224 0:00-0:20) |
| **P2 → P3** | "It stopped. And waited for me to finish." | Peephole ring: June's double, `stare`, phone lit red, lips parted on "Seven"; 1.2 s silence; card PART 3 | three hard knocks **from inside the spare room**, louder than the door, on frame 0; VO: "It got as far as Seven. Then my spare room knocked back." | threat on both sides of the barrier (T42u5xhrq-0 0:31-0:33 "in your room"); voice swap onto "you" (TEXT-FIGURE T6, T42u5xhrq-0 0:51-0:56); greatest-need cut (7659677578365537569 4:05) |
| **P3 → P4** | Mrs. Kowal, through the door, two soft neighbour taps at 6:04: "Good morning, June. The sun is up. Rule three is over." (editor fix: was "Three knocks" from the spare room, which repeated P3's own cold open) | FrontDoor in grey dawn light, Kowal's feet shadow, 7A's lamp lit again in the peephole; June `shocked`, hand on the chain; card PART 4 | daylight cold open: Kowal at the front of four neighbours in the corridor in reply order, smiling, unblinking; VO: "She was only the first. By noon, all four who replied were back. In the order they replied." | retro-reveal after safety (HOTEL-DOOR Qz-TrB6W2SM 2:28-2:39); the protection expires on the clock and the threat quotes the rulebook back (rule inversion, DORM-RULES 7670495663624408352 50-63%); count match as the next hook (SIEGE-CHAT 7659677578365537569 0:24 / 1:54, four = four) |
| **P4 → P5** | "The note said keep the bolt shut. The man who wrote it was asking me to open it." (editor fix: was the bolt sliding on its own, which broke the laws) | 11:59 p.m.: June's hand on the spare-room bolt; laptop above it shows two things at once: the Office pin "Unit 7C has two residents. Tonight, one will reply." and a lowercase DM from D. Rowe, "its asking me now / open the bolt before midnight / please"; card PART 5 / FINAL | frame 0: the bolt already drawn, the spare-room door an inch open, black inside; a man's voice: "Don't touch the handle. It's not here for you tonight." (she opened it: the choice is shown as done, not explained) | the two rulebooks collide inside one person: the note's author against the note (two rival authorities, PLAYBOOK §1D, DORM-RULES 7670495663624408352); the protector's voice as the lure (DOG-RULE gDNMSoGSZgQ 0:41.1 + ending); pre-announced failure point (NIGHT-BUS shTJ7_kRNJ8, H18) via the slip's rule 5; a decision the viewer argues about in the comments (Team Rowe, §9) |
| **P5 end** | Ending A: "Not even me." | ring shot: a new tenant's phone at 5:12, the Office's first message from P1 frame 0, word for word; under her sink, a note in June's hand; card THE END / "full story" | — (the series card points to the compile) | ring structure first/last line (TWO-WINDOWS kJCVK8xTkPk 5:06 inversion; NIGHT-BUS); complete-episode close with one loop left (FAKE-ROOMMATE 7650872317119057168, TWO-SUSPECTS 7659482056656735521) |

**Cliff strength ladder (editor pass 13:10 UTC; 1-10, what each cut takes away from June).** P1 7.0 (a counted knock: the threat reaches her door) → P2 8.0 (the threat is *her*: identity, and it only needs one word from her) → P3 8.4 (her last protection expires on the clock and a neighbour she trusts quotes the note back at her) → P4 8.8 (the note's own author asks her to break the note; the danger is now a choice inside the unit) → P5 Ending A (she makes the choice and it costs her the unit). Before the pass the ladder dipped: P3 ended on "three knocks from inside the spare room", the same image as P3's cold open (6.5, a repeat is weaker than its predecessor), and P4 ended on an object moving by itself (7.5, and it broke law 2: nothing but a resident can open anything in 7C).

Unpaid plants carried across each cut (PLAYBOOK §5 "≥2 unpaid specifics; pay one by ~45% of the next part, then open a bigger loop"):

| Planted | Plant | Paid (by ~45% of the next part unless noted) |
|---|---|---|
| P1 | the spare-room light under the door; "the rest was torn off"; Dale's lease "renews in eleven days" | P2 0:25 (light still on, bolt on her side); P3 end (torn end); P4 (Dale back, signing a renewal "early") |
| P2 | the bolt is on June's side; the Office's voice at Odette's door "using your voice"; 9% battery; "only she calls me Junie" (the door used it *before* June called her mother) | P3 0:20 (battery dies at 5:58, D. Rowe DMs on the laptop); P3 0:30-38 (D. Rowe: "it has been listening since you moved in", law 2a, pays "Junie"); P4 (Walt fitted the bolt); Alt B (Odette repeats "Junie") |
| P3 | 7C twice in the member list; Mrs. Kowal's light comes back and she knows rule three; the knock from inside (P3 0:00) | P4 0:00 (Kowal leads the four: her light came back because she was the first to be finished, law 2); P4 0:11-20 (how the taken know rule three: the Office has known the note since P1, "the note under the sink is out of date"; it heard Rowe say his rules aloud in 7C two years ago, law 2a); P4 20-30 (Walt: "if anyone knocks from inside, it isn't me") |
| P4 | the slip's back (rule 5); the floor plan wall; Office rule 5 "two residents"; Walt: "he asked me to bolt it from the outside" | P5 0:00-0:40 |

## 7. Per-part beat outlines

Tags: B1-B12 story beats and S1-S10 short beats from PLAYBOOK §1, P2 = sequel variant (HEARSE-P2). Times are targets at ~245 spoken wpm (Kokoro af_heart 1.3, as measured for Part 1). Each part: core hook ≤30 words / ≤6 s; a trusted source contradicted by ≤11 s; a jolt every ≤8 s (median ~3-4 s at this length, PLAYBOOK §3 Shorts row); one lull ≤8 s at 40-50%; turn at ~50%; the scariest image once at 60-85%, held ~4 s; no spoken subscribe.

### Part 1 — "Never Give Anyone Your Unit Number (Part 1/5)" · 78.8 s · canon

As written and measured in `backlog/horror/horror-new-building-rules/script.md` (beat table P1-1 … P1-12): the Office asks at 5:12 → the note forbids (5.9 s) → Odette: no office (11.2 s) → rules 2-4, torn end → Dale takes the stairs, the Office knows his lease → four amber lights → "the note under the sink is out of date" (midpoint) → roll call, four lights out, the knocking walks closer → Mrs. Kowal posts in full stops → 7A's door open a crack (held) → "every unit on seven has replied except one" → the spare-room light → knocks one, two, cut. Only change for the series: the end card reads PART 2/5.

### Part 2 — "It Used My Mother's Voice (Part 2/5)" · 82.8 s (estimated, not TTS-measured) · full script in `part2/script.md`

| t (s) | Beat | What happens |
|---|---|---|
| 0-3 | B1 / P2 cold hook | knock 3 on frame 0; Odette's voice at the door asks June's unit as the first spoken words (~1.6 s); "RULE 1: Never give anyone your unit number." on screen from frame 0 (editor fix: was "Third knock." first, question at 3.6 s) |
| 4-8 | B2 rule restated | rule 4 on the note: someone you know asking means it isn't them |
| 8-17 | B4 outside check | June texts the real Odette: under her bed on floor three, it's at her door too, using June's voice; Odette gives the series line and says the last tenant taught it to her |
| 17-21 | premise restated | four typed, four lights out, June's still on |
| 21-32 | B5 rung 1 + P1 plant paid | Dale's voice; his three stair photos, 5:16/5:19/5:23, floor six every time; rule two |
| 32-38 | B7 lull + plant | light under the spare-room door; "owner's storage"; the bolt is on her side |
| 38-42 | B8 turn (47%) | Odette: it knocked on both doors in the same second; one voice, two floors (scale-up, T10) |
| 42-46 | clock | sunrise 6:04, phone 5:41, 23 minutes, 9% battery |
| 46-54 | B5 reactor ladder | Walt the super (a gas-leak "log"), then her mother, using the pet name only she uses; every voice asks for the number ("which door is yours?", "your unit for the log", "what number are you?"), never to be let in (law 2) |
| 54-65 | B10 lifeline | June calls her real mother; the door repeats her mother's words half a second later; the call drops |
| 65-74 | B9 peak image (79-89%) | the peephole: June herself, her hoodie, her phone lit, staring; 2 s hold |
| 74-83 | B11/B12 twist + cut | the double, in June's voice: "Hi, this is June, from Seven" stops and waits for her to finish; cut, PART 3 |

### Part 3 — "Someone Else Lives In 7C (Part 3/5)" · 85 s

| t (s) | Beat | What happens |
|---|---|---|
| 0-3 | P2 cold hook | three knocks from inside the spare room on frame 0; "It got as far as Seven. Then my spare room knocked back." |
| 3-10 | B4 | the double goes silent; the peephole is empty; the series line restated by Odette in one text; rule three: stay in until sunrise |
| 10-20 | B4 plant paid (P1/P2) | the chat member list: 7C twice. June, and D. Rowe, the name on the note. Online. Typing. |
| 20-30 | B6 isolation | phone dies at 5:58 (the 9% pays); laptop on the kitchen floor; Odette's last message is delivered, not read |
| 30-38 | B7 lull | June DMs D. Rowe from the laptop: are you in my spare room? He answers instantly, lowercase: don't answer it, not even to me / dont say anything out loud / it has been listening since you moved in (law 2a; pays P2's "Junie") |
| 38-44 | B8 turn | the Office posts "7C?" in the chat, both 7C members tagged; for the first time it is not sure which one it is talking to |
| 44-58 | B5 bare-number ladder | the door stops using names, says only the unit as a question, louder each time (HOTEL-DOOR Qz-TrB6W2SM 1:25-1:41 polite → silence → command) |
| 58-66 | B9 peak image (68-78%) | under the front door, in the hall-light gap, four shadows of feet side by side: the four who replied, standing at her door; held 4 s, heartbeat only |
| 66-72 | B10 clock | 6:02, 6:03, 6:04; the knocking stops; Mrs. Kowal's light comes back, the other three stay dark; June `relieved` (false relief) |
| 72-78 | B11 twist after safety | the torn-off end slides out under the spare-room door: "I never left 7C. Whatever knocks, it isn't me." |
| 78-85 | B12 cut (editor fix) | two soft taps on the front door, a neighbour's knock, not the Office's (law 5: after sunrise only the taken knock). Mrs. Kowal, in full sentences: "Good morning, June. The sun is up. Rule three is over." She knows the note. Cut, PART 4. (Was: three knocks from inside the spare room, the same image as 0:00) |

### Part 4 — "The Building Posted New Rules (Part 4/5)" · 85 s

| t (s) | Beat | What happens |
|---|---|---|
| 0-3 | cold hook (count match) | daylight corridor: Kowal, Priya, Sam, Tess (+ Dale behind) in reply order, smiling, unblinking; "She was only the first. By noon, all four who replied were back. In the order they replied." |
| 3-11 | B2 new authority | the elevator notice and the pinned post: REVISED HOUSE RULES 1-4, each the note's rule turned over; June reads them against the note (two rulebooks side by side on screen) |
| 11-20 | B4 outside check | June finds Walt in 1A: "there's no building office", and the floor plan: the spare room is a wall |
| 20-30 | B5 | Walt, `sad`: two years ago D. Rowe paid him to build the room and bolt it **from the outside**, and told him "if anyone knocks from inside, it isn't me" |
| 30-37 | B7 lull + plant | June turns the slip over in daylight: rule 5, "If it says two residents, it means the room. Keep the bolt shut." |
| 37-45 | B8 turn (~50%) | Sam (7D) at June's door with a casserole, perfect sentences: "May I come in. I only need the number for the dish." (Sam, not Kowal: Kowal already had the P3 cut.) The taken can't come in unless invited, but they can ask |
| 45-56 | B5 / B6 | Odette on screen at last (1A lobby, `worried`); her own light is still on; Dale signs his lease renewal "early" in the lobby, in full stops; Walt's phone gets a chat invite from the Office |
| 56-66 | B9 peak image (66-78%) | Walt opens the chat to show June the account: its profile says "member since" two years ago, **unit 7C** |
| 66-76 | B10 clock | 11:40 p.m., 11:50, 11:58; June sits with her back to the bolt; Office pin goes up: "Unit 7C has two residents. Tonight, one will reply." (Office rule 5) |
| 76-85 | B11/B12 (editor fix) | 11:59: a DM from D. Rowe, lowercase (alive): "its asking me now / open the bolt before midnight / please". June's hand on the bolt, the slip's rule 5 beside it. "The note said keep the bolt shut. The man who wrote it was asking me to open it." Cut, PART 5 / FINAL. (Was: the bolt slides back on its own, which no law allows) |

### Part 5 — "Unit 7C Is Complete (Part 5/5, Final)" · 90 s

| t (s) | Beat | What happens |
|---|---|---|
| 0-3 | cold hook | the bolt already drawn (June chose; shown, not told), the spare-room door an inch open, black inside; a man's voice: "Don't touch the handle. It's not here for you tonight." |
| 3-12 | B2 / B4 | D. Rowe, a silhouette in the gap, speaks for the first time; rule 5 restated (two residents); the Office tags @7C @7C |
| 12-24 | B5 | the front door knocks with D. Rowe's own voice asking for his unit, from the hall; inside the spare room he goes silent, then whispers "it's using me now" |
| 24-34 | B7 lull + plant | D. Rowe explains one law, slowly: he can only leave if someone else says the unit is theirs, aloud |
| 34-44 | B8 turn (~45%) | Odette texts: it's at her door with June's voice again, and she is about to answer; June needs the knocking to stop now |
| 44-60 | B5 / B10 | D. Rowe: "say it to me, not to the door, then it stops asking either of us"; the knocks climb (Odette's, Dale's, her mother's, June's); 5:10, 5:11 |
| 60-68 | B9 peak image (67-75%) | the spare-room doorway: June's double standing behind D. Rowe's silhouette, `grin`, one frame, then `stare`, held |
| 68-78 | B11 truth twist (~80-87%) | June says it: "This is mine. Seven-C." The knocking stops. D. Rowe steps out lit for the first time (`relieved`), takes the chain off and walks out; "D. Rowe left the group." Her hall light goes out. Saying it opened it. He needed a replacement, and the rules kept her alive long enough to be one. Why she is not occupied (law check): she says it standing inside the unnumbered spare room, to Rowe, as he steps past her, so the Office opens 7C (light out, "Unit 7C is complete") but cannot reach the room she is in; exactly what Rowe did two years ago (law 7 backstory). She now cannot leave until someone else says it |
| 78-86 | B12 aftermath | June in the spare room (`sit`, then `sad`), writing on the back of a lease page; tape; under the sink |
| 86-90 | ring | 5:12 a.m., a new tenant's phone: the Office's P1 message word for word; under the sink, June's note: "Rule one. Never give anyone your unit number. Not even the building." VO, last line: "Not even me." THE END |

## 8. Endings

**Canonical — Ending A, "The Replacement"** (outlined above). T9 the trusted helper betrays (FLOOR-PHRASE 7694996216505060641 kicker) + T17 perspective inversion (TWO-WINDOWS kJCVK8xTkPk 5:06: the rule now describes you) + ring structure. Loops left open (complete-episode shape, PLAYBOOK §4D, ≤2): where D. Rowe went (his account shows up in another building's chat in the pinned comment); whether Odette ever answered.

**Alternate ending B, "Odette Was First"** (T14 knowledge slip, TWO-SUSPECTS 7659482056656735521 ~80%; T15 evidence erases itself, wh9ESTS69Dk). Swap P5 68-90 s: Odette texts that she has June's mother's voice at her door "calling you Junie". June never told Odette the pet name; the only other one who heard it was the door (P2 plant pays). June scrolls up: Odette's texts started at 5:13, one minute after the Office's first message, and the chat export shows a line at 5:12 nobody saw: "3B." Odette was the first reply; every "real Odette" text was the Office playing the helper. June keeps the bolt shut, as D. Rowe asks; at 5:12 the thread erases itself to one bubble. Last line: "Odette's light had been out the whole time. Mine is still on." Leaves 3 loops (keeps the door open for a season 2). Costs: needs the "Junie" plant kept exact in P2 (it is) and Odette's P1 line "we don't have a building office" to read as the Office building trust (it does: the Office never claims to be an office once June doubts it).

**Alternate ending C, "Moving Day"** (T11 fake win, TRUCKER-RULES 7692268145888873760; PLAYBOOK §4C ending 10, the threat moves into the viewer's phone, APP-STALKER 02nCBx8WqW0). P5 keeps the bolt shut all night: June never says it, D. Rowe never answers, and at sunrise she is out with two bags. Final 15 s: a new building across town, the agent's welcome text, a new residents' chat. 5:12 a.m.: "Building Office: Welcome, June. Please reply with your unit number." Her new hall light flickers once. Last line: "I haven't told anyone my new address. It didn't ask for that." Best standalone tone; weakest for a full-story compile because it reopens the master loop.

Decision rule: pick after Part 3's comments. If "Team Rowe vs Team Not Rowe" (P3 pinned) splits near even, ship A (it pays both sides). If Odette is the most-named character in P2-P3 comments, ship B. Ship C only if Parts 4-5 are cut for decay (it can attach to Part 3 as a 2-part close).

## 9. Comment bait and pinned-comment plan

Rules: no spoken subscribe or app funnel (PLAYBOOK §4C, mraevq control 1.06x); one in-premise question per part, carried by the pinned comment and the end card, never by the narrator (NIGHT-BUS shTJ7_kRNJ8 asks one in-premise question at 49%; we move it off the audio). **Never ask viewers for real personal details** (real unit numbers or addresses): every question is about the story's units. Pinned comments come from the channel account only; no fake "Building Office" commenter accounts (R5 inauthentic-content policy).

| Part | Built-in bait (on screen, never spoken) | Pinned comment (posted with the video) | Reply plan (first hour) |
|---|---|---|---|
| P1 | the torn edge of the note, held on screen for 0.8 s; the four amber lights for counting | "The bottom of the note was torn off. What do you think rule 5 said? Best guess gets pinned on Part 2." | heart every rule-5 guess; pin the winner on P2 as a second pinned reply |
| P2 | Dale's three photo timestamps (5:16, 5:19, 5:23) are readable; the battery reads 9% | "Which voice would have got you: your neighbor, the super, or your mom? (Do not finish June's sentence.)" | reply "it stopped on Seven for a reason" to anyone who finishes it with a letter |
| P3 | the member list shows 7C twice for 1.5 s (freeze-frame bait) | "Team ROWE: he's protecting her. Team NOT ROWE: whatever knocks, it isn't him. Pick one." | count the teams; P4's pinned comment reports the score |
| P4 | the two rulebooks side by side for 3 s | "The Office's new rules flip the note one by one, except one rule that's new. Which one, and what does it mean for tonight?" (answer: rule 5) | reply with the slip's rule 5 to the first right answer |
| P5 | the new tenant's chat shows a unit number we never say | "June's note has one new line. If you had to leave the next tenant one rule, what would it be?" + link to the full-story compile | pin a viewer rule as "the next note"; seeds a season-2 anthology |

## 10. Series mechanics (PLAYBOOK §5) applied

- **Sequel decay** (HEARSE-P2 7702661471641128224 got 16% of P1; TopScaryClips pt3 8% of pt2): every part is written as a pilot: frame-0 threat, forbidden question or knock by 3 s, contradiction by 11 s, the series line restated by 15 s.
- **Post order:** post Part N+1 a few seconds *before* re-surfacing Part N only when releasing a pair (udhwkz posted P2 9 s before P1). For this series: P2 and P1 go up together (P2 first), then P3, P4, P5 one per day at the same hour; P5 day also posts the full-story compile.
- **Labels:** "(Part N/5)" in the title and the end card; the end card repeats frame 0's request so the last shot bookends the first (HEARSE-P1 7702661541224566049 3:16-3:21.9). Hashtags: #HarrowCourt #June7C #NeverGiveYourUnit on every part (recurring character-name tags, mraevq pattern, PLAYBOOK §5).
- **Cut point:** each part closes its own early loops before 50% and leaves every loop opened after 50% open (open at each cut: P1 4, P2 4, P3 4, P4 4, P5 2).
- **Full story compile:** after P5, stitch P1-P5 into one ~6:30 upload with "the end" (FAKE-ROOMMATE 7650872317119057168 23.8x and TWO-SUSPECTS 7659482056656735521 11.2x are compiles; PLAYBOOK §5 on stitched full stories). In the compile the cold-hook recaps are trimmed and the micro cadence kept (§1C).
- **Fallback if decay is steep:** stop at Part 3 (Ending C bolted on) and move the world into an anthology with file numbers (TWO-WINDOWS kJCVK8xTkPk "file 017", NIGHT-BUS shTJ7_kRNJ8), where each upload is a pilot.

## 11. Production notes (for the build lane, not done here)

- Sets: FrontDoor (knocks, chain, feet shadow), Peephole ring (as P1 built it: Hallway + inline SVG lamps + ring mask), Hallway (daylight variant via `lights 3`, no `flicker`), Stairwell (`floor "6"`) in a photo border, LivingRoom (kitchen stand-in for the note), Bedroom (the spare-room door is inline SVG with a light gap, as in P1), ElevatorPanel (P4 notice taped beside it).
- The double (P2, P5) is the Protagonist rig inside the peephole ring mask, `expr stare`, `blink false`, `light red`, `pose phone`. No kit edit needed.
- FX budget per part: one RedText (P2: none; P3: "7C?"; P4: "VOID"; P5: "Not even me."), Glitch only on reframes, Heartbeat into each peak.
- Numbers are spelled out in TTS lines; captions and phone UI keep digits (P1 convention).

## 12. Risks

- Five parts of one night-and-a-half may decay faster than the corpus pair (n = 1 pair for decay data). Mitigation above: compile + stop-at-3 fallback.
- The double in P2 and P5 is the same device twice; P5 uses it for one held image only and adds D. Rowe's silhouette so it reads as a new picture.
- Editor pass 13:10 UTC (review.json): the P3 and P4 cuts were rebuilt so the cliff ladder climbs every part and no object acts outside the laws; P2's hook now asks the forbidden question as its first words. If P3's Kowal cut tests weaker than P2's double, the fallback is to keep it and move the spare-room knock (P3 0:00) to P3's B5 ladder, never to end two consecutive parts on a knock.
- P4 is a daylight part (no knocking by law 5). It carries its jolts with the taken, the paperwork and the Office's new rules; if its jolt median measures above 5 s, cut the Walt backstory (20-30 s) to one line.
