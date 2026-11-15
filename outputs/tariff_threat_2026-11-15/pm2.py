import pickle,numpy as np,pandas as pd
M=pickle.load(open('work/pm.pkl','rb')); Q={m['q'].strip():m for m in M}
# (A) 특정 위협의 실행 여부를 묻는 계약 — 질문 문구로 고정 (가격을 보기 전 기준: 조치·시한이 명시된 계약 전부)
A=["Will Trump impose 25% tariff on Mexico or Canada before February?","Trump tariffs on Canada in effect by May 1?","Trump tariffs on Mexico in effect by May 1?",
"25% aluminum tariff in effect before May?","25% steel tariff in effect before May?","Will Trump 10% China tariff increase go into effect by Friday?",
"Will Trump 10% blanket tariff go into effect by Saturday?","54% tariff goes into effect on China by Wednesday?","Trump imposes 200% tariff on China before June?",
"Trump imposes tariff on pharmaceuticals before May?","Will Trump impose film tariff by Friday?","50% tariff goes into effect on EU by June 1?","50% tariff goes into effect on EU by July 9?",
"35% Canada tariff in effect by August 1?","50% Brazil tariff in effect by August 1?","25% South Korea tariff in effect by August 1?","50% copper tariff in effect by August 1?",
"25% Japan tariff in effect by August 1?","30% EU tariff in effect by August 1?","50% India tariff in effect by August 27?","Trump imposes tariff on pharmaceuticals by August 31?",
"Trump imposes tariff on semiconductors by August 31?","Trump imposes tariff on pharmaceuticals by September 30?","Trump imposes tariff on semiconductors by September 30?",
"Trump imposes tariff on semiconductors by December 31?","100% tariff on China in effect by November 1?","Will any of Trump’s Greenland Tariffs go into effect by Feb 1?",
"Tariff increase on Canada in effect by June 30?","100% tariff on Canada in effect by June 30?","New 10% US blanket tariff goes into effect by February 28?",
"Will Trump raise tariffs on Canada by September 15?","Will Trump raise tariffs on Canada by October 31?"]
rows=[]
for q in A:
    m=Q[q]; s=m['s']; t0=m['t0']
    w=s[t0+pd.Timedelta(hours=12):t0+pd.Timedelta(hours=36)]
    life=(m['t1']-t0).total_seconds()/86400
    rows.append(dict(q=q,listed=t0.strftime('%Y-%m-%d'),life_d=round(life,1),p=float(w.median()) if len(w) else float(s.iloc[:24].median()),p_mid=float(s.iloc[len(s)//2]),y=int(m['last']>0.5)))
a=pd.DataFrame(rows); a.to_csv('out/pm_calibration.csv',index=False)
pd.set_option('display.width',220,'display.max_colwidth',70); print(a.round(3).to_string())
print('n',len(a),'mean p',a.p.mean().round(3),'realized',a.y.mean().round(3),'Brier',((a.p-a.y)**2).mean().round(3),'Brier(base rate)',((a.y.mean()-a.y)**2).mean().round(3))
a['bin']=pd.cut(a.p,[0,0.3,0.6,1]); print(a.groupby('bin',observed=True).agg(n=('y','size'),p=('p','mean'),y=('y','mean')).round(2))
from scipy import stats
print('MWU p (가격: 실행 vs 미실행)',stats.mannwhitneyu(a[a.y==1].p,a[a.y==0].p).pvalue.round(4)); 
u=stats.mannwhitneyu(a[a.y==1].p,a[a.y==0].p).statistic; print('AUC',round(u/(a.y.sum()*(1-a.y).sum()),3))
b=a[a.life_d>=7]; print('존속 7일 이상만: n',len(b),'mean p',b.p.mean().round(3),'realized',b.y.mean().round(3),'AUC',round(stats.mannwhitneyu(b[b.y==1].p,b[b.y==0].p).statistic/(b.y.sum()*(1-b.y).sum()),3))
# (B) 사건 시점의 확률 변화: 사건별로 직접 대응하는 기존 계약
r=pd.read_csv('out/event_responses.csv'); r['t']=pd.to_datetime(r.date+' '+r.time_et).dt.tz_localize('America/New_York').dt.tz_convert('UTC'); r=r.set_index('id')
B=[("E02","Will Trump increase tariffs on China before May?"),("E02","Trump tariffs on Canada in effect by May 1?"),("E03","Will Trump increase tariffs on Canada before May?"),
("E06","Will Trump increase tariffs on China before May?"),("E06","Trump imposes 100% tariff on China before July?"),("E14b","Trump imposes tariff on pharmaceuticals by September 30?"),
("E15","Will the U.S. tariff rate on China be between 100% and 150% on November 12?"),("E15","US x China tariff agreement by November 10?"),
("D03","Will Trump reduce majority of tariffs in April?"),("D04","50% tariff goes into effect on EU by June 1?"),("D06","25% South Korea tariff in effect by August 1?"),
("D08","Will any of Trump’s Greenland Tariffs go into effect by Feb 1?")]
def at(s,t):
    x=s[:t]; return float(x.iloc[-1]) if len(x) else np.nan
rows=[]
for i,q in B:
    s=Q[q]['s']; t=r.loc[i,'t']
    rows.append(dict(id=i,date=r.loc[i,'date'],q=q,p_before=at(s,t-pd.Timedelta(minutes=10)),p_3h=at(s,t+pd.Timedelta(hours=3)),p_24h=at(s,t+pd.Timedelta(hours=24)),final=int(Q[q]['last']>0.5),z=r.loc[i,'z'],ret_mkt=r.loc[i,'ret_mkt']))
b=pd.DataFrame(rows); b['dp']=b.p_3h-b.p_before; b.to_csv('out/pm_event_jumps.csv',index=False); print(b.round(3).to_string())
