# studio — storyboard JSON -> MP4 (Remotion)

One composition, `Storyboard`, renders any storyboard JSON. Size, fps and length come from
the JSON (`format` "9:16" = 1080x1920, "16:9" = 1920x1080).

```bash
# from the repo root on the Mac: sync, render on the Spark (CPU, lock-serialized), pull MP4 to out/
PROPS=studio/storyboards/test-9x16.json scripts/spark_render.sh Storyboard test-9x16.mp4

# on the Spark, inside ~/studio/app/studio
npx remotion render src/index.ts Storyboard out/x.mp4 --props=storyboards/test-9x16.json --concurrency=8
npx remotion still  src/index.ts Storyboard out/x.png --props=... --frame=90
npm run validate -- storyboards/*.json            # zod check + summary
npm run validate -- --json-schema > storyboards/storyboard.schema.json
```

## Storyboard model (src/core/schema.ts is the source of truth)

- Times in seconds. Scene-local: layer keyframes, enter/exit, callouts, camera, scene `sfx`.
  Global: `captions.words`, `audio.*`. Scenes play back to back; a `transitionIn`
  (cut | fade | dipBlack | whip | glitch) is centred on the boundary and never changes length.
- Positions: px in composition space or `"NN%"`; (x, y) is the layer anchor (default centre).
- Scene = `background` (color | gradient | image | component, with parallax `depth`) +
  `layers` (rect | circle | text | image | svg | particles | component) + `camera`
  (keyframes x/y/zoom/rotate or a preset: pushIn, pullOut, panLeft/Right/Up/Down, drift;
  plus `shake` cues) + `callouts` (label | stat | banner | lowerThird | title, screen space)
  + `grade` (brightness/contrast/saturate/hue, tint, vignette, flicker).
- Layer motion: `keyframes` [{t, x, y, scale, scaleX, scaleY, rotate, opacity, ease}],
  `enter`/`exit` presets (fade, pop, slide*, zoomIn/Out, wipe*, drop), `idle` loops
  (bob, breathe, sway, float, pulse, spin, jitter), `depth` parallax (0 screen-locked, 1 world, >1 foreground).
- Captions: word timings -> 1-3 word pages (breaks on maxWords / maxChars / pauses / punctuation),
  big bold uppercase, active word highlighted (`color` or `box`), kept inside the platform
  safe area (`SAFE_AREA` in schema.ts). `captions.src` can point at a JSON file in `public/`.
- Audio: `voice` clips, `music` with fade in/out and ducking under speech (voice clip
  durations, else caption word timings), `sfx` cues by `src` or `cue` (`<sfxDir>/<cue>.wav`).

## Kits

A kit registers React components by name; storyboards use them as
`{"type": "component", "name": "explainer/Whale", "props": {...}}` (layer or background).

```tsx
import {registerComponent, type KitComponentProps} from '../../core/registry';
const Whale: React.FC<KitComponentProps> = ({props, time, width, height}) => <svg .../>;
registerComponent('explainer/Whale', Whale);
```

Then add `import './explainer';` to `src/kits/index.ts`. `src/kits/demo` is a minimal example.
Unknown names render a magenta "missing: name" box instead of crashing.
