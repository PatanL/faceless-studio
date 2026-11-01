# Thumbnail concepts: explainer-never-meet-leopard-seal

Three concepts, all Remotion stills rendered on the Spark only. The thumbs kit outputs 1280x720 for YouTube plus 1080x1920 for the Shorts cover, and the art comes from the same explainer pieces the video uses, so the cover matches the video. Thumbs-kit rules (`studio/src/kits/thumbs/README.md`): one big subject and one tiny human, 2-4 words in Montserrat 900 white with a heavy black outline, and one red accent word that continues as a hand-drawn red pointer to the tiny human (the Depth Theory signature). Library rule (`research/library/index_notes/explainer.md`, technique 10): the text adds a claim the title doesn't make and pays off on screen early. The existing explainer templates are `eye`, `scale` and `abyss`, with placeholder subjects whale, squid and angler. Each concept below names the template it extends and the NEW subject it needs (`leopardSeal`, drawn from the NEW `explainer/LeopardSeal` rig, so it is built once and used in both places).

## A. "IT ISN'T SMILING" (recommended for YouTube 16:9, pairs with title 1)

- **Inspired by:** fGcgWaswMns SPERM (2.31M, 14.65x): huge head close on near-black, 2-3 words that add a new claim ("IT HEARS YOU.."), a red pointer to a tiny diver. Also VtrcKTkhDHU ORCA (8.29M): the predator's face filling the frame head-on. Ours stays side profile, because the kit is profile-only and the smile reads best that way.
- **Composition:** the 0:22 frame, pushed in. The leopard seal's side-profile head fills the right two-thirds, rising over the floe edge with the upturned mouth line catching the light, and one dark eye. Left third: the white floe edge, with a tiny kneeling YOU and camera on top, back to the seal. Under the waterline, a faint spotted body shape runs back under the ice, so the head is clearly attached to something 3.5 m long.
- **Text (3 words):** **IT ISN'T SMILING** ("SMILING" red), upper left. The red pointer runs from "SMILING" down to the tiny YOU.
- **Colours:** near-black teal sky and water (#06131a -> #0f3a4a), ice white #e8eef0 with a cold blue shadow #9fb3bb, seal grey #6d7a80 with darker spots #2b3438 and a pale throat #c9cfcf. Red #ff5a4a only on the word and pointer.
- **Kit assets:** thumbs `eye` template (subject `leopardSeal`, `surface` pose, sonar rings off), NEW `explainer/IceFloe`, `explainer/You` (`kneel` + `camera`), thumbs red pointer.
- **Payoff on screen:** the face rises at 0:22 and "It isn't smiling." is spoken at 0:28, both inside the first 30 s.

## B. "TWO OF YOU" (scale, A/B against A)

- **Inspired by:** the `scale` template lineage, fGcgWaswMns SPERM 1:12 (buses under the whale, an everyday unit next to the monster), and QxM2Hu70tVk PLANT (16.18M) and nAWpLtG-kNs ERAS (12.21M), whose shrunken or prey-sized human against a big subject reads at phone size.
- **Composition:** the full leopard seal side-on across the frame at true scale (`pxPerM`), jaw open about 40° with the fang row visible. Two tiny YOU figures lie end to end under it, the same length as the seal. A white ruler bar under them reads ~3.5 M. A penguin silhouette hangs from the seal's mouth line, cartoon-flat, no detail.
- **Text (3 words):** **TWO OF YOU** ("YOU" red); the red pointer lands on the second lying figure.
- **Colours:** mid-teal water gradient (#0f3a4a -> #082028), seal grey with spots, YOU figures white, ruler white with a black outline, red only on "YOU" and the pointer.
- **Kit assets:** thumbs `scale` template (subject `leopardSeal`, `label: "~3.5 M"`, `humanLabel` off), `explainer/You` NEW `lying` pose x2, NEW `explainer/Penguin` (silhouette).
- **Payoff on screen:** the two-of-you comparison lands at 0:59 (shot 9). That is later than A but still in the first minute, so it's fine for YouTube and not used as the Shorts cover.

## C. "IT FED HIM" (paradox, best for the Shorts cover and a later re-test)

- **Inspired by:** VtrcKTkhDHU ORCA (8.29M, 318.82x), whose title and thumbnail sell a restraint paradox rather than a threat; mzeN0BXR4e0 DEEP (17.22M), whose text makes a new claim ("WE REALLY CAN'T EXPLAIN"); and the Nat Geo competitor Zxa6P73Awcg (12.3M), which proves the Nicklen encounter is the most-watched leopard seal story.
- **Composition:** a diver with a big camera housing on the left, small. The seal fills the right half, jaw wide open with its mouth around the camera housing, looking almost tender. Between them, a single limp cartoon penguin drifts with a small gift-ribbon loop. Bubbles rise from the seal's nostrils.
- **Text (3 words):** **IT FED HIM** ("FED" red), or the 4-word variant **IT TRIED TO FEED HIM**. The red pointer goes to the diver.
- **Colours:** brighter shallow-water teal (#1d6f80 -> #0f3a4a) with light rays, so the image reads as strange rather than scary; seal grey, diver dark blue #1b2a3a with a yellow tank, penguin black and white, red only on "FED".
- **Kit assets:** thumbs `eye` or `scale` template with the `leopardSeal` subject at `jaw` 75 (the cap), `explainer/Diver` NEW `camera` prop, NEW `explainer/Penguin` `pose: limp`, core `particles` bubbles.
- **Payoff on screen:** the gift story is at 7:50-8:55, which is late. So use C for the Shorts cut-down of the payoff (where it pays off within 10 s), or as a YouTube A/B variant only after A and B have data. It must never be the long-form's only thumbnail.

## Render

Once the thumbs kit has a `leopardSeal` subject (it reuses the `explainer/LeopardSeal` rig), write `episodes/explainer-never-meet-leopard-seal/thumbs.json` with variants `smile` (A), `scale` (B) and `fed` (C). Then run, on the Spark only, `OUT=thumbs/explainer-never-meet-leopard-seal scripts/thumbs_render.sh episodes/explainer-never-meet-leopard-seal/thumbs.json`. Check the contact sheet at phone size: the text must read at 120 px tall, and the upturned mouth line in A has to stay visible at that size (thicken the lip stroke for the thumbnail if it doesn't).
