import json,glob,statistics,sys
out={}
for f in sorted(glob.glob('raw/peers/*.json')):
    d=json.load(open(f))
    es=[e for e in d['entries'] if e.get('view_count') is not None]
    v=[e['view_count'] for e in es]; med=statistics.median(v) if v else 0
    subs=d.get('channel_follower_count')
    print(f"\n== {d.get('channel')} {d.get('channel_id')} subs={subs} n={len(es)} median={med:,.0f}")
    for e in sorted(es,key=lambda x:-x['view_count'])[:int(sys.argv[1]) if len(sys.argv)>1 else 8]:
        print(f"   {e['view_count']:>11,} x{e['view_count']/max(med,1):5.1f} {int(e.get('duration') or 0)//60:>3}m {e['id']} {e['title'][:85]}")
    print('   newest:', [(x['title'][:45],x['view_count']) for x in es[:4]])
    out[d.get('channel_id')]={'channel':d.get('channel'),'subs':subs,'n':len(es),'median':med,'videos':[{'id':e['id'],'title':e['title'],'views':e['view_count'],'duration':e.get('duration'),'outlier':round(e['view_count']/max(med,1),2)} for e in es]}
json.dump(out,open('raw/peers_summary.json','w'),indent=1)
