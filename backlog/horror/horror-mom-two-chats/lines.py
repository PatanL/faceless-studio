"""Single source of the spoken lines for horror-mom-two-chats (final, single ~3 min cut).

Used by tts_measure.py (Kokoro on the Spark CPU), build.py (timeline, stats, storyboard.json) and,
through build.py's printed tables, script.md.

Entry kinds
  ("#", beat_key, heading)                         section marker
  (id, spk, text, opts)                            a spoken line; text is what Kokoro says (spoken form);
                                                   opts: gap (s after), cap (caption overrides {word: shown},
                                                   "" folds the word into the previous caption word), sfx
                                                   [(cue, offset, gain_db)] where offset is seconds from the line
                                                   start, "end", "end+0.3" or "w:<word>", screen (on-screen text)
  ("~", id, seconds, opts)                         timed silence (picture keeps moving, SFX only, no VO)

Voice convention: each account / person has one voice. The narrator is Nora. Both "Mom" chats are the same
voice (af_nicole) because they are the same contact; the private chat is read slower and colder. Dad's
family-chat bubbles land SILENT on screen (TEXT-FIGURE bubble rhythm), so the first time we hear Dad's voice
is the hotel landline. The real Mom (af_sky) only speaks after the rescue. The last bubble from the private
"Mom" thread is read in DAD's landline voice: the voice swap.
"""

# speaker -> Kokoro voice, speed (all voices below are cached on the Spark; no downloads)
VOICES = {
    "N": ("af_heart", 1.30),    # Nora, 17, narrator
    "M": ("af_nicole", 1.15),   # "Mom" in the Family group chat (warm, pleading)
    "P": ("af_nicole", 1.02),   # "Mom" in the private 1:1 chat (same contact, calm, colder)
    "D": ("am_michael", 1.12),  # Dad on the hotel landline (Lakeview Suites, Room 412)
    "R": ("af_sky", 1.18),      # the real Mom, in person, after the rescue
    "X": ("am_michael", 1.00),  # the private "Mom" thread's last bubble, in Dad's landline voice
}
SPEAKER_NAME = {"N": "Nora (narrator)", "M": "Family chat \"Mom\"", "P": "Private chat \"Mom\"", "D": "Dad (hotel landline)",
                "R": "Mom (in person)", "X": "Private chat \"Mom\", in Dad's voice"}

GAP = 0.2         # breath between lines, same speaker
TURN_GAP = 0.3    # speaker change

