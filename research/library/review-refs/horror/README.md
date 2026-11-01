# Horror review refs (pilot QA)

These are three outlier references with 12 frames each, all 1080x1920 (`NN_<qa_class>.jpg`). Every reference uses the same 12 shot classes in the same order, so `scripts/side_by_side.sh <pilot.mp4> horror` can put the pilot's frame for each class next to them. Timestamps and descriptions are in `../frames_spec.json`. All three are TikTok reposts of Chinese animated suspense series (BRIEF rule 5): study the frame grammar, never the stories or characters.

| Ref | Score | Why it's here |
|---|---|---|
| [7654526047005723937](https://www.tiktok.com/@mraevq/video/7654526047005723937) @mraevq, "A killer broke into my apartment complex" | **66.69x** (717K) | The top phone-chat outlier: the knock arrives at 5.4 s, the residents' group chat sits next to the character, floating comments add dramatic irony, and there's a 1% battery insert. 6 min. |
| [7702661541224566049](https://www.tiktok.com/@udhwkz/video/7702661541224566049) @udhwkz, "never cut off a funeral procession" | **63.13x** (2.2M) | The top udhwkz outlier: a taboo rule in the hook, POV through the windshield, dread shading on close-ups, a cut mid-sentence. It has **no phone UI**, so its phone rows are substitutes. 3.4 min. |
| [7659677578365537569](https://www.tiktok.com/@udhwkz/video/7659677578365537569) @udhwkz, "There's a killer hiding in our apartment complex" | 10.79x (376K) | The closest match to our pilots (and cited by them): a hand-held phone with group-chat screens takes about 45% of screen time, there's a knock at 11 s, and the story ends on a feature-phone cliffhanger. 4 min. |

`7664930759395888416` (39.82x) scores higher than 7659677578365537569 but was left out. It's a 15-min chase with almost no phone UI, so it is a weaker guide for a phone-chat pilot.

## Frames (row = shot class)

| # | Class | 7654526047005723937 | 7702661541224566049 | 7659677578365537569 |
|---|---|---|---|---|
| 01 | thumbnail | cover = frame 0 | cover = frame 0 | cover = frame 0 |
| 02 | hook_0s | axe silhouette in corridor + caption | POV behind driver, hearse ahead | grinning silhouette with knife in teal corridor |
| 03 | hook_twist | danmaku warning box at the door (8.5 s) | ECU funeral glyph | chat "killer had been caught" (false relief) |
| 04 | phone_chat | group chat beside character | MCU (substitute) | hand-held phone, group chat |
| 05 | phone_chat_2 | full-width chat | sedan blocked by a truck (substitute) | group chat 2 |
| 06 | character_medium | fake cop at the door | lead sedan | protagonist at door |
| 07 | reaction_closeup | dot-pupil horror eyes | passenger, dread shading | close-up, bruise shading |
| 08 | two_shot | two-shot, barricade | two-shot through windshield | two cops |
| 09 | insert_prop | 1% battery | glyph on hearse | WeChat "help" message |
| 10 | wide_establishing | kitchen medium-wide | aerial highway | music notes in dark hallway |
| 11 | overlay_or_pov | floating comments over character | POV through windshield | POV close-up of cop |
| 12 | cliffhanger_end | radio on table (orders overheard) | POV windshield, cut mid-line | feature phone "Don't let them find you" |

## What a pilot must match (pass/fail at review)

**Frame layout and captions**
- The format is 9:16. The references play a roughly 4:3 picture band (about 43% of the frame height) on black, with a **single-line white caption centred just above the band**: plain sans for mraevq, italic sans for udhwkz, 6-9 words at about 4% of frame height. The pilot may go full-bleed, but the caption must be **one short line, high contrast, placed outside faces and phone text, and changed every 1.4-2 s**.
- **Frame 0 = cover.** A readable threat (silhouette, weapon, door, a message that shouldn't exist) and a caption must be visible at frame 0. No fade from black, and no title card.

**Look**
- Flat cartoon with thick outlines, big heads, 2-4 characters, and expression swaps (normal, dot-pupil horror eyes, narrowed eyes). Held poses are fine: motion comes from cuts, pop-ins and small shakes.
- The palette is a desaturated night (teal/blue-grey or muted brown/olive) with **one warm danger accent** (red on a weapon, red text). No saturated daytime colours outside flashbacks.
- Phone UI is light grey or white with avatar, name and unit number, and the bubbles are readable on a phone: body text at least about 34 px at 1080 wide, at most about 6 visible messages. The phone is held by a hand (udhwkz) or sits beside the character (mraevq).

**Shot mix and pacing (over the whole pilot)**
- Close-ups plus inserts should outnumber two-shots and group shots; the 9:16 outliers are at about 35% vs 13%. Phone/chat screens should take 10-45% of screen time.
- A reversal (false safety inverted, or a rule broken) must land within the **first 12 s**, then a new anomaly or twist every 15-25 s.
- **The last frame cuts mid-action or mid-sentence**: a cliffhanger, not an outro or CTA card.

**What may differ:** the story, the characters, the UI language (ours is English), and full-bleed vs letterbox. Never reuse reference panels, names or plots.

## How to review

```bash
scripts/side_by_side.sh out/horror-member-41.mp4 horror                   # -> out/qa/horror-member-41_vs_horror.jpg
scripts/side_by_side.sh out/horror-member-41.mp4 horror --storyboard episodes/horror-member-41/storyboard.json --cell 300
```
Each row shows the references on the left and the pilot (red frame) on the right. The pilot's frame is taken from the storyboard scene whose id, notes or components match the class (e.g. `horror/HandPhone` maps to phone_chat, `horror/Peephole` to insert_prop). Rows with no match use the same relative position as the reference, and stdout says which rule picked each frame.
