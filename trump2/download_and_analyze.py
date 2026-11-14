from pathlib import Path
import sys,json,csv,hashlib,datetime,urllib.request,urllib.parse,concurrent.futures
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'work/research-python-packages'))
import numpy as np
from zoneinfo import ZoneInfo
B=Path(__file__).parent;raw=B/'raw';raw.mkdir(exist_ok=True)
firms=list(csv.DictReader((B.parent/'market/firm_universe.csv').open(encoding='utf-8-sig')))
bench={'US_ADR':'^GSPC','HK':'^HSI','A_SHANGHAI':'000001.SS','A_SHENZHEN':'399001.SZ'}
symbols=list(dict.fromkeys([f['symbol'] for f in firms]+list(bench.values())+['^SOX','KWEB','MCHI']))
def get(s):
 params={'period1':int(datetime.datetime(2023,1,1,tzinfo=datetime.timezone.utc).timestamp()),'period2':int(datetime.datetime(2026,1,1,tzinfo=datetime.timezone.utc).timestamp()),'interval':'1d','events':'div,splits','includeAdjustedClose':'true'}
 url='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(s,safe='')+'?'+urllib.parse.urlencode(params)
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as response: data=response.read();status=response.status
  obj=json.loads(data);result=obj['chart']['result'][0]
  if not result.get('timestamp'):raise ValueError('no price observations')
  p=raw/(s.replace('^','INDEX_')+'.json');p.write_bytes(data)
  return {'symbol':s,'url':url,'http_status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'rows':len(result['timestamp']),'status':'success'}
 except Exception as e:return {'symbol':s,'url':url,'status':'failed','error':str(e)[:200]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:access=list(pool.map(get,symbols))
(B/'access_receipt.json').write_text(json.dumps(access,indent=2),encoding='utf-8',newline='')
print(json.dumps(access,indent=2),flush=True)
prices={};full=[]
for r in access:
 if r['status']!='success':continue
 s=r['symbol'];obj=json.loads((raw/(s.replace('^','INDEX_')+'.json')).read_text())['chart']['result'][0]
 q=obj['indicators']['quote'][0];adj=obj['indicators']['adjclose'][0]['adjclose']; tz=ZoneInfo(obj['meta']['exchangeTimezoneName'])
 dates=[datetime.datetime.fromtimestamp(t,tz).date().isoformat() for t in obj['timestamp']]
 if len(dates)!=len(set(dates)):raise ValueError('duplicate date '+s)
 prices[s]={d:{'close':q['close'][i],'adjusted_close':adj[i],'volume':q.get('volume',[None]*len(dates))[i]} for i,d in enumerate(dates)}
 full += [dict(symbol=s,date=d,**v) for d,v in prices[s].items()]
def save(n,rs):
 if not rs:return
 with (B/n).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
save('prices_2023_2025.csv',full)
events=[('FEB18_CHIP_TARIFF','FEB18','2025-02-19','all_after_US_close',False),('MAY13_NONENFORCEMENT_AUX','MAY13','2025-05-13','timestamp_unconfirmed',True),('AUG06_CHIP_TARIFF_AUX','AUG06','2025-08-06','timestamp_unconfirmed',True),('OCT10_PRELIMINARY_THREAT','OCT10_EPISODE','2025-10-10','2025-10-10T10:57-04:00',False),('OCT10_SOFTWARE_AFTERCLOSE','OCT10_EPISODE','2025-10-13','2025-10-10T16:50-04:00;includes_Oct12_reassurance',False)]
records=[];missing=[]
for f in firms:
 s=f['symbol'];m=bench[f['market']]
 if s not in prices or m not in prices:missing.append({'symbol':s,'reason':'price_download_failed'});continue
 pd=prices[s];md=prices[m];peers=[x['symbol'] for x in firms if x['market']==f['market'] and x['symbol'] in prices]
 def priceok(v):return v is not None and np.isfinite(v) and v>0
 cal=[d for d in sorted(md) if not(md[d]['adjusted_close'] is None and all(prices[x].get(d,{}).get('volume')==0 for x in peers))]
 ri=np.full(len(cal),np.nan);rm=ri.copy()
 for i in range(1,len(cal)):
  a,b=md[cal[i-1]]['adjusted_close'],md[cal[i]]['adjusted_close']
  if priceok(a) and priceok(b):rm[i]=b/a-1
  pa,pb=pd.get(cal[i-1],{}),pd.get(cal[i],{})
  a,b=pa.get('adjusted_close'),pb.get('adjusted_close')
  if priceok(a) and priceok(b) and pa.get('volume',0)>0 and pb.get('volume',0)>0:ri[i]=b/a-1
 for event,episode,date,clock,sens in events:
  requested='2025-10-13' if event=='OCT10_PRELIMINARY_THREAT' and f['market']!='US_ADR' else date
  base=next(i for i,d in enumerate(cal) if d>=requested)
  for shift in ([0,1] if sens else [0]):
   pos=base+shift;est=np.arange(max(0,pos-250),pos-30);ok=np.isfinite(ri[est])&np.isfinite(rm[est]);fit=est[ok];eligible=pos>=250 and len(fit)>=180
   alpha=beta=np.nan
   if eligible:alpha,beta=np.linalg.lstsq(np.column_stack([np.ones(len(fit)),rm[fit]]),ri[fit],rcond=None)[0]
   for lo,hi,label in [(0,0,'[0,0]'),(0,1,'[0,+1]'),(-1,1,'[-1,+1]')]:
    idx=np.arange(pos+lo,pos+hi+1);valid=eligible and np.isfinite(ri[idx]).all() and np.isfinite(rm[idx]).all()
    car=float((ri[idx]-alpha-beta*rm[idx]).sum()) if valid else None
    records.append({'firm_id':f['firm_id'],'symbol':s,'market':f['market'],'benchmark':m,'event_id':event,'episode':episode,'day0':cal[pos],'clock':clock,'shift_sessions':shift,'window':label,'window_start':cal[idx[0]],'window_end':cal[idx[-1]],'n_estimation':len(fit),'alpha':alpha,'beta':beta,'CAR':car,'CAR_pct':car*100 if car is not None else None,'status':'ok' if valid else 'missing_or_insufficient','interpretation':'market_response_to_information_bundle_not_RnD_allocation'})
save('firm_event_car_2025.csv',records);save('missing_firms.csv',missing)
summary=[]
for event in sorted({r['event_id'] for r in records}):
 for m in bench:
  for w in ['[0,0]','[0,+1]','[-1,+1]']:
   rr=[r for r in records if r['event_id']==event and r['market']==m and r['window']==w and r['shift_sessions']==0 and r['status']=='ok']
   if rr:summary.append({'event':event,'market':m,'window':w,'n':len(rr),'mean_CAR_pct':float(np.mean([r['CAR_pct'] for r in rr]))})
save('market_event_summary_2025.csv',summary)
(B/'results_receipt.json').write_text(json.dumps({'price_rows':len(full),'CAR_rows':len(records),'download_successes':sum(r['status']=='success' for r in access),'downloads':len(access),'missing_firms':missing,'independent_review':'not_completed','no_paid_model_API':True,'original_causal_allocation_claim':'not_inferred_from_market_returns'},indent=2),newline='')
print(json.dumps(summary,indent=2),flush=True)
