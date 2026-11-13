from pathlib import Path
import csv,json,hashlib,collections

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[3]
REG=OUT.parent
input_rows=list(csv.DictReader((REG/'regulatory_dataset.csv').open(encoding='utf-8-sig',newline='')))
byid={r['node_id']:r for r in input_rows}
source='https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-part774.xml'
frsource='https://www.govinfo.gov/content/pkg/FR-2018-10-24/html/2018-22163.htm'

# 아래 문구는 실제 읽은 한정 단락의 요약이다. 추출 파일 전체를 검토했다는 뜻이 아니다.
data='''F02-S02|4D001;4D994|4D001.a는 통제된 4A001/4A003/4A004 또는 특정 4D 품목의 개발·생산용으로 특별설계/수정된 SW, b는 특정 APP 컴퓨터·집계조립품 개발·생산용 SW이다. 4D994 표제는 4A101/4A994 장비의 개발·생산·사용용 특별설계/수정 SW이다.|유전알고리즘의 최적화 대상이 실제 통제 컴퓨터/장비 개발·생산인지, 독립 응용코드인지와 설계변경·배포물 미상. genetic이라는 명칭은 생물 유전요소가 아니다.|최적화가 연구·공정·군사 중 어디에 사용되는지 미상.|4D001 Items a,b; 4D994 표제 및 Items|4D001;4D994
F02-S03|2D001;2B007|2D001.a는 2A001 또는 2B001~009 장비의 개발·생산용, b는 열거된 장비의 사용용 특별설계/수정 SW이다. 2B007은 실시간 완전 3D 처리/장면분석, 폭발물환경, 5×10^3Gy 초과 방사선 또는 30000m 초과 고도 조건을 가진 로봇과 전용 제어기·말단장치이다.|보상학습 코드가 훈련도구인지 실제 로봇 사용/개발 SW인지, 로봇의 3D 처리·환경 성능·전용성 미상.|게임·산업로봇·군사제어 중 실제 배치 대상과 임무 미상.|2D001 Items a,b 및 Note; 2B007 Items a~d·관련 주석|2D001;2B007
F02-S05|4D001;4D994|4D001.a의 통제 장비/SW 개발·생산 연계와 4D994 표제의 특정 장비 개발·생산·사용 연계를 확인했다. 규칙 기반 의사결정·교육 시스템 자체라는 이유만으로 이 설계관계를 입증할 수 없다.|지식베이스·추론엔진·통제장비용 개발도구 중 거래대상, 대상장비의 ECCN 및 특별설계/수정 관계 미상.|교육·의료·군사 의사결정의 실제 용도·배치기관 미상.|4D001 Items a,b; 4D994 표제 및 Items|4D001;4D994
F02-S06|5A001.b.6;5D001.a,c|5A001.b.6은 디지털 신호처리로 음성코딩 출력 700bit/s 미만을 제공하는 통신시스템·장비와 전용 부품/부속품이다. 가변율은 연속음성 출력 기준이며 사람음성 샘플을 특성을 고려한 디지털 신호로 바꾸는 음성코딩 정의를 읽었다. 5D001.a,c는 5A001 장비/기능 개발·생산·사용 또는 해당 기능 제공용 전용 SW이다.|음성인식/합성인지 실제 음성코덱인지, 연속음성 비트율·통신장비/부품 여부·SW 전용성 미상.|민간 음성서비스·통신·감청 용도와 실제 운용기관 미상.|5A001 Items b 서문,b.6 및 Technical Notes 1,2; 5D001 Items a,c|5A001;5D001
F02-S07|4D001;4D994|4D001.a,b와 4D994 표제는 특정 통제 컴퓨터/장비의 개발·생산 또는 사용과의 특별설계/수정 관계를 요구한다. 기계번역 기능이라는 이름은 그 관계를 직접 보여주지 않는다.|번역 모델·가중치·소스·개발도구 중 이전대상, 공개 여부 및 통제 하드웨어 개발/생산/사용용 설계관계 미상.|일반 언어서비스·정보분석·군사 응용과 접근당사자 미상.|4D001 Items a,b; 4D994 표제 및 Items|4D001;4D994
F02-S08|7D004|7D004는 7E004의 특정 개발기술을 포함하는 소스코드이며 총비행제어·추진/비행 통합제어 등 열거 시스템에 관한 것이다. Note는 특정 비행제어 기능을 제공하지 않는 일반 컴퓨터 요소·유틸리티 소스코드와 task scheduling mechanisms를 제외한다.|일정/게임 코드가 소스코드인지, 열거 개발기술을 포함하는지와 특정 비행제어 기능 여부 미상. 7E004 본문은 이번에 미검토.|물류 일정·게임·항공비행 임무 중 실제 스케줄링 대상 미상.|7D004 표제, Items a~g, Note|7D004
F02-S09|5A001.b.6;5D001.a,c|5A001.b.6의 음성코딩은 통신장비에서 700bit/s 미만 출력이라는 기능·성능 경계이다. 5D001.a,c는 5A001 통제 기능과의 전용 설계/수정 연계를 요구한다. 합성음성·영상 조작 표지만으로 그 요건을 충족시키지 못한다.|voice cloning/deepfake 생성기와 통신용 음성코딩을 구분할 기능설명, 출력률, 실제 장비/SW 및 특별설계 관계 미상.|콘텐츠 제작·기만·감시 중 실제 용도 및 운영기관 미상.|5A001 Items b.6, Technical Notes 1,2; 5D001 Items a,c|5A001;5D001
F06-S01|7D004.g;4D001|7D004.g의 three dimensional displays도 표제의 특정 개발기술 포함 소스코드 요건과 Note의 특정 비행제어 기능 경계를 함께 읽어야 한다. 4D001.a,b는 특정 장비/SW 개발·생산용 특별설계/수정 SW이다.|일반 시각화/렌더러인지 비행표시장치 소스인지, 7E004 개발기술 포함 여부와 통제 장비 개발·생산용 설계관계 미상.|연구 데이터 시각화·비행표시·군사 임무표시의 실제 용도 미상.|7D004 표제, Items g 및 Note; 4D001 Items a,b|7D004;4D001
F06-S03|7D003.a,b;7A005|7D003.a는 7A003/004/008 통제 수준으로 항법성능 개선/오차 감소하는 전용 SW, b는 heading과 Doppler/GNSS/DBRN 데이터를 계속 결합해 7A003/008 수준으로 개선하는 하이브리드 통합시스템 소스이다. 2018-01-01 7A005는 정부용 복호나 적응형 안테나 GNSS에 대한 ITAR 교차참조이다.|일반 상황인식과 항법융합 소스 구분, 실제 항법오차·센서조합·정부용 복호/공간널 생성 안테나 여부 미상.|휴대폰 위치서비스·자율주행·군사항법 중 실제 사용 플랫폼 미상.|7D003 Related Definitions(DBRN), Items a,b.1~3; 7A005 표제·Related Controls·Items a,b 및 Note/Technical Note|7D003;7A005
F08-S01|3A001.e.1;3A991.j|3A001.e.1은 20°C에서 1차 셀 550Wh/kg 초과 또는 2차 셀 350Wh/kg 초과이며 에너지밀도·셀 정의와 배터리(단일셀 배터리 포함) 제외 Note를 읽었다. 3A991.j는 1차 셀 550Wh/kg 이하, 2차 셀 300Wh/kg 이하 및 동일 배터리 제외이다. 이 문언만으로 300~350 구간 또는 다른 전력기기를 분류하지 않는다.|셀/배터리팩/발전기/연료전지/원자로/전력전자 중 실제 물품, 재충전성·20°C 정격·전압/용량/질량 미상.|민간 이동전원·야전 군수·우주 전력의 실제 용도 미상.|3A001 Items e.1.a,b, Technical Notes 1~4 및 바로 뒤 Note; 3A991 Items j.1,j.2·Note·Technical Notes 1~4|3A001;3A991
F08-S02|9D103;7D003.e|9D103은 미사일 또는 열거된 추진 등 하위시스템의 모델링·시뮬레이션·설계통합용 특별설계 SW에 관한 ITAR 교차참조이다. 7D003.e는 열거 7E004 기술의 능동비행제어/헬기 제어 개발용 전용 CAD SW이다.|범용 물류 시뮬레이션인지 미사일/항공제어 개발도구인지, 모델링 대상·연결 하위시스템·특별설계 여부 미상. ITAR와 7E004 본문은 미검토.|재고/배차·민간 항공·미사일 개발 중 실제 시뮬레이션 목적 미상.|9D103 표제 전체; 7D003 Items e|9D103;7D003
F08-S03|5A001.g;7A005|5A001.g PCL은 비레이더 송신기의 주변 RF 반사를 측정해 이동물체를 검출·추적하는 전용 장비이고 표적의 무선송신을 요구하는 장비는 제외한다. 7A005는 정부용 복호·적응형 안테나 GNSS에 관한 당시 ITAR 교차참조이며 통상 상용 GNSS의 7A994 안내가 있다.|RFID의 표적 송신 기반인지 수동 RF반사 PCL인지, GNSS 복호/안테나 방식·실제 서버/태그/수신기/SW 구성이 미상. 7A994 본문은 미검토.|일반 재고자산·군수자산 추적과 실제 이동체/시설 운용 미상.|5A001 Items g, Technical Note 및 Note a,b; 7A005 Related Controls, Items a,b 및 주석|5A001;7A005
F08-S04|5D001.a,c;5D002.a.1,c.1;5A002.a|5D001.a,c는 통제 5A001 통신장비/기능 전용 SW이다. 5D002.a.1,c.1는 5A002 장비 관련 전용 SW 또는 그 기능을 수행/모사하는 SW이며 OAM 전용·공개/상업 암호표준 예외와 적격 mass-market 분류 교차참조가 있다. 5A002.a는 데이터기밀성 암호의 키길이/기능 조건과 예외를 둔다.|DBLS의 배포·통신·암호 SW 구성, 키길이·정보보안 기능·OAM 한정성·분류/자체분류 자료·상용 적격 여부 미상.|분산 물류망이 민간 운송인지 군수지휘/보급인지와 운영망 미상.|5D001 Items a,c; 5D002 Related Controls/Definitions, Items a.1,c.1 및 c.1 Note; 5A002 Items a 서문,a.1~4 및 Technical Notes 1,2|5D001;5D002;5A002
F10-S04|2B007;§772.1 Robot|2018 Robot 정의는 다기능·3차원 위치/방향 변경·3개 이상 서보장치·사용자 접근 프로그래밍을 모두 요구한다. 2B007은 정의에 추가로 실시간 완전 3D 처리/장면분석 또는 열거 위험환경/방사선/고도 조건을 가진 로봇 등을 대상으로 한다.|분자 조립체가 기계적 조작 메커니즘/서보/사용자 프로그래밍 정의를 만족하는지, 물질·장비·제어코드 중 대상 및 2B007 조건 미상.|의료 분자운반·나노제조·생물/군사 응용 중 실제 용도 미상.|§772.1 Robot (a)~(d), Note(a)~(e); 2B007 표제·Items a~d 및 주석|2B007
F10-S05|2D001|2D001.a는 특정 2A001/2B001~009 장비 개발·생산용, b는 열거 장비 사용용 특별설계/수정 SW이다. Note는 여러 부품 가공의 NC코드를 생성하는 part programming SW를 제외한다. 이 제외는 모든 컴파일러나 로봇 SW에 대한 포괄 제외가 아니다.|원문 Robot compliers 의미를 확정할 자료, 컴파일/NC생성/로봇 제어 중 기능, 연결 장비 품목 및 특별설계 관계 미상. 원문 철자는 보존한다.|코드가 개발·생산·사용 어느 작업을 지원하며 누가 사용하는지 미상.|2D001 표제, Items a,b 및 Note|2D001
F10-S06|5A001.b.3,b.4;5A002.a;3A991.a|5A001.b.3은 사용자 프로그래밍 확산코드 등 조건의 확산대역 무선이며 1W 이하 출력 제외가 있다. b.4는 사용자 프로그래밍 코드의 UWB와 500MHz 초과 대역폭 또는 20% 이상 부분대역폭 조건이다. 5A002.a와 Note2.f는 기밀성 암호 및 PAN 전용/상용표준/30m 또는 최대7기기·100m 조건을 둔다. 3A991.a는 마이크로프로세서 등의 성능/클록/외부연결 문턱이다.|dust 센서의 프로세서·주파수·출력·확산/UWB 대역폭·코드변경성·암호키길이·PAN 거리/연결수·비트폭/클록 미상.|환경계측·분산 감시·군사 센서망 중 실제 배치 목적·장소 미상.|5A001 Items b.3,b.4 및 b.3 Notes; 5A002 Items a 및 Note2.f; 3A991 Items a.1~3|5A001;5A002;3A991
F13-S03|1C351;1C353;1C991|1C351 License Requirement Notes 1,4,5는 열거 병원체/독소·분리 생배양/독소제제와 백신 등 제외/1C991 이동의 경계이다. 1C353은 특정 병원성/독소 핵산서열을 가진 유전요소/변형생물과 정의를 요구한다. 1C991은 정의에 해당하는 백신·면역독소·특정 독소 의료제품/키트이다.|임플란트 고분자/생물유래 재료/생배양/독소/유전요소 중 대상, 조성·서열·제형·FDA/USDA 승인 및 제품/벌크 형태 미상.|정형외과 임플란트·조직공학·의료진단·생물무기 중 실제 용도 미상.|1C351 License Requirement Notes1,4,5; 1C353 Items a,b 및 Technical Notes1~4; 1C991 Related Definitions 및 Items a~e|1C351;1C353;1C991
F01-S04|6A006.a.1;3A991.a|6A006은 의료진단용 생체자기 측정에 특별설계된 계측기를 이 entry에서 제외한다고 한다. a.1 SQUID는 정지/이동잡음 및 1Hz 감도 문턱을 구별한다. 3A991.a는 마이크로프로세서/마이크로컴퓨터/마이크로컨트롤러의 성능·클록·연결 문턱이다.|신경기술이 MEG/SQUID 의료진단 전용인지 일반 자기센서인지, 정지/이동 감도와 구성 프로세서의 사양 미상. 신경자극/EEG 전체는 포괄하지 않는다.|의료진단 전용·연구·보조기 제어·군사 응용 중 실제 용도 미상.|6A006 Related Controls 및 Items a.1.a,b; 3A991 Items a.1~3|6A006;3A991
F11-S01|3A991.a,c|3A991.a의 마이크로프로세서 등은 5GFLOPS 및 32bit ALU, 25MHz 초과 클록 또는 특정 병렬 외부연결 문턱을 가진다. c는 3A001에 해당하지 않는 ADC에 해상도/출력률 조합 문턱을 둔다.|신경제어 인터페이스의 완제품/구성칩 구분, 프로세서 ALU/클록/연결률, 신호취득 ADC 해상도·출력률 미상.|보조기 신경제어·의료·군사 제어 중 실제 장치와 임무 미상.|3A991 표제 및 Items a.1~3,c.1~4|3A991
F11-S02|3A001.a.9;3A991.a|3A001.a.9는 neural network integrated circuits라는 전자 품목 문언이다. 생물학적 신경 인터페이스라는 뜻으로 확장할 수 없다. 3A991.a는 별도 비해당 프로세서의 성능·클록·연결 조건이다.|마음-기계 시스템이 실제 신경망 IC를 포함하는지 일반 프로세서인지, 칩 설계/기능·연산속도·ALU 폭·클록 미상.|의료/연구용 인터페이스·민간 제어·군사 사용 중 실현된 기능 미상.|3A001 Items a 서문,a.9; 3A991 표제 및 Items a.1~3|3A001;3A991
F11-S03|3A001.a.5.a;3A991.c|3A001.a.5.a의 ADC는 해상도 구간별 출력률 문턱을 둔다(예: 16bit 이상은 65MSPS 초과). 출력률/다중채널/인터리브 기준의 Technical Notes를 함께 읽었다. 3A991.c는 3A001 비해당 ADC의 더 낮은 문턱을 둔다.|직접신경 연결 장치가 분리 ADC IC인지 통합 감지/처리 IC인지, 해상도·최대출력률·다중채널/인터리브 구성 미상. 전체 이식장치를 ADC로 분류하지 않는다.|치료·진단·연구·군사 직접신경 신호취득 중 실제 용도 미상.|3A001 Items a.5.a.1~5 및 Technical Notes1~9; 3A991 Items c.1~4|3A001;3A991
F11-S04|3A991.a;4D001;4D994|3A991.a는 특정 프로세서 성능 조건이다. 4D001.a,b와 4D994 표제는 특정 장비/SW의 개발·생산 또는 사용용 특별설계/수정 SW를 대상으로 하며, 뇌-기계 제어 응용 자체와는 설계관계의 확인이 필요하다.|완성 BCI·구성 프로세서·신호처리 앱·장비 개발코드 중 이전대상, 칩사양·지원장비 분류·특별설계 관계 미상.|임상·민간 보조·군사 기계조작의 실제 목적과 운용기관 미상.|3A991 Items a.1~3; 4D001 Items a,b; 4D994 표제 및 Items|3A991;4D001;4D994'''

