"""Separate arithmetic checker; does not import producer script or change sources."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
out = json.loads((HERE/'falsification_results.json').read_text(encoding='utf-8'))
raw = json.loads((ROOT/'outputs/identification_rescue_2026-11-12/patstat_wo_monthly_raw.json').read_text(encoding='utf-8'))
pilot = json.loads((ROOT/'outputs/presentation_2026-11-13/data/patstat_pilot_final.json').read_text(encoding='utf-8'))
classes = ['C12N', 'G01S', 'G06F', 'G06N', 'H01L']
countries = ['CN', 'US', 'JP', 'KR', 'DE']
months = raw['panel']['months']
rows = {r['cls']: r for r in pilot['raw']['PILOT_TRIMMED_AGGREGATES']}
checks = []

def check(name, a, b):
    error = float(np.max(np.abs(np.asarray(a, float)-np.asarray(b, float))))
    assert error < 1e-11, (name, error)
    checks.append({'name': name, 'max_abs_error': error})

def coefficients(country, definition, anchor=None):
    other = [c for c in countries if c != country] if anchor is None else [anchor]
    yy = np.array([[math.log1p(raw['panel']['series'][j+'_'+country][t])-
                    np.mean([math.log1p(raw['panel']['series'][j+'_'+c][t]) for c in other])
                    for j in classes] for t in range(84)])
    if definition == 'ALL':
        bb = [rows[j]['us_fractional_pairs']/rows[j]['known_country_pairs'] for j in classes]
    else:
        bb = [rows[j]['applicant_us_fractional_pairs']/rows[j]['applicant_known_pairs'] for j in classes]
    # Direct unscaled-B least squares rather than centered projection weights.
    XX = np.column_stack([np.ones(5), bb])
    return np.linalg.lstsq(XX, yy.T, rcond=None)[0][1]*.1

for d in ['ALL', 'APP']:
    ss = coefficients('CN', d)
    check(d+' monthly direct OLS', ss, out['results'][d]['monthly_slope_per10pp'])
    for focal in countries:
        ss2 = coefficients(focal, d)
        actual = ss2[71:76].mean()-ss2[48:60].mean()
        check(d+' '+focal+' original', actual, out['country_placebo'][d][focal+'_remaining4']['original_2017_mean'])
    for geom in ['same_baseline_gap', 'immediate_prior12']:
        records = out['results'][d]['fake_windows_'+geom]['records']
        expected_n = 33 if geom == 'same_baseline_gap' else 44
        assert len(records) == expected_n
        for record in records:
            start = months.index(record['window_start'])
            b0 = months.index(record['baseline_start'])
            b1 = months.index(record['baseline_end'])+1
            assert b1-b0 == 12 and start+4 < 60
            check(d+' '+geom+' '+record['window_start'], ss[start:start+5].mean()-ss[b0:b1].mean(), record['contrast'])
    theta = out['results'][d]['original_2017_mean']
    for interval in out['bias_breakdown'][d]['intervals']:
        check(d+' conditional endpoints', [theta-interval['kappa'], theta+interval['kappa']], [interval['lower'], interval['upper']])
    for sim in out['simulation'][d]['scenarios']:
        assert sim['calibrated_absolute_critical_value'] > 0
        assert .045 < sim['independent_evaluation_size'] < .055
        assert all(0 <= sim[k] <= 1 for k in ['power_positive5pct', 'power_negative5pct', 'power_positive10pct', 'power_negative10pct'])
        assert sim['power_positive10pct'] >= sim['power_positive5pct']
        assert sim['power_negative10pct'] >= sim['power_negative5pct']
    # Homogeneous-noise scenarios must scale MDE exactly in log units.
    for model in out['simulation']['assumptions']['models']:
        scenarios = [r for r in out['simulation'][d]['scenarios'] if r['noise_model'] == model]
        ratios = [r['MDE80_log_per10pp_both_directions']/r['residual_scale'] for r in scenarios]
        check(d+' '+model+' MDE homogeneity', ratios, [ratios[0]]*3)

for relpath, digest in out['sha256'].items():
    assert hashlib.sha256((ROOT/relpath).read_bytes()).hexdigest() == digest, relpath
report = {'status': 'passed', 'scope': 'direct OLS and window/interval arithmetic; simulation internal invariants; source checksums',
          'not_verified': ['database return or individual families', 'causal identification', 'truth of simulation DGP', 'B measurement uncertainty'],
          'n_numeric_checks': len(checks), 'max_abs_error': max(c['max_abs_error'] for c in checks),
          'checks': checks}
(HERE/'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in report.items() if k != 'checks'}, ensure_ascii=False))
