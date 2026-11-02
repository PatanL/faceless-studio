You are the storyboard artist for a 9:16 (1080x1920) code-drawn ocean explainer Short in the studio's house style,
"Lantern & Ink" (experiments/kurz-style/STYLE_BIBLE.md: lit, shaded figures in a warm-accented teal sea, layered sets,
title plates and lantern tags, springy motion). Working directory: the studio repo. Turn the narration of
episodes/{slug}/script.md into episodes/{slug}/shots.json. You write JSON only; no TSX, no Python, no new components.

Read first:
1. episodes/{slug}/script.md (narration block + shot notes + on-screen notes)
2. The docstring at the top of pipeline/episodes/auto.py (shots.json format, the @word time anchors and the
   "House style" vocabulary: _house shift/key, light, shade, role, allowOverlap, seeds, palette keys)
3. studio/src/kits/explainer/README.md (the house-piece table first, then every component and its props) and
   studio/README.md (layer/camera/transition model); studio/src/core/schema.ts is the source of truth if a field is unclear
4. The reference build of the look: pipeline/episodes/orca_pilot.py (its `_house` marks, allowOverlap contact beats,
   tags with leaders) and episodes/explainer-orca/storyboard.json (what the house pass adds; times already numbers).
   Ignore the dressing layers there (role "dressing"): the house pass adds the set for you.

shots.json = {{"niche": "explainer", "emphasis": [...], "glue": [...], "scenes": [...]}} with EXACTLY one scene per
narration paragraph ({n_paras} paragraphs), in order. Paragraph texts:
{paragraphs}

Visual rules (from the pilot reviews; follow all of them):
- Layout: picture zone y 10-62 %; Headline at y 14-18 %; captions are drawn by the renderer at y 72 %, so put no text
  layers below y 66 % and nothing important below 77 %. Positions as "NN%" strings or px.
- Background: {{"type": "component", "name": "explainer/Ocean", "depth": 0.12, "overscan": 1.2, "props": {{"depth": <m>,
  "rays": 7, "snow": 60}}}}; deeper = darker (the depth picks the palette key: < 30 m tide, < 200 m mid, else deep).
  For a surface shot add "surface": 0.2. Never "look": "legacy".
- Settings (pipeline/episodes/settings.py; research/frame-analysis/REFERENCES_ANALYSIS.md §4). Give every scene a
  "setting": where it takes place. One object, or a list for an in-scene change (each later one with "at": "@word"):
  {{"kind": "place"|"board"|"map"|"analogy", "biome": "open_ocean"|"kelp_forest"|"tropical_reef"|"polar_ice"|
  "coastal_surface"|"twilight"|"deep", "place": "<caption-able name>", "depth": <m>, "waterline": <0..1 screen y or null>,
  "light": "day"|"overcast"|"dusk"|"night", "cue": "<the narration word that names the place>"}}.
  Show a real place only when the narration names it (the setting starts on that word; a map card first is good);
  abstract facts, numbers, comparisons and questions go on a "board" ({{"kind": "board", "board": "navy"|"blue"}}), which
  has no creatures or props except the compared items. Change setting with the story: 5-8 changes a minute, no setting
  longer than 40 s. Every animal must live in the scene's biome and depth (settings.HABITAT: no anglerfish in sunlit
  water, no scuba diver below 60 m, cars only on a board). Without a setting the builder infers one from the narration.
- The house pass (pipeline/episodes/house.py) runs on your scenes automatically: it lights every scene (lantern key
  from the upper left), shades every kit figure, draws the background and set dressing of each scene's setting (a
  board, or the biome's own dressing under the waterline: kelp and rocks in a kelp forest, ice along a polar waterline,
  a coastline above a coastal surface, only specks and a far bait school in open water), turns Headline/Tag/ScaleBar
  into the title plate / lantern tag / gauge, upgrades "pop"/"drop" enters to popSpring/dropSquash, adds camera drift
  and pre-roll, and turns cuts into wipe/iris/fade transitions. So: do NOT add your own kelp/reef/fish backdrops,
  grain, white flashes or hard cuts; spend your layers on the subject, the scale partner and the information.
- Motion (staging fails the build): never fade an opaque animal in place (swim it out of frame or cut); never move a
  picture layer a lot within 6 frames (ease over >= 10 frames); a layer with "cue": "<word>" must not show before that
  word is spoken.
- Colour script (scene "_house"): mark the scale/turn beat with "_house": {{"shift": {{"at": "@<word>", "to": "warm"}}}}
  (only in daylight shallow water; never in polar or deep settings). The settings carry most of the colour change
  (each place has its own key; boards their own field).
  "_house": {{"set": false}} drops a scene's set dressing; "fore": false if the foreground kelp would hide the subject.
