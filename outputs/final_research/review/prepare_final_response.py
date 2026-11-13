from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
paths=['report_main.md','report/연구보고서_최종.pdf','presentation/content.mjs','presentation/발표원고.md','presentation/참고문헌.md','presentation/슬라이드_주장_근거표.md','presentation/deliverables/최종_연구발표_시간정정.pptx','presentation/deliverables/최종_연구발표.pdf','literature/pdf_audit.md','literature/pdf_audit.json']
hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
response={
 'unit':'final_research_reporting','revision':1,'producer_response_by':'/root','date':'2026-11-13',
 'review':'review/final_referee_nov13.md',
 'scope':'미식별 인과가설의 실증·측정·식별 감사 보고서 및 발표자료. 원 효과 입증·주설계 채택·Gate·최초성·게재 승인 아님.',
 'responses':[
 {'finding_id':'FR-01','action':'보고서 §6.1/7.1 및 발표13/14/24장 노트·원고에 기존200-family/IPC B의 관청비한정→가족전체application확장, anyAPP+공통earliest target 규칙을 새24그룹 WO100·APP별대표 규칙 및 family footprint와 구분. 새로운 B로 월별β를 재추정하지 않았다고 명시.','requested_status':'독립 재확인 요청','location':['report_main.md §6.1/7.1','presentation/발표원고.md 13/14/24장','presentation/deliverables/최종_연구발표_시간정정.pptx notes13/14/24']},
 {'finding_id':'FR-02','action':'제공PDF7고유문헌 해시·판본·원문쪽수 감사. Gao85쪽June2026 CSL복수명단·해외고객/미국공급자2001–21, ZhangFeb2026 121분야28/93, Liu–Ruan–ZhengJune2026 TRS와본문/표시계불일치, He–Lyu US인용outcome 및 KZ/현금/학력 간접근거를 보고서·노트·참고문헌·근거표로 통합. 전문403은11월12일 웹접근 이력으로 한정.','requested_status':'독립 재확인 요청','location':['literature/pdf_audit.md/json','report_main.md §2.1/참고문헌','presentation/참고문헌.md','presentation/발표원고.md 4/37장']},
 {'finding_id':'SCI-01','action':'미국신호0인 모형의 관측동등성 및 중국정책/비교국파급 분리 실패를 명시. 회귀·방법추가로 해소하지 않음.','requested_status':'open, 인과결론 차단 유지'},
 {'finding_id':'SCI-02','action':'지식연결과 잠재차단손실의 차이, 국가미상 산술경계, 회수proxy의 별도구성과 원DB독립재조회 미완료를 명시.','requested_status':'open'},
 {'finding_id':'SCI-03','action':'최초행동·결정일, 추가제한/거래cutoff,무오염창 미확정. 후보5개월창과 Jan→Oct 규정판본 차이를 명시.','requested_status':'open'},
 {'finding_id':'SCI-04','action':'5IPC·고정B/정상잔차 조건부MDE·인공시뮬레이션 범위,가짜창순위p값아님,독립집계검산과DB검증구별을 유지.','requested_status':'open'},
 {'finding_id':'SCI-05','action':'최신제공원문통합을 완료하였으나 전수문헌감사/최초성/게재확정으로 승격하지 않음.','requested_status':'최신문헌누락만 재확인, 최초성판정은 open'}
 ],'minor_time_response':'첫 장 약37분을 원천·원고·최종PPTX노트에서38분45초로 통일. 실제 리허설 검증 또는 자동30분초과보장 주장은 하지 않음.','artifact_sha256':hashes,'no_gate_or_freeze':True,'historical_PCX02':'기존 두수정후 사용자결정대기 유지. 이보고자료 수정으로 해소하지 않음.'}
response.update({'phase':'revision','unit_id':'final_research_reporting','review_path':'outputs/final_research/review/final_referee_nov13.md','review_sha256':hashlib.sha256((ROOT/'review/final_referee_nov13.md').read_bytes()).hexdigest(),'author_id':'/root'})
for x in response['responses']:
 x['response']=x['action']
 x['location']='; '.join(x.get('location',['report_main.md 및 최종 발표 노트의 한계 명시']))
 x['verification_plan']='별도 fresh referee가 현재 원고·실제PPTX notes·원고·검증보고서를 대조. 새 사실은 별도 verifier receipt 필요.'
(ROOT/'review/final_referee_response_nov13.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
md=['# 최종 첫 심사에 대한 작성자 응답','', '2026-11-13 · 작성자 /root · 수정1. 응답은 독립 해소판정이 아니다.','',response['scope'],'']
for x in response['responses']:
 md += ['## '+x['finding_id'],'',x['action'],'','요청/보존 상태: '+x['requested_status'],'']
md += ['## 이력 및 후속 확인','','원심사·응답·현재해시를 보존한다. 새 독립 심사자가 실제보고서·PPTX노트·대본·문헌감사를 대조해야 FR-01/02를 해소할 수 있다. SCI사항은 원 인과가설 입증의 장애로 남고, 이를 문서사용승인과 혼동하지 않는다. 기존 PCX-02 두수정후 사용자결정대기는 그대로다.','', '## 현재 산출물 해시','']
md += ['- `'+p+'`: `'+h+'`' for p,h in hashes.items()]
md += ['', '## 기계 판독 응답', '', '```json', json.dumps(response,ensure_ascii=False,indent=2), '```']
(ROOT/'review/final_referee_response_nov13.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
(ROOT/'review/final_referee_nov13_r1_response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(ROOT/'review/final_referee_nov13_r1_response.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps({'response_findings':len(response['responses']),'hashes':len(hashes)},ensure_ascii=False))
