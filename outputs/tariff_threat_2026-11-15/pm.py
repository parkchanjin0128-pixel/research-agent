import json,glob,pickle,os,re,numpy as np,pandas as pd
P='/home/claude/parkchanjin0128-pixel/research-agent/data_raw/polymarket/prices/*.json'
if not os.path.exists('work/pm.pkl'):
    M=[]
    for f in glob.glob(P):
        j=json.load(open(f)); h=j['history']
        if len(h)<5: continue
        s=pd.Series([x['p'] for x in h],index=pd.to_datetime([x['t'] for x in h],unit='s',utc=True)); s=s[~s.index.duplicated()].sort_index()
        M.append(dict(q=j['question'],slug=j['slug'],s=s,t0=s.index[0],t1=s.index[-1],last=s.iloc[-1]))
    pickle.dump(M,open('work/pm.pkl','wb'))
M=pickle.load(open('work/pm.pkl','rb'))
r=pd.read_csv('out/event_responses.csv'); r=r[r.tier=='A']
r['t']=pd.to_datetime(r.date+' '+r.time_et).dt.tz_localize('America/New_York').dt.tz_convert('UTC')
def at(s,t):
    x=s[:t]; return x.iloc[-1] if len(x) else np.nan
rows=[]
for _,e in r.iterrows():
    for m in M:
        if m['t0']<e.t-pd.Timedelta(hours=6) and m['t1']>e.t+pd.Timedelta(hours=6):
            p0=at(m['s'],e.t-pd.Timedelta(minutes=10)); p1=at(m['s'],e.t+pd.Timedelta(hours=3)); p24=at(m['s'],e.t+pd.Timedelta(hours=24))
            rows.append(dict(id=e.id,type=e.type,date=e.date,target=e.target,q=m['q'],p0=p0,d3=p1-p0,d24=p24-p0,final=m['last']))
d=pd.DataFrame(rows); d.to_pickle('work/pm_ev.pkl')
print(len(M),len(d)); print(d.groupby('id').size().to_string())
pd.set_option('display.width',250,'display.max_colwidth',95)
for i,g in d.groupby('id'):
    g=g[(g.p0>0.03)&(g.p0<0.97)].reindex(g.d3.abs().sort_values(ascending=False).index).dropna(subset=['d3']).head(6)
    print('\n',i,r[r.id==i].iloc[0][['type','date','target']].tolist()); print(g[['q','p0','d3','d24','final']].round(3).to_string(index=False,header=False))
