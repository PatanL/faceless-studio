# House style: A (owner pick, 2026-11-01)

The look of every explainer, in code and in Codex art direction. The reference image is
`experiments/asset-gen/gen/style_board_A.png`: when in doubt, match it. Inspired by Kurzgesagt's flat frames; our
characters, assets, compositions and branding stay our own (FEEDBACK.md principle 7).

## Rules

- **Flat 2D.** Big, simple, rounded-geometric shapes with crisp edges. Each shape is one solid colour. No gradients,
  blur, texture, brush strokes or outlines.
- **Shading:** one flat shadow shape per object (a darker tone of its own colour, on the side away from the light).
  At most a few small flat glints. Light sources may have one flat halo ring.
- **Depth:** 3–5 flat layers per scene; far layers paler and less saturated. Never haze or blur.
- **Palette:** saturated, never photographic. Base swatches from the board (each gets a darker shadow tone and a
  lighter tint in code):
  `#250192` indigo-ink · `#0024fd` royal blue · `#01aefd` sky cyan · `#0de9e0` aqua · `#0bd4a4` sea green ·
  `#fddf35` sun yellow · `#fc6e0e` orange · `#fa302a` red · `#fb17b8` magenta · `#932efc` violet.
  Plus bone white for orca patches, foam and ice. Deep water and night skies are indigo/violet, not black.
- **Water:** flat colour bands; light rays, if any, are a few hard-edged translucent stripes; waves are simple
  flat curves.
- **Detail:** sparse. Lots of calm empty space; detail comes from a few distinct objects, not fine marks.
- **Creatures:** few large rounded parts, correct anatomy and markings, one shadow shape, a small eye with one glint.

## Making art direction with Codex

In `experiments/asset-gen`: write a short plain description of the scene (what is where, and why), append
`prompts/style_A_common.txt`, and run with the board attached:

```bash
REF=$PWD/gen/style_board_A.png ./gen_one.sh $PWD/prompts/<name>.txt <out-name>
```

Codex images are art direction only; what moves on screen is built in code.
