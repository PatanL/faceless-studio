# Two Windows, Resident Guidance (annotated)

| Field | Value |
|---|---|
| URL | https://www.youtube.com/watch?v=kJCVK8xTkPk |
| Title | "If Your Neighbour Waves from Two Different Windows… Only Wave Once \| Resident Guidance" |
| Channel | Resident Guidance (channel median 774 views over the 19 most recent uploads on the Videos tab) |
| Views | 13,473 |
| Outlier score | **17.41x** |
| Duration | 314 s (5:14). Speech runs 0:00 to about 5:08; then an RGB glitch sting (~5:10) and an "END OF FILE 017" card on black (5:12–5:14) |
| Upload date | 2026-10-18 |
| Format | 16:9 YouTube "resident guidance" rules video. A calm, neutral, British-English synthetic narrator speaks second-person procedure ("you") over flat white line-art pictograms on black: a two-storey house elevation with four windows, a glowing white stick-figure protagonist, lit window frames with a waving silhouette. Annotation overlays do the storytelling: dashed yellow sight-line arrows, yellow ticks and red crosses, red circles, a phone chat mock-up, a circular peephole vignette, checklists. A 1–5 rule tracker sits at the top of the frame (finished rules turn into red crossed boxes). Burned-in captions in small caps at the bottom: white for narration, **red** for warnings, **yellow** for the safe action. Music bed under everything (auto-subs flag [music] on almost every line). Two RGB-glitch stings only (~4:03 and ~5:10). Each video is framed as a numbered case file ("END OF FILE 017") |
| Total words | **736 spoken** in the auto-subs (116 VTT lines). About 20 words are clipped at line ends in the VTT; the burned-in captions restore them, so the full script is about **755** |
| Words/min | **~141 wpm** over the full runtime (736 / 5.23 min); **~147 wpm** over the spoken span 0:00–5:08 with the caption restorations. Slow, level and bureaucratic, the same band as the other English-native YouTube rules videos (144–179) and about half the TikTok repost pace. Average sentence about 7 words; many 2–4 word punch lines |

Sources:
- Transcript: `raw/kJCVK8xTkPk.txt` (yt-dlp en-orig auto-subs, run on the Spark, cleaned with `tools/vtt2lines.py`). Clipped line ends restored below from the burned-in captions and marked with [brackets]. One mishearing fixed from the caption: "tends to prompt a vision" is "tends to prompt a **visit**". "Dish you took round" is "The dish you took round".
- Frames: `sheets/kJCVK8xTkPk.jpg` (overview, 8x8 tiles, one frame every 5 s: tile n = second 5n, read left to right). 1 fps sheets on the Spark at `~/studio/refs/corpus_horror/sheets/kJCVK8xTkPk/s_001..027.jpg` (sheet k covers seconds 12(k-1) to 12k-1). Video at `~/studio/refs/corpus_horror/vid/kJCVK8xTkPk.mp4` (480p). I checked sheets 1, 3, 4, 5, 9, 10, 16, 18, 21, 25, 26, 27 plus the full overview.

Lines are quoted verbatim for internal research only. Never reuse the wording, the two-windows/wave premise, the "which one?" message, the "waving me over" tell phrase or the case-file framing.

**Key mechanic, the cold open shows the anomaly and the rules manage it.** Unlike the mother's-note format (cVUJmsVkUW4), the threat is shown in the first 30 s as a quiet, concrete wrongness (the same neighbour waving from two windows at once), and only then does the guidance begin ("There are five rules for what happens next"). Every rule is pinned to a moment in an ordinary evening (walk to the door, unpack shopping, a text, a knock, bedtime, next morning), so the rules list doubles as the plot timeline. Horror comes from four things:
1. **Procedure as dread.** Flat, specific chores (milk in the fridge, frozen things in the freezer) are given as survival steps. The calm makes the wrongness louder.
2. **Normal-versus-wrong tests.** The guidance tells you what a normal neighbour would say, then names the one phrase that means it is not your neighbour. The viewer listens for the tell with the protagonist.
3. **Hedged frequency words.** "Usually", "probably", "most will... a few will...", "sometimes it was the television". They imply the guidance-writer has seen many cases, and that some went badly.
4. **A closing inversion.** The final rule turns the situation around: now your neighbour is the one checking *your* two windows, and the last line ("They may not be waving at you") means there is now a second you. The opening rule ("wave once") is inverted to "keep your hands where they are".

There is no named monster, no backstory and no explanation of what the second figure is. The case-file number is the series hook.

## 1. Line-by-line

