from pathlib import Path
import sys,datetime,json,hashlib,csv,concurrent.futures,urllib.parse,urllib.request
from zoneinfo import ZoneInfo
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'work/research-python-packages'))
import numpy as np
B=Path(__file__).parent;raw=B/'hourly_raw';raw.mkdir(exist_ok=True)
symbols=['BIDU','BABA','JD','NTES','^GSPC','SPY','KWEB','MCHI']
def fetch(s):
 p1=int(datetime.datetime(2025,7,1,tzinfo=datetime.timezone.utc).timestamp());p2=int(datetime.datetime(2025,10,15,tzinfo=datetime.timezone.utc).timestamp())
 url='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(s,safe='')+f'?period1={p1}&period2={p2}&interval=60m&includePrePost=true&events=div%2Csplits'
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:data=r.read();status=r.status
  j=json.loads(data)['chart']['result'][0];(raw/(s.replace('^','INDEX_')+'.json')).write_bytes(data)
  return {'symbol':s,'http_status':status,'url':url,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'rows':len(j.get('timestamp',[])),'status':'ok'}
 except Exception as e:return {'symbol':s,'url':url,'status':'failed','error':str(e)[:300]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:receipts=list(pool.map(fetch,symbols))
(B/'hourly_access_receipt.json').write_text(json.dumps(receipts,indent=2),newline='')
prices={};allrows=[]
for r in receipts:
 if r['status']!='ok':continue
 s=r['symbol'];j=json.loads((raw/(s.replace('^','INDEX_')+'.json')).read_text())['chart']['result'][0];q=j['indicators']['quote'][0];tz=ZoneInfo(j['meta']['exchangeTimezoneName']);rows=[]
 for i,t in enumerate(j.get('timestamp',[])):
  dt=datetime.datetime.fromtimestamp(t,tz);o=q.get('open',[])[i];c=q.get('close',[])[i];v=q.get('volume',[])[i]
  rows.append({'symbol':s,'time':dt.isoformat(),'date':dt.date().isoformat(),'local_hm':dt.strftime('%H:%M'),'open':o,'close':c,'volume':v,'return':c/o-1 if o and c and o>0 and c>0 and (s.startswith('^') or (v and v>0)) else None})
 prices[s]=rows;allrows+=rows
def save(n,rs):
 if not rs:return
 with (B/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
save('hourly_prices.csv',allrows)
results=[];portfolios=[]
for hm,market,label in [('10:30','^GSPC','preliminary_threat_bar'),('16:00','SPY','tariff_software_joint_bar')]:
 if market not in prices:continue
 md={r['date']:r for r in prices[market] if r['local_hm']==hm and r['return'] is not None}
 previous=sorted(d for d in md if d<'2025-10-10');fitdates=previous[-65:-5]
 stockdata={s:{r['date']:r for r in prices.get(s,[]) if r['local_hm']==hm and r['return'] is not None} for s in ['BIDU','BABA','JD','NTES']}
 for s,sd in stockdata.items():
  dates=[d for d in fitdates if d in sd];er=sd.get('2025-10-10');em=md.get('2025-10-10');valid=len(dates)>=40 and er is not None and em is not None
  ar=None;alpha=beta=None;rank=None
  if valid:
   y=np.array([sd[d]['return'] for d in dates]);X=np.array([[1,md[d]['return']] for d in dates]);alpha,beta=np.linalg.lstsq(X,y,rcond=None)[0];res=y-X@np.array([alpha,beta]);ar=er['return']-alpha-beta*em['return'];rank=(1+int((np.abs(res)>=abs(ar)).sum()))/(len(res)+1)
  results.append({'symbol':s,'event_bar':label,'local_start':hm,'event_date':'2025-10-10','benchmark':market,'fit_start':dates[0] if dates else None,'fit_end':dates[-1] if dates else None,'fit_n':len(dates),'stock_return_pct':er['return']*100 if er else None,'benchmark_return_pct':em['return']*100 if em else None,'alpha':alpha,'beta':beta,'abnormal_return_pct':ar*100 if ar is not None else None,'same_clock_residual_reference_fraction_not_causal_p':rank,'status':'ok' if valid else 'unavailable_or_fewer40'})
  # Aggregate portfolio below uses all four fixed constituents only.
 common=[d for d in fitdates if all(d in stockdata[s] for s in stockdata)]
 if len(common)>=40 and '2025-10-10' in md and all('2025-10-10' in stockdata[s] for s in stockdata):
  y=np.array([np.mean([sd[d]['return'] for sd in stockdata.values()]) for d in common]);X=np.array([[1,md[d]['return']] for d in common]);a,b=np.linalg.lstsq(X,y,rcond=None)[0];e=y-X@np.array([a,b]);event_y=np.mean([sd['2025-10-10']['return'] for sd in stockdata.values()]);x0=np.array([1,md['2025-10-10']['return']]);ar=float(event_y-x0@np.array([a,b]));sd=float(np.sqrt((e@e)/(len(e)-2)*(1+x0@np.linalg.inv(X.T@X)@x0)))
  portfolios.append({'event_bar':label,'constituents':4,'n_same_clock_fit':len(common),'fit_start':common[0],'fit_end':common[-1],'raw_return_pct':float(event_y*100),'benchmark_return_pct':float(x0[1]*100),'abnormal_return_pct':ar*100,'model_prediction_sd_pct':sd*100,'conditional_standardized_prediction_error_not_causal_test':ar/sd,'same_clock_residual_reference_fraction_not_causal_p':(1+int((np.abs(e)>=abs(ar)).sum()))/(len(e)+1)})
save('hourly_firm_results.csv',results);save('hourly_portfolio_results.csv',portfolios)
(B/'hourly_results_receipt.json').write_text(json.dumps({'access':receipts,'observations':len(allrows),'firm_results':results,'portfolio_results':portfolios,'independent_review':'not_completed','interpretation':'observational_information_window;not_separate_software_effect;not_RnD_investment'},indent=2),newline='')
print(json.dumps({'access':[(r['symbol'],r['status'],r.get('rows')) for r in receipts],'portfolio_results':portfolios,'firms':results},indent=2))
