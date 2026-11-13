"""Integrate actual receipts; preserve unresolved science and prior decisions."""
from pathlib import Path
import json,csv,hashlib,io,re
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];BASE=HERE/'.publish_final/base';OUT=HERE/'.publish_final/state_out';OUT.mkdir(parents=True,exist_ok=True)
now=datetime.now(timezone.utc).isoformat();digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=HERE/'review/research_closure_referee_nov13.md';rj=json.loads(review.with_suffix('.json').read_text(encoding='utf-8'))
assert rj['original_hypothesis_identified'] is False and rj['entire_round_complete'] is False
status=json.loads((HERE/'STATUS.json').read_text(encoding='utf-8'))
status.update({'as_of_utc':now,'reporting_referee':'accept_limited_reporting; final independent scientific review','scientific_referee':'reject_current_version of original causal paper','fresh_literature_verification':{'status':'verified within scope','new_claims':26},'precedents_verification':{'papers':7,'key_claims':23,'status':'verified corrected specified primary-source scope'},'policy_verification':{'events':11,'signal_rows':5,'article_dates':35,'status':'verified within scope; earliest release/control access not implied'},'partial_regulatory_verification':'verified candidate text/row join only; entire audit incomplete','nonidentification_verification':{'claims':13,'status':'verified existence counterexample including original log1p-scale inverse construction'},'requirements_not_fulfilled':[0,3,5],'requirements_partly_fulfilled':[1,2,4,6,7,8],'reservations':'all known research schedules paused/disabled by latest direct instruction; current session only','remote_publication':'package prepared; readback receipt follows after conditional commit'})
(HERE/'STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# A separate current response acknowledges open scientific findings, without changing the referee.
responses=[]
for x in rj['inherited_scientific_findings']:
 responses.append({'finding_id':x['id'],'response':'현재 증거가 이 장애를 해소하지 못했다는 판정을 수용한다. 효과 입증·영효과·전체연구완료·게재준비 판정으로 올리지 않는다. '+x['reason'],'location':'report_main.md의 식별·측정·시점·추론·문헌 한계 및 STATUS.json; 새 별첨의 확인범위','verification_plan':'현재 한계와 검증된 사실을 분리해 전달한다. 추가 독립변이·최초결정/거래자료 없이 추정기 변경으로 해소하지 않는다.','status':'open'})
for k,v in rj['reporting_findings'].items():
 if k=='new_reporting_blocker':continue
 responses.append({'finding_id':k,'response':v+'; 최종 PPTX/원고/보고서 해시는 유지한다.','location':'보고서 §2/6/7 및 최종 PPTX notes1/4/13/14/24/37','verification_plan':'현재 실제 검증·심사 receipt의 파일해시와 판정범위를 유지.','status':'resolved per independent referee'})
response={'phase':'review','unit_id':'final_research_reporting','review_path':'outputs/final_research/review/research_closure_referee_nov13.md','review_sha256':digest(review),'author_id':'/root','responses':responses,'not_authorized':'원 연구전체완료·Gate·freeze·최초성·탑저널인과논문 채택은 선언하지 않음.','latest_user_execution':'모든 연구 예약중지, 현재 세션에서 실제검증수행. 독립새문헌/정책/선례/반례 검증을 실제완료한 사실로 기록.'}
md='# 최종 과학 심사에 대한 작성자 응답\n\n작성자 /root. 현재 산출물은 측정·식별감사 보고이며 원 인과논문 불채택을 수용한다. 과학적 지적은 해소로 바꾸지 않는다.\n\n'
for x in responses:md+='## '+x['finding_id']+'\n\n'+x['response']+'\n\n상태: '+x['status']+'\n\n'
md+='```json\n'+json.dumps(response,ensure_ascii=False,indent=2)+'\n```\n'
(HERE/'review/research_closure_referee_nov13_response.md').write_text(md,encoding='utf-8');(HERE/'review/research_closure_referee_nov13_response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary='''# 현재 결론과 검증 결과

2026-11-13. 보고서22쪽, 발표38장(본문32·부록6), 권장본문38분45초의 대본·목차·Q&A·참고문헌을 완성했다. 새 원문·선례·정책·정형반례를 실제 독립 검증하고 최종 심사를 받았다.

**원 질문의 인과효과는 미식별이다.** 현재 결과는 효과0을 입증한 것도 양/음효과를 입증한 것도 아니다. 허용한 중국×기술×시점 반사실 모형집합 안에서 동일 관측법칙과 양·0·음의 원척도 차등효과가 모두 양립하는 존재 반례를 독립 검증했다. 이는 실제 중국 정책이 결과를 전부 일으켰다는 증거가 아니다. 평행추세·독립정보도달·타당한 비교 등 추가 제한을 정당화한 설계까지 반박하지 않는다.

실제 월별 대조계수는 ALL−0.0806645, APP−0.0499468이지만 비교국·기술 제외·사전 예측에 민감하다. 이를 연구투자 증가율이나 정책효과로 발표하지 않는다. 새로운 family-footprint 측정은 국가 미상을 줄였지만 구성개념도 바뀌며 기존β를 재추정하지 않았다. 공개특허 지식과 실제 차단가능 보완투입, 법적 효력/공개/실제인도, 신청/선정/공고 시계의 구별이 핵심이다.

새 독립 검증은 문헌26개 주장, 선례7편의23개 핵심항목, 정책11사건·5신호·35연재날짜, 비식별13개 항목까지 수행했다. 441개 추가 독립 산술비교와 과거465항목은 서로 범위가 다르며 정책가설의 독립검정 횟수로 합산하지 않는다.

최종 독립심사는 측정·식별감사 자료의 한정사용을 허용하고, 원 인과논문 현 판본은 불채택했다. 원요구0/3/5는 미달,1/2/4/6/7/8은 부분달성이다. 특히 전수 규제적용, 같은pipeline의 비지목대조 실증, 기업별B×CAR 및 중국내 메커니즘은 충족하지 못했다. 기사·승인·특허·시장수익률을 다른 질문의 인과증거로 대체하지 않는다. SCI01 critical과SCI02–05 major/open, 기존PCX02 결정이력을 유지한다. 탑저널 게재수준이나 최초성을 확보했다고 말할 수 없다.

현재 자료로 발표할 정직한 결과는 성공적인 선제효과 추정이 아니라, 그 추정이 성립하려면 어떤 측정·법률·행동시계·반사실 조건이 필요한지 실제자료와 반례로 검증한 결과다. 더 유연한 계량기법의 추가만으로 이 공백이 채워지지 않는다. 최종판정·출처·파일해시는 review/research_closure_referee_nov13.*와 verification/에 있다.

모든 연구 예약은 최신 사용자 지시로 정지했다. Work 웹·로컬 예약은PAUSED, GitHub 연구workflow는disabled_manually를 실제 확인했다. 현재 대화에서만 작업하며 새 요청 없이 재개하지 않는다.
'''
(HERE/'현재_결론과_검증결과.md').write_text(summary,encoding='utf-8')
readme=(HERE/'README.md').read_text(encoding='utf-8')
addition='''\n## 최종 추가 검증과 판정\n\n- [현재 결론](현재_결론과_검증결과.md)과 [최종 과학 심사](review/research_closure_referee_nov13.md). 보고자료 한정사용 가능, 원 인과논문 현 판본 불채택. 전체 연구완료·최초성·게재 판정은 아니다.\n- [7편 선례의 독립 검증](verification/precedents_final_nov13.md), [새 문헌26개 주장 검증](verification/literature_final_nov13.md). 원문 모호함·판본 차이는 임의로 수선하지 않았다.\n- [정책11사건·5신호·35연재 독립 검증](verification/policy_final_nov13.md)과 [노출·시계 규칙](policy_completion/exposure_and_clock_rules.md).\n- [비식별의 정형 반례](empirics/nonidentification_proof.md)와 [13항목 독립 검증](verification/nonidentification_final_nov13.md). 같은 관측법칙에 양·0·음 인과차등효과를 구성한다. 실제 중국정책이나 영효과의 증거는 아니다.\n\n이 새 별첨은22쪽 PDF 본문을 바꾸지 않고 추가한 검증근거다. 생산 당시 pending 표식은 이력으로 보존되며 현재판정은 위 실제검증 receipt와 STATUS.json이 기준이다.\n'''
if '## 최종 추가 검증과 판정' not in readme:(HERE/'README.md').write_text(readme+addition,encoding='utf-8')
# State modifications are made from the pinned remote copies, never the dirty worktree.
def statewrite(rel,s):
 p=OUT/rel;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('w',encoding='utf-8',newline='') as f:f.write(s)
decision=(BASE/'state/decision_log.md').read_text(encoding='utf-8')
decision+='\n\n## '+now+' · 최신 직접 지시 및 실제 검증 결과\n\n사용자는 모든 연구 예약을 정지하고 이세션에서 연구를 마무리하며 미검증을 단순대기하지 말고 적극검증하라고 지시했다. Work웹 연구예약은 실제UI에서PAUSED, 로컬예약은PAUSED, GitHub Research cloud loop는공개REST 실제조회 disabled_manually를확인했다. 새요청없이예약/Claude/API연구를켜지않는다. 중단됐던 fresh문헌검증을 실제재개해26주장,7선례23항목,정책11사건/5신호/35날짜,비식별13항목을검증했다.\n\n최종보고자료는22쪽PDF/38장PPTX·PDF/대본·목차·Q&A·서지·별첨이다. 독립최종심사는 보고자료한정사용가능,원인과논문현판본불채택으로판정했다. SCI01–05와PCX02,Gate·charter는보존한다. 원요구0/3/5미달과나머지부분달성을숨기지않고전체연구완료로승격하지않는다. 새로운주설계·Gate·불가역freeze는채택하지않았다.\n'
statewrite('state/decision_log.md',decision)
progress=(BASE/'outputs/progress_log.md').read_text(encoding='utf-8')
progress+='\n\n## '+now+' · 현재 세션 최종자료 및 독립검증 통합\n\n- 실행: /root와분리된생산·검증·심사ID로진행. 현재세션수동실행만사용하고연구예약중지확인.\n- 증거:22쪽보고/38슬라이드/대본·Q&A·서지,24그룹국가회수,UNComtrade20행,NSFC340+MOST40,조달34품목·공고7120행,독립441산술비교,새문헌26·선례23·정책11/5/35·비식별13한정검증을보존. 세부범위는outputs/final_research/README.md와실제receipt.\n- 판정:원인과가설미식별;원인과논문현판본불채택. 보고자료한정사용가능. 원요구0/3/5미달,SCI01critical·SCI02–05major/open. 영효과·최초성·게재·Gate·freeze·전체회차완료선언없음.\n- 저장:이번조건부커밋묶음의대상이며실제ref갱신과재조회후에만저장성공으로보고한다. 논문전문/원웹전문/로컬사적경로는공개발행에서제외하고원본/발행본해시를구분한다. 원자료포함별도백업은로컬전용이다.\n- 후속:자동실행없음. 같은세션/수동재개시현재STATUS와최종심사를읽고남는식별장애에필요한실제자료를기준으로판단한다. 알려진산술을반복해원가설을통과로만들지않는다.\n'
statewrite('outputs/progress_log.md',progress)
threat=(BASE/'state/threat_register.md').read_text(encoding='utf-8')
threat+='\n\n## '+now+' · 실제 자료·반례로 추가 확인\n\n- SCI01 critical/open: unrestricted CN×k×t 반사실을허용하면관측법칙이같고원척도신호반응이양/0/음인witness가존재함을독립검증. 실제독자정책실재나영효과의증명아님.\n- 측정/법률 major/open:공개특허지식과차단가능투입구별,국가미상경계,APP2018-10-24완화와2019/2020IPC개정,신청/선정/공고/인도시계차를실제확인. 후보문언검토·행결합은전수규제감사아님.\n- 기존T10의비교국편향방향을항상0쪽감쇠로일반화하지않는다. donor반응의강도·부호에따라증폭·반전도가능. 실제LOO민감도는그구조를식별한것과다르다.\n- 원요구0/3/5미달및나머지부분달성은최종심사에명시. 기존위협과PCX02이력을삭제/하향하지않음.\n'
statewrite('state/threat_register.md',threat)
ledger=list(csv.DictReader((BASE/'state/claims_ledger.csv').open(encoding='utf-8-sig',newline='')));fields=list(ledger[0]);known={x['claim_id'] for x in ledger}
policy_updates={
 'C007':('ZTE denial activation order 즉시효력2018-04-15·FR게재04-23; specified order termination 즉시효력07-13·FR게재07-23','https://www.govinfo.gov/content/pkg/FR-2018-04-23/html/2018-08354.htm; https://www.govinfo.gov/content/pkg/FR-2018-07-23/html/2018-15633.htm'),
 'C008':('Section301 List1/2/3 추가관세시행2018-07-06/08-23/09-24. List3초기10%;중국산미국수입관세이지중국대미수입제한아님','https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/june/ustr-issues-tariffs-chinese-products; https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/august/ustr-finalizes-second-tranche; https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/september/ustr-finalizes-tariffs-200'),
 'C009':('DOJ China Initiative 창설발표 공식연설날짜2018-11-01.정확공개시각·별도품목규제시행일로확대하지않음','https://www.justice.gov/archives/opa/speech/attorney-general-jeff-sessions-announces-new-initiative-combat-chinese-economic-espionage'),
 'C010':('편집장1인칭정리전재와미상원제출증언부록에서科技日报35개기사발행일기록2018-04-19~07-03이35/35일치.원신문35지면전수열람아님','https://kunlunce.com/ssjj/fl1/2018-08-08/127123.html; https://www.govinfo.gov/content/pkg/CHRG-117shrg47983/pdf/CHRG-117shrg47983.pdf'),
 'C011':('NSFC2019집중접수2019-03-01~03-20 16:00;일부별도접수유형제외.이는선정·신청인의최초연구결정일이아님;F04/F05분류평가시범기록','https://fuwu.most.gov.cn/html/tztg/kjjhyjf/20181205/2960.html')}
for row in ledger:
 if row['claim_id'] in policy_updates:
  claim,url=policy_updates[row['claim_id']];previous={k:row.get(k,'') for k in ['verification_status','verified_by','verified_date','note']}
  row.update({'claim':claim,'source_url':url,'source_type':'독립 1차기록/공식본문 확인; 원문접근방식은 policy_final_nov13','verification_status':'verified','verified_by':'/root/nov13_policy_final_verify','verified_date':'2026-11-13','note':'2026-11-13 policy_final_nov13 한정검증. 실제품목구속/청정창/인과효과아님. 이전이력: '+json.dumps(previous,ensure_ascii=False)})
claims=[
 ('FNL-01','새24그룹 family-footprint의 known ALL쌍4659→6561 및경계폭중앙값60.9→41.4%p는보존집계에서독립재현;다른구성개념·전체순위미식별','/root/nov13_measurement_verify','verification/measurement_nov13.md'),
 ('FNL-02','중국2013–17수입HS8486/8542미국partner기간금액비중14.5582%/4.7515%;20행중12행UNSD집계플래그','/root/nov13_measurement_verify','verification/measurement_nov13.md'),
 ('FNL-03','보존월별2100셀기반반증·조건부simulation의441비교그룹독립산술일치;실제정책효과/DB재조회아님','/root/nov13_stats_verify','verification/empirics_nov13.md'),
 ('FNL-04','NSFC승인340·MOST서로다른예정선정40·조달34품목및공고7120행을한정범위독립대조;최초행동/전체신청분모아님','/root/nov13_measurement_verify','verification/behavior_nov13.md'),
 ('FNL-05','제공7고유문헌의새26주장원문선택쪽검증;실제코딩/최초성/저자결과재현아님','/root/nov13_literature_final_verify','verification/literature_final_nov13.md'),
 ('FNL-06','7편방법선례23핵심항목을현재수정판의원문선택절에서검증;Blume locator수정확인;원코드/판본모호함보존','/root/nov13_literature_final_verify','verification/precedents_final_nov13.md'),
 ('FNL-07','정책11사건·신호5행·35연재날짜를한정범위검증;효력/공표/정확공개일/실제구속차단은구별','/root/nov13_policy_final_verify','verification/policy_final_nov13.md'),
 ('FNL-08','원41행부분후보문언및81행기계결합검증;원27열보존,전체47중42부분검토5미검토;적용/청정월은미확인','/root/nov13_regulatory_final_verify','verification/regulatory_final_nov13.md'),
 ('FNL-09','unrestricted CN×k×t反事實모형집합에서동일관측법칙과원log1p척도양/0/음차등효과존재반례13항목검증;실제중국정책/영효과증명아님','/root/nov13_literature_final_verify','verification/nonidentification_final_nov13.md')
]
for cid,claim,agent,path in claims:
 if cid in known:continue
 row={k:'' for k in fields};row.update({'claim_id':cid,'claim':claim.replace('反事實','반사실'),'used_in':'최종 측정·식별감사 한정','source_url':'https://github.com/parkchanjin0128-pixel/research-agent/blob/main/outputs/final_research/'+path,'source_type':'독립원문/계산검증;원출처URL은보고서','added_by':'/root','added_date':'2026-11-13','verification_status':'verified','verified_by':agent,'verified_date':'2026-11-13','note':'해당보고서의한정확인범위만.원인과가설/Gate/최초성/전수감사검증아님.'});ledger.append(row)
s=io.StringIO(newline='');w=csv.DictWriter(s,fields);w.writeheader();w.writerows(ledger);statewrite('state/claims_ledger.csv',s.getvalue())
q=json.loads((BASE/'state/work_queue.json').read_text(encoding='utf-8'));q['updated_at']=now
for u in q['units']:
 if u['id'] in ('data_feasibility','novelty_recheck','precedents','concurrent_cn','regulatory_audit_41','round03_integration'):
  u.setdefault('notes',[]).append(now+' /root: outputs/final_research/README.md, STATUS.json, verification/, review/research_closure_referee_nov13.*에실제추가자료·독립검증·최종심사. 원인과논문불채택/보고한정사용. 해당단위전체완료나기존지적해소로승격안함. 예약모두중지/현재세션수동실행.')
q['latest_reporting_checkpoint']={'path':'outputs/final_research/STATUS.json','main_report_pages':22,'slides':38,'scope':'measurement and identification audit; original causal hypothesis unidentified','referee':'/root/nov13_research_closure_referee','referee_report':'outputs/final_research/review/research_closure_referee_nov13.md','referee_sha256':digest(review),'original_causal_paper':'reject_current_version','reporting':'accept_limited_reporting','entire_round_complete':False,'automation':'paused_by_user','updated_at':now}
statewrite('state/work_queue.json',json.dumps(q,ensure_ascii=False,indent=2)+'\n')
turn='''# Turn

최신 사용자 지시: 연구 예약을 모두 중지하고 현재 세션에서 연구를 마무리한다. 아래 상태는 자동 실행을 재개할 권한이 아니다.

```
workflow_version: codex_internal_v1
next: codex
round: 03
stage: review
active_unit: round03_integration
lock: none
lock_since: none
reviews_this_round: 0
internal_review_count: 14
updated_by: codex
updated_at: '''+now+'''
note: 보고22쪽·발표38장·대본완성. 실제추가독립검증/최종심사저장. 원인과논문불채택·미식별;보고한정사용가능. Gate/PCX02/SCI01–05보존. 모든연구예약정지,새요청없이재개금지.
run_id: none
run_started_at: none
run_url: none
automation_id: 6acc7ad834008191b7a20e074815c60b
automation_status: paused_by_user
```

독립검증·심사의새좁은확인범위와현재산출물은 outputs/final_research/README.md, STATUS.json 및 review/research_closure_referee_nov13.*를따른다. 내부회차심사카운트14는과거정식pipeline이력으로보존하며새보고자료내용심사3건을전체회차통과로계산하지않는다. 원요구0/3/5미달,나머지부분달성;원가설/전체연구완료아님. 현재세션수동작업의본인잠금을조건부발행시해제한다. 타인잠금을시간으로해제한것이아니다.
'''
statewrite('state/turn.md',turn)
print(json.dumps({'generated_utc':now,'new_scoped_claims':len(claims),'response_findings':len(responses),'state_files':[str(p.relative_to(OUT)) for p in OUT.rglob('*') if p.is_file()],'entire_research_complete':False},ensure_ascii=False))