| Time | Line (verbatim, internal only) | Beat | Device | Purpose | Visual |
|---|---|---|---|---|---|
| 0:00 | If your neighbor waves from two different windows, only wave once. | Hook (title rule) | Title-as-first-line, if/then rule, second-person "you" | States the whole premise and the core rule in 4 s; the viewer is instantly the protagonist | House elevation on black, both lit windows with a waving figure; caption white, then "ONLY WAVE ONCE." in red with red circles on the two windows |
| 0:04 | They wave. | Cold open (scene) | 2-word present-tense line | Switches from rule to live scene; slows the pace right down | Protagonist (glowing stick figure, shopping bag) in the foreground, house behind |
| 0:06 | You wave back. | Cold open | 3-word line, "you" action | Makes the viewer complicit in a normal, polite act | Close-up: figure raising a hand |
| 0:08 | Then you look up. | Cold open (turn) | Sequence word "then", short line | The turn: something is about to be wrong | Pull-back to the house |
| 0:10 | Your neighbor is also standing at the bedroom window. | Inciting image | Impossible detail stated flatly | The anomaly, shown not explained; "also" does all the work | Same neighbour in the upstairs window; RGB tremor on the house (first micro glitch) |
| 0:13 | Same shirt. | Cold open (escalation) | Fragment list ("same..."), 2 words | Rules out a second person; builds by repetition | House with a small yellow warning triangle by the roof |
| 0:15 | Same tilted head. | Cold open (escalation) | Fragment list, body detail | The tilted head is the first slightly uncanny body detail | Same, tighter |
| 0:17 | Their hand is already raised. | Cold open (escalation) | "Already" (anticipation) | The copy was waiting for you; implies intent | Upstairs figure, hand up |
| 0:21 | You glance back at the kitchen. | Cold open | Second-person action | Viewer checks the first window with the protagonist | Push in on the ground-floor window |
| 0:23 | They're still there. | Cold open (confirm) | 3-word confirmation | Both are real at once; no cut-away excuse | Both lit windows in close-up |
| 0:26 | For a moment, all three of you are holding a hand in the air. | Cold open (tableau) | Freeze-frame image, "three of you" | Holds the uncanny tableau; counts the protagonist in with the copies | Yellow dots marking three raised hands |
| 0:30 | Lower yours. | First instruction | 2-word imperative, yellow caption | The voice switches from narrator to guide; the first safe action | Figure lowers the arm; caption "LOWER YOURS." in yellow |
| 0:32 | You haven't done anything wrong yet. | Re-hook (stakes) | Reassurance with a sting ("yet") | Comfort and threat in one word; tells the viewer there is a way to go wrong | Small typed status text appears above the roof, then turns red |
| 0:35 | There are five rules for what happens [next]. | Contract | Numbered promise ("five rules") | Sets the runtime map: the viewer knows there are five beats to sit through | Black screen, boxes 1–5 appear one by one |
| 0:39 | Rule one. | Rule 1 card | Ordinal title card | Chapter break; the tracker becomes the progress bar | Tracker with box 1 lit, "RULE 1" in small yellow mono type |
| 0:42 | Only wave once. | Rule 1 | Rule restated (callback to 0:00) | Repetition locks the core rule in | "ONLY WAVE ONCE." centred under the tracker |
| 0:44 | It doesn't matter which window you acknowledged. | Rule 1 (clarify) | Pre-empting the viewer's question | Removes the "pick the right one" puzzle, which makes it stranger | Dashed yellow sight lines from figure to both windows, ticks |
| 0:47 | Don't try to correct yourself. | Rule 1 (warning) | Prohibition | Names the natural impulse and forbids it | Red sight line to the second window crossed out in red |
| 0:50 | Don't give the other window a little nod because it feels rude to ignore [them]. | Rule 1 (warning) | Social-politeness trap, specific micro-action ("a little nod") | Horror through manners: the danger is being polite | A head icon by the house gets a red prohibition circle |
| 0:56 | You have greeted your neighbor. | Rule 1 (closure) | Bureaucratic restatement | Turns the greeting into a counted transaction | Black screen, "GREETINGS GIVEN", a single tally mark, "1/1" |
| 0:58 | That is enough. | Rule 1 (closure) | 3-word punch line | Calm finality; the stamp lands | Red "SUFFICIENT" stamp on the 1/1 counter; caption yellow |
| 1:00 | Continue to your front door at your normal pace. | Rule 1 (movement) | Instruction, "normal" (motif word) | Starts the walk home; "normal" will recur as the safety word | Top-down path map to the door with a small pace gauge |
| 1:04 | If you drop your keys, pick them [up]. | Rule 1 (branch) | If/then on a mundane accident | Ordinary mishaps become tests; the viewer feels watched | Keys falling, one hand line |
| 1:08 | If a bag splits, collect your [shopping]. | Rule 1 (branch) | If/then, mundane | Second mishap; builds the pattern | Shopping bag with items on the ground |
| 1:12 | You can take your time. | Rule 1 (permission) | Permission line | Odd calm: rushing is the danger, not slowness | Same |
| 1:14 | Just don't look up to check whether they're still [watching]. | Re-hook | Prohibition, "still watching" | Implies they are watching the whole walk; the viewer wants to look | Figure walking past the house; a red crossed-out eye icon top right |
| 1:17 | You'll want to work out which window was the right one. | Rule 1 (open loop) | Naming the viewer's own thought | Opens the "which one is real?" loop and leaves it open | Figure at the door, red eye icon |
| 1:22 | For now, the important thing is that you only chose one. | Rule 1 (close) | "For now" (deferral) | Closes the rule; "for now" hints the question comes back (it does at 2:45) | Same, figure small |
| 1:27 | [music] | Breath | Music-only pause (~1 s) | Chapter breath before rule 2 | Transition |
| 1:28 | Rule two. | Rule 2 card | Ordinal title card | New chapter; tracker box 1 now red-crossed | Tracker, box 2 lit |
| 1:30 | Put your shopping away. | Rule 2 | Mundane imperative as a rule | Anticlimax on purpose: a chore given rule weight | "PUT YOUR SHOPPING AWAY." under the tracker |
| 1:31 | Lock your door as usual. | Rule 2 | "As usual" (normality motif) | The one defensive action, buried among chores | Door icon |
| 1:33 | Put the milk in the fridge. | Rule 2 | Hyper-specific chore | Grounds the viewer in a real kitchen | Fridge outline, item ticks |
| 1:35 | Put the frozen things in the freezer. | Rule 2 | Hyper-specific chore, rhythm (parallel lines) | Rhythm of chores as a lull | Fridge, "frozen" ticked |
| 1:37 | Give yourself something ordinary to finish. | Rule 2 (purpose) | Hidden rationale | Explains the chores as a coping technique: the guide knows how scared you are | Checklist: milk, frozen, fold the bags, put the kettle on (all ticked one by one) |
| 1:41 | From your kitchen, you may be able to see their [house]. | Rule 2 (threat returns) | Sight-line reminder | Brings the neighbour back into the safe space | Kitchen window framed by curtains, the neighbour's house inside it |
| 1:44 | Leave the curtains exactly as they were. | Rule 2 | Counter-intuitive rule ("exactly") | The natural move (close them) is forbidden | Curtain frame; the house window glows |
| 1:48 | Closing them suddenly tends to prompt a visit. | Re-hook (consequence) | Understated consequence, "tends to" (frequency hedge) | First stated consequence; "a visit" plants the knock at 3:00 | Curtains drawn; red caption; small red annotation text and a "knock" sound-wave icon |
| 1:51 | If you accidentally catch sight of your neighbor, they should have lowered their [hand]. | Rule 2 (test) | Normal-state test ("should have") | Gives the viewer a check to run | Curtains open, both windows; one figure lowers the hand |
| 1:56 | The other one won't have. | Re-hook | 5-word sting, "the other one" | Confirms the copy is still there with its hand up, watching your kitchen | Upstairs figure still waving, small red tag |
| 1:58 | Don't stare long enough to compare them. | Rule 2 (warning) | Prohibition on comparison | Implies comparing is dangerous, or that you might not like the answer | A thin loading bar fills above the roof; "≠" symbol |
| 2:01 | There won't be anything useful to notice. | Rule 2 (close) | Dismissal of curiosity | Shuts down the viewer's urge to solve it, which makes them want to more | Same |
| 2:04 | Rule three, if your neighbor messages you, let them speak first. | Rule 3 card | Ordinal + if/then on the card | Moves the threat to the phone: contact without proximity | Tracker box 3 lit; phone outline |
| 2:09 | It will usually be something normal. | Rule 3 | "Usually" hedge | Normal is the default, which makes the exception scary | Empty phone chat |
| 2:12 | A parcel. A borrowed tool. Whether your internet has gone down, too. | Rule 3 (list) | Triplet of mundane examples | Concrete, relatable texts; "too" hints at a shared outage (unexplained) | Example message bubbles |
| 2:18 | Answer the question they actually asked. | Rule 3 | Rule, "actually" | Narrow, literal answering as a defence | Reply bubble with yellow tick |
| 2:21 | Don't mention the windows. | Rule 3 (warning) | 4-word prohibition | Naming the anomaly is dangerous | Phone |
| 2:23 | If they ask whether you've just got home, say yes. | Rule 3 (script) | If/then with a scripted answer | Gives the viewer lines to say: ritual dialogue | "Just got home?" bubble, "Yes" reply |
| 2:27 | If they ask whether you saw them, say, yes, I waved, nothing more. | Rule 3 (script) | Scripted answer, "nothing more" | Exact wording as protection; plants the "wave once" logic in speech | "Did you see me?" bubble, short reply |
| 2:34 | They may take a while to reply. | Rule 3 (tension) | Delay | Tension through waiting | Chat, nothing |
| 2:36 | You might see them typing, stopping, then typing again. | Rule 3 (tension) | Typing-indicator beat | Universal modern anxiety; implies the other side is deciding | Typing dots appear and vanish |
| 2:41 | Eventually, they'll probably send a thumbs up. You can leave it there. | Rule 3 (false release) | "Probably" hedge, mundane release | The normal ending; a breath | Thumbs-up bubble |
| 2:45 | But if the next message says, which one? | Re-hook / peak 1 | "But if" reversal, the loop from 1:17 returns as a question from them | The neighbour (or the copy) asks the viewer's own question; first real chill, at 53% | Phone, new grey bubble "which one?" |
| 2:47 | Put your phone face down. | Rule 3 (counter) | Physical counter-action | Cut contact | Phone outline goes blank |
| 2:50 | Don't answer that question, | Rule 3 (warning) | Prohibition | Answering would mean admitting there were two | Blank phone |
| 2:52 | even if another message follows saying it was a joke. | Re-hook | Pre-empted manipulation | Shows the thing can lie and walk it back; raises the stakes for rule 4 | Blank phone, a second notification dot |
| 2:57 | Rule four. Don't return the visit. | Rule 4 card | Ordinal, callback to "a visit" (1:48) | The planted visit arrives; the loudest rule title | Tracker box 4 lit |
| 3:00 | There may be a knock at your door. | Rule 4 (threat) | "May be" hedge, knock | Physical contact, the classic door beat | Front door outline vibrating with sound arcs |
| 3:02 | Look through the peephole if you have [one]. | Rule 4 | Instruction, dry aside ("if you have one") | Bureaucratic humour keeps the calm voice credible | Door; then circular peephole vignette |
| 3:04 | Your neighbor will be standing at a normal distance, wearing the same clothes you saw earlier. | Rule 4 (test) | Normality description, "same clothes" callback | Gives the visual baseline; "normal distance" implies an abnormal one exists | Glowing figure inside the peephole circle; small yellow "NORMAL DISTANCE" tag |
| 3:10 | They might be holding something of [yours]. | Rule 4 (bait) | Bait object | The lure is your own property | Figure holding a small object |
| 3:12 | A parcel with your name on it. The dish you took round last month. | Rule 4 (bait list) | Specific bait examples | Concrete, believable; the dish is a callback to a past kindness | Parcel, then a dish |
| 3:17 | Something you really would open the door for. | Re-hook | Naming the temptation | The viewer admits they'd open it; stakes become personal | Same |
| 3:19 | Ask them to leave it on the step. | Rule 4 (counter) | Polite-refusal script | Safety through a small rudeness; yellow caption | Side view: figure, door line, figure; object on the step |
| 3:22 | A normal neighbor might sound confused. | Rule 4 (normal test) | "A normal neighbour..." baseline | Teaches the viewer what a real person does, so the tell will stand out | Speech bubble "?" |
| 3:25 | They might ask if you're all right. | Rule 4 (normal test) | Realistic reaction | Lowers suspicion; a lull | "You all right?" bubble |
| 3:27 | They might even be a little offended. | Rule 4 (normal test) | Social cost | Makes the protagonist feel rude: an emotional cost of the rule | "...Fine." bubble |
| 3:29 | That's fine. You can apologize tomorrow. | Rule 4 (permission) | Permission, implies there will be a tomorrow | Wry comfort; keeps the tone dry | Yellow tick and a small "TMRW" calendar icon |
| 3:33 | What you're listening for is, | Re-hook (set-up) | Withheld-detail cliff, colon pause | Leans the viewer in: here comes the tell | Peephole circle (glitch flicker on entry), an ear icon |
| 3:35 | I thought you were waving me over. | Peak 2 (the tell) | Tell phrase, callback to the wave (0:06) | The polite wave is reframed as an invitation; the copy came because you waved. Main horror beat at 68% | Peephole figure, ear icon |
| 3:38 | If they say that, tell them, I was only saying hello. | Rule 4 (counter script) | Scripted counter-phrase | A precise verbal ritual; it echoes the "nothing more" logic | Figure inside the circle raising a hand |
| 3:44 | Say it once, | Rule 4 | "Once" callback (core rule) | The core rule returns in speech | Yellow "ONCE." beside the figure |
| 3:46 | then step away from the [door]. | Rule 4 | Instruction | Breaks proximity | Door |
| 3:48 | You may hear their shoes shift on the mat. | Rule 4 (aftermath) | Sound detail, "may" | The thing lingers; sound-only horror | Door with a small sound tag at the base |
| 3:51 | You may hear the letterbox lift, although nothing comes through. | Re-hook | Uncanny sound with an absence | Something looks or listens through the slot: the creepiest single image, never shown | Door, letterbox highlighted, small caption tag |
| 3:55 | Don't wait beside the door for the sound of them leaving. | Rule 4 (warning) | Prohibition on confirmation | Denies the viewer closure; you never learn if it left | Door |
| 4:00 | Go and finish putting your shopping [away]. | Rule 4 (return to chore) | Callback to rule 2 chore | Back to the ordinary; a rhythm reset | Kitchen window in curtains, bag, yellow tick |
| 4:03 | Rule five, let the evening end normally. | Rule 5 card | Ordinal; "normally" motif | Promises calm; the viewer suspects it won't be | RGB glitch sting on the kitchen window (one of only two in the video), then tracker with boxes 1–4 red-crossed, box 5 lit |
| 4:06 | You don't need to stay awake, you don't need to watch the windows, | Rule 5 | Negative permissions, anaphora ("you don't need") | Removes vigilance on purpose; the calm becomes the unease | Eye icon, then a window icon, each crossed in red |
| 4:09 | make dinner, find something to watch, charge your phone. | Rule 5 | Chore triplet | Lull rhythm; "charge your phone" quietly keeps the phone in play | Pan icon, TV icon, phone icon in boxes |
| 4:13 | If you hear a tap against the glass, check the time instead of the [window]. | Re-hook | If/then, displacement action | A new sound threat; the rule diverts your eyes | Sofa, clock and TV; yellow caption |
| 4:16 | If you hear another, turn your television down [slightly]. | Rule 5 (branch) | Escalating branch | The second tap is handled with a quieter room: odd and unexplained | Figure on the sofa, TV, clock |
| 4:20 | Sometimes it was the television. | Re-hook (doubt) | Hedge ("sometimes") that implies other times | The comfort carries its own threat | TV with a yellow tick |
| 4:23 | You're allowed to accept that explanation. | Rule 5 (permission) | Permission to believe a comfort | The guide openly offers a cover story: gaslight comfort | Same |
| 4:25 | When you go to bed, close your curtains as you normally would. | Rule 5 (night) | "Normally" motif, contrast with 1:44 | Curtains are allowed now, at the normal time; the rule system is precise | Bedroom curtains |
| 4:29 | By morning, both windows should be empty. | Resolution (morning) | "Should be" hedge, time jump | The anomaly ends, conditionally | House with both windows dark, a yellow tick on one |
| 4:32 | Your neighbor may be outside putting a bin out or scraping their windscreen. | Resolution (normal) | Mundane morning detail | Return to normal life | Neighbour figure with a wheelie bin |
| 4:36 | You can speak to them. You can even ask about yesterday. | Resolution (permission) | Permissions, "even" | Loosens the rules; invites the question | Two figures, house between |
| 4:40 | Most will say they weren't at the window. | Re-hook (frequency) | "Most will" (statistics of past cases) | Reveals this has happened to many residents; the real neighbour may never have been there | Speech bubble over the neighbour |
| 4:42 | A few will say they remember waving. | Re-hook | "A few will" counter-case | Unsettling either way: which one did you meet? | Yellow tick |
| 4:44 | Either answer is fine. | Rule 5 | Flat dismissal | Refuses to resolve the loop | Same |
| 4:46 | Don't ask about the other window, and if they seem unusually relieved to see you, let them change the subject. | Re-hook (role hint) | "Unusually relieved" (implied mirror experience) | Hints the neighbour had the same night, but about *you*: sets up the inversion | Neighbour with a "Bins are early this week" style small-talk bubble |
| 4:53 | There is one final thing. | Coda card | "One final thing" title card (typed on) | The rules said five; this is a bonus rule, so the viewer knows it matters | Black screen, white typewriter text |
| 4:55 | For the next few days, when you arrive home, check which windows your neighbor looks at. | Coda (set-up) | Time-span extension, role swap (you watch them watch) | Flips the gaze: now you check where they look | "DAY 1", "DAY 2" cards on black, then the protagonist outside the house |
| 4:59 | If they look at your kitchen, then your bedroom, | Coda (reveal) | If/then mirror of the cold open | They are seeing two of you in your two windows | Red-yellow sight line from the figure to the ground then upper window |
| 5:03 | and give one small wave. | Coda (reveal) | "One" (they are following the same rule) | The neighbour is obeying the same guidance, about you | Figure raises a hand |
| 5:04 | Keep your hands where they are. | Coda (counter) | Inverted core rule, yellow caption | You must not wave at all now: the rule tightens from once to zero | Figure's hand down, yellow caption |
| 5:06 | They may not be waving at you. | Twist / cliff | Final line, "may" hedge, red caption | The second figure is in your house now. Ends on the anomaly turned inward | Slow push into the protagonist's own upstairs window, a waving silhouette inside; red caption; RGB glitch (~5:10); "END OF FILE 017" on black (5:12–5:14) |

