"""Independent raw-panel audit. Does not import or execute producer code.

Fits intercept+unscaled-B OLS to month/country records, and checks window
estimates by first aggregating each IPC's before/after log difference. Trend
HAC is separately implemented with month-demeaned FWL influence weights.
Writes verification.json only. No database query is executed.
"""
from pathlib import Path
import json, hashlib, math
import numpy as np

HERE = Path(__file__).resolve().parent
raw_path = HERE / 'patstat_wo_monthly_raw.json'
raw_bytes = raw_path.read_bytes()
raw = json.loads(raw_bytes)
reported = json.loads((HERE / 'monthly_diagnostics.json').read_text(encoding='utf-8'))
pilot = json.loads((HERE.parent / 'presentation_2026-11-13/data/patstat_pilot_final.json').read_text(encoding='utf-8'))
classes = ['C12N', 'G01S', 'G06F', 'G06N', 'H01L']
countries = ['CN', 'US', 'JP', 'KR', 'DE']
controls = countries[1:]
months = [f'{y}-{m:02d}' for y in range(2013, 2020) for m in range(1, 13)]
panel = raw['panel']
expected_keys = {f'{j}_{c}' for j in classes for c in countries}
assert panel['months'] == months
assert set(panel['series']) == expected_keys
records = {}
for key, values in panel['series'].items():
    assert len(values) == 84
    ipc, country = key.split('_')
    for month, value in zip(months, values):
        assert type(value) is int and value >= 0
        records[ipc, country, month] = value
assert len(records) == 2100
nonzero = sum(v > 0 for v in records.values())
total = sum(records.values())
sha = hashlib.sha256(raw_bytes).hexdigest()
assert nonzero == 2064 and total == 202110
assert sha == '8dcc8869d46c636174b200dc2b82c6ff399dd38a4016eb0d445ec279069fc9f0'
dose = {}
for row in pilot['raw']['PILOT_TRIMMED_AGGREGATES']:
    dose[row['cls']] = {'ALL': row['us_fractional_pairs']/row['known_country_pairs'],
                        'APP': row['applicant_us_fractional_pairs']/row['applicant_known_pairs']}

base = [m for m in months if m[:4] == '2017']
window = [m for m in months if '2018-12' <= m <= '2019-04']
pre = months[:60]
train = months[:48]

def mean(values):
    return float(np.mean(list(values)))

def fit_b(y, selected, definition):
    """Unscaled fraction regressor; output changes for +0.10 B."""
    design = np.array([[1.0, dose[j][definition]] for j in selected])
    return float(np.linalg.lstsq(design, np.array(y), rcond=None)[0][1] * .10)

def seasonal_trend(s, train_length):
    """FWL slope in MONTHS with separate twelve calendar-month intercepts."""
    times = np.arange(train_length, dtype=float)
    values = np.array(s[:train_length], dtype=float)
    month_group = np.arange(train_length) % 12
    avg_t = np.array([times[month_group == k].mean() for k in range(12)])
    avg_y = np.array([values[month_group == k].mean() for k in range(12)])
    tr = times - avg_t[month_group]
    yr = values - avg_y[month_group]
    slope = float(tr @ yr / (tr @ tr))
    intercepts = avg_y - slope * avg_t
    prediction = np.array([intercepts[t % 12] + slope*t for t in range(84)])
    resid = values - prediction[:train_length]
    # Scalar sandwich influence for the partialled-out trend coefficient.
    influence = tr * resid / float(tr @ tr)
    variance = float(influence @ influence)
    for lag in range(1, 13):
        variance += 2*(1-lag/13)*float(influence[lag:] @ influence[:-lag])
    variance *= train_length/(train_length-13)
    annual_se = math.sqrt(max(variance, 0))*12
    annual_slope = slope*12
    return prediction, {'slope_per_year_per_10pp': annual_slope,
                        'hac_se_lag12': annual_se,
                        'normal_approx_p': math.erfc(abs(annual_slope/annual_se)/math.sqrt(2)),
                        'n_months': train_length, 'n_regressors': 13}

comparisons = {}
max_discrepancy = 0.0
checks = []
def check(label, actual, expected):
    global max_discrepancy
    aa, ee = np.asarray(actual, dtype=float), np.asarray(expected, dtype=float)
    err = float(np.max(np.abs(aa-ee)))
    max_discrepancy = max(max_discrepancy, err)
    checks.append({'label': label, 'max_abs_discrepancy': err, 'pass': bool(np.allclose(aa, ee, rtol=1e-9, atol=1e-10))})

