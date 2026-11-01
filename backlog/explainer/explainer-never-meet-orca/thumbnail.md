# Thumbnail concepts: explainer-never-meet-orca

Three concepts for the 16:9 YouTube thumbnail (1280x720), rendered as Remotion stills on the Spark with the thumbs kit (`studio/src/kits/thumbs`) and the same explainer art the video uses, so thumbnail and video look the same. Thumbs-kit formula: one big subject, one tiny human, 2-4 words in Montserrat 900 with a heavy black outline, exactly one red accent word that continues as the hand-drawn red pointer.

Reference thumbnails studied (structure only, nothing traced):
- **fGcgWaswMns** (Depth Theory, 2.31M, 14.65x): black field, huge whale head from the right, tiny diver lower-left, sonar arcs, "IT HEARS YOU.." with the last word red, red arrow to the diver (`research/library/videos/fGcgWaswMns.json`).
- **VtrcKTkhDHU** (OctoLab, 8.29M, 318.82x): pure black; three orcas head-on in a row (centre one biggest, red eyes, teeth); "WE CAN'T EXPLAIN" across the top, last word red. It states an admission, not a label (pulled from YouTube via the Spark into `~/studio/refs/thumbs/`, studied only).
- **JkAcCdqYJN0** (Occam, 332K, 15.82x): white field, a "menu" of three threats each holding a tiny panicked stick human, mascot with a stopwatch, no text.
- **mzeN0BXR4e0** (17.2M) and **PsEZl1iV1h8** (library): stacked "WE / REALLY / CAN'T / EXPLAIN", last word big and red, tiny diver for scale.

Rules carried over: the text adds a claim the title doesn't make; the human is tiny; nothing is red except the accent word and pointer. The pilot's thumbnails already use "IT CHOSE NOT TO", "0 HUMAN KILLS" and "WHY NOT YOU?" (`episodes/explainer-orca/thumbs.json`), so none of those words are reused here.

## A. "THEY DECIDED." (recommended primary, pairs with title 1)

- **Inspired by:** VtrcKTkhDHU (three orcas head-on on black, an admission line instead of a label) and fGcgWaswMns (one tiny human, a red pointer to it, the threat already knows).
- **Composition:** near-black navy field (#05080b to #0b1a22). Three kit Orca heads head-on (`pose: "head"`): the centre one fills about 60% of the frame height, the two side ones at 70% scale and slightly behind, all looking down. Bottom centre, small: the yellow kayak with the seated stick-figure YOU (about 6% of the frame height). It's the only warm colour, so the eye lands on it. Faint white sound rings rise from under the kayak. The red pointer runs from the accent word down to the kayak.
- **Text (2 words):** **THEY DECIDED.** "THEY" white, "DECIDED." red, top-left over the dark field, two lines.
- **Colours:** black / navy, white orca patches, kayak #f2c230, one red #ff1f1f (word + pointer).
- **Kit assets:** thumbs `eye` template with `art: {component: "explainer/Orca", props: {pose: "head", idle: false}}`; the side heads and the kayak need two extra art slots, which the `eye` template doesn't have. Until it does, render the centre head only and set `humanArt` to `explainer/You` (`pose: "stand"`) with `humanLabel: "YOU"`.
- **Payoff on screen:** 0:25.8 ("deciding something about you"), and the title line at 9:40.

## B. "THREAT FILE: ORCA" (channel signature; the series look)

- **Inspired by:** JkAcCdqYJN0 (a tableau "menu" of threats with tiny humans) and the document stamps and strike-through lists in fGcgWaswMns. The folder itself is ours: the originality review asked for a signature element so the channel doesn't read as a Depth Theory clone.
- **Composition:** a dark teal dossier folder, slightly rotated, fills the frame. Six tabs run along the top (BODY, SPEED, PLAN, WAVE, SHARKS, GIANTS), each with a small red stamp. A polaroid of a side-view orca is paper-clipped to the folder, with a big red stamp "0" across the corner of the photo. Clipped at bottom-right is a smaller polaroid of the tiny kayak + YOU, with a green tick. The red pointer runs from the title word to the YOU polaroid.
- **Text (3 words):** **THREAT FILE: ORCA**, "ORCA" in red. Every episode in the series swaps only the animal word and the photo.
- **Colours:** folder #0f1d24 with #8fb3c0 edges, white tab text, red stamps, green tick; the polaroids are off-white.
- **Kit assets:** the `folder_svg` / `chip_svg` markup from `gen_storyboard.py`, kit Orca (side), kit You, the KAYAK markup. This needs a new thumbs template `file` (tier L for the thumbs kit; the video itself needs no new component). Build it once, since every THREAT FILE episode reuses it.
- **Payoff on screen:** the folder opens at 0:55 and the corner chip is on screen from 0:43.

## C. "EVERYTHING BUT YOU" (paradox menu; A/B against A)

- **Inspired by:** JkAcCdqYJN0 (white field, a row of threats, tiny humans) and VtrcKTkhDHU (paradox text). The menu idea is also the video's own running gag ("never ordered one", the family menu).
- **Composition:** a light ice-blue field (#e3f1f6) to stand out from the black orca thumbnails in the feed. A huge kit Orca side view runs left to right across the lower half, mouth toward the right. Above it, a row of four prey cut-outs, each with a red X: great white, blue whale (small, to show it's a "menu"), seal, herring ball. On the far right sits the tiny kayak + YOU with a green tick, and the red pointer runs from "YOU" to it.
- **Text (3 words):** **EVERYTHING BUT YOU**, "YOU" red.
- **Colours:** light field, orca black/white, prey in greys, one red word and pointer, small green tick.
- **Kit assets:** thumbs `scale` template with `art: {component: "explainer/Orca"}`, `humanArt: explainer/You`, `label` off; prey icons from the kit (GreatWhite, BlueWhale, Seal) need an extra-art slot like A.
- **Payoff on screen:** the three credentials at 0:43 (beach, great whites, blue whale) and the menu card at 8:02.

## Render

Add `episodes/explainer-never-meet-orca/thumbs.json` with variants `decided` (A, `eye`) and `menu` (C, `scale`) now. Add `file` (B) once the thumbs kit has the `file` template. Run `OUT=thumbs/explainer-never-meet-orca scripts/thumbs_render.sh <spec>` (renders on the Spark only), then check the contact sheet at phone size (about 168 px wide in the feed). The kayak must still read as a yellow boat with a person in it, and the text must stay legible.
