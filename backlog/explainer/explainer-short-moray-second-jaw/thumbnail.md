# Thumbnail concepts: explainer-short-moray-second-jaw

There are three concepts. Rules applied:

Thumbs-kit rules (`studio/src/kits/thumbs/spec.ts`):
- one big subject
- one tiny human or human part
- 2-4 words of high-contrast text
- exactly one red accent word

Library rules (`research/library/index_notes/explainer.md`):
- The text adds a claim the title does not make.
- White text, one red word, and a red arrow to the human.
- For Shorts, frame 0 is the thumbnail.
- The word should pay off on screen within ~10 s.

None of the Shorts references has a designed thumbnail. 6mRR91AbxjQ, XFFjxTllpoA and jw6bS-WL4F4 all use auto-frames (FLY's first frame and its auto-picked peak frame; PUFFER's hazard-sign title card). So the "inspired by" notes borrow the long-form designed thumbnails for layout and the Shorts' first frames for the cover logic.

**Production note: no moray in the thumbs kit yet.** The thumbs templates take `art` from a registered component, and there is no `explainer/Moray` (script.md section 7). Until it exists:
- Concept A is rendered as a storyboard still: `node src/cli/stills.mjs <storyboard> --at 0.2` on the Spark. Frame 0.2 s already shows the full A composition, including the x-ray. A 0.2 s still is in `out/stills/explainer-short-moray-second-jaw_storyboard.jpg` (tile 1).
- Concepts B and C are stills at 30.6 s (s07_pull) and 58.6 s (s14_twist) with the text layer swapped. Each is a one-off storyboard copy with a Headline layer replacing the caption.
- When `explainer/Moray` lands, all three move to the thumbs templates (`eye` for A and B, `scale` for C).

## A. "2 MOUTHS" (frame-0 cover, recommended for the 9:16 Shorts/TikTok post)

- **Inspired by:**
  - 6mRR91AbxjQ: frame 1 is the creature at macro scale on its "landscape" (the skin floor), which doubles as the cover. Here the reef wall is the landscape.
  - XFFjxTllpoA: frame 0 is a title card that is also the thumbnail, so the cover, the hook and the loop agree.
  - fGcgWaswMns: a 2-4 word claim and a red arrow to the human.
- **Composition:**
  - The video's actual frame 0. The coral wall fills the middle band (top edge at y 28%), with the black oval gap centred at y 38%.
  - Inside the gap: two pale eyes, plus the yellow x-ray throat jaw glowing behind them. This is the second mouth, shown but not named. At phone size it reads as "something with teeth inside the dark".
  - A bare hand in a blue wetsuit sleeve enters from the right, fingertips ~40 px from the gap.
  - The two-slot chip `MOUTH 1 · MOUTH 2` sits top-left.
  - The title says "bites you", so the cover adds the count. The count is the curiosity gap and the visual paradox (one hole, two mouths).
- **Text (2 words):** **2 MOUTHS** ("2" red, "MOUTHS" white). This is the kit Headline at y 19%, on dark water above the wall. Text inside the cover was moved there because red on the pink coral failed the legibility check in the first stills pass.
- **Colours:**
  - dark-teal ocean #0d3b45 -> #04161b
  - coral pink #c9727a and ochre #c89a52
  - hole #05080a
  - throat jaw yellow #ffe14d (the only saturated warm in the gap)
  - wetsuit blue #1f5fae, skin #e9b48f
  - red #e5483d for "2" only
- **Kit / storyboard assets:** explainer/Ocean (depth 12, rays 5), and the s01 layers: SVG_WALL, SVG_HOLE, SVG_EYES, SVG_PHARY (x-ray), SVG_HAND, chip rects, explainer/Headline.
- **Payoff on screen:** immediate. It is frame 0, and "two mouths" is spoken at 1.8 s.

## B. "DON'T PULL" (shelf / 16:9, A/B partner for A on the YouTube Shorts shelf)

- **Inspired by:**
  - fGcgWaswMns: monster-vs-human contrast on a dark ground, with a red arrow and a 2-4 word imperative claim.
  - XFFjxTllpoA: the hazard-sign title card (a warning as the thumbnail).
  - The mantis-shrimp thumbnail.md concept B: a late-payoff shelf variant, kept off the TikTok cover.
- **Composition:**
  - The s07_pull frame. The open-jawed moray head is side-on, filling the left 2/3, with the tooth row glowing red and the steel fish-hook overlay visible on the teeth.
  - The hand in the jaws at the right, with a thick red arrow pointing outward (the move you must not make).
  - No wound and no blood: the danger is the direction of the arrow against the direction of the hooks.
  - For 16:9: the head is on the left half and the text block is on the right.
- **Text (2 words):** **DON'T PULL** ("PULL" red). It adds a claim the title doesn't make (the counter-intuitive rule).
- **Colours:**
  - teal ground #0d3b45
  - moray olive #6f7d2e with yellow speckles #d9c64a
  - mouth #7a2b33, teeth #f5f2e8, hook steel #cfd6dc
  - red #e5483d for "PULL", the arrow and the tooth glow
- **Kit / storyboard assets:** s07 layers: SVG_HEAD_OPEN, SVG_HOOKS, SVG_TOOTH_GLOW (red), SVG_HAND, SVG_ARROW, explainer/Headline. Later: thumbs `eye` template with `explainer/Moray` (`jaw: 40`) as `art`.
- **Payoff on screen:** late. "Pull." lands at 27.6 s (39%). That breaks the ~10 s rule, so B is a shelf A/B variant only.

## C. "IT'S THE FRIENDLY ONE" (16:9 compilation / re-upload)

- **Inspired by:**
  - fGcgWaswMns and its villain-swap act (PLAYBOOK §5): a tiny human and a red arrow, with the text reversing the expected threat.
  - XFFjxTllpoA 0:43-0:47: its twist backdrop is the everyday human scene (a plate of fugu), not the animal. Ours is a diver holding out a fish.
  - mzeN0BXR4e0: a pale subject with a small human between the text and the creature.
- **Composition:**
  - The s14_twist frame on a bright, shallow reef (Ocean depth 6, rays 7). The moray slides out of its wall hole toward a Diver (arms forward) on the right, who holds out a small grey fish.
  - A red arrow from the text to the diver's hand, not the moray: the hand is the bait.
  - The light mood is the twist: the friendly-looking scene is the dangerous one.
- **Text (4 words):** **IT'S THE FRIENDLY ONE** ("FRIENDLY" red).
- **Colours:**
  - bright reef teal #1d6f80 -> #0d3b45, coral pink/ochre
  - moray olive, diver black #1a1d22 with yellow fins
  - white text, red "FRIENDLY" and arrow
- **Kit / storyboard assets:** explainer/Ocean, explainer/Diver (`arms: forward`, `bubbles`), SVG_WALL, SVG_MORAY_BODY, SVG_FISH, explainer/Headline. Later: thumbs `scale` template with `explainer/Moray` as `art` and `explainer/Diver` as `humanArt`.
- **Payoff on screen:** 56.1 s (78%). It gives away the twist, so it is not for the main upload. Use it for the 16:9 compilation cut or a re-upload titled with titles.md option 8.

## Ranking

A for the TikTok and Shorts cover (it is frame 0, so the cover and the loop agree), and B as the shelf A/B partner. C stays out of the main upload because it spoils the twist.
