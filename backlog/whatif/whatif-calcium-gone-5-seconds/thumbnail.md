# Thumbnail concepts: whatif-calcium-gone-5-seconds

There are three concepts. Each is rendered as a Remotion still on the Spark (thumbs kit, 1080x1920 cover plus 1280x720 for YouTube) from the same whatif and explainer art the video uses, so the cover looks like the video. Thumbs-kit rules: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a black outline, one accent colour (X-ray cyan #7FE3FF here, plus pure white, which means calcium in this episode). The thumbs kit has no `whatif` template yet (only explainer/horror), so each concept lists the layers that template needs. Library rule to respect: the thumbnail word or number must pay off on screen within about 10 s (research/library/index_notes/whatif.md, technique 10).

## A. "Frame-0 cover" (TikTok cover, recommended for the 9:16 post)

- **Inspired by:** 7693494009494342945 ELECTRONS and 7693617402180881697 NEUTRONS covers (frame 0 = a calm named place, the title in the upper third, the HUD countdown at left); 7693305573487562016 OXYGEN cover (calm baseline scene with the HUD baseline reading).
- **Composition:** the actual first frame. A sunny flat-vector Colosseum fills the middle third (three arcade tiers, broken outer ring on the right). The tourist queue stands on a pale travertine kerb in the lower third, YOU in white with the "YOU" tag, and the marble bust on its granite plinth at the right end of the queue. The serif title sits in the upper third with the cyan bone glyph above "calcium". HUD top-left: CALCIUM ● ONLINE / OFFLINE IN 7.000 S / IN EVERY BONE, HEARTBEAT AND LIMESTONE. Because the cover matches frame 0, the TikTok loop and the cover agree.
- **Text (2-4 words):** the cover keeps the serif video title instead of a block caption. For the YouTube Shorts shelf, add one outlined block in the sky: **5 SECONDS. NO BONES.** ("NO BONES." in cyan).
- **Colours:** noon sky #8EC9F0 → #F4E3C1, travertine beige #E6D8B8 with #B9A57E shadow lines, muted tourist colours; keyword, glyph and HUD numbers in cyan #7FE3FF; HUD text white with a 2 px dark shadow.
- **Kit assets:** whatif/Colosseum (mode day), whatif/Statue (day), explainer/You x9 + explainer/Tag, whatif/TitleCard (bone glyph), whatif/Hud.
- **Payoff on screen:** the same image is the first 5.5 s; "no bones" pays off at 0:07 (the blink-out) and 0:08 (bendy fingers).

## B. "X-ray split" (before/after, recommended for the YouTube 16:9 and the Shorts shelf)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (the same subject twice, "TODAY" vs "50 YEARS LATER", 4 words in total); J3XahLkDEzU LAST-HUMAN (a slanted split, the same hero in each half, labels in the top corners); the episode's own 0:05.5 scan line as the split edge.
- **Composition:** a slanted split along a glowing cyan scan line. Left half, X-ray "before": navy #050B18, the queue as cyan line-art skeletons with bones filled pure white, the Colosseum's blocks glowing white behind them. Right half, the same framing "after": every white gone, skeletons outline-only and folded into heaps, the arcade pouring into a sand mound. YOU's skeleton sits right on the split: white bones left of the line, empty outline right of it. A tiny "YOU" tag gives the human scale.
- **Text (4 words):** **WITH CALCIUM** (white, top-left corner) / **WITHOUT** (cyan, top-right corner), on label plates.
- **Colours:** navy #050B18 ground, cyan #7FE3FF line art, pure white only in the left half (white = calcium); thick black outlines on the text.
- **Kit assets:** whatif/XrayFigure x9 (glow 1 / slump 1), whatif/Colosseum (mode xray, glow 1 / pour 1 + mound), explainer/Tag, core rect (scan line with glow), thumbs-kit label plates.
- **Payoff on screen:** the left half is shot 2 (0:05.5); the right half is shot 8 (0:27.5-0:31.5). The "without" half pays later than 10 s, but the blink-out at 0:07 pays the white-to-outline change straight away.

## C. "1 M TOO HIGH" (twist hook, best for an A/B test against B)

- **Inspired by:** YznR5NmI3bc STOP-TIME (a huge foreground subject, one punchy line with a full stop, a complementary colour pair); _lu85gSD39k BILLION-YEARS and DK4EOHCrVvM (a big number in the text block); 7694025665993100576 POPSTAR (a measured gap between the hero and the thing above them).
- **Composition:** the twist frame. Low three-quarter view of the queue: one folded line-art heap (YOU) on the sand, and directly above it a glowing white ghost skeleton standing upright in mid-air, with a dashed cyan bracket between them labelled "1 M". The white ghost Colosseum hangs faintly over its sand mound behind.
- **Text (3 words):** **1 M TOO HIGH.** ("1 M" in cyan, "TOO HIGH." in white), heavy outlined block in the upper third.
- **Colours:** navy #050B18 and cyan line art against the pure-white ghost (the only white in the image), cyan bracket; a cool palette with one bright subject, so it reads at 120 px tall.
- **Kit assets:** whatif/XrayFigure (heap, plus `ghost: true`, `offsetYM: 1`), whatif/Colosseum (`ghost: true`, mound), core callout `label` for "1 M", dashed bracket svg.
- **Payoff on screen:** pays late (1:09.5-1:11). That breaks the "within 10 s" library rule, so use C only as an A/B variant. It also gives away the twist, so test it on the YouTube Shorts shelf, not as the TikTok cover.

## Render

Once the thumbs kit has a `whatif` template, write `episodes/whatif-calcium-gone-5-seconds/thumbs.json` with variants `cover` (A), `split` (B) and `ghost` (C), then run `OUT=thumbs/whatif-calcium scripts/thumbs_render.sh <spec>` (Spark only). Check the contact sheet at phone size: the text must read at 120 px tall, and in B the white bones must survive JPEG compression (raise the stroke to 4 px if they smear).
