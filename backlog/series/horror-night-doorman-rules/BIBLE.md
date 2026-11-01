---
id: horror-night-doorman-rules
kind: series bible
niche: horror
series_title: Night Desk Rules
parts: 5
runtime_target_s: {part1: 82, part2: 82, part3: 80, part4: 86, part5: 88}   # each 60-90 s; estimates, measure with TTS later
format: 9:16 narrated first-person story (Lena), phone-chat inserts, rule cards, flat puppets
voice: af_heart about 1.35x for Lena and every chat bubble she reads; bm_george about 1.05x for THE VOICE only (from Part 3 on)
wpm_target: 230-270 overall (PLAYBOOK §7, narrated story band)
supersedes: backlog/horror/horror-night-doorman-rules (2 x ~115 s draft). This bible re-cuts the same world into 5 parts of 60-90 s. The draft's cast, building, six rules (lines.py RULES, verbatim) and its identity model are kept; its scene builders (build.py desk_phone, keyboard, lobby, elevator_view, hallway_1903, cctv_grid, paper, count_track) are the prop source when the parts are built. The draft files are not edited.
revision: 2026-11-01 series-editor pass (scores and reasons in review.json). Fixed: sequel hooks cut to ≤ 14 spoken words (≈ 3 s); P2 and P4 cuts strengthened so each cliff outranks the last; rule-3 loophole in P4 made explicit so 6/6 still lands on rule 3 in P5; 3:04 log line replaced by an empty time box; Pell's fake number tied to the 1903 line; 2:41 made the nightly call minute; 96 hooks / 95 keys explained.
references:
  - id: 7702661541224566049
    url: https://www.tiktok.com/@udhwkz/video/7702661541224566049
    views: 2200000
    outlier_score: 63.13
    short: HEARSE-P1
    role: Part-1 skeleton; series plants; post order
  - id: 7702661471641128224
    url: https://www.tiktok.com/@udhwkz/video/7702661471641128224
    views: 343100
    outlier_score: 9.85
    short: HEARSE-P2
    role: sequel mechanics (no recap, plant paid at ~45%, outside check, diagnosis cut) and the 16% sequel decay we design against
  - id: 7692268145888873760
    url: https://www.tiktok.com/@udhwkz/video/7692268145888873760
    views: 694900
    outlier_score: 19.94
    short: TRUCKER-RULES
    role: job-rules engine ("taught me the rules, tonight I broke them"), two alternating ladders
  - id: gDNMSoGSZgQ
    url: https://www.youtube.com/shorts/gDNMSoGSZgQ
    views: 19845
    outlier_score: 19.84
    short: DOG-RULE
    role: 60 s narrated-Short timing (rule in 3.7 s, broken by 10 s, 2 s jolts, protector's voice as the lure)
  - id: shTJ7_kRNJ8
    url: https://www.youtube.com/watch?v=shTJ7_kRNJ8
    views: 3201
    outlier_score: 7.59
    short: NIGHT-BUS
    role: one rule per chapter, pre-announced failure rule, title rule re-read with one added clause (T17)
  - id: cVUJmsVkUW4
    url: https://www.youtube.com/watch?v=cVUJmsVkUW4
    views: 290919
    outlier_score: 30.95
    short: MOM-NOTE
    role: episode-count stakes as the series CTA; its hookless "Pt2" re-cut xKgepVHATm4 (1.0x) vs the urgent-hook sibling BciSW_2VMZg (11.0x) is why every part opens like a pilot
---

# Night Desk Rules: series bible (5 parts)

## 1. Logline

On her first night alone on the front desk of the Calloway, a 24-floor residential tower, Lena inherits six rules from a night man she never met, and by 7 a.m. she has broken all six, because the apartment the rules swear is empty keeps calling the desk, and every voice telling her to come up sounds like someone she should trust.

**Series promise (said in Part 1, line 2, and carried by the title card of every part):** six rules, one night, all six broken. The rule tracker (`RULES BROKEN n/6`) is the progress bar the viewer binges toward (MOM-NOTE cVUJmsVkUW4 episode-count stakes, PLAYBOOK §5 "Label"; NIGHT-BUS shTJ7_kRNJ8 one-rule chapters, §1C).

**Why this premise** (PLAYBOOK §8 premise boxes): an ownable rule the viewer can count against (rule 3, "1903 is empty"); a barrier the viewer knows (a desk phone line, an elevator, a door ajar); a human-shaped threat (a man in the night man's blazer who uses his voice, PLAYBOOK §6 TWO-WINDOWS kJCVK8xTkPk vs PIGEONS FDLk6TlVTq0); a fake authority in the phone (the "owner" contact, T1, SIEGE-CHAT 7659677578365537569). It is the TOPICS.md #1 pick on the strength of TRUCKER-RULES 7692268145888873760 (19.9x) and HEARSE-P1 7702661541224566049 (63.1x).

## 2. Recurring characters

The horror kit has two puppet specs (`studio/src/kits/horror/characters.tsx`): **Protagonist** (round head, the NORA spec) and **Neighbour** (long head, the HALE spec, also registered as `horror/Stranger`). Both take `expr`/`exprs`, `pose` (`idle | phone | ear | cover | sit`), `light` (`none | phone | red`), `silhouette`, `glitch` and a `colors` override. Every expression below is a key of `EXPRESSIONS` in that file. Nothing in the kit needs to change for this series; recolours go through the `colors` prop in the storyboard.

| Character | Who | Puppet + colours | Expression set (kit names) and when each is used | Poses / light | Rules for the character |
|---|---|---|---|---|---|
| **Lena** (narrator) | 24, first night on the desk, took the job for the overnight rate; dry, counts things when scared | `horror/Protagonist`, `colors.top #26324a`, `topShade #1c2538` (navy desk blazer); brass name badge as an SVG layer | `neutral` (setup), `suspicious` (reading a rule, a wrong number), `worried` (waiting, typing), `scared` (a sound behind her), `shocked` (each count match, each reveal), `terrified` (peak images only, once per part), `relieved` (fake calm, max once per part), `angry` (refusing the owner, Part 3) | `phone` (default, reading chat), `ear` (desk handset, Part 3-4), `cover` (stifled reaction after the peak), `sit` (Part 5 hallway floor); `light: phone` in the lobby, `light: red` whenever line 1903 is lit | Reads every chat bubble aloud as "Gus: ...". Never says "kid". Her right hand is the Part-2 plant (the key appears in it). |
| **Gus Brandt** (the real night man) | 31 years on the Calloway night desk; went up to 1903 at 2:41 last night and never signed out | `horror/Neighbour`, default colours (burgundy top `#5b2c35` reads as a concierge blazer), brass badge "G. BRANDT" layer | On screen only in the staff photo on the paper staff sheet (`smile`, Part 2-3) and in alternate ending B (`sad`, then `neutral`). Everywhere else he is **only a chat**: short imperatives, no emoji, no "kid" | `idle` in the photo; in ending B `idle` with `light: red` | Every chat order protects her (shut the door, let it ring, don't touch it, don't go up, don't listen to it). "I'm home in bed" is a protective lie, admitted in Part 4. |
| **The Voice / the man in the blazer** | the thing in 1903; wears Gus's blazer and voice | `horror/Neighbour`, same colours as Gus, **always** `silhouette: true` or seen from behind facing a wall; `glitch` cues on each line | `stare` (every spoken line: the kit's unblinking, barely-moving-lips face, `talkAmp 0.3`), `blank` (CCTV tiles), `grin` (used **once in the whole series**, alternate ending C only) | `idle`, `light: red`; never `phone` | The only speaker who says "kid" (re-watch clue, never stated). Speaks through the desk speaker (Part 3), the elevator (Part 4), and face-to-wall on 19 (Part 4-5). Never turns around on screen in the canon ending. |
| **"Mr. Pell"** (the owner contact) | a contact saved as the building owner; the number is wrong | never on screen: a grey contact avatar "P" and blue chat bubbles | none (text only) | none | Texts from 555-0143, which the paper staff sheet lists as the **disconnected 1903 line**; the same sheet lists the owner as 555-0178 (Part 2 on-screen plant, paid Part 3). Rule 5 is real; the thing in 1903 is texting under the owner's name. |
| **Marcus** (day shift) | the 7 a.m. desk man | `horror/Neighbour` recoloured: `colors.top #4a5058`, `topShade #3a3f46`, `hair #6a5a48`; seen from behind or at distance so the shared long-head spec never reads as Gus | `neutral`, `surprised` (finds the desk empty), `worried` (ending B) | `idle`, `phone` | Named in Part 1 ("the day man, Marcus, at seven") so the Part 5 handover needs no setup (DOG-RULE gDNMSoGSZgQ "protector named as the next arrival", 0:41). |

**Props shared by all parts** (built as SVG layers in each part's build script, reusing the draft's builders; not kit files): the work phone with the **Desk Handover** chat (Gus + Lena), the desk phone with a row of line buttons and **1903 under old yellow tape**, the key board (96 numbered hooks, 95 keys), the visitor log (paper, ruled), the paper staff sheet (photo of Gus, phone numbers), the CCTV monitor (4 tiles: lobby, elevator car, 19 hallway, garage), the elevator floor indicator, the desk clock, and the rule tracker card. Red is reserved for line 1903, rule stamps and the peak images (DOG-RULE gDNMSoGSZgQ visual grammar, §2).

## 3. The rule system and how it escalates

The six rules are stated **verbatim** every time they appear, copied from the draft's `lines.py`. On-screen rule cards are always the full rule; narration may quote a verbatim *fragment* ("nineteen-oh-three is empty", "do what he says"), never a paraphrase:

1. Never open the glass doors after 1.
2. If the elevator comes down empty, don't get in.
3. If 1903 calls, send nobody up. 1903 is empty.
4. At 3, count the keys. 95. If there's a 96th, don't touch it.
5. If Mr. Pell, the owner, texts you, do what he says.
6. Never leave the desk before 7.

**World facts the rules rest on** (keep fixed in every part): 24 floors x 4 apartments = **96 hooks** on the key board; **95 keys** because 1903's key went up with Gus last night and never came back (rule 4's "96th" is that key returning). 1903 calls the desk **every night at 2:41** (Gus's log line, P2; tonight's call, P1 cut). Rule 5 is genuine; the "Mr. Pell" texts come from **555-0143, the disconnected 1903 line** printed on the staff sheet, while Pell's real number is 555-0178. A rule is stamped broken only when Lena herself breaks it (rule 4 in P2 counts: her hand did it).

**Escalation = rule closeness** (PLAYBOOK §4A, TWO-WINDOWS kJCVK8xTkPk): each part's rule moves the threat one step nearer to Lena's body.

| Part | Clock | Rule broken (tracker) | Where the threat is | Ladder that runs it |
|---|---|---|---|---|
| 1 | 00:50-02:41 | **1** (glass doors) → 1/6 | the street, then the shaft (empty car comes down from 19) | proximity: street → lobby → elevator |
| 2 | 02:41-03:05 | **4** (the 96th key ends up in her fist) → 2/6 | the board behind her, then her own hand | count ladder (rings, keys) → body |
| 3 | 03:05-03:40 | **5** (she refuses the owner) → 3/6 | her phone (the owner), the desk speaker (the voice), the car riding down | channel removal: chat → owner → speaker |
| 4 | 03:40-04:20 | **6** (leaves the desk) and **2** (gets in the empty car) → 5/6; rule **3** dodged on a technicality ("Nobody sent me. I went.") | inside the car with her; then 19 | proximity: car → mirror → hallway |
| 5 | 04:20-07:00 | **3** (sends somebody up: herself) → 6/6 | the door of 1903; then the desk she left | barrier: door ajar → key → handover |

**How the rules themselves escalate (one new rule behaviour per part, so the system never stands still):**
- Part 1: a rule is broken **before it is read** and the building answers within seconds (HEARSE-P1 7702661541224566049, window rule broken 0:31, stated 0:36). Lesson for the viewer: the rules are real.
- Part 2: a rule is broken **without her choosing** (the key is in her hand). Lesson: the rules can be broken for you.
- Part 3: **two rules collide** (5 says go up, 3 says nobody goes up) and the collision is resolved by evidence, not by a rule (the number is wrong). Lesson: a rule's *source* can be faked (DORM-RULES 7670495663624408352, two rival authorities, T3).
- Part 4: she breaks two rules **on purpose to save the rule-writer** (Gus is up there), and talks her way round the third out loud: "Rule three said send nobody up. Nobody sent me. I went." (TRUCKER-RULES 7692268145888873760 hubris rule, 0:25). Lesson: the rules were written to protect *her* from what Gus did. This line is required: without it, riding up to 19 breaks rule 3 in P4 and the series' pre-announced last stamp is spent a part early.
- Part 5: the P4 loophole collapses. Every channel that night was *sending* her up (the log in her handwriting, "Pell" from the 1903 line, the voice in the car): 1903 calling *was* the sending, so rule 3 was broken the moment she obeyed it; the stamp lands at the twist. Then rule 3 is **re-read with one added clause** (T17, NIGHT-BUS shTJ7_kRNJ8; TWO-WINDOWS kJCVK8xTkPk at 98%): "send nobody up" was never about keeping guests safe; whoever goes up becomes the one who calls down. The series ends with the rewritten rule: *"3. If 1903 calls, send nobody up. Even if it sounds like me."*

**Pre-announced failure** (NIGHT-BUS shTJ7_kRNJ8, PLAYBOOK §1C): Part 1, line 2 says "rule three was the one that mattered", so the viewer counts toward rule 3 for five parts, and it is the last stamp of the series.

## 4. Series mechanics we use (PLAYBOOK §5) and the cliffhanger chain

**Mechanics, each mapped to its source:**
- **Every part is a pilot.** Sequel decay is steep: HEARSE-P2 7702661471641128224 got 16% of HEARSE-P1; WrONG Rules' hookless "Pt2" xKgepVHATm4 got 1.0x while its urgent-hook sibling BciSW_2VMZg got 11.0x. So every part opens with a **complete premise in ≤ 3 s** (PLAYBOOK §5): **≤ 14 spoken words** (≈ 3.0 s at the measured 4.7 words/s), a rule or place, and its contradiction landing by ~2.5 s, plus **one fact the previous part did not have**, so binge viewers are re-hooked by news, not by a recap of the frame they just saw (BciSW_2VMZg urgent sequel hook 11.0x vs hookless xKgepVHATm4 1.0x, PLAYBOOK §6). No recap, no "last time" (HEARSE-P2's no-recap cold open), but unlike HEARSE-P2 (hard hook at 0:20) the danger is in line 1.
- **Re-hook = the previous part's last image.** Frame 0 of part N+1 is the last frame of part N, re-framed (bookend, PLAYBOOK §4C: HEARSE-P1, CLASSMATE-PSA omuJBFs2L6c, HOTEL-DOOR Qz-TrB6W2SM). Binge viewers get continuity; cold viewers get a cover frame that shows the threat (§6 bottom line).
- **Plants:** ≥ 2 unpaid specifics per part; one is paid by ~45% of the next part, then a bigger loop opens within ~5 s (HEARSE-P2 plate 1574 at 1:28-1:29, 46%; PLAYBOOK §4B "close one, open a bigger one").
- **Cut point:** each part ends on a **new imperative** from a channel (chat, owner, voice), optionally followed by the rule it collides with (P2), never mid-sentence. **Each cliff must outrank the one before** on three counts: who gives the order (protector → fake authority → the threat in the protector's voice → the threat face to face → the threat inside the viewer's phone), how close the threat is to her body, and what obeying costs (the udhwkz control 7696062340852190496 cut mid-sentence with no part label at 0.77x). Loops from the first half get closed in that half; anything opened in the second half is left hanging for the next part (PLAYBOOK §5). 3-6 open at each cut.
- **Label:** title "(Part N/5)" plus the rule number in the title; end card `PART N/5 · RULES BROKEN n/6` (MOM-NOTE cVUJmsVkUW4 day-count stakes; anthology-style rule numbers make each part findable alone, TWO-WINDOWS kJCVK8xTkPk "file 017").
- **Post order:** Parts 1 and 2 go up together, Part 2 first and Part 1 about 10 s after it, which leaves Part 1 as the top tile of the profile grid (udhwkz posted HEARSE-P2 9 s before P1). Parts 3, 4, 5 follow one per day at the same hour. After Part 5, a **"full story" compile** (~6.5 min, all five parts, one "the end" card) as its own upload (FAKE-ROOMMATE 7650872317119057168 23.8x, TWO-SUSPECTS 7659482056656735521 11.2x).
- **Bingeable tags:** recurring character tags on every part (#NightDeskRules #Room1903 #GusTheNightMan), the mraevq repost-account practice (PLAYBOOK §5).

**The cliffhanger chain** (exact last line and last image of each part; exact first 3 s of the next):

| Seam | Last line of part N | Last image of part N (held ≥ 1 s, then end card) | Ending type (PLAYBOOK §4C) | First 3 s of part N+1 (spoken, ≤ 14 words; the new fact in bold) | Frame 0 of part N+1 | Source of the device |
|---|---|---|---|---|---|---|
| 1 → 2 | Gus: "Let it ring." | ECU of the desk phone: line **1903** lit red under the yellow tape; rule-3 bubble on the work phone behind it | 1. hard cut at greatest need + fresh imperative | "Rule three: nineteen-oh-three is empty. It rang my desk anyway. **Nineteen times.**" | the same ECU, LCD "LINE 1903 · CALLING", desk clock 2:41 | HEARSE-P1 7702661541224566049 bookend cut (3:16-3:21); SIEGE-CHAT 7659677578365537569 cliff on an imperative (4:05-4:08) |
| 2 → 3 | "Rule five: do what he says. Rule three: send nobody up." | her fist with the 96th key (tag 1903) under the phone: **Mr. Pell: "Bring the key to 1903. Now."**, rule 5 and rule 3 cards split left/right | 2. new order from a new authority, set against a second rule (T3 rule clash) | "The owner ordered me up to the empty apartment. **His texts came from it.**" | Pell's bubble over the key tag | DORM-RULES 7670495663624408352 new rule from a new authority; H3 official order undercut by 11 s (SIEGE-OVERLAY 7654526047005723937) |
| 3 → 4 | The Voice, from the open car: "Get in, kid." | lobby, the elevator doors open on an **empty, lit car**, floor indicator "L", button 19 already lit | 1. imperative from the threat, wearing the protector's voice | "The elevator came down empty. Rule two: don't get in. **Gus's voice: get in.**" | the same open car, 19 lit | DOG-RULE gDNMSoGSZgQ protector's voice as the lure (0:56-0:59); T1 fake authority |
| 4 → 5 | The man in the blazer, without turning, one hand held out backwards: "You brought my key, kid. Give it here." | 19th-floor hallway, 1903 open a crack, a man in a burgundy blazer facing the wall beside it (silhouette), his open palm toward her, the key in her raised fist foreground | 5. threat turned on "you" + imperative from the threat at arm's length | "Nineteenth floor. A man in Gus's blazer, facing the wall, **asked for my key.**" | the same hallway, one step closer | TEXT-FIGURE T42u5xhrq-0 threat turned on "you" (S10); HOTEL-DOOR Qz-TrB6W2SM door ladder |
| 5 → end | (canon) the handover chat, now from Lena: "3. If 1903 calls, send nobody up. Even if it sounds like me." | the work phone at the empty desk: "Lena added Marcus to Desk Handover", six rules stacking, rule 3 rewritten; line 1903 lights red behind it | 2 + 10. new rule from a new authority, threat moves into the viewer's phone; ring structure with Part 1 frame 0 | (season 2 or the compile) | — | NIGHT-BUS shTJ7_kRNJ8 / TWO-WINDOWS kJCVK8xTkPk title rule re-read with one clause (T17); PLAYBOOK §4C ring structure |

**Plant and payoff ledger** (each plant is a hyper-specific number, colour or object, PLAYBOOK §4A):

| Plant | Planted | Paid | How |
|---|---|---|---|
| "How did Gus know the door was open? He isn't in the building." | P1 ~55% | P2 44% | the visitor log: Gus went up to 1903 at 2:41 last night, no sign-out |
| The empty car came down from 19 with **19** already lit | P1 ~40% | P3 ~75%, P4 ~60% | the car rides down for the voice; in P4 it takes her up without a button press |
| **19** rings | P2 13% | P5 ~45% | 1903 has called the desk every night; 19 rings is the count Gus wrote on the sheet's margin |
| Owner's real number **555-0178** and "1903 · line disconnected · **555-0143**" on the paper staff sheet (on screen only, 2 s) | P2 ~44% | P3 ~40% | Pell texts from 555-0143: the texts come from the empty apartment; "neither rule was wrong; the number was" |
| Log line in **Lena's handwriting** with an **empty time box**: "__:__ 1903 called. Going up myself." | P2 85% | P4 ~55% | as she decides, she checks the log: the box now reads 4:12, the minute on the desk clock; she goes |
| The key in her right hand, palm soaked | P2 73% | P5 ~60% | the key fits 1903 from the hallway side: it locks, it doesn't open |
| Gus: "I'm home in bed." | P2 58% | P4 ~45% | she dials his cell from the staff sheet; line 1903 lights: his phone is upstairs |
| Only the voice says "kid" | P3 88% | P5 (never stated) | re-watch clue for the comments |
| Marcus at 7 | P1 ~20% | P5 92% | he is the next name on the handover chat |
| Tonight's call at **2:41** (desk clock, P1 cut / P2 shot 2) = Gus's log minute | P1 ~95%, P2 ~44% | P5 lore | 1903 calls every night at 2:41; Marcus's first night will get the same call |
| "Nobody sent me. I went." (rule-3 loophole) | P4 ~58% | P5 ~50% | the loophole collapses: 1903 calling was the sending |

## 5. Per-part beat outlines

Runtime targets are estimates at the draft's measured Kokoro rate (about 282 wpm speaking, 230-245 wpm overall with holds). The beat tags are PLAYBOOK §1A (B1-B12, the story skeleton compressed into 60-90 s) with Shorts cadence from §1B/§3: a jolt every 2-4 s (DOG-RULE gDNMSoGSZgQ median 2 s), no dry stretch over 6 s except the one held peak image (~4 s, silence + heartbeat).

### Part 1/5: "Rule 1" (target 82 s)
Title: *My Night Desk Has 6 Rules. Rule 3 Says Apartment 1903 Is Empty. (Part 1/5)*

| s (est.) | % | Beat | What happens | Borrowed from |
|---|---|---|---|---|
| 0-4 | 0-5 | B1 hook | Rule 3 as line 1 over the rule bubble; "by seven a.m. I'd broken all six" | TRUCKER-RULES 7692268145888873760 0:00-0:10 (rules + confession); H2 |
| 4-12 | 5-15 | B2 rules | Gus adds her to Desk Handover, six rules stack in; Marcus named for 7; "rule three was the one that mattered" (pre-announced failure) | NIGHT-BUS shTJ7_kRNJ8 "remember rule [K]"; DOG-RULE gDNMSoGSZgQ protector named as next arrival |
| 12-20 | 15-24 | B3 intrusion | 1 a.m., stuffy lobby, she props the glass door; Gus texts "Shut the door. Rule 1." before she read it | HEARSE-P1 7702661541224566049 rule broken before stated (0:31-0:36) |
| 20-34 | 24-41 | B4 proof | the empty car comes down from 19 by itself, doors open, 19 lit; rule 2 arrives just in time; doors close, it climbs back | TRUCKER-RULES radio match (0:29-0:53), compressed |
| 34-46 | 41-56 | B5 ladder + plant | "How did he know? He isn't in the building." She reads 4, 5, 6 fast; the yellow tape on line 1903 | SIEGE-CHAT 7659677578365537569 clue questions (0:18-0:19) |
| 46-56 | 56-68 | B8 turn | she asks Gus why 1903 has its own line if it's empty; typing on/off; "Nobody's lived there since before me." | HEARSE-P1 50% turn |
| 56-62 | 68-76 | B9 peak (held 4 s) | CCTV, 19th-floor tile: 1903's door, closed all night, is open a crack; nothing else moves | TRUCKER-RULES held image (2:09-2:12) |
| 62-74 | 76-90 | B11 twist | the gap widens one notch between two cuts; the desk phone's line 1903 LED flickers once, then lights | T7 planted identifier |
| 74-82 | 90-100 | B12 cut | it rings, desk clock 2:41; she reaches; Gus: "Let it ring." Card PART 1/5 · RULES BROKEN 1/6 | HEARSE-P1 bookend (3:16-3:21) |
Open at cut (5): who is calling from 1903; how Gus knew; why 1903 has a line; who opened 1903; what rule 3 really costs.

### Part 2/5: "Rule 4" (target 82 s; full script in `part2/script.md`)
Title: *At 3 A.M. My Night Desk Rules Say Count the Keys. There Was One Too Many. (Part 2/5)*

| s (est.) | % | Beat | What happens | Borrowed from |
|---|---|---|---|---|
| 0-3 | 0-4 | B1 cold hook | rule 3 fragment, then it rang anyway, nineteen times (contradiction by ~2.5 s; the count is news to P1 viewers) | HEARSE-P2 7702661471641128224 no-recap cold open (0:00-0:11), with the jolt moved to line 1 |
| 4-13 | 5-16 | B2/B4 | who Gus is, one order: let it ring; she counts **19 rings**, it stops on 19 "same as the floor" | T2 count match (SIEGE-CHAT 7659677578365537569) |
| 13-27 | 16-33 | B2/B3 | 3:00, rule 4 read; count track 93, 94, 95; a 96th key on the empty hook; tag 1903; still swinging | DOG-RULE gDNMSoGSZgQ rule stated then broken by 10 s (0:00-0:12) |
| 27-43 | 33-53 | B5 + P1 payoff | Gus: don't touch it, back to the board; the visitor log: Gus's line from last night, 2:41, "going up myself, back in five", no sign-out in 24 h (pays P1's "how did he know") | HEARSE-P2 Part-1 plant paid at 46% (1:28-1:29) |
| 43-48 | 53-59 | B8 turn | "did you ever come back down?" typing, stop, typing: "I'm home in bed." (a lie, paid P4) | HEARSE-P2 outside-check setup (1:36-1:47) |
| 48-56 | 59-68 | B5 sensory | the swinging stops; three slow taps on the board behind her; her right hand goes cold | TRUCKER-RULES sound before sight (1:45-1:51) |
| 56-60 | 68-73 | B9 peak (held 4 s) | "I looked down." Silence, heartbeat: her fist around the key, tag 1903, red light. Stamp **4 ✕** | DOG-RULE gDNMSoGSZgQ red reserved for the peak |
| 60-72 | 73-88 | B11 twist | she never reached for it; under Gus's log line, a new one in her handwriting with the time box empty: "1903 called. Going up myself." | T4 mirror ritual (HEARSE-P1 7702661541224566049 67-78%) |
| 72-82 | 88-100 | B12 cut | first text from "Mr. Pell, the owner": "Bring the key to 1903. Now." then rule 5 vs rule 3 as verbatim fragments. Card PART 2/5 · RULES BROKEN 2/6 | DORM-RULES 7670495663624408352 new order, new authority |
Open at cut (5): where Gus is; who wrote her line and when it comes true; what the key opens; rule 5 vs rule 3; Pell's number (on-screen clue).

### Part 3/5: "Rule 5" (target 80 s)
Title: *The Building Owner Texted Me to Go Up to the Empty Apartment. Rule 5 Says Obey Him. (Part 3/5)*

| s (est.) | % | Beat | What happens | Borrowed from |
|---|---|---|---|---|
| 0-3 | 0-4 | B1 cold hook | "The owner ordered me up to the empty apartment. His texts came from it." (P2's on-screen clue paid as the hook's news; the full proof follows at ~40%) | H3 official order (SIEGE-OVERLAY 7654526047005723937) |
| 4-11 | 5-14 | B4 contradiction | she forwards it to Gus; Gus in one second: "That isn't Pell's number." (contradiction at ~8 s) | PLAYBOOK §6: contradiction ≤ 11 s; SIEGE-CHAT deduction (1:54-1:58) |
| 11-32 | 14-40 | B5 rule clash | rule 5 vs rule 3 whip; the paper staff sheet: owner 555-0178; 555-0143 is the disconnected 1903 line (pays P2 plant at ~40%); "neither rule was wrong; the number was" | DORM-RULES 7670495663624408352 two rival authorities (T3); HEARSE-P2 plant at ~45% |
| 32-40 | 40-50 | B8 turn | she refuses (stamp **5 ✕**, 3/6); Pell: "Then I'll come down." | HEARSE-P1 50% turn |
| 40-55 | 50-69 | B5/B6 ladder | floor indicator counts down from 19 (19, 16, 12, 8...), Gus: "Don't watch the numbers. Watch the doors." CCTV elevator tile flickers | count ladder, physical rungs ~3 s (PLAYBOOK §4A) |
| 55-59 | 69-74 | B9 peak (held 4 s) | elevator tile: a man in a burgundy blazer riding down, face to the back wall | TRUCKER-RULES held image (2:09-2:12) |
| 59-70 | 74-88 | B11 twist | the desk speaker clicks on by itself; Gus's voice (bm_george): "Kid. The chat isn't me." Two Guses: chat vs voice | T6 voice swap (TEXT-FIGURE T42u5xhrq-0); T1 |
| 70-80 | 88-100 | B12 cut | ding; doors open on the lobby: the car is empty, 19 lit; the voice: "Get in, kid." Card 3/6 | DOG-RULE gDNMSoGSZgQ lure (0:56-0:59) |
Open at cut (4): which Gus is real; who rode down; how the empty line texts; the blank time on her log line.

### Part 4/5: "Rules 2 and 6" (target 86 s)
Title: *My Night Desk Rule 2: If the Elevator Comes Down Empty, Don't Get In. I Got In. (Part 4/5)*

| s (est.) | % | Beat | What happens | Borrowed from |
|---|---|---|---|---|
| 0-3 | 0-4 | B1 cold hook | "The elevator came down empty. Rule two: don't get in. Gus's voice: get in." | H14 rule then pressure (DOG-RULE gDNMSoGSZgQ) |
| 4-14 | 5-16 | B4 | she stays behind the desk; chat Gus: "That's not me. Don't listen to it." The voice repeats her name, which she never told it | SIEGE-CHAT channels take turns |
| 14-38 | 16-44 | B10 lifeline / outside check | she dials Gus's cell from the staff sheet. On the desk phone, line **1903** lights. His phone is ringing upstairs (pays P2 "home in bed") | HEARSE-P2 7702661471641128224 outside check "What uncle?" (1:36-1:47), T5 |
| 38-46 | 44-53 | B8 midpoint flip | chat Gus: "I lied so you'd stay down there. I'm in 1903. It wants a night man." The protector is the prisoner | HEARSE-P2 reframe (1:59-2:00) |
| 46-52 | 53-60 | decision | the log: her blank time box now reads 4:12, the desk clock's minute (pays P2 handwriting); "Rule three said send nobody up. Nobody sent me. I went."; she leaves the desk (**6 ✕**) and gets in (**2 ✕**) → 5/6 | TRUCKER-RULES hubris rule (0:25) |
| 52-62 | 60-72 | B5 physical ladder | doors close by themselves; the indicator climbs (4, 9, 14, 17); the car is warm; something breathes in rhythm with the fan | HEARSE-P2 fast physical ladder (0:20-0:45) |
| 62-66 | 72-77 | B9 peak (held 4 s) | the mirrored back wall: a burgundy blazer standing right behind her; she turns, nobody | T4 mirror; ElevatorPanel background |
| 66-76 | 77-88 | B11 | 19, doors open: hallway, 1903 ajar, the man in the blazer facing the wall beside it; Gus: "If I'm standing out there, it isn't me." | HOTEL-DOOR Qz-TrB6W2SM door ladder |
| 76-86 | 88-100 | B12 cut | without turning, his hand held out behind him: "You brought my key, kid. Give it here." Card 5/6 | TEXT-FIGURE T42u5xhrq-0 threat on "you" |
Open at cut (4): what the key does; can Gus get out; what the thing wants; who takes the desk at 7.

### Part 5/5: "Rule 3" (target 88 s, the finale)
Title: *Rule 3 of My Night Desk: If 1903 Calls, Send Nobody Up. So I Went Up Myself. (Part 5/5)*

| s (est.) | % | Beat | What happens | Borrowed from |
|---|---|---|---|---|
| 0-3 | 0-4 | B1 cold hook | "Nineteenth floor. A man in Gus's blazer, facing the wall, asked for my key." | bookend of P4's last frame |
| 4-16 | 5-18 | B6 isolation | battery 4%; 911 drops on the 19th floor; chat Gus from inside 1903: "Don't give it the key. Don't let it turn around." | SIEGE-CHAT dying lifeline (3:17-3:33) |
| 16-40 | 18-45 | lore (one drop) | Gus, in three short bubbles: 1903 calls the desk every night; whoever goes up answers the phone from then on; the rules keep the night man at the desk; last night he went up so the new kid wouldn't have to (pays 19 rings: his margin note) | DOG-RULE gDNMSoGSZgQ elder's stair-step lore (0:20-0:30) |
| 40-52 | 45-59 | B8 inversion | the P4 loophole collapses (the log, "Pell", the voice: 1903 calling *was* the sending); rule 3 re-read: send nobody up means **nobody follows** the one who went; the key locks 1903 from the hallway side (pays P2 fist), which is why it asked for the key | T17 NIGHT-BUS shTJ7_kRNJ8; T3 |
| 52-60 | 59-68 | B10 clock | the figure takes one step toward her with its back still turned; she has the key at the lock; Gus: "Lock it. With me inside. Then go back to the desk." | B10 lifeline under a clock |
| 60-64 | 68-73 | B9 peak (held 4 s) | the figure's head starts to turn; she shuts her eyes | one peak image, held |
| 64-78 | 73-89 | B11 twist (canon, ending A) | she turns the key; the voice, close behind her, in Gus's voice: "Thanks, kid. Your shift now." Stamp **3 ✕** (6/6) with the loudest hit; the light goes out | T1 + T9 |
| 78-88 | 89-100 | B12 | 7:00, the lobby: Marcus walks in to an empty desk; his phone: "Lena added you to Desk Handover"; six rules stack, rule 3 rewritten "Even if it sounds like me."; line 1903 lights behind him. Card PART 5/5 · RULES BROKEN 6/6 | T17 + ring structure |
Open at cut (3): is Lena in 1903 now; is Gus free; who calls Marcus at 2:41 tonight.

## 6. Two alternate endings (for Part 5, beats 64-88 s)

Both keep the same first 64 s, so the choice can be made at the build step (or both cut and A/B tested as separate uploads; PLAYBOOK §10 "treat as hypotheses").

**Ending B: "The trade" (sacrifice, softer; leaves a season-2 door).** As she turns the key, 1903's door opens inward and the real Gus (Neighbour puppet, `sad`, red light, the only time we see his face outside the staff photo) shoves her back into the elevator, takes the key and pulls the door shut from inside: "Rule three, kid. I wrote it for you." The car drops to L on its own. 7:00: Marcus (`surprised`) finds Lena at the desk, alive; the 96th hook is empty and Gus's blazer hangs on it. Last image: line 1903 lights; she lets it ring. Last line: "Nineteen rings. I counted." Uses T12 (the protective object becomes the victim) and §4C ending 8 (fake win plus lingering image). Risk: "kid" from the real Gus breaks the re-watch clue; if chosen, change his line to "Rule three. I wrote it for you."

**Ending C: "The narrator was the voice" (T13, threat turned on "you").** Beats 64-78 as canon. At 78 s the narration (which has been Lena's voice for five parts) switches to bm_george mid-sentence and the camera turns to face the viewer from the desk: "So, new night man. Six rules. Read them twice. Rule three: if 1903 calls, send nobody up. Trust me, kid." The figure is shown once, front-on, with the kit's `grin` (the only `grin` in the series). The viewer becomes the next hire (PLAYBOOK §4C ending 5/10; FAKE-ROOMMATE 7650872317119057168 narrator-is-the-monster at 76%). Strongest comment driver, weakest closure; best for the "full story" compile's ending.

## 7. Comment bait and pinned-comment plan

No spoken subscribe or app funnel in any part (PLAYBOOK §4C; the mraevq control 7665304797242821921 ended on an app funnel at 1.06x). Comments come from **in-premise questions** (NIGHT-BUS shTJ7_kRNJ8 asks one at 49%; VIDEO-CHAT-GAME 6WfCF7KsLaQ ends on a moral question) and **fair-play re-watch clues** (TWO-SUSPECTS 7659482056656735521 knowledge slip, T14). Each clue is on screen for ≥ 1.5 s so a pause can find it.

| Part | On-screen bait (no voice) | Pinned comment (posted by the channel, in-world voice) | Re-watch clue the pin points at |
|---|---|---|---|
| 1 | rule tracker 1/6 with rule 3 circled | "Rule 3 is the one that matters. Which rule would you have broken first?" | the 19 already lit on the empty car |
| 2 | staff sheet visible 2 s at ~44% | "Pause on the staff sheet, then look at who texts her at the end. Notice anything?" | 555-0143 is the 1903 line, not Pell (555-0178) |
| 3 | none extra (the cut is strong) | "Two Guses. One types, one talks. Which one would you trust?" | only one of them says "kid" |
| 4 | log page held at 4:12 | "In Part 2 her log line had no time. Who filled it in?" | the empty time box (P2) vs 4:12 (P4) |
| 5 | rule 3 rewritten on the last frame | "Marcus has the rules now. Write him rule 7." (best replies pinned as the "Part 6" teaser) | rule 3's new clause |

**Reply plan:** heart and reply to the first comments that find each clue with "Gus would've hired you", never confirm theories. The rule-7 replies from Part 5 feed the season-2 premise (the comment thread becomes the next handover sheet). Every part's description: the title rule, "Part N/5", and the series tags; the compile's description lists the parts.

## 8. Build notes (for the lane that builds the parts; this bible changes no code)

- Script format per part: references front matter, beat-alignment table, narration with timestamps, shot list (see `part2/script.md`). Each part's script must clear the originality gate (`scripts/originality_check.py`, against the corpus and library transcripts) before TTS.
- Timestamps in this bible are estimates; measure with Kokoro on the Spark (CPU, `CUDA_VISIBLE_DEVICES=""`) as the draft's `tts_measure.py` does, then re-place the beats.
- Props come from the draft's `build.py` helpers (copy, don't import or edit): `desk_phone`, `keyboard`, `lobby`, `elevator_view`, `hallway_1903`, `cctv_grid`, `paper`, `count_track`, `stamp`, `card`.
- The horror kit is locked (BRIEF Update 11:27) until `out/pilots/QA.md` shows horror PASS. Everything here works with the kit's existing components and props.
