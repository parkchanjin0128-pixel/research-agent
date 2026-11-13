# 2026-11-13 규제 부록 독립 검증

판정: **verified — 아래 한정 범위의 새 사실에 한함.** 전체 47행 규제감사·법률의견·China-binding cutoff 검증은 완료되지 않았다. 미통제 확인 0, 신규 중국행 binding 확정 0, 확인 청정 완전월 0을 유지한다.

검증자 `/root/nov13_regulatory_final_verify`; 생산자 `/root/nov13_regulatory_scope`, `/root/nov13_remaining_regulatory`; 통합자 `/root`. 확인시각 2026-11-13T07:50:48.951263+00:00. 작성·상태·Gate 파일을 수정하지 않았다.

## 범위와 독립 검산

원본은 `work/research-agent/.local/nov09-review/outputs/round_03/regulatory_dataset.csv`(SHA256 `66609889115208f62e9e25b6f93e67b8c6b72489a866e30fc119e21b4f8ddd33`)이며, 최상위 `outputs/regulatory_dataset.csv`와 구별했다. 원본81행=family14/subcategory47/ECCN20, 원본 열의 셀값·행순서·47개ID가 보존된다. 선택 후속사건의 분모는 round02 `announcement_window_audit.csv`에서 직접 재계산한 일부 연결6/미확인41이다. 단순히 규제표의 final-rule 칸이 비어 있는지 세는 계산과 다르다.

초기 overlay는 전체47: 부분문언20/기존메모5/직접미검토22, 원41: 부분문언19/메모5/직접미검토17이다. 추가22ID는 원41의 직접미검토17+신경메모5와 정확히 일치하고 중복이 없다. ID 결합 후 전체47은 부분문언42/직접미검토5, 원41은41 모두 부분문언·적용미확인이다. 42라는 수는 후보문언 근거를 연결한 장부상 범위이며 42행의 모든 법적 적용을 독립 검증했다는 뜻이 아니다.

직접미검토로 남는5개: F02-S01, F02-S04, F06-S02, F07-S01, F09-S01. 원47의 현재미통제 여부·기준선 미통제 갱신후보·창내 추가제한 갱신후보는 전부 미확인이고 청정월 칸은47행 모두0이다. 초기 coverage_summary는 추가검토 이전 이력으로서 정확하며 덮어쓰지 않았다. input_comparison의 원본/저장원격 사본 간 차이6개ID·열목록도 독립 재현했다. 저장된 원격 사본의 Git 서버 HEAD 자체를 재검증한 것은 아니다.

## 원문 접근과 정확한 확인 위치

