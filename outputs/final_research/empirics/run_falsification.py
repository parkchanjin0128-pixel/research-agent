"""Exploratory falsification and conditional design pilot; no causal inference.

Reads fixed existing aggregates. Writes only beside this script. NumPy only.
Run with the explicit bundled Python path recorded in README.md.
"""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import math
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SRC = ROOT / 'outputs/identification_rescue_2026-11-12'
PILOT = ROOT / 'outputs/presentation_2026-11-13/data/patstat_pilot_final.json'
CLASSES = ['C12N', 'G01S', 'G06F', 'G06N', 'H01L']
COUNTRIES = ['CN', 'US', 'JP', 'KR', 'DE']
raw_path = SRC / 'patstat_wo_monthly_raw.json'
raw = json.loads(raw_path.read_text(encoding='utf-8'))
panel = raw['panel']
months = panel['months']
assert months == [f'{y}-{m:02d}' for y in range(2013, 2020) for m in range(1, 13)]
counts = np.array([[panel['series'][j+'_'+c] for j in CLASSES] for c in COUNTRIES], dtype=float)
assert counts.shape == (5, 5, 84) and int(counts.sum()) == 202110
assert np.all(counts >= 0) and np.all(counts == np.floor(counts))
logy = np.log1p(counts)
pilot = json.loads(PILOT.read_text(encoding='utf-8'))
rows = {r['cls']: r for r in pilot['raw']['PILOT_TRIMMED_AGGREGATES']}
dose = {j: {'ALL': rows[j]['us_fractional_pairs']/rows[j]['known_country_pairs'],
            'APP': rows[j]['applicant_us_fractional_pairs']/rows[j]['applicant_known_pairs']}
        for j in CLASSES}
BASE = np.arange(48, 60)
WIN = np.arange(71, 76)
MATCH = np.array([48, 49, 50, 51, 59])
SHIFT24 = WIN-24
assert [months[i] for i in WIN] == ['2018-12', '2019-01', '2019-02', '2019-03', '2019-04']
FIVE_PCT, TEN_PCT = math.log(1.05), math.log(1.10)

def arr(x):
    return np.asarray(x, dtype=float)

def summary(x):
    x = arr(x)
    return {'n': int(x.size), 'min': float(x.min()), 'p05': float(np.quantile(x, .05)),
            'p25': float(np.quantile(x, .25)), 'median': float(np.median(x)),
            'p75': float(np.quantile(x, .75)), 'p95': float(np.quantile(x, .95)),
            'max': float(x.max()), 'mean': float(x.mean()), 'sd': float(x.std(ddof=1)) if x.size > 1 else None}

def bw(definition, keep=None):
    keep = np.arange(5) if keep is None else arr(keep).astype(int)
    x = np.array([dose[CLASSES[i]][definition]/.1 for i in keep])
    z = x-x.mean()
    return z/(z@z)

def slope(y, definition, keep=None):
    return bw(definition, keep) @ y

def relative(focal, anchor='remaining4'):
    index = COUNTRIES.index(focal)
    donor_indices = [i for i in range(5) if i != index] if anchor == 'remaining4' else [COUNTRIES.index(anchor)]
    return logy[index] - logy[donor_indices].mean(axis=0)

def design(n=84):
    t = np.arange(n)
    return np.column_stack([(t % 12 == j).astype(float) for j in range(12)] + [t/12])

X = design()

def holdout(y):
    beta = np.linalg.lstsq(X[:48], y[:48], rcond=None)[0]
    fitted = X @ beta
    train_error = y[:48]-fitted[:48]
    err = y[48:60]-fitted[48:60]
    return {'train_n_months': 48, 'holdout_n_months': 12,
            'train_rmse': float(np.sqrt(np.mean(train_error**2))),
            'holdout_rmse': float(np.sqrt(np.mean(err**2))),
            'holdout_mean_error': float(err.mean()),
            'holdout_month_errors': [float(v) for v in err],
            'training_slope_per_year': float(beta[-1]),
            'training_calendar_intercept_range': float(np.ptp(beta[:12]))}

def write_csv(name, rows):
    with (HERE/name).open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

