# asset-gen: Codex image model → vector assets

> **House style A is locked (owner, 2026-11-01): see `docs/HOUSE_STYLE.md`.** Prompts append `prompts/style_A_common.txt` and attach `gen/style_board_A.png` as `REF`. The v3 note below still describes how to write the scene part.
>
> **Earlier default prompt style: v3.** Write a short plain description of the scene (what is where, and why it is there), then append `prompts/style_v3_common.txt`, and attach style frames with `REF=$PWD/refs/ks_grid.jpg ./gen_one.sh $PWD/prompts/<name>.txt <out>` (absolute paths). Don't list hex codes, lighting recipes or "dozens of marks": the v1/v2 prompts below did, and got dense painterly art that suits illustration, not 2D animation. Use whole-scene images as art direction for a setting; our own code-built characters stay on screen.

Question: can an image model supply Kurzgesagt-level detail density (bible §8), and which conversion path turns its output into something our code can animate?

Nothing in `studio/src/` or `pipeline/` was touched. The work reads `../kurz-style/engine/src/lib/color.ts` and `../kurz-style/tools/tis/frame_metrics.py` but never edits them. Everything ran on the Mac and stayed light: Codex calls, vtracer, and rsvg stills. Nothing was rendered with Remotion, so the Spark was never used.

## 1. Codex image generation (works, non-interactive)

```bash
./gen_one.sh prompts/<name>.txt <out-name>     # -> gen/<out-name>.png, log in logs/
```

- The script wraps `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex exec --skip-git-repo-check -s read-only - < prompt`. The prompt tells Codex to use its image tool and reply with only the saved path.
- Codex saves the image to `~/.codex/generated_images/<session>/exec-*.png`, and the script copies it into `gen/`.
- `image_generation` is a stable feature that is already on. The script changes no config and passes no credentials.
- Each image takes about 40–60 s and comes out at 1536×1024 (3:2) or 941×1672 (9:16).
- The `codex` on PATH, `~/.nvm/.../@openai/codex`, is broken because its vendor binary is missing. Use the bundled CLI instead.

The prompts (`prompts/`) describe technique only and name no brands: flat vector, no outlines, a hard hue-shifted terminator, a warm key with a cyan rim, and dense micro-marks.

| file | verdict |
|---|---|
| `gen/a_orca_side_v1.png` | Rich marks, but the tail is a vertical shark tail (wrong anatomy), so it was regenerated |
| `gen/a_orca_side_v2.png` | **Used.** Correct horizontal flukes, flatter fills, amber top edge and cyan rim |
| `gen/b_orca_head_v1.png` | Strong: teeth, tongue, rake scars, ring spots, wet glints. Slightly painterly |
| `gen/c_reef_9x16_v1.png` | Very dense but painterly (brush texture), so it was regenerated |
| `gen/c_reef_9x16_v2.png` | **Used.** Cleaner shapes, 40+ named objects, calm open water in the upper third for a hero |
| `gen/d_diver_v1.png` | Good original diver with buckles, hoses, gauges and a torch. Has a tiny pseudo-logo on the chest; crop or paint it out |
| `gen/e_fish_sheet_v1.png` | 16 fish in a grid. The tang and the anemonefish are real species, but they sit close to famous film fish, so prefer redesigned colourways if they ever become characters |

## 2. Path A: auto-vectorize (vtracer)

`scripts/vectorize.py` runs three presets and records path count, SVG size and fidelity (PSNR against the PNG). Outputs go to `vec/`. The reef SVGs and PNGs are gitignored; rerun the script to rebuild them.

| asset | coarse | medium | fine |
|---|---|---|---|
| orca | 25 paths, 56 KB, 27.5 dB; **fins merge into the body** | 247 paths, 159 KB, 28.8 dB | 1,592 paths, 459 KB, 29.9 dB |
| reef | 461 paths, 1.7 MB, 17.6 dB; mush | 6,545 paths, 4.9 MB, 20.5 dB | 27,050 paths, 9.5 MB, 22.8 dB; light rays posterize into bands |

