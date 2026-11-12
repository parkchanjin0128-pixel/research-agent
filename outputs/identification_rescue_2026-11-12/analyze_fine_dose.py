"""Recorded-sample measurement diagnostics; interval widths are not confidence intervals."""
from pathlib import Path
import hashlib,json,statistics
H=Path(__file__).resolve().parent
b=(H/'finegroup_pre_dose_raw.json').read_bytes()
assert hashlib.sha256(b).hexdigest()=='6f4c983b54e3f092798f6c6024dbb94c2d5f39fc6b53978d24a4546bedfceabf'
d=json.loads(b); summary={}
assert len(d['selected_groups'])==24 and len(d['dose_rows'])==48
for o in ['ALL','APP']:
 rows=[r for r in d['dose_rows'] if r['origin']==o]
 assert len({r['main_group'] for r in rows})==24
 for r in rows:
  assert r['sampled_families']==100
  assert 0<=r['known_persons_over_pairs']<=r['listed_persons_over_pairs']
  assert 0<=r['us_persons_over_pairs']<=r['known_persons_over_pairs']
  if r['cited_family_pairs']:
   assert 0<=r['b_pair_us_lower']<=r['b_pair_us_upper']<=1
   assert abs(r['b_pair_us_lower']-r['us_fraction_lower_sum']/r['cited_family_pairs'])<1e-12
   assert abs(r['b_pair_us_upper']-r['us_fraction_upper_sum']/r['cited_family_pairs'])<1e-12
  else:
   assert r['b_pair_us_lower'] is None and r['b_pair_us_upper'] is None
 measured=[r for r in rows if r['cited_family_pairs']>0]
 lo=max(r['b_pair_us_lower'] for r in measured);hi=min(r['b_pair_us_upper'] for r in measured)
 summary[o]={
  'groups':24,'sampled_group_family_memberships':sum(r['sampled_families'] for r in rows),
  'pairs':sum(r['cited_family_pairs'] for r in rows),
  'known_pairs':sum(r['pairs_any_known_country'] for r in rows),
  'dose_defined_groups':len(measured),'dose_undefined_no_pairs':[r['main_group'] for r in rows if r['cited_family_pairs']==0],
  'known_only_point_defined_groups':sum(r['b_pair_us_known_only'] is not None for r in rows),
  'known_only_point_undefined_groups':[r['main_group'] for r in rows if r['b_pair_us_known_only'] is None],
  'median_person_country_interval_width':statistics.median(r['b_pair_us_upper']-r['b_pair_us_lower'] for r in measured),
  'point_range_known_only':[min(r['b_pair_us_known_only'] for r in rows if r['b_pair_us_known_only'] is not None),max(r['b_pair_us_known_only'] for r in rows if r['b_pair_us_known_only'] is not None)],
  'pair_n_lt20':[r['main_group'] for r in rows if r['cited_family_pairs']<20],
  'citing_source_family_n_lt10':[r['main_group'] for r in rows if r['citing_families_with_edges']<10],
  'marginal_interval_intersection':[lo,hi] if lo<=hi else None,
  'strict_pairwise_orders_certified_by_marginal_bounds':sum(a['b_pair_us_lower']>c['b_pair_us_upper'] for a in measured for c in measured if a['main_group']!=c['main_group']),
  'order_comparisons':len(measured)*(len(measured)-1),
 }
out={'status':'producer arithmetic; independent verification separately required',
 'raw_sha256':hashlib.sha256(b).hexdigest(),'summary':summary,
 'limits':['Bounds conditional on observed target applicant list/person slots and the chosen cited document; missing applicants entirely absent from lists are not fully bounded.',
 'Country-code admissibility used by SQL is not an independent audit of historical legal-entity domicile.',
 'Bounds exclude family-hash sampling uncertainty, source selection, country-attribution error, temporal revision and retrospective taxonomy uncertainty.',
 'Intersection of marginal intervals does not establish that all values are jointly feasible: shared target persons can couple unknown assignments.',
 'Twenty-four main groups are not established independent technology clusters; same patents/citations can overlap.',
 'No finegroup post-2017 outcome or treatment effect estimated.']}
(H/'finegroup_measurement_diagnostics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
