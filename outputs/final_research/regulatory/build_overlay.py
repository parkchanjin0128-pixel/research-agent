from pathlib import Path
import csv,json,hashlib,collections,datetime

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
SRC=BASE/'work/research-agent/.local/nov09-review/outputs/round_03/regulatory_dataset.csv'
AUD=BASE/'work/research-agent/outputs/round_02/announcement_window_audit.csv'
rows=list(csv.DictReader(SRC.open(encoding='utf-8-sig',newline='')))
historical={r['node_id']:r for r in csv.DictReader(AUD.open(encoding='utf-8-sig',newline=''))}

# 직접 대조한 범위는 부분 문언 확인이며 해당 기술의 품목분류·무통제 인증이 아니다.
data='''F01-S01|나노 물질의 조성·서열·병원성·장비 모델을 특정하지 못함|생물·화학무기 용도와 의료·민간 용도를 구별할 실제 자료 없음|생물|1C353|나노 크기는 1C353 요건이 아니며 실제 유전요소의 요건이 필요
F01-S02|서열·독소 관련성 및 합성기 자동화·연속길이·오류율 미상|합성 물질의 최종용도와 합성장비 수하인·연구실 미상|생물|1C353;2B352.j|2019판 장비 문언과 2021 후속 SW 사건을 분리
F01-S03|유전요소·변형생물의 유래·기능·서열과 장비/기술 이전 미상|대학·병원명만으로 최종용도·실제 거래 역할 판정 불가|생물|1C353;2B352.j|일반 유전공학과 특정 목록 병원성·독소 서열을 구별
F01-S04|신경신호 감지·자극기/IC/코드/노하우 중 대상과 성능 미상|의료 진단·민간 보조·군사 응용을 구별할 거래 자료 없음|신경메모||BCI와 겹치는 부분만 기존 메모 연결; 비 BCI 신경기술의 직접 ECCN 미검토
F02-S01|학습 알고리즘·모델·소스코드·훈련장비를 구별할 자료 없음|영상정보·군사 등 실제 응용과 접근받는 연구자 미상|미검토||R01은 특정 지리공간 SW 후속 사건이며 신경망 전부가 아님
F02-S02|유전알고리즘과 실제 생물 유전공학을 구별하고 코드 기능·이전형태 필요|최적화 대상과 실제 최종사용자·역할 미상|미검토||명칭의 genetic만으로 생물 ECCN 적용 금지
F02-S03|강화학습 코드/가중치/연산장치와 제어대상·성능 미상|민간 게임·로봇·군사 제어 응용의 실제 사용 미상|미검토||학습방식만으로 독립 ECCN을 지정하지 않음
F02-S04|영상 센서/범용 코드/특수 지리공간 SW의 구체 기능 미상|감시·민간 영상처리·군사 응용 및 실제 수하인 미상|미검토||R01·R02·R03 임시항목과 전체 컴퓨터 비전을 구별
F02-S05|규칙 기반 SW·모델·장비 중 이전 대상 및 특수설계 여부 미상|의료·교육·의사결정지원의 실제 최종용도·사용자 미상|미검토||전문가시스템이라는 연구분류만 존재
F02-S06|음성신호 처리 코드·마이크/전자장치의 기능·사양 미상|민간 음성서비스·감청 등 응용과 접근당사자 미상|미검토||음성 알고리즘의 직접 ECCN 문언 미검토
F02-S07|번역 모델·소스·공개문헌·비공개 노하우 중 법적 대상 미상|언어서비스의 실제 용도·접근국적·당사자 미상|미검토||텍스트 처리라는 표지로 장비 통제를 전파하지 않음
F02-S08|계획·일정·게임 코드와 특정 비행/무기 제어 기능의 구별 필요|스케줄링 대상·최종용도·사용자 미상|미검토||7D004의 일반 task scheduling 제외를 이 행 전체 무통제로 읽지 않음
F02-S09|합성 음성·영상 코드/가중치/장비의 실제 기능 미상|콘텐츠 제작·기만·감시 응용과 실제 최종사용자 미상|미검토||일반 deepfake 표지만으로 통제·무통제 불가
F02-S10|서버/IC/서비스/원격 코드접근을 구별하지 못하며 APP·최대구성·집계 미상|클라우드 서버 소재지·운영자·접근자·군사 최종용도 미상|컴퓨터|4A003;4A994;4D001;4E001|4A003 완화는 실제 컴퓨터·조립품 하위범위의 조건부 근거이며 클라우드 서비스 전체 판단 아님
F02-S11|신경망 IC 여부·부품번호·재료·온도·성능 및 장비/칩 구별 미상|군사용도·군사사용자 지식·BIS 통지와 거래당사자 미상|반도체|3A001.a.9;3A991;3E001|2018판 신경망 IC 문언은 존재하나 모든 AI 가속기 동일 분류 아님
F04-S01|IC 기능·클록·화합물반도체·ALU 폭·연산속도와 설계자료 미상|군사용도/사용자 지식 및 실제 공급·수하·최종사용자 미상|반도체|3A001;3A991;3E001|SoC는 완성 서버와 다른 품목; §744.17 별도 조건
F04-S02|EEPROM/SRAM/DRAM 종류·패키지·접근시간·온도·적층구조 미상|JHICC와 실제 거래·지정법인 역할 및 연구용도 미상|메모리|3A001;3A991;3E001|2018 메모리 후보·JHICC 지정·2024 HBM 후속범위 분리
F05-S01|인메모리 IC/일반 로직/완성컴퓨터와 사양·공정·설계기술 미상|JHICC 실제 거래 역할·용도와 공급망 간접 노출 구별 필요|메모리|3A001;3A991;3E001|2023 in-memory 예시를 2018 첫 통제로 소급하지 않음
F06-S01|표시 SW·렌더링 코드·특수 장비의 실제 기능·특수설계 여부 미상|연구 시각화·비행 표시·군사 응용과 최종사용자 미상|미검토||시각화의 직접 ECCN 미검토
F06-S02|범용 분석과 R01의 특정 지리공간 영상 자동분석 조건 구별 필요|분석자료·군사·정보수집 목적과 접근당사자 미상|미검토||선택 후속 R01 날짜가 기존 또는 다른 제한 부재를 보증하지 않음
F06-S03|센서·위치·상황인지 SW·코드 기능과 장비 성능 미상|민간 위치서비스·군사 상황인식 응용과 실제 사용자 미상|미검토||상황인지라는 분류로 PNT·통신 ECCN 자동 지정 금지
F07-S01|디지털/양자 하이브리드 구성·큐비트·부품·코드의 실제 이전 미상|연구실·실제 수하인과 군사·민간 연구용도 미상|미검토||2024 선택 후속사건 연결을 2018 미통제 증거로 쓰지 않음
F07-S02|QKD 장비인지 양자내성 고전암호인지 및 코드/구성품 미상|통신망·수하인·사용자 및 ENC 적격 조건 미상|양자암호|5A002.c|2018판은 QKD를 명시; post-quantum과 개념 구별
F07-S03|SQUID/광펌핑/핵세차 등 방식·주파수·감도·이동잡음 저감 성능 미상|의료 생체자기 진단 전용 여부와 군사·수중 최종용도 미상|양자센서|6A006|모든 양자 센싱 통제 아님; 의료 생체자기 진단 제외 문구도 조건부
F08-S01|배터리·발전기·원자로·전력전자 종류와 정격/에너지밀도 미상|야전·군사 또는 민간 이동전력 용도·최종사용자 미상|미검토||전력 형태부터 특정 필요; 해당 전력 품목 ECCN 미검토
F08-S02|범용 모델링·시뮬레이션 코드와 특수설계 개발 SW 기능 미상|물류·항공·탄도·핵 연구 등 실제 시뮬레이션 대상 미상|미검토||조달자료의 실제 시뮬레이션 플랫폼과 이 분류의 표본 연결 미확인
F08-S03|추적용 RFID·암호·위치센서·서버·SW 중 대상과 성능 미상|민간 자산·군수 자산의 실제 추적 목적·수하인 미상|미검토||자산 가시성이라는 목적만으로 개별 통신·위치장비 분류 불가
F08-S04|DBLS 시스템의 구성·최적화 코드·통신·장비 명세 미상|실제 물류망·군수 기능·운영자 및 접근권자 미상|미검토||분산 물류라는 기술명 외 직접 ECCN 문언 미검토
F09-S01|금속/고분자·공정·CNC 결합·모니터링 기능과 장비/코드 미상|제조 대상·군사 부품·핵 관련 용도 및 수하인 미상|미검토||후속 R06 명확화와 R18 지정 장비 사건을 2018 판정으로 소급 금지
F10-S01|비행/지상로봇·실제 GNSS 안테나·비행시간·풍속·시야 조건 미상|군용 플랫폼 여부·최종용도·실제 수하인과 부품 거래 미상|드론|2B007;9A012|GNSS 변경은 실제 해당 수신기 사용 시에만 관련; 드론 전체 날짜 아님
F10-S02|군집 제어코드와 개별 플랫폼·3D 장면분석·환경성능 미상|군집의 임무·군사/민간 사용자와 실제 제어코드 이전 미상|로봇경계|2B007|2B007 플랫폼 조건 확인만; 군집 알고리즘 직접 ECCN은 미검토
F10-S03|자가조립 메커니즘과 3D 처리·폭발환경·방사선·고도 성능 미상|자가조립 연구·생산·군사 응용과 수하인 미상|로봇경계|2B007|자가조립 능력 자체를 2B007의 요건으로 확인한 것은 아님
F10-S04|분자 조립체·물질·제어기·코드의 법적 대상과 작동성능 미상|생물·의료·나노제조·군사 응용과 실제 사용자 미상|미검토||일반 로봇 문언이 분자로봇에 대응함은 미확인
F10-S05|원문 Robot compliers의 의미·컴파일러/SW 기능·연결 장비 미상|코드가 개발/생산/사용 중 무엇을 지원하는지와 접근자 미상|미검토||원문 철자 보존; 2B007의 2D001 교차참조만으로 SW 직접 분류 불가
F10-S06|센서종류·무선/암호기능·크기·감도·전자부품·코드 구성 미상|분산 감시·민간 계측·군사 목적과 실제 사용자 미상|미검토||작은 센서라는 이유로 특정 센서·통신 ECCN 자동 적용 금지
F11-S01|신경제어 신호 입출력·프로세서·코드/노하우와 성능 미상|의료 보조·민간 제어·군사 용도 및 실제 접근자 미상|신경메모||§744.17 구성품 조건은 BCI 전체의 직접 ECCN과 다름
F11-S02|마음-기계 인터페이스 장비·IC·SW와 실현된 기능 미상|의료·연구·군사 최종용도 및 실제 사용자 미상|신경메모||2018·2021 의견수렴과 기존 구성품 규제를 분리
F11-S03|직접신경 연결방식·감지/자극·IC·코드·기술 이전 미상|이식·의료진단·연구·군사 용도와 수하인 미상|신경메모||직접신경이라는 이름만으로 기술/장비 통제 확정 불가
F11-S04|뇌-기계 신호처리·장치·구성 IC·비공개 개발기술 미상|의료·민간·군사 최종용도 및 실제 당사자 미상|신경메모||다른 BCI 표현들과 중복 범위; 독립 정책충격 4건으로 집계 금지
F12-S01|비행제어 소스코드·특수개발 기술 포함 여부·항법/GNSS 구성 미상|항공·UAV·미사일 플랫폼·실제 최종용도 및 사용자 미상|비행제어|7D003;7D004|7D004의 특정 소스코드와 일반 스케줄링 제외를 구별; GNSS는 부품 경로
F12-S02|램제트/스크램제트/터빈 등 추진방식·부품·코드·기술 미상|군사·미사일·민간 항공 플랫폼과 실제 사용자 미상|추진관할|9A011;9A101;9D001;9E001|9A011은 ITAR 교차참조이며 EAR99나 무통제 선언 근거 아님
F12-S03|흑연·세라믹·탄소복합재의 조성·밀도·입도·크기·용융점 미상|노즈팁·재진입체·미사일·민간 열관리 용도 및 사용자 미상|열재료|1C102;1C107|1C102는 ITAR 교차참조; 1C107의 특정 재료/용도 문턱을 구별
F12-S04|구조·센서 재료의 조성·강도·탄성률·열적/전자기 특성 미상|항공·미사일·민간 구조/센서 용도와 실제 사용자 미상|특수재료|1C010;1C107|구조/센서의 모든 특수재료를 해당 두 ECCN으로 포괄하지 않음
F13-S01|광학/IR/레이더/음향 위장 방식·주파수·흡수율·조성 미상|인체·차량·미사일/UAV 등 플랫폼과 군사/민간 최종용도 미상|위장재료|1C001;1C101|가변 위장과 특정 전자파흡수/저피탐 재료는 다른 범위
F13-S02|섬유 조성·비탄성률·비인장강도·온도·형태·길이 미상|민간 의류·항공복합재·군사 섬유의 실제 용도 및 사용자 미상|섬유|1C010|고기능 섬유 전체가 1C010 아님; 세부 물성/주석 필요
F13-S03|생체재료의 조성·용도·병원성 물질/단순 임플란트 구별 미상|의료 임플란트·조직공학·생물무기 용도와 실제 사용자 미상|미검토||Biomaterials를 유전요소 통제와 자동 동일시하지 않음
F14-S01|얼굴/성문 인식 알고리즘·센서·원시데이터·코드와 기능 미상|민간 인증·법집행 감시·군사 정보수집과 실제 사용자 미상|생체인식경계|4A003;4D001|열람한 CC 문구는 지문장비에 관한 것; 얼굴·성문과 동치 아님'''

