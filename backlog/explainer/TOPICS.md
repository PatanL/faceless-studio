# Explainer backlog — topic selection

Niche: ocean/animal "you vs X" 2D explainer in the Depth Theory style (scale comparisons, stick-figure YOU, stat callouts, "your options", escalating danger).
Mix: **6 Shorts (60–90 s, 9:16)** + **4 long-form (8–10 min, 16:9)**.
Selected 2026-11-01 ~09:00 UTC. View counts come from yt-dlp metadata read today.

## Evidence used

- `research/R1/topics.json`, `research/R1/raw/topics/*.json`, `research/R1/raw/peers_summary.json` (Depth Theory teardown, 10 peer channels with medians).
- `research/library/candidates-explainer.json` (outlier scores vs channel median).
- `research/R3/report.md` (finding: Shorts cut down from long-form flop; vertical-native Shorts are their own format).
- New checks for this file (Spark, `~/.local/bin/yt-dlp --flat-playlist`): 24 `ytsearch20:` queries, Zack D. Films Shorts tab (400 most recent, median 10M), Shorts tabs of Mr. Science, Spinosnack and other peers. Raw JSONL is in `backlog/explainer/evidence/` (and on the Spark in `~/studio/refs/topics_explainer/`).
- `episodes/` does not exist yet, so nothing is duplicated. Depth Theory's own topics (sperm whale, colossal squid, humpback, great-white tournament) are excluded on purpose.

**What the checks say about Shorts.** The long-form peer channels barely post Shorts. Mr. Science's two Shorts got 10K and 7.4K views, against a 1.25M long-form median. The animated Shorts that win are vertical-native and built on a single fact, like Zack D. Films ("How Cookiecutter Sharks Bite Whales" 57M, 5.7x a 10M median). Our Shorts should be built as their own one-mechanism stories with a "you" frame. They should not be trimmed from the long-form videos.

## 14 candidates

| # | Slug | Format | Premise (one line) | Key evidence | Code cost | Verdict |
|---|---|---|---|---|---|---|
| 1 | explainer-never-meet-orca | Long | The only animal named "killer" has never killed a person in the wild, and here is what it does to everything else | WILD VERSUS 56M (83x); OctoLab 8.2M (315x); BeyondTheBlue 2.7M (9x) | low | **PICK** |
| 2 | explainer-sinking-every-1000m | Long | You sink from the surface to 11 km; every 1,000 m brings a new creature and a new way the depth kills you | Mr. Science "Creepier the Deeper" 17.2M (12.9x); Insider Tech depth animation 83.6M; Spinosnack 5.5M (33x) | low | **PICK** |
| 3 | explainer-never-meet-leopard-seal | Long | Antarctica's cutest-looking predator, the one that toys with its prey before eating it | Animalogic 3.2M; Casual Geographic 3.0M; Nat Geo face-off 12.3M | low | **PICK** |
| 4 | explainer-every-animal-that-could-swallow-you | Long | Ranked mouth-gauge vs stick-figure YOU: every ocean giant, and which ones could actually fit you | What If "Swallowed by a Whale…4 Stomachs" 16.4M; Meet Arnold 19.7M; Occam 332K (16x on 2.9K subs) | low-med | **PICK** |
| 5 | explainer-never-meet-humboldt-squid | Long | The "red devil": packs of 50 kg squid that flash red and swarm divers at night | Travel Edit 7.1M; KQED 1.7M; DT colossal squid 124K | low | reserve: no recent long-form outlier, and it sits too close to DT's colossal squid |
| 6 | explainer-never-meet-greenland-shark | Long | A 400-year-old shark that moves at 1 km/h but still turns up with polar bears in its stomach | Astrum Earth 3.0M; Real Science 2.0M; BeyondTheBlue 875K | low | reserve: the danger is slow, so it depends on the twist |
| 7 | explainer-never-meet-saltwater-crocodile | Long | The largest reptile alive, swimming out to sea between islands | MrBallen 9.3M; Brave Wilderness 8.3M | low | reserve: an estuary animal, so it stretches the "ocean" brand |
| 8 | explainer-short-cookiecutter-shark | Short | A 50 cm shark that scoops perfect circles out of whales, and once out of a swimmer | Zack D. "How Cookiecutter Sharks Bite Whales" 57M (5.7x); Nat Geo 782K | very low | **PICK** |
| 9 | explainer-short-mantis-shrimp-punch | Short | Scale the mantis shrimp's punch up to your size and it hits like a bullet | Jon Bondy "Mantis Shrimp Destroys Clam" 36.3M; Nick SBF mantis vs pistol 5.5M | very low | **PICK** |
| 10 | explainer-short-box-jellyfish | Short | You can't see it, it has 60 tentacles, and you have about 2 minutes | TED-Ed sting 12.0M; George Kourounis "Stung by a Box Jellyfish" 8.2M; Animal Planet swarm 1.2M | very low | **PICK** |
| 11 | explainer-short-blue-whale-scale | Short | You next to a blue whale: its heart, its tongue, its aorta, and its mouthful | Global Data animal size 18.1M; Duke Jarboe encounter 14.6M; heart size comparison 5.1M | very low | **PICK** |
| 12 | explainer-short-mariana-pressure | Short | What 1,086 bar does to your body, one depth marker at a time | Insider Tech depth animation 83.6M; atomic marvel "Human body vs implosion" 10.3M (151 s); Infographics Show 1.2M | very low | **PICK** |
| 13 | explainer-short-moray-second-jaw | Short | Every moray eel has a second jaw in its throat that shoots forward and drags you in | Zack D. "Moray Eels Have Two Sets Of Jaws" 9.9M (1.0x); Zack D. eels escape a stomach 34M (3.4x); Caters moray attacks diver 638K | very low | **PICK** |
| 14 | explainer-short-pistol-shrimp | Short | A claw snap that makes a bubble almost as hot as the sun's surface | BBC Weird Nature 4.0M; Nat Geo 3.7M; Animalogic 3.7M | very low | reserve: second shrimp next to #9, with lower views |

