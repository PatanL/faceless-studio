# Thumbnail concepts: whatif-earth-had-rings

Three concepts. Each one is a Remotion still rendered on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube) from the whatif and explainer art the video itself uses, so the cover and the video look the same. Thumbs-kit rules apply: one big subject and one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, and one accent colour (ring gold #E8B04A instead of red, to match the video's keyword). The thumbs kit has no whatif template yet (only explainer and horror in `studio/src/kits/thumbs/templates`), so each concept lists the layers a `whatif` template needs. One library rule applies to all three: the thumbnail's word or number must pay off on screen within about 10 s (research/library/index_notes/whatif.md, technique 10).

## A. "Arch over Ocean Drive" (TikTok cover, recommended for the 9:16 post)

- **Inspired by:** 7693494009494342945 ELECTRONS and 7693617402180881697 NEUTRONS covers (calm named place, title in the upper third, HUD countdown at the left), and 7694025665993100576 POPSTAR-100x (the premise visible in frame 1, a giant subject over a real street).
- **Composition:** the 0:08 frame. Ocean Drive at dusk looking due south: pastel Art Deco hotel fronts with pink and mint neon fins on the right, palms and the beach on the left. The ring arch fills the upper half of the sky: cream B ring, a dark Cassini gap, a grey A ring. Small and lower-centre, "you" (explainer/You) stands back to camera on the sidewalk. The serif title sits under the arch with "rings like Saturn" in gold and the ringed-planet glyph. The top-left HUD reads RING SHADOW REACHES YOU IN / 144.0 DAYS. The cover differs from frame 0 only in that the arch is already up, so the post loops cleanly from the title repeat.
- **Text (2-4 words):** the cover keeps the serif video title. For the YouTube Shorts shelf, add one outlined word block low in the sky: **ITS SHADOW: 144 DAYS** ("144 DAYS" in gold).
- **Colours:** dusk palette (sky #7B5EA7 -> #F6A96B, mint #9FE3C9, flamingo #F7A1C4, lemon #F9E79F, palm #2E6B4F), rings #EADFC4 / #CFC8B8, keyword and HUD numbers in gold #E8B04A, HUD text white with a 2 px dark shadow.
- **Kit assets:** whatif/OceanDrive (time dusk), whatif/RingArch (lit 1), explainer/You, whatif/TitleCard (ringed-planet glyph), whatif/Hud.
- **Payoff on screen:** the arch lands at 0:07 and the 144.0-day countdown starts in the same frame.

## B. "Sun / shadow split" (recommended for the YouTube 16:9 and Shorts shelf)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (the same subject twice, "TODAY" vs "50 YEARS LATER", 4 words total), J3XahLkDEzU LAST-HUMAN (a slanted split with the same street and the same hero in each half, labels in the top corners), and YznR5NmI3bc STOP-TIME (a complementary colour pair).
- **Composition:** one Ocean Drive frame split by a hard diagonal shadow edge across the pavement, which is the ring's shadow arriving. The left/lower half is bright noon with hard palm shadows. The right/upper half is the same street in blue-grey ring shade with the neon fins switched on. "You" stands exactly on the edge, half lit and half shaded. The arch above is pale in the daylight sky, with its dark B band right over the shaded half.
- **Text (3-4 words):** **SUMMER** (white, top-left plate) / **NOON, DECEMBER** (gold, top-right plate), or as a single block **NOON. IN THE DARK.**
- **Colours:** warm noon side (sky #8EC9F0, sand #EAD7AE, pastels) against the shade side (#0E1620 + #5B6B7A tint, neon pink #FF7AC6); gold only on the second label; thick black outlines on the text.
- **Kit assets:** whatif/OceanDrive (time day), the soft-edged shade rect used in shot 13 (here a hard diagonal mask), whatif/RingArch (dayside), explainer/You, core grade overlays.
- **Payoff on screen:** the shadow edge on Ocean Drive appears at 0:55 (contact). That's late, so the TikTok cover stays A and B goes on the shelf, where the title explains it.

## C. "MIAMI < MOSCOW" (number hook, A/B test against B)

- **Inspired by:** _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM WEALTH (a big number or comparison in the text block), YznR5NmI3bc STOP-TIME (one punchy line with a full stop), and 7696143265405488416 PI=3 (a planet-scale rule turned into one exact local figure).
- **Composition:** the shot 12 map, Caribbean-wide. The dark ring-shadow band sweeps across Cuba and Florida, with grey "passed" pins on Havana and the cities to the south and a pulsing gold pin on Miami Beach. Inset top-right: a small Moscow pin icon with a snowflake. A tiny "you" glyph sits next to the Miami pin.
- **Text (3 words):** **LESS SUN THAN MOSCOW.** ("MOSCOW" in gold), heavy outlined block in the upper third.
- **Colours:** map ocean #0f3a4a, land #2d5a55, shadow band near-black at 55%, gold pin and gold word. The pins stay high-contrast white/grey so they read at small sizes.
- **Kit assets:** explainer/Map (static Caribbean view, pins), the band rect layers from `gen_storyboard.py`, whatif thumbs template text block.
- **Payoff on screen:** the claim pays off at 1:03.8 (caption 12). That breaks the "within 10 s" library rule, so use C only as an A/B variant on YouTube, never as the TikTok cover.

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-earth-had-rings/thumbs.json` with variants `cover` (A), `split` (B) and `moscow` (C), then run `OUT=thumbs/whatif-earth-had-rings scripts/thumbs_render.sh <spec>` on the Spark only. Check the contact sheet at phone size: the text has to read at 120 px tall, and the arch's three bands (B / gap / A) must stay distinct at that size.
