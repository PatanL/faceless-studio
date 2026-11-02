# Lane principles: story and what-if (outliers vs ordinary, same channel)

Built 2026-11-02 from metadata, auto-captions and 240p frame analysis pulled on the Spark (CPU, nice). Internal research only: nothing here (scripts, characters, titles) is for reuse.

**Method.** For each channel I took every Short in one style, ranked by views, and compared the top tier with the rest of the same channel. Each video was coded on: first line and first 3 s on screen, premise type, stakes, use of "you", length, words per minute, shot changes per second, where the payoff lands, whether the ending loops, and title pattern. A feature counts as a **principle** only when it splits the tiers clearly (shown as counts) and holds in more than one place where possible. Features that every tier shares are reported as **floor** (needed, but they don't separate hits from the rest).

- **Shot changes/s** come from `dgx-spark:~/studio/refs/lanes_tools/cuts.py`. It counts hard cuts *and* the 0.2-0.4 s whip/blur transitions these channels use. ffmpeg's scene filter finds only 2 changes in Rick's 30M video, against about 39 by eye.
- **Transcripts**: YouTube auto-captions (en-orig), deduplicated with `corpus/whatif/vtt.py`. TikTok: post captions plus faster-whisper small (CPU). Those accounts are mostly music with on-screen text.
- **Raw data** (info.json, VTT, cut lists, 6-frame strips at 0/1/2/3 s and the last 2 s): `dgx-spark:~/studio/refs/lanes/{ricks,zackd,tt}/`.
- **Confidence** labels: **high** = clean split and a second channel agrees; **medium** = clean split in one channel (n ≈ 8 vs 8-16); **low** = suggestive, small n or confounded.

---

## Lane 1: Story (RicksClips3000)

**Sample.** The channel switched format in early October. Before that it posted 122 comedy clips ("Oh Nah 💀"); the 24 newest Shorts (2026-10-07 to 11-01) are the stick-figure story style. Only those 24 are compared, so channel, look, voice and age are held constant. That style's median is **7.1M**, against 497K across the latest 60 including the old clips. Tiers: **top 8** (8.7-30.7M), **middle 8** (5.9-8.4M), **bottom 8** (0.10-4.6M).

**Age caveat.** Railroads (1 day old) and Storm Oil (3 days) are still climbing and are top-tier anyway. Mirror (4 days) and Button (5 days) may still rise a little, but Storm Oil passed 10M in 3 days.

| # | Title | Views | s | Changes/s | you/100w | Setting | Payload | Mechanism physical? | Stakes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | The Ancient Jar That Warned an Empire | 30.7M | 65 | 0.60 | 0.8 | ancient China | real (seismoscope) | yes, pendulum | empire |
| 2 | The Job Nobody Wants in Japan | 16.0M | 61 | 0.77 | 8.8 | Japan | real ("expulsion rooms") | no | your career |
| 3 | The Window That Breaks Japan's Gambling Law | 13.4M | 45 | 0.47 | 4.3 | Japan | real (pachinko prize exchange) | no | law |
| 4 | Your Brain's Secret Idea Zone | 13.3M | 39 | 0.33 | 9.7 | Edison | real (hypnagogia) | yes, steel balls | you |
| 5 | What the Grave Bell Really Meant | 10.9M | 60 | 0.48 | 1.8 | 1800s | real (safety coffin) + twist | yes, bell | buried alive |
| 6 | Why Sailors Carried Storm Oil | 10.8M | 65 | 0.66 | 1.2 | age of sail | real (oil calms waves) | yes | ship |
| 7 | Why Perfect Railroads Don't Work | 9.0M | 65 | 0.58 | 1.7 | 1800s rail | real (expansion gaps) | yes | train |
| 8 | Levels of Pirate Cannonballs | 8.7M | 64 | 0.55 | 0.9 | 1700s navy | real (shot types) | yes | fleets |
| 9 | An Unstoppable Spear vs an Unbreakable Shield | 8.4M | 45 | 0.58 | 0.6 | ancient | parable | no | war |
| 10 | Why Humans Can't Pick Random Numbers | 8.0M | 47 | 0.62 | 1.8 | modern | real (Benford) | no | fraud |
| 11 | The Burglar Who Only Moved Furniture | 7.7M | 58 | 0.72 | 0.8 | modern | fiction | no | house |
| 12 | Why the Second Draw Always Wins | 7.4M | 56 | 0.86 | 9.5 | Old West | real-ish (reaction time) | yes, reflex | duel |
| 13 | What If Humans Invented Teleportation? | 6.8M | 54 | 0.56 | 7.4 | future | hypothetical | no | billions |
| 14 | Why Cashiers Keep Winning The Lottery | 6.5M | 58 | 0.53 | 0.5 | modern | real (lottery stings) | no | arrest |
| 15 | The Scientist's Insane Time Test | 6.0M | 40 | 0.65 | 4.9 | modern | real (fall study) | no | fear |
| 16 | He Could Spot Winning Tickets Just by Looking | 5.9M | 63 | 0.48 | 0.0 | modern | real (scratch-card flaw) | no | money |
| 17 | How a Mirror Rigged a Horse Race | 4.6M | 64 | 0.64 | 0.4 | old racetrack | real-ish (wire delay) | yes, light | money |
| 18 | Would You Upload Your Brain? | 3.6M | 57 | 0.81 | 5.6 | modern/future | speculative | no | you |
| 19 | The Town Built Around a Button | 3.1M | 66 | 0.29 | 0.0 | fantasy | fiction | no | town |
| 20 | This Knight Found the Ultimate Loophole | 1.6M | 41 | 0.59 | 1.2 | medieval | legend | no | money |
| 21 | This Tree Hates You | 1.0M | 68 | 0.40 | 7.2 | modern | real (manchineel) | yes, sap | you |
| 22 | Every Memory Has a Price | 0.43M | 78 | 0.50 | 1.3 | fantasy | fiction | no | brother |
| 23 | How Painkillers Actually Work | 0.30M | 35 | 0.83 | 7.3 | modern | real | no | headache |
| 24 | The Science Behind Slot Machines | 0.10M | 31 | 0.58 | 5.3 | modern | real | no | money |

### Story principles

**S1. A real mechanism, set in a specific past or far-off world.** (confidence: medium-high, the strongest split found)
- Setting and truth combined: **top 8/8** are true (or true-rooted) *and* set in a named era or foreign place (ancient China, Japan, the age of sail, 1800s graves and railways, 1700s navies, Edison).
- Middle: **1/8** (the Old West draw). Bottom: **1/8** (the mirror race).
- Neither half works alone:
  - Period setting without a real payload (the spear parable, the knight legend) sits mid or bottom.
  - Real facts in a modern everyday setting (lottery cashiers, scratch cards, painkillers, slot machines) sit mid or bottom.
- Pure fiction appears in **0/8** of the top tier (burglar and button: 7.7M and 3.1M; memory-for-sale: 0.43M).

**S2. Someone does a strange, concrete thing, and the real reason lands at about two-thirds.** (medium)
- A protagonist acting is present in 7/8 top videos. The exception is Cannonballs, which uses a "levels" escalation ladder instead.
- In the bottom 8, four have no protagonist acting: Painkillers, Slots, Tree and Upload Brain are *you*-explainers or lists. Three have no real reveal at all (Brain, Button, Tree).
- The "You see, ..." reveal sits at a median of 66-70% of runtime in every tier. **Having** a reveal is the split; *where* it falls is not.

**S3. A mechanism you can watch work on screen.** (medium)
- Physical cause and effect is shown in the top tier 6/8 times: pendulum and dragon jaws, oil flattening a wave, rails buckling in the heat, steel balls crashing, a bell string, red-hot shot.
- Middle: 1/8. Bottom: 2/8.
- Social and legal mechanisms (the two Japan videos) also reach the top, but only when they are set in a foreign system (see S1).

**S4. Stakes bigger than one person.** (low-medium)
- An empire, ship, train or fleet is on the line in **4/8** top videos, against 2/8 middle and 1/8 bottom (Button's "town" stays abstract).
- Money-only stakes: top **0/8**, middle 2/8, bottom 3/8.

**S5. The title names the object and its world, and hides the mechanism.** (medium)
- Winning patterns: "The Ancient Jar That Warned an Empire", "The Window That Breaks Japan's Gambling Law", "Why Sailors Carried Storm Oil", "What the Grave Bell Really Meant".
- A setting word appears in the title in 6/8 top, 0/8 middle and 1/8 bottom.
- Literal "How X Works / The Science Behind X / This X ..." titles: **0/16** at or above the median, **4/8** in the bottom tier.
- "How a Mirror Rigged a Horse Race" gives away both the tool and the outcome.
- Agrees with Zack D.'s own data (CHANNEL.md): "Why X" 1.12× and "The X" 1.22×, against literal "How X Works" 0.84×.

**S6. Ridicule, then vindication.** (low)
- The court, the captain or the boss mocks the odd act, and the catastrophe proves them wrong: 3/8 top (Jar, Storm Oil, Railroads), 1-2/8 middle, 1/8 bottom (Mirror).
- It gives the payoff an emotional charge, but the sample is small.

**S7. Floor, not levers (identical across tiers).** (high)

| Feature | Top | Middle | Bottom | Spearman vs views |
|---|---|---|---|---|
| Duration (median s) | 62.5 | 55 | 60.5 | +0.07 |
| Words per minute | 220 | 220 | 228 | −0.30 |
| Shot changes/s | 0.57 | 0.60 | 0.59 | −0.04 |
| "you" per 100 words | 1.75 | 1.3 | 3.3 | +0.04 |
| Like rate | 2.5% | 2.7% | 2.7% | 0.00 |

- **Hook**: 23/24 open at 0.0 s on a declarative, concrete line (an odd act, a paradox fact, or "If you X, Y"), and those forms are spread across all tiers (odd act: 4/4/3). The only question hook ("How do painkillers know where the pain is?") is #23.
- **First 3 s on screen**: every video shows a character in a full set plus one-word captions from frame 0. There is no title card in any tier.
- **Second person** is not a lever here. It is *heaviest* in the bottom tier (*you*-explainers), unlike the explainer lane. It worked only as a POV for walking through a real foreign system (the two Japan videos).
- **Length**: the only signal is that the two shortest (31 s and 35 s) are the two lowest. Stay at 55-65 s.
- **Loops**: 0/24 loop the last line into the first. Videos end on the payoff image (rubble, wave, buckled train) within the last 2-3 s.
- **Likes**: like rate doesn't track views. The emotional fiction (Memory) has the highest like rate (4.2%) and nearly the lowest views. As at Zack D., emotion earns likes and mechanism earns views.

**S-env. The story happens in a place a camera can travel through.** (owner, 2026-11-02; checked against the catalog the same day; confidence: medium)
- Owner's observation: RicksClips picks topics where a 3D environment makes sense, such as a town, bridge, ship, prison, mine or market. The set is part of the mechanism, and the camera moving through it is what makes the 3D look worth having.
- **Check.** I went through the titles and the frame strips (0, 1, 2, 3 s and the last 2 s; `dgx-spark:~/studio/refs/lanes/ricks/strips/`) of all 24 story-style Shorts. Each was coded "travelable" when the story happens in a physical place the camera moves through or across (a street, ship and sea, canyon railway, palace and city, cemetery and village, harbour, racetrack, market), and "not" when it stays at one desk, counter, machine, room or abstract space.
  - **Top 8: 7/8 travelable.** Jar (palace throne room, then the city in the quake), Japan job (office floors and corridors; the weakest yes), pachinko window (neon street, alley, parlour, exchange window), Storm Oil (galley, deck, open sea, the wave), Grave Bell (cemetery, village), Railroads (canyon line, bridge), Cannonballs (deck, harbour fort, sea). The one exception is Brain Idea Zone (one dark room with a chair).
  - **Middle 8: 4/8.** Yes: Spear and Shield (a kingdom fair and fields), Burglar (a house, outside and in), Second Draw (a Western street), Time Test (a fairground tower). No: Random Numbers (an office desk), Teleportation (a booth and an abstract hall), Cashiers (a shop counter), Winning Tickets (a desk and a store).
  - **Bottom 8: 3/8.** Yes: Mirror (racetrack, betting hall), Button (a town square), Knight (a village market and road). No: Upload Brain (a lab), Tree (one tree on a beach), Memory (a shop counter), Painkillers (a kitchen and the body), Slots (one machine).
  - **Outliers vs the rest:** 7/8 of the top tier against 7/16 of the other 16. The median view count is 8.5M for the 14 travelable videos and 6.2M for the 10 that are not. Of the 10 non-travelable videos, only one reached the top tier.
- **The place is part of the mechanism in the hits.** The sea is what the oil calms, the canyon heat is what buckles the rails, the city is what the quake hits, and the cemetery is where the bell rings. In the lower tiers a travelable place appears without a real mechanism: a parable fair, a legend market, a fictional town square. So the rule is necessary but not enough on its own. Combined with S1 (real and period-set), it covers 7/8 of the top tier and 1/16 of the rest (Mirror).
- **Ordinary uploads.** The channel's 122 older Shorts are comedy clips in another format, so they are not a fair comparison and are left out. Every comparison above is within the 24 story-style Shorts (same look, voice and age).
- **Caveats.** n = 24, and the rule is confounded with S1, because period settings tend to come with big places. Confidence is medium.
- Chess Turk (v6) was a weak fit: one hall and a cabinet, so the judges saw too little change of setting (panel principle 3).
- **Use.** Screen every story premise with this rule before scripting. The premise should need two to four connected places (for example a town, then the river, the bridge and the far bank), and the mechanism should be visible in the place itself.

### Topic features beyond S1 and S-env (all 24 scored, 2026-11-02)

**Method.** I coded the same 24 story-style Shorts (tiers as above) on topic features only, from the titles, info.json and the deduplicated en-orig captions (`dgx-spark:~/studio/refs/lanes/ricks/{meta,subs}`). One coder (me), no second rater. *Surprise* is a judgement: 3 = the mechanism contradicts a common intuition and can't be guessed from the title or the first 10 s; 2 = interesting but guessable; 1 = no real mechanism, or an obvious one. *Kind* is the primary mechanism, one per video. p-values are one-sided exact tests (top 8 vs the other 16, or bottom 8 vs the other 16), uncorrected; I tested about ten features, so only p < 0.005 would survive a Bonferroni correction.

| # | Short | Era | Region | Mechanism kind | Stakes | Surprise | Title: concrete object, mechanism hidden? | Title form |
|---|---|---|---|---|---|---|---|---|
| 1 | Jar | ancient | East Asia | engineering | empire | 3 | yes | The [object] That ... |
| 2 | Japan job | modern | East Asia | law / institution | one person | 2 | yes | The [object] ... |
| 3 | Pachinko window | modern | East Asia | law / institution | one person | 3 | yes | The [object] That ... |
| 4 | Brain idea zone | c. 1900 (Edison) | US | mind / body | you | 2 | no (abstract "zone") | Your ... |
| 5 | Grave bell | 1800s | West | deception (con) | one person | 2 | yes | What the X Really Meant |
| 6 | Storm oil | age of sail | West / sea | physics | ship | 3 | yes | Why ... |
| 7 | Railroads | 1800s | West (US) | physics | train | 2 | yes | Why ... |
| 8 | Cannonballs | 1700s | West / sea | engineering | fleet | 2 | yes | Levels of ... |
| 9 | Spear vs shield | ancient (parable) | unplaced | deception (bluff) | two kingdoms | 2 | yes | X vs Y |
| 10 | Random numbers | modern | US | statistics | one person | 3 | no (no object) | Why ... |
| 11 | Burglar | modern | unplaced | deception (con) | family | 2 | yes | The [role] Who ... |
| 12 | Second draw | Old West | US | mind / body | one person | 2 | no (an act) | Why ... |
| 13 | Teleportation | future | unplaced | speculative | billions | 2 | no | What If ...? |
| 14 | Cashiers | modern | US | deception (sting) | one person | 2 | yes | Why ... |
| 15 | Time test | modern | US | mind / body | one person | 2 | no ("test") | The Scientist's ... |
| 16 | Winning tickets | modern | N. America | statistics | one person | 3 | yes | He Could ... |
| 17 | Mirror race | c. 1900 | US | deception (con) | one person | 2 | no (tool and outcome given) | How ... |
| 18 | Upload brain | near future | unplaced | speculative | you | 1 | no | Would You ...? |
| 19 | Button town | fantasy | unplaced | fiction, no mechanism | town | 1 | yes | The [place] Built Around ... |
| 20 | Knight loophole | medieval | Europe | deception (con) | one person | 2 | no ("loophole" given) | This X ... |
| 21 | Tree | modern | beach | mind / body (toxin) | you | 1 | yes | This X ... |
| 22 | Memory | fantasy | unplaced | fiction, no mechanism | brother | 1 | no | abstract statement |
| 23 | Painkillers | modern | the body | mind / body | you | 1 | no | How X Actually Works |
| 24 | Slots | modern | casino | statistics | you | 2 | no | The Science Behind X |

**Counts per tier (top / middle / bottom, 8 each)**

| Feature | Top | Middle | Bottom | Read |
|---|---|---|---|---|
| Era: a named past (before about 1920) | 6 | 2 | 2 | overlaps S1 |
| Region: East Asia | **3** | 0 | 0 | p = 0.03 (top vs rest) |
| Region: past West (Europe, sea, old America) | 5 | 1 | 2 | overlaps S1 |
| Region: modern US or unplaced real | 0 | 5 | 4 | |
| Kind: physics / engineering | **4** | 0 | 0 | p = 0.007, the cleanest new split |
| Kind: law / institution (a real national system) | 2 | 0 | 0 | both are Japan |
| Kind: deception / con / sting | 1 | 3 | 2 | not a split (p ≈ 0.3); the commonest kind in the 16 ordinary |
| Kind: mind / body | 1 | 2 | 2 | not a split |
| Kind: statistics | 0 | 2 | 1 | never top |
| Kind: speculative or fiction, no real mechanism | 0 | 1 | 3 | never top |
| Stakes: nation, empire or world | 1 | 2 | 0 | **not a lever on its own** |
| Stakes: group (ship, train, fleet, family, town) | 3 | 1 | 1 | |
| Stakes: one person or "you" | 4 | 5 | 7 | |
| Surprise 3 | 3 | 2 | 0 | weak |
| Surprise 1 | 0 | 0 | **5** | p = 0.001 (bottom vs rest), the only split that survives correction |
| Title names a concrete object, role or place and hides the mechanism | **7** | 4 | 2 | p = 0.03 |
| Title form "Why ..." | 2 | 3 | 0 | all five ≥ 6.5M |
| Title form "The [object] that/who ..." | 3 | 1 | 1 | |
| Title form "How ...", "This X ...", "The Science Behind ...", or a question | 0 | 1 | 6 | |
| Title states a tension or contradiction ("Perfect Railroads Don't Work", "Breaks Japan's Gambling Law", "Second Draw Always Wins") | 3 | 4 | 0 | p = 0.03 (top + middle vs bottom) |
| Title length (median words) | 5.5 | 6 | 5 | no split |
| A famous person named in the script | 1 (Edison) | 0 | 0 | the Jar's inventor (Zhang Heng) is never named |
| One documented event retold faithfully (no invented plot) | 0 | 2 | 0 | |
| Topic already done by Zack D. Films | 2 (Jar 10M, Grave bell 108M) | 1 (Teleportation 34M) | 0 | prior coverage didn't block a hit |

**Findings**

- **T1. The mechanism kind that wins is physics or engineering.** (medium-low) 4/8 top, 0/16 others. It is the S3 split seen one level deeper: the four are the ones whose *explanation* is a force or a machine (pendulum, oil film, thermal expansion, shot types), not just a prop on screen. The other top kind is a real national legal system (2/8, both Japan). Confounded with S1, because period settings bring physical mechanisms.
- **T2. Cons and stings are the ordinary story's default, not the hit's.** (low) Deception is the commonest kind among the 16 below the top (5/16) and appears once in the top 8 (Grave bell, which also carries a real device). Chess Turk, our first story, is a con; Vasa is engineering. Prefer topics where the trick is played by *nature or physics*, not by a swindler.
- **T3. East Asia has a perfect record so far.** (low) 3/3 East Asian topics are top tier (Jar 30.7M, Japan job 16.0M, Pachinko 13.4M), and no video set there is below the top. n = 3, so treat it as a tiebreaker only.
- **T4. Bigger stakes alone don't separate.** (low) Nation, empire or world stakes: 1/2/0. The two middle-tier ones are a parable (Spear) and a hypothetical (Teleportation). Big stakes help only on top of a real mechanism (S1). This refines S4: a group of people at risk (ship, train, fleet) is the common top pattern, not a nation.
- **T5. Low surprise is what sinks a story; high surprise doesn't guarantee a hit.** (medium) Surprise 1 is 0/16 in the top two tiers and 5/8 in the bottom (p = 0.001). Surprise 3 is 3/2/0, a weak gradient. So "a real mechanism you couldn't have guessed" is a floor to clear, and above it topic and setting decide.
- **T6. The title names the object and its world, hides the how, and often states a tension.** (medium; adds counts to S5)
  - Concrete object with the mechanism hidden: 7/4/2.
  - Tension or contradiction stated in the title: 3/4/0.
  - Title forms:
    - "Why [group] [did an odd thing]" and "The [object] That [did a big thing]" are 10 of the 16 top and middle titles, with only 1 in the bottom.
    - "How ...", "This X ...", "The Science Behind ..." and question titles are 6/8 of the bottom and 0/8 of the top.
    - Length doesn't matter (median 5-6 words in every tier).
- **T7. No famous names needed, and the plot can be composite.** (medium) No top video retells one documented event faithfully. Each wraps a true mechanism in an invented or composite plot: an unnamed inventor and a palace collapse for the Jar, a fictional young engineer for Railroads, a "you" POV for Japan. Only 1/24 names a famous person. Our rule: dialogue and minor characters may be invented, but every number, date and mechanism stated as fact must be sourced (STORY_TOPIC_QUEUE.md).
- **T8. Prior coverage isn't a veto.** (low) The Jar and Grave Bell retell topics Zack D. Films had already done (10M and 108M), and both made the top 8. We still prefer uncovered topics, but a strong topic done by someone else in a different style is fair game.
- **Check of the 10 premises above** (Zack D.'s full Shorts list, 4,122 titles, 2026-11-02):
  - Two of the ten are covered after all, because the earlier check only looked at Zack D.'s last 400 titles: the floor built to squeak ("Nightingale Floors Were Designed To Stop Ninjas", 30M) and the Broughton bridge ("Why Do Soldiers Break Step On Bridges?", 9.4M).
  - The *Vasa* is in production.
  - The vetted queue is research/library/STORY_TOPIC_QUEUE.md.
- **Screen for new topics** (in order): S1 real + period/foreign → S-env four places → T1 physics/engineering or a real foreign institution, not a con → T5 surprise ≥ 2 → T6 a title with a concrete object and a hidden mechanism → S6 ridicule if the history allows → T3 East Asia as a tiebreaker.

### 10 story premises that fit S1-S6 (not in Rick's 146 titles, Zack D.'s last 400, or the TikTok lists)

1. **The floor built to squeak** (Nijō Castle, Japan, 1600s). A shogun pays carpenters to make the floor chirp under every step. Courtiers mock the "broken" floor until an assassin crosses it at night. Mechanism: nails rubbing in clamps.
2. **The engineer who refused to build a dam** (Dujiangyan, China, 256 BC). Li Bing splits the flooding Min River with a "fish-mouth" levee and bamboo baskets of stones, and is ridiculed for not building a wall. The flood comes and his plain survives; the system still waters Chengdu today.
3. **They flooded their own farms** (Leiden, 1574). Starving and besieged, the Dutch break their own dikes. The water creeps in for weeks, the Spanish laugh at the puddles, then a storm-driven tide floats rescue ships over the fields to the walls.
4. **The king who drank poison every morning** (Mithridates VI). He builds tolerance with tiny daily doses while his court thinks he's mad. Payoff twist: when Rome finally traps him, his own poison won't kill him.
5. **The shields that heard the enemy digging** (ancient sieges, Aeneas Tacticus). A smith lays bronze shields on the ground around the city and watches for one to ring. Diggers' blows vibrate them, and the defenders dig a counter-tunnel straight into the enemy's.
6. **One more gun deck** (the *Vasa*, Stockholm, 1628). The king demands a taller warship and the shipbuilder's warning is ignored. A stability test with 30 sailors running side to side is hushed up, and the ship sinks 1,300 m into her maiden voyage in front of the whole city. Mechanism: centre of gravity.
7. **The clock that stopped shipwrecks** (John Harrison, 1700s). After 1,400 sailors die off Scilly because no one knows their longitude, a carpenter claims a *clock* can fix it, and the astronomers laugh. Payoff: time difference equals position, with the watch on the voyage proving it.
8. **She scratched smallpox into her son's arm** (Lady Mary Wortley Montagu, Istanbul, 1718). She copies Ottoman village women, London doctors call it murder, and the payoff is a trial on condemned prisoners. Bodily rather than physical, so it tests S3.
9. **Vinegar on a mountain** (Hannibal crossing the Alps, as told by Livy). A boulder blocks 40,000 men and the elephants. They light a fire on it and pour sour wine, the soldiers laugh, and the rock cracks. Mechanism: thermal shock; say on screen that the vinegar part is disputed.
10. **The bridge that marched itself apart** (Broughton Suspension Bridge, 1831). Soldiers march in step and the bridge collapses, so armies still "break step" on bridges. Mechanism: resonance, shown with a swing.

---

## Lane 2: What-if (Zack D. Films + What if? @man_ia_c + meanwhileanimations + polystoriesdaily)

### Zack D. Films: the 16 hypothetical Shorts (top 8 vs ordinary 8)

All 16 are 13-81 days old (mature) and share the house look and voice. Views are from today's pull. Zack's rolling-median outlier scores for these run 0.44-2.0×, so this compares a ~2× tier with a ~0.6× tier.

| # | Title | Views | s | wpm | you/100w | Changes/s | Impossible change on screen by 3 s? | Ending |
|---|---|---|---|---|---|---|---|---|
| 1 | Does Running Like Naruto Make You Faster? | 28.3M | 30 | 166 | 13.3 | 0.67 | yes (the run) | consequence (faceplant) |
| 2 | What If Your Hair Had Nerves | 20.5M | 26 | 178 | 2.6 | 0.92 | yes (writhing hair) | consequence (haircut = cutting fingers) |
| 3 | Could You Move Mount Everest To America? | 20.1M | 59 | 151 | 0.0 | 0.66 | yes (trench cut) | done (Everest in Alaska) |
| 4 | What If You Could Float Like A Duck? | 17.3M | 32 | 161 | 11.6 | 0.50 | yes (torso balloons) | done |
| 5 | What If You Hit Absolute Zero? | 17.2M | 34 | 173 | 13.3 | 0.62 | yes (atoms freeze) | consequence (shatter, goop) |
| 6 | What If The Wheel Was Never Invented? | 14.7M | 45 | 159 | 2.5 | 0.89 | yes (wheel-less bus) | consequence (air tubes) |
| 7 | Beating Earth At Rock Paper Scissors | 14.0M | 30 | 172 | 3.5 | 1.03 | yes (8B players) | surprise number (33) |
| 8 | Inheriting Ten Million Dollars In Pennies | 11.5M | 45 | 169 | 10.2 | 0.62 | no (grandpa scene) | surprise number ($1.6M fee) |
| 9 | What If One Vinyl Played Every Song? | 9.4M | 47 | 153 | 0.8 | 0.55 | no (normal record) | big number |
| 10 | Could Ticks Make An Infinite Chain | 8.1M | 27 | 176 | 2.5 | 0.41 | no (one normal tick) | **no, chain breaks** |
| 11 | What If Bullets Were Made Of Ice? | 8.0M | 41 | 174 | 1.7 | 0.68 | no (normal bullet) | **no, you'd still be caught** |
| 12 | Building The Death Star With Earth's Metal | 7.3M | 34 | 176 | 5.0 | 0.38 | no (junkyard robot) | **only a slice**, then doom |
| 13 | Can You Beat A Baby In A Staring Contest? | 7.3M | 25 | 187 | 6.4 | 0.64 | no (a face) | mild |
| 14 | What If Your Nose Hole Was Bigger? | 6.1M | 30 | 176 | 12.5 | 0.90 | yes (nose removed) | consequence |
| 15 | What If A Bird Loved A Fish? | 3.6M | 39 | 178 | 1.7 | 0.38 | no | **moral, it can't work** |
| 16 | Can You Get Rich Donating Plasma | 3.0M | 43 | 176 | 10.3 | 0.88 | no (normal donation) | joke |

### What if? (@man_ia_c, TikTok, caption-only 80 s sims, 23 posts, 2026-10-04 to 11-01)

- **Top 8:**
  - electrons for 5 s: 18.3M
  - oxygen for 5 s: 13.6M
  - neutrons: 5.1M
  - pop star 100× taller: 5.0M
  - π = 3: 4.0M
  - iron: 2.7M
  - pop star 10 billion×: 2.1M
  - every atom +1 proton: 1.2M
- **Other 15** (0.16-0.76M):
  - TikTok vanishes
  - Earth falls into a black hole
  - gravity off 60 s
  - human column
  - cruise-ship tsunami
  - gravity off
  - meteor at Burning Man
  - Earth leaves the universe
  - hydrogen
  - escalating earthquakes
  - wave hits New York
  - AI at 3:14 AM
  - Earth stops spinning
  - plane crash
  - every atom −1 proton
- **Like rate:** median 7.2% in the top 8, against 3.0% in the other 15.
- **Shot changes/s:** 0.30 against 0.38. All posts are about 80 s.

### meanwhileanimations (TikTok, 13 posts, 2026-10-04 to 10-31)

| Premise family | Posts and views |
|---|---|
| A whole group of people vanishes or swaps (gender) | All women die: **35.4M**; every man disappears: **20.0M**; men get pregnant: 2.3M; boys grow up without men: 0.92M; women become stronger: 0.40M |
| Policy or society | Free healthcare: 1.3M; every smartphone gone: 1.3M; every immigrant gone: 1.1M |
| Disaster at a named place | Vesuvius today: 2.0M; Three Gorges Dam: 1.1M; colder every day: 0.65M; dinosaur asteroid: 0.48M; Hong Kong hypercane: 0.47M |

**Shares/views:** 1.2-1.6% for the two gender hits, against 0.10-0.43% for the disasters.

### polystoriesdaily (TikTok, 8 posts, 1-9 days old)

- Every post is the same template: "What if your X doubled every second/day?", with one blocky character and a live counter.
- Top post: "piss PSI doubled every second" at 1.8M. The others range from 0.02M to 0.81M, but the youngest are 1-2 days old, so **no split can be read yet**.
- One clear fact: shares run 1.4-5.5% of views, 5-10× man_ia_c's 0.1-0.9%. Comedy is the share engine.

### What-if principles

**W1. Change something every viewer carries or uses, not a place they visit.** (high: three channels agree)
- Changes to universal things: an ingredient of all matter, a constant, your own body, half of humanity, the wheel, the whole planet.
- man_ia_c: disasters at a named place are **0/8** of the top tier and **6/15** of the rest. The top 8 are 6 invisible-ingredient changes (electrons, oxygen, neutrons, π, iron, protons) and 2 scale changes.
- meanwhileanimations: disasters at a named place have a 0.65M median. "Every woman/man vanishes" got 35.4M and 20.0M from the same team and look.
- Zack D.: the top tier changes your body or the whole world (Earth's population, Everest, the wheel, every atom in you).
- This confirms PLAYBOOK §10C and extends it to two more channels.

**W2. Show the impossible change within 2-3 s.** (medium, Zack D.; formats that use a countdown get the same effect from the deadline)
- Zack D.: the change is visible by 3 s in **7/8** top videos (hair writhing at 2 s, torso ballooning at 1 s, wheel-less bus at 2 s, trench at 1 s) against **1/8** ordinary.
- The ordinary ones open on a normal object (a record, a tick, a bullet, a baby, a junkyard) and say "you might think..."; they open with that set-up in **3/8**, the top tier in **0/8**.
- man_ia_c doesn't need this: every post holds a calm named place under a title and countdown, with the event at about 8 s. The visible deadline does the job, and this frame is the same in both of its tiers.

**W3. Commit to the premise and pay off with one concrete consequence, not a debunk.** (medium)
- Zack D. endings that say "it wouldn't work": top **1/8** (Naruto, and even that ends on a faceplant gag), against ordinary **4/8** (the tick chain breaks, the ice bullet still gets you caught, only a slice of a Death Star, the bird and fish can't live together).
- Top-tier payoffs are one image or one surprising number:
  - a haircut feels like cutting off fingers
  - you shatter, then melt into goop
  - only 33 games to beat the whole planet
  - Coinstar keeps $1.6M of your pennies
- man_ia_c's top tier works the same way: "Earth comes apart", "each person becomes a 7-megaton bomb", "your floor is at her hip height".

**W4. Put the effect on the viewer's body first.** (medium)
- man_ia_c: 5/8 top captions have an explicit body beat (light passes through your hands; your ears pop; you weigh as much as a 5-year-old; your blood turns grey; your office floor is at hip height), against about 3/15 of the rest.
- Zack D.: "you" per 100 words has a median of 7.0 in the top tier, 3.4 in the ordinary tier. "You/Your" appears in 5/8 top titles and 3/8 ordinary titles.
- **Lane difference:** this is the reverse of the story lane, where "you" doesn't help (S7).

**W5. Each premise family hits once. Sequels decay fast, so change the family, not the variable.** (high: two channels, clear order over time)

| Channel | Order posted | Views |
|---|---|---|
| man_ia_c, element series | electrons → oxygen (days 1-2) → neutrons → iron → +proton → hydrogen → −proton | 18.3M → 13.6M → 5.1M → 2.7M → 1.2M → 0.43M → 0.16M |
| man_ia_c, pop-star series | 100× → 10 billion× | 5.0M → 2.1M |
| meanwhileanimations, gender series | women → men → pregnancy → boys → strength | 35.4M → 20.0M → 2.3M → 0.92M → 0.40M |

- **Confound:** man_ia_c's non-series posts also slid later in the month, so part of the drop is channel-wide.
- For us: never post two Shorts from the same premise family within days of each other. This also applies to our own `whatif-grow-1cm` (scale-ladder family).

**W6. Premises about identity or society are the share and comment engine. Big upside, real risk.** (low-medium, n=13)
- meanwhileanimations' gender videos: like rates 14-20% and shares 1.2-1.6%, against 3-6% and 0.1-0.4% for its disasters.
- Divisive versions (gender, immigration) are a brand risk for us.
- The transferable part is **"what if a group that everyone has in their life vanished at a countdown"**, which can be non-divisive (pets, adults, strangers).

**W7. Floor, not levers.** (high)
- **Pacing:**
  - Zack D. top vs ordinary: 0.67 vs 0.60 changes/s, 167 vs 176 wpm (the top is slightly *slower*), 33 vs 36.5 s.
  - man_ia_c: 0.30 vs 0.38 changes/s, all about 80 s.
  - Neither split is meaningful.
- **Loops:** none of the 16 Zack D. videos loops its last line into the first (each ends on its payoff line). man_ia_c and meanwhileanimations end every post (23/23 and 13/13) on a black end card with a comment question ("Which one next? 👇"), so it doesn't separate either.
- **First 3 s:** identical across tiers within each TikTok channel (title over a calm named place, a countdown for man_ia_c and meanwhileanimations, a live counter for polystoriesdaily).
- **Titles:** Zack D.'s house pattern is a "What If / Could You / Does X Make You" question plus one emoji. man_ia_c and meanwhileanimations always use "What if [X] for N seconds?" or "What if every [group] disappeared?". The *noun* separates the tiers (W1), not the template.

### 10 what-if premises that fit W1-W6 (not in Zack D.'s last 400 titles or the three TikTok lists; each a new family)

| # | Premise | Universal (W1) | On screen by 2 s (W2) | Payoff (W3) | Body first (W4) |
|---|---|---|---|---|---|
| 1 | **What if friction disappeared for 5 seconds?** | everything | your shoelaces untie and you slide off your chair | knots, nails and screws let go; when friction returns, everything sliding stops in one jolt | you can't stand up |
| 2 | **What if sound moved at walking speed?** | a constant | your mouth moves, the words arrive 3 s later | thunder arrives an hour after the lightning; a concert has to be heard from the back first | you hear yourself after you finish talking |
| 3 | **What if ice sank?** | water's one strange rule, flipped for one winter | your ice cube drops to the bottom of your glass | lakes freeze from the bottom up and never fully thaw: the real reason fish survive winter | your drink |
| 4 | **What if everyone on Earth fell asleep for 60 seconds?** | everyone at once, with a countdown | everyone drops mid-step | planes on autopilot are fine, ~1M cars aren't, and the one person awake is you | |
| 5 | **What if every cat on Earth vanished at midnight?** | a non-divisive group-vanish (W6), with a countdown | | the rat population curve, grain stores, the internet goes quiet | someone's lap is empty |
| 6 | **What if every adult vanished for 24 hours?** | the kids-run-the-world sim | | hour by hour: who drives, who cooks, power-plant timers; the return twist is what the adults come back to | |
| 7 | **What if you had a second thumb on each hand?** | your body (Zack-style commit) | the thumb grows at 1 s | grip, typing, and the one thing it makes worse | your hand |
| 8 | **What if your heartbeat were loud enough for everyone to hear?** | your body plus a social payoff | | lying, first dates, exams, horror films | |
| 9 | **What if air were twice as thick?** | an invisible ingredient | | voices get deeper, a cardboard wing can lift you, rain falls slower, insects grow bigger over generations | your voice |
| 10 | **What if your phone charged from your own body heat and calories?** | a universal object plus body cost | | one full charge equals about 10 Wh of extra food (do the math on screen), so doom-scrolling burns a snack | |

---

## How confident to be, and what to test first

- **Strongest, and agreed across lanes:**
  - Topic choice (S1 and W1) separates hits far more than any craft metric.
  - Pacing, length and hook *form* are the floor in every channel: there is a house setting, and hits and misses share it.
- **Lane-specific and opposite:** "you" helps what-ifs (W4) but not stories (S7). Stories want a third-person protagonist in a far-off real world; what-ifs want the change on your body, here.
- **Weakest:** S4, S6 and W6 rest on 3-4 videos each.
- **First experiments** (log in docs/EXPERIMENTS.md):
  - Story: the floor built to squeak (S1+S2+S3+S5+S6) vs a modern everyday story with the same craft (expect at least 2× gap in average % viewed).
  - What-if: friction for 5 s (W1+W2+W4) vs a disaster-at-a-named-place sim (expect a higher viewed-vs-swiped rate for friction).
