---
id: explainer-blue-whale
niche: explainer
title: You Could Fit In Its Mouth. You'd Never Fit Down Its Throat.
alt_titles: What It's Like Next To A Blue Whale | The Biggest Animal Ever Can't Swallow You
format: 9:16
target_s: 70
speed: 1.1
template: pipeline/templates/explainer.md (Short)
music: deep_ocean
references:
  - id: jw6bS-WL4F4, url: https://www.youtube.com/watch?v=jw6bS-WL4F4, views: 6716278, outlier_score: 1.43
  - id: JkAcCdqYJN0, url: https://www.youtube.com/watch?v=JkAcCdqYJN0, views: 332151, outlier_score: 15.82
  - id: fGcgWaswMns, url: https://www.youtube.com/watch?v=fGcgWaswMns, views: 2307237, outlier_score: 14.65
---

# You next to a blue whale (Short)

**Premise.** A pure scale Short with a paradox: you'd fit inside the mouth of the biggest animal ever measured,
but it physically can't swallow you. Each rung compares one body part to something you know (buses, an elephant,
a golf cart), then the twist: the danger is not being eaten, it's being in the way.

## Beat alignment

| Our beat (paragraph) | Reference beat | Ref timestamp | Device borrowed |
|---|---|---|---|
| 1 Hook (11 words, both halves by ~2.5 s): fits in mouth, can't swallow you | JkAcCdqYJN0 title twist "only one actually can" | 0:00 | swallow-you paradox, absurd outcome first |
| 2-3 Length in buses, weight vs dinosaurs | fGcgWaswMns bus/elephant scale | ~1:05 | everyday-object scale |
| 4-6 Tongue = elephant, heart = golf cart, 2 bpm, call > jet engine | jw6bS-WL4F4 ESC ladder, "and that's exactly what it looks like" | 0:15-0:31 | one body part per rung, show the comparison |
| 7 Gulp | jw6bS-WL4F4 number rung | 0:15 | big-volume rung |
| 8 "So what happens to you?" (~50-55 % of runtime) | jw6bS-WL4F4 "that's not the worst part" | 0:31 | main re-hook as a question |
| 9 Krill count + throat = beach ball | JkAcCdqYJN0 throat-width verdict per animal | per entry | mouth vs throat gauge |
| 10 Twist: the turn and the tail | fGcgWaswMns "here's the surprising part" | ~70% | the real danger is elsewhere |
| 11 Bookend stinger, no CTA | jw6bS-WL4F4 callback button | 0:54 | callback to hook line, loops to frame 0 |

## Facts to verify

- Blue whale up to ~30 m, heaviest animal known (~150-190 t) — NOAA; Smithsonian Ocean.
- Tongue ~2.7 t — NOAA / NMNH.
- Heart ~180 kg, roughly golf-cart sized (Royal Ontario Museum specimen, 2015).
- Heart rate down to ~2 bpm on dives — Goldbogen et al. 2019, PNAS.
- Lunge-feeding engulfs a volume of water comparable to or larger than its body — Goldbogen et al. 2011/2012.
- Up to ~40 million krill per day — NOAA / Smithsonian.
- Throat/oesophagus too narrow to swallow a human (often compared to a beach ball or dinner plate) — Smithsonian / NOAA explainer; phrase as "roughly a beach ball".
- City bus ~12 m.
- Call up to ~188 dB re 1 uPa, often popularised as "louder than a jet engine"; low-frequency calls detectable hundreds of km away — NOAA / WWF.
- Tail fluke span up to ~7.5 m — NOAA Fisheries species page.
- Cut: no spoken CTA (PLAYBOOK S7). Next-creature question goes in the description / pinned comment: "Which animal should I put you next to next?"

## Narration

```narration
[music: deep_ocean] You'd fit inside a blue whale's mouth. It still couldn't swallow you.

This is the heaviest animal ever measured. Up to thirty metres long. That's two and a half city buses, parked nose to tail.

It can weigh close to two hundred tonnes. Heavier than the biggest dinosaurs we've ever dug up.

Its tongue alone weighs about as much as an elephant.

Its heart is the size of a golf cart. And on a deep dive, that heart can slow down to just two beats a minute. [sfx: heartbeat_slow @0.2]

Its call is louder than a jet engine, and it can carry for hundreds of kilometres.

To eat, it charges into a cloud of krill and takes one gulp of water bigger than its own body.

So what happens to you, floating right in the middle of that cloud?

Here's the surprising part. It eats up to forty million krill a day, and every one is tiny. Its throat only opens about as wide as a beach ball. Anything bigger just gets pushed back out.

The real danger isn't being eaten. It's being in the way when two hundred tonnes decides to turn, and a tail seven metres wide sweeps past. [sfx: whoosh_long]

Room for you in its mouth. No room down its throat. And it would barely notice you were there.
```

## Shot notes

All cuts are hard cuts; every scene has a camera (slow push + punch-ins on anchored words); no visual hold over 3 s
(build.py STRICT_HOLDS). Red only for threats: CAN'T SWALLOW YOU, the caption words THROAT / TURN, the arrow, stat rules.

| Scene | Visual | Kit |
|---|---|---|
| hook | frame 0 = cover: true-scale head close-up, mouth open, YOU lying on the lower jaw inside the gape, FITS IN ITS MOUTH; CAN'T SWALLOW YOU on the 2nd sentence, diver slides out | BlueWhale gape, Diver, Tag chip, Headline |
| length | whale nose-up (30 m tall), vertical ruler, 2.5 buses stacked, YOU at true scale | BlueWhale rotate, svg ruler, Bus |
| weight | head close-up + white ~190 TONNES, cut to a balance: whale outweighs a sauropod | Stat, Balance, Sauropod |
| tongue | balance: tongue slab vs elephant drops in, beam levels, ≈ 2.7 TONNES EACH | Balance, WhaleTongue, Elephant |
| heart | anatomical heart, golf cart slides in at true scale, YOU; on "deep dive" cut to depth gradient + ECG slowing, white 2 / BEATS A MINUTE with a slow red pulse ring | WhaleHeart, GolfCart, ECG, Stat |
| call | sound rings from the head, white 188 dB, jet slides in, camera pulls out on "carry" | BlueWhale, svg rings, Jet, Stat |
| gulp | head (60 %+ of frame) enters a dense krill swarm, pouch balloons on "gulp" | BlueWhale gape, particles, Krill |
| question | YOU alone in the cloud, whale silhouette looming, AND YOU? | Diver, particles |
| throat | krill macro + 40,000,000 KRILL A DAY, hard cut inside the mouth: throat ring, beach ball, diver drifts in head-first, stuck, white ✕, pushed back out | Krill, Stat, WhaleThroat, Diver |
| turn | whale passes under YOU, red arrow, turn + shake, tail sweeps past | BlueWhale, Diver, svg arrow |
| end | back to the exact frame-0 state (seamless loop), no CTA | BlueWhale, Diver, Headline |
