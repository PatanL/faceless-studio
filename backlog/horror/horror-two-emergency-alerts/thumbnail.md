# Thumbnails: horror-two-emergency-alerts

Three concepts, 1080x1920 (9:16 cover) with a 1280x720 crop note. PLAYBOOK §6 rules: the cover shows the threat, there is one red element on near-black, and the text is 2-4 words in the top third so it stays clear of the platform UI at the bottom. All art comes from what `build.py` already draws (no new assets): `WALLPAPER`, `alert_card()`, `PEEPHOLE`, `held_phone_svg()`, `DOOR_GAP`, `CHAIN_ECU`, the recoloured `horror/Protagonist` (TESS_COLORS), and `horror/Vignette` / `horror/Darkness`. Render them with `scripts/thumbs_render.sh` / the thumbs kit once promoted.

## A (primary): "THAT'S MY PHONE" (the peephole)

- **Composition:** the peephole circle fills the middle 80% of the frame (the `PEEPHOLE` svg at radius 440). The man's phone is pressed flat to the lens at 1.4x, as in shot s23's held frame. It shows her lock screen: wallpaper moon, 3:09, three red alert strips. The backlit man in the cap is behind it, and two open black doorways sit at the lens edges. Outside the lens is pure black.
- **Text:** `THAT'S MY PHONE` (3 words), white Anton with a 12 px black stroke, top 18% of the frame. "MY" is red #e0262f.
- **Colours:** near-black #030304, warm hall amber #3a3326 inside the lens, alert red #e0262f (the only saturated colour), moon cream #f3e3c3.
- **Kit assets:** `PEEPHOLE` + `held_phone_svg("3:09")` + `horror/Vignette` amount 0.5.
- **Why:** it is the scariest image (65-68%) and it reads at thumbnail size: a phone inside a peephole is legible at 200 px. Inspired by:
  - the door/peephole POV frames that carry SIEGE-OVERLAY's cover (7654526047005723937, sheet tiles 0:20 and 3:52: the antagonist framed in a dark doorway);
  - CLASSMATE-PSA's single red element on near-black (omuJBFs2L6c, the red figure against white pictograms).
- **16:9 crop:** the lens on the right two-thirds; the text stacked on the left.

## B: "SPOT THE FAKE" (the v)

- **Composition:** two alert cards stacked at 1.6x scale and tilted -4°, held in the static phone frame with the wallpaper behind. On the top card the sender reads "Lindhurst Count**v**" with a thick red hand-drawn ring around the v. The lower card reads "Lindhurst County" with a green underline under the y. A red arrow points at the ring.
- **Text:** `SPOT THE FAKE` (3 words) in the top band.
- **Colours:** wallpaper purple-to-navy, card black #1a0f12, alert red, one green #4ade80 underline.
- **Kit assets:** `phone_frame()` + `alert_card("a2")` + `alert_card("a1")` at scale 1.6, plus a red ring svg.
- **Why:** it is a participation prompt (viewers check the letter), and the countable-anomaly promise matches the title "One of Your Classmates Is Not Real" (omuJBFs2L6c, 763K). It also matches MOM-NOTE's colour-keyword covers (cVUJmsVkUW4, 291K, 31x). It pairs with title #4.
- **Risk:** at feed size the v vs y difference needs the ring. Check legibility at 240 px wide before picking it.

## C: "DON'T OPEN IT" (the door on the chain)

- **Composition:**
  - Left two-thirds: the `DOOR_GAP` frame, with the door open four inches on a taut chain and a blade of warm hall light.
  - Foreground lower right: Tess's hand (Protagonist, pose phone, light phone) holding her phone toward camera, with the alert 4 card readable: "TESS AVILA · 11F · ONE OCCUPANT. Open the door."
  - The `horror/Darkness` light pool is on the gap.
- **Text:** `DON'T OPEN IT` (3 words), with "OPEN" in red.
- **Colours:** blue-black #0a0c10, hall light #f2d79a, alert red.
- **Kit assets:** `DOOR_GAP`, `alert_card("a4")`, `horror/Protagonist` (TESS_COLORS), `horror/Darkness`.
- **Why:** the barrier the viewer knows (a door) plus the imperative, as in the ending of SIEGE-CHAT (7659677578365537569, 4:05-4:08: a lone phone glowing in a dark room with an order on it). HOTEL-DOOR's intruder-at-the-lock crop (Qz-TrB6W2SM, 1:25-1:29) frames the threat only through the door edge.
- **Note:** it gives away the final alert but not the twist. Use it for the 16:9 / long-shelf version.

**Pick:** A for Shorts/TikTok with title #1. A/B test B with title #4.
