"""Narration for explainer-never-meet-orca: the single source for script.md section 3, the TTS
duration check and storyboard.json (gen_storyboard.py). One entry per voiced line.

Fields: id, section, text (spoken = burned-in captions), on-screen text (or ''), pause after (s).
Sections marked SLOW are voiced at ~150 wpm (hook and the last ~30 s), the rest at ~165 wpm.
"""

SECTIONS = [
    # key, heading, slow
    ("L1", "L1 HOOK", True),
    ("L2", "L2 REFRAME + MASTER QUESTION + CREDENTIALS", False),
    ("L3", "L3 PROMISE", False),
    ("R1", "L4 TAB 1 BODY", False),
    ("R2", "L5 TAB 2 SPEED", False),
    ("R3", "L5 TAB 3 PLAN", False),
    ("R4", "L5 TAB 4 WAVE", False),
    ("R5", "L5 TAB 5 SHARKS", False),
    ("R6", "L5 TAB 6 GIANTS", False),
    ("PR", "L5 PROOF: COULD VS HAS", False),
    ("CL", "L6 CLIMAX: FOUR MOVES", False),
    ("TW", "L7 TWIST: THEY CHECKED", False),
    ("VS", "L7 VILLAIN SWAP", False),
    ("BE", "L8 BOOKEND", True),
    ("CTA", "L9 CTA", True),
]

