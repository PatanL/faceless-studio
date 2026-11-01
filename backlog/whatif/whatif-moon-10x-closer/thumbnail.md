# Thumbnail concepts: whatif-moon-10x-closer

There are three concepts. Each is rendered as a Remotion still on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube) from the same whatif art the video uses, so the cover looks like the video. Thumbs-kit rules apply: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, and one accent colour. Here the accent is moon-silver/ice-blue #CFE3FF with a warm amber #FFB547 for the number, instead of the library's default yellow, so it matches the HUD. The thumbs kit has no whatif template yet, so each concept lists the layers that template needs. Library rule to respect: the thumbnail word or number must pay off on screen within about 10 s (`research/library/index_notes/whatif.md`, technique 10).

## A. "Frame-0 cover" (TikTok cover, recommended for the 9:16 post)

- **Inspired by:** 7694025665993100576 POPSTAR-100x (the giant already in frame 1 with a distance HUD falling); 7693494009494342945 ELECTRONS and 7693617402180881697 NEUTRONS covers (frame 0 is a calm named place, the serif title sits in the upper-middle and the HUD counter is top-left).
- **Composition:** the 0:08 frame, not 0:00, so the Moon is at full size. St Margaret's Bay at blue hour looking SSE. The chalk headland fills the lower right. The giant Moon (5.78°, ~208 px at fovH 30°, enlarged to ~340 px for the cover by using fovH 18° on the same azimuth) hangs just above the cliff edge, upper right, with its halo and maria. A flat silver sea with a wide glitter band leads to the horizon at 80%. One tiny figure (explainer/You, silhouette) stands on the shingle near the seaweed tideline, lower centre, for scale. HUD top-left: THE MOON / 38,440 KM / DRIFTS 3.8 CM AWAY EACH YEAR.
- **Text (2 words):** the cover keeps the serif video title. For the YouTube Shorts shelf, add one outlined block in the sky, left of the Moon: **10× CLOSER** ("10×" in amber, "CLOSER" in white).
- **Colours:** blue-hour navy #1F3B66 → #6E8DB8 sky, chalk #EDEAE0 with cool shadows, sea #2C4F73 with a silver glitter band, Moon #E6ECF2 with a #CFE3FF halo; amber only on "10×".
- **Kit assets:** whatif/Cliffs (bearing 144, `clockHour` 19.0, `seaLevel` 0), whatif/Moon (sizeDeg 5.78, phase full-ish), explainer/You (silhouette), whatif/Hud (distance mode, frozen at 38,440 KM), title text layers.
- **Payoff on screen:** this is the 0:08 image; "10× CLOSER" pays off at 0:08 (the counter lands on 38,440 KM).

## B. "TODAY / 10× CLOSER split" (before/after, recommended for YouTube 16:9 and the Shorts shelf)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (the same subject twice, "TODAY" vs "50 YEARS LATER", 4 words total); J3XahLkDEzU LAST-HUMAN (a slanted split, same place in each half, labels in the top corners).
- **Composition:** a slanted split with a white bar. Left half: the White Cliffs by day with a normal small Moon, the sea at the shingle and a ferry floating offshore. Right half: the same cliffs and the same ferry, but the giant Moon fills the sky, the sea is gone to the horizon, and the ferry sits tilted on bare chalk seabed. A tiny figure stands in the same spot in both halves.
- **Text (3 words):** **TODAY** (white, top-left plate) / **10× CLOSER** (amber "10×" + white "CLOSER", top-right plate).
- **Colours:** left half warm daylight (sky #8EC3EA, sea #2F6E9A); right half the silver grade (hue +8, saturate 0.85) with the dry seabed in sand #D8C08E against a navy sky; white split bar; thick black text outlines.
- **Kit assets:** whatif/Cliffs twice (bearing 125; `seaLevel` 0 and −91), whatif/Moon (sizeDeg 0.52 and 5.78), whatif/Ferry (tilt 0 and 7), explainer/You (tiny), core grade.
- **Payoff on screen:** "10× CLOSER" pays off at 0:08. The dry seabed and the stranded ferry are 0:19-0:28, which is late for the 10 s rule, but the split label itself pays off at 0:08.

## C. "WALK TO FRANCE?" (map hook, best as an A/B test against B)

- **Inspired by:** YznR5NmI3bc STOP-TIME (one punchy line with a question mark, a complementary colour pair); _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM WEALTH (a big number in the text block); 7694025665993100576 POPSTAR-100x (a dotted closing line with a distance label on the HUD).
- **Composition:** a top-down strait map. England top-left and France bottom-right in dark land green; the strait floor is drained to sand colour with two small blue pools (Fosses Dangeard). An amber dotted line runs from a YOU pin (St Margaret's Bay) to a CAP GRIS-NEZ pin, labelled "33 KM". A tiny walking figure sits on the line a third of the way across. In the upper corner, a slice of the giant Moon's limb glows in from off-frame, so the cause is in the picture.
- **Text (3 words):** **WALK TO FRANCE?** (heavy outlined block in the upper third; "FRANCE?" in amber).
- **Colours:** sand #D8C08E strait against navy #123047 water and #2D5A55 land (a warm/cool pair); amber #FFB547 line and word; silver #CFE3FF Moon limb.
- **Kit assets:** explainer/Map (`channel` detail region, solid `zones`, `paths`, `pins`), whatif/Moon (cropped limb), explainer/You (tiny, walking), core text.
- **Payoff on screen:** the line pays off at 0:31.5. That breaks the "within 10 s" library rule, so use C only as an A/B variant against B, never as the TikTok cover (where frame 0 is the cover anyway).

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-moon-10x-closer/thumbs.json` with variants `cover` (A), `split` (B) and `walk` (C), then run `OUT=thumbs/whatif-moon scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text has to read at 120 px tall, and the Moon has to read as a disc, not a dot.
