# Thumbnail concepts: horror-babysitter-parent-rules

Three concepts. Render with the thumbs kit (`studio/src/kits/thumbs`, Spark only, 1080x1920 cover + 1280x720) or straight
from the storyboard with `scripts/spark_stills.sh` (frame 0 is already the cover: `out/stills/babysitter_cover.jpg`).
Kit formula: one big subject, 2-4 words in Montserrat 900 white with a black outline, one red accent word. Library rule
(`research/library/index_notes/horror.md`, PLAYBOOK §6): for Shorts, frame 0 is the cover and the cover shows the threat.
**Never put Theo (the child) on any thumbnail**: child-in-peril art on a cover risks "made for kids" misclassification and
reads as kid-appealing; the threat here is the note and the phones.

## A. "The note" (recommended TikTok / Shorts cover; it is frame 0)

- **Inspired by:** cVUJmsVkUW4 MOM-NOTE (30.95x), where the note itself is the subject and the key words are coloured;
  BciSW_2VMZg "New Household Rules" (11.04x, thumb in `research/library/thumbs/`): one subject drained of colour, a
  hand-lettered caption with a single red word.
- **Composition:** the actual s01 frame: the fridge note fills the top two thirds, rule 5 in red marker, double-underlined;
  the counter strip below with the handset "INCOMING · DOYLE" and Ivy's phone, "Mrs. Doyle · 9:40 PM: Still at dinner!".
  For the cover, push in 1.15x on the note so rule 5 sits at the centre line, and lift the lock-screen card 120 px so it
  isn't cut by the TikTok caption band.
- **Text (2 words):** **WHAT PASSWORD?** ("PASSWORD" red), in the top band above the magnet. It is the caller's line, so
  the cover asks the question the hook answers at 6.4 s.
- **Colours:** steel grey-blue (#7f8890 to #c7ced4), cream paper (#f3ead2), navy marker (#1f2d6b), one red (#c8102e on
  the paper, #ff4b55 for the word), dark wood counter (#3a2a20).
- **Kit assets:** `fridge_note()`, `highlight(5)` and `lock_preview()` from `gen_storyboard.py`; `horror/FeaturePhone`
  (sms "INCOMING / DOYLE"); thumbs text block.
- **Payoff on screen:** 0.0-6.4 s.

## B. "Two phones, one family" (YouTube Shorts shelf and 16:9 A/B)

- **Inspired by:** Xv32FAAUI-0 "SOMEONE IS WATCHING ME" (7.49x, thumb in `research/library/thumbs/`): one notification
  blown up to billboard size on a dark wall; and SIEGE-CHAT 7659677578365537569 (10.79x): the phone as the battleground
  between the fake and the real authority.
- **Composition:** split frame on a near-black counter. Left, the cordless handset huge and tilted, its LCD lit green:
  "INCOMING · DOYLE". Right, Ivy's lock screen with ONE giant notification card spanning half the width:
  "Mrs. Doyle · 9:40 PM — Still at dinner!". Nothing else. In 16:9, the two devices sit side by side with the text centred
  above.
- **Text (3 words):** **WHO'S CALLING THEN?** ("CALLING" red). The contradiction is the image; the words just point at it.
- **Colours:** black-blue (#0b0d12), LCD green (#9db59a with glow), white notification card, one red word.
- **Kit assets:** `horror/FeaturePhone` (scaled 2x), `lock_preview()` with a larger body font, thumbs text block.
- **Payoff on screen:** frame 0 (both devices) and 1:02.9 ("Above it, a text I'd missed. Nine forty. Still at dinner.").

## C. "The chain" (A/B for title 1)

- **Inspired by:** Qz-TrB6W2SM HOTEL-DOOR (1.52M, 9.01x): the closed hotel door is the whole threat; SIEGE-CHAT
  7659677578365537569 0:12-0:16 (the near-unlock at the peephole).
- **Composition:** the s23 chain insert: the door edge, the chain track, Ivy's fingers on the knob, the chain slid one inch
  open, lit only by the warm peephole glow; dark wood all round. One small detail in the lower third: the handset on the
  floor glowing "EXT 2".
- **Text (3 words):** **HE KNEW IT** ("KNEW" red). With title 1 ("They Didn't Know Their Own Password") it sets up the
  turn: the parents didn't, the door did.
- **Colours:** dark walnut (#2a211c / #5a3f2e), pale door frame (#d9cfc0), warm glow (#e7b46a), skin (#e9b996), one red word.
- **Kit assets:** `chain_plate()` + `chain_and_hand()` from `gen_storyboard.py`, `horror/Darkness` (radius 0.45), small
  `horror/FeaturePhone`, thumbs text block.
- **Payoff on screen:** 0:47.8-0:55.3 (the password at the door, the chain slides, "I let go"). Later than 10 s, so use C on
  the YouTube shelf, never as the TikTok cover.
