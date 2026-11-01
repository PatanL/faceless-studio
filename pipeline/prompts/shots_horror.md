You are the storyboard artist for a 9:16 (1080x1920) code-drawn phone-chat horror Short. Working directory: the studio
repo. Turn the narration of episodes/{slug}/script.md into episodes/{slug}/shots.json. You write JSON only; no TSX,
no Python, no new components.

Read first:
1. episodes/{slug}/script.md (narration block, chat transcript, shot notes)
2. The docstring at the top of pipeline/episodes/auto.py (shots.json format and the @word time anchors)
3. studio/src/kits/horror/README.md (every component and its props) and studio/README.md (layer/camera/transition model);
   studio/src/core/schema.ts is the source of truth if a field is unclear
4. Examples of finished, reviewed scenes: pipeline/episodes/horror_eps.py (helpers phone_scene / set_scene and
   pinned_rules) and episodes/horror-pinned-rules/storyboard.json (times already resolved to numbers)

shots.json = {{"niche": "horror", "emphasis": [...], "scenes": [...]}} with EXACTLY one scene per narration paragraph
({n_paras} paragraphs), in order. Paragraph texts:
{paragraphs}

Visual rules (from the pilot reviews; follow all of them):
- Shot grammar: alternate full set shots (a background component such as horror/FrontDoor, horror/Hallway, horror/Bedroom,
  horror/LivingRoom, horror/Stairwell, horror/ElevatorPanel as the scene "background" or a full-frame layer), phone inserts
  (horror/HandPhone full-frame with "phone": {{"mode": "chat", "chat": {{...}}}}) and reaction shots (horror/Protagonist or
  horror/Neighbour waist-up, "width": 640, "height": 973, "y": "100%", "anchorY": 1, with timed "exprs").
  No shot held longer than ~3 s without a cut, punch-in (camera keyframes zoom 1.0 -> 1.2), message pop-in or expression swap.
- Chat messages pop in on the words that describe them: messages [{{"from": "Jess", "text": "...", "at": "@texted"}}].
  Keep one chat object consistent across scenes (same title, members, earlier messages with "at": 0).
- Frame 0 is the cover: scene 1 shows the key image (a chat with the rule, or the door) fully at t=0. End on the cliffhanger
  with horror/EndCard (PART 2) in the last scene.
- Grade: dark but readable; full-frame overlays "horror/Vignette" (amount 0.4) and occasional "horror/Flicker" /
  "horror/Glitch" on the scare words, camera shake {{"at": "@knock", "duration": 0.4, "amplitude": 14}} on hits.
- Captions are drawn by the renderer; keep chat text and faces clear of y 72-80 %.
- Anchor every time to spoken words ("@knock", "@knock+0.2", "@door.end"); only use numbers for 0.
- Transitions: "fade" 0.25 s by default, "glitch" 0.2 s on scares, "dipBlack" 0.3 s before the last beat.
- emphasis: 6-12 red caption words (rule numbers, the wrong detail, the scare verb), content words only, written as spoken.

Gate: run `python3 -m pipeline.episodes.auto {slug} --check` and fix shots.json until it prints PASS with no WARN lines
about holds or layout. Then reply with one line: number of scenes and layers.
