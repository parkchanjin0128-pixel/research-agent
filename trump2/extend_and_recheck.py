"""Additional descriptive hourly projections and distinct-formula numerical checks."""
from pathlib import Path
import sys,json,csv,itertools,hashlib
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R/'work/research-python-packages'))
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).parent;O=B.parent/'analysis'
rows=list(csv.DictReader((B/'hourly_prices.csv').open(encoding='utf-8-sig')))
prices={s:{r['date']:float(r['return']) for r in rows if r['symbol']==s and r['local_hm']=='10:30' and r['return']} for s in ['BIDU','BABA','JD','NTES','^GSPC','SPY','MCHI','KWEB']}
day='2025-10-10';md=prices['^GSPC'];dates=sorted(d for d in md if d<day)[-65:-5]
base=json.loads((B/'hourly_results_receipt.json').read_text())
comparisons=[];metrics=[];past=[]
def fit_predict(sd,market,tag):
 ds=[d for d in dates if d in sd and d in market];x=np.array([market[d] for d in ds]);y=np.array([sd[d] for d in ds]);b=np.sum((x-x.mean())*(y-y.mean()))/np.sum((x-x.mean())**2);a=y.mean()-b*x.mean();res=y-a-b*x
 ar=sd[day]-a-b*market[day];X=np.column_stack([np.ones(len(x)),x]);x0=np.array([1,market[day]]);psd=np.sqrt(np.sum(res**2)/(len(x)-2)*(1+x0@np.linalg.inv(X.T@X)@x0))
 rr={'instrument':tag,'n_same_clock_fit':len(ds),'raw_return_pct':sd[day]*100,'benchmark_return_pct':market[day]*100,'abnormal_return_pct':ar*100,'prediction_sd_pct':psd*100,'standardized_error_conditional_model':ar/psd,'reference_rank_abs_1_is_largest':1+int((np.abs(res)>=abs(ar)).sum()),'reference_total':len(ds)+1}
 metrics.append(rr);past.extend({'instrument':tag,'date':d,'same_clock_residual_pct':float(v*100)} for d,v in zip(ds,res));return a,b,ar,psd,res
for s in ['BIDU','BABA','JD','NTES']:
 a,b,ar,psd,res=fit_predict(prices[s],md,s)
 orig=next(r for r in base['firm_results'] if r['symbol']==s and r['event_bar']=='preliminary_threat_bar')
 comparisons.append({'object':s,'AR_difference':ar*100-orig['abnormal_return_pct'],'beta_difference':b-orig['beta']})
for s in ['KWEB','MCHI']:fit_predict(prices[s],md,s)
ss=['BIDU','BABA','JD','NTES'];common=set.intersection(*(set(prices[s]) for s in ss));port={d:float(np.mean([prices[s][d] for s in ss])) for d in common}
a,b,ar,psd,pres=fit_predict(port,md,'four_ADR_equal_weight');p0=base['portfolio_results'][0]
comparisons.append({'object':'four_ADR_equal_weight','AR_difference':ar*100-p0['abnormal_return_pct'],'beta_difference':None})
fit_predict(port,prices['SPY'],'four_ADR_relative_SPY')
# These benchmarks also respond to China news; this is a changed descriptive estimand.
fit_predict(port,prices['MCHI'],'four_ADR_relative_MCHI_affected_benchmark')
fit_predict(port,prices['KWEB'],'four_ADR_relative_KWEB_affected_benchmark')
def save(p,rs):
 with p.open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
