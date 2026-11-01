# Thumbnail concepts: horror-elevator-maintenance-chat

Three concepts. All are Remotion stills rendered on the Spark only: 1080x1920 for the Shorts/TikTok cover and 1280x720
for YouTube. Thumbs-kit horror rules apply (`studio/src/kits/thumbs/README.md`): 2-4 words, Montserrat 900, white with a
heavy black outline, one red accent word, cold teal grade.

Library rules (`research/library/index_notes/horror.md`, cover row): frame 0 shows a **readable threat** plus burned-in
text; YouTube outliers put the premise in 3-6 big words or use a phone-notification mock-up; the controls' frame 0 shows
no threat (7696062340852190496, 0.77x). PLAYBOOK §6 bottom line: the cover frame shows the threat. The thumbnail text
should add a claim the title doesn't make. Title 1 says "Maintenance Texted First", so the thumbnails sell the mirror,
the button code or the missing number.

## A. "DON'T LOOK" (recommended: it IS frame 0, the Shorts/TikTok cover)

- **Inspired by:** the frame-0 covers of 7659677578365537569 (SIEGE-CHAT, 376K, 10.8x) and 7654526047005723937
  (SIEGE-OVERLAY, 717K, 66.7x): an official-looking message as a readable threat on frame 1; T42u5xhrq-0 (TEXT-FIGURE,
  869K, 25.5x) 0:00: the phone is the stage from the first frame.
- **Composition:** storyboard scene `s01_cover` at t=0. The hand-held lock screen reads **1:04**, with one notification
  from "Maintenance": "Stay calm, Nora. Don't look at the mirror." Behind it, blurred, the elevator panel with its red
  counter stuck on two dashes. At the right edge, the mirror strip catches the phone glow, with a pale face-height
  highlight (two dark eye dots) **facing the camera**. That is the visual threat the critique asked for, and it pays off at
  the 1:18 image. For 1280x720: the phone on the right half, tilted -6°, the mirror strip filling the far right with the
  face highlight, text on the left over the dark panel.
- **Text (2 words):** DON'T **LOOK** ("LOOK" red #ff4b55), upper third, a burned frame-0 text layer (the 9:16 cover
  already shows the banner, so the 9:16 variant can drop it and rely on the notification).
- **Colours:** near-black #0b0d12, steel panel #4c535c to #7a828c (blurred), counter dashes #ff3b30 (small, low), lock
  clock white #f1f3f6, notification card #282e3a, mirror strip #8a939c to #b6bec6, face highlight #eef2f5 at 38%.
- **Kit assets:** `horror/HandPhone` (lock mode, notifications at -1), `horror/ElevatorPanel` (at 999, target 0) +
  `dashes()` plate, `mirror_strip()` SVG, `horror/Darkness`, `horror/Vignette`. All already in `storyboard.json`; the look
  is checked in `out/stills/hemc_v2.jpg` (tile 1).
- **Payoff:** spoken at 0:04 ("Don't look at the mirror"); the face in the mirror pays at 1:18.

## B. "THE BACK OF MY HEAD" (YouTube A/B: the threat image itself)

- **Inspired by:** T42u5xhrq-0 0:54 (TEXT-FIGURE, 869K, 25.5x), the one image held back as proof; the thumbs `hallway`
  template (a figure where it shouldn't be, the human small); 7702661541224566049 (HEARSE-P1, 2.2M, 63.1x), whose B9 mirror
  ritual shows the entity once, held still.
- **Composition:** a frame from `s24_image`, pushed to 1.15: dark brushed-steel doors with the seam; Nora's terrified
  reflection large and translucent on the left; behind it, in the pale mirror rectangle, a smaller, crisp Nora with the
  `stare` face (unblinking, pupils dead centre), lit from below by the phone. For 16:9 the doors fill the frame and the
  calm face sits on the right third, at eye level.
- **Text (3 words):** NOT MY **REFLECTION** ("REFLECTION" red). The face is calm, not smiling, so the text names the wrongness instead of a grin.
- **Colours:** steel #4c5259 to #737b84 under a near-black vignette, mirror rectangle #b9c2ca at 30%, skin the only warm
  tone, red only on the accent word. No heartbeat tint on the thumbnail.
- **Kit assets:** `DOOR_FRAME` + `door_panel()` SVGs, `horror/Protagonist` x2 (`terrified` at 0.42 opacity, `stare` crisp),
  the thumbs text block. Checked in `out/stills/hemc_v2.jpg` (tile 7).
- **Payoff:** 1:18-1:23. It spoils the B9 image, so it's YouTube-only and never the TikTok cover. Non-graphic (a face),
  so it fits the R5 "clean thumbnail" rule.

## C. "2 · 11 · 5" (chat template, the code as the hook)

- **Inspired by:** the thumbs `chat` template (a giant tilted phone, the last line big, the resident lit by it);
  7659677578365537569 0:19-0:28 (the count that proves the authority is fake); BciSW_2VMZg (WrONG Rules, 104K, 11.0x),
  an imperative that presupposes the viewer is inside.
- **Composition:** thumbs `chat`, `chatTitle` "Maintenance", lines
  `[{from: "Maintenance", text: "Stay calm, Nora."}, {from: "Maintenance", text: "Press 2, then 11, then 5."}, {from: "Maintenance", text: "Never press the alarm."}]`,
  the last line big. The tiny human is Nora in the car (`horror/Protagonist`, pose phone, expr terrified) in place of the
  bed resident; the background is the blurred elevator panel.
- **Text (3 words):** NEVER PRESS **ALARM** ("ALARM" red).
- **Colours:** teal-grey grade, the Maintenance avatar #5b6470, white text, red only on "ALARM".
- **Kit assets:** thumbs `chat` template (spec fields `chat`, `chatTitle`), `humanArt` = `horror/Protagonist`. No new art.
- **Payoff:** spoken at 0:21.8 and broken on purpose at 1:34. It works for viewers who never see the cover frame, so it's
  the safest second YouTube variant.

**Spec for the thumbs CLI** (render on the Spark with `scripts/thumbs_render.sh`; A and B are frame grabs of the
storyboard, so only C needs the spec):

```json
{"id": "horror-elevator-maintenance-chat", "niche": "horror", "variants": [
  {"template": "chat", "chatTitle": "Maintenance", "text": "NEVER PRESS ALARM", "accent": "ALARM",
   "chat": [{"from": "Maintenance", "text": "Stay calm, Nora."}, {"from": "Maintenance", "text": "Press 2, then 11, then 5."},
            {"from": "Maintenance", "text": "Never press the alarm."}],
   "humanArt": {"component": "horror/Protagonist", "props": {"pose": "phone", "expr": "terrified"}, "time": 0.4}}
]}
```