for definition in ['ALL', 'APP']:
    comparisons[definition] = {}
    for comparison in ['equal_controls']+controls:
        cc = controls if comparison == 'equal_controls' else [comparison]
        rel = {(j,m): math.log1p(records[j,'CN',m]) - mean(math.log1p(records[j,c,m]) for c in cc)
               for j in classes for m in months}
        change = {j: mean(rel[j,m] for m in window)-mean(rel[j,m] for m in base) for j in classes}
        s = [fit_b([rel[j,m] for j in classes], classes, definition) for m in months]
        # Regress first-differenced IPC outcomes, independently of monthly s.
        normalized = [fit_b([rel[j,m]-mean(rel[j,b] for b in base) for j in classes], classes, definition) for m in months]
        win = fit_b([change[j] for j in classes], classes, definition)
        annual = {str(year): fit_b([mean(rel[j,m] for m in months if m[:4]==str(year))-mean(rel[j,b] for b in base) for j in classes], classes, definition) for year in range(2013,2020)}
        loo = {drop: fit_b([change[j] for j in classes if j != drop], [j for j in classes if j != drop], definition) for drop in classes}
        prediction, trend = seasonal_trend(s, 60)
        hold_prediction, _ = seasonal_trend(s, 48)
        hold_errors = np.array(s[48:60])-hold_prediction[48:60]
        result = {'monthly_relative_slope_per_10pp': s,
                  'monthly_baseline_normalized_beta': normalized,
                  'window_change_per_10pp': win,
                  'annual_beta': annual,
                  'loo_window_change_per_10pp': loo,
                  'class_window_relative_log_change': change,
                  'pretrend': trend,
                  'heldout_2017_rmse': float(np.sqrt(hold_errors @ hold_errors / 12)),
                  'heldout_2017_bias': float(hold_errors.mean()),
                  'window_pretrend_extrapolation_residual': mean(s[i]-prediction[i] for i,m in enumerate(months) if m in window)}
        comparisons[definition][comparison] = result
        rr = reported['results'][definition][comparison]
        for key in ['monthly_relative_slope_per_10pp','monthly_baseline_normalized_beta','window_change_per_10pp','heldout_2017_rmse','heldout_2017_bias','window_pretrend_extrapolation_residual']:
            check(f'{definition}/{comparison}/{key}',result[key],rr[key])
        for key in ['annual_beta','loo_window_change_per_10pp','class_window_relative_log_change','pretrend']:
            for item in result[key]:
                check(f'{definition}/{comparison}/{key}/{item}',result[key][item],rr[key][item])
for c in countries:
    for j in classes:
        for year in range(2013,2020):
            check(f'annual_counts/{c}/{j}/{year}',sum(records[j,c,m] for m in months if m[:4] == str(year)),reported['annual_counts'][c][j][str(year)])
for j in classes:
    for definition in ['ALL','APP']:
        check(f'dose/{j}/{definition}',dose[j][definition],reported['dose'][j][definition])
assert all(c['pass'] for c in checks)

out = {'status': 'verified_for_recorded_aggregate_arithmetic_only',
       'independent_database_query_executed': False,
       'raw_bytes': len(raw_bytes), 'sha256': sha,
       'grid_cells': len(records), 'nonzero_cells': nonzero, 'zero_cells': len(records)-nonzero,
       'sum_of_class_country_family_counts': total,
       'unique_family_count': None,
       'n_ipc_support_points': len(classes), 'dose': dose,
       'verification_method': 'long records; intercept plus unscaled fraction OLS times 0.10; aggregate IPC before-after OLS; month-demeaned scalar FWL HAC in months converted to years',
       'all_arithmetic_checks_pass': True, 'number_of_checks': len(checks),
       'maximum_absolute_discrepancy': max_discrepancy,
       'checks': checks, 'independent_results': comparisons,
       'scope_status': {
          'verified': ['Recorded raw byte hash, grid, integer/nonnegative counts, ALL/APP dose arithmetic, monthly/annual normalization, 10pp scaling, 10 comparison estimates, all 50 LOO estimates, seasonal pretrend HAC lag12, 2017 heldout predictions, annual counts',
                       'Recorded SQL groups by IPC x applicant-address country x DOCDB family before monthly counting; family counts may overlap across countries/classes'],
          'pending': ['Independent database query rerun and database snapshot provenance', 'Global unique family totals or underlying family-level duplicate validation', 'Historical applicant/IPC information available at the 2018 information date', 'Policy clean-window audit and causal identifying restrictions', 'Causal inference for the five selected IPCs and dose-estimation uncertainty'],
          'contradicted': ['p=0.9703 proves parallel trends', 'The recorded SQL performs global family deduplication across IPC classes and applicant countries', 'B is automatically a manipulable policy treatment dose', 'The estimate identifies causal R&D investment reallocation']},
       'primary_sources_checked': [
          {'url':'https://arxiv.org/html/2107.02637v8','version':'v8 metadata 2025-12-31','scope':'intro and identification discussion; ordinary PT does not remove selection across dose groups'},
          {'url':'https://asheshrambachan.github.io/assets/files/hpt-draft.pdf','version':'author draft 2022-04-01','scope':'pp1-4 sensitivity restrictions and uncertainty; not an HonestDiD numerical implementation'},
          {'url':'https://github.com/asheshrambachan/HonestDiD','scope':'author README; robust confidence sets require assumed restrictions and appropriate input covariance'},
          {'url':'https://arxiv.org/abs/2505.09942','version':'latest arXiv v3, 2025-07-18 per version history'},
          {'url':'https://marcelortiz.com/assets/pdf/DDD_OVS.pdf','version':'author PDF cover 2025-07-18','scope':'p4 distinguishes subgroup heterogeneity from double-eligibility DDD'},
          {'url':'https://arxiv.org/html/2505.09942v3','version_caution':'HTML body says 2026-08-24 although arXiv v3 metadata says 2025-07-18'},
          {'url':'https://www.aeaweb.org/articles?id=10.1257/aeri.20210236','scope':'publisher abstract; low pretrend-test power and pretest conditioning distortion'}]}
(HERE/'verification.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:out[k] for k in ['status','raw_bytes','sha256','grid_cells','nonzero_cells','zero_cells','sum_of_class_country_family_counts','number_of_checks','maximum_absolute_discrepancy']}, indent=2))
print(json.dumps({d:{c:{k:comparisons[d][c][k] for k in ['window_change_per_10pp','pretrend','heldout_2017_rmse','heldout_2017_bias','loo_window_change_per_10pp']} for c in comparisons[d]} for d in comparisons},indent=2))
