# Thumbnail concepts: whatif-breathe-underwater

There are three concepts. Each one is rendered as a Remotion still on the Spark (thumbs kit, 1280x720 for YouTube plus 1080x1920 for the Shorts cover) from the same kit art the video uses, so the cover matches the video. Thumbs-kit rules apply (`studio/src/kits/thumbs/README.md`): one big subject plus one tiny human, 2-4 words in Montserrat 900 white with a heavy black outline, and one red accent (#E5484D, the video's caption red), carried on into the kit's hand-drawn red pointer to the tiny YOU. Library rules (`research/library/index_notes/whatif.md`): a heavy rounded sans, a before/after pair often works, and the thumbnail word or number should pay off on screen within about 10 s. Because the premise is familiar (PLAYBOOK §10C), every concept leads with our angle (depth, the one-way trip, your own blood), never with "a person breathing underwater" alone.

The thumbs kit has only explainer and horror templates, so each concept lists the layers a `whatif` template needs. B can be approximated today with the explainer `abyss` template; A can be approximated with the explainer `scale` template, with the ruler as the subject.

## C. "0 M / 11 KM" split (recommended for the 16:9 YouTube main, pairs with title 1)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (two equal halves, the same subject before/after, "TODAY" / "50 YEARS LATER", 4 words in total, 107x outlier) and J3XahLkDEzU LAST-HUMAN (a slanted split with the hero in the same pose in both halves).
- **Composition:** a slanted white split bar. **Left half:** dusk split waterline: the lit ferry rail across the top, YOU mid-jump (`pose: panic`) just above the water, remora silhouette on your back. **Right half:** the same YOU in the same pose, standing on pale Challenger Deep mud in near-black water, a ring of amphipods around the feet and one red fibre drifting past the face. Each half has a tiny HUD depth readout in its top-left corner, taken from the video HUD.
- **Text (4 words):** **0 M** over the left half, **11 KM** over the right half ("11 KM" red). The two numbers are the before/after labels.
- **Colours:** left = violet-orange dusk sky (#4B3C78 -> #F2A15C) over teal water (#0E5A6B); right = blue-black (#04131A -> #000) with grey mud (#6E6A63). The only red is "11 KM", the fibre and the pointer.
- **Kit assets:** whatif/Ferry, explainer/Ocean (`surface` on the left, `depth: 10935` on the right), explainer/You x2, whatif/Fish (`remora`), explainer/Krill x6 (amphipods), the seafloor SVG string from `gen_storyboard.py`, whatif/Hud (readout only), thumbs pointer.
- **Payoff on screen:** "0 M" is on the HUD from frame 1. "11 KM" is spoken at 6:54 and drawn as the 10,935 route tick at 0:28. The "never come back up" gap in title 1 is stated at 0:16.

## A. "11 KM DOWN" (recommended 9:16 Shorts cover; pairs with titles 2 and 3)

- **Inspired by:** _lu85gSD39k BILLION-YEARS (a tiny hero dead centre and a big number phrase as the text block: "1 BILLION / YEARS."); our explainer thumbs `scale` template (a ruler with a `label` as the subject, tiny diver for scale); PLAYBOOK §10D (a ladder the viewer can see the length of).
- **Composition:** the whole water column as one vertical slice. A full-height DepthMeter ruler down the left edge (white ticks, the red 10,935 tick at the bottom, and the red 8,200 "wall" tick two-thirds of the way down). The tiny lit ferry sits at the very top edge. YOU is a speck standing on the trench floor at the bottom centre, with the red pointer. Halfway up, the remora silhouette drifts back toward the light. The trench walls narrow toward the bottom. In 9:16 this fills the frame naturally; in 16:9 the ruler goes horizontal-diagonal and the text block moves to the right half.
- **Text (3 words):** **11 KM DOWN** ("DOWN" red), in the upper third under the ferry.
- **Colours:** a teal-to-black gradient (#0E5A6B -> #04131A -> #000); white ruler and text; red only on DOWN, the 8,200 and 10,935 ticks and the pointer.
- **Kit assets:** explainer/Ocean (depth gradient), explainer/DepthMeter with the new `marks` prop, whatif/Ferry, explainer/You, whatif/Fish (`remora`), the trench-wall SVG strings, thumbs pointer.
- **Payoff on screen:** the route ruler with the 10,935 tick appears at 0:28 (outside the ~10 s rule; the map with the destination lands at 0:20), and the depth meter moves from 0:31. That's why A is the Shorts cover and C the main.

## B. "IT'S YOUR BLOOD." (A/B variant; carries title 7's twist as copy)

- **Inspired by:** y300HjYnHPw 10X-FASTER (the hero plus one huge number badge top-right, the "10x" device); DK4EOHCrVvM WEALTH (a glowing number pill over a person as the hook); our explainer thumbs `abyss` template (an anglerfish lure in the dark with a diver drifting toward it).
- **Composition:** black water at 1,000 m. An anglerfish lure glows in the lower-left corner, the decoy monster, with its jaws cropped by the frame. YOU fills the right-centre at medium scale, frost-blue tint, three gill slits on the neck, arms wrapped around yourself. The BODY readout from the HUD is blown up huge beside the head: **33.9°C** in red with the thin 35° HYPOTHERMIA line under it. The red pointer runs from the text to the readout, not to the fish.
- **Text (3 words):** **IT'S YOUR BLOOD.** ("BLOOD." red).
- **Colours:** near-black (#03090D) with cyan bioluminescent specks (#6FE3FF); YOU in pale frost blue (#CFE3F2); red only on BLOOD and the readout.
- **Kit assets:** explainer/Anglerfish, explainer/You (`color: #CFE3F2`), whatif/GillDiagram head-profile slits (or three stroked lines), whatif/Hud BODY readout in `focus: temp` mode, a stars `particles` still, thumbs pointer.
- **Payoff on screen:** the BODY readout is visible from frame 1 and starts falling at 0:04, so the number pays off within the 10 s rule. The meaning lands at the rug pull (2:41). It's the most curiosity-driven variant, but it gives away the twist, so test it against C rather than lead with it.

## Render

Once the thumbs kit has a `whatif` template (or the explainer templates take extra layers), write `episodes/whatif-breathe-underwater/thumbs.json` with variants `split` (C), `column` (A) and `blood` (B), then run `OUT=thumbs/whatif-breathe scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text has to read at 120 px tall, and in A the tiny YOU on the trench floor needs its pointer to be visible at all.