common_user='실제 수출자·원산지/미국산 내용·재수출 경로와 구매자/최종수하인/최종사용자의 법인·주소·거래역할·당시 등재·지식조건 미상. 후보 문언만으로 중국행 허가의무/거절을 확정하지 못함.'
common_version='2018-01-01 연간판. 2018-11-18 직전 유효문언 또는 2018-11-19~2019-04-30 전체 개정·정정·효력 연결을 확정하지 않음.'
common_pending='부분 문언 검토·적용 미확인 (pending(scope)); 미통제 확인 아님; 감사창 추가제한·최초 통제일·현재통제·허가거절 미확인'
rows=[]
for line in data.splitlines():
    i,eccn,scope,spec,enduse,loc,extracts=line.split('|')
    r=byid[i]
    files=['outputs/final_research/regulatory/remaining_review/source_extracts/2018_'+c+'.txt' for c in extracts.split(';')]
    urls=[source]
    if i=='F10-S04':
        files.append('outputs/final_research/ip_security/sources/cfr2018_772-1.xml')
        urls.append('https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec772-1.xml')
    app='행 전체에 적용하지 않음. 컴퓨터 개발·생산 SW 하위범위에서만 2018-10-24 4D001.b.1 APP 8→15WT와 조건부 관련. 실제 대상장비/APP·특별설계 관계 미상.' if '4D001' in eccn else 'APP 컴퓨터 완화를 이 기술행 전체에 배정하지 않음.'
    if '4D001' in eccn:
        urls.append(frsource)
        loc+='; 2018-10-24 83FR53771~53772 개정지시41(4D001.a,b.1,b.2)'
        files.append('outputs/final_research/regulatory/remaining_review/source_extracts/FR2018_22163_APP_review.txt')
    rows.append({'row_id':i,'기술':r['subcategory'],'원분모_구분':r['원분모_구분'],'기존_행검토상태':r['행검토상태'],'실제열람_ECCN_후보_확정아님':eccn,'조문문언_실제검토범위':scope,'판본':common_version,'세부사양_제한':spec,'최종용도_제한':enduse,'최종사용자_관할_제한':common_user,'판정':common_pending,'source_url':'; '.join(urls),'locator':loc,'실제열람_근거파일':'; '.join(files),'APP_완화_행적용경계':app,'미검토범위':'모든 ECCN·ITAR·개정연결·China Chart·Part740 예외·Parts742/744의 행별 전체 적용은 미검토. 후보를 벗어난 다른 통제 부재를 증명하지 않음.','검토일':'2026-11-13','검토수준':'생산자 부분 대조; 독립 검증·심사 대기'})

