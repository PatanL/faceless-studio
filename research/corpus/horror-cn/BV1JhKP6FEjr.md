# BV1JhKP6FEjr: "Dad dragged me out of the complex at midnight; the next day every resident was dead"

Internal research only. This file studies the structure of a source story. **Do not translate, retell or remix this story for publication.** Section 6 lists what a transposed story may borrow and what it must not reuse.

## 1. Header

| Field | Value |
|---|---|
| Source | https://www.bilibili.com/video/BV1JhKP6FEjr |
| Chinese title | 深夜老爸突然带我逃离小区，第二天小区住户就全部身亡 |
| Channel | 杰出影视本人 (Bilibili mid 75872737), the "Chen Jie" / 迷雾 studio |
| Uploaded | 2026-07-18 |
| Views | 53,648 plays and 1,660 likes on Bilibili, checked 2026-11-01 |
| Duration | 1,124 s (18:44) on Bilibili; 1,134 s (18:54) on the YouTube mirror |
| Tags | 原创动画, 反转, 惊悚, 恐怖, 烧脑, 细思极恐, 悬疑, 一口气看完 |
| English repost | **Confirmed by the hook.** mraevq TikTok 7664930759395888416: 428K views, 29K likes, 15:18, posted 2026-07-21, 3 days after the Bilibili upload. That is about 8x the source's plays. The gap is short, so both may come from an earlier Douyin post. The English cut is about 3.5 min shorter, which points to faster English TTS and/or trimmed travel beats. |
| Other mirror | YouTube 9fbeNvjDHms, channel 沙雕悬疑动画, 502 views, 18:54. This is a re-upload. |

**How the text was extracted.** Everything ran on the Spark CPU under `~/studio/refs/horror-cn/BV1JhKP6FEjr/`.
- **Truncated source.** Without a login, Bilibili's playurl API returns a single 529.98 s segment of the 1,124 s video, at every quality and with every `fnval`/`try_look` setting. So the Bilibili MP4 there stops at 8:50. The full story was taken from the YouTube mirror: AV1 480p plus Opus audio. The mirror's timestamps line up with Bilibili's to within about 5 s: the danmaku "不会已经不是老爸了吧" sits at 571 s on Bilibili, and the dad-returns beat is at 566 s on the mirror.
- **No subtitles.** The video has no auto-subs.
- **Captions by OCR.** The captions are burned in and match the narration word for word. I sampled one frame every 2 s and ran rapidocr (`ocr.jsonl` → `ocr_parsed.txt`), which recovered 496 caption lines.
- **Gaps filled by whisper.** I ran faster-whisper small (zh, CPU, 4 threads, nice 10) on 8 short spans where the 2 s sampling missed a line (`whisper_gaps.txt`). A full whisper pass was too slow under a box load of about 50, so I stopped it. The OCR captions already cover the narration.
- **Danmaku.** The danmaku file holds 18 comments, in `BV1JhKP6FEjr.danmaku.xml`.

## 2. Story outline (English, own summary)

