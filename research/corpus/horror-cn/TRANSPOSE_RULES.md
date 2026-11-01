# Transpose rules: writing an original story from a source's mechanics

Internal research. This file turns the 10 horror-cn studies (`BV*.md` in this folder) into a method for writing **original** stories in the 规则怪谈 / 悬疑脑洞 / 沙雕 suspense register. We learn the niche from these sources. We never translate, retell or remix one of them for publication (BRIEF rule 5, `SOURCES.md`). Many of these premises are themselves web-fiction adaptations that several studios animated, so "it's only a loose retelling" is both an originality problem and a rights problem.

The mechanics catalogue, with frequencies and timing medians, is in `research/corpus/horror/PLAYBOOK.md` § "Chinese source mechanics". Mechanic ids below (M1–M26) refer to that table.

Two gates run on every horror script, and both must print PASS:

```bash
python3 scripts/originality_check.py <script.md> research/corpus research/library/transcripts   # wording
python3 scripts/plot_similarity.py   <script.md> research/corpus/horror-cn                      # plot
```

`plot_similarity.py` fails a script that reuses a source's specific combination: 3+ specific events in the source's order, 3+ of its twists in order, or a source name plus a signature clue. Sharing generic mechanics does not fail it. It is lexical, so it can't see a rewrite that swaps every noun but keeps the twist *types* in the source's order. The checklist in §4 covers that by hand.

The worked examples in §5 are outlines, not narration. This folder is inside `research/corpus`, which `originality_check.py` scans, so a script built on one of them still needs its own lines.

---

## 1. The rule in one paragraph

Take the **engine**, not the **car**. An engine is a mechanic plus its timing: "an outside channel only the hero can see contradicts the authority within 10 s", or "every adviser's rule backfires and discredits the last one". A car is the source's expression of it: the fake cop and the danmaku overlay, the red bed curtain, the hearse and the cloth. From one source keep **at most three** generic mechanics, put **at least one** in a different order or role, and invent everything concrete: place, cast, threat, the clue's physical logic, the twist chain, the ending's motive and every line. Then add **one mechanic that source does not use**, so the skeleton itself is new.

## 2. What to keep (genre mechanics, free to use)

These come from the GENERIC lists in the 10 studies. They are the niche's grammar. They are not anyone's story.

- **Opening contract.** The premise or rule is complete by about 7 s (median; range 6–10). No intro, no title card. The title states the uncanny premise in one sentence (M1).
- **A rule system the viewer can count.** One rule or a short numbered list. Rules backfire, invert, or turn out to be planted by the threat (M2, M3).
- **Trusted source contradicted** within the first ~15% of the runtime, by a channel the viewer can see: a text, a log, a camera label, a recording, a document (M5, M11). All 10 sources do this.
- **A countable clue.** A number, a schedule, a headcount or a weight that makes someone's story impossible (M7; 10/10).
- **The barrier.** A knock or a voice at a door, a seat, a bunk, a phone. The voice uses a familiar name (M8, M20).
- **Isolation with one live channel.** Signal gone but the chat works; help is N minutes away (M10).
- **Knowledge leak.** Someone knows a thing they couldn't (M15; 7/10). This is the cheapest fair-play tell.
- **A test the hero can run**: a question only a local knows, a physical check, a machine's verdict (M14).
- **Rotating suspicion.** Two or three suspects or advisers, each discrediting the last with one piece of evidence (M12, M6).
- **The helper is the threat**, or the hero was ahead all along and explains it after the escape (M5b, M21).
- **Frame break** (a recording, a reconstruction, a test) or **the narrator is implicated** at the end (M19, M22).
- **Tempo.** A new turn about every 14 s in sources under 8 minutes and about every 27 s in the long ones; about one twist a minute; the main twist at about 85% of the runtime.

## 3. What must change

