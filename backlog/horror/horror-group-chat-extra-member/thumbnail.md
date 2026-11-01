# Thumbnails: horror-group-chat-extra-member (Part 1)

House formula (`studio/src/kits/thumbs/README.md`): one big subject + one tiny human, 2-4 words in Montserrat 900 white
with a heavy black outline, exactly one red accent (#ff1f1f), everything else a cold teal/blue-black grade. On TikTok the
cover is frame 0, which is already built as concept A's 9:16 version (phone over her own door, red scrawl).
Render on the Spark only: `OUT=pilots/<slug>/thumbs scripts/thumbs_render.sh backlog/horror/horror-group-chat-extra-member/thumbs.json`
(the spec below; not rendered yet).

## A. "WHO ANSWERED?" — chat template (recommended, matches frame 0)

- **Composition:** giant tilted phone fills the right two thirds, group chat "Larkspur Court Residents"; the last line is
  the big one. Tiny Nora at lower left in the dark, lit only by the phone. Behind the phone, a thin bright line of hall
  light under a door.
- **Chat lines:** "Ama · 3D: someone's in the hall??" / "Night Security: Nobody. Go back to bed, 3D." / "Leo · 7C: who's
  in the hallway?" / **"Night Security: One. Floor 8, by the stairs. Me."**
- **Text:** WHO ANSWERED? (accent: WHO)
- **Colours:** blue-black grade, grey shield avatar, white text, red only on WHO.
- **Kit assets:** thumbs `chat` template; `humanArt` `horror/Protagonist {pose: phone, expr: terrified, light: phone}`.
- **Inspired by:** Xv32FAAUI-0 (one oversized message card carries the whole hook, 7.5x); 7659677578365537569 and
  7654526047005723937 frame-0 covers (one subject, the threat readable at phone size, 10.8x / 66.7x).

## B. "IT BLINKED" — covered peephole

- **Composition:** the covered lens fills the frame: a black disc inside the grey door surround, one wet white glint on
  the rim (the 0:56 frame of the video). A lock-screen notification banner across the lower third: "Night Security:
  Step back from the peephole, 5B." Tiny Nora silhouette at the bottom edge, back to camera, facing the door.
- **Text:** IT BLINKED (accent: BLINKED)
- **Colours:** near-black, grey surround, a faint red heartbeat edge, white banner, red only on BLINKED.
- **Kit assets:** thumbs `door` template with `art` override `horror/Peephole {figure: 'none', exposure: 0.03, surround: '#26272d', radius: 0.52}`;
  banner drawn as a `horror/Phone` lock-mode notification or a core rect + text; `room: "5B"`.
- **Inspired by:** dqEIz_8bP-8 (dark door with one glowing line, single object), Xv32FAAUI-0 (single notification banner
  as the text carrier); PLAYBOOK B9 (the scariest image is the strongest cover candidate).

## C. "ROOM 5B" — hallway, figure at the door

- **Composition:** endless corridor in one-point perspective, a too-tall figure at the far end beside a door with plate
  "5B", stair exit sign glowing on the right. Tiny Nora close to camera, cropped, looking down at her phone.
- **Text:** WHO'S IN 5B? (accent: 5B). Teases the last line without giving the answer.
- **Colours:** teal corridor, green EXIT sign, black figure, white text, red only on 5B.
- **Kit assets:** thumbs `hallway` template, `room: "5B"`; `humanArt` `horror/Protagonist {pose: phone, expr: scared}`.
- **Inspired by:** 7659677578365537569 frame 0 (silhouette at a corridor's vanishing point, 10.8x);
  7654526047005723937 frame 0 (black silhouette in a corridor, 66.7x); tB9Ln4eINus (door + hallway split, 4.7x).

## Spec for `thumbs.json` (B6 format)

```json
{
  "id": "horror-group-chat-extra-member",
  "niche": "horror",
  "room": "5B",
  "chatTitle": "Larkspur Court Residents",
  "chat": [
    {"from": "Ama · 3D", "text": "someone's in the hall??"},
    {"from": "Night Security", "text": "Nobody. Go back to bed, 3D."},
    {"from": "Leo · 7C", "text": "who's in the hallway?"},
    {"from": "Night Security", "text": "One. Floor 8, by the stairs. Me."}
  ],
  "humanArt": {"component": "horror/Protagonist", "props": {"pose": "phone", "expr": "terrified", "light": "phone"}, "time": 0.4},
  "variants": [
    {"template": "chat", "text": "WHO ANSWERED?", "accent": "WHO"},
    {"template": "door", "id": "horror-group-chat-extra-member-peephole", "text": "IT BLINKED", "accent": "BLINKED",
     "art": {"component": "horror/Peephole", "props": {"figure": "none", "exposure": 0.03, "surround": "#26272d", "radius": 0.52}}},
    {"template": "hallway", "id": "horror-group-chat-extra-member-hall", "text": "WHO'S IN 5B?", "accent": "5B"}
  ]
}
```
