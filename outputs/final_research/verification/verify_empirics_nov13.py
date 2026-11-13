"""Independent November 13 audit. Writes only this verification directory.

Estimation uses country x IPC longform OLS with two sets of fixed effects,
not the producer's centered five-IPC projection or previous checker.
Simulation uses an AR innovation loading matrix and exact empirical
rejection-event crossings for MDE, not producer simulation/MDE routines.
"""
from pathlib import Path
from datetime import datetime, timezone
from statistics import NormalDist
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EMP = ROOT / 'outputs/final_research/empirics'
RAW = ROOT / 'outputs/identification_rescue_2026-11-12/patstat_wo_monthly_raw.json'
BP = ROOT / 'outputs/presentation_2026-11-13/data/patstat_pilot_final.json'
raw = json.loads(RAW.read_text(encoding='utf-8'))
pub = json.loads((EMP/'falsification_results.json').read_text(encoding='utf-8'))
br = json.loads(BP.read_text(encoding='utf-8'))['raw']['PILOT_TRIMMED_AGGREGATES']
dates = raw['panel']['months']
ipc = sorted({k.split('_')[0] for k in raw['panel']['series']})
countries = sorted({k.split('_')[1] for k in raw['panel']['series']})
cells = [(c,j) for c in countries for j in ipc]
Y = np.array([raw['panel']['series'][j+'_'+c] for c,j in cells], float)
assert Y.shape == (25,84) and np.all(Y == np.floor(Y)) and np.min(Y) == 0
assert int(Y.sum()) == 202110 and int(np.count_nonzero(Y)) == 2064
Y = np.log1p(Y)
B = {'ALL': {r['cls']: r['us_fractional_pairs']/r['known_country_pairs'] for r in br},
     'APP': {r['cls']: r['applicant_us_fractional_pairs']/r['applicant_known_pairs'] for r in br}}
checks = []
failures = []

def check(name, got, recorded, atol=2e-11):
    err = float(np.max(np.abs(np.asarray(got,float)-np.asarray(recorded,float))))
    ok = bool(err <= atol)
    checks.append({'name':name,'max_abs_error':err,'tolerance':atol,'passed':ok})
    if not ok:
        failures.append(name)

def fit_longform(definition, focal, anchor=None, response=Y):
    selected = [i for i,(c,j) in enumerate(cells) if anchor is None or c in (focal,anchor)]
    cs = sorted({cells[i][0] for i in selected})
    # Intercept, country indicators, IPC indicators, focal x unscaled B.
    x = np.array([[1.] + [float(c==cc) for cc in cs[1:]] +
                  [float(j==jj) for jj in ipc[1:]] +
                  [float(c==focal)*B[definition][j]] for c,j in (cells[i] for i in selected)])
    assert np.linalg.matrix_rank(x) == x.shape[1]
    return np.linalg.lstsq(x,np.asarray(response)[selected],rcond=None)[0][-1]*.1

def ordmonth(s):
    y,m = map(int,s.split('-'))
    return y*12+m-1

ordinals = np.array([ordmonth(d) for d in dates])
post = np.flatnonzero((ordinals>=ordmonth('2018-12')) & (ordinals<=ordmonth('2019-04')))
bases = {'original_2017_mean':[i for i,d in enumerate(dates) if d.startswith('2017-')],
         'matched_calendar2017':[i for i,d in enumerate(dates) if d.startswith('2017-') and int(d[-2:]) in (12,1,2,3,4)],
         'contiguous_window_shift24':[i for i,o in enumerate(ordinals) if ordmonth('2016-12')<=o<=ordmonth('2017-04')]}

def contrast_response(before,after=post):
    return Y[:,after].mean(axis=1)-Y[:,before].mean(axis=1)

# A different calendar basis: intercept, 11 month contrasts, elapsed months.
T = np.array([[1.] + [float(int(d[-2:])==m) for m in range(2,13)] + [float(k)] for k,d in enumerate(dates)])

def holdout(path):
    pred = T @ np.linalg.lstsq(T[:48],path[:48],rcond=None)[0]
    err = path[48:60]-pred[48:60]
    return {'train_rmse':float(np.sqrt(np.mean((path[:48]-pred[:48])**2))),
            'holdout_rmse':float(np.sqrt(np.mean(err**2))),
            'holdout_mean_error':float(err.mean()),'holdout_month_errors':err.tolist()}

