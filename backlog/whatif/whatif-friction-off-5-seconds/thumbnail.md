# Thumbnail concepts: whatif-friction-off-5-seconds

There are three concepts. Each is rendered as a Remotion still on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube) from the same whatif and explainer art the video uses, so the cover looks like the video. Thumbs-kit rules apply: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, and one accent colour (amber #FFB547 here instead of red, to match the video's keyword). The thumbs kit has no whatif template yet (only explainer/horror), so each concept below lists the layers a `whatif` template needs. Library finding to respect: the thumbnail word or number must pay off on screen within about 10 s (research/library/index_notes/whatif.md, technique 10).

## A. "Frame-0 cover" (TikTok cover, recommended for the 9:16 post)

- **Inspired by:** 7693494009494342945 ELECTRONS and 7693617402180881697 NEUTRONS covers (frame 0 = calm named place + title in the upper third + HUD countdown at left); 7696143265405488416 PI=3 cover (a small diagram floating over the sky).
- **Composition:** the actual first frame. Warm golden-hour Lombard Street from below hairpin 6: brick switchbacks rise to the top third, hedges and purple hydrangeas, the cable car with riders at the very top, two cars mid-bend. "You" (explainer/You, blue shirt) stands small on the bricks, lower-centre. The shoelace-bow icon sits above the title. The HUD at top-left reads FRICTION ● ON / OFF IN 6.900 S / HILL GRADE 27%. Because the cover matches frame 0, the TikTok loop and the cover agree.
- **Text (2-4 words):** the cover keeps the serif video title instead of a block caption. For the YouTube Shorts shelf, add one extra outlined word block in the sky: **5 SECONDS. ZERO GRIP.** ("ZERO GRIP." in amber).
- **Colours:** warm palette (brick #B5523B, hedge #3F6B3A, hydrangea #8E7CC3, sky #F2B880 -> #F7D9A8); keyword and HUD numbers in amber #FFB547; HUD text white with a 2 px dark shadow.
- **Kit assets:** whatif/LombardMap (keyframe "low"), whatif/CableCar, explainer/Car x2, explainer/You (shirt prop), whatif/TitleCard (shoelace icon), whatif/Hud.
- **Payoff on screen:** the same image is the first 4.5 s; "zero grip" pays off at 0:07 (the flip).

## B. "ON / OFF split" (before/after, recommended for the YouTube 16:9 and Shorts shelf)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (white ground, the same subject twice: "TODAY" vs "50 YEARS LATER", 4 words total); J3XahLkDEzU LAST-HUMAN and JGTawyfFG8g (slanted split, same street and same hero in each half, labels in the top corners).
- **Composition:** a slanted split with a white bar. Left half, warm: a close-up of one sneaker with a neat tied bow, a buttoned shirt cuff above it, bricks underneath. Right half, glossy cyan with diagonal streaks: the same shoe with the laces floating loose like weed and the shirt cuff peeling into white fluff wisps. Thin threads cross the split bar. A tiny "you" sliding on their back in the far background of the right half gives the scale contrast.
- **Text (4 words):** **FRICTION ON** (white, top-left corner) / **FRICTION OFF** (amber, top-right corner), on road-sign-style label plates.
- **Colours:** left warm brick/sky palette, right cyan (#9FE8FF overlay, desaturated); amber only on "OFF"; white split bar; thick black outlines on the text.
- **Kit assets:** whatif/ShoePair (states tied and loose), whatif/FluffWisps, whatif/SlopeStrip (bricks only, cropped), whatif/Streaks overlay, explainer/You (`sprawl`, tiny), core grade.
- **Payoff on screen:** the tied-to-loose laces are shot 4 (0:08-0:12); the shirt cuff becoming fluff is shot 9 (0:29.5).

## C. "66 FT TO STOP" (number hook, best for an A/B test against B)

- **Inspired by:** YznR5NmI3bc STOP-TIME (huge foreground subject, a single punchy word with a full stop, a complementary colour pair); _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM (a big number in the text block); 7693305573487562016 OXYGEN (a closing-distance meter on the HUD).
- **Composition:** a high three-quarter chase view down the hairpins (the shot 14 camera). "You" slides feet first, lower-left, on your back, with a 2-ghost motion trail. Top-right, straight down the fall line, is a heap of cars, boards and a white fluff pile against a garden wall. A dashed amber distance line runs from your feet to the pile with the tick label "15 FT". The HUD at top-left is in race state: BACK ON IN 0.000 S / YOU: 29 MPH.
- **Text (4 words):** **66 FT TO STOP.** ("66 FT" in amber, "TO STOP." in white), heavy outlined block in the upper third.
- **Colours:** cyan frictionless grade over the map (blue-teal) against the amber number and distance line (an amber/blue complementary pair, like STOP-TIME's yellow/purple). The fluff pile stays pure white so it reads at small sizes.
- **Kit assets:** whatif/LombardMap (keyframe "chase"), explainer/You (`sprawl`), whatif/TopDownCar x3, whatif/FluffPile, whatif/Hud (race state), core callout `label` for "15 FT".
- **Payoff on screen:** the number pays off late (1:04.2). That breaks the "within 10 s" library rule, so use C only as an A/B variant. The cyan chase look and the HUD race are visible from 0:51.

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-friction-off-5-seconds/thumbs.json` with variants `cover` (A), `split` (B) and `distance` (C), then run `OUT=thumbs/whatif-friction scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text has to read at 120 px tall.