assert len(rows)==22 and len({r['row_id'] for r in rows})==22
direct=[r for r in rows if r['기존_행검토상태']=='행별 직접 ECCN 미검토·추가 검토 필요']
memo=[r for r in rows if r['기존_행검토상태']=='기존 메모 부분 연결·직접 ECCN 미검토']
assert len(direct)==17 and len(memo)==5
assert all(r['원분모_구분']=='선택 후속사건 미확인 41행' for r in rows)
for r in rows:
    for p in r['실제열람_근거파일'].split('; '): assert (BASE/p).exists(),p
with (OUT/'remaining_eccn_addendum.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'검토행수':22,'기존_직접ECCN미검토17':len(direct),'기존_신경메모5':len(memo),'선택후속사건_원분모':{'일부연결':6,'미확인':41},'전체47_현재미통제여부':'47 모두 미확인 유지; 본 addendum은 22행 후보 문언 검토만 추가','미통제확인':0,'신규통제확정':0,'확인청정완전월':0,'원본수정':False,'cutoff확정':False,'전수ECCN_전수개정검토':False,'독립검증':'대기','원본현황SHA256':{p:hashlib.sha256((REG/p).read_bytes()).hexdigest() for p in ['regulatory_dataset.csv','regulatory_evidence_overlay.csv','coverage_summary.json']}}
(OUT/'review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 잔여행 후보 ECCN 문언 검토 추가자료','', '2018-01-01 연간 CCL의 실제 해당 단락과 2018-10-24 개정지시 41의 4D001 문언을 읽고 만든 제한적 추가자료이다. 기존 데이터셋·overlay·coverage summary·과거 심사/Gate는 변경하지 않았다. 문서검색 hit를 검토 근거로 쓰지 않았다. 추출파일 전문과 실제 검토범위는 다르다.','', '선택 후속사건 일부 연결 6/미확인 41은 round2 사건 링크의 분모이며, 전체 47행의 현재 미통제 여부는 모두 미확인이다. 이번 22행은 원41 중 직접 ECCN 미검토 17와 기존 신경메모 5에 해당한다. 후보 문언을 읽었다는 뜻이며 후보 충족·미충족, 미통제 또는 감사창 추가제한은 확정하지 않는다. 모든 ECCN·모든 개정 연결 검토가 아니고 cutoff도 확정하지 않았다. 독립 검증·심사는 대기 상태다.','', '## 행별 실제 검토','', '| 행 ID | 기술 | 실제 열람 후보 | 실제 문언 범위와 판정 |','|---|---|---|---|']
for r in rows: md.append('| '+r['row_id']+' | '+r['기술']+' | '+r['실제열람_ECCN_후보_확정아님']+' | '+r['조문문언_실제검토범위']+' 적용 미확인. |')
md+=['','세부사양·최종용도·최종사용자/관할의 행별 제한, 정확한 출처 URL·locator·근거파일은 remaining_eccn_addendum.csv에 기록했다. 공개특허 자체·미공개 노하우·장비·별도 코드의 EAR 관할은 구분해야 하며 이 추가자료는 기존 §734.10 메모를 확대하지 않는다.','', '## 확인된 경계','', '- 4D001/4D994는 일반 AI·번역·전문가시스템·시각화·BCI SW 전체를 통제하는 문언으로 읽을 수 없다. 실제 지원 장비·개발/생산/사용 목적·특별설계/수정 관계를 특정해야 한다. 반대로 범용 기술명만으로 모든 관련 SW가 미통제라고 결론내릴 수도 없다.','- 2018-10-24 지시41은 4D001.b.1 APP를 15WT로 재기재하며 a의 특정 장비/SW 개발·생산 연결은 계속 요구한다. 1월판 b.1은 8WT이다. 이 조건부 변경을 22행 전체의 규제완화로 집계하지 않는다.','- 3A001.e.1/3A991.j의 셀과 배터리 제외, 5A001.b.6의 700bit/s 미만 음성코딩, 7D004의 특정 비행제어 소스와 일반 task scheduling 제외, 9D103/7A005의 당시 ITAR 교차참조는 서로 다른 경계다. 다른 관할 또는 다른 ECCN이 없다는 뜻이 아니다.','- Biomaterials라는 명칭은 1C351/353/991의 병원체·서열·독소·제형 요건을 입증하지 않는다. neural network IC라는 전자 품목 명칭도 생물학적 신경 인터페이스 전체와 동의어가 아니다.','', '## 원문과 재현','', '- 로컬 원문: outputs/final_research/ip_security/sources/cfr2018_part774.xml의 FDSYS DATE=2018-01-01; Supplement No.1의 각 ECCN 항목. source_extracts는 이 원문에서 기계 추출했다. extract_manifest.json의 SHA256을 함께 보존한다.','- 직접 대조 출처: [2018 CCL 원문](https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-part774.xml), [2018 정의](https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec772-1.xml), [2018-10-24 규칙](https://www.govinfo.gov/content/pkg/FR-2018-10-24/html/2018-22163.htm). 온라인 XML/PDF 열기는 도구의 content-type/timeout으로 실패했으므로 읽은 법내용은 로컬 보존 원문에 근거한다.','- regulatory/raw_source_documents 폴더는 관측되지 않았다. 이 추가자료는 새로운 외부 다운로드나 최신 현행법 검토를 주장하지 않는다.','']
(OUT/'remaining_eccn_addendum.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
