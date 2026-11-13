"""Independent witness recalculation; does not import/execute producer code.

Read fixed raw files, solve monthly projections by least squares, evaluate
Poisson probabilities with scipy, and compare producer JSON only at the end.
No source data are changed. Results are printed, not written to source paths.
"""
from pathlib import Path
import hashlib, json, math, sys
import numpy as np
from scipy.stats import poisson
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[3]

def read(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

def digest(rel):
    return hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

def expectation_log1p(rate):
    # Finite sum with omitted Poisson upper-tail probability < 1e-13.
    stop=int(poisson.ppf(1-1e-13,rate))+1
    support=np.arange(stop+1)
    return float(np.dot(np.log1p(support),poisson.pmf(support,rate)))

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    rawpath='outputs/identification_rescue_2026-11-12/patstat_wo_monthly_raw.json'
    bpath='outputs/presentation_2026-11-13/data/patstat_pilot_final.json'
    r=read(rawpath);bdata=read(bpath)
    cc=('CN','US','JP','KR','DE');kk=('C12N','G01S','G06F','G06N','H01L')
    dates=r['panel']['months']
    # Build a row table first, avoiding producer's array construction/indexing.
    rows=[(c,k,m,int(r['panel']['series'][k+'_'+c][j]))
          for c in cc for k in kk for j,m in enumerate(dates)]
    observed=np.array([row[3] for row in rows],dtype=float)
    assert len(rows)==2100 and len(set((c,k,t) for c,k,t,n in rows))==2100
    assert all(float(n).is_integer() and n>=0 for n in observed)
    target_dates={'2018-12','2019-01','2019-02','2019-03','2019-04'}
    ref=np.array([t.startswith('2017-') for t in dates])
    win=np.array([t in target_dates for t in dates])
    pred=np.array([t<'2018-12' for c,k,t,n in rows])
    candidates=np.array([c=='CN' and t in target_dates for c,k,t,n in rows])
    nominal=observed+0.5
    bmap={row['cls']:row for row in bdata['raw']['PILOT_TRIMMED_AGGREGATES']}
    result={'observed_cells':len(rows),'count_sum':int(observed.sum()),
      'source_sha256':{rawpath:digest(rawpath),bpath:digest(bpath)},
      'product_poisson_joint_law':'independent cells conditional on fixed covariates, chosen as a valid witness submodel',
      'definitions':{}}
    published=read('outputs/final_research/empirics/nonidentification_witness.json')
    for name,nu,de in [('ALL','us_fractional_pairs','known_country_pairs'),
                       ('APP','applicant_us_fractional_pairs','applicant_known_pairs')]:
        dose={k:bmap[k][nu]/bmap[k][de]/0.1 for k in kk}
        exposure=np.array([dose[k] if c=='CN' and t in target_dates else 0.0 for c,k,t,n in rows])
        # Independently fit a 5-row intercept+slope regression each month.
        design=np.column_stack((np.ones(5),[dose[k] for k in kk]))
        monthly=[]
        for j,t in enumerate(dates):
            response=[]
            for k in kk:
                cn=math.log1p(r['panel']['series'][k+'_CN'][j])
                other=math.fsum(math.log1p(r['panel']['series'][k+'_'+c][j]) for c in cc[1:])/4
                response.append(cn-other)
            monthly.append(float(np.linalg.lstsq(design,np.array(response),rcond=None)[0][1]))
        monthly=np.array(monthly)
        contrast=float(monthly[win].mean()-monthly[ref].mean())
        scenarios=[]
        for theta in (-.2,0.,.2):
            offset=np.log(nominal)-theta*exposure
            actual_rate=np.exp(offset+theta*exposure)
            no_signal=np.exp(offset)
            ll=float(poisson.logpmf(observed,actual_rate).sum())
            effect=np.array([expectation_log1p(a)-expectation_log1p(z)
                       for a,z in zip(actual_rate[candidates],no_signal[candidates])])
            old=next(s for s in published['definitions'][name]['scenarios'] if s['theta']==theta)
            current={'theta':theta,'observed_rate_max_abs_difference':float(np.max(abs(actual_rate-nominal))),
              'joint_log_likelihood':ll,'candidate_CN_counterfactual_mean':float(no_signal[candidates].mean()),
              'pre_candidate_baseline_max_abs_difference':float(np.max(abs(no_signal[pred]-nominal[pred]))),
              'all_offwindow_or_nonCN_max_abs_difference':float(np.max(abs(no_signal[~candidates]-nominal[~candidates]))),
              'observed_projection_contrast':contrast,
              'candidate_Elog1p_causal_difference_range':[float(effect.min()),float(effect.max())],
              'theta_display_expected_log1p_dose_slope':float(np.linalg.lstsq(design,effect.reshape(5,5).mean(axis=1),rcond=None)[0][1]),
              'matches_published_json':abs(ll-old['observed_log_likelihood'])<1e-8
                 and abs(contrast-old['observed_projection_contrast'])<1e-12
                 and abs(float(no_signal[candidates].mean())-old['candidate_CN_mean_counterfactual_rate'])<1e-9}
            assert current['matches_published_json']
            assert current['observed_rate_max_abs_difference']<1e-9
            assert current['all_offwindow_or_nonCN_max_abs_difference']<1e-9
            if theta<0:assert np.all(effect<0)
            if theta>0:assert np.all(effect>0)
            if theta==0:assert np.max(abs(effect))<1e-12
            scenarios.append(current)
        # Additional exact-log1p-scale witness, distinct from the theta display.
        ix=np.flatnonzero(candidates)
        gx=np.array([expectation_log1p(nominal[i]) for i in ix])
        astar=float(.25*np.min(gx/exposure[ix]))
        inverse_cases=[]
        for a in (-astar,0.,astar):
            targets=gx-a*exposure[ix]
            assert np.all(targets>0)
            baseline_rates=[]
            for value,start in zip(targets,nominal[ix]):
                upper=max(1.,float(start))
                while expectation_log1p(upper)<value:upper*=2
                baseline_rates.append(brentq(lambda v:expectation_log1p(v)-value,0.,upper,xtol=1e-10))
            attained=gx-np.array([expectation_log1p(v) for v in baseline_rates])
            residual=float(np.max(abs(attained-a*exposure[ix])))
            # Candidate rows are technology-major with five repeated months.
            effect_slope=float(np.linalg.lstsq(design,attained.reshape(5,5).mean(axis=1),rcond=None)[0][1])
            assert residual<1e-8 and abs(effect_slope-a)<1e-8
            inverse_cases.append({'a':a,'minimum_target_Elog1p':float(targets.min()),
                'max_Elog1p_effect_minus_aX':residual,'causal_expected_log1p_dose_slope':effect_slope,
                'observed_rate_law':'same fixed nominal rate in every case'})
        result['definitions'][name]={'B':{k:dose[k]*.1 for k in kk},'scenarios':scenarios,
             'exact_log1p_inverse_witness':{'symmetric_a_bound':astar,'scenarios':inverse_cases},
             'likelihood_max_min_difference':max(s['joint_log_likelihood'] for s in scenarios)-min(s['joint_log_likelihood'] for s in scenarios)}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
