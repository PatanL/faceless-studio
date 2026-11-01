import json, sys, os
sys.path.insert(0, 'tools')
from vtt2lines import words_from_vtt, group
OUT = '/Users/patrickliu/Documents/faceless-studio/research/corpus/horror/raw'
TT_U = 'median of 40 most recent @udhwkz TikTok uploads = 34,850 views'
TT_M = 'median of 30 @mraevq TikTok uploads in its horror-cartoon era (2026-07-21..08-05) = 10,750 views (library basis)'
TT_T = 'median of 40 most recent @topscaryclips uploads = 4,110 views'
WH = 'faster-whisper small (int8, CPU, 4 threads, VAD) on the Spark; segment start times; proper names are phonetic guesses'
S = [
 # id, url, title, channel, views, median, median_basis, dur, upload, format, source
 ('7702661541224566049','https://www.tiktok.com/@udhwkz/video/7702661541224566049','#edit #anime #animetkitok #animerecommendation (funeral procession, Part 1)','udhwkz',2200000,34850,TT_U,201,'20261031','tiktok 9:16, translated Chinese 2D animation repost, English TTS narration + burned-in captions','wh'),
 ('7702661471641128224','https://www.tiktok.com/@udhwkz/video/7702661471641128224','#edit #anime #animetkitok #animerecommendation (funeral procession, Part 2)','udhwkz',343100,34850,TT_U,191,'20261031','tiktok 9:16, same story as 7702661541224566049 (posted together; this is the continuation)','wh'),
 ('7654526047005723937','https://www.tiktok.com/@mraevq/video/7654526047005723937','#chenjie #wangqiang (killer in complex, fake cop, group chat)','mraevq',716900,10750,TT_M,357,'20260623','tiktok 9:16, translated Chinese 2D animation repost, English TTS narration + burned-in captions, Chinese group-chat UI on screen','wh'),
 ('7659677578365537569','https://www.tiktok.com/@udhwkz/video/7659677578365537569','#edit #anime #animetkitok #animerecommendation (hallway-song killer, fake cop, group chat)','udhwkz',376200,34850,TT_U,249,'20260707','tiktok 9:16, translated Chinese 2D animation repost, English TTS narration + burned-in captions, Chinese owners-group-chat UI on screen','wh'),
 ('7692268145888873760','https://www.tiktok.com/@udhwkz/video/7692268145888873760','#edit #anime #animetkitok #animerecommendation (night-shift trucker rules)','udhwkz',694900,34850,TT_U,166,'20261003','tiktok 9:16, translated Chinese 2D animation repost, English TTS narration','wh'),
 ('7694996216505060641','https://www.tiktok.com/@udhwkz/video/7694996216505060641','#edit #anime #animetkitok #animerecommendation (apartment elevator, propane tank)','udhwkz',613300,34850,TT_U,165,'20261010','tiktok 9:16, translated Chinese 2D animation repost, English TTS narration','wh'),
 ('7670495663624408352','https://www.tiktok.com/@mraevq/video/7670495663624408352','#HorrorTok #CreepyTok #ScaryStories #HorrorComedy #DarkHumor (dorm red curtains, supervisor rules)','mraevq',193600,10750,TT_M,175,'20260805','tiktok 9:16, translated Chinese 2D animation repost, English TTS narration','wh'),
 ('cVUJmsVkUW4','https://www.youtube.com/watch?v=cVUJmsVkUW4',"Horror Stories | Mom's Note Day 1 | Scary Animation",'WrONG Rules',290919,9400,'median of 30 most recent WrONG Rules uploads (Shorts tab) = 9,400 views',135,'20230814','youtube 16:9 animated rules-note story, narrated mother voice + burned-in hand-lettered captions and title cards','cvuj'),
 ('omuJBFs2L6c','https://www.youtube.com/watch?v=omuJBFs2L6c','One of Your Classmates Is Not Real - Analog Horror','Dusk Broadcast',762944,41000,'median of 60 most recent Dusk Broadcast uploads (Videos tab) = 41,000 views',97,'20250627','youtube analog-horror emergency-broadcast short, synthetic announcer voice + on-screen text','vtt'),
 ('T42u5xhrq-0','https://www.youtube.com/shorts/T42u5xhrq-0','so scary 😨','Textify',868500,34000,'median of 60 most recent Textify Shorts = 34,000 views',60,'20240510','youtube short, iMessage chat screen over Minecraft parkour, two TTS voices read each bubble','manual'),
 ('gzXY52lcAcI','https://www.youtube.com/shorts/gzXY52lcAcI','The Creepiest Farmer Text Chat Ever!! - PART 1','Textify',352848,34000,'median of 60 most recent Textify Shorts = 34,000 views',59,'20240918','youtube short, iMessage 1:1 + family group chat over Minecraft parkour, TTS voices read bubbles, Part 1 of a series','manual'),
 ('Qz-TrB6W2SM','https://www.youtube.com/watch?v=Qz-TrB6W2SM','Someone Broke Into Our Hotel Room (Horror Animated)','Wansee Entertainment',1521857,169000,'median of 60 most recent Wansee uploads (Videos tab) = 169,000 views',168,'20181109','youtube 16:9 (also cut vertically as a Short) animated first-person true story, child-voice narrator with acted dialogue','wh'),
]
ALT = [
 ('7668625939458182422','https://www.tiktok.com/@topscaryclips/video/7668625939458182422','True water park horror story (part 2/3) #scary #creepy #true #horror','TopScaryClips',497800,4110,TT_T,88,'20260731','tiktok 9:16 clip of a 2D animated true-story channel, narrated, numbered multi-part series; premise off-niche, kept for series mechanics','wh'),
 ('7668626589122399510','https://www.tiktok.com/@topscaryclips/video/7668626589122399510','True water park horror story (part 3/3)','TopScaryClips',41200,4110,TT_T,96,'20260731','tiktok; the conclusion of 7668625939458182422 (drop-off from part 2: 498K -> 41K)','wh'),
 ('7694491037988818208','https://www.tiktok.com/@udhwkz/video/7694491037988818208','#edit #anime (family on roof, ladder betrayal)','udhwkz',623200,34850,TT_U,153,'20261009','tiktok; starts mid-story (continuation part)','wh'),
 ('BciSW_2VMZg','https://www.youtube.com/shorts/BciSW_2VMZg','New Household Rules (Pt3?) #scary #fyp #trending #horrorstories #viral','WrONG Rules',103714,9400,'median of 30 most recent WrONG Rules Shorts = 9,400 views',50,'20240207','youtube short, rules list, numbered part series','vtt'),
]
def mmss(t): return f"[{int(t//60):02d}:{int(t%60):02d}]"
def dur(d): return f"{d//60}:{d%60:02d}"
def lines_for(i, src):
    if src == 'wh':
        d = json.load(open(f'wh/{i}.json'))
        return [f"{mmss(s['s'])} {s['t']}" for s in d['segments']], WH
    if src == 'vtt':
        g = [f"{mmss(t)} {l}" for t, l in group(words_from_vtt(f'subs/{i}.en-orig.vtt'))]
        if i == 'omuJBFs2L6c' and g[-1].endswith('Stay'): g[-1] += ' safe.'
        return g, 'yt-dlp auto-subs (en VTT, run on the Spark), cleaned to [mm:ss] lines with rolling duplicates removed; cross-checked against faster-whisper small'
    if src == 'manual':
        return open(f'manual_{i}.txt').read().strip().split('\n'), 'caption-only chat video: 1 fps frames sampled on the Spark, contact sheets read visually; each chat bubble transcribed at the second it first appears, with speaker (left grey bubble = other party, right blue = phone owner); TTS voice reads every bubble (auto-subs used to confirm wording)'
    if src == 'cvuj':
        d = json.load(open('wh/cVUJmsVkUW4.json'))
        out = [f"{mmss(s['s'])} {s['t']}" for s in d['segments'] if s['s'] < 28]
        out += open('manual_cVUJ_patch.txt').read().strip().split('\n')
        out += [f"{mmss(s['s'])} {s['t']}" for s in d['segments'] if s['s'] > 73]
        return out, 'faster-whisper small (CPU) + yt-dlp auto-subs; 00:29-01:12 rebuilt from burned-in captions/title cards read off 1 fps contact sheets (whisper merged and dropped lines there); [title card] marks full-screen text cards'
for lst, d in ((S, OUT), (ALT, OUT + '/_alt')):
    for (i, url, title, ch, views, med, basis, du, up, fmt, src) in lst:
        ls, method = lines_for(i, src)
        score = round(views / med, 2)
        hdr = f"# {url} | {title} | {ch} | {views} | {score} | {dur(du)}\n"
        hdr += f"# format: {fmt} | channel_median_views: {med} ({basis}) | upload_date: {up} | transcript: {method}\n"
        open(f'{d}/{i}.txt', 'w').write(hdr + '\n'.join(ls) + '\n')
        print(i, score, len(ls))
