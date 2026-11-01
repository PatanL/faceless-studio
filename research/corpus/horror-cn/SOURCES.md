# Chinese rules-horror / suspense-chat sources (horror-cn)

This is internal research. It maps the Chinese 规则怪谈 / 悬疑脑洞 / 沙雕 suspense animation genre to the English TTS-repost ecosystem, so we can learn what the niche rewards. **Never translate, retell or remix any story listed here for publication.** We study the premise mechanics, hooks, pacing and why each story travelled. Every story we publish is an original, transposed story that passes `scripts/originality_check.py`.

Built 2026-11-01, roughly 13:25 to 14:30 UTC. All work was metadata only, on the Spark CPU with `nice -n 10` and `CUDA_VISIBLE_DEVICES=""`. Nothing was downloaded and nothing ran on the Mac.

## Method

- **YouTube searches.** I ran yt-dlp `ytsearch40` with 12 Chinese queries: 规则怪谈 动画, 悬疑动画 公寓, 沙雕动画 悬疑, 胡说漫, 业主群 规则, 悬疑脑洞 动画, 规则怪谈 小区, 细思极恐 动画 合集, 悬疑漫画 业主群, 沙雕动画 规则怪谈, 懸疑腦洞, 规则怪谈 宿舍. I also ran 10 English searches and listed 7 channels (200 most recent uploads each).
- **Bilibili searches.** yt-dlp's `bilisearch` returns only bare ids, so I used Bilibili's public web search API with a homepage cookie, metadata only. That covered 14 genre queries sorted by plays, about 70 plot-keyword queries (one for each English repost hit), and uploader queries.
- **Bilibili per-video stats.** The space listing for 杰出影视本人 returned 421 of 471 videos before Bilibili answered with HTTP 412. I pulled stats for all 421 with the `x/web-interface/view` API at about 1 request per second, plus stats for 13 key videos.
- **Repost side.** The English repost data comes from R2: `research/R2/data/*.jsonl` (TikTok `user_*` with the 40 latest posts per account, YouTube `ytc_*`), and the transcripts in `research/library/transcripts/` and `research/corpus/horror/raw/`.
- **Matching.** I matched each repost to its source by premise: the hook line of the English repost transcript or title against the Chinese title. One check is that the Chinese upload has to come before the repost. Matches are graded:
  - **confirmed:** the premise and a distinctive detail line up (zoo dinosaur that calls the hero "dad"; the number 6; a 20th-birthday SMS; a killer reported in the complex plus a danmaku livestream).
  - **probable:** the premise lines up at title level only.
- **Raw data.** Everything is in `dgx-spark:~/studio/refs/horror-cn/meta/`:
  - `s_*.jsonl`: YouTube searches.
  - `bili_*.jsonl`: Bilibili searches.
  - `view_jiechu.jsonl` (421 rows) and `view_key.jsonl`: Bilibili per-video stats.
  - `ytc_*.jsonl`: YouTube channel listings.
  - `yt_en.jsonl`, `yt_extra.jsonl`: other YouTube searches.
  - Helper scripts: `bili.py` (search), `bview.py` (stats), `search.sh` (ytsearch), plus `agg.py`, `bagg.py`, `byq.py`, `top.py`.
- **Limits.**
  - I couldn't reach Douyin, which is probably where many of these studios post first. The Bilibili numbers are a lower bound on Chinese demand.
  - Bilibili rate-limits listings (412) after a few hundred requests. The 异常收录档案 space listing was blocked, so its catalogue comes from search results only (40 videos).
  - "Views" means Bilibili 播放 or YouTube view_count as of 2026-11-01. TikTok counts come from R2 and were scraped the same day.

## Headline findings

1. **The English "Chenjie stories" ecosystem is reposted from one Chinese Bilibili/Douyin studio: 杰出影视本人 (Bilibili mid 75872737), and its 【迷雾 X】 ("Mist X") series.**
   - The series started on 2025-03-31. 119 uploads since 2025 have a **median of 83.6K plays**; the biggest is 524.6K.
   - Every top lehwh7 TikTok I could check maps to one 迷雾 episode, and so do mraevq's dinosaur and "dad dragged me out" posts, the R2 seed, and most of twezed, It'sChineseSlop and ChenJie Horror.
   - The hero's name "Chen Jie" fits the studio's name (杰).
   - The Douyin credit "rlqfz123" that R2 mentions is still unverified. It is probably this studio's Douyin handle.
