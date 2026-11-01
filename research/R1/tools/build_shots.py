"""Expand hand-labelled shot ranges (from 5 s contact sheets) into per-5s CSVs with transcript text + motion. Run from research/R1 with python3 -I."""
import json, csv
def s(t):
    m, sec = t.split(':'); return int(m) * 60 + int(sec)
# CODE | what is on screen.  Labels were made by looking at every 5 s frame (2.5 s offset) on the contact sheets.
SHOTS = {
'fGcgWaswMns': """
0:00-0:20|DIVER|Flat diver in sunlit blue water; silhouette against light burst; close diver push-in (POV 'you')
0:20-0:25|STOCK|Real footage: sperm whale + freediver
0:25-0:35|CARD|'DANGEROUS WHALES?' header, then orca card 'KILLER WHALE' in a framed tile
0:35-0:40|STOCK|Dark orca footage, tag 'APEX PREDATOR'
0:40-0:45|SCENE|Boat on flat surface horizon, label 'BY ACCIDENT'
0:45-0:55|LABEL|Whale silhouette left, stacked fact tags appear right ('BIGGEST PREDATOR WITH TEETH, EVER', 'HUNTS WHERE NO MAMMAL CAN')
0:55-1:00|DIVER|Tiny diver with torch in the dark, title-drop line
1:00-1:15|SCALE|Whale side view + '~16 M' bar, then yellow CITY BUS drops in under it
1:15-1:30|LABEL|Push-in on head: 'FOREHEAD?', red 'THE HEAD: ~1/3 OF THE WHOLE ANIMAL' bracket, 'NARROW LOWER JAW'
1:30-1:40|LABEL|Jaw close-up 'TEETH ON THE BOTTOM JAW ONLY' + inset card tooth vs hand '~1 KG EACH'
1:40-1:50|SPLIT|Split screen 'HUMPBACK: FILTERS' (baleen) vs 'SPERM WHALE: ?' -> red 'IT GRABS.'
1:50-1:55|CARD|Red underlined 'WHAT DOES IT EAT?' over whale diving
1:55-2:00|HERO|Whale diving diagonally into dark
2:00-2:15|LABEL|Red squid hero, 'HOOKS' tentacle close-up, 'BIGGEST SQUID BEAK KNOWN'
2:15-2:20|STOCK|Real sperm whale with diver near surface
2:20-2:25|LABEL|Whale with 'CIRCULAR SCARS' marks
2:25-2:30|CHART|'WHALE STOMACH' oval with counter '30 SQUID BEAKS' rising
2:30-2:40|GAG|'SPERM WHALE DINER' receipt unrolls (itemised squid) + wallet '...US' joke
2:40-2:50|DEPTH|Whale dives past vertical depth ruler 250 m -> 2,000+ m, breath timer ring
2:50-2:55|YOU|Swimmer in pool lane with red timer, 'YOU'
2:55-3:00|BLACK|Fade to black (no light at all)
3:00-3:10|LABEL|Cutaway head 'A BIOLOGICAL SPEAKER', 'SPERMACETI ORGAN - waxy oil'
3:10-3:20|HUD|Sound beam cone from head; green radar/sonar sweep labelling SQUID, FISH
3:20-3:35|STAT|'LOUDEST ANIMAL ON EARTH' meter bar fills green->red, '236 dB measured underwater'
3:35-3:45|DIVER|Whale and diver, click arcs hit diver, 'YOU FEEL IT IN YOUR CHEST'
3:45-3:50|HUD|Green x-ray diver, red 'YOU, BEING SCANNED' (callback to hook)
3:50-3:55|LABEL|'THEORY (1980s): STUN PREY WITH SOUND' whale + red squid
3:55-4:05|GAG|Two stick scientists at whiteboard 'dB -> ??? STUN??', 'SERIOUSLY CONSIDERED'
4:05-4:10|HERO|Extreme close-up eye/skin, grey
4:10-4:20|LABEL|X-ray head with pink brain 'LARGEST BRAIN OF ANY ANIMAL, EVER' -> balance scale brain ~8 kg vs bowling ball ~7 kg
4:20-4:25|HERO|'FAMILY GROUPS' whales with click dots
4:25-4:35|MAP|Caribbean map, Dominica in red, '2024 STUDY - PROJECT CETI', '~8,350 CODAS ANALYSED'
4:35-4:40|CHART|Dot rhythm rows RHYTHM/TEMPO/TIMING/EXTRA CLICK
4:40-4:45|CHART|'THEIR OWN DIALECTS' clans A/B/C
4:45-4:55|DIVER|Whale scanning diver; UI card 'TRANSLATING WHALE...' progress bar (joke)
4:55-5:05|SCENE|Surface line, sailing ship; 'AGAINST PEOPLE?' whale rising
5:05-5:25|SCENE|'THE ESSEX - NOVEMBER 1820 - PACIFIC OCEAN' whale rams ship, red 'RAMMED', 'DAY 35 ADRIFT' whaleboats
5:25-5:30|DOC|Book cover 'MOBY-DICK' 1851 'INSPIRED BY THE ESSEX'
5:30-5:40|SCENE|'THE ANN ALEXANDER - 1851' ship + impact ring
5:40-5:50|LABEL|Two males head-to-head 'A BATTERING RAM?' 'MALES FIGHTING EACH OTHER'
5:50-5:55|SCENE|Whaleboats chasing family
5:55-6:00|DOC|Paper 'OFFICIAL COMPLAINT' filed by one (1) sperm whale (joke)
6:00-6:05|DIVER|Top-down diver in torch beam, sonar rings
6:05-6:10|BLACK|Dark card: the question
6:10-6:15|STAT|Option 1 visual: diver + whale, speed bars 'YOU ~2 KM/H' vs 'SPERM WHALE - CRUISING ~5 KM/H'
6:15-6:20|HUD|Sonar tracking reticle on diver 'TRACKING 00:41'
6:20-6:25|GAG|Stick figure in a room full of eyes ('room that's already watching you')
6:25-6:35|GAG|Diver 'YOU' at surface with depth ruler; lamp-lit table in the dark ('walking into its kitchen')
6:35-6:40|OPTIONS|'YOUR OPTIONS' list, 1-2 struck through, '3. STAY PERFECTLY STILL' highlighted red box
6:40-6:45|DIVER|'IT DOESN'T NEED TO SEE YOU' ear icon, diver 'PERFECTLY STILL', whale with sound arcs
6:45-6:50|OPTIONS|List again, '4. SCARE IT OFF' highlighted
6:50-6:55|STAT|'VOLUME CONTEST' two meters YOU (SPLASHING) vs SPERM WHALE
6:55-7:05|OPTIONS|All options struck, dims; 'IF IT DECIDED YOU WERE A PROBLEM...'
7:05-7:10|SCENE|Old parchment map 'Here be Monsters' whale attacking ship
7:10-7:20|CHART|Pie 'WHAT SPERM WHALES EAT' MOSTLY SQUID / SOME FISH, 'HUMANS 0% NOT ON THE MENU', 'NO PATTERN OF HUNTING HUMANS'
7:20-7:30|SCENE|Bright water, swimmers above whales 'DOMINICA - PERMITTED SWIMMERS + RESEARCHERS', 'CALM CURIOSITY'
7:30-7:35|SPLIT|Split 'YOU vs A FLY' stick figure / 'A SPERM WHALE vs YOU'
7:35-7:50|HERO|Family swimming; vertical sleeping whales 'SHORT NAPS', 'STRAIGHT UP AND DOWN'
7:50-7:55|LABEL|'THE REAL DANGER' whale -> red arrow -> stick 'YOU' (arrow reverses)
7:55-8:00|SCENE|Sepia 1832 whaling ship, 'WHALE OIL' barrels
8:00-8:10|CHART|Pictogram grid of whale icons '~1,100,000 before commercial whaling' -> rows turn red '~520,000'
8:10-8:15|SCENE|1960s steam whaler harpoon, 'UP TO 25,000 KILLED PER YEAR' counter
8:15-8:20|DOC|IWC paper 'MORATORIUM ON COMMERCIAL WHALING' green 'STOPPED' stamp
8:20-8:25|CARD|'TODAY' on black
8:25-8:30|SPLIT|Triptych SHIP STRIKES / FISHING GEAR / UNDERWATER NOISE
8:30-8:35|STOCK|Aerial real whale footage
8:35-8:40|LABEL|Whale at longline hooks 'STEALING FROM LONGLINES' 'ALASKA - SOUTHERN OCEAN'
8:40-8:45|GAG|Police line-up mugshots SPERM WHALE vs COLOSSAL SQUID (cross-video callback)
8:45-8:50|BLACK|Transition
8:50-8:55|CHART|Food-web star diagram SURFACE/DEEP SEA/PLANKTON/FISH/SQUID/SEABIRDS
8:55-9:05|SCENE|Whale surfaces, 'BREATHE', orange poop plume
9:05-9:10|LABEL|Surface 'PLANKTON' bloom + molecule chain
9:10-9:20|STAT|'SOUTHERN OCEAN' counter ~0 -> '~240,000 TONNES of carbon removed every year' + block grid
9:20-9:25|GAG|Whale in straw hat at surface 'THE BIGGEST TOOTHED PREDATOR ON EARTH' (gardening)
9:25-9:35|DIVER|Bookend: same diver as opening
9:35-9:45|HERO|Whale in the dark '2000 m', pink brain glow
9:45-10:00|END|'THANKS FOR WATCHING' + comment bubble 'Which deep-sea creature next?' + end-screen slot
""",
'2819-mQEA9M': """
0:00-0:10|STOCK|Real lion feeding; real whale underwater ('we've filmed everything')
0:10-0:15|CHART|Grid of animal tiles each ticked (blue whale, great white, orca...) + red '???' tile
0:15-0:25|HUD|REC camera viewfinder in the deep, 'LIVE ADULT COLOSSAL SQUID FILMED: 0'
0:25-0:35|CARD|'WHAT'S SCARY IN THE OCEAN?' three cards SHARKS / KILLER WHALES / GIANT SQUID
0:35-0:45|STOCK|Real shark footage
0:45-0:50|HERO|Long red giant squid 'GIANT SQUID'
0:50-0:55|STOCK|Spaghetti fork photo (gag: 'spaghetti with opinions')
0:55-1:00|SPLIT|GIANT vs COLOSSAL with LONGEST tick
1:00-1:05|BLACK|Dark silhouette reveal
1:05-1:20|SPLIT|Giant squid = ROPE icon, colossal = BARREL icon; tags SHORTER ARMS / WIDER BODY / MORE WEIGHT
1:20-1:25|GAG|'CLASS PHOTO' tall thin kid GIANT vs stocky kid COLOSSAL
1:25-1:35|STOCK|Antarctica: zodiac boat, icebergs
1:35-1:45|DEPTH|Light rays fade with depth ruler, 'WATER: ABOUT -1 TO 2 C', '1000 m', 'SUNLIGHT: 0%'
1:45-1:50|DEPTH|Depth ruler with red 'ITS ZONE' band, squid silhouette
1:50-2:00|MAP|Antarctica globe, pin zoom to Ross Sea '2007 - NEW ZEALAND FISHING BOAT'
2:00-2:05|SCALE|Balance scale squid '~HALF A TON' vs GRAND PIANO
2:05-2:10|LABEL|'BIGGEST SQUID BEAK KNOWN'
2:10-2:15|LABEL|Arm crown top view with hooks (star)
2:15-2:20|LABEL|'GIANT SQUID SUCKER ringed with tiny teeth' macro
2:20-2:35|LABEL|Squid side: '8 ARMS' hooks highlighted, 'TENTACLE CLUB' swivel hooks
2:35-2:40|GAG|Hooked tentacle holding a fish (fishing lure reversed)
2:40-2:50|HERO|Squid full body drifting
2:50-2:55|BLACK|Darkness
2:55-3:00|HERO|Squid with 'THE BIGGEST EYES ON EARTH'
3:00-3:15|SCALE|Glowing eye '~27 CM ACROSS' ruler; SQUID EYE vs SOCCER BALL
3:15-3:20|DOC|Paper study card 'A Unique Advantage for Giant Eyes in Giant Squid' (Current Biology 2012)
3:20-3:25|CARD|'SMALL PREY?' fish icons
3:25-3:40|HERO|Bioluminescent plankton trail behind dark shape; eye in corner
3:40-3:50|HERO|Squid front, eye glowing; red 'WHAT SCARES A HALF-TON SQUID?'
3:50-4:00|HERO|'SPERM WHALE' hero, then diving with 'DEPTH 690 m'
4:00-4:05|STOCK|Real sperm whales
4:05-4:10|CHART|'WHALE STOMACH' oval full of beaks, counter '870 SQUID BEAKS'
4:10-4:15|DOC|Menu card 'SOUTHERN OCEAN - sperm whale's menu ... Colossal squid * CHEF'S SPECIAL'
4:15-4:25|DOC|Specimen jar 'Mesonychoteuthis 1925' 'FOUND IN A SPERM WHALE'S STOMACH'
4:25-4:30|STOCK|Real sperm whale skin close-up
4:30-4:35|LABEL|Whale with 'CIRCULAR SCARS / LONG SCRATCHES'
4:35-4:40|LABEL|'REMEMBER THESE?' hooks callback
4:40-4:50|HERO|Whale vs squid fight in the dark, tags '16 M WHALE' / 'HOOKS ON EVERY LIMB', 'NEVER SEEN BY A HUMAN'
4:50-4:55|DIVER|Diver with torch (the question)
4:55-5:00|OPTIONS|'YOUR OPTIONS' 5-item list appears
5:00-5:05|DIVER|Diver, 'DEPTH: HUNDREDS OF METRES / WATER: NEAR FREEZING'
5:05-5:10|SPLIT|'ITS VIEW' green night-vision diver vs black '...' (your view)
5:10-5:15|OPTIONS|'2. FIGHT' highlighted
5:15-5:20|STAT|Diver '2 ARMS' vs squid '10 ARMS + TENTACLES'
5:20-5:25|GAG|Stick figure under ceiling fan 'THAT'S NOT A FIGHT'
5:25-5:30|LABEL|Swivel hook on fish 'THE HOOK TURNS WITH YOU'
5:30-5:40|MAP|Zoom out to Antarctica, red 'YOU' dot
5:40-5:45|GAG|Phone 'No Service', 'Sharing location...'
5:45-5:50|OPTIONS|'5. HOPE IT SWALLOWS YOU' highlighted
5:50-5:55|LABEL|Diagram: donut BRAIN with THROAT through hole
5:55-6:00|LABEL|Beak 'SMALL PIECES ONLY'
6:00-6:05|OPTIONS|List fades (verdict)
6:05-6:15|CARD|Red-tinted 'HUNGRY MONSTER?' squid
6:15-6:25|DOC|Paper 'Slow pace of life of the Antarctic colossal squid' J. Marine Biological Assoc. 2010
6:25-6:35|STAT|Kitchen scale '30 g' -> '= ONE SLICE OF BREAD'
6:35-6:40|STAT|'ONE 5 KG FISH' -> calendar 'DAY 200'
6:40-6:45|HERO|Squid waiting, fish drifts close
6:45-6:50|GAG|Squid on couch in living room with TV 'LESS SHARK. MORE ROOMMATE.'
6:50-7:00|DIVER|Torch beam reveals dark squid silhouette
7:00-7:05|SCENE|Fishing boat with longline
7:05-7:10|STOCK|Real museum specimen in tank
7:10-7:20|CHART|Timeline 'A HANDFUL OF GOOD SPECIMENS' 1925 / 1981 / 2003
7:20-7:25|HERO|Squid eating toothfish on line
7:25-7:30|STOCK|Real toothfish photo
7:30-7:35|HERO|Squid with fish
7:35-7:40|STOCK|Te Papa museum specimen
7:40-7:50|STOCK|Ross Sea ice footage
7:50-8:00|MAP|Antarctica '2016 - ROSS SEA MARINE PROTECTED AREA' green wedge '1.5+ MILLION KM2'
8:00-8:05|BLACK|Dark silhouette
8:05-8:10|CARD|'MARCH 2025'
8:10-8:20|HUD|ROV 'SCHMIDT OCEAN INSTITUTE - ROV' descending with depth readout + minimap
8:20-8:40|SCALE|Translucent baby squid '~30 CM', 'SEE-THROUGH, LIKE GLASS', 'COLOUR CELLS: CLEAR <-> SOLID' (fades)
8:40-8:50|CHART|Timeline 1925 -> 2025 counter '0 YEARS' -> '100 YEARS' '...TO FILM A BABY'
8:50-8:55|HUD|REC viewfinder callback 'LIVE ADULT COLOSSAL SQUID FILMED 0'
8:55-9:15|CHART|Food chain: FISH -> COLOSSAL SQUID -> SPERM WHALES / SLEEPER SHARKS / SEABIRDS
9:15-9:25|LABEL|Whale scars callback, red 'KEEPS THE BIGGEST TOOTHED PREDATOR FED'
9:25-9:30|SCENE|Sunset over sea, ship
9:30-9:40|HERO|Squid in dark, eye glow (bookend)
9:40-10:00|END|'THANKS FOR WATCHING' + 'Which deep-sea creature next?' + 'WATCH NEXT' slot
""",
'mg2YJ04Hl9k': """
0:00-0:15|HERO|Outlined cartoon great white, blood drop, breach from below, kinetic caption 'fly out of the WATER.'
0:15-0:25|LABEL|Name tag 'Great White Shark', gold crown 'KING?'
0:25-0:30|HERO|Shark floating at surface 'washing up'
0:30-0:35|LABEL|X-ray shark, orange 'Shark liver'
0:35-0:40|STOCK|Dark real orca footage 'Orcas'
0:40-0:50|HERO|Cartoon orca 'just LEAVE.'; shark alone
0:50-0:55|SCALE|'Our great white' 5 m bar 'over a tonne'
0:55-1:00|DIAL|'every OCEAN' + rotating DT time-dial (era selector)
1:00-1:05|HERO|Shark cruising
1:05-1:20|DEPTH|Shark dives past vertical depth gauge 0-1200 m, 'ESCAPE into the deep'
1:20-1:25|SCORE|Legend: crown 'rules the ocean', check 'survives' (skull 'dies')
1:25-1:30|DIAL|Time dial spins
1:30-1:35|ERA|Era card '500 MILLION YEARS AGO / CAMBRIAN PERIOD'
1:35-1:40|LAND|Beige barren landscape 'no TREES, no GRASS'
1:40-1:45|HERO|Seafloor with trilobites 'EVERY animal'
1:45-1:55|MAP|Flat map card Gondwana / shallow seas
1:55-2:00|LAND|Landscape with huge moon 'The Moon, much closer' '21 HOURS'
2:00-2:30|HERO|Seafloor sponges + trilobites 'Cambrian EXPLOSION', Anomalocaris tag + highlight ring
2:30-2:50|HERO|Shark eats Anomalocaris; empty seafloor
2:50-2:55|STAT|Bar 'Oxygen today 100%'
2:55-3:00|HERO|Red-tinted water 'almost NONE.'
3:00-3:05|STAT|Shark + small oxygen bar 'SPORTS CAR'
3:05-3:10|DEPTH|Depth gauge on red 'even WORSE.' 699 m
3:10-3:15|HERO|Faded shark + crown 'slowly STARVING.' (verdict skull)
3:15-3:20|DIAL|Time dial
3:20-3:30|MAP|Map cards 'seas have risen HIGHER'
3:30-3:45|HERO|Orthocones swim; 'The first coral reefs'; 'plankton, snails, starfish, clams.'
3:45-3:50|LAND|'The first land plants'
3:50-4:00|MAP|Map with south-pole ice strip
4:00-4:10|HERO|Orthocone close
4:10-4:20|SCALE|Great white 5 m vs 'The famous claim' 9 m? -> 'Largest real shells' 5.5 m
4:20-4:30|HERO|'GOOD news' shark eats orthocone
4:30-4:35|LABEL|'Sea scorpion'
4:35-4:40|HERO|Shark
4:40-4:45|DEPTH|Depth gauge 'nothing' (deep is safe)
4:45-4:50|SCORE|Big crown + mini scoreboard corner (1 0 1)
4:50-4:55|DIAL|Dial advances
4:55-5:00|ERA|'370 MILLION YEARS AGO / DEVONIAN PERIOD'
5:00-5:10|LAND|Archaeopteris trees 'taller than a HOUSE'
5:10-5:20|STAT|'Oxygen in the coastal sea' bar drains 'CHOKED.'
5:20-5:25|HERO|Big reef 'Bigger than any reef alive today'
5:25-5:35|LAND|Tiktaalik on mud 'our own ANCESTORS.'
5:35-5:40|HERO|Ghost Dunkleosteus silhouette
5:40-6:00|HERO|Small sharks 'is FAMILY.' -> Dunkleosteus reveal 'no TEETH.' jaw open
6:00-6:05|LABEL|Bone blade jaws highlighted
6:05-6:20|SCALE|Great white 5 m vs 'Old reconstructions' 10 m? -> 'Dunkleosteus (2023)' 4.1 m 'great white BIGGER.'
6:20-6:35|HERO|Standoff 'FASTER', keep distance
6:35-6:45|SCORE|Scoreboard 1 RULED / 1 SURVIVED / 1 DIED
6:45-6:55|ERA|'300 MILLION YEARS AGO / CARBONIFEROUS & PERMIAN'
6:55-7:10|LAND|Giant dragonfly 'OXYGEN in the air'; millipede 'longer than' human; 'Coal swamp forests'
7:10-7:20|MAP|Continents merge 'Pangaea'
7:20-7:30|HERO|Ghost Dunkleosteus 'Extinct at the end of the Devonian'
7:30-7:55|HERO|Shark crowd 'GOLDEN AGE'; Stethacanthus, 'Edestus'; Helicoprion spiral; 'fun FACT.'
7:55-8:00|STOCK|Polaroid photo 'Ratfish (chimaera)'
8:00-8:20|HERO|'perfectly built HUNTER.' then grey-out 'nothing' (Great Dying)
8:20-8:25|DIAL|Dial
8:25-8:30|ERA|'250 MILLION YEARS AGO / TRIASSIC PERIOD'
8:30-8:35|HERO|Empty dark 'almost CLEAN.'
8:35-8:40|MAP|Pangaea deserts
8:40-8:45|HERO|Dead reef red X
8:45-8:50|LAND|Desert landscape reptile
8:50-9:00|HERO|'Ammonites'
9:00-9:10|HERO|Ichthyosaurs 'REPTILES' 'like' dolphins
9:10-9:15|SCALE|Great white 5 m vs Shonisaurus 15 m
9:15-9:25|HERO|'Thalattoarchon' reveal, teeth close-up
9:25-9:30|STAT|Big text '8 million years'
9:30-9:35|HERO|'bounced back' trio
9:35-9:40|SCALE|5 m vs Thalattoarchon 8.6 m 'isn't the BIGGEST.'
9:40-9:45|DEPTH|Dive 777 m 'Thalattoarchon gives up'
9:45-9:50|DIAL|Dial
9:50-9:55|ERA|'160 MILLION YEARS AGO / JURASSIC PERIOD'
9:55-10:05|MAP|'Pangaea splits'
10:05-10:10|LAND|Sauropod on shore
10:10-10:20|HERO|'Ammonites and belemnites'
10:20-10:25|LAND|'BIRDS'
10:25-10:40|HERO|'ONE thing' pliosaur cruising
10:40-10:45|SCALE|'Old documentaries' 25 m? vs great white
10:45-10:55|HERO|Pliosaur jaw 'most powerful BITES'
10:55-11:00|HERO|'there's FOOD'
11:00-11:10|HERO|'Leedsichthys' + pliosaur
11:10-11:15|HERO|'serious TROUBLE.'
11:15-11:25|DEPTH|1151 m 'pliosaur turns back'
11:25-11:35|SCORE|2 RULED / 3 SURVIVED / 1 DIED 'about to CHANGE.'
11:35-11:40|ERA|'80 MILLION YEARS AGO / CRETACEOUS PERIOD'
11:40-11:45|MAP|World map
11:45-11:55|HERO|'WARMER than any tropical sea'
11:55-12:05|LAND|Chalk cliffs; T. rex ghost on land
12:05-12:15|HERO|Ghost mosasaur; red-tinted shark
12:15-12:20|HERO|Mosasaur jaw close
12:20-12:25|SCALE|5 m vs Mosasaurus 13 m
12:25-12:35|HERO|'Tylosaurus', 'Cretoxyrhina'
12:35-12:40|SCALE|Our great white 5 m vs Cretoxyrhina 7 m
12:40-12:50|HERO|Chase
12:50-12:55|CHART|Two sharks on a trophic ladder
12:55-13:00|DEPTH|947 m, mosasaur follows
13:00-13:05|SCORE|Skull 'EATEN'
13:05-13:15|ERA|'40 MILLION YEARS AGO / EOCENE EPOCH'
13:15-13:20|MAP|'no ICE'
13:20-13:25|LAND|'Near the Arctic Circle' palms + croc
13:25-13:30|MAP|'Tethys Sea' ring
13:30-13:35|HERO|'FASTER'
13:35-13:50|LAND|'Pakicetus'; 'Wadi Al-Hitan, Egypt' skeleton in desert
13:50-14:05|HERO|'Basilosaurus'; 'TINY back legs' ring
14:05-14:10|STOCK|Framed photo 'Basilosaurus skeleton'
14:10-14:20|HERO|'whale CALVES' eaten; surface
14:20-14:25|DEPTH|'stay DEEP' 286 m
14:25-14:30|SCORE|Check 'PASS'
14:30-14:35|HERO|Red 'the WORST ocean'
14:35-14:45|ERA|'15 MILLION YEARS AGO / MIOCENE EPOCH'
14:45-14:50|MAP|World map ice strip
14:50-15:10|HERO|'plankton -> fish -> EVERYTHING'; 'Seals, penguins, whales'; 'RICHEST' kelp
15:10-15:25|HERO|Megalodon looms behind shark
15:25-15:35|SCALE|5 m vs Megalodon 15 m 'size of'
15:35-15:50|HERO|'a SNACK.'; whale flipper bite ring
15:50-15:55|LABEL|'Sperm whale (today)' -> Livyatan jaws
15:55-16:00|STOCK|Photo Livyatan skull cast
16:00-16:05|HERO|'in HALF.'
16:05-16:10|DEPTH|1200 m, Livyatan follows
16:10-16:15|DIAL|Dial
16:15-16:20|ERA|'5 MILLION YEARS AGO / PLIOCENE EPOCH'
16:20-16:35|MAP|Americas join, Pacific/Atlantic labels
16:35-16:45|HERO|'GIANT' ghost megalodon; 'real great WHITES'
16:45-16:50|STOCK|Photo fossil teeth 'Zinc in fossil teeth (2022)'
16:50-17:00|CHART|Trophic ladder 'SAME level' Megalodon / Early great white / same prey
17:00-17:05|STAT|'Climate change' bar
17:05-17:25|HERO|Two sharks; megalodon fades; 'still HERE.'
17:25-17:30|MAP|Modern map
17:30-17:45|HERO|Modern ocean, seals, orca appears; surface 'finally'
17:45-17:55|STOCK|Real orca footage 'Orcas: teams, plans, teachers'; aerial 'Farallon Islands, 1997'
17:55-18:05|HERO|Orca grabs shark; shark flipped
18:05-18:10|MAP|'California' coast, sharks leave
18:10-18:20|CHART|Line-up ghosts Armoured fish / Sea monsters / Mosasaurs / Pliosaurs
18:20-18:35|SCORE|'NOT THE KING' -> 2 RULED / 5 SURVIVED / 3 DIED 'mostly by staying deep'
18:35-18:40|CHART|Deaths: 'Starved: Cambrian', 'Eaten: Cretaceous'
18:40-18:45|HERO|Shark with crown
18:45-18:55|CHART|Rival line-up crossed out with red X
18:55-19:05|HERO|Shark; dives 71 m
19:05-19:15|HERO|Shark cruising (closing line)
19:15-19:20|END|'WHICH ANIMAL NEXT?' fake comments box
19:20-19:45|END|'DEPTH THEORY - WATCH NEXT' end-screen slot
"""}
for vid, block in SHOTS.items():
    words = json.load(open(f'subs/{vid}.words.json'))
    ch = json.load(open(f'raw/analysis/{vid}.changes.json'))
    rows = []
    rng = []
    for line in block.strip().splitlines():
        a, code, desc = line.split('|', 2)
        t0, t1 = a.split('-'); rng.append((s(t0), s(t1), code, desc))
    end = int(max(r[1] for r in rng))
    ev = ch['times_frac0.1']
    for w0 in range(0, end, 5):
        mid = w0 + 2.5
        lab = next(((c, d) for a0, a1, c, d in rng if a0 <= mid < a1), ('?', ''))
        txt = ' '.join(x['w'] for x in words if w0 <= x['t'] < w0 + 5)
        nev = sum(1 for t in ev if w0 <= t < w0 + 5)
        mot = ch['motion_per_5s'][w0 // 5] if w0 // 5 < len(ch['motion_per_5s']) else ''
        rows.append([f'{w0//60}:{w0%60:02d}', lab[0], lab[1], nev, mot, txt])
    with open(f'beatmaps/{vid}.shots.csv', 'w', newline='') as f:
        wr = csv.writer(f); wr.writerow(['t', 'shot_type', 'on_screen', 'visual_change_events', 'motion', 'narration'])
        wr.writerows(rows)
    from collections import Counter
    cnt = Counter(r[1] for r in rows)
    tot = len(rows)
    print(vid, tot, ', '.join(f'{k} {100*v/tot:.0f}%' for k, v in cnt.most_common()))
    json.dump({k: round(100 * v / tot, 1) for k, v in cnt.most_common()}, open(f'beatmaps/{vid}.shot_mix.json', 'w'))
