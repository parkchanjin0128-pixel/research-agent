# 메모리 2행 규제 범위 독립 검증

- 검증자 `/root/r3_memory_scope_verify` · 2026-11-10 KST. 생산자 `/root`와 별도 배정으로 1차 원문을 대조했다.
- 대상 `.local/nov09-review/outputs/round_03/nov10_memory_cutoff_probe.md`의 대조본 SHA-256 `bb5f8817f1cb4ac31e8cb39fc3b9a5882e3a7453e7faf150b28598a65106b10e`.
- 대조본의 문서 수준 판정은 **verified 5 / contradicted 0**이다. 두 행의 기간 내 실제 기술·거래 적용과 최초 제한일은 각각 **unverifiable**이다. 판정 범위는 아래 다섯 근거와 두 행의 원문 연결로 한정한다.

## 1차 원문 대조

### MEM-01 · verified · 2018-10-30 Jinhua 지정

83 FR 54519의 DATES와 54521의 중국 항목은 2018-10-30 효력을 확인한다. 54520의 ERC 결정 및 지정 문구는 Fujian Jinhua Integrated Circuit Company, Ltd. 한 법인과 별칭 JHICC, 푸젠성 진장시 주소를 특정한다. 이 법인에 대한 EAR 적용 품목의 수출·재수출·국내이전에는 품목 분류와 별도로 허가가 필요했다. 허가 심사는 거부 추정이고 허가 예외는 적용되지 않았다. 규칙 말미와 공식 공개 열람본은 10월 29일 오전 8시 45분 접수와 10월 30일 관보 게재를 구분한다. [83 FR 54519–54521, DATES·ERC 결정·지정 표](https://www.govinfo.gov/content/pkg/FR-2018-10-30/html/2018-23693.htm) · [관보 공개 열람본](https://public-inspection.federalregister.gov/2018-23693.pdf?1540817129=)

2019-01-01판 §744.11(a)와 해당 등재 항목은 지정 법인에 대한 거래를 기준으로 읽힌다. BIS는 2020년 최종 규칙에서 구매자·중간 수하인·최종 수하인·최종사용자 네 역할을 명문화하고, 기존에도 모든 거래당사자 역할을 포괄하려는 의도였다고 설명했다. 진화 지정문은 법인이 관여하는 거래의 사전 검토 취지를 설명하지만 네 역할을 개별 열거하지 않는다. 거래에서 진화가 수하인 또는 최종사용자인 경우를 직접 지정과 연결할 수 있다. 구매자·중간 수하인만으로 관여한 거래는 당시 거래 기록과 적용 근거를 별도로 대조해야 한다. 계열사나 공급망의 경제적 노출도 해당 법인이 거래에 관여했는지와 구분한다. [2019 CFR Part 744, §744.11(a)·Supplement No. 4 중국 표](https://www.govinfo.gov/content/pkg/CFR-2019-title15-vol2/pdf/CFR-2019-title15-vol2-part744.pdf) · [85 FR 51335–51337, Background·Changes Made to the EAR](https://www.govinfo.gov/content/pkg/FR-2020-08-20/html/2020-17908.htm)

경과조치는 지정으로 종전 허가 예외나 무허가 수출·재수출(NLR) 자격을 잃는 물량 가운데 10월 30일 실제 외국행 수출·재수출 주문에 따라 운송수단에 실려 수출·재수출 항구로 가던 선적물에 종전 자격으로 진행할 수 있게 했다. 조항이 열거하는 행위는 수출·재수출이다. 개별 물량의 경과조치 자격은 실제 주문과 운송 증거가 있어야 판정할 수 있다. [83 FR 54520, Savings Clause](https://www.govinfo.gov/content/pkg/FR-2018-10-30/html/2018-23693.htm)

### MEM-02 · verified · 2019-01-01판 CCL

- 3A001.a Note 2는 다중칩 IC와 3차원 IC를 IC 유형에 포함한다. .a.1은 방사선 내성 기준, .a.2는 열거된 IC 종류와 정격 온도 기준, .a.3은 열거된 프로세서·마이크로컨트롤러의 화합물 반도체 제조 및 40 MHz 초과 동작 요건을 둔다. .a.2가 열거하는 저장 IC도 화합물 반도체로 제조된 유형이다. [2019 CFR Part 774, 인쇄면 911](https://www.govinfo.gov/content/pkg/CFR-2019-title15-vol2/pdf/CFR-2019-title15-vol2-part774.pdf#page=121)
- 3A991은 3A001에서 통제하지 않는 전자장치·부품을 다룬다. .a는 특정 마이크로프로세서·마이크로컴퓨터·마이크로컨트롤러 회로의 성능·클록·연결 사양을 열거한다. .b가 열거하는 저장 IC는 정해진 용량 또는 용량과 접근시간 조건을 충족하는 EEPROM(플래시 포함)과 SRAM이다. [2019 CFR Part 774, 인쇄면 928](https://www.govinfo.gov/content/pkg/CFR-2019-title15-vol2/pdf/CFR-2019-title15-vol2-part774.pdf#page=138)
- 3B001은 열거된 반도체 소자·재료 제조장비와 특별히 설계된 부품·부속품을 다룬다. 3E001은 General Technology Note에 따른 대상 장비·재료의 개발·생산 기술을 다루며, 표제의 3A991 등 제외 항목과 Notes 1–3의 범위 제한이 있다. 같은 기술명 아래에서도 제품, 장비, 개발·생산 기술의 분류와 목적지 요건은 각각 판정해야 한다. 위 원문은 감사창 중 한 시점의 판본이다. [2019 CFR Part 774, 인쇄면 930–931 및 940–941](https://www.govinfo.gov/content/pkg/CFR-2019-title15-vol2/pdf/CFR-2019-title15-vol2-part774.pdf#page=140)

### MEM-03 · verified · 2018-11-01 DOJ 발표 중첩

DOJ는 9월 27일 제출된 진화·UMC 등 관련 기소장의 11월 1일 공개와 같은 날의 민사소송 제기를 발표했다. 보도자료는 DRAM 관련 영업비밀 혐의를 기술한다. 법무장관의 11월 1일 연설은 사건 공개와 China Initiative 신설을 같은 자리에서 발표했다. 따라서 11월 1일 일별 시장 반응은 이 발표들이 겹친 날의 반응으로 해석할 수 있으며, 각 발표의 별도 효과는 이 날짜만으로 식별되지 않는다. 공개 혐의의 DRAM을 두 ANPRM 기술 중 어느 하나에 연결할 사양은 확인되지 않았다. [DOJ 당일 보도자료](https://www.justice.gov/archives/opa/pr/prc-state-owned-company-taiwan-company-and-three-individuals-charged-economic-espionage) · [Sessions 당일 연설](https://www.justice.gov/archives/opa/speech/attorney-general-jeff-sessions-announces-new-initiative-combat-chinese-economic-espionage)

### MEM-04 · verified · 2023년 3A090 개정

2023-10-25 게재된 IFR의 개정 지시 38은 2023-11-17 효력으로 3A090을 개정했다. Note 1은 인메모리 프로세서를 대상이 될 수 있는 IC 예에 넣었다. .a와 .b의 디지털 처리 장치·총처리성능(TPP)·성능밀도 요건이 적용되며 Note 2는 데이터센터용으로 설계되거나 판매되지 않으면서 TPP가 4800 미만인 IC를 제외했다. 3A090 품목의 RS 허가 범위는 §742.6(a)(6)의 목적지 요건 및 적용 가능한 예외와 함께 읽어야 한다. 2022년 BIS 규칙이 이미 3A090을 신설했으므로 확인한 2023년 날짜는 해당 개정의 효력일이다. F05-S01 연결은 사양을 확인할 수 있는 일부 인메모리 프로세서의 후속 후보로 둔다. [88 FR 73458–73517, 지시 38·3A090 Notes 1–2·§742.6](https://www.govinfo.gov/content/pkg/FR-2023-10-25/html/2023-23055.htm) · [87 FR 62186–62215, 기존 3A090 신설](https://www.govinfo.gov/content/pkg/FR-2022-10-13/html/2022-21658.htm)

### MEM-05 · verified · 2024년 HBM 규칙

89 FR 96790의 DATES에 따르면 IFR의 효력일은 2024-12-02이고 관보 게재일은 12-05다. 3A090.c를 추가한 지시 31(a)와 DATES에서 함께 지정한 관련 지시의 준수일은 12-31이다. §III.C.1은 HBM 신설의 설명이고 §III.C.2는 관련 조항 정비를 설명한다. §V는 이 지시들로 종전 허가 예외 또는 NLR 자격을 잃는 적격 물량 중 실제 주문에 따라 2025-01-06에 운송 중인 선적이 2025-02-03까지 완료되면 종전 자격으로 진행할 수 있도록 했다. [89 FR 96790–96830, DATES·§III.C.1–2·§V·지시 31(a)](https://www.govinfo.gov/content/pkg/FR-2024-12-05/html/2024-28270.htm)

3A090.c의 문턱은 메모리 대역폭 밀도 2 GB/s/mm² **초과**다. 스택 또는 패키지의 대역폭을 면적으로 나누며, 스택이 패키지에 들어 있으면 패키지 기준을 사용한다. JEDEC 준수 여부와 무관하게 문턱을 넘는 DRAM IC가 포함된다. 연산이 주 기능인 HBM·로직 공패키지 IC는 .c 범위에서 제외되고, 물리계층 기능이 있는 제어 인터페이스용 로직 IC에 영구 부착된 HBM은 포함된다. §742.6(a)(6)(i)(B)는 마카오 및 중국을 포함하는 Country Group D:5 역내·향 3A090.c 품목과 연계 3D001·3E001의 RS 허가 요건을 둔다. §740.25의 HBM 예외는 별도 거래 요건을 충족해야 한다. F04-S02에는 이 사양에 해당하는 일부 HBM의 후속 연결로 기록한다. [89 FR 96790–96830, 3A090.c 기술 주석·§742.6(a)(6)(i)(B)·§740.25](https://www.govinfo.gov/content/pkg/FR-2024-12-05/html/2024-28270.htm)

## 행별 적용 판정

83 FR 58201–58202는 2018-11-19 게재한 의견수렴 공고다. F04-S02는 원문의 대표 범주 (4)(ii), F05-S01은 (5)(i)에 각각 대응한다. 공고는 해당 범주의 신규 ECCN이나 허가 의무를 도입하지 않았다. [83 FR 58201–58202, ACTION·SUMMARY·Representative Technology Categories](https://www.govinfo.gov/content/pkg/FR-2018-11-19/html/2018-25221.htm)

| 행 | 확인한 범위 | 2018-11-19~2019-04-30 기술·거래 적용 및 청정월 | 실제 최초 제한일 |
|---|---|---|---|
| F04-S02 Stacked Memory on Chip | ANPRM (4)(ii). 2019판에 다중칩·3차원 IC 관련 분류 후보가 있으며 2024년 일부 HBM 사양과 후속 연결 가능 | 미확인 · 검증된 청정 완전월 0/5 | 미확인 |
| F05-S01 Memory-centric logic | ANPRM (5)(i). 2019판에 프로세서·IC 관련 분류 후보가 있으며 2023년 일부 인메모리 프로세서와 후속 연결 가능 | 미확인 · 검증된 청정 완전월 0/5 | 미확인 |

완전월은 2018-12 및 2019-01~04다. 10개 행·월 조합은 모두 미확인이다. 확인 건수 0은 월별 무통제의 증거로 사용하지 않는다. Jinhua 지정은 창 이전의 법인 단위 의무이며, 두 기술에 대한 최초 제한일이나 당시 실제 거래가 처음 제약된 날을 부여할 근거는 아직 없다. 실제 품목·장비·기술 사양과 거래 당사자·역할, 최종용도·목적지, EAR 적용성, 허가·예외 및 주문·운송 시점을 이어 확인해야 한다.
