# Thumbnail concepts: horror-delivery-photo-inside

Three concepts. All are Remotion stills rendered on the Spark only: 1080x1920 for the Shorts/TikTok cover and
1280x720 for YouTube. The thumbs kit horror rules apply (`studio/src/kits/thumbs/README.md`): 2-4 words in
Montserrat 900, white with a heavy black outline, one red accent and a cold teal grade.

Library rules (`research/library/index_notes/horror.md`, technique 10 and the Cover row):
- Frame 0 shows a **readable threat** plus a burned-in first-person fragment.
- YouTube outliers also use a **phone-notification mock-up**.
- The thumbnail text should add a claim the title doesn't make. Title 1 states the rating rule, so the
  thumbnails sell the photo or the inside angle (originality critique: not just "creepy delivery photo").

## A. "TAKEN FROM INSIDE" (recommended: it IS frame 0, the TikTok/Shorts cover)

- **Inspired by:** the frame-0 covers of 7659677578365537569 (SIEGE-CHAT, 376K, 10.8x) and
  7654526047005723937 (SIEGE-OVERLAY, 717K, 66.7x): a readable threat with a burned-in caption on the first
  frame. Also T42u5xhrq-0 (TEXT-FIGURE, 869K, 25.5x) at 0:54, where the photo message inside the phone UI is
  the proof image.
- **Composition:** the exact storyboard frame 0 (`storyboard.json` scene s01_hook, t=0), pushed in to 1.15:
  - the static phone with the "bites" order card and a green "✓ Left at door · 9:41 PM";
  - the white-bordered proof photo of the front door from inside;
  - the chain with the pulsing red ring and the red label "taken from INSIDE →" angled -4°.
  - For the 1280x720 YouTube version: the photo card on the right half, and the text on the left over near-black.
- **Text (3 words):** TAKEN FROM **INSIDE** ("INSIDE" red). On the 9:16 cover it is the burned label itself, not
  a second text block.
- **Colours:** near-black #07080b and phone #15171c; warm door photo (hall light #e7b46a, door #4d3d35); a
  white photo border #f4f1ea; one accent red #ff3b3b (ring + label); a small green #4ade80 status tick for
  the "everything is fine" irony.
- **Kit assets:** already rendered. These are core rect/text/circle layers, `horror/FrontDoor` (chain on,
  hallLight 0.9), and the inline SVG mirror plant. A thumbs `phone-card` variant that reuses
  `build.py:door_photo()` would make it a spec instead of a frame grab.
- **Payoff:** spoken at 0:01.6 ("taken from inside"), proven at 0:10-0:11 (the chain timeline).

## B. "HE NEVER LEFT" (YouTube A/B, threat image)

- **Inspired by:** the thumbs `door` template lineage (a figure where the safe place should be); HOTEL-DOOR's
  bookend (Qz-TrB6W2SM 2:40-2:48: the opening place returns with a figure added); TEXT-FIGURE's last-beat
  threat turned on the viewer.
- **Composition:** the bookend proof photo (scene s16_bookend after the ping):
  - the front door full-frame, chain on;
  - Nora's back-view silhouette in the lower foreground, rim-lit;
  - a white proof-photo border with "✓ Delivered to customer · 9:58 PM";
  - for the thumbnail only, a faint violet scooter-icon pin hovering just behind her shoulder (the "you are
    here" map language).
- **Text (3 words):** HE NEVER **LEFT** ("LEFT" red), upper third.
- **Colours:** cold teal-grey grade (#2c3443 -> #1a1f29), white border, a violet #8b6cff pin, red only on "LEFT".
- **Kit assets:** `horror/FrontDoor`, the `SILHOUETTE_BACK` SVG and the scooter SVG from `build.py`, and the
  thumbs text block.
- **Payoff:** "She thinks I left." (1:20) and the final ping (1:23). It pays off late, so it stays YouTube-only
  and never becomes the TikTok cover.

## C. "RATE HIM ★★★★★?" (notification mock-up, comment bait)

- **Inspired by:** the phone-notification mock-up covers the library notes call out on YouTube; the thumbs
  `chat` template (a giant tilted phone, the last line big); 7659677578365537569's held phone with a chat panel.
- **Composition:**
  - the thumbs `chat` template's tilted phone with Nora in bed lit by it, as the tiny human;
  - on the phone, the bites rating sheet with four gold stars and one empty;
  - the timer "0:03" in red;
  - above it, a lock-screen banner "Proof of delivery updated", whose photo thumbnail is photo 2 (her from
    behind).
- **Text (2-4 words):** RATE HIM **★★★★★?** or WOULD YOU RATE? ("RATE" red).
- **Colours:** dark UI (#1a1d24), gold stars #ffc83d, red timer #ff3b3b, a cold teal room.
- **Kit assets:** thumbs `chat` template (NEW `rating` screen mode, reusing `build.py:rating_sheet()`),
  `horror/Protagonist` (pose phone, expr terrified, light phone), `horror/Bedroom`.
- **Payoff:** the rating dilemma is on screen from 0:16 (near-compliance) and in the clock at 0:56. It pairs
  with the pinned comment "Six people never rated him. Would you have?"

## Render

Concept A needs no new code. Render it on the Spark with
`NO_SYNC=1 scripts/spark_stills.sh backlog/horror/horror-delivery-photo-inside/storyboard.json 0.0` (already
checked in `out/stills/horror-delivery-photo-inside_v2.jpg`, tile 1). B and C need a thumbs spec
(`episodes/horror-delivery-photo-inside/thumbs.json`) once the episode is promoted. Check the contact sheet at
phone size: the red label must read at 120 px tall, and the chain ring must stay visible.