## 2. Structure summary

### Beat sequence (314 s)

| # | Beat | Time | Seconds | % runtime |
|---|---|---|---|---|
| 1 | Cold open: title rule, then the two-windows scene in short present-tense lines, "lower yours", "...yet", "five rules" | 0:00–0:39 | 39 | 12% |
| 2 | Rule 1, the greeting: wave once, no correcting, no nod, "that is enough", walk home at a normal pace, don't look up | 0:39–1:28 | 49 | 16% |
| 3 | Rule 2, indoors: chores, curtains stay as they are ("prompt a visit"), the other one hasn't lowered its hand | 1:28–2:04 | 36 | 11% |
| 4 | Rule 3, the message: scripted replies, typing dots, thumbs up, then "which one?" (peak 1) | 2:04–2:57 | 53 | 17% |
| 5 | Rule 4, the knock: peephole, bait object, normal reactions, the tell phrase (peak 2), counter-phrase, shoes and letterbox | 2:57–4:03 | 66 | 21% |
| 6 | Rule 5, the evening and morning: no vigilance, taps on the glass, "sometimes it was the television", empty windows, neighbour at the bins, "most... a few..." | 4:03–4:53 | 50 | 16% |
| 7 | Bonus rule and twist: next few days, they look at your two windows and wave once, keep your hands still, "not waving at you" | 4:53–5:08 | 15 | 5% |
| 8 | Glitch sting and "END OF FILE 017" card | 5:08–5:14 | 6 | 2% |