| Layer | Must change | Why |
|---|---|---|
| **Setting** | The place, the occasion and the social unit. Not a dorm with bunk curtains, a housing-complex WeChat group, a zoo, a bullet train, a hearse convoy or a New Year's Eve dinner, unless the rest of the story is unrelated. | The setting carries half the premise. "Killer in the complex" plus "group chat" is already the R2 seed. |
| **Characters** | Names, the relationship web and the roles' functions. No Chen Jie, Wang Qiang, Uncle Wang, Professor Han, Xiaoru, the Aunt or any name in a SPECIFIC list. Don't keep a source's role trio (smart narrator + dim friend + stranger who is the monitor; grandfather + father + helpful neighbour). | A renamed cast with the same functions is a retelling. |
| **Threat** | The creature or entity and its rule of operation. Not a teeth-grinder, a dream-eater fog, a 伪人 with heart-flesh reproduction, a road soul that needs a pass, a zoo dinosaur with your DNA. | Each source's monster is its signature. |
| **Clue specifics** | The object, its physical logic and the number. Not exactly six posters / seventh flat, 400 kg down eight floors, 2 a.m. then 4 a.m., a hill too low for lightning, the face you can't dream, the plate J1574. A *count clue* is generic. *Its math* is specific. | The clue is what viewers remember and repeat in comments. |
| **Twist chain** | The order and the triggers. Don't follow any source's twist inventory in order, even with new nouns. Don't end on the same twist type *with the same motive* (shut the door after "I'm sorry"; "the zoo is ours"; insurance collected; the son signs the father's contract). | Each SPECIFIC list says the chain itself counts as retelling. |
| **Lines** | Every line, in any language. No quoted line from a study, no translation of one, no near-paraphrase ("the fire was fake but the trap is real" → "the flood was fake but…"). | `originality_check.py` catches wording. Paraphrased signature lines are still recognisable. |
| **Visual signature** | The hero's costume code, the overlay's look and the central prop. No neon-yellow lightning jacket, no blue "system window" overlay, no red curtain as the only saturated colour. | These read as the studio's brand. |

**Culture-specific engines need a native equivalent.** Don't import the surface. Find the Western mechanism that does the same job:

| Source engine | Job it does | Western-native equivalents |
|---|---|---|
| Folk taboo or trade lore ("every trucker knows", 拦车孝) | An insider rule in line 1 with an official and a real reason | Workplace SOP and night-shift lore (hotel night audit, hospital porter, toll plaza, security patrol); HOA bylaws; ship or base standing orders |
| Five elements, yin/yang, midnight | Makes the rules feel deducible | Building codes, machine behaviour (badge readers, camera AI, elevator logs), tides, shift schedules, physics |
| The starch-sausage price shibboleth | Book knowledge kills, lived knowledge saves | A question every local answers "wrong" by the book: what the regulars call a place, the real closing time of the gas station, which stair creaks |
| 替身 (a replacement must die in your place) | The motive behind the rules | Keep it generic (someone must take your place), but find a new mechanism: a roster, a headcount, a lease, a shift that must be covered |
| 弹幕 / "system" overlay | A channel only the hero sees, which contradicts authority | Doorbell AI labels, a hearing aid's captions, a baby monitor, a car's driver-assist warnings, an old radio scanner |
| WeChat 业主群 / 班级群 | The chorus that pressures the hero | HOA app, Nextdoor-style street chat, Discord server, dorm GroupMe, a crew WhatsApp |
| Caption self-censorship (虾人犯) | Platform safety | TikTok algospeak where needed. Never as a joke. |
| 沙雕 dark-comic ethics (locks the door on the neighbour) | A tonal spike that makes the hero vivid | Keep the spike, but give it a native flavour: deadpan practicality, a petty grudge, an HOA-style pettiness |

## 4. Method and checklist

**Method (about 30 minutes before any line is written)**

1. **Pick one primary source** for the engine (two at most), and read its §5 twist inventory and §6 GENERIC vs SPECIFIC.
2. **Write the source skeleton in mechanic ids only**, with no nouns. Example: `M1 rule → M5 trusted source flips → M7 count → M8 barrier → M5b helper is the threat → M21 hero ahead`.
3. **Cut it to three kept mechanics.** Mark them KEEP. Everything else is gone.
4. **Change the order or the role of one kept mechanic** (for example, the warning voice becomes the trap instead of the ally; the count clue is what proves the helper lied instead of what proves the authority lied).
5. **Add one mechanic the source doesn't use**, from the PLAYBOOK catalogue or a Western source (a machine's verdict, a log, a schedule).
6. **Invent the concrete layer**: setting, cast, threat, clue object and its math, the ending motive. Write the distance table (source specific → ours, as in §5).
7. **Outline the beats with timings** for the format (§5 shows 60–90 s Shorts and one series plan). Hit the PLAYBOOK timing: premise ≤ 7 s, first flip ≤ 15%, a turn every ~8–15 s in a Short.
8. Write the narration, then run both gates. Fix and rerun until both print PASS.