records={}
for line in data.splitlines():
 i,spec,enduse,kind,eccn,boundary=line.split('|')
 records[i]=dict(spec=spec,enduse=enduse,kind=kind,eccn=eccn,boundary=boundary)
assert len(records)==47

memo_base='work/research-agent/.local/nov09-review/outputs/round_03/'
memo_map={
'생물':['nov09_bio_cutoff_probe.md','regulatory_audit_rows_nov09.md','verification_bio_cutoff_nov09.md'],
'반도체':['ear_semiconductor_baseline_nov10.md','nov09_soc_bci_cutoff_probe.md'],
'메모리':['nov10_memory_cutoff_probe.md','verification_memory_cutoff_nov10.md','ear_semiconductor_baseline_nov10.md'],
'신경메모':['nov09_soc_bci_cutoff_probe.md'],
'드론':['ear_gnss_change_nov10.md'],
'비행제어':['ear_gnss_change_nov10.md']}
source_rules={
'생물':'2018-01-01 1C353의 목록·서열·독소 요건; 2019-01-01 2B352.j 장비 요건(합성/유전공학만); 기존 2018-04-02 개정 및 Chart 검증은 기존 메모의 한정 범위',
'반도체':'2018-01-01 3A001.a.9 및 3A991.a·b·3E001 표제/허가 주석; 2018-10-24 및 11-02 연결은 기존 메모 범위',
'메모리':'2018-01-01 3A001·3A991.a·b·3E001 표제/주석 및 2019-01-01 분류; MEM-01~05의 기존 검증은 문서 5건 범위이고 두 행 거래 적용은 unverifiable',
'신경메모':'기존 2019-01-01 §744.17/2020 확대/2021 BCI 공고 검토 메모의 범위만 연결; BCI 직접 ECCN 미검토',
'컴퓨터':'2018-01-01 4A003·4A994·4D001·4E001; 2018-10-24 개정지시39·41·42 및 2019-01-01 4A003/4D001/4E001 APP 문턱; 서비스/원격접근 전체 규칙 미검토',
'양자암호':'2018-01-01 5A002.c 및 QKD 기술주석·허가 사유·ENC 조건부 교차참조. 2018-11-18까지 개정 연결과 §740.17 전체는 미검토',
'양자센서':'2018-01-01 6A006 전체 문언의 센서 방식·감도·주파수·의료 생체자기 진단 제외. 다른 양자센서·후속개정 미검토',
'드론':'2018-01-01 2B007·9A012 성능·용도·관련통제 문언; GN18 기존 메모의 2018-12-20 7A005/7A105 변경',
'로봇경계':'2018-01-01 2B007의 3D 처리·폭발환경·방사선·고도 조건과 관련 SW/기술 교차참조. 군집/자가조립 SW 직접 분류 미검토',
'비행제어':'2018-01-01 7D003·7D004의 특정 항법/비행제어 소스코드·일반 요소 제외; 기존 GN18 부품 경로',
'추진관할':'2018-01-01 9A011의 ITAR 교차참조·9A101 엔진·9D001/9E001 관련통제 표제. ITAR 원문·적용 판정 미검토',
'열재료':'2018-01-01 1C102 ITAR 교차참조와 1C107 특정 흑연/세라믹 재료·용도 조건. ITAR 원문·당일 적용 미검토',
'특수재료':'2018-01-01 1C010 물성/주석 및 1C107 특정 재료·용도. 전체 구조재·센서재 목록 미검토',
'위장재료':'2018-01-01 1C001 전자파흡수 재료·제외 및 1C101 저피탐 재료·용도 문언. 모든 가변 위장 방식 미검토',
'섬유':'2018-01-01 1C010 표제·허가사유·비탄성률/비인장강도/재료·형태별 주석. 완성 직물 전체 미검토',
'생체인식경계':'2018-01-01 4A003/4D001의 CC 지문장비 문구만 확인. 얼굴/성문 직접 ECCN과 2018-19 감시 규칙은 미검토',
'미검토':'2018 ANPRM 대표 분류와 §734.10(a)의 공통 관할 경계만 확인; 이 행의 직접 ECCN·품목별 규칙은 미검토'}