The five rules take 254 s (81%), about 36–66 s each. Each rule is longer than the one before it except rule 2 (the lull), and rule 4 (the face-to-face beat) is the longest.

### Hook

- **Hook line: 0:00–0:04, 12 words, about 4 s.** The title, verbatim, is the first line, with the rule ("only wave once") in red.
- **Full hook: 0:00–0:39, about 73 words in 39 s (12% of runtime).** It is a cold-open scene, not a rules preamble: short present-tense lines (2–9 words) build the anomaly image ("also", "same shirt", "same tilted head", "already raised", "all three of you"), then switch voice to the guide ("Lower yours"), then a "yet" sting, then the contract ("five rules").
- The threat is fully shown inside 13 s, but never explained.
- Slow pace (about 112 wpm in the hook vs about 147 overall): the gaps between short lines are the tension.

### Re-hooks

Something new (an instruction twist, threat sign, consequence, branch, rule card or sting) lands at:

0:04, 0:08, 0:10, 0:13, 0:17, 0:23, 0:26, 0:30, 0:32, 0:35, 0:39, 0:42, 0:47, 0:50, 0:56, 0:58, 1:04, 1:08, 1:14, 1:17, 1:28, 1:41, 1:44, 1:48, 1:51, 1:56, 1:58, 2:04, 2:12, 2:21, 2:27, 2:36, 2:45, 2:47, 2:52, 2:57, 3:00, 3:04, 3:10, 3:17, 3:19, 3:33, 3:35, 3:38, 3:44, 3:48, 3:51, 3:55, 4:03, 4:06, 4:13, 4:16, 4:20, 4:29, 4:40, 4:42, 4:46, 4:53, 4:55, 4:59, 5:04, 5:06