save(B/'hourly_extended_results.csv',metrics);save(B/'hourly_same_clock_residuals.csv',past);save(B/'separate_formula_checks.csv',comparisons)
assert max(abs(r['AR_difference']) for r in comparisons)<1e-10
d=json.loads((B.parent/'patstat/historical_source_and_ip5_raw.json').read_text())['historical_firms'];fr=[dict(zip(d['columns'],r)) for r in d['rows']];br={r['unit'].replace('_group',''):r['known_us_mass']/r['known_pairs'] for r in fr if r['unit'].endswith('_group') and r['variant']=='ALL'}
rr=[r for r in metrics if r['instrument'] in ss];xx=np.array([br[r['instrument']]/.1 for r in rr]);yy=np.array([r['abnormal_return_pct'] for r in rr]);slope=np.polyfit(xx,yy,1)[0];loos=[float(np.polyfit(np.delete(xx,i),np.delete(yy,i),1)[0]) for i in range(4)]
ref=[float(np.polyfit(np.array(p),yy,1)[0]) for p in itertools.permutations(xx)];grad={'slope_pctpoints_per10pp_legacy_B':float(slope),'leave_one_out_min':min(loos),'leave_one_out_max':max(loos),'reference_24_permutations_not_causal_p':sum(abs(v)>=abs(slope) for v in ref)/24,'B_scope':'2013–2017 public-document citations of confirmed2017entity_subset;not2024currentdependence','no_inference':'four_firms;overlapping_information_and_unknown_country_mass'}
(B/'legacy_B_hourly_gradient.json').write_text(json.dumps(grad,indent=2),newline='')
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(figsize=(8.5,4.6));z=[r for r in metrics if r['instrument'] in ss+['KWEB','MCHI']];ax.bar([r['instrument'] for r in z],[r['abnormal_return_pct'] for r in z],color=['#284f78']*4+['#758899']*2);ax.axhline(0,color='black',lw=.6);ax.set_ylabel('Market-model abnormal return (%)');ax.set_title('10 Oct 2025, 10:30–11:30 EDT');fig.tight_layout();fig.savefig(O/'trump2_hourly_AR.png',dpi=200);plt.close(fig)
fig,ax=plt.subplots(figsize=(8.5,4.4));ax.hist(pres*100,bins=14,color='#b7c7d8',edgecolor='white');ax.axvline(ar*100,color='#b5272f',lw=2,label=f'Event hour: {ar*100:.2f}%');ax.set_xlabel('Four-ADR portfolio residual at 10:30 (%)');ax.set_ylabel('Pre-event trading days');ax.legend();fig.tight_layout();fig.savefig(O/'trump2_hourly_reference.png',dpi=200);plt.close(fig)
# Raw cumulative price path: hourly endpoints, no minute interpolation.
regular=['09:30','10:30','11:30','12:30','13:30','14:30','15:30'];path=[]
for sym in ss+['^GSPC']:
 z=[r for r in rows if r['symbol']==sym and r['date']==day and r['local_hm'] in regular];z=sorted(z,key=lambda r:r['local_hm']);op=float(z[0]['open']);path.append([100*(float(r['close'])/op-1) for r in z])
fig,ax=plt.subplots(figsize=(8.6,4.5));x=np.array([10.5,11.5,12.5,13.5,14.5,15.5,16]);ax.plot(x,np.mean(np.array(path[:4]),axis=0),marker='o',color='#284f78',label='Four Chinese ADRs');ax.plot(x,path[4],marker='s',color='#7a7a7a',label='S&P500');ax.axvspan(10.5,11.5,color='#dce7f2',alpha=.7);ax.axvline(10+57/60,color='#b5272f',ls='--',label='10:57 threat');ax.set_xticks(x,['10:30','11:30','12:30','13:30','14:30','15:30','16:00']);ax.set_xlabel('Bar end (EDT); observations are hourly');ax.set_ylabel('Price change from 09:30 open (%)');ax.legend(fontsize=9);fig.tight_layout();fig.savefig(O/'trump2_intraday_path.png',dpi=200);plt.close(fig)
# After-hours quote observations: reported volume is zero; do not claim executed-trade returns.
quote=[]
for s in ss+['SPY','KWEB','MCHI']:
 r=next((r for r in rows if r['symbol']==s and r['date']==day and r['local_hm']=='16:00'),None)
 if r:quote.append({'symbol':s,'bar':'16:00–17:00_EDT','open':r['open'],'close':r['close'],'reported_volume':r['volume'],'quote_change_pct':100*(float(r['close'])/float(r['open'])-1),'use_rule':'quote_only_sensitivity;zero_reported_volume;excluded_from_primary_model'})
save(B/'afterhours_quote_only.csv',quote)
print(json.dumps({'hourly_metrics':metrics,'legacy_B_gradient':grad,'numeric_recheck_max_AR_difference':max(abs(r['AR_difference']) for r in comparisons)},indent=2))
