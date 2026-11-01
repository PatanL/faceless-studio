# Thumbnail concepts: sinking-to-the-bottom

Three 16:9 concepts (1280x720) in the **Depth Theory thumbnail house style from R1** (`research/R1/report.md`, THUMBNAILS; reference image `research/R1/thumbs/fGcgWaswMns.jpg`, the 2.29M / 16.3x sperm whale upload):

- a **black monochrome engraving** of the creature filling about **two-thirds** of the frame, entering from the right, head toward the human;
- a **tiny diver with a torch** for scale, lower-left, its beam pointing at the creature;
- a **red hand-drawn arrow** curving from the text down to the tiny human;
- **2-3 words naming a sense or an action on you**, white heavy sans with **"YOU" in red** and a trailing "..", top-left ("IT HEARS YOU..", "IT SEES YOU..");
- pure near-black background, no colour other than the red. R1 notes BeyondTheBlue and OctoLab use the same house style, and that it does not need to match the video art.

Library rule (`research/library/index_notes/explainer.md` rule 10): the text adds a claim the title does not make. The `studio/src/kits/thumbs` kit already renders this formula (white-on-black scratchboard, one red accent continued as the pointer, tiny human); templates `eye`, `abyss`, `scale`. Renders happen on the Spark later (`scripts/thumbs_render.sh`); this lane only writes the specs.

In our video the "diver" is YOU on the sled, so `humanArt` is `explainer/You` with a torch glow; at 30-40 px tall it reads as a diver, as the house style needs.

## A. "IT SEES YOU.." (recommended; pairs with title 1)

- **Subject:** a giant squid, engraved in white line on black, filling the right two-thirds: mantle and arms trailing off the right edge, the **eye** (the largest eye of any animal, ~27 cm) dead centre-right with a single specular glint. Faint concentric light rings around the eye replace the sperm whale's sonar rings.
- **Human:** tiny YOU on the sled (drawn monochrome), lower-left, torch beam reaching toward the eye. The red arrow drops from "YOU.." to the figure.
- **Text:** **IT SEES YOU..** (3 words), "YOU.." red.
- **Why it works:** the title asks a number ("how many times"); the thumbnail adds a threat with an eye on the viewer. It is true and paid early: the squid and its eye arrive at 2:05 (21%) and line 13 turns that eye on YOU ("and it has turned toward you"; s21 pupil slides to YOU), so IT SEES YOU is literally paid, teaser 1 in the hook. Closest to the house formula and to the reference image, so the channel's shelf looks consistent.
- **Spec:**
  ```json
  {"id": "sinking-a", "niche": "explainer", "template": "eye", "text": "IT SEES\nYOU..", "accent": "YOU..",
   "subject": "squid", "humanArt": {"component": "explainer/You", "props": {"pose": "stand", "color": "#f3f6f7"}}}
  ```
  The `squid` placeholder is the colossal squid art; for the final, pass `art: {component: "explainer/ColossalSquid", props: {hooks: false}}` so it matches the giant squid in the video.

## B. "IT LEAVES YOU.." (A/B partner; pairs with title 2 or 4)

- **Subject:** a snailfish, engraved pale and see-through (skeleton dotted inside the body, ghostly), huge at right two-thirds, already **turning away** with its tail toward the human. Below it, across the bottom fifth, a thin dashed white line (the fish ceiling), no label.
- **Human:** tiny YOU on the sled lower-left, just **below** the dashed line, torch pointing up at the departing fish; red arrow from the text.
- **Text:** **IT LEAVES YOU..** (3 words), "YOU.." red.
- **Why it works:** a creepy-gentle subject (the "wet tissue paper" fish) with an implied abandonment the title does not mention. It is paid at 6:58 (71%): the last fish turns back and you sink through its ceiling (DEATH 3). The see-through fish is new on the shelf next to the usual teeth-and-jaws thumbnails, which helps it stand out.
- **Spec:**
  ```json
  {"id": "sinking-b", "niche": "explainer", "template": "abyss", "text": "IT LEAVES\nYOU..", "accent": "YOU..",
   "art": {"component": "explainer/Snailfish", "props": {"xray": true}, "facing": "right"},
   "humanArt": {"component": "explainer/You", "props": {"pose": "point", "color": "#f3f6f7"}}}
  ```
  Needs the NEW `explainer/Snailfish` figure (assets.md). Until it exists, this concept cannot be rendered in the house style; use A.

## C. "IT BEAT YOU.." (re-upload / title 10 only)

- **Subject:** a pale crumpled shape, engraved like a ghost or a jellyfish, half-lifted off the mud in the torch beam and filling the right two-thirds. It is the 1998 plastic bag, drawn so that at shelf size it reads as an unknown pale creature (the house style's mystery), which keeps the twist.
- **Human:** tiny YOU standing on the landed sled lower-left, torch on the shape; red arrow from the text.
- **Text:** **IT BEAT YOU..** (3 words), "YOU.." red.
- **Why it is third:** it is the most curious of the three, but its claim is the 88% twist ("you weren't the first"). A thumbnail that sells the twist trains viewers to skip the ladder, so use it only for a later title/thumbnail swap if A and B underperform, or for a Short promo.
- **Spec:**
  ```json
  {"id": "sinking-c", "niche": "explainer", "template": "scale", "text": "IT BEAT\nYOU..", "accent": "YOU..",
   "art": {"component": "core/svg BAG (scratchboard redraw)"}, "humanArt": {"component": "explainer/You", "props": {"pose": "stand"}}}
  ```
  Needs a small NEW scratchboard redraw of the parent's BAG SVG as thumbs art (assets.md §4); `art.component` above is a placeholder until it is registered.

## Testing

Upload with A. If CTR after 48 h is below the channel median, swap to B (YouTube "Test & compare" if available). Keep C in reserve. Never put text that restates the title, and never put "plastic" on the thumbnail.