2. **The single biggest English repost spike traces to a second studio, 异常收录档案** (Bilibili mid 3461575153289625; on YouTube as 异常收录局 and 异常收录档案). Its "拦车孝" funeral-procession episode (740.6K, 2026-10-15) became udhwkz's 2.2M Part 1 sixteen days later.
   - The studio's Bilibili catalogue is far bigger than 杰出影视's: 7.4M, 3.3M, 2.9M, 2.8M and so on.
   - Few of those big stories have English reposts yet. That is the clearest sign of unexploited supply.
3. **English reposts often beat the Chinese originals in raw views.**
   - lehwh7 gets 2 to 10 times the Bilibili count on the same story, and udhwkz gets about 3 times.
   - Short-premise stories travel best: a monster at the door, a warning message, one rule, a loop.
   - The Chinese hits that are China-specific don't appear in English at all: Myanmar scam compounds, folk-religion items, parodies of 哆啦A梦 or 熊出没.
4. **One text story, several studios.** Many premises are adaptations of web fiction (知乎 / 番茄 short stories), and several studios animate the same one:
   - The killer-in-the-complex story: 杰出影视 (danmaku livestream version), 橘里漫剧 (hallway-song version, which is udhwkz's source), 胡说漫 (29-min version, 2026-06-17, 98 views).
   - The red bed-curtain story: 夏哭有点怂, plus at least 3 text readings.
   - The used mattress: 杰出影视 and 在下楚南.

   This is why "translate the Chinese story" is both a legal and an originality trap. The premise isn't the studio's own either. Our moat has to be original premises built on the proven mechanics.

## Chinese source channels

| Channel | Platform / id | Scale | Role in this niche |
|---|---|---|---|
| **杰出影视本人** | Bilibili mid 75872737 (471 videos) | 2025+ median 83.6K, max 524.6K (迷雾疑凶). Older 不自然博物馆 explainers reach 2.2M | **Source of the "Chenjie" repost ecosystem** (lehwh7, mraevq, twezed, It'sChineseSlop, ChenJie Horror, The Story Vault, HistoriasBizarras ES). 7–20 min single episodes; recurring hero; one-line "uncanny premise" titles. |
| **异常收录档案** | Bilibili mid 3461575153289625. YouTube: 异常收录局 UCeiJ-syU21RJTpsYGoZG0ww (max 1.4M), 异常收录档案 UCHmM6Tbq19DIyeW2Qe5cieQ (max 100K) | Bilibili hits: 7.41M 猴绳, 3.60M, 3.33M 我伪装夜盲症…, 1.51M + 1.32M 提前预知黑熊会进公寓杀人 (2 parts), 1.29M 深夜物业说要检查门窗, 1.27M 奶奶过寿那天，有人上门借7粒米, 0.74M 拦车孝 | **Source of udhwkz's 2.2M funeral procession.** Folk-taboo "你们知道X吗？" (did you know X?) openers, which is the "unspoken rules" hook. The biggest untranslated supply. |
| **Aoniao Lee's Horror Animations (李凹鳥怪談動畫)** | YouTube UCGaVdYnSnyKnadGLNQ83wag, 136K subs | 2.6M Zombie Campus; **548.7K 噩夢小區規則怪談 "Neighborhood Rules (Full Version)"** (2023-05-05) + 125.8K 2/2; 617K "don't open the door at midnight" | Original animator (轻漫计划), publishing to YouTube directly with bilingual titles. The "homeowner group warns: don't open the door to any neighbour" premise is the purest group-chat rules story in the pool. |
| 胡说漫 (Hushuo Man) | YouTube UCAYcZO5vo5UlNRJJEN40rKQ, 1.47K subs | Max 398K (a neighbour revenge story); the killer-in-the-complex video Qx_l91Oz7YI has 98 views | A late re-adaptation (2026-06-17) of the R2 seed premise, 8 weeks after 杰出影视. Mostly 爽文 revenge drama, not horror. Not the origin. |
| 橘里漫剧 | Bilibili BV1f9TF6DEEz | 18.4K (2026-06-30) | Hallway-song killer version of the seed premise (= udhwkz 376K, 2026-07-07). |
| 夏哭有点怂 | Bilibili BV1DbK563Eih | 53.6K (2026-07-16) | 诡夜红床 dorm-curtain rules story (= mraevq 194K, 2026-08-05). |
| 江不眠 / 我叫江不眠 | YouTube UCMbzFNvgFaUG3oIGVXgO9bg; Bilibili | 246K 春节列车规则怪谈, 128K, 127K | Short 规则怪谈 comics (11–14 min). 台风夜有人冒充我父母敲门 (someone posing as my dead parents knocks on a typhoon night) has 33K on Bilibili. |
| 麻吉先生 / 麻吉先生呀 | YouTube UCE_u7yfRcYXCLJ8mMgmM7Qg; Bilibili | 195.6K 噪音怪谈 (业主群 death warning for noise over 55 dB); Bilibili 2.43M; 52.6K 千万别开门 (业主群 + a DM warning) | Group-chat (业主群) warning premises. |
| 灵异讲述屋 | YouTube UCOwpEg1ZxMATJPrUGz0ep5w | 308K 凌晨宿舍规则 (anonymous 班级群 message rule) | Rule arrives through a class group chat. |
| 蛋泥动画 | YouTube UCqEf-Qgn1KKQq5b7MB8R1ag; Bilibili mid 435817645 | YouTube 667K 麦当劳夜班生存守则; Bilibili 4.5M | Job-rules ("night shift survival rules") 规则怪谈. |
| Bilibili 规则怪谈 mega-hits (context) | various | 不明电费 10.3M (无敌被窝); 封校凝云 8.2M (靓坤大人哦); 黑月公司 6.1M (猫me欢乐剧场); 高铁怪谈 5.9M (爆笑沙雕漫画); 凌晨宿舍的敲门声 5.6M (王大嗓门儿); 超市停电规则 2.6M; 说话超过50字者-嘎！ 2.6M (米花学姐) | Shows the scale of the domestic genre. None of these has a visible English repost. |

## English repost channels (from R2 data and new searches)

| Channel | Platform | Median / max | Main source | Notes |
|---|---|---|---|---|
| **lehwh7** | TikTok (YouTube mirror UCL9e-wgDpotrqg_0Qje3Pyg) | TikTok median 169K, max 1.9M; YouTube median about 16K, max 56.7K | 杰出影视本人 迷雾 | Full 7–16 min episodes; posts 2–10× the Bilibili count. |
| **udhwkz** | TikTok | median 34.9K, max 2.2M | 异常收录档案; 橘里漫剧 | Cuts episodes into 2.5–3.5 min parts and posts Part 2 first. |
| **mraevq** | TikTok | median about 7K (throttled since 23 Oct), max 717K | 杰出影视本人; 夏哭有点怂 | Mirrored footage. |
| melovebz | TikTok | median 5.7K, max 185K | not located (fake-human roommate + online exorcist) | |
| twezed | YouTube UCFdsJhEMtQ7tz4d6DgMBGWw | median about 13K, max 60.6K | 杰出影视本人 | 读心 → 24.7K, 蚂蚁 → 23K, 噬皮 → 15K, 宿管 → 36K (probable). |
| It'sChineseSlop | YouTube UCD-zwI3JWuIq7AlGJcB4D8Q | median about 11K, max 32K | 杰出影视本人 | 愿望 → 20K, 双眼 → 11K, 迷雾家人 → 32K (probable). |
| ChenJie Horror | YouTube UCGiyjv5TpEHrlaIvYVvdg_A | median about 7.8K, max 14K | 杰出影视本人 | 疑凶 → 12K, 卫衣 → 14K, 月饼 → 7.1K, 计时 → 6.2K. |
| The Story Vault | YouTube UCXOXwdDH46jWch0YHxZ0H0A | about 1K, max 19.8K | 杰出影视本人 | Compilations. |
| HistoriasBizarras | YouTube (Spanish) | 4K | 杰出影视本人 | Spanish dub of a dorm-killer loop. |

## The 10 strongest distinct source stories

Ranked by the evidence that the story crossed into English, then by Chinese demand. In the views column, "B" means Bilibili plays. "Repost multiple" is the best English repost divided by the Chinese source.

| # | Source story (CN) | CN channel, link, views, date | English repost(s), views, date | Match | Repost multiple | Mechanic to learn (not to copy) |
|---|---|---|---|---|---|---|
| 1 | **拦车孝**: never overtake a hearse convoy (funeral procession taboo) | 异常收录档案, [BV1TEJ164EHc](https://www.bilibili.com/video/BV1TEJ164EHc), **740.6K B**, 43K likes, 21:34, 2026-10-15 | udhwkz [Part 1](https://www.tiktok.com/@udhwkz/video/7702661541224566049) **2.2M** (164K likes) + [Part 2](https://www.tiktok.com/@udhwkz/video/7702661471641128224) 343K, 2026-10-31 | confirmed: premise, hearse convoy, night drive | 3.0× | A folk taboo stated in line 1, broken in the first minute; ritual repetition; 2-part cut with Part 2 posted first. |
| 2 | **磨牙怪**: teeth grinding at the door at 2 a.m., an online helper, two relatives who each accuse the other of being the shapeshifter, and a dream test | 杰出影视本人. The standalone episode was not in the listing I got. It is in the compilation [BV1qbL56CE74](https://www.bilibili.com/video/BV1qbL56CE74) 【怪物悬疑七部曲】 (41.8K B, 68 min, 2026-05-16) | lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7659482056656735521) **1.9M** (143K likes, 9:45, 2026-07-06); [YouTube tP5JPBvdMzg](https://www.youtube.com/watch?v=tP5JPBvdMzg) 21.8K | probable: the compilation title names 磨牙怪; hero, studio and repost channel all fit | n/a (standalone count unknown) | An anonymous online stranger as the warning channel; a two-suspect whodunit; a nested-dream reveal. The biggest lehwh7 post. |
| 3 | **小区闯入了杀人犯，我却能看见弹幕，原来这是一场直播秀**: killer in the complex, the chat says he's caught, a fake cop at the door, floating danmaku say he is the killer, and the hero is the star of a livestream (R2 seed) | 杰出影视本人, [BV1nEoYBBEXE](https://www.bilibili.com/video/BV1nEoYBBEXE), **151.7K B**, 7:21, 2026-04-23. Sister versions: 橘里漫剧 hallway-song version [BV1f9TF6DEEz](https://www.bilibili.com/video/BV1f9TF6DEEz) 18.4K, 2026-06-30; 胡说漫 [Qx_l91Oz7YI](https://www.youtube.com/watch?v=Qx_l91Oz7YI) 98, 2026-06-17 | mraevq [TikTok](https://www.tiktok.com/@mraevq/video/7654526047005723937) **717K** (2026-06-23); udhwkz [TikTok](https://www.tiktok.com/@udhwkz/video/7659677578365537569) **376K** (2026-07-07, from the 橘里漫剧 version) | confirmed | 4.7× | Group-chat all-clear → knock → a supernatural overlay contradicts the authority; count deduction; isolation; a burner phone. Our core T1 template. |
| 4 | **迷雾恐龙**: a dinosaur bred at the zoo knocks on the hero's door at night and calls him "dad" | 杰出影视本人, [BV1fR7szYEDq](https://www.bilibili.com/video/BV1fR7szYEDq), **230.5K B**, 10.3K likes, 7:47, 2025-05-31 | mraevq [TikTok](https://www.tiktok.com/@mraevq/video/7666044652910316833) **326K** (2026-07-24); lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7649861675100753185) **305K** (2026-06-10); lehwh7 YouTube [FiNl_v_Eswg](https://www.youtube.com/watch?v=FiNl_v_Eswg) 16.7K | confirmed: transcript hook | 1.4× (two reposts, 631K combined) | Absurd creature + door siege + phone call from a friend. Proves that 沙雕 absurdity travels when the door/knock frame is kept. |
| 5 | **迷雾伪行**: on his 20th birthday the hero gets an SMS saying he is not human | 杰出影视本人, [BV14EiCBdEUh](https://www.bilibili.com/video/BV14EiCBdEUh), **49.6K B**, 15:46, 2026-01-07 | lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7651280297169816865) **529K** (33K likes, 2026-06-14); YouTube [BCjSTd7cJxw](https://www.youtube.com/watch?v=BCjSTd7cJxw) 23K | confirmed: birthday + SMS + not human | **10.7×** | Unknown-number text as the warning channel; identity doubt. The largest English-over-Chinese multiple: phone-text premises travel. |
| 6 | **迷雾列车**: the hero gets stuck in a loop on a train | 杰出影视本人, [BV1WchTz9Ejt](https://www.bilibili.com/video/BV1WchTz9Ejt), **167.7K B**, 15:06, 2025-08-03 | lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7660648679811845408) "note says the train will crash in 2 minutes" **508K** (2026-07-09) + [TikTok](https://www.tiktok.com/@lehwh7/video/7649870481021062432) "The train full story" **347K** (2026-06-10); YouTube [3CM0hVUNm78](https://www.youtube.com/watch?v=3CM0hVUNm78) 24K | probable (title level) | 3.0× | Countdown note + loop with reset; each loop teaches a rule. |
| 7 | **迷雾沉睡**: don't fall asleep or you die | 杰出影视本人, [BV1oPbFzDEX6](https://www.bilibili.com/video/BV1oPbFzDEX6), **186.9K B**, 14:49, 2025-08-13 | lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7652341774991641878) "If you sleep you pass away" **486K** (2026-06-17); YouTube [bhLz-Kc9Hpg](https://www.youtube.com/watch?v=bhLz-Kc9Hpg) 22K | confirmed: premise | 2.6× | One survival rule in the title; a body-clock countdown. |
| 8 | **深夜老爸突然带我逃离小区，第二天小区住户就全部身亡**: Dad drags the family out at night, and everyone in the complex is dead by morning | 杰出影视本人, [BV1JhKP6FEjr](https://www.bilibili.com/video/BV1JhKP6FEjr), **53.6K B**, 18:45, 2026-07-18 (reupload by 张婷你可以的: 59.7K) | mraevq [TikTok](https://www.tiktok.com/@mraevq/video/7664930759395888416) **428K** (29K likes, 15:18, 2026-07-21) | confirmed: transcript hook | 8.0× | A parent's unexplained warning; a cold-open consequence (the whole complex dead), then the why. Only 3 days between source and repost, so both may come from an earlier Douyin post. |
| 9 | **迷雾疑凶**: a slip of paper in a dumpling warns "the killer is coming" | 杰出影视本人, [BV1dbwuz3EvY](https://www.bilibili.com/video/BV1dbwuz3EvY), **524.6K B** (30.6K likes, 19:00, 2026-03-15) + short cut [BV1dbwXzcEAM](https://www.bilibili.com/video/BV1dbwXzcEAM) 146.7K | ChenJie Horror [vrk6RQ11W6M](https://www.youtube.com/watch?v=vrk6RQ11W6M) 12K (78-min YouTube compilation); no TikTok repost seen | confirmed | 0.02× (YouTube only) | **The studio's biggest Chinese hit and a pure door-siege premise, but under-reposted.** A good model for a warning-note hook. |
| 10 | **诡夜红床**: the roommate buys red bed curtains, and the dorm supervisor says the roommate isn't human and hands over protective rules | 夏哭有点怂, [BV1DbK563Eih](https://www.bilibili.com/video/BV1DbK563Eih), **53.6K B**, 13:35, 2026-07-16 (the underlying 知乎-style text story has several readings, such as BV1ZjySYHEhh) | mraevq [TikTok](https://www.tiktok.com/@mraevq/video/7670495663624408352) **194K** (14K likes, 2:55, 2026-08-05; outlier 18×) | confirmed: transcript hook | 3.6× | Authority hands out rules → every rule backfires → the authority is the predator. The only 3-minute single-part rules story in the set. |

### Runners-up (also verified, weaker or off-genre)

- **迷雾床垫**: a used mattress lets him dream the future. 杰出影视 [BV1kGVozmEMh](https://www.bilibili.com/video/BV1kGVozmEMh) 150.9K (also 在下楚南 怪诞床垫 136K) → lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7656867469151276321) 403K.
- **迷雾南极**: a New Year trip to Antarctica, and another "me" is at home. [BV1vfAnz5Edm](https://www.bilibili.com/video/BV1vfAnz5Edm) 69.6K + recut [BV1VSD1B5Eg5](https://www.bilibili.com/video/BV1VSD1B5Eg5) 99.8K → lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7652871597438635296) 377K, YouTube [oQIBqUenPoM](https://www.youtube.com/watch?v=oQIBqUenPoM) 36K.
- **迷雾数字**: Dad fears the number 6. [BV1yV43z4Eyf](https://www.bilibili.com/video/BV1yV43z4Eyf) 83.6K + recut [BV1U4XrB8EGP](https://www.bilibili.com/video/BV1U4XrB8EGP) 335.7K → lehwh7 YouTube [CQKPC9MlciE](https://www.youtube.com/watch?v=CQKPC9MlciE) 51K (lehwh7's best on YouTube).
- **迷雾借寿**: a roommate's banknote. [BV1cVpAzDEit](https://www.bilibili.com/video/BV1cVpAzDEit) 17.6K → lehwh7 [TikTok](https://www.tiktok.com/@lehwh7/video/7659082311312477472) 318K (18×).
- **噩夢小區規則怪談 "Neighborhood Rules"** (Aoniao Lee): [vPk0lY7wi1g](https://www.youtube.com/watch?v=vPk0lY7wi1g) 548.7K + [GVW589k-CT0](https://www.youtube.com/watch?v=GVW589k-CT0) 125.8K. No English TTS repost found, but it already reaches non-Chinese YouTube with bilingual titles. **The most on-genre premise:** a group-chat rule against opening the door to neighbours.
- **深夜物业说要检查门窗**: property management says it will check doors and windows at night, but the community has no property management. 异常收录档案 [BV1Br421W72S](https://www.bilibili.com/video/BV1Br421W72S) 1.29M + parts 2–3 on YouTube. No English repost found. A fake-authority-at-the-door premise with seven-figure Chinese demand.
- **提前预知黑熊会进公寓杀人**: foreknowledge that a black bear will break into the apartments. 异常收录档案 [BV1Sc2mY6EyY](https://www.bilibili.com/video/BV1Sc2mY6EyY) 1.50M + part 2 1.32M; YouTube [hVyXj65e-Vs](https://www.youtube.com/watch?v=hVyXj65e-Vs) 748K. No clear English repost found. twezed's "A Bear With Human Intelligence Is Hunting Me" (22K) may come from 杰出影视's 迷雾熊爸 instead.
- Other 杰出影视 → English pairs: 迷雾读心 [BV1kqZ8YGEzM](https://www.bilibili.com/video/BV1kqZ8YGEzM) 114.9K → twezed [-NOl0PDpITU](https://www.youtube.com/watch?v=-NOl0PDpITU) 24.7K; 迷雾蚂蚁 168.6K → twezed 23K; 迷雾愿望 161.6K → It'sChineseSlop 20K; 迷雾电梯 41.7K / 85.6K → lehwh7 YouTube 24K; 迷雾人鱼 151.1K → lehwh7 YouTube 22K.

### Not yet traced

These are sources still to find:
- udhwkz trucker rules (695K)
- udhwkz elevator propane-tank "polite question" (613K)
- udhwkz roof/grandma (623K)
- melovebz fake-human roommate (134K)
- lehwh7 "keep silent aliens" (230K), "mountain demon in dorm" (216K), "Wang Qiang says my gf is a zombie" (217K)

The udhwkz ones are probably 异常收录档案 episodes. Its Bilibili space listing was blocked (412), so that is the next thing to retry.

## What this says for our niche

- **Demand is real and crosses cultures.** Ten Chinese stories with a combined about 2.2M Bilibili plays became about 8.7M English TikTok views across 13 reposts. The English multiple is highest (8–18×) on phone/text or parent-warning premises, and lowest on story-dense whodunits.
- **What travels:**
  - A one-sentence uncanny premise in the title or first line: a rule, a warning text, a knock, a countdown.
  - A small cast in a home, dorm or vehicle.
  - Rules and warnings delivered through a phone channel: SMS, group chat, danmaku, an online stranger.
  - A reveal that flips an authority figure.
- **What doesn't travel (no reposts seen):**
  - China-specific social satire.
  - IP parodies (哆啦A梦, 熊出没).
  - 爽文 revenge drama.
  - Multi-hour "无限流" sagas.
- **Supply gap.** 异常收录档案's 1M+ stories and Aoniao Lee's group-chat rules stories have little or no English TTS coverage, while the 杰出影视 catalogue is already mined by more than 6 channels. That still doesn't make reposting OK. It means **English-native originals in the 异常收录档案 folk-taboo register and the Aoniao Lee group-chat register are the least crowded lanes.**
- **Originality reminder.** Many of these premises are themselves adaptations of web fiction, with several studios animating each one. For each study story, we extract the mechanic: the warning channel, the fake-authority tell, the rule that backfires, the loop reset. Then we invent a new place, cast, rule and twist. Run the originality gate against `research/corpus/` before anything is scripted.
