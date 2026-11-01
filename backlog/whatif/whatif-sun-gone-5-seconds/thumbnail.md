# Thumbnail concepts: whatif-sun-gone-5-seconds

There are three concepts. Each is rendered as a Remotion still on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube) from the same whatif art the video uses, so the cover looks like the video. Thumbs-kit rules apply: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, and one accent colour (amber #FFB547, matching the video's keyword and HUD). The thumbs kit has no whatif template yet (only explainer/horror), so each concept lists the layers a `whatif` template needs. Library rule to respect: the thumbnail word or number must pay off on screen within about 10 s (research/library/index_notes/whatif.md, technique 10).

## A. "Two vantages" (TikTok cover, recommended for the 9:16 post)

- **Inspired by:** 7693494009494342945 ELECTRONS and 7693617402180881697 NEUTRONS covers (frame 0 = calm named place + serif title + HUD countdown at top-left); b6jmbFcJZCY EVERY-HUMAN (the same subject shown twice as a before/after pair).
- **Composition:** frame 0.07 s after the event, not frame 0, so the contradiction is visible: top 40% is the AT THE SUN panel with an empty dark point where the Sun was and a fading white ring; bottom 60% is Copacabana at noon, still bright, with the ghost Sun in its sky and the small amber label STILL SHINING. STILL PULLING. "You" stands small on the sand with a short noon shadow. HUD top-left reads SINCE THE SUN VANISHED / T+0:00.070 / 1×.
- **Text (2-4 words):** the cover keeps the serif video title in the beach sky. For the YouTube Shorts shelf, add one outlined block across the seam: **SUN GONE. BEACH FINE.** ("SUN GONE." in amber on the top panel, "BEACH FINE." in white on the beach).
- **Colours:** black space (#05070D) over a bright beach (sand #F3E3C3, sea #2FB7C9 -> #1C7FA6, headland #3E7D4E, sky #9AD6F0); amber #FFB547 for the keyword, labels and HUD numbers; white seam line.
- **Kit assets:** whatif/SolarMap (mode sunClose, sunScale 0, emptyMarker), whatif/BeachNoon (day, ghostSun), explainer/You (stand), whatif/Hud, whatif/TitleCard, a core circle for the white ring.
- **Payoff on screen:** the same image is on screen at 0:07-0:12; "STILL SHINING" pays off at 0:08.5.

## B. "The shadow is coming" (YouTube 16:9 and the Shorts shelf)

- **Inspired by:** 7694025665993100576 POPSTAR-100x and 7693305573487562016 OXYGEN (a threat with a distance counting down to HERE); _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM (a big number as the text block).
- **Composition:** the full-frame space diagram from shot 4 at about 0:34: a pale amber sunlight wash, the dark 5-light-second band with bright edges sweeping outward, Mercury and Venus already grey, Earth blue with the YOU pin just ahead of the band. A dashed amber distance line from the band to the pin carries the tick label "19 MILLION KM". The HUD reads SHADOW: 19.2 MILLION KM AWAY / ▶▶ 30×.
- **Text (3-4 words):** **IT'S COMING. 8 MIN.** ("8 MIN." in amber), heavy outlined block in the upper third.
- **Colours:** near-black space with the warm amber wash, a cool grey band, saturated blue Earth (#4FB3FF) against the amber text: a blue/amber complementary pair.
- **Kit assets:** whatif/SolarMap (mode inner, band, planets greyed, YOU pin), core particles stars, whatif/Hud, core label callout for the distance tick.
- **Payoff on screen:** the 8-minute number pays off at 0:16.3 ("Its light needs 8 minutes 19 seconds."), and the band from 0:22. Both inside the first 25 s; the HUD distance line is on screen from 0:12.

## C. "+47 µs" (number hook, best as an A/B variant against B)

- **Inspired by:** YznR5NmI3bc STOP-TIME (one huge foreground subject, a single punchy word with a full stop, a complementary colour pair); 7693494009494342945 ELECTRONS end card (a small "your" fact under the title).
- **Composition:** the shot 11 orbit diagram, cropped: Earth's old orbit dashed white and the new one solid amber, pulled visibly apart (exaggerated), with the YOU pin on Earth; a small birthday-cake icon riding on the amber orbit. Tiny "you" figure standing on top of the Earth dot for scale contrast.
- **Text (2-3 words):** **YOUR YEAR: +47 µs** ("+47 µs" in amber), outlined block upper third.
- **Colours:** black space, white/amber orbits, amber text; the cake icon is the only extra colour (pink #F29BB8) so it reads at small sizes.
- **Kit assets:** whatif/SolarMap (mode fullOrbit, offset exaggerated), explainer/You (stand, tiny), a small cake `svg`, core text.
- **Payoff on screen:** late (1:08.3). It breaks the "within 10 s" library rule, so use C only as an A/B variant; the ONE YEAR: 365.256 DAYS plant is on screen from frame 0, which softens the miss.

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-sun-gone-5-seconds/thumbs.json` with variants `vantages` (A), `shadow` (B) and `year` (C), then run `OUT=thumbs/whatif-sun scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text has to read at 120 px tall, and in A the empty top panel must still read as "Sun gone" (keep the white ring at least 40% opacity).