- **All re-hooks: 62 in 308 s, mean about 5.0 s, median about 3–4 s.** Every line is a new instruction, so the format re-hooks by default.
- **Threat re-hooks only** (a new sign the thing is present or a consequence, not just a new rule): 0:10, 0:17, 0:32, 1:14, 1:48, 1:56, 2:45, 2:52, 3:00, 3:17, 3:35, 3:51, 4:03 (glitch), 4:13, 4:20, 4:40, 4:46, 5:03, 5:06. **Mean interval about 16 s; the longest gaps are 0:32 to 1:14 (42 s, all of rule 1) and 1:56 to 2:45 (49 s, the phone set-up).** Those stretches run on procedure, rule cards and the "normal" lull, not on threat. This is a slower threat cadence than any short in the corpus and it still holds a 17x outlier, because the cold open front-loads the image and the calm procedure is itself the texture.
- **Biggest gap between any re-hooks: 3:19 to 3:33 (14 s)**, the "normal neighbour might sound confused / offended / apologise tomorrow" run. It is a deliberate baseline-setting lull right before the tell phrase.
- **Rule cards** at 0:39, 1:28, 2:04, 2:57, 4:03, plus the bonus card at 4:53: about every 36–66 s. The top tracker keeps the viewer's place.
- **Picture cadence:** a new pictogram or overlay change about every 3–5 s; the overlays (ticks, crosses, sight lines, bubbles) change more often than the base art.

