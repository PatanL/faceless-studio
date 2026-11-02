# three-lane: assets and licences

Everything in `public/` was downloaded on 2026-11-02 from Poly Haven's official sources (the public API
`api.polyhaven.com` and its file host `dl.polyhaven.org`), at 1k texture resolution, glTF format, unmodified.
Total 5.4 MB, committed.

| Asset | Folder | Source page | Author | Licence | Files |
|---|---|---|---|---|---|
| Chinese Cabinet (15,668 tris, 1.26 x 0.55 x 2.87 m) | `public/models/chinese_cabinet/` | https://polyhaven.com/a/chinese_cabinet | Kirill Sannikov | CC0 1.0 | `chinese_cabinet_1k.gltf`, `.bin`, `textures/*_diff_1k.jpg`, `*_nor_gl_1k.jpg`, `*_arm_1k.jpg` |
| Chinese Tea Table (2,508 tris, 0.84 x 0.84 x 0.50 m) | `public/models/chinese_tea_table/` | https://polyhaven.com/a/chinese_tea_table | Kirill Sannikov | CC0 1.0 | same layout |
| Chinese Armchair (2,675 tris, 0.85 x 0.79 x 1.59 m) | `public/models/chinese_armchair/` | https://polyhaven.com/a/chinese_armchair | Kirill Sannikov | CC0 1.0 | same layout |

Licence check: https://polyhaven.com/license (read 2026-11-02) says all assets on the site (HDRIs, textures and
3D models) are licensed CC0, usable for any purpose including commercial work, with no attribution required.
We credit the author here anyway.

Only the diffuse (`_diff_`) maps are used; the renderer swaps the PBR materials for two-tone Lambert. The normal and
ARM maps are kept so the glTF files stay as published (the loader requests them).

**Not used:** Kenney (kenney.nl) was the first choice, but kenney.nl answers HTTP 403 to non-browser requests from
the Spark, and we did not work around that. No files from `mromidev/claude-animated-shorts` are assets here: in
particular nothing from its `references/frames` or `references/sheets` (RicksClips screenshots).

**Code-painted (ours, no licence needed):** plank floor, plaster, red lacquer, rug, window sky, contact-shadow blob
(`src/paint.ts`) and the stick-figure card (`src/card.ts`).

**Ported code (MIT):** `src/ink.ts`, `src/lensblur.ts`, `src/grade.ts`, `src/shade.ts` are adapted from
mromidev/claude-animated-shorts `templates/bridge/` (commit e3b817b, "Copyright (c) 2026 Mr omi", MIT). Each file
carries the full copyright and permission notice in its header.
