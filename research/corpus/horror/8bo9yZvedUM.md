# Little brother home alone, older brother at a party: Luke Davidson (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=8bo9yZvedUM |
| Title | THE SCARIEST TEXT CHAT EVER!!! |
| Channel | Luke Davidson (median of the 60 most recent uploads on the Videos tab: 476,000 views) |
| Views | 16,247,875 |
| Outlier score | **34.13** (views divided by the channel median) |
| Duration | 621 s (10:21) |
| Upload date | 2024-02-18 |
| Format | 16:9 long-form YouTube **reaction read-along**. A creator reads a pre-made iMessage-style horror chat aloud on screen, doing light character voices, and talks over it between bubbles (predictions, personal asides, jokes, "uh-oh"). The chat itself is the story; the chat app adds music stings at two points (4:46 time skip, 6:02 the intruder). Two parties: P = Paul, "little bro" (grey, left, the victim, home alone); A = Andrew, the older brother (blue, right, the phone owner, at a party). C = the creator's own commentary |
| Total words | **1,410** (auto-subs). Roughly **half are the creator's commentary** (~690 words, hand-tagged estimate) and half are read chat bubbles (~720 words) |
| Words/min | **136 wpm** over 621 s. Per 60 s window: 165 · 204 · 129 · 131 · 121 · 119 · 71 · 121 · 134 · 114 · 101 (last 21 s). The fast first two minutes are the creator's intro and a 30 s childhood aside; the slowest minute (6:00–7:00, 71 words) is the break-in itself, where single-word bubbles land with pauses between them |