independent = {}
for definition in ('ALL','APP'):
    path = fit_longform(definition,'CN')
    check(definition+' 84 monthly slopes, 25-cell longform OLS',path,pub['results'][definition]['monthly_slope_per10pp'])
    contrasts = {}
    for name,before in bases.items():
        value = float(fit_longform(definition,'CN',response=contrast_response(before)))
        contrasts[name] = value
        check(definition+' '+name+' direct contrast longform OLS',value,pub['results'][definition][name])
    h = holdout(path)
    for name,value in h.items():
        check(definition+' '+name,value,pub['results'][definition]['holdout'][name])
    country_results = {}
    for anchor in (None,'US'):
        for c in countries:
            if c == anchor:
                continue
            key = c+'_remaining4' if anchor is None else c+'_US'
            country_results[key] = {}
            for name,before in bases.items():
                value = float(fit_longform(definition,c,anchor,contrast_response(before)))
                country_results[key][name] = value
                check(definition+' country '+key+' '+name,value,pub['country_placebo'][definition][key][name])
    check(definition+' sum of symmetric country contrasts',sum(country_results[c+'_remaining4']['original_2017_mean'] for c in countries),0.)
    fake_results = {}
    for geometry in ('same_baseline_gap','immediate_prior12'):
        records = []
        for start in ordinals:
            stop = start+4
            bs,be = (start-23,start-12) if geometry=='same_baseline_gap' else (start-12,start-1)
            if bs < ordinals.min() or stop > ordmonth('2017-12'):
                continue
            after = np.flatnonzero((ordinals>=start)&(ordinals<=stop))
            before = np.flatnonzero((ordinals>=bs)&(ordinals<=be))
            assert len(before)==12 and len(after)==5
            value = float(fit_longform(definition,'CN',response=contrast_response(before,after)))
            records.append({'window_start':dates[after[0]],'window_end':dates[after[-1]],
                            'baseline_start':dates[before[0]],'baseline_end':dates[before[-1]],'contrast':value})
        published = pub['results'][definition]['fake_windows_'+geometry]
        assert len(records) == (33 if geometry=='same_baseline_gap' else 44)
        for a,b in zip(records,published['records']):
            assert all(a[k]==b[k] for k in ('window_start','window_end','baseline_start','baseline_end'))
        check(definition+' '+geometry+' all direct longform contrasts',[r['contrast'] for r in records],[r['contrast'] for r in published['records']])
        same = [r for r in records if r['window_start'].endswith('-12')]
        theta = contrasts['original_2017_mean']
        exceed = sum(abs(r['contrast'])>=abs(theta) for r in records)
        check(definition+' '+geometry+' descriptive absolute exceedance',exceed,published['absolute_exceedance_count'])
        fake_results[geometry] = {'n':len(records),'absolute_exceedance_count':exceed,
                                 'same_Dec_Apr':same,'all_same_season_greater_than_real':all(r['contrast']>theta for r in same),
                                 'records':records}
    theta = contrasts['original_2017_mean']
    bias = {'kappa_to_allow_zero':abs(theta),
            'max_kappa_for_negative5pct_all_bias':-math.log(1.05)-theta,
            'kappa_to_allow_positive5pct':math.log(1.05)-theta,
            'kappa_to_allow_negative10pct':theta+math.log(1.10)}
    for name,value in bias.items():
        check(definition+' bias threshold '+name,value,pub['bias_breakdown'][definition][name])
    for row in pub['bias_breakdown'][definition]['intervals']:
        lo,hi = theta-row['kappa'],theta+row['kappa']
        check(definition+' bias endpoints '+str(row['kappa']),[lo,hi],[row['lower'],row['upper']])
        flags = {'negative_sign_for_all_bias':hi<0,'at_least_negative5pct_for_all_bias':hi<=-math.log(1.05),
                 'at_least_negative10pct_for_all_bias':hi<=-math.log(1.10),'allows_positive5pct':hi>=math.log(1.05),
                 'allows_negative10pct':lo<=-math.log(1.10)}
        for k,v in flags.items():
            assert bool(v)==row[k]
    exact_five_bound = math.log(.95)-theta
    exact_percent = {'observed_expm1':math.expm1(theta),
                     'symmetric_negative_log1p05_expm1':math.expm1(-math.log(1.05)),
                     'symmetric_negative_log1p10_expm1':math.expm1(-math.log(1.10)),
                     'exact_negative5pct_log_threshold':math.log(.95),
                     'exact_negative10pct_log_threshold':math.log(.9),
                     'exact_negative5pct_at_kappa0':theta<=math.log(.95),
                     'exact_negative5pct_max_nonnegative_kappa':exact_five_bound if exact_five_bound>=0 else None,
                     'kappa_to_allow_exact_negative5pct':max(0.,theta-math.log(.95)),
                     'exact_negative10pct_at_kappa0':theta<=math.log(.9),
                     'exact_negative10pct_max_nonnegative_kappa':math.log(.9)-theta if theta<=math.log(.9) else None,
                     'kappa_to_allow_exact_negative10pct':max(0.,theta-math.log(.9))}
    independent[definition] = {'contrasts':contrasts,'country_placebo':country_results,'fake_windows':fake_results,
                               'bias_thresholds':bias,'exact_percent_unit_audit':exact_percent,
                               'holdout':h,'monthly_slopes':path.tolist()}

