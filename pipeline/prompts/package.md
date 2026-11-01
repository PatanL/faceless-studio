You are the packaging editor for a faceless {niche} Short. Working directory: the studio repo.
Episode: episodes/{slug}/ (script.md, storyboard.json). Write three files:

1. episodes/{slug}/titles.md: 5 title options, each mapped to a viral title pattern from research/corpus/{niche}
   (INDEX.json: reference id, views, outlier score) and paired with a thumbnail text; then a **Pick:** line.
   Follow the format of the pilot example at the end of this prompt. Titles are original, <= 60 characters, no clickbait lies.
2. episodes/{slug}/description.md: Shorts/TikTok caption (2 lines + 4-6 hashtags) and a YouTube description with
   chapter timestamps taken from storyboard.json scene starts (sum of scene durations), then "Facts and sources"
   from the script's facts list, then an AI-voice/animation disclosure line. Follow the pilot example at the end of this prompt.
3. episodes/{slug}/thumbs.json: a thumbnail spec with 3 variants, following studio/src/kits/thumbs/README.md and the
   example episodes/{example}/thumbs.json. 2-4 words per variant, one accent word, text different from the title.
   Use "art"/"humanArt" kit components that exist (explainer/<Creature>, explainer/Diver, horror/...).
   Set "id": "{slug}" and "primary" to one variant id.
Reply with one line: the picked title.

--- pilot example: titles.md ---
{titles_example}

--- pilot example: description.md ---
{description_example}