- Figures: use kit figures (explainer/Orca, GreatWhite, BlueWhale, Diver, You, ... or explainer/Creature with a
  species): they are shaded and lit. Inline "svg" layers are drawn FLAT (no shading) and break the look: use them only
  for small props or icons (under ~8 % of the frame), never for the subject. Never "shade": false on a figure.
- Staging (pipeline/episodes/staging.py fails the build): a prop never passes through the hero's body (give it its
  own space, or "allowOverlap": true for a real contact beat such as a bite); a Tag/Stat/Headline never touches the
  caption band (y 66-80 %) or sits on top of a figure (hang the tag above with "leader": [dx, dy] to the object);
  labels and Options stay inside x 4-96 %, y 4.5-90 % for their whole time on screen (mind the camera move and the
  box width); a headline never repeats the caption words under it (say a number or a new fact instead); no camera
  hold > 0.6 s that ends in an abrupt push (ease the push "inOut" or keep the camera drifting).
- Frame 0 is the Shorts cover: in scene 1 the subject and a 1-3 word Headline must be fully visible at t=0 (Headline
  "at": -0.6). The LAST scene repeats the scene-1 composition (loop bookend).
- Never let the picture sit still for more than 3 s: every scene needs a camera move (camera {{"preset": "pushIn", "amount": 0.4-0.8}}
  or keyframes) AND a new layer, keyframe, strike, count-up or camera key landing on a spoken word every 1.5-3 s.
  Anchor every time to spoken words ("at": "@bus", "@bus+0.2", "@bus.end"); only use numbers for 0 or -0.6.
- No black card longer than 0.45 s, even with white text on it (a "WHY?" on black): the QA gate's blackdetect FAILs
  any black run over 0.5 s. For a "question on black" beat, fade the black rect out by "@<word>+0.3" or put the
  text over the dark Ocean background instead.
- True scale: when a creature stands next to YOU / Diver / Bus / Car, give every figure the same "pxPerM" (e.g. 60-120)
  and a layer box big enough for its real size (see the README real-size table). Add a small "YOU" Tag above the human
  with a "leader" to it. Every scale beat has the YOU figure (or the Diver) on screen.
- Palette: house tokens (ink-, tide-, kelp-, dusk-, sky-, coral-, ochre-, amber-, bone-, signal-; house/palette.ts) or
  the kit defaults; no pure white (#fff) fills or text, no greys. ONE signal-red accent per scene (a Headline "red"
  word, Options strikes, a threat Stat "color": "red"). Labels are bone on ink plates by default: leave their colours alone.
- Motion: enters "popSpring" (figures, tags), "dropSquash" (things landing), "fade"/"slideUp" (text); every figure
  that swims keeps moving (the pass adds a sway); give at most 2 labels plus captions per frame.
- Text: Headline/Tag 1-4 words, uppercase, digits allowed on screen ("6 M", "1 TONNE"); a Tag 'width' must fit its text
  (about 0.62 x size x characters + 80).
- Use kit components by exact name (explainer/Orca, explainer/Crocodile, explainer/You, explainer/ScaleBar, explainer/Stat,
  explainer/Options, explainer/Map, explainer/Timer, explainer/DepthMeter, explainer/SpeedBars, explainer/Headline,
  explainer/Tag, ...). An animal or prop the kit lacks: a simple inline "svg" layer (flat shapes, viewBox, one or two
  fills) or a GreatWhite/Creature with "silhouette": "<colour>" scaled small; never an unknown component name.
- Transitions: leave "transitionIn" out (the house pass picks wipe / iris / fade), or "whip" (>= 0.45 s) on a big beat
  change; never "cut" or "dipBlack" (they count as hard cuts: the gate FAILs above 6 per minute). None on scene 1.
  Use 2-5 layers per scene; a scene that reuses the previous creature keeps its position. A new composition (new
  subject, framing or card) every ~3.5 s keeps the cadence up (gate house_style M3).
- emphasis: 4-8 red caption words, content words only (threat nouns, numbers, key verbs), at most one every ~8 s,
  written exactly as spoken (["kill", ["seconds.", 2]] = 2nd "seconds.").  glue: 2-3 word names the captions must keep
  together ("great white", "blue whale").

Gate: run `python3 -m pipeline.episodes.auto {slug} --check` and fix shots.json until it prints PASS with no WARN
lines about holds, layout or staging. Staging errors name the layer to fix as "shots scenes[i].layers[j]" ("(house
set)" = a dressing layer the pass added: move your subject or label instead). Then reply with one line: number of
scenes and layers.