### Open loops

| Loop | Opens | Development | Closes? |
|---|---|---|---|
| L1 What is the second figure, and which window is the real neighbour? | 0:10 | "Work out which window was the right one" 1:17; "don't stare long enough to compare them" 1:58; "which one?" 2:45 | Open; deliberately never answered |
| L2 What counts as doing something wrong? | 0:32 ("yet") | Every rule is a way to go wrong | Partly closed by the rules themselves |
| L3 What happens if you close the curtains? | 1:48 ("prompt a visit") | The visit comes anyway at 3:00 | Closed by the knock (rule 4) |
| L4 Who is asking "which one?" | 2:45 | "Even if... it was a joke" 2:52 | Open |
| L5 Is the person at the door your neighbour? | 3:00 | Normal baseline 3:22–3:29, tell phrase 3:35 | Conditional: you can tell by the phrase |
| L6 Did it leave? What came through the letterbox? | 3:48–3:51 | "Don't wait beside the door" 3:55 | Open |
| L7 What is tapping on the glass? | 4:13 | "Sometimes it was the television" 4:20 | Open; the hedge means some times it wasn't |
| L8 What did the real neighbour experience? | 4:40 ("most... a few...") | "Unusually relieved to see you" 4:46 | Answered by the twist (they saw two of you) |
| L9 Is there now a second you? | 4:59–5:06 | (none) | Open; the case file ends here |

