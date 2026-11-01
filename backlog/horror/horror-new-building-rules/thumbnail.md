# Thumbnail concepts: horror-new-building-rules

Three concepts, all rendered as code stills with the thumbs kit (`studio/src/kits/thumbs`, horror templates `chat`, `hallway`, `door`) from `thumbs.json` in this folder, on the Spark: `OUT=thumbs/horror-new-building-rules scripts/thumbs_render.sh backlog/horror/horror-new-building-rules/thumbs.json`. Results (1280x720 and 1080x1920, plus contact sheets) are in `out/thumbs/horror-new-building-rules/`; I checked the 16:9 sheet at feed size.

House formula (thumbs README): one big subject, one tiny human, 2-4 words in Montserrat 900 with a heavy outline, exactly one red accent word, a cold teal grade. The pilot's thumbnails already use "RULE 4: DON'T ANSWER THE DOOR" and "WHO WROTE RULE 4?" (`episodes/horror-pinned-rules/thumbs.json`), so no "RULE 4", "door" or "who wrote" wording is reused here.

On TikTok the cover is **frame 0**, not a designed thumbnail (library horror notes: the outliers' frame 0 shows a readable threat with a burned-in caption fragment). Both parts are built for that:
- P1 frame 0: the residents' chat with the red Building Office alert ("Night check. Please reply with your unit number...") over the blurred front door with a **feet shadow** under it, caption "At 5:12," on top.
- P2 frame 0: the front door on the tail of the third knock, impact marks, hall light under it, the feet shadow; caption "Three knocks."

Reference thumbnails studied (structure only, nothing traced; notes in `research/library/videos/<id>.json`):
- **7659677578365537569** (SIEGE-CHAT, 376K, 10.8x): one-point corridor, a figure near the vanishing point, a short first-person caption fragment above the picture, a single red accent.
- **7654526047005723937** (SIEGE-OVERLAY, 717K, 66.7x): black silhouette in a dim corridor, the threat readable at feed size, one caption line.
- **BciSW_2VMZg** (WrONG Rules "New Household Rules (Pt3?)", 104K, 11.0x): one centred subject filling the frame, 3 scratchy all-caps words, an instruction rather than a label.
- **T42u5xhrq-0** (TEXT-FIGURE, 869K, 25.5x) and the library note that YouTube horror outliers use a "phone-notification mock-up": the chat itself as the image.

## A. "DON'T REPLY" (primary for Part 1, pairs with title 1)

- **Inspired by:** T42u5xhrq-0 (the chat is the scare) and BciSW_2VMZg (an order, not a label). The roll call reads as a pattern even at thumbnail size: request, 7A, 7B, 7E, then "except one".
- **Composition:** big tilted phone filling the right half with the residents' chat: Building Office "Please reply with your unit number.", three one-word replies (7A / 7B / 7E), then Building Office "Every unit has replied except one." in the large last bubble. Tiny June bottom-left in bed, lit by her phone, terrified.
- **Text (2 words):** **DON'T REPLY**, "REPLY" red, top-left.
- **Colours:** near-black teal room, white phone UI, one red word.
- **Kit assets:** thumbs `chat` template; `humanArt` = `horror/Protagonist` (pose phone, expr terrified, light phone); `chat` lines in thumbs.json.
- **Pays on screen:** 0:00-0:04 (the request) and 1:06 (the DM).
- **Check:** the five chat lines read at 16:9 feed size; at 9:16 the last bubble must stay above the platform UI band.

## B. "EXCEPT ONE" (A/B partner; the series look for Part 2)

- **Inspired by:** 7659677578365537569 (one-point corridor, a small figure at depth) and 7654526047005723937 (a black silhouette that reads at a glance).
- **Composition:** a long dark corridor; doors down both sides, the far door on the right plated "7C"; tiny June sits at the far end with her phone; a huge black silhouette crops into the right edge of the frame with glinting eyes.
- **Text (2 words):** **EXCEPT ONE**, "ONE" red, top-left.
- **Colours:** grey-teal corridor, black figure, one red word.
- **Kit assets:** thumbs `hallway` template, `room: "7C"`, the same `humanArt`.
- **Pays on screen:** 1:06 P1 ("Every unit on seven has replied except one") and the dark doors in both parts.
- **Note:** the template's corridor has no door lamps. If B wins the A/B, add amber lamps over three doors and leave the 7C door lit; that is a thumbs-kit tier-S tweak, not a new asset.

## C. "NEVER LEFT 7C" (primary for Part 2, pairs with "Someone Else Lives In My Apartment")

- **Inspired by:** BciSW_2VMZg (one subject, a short line from the story itself) and HEARSE-P1's bookend logic (the cover is the last image of the episode, one step worse).
- **Composition:** a door marked 7C standing open, a too-tall black figure in the gap, a warm pool of light on the floor where tiny June sits with her phone. Reads as "it's already inside her apartment", which is the Part 2 twist without spelling it out.
- **Text (3 words):** **NEVER LEFT 7C**, "7C" red.
- **Colours:** blue-black walls, warm floor pool, black figure, one red token.
- **Kit assets:** thumbs `door` template, `room: "7C"`, the same `humanArt`.
- **Pays on screen:** P2 1:13 (the slip: "I never left 7C.") and the knocks from inside.
- **Caution:** the template's grin is generic; keep it (it reads at feed size) but don't add any blood or injury (ad suitability, research/R5).

## Pick

- YouTube Shorts thumbnail / cover override: **A for Part 1, C for Part 2**. A/B **B** against A on Part 1 if the platform allows.
- TikTok: frame 0 is the cover (built into both storyboards); no override.