## Final 10

### Long-form (8–10 min)

1. **explainer-never-meet-orca**: "Why You'd Never Want To Meet An Orca". The hook is the paradox of "killer" yet zero wild human kills. The escalation runs hunting plans, wave-washing, killing great whites for their livers, then your options. — *Evidence:* WILD VERSUS "This Is Why Orcas Are Called Killer Whales" 56M (83x) and OctoLab 8.2M (315x on 82K subs) prove demand. DT-clone uploads with this title got 43 views, so the thumbnail and execution have to carry it.
2. **explainer-sinking-every-1000m**: "What You'd Meet Sinking To The Bottom Of The Ocean". A depth meter runs alongside an "are you still alive" meter. Each 1,000 m adds one creature and one physical threat (light, cold, pressure). — *Evidence:* Mr. Science "Why Deep Sea Creatures Get Creepier the Deeper You Go" 17.2M (12.9x) and Insider Tech "How Deep The Ocean Really Is" 83.6M. This is the highest-ceiling format in the niche, and it reuses the depth-meter component.
3. **explainer-never-meet-leopard-seal**: "Why You'd Never Want To Meet A Leopard Seal". The hook is the cute face hiding a 3 m predator that plays with penguins. It ends on the twist that it brought a photographer penguins to eat. — *Evidence:* Animalogic 3.2M, Casual Geographic "The Predator We Still Can't Figure Out" 3.0M, Nat Geo face-off 12.3M. Proven demand and no strong "you vs" long-form version yet.
4. **explainer-every-animal-that-could-swallow-you**: a ranked "could it swallow you?" ladder. YOU stands next to each mouth with a throat-width bar: whale shark, basking shark, humpback, grouper, sperm whale. — *Evidence:* "swallowed by a whale" videos run 16.4M (What If) and 19.7M (Meet Arnold), and Occam's list got 16x its channel median. Our title, structure and wording must differ from Occam's "Every Animal That Could Swallow You (Only One Actually Can)".

### Shorts (60–90 s, vertical-native)

5. **explainer-short-cookiecutter-shark**: the circle-shaped bite, shown on a whale and then on YOU. — *Evidence:* Zack D. Films "How Cookiecutter Sharks Bite Whales" 57M (5.7x on a 10M median), the biggest ocean Short in the sample.
6. **explainer-short-mantis-shrimp-punch**: the punch scaled to human size, shown as bullet, car and glass callouts. — *Evidence:* Jon Bondy "Mantis Shrimp Destroys Clam" 36.3M (50 s). A single-mechanism Short with a ready-made scale-up stat.
7. **explainer-short-box-jellyfish**: the invisible animal, 60 tentacles, a countdown timer and your options. — *Evidence:* TED-Ed "How does a jellyfish sting?" 12.0M and George Kourounis "Stung by a Box Jellyfish" 8.2M. The "what happens to you" angle is proven, and translucent shapes cost almost nothing to animate.
8. **explainer-short-blue-whale-scale**: YOU against the whale, its heart, its tongue and its mouthful, in one pure scale-comparison Short. — *Evidence:* Global Data "Animal Size Comparison" 18.1M, Duke Jarboe "Blue Whale encounter" 14.6M, heart-size comparison 5.1M. Scale bars are the kit's core device.
9. **explainer-short-mariana-pressure**: what the pressure does to your body at 10 m, 100 m, 1 km and 11 km. — *Evidence:* Insider Tech depth animation 83.6M and atomic marvel "Human Body vs Implosion" 10.3M. It is a separate body-only premise. It is not a cut-down of #2 (R3 found cut-downs flop), so the scripts must not share lines.
10. **explainer-short-moray-second-jaw**: the hidden second jaw (pharyngeal jaws) firing out of the throat, with you as the hand reaching into a reef hole. — *Evidence:* Zack D. Films "Moray Eels Have Two Sets Of Jaws" 9.9M and "Japanese Eels Can Escape A Fish's Stomach" 34M (3.4x). Eel-mechanism Shorts outperform.

## Reserve (next in line)

explainer-never-meet-humboldt-squid, explainer-short-pistol-shrimp, explainer-never-meet-greenland-shark, explainer-never-meet-saltwater-crocodile. Also from R1, but deferred because they are creature-heavy: "How Long Would You Last In Every Prehistoric Ocean?" (Fossil 12M at 112x; BeyondTheBlue 3.3M).

## Notes for script writers

- Follow BRIEF Update 09:00: pick the 2–3 closest corpus scripts in `research/corpus/explainer/`, add a beat alignment table, and pass `scripts/originality_check.py`. Several comparables above are Zack D. Films or Nat Geo clips. Use them only for topic demand, never for wording or structure beyond general devices.
- Shorts hook: state one striking fact about YOU in the first 2 s, show one mechanism, escalate 3–4 beats, and end on a stat callout. Long-form follows DT's skeleton: cold open, size comparison, how it hunts, "your options", escalation, then the twist.