**Checklist (tick every box before TTS)**

- [ ] Front matter `references:` lists the source study (or studies) whose engine you used, as well as the English repost corpus scripts.
- [ ] The source skeleton is written in mechanic ids, and **at most 3** are kept.
- [ ] At least one kept mechanic changed order or role. At least one new mechanic was added.
- [ ] The setting, cast, threat, clue object, clue math and ending motive each differ from **every** study, not only from the primary source (check the SPECIFIC lists of all 10).
- [ ] No name, role trio, prop, number or line from any SPECIFIC list. No translated or paraphrased signature line.
- [ ] **The twist-type chain is not the source's.** Write ours as types in order, set it next to the source's §5 types, and make sure they don't match for 3 in a row.
- [ ] The ending is a different type from the source's ending, or the same type with a different motive and a different final image.
- [ ] One replay clue settles the truth (the sources that leave "who lied?" open lose clarity; see `BV1DbK563Eih.md` §6 and `BV1fR7szYEDq.md` §5).
- [ ] Culture-specific engines use a native equivalent (§3), not an imported surface.
- [ ] `originality_check.py` PASS and `plot_similarity.py research/corpus/horror-cn` PASS. Paste both outputs into the script's notes.
- [ ] Captions: death words handled by algospeak only where the platform needs it.

---

## 5. Worked examples

Each example starts from one source's mechanics, keeps three of them, and builds a new premise in a Western setting. The outlines were run through both gates as draft narration on 2026-11-01. `originality_check.py` printed PASS against `research/corpus` and `research/library/transcripts`. `plot_similarity.py` printed PASS against all 10 horror-cn studies: the longest matched-event chain was 1 (gate: 3), with no source names and no more than two half-weight signature words.

### Example A: suburban HOA chat (engine from BV1nEoYBBEXE, 75 s Short)

**Source mechanics (skeleton only).** A building chat posts an all-clear → an authority figure knocks → a channel only the hero can see contradicts him within 10 s → a count deduction (N confirmations = N victims, the hero is next) → the chat pressures the hero to open → comms cut → a trusted contrarian voice turns out to be the trap → the hero out-thinks it and explains after the escape → an overheard enemy plan as the cliffhanger.

