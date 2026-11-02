# Story topic queue (RicksClips3000 lane)

Built 2026-11-02. Ten history-mechanism topics, ranked and fact-checked, for the story lane. The target is RicksClips3000 parity: 2D characters lit in a 3D world, the paradox stated as fact in line 1, the "You see, ..." reveal at about 2/3, and an ironic last line.

**Already used, don't reuse:** story-chess-turk (posted), story-vasa (in production). Two of the earlier premises in LANE_PRINCIPLES.md were already done by Zack D. Films: the Nijō squeaking floor (30M) and the Broughton bridge "break step" (9.4M). Neither is in this queue.

**Status rule.** A topic is **used** once `episodes/<slug>` exists. To refresh the Status column, run:

```
python3 research/library/story_queue_status.py
```

It only rewrites that column in this file. Pick the highest open row.

## How each topic was vetted

- **Principles.** Every topic passes the screen in LANE_PRINCIPLES.md ("Topic features beyond S1 and S-env"):
  - S1: real, and set in a named past or foreign world.
  - S-env: at least 4 places the camera can travel through.
  - T1: the mechanism is physics, engineering or a real institution, not a con.
  - T5: surprise of 2 or more.
  - T6: a title that names the object and hides the mechanism.
  - S6 (ridicule, then vindication) and T3 (East Asia) count as bonuses.
- **Facts.** Each fact was checked against two independent reputable sources: encyclopedias, peer-reviewed or university pages, museums, heritage and government bodies, and translated primary texts. Wikipedia was not counted as a source.
  - **Exception:** for ancient events the only witness is the ancient author. There, "two sources" means two ancient authors where possible, or the author in two independent translations, and the fact is flagged *single ancient source*.
  - Anything contested is marked **CONTESTED**, with the wording that is safe to use.
- **Dramatization rule (T7).** RicksClips invents plot, dialogue and minor characters around a true mechanism, and so may we. What may not be invented is any number, date, name or mechanism that is stated as fact; those come from the facts below. Contested items are either left out or hedged on screen ("by one count", "legend says").
- **Coverage check** (2026-11-02, on the Spark, metadata only):
  - RicksClips3000: all 146 titles.
  - Zack D. Films: all 4,122 Shorts titles.
  - Shorts tabs of Kings and Generals (527), Simple History (451), The Infographics Show (598), National Geographic (864) and TED-Ed (24).
  - `yt-dlp ytsearch20` with two phrasings per topic (one with "#shorts").
  - "Clear" means no Short on the topic above about 10K views.

## Queue

| Rank | Slug | Working title | Place / era | Status |
|---|---|---|---|---|
| 1 | story-barca-shield | The Ancient Shield That Heard an Army Underground | Barca, Libya, c. 515-510 BC | open |
| 2 | story-myeongnyang | The Korean Strait That Changed Sides | Myeongnyang strait, Korea, 1597 | open |
| 3 | story-dutch-waterline | Why the Dutch Flooded Their Own Country | Holland, 1672 | open |
| 4 | story-dujiangyan | Why China's 2,000-Year-Old Dam Isn't a Dam | Sichuan, c. 256 BC | open |
| 5 | story-storm-bells | Why Bell Ringers Kept Dying in Storms | Germany / Brescia, 1700s | open |
| 6 | story-edo-firemen | Why Japan's Firemen Smashed the Wrong House | Edo (Tokyo), 1657-1720 | open |
| 7 | story-fresnel-lens | Why Lighthouse Lenses Look Broken | Cordouan, France, 1823 | open |
| 8 | story-copper-navy | Why Old Warships Had Copper Bottoms | Royal Navy, 1761-1825 | open |
| 9 | story-thames-shipworm | The Worm That Dug Under the Thames | London, 1818-1843 | open |
| 10 | story-eupalinos | The Ancient Tunnel Dug From Both Ends | Samos, 6th c. BC | open |

**Why this order.**
- **Ranks 1-4** carry the most of the top-tier pattern:
  - a physical mechanism the viewer couldn't guess;
  - a city or nation at stake;
  - a place that changes as the story moves (above ground to underground, open sea to narrows, dry farms to flood to ice, mountain to river to plain).
  - Ranks 2 and 4 also get the East Asia tiebreak (T3).
- **Ranks 5-7** are strong on mechanism but carry contested figures (5) or smaller stakes (6, 7).
- **Ranks 8-10** need the most explaining (8) or have the least visible mechanism (9, 10).

---

## 1. The Ancient Shield That Heard an Army Underground (`story-barca-shield`)

- **Paradox first line:** "An army was camped outside the city walls, and the city's bronze-smith spent every day laying a shield on the ground."
- **Story:**
  - The Persian army besieges Barca for months, and assaults on the walls fail.
  - Inside, a metalworker walks the inner wall, sets his bronze shield face-down on the earth, and moves on. The soldiers mock him.
  - At one spot the shield starts to ring, and dust shivers on the bronze.
- **"You see" reveal (about 2/3):** "You see, the Persians had stopped attacking the wall. They were digging under it."
  - Over solid ground a bronze shield gives a dead thud. Over a hollow, with picks striking below, it rings.
  - Wherever it rang, the defenders dug down and broke into the Persian tunnel.
- **Ironic ending (true):** the city still fell, but not from below.
  - The Persians dug a trench, covered it with thin planks and earth, and swore a truce to last "as long as this earth stays as it is". Then they broke the planks and walked in.
  - Last line: "They couldn't get under the city, so they made the ground lie instead."
