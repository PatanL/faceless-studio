# Thumbnail concepts: explainer-short-cookiecutter-shark

Three concepts, each a Remotion still rendered on the Spark only, built from the same svg art as the video (the `CC_SIDE` hero and its overlays, `SKIN_WALL_HUMAN`, `RING`, `HOLE` from `gen_storyboard.py`), so the cover and the video match. The thumbs-kit formula applies (`studio/src/kits/thumbs/README.md`): one big subject plus one tiny human, 2-4 words in Montserrat 900 with a heavy black outline, and one red accent word. The thumbs kit has no cookiecutter subject. Its placeholders are whale, squid and angler. So each concept lists what an `explainer` template needs: an `svg` subject slot that takes the `CC_SIDE` markup. Library rule: the cover's words must pay off on screen within about 10 s.

## A. "Latched" (recommended: TikTok cover and Shorts first frame)

- **Inspired by:** 6mRR91AbxjQ FLY. Its effective thumbnail is frame 1: the creature itself, macro, on a skin plane against a flat backdrop (library card `research/library/videos/6mRR91AbxjQ.json`). PLAYBOOK hook rule: the subject is on screen in frame 1.
- **Composition:** this is the video's frame 0 (rendered and checked at 0.0 s). A human-toned skin wall fills the lower 45%. The dark cookiecutter, 880 px long, is diagonal at 55° and latched mouth-first into the wall, with a yellow ring at the bite and its green belly glow on. To the right is one finished round hole with a yellow ring. The text sits in the upper third. For the thumbs-kit "tiny human" rule, add a small `You` silhouette standing on the far edge of the skin wall: the skin is someone's, and the shark is huge next to them.
- **Text (2 words):** **PERFECT CIRCLES**, with CIRCLES in red (kit Headline `red` prop).
- **Colours:** ocean teal gradient (the explainer Ocean, depth 30), skin #e0b294 → #b98262, shark #3b2c25, belly glow #3dff9a, ring #ffe14d, red #e5483d on CIRCLES only.
- **Kit assets:** explainer/Ocean, svg `CC_SIDE` + `CC_GLOW` + `RING` + `HOLE` + `SKIN_WALL_HUMAN`, explainer/Headline, explainer/You.
- **Payoff on screen:** immediately, because the voice says "perfect circles" at 0:01.6 over this exact picture, and the last frame (1:14.9) returns to it.

## B. "Speck on a whale" (YouTube 16:9 and the Shorts shelf)

- **Inspired by:** jw6bS-WL4F4 JELLY (the tiny subject next to an everyday object for scale, 0:10-0:13, so the paradox is the picture) and the thumbs-kit `scale` template (whole animal side-on, tiny human, ruler).
- **Composition:** a blue whale side-on fills the frame width (explainer/BlueWhale at honest pxPerM). On its front flank a 0.5 m shark at the same scale is just a speck, circled in a thick yellow ring. A red hand-drawn pointer (the kit signature) runs from the text to the ring. Inset at bottom-right: the same shark at 1:1 over a forearm silhouette, labelled 50 CM, so the viewer gets both scales.
- **Text (3 words):** **IT BITES WHALES** ("WHALES" in red). Optional 4-word variant: **SHORTER THAN YOUR ARM**.
- **Colours:** ocean teal, whale #8f9aa4 with darker mottling, yellow ring, white text with a black outline, red on one word.
- **Kit assets:** thumbs `scale` template (subject = BlueWhale), svg `CC_SIDE` at width 0.5 × pxPerM, `RING`, `FOREARM`.
- **Payoff on screen:** the whale speck shot is at 0:01.1-0:01.8 and again at 0:22.7, and "even a whale" is spoken at 0:22.3. The cover word lands in the first 2 s.

## C. "The hole" (A/B test against A)

- **Inspired by:** XFFjxTllpoA PUFFER (first frame = one full-bleed symbol, the hazard sign, with a short text block, library card) and the PLAYBOOK "show the result first" hook H9 (Ky0XPonYDcc EEL: the absurd true outcome as the image).
- **Composition:** a full-bleed close-up of human-toned skin with one perfect dark round hole in the centre, ringed in glowing yellow. A thumb silhouette next to the hole gives depth scale (the 7 cm fact). The shark is only a small dark silhouette leaving the frame top-right, with its green glow trail. There is no gore: the hole is a flat dark disc, as in the video's shot 29.
- **Text (3 words):** **A SHARK DID THIS** ("SHARK" in red), 4 words.
- **Colours:** skin #e0b294, hole #140707 with a #5a2b28 edge, ring #ffe14d, glow #3dff9a, red on one word.
- **Kit assets:** svg `SKIN_WALL_HUMAN`, `HOLE`, `RING`, `THUMB_SIL`, `CC_SIDE` (small, silhouette fill), thumbs `explainer` text block.
- **Payoff on screen:** the hook says it at 0:00-0:02.4, and the exact image appears at 0:48.1-0:49.6 (the purpose reveal). It is a strong curiosity gap, but the image itself is late, so use C only as a YouTube A/B variant, never as the TikTok cover.

## Render

When the thumbs kit has an svg-subject slot, write `episodes/explainer-short-cookiecutter-shark/thumbs.json` with the variants `latched` (A), `speck` (B) and `hole` (C). Then run `OUT=thumbs/explainer-short-cookiecutter-shark scripts/thumbs_render.sh <spec>` (it renders on the Spark). Check the contact sheet at phone size: the ring has to read at 120 px tall, and the shark must not merge into the dark ocean (keep the green belly glow on).