out = {'created_utc': datetime.now(timezone.utc).isoformat(),
       'status': 'exploratory descriptive falsification and conditional simulation; no causal claim',
       'unit': 'slope change in CN minus mean-country log(1+family count) per +10 percentage points of pre-B',
       'B_role': 'pre-period effect modifier, not a policy-assigned treatment dose',
       'classes': CLASSES, 'countries': COUNTRIES, 'months': months,
       'grid_cells': int(counts.size), 'sum_country_class_families': int(counts.sum()),
       'technical_support_points': 5, 'independent_clusters_established': False,
       'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in [raw_path, PILOT, HERE/'exploratory_execution_record.md']},
       'dose': dose, 'results': {}, 'country_placebo': {}, 'ipc_diagnostics': {},
       'bias_breakdown': {}, 'simulation': {}}

rel = relative('CN')
ipc_csv = []
for j, ipc in enumerate(CLASSES):
    h = holdout(rel[j])
    # De-trend first, then compare calendar means. Pure descriptive seasonality.
    b60 = np.linalg.lstsq(X[:60], rel[j, :60], rcond=None)[0]
    season = b60[:12]-b60[:12].mean()
    h.update({'pre60_calendar_effects_demeaned': list(map(float, season)),
              'pre60_calendar_range': float(np.ptp(season)),
              'original_window_change': float(rel[j, WIN].mean()-rel[j, BASE].mean()),
              'matched_calendar2017_window_change': float(rel[j, WIN].mean()-rel[j, MATCH].mean()),
              'shift24_window_change': float(rel[j, WIN].mean()-rel[j, SHIFT24].mean()),
              'country_counts_monthly_mean': {c: {
                  'baseline2017': float(counts[ci, j, BASE].mean()),
                  'matched2017': float(counts[ci, j, MATCH].mean()),
                  'candidate': float(counts[ci, j, WIN].mean())}
                  for ci, c in enumerate(COUNTRIES)}})
    out['ipc_diagnostics'][ipc] = h
    ipc_csv.append({'ipc': ipc, **{k: v for k, v in h.items() if isinstance(v, (float, int))}})

