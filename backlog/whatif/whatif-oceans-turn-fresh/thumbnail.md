# Thumbnail concepts: whatif-oceans-turn-fresh

Three concepts. Each one renders as a Remotion still on the Spark (thumbs kit, a 1080x1920 cover plus 1280x720 for YouTube), using the same whatif and explainer art as the video, so the cover matches what plays. Thumbs-kit rules apply: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, and one accent colour (sea-glass cyan #7fe3ff, the video's keyword colour, with the orange current #ff8a3d as the only warm counter-colour). The thumbs kit has no whatif template yet (only explainer and horror), so each concept lists the layers a `whatif` template needs. Library rule to respect: the thumbnail word or number has to pay off on screen within about 10 s (research/library/index_notes/whatif.md, technique 10).

## A. "Frame-0 cover" (TikTok cover; recommended for the 9:16 post)

- **Inspired by:** the 7693494009494342945 ELECTRONS and 7693305573487562016 OXYGEN covers (frame 0 is a calm named place, the title in the upper third and the HUD countdown at left). 7696143265405488416 PI=3 for the small icon floating above the title.
- **Composition:** the actual first frame. A bright moonlit Bergen harbour: Bryggen's red, ochre and white gabled wharf houses on the right with lit windows, Mount Fløyen behind, a big full moon top-right with a wide shimmering reflection column. A broad orange current ribbon flows in from the left through the harbour mouth. "You" stands small on the quay at lower left, rod out, line in the water. The HUD at top left reads SALT GONE IN 0:08.000 / OCEAN SALT 35.0 g/kg / GULF STREAM: OFFSHORE. Because the cover is frame 0, the TikTok loop and the cover match.
- **Text (2-4 words):** the cover keeps the serif video title (wave-and-salt-grain icon, "salt" in cyan). For the YouTube Shorts shelf, add one outlined word block in the sky: **SALT: GONE.** ("GONE." in cyan).
- **Colours:** moonlit blues (sky #2c5d8f to #6f9cc6, water #1f5f86, moon path #eaf6ff) against Bryggen's red #c0473a and ochre #e0a33b. The current is orange #ff8a3d, the keyword cyan #7fe3ff.
- **Kit assets:** whatif/BergenHarbor (`time: night`), whatif/CurrentRibbon, explainer/You + whatif/RodLine, whatif/TitleCard, whatif/Hud (frame-0 state).
- **Payoff on screen:** it is the first 8 s; "GONE" pays off at the 0:08 flip, when the readout drops 35.0 to 0.0.

## B. "35 → 0 split" (before/after; recommended for the YouTube 16:9 and the Shorts shelf)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (the same subject twice, then and after, with 4 words in total) and J3XahLkDEzU LAST-HUMAN (a slanted split, the same place in each half, labels in the top corners). OXYGEN's baseline-delta readout (14.7 PSI to 11.6 PSI) supplies the number device.
- **Composition:** a slanted split with a white bar. The left half, labelled "SALTY", is underwater and healthy: a herring school in teal, kelp, salt glints. The right half, labelled "FRESH", is the same water under the glassy cyan overlay, where the same herring are puffed up and drifting down. The split bar is made of white salt crystals breaking off. A tiny "you" on the quay above the waterline in the right half gives the scale and the human.
- **Text (4 words):** **35 g/kg** (white, top-left corner plate) / **0.0** (red #ff5a4f, top-right corner plate). A heavy outlined number pair, no sentence.
- **Colours:** left teal #1b6f8f to #0b3550, right desaturated cyan (#bfeaff overlay), red only on "0.0", a white split bar, thick black outlines on the text.
- **Kit assets:** whatif/FishSchool (states `swell: 0` and `swell: 1`), whatif/Kelp, explainer/Ocean (underwater), core particles (glints), explainer/You (tiny), core grade.
- **Payoff on screen:** the readout drop is at 0:08 (inside 10 s); the swollen fish are at 0:24-0:31.

## C. "THE CURRENT STOPS?" (map hook; A/B variant only)

- **Inspired by:** _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM (a big text block over a simple map or diagram); 7696143265405488416 PI=3's "THE PLANET" chapter frame (one huge diagram owns the sky); OXYGEN's planted element given its own visual (the hydrogen cloud).
- **Composition:** the video's North Atlantic map (land #2a3b4c, sea #0f2a40). A thick orange Gulf Stream arrow sweeps from Florida up to a cyan "YOU" pin at Bergen. Its last third, north of Scotland, fades to grey dashes, and two blue sinking rings near Greenland are crossed out. Snow particles drift over Norway. A tiny "you" stands on the pin with a fishing rod, scaled like a map figure.
- **Text (3 words):** **THE CURRENT STOPS?** ("STOPS?" in cyan). The question mark keeps it honest: the video shows the northern branch stalling, not the whole Gulf Stream stopping.
- **Colours:** dark map blues against the orange arrow (an orange/blue complementary pair). The grey fade carries the change; snow is pure white so it reads at small sizes.
- **Kit assets:** explainer/Map (with the new `paths`, `rings`, `pins`; PLACES bergen, floridaStraits, labradorSea, nordicSeas), core particles `snow`, explainer/You (tiny).
- **Payoff on screen:** late (the map at 0:43, the status line at 0:55, the twist at 1:06). That breaks the 10 s library rule, so use C only as an A/B test against B, never as the TikTok cover.

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-oceans-turn-fresh/thumbs.json` with the variants `cover` (A), `split` (B) and `current` (C), then run `OUT=thumbs/whatif-oceans scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text must read at 120 px tall, and the moon reflection must not wash out the HUD in A.
