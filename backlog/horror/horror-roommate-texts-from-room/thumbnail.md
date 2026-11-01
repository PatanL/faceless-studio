# Thumbnail concepts: horror-roommate-texts-from-room

Three concepts. Render with the thumbs kit (`studio/src/kits/thumbs`, Spark only, 1080x1920 cover + 1280x720) or straight
from the storyboard with `scripts/spark_stills.sh` (frame 0 is already the cover). Kit formula: one big subject, one tiny
human, 2-4 words in Montserrat 900 white with a black outline, one red accent word. Library rule
(`research/library/index_notes/horror.md`): for Shorts, frame 0 is the cover, and the cover must show the threat.

## A. "The banner" (recommended TikTok / Shorts cover; it is frame 0)

- **Inspired by:** Xv32FAAUI-0 "SOMEONE IS WATCHING ME" (7.49x): one giant lock-screen notification blown up to
  billboard size, a second-person threat, a dark wall. Also T42u5xhrq-0 (TEXT-FIGURE, 25.54x): the chat itself is
  the image.
- **Composition:** the actual frame 0 (s01). HandPhone on the lock screen, 11:40, banner "Dani: don't come out of your
  room". Behind the phone, Maya's bedroom door, blurred, with the warm strip of light under it. For the cover, scale
  the banner up so it spans about 90% of the width across the middle third (the in-video banner is too small at feed
  size), and add the text block above it.
- **Text (3 words):** **DON'T COME OUT** ("OUT" red). It repeats the banner on purpose: at thumbnail size the banner
  is texture and the headline is the read.
- **Colours:** near-black blue night (#0b0d12 to #232a36), the white banner card, the warm amber strip (#ffd38e) as the
  only warm tone, one red word (#ff4b55).
- **Kit assets:** thumbs `chat` template with the phone set to the lock screen (`chat` lines: "Dani: don't come out of
  your room"), or a still of s01 at 0.0 plus the thumbs text block; `door_svg()` from gen_storyboard.py, blurred.
- **Payoff on screen:** 0.0 s (it is the first frame and line 1).

## B. "Three plates" (YouTube Shorts shelf and 16:9 A/B)

- **Inspired by:** BciSW_2VMZg "New Household Rules" (11.04x): one subject, drained to greyscale, with a single red
  word. And BRtVGm2qt-k (Textify "5 Of Us ... We Keep Counting 6", 675K): the count that doesn't add up is the hook.
- **Composition:** the s08 table top from above: three white plates on a dark wood table under warm light, filling the
  frame. Small in the bottom corner, the strip of light under Maya's door with one pair of foot shadows (the tiny
  human is replaced by the threat's feet). Grade everything to near greyscale except the warm table light.
- **Text (4 words):** **3 PLATES. 2 OF US.** ("3" red). It adds the count the title might not carry (use it with title
  options 1, 3 or 4, not with option 2, which says the same thing).
- **Colours:** desaturated wood (#5a3c28 at 40% saturation), off-white plates (#efece4), black feet shadows, one red
  digit.
- **Kit assets:** `plates_svg()` and `feet_svg(1)` from gen_storyboard.py inside the thumbs kit's art slot (the kit needs
  an inline-svg art slot, the same small addition the explainer blue-whale thumbnail asked for), thumbs text block.
- **Payoff on screen:** 17.6-21.9 s ("I set three plates!" / "Three plates. There's two of us."). Later than 10 s, so
  use B on the YouTube shelf, never as the TikTok cover.

## C. "The photo" (A/B variant; the scariest image)

- **Inspired by:** x--ui6_mAxE "I gave her a ride, but she was....." (9.45x): the figure that answers half the
  title, on black; and T42u5xhrq-0's held photo at 0:54 (the only image in a chat Short).
- **Composition:** the s28 photo card, tilted 2 degrees with its white border, filling about 80% of the frame: from
  inside a dark doorway, across the hall, a closed door with a white strip under it and a faceless black figure
  standing at it. The blurred chat behind the card. The "11:51 PM" stamp stays.
- **Text (3 words):** **SHE SENT THIS** ("THIS" red).
- **Colours:** greyscale photo (#050505 to #e6e6e6) on the dark-blue thread; the white card border is the brightest
  area; one red word.
- **Kit assets:** `photo_svg()` from gen_storyboard.py, `horror/HandPhone` (blurred, opacity 0.5), thumbs text block.
- **Payoff on screen:** 68.6-72.4 s. That is late, and it shows the scariest image, so test C only against A on the
  YouTube shelf. It does not reveal who is at the door or the mom's answer, so no loop is spoiled.

## Render

Write `backlog/horror/horror-roommate-texts-from-room/thumbs.json` with variants `banner` (A, template `chat`), `plates`
(B) and `photo` (C) once the thumbs kit has an inline-svg art slot. Then run
`OUT=thumbs/roommate-texts scripts/thumbs_render.sh <spec>` (Spark only). Until then, A comes straight from the
storyboard: `NO_SYNC=1 scripts/spark_stills.sh backlog/horror/horror-roommate-texts-from-room/storyboard.json 0.0`
(checked: out/stills/roommate_v3.jpg, tile 1). At phone size the banner text is small, so the headline must carry A.