Only L3 closes cleanly and L5 conditionally. L8 is answered by the twist, which opens L9 as the final cliff.

### Escalation ladder

1. A wrong image at a distance (two windows, one person).
2. You must not acknowledge it twice (rule about your own body).
3. It watches the walk home (don't look up).
4. It can see into your home (curtains, the other one hasn't lowered its hand).
5. It contacts you remotely (a text: "which one?").
6. It lies and walks back the lie ("it was a joke").
7. It comes to the door with bait from your own life.
8. It reveals itself with a phrase that reframes your polite wave as an invitation (main peak, 3:35, 68%).
9. It lingers and probes (shoes, letterbox).
10. It is ambient at night (taps on the glass), and you are told to accept a cover story.
11. Morning normality, with hints many residents have been through this.
12. The inversion: it is now in your windows, and your neighbour is following the rules about you (final twist, 5:06, 98%).

Two peaks: "which one?" at 2:45 (53%) and the tell phrase at 3:35 (68%), then a long, quiet de-escalation (4:03–4:53) that sets up the late twist. The twist is quiet, not loud: one red caption line and a push-in on a window.

### How it ends

- **A quiet reversal, not a cliffhanger.** The bonus "one final thing" rule repeats the cold-open situation from the neighbour's side: they look at your kitchen, then your bedroom, and wave once. The protagonist is told not to wave back, and the last line says the wave is not for them.
- The opening rule is inverted (wave once becomes do not wave), and the anomaly moves from their house to yours. The viewer replays the whole video in their head.
- No spoken CTA and no "part 2". The anthology frame ("END OF FILE 017") is the series hook: there are other files.
- The emotional state at the end is cold unease: the procedure worked, and it didn't matter.

### Pacing stats

- About 141 wpm (full runtime), about 147 wpm over the spoken span with caption restorations. The hook runs slower (about 112 wpm).
- About 116 VTT lines; the average sentence is about 7 words. Punch lines of 5 words or fewer: 0:04, 0:06, 0:08, 0:13, 0:15, 0:23, 0:30, 0:39, 0:42, 0:58, 1:28, 1:56, 2:21, 2:47, 2:57, 3:44, 4:20, 4:44, 4:53, 5:04. About one every 15 s, clustered at the open and at each rule card.
- About 70% of sentences are second-person instructions or permissions. 16 uses of "if" (if/then branches). "Normal / normally / ordinary / usual / usually" appears 9 times as the safety motif. About 20 frequency or modal hedges ("usually", "probably", "may", "might", "should", "tends to", "most", "a few", "sometimes").
- No dialogue except short scripted lines for you to say and the one tell phrase from the visitor.

### Visual notes

- **One base drawing does most of the work.** A white line-art house elevation (two storeys, four windows, a door) on near-black, reused in about half the frames with different overlays. Other sets: phone chat mock-up, front door, circular peephole vignette, fridge, curtains framing the view from the kitchen, sofa with clock and TV, a top-down path map, icon boxes.
- **Overlays carry the meaning:** dashed yellow sight lines from the protagonist to windows, yellow ticks for allowed actions, red crosses and red prohibition circles for forbidden ones, a tally counter ("GREETINGS GIVEN 1/1" with a red "SUFFICIENT" stamp), checklists that tick themselves, small mono-type status labels.
- **Rule tracker** at the top of the frame: five boxes; the current one is lit, finished ones become red crossed boxes. It works as a chapter marker and progress bar.
- **Caption colour code:** white for narration, red for warnings and consequences ("ONLY WAVE ONCE.", "CLOSING THEM SUDDENLY TENDS TO PROMPT A VISIT.", "THEY MAY NOT BE WAVING AT YOU."), yellow for safe actions ("LOWER YOURS.", "THAT IS ENOUGH.", "ONCE.", "KEEP YOUR HANDS WHERE THEY ARE.").
- **Only two loud effects:** RGB-split glitches at about 4:03 (before rule 5) and at about 5:10 (after the twist), plus a slight flicker on the peephole entry. The restraint makes them land.
- **Black title cards** for "There is one final thing", "DAY 1", "DAY 2" and "END OF FILE 017" (typewriter text).
- **Code-only fit: very high, the best in the corpus.** Everything is vector line art, icons, text and simple motion (push-ins, draw-ons, tick animations). A Remotion kit of a house elevation component, a stick figure with 3–4 poses, sight-line arrows, tick/cross/stamp overlays, a rule tracker, a phone chat component and a glitch filter would rebuild the whole look.

## 3. Transferable skeleton (no original wording)

Use this for a 4:30–5:30 YouTube 16:9 "official guidance" horror episode, at 140–150 wpm, about 650–780 words, 5 numbered rules plus a bonus rule. The narrator is a calm, impersonal guidance voice; the protagonist is "you", a silent pictogram on screen.

1. **Cold open, 0–12% (60–80 words, 35–40 s):**
   - Line 1 is the title: an if/then rule about a small, everyday anomaly, with the core rule in red. About 4 s.
   - Then a present-tense micro-scene in 2–9 word lines: an ordinary act you do, then the turn ("then you notice..."), then the impossible detail stated flatly, then 2–3 "same..." fragments that rule out a normal explanation, then one detail showing it was waiting for you.
   - Hold a short tableau that counts you in with the anomaly.
   - The voice becomes the guide: a 2-word safe action in yellow, then a reassurance with a one-word sting (not wrong *yet*).
   - The contract: the number of rules, and a tracker appears.
2. **Rule 1, the trigger moment, 12–28%:**
   - Restate the core rule. Pre-empt the viewer's question with "it doesn't matter which...".
   - Forbid the natural correction and the polite micro-gesture.
   - A bureaucratic closure (a counter or a stamp: "that's enough").
   - Movement home at a "normal" pace, two mundane-mishap branches, and one prohibition on looking back. Name the viewer's own question and defer it ("for now").
3. **Rule 2, the lull indoors, 28–39%:**
   - 3–4 hyper-specific chores given as rules, with a hidden rationale (something ordinary to finish).
   - The threat re-enters through a sight line from the safe room. Forbid the obvious defence and give a hedged consequence that plants the next beat ("tends to...").
   - A normal-state test ("it should have...") and a 5-word sting that the other one hasn't.
   - Forbid comparing; dismiss curiosity.
4. **Rule 3, remote contact, 39–56%:**
   - It contacts you through a modern channel. "Usually normal", with a triplet of mundane examples.
   - Scripted literal answers, a forbidden topic, waiting and a typing indicator, a mundane release.
   - Peak 1 at about 50–55%: "but if" the message asks the question the viewer has been asking. A physical counter-action (cut contact) and a pre-empted manipulation (a walk-back).
5. **Rule 4, the visit, 56–77% (the longest rule):**
   - The planted consequence arrives at the door. A dry aside keeps the voice calm.
   - The visual baseline ("normal distance, same clothes"), bait from your own life (2 specific items), and a polite refusal script.
   - Baseline-setting lull: 3 lines of how a real person would react, plus a permission to apologise later (10–15 s, deliberately flat).
   - "What you're listening for is..." then the tell phrase, which reframes your innocent act from the cold open as an invitation. **Main peak at about 65–70%.**
   - A one-time counter-phrase ("say it once"), step away, two sound-only aftermath details (one with an absence), and a prohibition on waiting for confirmation. Return to the chore.
6. **Rule 5, the evening ends "normally", 77–93%:**
   - A glitch sting before the card. Negative permissions (no vigilance), a chore triplet.
   - An ambient sound threat with a displacement action, a second-instance branch, and a comfort hedge ("sometimes it was...") plus permission to believe it.
   - The time jump to morning: "should be" empty, the neighbour doing something mundane, permission to ask.
   - Frequency hedges about other residents ("most will say..., a few will say...") and one line that hints the neighbour had a mirror experience.
7. **Bonus rule and inversion, 93–98%:**
   - A black "one final thing" card. Extend the time span (the next few days).
   - Replay the cold-open situation from the other side, so the anomaly is now in your home.
   - Tighten the core rule (from once to never) in yellow, then a last line in red that says the gesture isn't meant for you.
8. **Sting and file card, 98–100%:** a glitch, then a numbered case-file end card. No spoken CTA.

**Devices to reuse:**
- Title rule as the first line, then a cold-open scene before any rules.
- Impossible detail stated flatly, then "same..." fragments.
- A one-word sting on reassurance ("yet").
- A numbered contract and an on-screen rule tracker.
- Rules pinned to an ordinary timeline (arrival, chores, message, knock, evening, morning, next days).
- Hyper-specific chores as survival steps; "normal" as a repeated safety word.
- Forbidding the polite or natural move.
- Hedged consequences that plant later beats ("tends to...").
- Scripted literal answers and counter-phrases said once.
- A normal-versus-wrong baseline before a tell phrase.
- Sound-only aftermath with an absence.
- Frequency hedges that imply many past cases.
- Permission to accept a comforting explanation.
- A bonus rule that inverts the opening and moves the anomaly to you.
- Caption colour code: red for warnings, yellow for safe actions.
- Two glitch stings only, case-file numbering as the series hook.

**Pacing targets:**
- 140–150 wpm, with the cold open slower (110–120 wpm) and built from 2–9 word lines.
- A new instruction every 3–5 s; a rule card every 35–65 s; a threat sign at least every 20 s outside rule 1. Keep the longest threat-free run under 50 s and fill it with procedure and overlays.
- A new overlay or pictogram change every 3–5 s.
- Peaks at about 50–55% (remote contact) and 65–70% (the tell), a calm 15–20% de-escalation, then a quiet twist in the last 5%.
