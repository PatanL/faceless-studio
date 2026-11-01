# Thumbnail concepts: whatif-you-100x-taller

There are three concepts. Each is rendered as a Remotion still on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube) from the same whatif and explainer art the video uses, so the cover looks like the video. Thumbs-kit rules apply (`studio/src/kits/thumbs/README.md`): one big subject plus one tiny human, 2-4 words in Montserrat 900 with a heavy black outline, and one accent colour. Here the accent is the video's keyword yellow (#FFE14D) instead of the kit's default red. The thumbs kit has no whatif template yet (only explainer/horror), so each concept lists the layers a `whatif` template needs. Library rule to respect: the thumbnail word or number should pay off on screen within about 10 s (`research/library/index_notes/whatif.md`, technique 10). Retention note: lean on the twist angle (your own body is the threat), not on size alone, because size-only near-repeats decay (PLAYBOOK §8).

## A. "Frame-0 cover" (TikTok cover, recommended for the 9:16 post)

- **Inspired by:** 7694025665993100576 POPSTAR (cover = the giant already in frame 1 under the title); 7693494009494342945 ELECTRONS and 7693617402180881697 NEUTRONS (cover = calm named place + title in the upper third + HUD countdown top-left).
- **Composition:** the actual first frame. A pre-dawn side view of the Champ de Mars: the 170 m YOU lies asleep along the lawn, head to camera-left, feet toward the Eiffel Tower (about twice your length). Dot-sized cars on the avenue and one tiny walker (explainer/You, 1.75 m) beside your hand give the tiny-human scale; at true scale the walker is about 5 px, so add a thin yellow pointer ring around it (the kit's pointer, recoloured). HUD top-left: YOU WAKE UP IN 6.9 S / 170 M TALL. Because the cover is frame 0, the TikTok loop and the cover agree.
- **Text (2 words):** **100× TALLER** ("100×" in yellow), in a heavy outlined block in the sky above the title area. On TikTok the serif title can stay instead of the block.
- **Colours:** pre-dawn blue sky (#2B3F66 -> #E9A27A at the horizon), lawn #5E8A4F, roofline #3A3550, tower #6B5B4E; yellow only on "100×" and the pointer ring; HUD white with a 2 px dark shadow.
- **Kit assets:** whatif/ParisSkyline (palette "predawn"), whatif/EiffelTower, whatif/GiantYou (lying, eyes closed), explainer/You (tiny walker), whatif/Hud (pre-event state), thumbs pointer.
- **Payoff on screen:** it is frame 0, and "100 times taller" is spoken at 0.2 s.

## B. "YOU LAST 6 MINUTES" (twist angle, A/B test against A on the YouTube Shorts shelf)

- **Inspired by:** _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM WEALTH (a big number in the text block); YznR5NmI3bc STOP-TIME (one punchy line with a full stop, complementary colour pair); 7693494009494342945 ELECTRONS (HUD clock as the hook).
- **Composition:** the race frame (54-60 s). The wide side view with YOU half up on one bent leg, torso at 34°, head 50 m above the lawn; a dashed white ghost crack runs along the planted thigh (the femur card's ghost style). The HUD top-left shows YOU HAVE LASTED 6 MIN 21 S, the stress bar at ×24 against the red ~×25 line, and BLACKOUT IN 0.4 S. A tiny café waiter at the lower right is the tiny human.
- **Text (4 words):** **YOU LAST 6 MINUTES.** ("6 MINUTES." in yellow).
- **Colours:** warm daylight Paris desaturated 20% with a red-orange edge vignette (the blackout); the stress bar's red line is the only red; yellow on the number.
- **Kit assets:** whatif/ParisSkyline (day), whatif/GiantYou (`torsoDeg` 34, `knee` bent), whatif/Bone ghost-crack overlay, whatif/Hud (race state), explainer/You (`pose: stand`, waiter), whatif/StreetFacade café awning (cropped).
- **Payoff on screen:** the survival clock is on screen from 7.0 s, so the idea pays off within 10 s; the exact number lands at 66.4 s. Use B as the A/B variant, not the TikTok cover.

## C. "ON YOUR THUMBNAIL" (wonder image, best screenshot moment)

- **Inspired by:** 7693494009494342945 ELECTRONS 0:15 (POV hands, wonder before horror); b6jmbFcJZCY EVERY-HUMAN and _lu85gSD39k BILLION-YEARS (huge foreground subject plus one tiny human, 2-3 words).
- **Composition:** the POV close (11.2 s). A huge white rounded-rect thumb rises from the bottom edge against a gold sunrise sky, the nail ellipse filling the middle third. A 1.75 m tourist (explainer/You, `pose: wave`, red backpack prop optional) stands on the nail, waving. A thin 1.5 M ScaleBar sits across the nail. The Eiffel Tower is small and soft in the far background so the place still reads.
- **Text (3 words):** **ON YOUR THUMBNAIL.** ("THUMBNAIL." in yellow).
- **Colours:** sunrise gradient (#F2B880 -> #F7D9A8), white thumb with a light grey #D9DEE3 nail, a blue-shirt tourist (#3A8FD6) as the complementary pop against the gold; yellow only on the keyword.
- **Kit assets:** core rect/circle layers (thumb and nail), explainer/You, explainer/ScaleBar, whatif/EiffelTower (background, blurred 2 px).
- **Payoff on screen:** 11.2 s, about 1 s outside the 10 s rule, so it is a second A/B variant. It is the most shareable still and suits the YouTube 16:9 crop (thumb at left, tourist centre, text at right).

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-you-100x-taller/thumbs.json` with variants `cover` (A), `lasted` (B) and `thumb` (C), then run `OUT=thumbs/whatif-100x scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text has to read at 120 px tall, and the tiny walker in A needs its pointer ring to be visible at all.
