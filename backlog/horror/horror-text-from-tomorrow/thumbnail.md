# Thumbnail concepts: horror-text-from-tomorrow

Three concepts. All are Remotion stills rendered on the Spark only: 1080x1920 for the Shorts/TikTok cover and 1280x720
for YouTube. Thumbs-kit horror rules apply (`studio/src/kits/thumbs/README.md`): 2-4 words, Montserrat 900, white with a
heavy black outline, one red accent word, cold teal grade.

Library rules (`research/library/index_notes/horror.md`, cover row): frame 0 shows a readable threat plus a burned-in
first-person fragment; YouTube outliers also use phone-notification mock-ups. The thumbnail text should add a claim the
title doesn't make. Title 1 says "39 minutes early", so the thumbnails sell the stamp, the warning or the door.

## A. "SENT 2:31 AM" (recommended: it IS frame 0, the Shorts/TikTok cover)

- **Inspired by:** the frame-0 covers of 7654526047005723937 (SIEGE-OVERLAY, 717K, 66.69x) and 7659677578365537569
  (SIEGE-CHAT, 376K, 10.79x), a readable threat on frame 1 with burned-in text; gzXY52lcAcI (FARM-FLASHFWD, 353K, 10.38x)
  0:00, a message from the future as the first image.
- **Composition:** storyboard scene `s01_cover` at t=0, pushed to 1.12: the hand-held lock screen with the big white
  clock **1:52**, the "Me · 2:31 AM" notification on top, the office's "All clear" notification under it, and the red
  "SENT 2:31 AM" over the top third. The contradiction (clock vs stamp) is the whole image. For 1280x720: the phone on
  the right half, tilted -6°, text on the left over near-black.
- **Text (3 words):** SENT **2:31 AM** ("2:31 AM" red #ff4b55). On the 9:16 cover this is the burned frame-0 text layer,
  not a second block.
- **Colours:** near-black #0b0d12, phone #15171c, lock clock white #f1f3f6, notification card grey #2a2f38, one red
  #ff4b55, Bedroom blurred at lamp 0.2 behind (cold teal).
- **Kit assets:** `horror/HandPhone` (lock mode, notifications), `horror/Bedroom` (blurred), `horror/Vignette`, a core text
  layer. Already in `storyboard.json`; the look is checked in `out/stills/ttft_v1.jpg` (tile 1).
- **Payoff:** spoken by 0:03.7; the stamp's meaning pays at 1:17 (same minute, same sender).

## B. "IT'S JUST ME" (YouTube A/B, threat image)

- **Inspired by:** the thumbs `door` template (a figure where the safe place should be); T42u5xhrq-0 0:54 (TEXT-FIGURE,
  869K, 25.54x), the only image held back as proof; the HOTEL-DOOR bookend (Qz-TrB6W2SM 2:40-2:48, 1.52M, 9.01x), the
  opening place returning with a presence added.
- **Composition:** the door-gap insert (scene `s28_gap`): a black field, the door's bottom edge across the upper third, a
  warm line of hall light, and two grey socked feet under the door with a pale toe through the hole in the left sock,
  lit from the gap. Upper left, a small lock-screen bubble "Me: Open up. It's just me." as the tiny human element (a phone
  on the floor at the frame edge).
- **Text (3 words):** IT'S JUST **ME** ("ME" red), upper third.
- **Colours:** near-black #050507, floor #1d1a1c, sock grey #8a90a0, skin #f2cfa8 (the only warm spot besides the hall
  line #e7b46a), red only on "ME".
- **Kit assets:** the inline `sock_feet()` SVG from `gen_storyboard.py` (door=True), `horror/Phone` lock mode for the
  small bubble, the thumbs text block. Checked in `out/stills/ttft_v3.jpg`.
- **Payoff:** 1:27-1:35. It pays off late, so it stays YouTube-only and never becomes the TikTok cover. The image is
  non-graphic (feet in socks), so it fits the R5 "clean thumbnail" rule.

## C. "DON'T GO UP" (chat template, rule-as-text)

- **Inspired by:** the thumbs `chat` template (a giant tilted phone, the last line big, the resident in bed lit by it);
  7654526047005723937 0:02-0:12, the official channel contradicted by an impossible source; BciSW_2VMZg (WrONG Rules,
  104K, 11.04x), an urgent imperative that presupposes the viewer is inside the story.
- **Composition:** the thumbs `chat` template, `chatTitle` "Me", lines:
  `[{from: "Me", text: "At 2:14 they'll send everyone to the roof."}, {from: "Me", text: "Don't go."}]`, the last line big;
  behind the phone, a faint red alert bubble from the residents chat "Gas leak. Everyone up to the roof." to show the
  contradiction; the tiny resident in bed under the phone glow, looking up at the ceiling.
- **Text (3 words):** DON'T GO **UP** ("UP" red).
- **Colours:** teal-grey grade, the "Me" avatar olive #55704f, the alert bubble red at 40% opacity (so "UP" stays the only
  full red), white text.
- **Kit assets:** thumbs `chat` template (spec fields `chat`, `chatTitle`); no new art.
- **Payoff:** spoken at 0:04-0:10 and inverted at 0:35 (2:14). It works for viewers who will never see the cover frame,
  so it's the safest second YouTube variant.

**Spec for the thumbs CLI** (render on the Spark with `scripts/thumbs_render.sh`; concepts A and B are frame grabs of the
storyboard, so only C needs the spec):

```json
{"id": "horror-text-from-tomorrow", "niche": "horror", "variants": [
  {"template": "chat", "chatTitle": "Me", "text": "DON'T GO UP", "accent": "UP",
   "chat": [{"from": "Me", "text": "At 2:14 they'll send everyone to the roof."}, {"from": "Me", "text": "Don't go."}]}
]}
```
