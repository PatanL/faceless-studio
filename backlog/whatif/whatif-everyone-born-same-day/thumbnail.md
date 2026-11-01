# Thumbnail concepts: whatif-everyone-born-same-day

There are three concepts, each rendered as a 1280x720 Remotion still on the Spark from the same `whatif` assets the video uses, so the thumbnail looks like the video. Thumbs-kit rules: one big subject plus one tiny human, 2-4 words in heavy Montserrat 900 with a thick black outline, and one accent colour. The accent here is the cohort amber `#F2B33D`, matching the video's keyword colour instead of the kit's default yellow. `studio/src/kits/thumbs/templates/` has only `explainer.tsx` and `horror.tsx`, so each concept lists the layers a `whatif` template needs. Library rule to respect (research/library/index_notes/whatif.md, technique 10): the thumbnail word or number should pay off on screen within about 10 s.

## A. "8 BILLION. ONE DAY." (recommended default)

- **Inspired by:** 6oZ9fdM0n50 RESTART (4.22M; "ONLY 2 LEFT": 3 words, cream text, the number as the only coloured word, tiny characters in a pool of warm light on a cool street); _lu85gSD39k BILLION-YEARS (413K, 41x; "1 BILLION / YEARS." stacked with a full stop, small centred hero in a big crowd).
- **Composition:** frame 0 of the video, from slightly higher. Side-on rows of cribs run to the horizon at dawn and shrink into a pattern fade. Every crib holds a small amber baby. Front-centre, one crib is a little larger with the cream YOU ring. Beside it stands one grey borrowed adult (`whatif/Person` adult, pose hold), the "tiny human" for scale against the endless field. The top-right corner shows the counter chip `BIRTHS TODAY: 8,000,000,000`.
- **Text (4 words):** **8 BILLION.** (cream) over **ONE DAY.** (amber), stacked bottom-left at ~40% width, full stops on both lines for finality.
- **Colours:** cool dawn blue-violet sky and far rows (#2B3566 -> #5B6AA8) against warm amber cribs and a window-light pool on the front row (complementary violet/amber, as in RESTART); text cream #F4EEDF and amber #F2B33D with a 10 px black outline.
- **Kit assets:** `whatif/Set` (ward, light dawn), `whatif/Crowd` (age baby, fill 1, youIndex), `whatif/Person` (adult, hold, grey), `explainer/Stat` chip.
- **Payoff on screen:** the crib field is 0:00, every crib fills at 0:08 ("Same day as you. Same year as you.") and "Eight billion newborns" lands at 0:11. Within the 10 s rule, near enough.

## B. "TODAY" / "SAME DAY" pyramid split (A/B test against A)

- **Inspired by:** b6jmbFcJZCY EVERY-HUMAN (1.08M, 107x; white ground, the same subject twice, "TODAY" vs "50 YEARS LATER", 4 words); J3XahLkDEzU LAST-HUMAN (914K; slanted white split bar, yellow road-sign labels "DAY 1" / "YEAR 20", 3 words).
- **Composition:** a slanted white split bar. Left half on navy: the real 2024 world pyramid in cream/grey (`whatif/Pyramid` kind world2024), with a tiny stick figure standing on the age-0 band. Right half on navy: the same axes, but one enormous amber bar at age 0 bursting out past the right edge (overflow chevron and `×12` label), with eight tiny amber babies spilling off its end. This answers the "same calendar day or same year?" ambiguity the reference critic raised: one bar means one year.
- **Text (3 words):** road-sign plates **TODAY** (cream plate, top-left) and **SAME DAY** (amber plate, top-right), heavy black sans.
- **Colours:** navy board #13213A both halves; cream/grey bands left, a single saturated amber bar right; white split bar; amber used only on the right plate and bar.
- **Kit assets:** `whatif/Pyramid` x2 (world2024 / cohort with overflow), `whatif/Person` (kid, stand, tiny), `whatif/Crowd` (baby, 8), core `rect` plates + `text`.
- **Payoff on screen:** the pyramid collapse is shot 10 at 0:47, which breaks the 10 s rule. If B wins the A/B, add a 1-second pyramid flash into shot 2 (0:04, the 60-years-of-dots board) so the image appears inside the hook.

## C. "OLDEST: 30" (mid-video hook, best for the Shorts cut and a second A/B)

- **Inspired by:** DK4EOHCrVvM WEALTH (1.17M; a huge glowing number tag floating above a figure, no title text, warm vs dark contrast); 6oZ9fdM0n50 RESTART ("ONLY 2 LEFT": a count as the hook word).
- **Composition:** the YEAR 30 board. A single amber bar at age 30 sits low in frame and empty navy space fills everything above it, with a faint dotted outline where the grey "old world" bands used to be. On the bar stand four tiny amber 30-year-olds in role hats (scrubcap, wig, cap, hardhat). A glowing amber number tag `30` floats above the surgeon. A small grey key icon falls from the empty space.
- **Text (2 words + number):** **OLDEST: 30** (cream "OLDEST:", amber "30"), upper-left, very heavy.
- **Colours:** navy #13213A with a slight vignette; amber bar, figures and tag #F2B33D; dotted outline in grey #9AA3AE at 40%; text cream + amber, 10 px black outline.
- **Kit assets:** `whatif/Pyramid` (cohort at 30, ghost outline of old bands), `whatif/Person` x4 (adult, stand, hats), `whatif/Icon` key, `explainer/Tag` for the number tag.
- **Payoff on screen:** 4:02 ("Nobody on Earth is older than you") in the long video, which is too late for the main upload. Use C as the cover for a 9:16 Shorts cut of 3:48-4:29, where it pays off at about 14 s.

## Render

Once the thumbs kit has a `whatif` template (after the kit gate shot passes), write `episodes/whatif-everyone-born-same-day/thumbs.json` with variants `field` (A), `split` (B) and `oldest` (C), then run `OUT=thumbs/whatif-born-same-day scripts/thumbs_render.sh <spec>` on the Spark only. Check the contact sheet at phone size: the text must read at 120 px tall, and the amber must not sink into the dawn violet on A.
