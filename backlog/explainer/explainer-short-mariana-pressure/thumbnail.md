# Thumbnail concepts: explainer-short-mariana-pressure

Three concepts. Each is rendered as a Remotion still on the Spark with the thumbs kit (1080x1920 cover plus 1280x720 for YouTube) and drawn with the same flat art the video uses, so the cover matches the video.

Thumbs-kit rules apply (`studio/src/kits/thumbs/README.md`):
- one big subject plus one tiny human;
- 2-4 words in Montserrat 900, white with a heavy black outline;
- one red accent word, continued as a red pointer to the tiny human.

For a Short, frame 0 is the cover, so the cover has to read at phone size. Concept A is built from frame 0 for that reason.

Kit gap for all three: the thumbs kit's explainer templates (`eye`, `scale`, `abyss`) have no trench, breath-bubble or can subject. Pass the episode's svg markups (trench section, Everest, can upright/crushed, the breath `circle`) through the `KitArt` bridge as `art`, the same way the box-jellyfish cover does. These markups are defined in `gen_storyboard.py` (SVG_TRENCH, SVG_EVEREST, SVG_CAN, SVG_CAN_CRUSHED).

## A. "YOU WON'T IMPLODE" (myth-bust cover; recommended for the 9:16 post and the Shorts shelf)

- **Inspired by:**
  - fGcgWaswMns (Depth Theory, "IT HEARS YOU..."): white words with one red word, a red hand-drawn arrow to a tiny human, a huge dark space;
  - mzeN0BXR4e0 (DEEP): a giant pale subject, a tiny diver and a 4-word stacked claim with one red word ("WE / REALLY / CAN'T / EXPLAIN");
  - fmZfphacPPQ (PRESSURE): a lone figure in a dark water column.
- **Composition:**
  - The trench cross-section fills the frame, near-black at the bottom. A tiny grey YOU stands on the trench floor (bottom third).
  - Beside YOU, a sealed can crushed flat to the same height, so the contrast reads at once: the can lost, you didn't.
  - The log depth meter runs on the left edge with all six pins red and "x1,072" stamped at the bottom.
  - Red arrow from the accent word to YOU.
- **Text (3 words):** **YOU WON'T IMPLODE**, with "IMPLODE" in red and a thin white strike-through, so it reads as "the thing everyone says, crossed out". The title says the myth-bust and the cover shows the proof object (the crushed can).
- **Colours:** water #2b8197 -> #10465a -> #02080c (the Ocean kit gradient); trench rock #1a1410 with a #5c4a3a edge; YOU #f3f6f7 with a #0b1a22 outline; can #c8d2da with a red #e5483d band; red #e5483d (word, arrow, meter pins); white text with a black outline.
- **Kit assets:** template `abyss` layout (dark field, tiny human low) with `art` = SVG_TRENCH + SVG_CAN_CRUSHED; `humanArt` = `explainer/You` pose stand; the meter as an extra layer (copy the meter() layers from gen_storyboard.py with every pin stamped); fx red arrow.
- **Payoff on screen:** the implode myth is planted at 0:10.5, the can is crushed at 1:04.6, and "you never imploded" lands at 1:00.4.

## B. "YOUR LAST BREATH" (breath-bubble split; best for YouTube 16:9 and an A/B against A)

- **Inspired by:**
  - jw6bS-WL4F4 (JELLY): one translucent subject on dark water that still reads at thumbnail size;
  - fGcgWaswMns: the scale contrast, with the big thing on one side and the tiny human on the other;
  - XFFjxTllpoA (PUFFER): a frame-0 warning card that restates the premise.
- **Composition:**
  - Split left/right.
  - Left 50%: bright surface water, a huge breath bubble (glassy circle, white rim) beside a small YOU, label "100%".
  - Right 50%: black water at the trench floor, the same YOU and a bubble the size of a pea next to a teaspoon, label "0.09%".
  - A red arrow from the big bubble to the pea. The split line is the depth meter, running from 0 M at the top to 10,935 M at the bottom.
- **Text (3 words):** **YOUR LAST BREATH**, with "BREATH" in red. The title says the place; the cover says what gets crushed.
- **Colours:** left #2b8197 with light rays and a sky band #e8f6f8; right #02080c with sparse marine snow; bubble #bff3ff at 28% with a white rim; teaspoon #d9e2e8; red #e5483d.
- **Kit assets:** template `scale` (subject left, tiny human right with `humanLabel` "YOU"), `explainer/Ocean` depth 0 surface 0.22 and depth 10935 as two `bg` halves, the breath `circle`, SVG_SPOON, `explainer/You` pose stand.
- **Payoff on screen:** the bubble is in frame 0 ("YOUR AIR 100%"), shrinks at every stop, and "one teaspoon" is at 0:51.9.

## C. "DEEPER THAN EVEREST" (landmark scale; test as a TikTok cover variant)

- **Inspired by:**
  - mzeN0BXR4e0 (DEEP): the Everest-in-the-trench image, its single most memorable scale shot (13:02-13:07);
  - fmZfphacPPQ (PRESSURE): a landmark shown top to bottom at the final number (0:27);
  - fGcgWaswMns: the tiny human with a red arrow.
- **Composition:**
  - Full-height trench cross-section. Everest in grey with a white snowcap stands inside it at an honest 81% of the column, and its peak is still well under the waterline.
  - A red bracket "~2 KM" above the peak.
  - A tiny white YOU dot on the trench floor next to Everest's base, with a red arrow from the text down to it.
- **Text (3 words):** **DEEPER THAN EVEREST**, with "EVEREST" in red.
- **Colours:** water gradient #2b8197 -> #02080c, rock #1a1410, mountain #6b6f76 with a #ffffff cap and outline, red #e5483d, white text.
- **Kit assets:** template `scale` with `art` = SVG_TRENCH + SVG_EVEREST, `humanArt` = a white `circle` with `humanLabel` "YOU", no ruler label.
- **Payoff on screen:** "drop Everest in beside you" at 0:52.9 (71%). This is the weakest concept for the myth-bust title, and the Everest-in-the-trench image is common (DEEP and several competitors use it), so test it only as a variant.

## Render

Write `episodes/explainer-short-mariana-pressure/thumbs.json` with the variants `implode` (A), `breath` (B) and `everest` (C). Then run `OUT=thumbs/mariana-pressure scripts/thumbs_render.sh <spec>` (Spark only).

Check the contact sheet at phone size:
- the crushed can and YOU must both read at 120 px tall;
- "0.09%" must read at 64 px;
- the strike-through on "IMPLODE" must not hide the word.
