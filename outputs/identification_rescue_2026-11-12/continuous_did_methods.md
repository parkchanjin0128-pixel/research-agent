# 연속노출·DDD 식별 복구를 위한 최근 방법 검토

작성·웹 원문 확인일: 2026-11-12. 이 문서는 기존 연구원장·주분석·코드를 변경하지 않는 별도 검토다. 검토한 입력은 `outputs/presentation_2026-11-13/report_draft.md`와 그 하위 `data/patstat_pilot_final.json`이다. 아래 문헌과 저자·공식 패키지 문서의 존재와 관련 부분을 확인했으나 실제 정책효과를 새로 추정하거나 저자 코드를 재현하지 않았다. **방법론 원문 확인은 효과의 실증 검증이 아니다.**

## 먼저 정해야 하는 추정대상

질문은 “2018년 미국 공식 신호 이후, 실제 추가 접근제한 이전, 사전 미국연결 B가 높은 중국 기술의 상대 연구·자본 배분이 달라졌는가”이다. 여기서 B는 과거 지식·거래 연결의 대리변수다. B 자체를 정책당국이 지급한 처치량으로 간주하거나, B가 높은 기술과 낮은 기술의 비교를 동일 기술의 B를 올린 인과효과로 바꾸면 안 된다. 동일한 공식 신호의 효과 이질성과 조작 가능한 연속처치의 causal response는 별개다. CGBS는 dose별 ATT 사이 비교에 선택항이 남는다고 보이며, 최신 DDD 논문도 subgroup 이질성 질문은 자신의 이중 자격기준 처치 설계와 다른 가정·모수라고 명시한다. [CGBS 최신판 §3.2·5](https://arxiv.org/html/2107.02637v8), [Ortiz-Villavicencio–Sant’Anna p.4](https://marcelortiz.com/assets/pdf/DDD_OVS.pdf)

현재 주장 가능한 1차 후보는 고정한 공통 모집단·동일 B 분포 Q에서 계산하는 **신호 이후 상대 기울기 변화**다. 이는 선형 투영 대조이며, 별도 가정 없이 중국 전체 수준효과, B의 인과미분, 실제 제한의 증분효과가 아니다. 신호가 비교국·비지목 기술에도 영향을 주면 그 반응도 들어간다. 후속 방법을 비교할 때 대상 모집단·결과 단위·창·Q를 같게 유지해야 방법 간 차이를 해석할 수 있다.

## 방법 × 추정대상 × 가정 × 자료 × 한계 × 실행경로

아래 표의 ‘가정’은 주요 조건만 적은 것으로 정리·추론의 전체 정규조건을 대신하지 않는다. 각 방법을 원래 질문에 적용할 수 있다는 판정과 방법의 존재를 구별했다.

| 방법·직접 확인 원문 | 추정대상 | 핵심 가정 | 추가 필요자료 | 해결하지 못하는 것 | 이 연구의 실행경로·우선순위 |
|---|---|---|---|---|---|
| 1. Callaway–Goodman-Bacon–Sant’Anna(CGBS), NBER 32117(2024), arXiv v8(2025-12-31), [원문](https://arxiv.org/html/2107.02637v8) | dose별 ATT(d\|d); stronger PT 아래 causal response/그 집계 | 무처치 결과의 dose별 PT, no anticipation, 유효 비교군·지원; dose 간 causal response에는 더 강한 조건 | 안정 단위별 사전 고정 dose·채택시점·전후 outcome·비처치 관측 | B 선택, 중국 기술정책, B 측정오차·공유파급, 청정창 부재 | 실제 신호강도 D와 B의 역할을 먼저 분리. B를 effect modifier로 유지하면 원문 estimator를 그대로 주분석으로 이식하지 않음. contdid 0.1.2 공식 배포 확인; covariate 요구사항까지 검증 후 사용 |
| 2. CGBS, Event Studies with a Continuous Treatment, AEA P&P114:601–605(2024), [출판 원문·서지](https://www.aeaweb.org/articles?id=10.1257/pandp.20241047) | ATT(g,t,d)의 dose·상대시간 집계; 시점별/부분 dose별 동학 | 구성과 dose 가중을 명시한 PT·no anticipation; 효과를 비교할 지지 유지 | 각 cohort×event-time×dose 지원, 고정 dose 분포·공통 셀 | 사건시간별 표본·dose 구성이 달라지는 현상, 짧은 신호창의 행동시차 | 사전 고정 Q와 동일 기술 집합으로 월별 상대대조를 만들 때 집계 원칙으로 사용. 표본 바뀐 동학을 반응 변화로 해석하지 않음 |
| 3. de Chaisemartin–D’Haultfœuille–Pasquier–Sow–Vazquez-Bare, arXiv2201.06898 v7(2026-07-22), [고정 PDF](https://arxiv.org/pdf/2201.06898v7) | switchers의 AS·WAS: 실제 D1→D2 구간의 potential-outcome slope 평균 | 동일 baseline D에서 switcher–stayer PT; no anticipation; 기본형 no dynamic effects; stayer의 조건부 지원 | 매 기간 실제 연속 D, 변화·불변 단위, 동일 baseline 근방 지원과 outcome; IV는 유효 도구·first stage 추가 | stayer가 없는 경우, B가 고정인 설계, R&D 시차를 무시한 static 명세, 도구의 외생성 부재 | 실제 제한강도 경로가 관측되는 시행 후 별도 질문에 검토. 현재 고정 B×signal을 이 방법 때문에 가변처치로 재정의하지 않음. 저자 did_multiplegt_stat 연결을 사용하고 버전 고정 |
| 4. de Chaisemartin–D’Haultfœuille–Vazquez-Bare, No Stayers, AEA P&P114:610–613(2024), [4쪽 원문](https://gvazquezbare.github.io/papers/Chaisemartin-DHaultfoeuille-VazquezBare_2024_AEAPP.pdf) | 실제 변화량 절댓값으로 가중한 switcher slope(WAOSS) | baseline 조건부 PT·static model·Lipschitz; ΔD가 0에 임의로 가까워지는 quasi-stayers | D1,D2,ΔD가 매우 작은 관측의 충분한 밀도·outcome | “모두 변했다”만으로 식별 불가; near-zero 변화 지원이 없으면 비모수 대조 없음; 느린 수렴 | 인위적 반올림으로 stayers를 만들지 않음. 시간가변 처치가 실제로 정의될 때만 후보; 현재 사전 B만으로 실행 대상 아님 |
| 5. de Chaisemartin–Ciccia–D’Haultfœuille–Knau, No Unit Remains Untreated, arXiv2405.04465 v8(2026-10-12), [최신 원문 §3–4](https://arxiv.org/html/2405.04465v8) | 전원 0→양의 dose 채택 시, quasi-untreated 비교가 식별하는 unit-dose당 가중평균 효과 | 공통 채택 HAD, PT, true dose가 0 근처까지 지원·경계 regularity; 없으면 추가 모형 | 실제 양의 dose 분포·경계 근방 표본, 전후 outcome·사전월 | 가장 낮은 B가 곧 무신호인 것은 아님; 양의 하한의 dose를 0까지 외삽할 수 없음 | near-zero B를 ‘quasi-untreated’로 명명하기 전에 B=0이 무신호를 뜻하는지 검증. 통과 못하면 비모수 신호 수준효과의 구제책으로 배제; did_had 경로 확인 |
| 6. de Chaisemartin–D’Haultfœuille, Intertemporal Treatment Effects, arXiv2007.04267 v14(2026-05-12), [원문 §2–3](https://arxiv.org/html/2007.04267v14), [저자 패키지](https://github.com/Credible-Answers/did_multiplegt_dyn) | 최초 변화 후 실제 처치경로 대 baseline 유지경로의 누적 차이; normalized 효과는 현·과거 dose의 가중반응 | baseline 조건부 PT·no anticipation·not-yet-switchers; 설계·no-crossing 조건; 연속 baseline 확장에는 함수 가정 | 반복 증가·감소를 포함한 실제 처치 이력, 비교 switcher 지원, 여러 사전·사후월 | 신호와 구속을 한 scalar로 합치면 두 효과 분리 불가; 잘못된 사건달력·중국만의 동시충격 | 신호에서 시작되는 반응을 구속의 pretrend로 제거하면 질문이 사라짐. 신호·제한 경로를 분리한 별도 동학 확장용; 현재 cleanwindow를 대신하지 않음 |
| 7. Borusyak–Jaravel–Spiess, REStud91(6):3253–3285(2024), [출판 원문](https://doi.org/10.1093/restud/rdae007), [저자 공개 PDF](https://www.restud.com/wp-content/uploads/2024/01/main.pdf) | 사전 명시한 heterogeneous unit-time 효과의 가중평균; untreated-only fitting에 의한 imputation | 유효 무처치 셀에서 반사실 선형모형 식별, no anticipation, 적절한 오차·집계 추론 | untreated 학습 셀, outcome panel, 사전 지정 효과 가중 | 처치 후 FE로의 오염은 줄여도 무처치모형 오지정·파급·dose 선택 해결 불가 | 유효 무반응 donor가 생기면 동일 target 모집단의 보조 추정. did_imputation과 별도 사전추세 검사 사용; 비이진·DDD는 원문 허용형식 확인 후 적용 |
| 8. Wing–Freedman–Hollingsworth, Stacked DiD, NBER32054(2024), [원문](https://www.nber.org/system/files/working_papers/w32054/w32054.pdf), [저자 예제](https://github.com/hollina/stacked-did-weights) | 고정 event-window 구성의 trimmed aggregate ATT | 각 stack의 clean controls·PT·no anticipation; 교정 가중으로 처리·비교 추세 가중 일치 | 여러 실제 adoption cohort, 전체 창이 가능한 cohort와 never/not-yet controls | 단순 stacking은 가중편향; 공통 2018 신호 하나에 가상 cohort를 만들 수 없음; trimming 선택 | 실제 다른 신호 날짜가 입증될 때만 cohort 구성. 공통 날짜이면 추정량 교체 이익 제한. 교정 가중·원단위 중복의 cluster 반영; 미확인 거래 제거로 창을 만들지 않음 |
| 9. Ortiz-Villavicencio–Sant’Anna, Better Understanding DDD, arXiv2505.09942 v3(2025-07-18), [60쪽 원문](https://marcelortiz.com/assets/pdf/DDD_OVS.pdf), [공식 triplediff](https://marcelortiz.com/triplediff/) | enabling group×binary eligibility로 정의되는 ATT(g,t); RA/IPW/DR 조건부 DDD | covariate-adjusted DDD PT, overlap·no anticipation·유효 4셀; 각 comparison cohort 처리 필요 | country×technology×month outcome, enabling·binary eligibility, 사전 X·B, 4셀 조건부 지원 | FE 추가나 두 개의 조정 DiD 차이만으로 조건부 DDD가 되지 않음; fixed B 기울기 자체 대상 아님; 공동파급·후정책 교란 | **우선후보 2**: 사전 B층별 binary signal DDD를 별도 estimand로 추정. 중국과 지목기술을 두 자격조건으로 삼을 이론과 비교셀 무반응을 먼저 감사. 임의 B 이분화로 원래 기울기를 대체하지 않음 |
| 10. Rambachan–Roth, REStud90(5):2555–2591(2023), [출판 PDF](https://jonathandroth.github.io/assets/files/HonestParallelTrends_Main.pdf), [저자 HonestDiD](https://github.com/asheshrambachan/HonestDiD) | bias 제한 아래 사전 지정 post 효과 선형집계의 부분식별·강건 신뢰집합 | 추정 event vector·공분산의 유효성; β=τ+δ, 사전 τ=0; 상대크기 또는 곡률 제한에 실질 근거 | 같은 고정연산자의 pre/post 계수·전체 공분산, 허용 편향 M 또는 Mbar·target l | 사후에만 튀는 중국 기술정책·동시제한이 제한밖이면 보호 안 됨; 식별되지 않은 estimator를 식별로 바꾸지 않음 | **우선후보 1**: 고정 Q 상대기울기 월별 vector에 적용 가능성부터 도출. 상대기울기 대조에 대한 위 분해·추론이 유효해야 하며 black-box DDD 허용 선언 아님. 비유의 pretrend로 통과시키지 않고 breakdown/판별불가 보고 |
| 11. Arkhangelsky–Athey–Hirshberg–Imbens–Wager, AER111(12):4088–4118(2021), [공식 출판](https://www.aeaweb.org/articles?id=10.1257/aer.20190159), [저자 패키지](https://synth-inference.github.io/synthdid/) | binary block treatment의 ATT; 단위·시점 가중으로 반사실 구성 | 잠재 factor 구조·가중 근사오차 제어, 무오염 donor, no anticipation, 충분한 panel | 긴 사전 outcome·비교단위, block assignment·고정 타깃 | China-specific 새 기술정책이 treatment와 동시이면 분리 못함; 사전 fit 좋음이 인과증명 아님; continuous B slope가 기본 estimand 아님 | 월별 panel 확보 뒤 held-out premonth 예측 비교용. B층별 ATT를 새 estimand로 명시할 수 있으나 원 질문의 slope와 같다고 하지 않음. 공식 synthdid block 제약 확인 |
| 12. Xu, GSC, Political Analysis25(1):57–76(2017), [출판 원문](https://doi.org/10.1017/pan.2016.2); Athey et al., MC, JASA116(536):1716–1730(2021), [원문 v5](https://arxiv.org/html/1710.10251); [공식 최신 fect](https://yiqingxu.org/packages/fect/) | GSC의 treated counterfactual/ATT; MC는 무처치 outcome matrix 저랭크 복원 후 ATT | 안정적 latent factors/loadings, donor 정보와 rank/regularization 지원, idiosyncratic treatment-selection 제어·무파급 | 충분한 사전·대조 panel, missing/treatment mask, 사전 전용 rank/penalty 선택 | 관측 불가 월을 연구결정월로 만들 수 없음; 식별되지 않는 China×target post shock은 예측 residual에 혼입; MC는 causal missingness 가정이 필요 | 구조가 다른 반사실 보조군. rolling/blocked held-out 사전검증·weight/loadings 진단을 먼저 하고 고정 타깃으로 비교. 낮은 사전오차만으로 채택하지 않음 |

## 당장 실행할 최우선 두 경로와 중단 조건

### 1순위: 고정 Q·고정 모집단의 월별 상대대조와 HonestDiD 민감도

이 경로가 가장 원 질문을 덜 바꾼다. 실무 순서는 (1) 결과를 보지 않고 법적 완전월 마스크·단위·B 정의·Q를 고정, (2) 매월 동일한 대조 d_t와 기준월 대비 event vector 및 전체 공분산을 산출, (3) 사전기간을 학습/검증으로 나눠 같은 연산자의 가짜 창·비선형 사전추세를 확인, (4) 효과단위에서 변환한 smoothness 및 relative-magnitude 허용편향 아래 post 평균의 robust CI와 breakdown 값을 보고하는 것이다. Mbar=0.5,1,2 등은 설명용 격자로만 제시할 수 있고 연구의 사실로 가정하지 않는다. 정치·산업정책 달력과 경제적으로 방어할 편향 범위를 연결해야 한다. HonestDiD 입력으로 넘기는 계수순서·기준월·시간간격을 고정하고 불규칙 간격을 동일 월로 취급하지 않는다. [Rambachan–Roth §2–3](https://jonathandroth.github.io/assets/files/HonestParallelTrends_Main.pdf)

중단·보류: 실제 공통 청정월 미확정 또는 확인된 공집합; 월별 결정시계 outcome 부재; 당시 정보 B 구성 불가; 두 팔의 공통 지지·잔차 B 분산/rank 부재; 독립 묶음 수·공분산 추론 불충분이면 추정 전 중단한다. 법적 날짜가 신호 자체보다 빠르거나 더 이른 관련 정보가 있으면 no-anticipation 기준을 재감사한다. 사전 확정 SESOI보다 MDE가 크면 작은 효과의 유무 판단을 보류한다. 방어 가능한 편향 범위에서 CI가 0과 양·음의 실질효과를 모두 포함하면 ‘판별불가’를 결과로 보고한다. 유의하도록 창·Mbar·dose·분류·국가를 재선택하지 않는다.

### 2순위: 사전 B별 이질성을 갖는 조건부 DRDDD

중국 여부와 기술지목이라는 두 이진 조건이 실제 처치구조를 나타내고 4셀의 비교 해석이 가능하다면, 사전 X와 B를 conditioning set에 넣어 binary signal ATT(g,t)를 추정하고 사전 정한 B 구간별 ATT를 보고한다. 구간을 나누면 연속 기울기와 다른 estimand이므로 구간 선택을 결과 이전에 고정하고 전체 함수를 반올림한 것처럼 말하지 않는다. 각 성향·회귀 모형의 지원을 확인하며, 통계적 double robustness는 식별가정의 이중 보장을 뜻하지 않는다. 결과 기반으로 균형 좋은 사양을 고르는 대신 추론까지 포함한 사전 규칙으로 nuisance fitting과 집계를 고정한다. [DDD 원문 §3–4](https://marcelortiz.com/assets/pdf/DDD_OVS.pdf)

중단·보류: B×X층의 네 셀 지원이 없거나 거의 0인 성향으로 가중 집중이 크면 외삽하지 않는다. 비교국/비지목도 신호에 반응하여 네 셀을 모두 untreated로 간주할 수 없다면 기본 ATT 해석을 중단한다. 이때 관측 DDD를 상대 노출대조로 기술할 수는 있지만, 원문 DRDDD 패키지가 총 신호효과를 회복했다고 하지 않는다. 신호와 완전히 겹치는 중국 고유 정책이 별도 비교·자료·변동으로 분리되지 않으면 미국 신호 단독 귀속을 중단한다. 사후 정책을 모두 통제해 신호의 매개경로를 제거하는 방법도 채택하지 않는다.

## 적용을 미루는 이유와 최신판 점검

- **반복처치**: 실제 신호 이력과 구속 이력이 여러 번 바뀌면 intertemporal 효과가 맞는 질문일 수 있다. 그러나 신호→제한이라는 서로 다른 처치를 하나의 숫자 0,1,2로 코딩하면 ‘한 단위 증분’이 동일 개입을 뜻하지 않는다. 동학 방법은 이 정의 문제를 해결하지 않는다.
- **준무처치**: low B≠low actual signal dose다. B가 모두 양수라는 이유만으로 2026 no-untreated 논문을 적용할 수 없다. 이 원문은 참 처치량이 0으로 접근하는 support를 요구한다.
- **합성 비교·matrix completion**: 전통 PT 대신 factor/예측 구조를 사용한다. 중국만의 동시 기술충격을 자동 제거하는 방법이 아니다. 원래 추정대상과 다른 ATT를 산출했다면 일치하는 부호를 독립적 확인이라고 합산하지 않는다.
- **최근 2026 추가 후보**: [Covariate-Balanced Weighted Stacked DiD, arXiv2604.02293](https://arxiv.org/abs/2604.02293)와 [Stacked Triple Differences, arXiv2604.22982](https://arxiv.org/abs/2604.22982)는 원문 초록을 확인한 추가 탐색항목이다. 이번 검토에서 정리·코드까지 확인하지 않았으므로 실행 우선후보에 넣지 않는다. 최근성 자체를 검증으로 간주하지 않는다.

공식 CRAN의 contdid는 0.1.2, 공개일 2026-10-30이다. 오래된 저자 홈페이지의 alpha 설명과 GitHub DESCRIPTION의 0.1.1, 최신 r-universe 설명의 기본값·기능이 일치하지 않으므로 설치본 버전·함수 서명·기본값을 직접 저장하고 재현파일에 고정해야 한다. 현재 CRAN reference manual 직접 열람은 시간초과여서 공변량 지원 여부를 최신 배포에서 확인했다고 주장하지 않는다. [CRAN](https://cran.r-project.org/web/packages/contdid/index.html), [저자 GitHub DESCRIPTION](https://github.com/bcallaway11/contdid/blob/main/DESCRIPTION)

Stayers 논문도 2024 4저자판을 최신판으로 인용하면 안 된다. 최신 arXiv 메타데이터는 5저자, v7·2026-07-22, 제목은 *Treatments Continuously Distributed at Every Period*다. v7 고정 PDF 표지는 *Continuous Treatments and Instruments with Stayers*, 날짜 2026-07-23이다. 비고정 HTML에는 2026-08-24가 표시되어 불일치가 있으므로 본 표는 v7 고정 PDF를 기준으로 삼는다. Stacked DiD는 SSRN에서 2026-08-02 수정표시를 확인했지만 최신 수정 PDF까지 직접 비교하지 못했다. NBER2024 원문과 저자 repo 확인 범위로 제한한다. [Stayers 메타데이터](https://arxiv.org/abs/2201.06898), [고정 PDF](https://arxiv.org/pdf/2201.06898v7), [Stacked 저자 게시](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4702247)

## 이 검토가 실제로 검증한 것

확인한 것은 방법·버전·식별조건과 원 질문의 부합 여부다. 실제 PATSTAT 파일럿은 5개 넓은 IPC의 출처·국가귀속 측정 감사이며, 국가×기술×월의 배분 outcome도 정책처치 이력도 아니다. 따라서 이 자료에 12개 방법을 기계적으로 실행하여 가설을 검증할 수 없다. 지금 가능한 결론은 **직접 실행 전 자료·지원·시간 및 추정대상의 게이트가 필요하며, 그 게이트를 통과하면 상대 대조+강건 민감도와 조건부 DRDDD를 먼저 시행한다**는 것이다. 효과의 존재·부호·유의성은 여전히 미검증이다.

원문 열람 위치·서지·버전·미확인 범위는 `sources_did.json`에 기록했다. 초록·관련 절을 직접 확인한 것과 증명·코드 전체 검증은 구별했으며, 후자는 이번 작업에서 하지 않았다.

### 병행 중인 WO 월별 패널과 이 문서의 경계

상위 작업에서 2013–2019년 WO 국제출원에 한정한 CN/US/JP/KR/DE×5 IPC 월별 건수 패널을 실제 집계 중이라는 진행상황을 전달받았다. 이 문서는 그 패널을 열람·분석하지 않았으며 추정결과를 포함하지 않는다. WO 한정이 결과를 보기 전 기록된 프로토콜이라면 주소결측으로 인한 측정위험을 줄일 수 있지만, 추론 모집단은 WO 신청인 주소로 귀속한 출원행동이다. 중국 전체 R&D·자본배분이나 국내 특허 전체의 결과로 바꿀 수 없다.

이 패널은 실제 시계열에 대한 dose 사전추세·국가대조 민감도의 탐색 진단에 활용할 수 있다. 다만 고정 B가 넓은 IPC5개에만 존재하면 국가·월 관측이 늘어도 독립적인 기술 dose지지가 5개보다 많아지는 것은 아니다. 기술 간 분류 중첩·공유인용으로 독립성은 더 약할 수 있다. 한 기술 제외 영향·함수형태·잔차 B rank를 먼저 확인하고, 소수 기술군에서 통상 cluster CI나 bootstrap을 충분히 정당화된 인과추론처럼 제시하지 않는다. 국가 교체 진단의 안정성은 공유 파급 배제의 증명이 아니며, 임의 placebo·permutation은 처치배정기제가 정당화되지 않으면 randomization inference가 아니다.
