# Thumbnail concepts: explainer-sinking-every-1000m

There are three concepts, all 16:9 (1280x720 shelf; the 9:16 crop is for Shorts promos only). Each one renders as a Remotion still on the Spark from `studio/src/kits/thumbs` (`Thumbnail.tsx`, templates `scale` / `abyss` / `eye`) using the same explainer kit art as the video, so the thumbnail and the video match.

Rules from the thumbs kit (`spec.ts`): one big subject, one tiny human for scale, 2-4 words of high-contrast text, exactly one red accent word, everything else desaturated.

Rules from the library (`research/library/index_notes/explainer.md` rows "Thumbnails" and rule 10):
- The text adds a claim the title does not make.
- White heavy condensed text with one red word, and a red arrow to a tiny human.
- Monster-vs-human scale contrast on near-black.

Reference thumbnails used:
- **fGcgWaswMns** (Depth Theory sperm whale, 2.31M, 14.65x): "IT HEARS YOU..", with a huge dark subject entering from one side and a tiny diver lower-left.
- **mzeN0BXR4e0** (Mr. Science, 17.22M, 12.86x): "WE / REALLY / CAN'T / EXPLAIN" stacked, with EXPLAIN in red, a huge pale creature and a tiny diver for scale.
- **nAWpLtG-kNs** (Fossil, 12.21M, 113.57x): a verdict/tier device as the visible promise; its board is the scoreboard idea behind concept B's gauge.

## A. "DIED 3 TIMES" (recommended, pairs with title 1)

- **Inspired by:** fGcgWaswMns (2-3 word claim with a trailing threat, tiny human lower-left) and mzeN0BXR4e0 (stacked words, last one red, tiny human against a huge dark field).
- **Composition:** template `abyss`, tall cross-section. A narrow column of water drops from a thin bright surface strip (top 8%) into near-black; a red dashed line at the very bottom labelled 10,935 M. The tiny YOU (orange heated suit, 40 px tall) on the yellow sled sits two-thirds down, with a red hand-drawn arrow from the text. Along the left edge, three small red X stamps step down the column at 3 km, 6 km and 8.3 km (the three deaths). Right third: the text.
- **Text (3 words):** **DIED 3 TIMES** stacked, "3" in red (the accent), heavy condensed white with a black outline.
  - New claim: the title asks "how many times"; the thumbnail answers with a number, which is the curiosity hook. Viewers click to see how you survived dying three times. It is also true: it is the board's final reading.
- **Colours:**
  - water #0d3b45 at the top -> #04161b -> #020608
  - surface strip #9fd3ff
  - YOU orange #ff8a2a (the only warm colour besides the red)
  - sled #f2c230 (small)
  - X stamps and the "3" red #e5483d
  - text white #f3f6f7
- **Kit assets:**
  - `explainer/Ocean` (depth gradient, surface strip) as the background
  - `explainer/You` with `color: "#ff8a2a"` as `humanArt`
  - the sled SVG from `gen_storyboard.py` (SLED)
  - `explainer/DepthMeter` cropped to the bottom marker (10,935 M)
  - red X stamps: the `AliveMeter` NO stamp drawing once it is built, otherwise a text "X"
- **Thumbs CLI:** `{niche: 'explainer', template: 'abyss', text: 'DIED\n3 TIMES', accent: '3', humanArt: {component: 'explainer/You', props: {color: '#ff8a2a', pose: 'panic'}}, label: '10,935 M'}`

## B. "0 CHEATS LEFT" (pairs with title 2; best A/B partner for A)

- **Inspired by:** nAWpLtG-kNs (the scoreboard device as the promise) and fGcgWaswMns (dark field, one subject, tiny human, short threat text).
- **Composition:** template `eye`, re-skinned. The big subject is the ALIVE? gauge, filling the left 55%: a half-dial from green YES through yellow "?" and orange BARELY to red NO, with the needle pointing just short of NO. Right: the tiny YOU on the sled near the bottom, a red arrow from the text to YOU, and a faint snailfish silhouette turning away above YOU (the last fish leaving). Near-black background with a few blue bioluminescent dots.
- **Text (3 words):** **0 CHEATS LEFT**, with "0" in red.
  - New claim: the title promises deaths; the thumbnail adds the game rule (cheats) and says you are out of them, which implies the next death is final.
- **Colours:**
  - background #04161b
  - gauge arc green #3ecf6e / yellow #ffe14d / orange #ff9a2a / red #e5483d (the gauge is the only saturated element besides the "0")
  - needle white
  - YOU and text white
- **Kit assets:**
  - `explainer/AliveMeter` (new kit component, see script.md "Kit work") as `art`, props `{state: 'BARELY', size: 2}`
  - `explainer/You` as `humanArt`
  - `explainer/Snailfish` at `silhouette: '#1b2a33'`
  - particles `stars` in #5fd3ff
  - Needs AliveMeter to be built first. Until then, render this concept from the storyboard still at 8:18 (s74_last_test) as a mock.

## C. "IT GOT HERE FIRST" (pairs with title 8; re-upload / Short promo only)

- **Inspired by:** mzeN0BXR4e0 (a pale subject lit in the dark, with the text claiming something strange) and fGcgWaswMns ("IT ..." pronoun text with the subject withheld).
- **Composition:** template `scale`. The seabed at the bottom 30%, lit by an ROV light cone from the top right. In the light, a white crumpled shape half-buried in mud. It is drawn as the plastic bag, but at thumbnail size it reads as a pale creature, so the bag is not spoiled. The tiny YOU on the landed sled stands at the left edge of the light, facing it, with a red arrow from the text to the shape (not to YOU, which breaks the template on purpose: the shape is the subject).
- **Text (4 words):** **IT GOT HERE FIRST**, with "FIRST" in red.
  - New claim: someone or something reached the bottom before you, which opens a mystery loop. It spoils the twist, which is why it is ranked third and limited to a re-upload or Short.
- **Colours:**
  - mud #3b2f28
  - water #02060a
  - light cone #fff6d8 at 30%
  - the shape #f3f6f7
  - YOU orange
  - "FIRST" and the arrow red
- **Kit assets:**
  - MUDFLOOR, ROV_LIGHT and BAG SVGs from `gen_storyboard.py`
  - `explainer/You` (`color: '#ff8a2a'`)
  - the sled SVG
- **Thumbs CLI:** `{niche: 'explainer', template: 'scale', text: 'IT GOT HERE\nFIRST', accent: 'FIRST', art: {component: 'svg:BAG'}, humanLabel: 'YOU'}`. The bag is an inline SVG, so pass it as a static image layer; the `scale` template's ruler is hidden.

## Checks for all three

- The text never repeats the title's words ("ocean", "kill", "bottom").
- The red accent is a single word or number.
- YOU is visible at 120 px wide (YouTube mobile shelf): scale the sled and YOU to at least 6% of the frame height and put the arrow on them.
- Render on the Spark only (`scripts/thumbs_render.sh`); look at the PNGs before choosing.
