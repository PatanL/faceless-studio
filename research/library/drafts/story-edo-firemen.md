---
id: story-edo-firemen
lane: story (RicksClips3000 parity)
status: v1 draft (Storm Oil form, anonymous) from the script track (research/library/STORY_TOPIC_QUEUE.md section 6, re-rank #2); proposal only, no episode folder
title: Why Edo's Firemen Smashed the Wrong House
target_runtime_s: about 62 at 3.9 words/s (about 4.0 in setup and escalation, 3.7 on the mechanism; 242 words)
facts_source: STORY_TOPIC_QUEUE.md section 6 (Cabinet Office Meireki report, Tokyo Fire Department, Tokyo Metropolitan Library)
stress: tea, broom, bowl, wrong, roof, buckets, gust, finger, quiet, pumps, starve, politely
unstress: says, just, then, out, back, fire, house, street
melody: rules
voice: am_eric
hook_boost: 1.35
hook_act_st: 9
emphasis: off
---

# Why Edo's Firemen Smashed the Wrong House: v1 (Storm Oil form)

**Form.** Same as Dutch waterline v1: an anonymous "he", an invented and exaggerated plot, and a true "You see"
mechanism. No real person is named. The only real-world anchor is the "You see" block (firemen in old Edo, their
weak hand pumps, tearing down houses in the fire's path), kept apart from the invented fireman, owner and street.
- **True and stated** (queue section 6, fact 1):
  - Edo firemen fought fires by pulling down the houses in the fire's path, because their equipment was poor
    (fact 1: Cabinet Office report, Tokyo Fire Department);
  - the hand pump (*ryūdosui*) could not throw water far; the narration says "barely past the next roof", the
    queue's own reveal wording (fact 1);
  - the crews used long hooked poles (*tobiguchi*), shown as his prop and said only as "a pole";
  - Edo was a city of wooden houses, and wind drove its fires (fact 2: the Meireki fire came in strong wind).
- **Invented:** the fireman, the owner, his tea, rice bowl and broom, the laughing street and its buckets, the finger
  to the wind, the gust, the fire dying at the owner's feet, the new house and the second, polite knock.
- **Left out on purpose:** the Meireki fire and its death toll (CONTESTED, 30,000 to over 100,000; the "tens of
  thousands" hedge is not needed because the fire is not mentioned), the *matoi* and the 1720 brigades (a
  sequel), and the Ryōgoku entertainment-district ending (fact 3 carries a 2021 "partly myth" flag).
- **Numbers:** no year or count is stated; the judge's only number token is "half" ("Half the street").

**Title (T6).** "Why Edo's Firemen Smashed the Wrong House": names the role and the strange act, hides the why
(the queue's T6 title, with "Japan's" swapped for "Edo's" so the place is in the title). Alternative: "The Fireman
Who Couldn't Find the Fire" (the street's own jeer).

**Hook (Rick shape):** "He [smashed a man's house during breakfast], with [a fire] so close [the man's tea was
boiling in his cup]."
- ASR-safe: plain words with no homophone risk in context ("smashed", "breakfast", "tea", "boiling", "cup"); the
  body says "pole" and never "tobiguchi", "matoi" or "ryūdosui".
- **Frame 0:** him close, yanking a long hooked pole into the edge of a tiled roof, tiles flying; through the torn
  paper wall, the owner at a low breakfast table with his rice bowl, tea boiling over (prompt:
  `experiments/asset-gen/prompts/kf_edo_hook.txt`).
- **At 2-4 s:** the burning house right behind them, flames and sparks leaning in the wind.

**Running gag:** "Wrong house!" (the owner, twice) and the rice bowl he never puts down (in his hand when he jumps up
and during the broom chase), paid off by the same fireman knocking politely at his new house a week later.

**Mocker proved wrong:** the owner ("Wrong house!", the broom) and the street ("Some fireman! He can't even find the
fire!"), who go quiet when the fire dies at the gap where his house stood (one of them puts down his bucket); the
owner ends with a new house next to another fire, and the same fireman at his door.

**Stress marks.** Writer-marked for `melody: rules`: the joke props (TEA, BROOM, BOWL), the gag word (WRONG), the
act's target (ROOF), the mechanism's key words (PUMPS, STARVE), the finger test (FINGER), QUIET for the turn,
the street's BUCKETS (set up so the bucket put down later lands), the GUST, and POLITELY in the last line; the hook's act verb (SMASHED) comes from the rules. Vetoed: speech and routine verbs (says,
just), particles (then, out, back), and "fire", "house" and "street" (each is in almost every line, so stressing
them would flatten the contrast; "Wrong house" lands on WRONG).

## Narration

```narration
[sfx: crash] He smashed a man's house during breakfast, with a fire so close the man's tea was boiling in his cup.

[sfx: knock] The owner jumps up, still holding his rice bowl. "The fire's next door, you've got the wrong house!"

[sfx: creak] He licks a finger, checks the wind, then hooks a pole into the roof and pulls.

[sfx: whoosh] The owner grabs a broom and chases him around the house, rice bowl in the other hand.

[sfx: crowd] Half the street comes out with buckets, laughing. "Some fireman! He can't even find the fire!"

[sfx: tick] Then he pulls down the last wall, just as the wind picks up. "Wrong house!"

[sfx: whoosh_long] Soon a gust drives the fire straight toward the gap, and the laughing street behind it.

[sfx: crash] Seconds later, the flames leap over and land on the bare dirt where the house used to be.

[sfx: tick] And there they stop. They flicker, they shrink, and they die, right at the owner's feet.

[sfx: knock] The street goes quiet, and somebody slowly puts down his bucket.

[sfx: whoosh] You see, firemen in old Edo really did this, because their hand pumps could barely throw water past the next roof.

In a wooden city, in a strong wind, that won't drown a fire.

But you can starve it. Tear down the houses in its path, and when it arrives, there's nothing left to burn.

[sfx: impact] A week later, the owner finishes his new house, the house next door catches fire, and the same fireman knocks politely, holding his pole.
```

## Scores

- **script_judge** at 3.9 words/s (no audio yet): **100.0 / 100** on the checkable points (rubric items not
  answered; report in `story-edo-firemen.judge.md`).
  - 242 words, about 62 s;
  - hook 20 words / 5.1 s;
  - setup ends at 36 %;
  - 3 escalation steps (then the last wall / soon a gust / seconds later);
  - "You see" at 67 %; mechanism 55 words;
  - 1 number token ("Half the street"); last line 24 words.
- **Cold read, pass A (1 fresh reader, Sonnet, no tools; budget allowed one), on the pre-fix text: FAIL, 70.0.**
  - Every beat retold (who, what, why, twist coverage 1.0, understanding 100); reader confidence 3; hook
    keep-watching 4/5 ("who is he, and why smash a house during breakfast with a fire nearby?"); funny 3/5.
  - Story vs fact: the reader took only "Edo firemen tore houses down because their pumps were weak" as true and
    the breakfast, broom, tea, street, fire and knock as dramatised.
  - Failed on 2 `lost` lines and 3 blocking jumps (friction 40). Key: `story-edo-firemen.cold_key.json` (written
    before the read); answer `story-edo-firemen.cold_A.json`; report `story-edo-firemen.cold_report.md`.
  - **Fixed after the read** (judge rerun on the fixed text, 100):
    - `lost` "Soon the wind shoves the fire sideways" (which fire, which way?) and the blocking "finger test looks
      like luck": the finger test now comes first, before the first pull ("He licks a finger, checks the wind, then
      hooks a pole..."), the wall comes down "just as the wind picks up", and the fire goes "straight toward the
      gap, and the laughing street behind it".
    - `lost` last line ("his new house": the fireman's or the owner's? who knocks?): now "the owner finishes his
      new house, ... and the same fireman knocks politely, holding his pole."
    - `slowed` bucket with no setup: the street now "comes out with buckets, laughing".
    - `slowed` "right in front of the rice bowl": now "right at the owner's feet".
  - **Left open:** the blocking "why does he ignore the protest" jump is the hook's question by design (answered at
    "You see"), now softened by the finger test; "tea boiling in the cup" is a deliberate exaggeration; "Edo" is
    not glossed (the shots show the city). **Not yet confirmed: the fixed text needs one more fresh reader (pass A)
    before voicing; the budget allowed only one.**
