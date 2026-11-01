You are the script writer for a faceless phone-chat horror story channel (2D code-drawn animation: group-chat phone
screens, an apartment building, two cartoon characters). Working directory: the studio repo. Write ONE original Part 1
script.

Premise: {topic}
Slug: {slug}
Output file: episodes/{slug}/script.md

Read first (skim the long ones):
1. pipeline/templates/horror.md (beats, pacing, visual grammar, gates; follow it exactly)
2. research/corpus/horror/PLAYBOOK.md and research/corpus/horror/INDEX.json
3. The 2-3 corpus transcripts in research/corpus/horror/*.md closest to this premise
4. A finished example of the file format: episodes/horror-pinned-rules/script.md
5. studio/src/kits/horror/README.md (what the kit can draw: Phone/HandPhone chat, lock screen, call, banners;
   Protagonist "Nora" and Neighbour "Mr. Hale" with expressions; FrontDoor, Peephole, Hallway, ElevatorPanel, Bedroom,
   LivingRoom, Stairwell; Flicker, Glitch, Darkness, Heartbeat, RedText, EndCard). Stay inside these sets.

Hard rules:
- Original story. The references are translated reposts of other people's series: study the format, never the plot,
  names, rules or lines.
- Front matter: id, niche: horror, title (ends "(Part 1)"), alt_titles, voice and speed as the template says (af_heart 1.12 for Nora), music: dread, references:
  (2-3 corpus ids with url, views, outlier_score, why_chosen). Then a beat alignment table, the chat transcript
  (who sends what, in order) and shot notes per paragraph naming the kit components.
- The narration goes in ONE fenced ```narration block. One paragraph = one scene. 11-15 paragraphs, 200-260 spoken
  words, first-person past tense. Hook <= 15 words with the rule/contradiction by ~10 s. A PART 2 cliffhanger at the end.
  Only [sfx: name], [pause: s], [music: name] markers (sfx: knock, knock3, knock3_slow, phone_buzz, phone_buzz_long,
  ding, notify, message_pop, stinger, door_creak, footsteps, heartbeat, static, glitch, breath; see studio/public/sfx).
- No gore, no real people or brands.

Gate: run `python3 scripts/originality_check.py episodes/{slug}/script.md research/corpus research/library/transcripts`
and fix the script until it prints PASS. Then reply with one line: the title and the word count.
