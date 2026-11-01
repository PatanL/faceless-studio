# Thumbnail concepts: whatif-light-walking-speed

Three concepts. Each one renders as a Remotion still on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube), using the same whatif art the video uses so the cover looks like the video. Thumbs-kit rules apply: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, and one accent colour. The accent here is amber #FFB547, matching the "walked" keyword and the light bubble. The thumbs kit has no `whatif` template yet (only explainer and horror), so each concept lists the layers a `whatif` template would need. Library rule to respect: the thumbnail's word or number must pay off on screen within about 10 s (research/library/index_notes/whatif.md, technique 10). The reference review also asks that the cover lead with the strongest original image rather than a generic crossing, because slow-light videos already exist.

## A. "One bubble of light" (recommended TikTok cover and Shorts thumbnail)

- **Inspired by:** 7693494009494342945 ELECTRONS (its post-flip cover look: the place transformed into one striking alternate render, with the HUD visible); YznR5NmI3bc STOP-TIME (one huge, simple subject, a single punchy phrase and a complementary colour pair); _lu85gSD39k BILLION-YEARS (a lone small figure against a vast dark field).
- **Composition:** the 0:57 frame. Shibuya Crossing at night, entirely black except for faint 6% ghosts of the towers, giant screens and zebra stripes. Lower-centre, "you" (explainer/You, blue jacket) stand on the kerb inside a warm glowing dome of light about 6 m across. Inside it, the lit kerb, a strip of road and your friend mid-wave are in full colour. The dome's edge is a soft amber rim with the ring tag "6.0 M". Top-left, the HUD reads LIGHT RETURNS IN 0:00.418 / LIGHT PILED UP: 4.58 S.
- **Text (3 words):** **LIGHT IS WALKING.** ("WALKING." in amber), a heavy outlined block in the black upper third. The black sky gives clean negative space.
- **Colours:** near-black #010203 field, ghost lines in #1B2430, dome interior in normal neon colours (magenta #FF5FA2, cyan #53D8FB, warm street #F2C27B), amber rim #FFB547, white text with 10 px black outline.
- **Kit assets:** whatif/CrossingSet (`light: slow`, `view: wide`, tau 4.6), whatif/RadialSplit (inside CrossingSet), explainer/You x2 (you; friend with the armR track), whatif/Hud (frozen state), thumbs text block.
- **Payoff on screen:** the black city with a glow around you appears at 0:07, and the HUD says 1.4 M/S = WALKING PACE at 0:07. Both are inside 10 s.

## B. "The car you can't see" (A/B variant against A)

- **Inspired by:** DK4EOHCrVvM WEALTH and b6jmbFcJZCY EVERY-HUMAN (a big outlined phrase with a question or full stop, over an image that looks wrong); 7694025665993100576 POPSTAR-100x (the threat right next to "you", scale contrast); 7693305573487562016 OXYGEN (a closing-distance HUD meter).
- **Composition:** the 0:36 frame. Close three-quarter shot of you at the kerb edge, jacket blown sideways by wind. Right in front of you, a metre away, two semi-transparent copies of the same blue car slide apart: the left copy reverses (motion lines trailing in front of its nose, which is the wrong way), the right copy creeps on. Everything past the bubble is black. A dashed amber line from your feet to the car is labelled "1 M".
- **Text (2-3 words):** **DRIVING BACKWARDS?** ("BACKWARDS?" in amber), outlined block in the upper third.
- **Colours:** black field, the car in desaturated steel blue #7FA7B8 at 70% opacity per copy, amber line and word, white text with black outline. Blue/amber is the complementary pair.
- **Kit assets:** whatif/CrossingSet (`light: slow`, heroCar images at t 36.0), explainer/You (wind prop), core `svg` dashed line, thumbs text block.
- **Payoff on screen:** the reversing car appears at 0:34.3, late, which breaks the 10 s rule. Use B only as an A/B variant. The black city and the bubble, which carry the frame, are visible from 0:07.

## C. "Before / after split" (recommended for the YouTube 16:9 shelf)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (the same subject twice, "TODAY" vs "50 YEARS LATER", 4 words); J3XahLkDEzU LAST-HUMAN (slanted split, same street and same hero in each half, labels in the top corners); 7693305573487562016 OXYGEN (the baseline reading next to its delta: 14.7 PSI -> 11.6 PSI).
- **Composition:** a slanted split with a thin white bar, and the same framing in each half (frame 1 of the video). Left half: the normal neon crossing, busy with cars, crowd and screens. Right half: the identical framing gone black, with one small amber glow around your head and a ghost Moon. A tiny "you" sits on the kerb in both halves at the same spot.
- **Text (4 words):** two road-sign plates in the top corners, **299,792,458 M/S** (white, left) and **1.4 M/S** (amber, right). On the 16:9 version, add a centred **5 SECONDS.** block in white.
- **Colours:** left in full neon (magenta, cyan, warm white); right in black with amber only; white split bar; black outlines on all text.
- **Kit assets:** whatif/CrossingSet twice (`light: normal` at t 0.0 and `light: slow` at t 8.0), whatif/SkyBodies (ghost Moon), thumbs split template (new: slanted mask + bar), thumbs text plates.
- **Payoff on screen:** both numbers are in the HUD by 0:07 (the baseline at 0:00, the flip at 0:07).

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-light-walking-speed/thumbs.json` with variants `bubble` (A), `backwards` (B) and `split` (C). Then run `OUT=thumbs/whatif-light scripts/thumbs_render.sh <spec>` on the Spark only. Check the contact sheet at phone size: the text must read at 120 px tall, and the dome in A must still read as a light bubble, not a vignette (keep the amber rim at least 6 px at 1080 wide).