V = [
    ("#", "B1", "B1 HOOK: two texts from Mom, nine seconds apart"),
    ("n1", "N", "Mom texted:",
     {"gap": 0.12, "sfx": [("notify", -0.05, -4)],
      "screen": "FRAME 0 = COVER. Lock screen 11:40, two banners already stacked and fully readable: \"Family · Mom: I'm outside. Unlock the door.\" over \"Mom: Don't open it. I'm still at work.\" Behind the phone, sharp: our front door, the red EXIT-sign strip under it broken by two feet"}),
    ("f1", "M", "I'm outside. Unlock the door.",
     {"screen": "Punch-in on banner 1 (Family · Mom)"}),
    ("n2", "N", "Nine seconds later:",
     {"gap": 0.12, "sfx": [("notify", 0.0, -2)], "screen": "Punch-in on banner 2 (Mom, the private thread), timestamps 11:40 / 11:40"}),
    ("p1", "P", "Don't open it. I'm still at work.",
     {"sfx": [("glitch", "w:still", -10)], "screen": "Banner 2 held, red edge pulse"}),
    ("n3", "N", "And one of them was right outside our door.",
     {"sfx": [("whoosh", 0.0, -6), ("drone", 0.2, -10)],
      "screen": "Whip to the front door from inside: hall side dark, only the red EXIT glow under the door, two feet breaking it"}),

    ("#", "B2", "B2 RULE: the fridge note (plants: the key loophole, Room 412)"),
    ("n4", "N", "Mom's rule is on our fridge. After ten, the door stays locked. Even for her. She has her own key.",
     {"sfx": [("click", 0.1, -8)],
      "screen": "Yellow sticky note on the fridge: \"AFTER 10 THE DOOR STAYS LOCKED. EVEN FOR ME. I HAVE MY KEY. —M\"; smaller second line in Dad's hand: \"Dad: Lakeview Suites, Rm 412 (back Sun)\". \"EVEN FOR ME\" underlines itself in red"}),

    ("#", "B3", "B3 PRESSURE: the warm Mom, the rule as a test, the near-open"),
    ("f2", "M", "Hands full, honey. Phone's on three percent. Please.",
     {"cap": {"three": "3%.", "percent.": ""}, "sfx": [("typing", -0.5, -10), ("message_pop", 0.0, -2)],
      "screen": "Family thread (Mom, Dad, Nora). Mom: \"hands full honey\" / \"phone's on 3%\" / \"please\""}),
    ("n5", "N", "So I sent her the rule. Use your key.",
     {"sfx": [("message_send", "w:Use", -2)], "screen": "Me (blue): \"Rule. Use your key.\""}),
    ("f3", "M", "Forgot them this morning. Check the hook.",
     {"sfx": [("message_pop", 0.0, -2)], "screen": "Mom: \"forgot them this morning\" / \"check the hook\""}),
    ("n6", "N", "Her keys were on the hook, on the red hospital lanyard. My hand went to the deadbolt.",
     {"sfx": [("tick", 0.6, -6), ("heartbeat_slow", "w:hand", -6)],
      "screen": "Key hook by the door: Mom's key ring on a plain red lanyard. Then the deadbolt thumb-turn, close; Nora's hand reaching in (near-open)"}),

    ("#", "B4", "B4 COUNTER-VOICE: the private Mom sees the lock, then lies"),
    ("p2", "P", "Don't touch that lock.",
     {"sfx": [("phone_buzz", -0.15, -2)],
      "screen": "Buzz. Private thread \"Mom\": \"Don't touch that lock.\" arrives with NO typing dots"}),
    ("n7", "N", "How did she know? I typed, your keys are right here.",
     {"sfx": [("message_send", "end", -2)], "screen": "Me: \"ur keys are right here on the hook??\""}),
    ("p3", "P", "No they're not. They're in my pocket.",
     {"sfx": [("message_pop", 0.0, 0)], "screen": "Instant, no dots: \"No they're not.\" / \"They're in my pocket.\""}),
    ("n8", "N", "No typing dots. One second. And I was staring at her keys.",
     {"screen": "Punch-in on the empty space where typing dots should be; cut to the keys on the hook"}),

    ("#", "S4", "S4 TEST: the code word (micro loop)"),
    ("n9", "N", "So I asked both of them for our code word. Mom and I picked it at the kitchen table. We never typed it anywhere.",
     {"sfx": [("message_send", "w:asked", -4), ("message_send", "w:both", -4)],
      "screen": "Me, in both threads: \"what's our word?\" (two whips). Nora close-up on \"kitchen table\""}),
    ("f4", "M", "Nora, I'm not doing this in the hallway. Open up.",
     {"sfx": [("message_pop", 0.0, -2)], "screen": "Family · Mom: \"Nora I'm not doing this in the hallway\" / \"open up\""}),
    ("p4", "P", "Marigold. Now put the chain on.",
     {"sfx": [("message_pop", 0.0, 0)], "screen": "Private · Mom: \"Marigold.\" / \"Now put the chain on.\""}),
    ("n10", "N", "Only Mom knew that. I slid the chain on.",
     {"sfx": [("click", "w:chain", 0)], "screen": "Insert: the door chain sliding into its track"}),

    ("#", "B5a", "B5 RUNG: the doorbell, the peephole, the light that never clicks"),
    ("n11", "N", "Then the doorbell rang.",
     {"gap": 0.1, "sfx": [("ding", "w:doorbell", 0)], "screen": "Front door, shake on the bell"}),
    ("n12", "N", "Through the peephole, blue scrubs. Head down. Too close to the lens to see a face.",
     {"sfx": [("breath", 0.8, -10)],
      "screen": "Peephole POV: the corridor dark except the red EXIT sign; a blue-scrubs shoulder and a bowed head fill the bottom of the lens"}),
    ("n13", "N", "Our hall light is on a motion sensor. It clicks on for anyone, even the neighbor's cat. It never clicked on.",
     {"screen": "Hold the dark peephole; cut on \"never\" to the strip under the door: still only red"}),

    ("#", "B5b", "B5 TOP AUTHORITY: Dad, who never posts"),
    ("n14", "N", "Then Dad posted in the family chat. Dad never posts.",
     {"sfx": [("typing", "w:Dad#2", -10)], "screen": "Family thread: Dad's avatar (D, slate) with typing dots; his last message above it, from Sep 14: \"ok\""}),
    ("~", "q1", 2.6, {"sfx": [("message_pop", 0.1, -2), ("message_pop", 0.95, -2), ("message_pop", 1.8, -2)],
                      "screen": "SILENT bubbles (no VO), big punch-in: Dad: \"It's really her, kiddo.\" / \"I just talked to her.\" / \"Let your mother in.\""}),
    ("n15", "N", "Dad was in Columbus till Sunday. And he has never lied to me.",
     {"screen": "Nora close-up, worried. Behind her, out of focus: the hall closet door"}),

    ("#", "S7", "S7 PROXIMITY + TYPOGRAPHY LADDER (calm -> CAPS)"),
    ("f5", "M", "I can see your shadow under the door, Nora.",
     {"sfx": [("message_pop", 0.0, -2)],
      "screen": "Family · Mom: \"I can see your shadow under the door, Nora.\" Cut to floor level: Nora's shadow strip inside, the feet outside"}),
    ("n16", "N", "The handle tilted down. Slowly. Then up.",
     {"sfx": [("door_creak", 0.3, -10)], "screen": "Macro: the lever handle tilts down slowly, then back up"}),
    ("~", "q2", 1.5, {"sfx": [("phone_buzz", 0.0, 0), ("knock3", 0.25, 0)],
                      "screen": "SILENT CAPS bubble (red alert style), phone vibrates, door knocks: \"NORA. OPEN. THE DOOR.\""}),

    ("#", "B8", "B8 TURN: the voucher is in the house"),
    ("n17", "N", "I didn't text Dad back. I called him.",
     {"sfx": [("click", "end", -6)], "screen": "Outgoing call screen: \"Dad · mobile · calling…\" with one red End button"}),
    ("~", "q3", 1.0, {"sfx": [("phone_buzz", 0.1, -16)], "screen": "Ringback, faint, in the earpiece only"}),
    ("n18", "N", "Two rings and a pause. Dad's old desk-phone ringtone. Not in my ear. Behind me. In our hall closet.",
     {"sfx": [("desk_bell_ring", 0.0, -7)],
      "screen": "Nora's eyes go wide (no blink). On \"Behind me\": over-the-shoulder, past her back-view silhouette, to the hall closet door; phone glow pulses under it with each ring"}),
    ("~", "q4", 4.0, {"sfx": [("desk_bell_ring", 0.0, -2), ("heartbeat_fast", 0.4, -6)],
                      "screen": "SILENCE BEAT 4.0 s: two more full ring cycles from the closet, no VO, music out. The glow pulses, then goes dark"}),

    ("#", "B6", "B6 ISOLATION: only the enemy's channel answers"),
    ("n19", "N", "The ringing stopped. And in the family chat, Dad was typing.",
     {"sfx": [("typing", "w:Dad", -8)], "screen": "Family thread header: \"Dad is typing…\""}),
    ("~", "q5", 2.0, {"sfx": [("message_pop", 0.1, -2), ("message_pop", 1.0, -2)],
                      "screen": "SILENT calm bubbles: Dad: \"Don't turn around, kiddo.\" / \"Just open the front door.\""}),

    ("#", "B10", "B10 LIFELINE: the hotel landline, under a battery clock"),
    ("n20", "N", "I backed away from the closet and called the hotel number on the fridge. Room four twelve.",
     {"cap": {"four": "412.", "twelve.": ""}, "sfx": [("footsteps", 0.0, -12), ("phone_buzz", "end", -14)],
      "screen": "Walk-back: Nora toward camera, the closet behind her. Insert: the fridge note's \"Rm 412\" line. Outgoing call \"Lakeview Suites · Room 412\""}),
    ("d1", "D", "Hello? Nora? What's wrong, kiddo?",
     {"sfx": [("click", -0.25, -8)], "screen": "Call connects; timer starts 00:00"}),
    ("n21", "N", "His real voice. Half asleep. Where's your phone, Dad?",
     {"screen": "Nora close-up, phone to her ear, whispering"}),
    ("d2", "D", "My cell? It's in my winter coat. In the hall closet. I forgot it.",
     {"screen": "Call screen; cut on \"closet\" to the closet door, dark"}),
    ("n22", "N", "Then who's typing on it?", {"screen": "Nora close-up, scared"}),
    ("~", "q6", 0.8, {"screen": "Call timer runs; silence on the line"}),
    ("d3", "D", "Stay on the line. I'm having the front desk call your police.",
     {"screen": "Call screen, timer running"}),
    ("n23", "N", "Eight minutes, they said. My battery said two percent.",
     {"cap": {"Eight": "8", "two": "2%.", "percent.": ""}, "sfx": [("clock_ticking", 0.0, -14)],
      "screen": "Battery glyph in the status bar flips red: 2%; chip \"police · 8 min\""}),

    ("#", "B5c", "B5 BARRIER LADDER: hook, key, deadbolt, chain (rule spoken back)"),
    ("f6", "M", "Who are you whispering to, honey?",
     {"sfx": [("notify", -0.1, -2), ("knock", "end", -2)], "screen": "Banner over the call: \"Family · Mom: who are you whispering to, honey?\""}),
    ("n24", "N", "I looked at the hook. Empty. Nobody had come in. I'd been standing right here.",
     {"sfx": [("impact", "w:Empty", -12)], "screen": "Same framing as the key-hook insert: the hook is empty. Then Nora, looking around her own hallway"}),
    ("n25", "N", "Then a key slid into our lock, from outside.",
     {"sfx": [("key_scrape", 0.4, 0)], "screen": "Macro on the lock cylinder, the key sound only"}),
    ("n26", "N", "Even for her, the door stays locked. She has her own key.",
     {"screen": "Flash insert of the fridge note: \"I HAVE MY KEY\" turns red"}),
    ("n27", "N", "The deadbolt turned. The door slammed open against the chain. Three inches of black. Nothing came in.",
     {"sfx": [("click", "w:deadbolt", 0), ("impact", "w:slammed", 0), ("door_creak", "w:slammed", -8)],
      "screen": "The thumb-turn rotates by itself; the door jerks open to the chain; the gap is pure black; cold air drifts in; nothing is ever visible in the gap"}),

    ("#", "T3", "T3 RULE INVERSION: the helper's safe place is the threat"),
    ("p5", "P", "Get in the hall closet. Shut the door. Don't make a sound.",
     {"sfx": [("notify", -0.1, -2)], "screen": "Banners from the private \"Mom\": \"Get in the hall closet.\" / \"Shut the door.\" / \"Don't make a sound.\""}),
    ("n28", "N", "Mom says hide in the closet.", {"screen": "Nora whispering into the phone"}),
    ("d4", "D", "Nora, no. That's where my phone is. Whatever's typing is in there. Lock yourself in the bathroom.",
     {"screen": "Call screen; on \"in there\" a fast cut to the closet door"}),
    ("n29", "N", "I ran for the bathroom. Halfway there, my screen went black. Dead.",
     {"sfx": [("footsteps", 0.0, -8), ("static", "w:black", -10)],
      "screen": "Hall, running; the phone in her hand goes black (battery dead): the landline is gone"}),
    ("~", "q7", 1.2, {"sfx": [("drone", 0.0, -8)], "screen": "Dark hallway; her breath; the closet door beside her"}),

    ("#", "B9", "B9 PEAK: the closet opens itself (the one held image)"),
    ("n30", "N", "And the closet door swung open by itself.",
     {"sfx": [("door_creak", 0.4, -2)], "screen": "The hall closet door swings open on its own"}),
    ("n31", "N", "Dad's coat. Nobody in it. But the sleeve was still swinging.",
     {"screen": "Inside: coats on hangers; Dad's grey winter coat in the middle; its empty sleeve still swinging, slowing"}),
    ("n32", "N", "His phone was lit in the pocket, and it was typing.",
     {"sfx": [("typing", "end", -8)], "screen": "Push in on the coat pocket: a phone screen glowing through the fabric"}),
    ("~", "q8", 4.0, {"sfx": [("tick", 0.6, -10), ("tick", 1.4, -10), ("tick", 2.2, -10), ("tick", 3.0, -10)],
                      "screen": "THE scariest image, held ~4 s, no music: macro on the phone half out of the pocket, Family thread, draft field typing one letter at a time: \"turn around nora\""}),
    ("n33", "N", "It typed, turn around, Nora. I didn't.",
     {"screen": "Nora's face, eyes locked forward; behind her (out of focus) the front door, open to the chain, black gap"}),

    ("#", "B10b", "B10 RESCUE: the planted light decides"),
    ("n34", "N", "Then red and blue light slid under the front door. The gap eased shut by itself.",
     {"sfx": [("siren", 0.0, -4), ("click", "end", -6)],
      "screen": "Red/blue wash pulses under the door and across the wall; the black gap narrows to nothing; the latch clicks"}),
    ("n35", "N", "A man's voice. Police. Your dad called us.",
     {"sfx": [("knock3", 0.0, -2)], "screen": "Front door, three knocks, red/blue light"}),
    ("n36", "N", "Voices lie. So I watched the light under the door.",
     {"screen": "Floor level: the strip under the door, red/blue only"}),
    ("n37", "N", "Click. The hall light came on for them. It had never come on for her.",
     {"sfx": [("relay_click", 0.0, 0)], "screen": "On \"Click\" the strip turns warm white: the motion light. Peephole: two officers, lit"}),
    ("n38", "N", "So I broke Mom's rule. Chain off.",
     {"sfx": [("click", "w:Chain", 0)], "screen": "Insert: chain off"}),
    ("n39", "N", "Two officers. And Mom, running out of the elevator in her blue scrubs.",
     {"sfx": [("ding", "w:elevator", -6), ("footsteps", "w:running", -6)],
      "screen": "Elevator panel arrives at 6; the lit corridor, a figure running toward us"}),

    ("#", "B11", "B11 TRUTH TWIST after safety: it was worse than you knew"),
    ("r1", "R", "Baby, my phone died at nine. I never texted you.",
     {"screen": "Insert: Mom's hand holding her phone, black, dead; it reflects the hall light"}),
    ("n40", "N", "But the private chat knew Marigold.", {"screen": "Nora close-up, relief turning to fear"}),
    ("r2", "R", "Nobody knows Marigold. We only ever said it out loud, in our kitchen.",
     {"screen": "Slow push into our dark kitchen behind them, the fridge note just visible"}),
    ("n41", "N", "So whatever answered had been in our kitchen.",
     {"sfx": [("drone", 0.0, -8)], "screen": "Nora looking back into the apartment, terrified"}),

    ("#", "B12", "B12 VOICE SWAP + BOOKEND"),
    ("n42", "N", "Then my dead phone lit up. The private chat. Mom.",
     {"sfx": [("phone_buzz", "w:lit", 0)], "screen": "Her black phone wakes by itself: lock screen, banner \"Mom\" (same avatar as frame 0)"}),
    ("p6", "P", "Now I know whose voice you trust.",
     {"sfx": [("message_pop", 0.0, 0)],
      "screen": "Private thread: typing dots for the FIRST time (the tell breaks), then \"Now I know whose voice you trust.\""}),
    ("x1", "X", "Next time, I'll call from Room four twelve.",
     {"cap": {"four": "412.", "twelve.": ""}, "sfx": [("message_pop", 0.0, 0), ("stinger", "end+0.2", -2)],
      "screen": "Second bubble, read in DAD's landline voice: \"Next time, I'll call from Room 412.\" Bookend: phone over the front door, as in frame 0"}),
    ("~", "q9", 1.5, {"screen": "Hold on the bookend frame; hard cut to black. No CTA, no part card"}),
]


def spoken():
    return [e for e in V if e[0] not in ("#", "~")]