common_gap='2018-11-18 직전 유효 문언과 2018-11-19~2019-04-30의 개정·정정·선행공표/창내효력·개별통지 전수연결 미완료. China Chart·Part740 예외·Parts742/744·거래 관할을 행별 확정하지 못함.'
common_user='실제 수출자·원산지/미국산내용·재수출 경로, 구매자·중간/최종수하인·최종사용자의 정확한 법인/주소/거래역할과 당시 등재·지식조건 미상.'
pub='2018 §734.10(a): 특허청에서 이용 가능한 특허/공개출원에 담긴 기술의 EAR 제외를 먼저 판별. 특허수/인용은 간접 역량지표이며 공개특허 자체의 통제기술 이전과 동일시 금지; 미공개 노하우·장비·별도 코드 자동 제외 불가.'
overlay=[]
for r in rows:
 if r['layer']!='subcategory':continue
 i=r['node_id'];d=records[i];h=historical[i]
 known=h['first verified later restriction in selected events']!='미확인'
 direct=d['kind'] not in ['미검토','신경메모']
 status='부분 문언 검토·적용 미확인' if direct else ('기존 메모 부분 연결·직접 ECCN 미검토' if d['kind']=='신경메모' else '행별 직접 ECCN 미검토·추가 검토 필요')
 refs=[memo_base+n for n in memo_map.get(d['kind'],[])]
 if d['eccn']:
  for c in d['eccn'].split(';'):
   c=c[:5];p=OUT/'source_extracts'/f'2018_{c}.txt'
   if p.exists():refs.append(str(p.relative_to(BASE)).replace('\\','/'))
  if i in ['F01-S02','F01-S03']:refs.append('outputs/final_research/regulatory/source_extracts/2019_2B352.txt')
 if d['kind']=='컴퓨터':refs.extend(['outputs/final_research/ip_security/sources/fr2018_oct24_2018_22163.txt','outputs/final_research/verification/primary_sources.md','outputs/final_research/ip_security/gpu_case_legal_scope.md'])
 o={'node_id':i,'원분모_구분':'선택 후속사건 일부 연결 6행' if known else '선택 후속사건 미확인 41행','선택후속사건_ID':h['selected verified restriction event IDs'],'선택후속사건_날짜_원값':h['first verified later restriction in selected events'],'행검토상태':status,'검토분류':d['kind'],'실제열람_ECCN_규칙_범위':source_rules[d['kind']],'ECCN_후보_확정아님':d['eccn'] or '직접 후보 미검토','실제열람_근거파일':'; '.join(dict.fromkeys(refs)) or '공통 ANPRM·§734.10만; 행별 ECCN 근거 미확보','세부사양_공백':d['spec'],'최종용도_공백':d['enduse'],'최종사용자_관할_공백':common_user,'판본_조건_공백':common_gap,'경계_오분류위험':d['boundary'],'2018_10_24_APP완화_행적용':'물리적 컴퓨터·조립품인 하위범위에만 조건부 관련. 4A003.b 16→29WT, 4D001.b.1·4E001.b.1 8→15WT. 실제 구성·APP 미상으로 적용 미확인.' if i=='F02-S10' else '이 행 전체에 APP 완화를 배정하지 않음; 컴퓨터 품목 확인 없이 소급하지 않음','공개특허_관할위험':pub,'기준선_당시미통제_갱신후보':'미확인','창내_추가제한_갱신후보':'미확인','확인청정_완전월수':0,'실제허가거절_인도차단':'미관측','검토수준':'생산자 자체 대조; 본 overlay 독립 검증·심사 대기','검토일':'2026-11-13'}
 overlay.append(o)