- **Camera travels through:**
  1. the Persian camp on the plain;
  2. the walls and the streets behind them (the smith's walk);
  3. a cross-section of the tunnel under the wall, with diggers by lamplight;
  4. the countermine breaking through;
  5. the truce trench at the gate.
- **Why it should hit:**
  - S1: real, ancient, foreign.
  - S2: an odd concrete act, with the real reason landing at 2/3.
  - S3 and T1: a physical mechanism you can watch, a ringing shield.
  - S4: a city at stake.
  - S6: mocked, then vindicated.
  - S-env: above ground and below ground, five places.
  - T5: surprise 3. The shield is used as an ear, not as armour.
  - T6: the title names the object and the world and hides the how.
  - The same family as the Jar (30.7M): an ancient object that "senses" a threat no one else can.
- **Verified facts:**
  1. **The siege, the tunnels and the shield.** Aryandes' army besieged Barca for nine months, digging mines toward the wall. A bronze-worker laid a bronze shield on the ground inside the wall. It was dull over solid ground and rang over a tunnel, and the Barcaeans countermined there and killed the diggers.
     - Herodotus 4.200: https://lexundria.com/hdt/4.200/mcly (Macaulay translation).
     - Aeneas Tacticus, *On Siegecraft* 37.6-7, tells the same shield story independently and says the method was still in use in his day (4th c. BC): https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Aeneas_Tacticus/F*.html (Loeb).
     - The nine-month length is in Herodotus only (*single ancient source*). It is also in the Rawlinson translation: https://en.wikisource.org/wiki/The_History_of_Herodotus_(Rawlinson)/Book_4
  2. **The trench-and-oath trick.** The Persians dug a trench at night, covered it with weak timbers and earth, and swore the truce on top of it, to hold "so long as this earth should continue to be as it was". Then they broke the planks and entered.
     - Herodotus 4.201 in two translations: https://lexundria.com/hdt/4.201/mcly · Rawlinson (link above).
     - *Single ancient source.*
  3. **The same principle at Apollonia.** The architect Trypho of Alexandria hung bronze vessels in galleries inside the wall. The vessels rang from the enemy's iron tools, and the defenders killed the miners with boiling water, pitch and hot sand.
     - Vitruvius 10.16.9-10: https://penelope.uchicago.edu/Thayer/E/Roman/Texts/Vitruvius/10*.html (Gwilt) · https://www.gutenberg.org/files/20239/20239-h/20239-h.htm (Morgan).
  4. **Date. CONTESTED.** Livius.org gives c. 512 BC: https://www.livius.org/articles/person/aryandes/ . The University of Colorado coin project gives 510 BC: https://www.colorado.edu/project/expressionsofidentity/2026/04/17/barca . Say "about 2,500 years ago" or "c. 515-510 BC".
  - **Leave out:** Herodotus 4.202 (the impalements and mutilations). It is true but too graphic for the lane.
- **Coverage: clear.**
  - Not in RicksClips' titles, Zack D.'s titles or the big channels' Shorts.
  - The searches ("bronze shield detect enemy tunnels siege #shorts", "Herodotus Barca shield mining", "ancient trick to find enemy tunnels") return no Short on the topic. The top hits are Vietnam-tunnel and survival-build videos.

## 2. The Korean Strait That Changed Sides (`story-myeongnyang`)

- **Paradox first line:** "The king ordered him to give up the navy, so he took his last thirteen ships and sailed them at a hundred and thirty-three."
- **Story:**
  - Korea's fleet has just been wiped out at Chilcheollyang, and the king orders Admiral Yi Sun-sin ashore. He answers that he still has twelve ships.
  - He waits at the mouth of the loudest, narrowest strait in Korea. The locals call it Uldolmok, roughly "the crying strait", for the roar of its water.
  - The Japanese fleet pours in with the current behind it, and his own captains hang back in fear.
- **"You see" reveal (about 2/3):** "You see, the water in that strait runs like a river, and four times a day it turns around."
  - The Japanese rode the current in through a gap 293 m wide, where only a few ships could reach him at once.
  - When the tide turned, the same current shoved their ships back into each other.
- **Ironic ending (true):**
  - Korean records count 31 Japanese ships lost and none of Yi's. He still had to withdraw north afterwards.
  - Today a tidal power station runs on that same current.
  - Last line: "He didn't have a navy. He had a sea that could change sides."
- **Camera travels through:**
  1. the burning wreck of the fleet after Chilcheollyang;
  2. the royal court and the messenger;
  3. the strait seen from the Jindo cliffs, with whirlpools;
  4. the Japanese anchorage at Eoranpo (about 330 ships);
  5. the narrows battle;
  6. the strait today, with the turbine.
- **Why it should hit:**
  - S1: real, foreign, 1597.
  - S2: an odd act (13 against 133), with the reason at 2/3.
  - S3 and T1: physics. You can watch the current run and reverse.
  - S4 and T4: a nation at stake, which here sits on a real mechanism.
  - S6: ordered to quit, then vindicated.
  - S-env: six places.
  - T3: East Asia.
  - T5: surprise 2-3.
  - T6: the title names the strait and hides the tide.
- **Verified facts:**
  1. **When and where.** The battle was fought on the 16th day of the 9th lunar month, 1597 (26 Oct 1597 Gregorian), in the Myeongnyang (Uldolmok) strait between Jindo island and Haenam on the mainland.
     - Encyclopedia of Korean Culture: https://encykorea.aks.ac.kr/Article/E0018249
     - Kim Hyun-jong, *J. Korean Navigation & Port Research* 39(3), 2015: https://db.koreascholar.com/Article/Detail/309488
  2. **The current.** Up to 11.5 knots at spring tide (PNNL gives about 6 m/s). The strait is 293 m wide and 19 m deep at its narrowest. The flow reverses about four times a day.
     - Encykorea (above).
     - PNNL Tethys: https://tethys.pnnl.gov/project-sites/uldolmok-tidal-power-station
  3. **The odds.** Yi had 13 ships. About 330 Japanese ships had gathered at Eoranpo, and about 133 entered the strait. Korean sources record 31 Japanese ships destroyed.
     - Korea JoongAng Daily: https://www.koreajoongangdaily.com/korea/separating-historical-films-facts-from-fiction/11137249
     - Encykorea (above).
     - **CONTESTED:**
       - The Japanese records give no ship-loss total.
       - Japanese historians call it a Korean tactical win but a Japanese strategic win: https://ipu.repo.nii.ac.jp/records/792
       - Say "Korean records count 31".
  4. **The order and the reply.** After Chilcheollyang (late August 1597), the king told Yi to give up the navy and fight on land. Yi refused, saying he still had twelve warships (今臣戰船 尙有十二).
     - Korea Times: https://www.koreatimes.co.kr/opinion/20250511/modern-korea-takes-pride-and-heart-in-adm-yi-sun-sins-legacy
     - Encykorea (Chilcheollyang): https://encykorea.aks.ac.kr/Article/E0058551
     - Treat the exact wording as the *traditional quotation*.
  5. **The tide turned mid-battle. CONTESTED** (a modern reconstruction).
     - Encykorea says the current switched in Korea's favour.
     - Kim 2015 reconstructs that day's turns at about 06:36, 12:48 and 19:06.
     - Yi's diary does not plainly say "the tide turned".
     - Safe wording: "historians reconstruct that the tide turned".
  - **Leave out:** the iron chains strung across the strait. They are probably legend; no primary source records them: http://www.ppss.kr/news/articleView.html?idxno=25678
- **Coverage: clear for Shorts.**
  - Zack D. has "How Turtle Ships Worked" (37M): same admiral, different topic.
  - Searches turn up only small Shorts (≤ 4K views: an Age of Empires clip and a travel clip), plus a "Decisive Korean Victory meme" Short (608K, 51 s). From its title it is a meme, not a story; I didn't open it to check.
  - Long-form exists (Samuel Hawley's Imjin War series, 43K) and the 2014 film *The Admiral: Roaring Currents*. The film may raise recognition in Korea.

## 3. Why the Dutch Flooded Their Own Country (`story-dutch-waterline`)

- **Paradox first line:** "To stop the biggest army in Europe, the Dutch opened their own dikes and drowned their own farms."
- **Story:**
  - It is June 1672, and Louis XIV's army is across the Rhine.
  - A sluice-keeper (a composite figure) opens the gates, and water creeps across the fields: ankle-deep, then knee-deep, then it stops rising.
  - Farmers riot, and in Gouda they storm the town hall. The French officers laugh: Holland is defended by puddles.
  - French cavalry ride in. A horse steps forward and vanishes.
- **"You see" reveal (about 2/3):** "You see, the water was kept about forty centimetres deep, on purpose."
  - That is too shallow for any boat, and too deep to march through with horses and cannon.
  - Under it, every ditch and canal disappeared. Each step could be solid field or a drowning.
- **Twist ending (true):**
  - In December a hard frost turns the water to a road. French troops march across the ice and burn Bodegraven and Zwammerdam.
  - Then the thaw comes, the ice softens under them, and they hurry back.
  - Last line: "Holland was safe as long as its water stayed water."
- **Camera travels through:**
  1. French columns at the Rhine;
  2. a sluice and a dike being cut;
  3. flooded polders, with fences and trees half under water;
  4. the Gouda town-hall riot;
  5. the frozen white plain;
  6. the burning villages;
  7. the thaw.
- **Why it should hit:**
  - S1: real, 1672.
  - S2: an odd act, flooding your own land.
  - S3 and T1: physics. The depth is the mechanism, and you can watch it hide the ditches.
  - S4: a nation at stake.
  - S6: mocked by the enemy and fought by the farmers, then vindicated.
  - S-env: seven places, and the set itself changes (dry, flood, ice, thaw).
  - T5: surprise 3. Shallow water as the defence.
  - T6: a "Why [group] [did odd thing]" title.
- **Verified facts:**
  1. **The flooding orders.** The French crossed the Rhine on 12 June 1672, and Holland ordered the inundations on 13 June. Amsterdam opened its sluices on 19 June. The flooding stopped the French short of Holland.
     - Berends et al., *Tijdschrift voor Waterstaatsgeschiedenis* 2023: https://waterstaatsgeschiedenis.nl/tijdschrift/2023-2/TWG2023-2_53-70.pdf
     - Britannica, "Dutch War": https://www.britannica.com/event/Dutch-War
  2. **The depth.** About 40 cm: too deep to wade with horses and cannon, too shallow for boats, and the edges of ditches and rivers became invisible. Amsterdam's resolution of 23 June 1672 ordered the water kept high enough that "one cannot tell the ditches between the fields".
     - Erfgoedhuis Zuid-Holland: https://www.erfgoedhuis-zh.nl/media/kfzhip1c/basisinformatie-lesproject-oude-hollandse-waterlinie.pdf
     - TWG 2023 (above).
     - Other figures run 30-60 cm. Say "about knee-deep / 40 cm".
  3. **Farmers fought it.** They sabotaged dikes, closed breaches and pumped polders dry with windmills. On 16 July 1672 farmers stormed Gouda's town hall and held the council hostage.
     - TWG 2023 (above).
     - Erfgoedhuis Zuid-Holland (above).
  4. **The frost and the thaw.** "A hard frost in December enabled Luxemburg to penetrate into Holland, but a rapid thaw compelled a hasty withdrawal." Bodegraven and Zwammerdam were terrorized and burned on 28-30 December 1672.
     - Edmundson, *History of Holland* (Cambridge, 1922): https://www.historion.iovan.net/history-holland/chapter-xviii-stadholderate-william-iii-1672-1688
     - *De Boekenwereld* (DBNL): https://www.dbnl.org/tekst/_boe022198801_01/_boe022198801_01_0003.php
     - **CONTESTED:**
       - The crossing date varies between 27 and 30 December.
       - The target was The Hague, not Leiden.
       - Much of the atrocity detail comes from Dutch propaganda prints. Say "reported atrocities".
  - **Caveat:** the 1672 line itself is not UNESCO-listed. Its 1870-1940 successors (Dutch Water Defence Lines, 2021) are: https://www.uu.nl/en/in-the-media/the-new-dutch-waterline-included-on-world-heritage-list-unesco
- **Coverage: clear.**
  - Neither the Ricks nor the Zack lists cover it.
  - The Infographics Show has "How the Dutch Reclaimed So Much Land From the Sea" (177K), and TED-Ed has a long video, "Why isn't the Netherlands underwater?" (3.7M). Both are about land reclamation, not the defensive flood.
  - No Short on 1672 turned up.

## 4. Why China's 2,000-Year-Old Dam Isn't a Dam (`story-dujiangyan`)

- **Paradox first line:** "Every summer the river drowned the plain, and the new governor refused to build a dam."
- **Story:**
  - The Min River crashes out of the mountains onto the Chengdu plain.
  - Li Bing, the Qin governor of Shu, doesn't wall it off. Instead he has workers sink long bamboo baskets of river stones in the middle of the current, shaping a pointed island like a fish's mouth.
  - He also cuts a narrow gap through a mountainside. Officials scoff (dramatized).
  - Then the summer flood arrives.
- **"You see" reveal (about 2/3):** "You see, he didn't stop the river. He split it in two, at a bend."
  - In the dry season the deeper inner channel takes about 60% of the water, to the farms.
  - In flood, the wider outer channel takes about 60%, away from them.
  - A spillway, the Flying Sand Weir, throws excess water and most of the sand back into the outer river.
  - Nothing blocks the river, so there is nothing to burst.
- **Ending (true):**
  - It still waters about 11.65 million mu (about 777,000 ha) for over 30 million people.
  - In the 2008 Wenchuan earthquake the Fish Mouth got only minor cracks, while nearby modern dams were being watched for collapse.
  - Last line: "He didn't fight the river. He gave it two roads."
- **Camera travels through:**
  1. the snowy gorge the Min comes out of;
  2. the flooded plain;
  3. the river island being built from stone baskets;
  4. the cut through Mount Yulei (the Bottle-Neck);
  5. the weir in flood;
  6. green fields and the city today.
- **Why it should hit:**
  - S1: real, ancient China.
  - S2: an odd refusal, with the reason at 2/3.
  - S3 and T1: hydraulics you can watch.
  - S4: a whole province at stake.
  - S-env: six places along one river.
  - T3: East Asia.
  - T5: surprise 3. A dam that isn't a dam.
  - T6: a tension title in the same shape as "Why Perfect Railroads Don't Work".
- **Verified facts:**
  1. **Who and when.** Built around 256 BC by Li Bing, Qin governor of Shu. It is still in use, and was inscribed on the UNESCO World Heritage list in 2000 with Mount Qingcheng.
     - UNESCO: https://whc.unesco.org/en/list/1001
     - Asian Development Bank: https://development.asia/explainer/applying-ancient-wisdom-disaster-risk-mitigation
     - **CONTESTED:** the date is conventional (other accounts give 251 BC for completion). Say "about 2,300 years ago".
  2. **The "four-six" split.** About 60% of the water goes to the inner river in the dry season and about 40% in flood.
     - ADB: https://www.adb.org/news/videos/nature-based-approach-managing-climatic-risks-and-natural-disasters
     - Sixth Tone: https://www.sixthtone.com/news/1008097
  3. **The weir and the baskets.** The Flying Sand Weir spills excess water and silt into the outer river (ADB: up to 90% of the sediment). The levees were built from stone-filled woven bamboo cages (*zhulong*) braced with wooden tripods.
     - ADB (development.asia, above).
     - Sixth Tone (above).
  4. **What it waters today.** 11.65 million mu irrigated in 2025, in 8 cities and 41 counties, serving over 30 million people.
     - Science and Technology Daily: https://www.stdaily.com/web/gdxw/2026-01/05/content_457227.html
     - Xinhua, which gives the round figure "ten million mu": https://www.news.cn/local/20260322/c054f47444584f4dbda3b58c5b484fc0/c.html
  - **CONTESTED, don't state as fact:**
    - That the Bottle-Neck was cracked open with fire and cold water. The earliest text (*Huayang Guozhi*) has Li Bing burning a cliff at a different site, and mentions no water.
    - That Dujiangyan "fed Qin's unification". This is interpretation.
- **Coverage: partial.**
  - Clear on the Ricks and Zack lists.
  - National Geographic has a documentary Short, "See an Ancient Wonder of China that Transforms a River" (1.8M, 140 s). It is footage-led, not a story, and T8 says prior coverage doesn't block a story retelling, but it is the one topic here already seen at scale.

## 5. Why Bell Ringers Kept Dying in Storms (`story-storm-bells`)

- **Paradox first line:** "Whenever lightning came, the village sent one man up into the tallest building in town."
- **Story:**
  - The bells say it themselves: *fulgura frango*, "I break the lightning".
  - In every storm a young ringer climbs the church tower and hauls the wet rope, while the village prays below.
  - Towers are struck and ringers die, and the priest says to ring harder. A visiting scholar suggests an iron rod on the roof, and is laughed out of the square (dramatized; see fact 5).
- **"You see" reveal (about 2/3):** "You see, the bell tower was the tallest point for miles, and lightning takes the shortest road to the ground."
  - A soaked rope, with a man holding it, was that road.
  - The ringing never pushed a storm anywhere. The tower just showed the lightning where to land.
- **Big payoff (true):**
  - Brescia, 18 August 1769: the Republic of Venice kept about 2,800 barrels of gunpowder in the tower of the San Nazaro bastion.
  - Lightning hit it, and hundreds died.
  - Within a decade, Venice ordered lightning rods on every powder magazine, and later on its bell towers.
  - Last line: "The bells never broke a single bolt of lightning. They just called it in."
- **Camera travels through:**
  1. the village square in the storm;
  2. inside the belfry, with the rope and bells;
  3. the tower roof against the sky;
  4. Brescia's walls and the powder tower;
  5. the ruined quarter;
  6. a rod on a tower, with lightning running harmlessly down.
- **Why it should hit:**
  - S1: real, 1700s Europe.
  - S2: an odd act (climbing into the storm), with the reason at 2/3.
  - S3 and T1: physics, a lightning path you can see.
  - S4: a city at stake (Brescia).
  - S6: the rod is mocked, then vindicated.
  - S-env: six places.
  - T5: surprise 3. The ritual meant to protect them is what killed them.
  - T6: a "Why [group] ..." title stating a tension.
- **Verified facts:**
  1. **Ringing against storms.** Bells were rung during thunderstorms to drive lightning away. The 1486 bell of Schaffhausen Minster reads "Vivos voco, mortuos plango, fulgura frango".
     - Britannica: https://britannica.com/print/article/527011
     - University of Notre Dame (CurateND): https://curate.nd.edu/articles/figure/Imperial_Abbey_of_All_Saints_in_Schaffhausen_Cathedral_bell_Schiller_Bell_on_display/24728472
  2. **The German count.** Johann Nepomuk Fischer (Munich, 1784) counted about 386 towers struck and about 120 bell-ringers killed in Germany over 33 years.
     - French petition of the 1780s, Archives de la Meuse: https://archives.meuse.fr/media/6eb3ed70-a917-4620-82f4-4e09bf6e310d.pdf
     - A. D. White (1896), ch. XI: https://www.gutenberg.org/cache/epub/505/pg505.txt
     - **CONTESTED:**
       - The petition's scan reads "38" towers where the archive's editor gives 386, and the ringer figure is 120-121.
       - The "103 ringers" often quoted is an unsourced French figure. Don't use it.
       - Fischer's book itself was not read.
  3. **A ban.** The Parlement of Toulouse banned storm-ringing on 14 July 1786, citing "ringers crushed by lightning".
     - Études Héraultaises: https://www.etudesheraultaises.fr/wp-content/uploads/grec-art-2014-a06-sonneries-cloches.pdf
     - Archives de la Meuse (above).
     - A Paris ban is unconfirmed.
  4. **Brescia, 18 August 1769, about 4 a.m.** Lightning struck the powder tower on the San Nazaro bastion, which held about 234,800 Venetian *libbre* of powder (about 2,800 barrels, roughly 70-110 t).
     - Garbelli, *Le rovine di Brescia* (1771): https://archive.org/stream/lerovinedibresci00garb/lerovinedibresci00garb_djvu.txt
     - Gatta, *Civiltà Bresciana*: https://www.civiltabresciana.it/iniziative/2016/06-S_Nazaro-Rivellino.pdf
     - **CONTESTED death toll:**
       - Parish-register count about 308 (Garbelli); over 500 (Gatta).
       - The "3,000" in later English books is inflated.
       - Say "hundreds were killed".
       - 190 houses were destroyed (Garbelli). "A sixth of the city" is unsourced.
  5. **Rods after the disasters.** A Royal Society committee including Franklin recommended rods for the Purfleet powder magazine in 1772: https://founders.archives.gov/documents/Franklin/01-19-02-0157
     - The Venetian Senate ordered rods on all its powder magazines on 9 May 1778, and on bell towers in 1786: Bertucci, Yale 2009, https://hshm.yale.edu/sites/default/files/files/Bertucci2009.pdf
     - The Venetian orders rest on a *single scholarly source*.
     - The famous "heretical rod" phrase is **not supported**. Don't use it.
- **Coverage: clear.**
  - Not on the Ricks or Zack lists or in the big channels' Shorts.
  - Searches show only sound-effect bell Shorts and two small long-form videos ("They Rang Bells to Break the Lightning", 1.7K; "The Brescia Disaster", 1.4K).

## 6. Why Japan's Firemen Smashed the Wrong House (`story-edo-firemen`)

- **Paradox first line:** "When a house caught fire in Edo, the firemen ran right past it and tore down the house next door."
- **Story:**
  - A wooden city at night. A bell rings from the fire tower.
  - A brigade sprints in with hooked poles. Their standard-bearer climbs onto a roof that isn't burning, and twirls the brigade's *matoi* there.
  - The crew rips that house apart while its owner screams at them.
- **"You see" reveal (about 2/3):** "You see, Edo's pumps could barely throw water past the next roof, and you can't drown a fire in a wind."
  - What you can do is starve it. Tear down the houses in its path and the fire reaches a gap with nothing left to burn.
  - The roof where the *matoi* stood was the line the brigade claimed.
- **Ending (true):**
  - After the Great Meireki Fire of 1657, which burned about 60% of the city, the shogunate cleared wide firebreak streets and open lots, and built Ryōgoku Bridge across the Sumida.
  - The empty firebreak lots by the bridge became Edo's busiest entertainment district.
  - Last line: "Edo saved itself with empty space, and then filled it with a party."
- **Camera travels through:**
  1. a narrow Edo street at night;
  2. the fire watchtower;
  3. the rooftops with the *matoi*;
  4. the torn-down gap with the fire stalling;
  5. the Meireki inferno from above;
  6. the Sumida River and Ryōgoku Bridge;
  7. the festival crowd on the old firebreak.
- **Why it should hit:**
  - S1: real, Japan.
  - S2: a very odd act, with the reason at 2/3.
  - S3 and T1: fire physics (fuel, wind), shown in the place itself.
  - S4: a city at stake.
  - S6: the screaming owner, then the line holds.
  - S-env: seven places.
  - T3: East Asia.
  - T5: surprise 2. Firebreaks are half-known, so the "wrong house" framing carries it.
  - T6: the title names the role and hides the why.
- **Verified facts:**
  1. **Destructive firefighting.** Edo relied on it because equipment was poor; the hand pump (*ryūdosui*) couldn't throw water far. Crews tore houses down with hooked poles (*tobiguchi*).
     - Cabinet Office disaster report: https://www.bousai.go.jp/kyoiku/kyokun/kyoukunnokeishou/rep/1657_meireki_edotaika/index.html
     - Tokyo Fire Department: https://www.tfd.metro.tokyo.lg.jp/learning/elib/times/times01.html
  2. **The Meireki Fire (1657).** It started after more than 80 days without rain, in strong wind, and burned about 60% of the city.
     - Tokyo Metropolitan Library: https://www.library.metro.tokyo.lg.jp/portals/0/edo/tokyo_library/english/machi/page2-1.html
     - Cabinet Office (above).
     - **CONTESTED deaths:** estimates run from 30,000 to over 100,000. The Cabinet Office says 68,000+; the traditional figure is 107,046. Say "tens of thousands".
  3. **Rebuilding.** Firebreak streets (*hirokōji*) and lots (*hiyokechi*) followed. Ryōgoku Bridge was built in 1659 because of the fire, and its firebreak lots became an entertainment district.
     - National Diet Library: https://www.ndl.go.jp/landmarks/sights/ryogokubashi
     - Cabinet Office (above).
     - Flag: a 2021 book by Iwamoto Kaoru argues that the grand-remodelling story is partly myth: https://www.d-lab.kit.ac.jp/?p=14406
  4. **Town brigades and the *matoi*.** Town brigades (*machi-bikeshi*) were ordered in 1718 by magistrate Ōoka Tadasuke and organized in about 1720 into 47 "iroha" groups. The *matoi* was swung on a roof near the fire to show that the brigade had arrived and claimed the spot.
     - Tokyo Fire Department: https://www.tfd.metro.tokyo.lg.jp/learning/elib/qa/qa_03.html
     - Kotobank: https://kotobank.jp/word/町火消
     - "Where they made their stand" is popular framing. Say "claimed the spot".
  5. **The saying.** "Fires and quarrels are the flowers of Edo" (火事と喧嘩は江戸の花).
     - Kotobank: https://kotobank.jp/word/火事と喧嘩は江戸の花
     - Tokyo Fire Department: https://www.tfd.metro.tokyo.lg.jp/learning/elib/qa/qa_34.html
- **Coverage: clear.**
  - Not on the Ricks or Zack lists or in the big channels' Shorts.
  - Searches show only small Shorts on uniforms and drills (≤ 29K) and a long-form video, "Edo Was Built to Burn" (18K).

## 7. Why Lighthouse Lenses Look Broken (`story-fresnel-lens`)

- **Paradox first line:** "To make the lighthouse brighter, he threw away most of the glass."
- **Story:**
  - Ships keep breaking up on the rocks of the Gironde estuary.
  - The lighthouse burns oil lamps in front of polished metal mirrors, and still the light is dim.
  - Augustin Fresnel, a sickly road engineer, is told the cure is a bigger glass lens. Instead he slices one into thin rings and throws the middle away, and the experts are sceptical (dramatized).
  - Cordouan is lit in July 1823.
- **"You see" reveal (about 2/3):** "You see, a lens only bends light where it meets the surface. All that thick glass in the middle just adds weight and swallows light."
  - Keep only the curved surfaces as a ladder of rings of prisms, and you get a lens that is thin, light and brighter.
  - It also burned half the oil.
- **Ending (true):**
  - Fresnel died of tuberculosis in 1827, aged 39.
  - Within about thirty years, nearly every lighthouse in the United States had one of his lenses.
  - Last line: "He never saw most of the lights he made."
- **Camera travels through:**
  1. a ship in a storm off the rocks;
  2. Cordouan lighthouse standing alone in the estuary;
  3. the lamp room with its mirrors;
  4. Fresnel's workbench with glass rings;
  5. the beam sweeping across the sea;
  6. a chain of American coast lights coming on.
- **Why it should hit:**
  - S1: real, 1820s France.
  - S2: an odd act, with the reason at 2/3.
  - S3 and T1: optics you can watch bend.
  - S4: ships and crews at stake (a group).
  - S-env: six places.
  - T5: surprise 3. Less glass gives more light.
  - T6: the "Why [object] looks broken" tension title.
  - **Weaker on:** S6 (the ridicule is invented) and nation-scale stakes.
- **Verified facts:**
  1. **Dates.** Fresnel presented the lens to the Académie on 29 July 1822, and Cordouan's lens was operational from 25 July 1823.
     - Royal Society archive (Fresnel's letter to Young): https://catalogues.royalsociety.org/CalmView/rdf/catalog/MS/242/27
     - Cordouan (French Ministry of Culture): https://cordouan.culture.gouv.fr/en/cordouans-first-lens
     - One ministry page says 25 August; the Fresnel letter outweighs it.
  2. **The old reflectors** returned only about 50% of the light.
     - American Institute of Physics: https://www.aip.org/inside-science/the-remarkable-lens-in-americas-oldest-lighthouse-station
     - Publishers Weekly review of Levitt, *A Short Bright Flash*: https://www.publishersweekly.com/9780393068795
  3. **Range.** A Fresnel light was visible for more than 20 miles; earlier ones were generally under 10.
     - AIP (above).
     - Guinness World Records: https://www.guinnessworldrecords.com/world-records/717348-first-fresnel-lens-in-a-lighthouse
     - The "half the oil" claim (1.5 lb against 3 lb an hour) is from Fresnel's own letter only (*single primary source*).
  4. **His death.** Tuberculosis, 14 July 1827, aged 39.
     - Florida State University (Molecular Expressions): https://micro.magnet.fsu.edu/optics/timeline/people/fresnel.html
     - École des Ponts: https://ecoledesponts.fr/en/glory-fresnels
  5. **US adoption.** The US Lighthouse Board (1852) was told to fit Fresnel lenses, and nearly every US lighthouse had one by 1859.
     - National Park Service: https://www.nps.gov/articles/000/history-of-lighthouses.htm
     - Publishers Weekly (above).
  - **Don't claim:**
    - Shipwreck-reduction numbers (none found).
    - That Fresnel invented the stepped lens. Buffon proposed it in 1748, and Fresnel credited him.
- **Coverage: clear.**
  - Not on the Ricks or Zack lists or in the big channels' Shorts.
  - Searches show product clips and a HISTORY Short on one lighthouse (7.8K), but no Fresnel story.

## 8. Why Old Warships Had Copper Bottoms (`story-copper-navy`)

- **Paradox first line:** "Britain wrapped every warship in its navy in copper, and then the bolts holding the ships together started to vanish."
- **Story:**
  - Tropical worms are eating the Navy's hulls from the inside.
  - In 1761 a frigate is sheathed in copper. Two years later, no worms and no barnacles.
  - By 1782 the whole battle fleet is coppered, and faster. The First Lord boasts "Copper bottoms need fear nothing."
  - Then, in a dry dock, shipwrights pull out bolts that have rotted to needles.
- **"You see" reveal (about 2/3):** "You see, two different metals in seawater make a battery."
  - The copper sheet and the iron bolts underneath were wired together by the sea, and the iron was eaten away to protect the copper.
  - The fix was bolts of copper alloy, adopted from 1783 and fleet-wide by 1786.
- **Twist ending (true):**
  - Forty years later, the great chemist Humphry Davy used the same battery on purpose. He fixed lumps of iron to the copper so the copper would stop corroding.
  - It worked, but copper that doesn't dissolve doesn't poison anything, so on some ships weed and shellfish came back. The Admiralty dropped the idea in 1825.
  - Last line: "The copper only worked because it was being eaten."
- **Camera travels through:**
  1. a cross-section of a hull riddled by shipworm;
  2. the dockyard where the copper is nailed on;
  3. the battle fleet at sea, now faster;
  4. a dry dock with hollow bolt holes;
  5. Davy's laboratory and the test ship;
  6. a hull bearded with weed.
- **Why it should hit:**
  - S1: real, 1700s navy.
  - S2: an odd act, with the reason at 2/3.
  - S3 and T1: chemistry and physics you can watch (metal vanishing).
  - S4: a navy at stake.
  - S-env: six places.
  - T5: surprise 3.
  - T6: the title names the object and hides the battery.
- **Risk:** two mechanisms (galvanic corrosion, then the toxicity irony) in 60 s. Script the Davy twist in two lines at most.
- **Verified facts:**
  1. **The first coppering.** HMS *Alarm* was sheathed in October 1761. The Navy Board's report of 31 August 1763 found no worm or barnacles where the copper was intact. 82 capital ships were coppered by early 1782.
     - Staniforth (maritime archaeologist): https://navalmarinearchive.com/research/pdf/copper_sheathing_staniforth.pdf
     - Northover (Oxford metallurgist), ASM: https://connect.asminternational.org/discussion/history-is-written-by-the-winners-the-development-and-use-of-copper-sheathing-and-fastenings-by-the-royal-navy-from-the-1760s-onwards
  2. **The bolts.** Iron corrosion under the copper was seen by 1763 ("the bad effect that copper has upon iron"). Copper-zinc bolts were adopted in December 1783, and all ships were ordered to switch in 1786.
     - Staniforth (above).
     - Northover (above).
  3. **Davy's protectors.** Davy's papers were read to the Royal Society in 1824-25, with the first ship trial on the *Sammarang* in 1824. The Admiralty discontinued the scheme on 19 July 1825.
     - Institute of Corrosion: https://www.icorr.org/200-years-on-sir-humphry-davy-and-cathodic-protection/
     - Prof. Sharon Ruston (Lancaster), BARS: https://www.bars.ac.uk/blog/?p=4782
     - **CONTESTED:** how widespread the fouling was. The Sammarang stayed clean, and fouling showed where too much protector metal was fitted. Say "on some ships".
  4. **"Copper-bottomed"** (reliable) comes from the practice; the OED's first figurative use is from 1807.
     - World Wide Words: https://www.worldwidewords.org/qa-cop4.html
     - Phrase Finder: https://www.phrases.org.uk/meanings/copper-bottomed.html
  - **Don't claim:**
    - That HMS *Royal George* (1782) sank from corroded bolts. Rejected; her timbers were decayed: https://www.rmg.co.uk/stories/maritime-history/toll-brave-curious-sinking-royal-george
    - That *Ramillies* and *Centaur* foundered in 1782 from corroded bolts, unless it is hedged. Staniforth says so, but it is a *single source*.
- **Coverage: clear.**
  - Not on the Ricks or Zack lists or in the big channels' Shorts.
  - Searches show only a museum process clip (USS Constitution, 6.7K) and boat-anode explainers.

## 9. The Worm That Dug Under the Thames (`story-thames-shipworm`)

- **Paradox first line:** "He stared at a rotten piece of a ship for hours, and it showed him how to dig under a river."
- **Story:**
  - Every attempt to tunnel under the Thames has collapsed.
  - In Chatham dockyard, Marc Brunel watches a ship's timber bored through by shipworms, and patents an iron "shield" (1818).
  - The dig starts at Rotherhithe in 1825. Men in a honeycomb of 36 cells each shave a few inches of clay, then the frames are screwed forward, and bricklayers follow right behind.
  - The river breaks in twice. Six men drown in 1828, and his son Isambard barely escapes. Work stops for seven years, and London calls it a folly (dramatized).
- **"You see" reveal (about 2/3):** "You see, a shipworm never leaves its hole open."
  - Two little shell blades on its head grind the wood, and behind them it lines the tunnel with a hard shell tube.
  - Brunel's iron shield was the blades; the brick lining was the tube.
- **Ending (true):**
  - It opened on 25 March 1843, the first tunnel known to run under a navigable river, and a million people walked through it in ten weeks.
  - Trains still run through it today.
  - Last line: "A worm that eats ships built the road under them."
- **Camera travels through:**
  1. Chatham dockyard and the bored timber;
  2. the Rotherhithe shaft;
  3. inside the shield face;
  4. the river breaking in;
  5. the river above, with ships passing over;
  6. a train in the tunnel today.
- **Why it should hit:**
  - S1: real, 1820s London.
  - S2: an odd act, with the reason at 2/3.
  - S3 and T1: engineering you can watch, plus biology.
  - S4: a group (the workers) at stake.
  - S6: a folly, then vindicated.
  - S-env: six places.
  - T5: surprise 2-3.
  - T6: the title names the object and the world.
- **Verified facts:**
  1. **The patent and the worm.** Patent GB 4204/1818, Brunel with Thomas Cochrane. In a letter of 10 March 1842, Brunel recalled seeing worm-bored keel timber at Chatham around 1812.
     - Royal Museums Greenwich: https://www.rmg.co.uk/stories/blog/library-archive/musing-on-mollusc-brunels-inspiration-thames-tunnel
     - German Patent Office (DPMA): https://dpma.de/english/our_office/publications/milestones/inventionsthatmadehistory/theworldsfirstunderground/index.html
     - Flag: this is Brunel's own recollection 30 years later.
  2. **Build and opening.** Built 1825-1843 and opened 25 March 1843, the first tunnel known to have been built under a navigable river.
     - Grace's Guide: https://www.gracesguide.co.uk/Thames_Tunnel
     - London Museum: https://www.londonmuseum.org.uk/collections/london-stories/thames-tunnel-marc-brunels-engineering-marvel/
  3. **The floods.** The river broke in on 18 May 1827 and 12 January 1828. Six men drowned in 1828, Isambard was badly hurt, and work stopped for about seven years.
     - Linda Hall Library: https://www.lindahall.org/about/news/scientist-of-the-day/marc-isambard-brunel/
     - Brunel Museum (1828 newspaper report): https://thebrunelmuseum.com/newsclippings/another-serious-accident-at-the-thames-tunnel-and-loss-of-lives/
     - There is no reliable total death toll for the whole build.
  4. **The worm.** The shipworm's two small ridged valves grind wood, and the animal lines its burrow with a calcareous tube.
     - Smithsonian NEMESIS: https://invasions.si.edu/nemesis/panama/species_summary/81862
     - Australian NIMPIS: https://nimpis.marinepests.gov.au/species/species/42
     - Flag: the Brunel Museum's "excreted wood lining" is wrong.
  5. **Today.** It is still used by trains (London Overground, Windrush line), and one million visitors came in its first ten weeks.
     - London Museum (above).
     - Brunel Museum: https://thebrunelmuseum.com/online/visitors-to-the-thames-tunnel/
- **Coverage: clear.**
  - Not on the Ricks or Zack lists or in the big channels' Shorts.
  - Searches show small long-form videos only (≤ 25K), plus TED-Ed's long video on a different tunnel.

## 10. The Ancient Tunnel Dug From Both Ends (`story-eupalinos`)

- **Paradox first line:** "Two crews started digging into opposite sides of a mountain, and neither could see the other for a kilometre."
- **Story:**
  - Samos's only good spring lies on the far side of a mountain, and any besieger could cut the water.
  - The engineer Eupalinos of Megara sends one crew in from the north and one from the south, digging by lamplight for years.
  - Near the end the north tunnel suddenly zigzags, as if the crew were lost, and the workers grumble (dramatized).
- **"You see" reveal (about 2/3):** "You see, two straight tunnels aimed at each other can miss by a few metres and pass forever in the dark."
  - Bend both toward the same side near the end, and they have to cross.
  - This is one leading interpretation of the kink; hedge it on screen: "many engineers think".
  - The crews met, and the floors were off by only about 60 cm.
- **Ending (true):**
  - It carried the town's water for about 1,100 years.
  - About 700 years later, Roman engineers digging from two ends at Saldae, in Algeria, missed each other.
  - Last line: "The Greeks didn't aim better. They made sure they couldn't miss."
- **Camera travels through:**
  1. the walled town of Samos;
  2. the spring on the far side of the mountain;
  3. the mountain slope with two hidden entrances;
  4. the north tunnel by lamplight;
  5. the south tunnel;
  6. the meeting point;
  7. the water channel cut beside the level floor.
- **Why it should hit:**
  - S1: real, ancient Greece.
  - S2: an odd act, with the reason at 2/3.
  - S3 and T1: geometry you can watch from above.
  - S4: a city's water at stake.
  - S-env: seven places.
  - T6: the title names the object and the feat and hides the trick.
  - **Weaker on:** surprise (T5 = 2) and visible jeopardy. The trick is also only the leading interpretation.
- **Verified facts:**
  1. **The tunnel.** 1,036 m long and about 1.8 × 1.8 m, dug from both ends. Herodotus (3.60) names "Eupalinos son of Naustrophos, a Megarian".
     - Apostol, Caltech *Engineering & Science* 67/1 (2004): https://calteches.library.caltech.edu/4106
     - Greek News Agenda (Greek government): https://www.greeknewsagenda.gr/eupalinos-aqueduct-in-samos-island-open-to-visitors/
     - The Polycrates attribution is a scholarly inference.
  2. **The meeting error.** The floor drops about 60 cm at the junction (Apostol); Stiros gives about 50 cm vertically.
     - Apostol (above).
     - Stiros, *Survey Review* 41 (2009): https://www.eupalinos-tunnel.gr/uploads/1/2/2/2/12220305/orientation_and_alignment_of_the_5th_century_bc.pdf
     - There is no reliable horizontal figure. Don't use "4 cm".
  3. **Time and purpose.** The build took an estimated 8-15 years (Apostol; the Greek Tunnelling Society says 8-10). The aqueduct was kept underground so an enemy couldn't find and cut it, and it supplied the town for about 1,100 years.
     - Apostol (above).
     - Greek News Agenda (above).
  4. **The deliberate bend. CONTESTED.**
     - The Greek Tunnelling Society and Structurae describe deliberately angled headings, so the bores would cross even if they ran parallel: https://www.eupalinos-tunnel.gr/eupalinos-tunnel.html · https://structurae.net/en/structures/tunnel-of-eupalinos
     - Apostol says "No one knows for sure", and also suggests water seeps or soft rock as reasons.
  5. **UNESCO.** Part of "Pythagoreion and Heraion of Samos" (1992).
     - Greek News Agenda (above).
     - https://www.worldheritagesite.org/list/id/595
  - The Saldae miss is from Stiros (*single scholarly source*).
- **Coverage: clear.**
  - Not on the Ricks or Zack lists or in the big channels' Shorts.
  - Searches show only small Shorts (≤ 1.4K) and Caltech's long-form *Project MATHEMATICS!* episode (23K).

---

## Considered and dropped

- **Covered by Zack D. Films** (full 4,122-title list): Nijō nightingale floors (30M), Broughton bridge / break step (9.4M), Tudor's ice to India (16M), Venice's wooden piles (9.8M), miners' safety lamps (8.3M), and earthquake-proof Chinese temples (4.9M). The last overlaps the Japanese pagoda *shinbashira* idea.
- **Covered by history Shorts:** Mehmed's ships over the Galata hill, 1453 (Mapograph Short, 291K, plus many small ones).
- **Too contested to anchor a story:** Hannibal's vinegar on the Alpine rock (Livy), the south-pointing chariot's origin, and the Hakata wall vs the "divine wind".
- **Off-lane mechanism (T1/T2):**
  - Chappe telegraph stock hack, 1834: a con, in the same family as the Mirror race (4.6M).
  - John Snow's pump (biology, an invisible germ).
  - Mithridates and Lady Montagu (the body).
- **Kept as backups:**
  - Relief of Leiden, 1574: overlaps rank 3.
  - Halley's diving bell, 1690.
  - The Siege of Ambracia smoke-out, 189 BC (Polybius).
