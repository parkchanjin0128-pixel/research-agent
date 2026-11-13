"""Constructive identification counterexample; no fitted causal model.

Real observed aggregate counts and fixed old B are held unchanged.
Three structural scenarios have different counterfactual rates but the same
conditional distribution for every observable. This witnesses failure of
identification in a model class allowing unrestricted China x IPC x time
counterfactual shocks. It does not say that Chinese policy actually caused Y.
"""
from pathlib import Path
import hashlib,json,math
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
rp=ROOT/'outputs/identification_rescue_2026-11-12/patstat_wo_monthly_raw.json'
bp=ROOT/'outputs/presentation_2026-11-13/data/patstat_pilot_final.json'
r=json.loads(rp.read_text(encoding='utf-8'));p=json.loads(bp.read_text(encoding='utf-8'))
classes=['C12N','G01S','G06F','G06N','H01L'];countries=['CN','US','JP','KR','DE']
brows={x['cls']:x for x in p['raw']['PILOT_TRIMMED_AGGREGATES']}
months=r['panel']['months'];window=np.array([m in ['2018-12','2019-01','2019-02','2019-03','2019-04'] for m in months],float)
n=np.array([[r['panel']['series'][k+'_'+c] for k in classes] for c in countries],float)
assert n.shape==(5,5,84) and int(n.sum())==202110
log_observed_rate=np.log(n+0.5) # an admissible saturated witness, not an estimated true rate
out={'scope':'constructive counterexample, not synthetic evidence of an actual effect','observed_cells':int(n.size),'theta_unit':'log conditional mean count per +10pp B, restricted to the candidate five-month window; not the observed log(1+count) projection coefficient','saturated_witness_rate':'observed count+0.5; chosen only to give a positive probability to every observed nonnegative integer, not fitted/validated','model_class':'A chosen common conditionally independent product-Poisson joint law across cells, only as an admissible witness submodel; not a claim that real IPC/family counts are independent. Unrestricted China x technology x time counterfactual log-rate offset; same observable covariates and fixed B in all scenarios. Marginal equality alone would not prove equality for arbitrary distinct dependence structures.','definitions':{},'source_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [rp,bp]},'causal_identification':False,'actual_China_policy_mechanism_verified':False}
for definition,num,den in [('ALL','us_fractional_pairs','known_country_pairs'),('APP','applicant_us_fractional_pairs','applicant_known_pairs')]:
 b=np.array([brows[k][num]/brows[k][den] for k in classes]);x=np.zeros_like(n);x[0]=b[:,None]/.10*window[None,:]
 observable_projection=[];scenarios=[]
 for theta in [-0.20,0.0,0.20]:
  baseline=log_observed_rate-theta*x
  observed_log=baseline+theta*x
  observed_rate=np.exp(observed_log);counterfactual=np.exp(baseline)
  ll=math.fsum(float(y*z-mu-math.lgamma(y+1)) for y,z,mu in zip(n.ravel(),observed_log.ravel(),observed_rate.ravel()))
  actual=np.log1p(n)
  rel=actual[0]-actual[1:].mean(axis=0);z=b/.10;z=z-z.mean();slope=z@rel/(z@z)
  contrast=float(slope[window.astype(bool)].mean()-slope[48:60].mean())
  observable_projection.append(contrast)
  scenarios.append({'theta':theta,'counterfactual_log_rate_offset':'log(observed count+0.5)-theta*China*(B/.10)*candidate_window','observed_rate_max_abs_difference':float(np.max(np.abs(observed_rate-(n+.5)))),'observed_log_likelihood':ll,'candidate_CN_mean_counterfactual_rate':float(counterfactual[0,:,window.astype(bool)].mean()),'counterfactual_rate_CN_range':[float(counterfactual[0].min()),float(counterfactual[0].max())],'observed_projection_contrast':contrast,'preperiod_counterfactual_rate_max_difference':float(np.max(np.abs(counterfactual[:,:,:60]-(n[:,:,:60]+.5))))})
 assert max(abs(s['observed_projection_contrast']-observable_projection[0]) for s in scenarios)==0
 assert max(s['observed_rate_max_abs_difference'] for s in scenarios)<1e-9
 assert max(s['preperiod_counterfactual_rate_max_difference'] for s in scenarios)<1e-9
 assert max(s['observed_log_likelihood'] for s in scenarios)-min(s['observed_log_likelihood'] for s in scenarios)<1e-8
 out['definitions'][definition]={'B':dict(zip(classes,b.tolist())),'scenarios':scenarios,'likelihood_max_min_difference':max(s['observed_log_likelihood'] for s in scenarios)-min(s['observed_log_likelihood'] for s in scenarios)}
out['interpretation']='Observable laws coincide; any test/estimator using only this observable dataset has the same sampling distribution in all three scenarios. Counterfactual count rates, and therefore E[log(1+count)] by strict stochastic monotonicity of Poisson means, differ. Sign of the causal response is not identified in this unrestricted-shock class. Strong parallel trends or an independent valid variation could exclude scenarios, but those restrictions do not follow from this exercise or from passing pretrend tests.'
(HERE/'nonidentification_witness.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cells':out['observed_cells'],'ALL':out['definitions']['ALL']['scenarios'],'APP':out['definitions']['APP']['scenarios']},ensure_ascii=False))
