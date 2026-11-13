"""Correct reporting units without changing the historical computed contrasts/draws."""
from pathlib import Path
import json,math,hashlib
H=Path(__file__).resolve().parent
note=('효과 크기의 legacy 5pct/10pct 필드명은 각각 ±log(1.05)/±log(1.10)의 대칭 로그이동이다. '
      '음의 이동을 비율로 환산하면 각각 -4.7619048%/-9.0909091%이다. 정확한 -5%/-10%는 log(0.95)/log(0.90)이다. '
      '유의수준 5% 및 검정력 80%는 이 효과크기 표기와 별개다. 24개 시나리오는 8개 기본모형의 calibration/evaluation 쌍을 3배율에 공통 사용하며, 독립 기본 난수 seed는 16개다.')
replacements={
 '모든 bias에서 −5% 이하를 유지하는 최대 κ':'모든 bias에서 −log(1.05) 이하를 유지하는 최대 κ',
 '−10% 허용 κ':'−log(1.10) 허용 κ',
 '5% 양/음 검정력':'±log(1.05) 검정력',
 '10% 양/음 검정력':'±log(1.10) 검정력',
 '각 시나리오의 독립된 10만 calibration/10만 evaluation 추출을 사용했다.':'8개 기본모형 각각에 별도 10만 calibration/10만 evaluation 추출을 사용하고 세 잔차배율에서 그 난수를 공유했다.',
}
for name in ['analysis.md','run_falsification.py']:
 p=H/name;s=p.read_text(encoding='utf-8')
 for a,b in replacements.items():s=s.replace(a,b)
 if name.endswith('.md') and '## 효과 단위 정정' not in s:s+='\n\n## 효과 단위 정정\n\n'+note+'\n'
 if name.endswith('.py') and 'LEGACY_EFFECT_UNIT_NOTE' not in s:
  s=s.replace('N_CAL, N_EVAL, SEED =', 'LEGACY_EFFECT_UNIT_NOTE = '+repr(note)+'\nN_CAL, N_EVAL, SEED =')
  s=s.replace("out['simulation']['assumptions'] = sim_assumptions", "sim_assumptions['legacy_effect_unit_note'] = LEGACY_EFFECT_UNIT_NOTE\nout['simulation']['assumptions'] = sim_assumptions")
  s=s.replace("(HERE/'analysis.md').write_text", "lines += ['', '## 효과 단위 정정', '', LEGACY_EFFECT_UNIT_NOTE]\n(HERE/'analysis.md').write_text")
 p.write_text(s,encoding='utf-8')
for name in ['findings_for_manuscript.md','README.md']:
 p=H/name;s=p.read_text(encoding='utf-8')
 if '## 효과 단위 정정' not in s:s+='\n\n## 효과 단위 정정\n\n'+note+'\n'
 p.write_text(s,encoding='utf-8')
d=json.loads((H/'falsification_results.json').read_text(encoding='utf-8'))
corrected={}
for definition in ['ALL','APP']:
 theta=d['results'][definition]['original_2017_mean']
 corrected[definition]={'observed_log_contrast':theta}
 for p in [.05,.10]:
  threshold=math.log(1-p)
  corrected[definition][str(p)]={'exact_negative_ratio_threshold_log':threshold,
   'minimum_kappa_to_allow_effect_at_or_below_threshold':max(0.,theta-threshold),
   'maximum_nonnegative_kappa_for_all_effects_at_or_below_threshold':threshold-theta if theta<=threshold else None}
out={'note':note,'raw_results_unchanged':True,'scope':'conditional bias arithmetic only; not a causal CI or identified effect bound',
     'raw_results_sha256':hashlib.sha256((H/'falsification_results.json').read_bytes()).hexdigest(),'exact_negative_effects':corrected}
(H/'effect_unit_correction.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(corrected,ensure_ascii=False))