Sources: `raw/8bo9yZvedUM.txt` (yt-dlp en-orig auto-subs, run on the Spark, cleaned with `tools/vtt2lines.py` to `[mm:ss]` lines; timestamps are caption-chunk starts, so a bubble split across chunks takes the first chunk's time). No overview sheet was made for this video, so there is no Visual column; the format line above comes from the transcript and the title. Speaker attribution is inferred from the dialogue (auto-subs do not mark speakers), and the creator says at 0:49 that little bro is on the left. Lines are quoted verbatim **for internal research only. Never reuse the wording, names or plot.**

Auto-sub errors worth knowing about:
- "I'll be soon" (4:42): "I'll be home soon".
- "someone must have broke" (6:19): "...broken in".
- "call Collective" (7:26): unintelligible creator interjection, before Paul's line about the mom's room.
- "Paul oh we got a name Paul" (6:43): the first time the little brother's name appears in the chat, and the creator points it out.

**Key mechanic:** the same "viewer holds the listener's phone" set-up as the Textify chats in this corpus, but stretched to 10 minutes by two things. First, the **first 48% of the runtime has no threat at all**: it is a sibling negotiation (stay home vs. party, threat to tell Mom, a **bribery auction** from $20 to $100) that works as a comedy of stakes and plants **guilt** (the older brother left the child alone, so whatever happens is his fault). Second, a **human creator layer** sits on top of the chat: he states the premise (break-in at 3 a.m.) in the first 8 s, so the long, harmless setup reads as dramatic irony, and he keeps making predictions that act as re-hooks ("never make promises you can't keep", "something bad happens and you weren't there", "they're going to send a photo", "plot twist, the bad guy has the phone"). The horror then runs as a classic home-invasion ladder in text (heard you come in → I'm not home → back door open → hide → footsteps → he's in Mom's room → he's at my door → twisting the knob). The ending is a **subverted twist**: an "I took care of it, you can come out" message that both the creator and the viewer are primed to read as the intruder holding the phone turns out to be the brother for real, and the opening promise is called back as a wholesome close.

## 1. Line-by-line

P = Paul (little bro, victim, home), A = Andrew (older brother, phone owner, at a party), C = creator commentary. Fragmented auto-sub chunks are merged into one bubble per row.

| Time | Line (verbatim, internal only) | Beat | Device | Purpose |
|---|---|---|---|---|
| 0:00 | C: today we're going to be checking out a scary text conversation about someone breaking in to the person's house | **Hook (premise)** | Spoiler-as-promise; the host states the event | Tells the viewer the break-in *will* happen, so everything before it plays as dramatic irony |
| 0:04 | C: and we can't forget that it's at 3:00 a.m. as well | Hook (clock) | Specific witching-hour time | A second promise with a number; the viewer now waits for "3:00 a.m." to appear in the chat (it does at 4:50) |
| 0:08 | C: let's get on in okay so at 10:24 we got Sunday October 28th ... a message earlier today but that goes out the window because it says now | Setup (frame) | Reading the chat UI aloud (timestamp, date) | Grounds the chat as a real phone; the 10:24 p.m. start sets up the 4.5-hour time skip later |
| 0:18 | P: Andrew where are you | **Inciting (soft)** | Late-night "where are you" question | First bubble is a question, from a child; establishes the phone owner's name |
| 0:22 | C: okay he's in his bedroom | Reaction | Host guesses wrong | The host is a stand-in viewer who can be wrong, which invites the audience to predict too |
| 0:24 | P: but I just checked your room / you're not there | Setup | Small reversal | First micro-loop closed in 6 s; the house is emptier than assumed |
| 0:28 | C: should I get the voices going again guys where did you go | Aside | Direct address, voice gag | Personality beat; keeps the creator channel warm |
| 0:32 | A: okay / fine / I'm not at home | Setup (confession) | Grudging admission, split into 3 bubbles | Splitting the reply drags it out like real typing |
| 0:38 | P: where are you | Setup | Repeated question | Repetition marks the child's insistence |
| 0:41 | A: I went to a party | **Stakes plant (guilt)** | Selfish reason for absence | Plants the moral debt that the ending pays back |
| 0:43 | C: oh no little bro's going to be mad | Reaction | Host predicts emotion | Small re-hook: conflict incoming |
| 0:46 | P: what / wait | Reaction | Two one-word bubbles | Shock rendered as rhythm, not description |
| 0:49 | C: okay yes little bro is on the left okay you went to a party | Orientation | Host explains the UI | Tells the viewer which side is the victim |
| 0:53 | P: but mom told you to stay home with me | Stakes | Broken parental rule | The rule names the protector who is missing (Mom) and the duty Andrew broke |
| 0:56 | P: no I'm the only one at home | **Stakes (isolation)** | "Only one at home" | Child alone in the house: the precondition for the whole genre |
| 0:59 | A: I'll be home soon / just go back to sleep | Reassurance | False reassurance | The protector's first "nothing will happen" line; the story will punish it |
| 1:04 | C: uh-uh little bro a ain't going back to sleep too scared | Reaction | Host prediction | The host voices the viewer's suspicion that sleep won't come |
| 1:07 | P: but I can't sleep | Fear | Confession | Matches the host's prediction, rewarding him (and the viewer) for guessing |
| 1:11 | A: why | Fear | One-word question | Ping-pong rhythm |
| 1:12 | P: because I'm scared | Fear | Plain statement | The first named emotion in the chat |
| 1:16 | P: what if something bad happens | **Foreshadow** | Child's "what if" | Voices the premise inside the story; an open loop the host already promised to close |
| 1:18 | A: nothing is going to happen | Reassurance | Famous last words | Ironic line, since the host has told us something will |
| 1:18 | C: that was like me actually when I was younger ... my parents were like out doing something like for example curling ... I would just stay up until they got home ... make my parents leave my door open and also keep the hallway light on | **Personal aside (30 s)** | Relatable childhood confession | Builds parasocial warmth and makes the child's fear feel real; also a breather before the conflict |
| 1:48 | A: just go back to sleep / nothing's going to happen just go back to sleep | Reassurance | Repetition | The protector repeats the dismissal, raising the irony |
| 1:53 | A: I'll be home soon / I promise you | **Plant (promise)** | Promise | Planted here, called back as the final two bubbles at 9:51 |
| 1:55 | C: uh-oh never make a promise never make promises you can't | Re-hook | Host proverb / foreshadow | Turns the promise into a ticking question: will he break it? |
| 2:00 | P: I'm calling Mom | Conflict | Threat of escalation to authority | Shifts the chat from fear to sibling leverage |
| 2:00 | A: no don't | Conflict | Two-word refusal | |
| 2:01 | C: uhoh Andrew's getting in trouble | Reaction | Host commentary | Keeps the comedy register going |
| 2:06 | P: why not | Conflict | Question | |
| 2:08 | A: if you call Mom / she will be mad at me for leaving you at home alone | Conflict (guilt stated) | Self-incrimination | The older brother names his own guilt; "home alone" becomes a refrain |
| 2:15 | C: same thing home alone | Reaction | Host echoes the key phrase | Hammering the phrase "home alone" |
| 2:19 | P: then come back / I can't be home alone / you have to come back | Conflict | Demand + refrain | |
| 2:28 | P: or else I will call mom | Conflict | Ultimatum | First explicit leverage |
| 2:28 | A: no / please don't call Mom / she will be really mad at me | Conflict | Pleading, split bubbles | Power shifts to the child: comedy of reversed sibling roles |
| 2:34 | C: oh no she will be really mad | Reaction | Echo | |
| 2:38 | A: if she finds out / I just went to a party / I will be back no I will be home soon / please don't tell Mom | Conflict | Bargain | Repeats the "home soon" promise a third time |
| 2:48 | C: now Andrew what if something happens bad happens to little bro well you were supposed to be there ... mama ain't gonna be too happy and I think that's what's going to happen in this text conversation | **Re-hook (prediction)** | Host spells out the coming harm | Reminds the viewer of the promised horror at the 27% mark, when the chat has gone two minutes without danger |
| 3:04 | A: please / please / please | Conflict | Triple repetition | Visual rhythm of spam-texting |
| 3:09 | C: did you know that that actually isn't like praying that actually means high five ... I could be wrong | Aside | Trivia about the emoji | Comic micro-aside, changes texture |
| 3:18 | P: I don't know / no way / I'm telling Mom right now | Conflict | Escalated ultimatum | |
| 3:22 | A: please bro / I can't miss this party | Conflict | Selfish motive restated | Keeps the guilt fresh |
| 3:28 | C: fear of missing out | Reaction | Label joke | |
| 3:30 | A: all right / fine / I will pay you | **Bribery (turn)** | Bribe | Opens a new loop: how much will it take? |
| 3:32 | C: oh my gosh bribery | Reaction | Host names the device | |
| 3:37 | P: how much | Bribery | Question | |
| 3:39 | A: I'll give you $20 | Bribery rung 1 | Number ladder | Numbers make an escalation the viewer can track and bet on |
| 3:40 | C: not enough not enough | Reaction | Host sides with the child | Turns viewers into bidders |
| 3:43 | P: no I cannot be home alone / you need to come back | Bribery | Refrain | |
| 3:48 | A: how about $50 | Bribery rung 2 | Number ladder | |
| 3:49 | C: okay now we're getting up there | Reaction | | |
| 3:52 | P: no just come back / I'm scared to be home alone by myself | Bribery | Refrain + fear | Keeps fear audible inside the comedy |
| 3:58 | A: $70 | Bribery rung 3 | Number alone as a bubble | |
| 3:59 | C: n I wouldn't be taking the money ... I used to be so scared man money wouldn't do anything | Aside | Host empathy, callback to his childhood aside | Ties the comedy back to the fear |
| 4:11 | P: make it a 100 | **Bribery (counter-offer)** | Child takes control | Payoff of the ladder: the victim sets the price |
| 4:14 | C: and we have a $100 | Reaction | Auctioneer voice | |
| 4:19 | A: that's too much it's only $30 more than what you... | Bribery | Haggling | |
| 4:23 | P: then I'm going to call Mom / I want to tell her you went to a party / left me home alone | Bribery | Ultimatum repeated with the refrain | |
| 4:23 | C: fine Andrew's going to give in | Reaction | Host prediction | Rewarded 10 s later |
| 4:31 | A: okay okay / $100 / deal | Bribery close | Deal | Closes the loop opened at 3:30 |
| 4:38 | P: deal | Bribery close | Echo | |
| 4:39 | C: I knew it I knew it | Reaction | Host is right | Prediction-reward loop |
| 4:41 | A: okay / I'll be home soon / now go back to bed | Reassurance | Fourth "home soon" | The promise is now paid for, which raises the cost of breaking it |
| 4:46 | C: oh the music / oh / 3:00 a.m. okay wait wa wait okay so it's like 10 something now it's 3:00 a.m. | **Time skip + sting** | Music cue, clock jump to the hour the hook named | Closes the 0:04 clock promise; the viewer knows the break-in is next |
| 4:54 | P: oh thank God you're home | **False relief** | Relief before the scare | Relief line makes the next reveal hit harder |
| 4:57 | C: uh-oh / uhoh someone broke broke into my house at 3:00 a.m. that's not that's not Andrew | Reaction | Host jumps ahead of the chat | The host is ahead of the characters, the classic suspense gap |
| 5:06 | A: what | Inciting | One-word reply | |
| 5:06 | P: I couldn't sleep / I just heard you come in | **Inciting (threat onset, 48%)** | Sound in the house | The first sign of the intruder, as a noise |
| 5:08 | A: what / what do you mean / I'm still at the party | **Reveal** | Protector is elsewhere, so the noise is someone else | The core reversal: the sound the child took for safety is the threat |
| 5:15 | C: holy 3:00 a.m. you're out there late buddy | Reaction | Joke | Releases a little pressure |
| 5:20 | P: I can hear you downstairs LOL | Dramatic irony | Victim still thinks it's a prank | The "LOL" is the last moment of innocence |
| 5:22 | A: I'm just about to leave the party | Reveal (confirm) | Distance stated | Establishes the race: brother vs. intruder |
| 5:28 | P: what / so who did I just hear downstairs | Open loop | The question the title promised | Who is in the house? |
| 5:33 | P: someone just entered the house | Escalation | Statement of fact | |
| 5:36 | A: it's probably your imagination go back to bed | Rationalization | Skeptic voice | The protector dismisses it (a fifth time) |
| 5:40 | C: even though he was not sleeping okay I sorry that was a bad prediction | Aside | Host admits a wrong guess | Keeps him fallible and human |
| 5:43 | P: no I could really hear someone downstairs / is it really not you / I'm getting scared | Escalation | Insistence + fear | |
| 5:50 | A: it's it's not me / I just left the party / not quite long | Escalation | Denial of being the noise | Closes off the innocent explanation |
| 5:59 | P: so so then who is downstairs | Open loop (re-asked) | Repeated question | |
| 6:02 | C: oh my god oh the music | **Sting 2** | Music cue | Signals the threat is now active |
| 6:04 | A: what's... / hello / are you there | **Silence beat 1** | Unanswered check-in | The gap between bubbles is the scare |
| 6:15 | C: uh-oh what happened | Reaction | | |
| 6:17 | P: the back door open / someone must have broke [in] | **Proof of entry** | Physical evidence | Turns "a noise" into "a break-in" |
| 6:23 | A: what | Reaction | | |
| 6:24 | P: what do I do / I'm getting scared | Plea | Question to the protector | The child hands control to the absent brother |
| 6:29 | A: okay listen to me / call the police / go back to your room / and lock the door / hide | **Protocol** | Step-by-step instructions, one per bubble | Gives the viewer a checklist to watch fail |
| 6:43 | C: Paul oh we got a name Paul the bro | Aside | Host notices a detail | The victim's name first appears at 65% of runtime; until then he is only "little bro" |
| 6:47 | P: okay okay | Compliance | | |
| 6:48 | A: are you in your room | Check | Status question | |
| 6:55 | P: yeah | Check | | |
| 6:56 | A: have you locked the [door] | Check | | |
| 7:00 | P: yeah | Check | | |
| 7:01 | C: oh sorry yes I just did | Aside | Host voice slip | |
| 7:04 | P: I can hear the person footsteps / I can hear him walking around the house | **Escalation (sound)** | Footsteps | The threat moves through the house |
| 7:10 | P: what if he finds me / what do I do | Escalation | "What if" callback to 1:16 | The child's fear from the setup returns in concrete form |
| 7:16 | A: I'm already close to the house | Race | Rescuer's distance | Puts the brother on a clock |
| 7:19 | A: just stay quiet / and try to stay calm | Protocol | Instruction | |
| 7:26 | P: I just heard him go to Mom's room | **Escalation (location)** | Room-by-room tracking | The intruder enters the absent parent's room; distance ladder rung 2 |
| 7:29 | A: do you have anything to protect yourself with | Escalation | Weapon question | Raises the possibility of a fight |
| 7:32 | C: just just protect yourself sorry getting ahead of myself | Aside | Host reading ahead | |
| 7:36 | P: there's nothing with me | Escalation | Helplessness | No weapon, so rescue must come from outside |
| 7:38 | A: all right just stay where you are / I'm already close | Race | Repeated distance | |
| 7:47 | P: oh no | **Silence beat 2 (opens)** | Two-word dread line, then nothing | Victim sees something but doesn't say what |
| 7:49 | A: what's wrong | Silence beat 2 | Question | |
| 7:51 | C: what's going to happen guys what's going to happen | Reaction | Direct address | Invites comment predictions |
| 7:54 | A: did something happen / oh no / Paul / what's wrong / Paul / hello / Paul / are you there | Silence beat 2 | Repeated name checks, unanswered | Same device as the Textify chats: unanswered name checks right before the reveal |
| 7:58 | C: the guy's in the bedroom with them | Reaction | Host's worst-case guess | |
| 8:05 | C: oh no they're going to send a photo | Re-hook | Host predicts a photo | Primes a visual payoff that never comes (subverted) |
| 8:09 | P: he knows I'm here / he knows I'm hiding in my room | **Escalation (detected)** | Victim is found | Distance ladder rung 3 |
| 8:12 | C: oh my God | Reaction | | |
| 8:17 | P: he's at the door / he keeps twisting the door knob / trying to open it | **Climax (barrier)** | Door-knob siege | Distance ladder rung 4: one door between them |
| 8:22 | C: send a picture Paul send a picture | Reaction | Host repeats the photo wish | |
| 8:27 | P: Andrew where are you | Callback | Exact echo of the first bubble (0:18) | The opening question returns in life-or-death form |
| 8:27 | C: Andrew you got got to be close now | Reaction | | |
| 8:31 | P: I'm really scared / Andrew why aren't you answering | Silence (reversed) | Now the protector goes silent | Mirrors silence beat 2 from the other side |
| 8:34 | P: wait something is happening / he just screamed in pain | **Turn (off-screen fight)** | Sound only | The rescue happens off-screen, as sound |
| 8:38 | C: oh Andrew's there | Reaction | Host infers the rescue | |
| 8:42 | P: Andrew / I think he fell down | Turn | | |
| 8:43 | C: Andrew Andrew got him Andrew has been replying ... it's Andrew man Andrew came me Clutch | Reaction | Host celebrates early | Sets up the false-twist doubt |
| 8:47 | P: someone else is out there / I can hear them fighting | Turn | Fight as sound | |
| 8:51 | C: oh no something's going to happen to Andrew | Reaction | Host flips back to dread | |
| 8:55 | A: you can come out now Paul I took care of it | **False all-clear (ambiguous)** | Message from the protector's phone that could be the intruder | Classic "the killer has the phone" set-up; the viewer can't trust it |
| 9:01 | P: what / are you sure | Doubt | Question | |
| 9:05 | A: don't worry it's safe | Ambiguous reassurance | | |
| 9:07 | C: oh no oh no oh no oh plot twist we got like 30 seconds left but plot twist ... it's actually the person that broke in ... and now the bad guy's got the phone | **Re-hook (twist theory)** | Host builds a twist out loud, points at the remaining runtime | Makes the last 50 s tense even though the chat itself is resolving |
| 9:27 | P: wait / was that you fighting the man | Confirmation | Direct question | |
| 9:30 | A: yeah / he can't hurt you anymore | Resolution | | |
| 9:33 | C: oh no plot twist here comes | Re-hook | Host still expects a twist | |
| 9:35 | A: I'm sorry for leaving you home / I shouldn't have done that / I will never do that again | **Resolution (guilt paid)** | Apology | Closes the guilt loop from 0:41 / 2:08 |
| 9:40 | C: uh-oh | Reaction | | |
| 9:51 | P: you promise | **Callback** | The promise word from 1:53 | Bookend |
| 9:52 | A: I promise | Ending | Callback | The last chat bubble answers the host's 1:55 "never make promises" |
| 9:59 | C: what / there's no plot twist there's just a good wholesome story ... Andrew came home just in time to attack the guy before he got into the bedroom | **Subverted twist** | Host recaps and admits no twist | Lets the viewer feel both relief and the "too clean?" itch |
| 10:09 | C: and then what happened to the bad guy ... knocked out cold maybe you're not alive / who knows guess we'll never know | Open loop (left) | Unanswered question | Gives the comments something to argue about |
| 10:13 | C: let me know your predictions down below and I'll see you guys in the next one wait wait wait make sure you drop a like ... and subscribe ... peace | CTA | Comment prompt + like/sub with a fake-out "wait wait" | Standard outro |

## 2. Structure summary

### Beat sequence (% of 621 s)

| Range | Beat | Words | % runtime |
|---|---|---|---|
| 0:00–0:17 | Host hook: premise spoiled (break-in) + clock (3 a.m.) + reading the chat's date stamp | 69 | 3% |
| 0:18–1:03 | Setup: "where are you" → not home → party → Mom's rule broken → "only one at home" → "go back to sleep" | 101 | 7% |
| 1:04–1:47 | Fear plant ("what if something bad happens") + **host's 30 s childhood aside** | 168 | 7% |
| 1:48–1:59 | Promise plant + host's "never make promises" foreshadow | 31 | 2% |
| 2:00–3:03 | Leverage: "I'm calling Mom" ↔ "she'll be mad at me"; refrain "home alone"; host predicts the harm at 2:48 | 139 | 10% |
| 3:04–3:30 | Pleading + host emoji-trivia aside + "I'm telling Mom right now" | 53 | 4% |
| 3:31–4:45 | **Bribery auction** $20 → $50 → $70 → child names $100 → deal; "go back to bed" | 147 | 12% |
| 4:46–4:57 | Music sting + time skip to 3:00 a.m. + false relief ("thank God you're home") | 32 | 2% |
| 4:58–5:35 | **Threat onset (48%)**: "heard you come in" → "I'm still at the party" → who's downstairs? | 77 | 6% |
| 5:36–6:03 | Rationalization ("your imagination") → denial → question re-asked → music sting 2 | 61 | 4.5% |
| 6:04–6:28 | Silence beat 1 → back door open → "what do I do" | 24 | 4% |
| 6:29–7:03 | Protocol: police, room, lock, hide; status checks; the child's name appears | 45 | 5.5% |
| 7:04–7:46 | Footsteps → "what if he finds me" → he's in Mom's room → no weapon → brother "close" | 86 | 7% |
| 7:47–8:08 | Silence beat 2: "oh no" then unanswered name checks; host primes a photo | 42 | 3.5% |
| 8:09–8:33 | Found → at the door → twisting the knob → first bubble echoed → brother silent | 55 | 4% |
| 8:34–8:54 | Off-screen fight as sound: scream, fall, someone else, fighting | 51 | 3.5% |
| 8:55–9:26 | Ambiguous all-clear from the brother's phone + host's out-loud twist theory | 86 | 5% |
| 9:27–9:58 | Confirmation → apology → "you promise" / "I promise" | 41 | 5% |
| 9:59–10:21 | Host: "no plot twist", unanswered question about the intruder, CTA | 102 | 3.5% |

Four acts:
- **Sibling comedy of stakes (0:00–4:45, 46%)**: no danger in the chat; the guilt, the promise and the "home alone" refrain are planted.
- **Hinge (4:46–4:57, 2%)**: music, clock jump, false relief.
- **Home-invasion ladder (4:58–8:54, 38%)**: noise → proof → hide → footsteps → room → door → fight.
- **Ambiguous rescue and bookend (8:55–10:21, 14%)**: trust test, apology, promise callback, host wrap.

The threat starts at **48% of runtime**. That would kill a narrated Short, but here it works because the host spoiled the premise in the first 4 s and the setup is entertaining on its own (an auction, comic power reversal, the host's personality).

### Hook

- **The host's spoken premise is the hook**: about 25 words / 8 s ("a scary text chat about someone breaking in ... at 3 a.m."), backed by an all-caps superlative title. The first chat bubble lands at 0:18.
- The hook gives away the *event* and the *time*, and withholds *who* and *what happens to the child*. The 3 a.m. promise is closed exactly at 4:50, which pays off the viewer's patience.
- First fear line inside the chat: 1:12 ("because I'm scared", 12% runtime). First threat in the chat: 5:06 ("I just heard you come in", 48%).
- **For our pilots:** in a narrator-led horror video we can copy this by stating the incident and the hour in the first sentence and then letting a non-horror setup run long, *as long as the setup has its own engine* (an argument with rising numbers, a bet, a rule).

### Re-hook interval

60 jolts tagged (new information, a reversal, a music sting, or a host prediction).

- Gaps (s): 4, 14, 8, 15, 12, 3, 16, 4, 39, 5, 10, 18, 20, 34, 10, 7, 9, 10, 13, 12, 13, 10, 4, 8, 11, 6, 16, 12, 7, 9, 3, 8, 7, 15, 11, 21, 6, 16, 3, 7, 11, 10, 8, 4, 8, 3, 13, 5, 5, 4, 4, 4, 12, 20, 8, 16, 8, 10, 4.
- **Median 9 s, mean 10.4 s.** Before the threat (0:00–4:57): median 10 s, mean 12.4 s. After it (4:58 on): median 8 s, mean 9 s. In the door siege and fight (8:09–8:55) they come every **4–5 s**.
- The two longest dry stretches are both **host asides**: the childhood story (1:16–1:55, 39 s) and the run-up to the host's prediction (2:28–3:02, 34 s). The format tolerates them because the host himself is the attraction.
- **Host predictions are a re-hook device of their own**: 1:04, 1:55, 2:48, 4:23, 5:00, 7:58, 8:05, 8:43, 9:07, 9:33. About one every 50 s, and each opens a "was he right?" loop. Several are wrong on purpose or by accident (5:40, 8:05 photo, 9:07 twist), which keeps the ending uncertain.
- **Silence as a re-hook**: two unanswered-check-in runs (6:04–6:15 and 7:47–8:08) plus a reversed one where the protector goes silent (8:31).

### Open loops (open → close)

| Loop | Opens | Closes |
|---|---|---|
| Title + host: someone breaks in at 3 a.m. | 0:00 / 0:04 | 4:50 (3 a.m. on screen) → 6:17 (back door open) |
| Where is Andrew? | 0:18 | 0:41 (a party) |
| Will Paul tell Mom? | 2:00 | 4:36 (the bribe closes it); never reopened, Mom never appears |
| "What if something bad happens" | 1:16 | 6:17–8:20 (it does) |
| The promise (host: "never make promises you can't") | 1:53 / 1:55 | 9:51–9:52 ("you promise" / "I promise") |
| How much will the bribe be? | 3:30 | 4:36 ($100 deal) |
| Who is downstairs? | 5:28 | Never named: the intruder stays a faceless "he" / "the man" |
| Will Andrew get there in time? | 5:22 / 7:16 | 8:34–8:51 (off-screen fight) → 9:30 |
| Is the all-clear really from Andrew? | 8:55 | 9:27–9:30 (yes) |
| Host's photo prediction | 8:05 | Never paid: no photo is sent (a deliberate frustration) |
| What happened to the intruder? | 10:09 | Left open for the comments |

Two to four loops are open at any moment. The comedy loops (Mom, the bribe) close **before** the horror starts, so the second half runs on just three: who, in time, and can we trust the phone.

### Escalation ladder

- **Setup ladder (social stakes):** brother not home → at a party → Mom's rule broken → child alone → child scared → threat to tell Mom → bribe $20 → $50 → $70 → $100.
- **Distance ladder (the threat gets closer, one rung every ~20–40 s):** a sound downstairs (5:06) → "someone entered" (5:33) → back door open (6:17) → footsteps around the house (7:04) → in Mom's room (7:26) → "he knows I'm here" (8:09) → at my door, twisting the knob (8:17).
- **Rescue ladder in parallel:** "about to leave the party" (5:22) → "just left" (5:52) → "already close" (7:16, 7:43) → silence (8:31) → a scream (8:38). The two ladders meet at the bedroom door.
- **Sound ladder:** footsteps → doorknob → scream → fall → fighting. All the action is heard, never seen.
- **Register ladder:** the host's tone runs from jokey (curling, emoji trivia, FOMO) to quieter one-word reactions from 6:00, then back to celebration at 8:43 and to dread again at 8:51.

### How it ends

- A **trust test** (an all-clear from a phone that could be compromised), amplified by the host theorizing a twist out loud with "30 seconds left".
- The twist is then **subverted**: it really was the brother. The guilt loop closes with an apology, and the promise planted at 1:53 closes as the last two bubbles, a clean bookend.
- The host lampshades it ("there's no plot twist, just a good wholesome story") and leaves one question open (is the intruder dead?) as the comment prompt. CTA: predictions in the comments, like, subscribe, with a "wait wait wait" fake-out.

### Pacing and device notes for the PLAYBOOK

- **136 wpm overall**, about half of it host talk. The chat alone runs at roughly 70 wpm of read bubbles, much slower than the 270 wpm Textify Shorts, because the host leaves room between bubbles and talks over them.
- **Spoil the event, not the outcome.** Stating the incident and its hour up front buys a 46% non-horror setup.
- **Give the setup its own engine:** a negotiation with rising numbers (the bribe auction) keeps re-hooks coming every 10–15 s with no danger at all.
- **Guilt plant → apology payoff** and **promise plant → final-line callback** give a 10-minute chat a satisfying shape.
- **First-line echo at the climax:** the opening question comes back word for word when the threat is at the door.
- **Protector instructions as a checklist** (call police, go to room, lock, hide, stay quiet) followed by status checks: the viewer watches each safeguard get tested.
- **The rescue happens off-screen as sound**, reported by the victim in real time.
- **Host predictions as re-hooks**, roughly every 50 s, some wrong on purpose. For a faceless channel, an on-screen "narrator voice" or a comment-style overlay could take this role.

## 3. Transferable skeleton (no original wording)

For a **long-form (8–11 min) text-chat home-invasion story, read along by a host voice** who reacts between bubbles. Two parties: the **victim** (a child or vulnerable person alone at home) and the **absent protector** (whose phone the viewer holds). Pace: ~130–140 wpm total, about half host talk; one jolt every ~10 s in the setup and every ~5 s at the climax.

| % of runtime | Beat | What happens (abstract) | Device |
|---|---|---|---|
| 0–3% | Host hook | The host states the incident and the exact late hour in one or two sentences, then reads the chat's date stamp | Spoil the event, withhold the outcome; a clock number to wait for |
| 3–10% | Absence | The victim asks where the protector is; a small reversal (not where they said); the protector admits a selfish reason for being away; a broken household rule; "I'm the only one here" | First bubble is a question; guilt plant |
| 10–17% | Fear plant + aside | The victim can't sleep and asks "what if"; the protector dismisses it; the host tells a short relatable memory about being scared as a kid | Famous-last-words reassurance; parasocial aside (≤30 s) |
| 17–19% | Promise plant | The protector makes a promise to be back; the host warns about promises | Plant for the final line |
| 19–34% | Leverage | The victim threatens to tell the missing authority figure; the protector begs; a two-word refrain about being alone is repeated; the host predicts out loud that something bad will happen | Power reversal comedy; refrain; host prediction as re-hook |
| 34–46% | Auction | The protector offers a bribe; it rises in 3–4 steps; the victim names the final price; deal; "go to bed" | Number ladder the viewer can bet on |
| 46–48% | Hinge | A music sting and a jump to the promised hour; the victim greets a noise as the protector coming home | Close the hook's clock promise; false relief |
| 48–58% | Onset | The protector is still away, so the noise is someone else; the protector rationalizes; the victim insists; question re-asked; second sting | Reversal of a reassuring sound |
| 58–63% | Proof | An unanswered check-in, then physical evidence of entry | Silence beat |
| 63–69% | Protocol | The protector sends one instruction per bubble (call for help, go to a room, lock, hide); status checks | Checklist to be tested |
| 69–76% | Closing in | Footsteps, a room-by-room location, "no weapon", the protector says they are close | Distance ladder + rescue ladder in parallel |
| 76–80% | Silence 2 | The victim sends a two-word dread line, then goes quiet; repeated name checks; the host predicts a photo | Unanswered name checks; a primed payoff that never comes |
| 80–84% | Siege | Found; at the bedroom door; the handle moving; the victim echoes the first bubble word for word; now the protector goes silent | First-line echo; reversed silence |
| 84–87% | Off-screen fight | Reported only as sounds (a scream, a fall, struggling) | Rescue as sound |
| 87–92% | Trust test | An all-clear arrives from the protector's phone; the victim doubts; the host builds a "the bad guy has the phone" twist out loud and points at the remaining runtime | Compromised-phone suspicion |
| 92–97% | Resolution | Confirmation; apology for leaving; "promise?" / "promise" as the last two bubbles | Guilt paid; bookend callback |
| 97–100% | Wrap | The host admits there was no twist, leaves one small question open (the intruder's fate), asks for predictions in the comments, CTA | Lampshade + comment prompt |

Production notes:
- The chat app needs **music stings** on two beats (the time jump and the moment the threat becomes active).
- Single-word bubbles land with real pauses at the climax; the slowest minute of the video (71 words) is the break-in.
- Never show the intruder; no image in the chat.
- Title: all-caps superlative ("scariest ... ever") with no spoiler beyond the genre. The thumbnail and the host's first line carry the incident.
- For our faceless kit, the host layer can be a second TTS "reader" voice or on-screen reaction captions; its predictions are a re-hook device worth copying, while its personal asides need a real persona and are optional.
