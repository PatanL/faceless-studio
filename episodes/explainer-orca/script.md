---
id: explainer-orca
niche: explainer
title: Why You'd Never Want To Meet An Orca
alt_titles: The Killer Whale Has Never Killed You. Here's Why. | Orcas Could Hunt You. They Choose Not To.
format: 9:16
target_s: 75
pilot: true
template: pipeline/templates/explainer.md (Short)
voice: am_michael
speed: 1.22
music: deep_ocean
references:
  - id: VtrcKTkhDHU, url: https://www.youtube.com/watch?v=VtrcKTkhDHU, views: 8289332, outlier_score: 318.82
  - id: fGcgWaswMns, url: https://www.youtube.com/watch?v=fGcgWaswMns, views: 2307237, outlier_score: 14.65
  - id: jw6bS-WL4F4, url: https://www.youtube.com/watch?v=jw6bS-WL4F4, views: 6716278, outlier_score: 1.43
---

# Why You'd Never Want To Meet An Orca (Short, PILOT)

**Premise.** The paradox hook: the animal named "killer" has no recorded wild human kill. Escalate through
what it does to everything else (wave-washing, great white livers, a blue whale), ask the question,
strike the wrong answers, land on culture, then twist with the Iberian rudder attacks: maybe they just haven't decided about us.

**Why this is the pilot.** Strongest demand in R1/backlog (WILD VERSUS orca 56M at 83x, OctoLab 8.2M at 319x,
BeyondTheBlue 2.7M), it is not a Depth Theory topic, and every beat maps to an existing kit piece (`Orca`,
`GreatWhite`, `BlueWhale`, `SpeedBars`, `Options`, `Map`). R1 recommended it over the colossal squid.

## Beat alignment

| Our beat (paragraph) | Reference beat | Ref timestamp | Device borrowed |
|---|---|---|---|
| 1 Hook: "killer" with zero wild kills | VtrcKTkhDHU curiosity paradox open | 0:00-0:20 | paradox: deadliest predator that refuses to kill us |
| 2 Scale: eight metres, four cars | fGcgWaswMns scale vs a bus | ~1:05 | everyday-object scale anchor |
| 3 Speed bars: you vs orca | jw6bS-WL4F4 ESC-1 multiplier vs known animals | 0:15 | number ladder against something familiar |
| 4-7 Hunting rungs (pods, wave, livers, blue whale) | jw6bS-WL4F4 escalation ladder ESC-1..3 | 0:15-0:31 | each rung more extreme, signposted |
| 8 "Here's the question" | fGcgWaswMns "the question we're all thinking" | options beat (~60%) | explicit re-hook question |
| 9-10 Options struck, culture verdict | fGcgWaswMns numbered options + verdict | ~60-70% | strike-through list, hard verdict |
| 11 Twist: rudder attacks | fGcgWaswMns "here's the surprising part" | ~70% | twist that flips the comfort |
| 12 Bookend + comment CTA | fGcgWaswMns comment CTA; jw6bS-WL4F4 callback button | end | callback to hook, comment question |

## Facts to verify (paraphrased; check before publishing)

- No confirmed case of a wild orca killing a human (captive incidents exist) — NOAA Fisheries / Whale and Dolphin Conservation.
- Adult males reach ~8 m (record ~9.8 m) and ~6 t — NOAA species profile.
- Burst speed ~56 km/h (~34 mph) — NOAA; recreational swimmers ~3 km/h, elite ~8 km/h.
- Pods have distinct vocal dialects and diets (resident fish-eaters vs mammal-eating Bigg's/transients) — Ford et al.; NOAA.
- Wave-washing seals off ice floes, Antarctic Peninsula — Pitman & Durban 2012, Marine Mammal Science.
- Great white carcasses with livers removed near Gansbaai, South Africa from 2017; sharks left the area — Towner et al. 2022, Ecology.
- First documented kill of an adult blue whale, March 2019, off Bremer Bay, Western Australia — Totterdell et al. 2022, Marine Mammal Science.
- Iberian orca–boat interactions since 2020 off Spain/Portugal, rudders damaged, several sailboats sank — Atlantic Orca Working Group / CA2 reports.
- On-screen stat says "~7 boats sunk (and counting)": confirm the current count before publishing (6-7 sinkings reported through 2025).

## Narration

```narration
[music: deep_ocean] There's an animal people call the killer whale. And in the wild, it has never killed a single person.

That's not because it can't. A grown male is eight metres long and weighs as much as four cars.

It can hit fifty-six kilometres an hour. An Olympic swimmer manages about eight. You, maybe three.

And it never hunts alone. Every family pod has its own calls, its own menu, and its own plan.

In Antarctica, a pod lines up and charges an ice floe together. The wave washes the seal straight into the water.

Off South Africa, great whites started washing up with one organ missing. The liver. The orcas took it and left the rest. [sfx: impact @0.1]

The surviving great whites fled the area for months.

And in twenty nineteen, off Western Australia, a pod brought down the biggest animal on the planet. An adult blue whale.

So here's the question. Something this fast and this smart. Why has it never come for us?

Maybe we taste bad? Nobody's ever proven that. Too small to bother with? They hunt seals smaller than you.

The best answer is culture. Orcas eat what their mothers taught them. And no orca mother has ever taught her calf to eat a human.

Comforting, right? Except since twenty twenty, orcas off Spain and Portugal have been ramming sailboats and snapping their rudders. Several have sunk. [sfx: stinger @0.2]

Nobody knows why. So maybe they just haven't decided about us yet. What do you think they're learning?
```

## Shot notes (paragraph = scene; built by pipeline/episodes/build.py)

| Scene | Visual | Kit |
|---|---|---|
| hook | surface ocean, orca glides in, "KILLER WHALE" headline, stat "0 wild human kills" pops on "single" | Ocean(surface), Orca, Headline, Stat |
| scale | orca at true scale over a scale bar, four cars drop in one by one | Orca pxPerM, ScaleBar "~8 M", Car x4 |
| speed | speed bars You 3 / swimmer 8 / orca 56, orca crosses | SpeedBars, Orca |
| pod | three orcas, desynced, "FAMILY POD" tag | Orca x3, Tag |
| wave | waterline, ice floe + seal (inline SVG), three orcas line up and charge, shake | Ocean(surface), svg, Orca x3 |
| liver | great white silhouette, red "LIVER: MISSING" tag, map pin South Africa | GreatWhite, Tag, Map |
| fled | great whites swim off screen, "GONE FOR MONTHS" headline | GreatWhite x2, Headline |
| bluewhale | blue whale at scale with small orcas circling, "2019 · WESTERN AUSTRALIA" tag | BlueWhale, Orca x3, Tag |
| question | dark ocean, headline "WHY NOT US?", tiny You | Headline, You |
| options | options list, strikes on "proven" and "smaller" | Options |
| culture | select "Culture", mother + calf orca | Options, Orca x2 |
| twist | map zoom to Strait of Gibraltar, red ring, "BOATS SUNK" stat | Map, Stat |
| end | hook shot again: orca circles a tiny You at the surface, comment question tag | Ocean(surface), Orca, You, Tag |
