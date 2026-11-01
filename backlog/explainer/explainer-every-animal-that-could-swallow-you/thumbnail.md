# Thumbnail concepts: explainer-shoulder-test

Three concepts, rendered as Remotion stills on the Spark with the thumbs kit (`studio/src/kits/thumbs`, 1280x720 for YouTube, plus a 1080x1920 cover). Kit rules: one big subject, one tiny human, 2-4 words in Montserrat 900 with a heavy black outline, one red accent continued as a hand-drawn red pointer to the tiny human. Library rule (`research/library/index_notes/explainer.md` §Thumbnails, technique 10): the words must add a claim the title doesn't make, not restate it. The thing the thumbnail shows should also pay off on screen early.

The device that is ours, and that every concept shows, is the **red hoop around the tiny YOU's shoulders**. This is the shoulder gauge seen in frame 1 of the video.

## A. "WON'T FIT.." (recommended for the main upload)

- **Inspired by:** fGcgWaswMns SPERM, "IT HEARS YOU.." (2.31M, 14.65x): black field, giant white scratchboard head filling the right two-thirds, tiny diver lower-left, white words with one red word, red hand-drawn arrow to the human. The same template family also made mzeN0BXR4e0 DEEP work: big text on the left, the human between it and the monster.
- **Composition:** Template `eye` with subject `whale` (the existing sperm-whale head art). The head enters from the right, lower jaw dropped open with the teeth visible, and the dark throat is the focal point at about 62% x, 58% y. Lower-left at about 3% of the frame height is the tiny front-view YOU (`humanArt`: `explainer/You`, pose stand) with a red hoop, drawn as an ellipse, around its shoulders. The red arrow runs from the accent word to the hoop.
- **Text (2 words):** **WON'T FIT..** ("FIT.." in red). It adds a claim the title only asks about.
- **Colours:** near-black `#05080a` ground, white/grey scratchboard whale, red `#ff2a2a` for the word, the arrow and the hoop only.
- **Kit assets:** thumbs `eye` template, `whale` subject, `humanArt` = `explainer/You` + one ellipse layer for the hoop (add a `hoop: true` prop on the human slot: a ~12-line change in `templates/explainer.tsx`).
- **Payoff on screen:** the hoop snaps round YOU at 0:01. The open sperm-whale throat is the climax (7:28 "What does the ring say?" → "Nothing.").

## B. "ONLY ONE MIGHT" (A/B test against A)

- **Inspired by:** mzeN0BXR4e0 DEEP "WE REALLY CAN'T EXPLAIN" (17.2M, 12.86x), stacked text block on the left with one red word and the subject on the right; nAWpLtG-kNs ERAS (12.2M, 113.57x), where the ranking board is the format promise and also the comment bait.
- **Composition:** The right 60% is the shoulder-gauge board seen at an angle: six short pale-blue columns under a thick red line labelled "YOUR SHOULDERS", and one grey dashed column with a big "?" breaking through the line. A small sperm-whale silhouette sits on top of that column. The tiny YOU with its red hoop stands at the foot of the board, with the red arrow from the text to the "?" column. The left 40% holds the stacked words.
- **Text (3 words):** **ONLY ONE / MIGHT** ("MIGHT" in red), stacked on 2 lines.
- **Colours:** dark teal `#0b2028` → black gradient, columns `#9fd3e0`, red line and word `#ff5a4a`, `?` in yellow `#ffd23f` (the video's estimate colour).
- **Kit assets:** a new thumbs template `board` (about 60 lines). It reuses the generator's column geometry from `gen_storyboard.py` (`board()`), plus `explainer/SpermWhale` with `silhouette` and `explainer/You`.
- **Payoff on screen:** the empty board is up at 0:36 and the first column grows at 1:46. The "?" column only arrives at 8:00, so B breaks the "pay off within 10 s" rule for the column itself. That's why it is the A/B variant, not the default.

## C. "PICK ONE" menu (the no-text style; best for the 9:16 cover)

- **Inspired by:** QxM2Hu70tVk PLANT (16.2M, 2.82x). That's the no-text family the library notes found among outliers: a menu of threats around one tiny human, all mouths open toward it. ERAS's hook tableau shows every threat at once (PLAYBOOK H11 "show every threat in one tableau").
- **Composition:** The frame-1 tableau of the video, lit like the thumbnail: six open mouths fanned around a centred, tiny YOU with the red hoop. They are the blue whale (gape 1, top-left), whale shark (jaw open, left), basking shark (jaw open, bottom), humpback (pleats, top-right), goliath grouper (flare, right) and sperm whale (teeth, bottom-right). Optional 2-word block: **PICK ONE** (red "ONE"). With no text it still reads, PLANT-style.
- **Colours:** ocean gradient from the video (`explainer/Ocean` depth 8 with rays) darkened 40% at the edges. Creatures in flat grey `#9fb3b8`, YOU white, hoop red.
- **Kit assets:** `explainer/Ocean`, `BlueWhale` (`gape`), `SpermWhale` (`teeth`). It also needs the 4 new figures this episode depends on: `WhaleShark`, `BaskingShark`, `Humpback`, `GoliathGrouper`. So C can only render once those exist; A and B can render today.
- **Payoff on screen:** it is frame 1 of the video (0:00-0:08), so the cover loops into the opening shot.

## Render

Write `episodes/explainer-shoulder-test/thumbs.json` with variants `wontfit` (A, template `eye`, subject `whale`, text "WON'T FIT..", accent "FIT..", humanArt You + hoop), `board` (B, once the template exists) and `menu` (C, once the figures exist). Then run `OUT=thumbs/explainer-shoulder-test scripts/thumbs_render.sh episodes/explainer-shoulder-test/thumbs.json` (renders on the Spark only). Check the contact sheet at 168 px wide, the YouTube mobile shelf size. The red hoop must still read as a ring around the shoulders at that size. If it doesn't, scale the human up to about 6% of the frame height before shrinking anything else.
