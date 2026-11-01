# Thumbnail concepts: explainer-short-mantis-shrimp-punch

There are three concepts. Each renders as a Remotion still on the Spark (`studio/src/kits/thumbs`, 1080x1920 cover and 1280x720 shelf) from the same explainer art the video uses, so the cover looks like the video.

Thumbs-kit rules (`spec.ts`): one big subject and one tiny human, 2-4 words of high-contrast text, and exactly one red accent word. Everything else is desaturated.

Library rules (`research/library/index_notes/explainer.md`):
- The text adds a claim the title does not make.
- White text with one red word, plus a red arrow to a tiny human.
- For Shorts, frame 0 is the thumbnail.
- The word should pay off on screen within about 10 s.

None of the Shorts references has a designed thumbnail: XFFjxTllpoA, jw6bS-WL4F4, 6mRR91AbxjQ and Ky0XPonYDcc all use auto-frames. So the "inspired by" notes below borrow the long-form designed thumbnails for layout, and the Shorts' first frames for the cover logic.

All three need `explainer/MantisShrimp` (the new kit figure, see script.md "Kit work") passed as `art`, with `facing: "right"`.

## A. "AT YOUR SIZE" (frame-0 cover, recommended for the 9:16 TikTok/Shorts post)

- **Inspired by:**
  - XFFjxTllpoA: its first frame is a title card that doubles as the thumbnail, so the cover and the loop agree.
  - fGcgWaswMns: huge creature entering from the right, tiny diver lower-left, near-black ground, 2-4 words adding a new claim (14.65x).
  - mzeN0BXR4e0: pale creature filling the right two-thirds, small human between the text and the creature.
- **Composition:** the actual frame 1. On a dark-teal `Ocean` (depth 6, rays) over the seabed band, the peacock mantis shrimp in its meral-spread threat pose fills the right ~60%: front raised, club cocked, eye stalks toward the viewer. YOU stands at the lower left, the same height as the shrimp's raised front, in the "panic" pose. A red hand-drawn arrow points from the text to YOU, with the "YOU" tag.
  - The title says "hit you twice", so the cover adds the size claim. Size is what makes the threat legible at 120 px tall.
  - The cover matches frame 0, so the TikTok loop and the cover agree, and the hook line reads over it.
- **Text (3 words):** **AT YOUR SIZE** ("SIZE" red), heavy condensed white with a black outline, upper third.
- **Colours:**
  - ocean #0d3b45 -> #04161b
  - the shrimp is the only saturated subject: green #2fa36b carapace, red #e5483d club, orange legs
  - YOU and the text in white #f3f6f7
  - red #ff1f1f for "SIZE" and the arrow only
- **Kit assets:** explainer/Ocean, explainer/MantisShrimp (`lengthM` 1.75, `pose: display`, `club: -40`), explainer/You (`pose: panic`) as `humanArt`, thumbs template `scale` (the subject side-on with a tiny human).
- **Payoff on screen:** immediate. It is frame 0 to 2.3 s, and "your size" is word 2 of the hook.

## B. "200-TON PUNCH" (shelf / 16:9, A/B partner for A on the YouTube Shorts shelf)

- **Inspired by:**
  - fGcgWaswMns: monster-vs-human scale contrast on near-black, with a red arrow to a tiny human.
  - The blue-whale pilot's own `scale` variant ("TOO BIG TO EAT" with a "30 M" ruler label, episodes/explainer-blue-whale/thumbs.json).
  - PRESSURE fmZfphacPPQ: the number is felt through a landmark, not stated alone. Here the landmark is a ghosted blue whale.
- **Composition:**
  - Near-black ground.
  - The human-size shrimp side-on at the right, club fully extended mid-strike, white flash ring at the club tip.
  - Behind the club, a ghosted pale-grey `BlueWhale` silhouette at ~30% opacity, as long as the frame is wide, tapering into the club like a comet tail. The whale is "inside" the punch.
  - Tiny YOU at the left edge, at the point of impact, with the red arrow and "YOU" tag.