1. **Escape and news hook.** Late at night, the narrator's father pulls him out of their flat with the warning "it's coming, don't look back" and drives to the next city. The next morning a news app reports that every owner in their residential complex died in their sleep. Only two households survived, because they weren't home.
2. **Dad goes dark.** A phone call shakes Dad. He buys a new phone and SIM, smashes the old phone ("it can be tracked") and makes his son memorise a phone number from a slip of paper and then swallow the paper. They drive to a forest, take two pre-packed bags (food, water, a folding army shovel) and walk to a cabin.
3. **Backstory and first rule.** Dad explains that in university he joined a secret research group on unknown phenomena. The group was shut down, the files destroyed and an NDA signed. The killer is a formless "rule": if you notice it and try to look at it, you are marked, and it erases you and everyone around you. Someone in the complex broke the rule. The group had an early-warning system, and the call was the alarm.
4. **Neighbour at the door.** That night someone knocks on the remote cabin's door. It's the voice of the old neighbour from across the hall, one of the two households that survived. Dad blocks the door. The "neighbour" proves who he is with a domestic detail: the flavour of the dumplings he brought over two days ago. Dad orders the son back to bed. At dawn it's gone, but the safe house is burned.
5. **Dad admits a lie.** There is more than one rule. The group had found an incomplete old notebook full of rules, and each rule is tied to an unknown entity that the professor called a 规则体 ("rule-entity"). "Don't look back" is just the most basic rule. An activated entity spreads by "information assimilation": it copies and imitates, which explains the neighbour's voice and memories. Of the 7 members, the professor and 2 others deliberately triggered a worse rule and vanished along with their lab. The remaining hope is Lin Feng, the group's best technician. He kept researching in secret and found that the entity's assimilation has a ceiling, a point where it "lags and crashes". He is at an abandoned weather station in the north-west no-man's-land, "the weakest signal in the country".
6. **Two pursuers.** An eye-in-a-circle symbol appears carved on a tree, a shadow follows them, and they run. On a road, a black car with the same eye symbol stops near them for ten minutes and scans. Dad calls these people "scavengers" (清道夫): they don't rescue anyone, they erase every trace, including people who were triggered or marked. In his words they're worse than the entities, because they're human and equipped. The two flee into the mountains and follow an abandoned railway. Dad passes on the professor's theory: the entities are the universe's immune system, and people who know about them are the virus.
7. **Tunnel.** A stone cairn and an empty tin can show that someone was here recently. In a long tunnel, bat-like monsters hang from the ceiling. Light makes them convulse and drop. Dad falls and tells his son to run. Screams. The son weeps outside, and then Dad walks out, wounded, saying he fought them off with the shovel.
8. **Strangers.** In abandoned train carriages they meet three survivors with a hunting rifle: the leader "Uncle Ma", his daughter and a red-haired young man. The strangers are hostile until the son says they came through the tunnel, which no one survives. They swap stories. The strangers' village was wiped out by a different rule: a night broadcast of an indescribable noise, and anyone who heard it disappeared. They survived with cotton in their ears in a cellar. Afterwards helicopters circled and the village burned all night, which was the scavengers' work. The red-haired man has a map and the same plan, the north-west no-man's-land. The five travel together, with Uncle Ma in command.
9. **Being herded.** They pass a smoking crater from an incendiary (scavengers), then an abandoned scavenger car with a strange radio-like device. At night a drone hovers at their cave mouth and leaves. Dad: "it saw us; it's marking us; they're waiting to take us all at once."
10. **Ambush on the bridge.** At a gorge crossed only by a wooden bridge, red hazmat scavengers close in from both ends. Their leader names the target: Dad, "Project Chimera, sole survivor", under a "final cleanup protocol". Dad isn't surprised: "Have you collected enough data?" Their weapons glow blue. Dad's body smokes, and his eyes glow the same blue. The beams bounce off him: "the rule is being rewritten; he isn't losing control, he's awakening." He tells the kids to jump into the river and find Lin Feng. He turns translucent, smiles, and says "those three words". Whisper confirms the words are "别回头" (don't look back).
11. **Weather station.** The narrator, the daughter and the red-haired man wash up on a beach. Uncle Ma is missing. The station is empty and thick with dust. Lin Feng's notebook says they were all wrong. The entities aren't a virus or an immune system: they are the world's base source code. Conscious life is the bug, and the scavengers are the repair program. Project Chimera was the professor's attempt to escape the rules. Lin Feng found "Zone Zero", a blank spot outside the system right under this station, but it's unstable unless a strong enough "anchor" holds it, and Dad is that anchor. The narrator realises Dad wasn't fleeing: he was walking to his fate, giving his life to keep a last safe place for people like them. 全剧终 (the end).

## 3. Beat table

Timestamps come from the YouTube mirror, which is roughly the Bilibili time plus 0 to 5 s.

| t | Beat | Mechanic | What the viewer believes now | Open loops |
|---|---|---|---|---|
| 0:00 | Dad drags son out at night: "it's coming, don't look back" | Cold-open action + an imperative rule spoken before any context | Something supernatural is hunting them, and Dad knows what it is | What is "it"? Why not look back? |
| 0:06 | News app: every owner in the complex died in their sleep, 2 households were away | Authority artifact (news UI) confirms the stakes; **count clue** (2 households) | It was real and total | Who is the other household? |
| 0:12 | Son confronts Dad; "it is unnameable" | Withheld explanation | Dad knew in advance | How did he know? |
| 0:22 | Phone rings; Dad trembles and listens for 30 s; "we have to go"; "not knowing is safer" | Mystery caller, plus a protective lie | Someone else is tracking this | Who called? |
| 0:46 | New phone and SIM, old phone smashed, number memorised, paper swallowed | **Burner phone** ritual; Chekhov number ("call this if we're separated") | They're fugitives from people as well | The number is never used (unpaid loop) |
| 1:10 | Dad never checks the mirror; walks into the forest with prepared bags and a shovel | Rule shown through behaviour; prop plant (shovel) | Dad prepared for this for years | |
| 1:26 | Backstory: university group, classified, NDA; "once a rule is known you can't escape it" | Backstory dump framed as a confession | The neighbours broke a rule | What was found? |
| 1:50 | Cabin safe house; "we carry a mark, like a candle in the dark" | Temporary refuge, ticking threat | Safe for now | How long? |
| 2:18 | The rule: noticing or observing it marks you; then it erases you and everyone near you | **Rule statement** (one clean rule) | The rule is understood | Who broke it? |
| 2:36 | The group's early-warning system; the call was the alarm | Answers the caller loop | The caller was an ally | |
| 2:44 | Recall: 2 households away, us and the old couple opposite | **Count clue** made explicit | The neighbours may have sensed it too | Are they safe? |
| 2:54 | Knock at the cabin at night; the neighbour's voice | Mimic at the door; count clue pays off as dread | It might really be the neighbour | |
| 3:12 | Dad blocks the door; "you're the fake one"; the dumpling-flavour proof | **Fake authority + correct detail** (the proof of identity is itself the giveaway) | The son wavers, the viewer wavers | How does it know that detail? |
| 3:30 | Dawn: it withdrew but has locked on; the safe house isn't safe | Partial win, then escalation | The threat follows them | |
| 3:40 | "I lied: there is more than one rule" | **Trusted source contradicted** (Dad's own earlier statement) | The world is bigger: a whole rule ecology | How many rules? |
| 3:44 | Incomplete notebook of rules; rule-entities; "don't look back" is the most basic | Lore expansion, a "bestiary" promise | Each rule is a monster type | |
| 4:02 | Assimilation = copy and imitate, which explains the neighbour | Explains the knock | Mimics have memories | But the neighbour wasn't home: how was he copied? (dismissed: "not my problem") |
| 4:14 | 7 members; the professor and 2 deliberately triggered a worse rule and vanished with the lab | Count plant (7, minus 3) | Dad is a minor survivor | Is Dad telling the whole truth? (he isn't: see 15:56) |
| 4:30 | Goal: find Lin Feng | Quest object named | There is a way out | Where is he? |
| 4:44 | Eye-in-a-circle carved on a tree | **Sigil** = a calling card | "It" is taunting them | Whose symbol is it? (it turns out to be the scavengers') |
| 5:04 | A shadow flits past: "run" | Chase micro-beat | | |
| 5:14 | During the chase: Lin Feng copied the files; assimilation has a ceiling, "like a PC with too much junkware" | Mid-chase exposition; plants the "data overload" idea | The monster can be beaten by overload | Never used as a weapon (red herring for the anchor payoff) |
| 5:44 | Destination: an abandoned weather station in the north-west, the weakest signal | Destination plant | Signal-dead zone = safety | |
| 5:56 | A car approaches; Dad pulls the son flat; the same eye symbol on the car | **Symbol callback** reassigns the threat from monster to humans | The symbol belongs to an organisation | |
| 6:16 | The car idles for 10 min, "scanning", and leaves | Hide-and-hold tension | They got lucky | "Why didn't they find us?" "Maybe luck" (actually being tracked) |
| 6:30 | "Scavengers": erase every trace, including the triggered and the marked | Second antagonist; human worse than monster | Two predators, prey in the middle | |
| 7:08 | They head to the safe house to "process" it | Stakes behind them | | |
| 7:38 | Abandoned railway, a fixed route | Travel-structure device | | |
| 7:48 | Professor's theory: entities = the universe's immune system, we = the virus | **Theory A** (to be overturned) | Humans are the error | |
| 8:12 | Stone cairn and empty tin: someone was here recently | Plant for the strangers | Friend or foe? | |
| 8:24 | A tunnel shortcut ("a day to go around") | Choice under time pressure | | |
| 8:44 | "Don't talk, listen": swarms of bat-monsters on the ceiling | Reveal under flashlight | | |
| 8:54 | Lit monsters convulse and drop; running with the torch backwards | A **rule discovered in action** (light kills them) | They can survive by rule-play | |
| 9:10 | Torch dying; exit in sight; Dad falls: "leave me, run"; screams | Fake death | Dad is dead | |
| 9:24 | Dad walks out wounded: "fought them off with the shovel" | **Reversal** + suspicious survival (the plant pays off) | Is it really Dad? (danmaku: "it's not Dad anymore", "monsters can imitate people") | Mimic suspicion, never resolved as mimicry: paid off as Chimera at 15:56 |
| 9:46 | Abandoned train carriages, signs of a camp | Cairn payoff | | |
| 10:08 | 3 strangers, one with a hunting rifle | Standoff | Out of the tiger's den, into the wolf's lair | |
| 10:24 | Dad's "travellers" lie fails; "you don't look like hikers" | Cover story fails | | |
| 10:48 | "Have you forgotten our rule? Any stranger could be death" | The human group has its own rules | | |
| 11:02 | "We came through the tunnel": the strangers freeze; "a companion of ours only got near its mouth" | **Status flip**: the danger proves them | Surviving the tunnel is impossible, so Dad's survival is very odd | Doubles the Dad suspicion |
| 11:24 | Dad: "we're the same kind of people, hiding from things that shouldn't exist" | Alliance pivot | | |
| 11:36 | Names: Ma Jianguo (Uncle Ma), red-haired Wang Qiang, daughter Lili; the son and Dad give their names | Cast intro, late (11 min in) | | |
| 11:58 | Second rule story: night broadcast of an indescribable sound; anyone who heard it vanished; cotton in the ears, cellar for 3 days | **Embedded rule tale** (a mini rules-horror inside the story) | Many rules are active across the country | |
| 12:40 | Helicopters circled; the village burned all night | Scavengers' MO confirmed | The authorities clean up by fire | |
| 12:56 | Wang Qiang's map; the north-west no-man's-land with the weakest geomagnetic signal | Independent corroboration of the destination | The destination is real | |
| 13:26 | Uncle Ma: "everyone follows my orders; my daughter is not to be endangered" | Group-dynamics friction | | |
| 13:44 | Smoking crater, burnt-plastic smell, incendiary: scavengers were here | Environmental dread | | Who did they burn? |
| 14:12 | Abandoned scavenger car with a radio-like device that has an LCD | Object plant | | Why abandoned? Never answered |
| 14:32 | Cave; "ten more days at this pace" | Time pressure | | |
| 14:44 | Buzz, a drone at the cave mouth for ~10 s, then it leaves | Hide-and-hold, second time | They weren't seen | |
| 15:04 | "It saw us; it's only marking us; they're waiting to catch us all at once" | **Reinterpretation** of earlier luck (car at 6:16) | They're being herded | |
| 15:22 | Gorge with only a wooden bridge; a week to go around | Bottleneck choice | | |
| 15:36 | Mid-bridge: hazmat scavengers behind and in front | Trap closes | | |
| 15:54 | "Target locked: Chen Dashan. Codename Project Chimera, sole survivor. Executing final cleanup protocol." | **Identity reveal by enemy roll-call**; contradicts Dad's backstory | Dad lied about his role | What is Chimera? |
| 16:08 | Dad: "Finally. Have you collected enough data?" / "Your existence is the key data; time to format this error" | Dad knew all along; the enemy uses the computer metaphor | Dad was bait or a subject | |
| 16:20 | Blue weapon glow; Dad smokes; his eyes glow the same blue; the beams bounce off | **Visual rhyme** (matching blue) = Dad is part of the rule system | He's becoming a rule-entity | |
| 16:42 | "The rule is being rewritten: not losing control, awakening" | Power-up reversal | Dad might win | |
| 16:48 | "Jump; find Lin Feng at the weather station; he knows the answer" | Quest handoff | | |
| 16:56 | Dad turns translucent, smiles, says "those three words": "don't look back" | **Bookend callback** to the 0:02 rule; sacrifice | Dad is gone | |
| 17:04 | Beach; Uncle Ma missing; Lili sobs | Loss beat, cast reduction | | Uncle Ma's fate is never resolved |
| 17:34 | The station is empty and dusty; Lin Feng's notebook | Discovered document | Lin Feng is dead or gone | |
| 17:48 | Notebook scroll: entities = source code; we are the bug; scavengers = repair program; Zone Zero; it needs an anchor; Dad is the anchor | **Theory B overturns Theory A** + final re-reading of the whole journey | Dad sacrificed himself to stabilise the safe zone | |
| 18:38 | "Dad wasn't fleeing; he was walking toward his fate"; "全剧终" | Emotional resolution, closed ending | | No part 2 |

## 4. Clue chain

| Clue planted | Where | Payoff | Where |
|---|---|---|---|
| "Don't look back" (first spoken line) | 0:02, 1:10–1:14 (Dad never uses the mirror) | Defined as the basic rule (2:18, 3:54); **Dad's last words** | 16:58–17:00 |
| "2 households weren't home" | 0:10 news, 2:44 recall | The neighbour mimic knocks at the remote cabin | 3:02 |
| The neighbour proves himself with a private food detail | 3:18 | Explained as assimilation (copied memories) | 4:02–4:06 |
| "But the neighbour wasn't home: how was he copied?" | 4:08 | Dismissed ("not my problem"); never paid. A deliberate unease or a plot hole | — |
| Mystery phone call | 0:22 | The group's early-warning system | 2:36–2:42 |
| Number memorised and paper swallowed | 0:56–1:06 | **Never paid** (danmaku jokes about the clerk) | — |
| Army shovel in the bag | 1:20 | Dad "fought the monsters off with the shovel" | 9:28 |
| "We're marked, like a candle" | 2:10 | The drone is "marking" them; ambush | 15:04, 15:36 |
| 7 members; the professor and 2 vanished | 4:16–4:24 | Dad is the "sole survivor of Project Chimera", so he was in the experiment | 15:56 |
| Lin Feng: assimilation has a ceiling, overload "crashes" it | 5:30–5:40 | Not used as a weapon; reframed as the "data" line ("collected enough data?") | 16:10 |
| Weather station, weakest signal | 5:44–5:48 | Corroborated by Wang Qiang's map (13:02); the station sits on Zone Zero | 17:34, 18:26 |
| Eye-in-circle symbol on a tree | 4:50 | The same symbol on the black car, so it's the scavengers' mark | 6:10–6:12 |
| The car scans and leaves: "maybe luck" | 6:16–7:06 | Reinterpreted: they were being tracked; drone; trap | 15:04–15:50 |
| Professor's theory: entities = immune system, humans = virus | 7:52–8:08 | Overturned: entities = source code, humans = bug | 17:50 |
| Cairn and empty tin can | 8:14–8:16 | The strangers' camp | 9:52–10:04 |
| Light kills the bat-monsters | 8:54–9:08 | Implicit: Dad survived in the dark, which signals he isn't normal | 9:24, 11:08–11:16 |
| Dad survives the tunnel with wounds | 9:24–9:36 | Strangers: no one survives that tunnel (11:08–11:16). Payoff: Dad is a Chimera subject who can resist rules | 16:20–16:44 |
| A village rule: a sound you must not hear | 11:58–12:34 | World-building: rules are spreading. The scavengers burned the village | 12:40–12:52 |
| Scavengers use fire | 12:48 | Incendiary crater | 13:48–13:58 |
| Abandoned scavenger car with a device | 14:12–14:30 | **Never paid** | — |
| Scavenger weapon glows blue | 16:20 | Dad's eyes glow the same blue | 16:28–16:30 |
| "Those three words" | 17:00 | They are "don't look back" (audio only; the caption cuts away) | 17:00 |
| Dad's calm, fated look | 16:02–16:06 | Notebook: Dad is the anchor; the trip was a pilgrimage | 18:36–18:46 |

## 5. Twist inventory

| # | Twist | Type | Setup |
|---|---|---|---|
| 1 | The trusted neighbour at the door is a copy | Mimic / impostor at the threshold | The 2-surviving-households count clue plus the remoteness of the cabin ("how could he find us?") |
| 2 | "I lied: there's more than one rule" | The narrator's guide admits a lie (unreliable mentor) | Dad had been withholding information since 0:12 ("not knowing is safer") |
| 3 | The eye symbol belongs to humans, not the monster | Reattribution of a sign | Tree carving at 4:50 read as the entity taunting them |
| 4 | Human cleaners are worse than the monster | Second-antagonist reveal (authority as predator) | Burner-phone ritual (they're running from people too); the car |
| 5 | Dad "dies" in the tunnel, then walks out | Fake death and return, with a mimic suspicion | Light-kills-monsters rule; the strangers say no one survives |
| 6 | The strangers' fear flips to respect | Status flip through a shared ordeal | Gun standoff; the tunnel's reputation |
| 7 | Luck was surveillance: they were being herded | Reinterpretation of past events | "Why didn't they find us?" "Maybe luck" (7:04) |
| 8 | Dad is the target and the sole survivor of the secret project | Identity reveal by the enemy's roll-call | 7-member count, the vanished three, Dad's impossible survival, his lack of surprise |
| 9 | Dad's power matches the enemy's (blue eyes); he awakens | Hero is part of the system (hybrid / "Chimera") | Weapon glow established one beat before |
| 10 | Last words = the first rule | Bookend callback | Opening line |
| 11 | Monster = the world's code; humans = the bug; cleaners = the repair program | Cosmology inversion (Theory B overturns Theory A) | Professor's immune-system theory; recurring "virus" and "computer junkware" metaphors |
| 12 | Dad was never fleeing; he was going to become the anchor | Purpose reveal (flight → pilgrimage) | "Have you collected enough data?"; Dad's fated calm; Lin Feng as the goal from 4:30 |

Twist density: about 12 in 18.9 min, roughly one every 95 s. Smaller reversals (shadow, drone, bridge) fill the gaps.

## 6. GENERIC vs SPECIFIC

**GENERIC: genre conventions anyone can use**
- Cold open with a parent pulling a child out of the house at night, then a news artifact confirming mass death. (The "warned the night before" premise is common across studios.)
- A single imperative rule spoken before any explanation ("don't X"), which comes back as the last line.
- A count clue in a casualty report ("N survivors"), paid off when a "survivor" shows up where they shouldn't.
- A mimic at the door that proves its identity with an intimate detail. The detail itself is what gives it away.
- A burner-phone ritual (destroy the trackable phone, memorise a number) to signal that the hunters are human too.
- A mentor who admits "I lied, there's more than one rule", which expands the world into a rule ecology.
- Two predators: a supernatural force plus a human clean-up organisation that erases witnesses. A calling-card symbol links them.
- An embedded mini rules-tale told by other survivors (a different rule, a different village), which shows the scale.
- A rule discovered in action (a light or sound weakness) during a chase.
- A fake death followed by a suspicious survival, letting the audience suspect a replacement.
- "Luck" re-read as surveillance; a drone or vehicle that sees but doesn't strike.
- Roll-call reveal: the enemy reads out the hero's codename.
- Matching visual tint (eyes glow like the enemy's weapon) = secret kinship.
- A found notebook at the destination that overturns the cosmology; a sacrifice ending.
- Computer metaphors for cosmic horror (bug, format, source code, repair program) are common in 2025–26 Chinese 脑洞 content.
- Censorship homophones in captions (三 for 死 "death", so 三亡, 殊三搏斗). This is a platform workaround, not style. English versions don't need it.

**SPECIFIC: this author's expression; a transposed story must NOT reuse**
- Names and roles: 陈大山 (the dad), 陈杰 / 小杰 (the son), 李大爷 (the neighbour), 陈教授 (the professor), 林峰 (the technician), 马建国 / 马叔 (the survivors' leader), 王强 (red-haired), 丽丽 (the daughter). Also the complex named after the studio (杰出小区).
- The exact twist chain: university research group, NDA, 7 members, the professor and 2 vanish, Dad as the Chimera survivor, awakening, anchor of Zone Zero at a weather station.
- Named concepts: 规则体 ("rule-entity"), 信息同化 ("information assimilation"), 清道夫 (the "scavengers"), 奇美拉项目 (Project Chimera), 零号地带 (Zone Zero), "anchor", "final cleanup protocol".
- The specific clue combination: the dumpling-filling proof; swallowing the phone-number slip; the eye-in-circle symbol on a tree and then on a car; cairn plus tin can; bat-monsters killed by flashlight in a railway tunnel; a village broadcast noise with cotton in the ears; a smoking incendiary crater; an abandoned car with a radio device; a drone at the cave mouth; the wooden-bridge ambush with a river jump.
- Cosmology lines: "the entities are the world's source code, we are the bug, the scavengers are the repair program"; "like a PC loaded with junk software"; "a candle lit in the dark"; "your existence is the key data; time to format this error".
- The ending image: last words "don't look back" as a reveal held back from the captions; the dad turning translucent on the bridge.
- Strangers met in abandoned train carriages, with the leader holding a hunting rifle and a "my daughter must not be endangered" condition.

**Transposition note.** Borrow the skeleton: night escape → rule → mimic → mentor's lie → two predators → embedded tale → herded → roll-call reveal → sacrifice → cosmology inversion. Change everything else: a different relationship (for example a sister or a landlord), a different rule sense (for example counting or reading instead of looking), a different organisation and sigil, a different sanctuary logic, different set pieces and our own metaphor family (not "bug/source code").

## 7. Pacing

- **Caption density.** 496 OCR caption lines over about 17.9 min of narrated content (the 50 s notebook scroll is excluded). That's about **28 lines/min**, one new caption every 2.1 s, steady at 26–29 lines in every minute bucket from 0 to 16. It's a lower bound, because 2 s sampling misses some short lines (whisper found about 5 missing in 8 spot-checked spans).
- **Words per minute.** About **325 hanzi/min** (6,135 hanzi), 12.4 hanzi per line. English equivalent: about 170–190 wpm of TTS. The 15:18 English repost is consistent with that.
- **Line shape.** One clause per caption. Narration ("随后…", "我听罢…", "就在这时…") alternates with dialogue about 50/50. "就在这时" (just then) is used as a re-hook connector roughly every 1–2 min.
- **Re-hook interval.** A new threat, reveal or reversal arrives roughly every **25–40 s** (median about 30 s): 0:00, 0:06, 0:22, 0:46, 1:26, 2:18, 2:54, 3:12, 3:40, 4:14, 4:44, 5:04, 5:56, 6:30, 7:48, 8:12, 8:44, 9:14, 9:24, 10:08, 11:02, 11:58, 12:40, 13:48, 14:12, 14:44, 15:04, 15:36, 15:54, 16:20, 16:56, 17:46. The longest lull is 7:08–7:48 (walking and railway exposition, 40 s).
- **Hook.** 10 s: the action line, the "don't look back" rule, then the news screen with mass death and a survivor count. The confrontation question comes at 0:12. The title gives away the hook premise. The video delivers it in 10 s and then moves on.
- **Structure.** Escape/lore (0–5 min) → road with two predators (5–9:30) → group (9:30–15:20) → ambush/reveal (15:20–17) → coda/notebook (17–18:54). Major reveals land at about 21%, 50%, 84% and 95%.
- **Cliffhanger / part 2.** None. It's a single closed episode ("全剧终"), with no on-screen part card. Dangling threads (Uncle Ma's fate, the phone number, the device, Wang Qiang's eagerness over the map) are left open but not used as hooks. For TikTok, a reposter would have to cut parts at internal cliffhangers. Candidates: 3:12 (door), 9:20 (Dad falls, screams), 15:54 (roll-call reveal). They are about 3–6 min apart, which suits udhwkz-style 3-min parts.
- **Exposition load.** It's heavy. About 30% of the lines are lore dialogue (2:16–2:44, 3:40–4:40, 5:12–5:48, 6:30–7:02, 7:48–8:10, 17:48–18:36). The author hides it inside motion (running, walking the railway), so the frame is never static during exposition.
- **Danmaku spikes** (viewer engagement) fall at: the phone-shop clerk/number (63 s); the dad return, with suspicion "not Dad anymore" (571–586 s); the "travellers" cover story mocked ("travellers carrying a shovel?", 634 s); "monsters can imitate people" still being posted during the group march (808 s); the Project Chimera reveal (952 s). Suspicion of the returning parent is the strongest engagement point.

## 8. Visual vocabulary

- **Style.** 沙雕 flat 2D vector puppets: big heads, thick black hair, exaggerated eyebrows and eye-bags, and a limited set of expressions (furrowed anger, wide-eyed shock with tiny pupils, tearful wobble, a blank stare for creepiness). The hero always wears a neon-yellow jacket and Dad a black T-shirt, a costume code that makes them readable at thumbnail size. 16:9 at 854×480, with captions burned in as white text with a dark outline, bottom-centre.
- **Phone UI.** Only once: a hand holding a phone with a "新闻频道" (news channel) app card and a short headline paragraph, at 0:08. Not a chat story; no group chat or DM UI.
- **Paper props.** The phone-number slip in close-up at 0:56–1:06, a folded map, and the final notebook. The notebook is a full-screen aged-paper page that scrolls slowly, about 25 lines held about 50 s while the narration reads it. The captions double up here: the current line plus the held key line "Dad is the anchor".
- **Rooms and locations.** Bedroom/doorway at night, phone shop, green car on the road, forest (layered bush parallax), cabin interior (table, two chairs, wooden door), black SUV with the sigil, railway, dark tunnel with a flashlight cone, abandoned train carriage interior, village loudspeaker pole with lightning-bolt "sound" marks, smoking crater, abandoned car interior with a gadget, cave mouth with a drone, an orange-sky gorge with a wooden bridge, a beach, and a dusty living room at the weather station.
- **Monsters.** Silhouetted bat-creatures with red eyes in a dark frame; they're never shown in daylight. The "rule" itself is never drawn: it's shown through a knock, a voice, a symbol or an eye-sigil. The scavengers are red hazmat suits with gas masks and black rifles.
- **Overlays and FX.** Lightning-bolt marks for a phone ringing or the loudspeaker; a flashlight cone; a white smoke puff; a blue eye glow (lens flash); translucency or fade for the dissolving dad; a red-dot eye sigil drawn as an inset close-up; an orange sky for the climax.
- **Camera grammar.** Two-shot of father and son for exposition, with slow push-ins on reaction faces. A cut to an insert of an object (paper, sigil, gadget) on every clue line. Group lineups for the five-person segment. Almost no camera movement beyond pans and zooms on stills, which makes this cheap to reproduce in Remotion/SVG.
