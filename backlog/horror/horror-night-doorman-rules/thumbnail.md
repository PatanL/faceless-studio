# Thumbnail concepts: horror-night-doorman-rules

Three concepts. Rules applied:
- Thumbs kit (`studio/src/kits/thumbs/README.md`, `spec.ts`): one big subject, one tiny human, **2-4 words** in
  Montserrat 900 white with a black outline, **exactly one red accent word**, cold teal horror grade.
- Library notes (`research/library/index_notes/horror.md` rows "Cover / thumbnail" and item 10): on TikTok the cover IS
  frame 0, and outliers' frame 0 shows a **readable threat** with a burned-in first-person fragment (SIEGE-OVERLAY
  7654526047005723937, SIEGE-CHAT 7659677578365537569, HEARSE-P1 7702661541224566049). Controls fail with no visible
  threat in frame 0 (7696062340852190496, 7665304797242821921, xKgepVHATm4). YouTube outliers put the premise in 3-6
  big words or use a phone-notification mock-up.
- The words must pay off on screen within ~10 s.

**Production note.** The thumbs kit has no lobby/desk-phone art (`horror/LobbyDesk` is not built; the horror kit is
locked), so concepts A and B are rendered as storyboard stills on the Spark
(`node src/cli/stills.mjs <storyboard> --at <t>`, see the frame list below) with a text layer added in a one-off
copy of the storyboard. Concept C uses the existing thumbs `chat` template plus `humanArt` (horror/Protagonist), so it
renders today. When LobbyDesk exists, register it in the thumbs KitArt and move A and B to templates.

## A. "1903 IS EMPTY" (frame-0 cover, recommended for Part 1, 9:16)

- **Inspired by:** HEARSE-P1 7702661541224566049 frame 0 (the threat object itself, the hearse, fills the frame in
  second 1) and SIEGE-CHAT 7659677578365537569 frame 0 (a burned-in rule fragment over the threat). PLAYBOOK §6 bottom
  line: "the cover frame (frame 0) shows the threat".
- **Composition:** the actual frame 0 of Part 1 (storyboard.json t = 0.0, rendered in
  `out/stills/doorman_p1_fix.jpg` tile 1). The desk phone fills the frame; the 1903 button sits left of centre at
  ~y 53% under yellow tape, with the red light glowing **bright** through it (cover intensity, halo 0.55). LCD
  "LINE 1903" in red. The rule-3 card ("3. If 1903 calls, send nobody up. 1903 is empty.") sits at y 26%, under the
  caption band. Tiny human: none in frame 0; for the YouTube 16:9 crop, add Lena small at the right edge from the
  lobby wide (horror/Protagonist, pose phone, expr scared).
- **Text (3 words):** **1903 IS EMPTY** with **EMPTY** in red (the lie the red light contradicts).
- **Colours:** near-black desk (#0b0c0f), beige phone body (#cfc8b8), tape yellow (#e8c547 at 80%), the one hot colour
  is the red glow (#ff3b30 / rgba(255,40,30)); text white + black stroke; red accent word.
- **Kit assets:** inline SVG `desk_phone()` + `TAPE` from build.py, core circles for the glow, core text; Vignette 0.4.
- **Pays off:** 0:00-0:04 (the rule is the first line, "Nineteen-oh-three is empty" at ~0:03).
- **Part 2 variant:** Part 2 frame 0 (storyboard_p2.json t = 0.0): same phone, LCD "LINE 1903 · CALLING", text
  **IT'S CALLING** (red: CALLING).

## B. "NOT EMPTY." (the CCTV peak, for YouTube 16:9 / an A/B cover)

- **Inspired by:** library note "a silhouette ... in a corridor" as a readable threat (SIEGE-OVERLAY
  7654526047005723937 frame 0), the thumbs `hallway` template (figure + corridor), and TRUCKER-RULES
  7692268145888873760's held image at 2:09-2:12 (one wrong figure, held still).
- **Composition:** Part 1 storyboard.json t = 88.5 (inside the 3.8 s hold; rendered at 86.88 in
  `out/stills/horror-night-doorman-rules_storyboard.jpg`, row 5 tile 3). Grey CCTV frame, "CAM 19-E 02:44:07" + red
  REC dot top corners, one-point corridor, 1903's door open a dark crack with the plate "1903" readable, the back-view
  man in a navy concierge blazer facing the wall beside it, right of centre at the rule of thirds. Camera zoom 2.45 on
  the end wall so the figure is ~40% of frame height. Tiny human: the figure doubles as the human; for 16:9 add Lena's
  small lit face in the lower-left corner (a monitor reflection).
- **Text (2 words):** **NOT EMPTY.** with **EMPTY.** in red.
- **Colours:** desaturated grey (scene grade saturate 0), the only colour is the red REC dot and the red accent word;
  the blazer reads as a dark-navy block against the light corridor.
- **Kit assets:** horror/Hallway (lights 1, endDoor) + `hallway_1903()` overlays (gap rect, plate text, `FIGURE` SVG),
  horror/Glitch 0.08 (scanlines), Vignette 0.65.
- **Pays off:** 1:20-1:30 in Part 1 (late), so use it only where the title carries the early payoff (YouTube with
  title option 1 or 8), not as the TikTok cover.

## C. "WHICH RULE WINS?" (chat mock-up, renders today with the thumbs kit)

- **Inspired by:** the YouTube phone-notification mock-ups noted in `index_notes/horror.md`; SIEGE-CHAT
  7659677578365537569 (the held phone with an authority's command, 1:43-1:51); the existing horror-pinned-rules
  `chat` thumbnail spec (`episodes/horror-pinned-rules/thumbs.json`).
- **Composition:** thumbs template `chat`: a giant tilted phone, chat title "Desk Handover (2)", four lines, the last
  one big; tiny human = Lena in bed-light pose replaced by `humanArt` horror/Protagonist (pose phone, expr terrified,
  light phone, navy blazer colours) at the lower left.
- **Spec (drop into a thumbs JSON):**
  ```json
  {"id": "horror-night-doorman-rules", "niche": "horror", "template": "chat", "room": "1903",
   "chatTitle": "Desk Handover (2)",
   "chat": [
     {"from": "Gus", "text": "3. If 1903 calls, send nobody up. 1903 is empty."},
     {"from": "Mr. Pell (Owner)", "text": "1903 needs help. Go up now."},
     {"from": "Gus", "text": "5. If Mr. Pell, the owner, texts you, do what he says."},
     {"me": true, "text": "Which rule wins?"}
   ],
   "humanArt": {"component": "horror/Protagonist", "props": {"pose": "phone", "expr": "terrified", "light": "phone",
                "colors": {"top": "#1d2740", "topShade": "#141b2e", "shirt": "#e9e4d8"}}, "time": 0.4},
   "text": "WHICH RULE WINS?", "accent": "WINS?"}
  ```
- **Text (3 words):** **WHICH RULE WINS?** with **WINS?** in red.
- **Colours:** thumbs-kit cold teal grade, dark chat UI, the rule-3 bubble red, one red accent word.
- **Pays off:** the clash is on screen at 1:02 in Part 1 (s19 "VS" cards) and asked aloud at 1:07, so this is the
  weakest early payoff of the three; best for YouTube where the title (option 1) carries the first 10 s.

**Recommendation:** A for both TikTok covers (it is frame 0, so the cover, hook and loop agree; the Part 2 variant
reads "IT'S CALLING"). B vs C as the YouTube A/B pair.
