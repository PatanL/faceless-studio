# Thumbnail concepts: horror-mom-two-chats

Three concepts. All are Remotion stills rendered on the Spark only: 1080x1920 for the Shorts/TikTok cover and 1280x720
for YouTube. The thumbs kit rules for horror apply (`studio/src/kits/thumbs/README.md`): 2-4 words in Montserrat 900,
white with a heavy black outline, one red accent word, and a cold teal grade. Here the one extra red is the EXIT-sign
strip under the door, which is the story's own colour.

Library rules (`research/library/index_notes/horror.md`, the Cover row and technique 10; PLAYBOOK §6 bottom line):
- Frame 0 shows a **readable threat**.
- YouTube outliers also use a **phone-notification mock-up**.
- The thumbnail text adds a claim the title doesn't make. Title 1 already says "only one said don't open the door", so the
  thumbnails sell the question (which one?), the closet, or the final threat.

## A. "WHICH ONE IS MOM?" (recommended; it is frame 0, the TikTok/Shorts cover)

- **Inspired by:** the frame-0 covers of 7659677578365537569 (SIEGE-CHAT, 376K, 10.8x) and 7654526047005723937
  (SIEGE-OVERLAY, 717K, 66.7x), where a readable threat and the chat sit in the first frame. Also gzXY52lcAcI
  (FARM-FLASHFWD, 353K, 10.4x), whose opening sets a parent's order against the kid's thread (0:00-0:13).
- **Composition:** the storyboard frame 0 (scene s01_hook, t = 0), pushed to 1.1.
  - Top two-thirds: the phone's lock screen, 11:40, with the two banners stacked and readable. "Mom: Don't open it.
    I'm still at work." sits over "Family · Mom: I'm outside. Unlock the door."
  - Bottom third: the front door from inside, the hall side dark. Only the red EXIT strip shows under the door, broken
    by two black feet.
  - For the 1280x720 YouTube version: the phone on the left half, tilted -3°; the door bottom with the feet on the right;
    the text at top right.
- **Text (4 words):** WHICH ONE IS **MOM?** ("MOM?" red), centred over the lock-screen wallpaper between the clock and
  the banners, or at the top on 16:9.
- **Colours:** lock-screen navy #121826 -> #2a2236; banner grey rgba(40,46,58); door wall #2c3443; EXIT red #ff2a24 on
  the strip only; red accent #ff3b3b on "MOM?".
- **Kit assets:** already rendered. `horror/Phone` (lock mode, two notifications), `horror/FrontDoor` (hallLight 0) and
  the red-strip + feet core layers from `build.py:door()`. As a thumbs spec this is a new `lock` variant of the `chat`
  template that shows notifications instead of a thread.
- **Payoff:** spoken at 0:00-0:07. The question it asks is answered at 2:54 ("neither").

## B. "IT RANG IN HERE" (YouTube A/B, threat image)

- **Inspired by:** the thumbs `door` template (a door ajar with something in the gap; resident small under a ceiling
  light); HOTEL-DOOR's bookend (Qz-TrB6W2SM 2:40-2:48, the place returns with a presence added); 7666044652910316833
  (30.3x), the ringtone-from-next-door turn.
- **Composition:** the peak (scene s16_peak_closet), recomposed:
  - the louvered hall-closet door a third open (hinge left), coats in the dark;
  - one phone screen glowing cold blue through the pocket of the grey coat, with its light spilling under the door;
  - the empty sleeve angled out as if it just moved;
  - Nora as the SVG back silhouette (no eyes), small, lower right, under the one hall light.
- **Text (4 words):** IT RANG IN **HERE** ("HERE" red), in the upper third over the wall.
- **Colours:** inner-hall wall #1c2129 -> #272d38; closet interior #060708; coat grey #5b616b; phone glow #7fb4ff (the only
  saturated colour besides the red word).
- **Kit assets:** `CLOSET_DOOR`, `CLOSET_INSIDE`, `SLEEVE` and `SILHOUETTE_BACK` SVGs from `build.py`, plus the thumbs
  text block and vignette. Add a `closet` variant of the `door` template that takes these SVGs through the KitArt bridge.
- **Payoff:** the ringtone at 1:19-1:28 and the closet opening at 2:24-2:37. It is too late a payoff for the TikTok cover,
  so it stays YouTube-only.

## C. "WHOSE VOICE?" (chat mock-up, comment bait)

- **Inspired by:** the thumbs `chat` template (a giant tilted phone with the last line big); T42u5xhrq-0
  (TEXT-FIGURE, 869K, 25.5x) 0:56-0:58, where the victim's thread speaks calmly as the entity; DORM-RULES
  (7670495663624408352, 18.0x) 2:38-2:55, where the trusted voice becomes suspect.
- **Composition:**
  - The `chat` template's tilted phone showing the private "Mom" thread: "Marigold." / "Now put the chain on." small at
    the top, and the last bubble big: "Next time, I'll call from Room 412."
  - Typing dots under it (the tell that breaks).
  - Tiny Nora at the open front door in the lit corridor, as the small human.
- **Text (2 words):** WHOSE **VOICE?** ("VOICE?" red).
- **Colours:** dark chat UI #1a1d24; bubbles #262b34; Mom avatar orange #d9822b; corridor warm #f1c37c; red accent only on
  the word.
- **Kit assets:** thumbs `chat` template (lines from `build.py` PRIVATE[-3:]); `horror/Protagonist` (expr terrified,
  light none) or the back silhouette; `horror/Hallway` (lights 3).
- **Payoff:** the last 6 s. Pair it with the pinned comment "Which Mom would you have trusted?"

## Render

Concept A needs no new code: `NO_SYNC=1 scripts/spark_stills.sh backlog/horror/horror-mom-two-chats/storyboard.json 0.0`
(already rendered as tile 1 of `out/stills/horror-mom-two-chats_v1c.jpg`). B and C need a thumbs spec
(`episodes/horror-mom-two-chats/thumbs.json`) once the episode is promoted. Check the contact sheet at phone size: the
banner text and the feet must read when the image is 120 px tall. If the banners don't, the A text carries the claim.