placebo_csv, fake_csv, bias_csv = [], [], []
reported = json.loads((SRC/'monthly_diagnostics.json').read_text(encoding='utf-8'))
for definition in ['ALL', 'APP']:
    s = slope(rel, definition)
    theta = float(s[WIN].mean()-s[BASE].mean())
    assert abs(theta-reported['results'][definition]['equal_controls']['window_change_per_10pp']) < 1e-12
    seasonal_pre = np.array([s[:60][np.arange(60) % 12 == (i % 12)].mean() for i in WIN])
    matched = float(s[WIN].mean()-s[MATCH].mean())
    shifted = float(s[WIN].mean()-s[SHIFT24].mean())
    h = holdout(s)
    assert abs(h['holdout_rmse']-reported['results'][definition]['equal_controls']['heldout_2017_rmse']) < 1e-12
    result = {'original_2017_mean': theta, 'matched_calendar2017': matched,
              'matched_minus_original': matched-theta, 'contiguous_window_shift24': shifted,
              'pre60_calendar_mean_baseline': float(s[WIN].mean()-seasonal_pre.mean()),
              'original_baseline_months': [months[i] for i in BASE],
              'matched_baseline_months': [months[i] for i in MATCH],
              'shift24_baseline_months': [months[i] for i in SHIFT24],
              'monthly_slope_per10pp': list(map(float, s)), 'holdout': h,
              'projection_weights': {j: float(w) for j, w in zip(CLASSES, bw(definition))},
              'leave_one_ipc_out_original': {j: float(slope(rel[np.arange(5) != i], definition, np.flatnonzero(np.arange(5) != i))[WIN].mean()-slope(rel[np.arange(5) != i], definition, np.flatnonzero(np.arange(5) != i))[BASE].mean()) for i, j in enumerate(CLASSES)}}
    # Original geometry: baseline k-23..k-12, gap k-11..k-1, post k..k+4.
    for geometry in ['same_baseline_gap', 'immediate_prior12']:
        records = []
        starts = range(23, 56) if geometry == 'same_baseline_gap' else range(12, 56)
        for k in starts:
            base = np.arange(k-23, k-11) if geometry == 'same_baseline_gap' else np.arange(k-12, k)
            win = np.arange(k, k+5)
            v = float(s[win].mean()-s[base].mean())
            record = {'definition': definition, 'geometry': geometry, 'window_start': months[k],
                      'window_end': months[k+4], 'baseline_start': months[base[0]],
                      'baseline_end': months[base[-1]], 'contrast': v,
                      'same_Dec_Apr_season': k % 12 == 11}
            records.append(record)
            fake_csv.append(record)
        values = [r['contrast'] for r in records]
        same_season = [r for r in records if r['same_Dec_Apr_season']]
        result['fake_windows_'+geometry] = {'summary': summary(values), 'records': records,
            'same_season_records': same_season,
            'absolute_exceedance_count': sum(abs(v) >= abs(theta) for v in values),
            'absolute_exceedance_fraction_descriptive_NOT_p': float(np.mean(np.abs(values) >= abs(theta))),
            'same_season_summary': summary([r['contrast'] for r in same_season])}
    out['results'][definition] = result
    out['country_placebo'][definition] = {}
    for anchor in ['remaining4', 'US']:
        focal_countries = COUNTRIES if anchor == 'remaining4' else ['CN', 'JP', 'KR', 'DE']
        records = []
        for c in focal_countries:
            sc = slope(relative(c, anchor), definition)
            vals = {'original_2017_mean': float(sc[WIN].mean()-sc[BASE].mean()),
                    'matched_calendar2017': float(sc[WIN].mean()-sc[MATCH].mean()),
                    'contiguous_window_shift24': float(sc[WIN].mean()-sc[SHIFT24].mean())}
            out['country_placebo'][definition][c+'_'+anchor] = vals
            record = {'definition': definition, 'focal': c, 'anchor': anchor, **vals}
            placebo_csv.append(record)
            records.append(record)
        if anchor == 'remaining4':
            assert abs(sum(r['original_2017_mean'] for r in records)) < 1e-12
    # Conditional bias arithmetic. These are not partial-ID intervals or CIs.
    grid = [0., .025, FIVE_PCT, TEN_PCT, .15, .20, .30]
    intervals = []
    for kappa in grid:
        lo, hi = theta-kappa, theta+kappa
        row = {'definition': definition, 'kappa': kappa, 'lower': lo, 'upper': hi,
               'negative_sign_for_all_bias': bool(hi < 0),
               'at_least_negative5pct_for_all_bias': bool(hi <= -FIVE_PCT),
               'at_least_negative10pct_for_all_bias': bool(hi <= -TEN_PCT),
               'allows_positive5pct': bool(hi >= FIVE_PCT),
               'allows_negative10pct': bool(lo <= -TEN_PCT)}
        intervals.append(row)
        bias_csv.append(row)
    out['bias_breakdown'][definition] = {'condition': 'observed = target + bias; fixed reported B; |bias| <= kappa, no sampling uncertainty',
       'not_partial_identification_or_confidence_interval': True, 'intervals': intervals,
       'kappa_to_allow_zero': abs(theta),
       'max_kappa_for_negative5pct_all_bias': max(0., -FIVE_PCT-theta),
       'negative5pct_robust_at_kappa0': bool(theta <= -FIVE_PCT),
       'negative10pct_robust_at_kappa0': bool(theta <= -TEN_PCT),
       'kappa_to_allow_positive5pct': max(0., FIVE_PCT-theta),
       'kappa_to_allow_negative10pct': max(0., theta+TEN_PCT)}

