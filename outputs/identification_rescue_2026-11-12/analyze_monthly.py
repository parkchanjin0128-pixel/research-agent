"""Exploratory diagnostics, not a causal policy estimator. NumPy only."""
from pathlib import Path
import json, hashlib, math
import numpy as np

HERE=Path(__file__).resolve().parent
PILOT=HERE.parent/'presentation_2026-11-13/data/patstat_pilot_final.json'
raw_bytes=(HERE/'patstat_wo_monthly_raw.json').read_bytes()
assert hashlib.sha256(raw_bytes).hexdigest()=='8dcc8869d46c636174b200dc2b82c6ff399dd38a4016eb0d445ec279069fc9f0'
raw=json.loads(raw_bytes)
p=raw['panel']; months=p['months']; series=p['series']
classes=['C12N','G01S','G06F','G06N','H01L']; controls=['US','JP','KR','DE']
assert len(months)==84 and len(series)==25
assert all(len(v)==84 and all(isinstance(x,int) and x>=0 for x in v) for v in series.values())
assert sum(sum(v) for v in series.values())==p['sum_class_country_families']==202110
assert sum(sum(x>0 for x in v) for v in series.values())==p['nonzero_rows']==2064
dose_rows=json.loads(PILOT.read_text(encoding='utf-8'))['raw']['PILOT_TRIMMED_AGGREGATES']
dose={r['cls']:{'ALL':r['us_fractional_pairs']/r['known_country_pairs'],
                    'APP':r['applicant_us_fractional_pairs']/r['applicant_known_pairs']} for r in dose_rows}
y={c:np.array([series[k+'_'+c] for k in classes],float) for c in ['CN']+controls}
log_y={c:np.log1p(v) for c,v in y.items()}
pre=np.array([m<'2018-01' for m in months]); base=np.array([m.startswith('2017-') for m in months])
window=np.array(['2018-12'<=m<='2019-04' for m in months])
t=np.arange(84)/12
design=np.column_stack([np.ones(84),t]+[(np.arange(84)%12==j).astype(float) for j in range(1,12)])

def slope(v,x):
    z=x-x.mean()
    return z@v/(z@z)

def hac(v,X,lags=12):
    """OLS + Bartlett Newey-West. Conditional 60-month large-T approximation only."""
    n,k=X.shape; inv=np.linalg.inv(X.T@X); b=inv@X.T@v; u=v-X@b; scores=X*u[:,None]
    meat=scores.T@scores
    for h in range(1,min(lags,n-1)+1):
        cross=scores[h:].T@scores[:-h]; meat+=(1-h/(lags+1))*(cross+cross.T)
    cov=inv@meat@inv*n/(n-k)
    se=math.sqrt(max(float(cov[1,1]),0))
    z=float(b[1]/se) if se else None
    return {'slope_per_year_per_10pp':float(b[1]),'hac_se_lag12':se,
            'normal_approx_p':math.erfc(abs(z)/math.sqrt(2)) if z is not None else None,
            'n_months':n,'n_regressors':k,
            'interpretation':'conditional time-series trend diagnostic; not valid causal inference; ignores estimated B uncertainty and cross-IPC population sampling'}

out={'scope':p['scope'],'data_sha256':hashlib.sha256(raw_bytes).hexdigest(),
     'grid_cells':2100,'nonzero_cells':2064,'class_country_family_counts':202110,
     'technical_support_points':5,'baseline':'2017 monthly mean','candidate_window':['2018-12','2019-04'],
     'dose':dose,'results':{},'annual_counts':{},'coverage_compare':raw['coverage_compare'],
     'inference_warning':'5 selected IPCs; no verified untreated placebo; country spillovers; heterogeneous selection; B estimation and historical snapshot uncertainty; no causal confidence interval or policy p-value'}
for c in y:
    out['annual_counts'][c]={k:{str(year):int(y[c][i,(year-2013)*12:(year-2012)*12].sum()) for year in range(2013,2020)} for i,k in enumerate(classes)}
for definition in ['ALL','APP']:
    x=np.array([dose[k][definition]/.1 for k in classes])
    out['results'][definition]={}
    for comparison in ['equal_controls']+controls:
        ctrl=np.mean([log_y[c] for c in controls],axis=0) if comparison=='equal_controls' else log_y[comparison]
        rel=log_y['CN']-ctrl
        s=slope(rel,x)
        beta=s-s[base].mean()
        b=np.linalg.lstsq(design[pre],s[pre],rcond=None)[0]
        pred=design@b
        train=np.array([m<'2017-01' for m in months]); held=base
        b_hold=np.linalg.lstsq(design[train],s[train],rcond=None)[0]
        pred_hold=design@b_hold
        loo={}
        for i,k in enumerate(classes):
            keep=np.arange(5)!=i
            si=slope(rel[keep],x[keep])
            loo[k]=float(si[window].mean()-si[base].mean())
        result={'monthly_relative_slope_per_10pp':[float(v) for v in s],
                'monthly_baseline_normalized_beta':[float(v) for v in beta],
                'annual_beta':{str(year):float(beta[(year-2013)*12:(year-2012)*12].mean()) for year in range(2013,2020)},
                'window_change_per_10pp':float(beta[window].mean()),
                'window_pretrend_extrapolation_residual':float((s-pred)[window].mean()),
                'pretrend':hac(s[pre],design[pre]),
                'heldout_2017_rmse':float(np.sqrt(np.mean((s[held]-pred_hold[held])**2))),
                'heldout_2017_bias':float(np.mean(s[held]-pred_hold[held])),
                'loo_window_change_per_10pp':loo,
                'class_window_relative_log_change':{k:float(rel[i,window].mean()-rel[i,base].mean()) for i,k in enumerate(classes)}}
        out['results'][definition][comparison]=result

(HERE/'monthly_diagnostics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'monthly_query.sql').write_text(raw['monthly_sql']+'\n',encoding='utf-8')
(HERE/'coverage_query.sql').write_text(raw['coverage_sql']+'\n',encoding='utf-8')
for d in ['ALL','APP']:
    r=out['results'][d]['equal_controls']
    print(d,json.dumps({k:r[k] for k in ['annual_beta','window_change_per_10pp','window_pretrend_extrapolation_residual','pretrend','heldout_2017_rmse','loo_window_change_per_10pp']},ensure_ascii=False))
print('COUNTRY_SENSITIVITY',json.dumps({d:{c:out['results'][d][c]['window_change_per_10pp'] for c in ['equal_controls']+controls} for d in ['ALL','APP']}))