byid={o['node_id']:o for o in overlay};extra=[k for k in overlay[0] if k!='node_id']
def write_csv(p,rs,fields):
 with p.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rs)
write_csv(OUT/'regulatory_evidence_overlay.csv',overlay,list(overlay[0]))
candidate=[]
for r in rows:
 n=dict(r);n.update({k:byid[r['node_id']][k] if r['node_id'] in byid else '대상 외: 원본 family/ECCN 사건행 보존' for k in extra});candidate.append(n)
write_csv(OUT/'regulatory_dataset.csv',candidate,list(rows[0])+extra)
unknown=[o for o in overlay if o['원분모_구분'].endswith('41행')]
summary={'원본행수':len(rows),'원본층별행수':dict(collections.Counter(r['layer'] for r in rows)),'원본하위기술ID보존':len(overlay)==47 and [r['node_id'] for r in rows if r['layer']=='subcategory']==[o['node_id'] for o in overlay], '선택후속사건_일부연결':47-len(unknown),'선택후속사건_미확인':len(unknown),'전체47_원본현재미통제여부':dict(collections.Counter(r['기준일 현재 미통제 여부'] for r in rows if r['layer']=='subcategory')),'미통제확인':0,'신규_통제확정':0,'확인청정완전월':0,'전체47_행검토상태':dict(collections.Counter(o['행검토상태'] for o in overlay)),'원41_행검토상태':dict(collections.Counter(o['행검토상태'] for o in unknown)),'원本열셀값순서보존':all(all(c[k]==r[k] for k in r) for c,r in zip(candidate,rows)),'입력SHA256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'독립검증':'대기','규제감사완료':False}
(OUT/'coverage_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[]
for p in sorted((OUT/'source_extracts').glob('*.txt')):
 manifest.append({'파일':str(p.relative_to(BASE)).replace('\\','/'),'SHA256':hashlib.sha256(p.read_bytes()).hexdigest(),'주의':'기계추출 원문; 실제 행 연결 범위는 overlay 실제열람_ECCN_규칙_범위에 한정. 추출 전체=전문 법률검토 아님'})
(OUT/'extract_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
