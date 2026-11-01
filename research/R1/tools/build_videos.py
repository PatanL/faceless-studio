"""Build research/R1/videos.json from raw yt-dlp metadata + Spark analysis. Run from research/R1 with python3 -I."""
import json, statistics, datetime
NOW = datetime.datetime(2026, 11, 1, 8, 50, tzinfo=datetime.timezone.utc).timestamp()
IDS = ['fGcgWaswMns', 'mg2YJ04Hl9k', '2819-mQEA9M', '4Mmo_dlsArE']
MANUAL = {
 'fGcgWaswMns': dict(
   title_formula="Why You'd Never Want To Meet A [Animal]  (second-person 'you', negative curiosity, 7 words, no number)",
   thumbnail="Black background, monochrome scratchboard/engraving-style sperm whale head filling right 2/3, sonar rings; tiny diver with flashlight bottom-left for scale; hand-drawn red arrow from text to diver; 3-word text top-left 'IT HEARS YOU..' white + red 'YOU'. One creature, one human, one verb about a sense.",
   visual_style="Flat 2D vector, no outlines, dark navy-teal vertical gradient + god rays + floating particles; grey whale silhouette with subtle texture; white uppercase sans labels (Montserrat/Poppins-like), red underlined headline labels; ~5% real stock clips; stick-figure gags.",
   structure="single-animal 'never want to meet' template"),
 '2819-mQEA9M': dict(
   title_formula="Why You Never Want to Meet a [Animal]  (same template, first upload, slightly different wording)",
   thumbnail="Black bg, monochrome engraving colossal squid with giant eye left 2/3; tiny diver with flashlight right; red arrow to the eye; text 'IT SEES YOU..' (red YOU).",
   visual_style="Same flat-vector deep-ocean look as sperm whale video but red squid; more real stock footage/photos (lion, shark, spaghetti, Antarctica, museum specimen ~12% of runtime); REC camera HUD, paper study cards, maps.",
   structure="single-animal 'never want to meet' template"),
 'mg2YJ04Hl9k': dict(
   title_formula="Would A [Familiar Apex Animal] Survive Every Prehistoric Ocean?  (yes/no question + 'every' tournament; clone of Fossil's 'Would Orcas Dominate Every Prehistoric Ocean?' 3.8M)",
   thumbnail="Black bg, engraving great white with gold crown left, 4 prehistoric monsters (orthocone, Dunkleosteus, mosasaur, megalodon) stacked right; text 'Still King?' white + red 'King?'. Near copy of Fossil's 'New King?' orca thumbnail.",
   visual_style="Different art style: outlined cartoon creatures (dark outline, cel shading), teal water with god rays, beige/green flat landscapes, map cards; kinetic word captions with one orange/red emphasised word ('fly out of the WATER.'); era title cards ('500 MILLION YEARS AGO / CAMBRIAN PERIOD'); rotating 'DT' time-dial transitions; crown/check/skull scoreboard; vertical depth gauge each era.",
   structure="tournament / era-by-era scoreboard"),
 '4Mmo_dlsArE': dict(
   title_formula="Why You'd Never Want To Meet A [Animal]",
   thumbnail="Black bg, engraving humpback head right, sonar rings, tiny diver with flashlight, red arrow; text 'IT CAN'T SEE YOU' (red YOU).",
   visual_style="Third art style: more detailed illustrated whale with outline, blueprint grid backgrounds, x-ray/hologram whale, polaroid/postcard frames, more real breach footage, HUD corner brackets; dark red 'inside the mouth' cold open.",
   structure="single-animal template; cold open is a real incident (lobster diver scooped up)"),
}
out = {"generated_utc": "2026-11-01T08:50Z", "channel": {}, "videos": [], "peers": {}}
vids = []
for vid in IDS:
    d = json.load(open(f'raw/{vid}.json'))
    cuts = json.load(open(f'raw/analysis/{vid}.cuts.json'))
    ch = json.load(open(f'raw/analysis/{vid}.changes.json'))
    words = json.load(open(f'subs/{vid}.words.json'))
    age_d = (d['epoch'] - d['timestamp']) / 86400  # age at metadata fetch time
    v = dict(id=vid, url=f'https://www.youtube.com/watch?v={vid}', title=d['title'], upload_utc=datetime.datetime.fromtimestamp(d['timestamp'], datetime.timezone.utc).isoformat(),
             age_days=round(age_d, 2), views=d['view_count'], likes=d['like_count'], comments=d['comment_count'], duration_s=d['duration'],
             views_per_day=round(d['view_count'] / age_d), like_rate_pct=round(100 * d['like_count'] / d['view_count'], 2),
             view_sub_ratio=round(d['view_count'] / d['channel_follower_count'], 1),
             chapters=[(c['start_time'], c['title']) for c in d.get('chapters') or []],
             words=len(words), wpm=round(len(words) / (d['duration'] / 60), 1),
             hard_cuts_per_min=cuts['cuts_per_min_0.3'], mean_shot_s=cuts['mean_shot_s_0.3'],
             visual_change_events_per_min=ch['events_per_min_frac0.1'], big_change_events_per_min=ch['events_per_min_frac0.25'],
             thumbnail_file=f'research/R1/thumbs/{vid}.jpg', **MANUAL[vid])
    vids.append(v)
med = statistics.median(v['views'] for v in vids)
med_vpd = statistics.median(v['views_per_day'] for v in vids)
for v in vids:
    v['outlier_vs_median_views'] = round(v['views'] / med, 2)
    v['outlier_vs_median_views_per_day'] = round(v['views_per_day'] / med_vpd, 2)
seed = json.load(open('raw/fGcgWaswMns.json'))
out['channel'] = dict(name='Depth Theory', handle=seed['uploader_id'], id=seed['channel_id'], subs=seed['channel_follower_count'],
    uploads=len(vids), first_upload='2026-10-26', median_views=med, median_views_per_day=med_vpd,
    note='Brand-new channel: all 4 uploads within 6 days (Oct 26 - Nov 1 2026). No Shorts. Category Education. Sperm whale video is a 16x outlier; channel is mostly riding one hit.')
out['videos'] = sorted(vids, key=lambda v: -v['views'])
peers = json.load(open('raw/peers_summary.json'))
for cid, p in peers.items():
    if cid == seed['channel_id']: continue
    top = sorted(p['videos'], key=lambda x: -x['views'])[:8]
    out['peers'][cid] = dict(channel=p['channel'], subs=p['subs'], n_videos=p['n'], median_views=p['median'],
        top_outliers=[dict(id=t['id'], title=t['title'], views=t['views'], outlier=t['outlier'], duration_s=t['duration']) for t in top])
json.dump(out, open('videos.json', 'w'), indent=1, ensure_ascii=False)
for v in out['videos']:
    print(v['id'], v['views'], v['age_days'], v['views_per_day'], v['outlier_vs_median_views'], v['outlier_vs_median_views_per_day'], v['view_sub_ratio'], v['wpm'], v['hard_cuts_per_min'], v['visual_change_events_per_min'], v['like_rate_pct'])