# Simulation calibrates ONLY an explicitly assumed 60-month residual process.
# The Gaussian scenarios preserve its observed marginal SD and vary persistence.
# All IPC cross-correlation is retained in their aggregate slope; no G=5 CLT.
LEGACY_EFFECT_UNIT_NOTE = '효과 크기의 legacy 5pct/10pct 필드명은 각각 ±log(1.05)/±log(1.10)의 대칭 로그이동이다. 음의 이동을 비율로 환산하면 각각 -4.7619048%/-9.0909091%이다. 정확한 -5%/-10%는 log(0.95)/log(0.90)이다. 유의수준 5% 및 검정력 80%는 이 효과크기 표기와 별개다. 24개 시나리오는 8개 기본모형의 calibration/evaluation 쌍을 3배율에 공통 사용하며, 독립 기본 난수 seed는 16개다.'
N_CAL, N_EVAL, SEED = 100000, 100000, 20261112
sim_csv = []
sim_assumptions = {'calibration_draws': N_CAL, 'evaluation_draws': N_EVAL, 'seed': SEED,
 'window_geometry': '28 simulated months: baseline 0:12; omitted gap 12:23; post 23:28',
 'alpha_two_sided': .05, 'target_power': .8,
 'alternatives_log_units_per10pp': {'5pct': FIVE_PCT, '10pct': TEN_PCT},
 'models': ['circular_moving_block12', 'gaussian_AR1_rho0', 'gaussian_AR1_rho0.5', 'gaussian_AR1_rho0.8'],
 'residual_scale_factors': [.5, 1., 2.],
 'scope': 'conditional, fixed-B/fixed-IPC, stationary residual simulation; not policy-effect power or an inferential correction',
 'known_failures_excluded': 'nonstationary breaks, uncertain B, historical taxonomy, selection, policy overlap, new China-specific shock, unknown patent decision lag'}
sim_assumptions['legacy_effect_unit_note'] = LEGACY_EFFECT_UNIT_NOTE
out['simulation']['assumptions'] = sim_assumptions

def noise_draws(resid, model, rng, n):
    sd = float(np.std(resid, ddof=1))
    if model == 'circular_moving_block12':
        starts = rng.integers(0, 60, size=(n, 3))
        positions = (starts[:, :, None]+np.arange(12)) % 60
        yy = resid[positions].reshape(n, 36)[:, :28]
    else:
        rho = float(model.split('rho')[1])
        yy = np.empty((n, 28))
        yy[:, 0] = rng.normal(0, sd, n)
        for t in range(1, 28):
            yy[:, t] = rho*yy[:, t-1]+rng.normal(0, sd*math.sqrt(1-rho*rho), n)
    return yy[:, 23:28].mean(axis=1)-yy[:, :12].mean(axis=1)

for di, definition in enumerate(['ALL', 'APP']):
    s = arr(out['results'][definition]['monthly_slope_per10pp'])
    b = np.linalg.lstsq(X[:60], s[:60], rcond=None)[0]
    resid = s[:60]-X[:60]@b
    resid -= resid.mean()
    sd = float(resid.std(ddof=1))
    out['simulation'][definition] = {'residual_sd': sd,
        'residual_lag1_corr': float(np.corrcoef(resid[1:], resid[:-1])[0, 1]),
        'observed_holdout_failure_retained': out['results'][definition]['holdout'], 'scenarios': []}
    for mi, model in enumerate(sim_assumptions['models']):
        cal = noise_draws(resid, model, np.random.default_rng(SEED+100*di+2*mi), N_CAL)
        ev = noise_draws(resid, model, np.random.default_rng(SEED+100*di+2*mi+1), N_EVAL)
        crit1 = float(np.quantile(np.abs(cal), .95))
        for scale in sim_assumptions['residual_scale_factors']:
            c, e = cal*scale, ev*scale
            crit = crit1*scale
            size = float(np.mean(np.abs(e) > crit))
            naivecrit = 1.96*sd*scale*math.sqrt(1/12+1/5)
            def power(delta):
                pp = float(np.mean(np.abs(e+delta) > crit))
                pn = float(np.mean(np.abs(e-delta) > crit))
                return pp, pn
            lo, hi = 0., max(1., 10*crit)
            for _ in range(45):
                mid = (lo+hi)/2
                if min(power(mid)) >= .8:
                    hi = mid
                else:
                    lo = mid
            p5, n5 = power(FIVE_PCT)
            p10, n10 = power(TEN_PCT)
            row = {'definition': definition, 'noise_model': model, 'residual_scale': scale,
               'null_contrast_sd': float(e.std(ddof=1)), 'calibrated_absolute_critical_value': crit,
               'independent_evaluation_size': size, 'size_MC_SE': math.sqrt(size*(1-size)/N_EVAL),
               'iid_normal_critical_value': naivecrit,
               'iid_normal_actual_size_under_this_DGP': float(np.mean(np.abs(e) > naivecrit)),
               'power_positive5pct': p5, 'power_negative5pct': n5,
               'power_positive10pct': p10, 'power_negative10pct': n10,
               'MDE80_log_per10pp_both_directions': hi,
               'MDE80_exp_minus1': float(np.expm1(hi)),
               'MDE5pct_feasible_under_DGP': bool(min(p5, n5) >= .8),
               'MDE10pct_feasible_under_DGP': bool(min(p10, n10) >= .8)}
            sim_csv.append(row)
            out['simulation'][definition]['scenarios'].append(row)