- **Text (3 words):** **200-TON PUNCH** ("PUNCH" red), top-left block.
- **Colours:** black #05090c, pale-grey whale #8a9aa3 at 30%, the shrimp's palette, white text, red "PUNCH" and arrow.
- **Kit assets:** explainer/MantisShrimp (`club: 60`), explainer/BlueWhale (`silhouette: "#8a9aa3"`), explainer/You, a circle flash (template fx), thumbs template `eye` (subject from the right, arrow to a tiny human), with `noArrow: false`.
- **Payoff on screen:** late. "Two hundred tons" lands at 0:52.8 and the whale at 0:53.9. That breaks the ~10 s rule, so B is an A/B variant for the shelf, not the TikTok cover. It also adds a claim the title doesn't make (force), which the library rules prefer.

## C. "THEY NAMED HIM TYSON" (story hook, for the 16:9 compilation or a re-upload titled "The Shrimp That Cracked Its Own Tank")

- **Inspired by:**
  - Ky0XPonYDcc "You could've FaceTimed an Eel" (8.61M, 1.83): a true-story Short whose first frame is a real aquarium with an absurd one-line claim over it.
  - jw6bS-WL4F4: the tiny subject shown as tiny, in a jar or beside a coin, so the danger reads as a paradox.
- **Composition:**
  - A room-lit home/aquarium tank face-on, filling the frame.
  - A star-shaped crack (the episode's crack svg, scaled up) radiates from the centre of the glass.
  - At the centre of the crack, the tiny real-size shrimp (about thumb size on screen), club extended, eyes toward camera.
  - The giant YOU silhouette at the right edge, looking in. This is the episode's last frame, the contrast with frame 1.
- **Text (4 words):** **THEY NAMED HIM TYSON** ("TYSON" red), two lines, top.
- **Colours:**
  - room grey #2a2f36 -> #15181d
  - glass tint rgba(90,170,200,.28) with a #cfe6ee frame
  - white crack lines
  - the shrimp's palette as the only colour
  - red "TYSON"
- **Kit assets:** thumbs template `abyss` reworked as a lit tank (it already has a central cone/glow composition; swap the light cone for the crack star), explainer/MantisShrimp (`lengthM` 0.1), explainer/You (`silhouette: true`), the crack svg from gen_storyboard.py.
- **Payoff on screen:** very late (1:16-1:21), and it gives away the stinger. Use it only where the title is the Tyson story (titles.md option 6), never as the cover for option 1.

## Render

```json
{
 "id": "explainer-short-mantis-shrimp-punch",
 "niche": "explainer",
 "art": {"component": "explainer/MantisShrimp", "props": {"lengthM": 1.75, "pose": "display", "club": -40, "idle": false}, "facing": "right"},
 "humanArt": {"component": "explainer/You", "props": {"pose": "panic"}},
 "variants": [
  {"template": "scale", "id": "explainer-short-mantis-shrimp-punch-a", "text": "AT YOUR\nSIZE", "accent": "SIZE", "humanLabel": "YOU", "subjectScale": 0.9},
  {"template": "eye", "id": "explainer-short-mantis-shrimp-punch-b", "text": "200-TON\nPUNCH", "accent": "PUNCH", "humanLabel": "YOU",
   "art": {"component": "explainer/MantisShrimp", "props": {"lengthM": 1.75, "club": 60, "idle": false}, "facing": "right"}},
  {"template": "abyss", "id": "explainer-short-mantis-shrimp-punch-c", "text": "THEY NAMED\nHIM TYSON", "accent": "TYSON", "noArrow": true,
   "art": {"component": "explainer/MantisShrimp", "props": {"lengthM": 0.1, "club": 60, "idle": false}, "facing": "right"}}
 ],
 "primary": "explainer-short-mantis-shrimp-punch-a"
}
```

1. Once `explainer/MantisShrimp` exists, copy this spec to `episodes/explainer-short-mantis-shrimp-punch/thumbs.json`.
2. Run `scripts/thumbs_render.sh` (Spark only).
3. Check the contact sheet at phone size: the text must read at 120 px tall. In B, the ghost whale must still read as a whale after JPEG compression. If it doesn't, raise it to 40% opacity.
4. Variant C needs the `abyss` template's light cone swapped for the crack art, which is a small template option (`crack: true`). Until then, render C from a storyboard still of shot 25 (`scripts/spark_stills.sh`).