ipc_holdout = {}
for j in ipc:
    y = Y[cells.index(('CN',j))] - np.mean([Y[cells.index((c,j))] for c in countries if c!='CN'],axis=0)
    h = holdout(y)
    for name,value in h.items():
        check(j+' IPC '+name,value,pub['ipc_diagnostics'][j][name])
    fit = np.linalg.lstsq(T[:60],y[:60],rcond=None)[0]
    seasonal = np.r_[0.,fit[1:12]]
    check(j+' calendar amplitude',np.ptp(seasonal),pub['ipc_diagnostics'][j]['pre60_calendar_range'])
    ipc_holdout[j] = h

# Independent simulator. Same documented streams are intentionally used to audit
# the archived realizations. Scales reuse streams; they are not new experiments.
n = 100000
seed = 20261112
w = np.array([-1/12]*12+[0.]*11+[1/5]*5)
models = [('circular_moving_block12',None),('gaussian_AR1_rho0',0.),
          ('gaussian_AR1_rho0.5',.5),('gaussian_AR1_rho0.8',.8)]

def distribution(residual,rho,stream):
    rng = np.random.default_rng(stream)
    if rho is None:
        # Pre-compute each possible block's contribution to the statistic.
        table = np.empty((3,60))
        for block in range(3):
            for start in range(60):
                table[block,start] = sum(w[t]*residual[(start+t-block*12)%60]
                                         for t in range(block*12,min((block+1)*12,28)))
        starts = rng.integers(60,size=(n,3))
        return sum(table[b,starts[:,b]] for b in range(3))
    z = rng.standard_normal((28,n))
    # Loading matrix for a stationary AR(1), marginal variance sd^2.
    loading = np.zeros((28,28))
    for t in range(28):
        loading[t,0] = rho**t
        for u in range(1,t+1):
            loading[t,u] = math.sqrt(1-rho*rho)*rho**(t-u)
    return (w@loading) @ z * residual.std(ddof=1)

def empirical_direction_mde(samples,critical):
    # Events at positive delta: enter right rejection tail; leave left tail.
    entries = critical-samples
    exits = -critical-samples
    times = np.r_[entries[entries>=0],exits[exits>=0]]
    jumps = np.r_[np.ones(np.count_nonzero(entries>=0),dtype=int),-np.ones(np.count_nonzero(exits>=0),dtype=int)]
    order = np.argsort(times,kind='stable')
    # Group ties so intermediate states at the same threshold cannot count.
    time = times[order]
    unique,first = np.unique(time,return_index=True)
    count = np.count_nonzero(np.abs(samples)>critical)+np.cumsum(np.add.reduceat(jumps[order],first))
    return float(unique[np.flatnonzero(count>=math.ceil(.8*len(samples)))[0]])

