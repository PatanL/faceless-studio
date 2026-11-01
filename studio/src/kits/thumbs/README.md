# thumbs: code-rendered thumbnails (B6)

Remotion stills, 1280x720 (16:9, YouTube) and 1080x1920 (9:16, Shorts/TikTok cover).
Rendered on the Spark only (CPU, one Chrome tab, ~0.7 s per still).

## Formula (all templates)

- One **big subject** plus one **tiny human** for scale.
- **2-4 words**, Montserrat 900, white with a heavy black outline. The CLI warns outside 2-4.
- **One red accent**: the `accent` word (default: the last word). Explainer templates
  continue it as a hand-drawn red pointer to the tiny human (Depth Theory signature;
  `noArrow` turns it off). Nothing else is red: explainer art is white-on-black
  scratchboard, horror is a cold teal grade.

| niche | template | big subject | tiny human | default text idea |
|---|---|---|---|---|
| explainer | `eye` | creature head/eye fills 2/3, sonar rings | diver with torch | IT SEES YOU.. |
| explainer | `scale` | whole animal side-on (dives head-down in 9:16), ruler with `label` | diver at the snout + `humanLabel` | BIGGER THAN A BUS |
| explainer | `abyss` | angler lure in the dark, huge jaws below | diver drifting toward the light | NOT A LIGHT |
| horror | `door` | door ajar, too-tall figure in the gap, room `room` plate | resident under a ceiling light | DON'T OPEN IT |
| horror | `chat` | giant tilted phone with the `chat` lines (last one big) | resident in bed lit by the phone | WHO SENT THIS? |
| horror | `hallway` | figure in the foreground, cropped by the frame | resident far down the corridor | DON'T LOOK BACK |

Placeholder subjects: `whale` (sperm whale), `squid` (colossal squid), `angler`.

## Run

From the Mac (syncs code, renders on the Spark, pulls JPGs + contact sheets to `out/<OUT>`):

```bash
OUT=thumbs/ep01 scripts/thumbs_render.sh studio/src/kits/thumbs/samples/episode-example.json
```

On the Spark, in `~/studio/app/studio`:

```bash
node src/kits/thumbs/render.mjs spec.json [more.json] --out out/thumbs/x [--formats 16:9,9:16] [--png] [--sheet]
```

Output: `<id>_<niche>-<template>_<16x9|9x16>.jpg` (JPEG q90, all well under YouTube's 2 MB cap).
`remotion studio src/kits/thumbs/entry.ts` shows every template in both formats.

## Spec (`spec.ts`)

```jsonc
{
  "id": "colossal-squid", "niche": "explainer", "subject": "squid",
  "variants": [                      // one video -> 3 thumbnails; each variant merges over the base
    {"template": "eye",   "text": "IT SEES YOU..", "accent": "YOU.."},
    {"template": "scale", "text": "LONGER THAN A BUS", "accent": "BUS", "label": "14 M", "humanLabel": "YOU"},
    {"template": "abyss", "subject": "angler", "text": "DON'T SWIM DOWN", "accent": "DOWN"}
  ]
}
```

A spec without `template` or `variants` expands to all three templates of its niche.
Horror fields: `chat` [{from, text, me}], `chatTitle`, `room`. Any spec: `bg` (tone), `noArrow`.

## Using the episode kits' art

`art` (big subject) and `humanArt` (tiny human) take any component registered by
`src/kits/*` and draw it in the template's box at `time` seconds, e.g.

```json
"humanArt": {"component": "horror/Protagonist", "props": {"pose": "phone", "expr": "terrified"}, "time": 0.4}
```

(see `samples/kit-art-example.json`). The kits are picked up through `src/kits/index.ts`;
when `explainer/*` creatures are registered there, pass e.g. `"art": {"component": "explainer/<Creature>"}`.
Unregistered names fall back to the built-in placeholder, so specs never break.

## Files

`spec.ts` types + template list · `fx.tsx` engraving fill, grain, vignette, sonar, red arrow,
headline fit (real font metrics via `measure.ts`) · `art/` placeholder creatures and people,
`KitArt` bridge · `templates/` the six layouts · `Thumbnail.tsx`, `Root.tsx`, `entry.ts` the
Remotion root (separate from `src/Root.tsx`) · `render.mjs` the CLI · `preview/` contact sheets.