out['cross_definition_measurement_sensitivity'] = {
  'APP_minus_ALL_original': out['results']['APP']['original_2017_mean']-out['results']['ALL']['original_2017_mean'],
  'interpretation': 'Changing ALL to APP changes the B definition, not an estimated sampling distribution of the true B.'}
out['verification'] = {'raw_sum_matches': True, 'original_window_matches_prior_report_tol1e12': True,
 'holdout_rmse_matches_prior_report_tol1e12': True, 'country_symmetric_contrasts_sum_zero': True,
 'fake_geometry_count': 33, 'immediate_prior_count': 44, 'simulation_scenarios': len(sim_csv),
 'source_database_requeried': False, 'source_files_written': False}
write_csv('country_placebo.csv', placebo_csv)
write_csv('fake_event_windows.csv', fake_csv)
write_csv('ipc_holdout_seasonality.csv', ipc_csv)
write_csv('conditional_bias_breakdown.csv', bias_csv)
write_csv('simulation_pilot.csv', sim_csv)
(HERE/'falsification_results.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

lines = ['# 새로 실행한 반증분석과 조건부 설계 파일럿', '',
 '이 분석은 기존 결과를 본 뒤 기록한 탐색이다. 2,100셀의 산술을 재사용했지만 인과식별이나 원가설 완료를 판정하지 않는다. B는 사전 미국연결의 효과수정변수다. 5개 IPC가 독립 cluster라는 근거는 없으며 아래에서 cluster p값·정규 정책 p값을 제시하지 않는다.', '',
 '## 계절 구성과 기술별 사전 예측', '',
 '| B | 원 2017 평균 기준 | 동일 2017 calendar월 | 기준변경 차이 | 연속 24개월 전 창 | 2017 holdout RMSE / 평균오차 |',
 '|---|---:|---:|---:|---:|---:|']
for d in ['ALL', 'APP']:
    r = out['results'][d]; h = r['holdout']
    lines.append(f"|{d}|{r['original_2017_mean']:.6f}|{r['matched_calendar2017']:.6f}|{r['matched_minus_original']:+.6f}|{r['contiguous_window_shift24']:.6f}|{h['holdout_rmse']:.6f} / {h['holdout_mean_error']:+.6f}|")
lines += ['', '원 후보창은 2018-12–2019-04다. 동일 calendar월 비교는 2017-01–04 및 2017-12의 다섯 달이다. 1–4월의 간격은 2년, 12월은 1년으로 다르다. 연속 24개월 전 비교는 2016-12–2017-04다. 계절을 맞추는 것과 장기추세를 맞추는 것은 동시에 해결되지 않는다. 기준변경은 동일 표본의 시간가중 차이를 드러내며 대안 반사실을 입증하지 않는다.', '',
 '| IPC | 2013–16 학습 RMSE | 2017 검증 RMSE | 2017 평균오차 | pre60 calendar효과 진폭 | 원창 IPC 상대변화 | 동일월 기준 |',
 '|---|---:|---:|---:|---:|---:|---:|']
for j in CLASSES:
    r = out['ipc_diagnostics'][j]
    lines.append(f"|{j}|{r['train_rmse']:.4f}|{r['holdout_rmse']:.4f}|{r['holdout_mean_error']:+.4f}|{r['pre60_calendar_range']:.4f}|{r['original_window_change']:+.4f}|{r['matched_calendar2017_window_change']:+.4f}|")
lines += ['', 'IPC별 값의 단위는 국가상대 log(1+n)이며 위 B기울기와 다르다. calendar효과는 2013–17의 12개 월 절편과 선형추세를 함께 적합한 뒤 절편의 최대−최소다. 적은 5년 자료·저빈도 G06N·0셀 때문에 이를 안정된 구조적 계절성으로 해석할 수 없다. 2013–16에 고정한 월절편+선형추세가 2017을 예측하지 못한 사실은 유지된다. 기술별 경로를 상쇄한 평균 pretrend 비유의성으로 이 실패를 덮을 수 없다.', '',
 '## 국가 교체 반례', '',
 '| B | focal | 나머지4국, 원기준 | 나머지4국, 같은월기준 | US앵커, 원기준 |',
 '|---|---|---:|---:|---:|']
for d in ['ALL', 'APP']:
    for c in ['CN', 'JP', 'KR', 'DE']:
        a = out['country_placebo'][d][c+'_remaining4']; u = out['country_placebo'][d][c+'_US']
        lines.append(f"|{d}|{c}|{a['original_2017_mean']:+.6f}|{a['matched_calendar2017']:+.6f}|{u['original_2017_mean']:+.6f}|")
lines += ['', 'pseudo-China는 JP/KR/DE다. JP/KR의 원기준 값은 음수지만 CN보다 작고, DE는 반대 부호이며 절댓값은 CN보다 크다. 따라서 이 표는 동일 방향의 중국효과가 placebo에서 재현되었다는 결과가 아니다. 큰 국가별 이질변동이 있음을 드러내며 중국만의 공통 신호 귀속을 확인해 주지 않는다. 대칭 교체에서는 실제 CN이 donor에 들어가며 다섯 국가계수의 합이 0이므로 결과는 종속적이다. 공통 US앵커는 US의 파급·동시정책을 제거하지 않는다. placebo가 작아도 무파급·평행추세를 입증하지 않는다. 국가를 임의배정할 기제가 없으므로 이 표는 randomization inference가 아니다.', '',
 '## 사전 가짜 사건일: 동일 길이와 간격', '',
 '| B | n 가짜창 | min | 중앙값 | max | 실제보다 절댓값 큰 창 | Dec–Apr 3개 값 |',
 '|---|---:|---:|---:|---:|---:|---|']
for d in ['ALL', 'APP']:
    q = out['results'][d]['fake_windows_same_baseline_gap']; z=q['summary']
    v = ', '.join(f"{r['window_start']}: {r['contrast']:+.4f}" for r in q['same_season_records'])
    lines.append(f"|{d}|{z['n']}|{z['min']:+.6f}|{z['median']:+.6f}|{z['max']:+.6f}|{q['absolute_exceedance_count']}/{z['n']}|{v}|")
lines += ['', '주 가짜창은 2014-12–2017-08의 33개 시작점이다. 원창과 똑같이 12개월 기준, 11개월 공백, 5개월 후창을 둔다. 33개는 서로 다른 calendar계절을 섞은 기술적 분포이며 IPC별 계절성이 있으므로 실제 Dec–Apr 창과 교환가능하지 않다. 같은 Dec–Apr 세 값과 비교하면 실제 값이 모두 더 음수이지만, 3개만으로 5% 꼬리나 검정력을 학습할 수 없다. 창들이 겹치므로 독립 추정량이 아니며 사건일 배정 귀무분포도 아니다. 위 절댓값 초과비율은 기술적 순위이며 p값이 아니다. 바로 이전12개월을 기준으로 한 44개 창은 CSV/JSON에 전부 보존했다.', '',
 '## 허용편향의 조건부 산술', '',
 '| B | 0 허용에 필요한 κ | 모든 bias에서 −log(1.05) 이하를 유지하는 최대 κ | +5% 허용 κ | −log(1.10) 허용 κ |',
 '|---|---:|---:|---:|---:|']
for d in ['ALL', 'APP']:
    r=out['bias_breakdown'][d]
    lines.append(f"|{d}|{r['kappa_to_allow_zero']:.6f}|{r['max_kappa_for_negative5pct_all_bias']:.6f}|{r['kappa_to_allow_positive5pct']:.6f}|{r['kappa_to_allow_negative10pct']:.6f}|")
lines += ['', '가정은 reported B가 고정되어 있고 observed = target + bias, |bias|≤κ라는 것이다. κ는 추정한 편의가 아니라 외부에서 방어해야 할 범위다. 이때 [observed−κ, observed+κ]라는 산술만 계산했다. B의 측정오차·역사정보·공분산이 미확정이므로 이를 부분식별구간, HonestDiD, 강건 신뢰구간으로 부르지 않는다. 5%/10%는 각각 log(1.05)/log(1.10) per +10pp B인 실질크기 기준이다. 상대 log(1+n)의 변화이며 중국 총출원이나 R&D 예산의 5%/10% 변화가 아니다.', '',
 '## 조건부 simulation: size와 MDE', '',
 '원 12개월 기준과 11개월 간격, 5개월 후보창을 복제한 28개월을 생성했다. pre60 월별 B기울기에 calendar월+선형추세를 적합한 잔차의 규모를 사용했다. 적합 추세·계절의 추정불확실성은 추가하지 않았으며, 대안은 5개월 모두에 같은 고정shift를 가하는 모형이다. 지연·anticipation·시변효과의 검정력이 아니다. 원형 12개월 block은 경험적 월별 의존을 제한적으로 유지하며, Gaussian AR(1)은 같은 주변분산에서 rho를 0/.5/.8로 가정한다. 잔차규모 .5/1/2를 모두 계산했다. 8개 기본모형 각각에 별도 10만 calibration/10만 evaluation 추출을 사용하고 세 잔차배율에서 그 난수를 공유했다. 실제 2017 holdout 실패가 있으므로 이 정상잔차 가정은 채택된 참모형이 아니다.', '',
 '| B | 모형 | 잔차배율 | 보정 size | IID 1.96 기준 실제 size | ±log(1.05) 검정력 | ±log(1.10) 검정력 | 80% MDE log |',
 '|---|---|---:|---:|---:|---:|---:|---:|']
for r in sim_csv:
    lines.append(f"|{r['definition']}|{r['noise_model']}|{r['residual_scale']:.1f}|{r['independent_evaluation_size']:.4f}|{r['iid_normal_actual_size_under_this_DGP']:.4f}|{r['power_positive5pct']:.3f}/{r['power_negative5pct']:.3f}|{r['power_positive10pct']:.3f}/{r['power_negative10pct']:.3f}|{r['MDE80_log_per10pp_both_directions']:.4f}|")
lines += ['', '보정 size가 .05에 가깝다는 것은 같은 가정의 가상자료에서 임계값이 동작했다는 뜻뿐이다. 실제 자료의 오차분포·사건선택·B 측정오차가 보정된 것이 아니다. 10만 평가의 size MC SE는 약 .00069다. MDE는 양·음 방향 중 더 낮은 검정력이 .80에 도달할 최소 고정shift다. Gaussian대안과 block대안은 서로 독립적인 실증 확인이 아니다. 실제 정책사건이 하나이고 기술지지가 5개라는 한계를 반복 simulation으로 늘릴 수 없다. IID 1.96의 과대 size는 상관무시의 가상 반례로만 제시했다.', '',
 '이번 계산으로 연구자금·프로젝트·투자의 선제 재배분은 관측되지 않는다. 원가설의 인과효과는 미식별이며 특허 시계·청정창·사전고정 B·미국과 중국 동시정책·무파급 비교에 대한 추가자료가 필요하다. 새 반증결과는 가설의 완료판정을 대신하지 않는다.', '',
 '재현: `run_falsification.py`는 기존 raw JSON과 pilot B만 읽으며 이 디렉터리에 JSON/CSV/메모를 쓴다. 입력 SHA-256, 전체 가짜창, 국가교체, IPC holdout, 24개 simulation 시나리오는 `falsification_results.json`에 보존했다. 원시 DB는 재조회하지 않았다.']
lines += ['', '## 효과 단위 정정', '', LEGACY_EFFECT_UNIT_NOTE]
(HERE/'analysis.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps({'status': 'completed', 'output': str(HERE), 'original': {d: out['results'][d]['original_2017_mean'] for d in ['ALL','APP']}, 'simulation_scenarios': len(sim_csv)}, ensure_ascii=False))