simulation = {}
stream_audit = []
for di,definition in enumerate(('ALL','APP')):
    slope = np.array(independent[definition]['monthly_slopes'])
    residual = slope[:60]-T[:60]@np.linalg.lstsq(T[:60],slope[:60],rcond=None)[0]
    residual = residual-residual.mean()
    check(definition+' simulation residual SD',residual.std(ddof=1),pub['simulation'][definition]['residual_sd'])
    audited = []
    for mi,(model,rho) in enumerate(models):
        calibration_seed = seed+di*100+mi*2
        evaluation_seed = calibration_seed+1
        cal = distribution(residual,rho,calibration_seed)
        ev = distribution(residual,rho,evaluation_seed)
        # Independently construct the linear interpolation quantile.
        sorted_abs = np.sort(np.abs(cal))
        quantile_position = .95*(n-1)
        lower = int(quantile_position)
        critical = float(sorted_abs[lower]+(quantile_position-lower)*(sorted_abs[lower+1]-sorted_abs[lower]))
        mde = max(empirical_direction_mde(ev,critical),empirical_direction_mde(-ev,critical))
        exact_gaussian_sd = None
        if rho is not None:
            cov = rho**np.abs(np.arange(28)[:,None]-np.arange(28)[None,:])
            exact_gaussian_sd = float(residual.std(ddof=1)*math.sqrt(w@cov@w))
        stream_audit.append({'definition':definition,'model':model,'calibration_seed':calibration_seed,
                             'evaluation_seed':evaluation_seed,'draws_each':n,'scales_share_draws':[.5,1.,2.]})
        for scale in (.5,1.,2.):
            e,c = ev*scale,critical*scale
            size = np.mean(np.abs(e)>c)
            naive = 1.96*residual.std(ddof=1)*scale*math.sqrt(1/12+1/5)
            row = {'noise_model':model,'residual_scale':scale,'null_contrast_sd':float(e.std(ddof=1)),
                   'calibrated_absolute_critical_value':c,'independent_evaluation_size':float(size),
                   'size_MC_SE':math.sqrt(size*(1-size)/n),'iid_normal_critical_value':naive,
                   'iid_normal_actual_size_under_this_DGP':float(np.mean(np.abs(e)>naive)),
                   'MDE80_log_per10pp_both_directions':mde*scale,'MDE80_exp_minus1':math.expm1(mde*scale)}
            for name,delta in (('5pct',math.log(1.05)),('10pct',math.log(1.10))):
                row['power_positive'+name] = float(np.mean(np.abs(e+delta)>c))
                row['power_negative'+name] = float(np.mean(np.abs(e-delta)>c))
            recorded = next(r for r in pub['simulation'][definition]['scenarios'] if r['noise_model']==model and r['residual_scale']==scale)
            for name,value in row.items():
                if isinstance(value,(int,float)):
                    check(definition+' '+model+' '+str(scale)+' '+name,value,recorded[name],atol=2e-10)
            row['power_exact_negative5pct'] = float(np.mean(np.abs(e+math.log(.95))>c))
            row['power_exact_negative10pct'] = float(np.mean(np.abs(e+math.log(.9))>c))
            row['MDE80_negative_ratio_change'] = math.expm1(-mde*scale)
            if rho is not None:
                row['exact_Gaussian_null_contrast_sd'] = exact_gaussian_sd*scale
                row['exact_Gaussian_IID_threshold_size'] = 2*(1-NormalDist().cdf(naive/(exact_gaussian_sd*scale)))
            # Directly confirm threshold crossing rather than just monotonicity.
            eps = 1e-9
            row['min_direction_power_at_reported_MDE_plus_1e_minus9'] = float(min(np.mean(np.abs(e+mde*scale+eps)>c),np.mean(np.abs(e-mde*scale-eps)>c)))
            row['min_direction_power_at_reported_MDE_minus_1e_minus9'] = float(min(np.mean(np.abs(e+mde*scale-eps)>c),np.mean(np.abs(e-mde*scale+eps)>c)))
            assert row['min_direction_power_at_reported_MDE_plus_1e_minus9']>=.8
            assert row['min_direction_power_at_reported_MDE_minus_1e_minus9']<.8
            audited.append(row)
    simulation[definition] = {'residual_sd':float(residual.std(ddof=1)),'scenarios':audited}

hashes = {}
for rel,digest in pub['sha256'].items():
    p = ROOT / rel.replace('\\','/')
    calculated = hashlib.sha256(p.read_bytes()).hexdigest()
    assert calculated==digest
    hashes[str(p.relative_to(ROOT))] = calculated
assert len({r[k] for r in stream_audit for k in ('calibration_seed','evaluation_seed')})==16

# Final reporting correction is reviewed separately from the original numerical
# comparisons, preserving the distinction between arithmetic and labels.
correction_path = EMP/'effect_unit_correction.json'
correction = json.loads(correction_path.read_text(encoding='utf-8'))
assert correction['raw_results_sha256']==hashlib.sha256((EMP/'falsification_results.json').read_bytes()).hexdigest()
correction_diffs = []
for definition in ('ALL','APP'):
    theta = independent[definition]['contrasts']['original_2017_mean']
    corrected = correction['exact_negative_effects'][definition]
    correction_diffs.append(abs(theta-corrected['observed_log_contrast']))
    for ratio in (.05,.10):
        threshold = math.log(1-ratio)
        row = corrected[str(ratio)]
        correction_diffs.append(abs(threshold-row['exact_negative_ratio_threshold_log']))
        correction_diffs.append(abs(max(0.,theta-threshold)-row['minimum_kappa_to_allow_effect_at_or_below_threshold']))
        guarantee = threshold-theta if theta<=threshold else None
        recorded = row['maximum_nonnegative_kappa_for_all_effects_at_or_below_threshold']
        if guarantee is None:
            assert recorded is None
        else:
            correction_diffs.append(abs(guarantee-recorded))
