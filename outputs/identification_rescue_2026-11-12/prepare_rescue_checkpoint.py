"""Append an auditable research checkpoint; no Gate or review acceptance changes."""
from pathlib import Path
import json,re,datetime as dt,hashlib,zipfile,csv,io
HERE=Path(__file__).resolve().parent
ORIGINAL=HERE/'.publish_original'
stamp=dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M KST')
files=[]
def add(path,content):files.append({'path':path,'mode':'100644','type':'blob','content':content})
for p in sorted(HERE.iterdir()):
 if p.is_file() and p.suffix in {'.md','.json','.py','.sql'} and p.name not in {'publish_manifest.json','package_manifest.json','remote_receipt.json'}:
  content=p.read_text(encoding='utf-8-sig')
  # Public work product contains public research only. Remove host-specific paths.
  content=content.replace('workspace/','workspace/')
  add('outputs/identification_rescue_2026-11-12/'+p.name,content)
turn=(ORIGINAL/'state/turn.md').read_text(encoding='utf-8')
for key,val in {'next':'codex','stage':'production','active_unit':'data_feasibility','updated_at':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
 'note':'실제 WO 국제특허 월별 2100셀·방법22행 추가. 465 독립 산술검산 일치. 인과효과 미식별·referee 표현수정 후 재확인 한도대기. 공개 지연의 사전 코호트 절단을 실측; 세부기술 동일모집단 측정 계속. resume.md 참조.'}.items():
 turn,n=re.subn('^'+re.escape(key)+':.*$',key+': '+val,turn,flags=re.M); assert n==1,key
assert 'lock: none' in turn
add('state/turn.md',turn)
q=json.loads((ORIGINAL/'state/work_queue.json').read_text(encoding='utf-8'))
u=next(x for x in q['units'] if x['id']=='data_feasibility')
u['notes'].append(stamp+' /root: 최신 사용자의 실제 검증 지시로 outputs/identification_rescue_2026-11-12 탐색 실측·방법검토·독립 검산·초기 referee·표현수정·재개기록을 저장. WO 2100셀, ALL/APP 후보창 상대기울기 -0.080665/-0.049947, H01L/국가별 LOO 불안정. 원 가설·주설계·단위 완료 아님. referee 마지막 재확인은 구독한도로 중단, pending 보존. 세부기술 사전표본은 공개시차로2017관측합1을 진단. 같은 WO 모집단 dose·세부기술 지원을 다음 준비작업으로 우선한다. 기존 DF 수정이력·검증·review 상태를 변경하지 않음.')
q['updated_at']=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
add('state/work_queue.json',json.dumps(q,ensure_ascii=False,indent=2)+'\n')
decision=(ORIGINAL/'state/decision_log.md').read_text(encoding='utf-8')
decision+='\n\n## '+stamp+' · 실제 검증을 위한 탐색 자료 확장\n\n사용자가 미검증 가설에 대해 모든 관련 최신 방법을 검토하고 실제 검증을 진행하라고 지시했으며 이어서 계속 진행하라고 재지시했다. 이 직접 지시를 국가×기술×월 특허 활동 등 실자료 탐색의 승인으로 해석해 분석 전 규칙을 기록하고 실행했다. 결과를 이미 본 표본이므로 사전등록·확인분석으로 소급하지 않는다. 원래 질문·Gate·주분석 freeze·중국정책/실제제한 분리·기존PCX-02의 사용자 결정 대기를 유지한다. 방법군검토는 전수조사·실증입증이 아니다. 독립 referee 재확인은 한도로 대기하며 승인·완료를 대신 선언하지 않는다.\n'
add('state/decision_log.md',decision)
ledger=(ORIGINAL/'state/claims_ledger.csv').read_text(encoding='utf-8')
existing=list(csv.DictReader(io.StringIO(ledger))); ids={r['claim_id'] for r in existing}
extra=[]
def claim(suffix,text,source,verifier,note,status='verified'):
 ident='EMP-20261112-'+suffix
 assert ident not in ids
 extra.append([ident,text,'outputs/identification_rescue_2026-11-12',source,'실집계·독립 산술/원문 범위','/root','2026-11-12',status,verifier,'2026-11-12' if verifier else '',note])
