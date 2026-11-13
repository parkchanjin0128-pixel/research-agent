"""Join partial candidate-text reviews; never infer an absence of controls."""
from pathlib import Path
import csv,json,hashlib,collections
HERE=Path(__file__).resolve().parent
def rows(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
a=rows(HERE/'regulatory_dataset.csv');b=rows(HERE/'remaining_review/remaining_eccn_addendum.csv')
by={r['row_id']:r for r in b}; assert len(by)==22
sub=[r for r in a if r['layer']=='subcategory']; assert len(sub)==47
fields=list(a[0])+['추가검토_조문범위','추가검토_출처_locator','추가검토_판본','추가검토_잔여공백','추가검토_수준']
for r in a:
 for f in fields:r.setdefault(f,'')
 if r['node_id'] not in by:continue
 x=by[r['node_id']]
 r['행검토상태']='부분 문언 검토·적용 미확인'
 r['추가검토_조문범위']=x['실제열람_ECCN_후보_확정아님']+' | '+x['조문문언_실제검토범위']
 r['추가검토_출처_locator']=x['source_url']+' | '+x['locator']+' | '+x['실제열람_근거파일']
 r['추가검토_판본']=x['판본']
 r['추가검토_잔여공백']=' | '.join(x[k] for k in ['세부사양_제한','최종용도_제한','최종사용자_관할_제한','미검토범위'])
 r['추가검토_수준']=x['검토수준']
out=HERE/'integrated';out.mkdir(exist_ok=True)
with (out/'regulatory_dataset.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fields);w.writeheader();w.writerows(a)
origin41=[r for r in sub if '41' in r['원분모_구분']]
assert len(origin41)==41
def counts(rr):return dict(collections.Counter(r['행검토상태'] for r in rr))
summary={'date':'2026-11-13','role':'orchestrator join, not new legal judgment','rows':len(a),'layers':dict(collections.Counter(r['layer'] for r in a)),'added_join_rows':22,'original41':counts(origin41),'all47':counts(sub),'confirmed_uncontrolled':0,'confirmed_new_binding_control':0,'confirmed_clean_full_months':0,'legal_audit_complete':False,'original27_columns_preserved':all(list(r.values())[:27]==list(s.values())[:27] for r,s in zip(a,rows(HERE/'regulatory_dataset.csv'))),'source_sha256':{str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE/'regulatory_dataset.csv',HERE/'remaining_review/remaining_eccn_addendum.csv']},'output_sha256':hashlib.sha256((out/'regulatory_dataset.csv').read_bytes()).hexdigest(),'independent_verification':'pending'}
assert summary['original27_columns_preserved']
(out/'coverage_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(out/'README.md').write_text('# 규제표 통합본\n\n2026-11-13. 기존81행표에 추가22행 후보문언 감사를 ID로 결합한 최신사본이다. 앞27개원본열은 그대로 보존했다. 이전파일/분모/심사/Gate를 덮어쓰지 않는다.\n\n원41행 전부가 이제 적어도 일부후보ECCN문언의 직접열람근거를 갖는다. 그41개는 모두 **적용미확인**이다. 전체47은 부분문언42개, 직접ECCN미검토5개다. 후보조문검토는 전수규제/개정/거래요건의 감사가 아니다. **미통제(확인), 신규China-binding, 청정완전월의 확인은 모두0**이다. 이는 실제대상이 없다는 뜻이 아니라 확인에 충분한 증거가 없다는 뜻이다.\n\n초기coverage_summary.json은 추가검토 전 이력으로 보존된다. 새통합출력·원본SHA256은 이폴더 coverage_summary.json, 별도독립검증은 verification/regulatory_final_nov13.*에 기록한다.\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