At medium and fine, the result looks almost identical to the PNG. But it is a stack of colour blobs. There are no parts, no pivots and no light. Shadows and highlights are baked in, so the asset cannot be relit, rotated or re-posed. Animation is limited to whole-image transforms (parallax, drift, scale). Cutting regions out of 6,000 anonymous paths by hand is slower than redrawing.

## 3. Path B: structured redraw (`orca-b/`)

1. `scripts/extract_orca.py` reads the reference image and outputs `orca-b/orca_geom.json`.
   - **Measured from the image:** the silhouette, the bone patches (eye patch, throat, flank), the saddle, and **187 surface marks** (50 scars and 137 dots/pores, each with position, length, angle and size).
   - **Placed by hand:** the cut lines and pivots for the dorsal fin, fluke, both pectorals and the jaw, plus hidden overlaps so parts can rotate without opening gaps.
   - `orca-b/extract_debug.jpg` shows the part map.
2. `orca-b/OrcaB.tsx` is pure React SVG with no Remotion dependency.
   - **Named parts, back to front:** `pecFar`, `fluke`, `dorsal`, mouth interior with teeth (drawn only while the jaw is open), `body`, `jaw`, `eye` (blink), `pecNear`.
   - **Shading:** every part is re-shaded from **one light vector** with the bible §4.3 stack: L0 form gradient, L1 hard core crescent (group-aware, with a per-colour shadow tone), L3 occlusion, L4 bounce, L5 highlight plus a warm lit edge, L6 glints, L7 cyan rim and L8 marks. Lit-side and shadow-side marks get different tones.
   - **Animation:** whale-style vertical travelling-wave swim plus phase-lagged fluke pitch, dorsal sway and flipper follow-through. Props: `t`, `amp`, `jaw`, `pec`, `blink`, `light`.
3. `npm run render-b` writes `orca-b/out/hero|poses|light.svg/.png`. Rendering uses react-dom/server and rsvg-convert. The hero SVG is 209 KB with 531 elements.

## 4. Comparison (`compare.jpg`, metrics in `compare_metrics.json`)

The metrics come from `frame_metrics.py` (edge density and outline response) and the KB speck counter. Each orca was measured on a 1536×1024 plain-background panel. The kit crop includes some scene background, so its numbers are only indicative.

| | edge density | outline response | specks | animatable |
|---|---|---|---|---|
| source PNG | 0.030 | 0.024 | 176 | no |
| A medium (247 paths) | 0.028 | 0.021 | 69 | whole image only |
| A fine (1,592 paths) | 0.029 | 0.022 | 127 | whole image only |
| **B structured** | **0.032** | **0.012** | **215** | parts + light |
| kit orca (v3) | 0.032 | 0.001 | 144 | parts + light |

On the reef, A medium matches the source's edge density (0.170 vs 0.165; the kit reef scores 0.077) and keeps 500 of its 1,301 specks.

**Verdict**

- **(i) Look.** On the orca, A-fine is closest to the source because it is a near-copy. B comes second and is already denser than the kit orca: 187 marks against about 40, with more specks and a rim plus warm edge. B's open problems are the flipper-root junction and a cooler, greyer belly shadow than the source. For backgrounds such as the reef, **A-medium wins outright**: no hand redraw of 40+ objects can compete on cost, and the result reaches the §8 density targets in a single image.
- **(ii) Animation.** **B wins clearly.** It has separate pivots, a jaw with teeth, blinks and a swim wave, and the light vector can move. A has none of these.
- **Recommendation.** Use a hybrid:
  - **Heroes and characters:** Path B. Codex image, then extraction (silhouette, patches, marks), then a hand rig and the bible shading. Roughly an hour per creature, now that the extractor and `ShadedPart` exist.
  - **Environments:** Path A at medium, split into depth planes. Either generate each plane as its own Codex image on a flat background, or mask the vtracer output by y-band, so the planes still parallax and take haze.
  - **Fish and props:** whichever is cheaper. Small objects can stay vtracer-medium cutouts with a whole-sprite wiggle.

## Next steps (not done)

- Move B's `ShadedPart` onto the engine's `Shaded` once that lane settles.
- Fix the flipper-root seam and warm up the belly shadow.
- Try plane-split reef generation: far, mid, floor and foreground as separate Codex images.
- Render a short B swim clip on the Spark.
