# 미국의 규제 신호와 중국의 선행 정책 — 2회차

기준일·작성일: **2026-10-12**. 이 문서는 2회차의 평가본이다. 법적 날짜가 확인된 사건과 미확인 항목을 구별한 **부분 검증 데이터셋**을 사용한다. 2026년 현행 EAR 전체 또는 중국 지원정책 전체를 복원한 자료가 아니다. 미국 Trump 2기 정책 검증은 요청한 순서대로 5회차에 남겼다.

**결론:** 2018년 11월 ANPRM은 신규 품목허가를 시행한 사건은 맞지 않지만, 모든 기술에 대한 최초 경고도 아니다. 중국에서는 그 이전부터 상당수 분야를 지원하고 있었다. 그러므로 2018년 이후 중국의 특허·투자 증가를 이 ANPRM 하나의 효과로 해석할 수 없다. 이것은 효과가 없다는 결론이 아니라 현재 설계의 식별 근거가 부족하다는 결론이다.

## 1. ANPRM의 법적 성격과 날짜

2018 문서의 ACTION은 “Advance notice of proposed rulemaking (ANPRM)”이며, 절차가 **“is anticipated to result in proposed rules”**라고 설명한다. 즉 향후 구체적인 규칙안을 만들기 위한 의견수렴이었다. 당시 기존 CCL 통제를 변경하려는 문서가 아니며, EAR의 fundamental research 범위를 확대하지 않는다고 명시한다. 다만 이것이 모든 열거 기술에 기존 통제가 전혀 없었다는 뜻은 아니다. [공식 원문, 83 FR 58201–58202](https://www.govinfo.gov/content/pkg/FR-2018-11-19/pdf/2018-25221.pdf)

|항목|확인한 값|
|---|---|
|FR document|2018-25221|
|Docket|180712626–8840–01; Regulations.gov BIS-2018-0024|
|RIN|0694-AH61|
|작성일|2018-11-14|
|Filing|2018-11-16 08:45|
|FR 발행일|2018-11-19|
|의견 마감|원래 2018-12-19 → 2019-01-10|
|신규 중국행 품목허가 효력일|해당 없음: ANPRM 자체로 발생하지 않음|

마감 연장은 2018-12-14의 83 FR 64299, document 2018-27148에서 확인했다. [연장 원문](https://www.govinfo.gov/content/pkg/FR-2018-12-14/pdf/2018-27148.pdf)

일별 시장 반응을 분석한다면 월요일 11/19만 고정해서는 안 된다. 금요일 11/16 filing을 조기 공개의 후보로 남겨야 한다. 본 자료는 filing을 확인했지만 최초 대중 열람·보도 시각까지 입증하지는 않았다. 연도별 연구·투자자료는 이 3일 차이를 구별할 수 없다.

## 2. 원문 분류의 전수 입력과 법적 이력의 부분 검증

`regulatory_dataset.csv`는 **14 family + 47 subcategory/example + 20 ECCN 사건행 = 81행**이다. `node_id`와 `parent_id`, `related_ids`를 사용한다. 한 ECCN 사건이 여러 기술과 연결돼도 독립 정책 충격 여러 건으로 세지 않는다.

|ID|Family|하위 예시 행수|
|---|---|---:|
|F01|Biotechnology|4|
|F02|AI and machine learning|11|
|F03|PNT|0|
|F04|Microprocessor|2|
|F05|Advanced computing|1|
|F06|Data analytics|3|
|F07|Quantum information and sensing|3|
|F08|Logistics|4|
|F09|Additive manufacturing|1|
|F10|Robotics|6|
|F11|Brain-computer interfaces|4|
|F12|Hypersonics|4|
|F13|Advanced Materials|3|
|F14|Advanced surveillance|1|
|합계||47|

F03에는 원문상 별도 하위 예시가 없다. F09의 3D printing은 괄호 속 예시를 별도 행으로 보존했다. 따라서 47은 동등한 법적·경제적 단위 47개가 아니다. Biotechnology의 원문 번호 (iii) 누락, `Robot compliers` 표기, faceprint/voiceprint의 결합 예시도 보존했다. BCI의 유사한 네 표현 역시 독립 기술 군집 네 개라고 볼 수 없다.

정책 강도는 데이터 작성 전에 `regulatory_coding_rules.md`에서 정의했다. 신규허가와 열린 심사가 확인되면 1, 제한적 심사면 2, 거절추정·금지면 3이다. 0은 **해당 사건이 추가한 제한이 없음**이며, 기존 규제가 없다는 뜻이 아니다. 예외·기존 의무·당시 심사정책이 충분히 확인되지 않으면 `미확인`이다. 상위 family의 최초 통제일과 강도를 좁은 ECCN에서 복사하지 않았다.

### 설계에 직접 영향을 주는 확인 결과

|사건|날짜·범위|코딩상의 의미|
|---|---|---|
|지리공간 영상 AI SW, R01|2020-01-06; 0D521 No.1; 네 기술요건을 충족하는 SW; 캐나다 제외 목적지 허가, case-by-case|신규대상 중국행 거래의 강도1. 모든 AI·컴퓨터비전 통제가 아님|
|동 SW 연장·일몰, R02–03|2021 첫 연장, 2022 두 번째 연장; 2023-01-06 만료|영구적인 absorbing treatment로 처리 불가. 다른 통제의 부재까지 확인한 것은 아님|
|2020 WA 이행, R06–09c|2B001 hybrid machine 명확화, EUV SW·wafer 기술 등|이미 통제된 CNC에 적층제조 기능이 붙어도 통제가 유지된다는 명확화를 신규 전체 3D-printing 통제로 해석하면 안 됨|
|핵산 합성 SW, R10|2020-11-06 제안; 2021-10-05 final, 2D352/관련 기술|기존 합성장비 통제와 SW 추가를 구별. AG 다자 합의 이행; 중국의 순증 접근제한일은 추가 검증 필요|
|2022 WA 4개 기술, R11–14|Ga₂O₃·diamond·PGC는 8/15; GAAFET ECAD 3D006은 10/14|발표일과 품목별 효력일을 구분. 소재는 F13 관련이지만 원문 세 하위 예시와 직접 대응하지 않음|
|첨단연산 IC, R15|2022-10-21 해당 품목 조항 시행; SME·미국인 지원은 각각 다른 날|일반 신규대상 중국행 거래에서 강도3. 선행 기업제재·TGL·최종용도는 별도|
|Quantum/metal additive, R16–18|2024-09-06; 4A906 및 지정 SW·기술, 2B910 등|전 세계 허가 원칙이나 국가별 예외·심사 차이. 중국행 지정 신규품목은 거절추정. A:1 quantum 유예를 중국에 적용하지 않음|

근거: [2020 지리공간 규칙](https://www.govinfo.gov/content/pkg/FR-2020-01-06/pdf/2019-27649.pdf), [2022 연장](https://www.govinfo.gov/content/pkg/FR-2022-01-06/html/2021-28444.htm), [BIS의 역사 목록](https://www.bis.gov/about-bis/bis-leadership-and-offices/OTE/emerging-technology-division), [2020 WA 규칙](https://www.govinfo.gov/content/pkg/FR-2020-10-05/html/2020-18334.htm), [2021 생물장비 SW 규칙](https://www.govinfo.gov/content/pkg/FR-2021-10-05/html/2021-21493.htm), [2022 WA 규칙](https://www.govinfo.gov/content/pkg/FR-2022-08-15/html/2022-17125.htm), [2022 첨단연산 규칙](https://www.govinfo.gov/content/pkg/FR-2022-10-13/html/2022-21658.htm), [2024 규칙](https://www.govinfo.gov/content/pkg/FR-2024-09-06/html/2024-19633.htm).

2024 규칙의 D:1/D:5 거절추정과 중국의 국가그룹은 [2024 CFR, 인쇄356쪽](https://www.govinfo.gov/content/pkg/CFR-2024-title15-vol2/pdf/CFR-2024-title15-vol2-part740.pdf)과 대조했다. 실제 중국 수출과 미국 내 외국인에게 기술을 공개하는 deemed export에는 서로 다른 예외가 있을 수 있다. 이를 일률적인 ‘중국 연구자 접근금지’로 읽어서는 안 된다.

### 아직 계산하지 않는 비율

‘14개 중 몇 개가 통제됐다’나 ‘47개 중 대다수는 2026년에도 미통제’라는 비율은 제시하지 않는다. 통제되는 것은 품목·성능·용도·사용자이고, 하나의 넓은 예시 전체가 아니기 때문이다. 경제적 비중의 분모도 확보하지 못했다. **기준일까지 단 한 번도 중국에 추가 제한이 생기지 않았음을 확정한 하위 예시는 현재 0개**이다. 이것은 전부 통제됐다는 뜻이 아니라 그런 부재 검증을 완료한 사례가 없다는 뜻이다.

18개 예시가 아니라 **20개 ECCN 사건행**을 검토했어도 규제 이력이 완전해지지는 않는다. 2018 이전 기준선, 모든 end-user/end-use 통제, 2023 반도체 개정·2024 HBM 등 연관 규칙의 상세 매핑, 모든 다자 합의 품목, 2025–26 현행상태는 잔여 검증이다. 미확인 행을 회귀분석의 untreated=0으로 바꾸지 않는다.

## 3. 미국 신호는 연쇄로 다뤄야 한다

`signal_timeline.csv`에 16개 사건을 기록했다. 핵심 순서는 다음과 같다.

|날짜|사건|11월 ANPRM과의 관계|
|---|---|---|
|2017-11-08|FIRRMA 발의|중요기술 접근·투자 심사 강화 논의 선행|
|2018-02-15|ECRA 법안 발의|통제 법제화 논의 선행|
|2018-04-15 효력|ZTE denial order 활성화|실제 기업제재로 정책 실행 가능성을 보여줌; 기술별 ANPRM과 동일 처치 아님|
|2018-06-26|하원 논의에서 AI·robotics·biotech·advanced materials 지목|적어도4/14 family가 ANPRM 이전에 언급됨|
|2018-07-13 효력|ZTE denial order 종료|6/8 합의 발표와 실제 제한 종료일을 구별해야 함|
|2018-08-13|FIRRMA/ECRA 제정|§1758의 신흥·기반기술 통제 경로 확정|
|2018-11-16 filing / 11-19 발행|Emerging ANPRM|14개 family·세부 예시·공식 의견수렴이라는 추가 구체성|
|2020-08-27|Foundational ANPRM|별도 범주 정의의 후속 신호; 더 깨끗한 최초 신호라고 미리 가정 불가|
|2021-10-26|BCI ANPRM|2018에 이미 지목된 BCI의 재지목·구체화|
|2022-05-23|Section1758 명칭 통합 설명|emerging/foundational 구분을 줄인 것; 당일 전체 실제통제가 생긴 것은 아님|

선행 기술명은 [하원 원문 H5691](https://www.govinfo.gov/content/pkg/CREC-2018-06-26/html/CREC-2018-06-26-pt1-PgH5674-4.htm), ZTE 날짜는 [종료 명령](https://www.govinfo.gov/content/pkg/FR-2018-07-23/html/2018-15633.htm), 명칭 변경은 [2022 proposed rule 설명](https://www.govinfo.gov/content/pkg/FR-2022-05-23/html/2022-10907.htm)에 근거한다. 4/14는 선행 언급을 찾은 하한이며 나머지10개가 새 정보였다는 비율은 아니다.

## 4. 중국 정책과의 중첩

`china_policy_dataset.csv`에 10개 정책·펀드를 기록했다. `china_policy_overlap.csv`에는 미국의 61개 taxonomy 행 각각에 대응 판정·정책 ID·근거 위치·발표 간격을 넣었다. 중국정책 모집단 전체의 무작위 표본은 아니다. **2018 이전의 주요 중앙계획을 우선 선정한 문서집에서 확인되는 중첩**이다.

|정책|문서/공표 시점|확인 범위|
|---|---|---|
|Big Fund1|2014-09 설립 월|재정부 페이지 접속 불가; 색인 본문만 확인. 확정 overlap 계산 제외|
|Made in China2025|2015-05-08 작성, 5/19 공표|NDRC 공식 전재 전문|
|로봇 산업계획|2016-03-21 발행; 4/26 기자회견|MIIT 기자회견 원문; 6개 exotic robotics 하위항목 지원으로 확대하지 않음|
|13차 국가 과학기술혁신계획|2016-07-28 작성, 8/8 공표|NEA 전재 전문·CAC 공표일 대조|
|신세대 AI계획|2017-07-08 작성, 7/20 공표|NEA 전재의 boxed list 포함 확인|
|적층제조 행동계획|2017-11-30 작성, 12/13 공표|MIIT 통지 확인; 첨부 세부계획은 미확인|
|Big Fund2|2019-10-22 설립|SSE 공시 법률의견서의 법인정보 확인; 당시 최초 발표일 별도 미확인|
|14차 5개년계획|2021-03-12 배포, 3/13 MIIT 게시|본문의 뇌과학·양자·AI 등 확인; 이미지/boxed list 세부 BCI 매핑 보류|
|Big Fund3|2024-05-27 은행 공고|공고 페이지 날짜 확인; 총액·납입조건은 금융기관 보도의 정부 전재로2차 확인|
|BCI 산업발전 실시의견|2025-07-23 작성, 7/30 공표|MIIT 공식 원문; 2018 사전중첩 계산에는 제외|

핵심 원문: [2015 제조계획](https://www.ndrc.gov.cn/xxgk/zcfb/qt/201505/t20150520_967388.html), [2016 혁신계획](https://www.nea.gov.cn/2016-08/19/c_135614163.htm), [2017 AI계획](https://www.nea.gov.cn/2017-07/21/c_136462035.htm), [2021 계획](https://wap.miit.gov.cn/xwdt/szyw/art/2021/art_86371f315d484a36811c5c94298912fa.html), [2025 BCI정책](https://www.miit.gov.cn/zwgk/zcwj/wjfb/yj/art/2025/art_ea3ff408de194612891df352d24dd26a.html). 접속 실패와 전재 여부는 `policy_source_log.csv`에 남겼다.

### 사전 중첩의 보수적인 집계

|분류 수준|명시적·기능상 직접 대응|넓은 관련만 확인|선정 문서에서 직접 지목 미발견|분모|
|---|---:|---:|---:|---:|
|Family|11 (78.6%)|2 (14.3%)|1 (7.1%)|14|
|하위 예시|17 (36.2%)|18 (38.3%)|12 (25.5%)|47|

직접 대응은 전체 법적 범위가 같다는 뜻이 아니다. 예를 들어 ‘decision support’와 중국계획의 AI 의사결정 시스템은 기능상 대응으로 포함했지만, IC 지원을 모든 SoC·stacked memory에, 군중지능을 로봇 swarm에 자동 확장하지 않았다. 17개는 문서에 있는 연구·육성 목표이지 실제 집행된 자금·인력의 관측치가 아니다. 함수적 대응도 연구자의 수작업 판정이므로 후속 독립 검토 대상이다.

선정한 대응 정책에서 ANPRM까지의 간격은 직접 대응 하위 예시 기준 **487일10개, 833일6개, 1,280일1개**다. 각각 2017 AI계획, 2016 혁신계획, 2015 제조계획이다. 정책의 최초 등장일을 전수 검색한 결과가 아니라, 검증한 선행 정책과의 간격이다. 따라서 ‘발표가 수일 내 겹친다’는 근거는 아니지만, 장기간 진행되던 중국의 기술별 지원과 성장경로를 반드시 분리해야 한다는 근거다. 같은 기술의 모든 정책 중 미국 발표에 가장 가까운 사건도 아직 전수 계산하지 않았다.

### ‘지원이 없던 기술’ 대신 보존한 미발견 목록

다음12개는 선정 문서에서 직접 대응을 찾지 못한 항목이다. **2018 이전 중국의 전략기술이 아니었다고 확인한 목록이 아니다.**

|ID|항목|
|---|---|
|F02-S02|Evolution/genetic computation|
|F02-S09|Audio/video manipulation, voice cloning/deepfakes|
|F08-S01|Mobile electric power|
|F10-S03–S06|Self-assembling robots; molecular robotics; Robot compliers; Smart Dust|
|F12-S01–S04|극초음속의 비행제어·추진·열보호·특수소재|
|F13-S01|Adaptive camouflage|

특히 극초음속·위장기술은 민간 공개계획에서 안 보인다는 사실 자체가 비교군 적합성을 보장하지 않는다. 군사·기밀·지방정책이 누락돼 있을 수 있다. 따라서 이12개로 ‘사전 정책 없는 표본’을 즉시 만들지 않는다.

펀드도 별도의 주의가 필요하다. Big Fund2의 공시상 등록자본은2,041.5亿元이고 Big Fund3의 보도상 등록자본은3,440亿元이다. 등록자본·출자약정·납입·기업별 실제 투자는 서로 다른 변수다. 총액을 설립연도의 투자 flow로 쓰면 안 된다. [Big Fund2 법률의견서 PDF20쪽](https://static.sse.com.cn/stock/disclosure/announcement/c/202603/688347_20260330_NQAU.pdf), [Big Fund3 보도 전재](https://jrj.wuhan.gov.cn/ztzl_57/xyrd/yxy/202405/t20240529_2408713.shtml)

## 5. 분석용으로 넘길 때의 경계

본 회차는 요청한 최소 완료 기준인 taxonomy 전수행, 확인/미확인 날짜·강도, 신호 연쇄, 중국정책 표와 중첩 집계, Gate 판단까지 완료했다. 그러나 규제 전수조사나 인과분석용 패널 구축을 완료한 것은 아니다. 다음 회차는 `gate_2_3_assessment.md`의 제한을 반영해 설계를 좁혀야 한다.

특히 미확인 법적 날짜는 미래의 검열일도, 미처리 표시도 아니다. 현재 자료로 생성한 ‘clean 기간’ 변수를 회귀에 투입하면 안 된다. 각 기술의 제한 부재를 실제로 검증하기 전까지는 정책 신호·후속규칙·중국 배분 변화의 사건기술과 좁은 사례 비교가 출발점이다.