LINES = [
    # ---------------------------------------------------------------- L1 hook (73 words)
    ("h01", "L1", "You're in a sea kayak on cold, glassy water.", "", 0.25),
    ("h02", "L1", "The sea is flat and your life jacket is zipped.", "SEA: FLAT ✓ · LIFE JACKET: ON ✓", 0.25),
    ("h03", "L1", "And the one animal out here with killer in its name has never killed anyone in the wild.", "WILD HUMAN KILLS: 0", 0.45),
    ("h04", "L1", "Then, through the thin plastic under your legs, you hear squeaks and creaks, like a rusty gate trying to sing.", "", 0.35),
    ("h05", "L1", "Then it all goes quiet.", "", 0.95),
    ("h06", "L1", "That quiet is a pod of orcas, deciding something about you.", "THEY'RE DECIDING SOMETHING", 0.5),
    # ---------------------------------------------------------------- L2 reframe, master question, credentials
    ("r01", "L2", "Sharks bite around sixty to seventy people a year, unprovoked. The orca, the one called killer, sits on zero.", "SHARKS: ~60-70 BITES / YR · ORCA: 0", 0.35),
    ("r02", "L2", "So why has an animal built for killing never picked you?", "WHY HAS IT NEVER PICKED YOU?", 0.85),
    ("r03", "L2", "It's not that it can't. It surfs onto beaches for sea lions, leaves great whites washed up without their livers, and has taken down the largest animal that ever lived.",
     "1 BEACH RAIDS · 2 GREAT WHITES, NO LIVERS · 3 THE LARGEST ANIMAL EVER", 0.35),
    # ---------------------------------------------------------------- L3 promise
    ("p01", "L3", "So let's open its threat file, one tab at a time.", "THREAT FILE: ORCA [1 BODY] [2 SPEED] [3 PLAN] [4 WAVE] [5 SHARKS] [6 GIANTS]", 0.3),
    # ---------------------------------------------------------------- R1 body
    ("b01", "R1", "Tab one, the body. A big male runs about eight metres long and weighs around six tonnes.", "~8 M · ~6 TONNES", 0.25),
    ("b02", "R1", "That's nearly two family cars nose to tail, as heavy as four of them.", "≈ 2 CARS LONG · ≈ 4 CARS HEAVY", 0.3),
    ("b03", "R1", "His dorsal fin alone can stand about as tall as you.", "FIN: ~1.8 M · YOU: ~1.75 M", 0.3),
    ("b04", "R1", "Inside the mouth sit up to fifty-six cone-shaped teeth, the biggest around ten centimetres, longer than your credit card.", "40-56 TEETH · UP TO ~10 CM", 0.25),
    ("b05", "R1", "They interlock when the jaw closes and aren't made for chewing, so you'd be held, torn and swallowed in chunks.", "HOLD · TEAR · SWALLOW", 0.35),
    ("b06", "R1", "It isn't even a whale. It's the biggest dolphin there is, and there's also a false killer whale and a pygmy one, so somebody was nervous.", "NOT A WHALE. A DOLPHIN. · ALSO REAL: FALSE KILLER WHALE · PYGMY KILLER WHALE", 0.25),
    # ---------------------------------------------------------------- R2 speed
    ("s01", "R2", "So could you outswim one? No.", "COULD YOU OUTSWIM IT?  NO.", 0.25),
    ("s02", "R2", "In a sprint an orca hits about fifty-six kilometres an hour, the speed you'd drive through town.", "ORCA: ~56 KM/H = YOUR CAR IN TOWN", 0.25),
    ("s03", "R2", "The fastest human swimmers manage about eight. You, in a borrowed wetsuit, maybe three.", "OLYMPIC SWIMMER: ~8 · YOU: ~3", 0.3),
    ("s04", "R2", "All that speed burns fuel, and a big adult can eat up to about a hundred and thirty kilos on a big day, more than you weigh.", "UP TO ~130 KG / DAY > YOU", 0.3),
    ("s05", "R2", "So you'd be a perfectly sized meal. It's just never ordered one.", "ORDERS PLACED: 0", 0.45),
    # ---------------------------------------------------------------- R3 plan
    ("pl01", "R3", "But speed isn't what makes it dangerous. It plans.", "IT PLANS.", 0.3),
    ("pl02", "R3", "Orcas live in family pods led by older females, and in the North Pacific some eat only fish while others eat only mammals.", "PODS · LED BY GRANDMOTHERS", 0.25),
    ("pl04", "R3", "The fish eaters chatter all day, since salmon barely hear them. Mammal hunters can't, because seals hear orca calls well, so these pods hunt in near silence, by listening.", "FISH EATERS: NOISY · MAMMAL HUNTERS: SILENT, HUNT BY EAR", 0.25),
    ("pl06", "R3", "Underwater microphones show most of their calling starts after the kill.", "CALLS: AFTER THE KILL", 0.3),
    ("pl07", "R3", "Remember the squeaking through your kayak, and then the silence?", "", 0.35),
    ("pl08", "R3", "Noisy is an orca off duty. Quiet is an orca at work.", "QUIET = WORKING", 0.4),
    ("pl09", "R3", "And the planning gets taught. In Argentina, orcas surf up the beach to grab young sea lions, then slide back on the next wave.", "ARGENTINA · BEACH RAIDS", 0.25),
    ("pl10", "R3", "On the Crozet Islands, mothers have been seen pushing calves up the sand, and calves rehearse on empty beaches.", "CROZET ISLANDS · BEACH SCHOOL", 0.45),
    # ---------------------------------------------------------------- R4 wave
    ("w01", "R4", "In Antarctica, a seal can escape all that by hauling out onto floating ice. Smart.", "ANTARCTICA · SAFE ON ICE?", 0.25),
    ("w02", "R4", "Except a pod swims up, lifts their heads out of the water, and takes a look first.", "THEY CHECK FIRST", 0.25),
    ("w03", "R4", "Scientists noticed they kept choosing Weddell seals, even where others were easier to find.", "PREFERRED: WEDDELL SEAL", 0.25),
    ("w04", "R4", "Then the pod backs off, lines up, and charges together. At the last second they dive, and their wave rolls over the floe and tips the seal in.", "WAVE-WASHING", 0.2),
    ("w06", "R4", "If it fails, they go again. A seal on an ice floe isn't safe. It's served.", "ATTEMPT 2... 3...  NOT SAFE. SERVED.", 0.4),
    ("w07", "R4", "Now picture your kayak again: a small flat thing on the water, with something warm on top. Look familiar?", "LOOK FAMILIAR?", 0.45),
    # ---------------------------------------------------------------- R5 sharks
    ("k01", "R5", "Which brings us back to those sharks.", "", 0.2),
    ("k02", "R5", "In one week in May 2017, three great whites washed up near Gansbaai, South Africa.", "GANSBAAI · MAY 2017 · 3 IN ONE WEEK", 0.25),
    ("k03", "R5", "Each had wounds near the front fins and no liver, and at least one had lost its heart too.", "LIVER: GONE · HEART: GONE (AT LEAST 1)", 0.25),
    ("k04", "R5", "The suspects were two local males, Port and Starboard, named for their floppy dorsal fins.", "SUSPECTS: PORT & STARBOARD", 0.25),
    ("k05", "R5", "Why the liver? In a great white it can be a quarter of the body, and it's full of oil.", "LIVER ≈ 1/4 OF THE BODY · OIL", 0.25),
    ("k06", "R5", "Think of it as the shark's fuel tank. The orcas take the tank and leave the car.", "TAKE THE TANK. LEAVE THE CAR.", 0.3),
    ("k07", "R5", "Scientists suspect they flip sharks into a trance called tonic immobility, though that is still unconfirmed.", "TONIC IMMOBILITY? (UNCONFIRMED)", 0.3),
    ("k08", "R5", "What is on film is Starboard, in 2023, killing a young great white alone in under two minutes, less time than you spend brushing your teeth.", "2023 · ONE ORCA · < 2 MIN", 0.3),
    ("k09", "R5", "And the sharks? They left, for months at a time, so a cage dive there could mean you staring at empty water all day.", "GREAT WHITES: GONE", 0.25),
    ("k11", "R5", "Imagine being the most feared fish in the ocean and moving house because of a dolphin.", "MOVING HOUSE", 0.45),
    # ---------------------------------------------------------------- R6 giants
    ("g01", "R6", "Think being huge would save you?", "", 0.2),
    ("g02", "R6", "In March 2019, off Bremer Bay in Western Australia, more than a dozen orcas brought down an adult blue whale around twenty metres long.", "BREMER BAY · MARCH 2019 · ~20 M", 0.25),
    ("g03", "R6", "Line up eleven of you head to toe and you'd only just match it.", "≈ 11 OF YOU", 0.25),
    ("g04", "R6", "They took turns biting its fins and flanks and pushing it under until it gave out.", "BITE · RAM · PUSH UNDER", 0.25),
    ("g05", "R6", "It was the first ever documented, and it has happened twice more since, both to young whales.", "2019 · 2019 · 2021", 0.3),
    ("g06", "R6", "So size doesn't stop it, and nothing in the sea hunts it back. Which makes your seventy-odd kilos a strange exception.", "NO UPPER LIMIT · NO NATURAL PREDATOR → SO WHY NOT YOU?", 0.45),
    # ---------------------------------------------------------------- proof
    ("pr01", "PR", "So has an orca ever turned any of this on a person?", "HAS IT EVER TRIED IT ON A HUMAN?", 0.3),
    ("pr02", "PR", "A handful of bites and bumps are on record, and no deaths. The closest call is in an explorer's diary.", "BITES & BUMPS: A HANDFUL · DEATHS: 0", 0.3),
    ("pr03", "PR", "In January 1911, on Scott's Antarctic expedition, photographer Herbert Ponting walked onto the sea ice to photograph a pod.", "ANTARCTICA · JANUARY 1911", 0.25),
    ("pr04", "PR", "Seconds later the ice under him heaved and split, broken from below, the same idea as the floe trick.", "THE ICE CRACKS", 0.25),
    ("pr05", "PR", "Ponting leapt slab to slab and made it back, off ice thick enough to hold sled dogs. You'd have a few millimetres of plastic.", "HE MADE IT · HIS ICE vs YOUR HULL", 0.25),
    ("pr07", "PR", "Were they after him, his dogs, or a dark shape on the ice? Nobody knows.", "HIM? THE DOGS? A SHAPE?", 0.3),
    ("pr08", "PR", "Could it? Clearly. Has it? Wild orcas, human deaths: zero.", "COULD: YES · HAS: 0", 0.45),
    # ---------------------------------------------------------------- climax
    ("c01", "CL", "Still, run the thought experiment. A pod has picked you, and you get four moves.", "YOUR FOUR MOVES: 1 SWIM · 2 CLIMB · 3 DIVE · 4 PLAY DEAD", 0.3),
    ("c02", "CL", "One, swim for it: fifty-six against your three. That's not a race, it's a delivery.", "", 0.3),
    ("c03", "CL", "Two, climb onto something, a rock, a buoy, your flipped kayak. You've seen what they do to things on top of the water. Up there, you're the seal.", "", 0.3),
    ("c04", "CL", "Three, dive and hide. Remember, they hunt by listening, and you kicking down on burning lungs are exactly the noise they want.", "THEY HUNT BY EAR", 0.3),
    ("c05", "CL", "Four, play dead. If the theory is right, that's roughly what a flipped great white does. Ask its liver how that went.", "ASK THE LIVER", 0.35),
    ("c06", "CL", "Four moves, four losses. Once a pod picks you, the outcome is not up to you.", "ONCE IT PICKS YOU, IT'S NOT YOUR CALL.", 0.85),
    # ---------------------------------------------------------------- twist
    ("t01", "TW", "And yet no wild pod has ever made that pick.", "AND YET: 0", 0.3),
    ("t03", "TW", "Off Spain and Portugal since 2020, some pods have rammed sailboats and snapped off their rudders, and a few boats sank.", "IBERIA · SINCE 2020 · RUDDERS", 0.25),
    ("t04", "TW", "Even then they swim off once the rudder's gone, and nobody aboard has been seriously hurt.", "BOATS SUNK: A FEW · PEOPLE HURT: 0", 0.3),
    ("t05", "TW", "You're slow, soft, and floating in their kitchen, and still they swim past.", "", 0.35),
    ("t06", "TW", "So why? Nobody knows for certain, but two things help.", "WHY? (NOBODY KNOWS FOR SURE)", 0.25),
    ("t07", "TW", "Shark bites on people are often thought to be mistakes, because from below, you on a board look a lot like a seal.", "SHARKS: MISTAKEN IDENTITY?", 0.25),
    ("t08", "TW", "Orcas don't work that way. Remember, they check first, looking and listening, so that mistake is much harder to make.", "THEY CHECK FIRST", 0.25),
    ("t09", "TW", "And what they check has to be on the family menu, because an orca eats what its grandmother taught its mother to eat.", "CULTURE", 0.25),
    ("t10", "TW", "Fish-eating pods off Canada swim past seals without a second look, and mammal hunters learn which mammals count, like those Weddell-choosing pods.", "FISH EATERS IGNORE SEALS", 0.25),
    ("t11", "TW", "In all those generations of handed-down menus, you have never made the list.", "MENU: SALMON · HERRING · SEAL · SHARK LIVER · YOU (never)", 0.3),
    ("t12", "TW", "So the quiet under your kayak was a check, silent while they look and chatty once they've decided.", "QUIET WHILE CHECKING · NOISY ONCE DONE", 0.25),
    ("t13", "TW", "They checked, and you weren't food.", "THEY CHECKED. YOU WEREN'T FOOD.", 0.55),
    # ---------------------------------------------------------------- villain swap (jokes retired from here)
    ("v01", "VS", "Which leaves three words from the start: in the wild.", "\"IN THE WILD\"", 0.3),
    ("v02", "VS", "Every human death ever linked to an orca happened in a marine park, with animals taken from the sea or born in tanks. There have been four.", "HUMAN DEATHS: 4 · ALL IN CAPTIVITY", 0.35),
    ("v03", "VS", "Out in the open, the harm mostly flows from people like you and me to them.", "US → THEM", 0.3),
    ("v04", "VS", "In the 1960s and 70s, dozens of orcas were caught or killed around Puget Sound for aquarium shows.", "1960s-70s · DOZENS TAKEN", 0.25),
    ("v05", "VS", "The Southern Residents who live there today number about seventy-five, down from ninety-eight in 1995, roughly one school bus full.", "1995: ~98 → TODAY: ~75 ≈ 1 SCHOOL BUS", 0.25),
    ("v06", "VS", "Their salmon is vanishing, ship noise drowns out the clicks they hunt it with, and their blubber holds some of the highest chemical loads of any marine mammal.", "SALMON ↓ · SHIP NOISE · CHEMICALS", 0.3),
    ("v07", "VS", "Nothing in the sea hunts the orca. The closest thing it has to a predator is us.", "NO NATURAL PREDATOR. EXCEPT US.", 0.65),
    # ---------------------------------------------------------------- bookend (slow)
    ("e01", "BE", "Back to your kayak. The water's glassy, the inlet's cold.", "", 0.3),
    ("e02", "BE", "The squeaking starts up again, louder, and the pod slides by close enough to hear them breathe.", "", 0.35),
    ("e03", "BE", "The rule you paddled out with still holds. In the wild, zero.", "WILD HUMAN KILLS: 0", 0.3),
    ("e04", "BE", "But the animal passing you outsizes you, outruns you, plans ahead, washes seals off ice, empties great whites and brings down blue whales.", "FILE: 6 TABS STAMPED", 0.3),
    ("e05", "BE", "And it just looked you over, then kept swimming.", "", 0.5),
    ("e06", "BE", "Orcas could hunt you. They decided not to.", "THEY DECIDED NOT TO.", 0.5),
    ("e07", "BE", "And the only thing keeping you off that menu is a habit, in an animal that keeps picking up new ones.", "YOU'RE SAFE BECAUSE OF A HABIT.", 0.75),
    # ---------------------------------------------------------------- CTA
    ("x01", "CTA", "Next file: leopard seal or box jellyfish? Pick one in the comments.", "NEXT FILE: LEOPARD SEAL or BOX JELLYFISH?", 0.0),
]