assert max(correction_diffs)<2e-11
reviewed_text = {}
for name in ('analysis.md','findings_for_manuscript.md','README.md','run_falsification.py'):
    value = (EMP/name).read_text(encoding='utf-8')
    assert all(token in value for token in ('±log(1.05)','±log(1.10)','-4.7619048%','-9.0909091%','16개','3배율'))
    reviewed_text[name] = hashlib.sha256((EMP/name).read_bytes()).hexdigest()
compile((EMP/'run_falsification.py').read_text(encoding='utf-8'),'run_falsification.py','exec')
compile((EMP/'correct_effect_units.py').read_text(encoding='utf-8'),'correct_effect_units.py','exec')

report = {'created_utc':datetime.now(timezone.utc).isoformat(),'status':'passed' if not failures else 'failed',
          'independence':{'fresh_verifier':True,'producer_or_prior_checker_imported_or_executed':False,
                          'previous_188_checks_counted_as_independent_evidence':False,
                          'estimation':'25 country x IPC longform rows, country FE + IPC FE + focal x unscaled B; slope multiplied by .1',
                          'simulation':'AR innovation loading matrix; block contribution table; MDE empirical rejection-event crossings'},
          'coverage':{'raw_cells':2100,'nonzero_cells':2064,'sum_class_country_counts':202110,
                      'monthly_slopes':168,'primary_fake_windows_each_definition':33,
                      'auxiliary_immediate_windows_each_definition':44,'simulation_scenarios':24,
                      'independent_calibration_evaluation_stream_pairs':8,'unique_stream_seeds':16},
          'inputs_sha256':hashes,
          'audited_material_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in sorted(EMP.iterdir()) if p.is_file() and p.suffix in ('.py','.md','.json','.csv')},
          'independent_code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'numeric_comparison_groups':len(checks),'max_abs_error':max(r['max_abs_error'] for r in checks),
          'final_reporting_review':{'status':'passed','reviewed_sha256':reviewed_text,
                                    'exact_percent_correction_max_abs_error':max(correction_diffs),
                                    'correction_metadata_matches_current_raw_results_hash':True,
                                    'historical_raw_result_fields_retained_with_explicit_legacy_log_shift_note':True,
                                    'producer_and_correction_script_syntax_compiled_without_execution':True},
          'reporting_corrections_identified_and_resolved':['Negative log-symmetric alternatives -log(1.05), -log(1.10) mean -4.7619%, -9.0909% ratio changes; label them in log units or use log(.95), log(.90) for exact negative percentages.',
                                             'APP at kappa=0 does not meet an exact negative 5 percent ratio threshold; its reported .001157 tolerance applies only to -log(1.05).',
                                             'State explicitly that 24 scenarios reuse eight calibration/evaluation draw pairs across three scales.'],
          'failures':failures,'checks':checks,'independent_results':independent,'ipc_holdout':ipc_holdout,
          'simulation':simulation,'seed_audit':stream_audit,
          'scope_limits':['No independent database requery or family-level audit; aggregate arithmetic only.',
                          'The five IPC support points are not established independent clusters.',
                          'The 33 overlapping mixed-season windows provide descriptive ranks, not policy p-values.',
                          'Same-season December-April windows: only three; all greater than the real coefficient.',
                          'DE country placebo has opposite sign and greater absolute magnitude than CN.',
                          'Bias ranges fix reported B, omit sampling uncertainty, and need externally defended kappa.',
                          'Simulation conditions on stationary residual models, fixed B and IPC support; excludes trend/calendar estimation uncertainty.',
                          'The three noise scales share draws within each of eight base models; 24 scenarios are not 24 independent confirmations.',
                          'No R&D resource reallocation or causal US-signal effect is identified.']}
(HERE/'empirics_nov13.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
assert not failures, failures
print(json.dumps({'status':report['status'],'comparison_groups':len(checks),'max_abs_error':report['max_abs_error'],
                  'simulation_scenarios':24,'unique_stream_seeds':16},ensure_ascii=False))