공식 [2018 CCL XML](https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-part774.xml), [2018 §772.1 정의](https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec772-1.xml), [2018-10-24 FR2018-22163](https://www.govinfo.gov/content/pkg/FR-2018-10-24/html/2018-22163.htm)를 직접 GET해 HTTP200을 확인했다. 브라우저 도구의 XML 형식/접근 실패와 실제 HTTP 접근 성공을 구별했다. XML의 FDSYS DATE는2018-01-01이다.

| 원문 | HTTP·본문 대조 | SHA256(현재 HTTP 응답) |
|---|---|---|
| 2018_CCL | 200 · 로컬과 바이트 동일 | `8a909740fda2ba36c065d3f2cb8ddf6614b88271920099243d8a6fb7a2e3d19f` |
| 2018_definitions | 200 · 로컬과 바이트 동일 | `0101a16193c6f13452f3591c33ae71c60a940e738e01083850c911922977ceeb` |
| 2018_oct24 | 200 · 로컬과 HTMLParser 본문·지시41 동일; raw bytes 다름 | `12d0664bedc13828ad967de2fdc1501ed314e0b21b2ac01baf8688d8215682a7` |

원문 로컬SHA·HTTP시각·content type·source locator·원문 관찰단락은 동반JSON에 보존했다. 추가자료의20개 ECCN 추출은 공식HTTP와 바이트가 동일한 보존XML에서 독립 재추출해 저장추출과 전부 일치했다. 초기47개 추출파일과 추가20개 추출파일의 manifest 해시도 전부 일치한다. 기계추출 전문의 일치는 전문 법률검토 완료를 뜻하지 않는다. `source_manifest.json`은 이 규제폴더에 없으며 실제 `extract_manifest.json`, `source_extract_index.json`, `remaining_review/extract_manifest.json`을 확인했다.

주요 인쇄페이지/단락: 4D001 a,b=914;4D994=914;5A001 b.3,b.4=917/b.6,g=918;5D001 a,c=923;5A002 a/주석=928–930;5D002 a.1,c.1=931;3A001 ADC=879/신경망IC=880/셀=885;3A991 a,c=895/j=896;6A006 의료진단 제외·SQUID=949;7A005=972;7D003=978–979;7D004=979;9D103=1018;2B007=847;2D001=865;1C351 주석=814–816/1C353=817/1C991=823–824. XML의 PRTPAGE는 페이지 전환 표식이므로 JSON은 단락 시작시점 페이지도 별도 기록했다.

## 22행 후보 문언 대조

아래22행은 후보 문언에 대한 사실만 verified이다. 각 행의 실제 물품·코드·세부사양·특별설계 관계·최종용도·사용자·EAR/ITAR 관할·중국행 허가/거절은 **unverifiable**로 유지한다. locator는2018-01-01 Supplement No.1 to Part774 기준이며 §772.1/Oct24 표시는 별도 원문이다.

| 행ID | 직접 대조 locator | 확인 조건·제외와 확대 방지 |
|---|---|---|
| F02-S02 | 4D001.a,b;4D994 heading; Oct24 instruction41 | 특정 통제장비/SW 개발·생산 또는 지정장비 사용과의 특별설계/수정 관계. 유전알고리즘 자체 분류 아님. |
| F02-S03 | 2D001.a,b,Note;2B007.a~d,Notes | 강화학습 자체 분류 아님. 2B007.a는 3D 처리/장면분석으로 프로그램/수치프로그램 데이터를 생성·수정하는 목적까지 필요. b의 도장부스 제외도 확인. |
| F02-S05 | 4D001.a,b;4D994 heading; Oct24 instruction41 | 전문가/교육/의사결정지원이라는 응용명만으로 특정 통제장비/SW와 설계관계가 성립하지 않음. |
| F02-S06 | 5A001.b intro,b.6,Technical Notes1~2;5D001.a,c | 통신장비·전용 부품/부속품, 음성코딩 출력700bit/s 미만; 가변율은 연속음성. 인식/합성 전체 통제 아님. |
| F02-S07 | 4D001.a,b;4D994 heading; Oct24 instruction41 | 기계번역 자체 표지는 통제장비 개발/생산/사용용 특별설계/수정 관계의 입증이 아님. |
| F02-S08 | 7D004 heading,a~g,Note | 특정7E004 개발기술 포함 소스와 열거시스템 조건. 특정 비행제어 기능 없는 일반 task scheduling 등은 이 entry에서 제외. |
| F02-S09 | 5A001.b intro,b.6,Technical Notes1~2;5D001.a,c | 음성코딩700bit/s 미만과 통신장비/전용SW 관계를 요구. voice cloning/deepfakes 전체로 확대하지 않음. |
| F06-S01 | 7D004 heading,g,Note;4D001.a,b; Oct24 instruction41 | three dimensional displays도 특정 개발기술 포함 소스라는 표제 조건과 함께 읽음. 모든 시각화 SW 아님. |
| F06-S03 | 7D003.a,b.1~3,DBRN definition;7A005 heading,Items,Notes | 항법개선 수준·heading의 지속결합 조건 확인. 정부용 복호/적응형 GNSS의 당시 ITAR 교차참조를 무통제로 읽지 않음. |
| F08-S01 | 3A001.e.1.a,b,Technical Notes1~4,Note;3A991.j.1~2,Notes | 20°C 1차>550/2차>350 Wh/kg와 하위 entry의<=550/<=300. 단일셀 포함 배터리 제외는 해당 entry 경계. 300~350구간·다른 전력기기 분류 안함. |
| F08-S02 | 9D103 heading;7D003.e | 미사일/열거하위시스템 모델링의 특별설계SW는 당시 ITAR 교차참조. 별도7E004 관련 비행제어 개발CAD 조건. 범용 시뮬레이션 전체 아님. |
| F08-S03 | 5A001.g,Technical Note,Note a,b;7A005 Related Controls,Items,Notes | PCL의 비레이더 주변RF 반사·이동물체 검출추적과 표적송신 요구장비 제외. GNSS의 정부용 복호/적응형 안테나 조건 구별. |
| F08-S04 | 5D001.a,c;5D002.a.1,c.1,Note,Related Controls;5A002.a,Technical Notes | 통제 통신/암호기능과의 설계관계, 데이터기밀성·키길이 및 OAM 한정/공개·상업표준 예외. mass-market는 적격 분류/자체분류 후 교차참조. |
| F10-S04 | 772.1 Robot(a)~(d),excluded(a)~(e);2B007.a~d,Notes | Robot의 네 가지 누적 요건과 제외장치 확인. 추가2B007 성능/환경요건 필요. 분자 조립체에 자동 적용하지 않음. |
| F10-S05 | 2D001 heading,a,b,Note | 특정 장비 개발/생산/사용SW와 NC part-programming 제외. 원문compliers 철자 보존. 모든 컴파일러/로봇SW 제외 아님. |
| F10-S06 | 5A001.b.3,b.4,Notes;5A002.a,Note2.f;3A991.a.1~3 | 확산무선1W 이하 제외, UWB 사용자프로그래밍·대역폭 조건; PAN의 상용표준/거리/기기수 조건. dust라는 명칭으로 분류하지 않음. |
| F13-S03 | 1C351 License Requirement Notes1,4,5;1C353.a,b,Technical Notes;1C991 definitions,a~e | 목록병원체/독소, 분리생배양·독소제제 및 특정 핵산서열·제형 조건. 백신 등1C991 이동은 미통제 뜻 아님. Biomaterials 전체로 확대 안함. |
| F01-S04 | 6A006 Related Controls,a.1.a,b;3A991.a.1~3 | 의료진단용 생체자기 측정에 특별설계된 계측기 제외와 SQUID 정지/이동잡음·1Hz 감도 구별. 모든 신경기술 아님. |
| F11-S01 | 3A991 heading,a.1~3,c.1~4 | 프로세서 성능/ALU·클록·외부연결과 ADC 해상도/출력률 조건. 완성 신경제어 인터페이스 전체에 자동적용 안함. |
| F11-S02 | 3A001.a intro,a.9;3A991 heading,a.1~3 | neural network integrated circuits는 전자 품목 문언. 생물학적 신경 인터페이스 전부와 동의어가 아님. |
| F11-S03 | 3A001.a.5.a.1~5,Technical Notes1~9;3A991.c.1~4 | 16bit이상>65MSPS 예시 및 다중채널/인터리브 출력률 기준 확인. 전체 이식장치를 ADC로 분류하지 않음. |
| F11-S04 | 3A991.a.1~3;4D001.a,b;4D994 heading; Oct24 instruction41 | 프로세서 조건과 특정장비 개발/생산/사용SW의 특별설계관계를 구별. BCI 응용 자체가 포괄통제 근거 아님. |

2B007의 생산자 요약은 간략화된 문장이다. 원문a의 프로그램/수치프로그램 데이터 생성·수정 목적, b의 폭발성 탄약환경 국가안전기준 및 도장부스 제외도 적용검토 시 함께 읽어야 한다. 저장원문은 이를 포함하고 있고 이번22행에는 긍정적 적용판정이 없으므로 해당 요약에서 새로운 통제확정을 도출하지 않았다.

## 개정 연결·통합본·판정 한계

2018-10-24 83FR53771–53772 지시41의4D001.b.1은APP15WT이고 1월판은8WT다. 같은지시의a는 특정4A/4D 품목의 개발·생산용 특별설계/수정 조건을 유지한다. b.2의집계조건, TSR/STA의29WT는 b.1의15WT와 구별했다. 이 선택된 두 문언 대조만으로 1월→10월 전체개정 연결이나11월18일 직전 유효문언이 폐쇄되지는 않는다. 이를 AI·음성·물류·BCI 전체의 완화로 집계할 근거는 없다.

통합CSV의 현재SHA256은 `32473a33630b14419fd6810d276104028825065c794a7ecac1c21e3b0556d221`이다. 81행순서·원본27열(나머지 원본입력열도 포함)의 값보존,22ID만 추가열 결합, 기존셀 변경이22행의 부분문언 상태 상향에 한정됨,42+5/원41모두부분문언,미통제·창내추가제한 미확인/청정0을 독립검산했다. 이것은 기계적 통합의 verified이며 기존20행의 전체규제검증으로 확대할 수 없다.

범용기술 전체 통제·미통제, 중국행 binding 최초일, 실제 허가거절/인도차단,2018-11-19~2019-04-30의 추가제한 부재를 확정하지 않았다. 미공개 노하우/장비/별도SW와 공개특허의 관할 구별도 이22행 검토로 해결되지 않는다. 기존 C006–C027의 검증 범위·Gate·cutoff·전체감사 미완료 상태를 변경할 제안은 없다. 새 후보문언·분모·결합 사실에는 contradicted를 발견하지 않았다.

## 현재 artifact 해시

| 경로(outputs/final_research/regulatory 기준) | SHA256 |
|---|---|---|
| regulatory_dataset.csv | `4a25775b5ce32914786cdf51d9620a07640d91a286113bf343c2deb1df0064ee` |
| regulatory_evidence_overlay.csv | `8157c829a216057a41f16a1dca50c06ee18338f7201dd7840959749148e51e4d` |
| coverage_summary.json | `d5e6f8f235928e7b98ddb99fae78083d2caf6791dd3b577dc6d0ae7dfe163673` |
| input_comparison.json | `15e82b482ca12aa166ddfb54acc10a2c63df825edf52263ef752444c9773ab4f` |
| remaining_review/remaining_eccn_addendum.csv | `72cf5da2c8af4a03d962b5ed44db529e203169d255664f0a532fefab929439b7` |
| remaining_review/remaining_eccn_addendum.md | `c3899f4cd86524641f7178dee77c732f57324e46efb8e25071a62d01ae66ef7f` |
| remaining_review/review_summary.json | `231498c51307177024a63974462625081d6945350e92a749d4fec77de6a2d5ff` |
| remaining_review/extract_manifest.json | `5099a24469618d3e988912b89734a66e0eca60535f9ce6dad35e5a678a2891eb` |
| integrated/regulatory_dataset.csv | `32473a33630b14419fd6810d276104028825065c794a7ecac1c21e3b0556d221` |
| integrated/coverage_summary.json | `e308c1d25124350827761a915d7550c06e0aa584f4d6dfc25a0670e9d8b747de` |
| integrated/README.md | `e3d3792d630cd22d5be1787868b2f59ba449dd9ecb38370fba47931d636ffc97` |

모든 읽은 규제 artifact·원문·독립계산코드의 해시,22행별 source/locator/판정,HTTP 관측값은 `regulatory_final_nov13.json`에 있다. 재현코드: `regulatory_final_nov13_calc.py`. 생산물·상태·Gate 수정 없음.
