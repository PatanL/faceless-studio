# Thumbnail concepts: explainer-short-blue-whale-scale

Three concepts, rendered with the thumbs kit (`studio/src/kits/thumbs`, Spark only, 1080x1920 cover + 1280x720) from the same explainer art the video uses, so the cover matches the video. The kit formula:
- one big subject plus one tiny human
- 2-4 words in Montserrat 900, white with a black outline
- one red accent word, continued as a hand-drawn red pointer to the tiny human

Library rule (`research/library/index_notes/explainer.md` #10): the thumbnail adds a claim the title does not make, and for Shorts frame 0 is the cover. Every concept must also pay off on screen within ~10 s or say why it does not.

## A. "Frame-0 scoreboard" (recommended TikTok / Shorts cover)

- **Inspired by:** fGcgWaswMns (Depth Theory sperm whale: a huge whale on the right, a tiny diver lower left, a red arrow from the red word to the human, 3 words "IT HEARS YOU.."). Also 6mRR91AbxjQ (frame 0 is the thumbnail and the subject is on screen in the first frame).
- **Composition:** the actual frame 0. The whole blue whale, in full colour, spans the upper third (pxPerM 36). The true-scale YOU (63 px) floats at its eye. A white-ringed magnifier inset (lower right) shows YOU at 300 px pointing at the whale, linked by a dashed line. The scoreboard chip `WHALE 0 : 0 YOU` sits top centre. Over the empty water in the middle third, the cover adds one text block, with the kit's red pointer curving from "ONE" down to the magnified YOU.
- **Text (4 words):** **YOU WIN ONE.** ("ONE." in red). It adds a claim to option-1 title wording only when the title is A/B'd to option 2 or 3. With option 1, use **WHICH ONE?** instead (2 words, "ONE?" red).
- **Colours:** ocean teal gradient #0b3a4a → #06141b, whale blue-grey #5f7f96 with pale spots, YOU white, chip #0b1a22 with a red left bar, one red #e5483d accent.
- **Kit assets:** explainer/Ocean, explainer/BlueWhale (pxPerM 36), explainer/You x2 (shrug 63 px, point 300 px), core circle (magnifier), explainer/Tag (scoreboard), thumbs `scale` template text block + red pointer.
- **Payoff on screen:** it is the first 2.9 s, and "you win one" is spoken at 2.25 s.

## B. "The ring" (recommended for the YouTube Shorts shelf and the 16:9 grid)

- **Inspired by:** QxM2Hu70tVk (Dumb Doggo: a flat cartoon stick-figure YOU caught mid-comedy by the threat, no text, a menu of threats in one tableau), fGcgWaswMns (red word plus pointer), and the episode's own 0:52-0:54 beat.
- **Composition:** the round-5 set. The deep red inside-the-vessel gradient, with the 23 cm aorta ring (red, 18 px stroke) stuck around the grey face-on bust's shoulders. The head pokes through, the face is a deadpan smile, and two small red impact ticks mark where the shoulders hit. The scoreboard chip top centre reads `WHALE 4 : 1 YOU`, with the "1" in green.
- **Text (3 words):** **TOO BIG. FINALLY.** ("BIG." in red). It adds the irony the title only hints at. It does not say which round, so the spine loop survives. It reads at 120 px tall.
- **Colours:** red interior #6a1018 → #120203, slate bust #8fa3ae with a white outline, ring and accent word red #e5483d, one green #3ddc84 digit in the chip. Use one red accent only. The green is a score colour, not a second word accent.
- **Kit assets:** inline svg bust and ring from `gen_storyboard.py` (`bust_svg`, core circle), explainer/Tag (chip), thumbs text block. The thumbs kit needs one small addition: an `art` slot that takes an inline svg layer (the `scale`/`eye`/`abyss` templates are fixed art).
- **Payoff on screen:** late (0:52-0:56). That breaks the 10 s rule, so use B only on the YouTube shelf, where the thumbnail is not the video's first frame, and never as the TikTok cover. It also gives away the result, so test it against A.

## C. "35 of you" (A/B variant, turnstile hook)

- **Inspired by:** fGcgWaswMns (a huge subject, a tiny human, a red pointer) and jw6bS-WL4F4 (Casual Geographic: a "tiny thing is worse" paradox. Here it is reversed: a baby that outweighs a crowd of you).
- **Composition:** the round-3 lagoon set (turquoise #5fd0d8 → #0d4f66). The newborn calf (7 m) fills the upper half. Below it is the 7x5 grid of 35 white stick icons, and one icon is red with the red pointer to it ("you").
- **Text (3 words):** **IT'S A BABY.** ("BABY." in red).
- **Colours:** lagoon turquoise, calf blue-grey, white icons, one red icon plus the red word.
- **Kit assets:** explainer/Ocean (topColor/midColor/bottomColor), explainer/BlueWhale (pxPerM 30), the count-grid svg rows (`icon_row` in `gen_storyboard.py`), explainer/Stat "~2.5 T" (optional, small), thumbs text block + pointer.
- **Payoff on screen:** 0:26.5-0:30 ("it's a baby" ... "thirty-five of you"). That is later than 10 s, but it is the turnstile, so the cover promise is paid at 45%. It does not touch the win, so the spine loop stays open.

## Render

Once the thumbs kit can take inline svg/component art, write `episodes/explainer-short-blue-whale-scale/thumbs.json` with variants `cover` (A), `ring` (B) and `baby` (C), then run `OUT=thumbs/blue-whale-scale scripts/thumbs_render.sh <spec>` (Spark only). Until then, A can come straight from the storyboard: `scripts/spark_stills.sh backlog/explainer/explainer-short-blue-whale-scale/storyboard.json 0.0` already renders the cover frame (checked at 11:37 UTC, out/stills/bw_scale.jpg tile 1). Check the sheet at phone size: the 63 px YOU is too small to read, which is why A carries the 300 px inset, and the "ONE" pointer must land on the inset, not on the tiny figure.
