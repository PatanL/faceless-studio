You are the storyboard artist for a 9:16 (1080x1920) code-drawn ocean explainer Short. Working directory: the studio
repo. Turn the narration of episodes/{slug}/script.md into episodes/{slug}/shots.json. You write JSON only; no TSX,
no Python, no new components.

Read first:
1. episodes/{slug}/script.md (narration block + shot notes + on-screen notes)
2. The docstring at the top of pipeline/episodes/auto.py (shots.json format and the @word time anchors)
3. studio/src/kits/explainer/README.md (every component and its props) and studio/README.md (layer/camera/transition model);
   studio/src/core/schema.ts is the source of truth if a field is unclear
4. Examples of finished, reviewed scenes: pipeline/episodes/orca_pilot.py and the first scenes of
   episodes/explainer-orca/storyboard.json (same layout conventions, times already resolved to numbers)

shots.json = {{"niche": "explainer", "emphasis": [...], "glue": [...], "scenes": [...]}} with EXACTLY one scene per
narration paragraph ({n_paras} paragraphs), in order. Paragraph texts:
{paragraphs}

Visual rules (from the pilot reviews; follow all of them):
- Layout: picture zone y 10-62 %; Headline at y 14-18 %; captions are drawn by the renderer at y 72 %, so put no text
  layers below y 66 % and nothing important below 77 %. Positions as "NN%" strings or px.
- Background: {{"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": {{"depth": <m>,
  "rays": 7, "snow": 60}}}}; deeper = darker. For a surface shot add "surface": 0.2, "skyTop": "#071620", "skyBottom": "#1b3b4a".
- Frame 0 is the Shorts cover: in scene 1 the subject and a 1-3 word Headline must be fully visible at t=0 (Headline
  "at": -0.6). The LAST scene repeats the scene-1 composition (loop bookend).
- Never let the picture sit still for more than 3 s: every scene needs a camera move (camera {{"preset": "pushIn", "amount": 0.4-0.8}}
  or keyframes) AND a new layer, keyframe, strike, count-up or camera key landing on a spoken word every 1.5-3 s.
  Anchor every time to spoken words ("at": "@bus", "@bus+0.2", "@bus.end"); only use numbers for 0 or -0.6.
- True scale: when a creature stands next to YOU / Diver / Bus / Car, give every figure the same "pxPerM" (e.g. 60-120)
  and a layer box big enough for its real size (see the README real-size table). Add a small "YOU" Tag above the human.
- Palette: white/grey art and white uppercase labels, ONE red accent per scene (Headline "color": "red", Options strikes,
  Stat "color": "#e5483d" only for a threat number). Stats are white by default.
- Text: Headline/Tag 1-4 words, uppercase, digits allowed on screen ("6 M", "1 TONNE"); a Tag 'width' must fit its text
  (about 0.62 x size x characters + 80).
- Use kit components by exact name (explainer/Orca, explainer/Crocodile, explainer/You, explainer/ScaleBar, explainer/Stat,
  explainer/Options, explainer/Map, explainer/Timer, explainer/DepthMeter, explainer/SpeedBars, explainer/Headline,
  explainer/Tag, ...). An animal or prop the kit lacks: a simple inline "svg" layer (flat shapes, viewBox, one or two
  fills) or a GreatWhite/Creature with "silhouette": "<colour>" scaled small; never an unknown component name.
- Transitions: "transitionIn" {{"type": "fade", "duration": 0.3}} by default, "whip" on beat changes, "dipBlack" before the
  twist, none on scene 1. Use 2-5 layers per scene; a scene that reuses the previous creature keeps its position.
- emphasis: 4-8 red caption words, content words only (threat nouns, numbers, key verbs), at most one every ~8 s,
  written exactly as spoken (["kill", ["seconds.", 2]] = 2nd "seconds.").  glue: 2-3 word names the captions must keep
  together ("great white", "blue whale").

Gate: run `python3 -m pipeline.episodes.auto {slug} --check` and fix shots.json until it prints PASS with no WARN
lines about holds or layout. Then reply with one line: number of scenes and layers.
