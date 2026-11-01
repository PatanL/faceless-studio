# Thumbnail concepts: explainer-short-box-jellyfish

Three concepts, each rendered as a Remotion still on the Spark with the thumbs kit (1080x1920 cover plus 1280x720
for YouTube) and drawn with the same explainer art the video uses, so the cover matches the video. Thumbs-kit
rules apply (`studio/src/kits/thumbs/README.md`): one big subject plus one tiny human, 2-4 words in Montserrat 900,
white with a heavy black outline, one red accent word continued as a red pointer to the tiny human. Library rule
(`research/library/index_notes/explainer.md`, technique 10): the thumbnail adds a claim the title doesn't make, and
for Shorts frame 0 is the cover, so the cover must also read at phone size.

Kit gap for all three: the thumbs kit has explainer templates `eye`, `scale` and `abyss` but no jellyfish subject.
Until a `boxJellyfish` figure exists in `kits/explainer/marine.tsx`, pass the episode's bell + tentacle svgs as
`art` through the `KitArt` bridge (or add them as a thumbs placeholder subject). Listed per concept below.

## A. "IT'S ON YOU" (frame-0 cover; recommended for the 9:16 post and the Shorts shelf)

- **Inspired by:** fGcgWaswMns (Depth Theory, "IT HEARS YOU..": white words with one red word, a red hand-drawn arrow
  to a tiny human, a huge subject on near-black); XFFjxTllpoA (the frame-0 cover is a warning card that restates the
  premise, with the threat already present).
- **Composition:** the s01 hook frame, pushed in. Underwater just below a bright waterline (top 20%). The
  translucent bell fills the right two-thirds, rim glowing cyan; tentacles hang off-frame below. The stick-figure
  YOU treads water small at upper left, and one glowing tentacle crosses its leg. The red 2:00 Timer box sits
  top-right inside the safe area. Red arrow from the text to the leg contact.
- **Text (3 words):** **IT'S ON YOU** ("YOU" in red). The title says the clock; the cover says the contact.
- **Colours:** shallows teal #0f4c5c -> #062a33, waterline glare #e8fbff, bell #bff3ff at 40% with a #effdff rim
  and glow, red #e5483d (word, arrow, Timer border), white text with a black outline.
- **Kit assets:** template `eye` layout (subject right, human left) with `art` = the episode's bell + tentacle svgs
  (or `explainer/Ocean` surface 0.2 as `bg`); `humanArt` = `explainer/You` pose "stand"; `explainer/Timer` (from 120,
  rate 0) as an extra layer; fx red arrow.
- **Payoff on screen:** frame 0 shows exactly this; "your leg" at 0:01, "stuck to your shin" at 0:14.

## B. "2:00" clock split (best for YouTube 16:9 and an A/B against A)

- **Inspired by:** fGcgWaswMns (monster-vs-human scale contrast on black, one red word); jw6bS-WL4F4 (the cover is a
  single glowing translucent box jellyfish on dark green water, which still reads at thumbnail size with the
  presenter and a caption over it).
- **Composition:** left 55%: one big glowing box jellyfish on near-black, bell top-left, tentacles sweeping
  diagonally down and right toward a tiny YOU at bottom right. Right 45%: the giant red Timer box reading **2:00**,
  tilted -4 degrees, with the red arrow from the Timer to the tiny figure.
- **Text (2 words):** **2:00 LEFT** (the Timer face carries "2:00"; "LEFT" in white under it). Red is only the
  Timer.
- **Colours:** near-black #05121a with sparse marine snow, jellyfish #bff3ff with a cyan glow, timer panel #0b1820
  with a red #e5483d border and red digits, white "LEFT".
- **Kit assets:** template `scale` (subject on one side, human with `humanLabel` "YOU"), `art` = bell + tentacle svgs,
  `explainer/Timer` drawn large as a layer, `explainer/Ocean` depth 300 as `bg`.
- **Payoff on screen:** the Timer is on screen from frame 0 and the voice says "two minutes" at 0:02.

## C. "NOT A PLASTIC BAG" (scale/invisibility hook; test as a TikTok cover variant)

- **Inspired by:** jw6bS-WL4F4 (near-invisible jellyfish shown at real scale next to an everyday object; the
  "tiny but worse" paradox); 6mRR91AbxjQ (a close-up of the moment of contact, told as a mechanism).
- **Composition:** top-down view of clear shallow water over sand. A dinner plate (same svg as the 0:05 shot) lies
  at bottom left for scale; next to it, barely visible, the bell's rim outline at the same size with faint
  tentacles trailing toward the top of frame, where a tiny YOU's legs dangle in from the surface. A red ring circles
  the bell.
- **Text (4 words):** **CAN YOU SEE IT?** ("IT?" in red). It is a question the viewer answers by staring, which
  is the "almost clear" beat.
- **Colours:** sand #e8d9b5 under clear water #7fd3e6 at 30%, bell rim #ffffff at 50%, plate #f4f1ea, red ring and word.
- **Kit assets:** new top-down composition (no thumbs template fits; closest is `scale` with a custom `bg`), the
  episode's plate svg, the bell svg rotated to top-down (a circle rim: a small extra markup), `explainer/You` legs
  cropped.
- **Payoff on screen:** the plate comparison lands at 0:05 and "nearly clear" at 0:04, inside the 10 s rule. Weakest
  of the three at small sizes (low contrast is the point), so test it only as a variant.

## Render

Once the jellyfish art is reachable from the thumbs kit, write `episodes/explainer-short-box-jellyfish/thumbs.json`
with variants `onyou` (A), `clock` (B) and `seeit` (C), then run
`OUT=thumbs/box-jellyfish scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the
bell must read as an object at 120 px tall, and the Timer digits must read at 64 px.
