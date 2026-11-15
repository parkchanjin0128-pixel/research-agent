import glob,os,zipfile,numpy as np,pandas as pd
from scipy import stats
import pipeline as P
R='/home/claude/parkchanjin0128-pixel/research-agent/data_raw/dukascopy'
fr=[]
for zp in sorted(glob.glob(R+'/*_2018.zip')+glob.glob(R+'/*_2019.zip')):
    inst=os.path.basename(zp).rsplit('_',1)[0]
    with zipfile.ZipFile(zp) as z:
        for nm in z.namelist():
            df=P.decode_bi5(z.read(nm),nm[:-4],inst)
            if df is not None: fr.append(df[df.vol>0])
fx=pd.concat(fr,ignore_index=True); print(fx.groupby('inst').agg(n=('close','size'),med=('close','median'),t0=('ts','min'),t1=('ts','max')))
S=P.build_series(fx)
ev=pd.read_csv('events_t1_v1.csv',dtype=str).fillna('')
ev['ts']=[pd.Timestamp(d+' '+t,tz='America/New_York').tz_convert('UTC') for d,t in zip(ev.date,ev.time_et)]
out=[]
for w in [(5,30),(5,15),(5,60),(5,120)]:
    r=P.responses(ev,S,w).merge(ev.drop(columns=['ts']),on='id'); r['win']=w[1]; out.append(r)
a=pd.concat(out); a.to_csv('out/t1_responses.csv',index=False)
r=a[a.win==30]; pd.set_option('display.width',220)
print(r[['id','date','time_et','type','target','outcome','z','z_mkt','z_fx','ret_mkt','ret_fx','closed']].round(2).to_string())
for w,g in a.groupby('win'):
    e=g[g.type=='ESC'].z.dropna(); d=g[g.type=='DEESC'].z.dropna()
    print('win',w,'ESC n',len(e),'mean',round(e.mean(),2),'med',round(e.median(),2),'pos',(e>0).sum(),'t',round(e.mean()/(e.std(ddof=1)/np.sqrt(len(e))),2),'| DEESC n',len(d),'mean',round(d.mean(),2))
e=r[r.type=='ESC']; x=e[e.outcome!='NOT_EXECUTED'].z.dropna(); y=e[e.outcome=='NOT_EXECUTED'].z.dropna()
print('exec/partial',len(x),round(x.mean(),2),'| not',len(y),round(y.mean(),2),'MWU',round(stats.mannwhitneyu(x,y).pvalue,3))
print('S&P 30m median(하락=+)',round(e.ret_mkt.median(),3),'DEESC',round(r[r.type=="DEESC"].ret_mkt.median(),3))
t2=pd.read_csv('out/event_responses.csv'); z2=t2[(t2.type=='ESC')&t2.z.notna()].z; z1=e.z.dropna()
print('1기 vs 2기 ESC z: ',round(z1.mean(),2),round(z2.mean(),2),'MWU',round(stats.mannwhitneyu(z1,z2).pvalue,3),'| 2기 E07 제외',round(z2[t2.loc[z2.index,'id']!='E07'].mean(),2))