**Kept (3):** a private channel contradicts the authority by ~9 s (M11 + M5); a number deduction by ~20 s (M7); the trusted contrarian voice is the trap (M5b).
**Changed role:** the number clue is what exposes the *ally*, not only the authority.
**Added:** an outside records check (a utility's recorded line) and a machine's verdict as the private channel. The threat is already inside at the end; there is no escape set piece.

**Premise.** 1 a.m. The Willow Bend HOA app says the gas leak on Aster Lane is fixed and a technician will knock to read meters. A man in a utility vest knocks. The doorbell camera labels him "No person detected."

| Time | Our beat | Kept from the source | What is new |
|---|---|---|---|
| 0–5 s | HOA push: the leak is fixed, a technician will knock, please let him in | All-clear from an authority channel | HOA app, gas meter |
| 5–9 s | Knock; the doorbell screen shows him, captioned "No person detected" | Private channel contradicts authority (M11) | A machine label, not an audience overlay |
| 9–20 s | The post has 11 hearts; the lane has 12 houses; the hearts came in house-number order, one every 90 s; she is #12 and it's 1:22 | Count deduction (M7) | Schedule math, not a poster count |
| 20–32 s | He says her name, "it takes a minute"; the street chat vouches: "took a minute, let him in" | Chat pressure | Neighbours vouch for timing |
| 32–42 s | The gas company's night line: no work orders on Aster Lane tonight | — | Records check (added) |
| 42–52 s | DM from Ruth at #11: don't open the front, come out the back, I'm by your fence; the backyard camera tags "Familiar face: Ruth" | Trusted contrarian voice | A rescue offer at a second door |
| 52–62 s | Ruth's heart came at 1:20:30, ninety seconds before hers: #11 was visited already | The voice is the trap (M5b), proved by the same schedule | One clue settles both lies |
| 62–75 s | She opens neither door. The knocking stops. The living-room camera: "Person detected: 2." She lives alone | — | The ending is an inside threat, not an overheard plan |

**Distance table.**

| Source specific (BV1nEoYBBEXE §6) | Ours |
|---|---|
| Killer in a fake police uniform | A gas technician whom the camera doesn't register |
| Danmaku livestream audience as the overlay | Doorbell AI labels (no audience, no "streamer") |
| Exactly six all-clear posters, seventh flat | Eleven hearts in house order, ninety seconds apart |
| 601 warns of bloody footprints in the lift, then the admin mutes the group | Ruth offers a back-fence escape; nobody is muted |
| Previous tenant's phone; real police describe the real manager | Gas company's recorded line |
| Lights-off kitchen ambush; floors 1–5, exit at 6; walkie-talkie plan | No ambush, no escape; the count reaches the living room |

**Series hook (optional Part 2):** who are the eleven hearts? Every heart's profile photo is now the same front door.

### Example B: cruise ship crew deck (engine from BV1DbK563Eih, 3-part series, Part 1 ≈ 90 s)

**Source mechanics.** An authority flags the roommate as not human within 5 s → rule 1 backfires on the rule-follower and seeds the identity twist → a second adviser contradicts the first with a physical test → an evidence artifact with a room match → each adviser's rule discredits the last (an authority carousel of 6 handoffs) → a doubled artifact with one extra detail → "you're the ghost" → an ambiguous selfish ending.

**Kept (3):** the authority carousel, cut to 3 advisers with one rule each (M6); the first rule backfires on *you* as the identity seed (M3); the advisers' tests are physical checks (M14).
**Changed role:** the identity twist is "you're the replacement on an old roster", not "you're the ghost". The roommate the authority flagged is the real one.
**Added:** a machine verdict (the crew palm scanner) and a single replay clue that settles who lied (the itinerary poster).

**Premise.** On her first contract, junior steward Noor shares cabin 2117, below the waterline, with Bea, a ten-year veteran. On day one the chief purser says Bea signed off in Cozumel three weeks ago: whatever sleeps in her bunk, don't answer when it says your name.

**Part 1 (≈ 90 s), ends on a new authority's call:**

| Time | Our beat | Kept from the source | What is new |
|---|---|---|---|
| 0–6 s | The purser flags Bea: "signed off in Cozumel" | Authority names the roommate as not real | Crew paperwork, not a shroud |
| 6–14 s | His rule: lock your locker with your badge every night; the ship only counts what's locked in | Rule from adviser 1 | Badge and locker logic |
| 14–26 s | 2 a.m.: her badge opens Bea's locker, not hers. Inside is a name tag with *her* name, dated 2019 | Rule 1 backfires on the follower (identity seed) | Old roster, not a lost bed |
| 26–40 s | Bea is awake: "He gives every new girl one rule." Her test is the crew-mess palm scanner. Bea: green. Noor: "unregistered" | Adviser 2 + physical test | A machine's verdict |
| 40–52 s | Bea's rule: at boat drill, stand in Haldane's lifeboat line, not ours, and hide your tag | Counter-rule | Drill logistics |
| 52–62 s | The itinerary on the cabin wall: the ship never calls at Cozumel | — | The single replay clue (added): the purser lied |
| 62–90 s | 3 a.m. intercom: "Steward Noor Haddad, report to the purser's office." Then a second voice from their own cabin speaker: "I'm already here." | Part ends on a new authority (adviser 3) | The intercom as the third adviser |

**Parts 2–3 (plan).** Part 2: the drill line's printed headcount, and adviser 3 (the night radio officer) with his own rule. The doubled artifact is the crew-portal profile: its hire date changes from this month to 2019 between two checks, not an extra face in a photo. Part 3: the purser hires a new steward under the same name every few contracts to fill the first Noor Haddad's berth, and his rules make each newcomer accept the old roster. Noor follows none of the three rules and walks off at the next port. The last shot is the crew portal listing a new hire with her name. No shut door, no "I'm sorry".

**Distance table.**

| Source specific (BV1DbK563Eih §6) | Ours |
|---|---|
| Dorm 7-404, the supervisor, the Taoist | Crew cabin 2117, the chief purser, the night radio officer |
| Red curtain of burial shroud flipping meaning | Crew badge and locker (the object never flips meaning) |
| Shoes one forward one back; incense ash with bone; lightning wood is coffin wood; the five elements | Badge-lock rule; palm scanner; drill-line rule; itinerary logic |
| News photo gains the daughter's face | Portal hire date moves |
| Survivor-envy mother; daughter refuses for love | A purser who keeps a dead hire's name on the roster |
| "You're a trapped living soul"; shuts the door on both | "You're the replacement"; she leaves, the name gets reused |

### Example C: hotel night shift (engine from BV1TEJ164EHc, 75 s Short)

**Source mechanics.** An insider trade rule in line 1 with an official and a real reason → a second rule broken before it is stated → a stranger breaks the big rule through a ritual shown in full → a companion mirrors the ritual with one step changed → an outside phone check falsifies the companion's claim → mentor chain → the expert names the entity → body-mark timer → remedies refused and failed → the villain turns out to be a victim → a reunion rite.

**Kept (3):** an insider rule in line 1 with official vs real reason (M2); the stranger breaks it first and the companion mirrors him with one step changed (a ritual template, then its mirror); a check that falsifies the companion's claim (M11).
**Changed role:** the check is a machine log, not a family phone call. The stranger's fate is shown before the companion mirrors him, so the viewer is ahead of the hero.
**Added:** a phone call from the room that should be empty, and a closing count (two of the same person). No possession tells, no expert, no mark on the body, no victim backstory.

**Premise.** Every night auditor at a highway hotel learns one rule: if the desk bell rings and the lobby is empty, you never say "one moment". Officially it's the camera's blind spot by the doors. Really, whatever you promise an empty lobby, it collects.

| Time | Our beat | Kept from the source | What is new |
|---|---|---|---|
| 0–7 s | The rule, with the official reason and then the real one | Insider rule in line 1 (M2) | Front-desk lore, not a road taboo |
| 7–15 s | The trainee props the side door with a wedge to vape. "Never prop the side door after midnight." | Second rule broken before it is stated | A door wedge, not a window spit |
| 15–27 s | A trucker at the counter hears the bell ring by itself and calls "one moment" to nobody, then asks for a second key "for my wife". He checked in alone | A stranger breaks the big rule (ritual template) | A key card as the token |
| 27–33 s | 3:10: he checks out without his luggage and walks into the dark lot | The stranger's fate previewed | Shown, not reported later |
| 33–45 s | 4:00: the bell rings twice. The trainee smiles, says "one moment", and cuts a second key for her own room | The companion mirrors it with one step changed | Two rings, her own room |
| 45–57 s | She says her cousin is driving in late. The key-encoder log: her card was cut at 4:02, and so was the trucker's "wife" card yesterday. Same minute, same room type | Check falsifies the companion's claim (M11) | A machine log, not a family call |
| 57–67 s | The house phone: room 214, the trucker's room, empty since 3:10. A woman: "My husband says thank you for the key." | — | A call from the empty room (added) |
| 67–75 s | It rings again, from the trainee's room, while the trainee stands beside the narrator, still smiling | — | The closing count: two of her |

**Distance table.**

| Source specific (BV1TEJ164EHc §6) | Ours |
|---|---|
| The 拦车孝 custom: kowtow to a hearse for coffin cloth; the cloth as a pass | The desk-bell rule; a duplicate key card |
| Plate J1574, 47 km, a dozen deaths a year, road 107 | No numbers carried over: 4:02, room 214 |
| Window spit as the entry point | A propped side door (the slip is never paid off as the entry) |
| "Saw the portrait when we passed the hearse"; only child, no uncle | "Cousin driving in"; disproved by the encoder log |
| Five-emperor coin; the 120 km/h cliff; blue-black wrist mark | None: no charm, no vehicle set piece, no body timer |
| Mentor, funeral shop, failed godson rite, ghost mother, one-handed son | None: the Short ends on the count |

---

## 6. Red flags (stop and re-plan)

- You can name the source story from your logline.
- Your twist list read top to bottom matches a source §5 for three rows, even with different nouns.
- Your clue is a source clue with the unit changed: floors → decks, km → miles, or "exactly six posters, so I'm the seventh" → "exactly eleven hearts, so I'm the twelfth". Example A keeps a count, but its math is a timetable (one heart every 90 s, in house order), and the same timetable is what exposes the ally.
- The ending has the source's last image or its last motive.
- You needed a source name or a source line to explain your premise to a teammate.
- `plot_similarity.py` prints a chain of 2 against one source. That isn't a FAIL, but look at which events matched and move one.
