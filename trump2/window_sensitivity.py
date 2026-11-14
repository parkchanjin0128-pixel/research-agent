from pathlib import Path
import csv,json,numpy as np
H=Path(__file__).parent
raw=list(csv.DictReader((H/'hourly_prices.csv').open(encoding='utf-8-sig')))
data={s:{r['date']:float(r['return']) for r in raw if r['symbol']==s and r['local_hm']=='10:30' and r['return']!=''} for s in ['BIDU','BABA','JD','NTES','^GSPC','KWEB','MCHI']}
md=data['^GSPC'];prev=sorted(d for d in md if d<'2025-10-10');rows=[]
for label,dates in [('implemented_60_bars_after_5_day_gap',prev[-65:-5]),('literal_prior60_minus5_equals55',prev[-60:-5])]:
 for name,syms in [(s,[s]) for s in ['BIDU','BABA','JD','NTES','KWEB','MCHI']]+[('four_ADR_equal_weight',['BIDU','BABA','JD','NTES'])]:
  ds=[d for d in dates if all(d in data[s] for s in syms)];X=np.array([[1,md[d]] for d in ds]);y=np.array([np.mean([data[s][d] for s in syms]) for d in ds]);b=np.linalg.lstsq(X,y,rcond=None)[0];e=np.mean([data[s]['2025-10-10'] for s in syms]);ar=100*(e-b[0]-b[1]*md['2025-10-10'])
  rows.append({'fit_rule':label,'instrument':name,'n_fit':len(ds),'fit_start':ds[0],'fit_end':ds[-1],'abnormal_return_pct':float(ar)})
with (H/'estimation_window_sensitivity.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
receipt={'reason':'Clarify ambiguous pre-price prose: code implemented previous65[-65:-5] (60 target bars after 5-day gap). Preserve original wording; additionally compute literal previous60[-60:-5] (55 target bars). Analysis unchanged in primary; sensitivity added after observing results.','portfolio_results':[r for r in rows if r['instrument']=='four_ADR_equal_weight']}
(H/'estimation_window_clarification.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8');print(json.dumps(receipt,indent=2))