claim('01','기록된 WO 5 IPC×5국×84개월 격자는2100셀·양수2064·합202110 class-country-family counts다','https://tip.epo.org/','/root/nov12_rescue_verifier','verification.md; raw SHA8dcc8869…fc9f0. 전역 고유수·대표성·DB독립재실행·인과효과 검증 아님.')
claim('02','기록된 5 IPC 패널의 2017평균 대비2018-12~2019-04 상대기울기는 미국인용B10%p당 ALL -0.0806645·APP -0.0499468이다','outputs/identification_rescue_2026-11-12/patstat_wo_monthly_raw.json','/root/nov12_rescue_verifier','465 독립 산술비교. 기술·donor LOO 부호역전과 예측실패 존재. 최초출원 코호트이며 실제 제한 전 R&D효과 아님.')
claim('03','24 main group의 각100WO family 표집에서 ALL10747인용쌍/known4659·APP765쌍/known726을 기록했다','outputs/identification_rescue_2026-11-12/finegroup_pre_dose_raw.json','/root/nov12_fine_dose_verifier','finegroup_verification.md/json; 합계는 group별 중복허용. 원시pair별 국적·DB 독립조회 미확인.')
claim('04','ALL 개별person국가미상 경계폭 중앙값0.608782026이며 marginal교집합은[0.3770150484,0.6310570645]다','outputs/identification_rescue_2026-11-12/finegroup_pre_dose_raw.json','/root/nov12_fine_dose_verifier','관측 신청인 목록 조건부 sample 경계. 공동배정 가능성·전체모집단 순위·신뢰구간 아님. APP경계21/24·known-only점17/24;APP18/24 pair<20·22/24sourcefamily<10.')
claim('05','WIPO PCT21(2)는 예외를 전제로 우선일18개월 뒤 국제공개와 요청시 조기공개를 규정한다','https://www.wipo.int/en/web/pct-system/texts/articles/a21','/root/nov12_fine_dose_verifier','국제공개 일반규칙 확인. 개별2017관측누락원인 전부 입증 아님.')
claim('06','WIPO IPC2024 G06공식스킴은 G06F40/00[2020.01]·G06N20/00[2019.01] 표지를 보인다','https://www.wipo.int/ipc/itos4ipc/ITSupport_and_download_area/20240101/pdf/scheme/full_ipc/en/g06.pdf','/root/nov12_fine_dose_verifier','PDF p14/p22 직접확인. 역사적 concordance·전체 재분류 이력은 미검증.')
claim('07','미국2018신호가 실제 제한 전에 중국 연구·자본배분을 의존도별로 바꿨다는 원 인과가설','outputs/identification_rescue_2026-11-12/overview.md','','직접 결정시계·유효 비교·정책/제한 분리·B측정·유효추론 미확보. 특허 진단으로 가설 채택/기각하지 않음.','unverified')
s=io.StringIO(newline='');csv.writer(s,lineterminator='\n').writerows(extra)
ledger=ledger.rstrip('\r\n')+'\n'+s.getvalue()
assert len(list(csv.DictReader(io.StringIO(ledger))))==len(existing)+len(extra)
add('state/claims_ledger.csv',ledger)
log=(ORIGINAL/'outputs/progress_log.md').read_text(encoding='utf-8')
log+='\n\n## '+stamp+' · 실제 월별 패널과 가설 검증 경로\n\n- [추가 실증 보고](identification_rescue_2026-11-12/overview.md): 실제 PATSTAT WO 표본5 IPC×5국×84개월,2100셀; 원자료11403bytes SHA256 일치. ALL/APP 상대기울기 음수이나 LOO/사전예측 불안정, 인과효과 아님.\n- [독립 검산](identification_rescue_2026-11-12/verification.md):465항목 일치,DB독립재실행은미수행. [referee](identification_rescue_2026-11-12/referee.md)는진단범위만심사;3개표현수정반영후재확인중구독한도로중단,accept아님.\n- 방법12행+대안10군과원문확인범위/판본을저장했다. 단일사건·중국특화충격의관측동등성을추정기교체로해결하지않는다.\n- 자체WO공보2017년말cutoff의큰우측절단을실측하고새탐색규칙24main group×100WO family에서ALL10747쌍/APP765쌍을추가집계했다. [새 독립검산](identification_rescue_2026-11-12/finegroup_verification.md)은산술·WIPO원문범위에서통과;경계공통부분은공동배정증명이아님. APP는경계21/24·known-only점17/24로정의되며희소성심각. 새회귀전B측정보류.\n- 6쪽추가PDF와코드·데이터·검증·초기심사·응답을백업한다. EMP-20261112-01~07을원장에기록하되원인과가설은unverified다. 메인회차완료·Gate통과아님. 다음차례는[재개메모](identification_rescue_2026-11-12/resume.md)를먼저읽고준비된독립작업을계속한다.\n'
add('outputs/progress_log.md',log)
(HERE/'publish_manifest.json').write_text(json.dumps(files,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'files':len(files),'characters':sum(len(x['content']) for x in files),'state':'next codex; no lock; no acceptance change'}))
