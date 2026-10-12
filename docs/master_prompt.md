# 연구 주제 구체화 요청: 미국의 대중 첨단기술 수출통제 "신호"와 중국의 선제적 연구·자본 배분

나는 한 학기 동안 수행할 연구 주제를 구체화하고 있다. 주제는 **미국의 대중 첨단기술 수출통제와 중국의 기술개발·혁신 반응**이다.

"수출통제가 중국의 혁신을 촉진했는가/억제했는가"를 묻는 연구는 이미 상당히 존재한다. 따라서 기존 연구와 겹치지 않는 **gray area**를 찾고, 실제로 식별 가능한 연구질문과 연구계획을 만들어라.

이번 작업의 핵심 관심은 **실제 수출통제 시행(actual implementation)이 아니라 announcement / anticipatory effect**이다.

이 작업의 기본 태도는 **내 아이디어를 살리는 것이 아니라 먼저 깨 보는 것**이다. novelty, announcement의 정보충격 타당성, 식별 가능성을 순서대로 검증하고, 살아남은 설계만 발전시켜라.

---

# 0. 작업 조건과 검증 프로토콜 (모든 섹션에 우선 적용)

## 0-1. 기준일
- 기준일은 **2026-10-12**이다.
- 모든 정책 항목에는 **as-of 날짜**를 붙여라.
- Trump 2기 정책은 번복이 잦으므로 최신 상태를 반드시 검색으로 확인하라.

## 0-2. 확인 수준 표시
모든 문헌·정책·데이터 항목에 **확인 수준**을 표시하라.
- 문헌: `전문 확인 / WP PDF 확인 / abstract만 / 2차 자료 / 추정`
- 데이터 소스: `공식 페이지 직접 확인 / 공식 문서·매뉴얼 / 2차 자료 / 추정`
- 정책: `Federal Register·BIS 원문 / 기타 1차 자료 / 2차 자료`

## 0-3. 날조 금지와 미확인 처리
- DOI, Federal Register document number(및 FR citation), docket number, RIN, URL, 데이터베이스 table/field 이름을 **확인하지 못했으면 빈칸이나 "미확인"으로 두어라. 추정해서 채우지 마라.**
- 접속할 수 없는 사이트(중국 사이트 포함)는 **"접속 불가"**로 표시하고, 접속한 것처럼 메뉴 경로를 서술하지 마라.
- 학교(KAIST) 구독 여부는 직접 확인할 수 없으므로 **"구독 여부 확인 필요"**로 표시하라.
- 문헌이든 정책이든 **"전부 찾았다"고 주장하지 마라.** 완전성은 섹션 1-2의 검색 프로토콜 기준으로만 서술하라.

## 0-4. 실행 방식: 같은 대화에서 6회로 나누어 실행
이 작업은 한 번에 끝내지 않는다. **같은 대화 안에서 6회차로 나누어** 실행한다.
- 각 실행에서는 **해당 회차의 범위만 완료 기준(0-5)까지** 수행하고 멈춰라.
- 내가 **"이어서"**라고 보내면 `progress_log.md`와 이전 산출물을 읽고 다음 작업을 시작하라.
- 첫 실행은 1회차다.

| 회차 | 범위 | 끝에 있는 Gate | 저장할 산출물 |
|---|---|---|---|
| 1 | 섹션 1–2 (문헌, novelty) | Gate 1 | `literature_table.csv`, `search_log.csv`, `part2_literature.md`, `part4_gap_novelty.md` |
| 2 | 섹션 3–5 (미국 규제 timeline, 중국 정책 timeline, 신호·식별 평가) | Gate 2, Gate 3 | `regulatory_dataset.csv`, `china_policy_dataset.csv`, `part3_timeline.md`, `gate_2_3_assessment.md` |
| 3 | 섹션 6–8, 11–12 (메인 설계, 분해, selection, 교란, 식별 위협) | — | `part6_design_draft.md`, `confounders.csv`, `part8_threats.md` |
| 4 | 섹션 9–10, 13–14 (데이터, crosswalk, salience, BCI) | Gate 4 | `part7_data_manual.md`, `crosswalk_plan.md`, `outcome_freeze.md` |
| 5 | 섹션 15 (Trump 2기 extension, 범위 제한) | — | `policy_events_trump2.csv`, `event_study_candidates.csv`, `part_trump2_extension.md` |
| 6 | 섹션 16–18 (설계 3안, referee, 최종 보고서) | — | `final_report.md` (Part I–X 통합) |

### 모든 회차 공통 규칙
1. **회차 시작 시:** `progress_log.md`와 이전 회차 산출물을 먼저 읽어라.
2. **이전 판단 유지:** 이전 회차에서 확정한 판단(Gate 판정, 규제 데이터셋, crosswalk 정의, outcome freeze)을 임의로 바꾸지 마라. 바꿔야 하면 사유와 변경 전후 내용을 로그에 기록하라.
3. **회차 종료 시:** 산출물을 파일로 저장하고 `progress_log.md`를 갱신하라. 로그에는 다음을 적는다.
   - 완료 기준 체크리스트의 항목별 충족 여부
   - 미충족·미착수 항목
   - Gate 판정 결과 (해당 회차에 Gate가 있으면)
   - 다음 실행의 시작점
   - 핵심 판단 요약
4. **대화창 보고:** 회차가 끝나면 대화창에 짧게 보고하고 멈춰라. 보고 내용은 다음과 같다.
   - 이번 회차의 핵심 결론 5줄 이내
   - 완료 기준 충족 여부
   - Gate 판정과 그에 따른 다음 회차 방향
   - 내가 결정하거나 확인해야 할 사항

## 0-5. 깊이 원칙과 회차별 완료 기준

### 깊이 원칙: "넓게 얕게"보다 "좁게 깊게"
- 실행 중 예산이 부족해지면 **남은 항목을 얕게 채워 넣지 마라.**
- 완료 기준을 충족한 항목까지만 작성하고, 나머지는 **"미착수"**로 로그에 남긴 뒤 멈춰라.
- 다음 "이어서"에서는 **다음 회차로 넘어가지 말고 같은 회차의 미착수 항목부터** 이어서 수행하라.
- 회차 번호와 실제 실행 횟수가 달라져도 괜찮다.

### 회차별 완료 기준

**1회차**
- 섹션 1-2의 검색 프로토콜을 수행했고, `search_log.csv`에 기록했으며, saturation 도달 여부를 보고했다.
- 가장 가까운 논문 최소 10편을 상세 검토했다. 그중 확인 수준이 전문 또는 WP인 논문 수를 로그에 보고하라.
- **검색 프로토콜상 확인된** 2018 ANPRM 기반 논문 각각에 대해 섹션 1-5의 네 질문에 답했다.
- 문헌군 1–9 각각에 대해 최소한 표 기록이 있다.
- Gate 1 판정과 근거(2-3 기준 요소별)를 기록했다.
- 대안 연구질문 2–3개를 제시했다.

**2회차**
- 2018 ANPRM이 규칙이 아님을 보여주는 원문 문구를 인용했다.
- 14개 family와 ANPRM에 나열된 하위기술이 데이터셋에 행으로 존재한다 (ANPRM 원문의 나열과 대조해 누락 여부를 확인했다).
- 각 행에 legal control date, China-binding restriction date, restriction intensity가 채워져 있거나 "미확인"으로 표시되어 있다.
- 신호 연쇄 timeline을 작성했다.
- 중국 정책 timeline 데이터셋과 미국 지목 기술과의 overlap 정량화가 있다.
- Gate 2와 Gate 3 판정과 근거를 기록했다.

**3회차**
- Gate 2·3 결과를 반영한 treatment 정의와 회귀식, 식별 변동 분해를 작성했다.
- 대조 기술 풀 대안 3개를 평가했다.
- 비교국가 오염의 편향 방향을 서술했다.
- censor 규칙(China-binding date, intensity 기준)을 비교했다.
- outcome별 시점 매핑 표를 작성했다.
- inference 방법, multiple testing 처리, MDE 계산 계획을 결정했다.
- confounder 표 전체를 작성했다.
- 반론 7개 각각에 test를 제시했다.

**4회차**
- 섹션 9의 모든 데이터 소스에 필수 항목이 채워져 있다 ("미확인" 표기 허용).
- outcome A–E 각각에 대해 **실행 가능한 확보 경로 최소 1개** 또는 **"현실적으로 불가능" 판정**이 있다.
- crosswalk pipeline과 embedding 모델 후보를 제시했다.
- salience 소스를 평가했다.
- BCI case study 가능성을 판정했다.
- Gate 4 (primary outcome freeze)를 수행하고 `outcome_freeze.md`에 기록했다.

**5회차**
- 섹션 15의 범위 제한 안에서 핵심 사건을 정리했다.
- 각 사건에 발표일, 법적 효력 발생일, 법적 근거, as-of가 있다.
- event study 후보 평가 CSV를 작성했다.

**6회차**
- 설계 3안이 섹션 16의 모든 항목을 포함한다.
- referee report와 Reject / R&R / Accept 평가를 작성했다.
- 수정된 최종안을 작성했다.
- `final_report.md`에 Part I–X를 통합했다.
- 첫 4주 작업 계획을 작성했다.

### 중복 금지
같은 내용을 여러 섹션에서 반복하지 마라.
- confounder는 **섹션 11**에서만 상세히 다룬다.
- 식별 위협과 검정 방법은 **섹션 12**에서만 상세히 다룬다.
- 섹션 6, 17과 Part VIII에서는 해당 표나 번호를 참조하고, 새로운 논점만 추가하라.

## 0-6. Gate 규칙 요약

| Gate | 시점 | 질문 | 실패 시 |
|---|---|---|---|
| Gate 1 — Novelty | 1회차 끝 | 핵심 질문이 기존 연구에서 이미 답변되었는가? (섹션 2) | 3회차 이후 모든 작업을 섹션 2의 대안 연구질문 기준으로 수행 |
| Gate 2 — Announcement-date validity | 2회차 끝 | 2018-11-19 ANPRM이 이전 신호 대비 의미 있는 정보충격인가? (섹션 5-1) | ANPRM을 단일 T=0으로 강제하지 말고 multi-signal / signal-intensity 설계 또는 더 깨끗한 기술별 announcement로 전환 |
| Gate 3 — Identification feasibility | 2회차 끝 | 데이터 구조상 인과식별이 가능한가? (섹션 5-2) | DDD를 기정사실화하지 말고 다른 식별전략 또는 descriptive/case-study 설계로 전환 |
| Gate 4 — Outcome freeze | 4회차 끝 | primary / secondary outcome을 결과를 보기 전에 확정 (섹션 9-F) | — (freeze 후 변경 금지) |

- 각 Gate 판정은 해당 회차 보고에서 분명히 밝혀라.
- 내가 "이어서"와 함께 방향을 지정하면 그 지시를 따르라.
- Gate 1이 실패해도 2회차(timeline)는 수행한다. 대안 질문에도 timeline이 필요하기 때문이다.

## 0-7. Trump 2기의 위상
- **Trump 2기는 본 연구의 main identification이 아니다.** motivation과 optional extension으로만 취급한다.
- 1–4회차에서는 Trump 2기 정책 조사를 하지 마라. 예외는 1회차 문헌군 8의 문헌 기록뿐이다.
- Trump 2기 분석은 5회차에서만, 섹션 15의 범위 제한 안에서 수행한다.

## 0-8. 보고서 순서와 산출물 형식
- 최종 보고서는 섹션 18의 Part 구성을 따른다.
- 본문은 **한국어**로 작성하고, 학술 용어·변수명·법령명은 영어를 병기하라.
- 문헌 표, 검색 로그, 규제 데이터셋, 중국 정책 데이터셋, 이벤트 목록은 본문 표와 별도로 **CSV 파일**로도 제공하라.

---

# 연구의 출발점

> 미국 정부가 특정 기술을 향후 수출통제 대상으로 고려한다고 공식적으로 발표했지만 실제 통제가 즉시 시행되지 않은 경우, 그 "통제 가능성의 신호"만으로도 중국 정부·기업·연구자·투자자가 해당 기술분야에 선제적으로 연구자금과 자본을 배분했는가?

## 출발점이 되는 사례: 2018 ANPRM
2018년 11월 BIS의 **"Review of Controls for Certain Emerging Technologies" ANPRM**은 AI, biotechnology, quantum, advanced computing, microprocessors, robotics, additive manufacturing, brain-computer interfaces 등 여러 emerging technologies를 향후 통제 후보로 제시했다. 그러나 이것 자체는 즉각적인 수출금지나 최종규칙이 아니었다.

기존 논문 중 일부는 이 2018년 발표를 사실상 export-control shock으로 이용하여 이후 중국 특허 변화를 분석한 것으로 알고 있다.

## 시점 구분 원칙
다음을 반드시 구분하라. **"통제를 고려한다는 공식 신호"와 "실제 통제"를 섞지 마라.**
- announcement date
- ANPRM / request for comments (comment 마감일과 연장 포함)
- proposed rule
- final rule / interim final rule
- effective date
- legal control date: 법적으로 해당 기술이 통제 대상이 된 날
- China-binding access restriction date: 중국 측의 해당 기술 접근에 **실질적인 추가 제한**이 생긴 날

## 신호는 단일 날짜가 아니라 연쇄일 수 있다
2018-11 ANPRM 이전과 이후에도 관련 신호가 있었다. 예를 들면 다음과 같다.
- 2018 ZTE 제재
- FIRRMA·ECRA 입법 논의
- 2018-08 ECRA 제정 (emerging technology 식별 절차를 법제화)
- 2020-08 foundational technologies ANPRM
- 2021 BCI ANPRM

따라서 2018-11 ANPRM을 **처음부터 T=0으로 전제하지 마라.** announcement를 **신호들의 연쇄(signal chain)**로 다루고, ANPRM이 메인 event로 적합한지는 Gate 2에서 판정한다.

---

# 1. 선행연구 review

## 1-1. 범위와 깊이
- **가장 가까운 논문 10–15편:** 원문 기준으로 상세 검토하라.
- **나머지:** 간략 표로 정리하라.
- **6번 문헌군(타 분야 regulation threat):** 대표 논문 3–5편으로 제한하라.

## 1-2. 검색 프로토콜
"전부 찾았다"고 주장하는 대신, 다음 프로토콜을 수행하고 기록하라.
1. **데이터베이스:** Google Scholar, Crossref 또는 OpenAlex, SSRN, RePEc/IDEAS, NBER, 그리고 접근 가능한 기타 bibliographic database
2. **검색어:** 영어 검색어 조합을 사전에 정의하라. 예: export control, Entity List, emerging technologies, ANPRM, China innovation, patents, anticipation, policy uncertainty. 가능하면 중국어 검색어(出口管制, 实体清单, 创新, 专利 등)로 CNKI 등 중국어 문헌도 검색하라. 접속이 안 되면 "접속 불가"로 기록하라.
3. **Citation search:** 핵심 논문의 backward citation(참고문헌)과 forward citation(인용한 논문)을 검색하라.
4. **기록:** 다음 컬럼으로 `search_log.csv`를 작성하라.
   `search date | database | query | hit count | screened count | new directly-relevant papers`
5. **Saturation:** 연속 두 차례의 검색 라운드에서 새로운 직접 관련 논문이 나오지 않을 때를 saturation으로 정의하라. 도달 여부를 보고하라.

## 1-3. 검토할 문헌군

1. **Trump 1기 Entity List / Huawei / ZTE / FDPR의 영향.** 중국 기업의 다음 변수에 미친 영향을 본 연구:
   - R&D
   - patent quantity
   - patent quality
   - breakthrough innovation
   - domestic substitution
   - M&A
   - financing
   - VC
   - supply-chain restructuring
2. **2018 Emerging Technologies ANPRM을 treatment로 사용한 연구**
3. **export-control announcement / policy uncertainty / anticipation effect를 직접 연구한 논문**
4. **trade-policy uncertainty와 firm R&D 또는 innovation**
5. **tariff announcement와 innovation 또는 investment**
6. **타 분야의 regulation threat / proposed regulation / rulemaking announcement와 기업행동**
   - environmental, financial, antitrust, pharmaceutical regulation 등
   - 대표 3–5편만
7. **2022–2024 Biden administration semiconductor export controls 실증연구**
8. **Trump 2기(2025–기준일)의 기술수출통제·관세·AI chip policy 관련 최신 문헌**
   - working paper, policy paper, NBER/SSRN/RePEc/CEPR/Fed 논문
   - 문헌 기록만 하고, 정책 조사 자체는 5회차에서 한다 (0-7).
9. **미국 공급기업 측 효과** (매출·R&D·시장가치 손실)

## 1-4. 문헌 표의 컬럼
각 논문에 대해 다음을 표로 정리하라.
- full citation
- publication / working paper status
- 확인 수준 (0-2 기준)
- sample period
- treatment, 그리고 **treatment date로 사용한 날짜**
- 기술 분류·매핑 방법 (어떤 IPC/CPC/키워드로 treated technology를 정의했는지)
- identification strategy
- dependent variables
- main findings
- 내 연구와 겹치는 부분
- 남아 있는 research gap

## 1-5. 2018 ANPRM 기반 논문에 대한 핵심 확인 사항
검색 프로토콜상 확인된, 2018 ANPRM 이후 중국 특허·혁신 변화를 분석한 논문 각각에 대해 다음을 원문 기준으로 확인하라.
- announcement effect를 실제로 분리했는가, 아니면 단순히 2018 이후를 post로 두었는가?
- 표본 기간에 ANPRM 대상 기술 중 **이후 실제 통제된 하위기술**이 포함되어 있는가? 포함되어 있다면 그 시점 이후를 어떻게 처리했는가?
- 비교국가나 비교기술을 썼는가? 썼다면 무엇을 썼는가?
- patent date로 application / priority / publication / grant 중 무엇을 썼는가?

---

# 2. Novelty 검증 (Gate 1)

## 2-1. 검증할 질문
> **Does the threat of future export controls induce anticipatory innovation and investment before actual restrictions are implemented?**

더 구체적으로는:

> 미국이 특정 기술을 미래 수출통제 후보로 공식 지목했지만 실제 통제가 아직 시행되지 않은 기간에, 중국의 연구자금, VC, 논문, 특허, 기업 R&D가 상대적으로 증가하는가?

그리고:

> 실제 통제가 나중에 도입되었을 때 추가적인 반응이 존재하는가, 아니면 대부분의 반응이 announcement 단계에서 이미 발생하는가?

## 2-2. 효과의 정의
다음 세 효과를 아래 정의대로 사용하라.
1. **Announcement effect:** 공식 신호 이후, China-binding access restriction 발생 이전 구간에서의 상대적 반응
2. **Implementation effect:** China-binding access restriction 발생 이후 announcement effect를 넘어서는 추가 반응. 가능하면 restriction intensity(섹션 3-4)별로 구분한다.
3. **Persistence effect:** 신호 이후 추가 신호나 실제 통제가 없는 상태에서도 반응이 유지되는지 여부
   - 후속 신호(2020 foundational ANPRM, 2021 BCI ANPRM, 다른 통제 뉴스)에 의해 **재점화된 반응**과 구분해야 한다.

## 2-3. 판정 기준
기존 연구가 다음 네 요소를 **모두** 다루었으면 "실질적으로 답변됨"으로 판정하라.
- (a) treatment가 **실제 제한 없는 공식 신호**로 정의됨
- (b) **실제 통제 이후 구간을 분리하거나 제외**함
- (c) outcome이 **연구자금·자본·연구활동**을 포함함 (특허만이 아님)
- (d) 기술 단위의 **비교집단**을 가짐

판정은 다음 셋 중 하나로 내리고, 근거 논문과 해당 요소를 명시하라.
- 실질적으로 답변됨
- 부분적으로 답변됨 (어떤 요소가 비어 있는지 명시)
- 미답변

## 2-4. 가장 흥미로운 subgroup에 대한 확인
특히 흥미로운 subgroup은 다음이다.

> **2018년에 통제 후보로 공식 지목되었지만 수년간 실제 통제가 시행되지 않은 기술**

이 집단에서 연구투자가 지속적으로 증가했다면, "미국이 실제 기술접근을 막지 않았음에도 중국의 연구방향을 바꿨다"는 결과가 가능하다.

다만 다음을 먼저 확인하라.
- 이 집단이 실제로 소수인지, 아니면 **ANPRM 대상 하위기술의 다수**인지 (2회차 데이터셋으로 최종 확인)
- BIS의 식별 절차가 느렸다는 비판이 있었다면, 시간이 지나며 **신호의 신뢰도가 하락**했을 가능성 (시장이 "BIS는 느리다"는 것을 학습했을 가능성)

## 2-5. 기존 연구 재해석 가능성
궁극적 질문의 두 번째 부분은 다음이다.

> 기존 연구에서 관찰된 '수출통제 이후 중국 혁신 증가' 중 일부는 anticipatory response였던 것은 아닌가?

이에 답하려면 다음을 구체적으로 평가하라.
- **어떤 기존 논문의 어떤 추정치**를 announcement 구간과 implementation 구간으로 재분해해야 하는가?
- 그 논문의 표본 정의·treatment 정의를 **재현할 수 있는가?** (replication package 공개 여부 포함)

## 2-6. 대안 제시
novelty가 없거나 부분적이면 숨기지 말고 명시하라. 그리고 **더 좁고 참신한 대안 연구질문 2–3개**를 제시하라.

**1회차 종료:** 0-4의 산출물을 저장하고, 로그를 갱신하고, Gate 1 판정을 대화창에 보고한 뒤 멈춰라.

---

# 3. 미국 규제 timeline 구축 (Trump 1기 ~ Biden기)

## 3-1. 자료 원칙
Federal Register, BIS, U.S. Department of Commerce, Regulations.gov 등 **1차 자료**를 사용하라.

## 3-2. 포함할 항목
- 2018 ZTE 제재와 FIRRMA·ECRA 입법 과정, 2018 ECRA 제정
- 2018-11-19 Emerging Technologies ANPRM
  - FR citation, document number, docket number
  - comment 마감일과 연장 여부
- ANPRM의 14개 기술군과 **ANPRM 본문에 나열된 세부 하위기술**
- 2020 foundational technologies ANPRM
- 2021 BCI ANPRM
- 이후 각 하위기술의 실제 regulation history
- 2022년 이후 "Section 1758 technologies" 체계로의 전환
- unilateral control인지, Wassenaar 등 multilateral regime을 통한 것인지

2018 ANPRM 자체가 "actual control"이 아니었다는 점은 **ANPRM 원문의 공식 문구를 인용하여** 검증하라.

## 3-3. 세 층위 데이터셋
실제 통제는 넓은 기술군(family) 단위가 아니라 **좁은 ECCN 단위**로 들어왔다. 확인 필요한 예시는 다음과 같다.
- 2020-01 geospatial imagery 분석 소프트웨어 interim final rule
- 2020년 Wassenaar 합의 반영 품목
- 2022-08 GAAFET용 ECAD, Ga₂O₃, diamond 등 interim final rule
- 2024 quantum 관련 interim final rule

따라서 데이터셋을 **family / subcategory / ECCN** 세 층위로 만들고, 상위 층위와의 연결을 유지하라. 각 행의 컬럼은 다음과 같다.

`layer | family | subcategory | technology description | 2018 announced? | 후속 ANPRM/proposed rule (날짜, FR citation) | final/interim final rule (날짜, FR citation) | effective date | legal control date | China-binding access restriction date | restriction intensity | intensity 판정 근거 | ECCN | 통제 지역 범위 (전 세계 / 특정국 / 중국·우려국 한정) | unilateral vs multilateral | actual restriction description | 기준일 현재 미통제 여부 | as-of | source URL | 확인 수준`

## 3-4. Legal control과 China-binding restriction의 구분
어떤 규칙이 법적으로 기술을 통제했더라도, 중국 측의 해당 기술 접근에 **실질적인 추가 제한**을 만들지 않았을 수 있다. 예를 들면 다음과 같은 경우다.
- 해당 품목이 이미 다른 ECCN이나 중국 대상 기존 제한으로 묶여 있었던 경우
- license exception이 넓게 적용되는 경우

또 규제 형태에 따라 경제적 의미가 크게 다르다.
- 전 세계 대상 license requirement
- China-specific restriction
- 특정 end-user만 대상
- case-by-case review
- presumption of denial

따라서 각 규칙에 **restriction intensity**를 코딩하라.
- `0` = 중국 측에 실질적 추가 제한 없음
- `1` = license requirement (approval 정책이 열려 있거나 case-by-case)
- `2` = restrictive review policy (중국·우려국에 대해 제한적 심사)
- `3` = presumption of denial 또는 사실상 금지

**임의적 index가 되지 않도록, 각 단계의 법적 판정 기준(license review policy 문구, 적용 지역, 적용 대상)을 데이터 코딩 전에 문서로 정의하라.** 판정 근거는 각 행의 `intensity 판정 근거` 컬럼에 기록하라.

## 3-5. 부분통제 정리
각 family와 subcategory에 대해 다음을 정리하라.
- 하위 단위 중 일부만 통제된 경우, **언제 어떤 비중이 어떤 intensity로** 통제되었는지
- 2018 지목 이후 **기준일까지 China-binding restriction이 한 번도 생기지 않은 하위기술의 목록과 비중**

## 3-6. 통제 지역 범위
emerging technology 통제 중 상당수는 중국 전용이 아니라 **전 세계 대상 license requirement**였을 수 있다 (예: 0Y521 계열). 각 통제의 지역 범위를 반드시 기록하라. 이는 섹션 6의 비교국가 오염 문제와 직결된다.

데이터셋은 `regulatory_dataset.csv`로 저장하라.

---

# 4. 중국 정책 timeline 구축

중국 측 기술별 산업정책은 이 연구의 **가장 큰 식별위협**이다. 단순한 robustness 항목으로 두지 말고 **별도 데이터셋**으로 구축하라.

## 4-1. 수집 범위
- State Council, MIIT, MOST, NDRC 등 중국 중앙정부의 기술별 육성계획·보조정책·산업계획·국가 프로젝트를 수집하라.
- 예 (검증 필요):
  - Made in China 2025 (2015)와 그 중점 분야
  - 2017 新一代人工智能发展规划
  - 반도체 Big Fund 1·2·3기
  - 양자·BCI·로봇 등 기술별 계획과 14차 5개년 계획의 전략기술 목록
- 2015년 전후부터 기준일까지를 범위로 하되, **2018-11 이전에 이미 전략기술이었는지**를 판별할 수 있도록 2018년 이전 정책을 우선 확보하라.

## 4-2. 데이터셋 형식
각 정책에 대해 다음을 기록하라.

`policy name | issuing body | announcement date | effective date | targeted technology | ANPRM family/subcategory ID 매핑 | policy type (계획 / 보조금 / 펀드 / 국가 프로젝트 / 규제) | funding commitment | source URL | 확인 수준`

- 기술 매핑은 섹션 3 데이터셋과 **동일한 ID 체계**를 사용하라.
- 중국 정부 사이트에 접속할 수 없으면 "접속 불가"로 표시하고 대체 출처(공식 문건 전재본, 학술 자료)를 사용하되 확인 수준을 낮춰 표시하라.

## 4-3. Overlap 정량화
- 미국 ANPRM 지목 기술(family/subcategory)과 중국 기존 정책 대상 기술의 overlap을 정량화하라.
- 미국 신호와 중국 정책 발표 시점이 **같은 기술에서 얼마나 가까이 붙어 있는지**를 기술별로 정리하라.
- **2018-11 이전에 중국에서 명시적으로 전략기술이 아니었던 하위기술**의 목록을 만들어라. 이 목록은 이후 robustness 표본으로 쓴다.

데이터셋은 `china_policy_dataset.csv`로 저장하라.

---

# 5. 신호 타당성과 식별 가능성 평가 (Gate 2, Gate 3)

섹션 3–4의 데이터셋을 바탕으로 두 Gate를 판정하라. 결과는 `gate_2_3_assessment.md`로 저장하라.

## 5-1. Gate 2 — Announcement-date validity
2018-11-19 ANPRM이 이전 신호 대비 어떤 **새로운 정보**를 제공했는지 평가하라.
1. ANPRM이 **처음으로 특정 기술군을 명시**했는가? ECRA 조문, 의회 논의, 이전 정부 발표에 이미 같은 기술이 거론되었는가?
2. 시장이나 중국 언론의 관심이 ANPRM 시점에 **비연속적으로 증가**했는가? 이 회차에서는 확보 가능한 범위의 예비 지표(뉴스 검색량, 중국 언론 보도 건수 등)로 평가하고, 본격적인 salience 측정은 섹션 13으로 넘긴다고 명시하라.
3. 이전 신호(ZTE 제재, FIRRMA/ECRA 논의)만으로 **treatment 기술을 예상할 수 있었는가?**

판정:
- **통과:** ANPRM이 충분한 incremental information shock이다. 메인 event로 쓴다.
- **실패:** ANPRM을 단일 T=0으로 강제하지 마라. 다음 중 대안을 제시하라.
  - multi-signal design (신호별 별도 event)
  - signal-intensity design (신호의 구체성·언론 주목도로 노출 강도 정의)
  - 더 깨끗한 기술별 announcement 이용 (예: 2020 foundational ANPRM, 2021 BCI ANPRM)

## 5-2. Gate 3 — Identification feasibility
novelty가 있어도 식별이 불가능할 수 있다. 다음 네 조건을 평가하라.
1. China-binding restriction 이전의 **clean announcement-only period**가 충분히 존재하는가? (기술별 기간 분포를 제시하라)
2. 비교 가능한 **untreated 또는 later-signaled technology**가 충분한가?
3. **중국의 동시 기술별 산업정책과 미국의 신호를 시간적으로 구분**할 수 있는가? (섹션 4-3 결과 사용)
4. treated technology 수와 기간이 **통계적 inference에 충분**한가?

판정:
- 각 조건을 `충족 / 부분 충족 / 심각하게 미충족`으로 판정하고 근거를 적어라.
- 하나라도 **심각하게 미충족**이면 3회차에서 기본 DDD를 기정사실화하지 마라. 다른 식별전략(섹션 16의 설계 후보) 또는 descriptive/case-study 설계로 전환할 것을 제안하라.

**2회차 종료:** 0-4의 산출물을 저장하고, 로그를 갱신하고, Gate 2·3 판정과 3회차의 설계 방향을 대화창에 보고한 뒤 멈춰라.

---

# 6. 메인 empirical design

**Gate 1–3의 결과를 반영해 이 섹션을 작성하라.** 아래 DDD는 Gate를 모두 통과했을 때의 기본형이다. Gate 2가 실패했다면 treatment 정의를 그 결과에 맞게 바꿔라.

## Core question
> 실제 수출통제가 시행되기 전에 "향후 이 기술이 통제될 수 있다"는 미국 정부의 공식 신호만으로, 중국의 연구·투자가 해당 기술에 증가했는가?

## 6-1. 기본 DDD

$$
Y_{ckt}=\alpha_{ck}+\delta_{ct}+\lambda_{kt}+\beta\,(China_c \times ThreatenedTechnology_k \times PostSignal_t)+\epsilon_{ckt}
$$

- 분석단위: `country × technology × period`
- 비교국가 후보: China, South Korea, Japan, Taiwan, United States, Germany 등
- `PostSignal_t`의 정의는 Gate 2 결과를 따른다.

각 fixed effect가 무엇을 제거하는지 설명하고, 다음을 반드시 다뤄라.

**(1) 식별 변동의 원천 분해**
β가 실제로 어떤 비교에서 나오는지 명시하라.
- 중국 vs 타국의 차이인가?
- 지목 기술 vs 비지목 기술의 차이인가?

**(2) 대조 기술 풀(control technology pool)의 정의**
2018 ANPRM의 14개 기술군은 frontier 기술 대부분을 포괄한다. 그래서 "지목되지 않은 기술"이 성숙·저기술 분야로 쏠려 비교 불가능할 위험이 있다. 다음 대안을 비교하라.
- 지목 이전 성장률이나 세계적 R&D 강도로 매칭한 비지목 기술
- 같은 기술군 안에서 지목된 하위기술 vs 지목되지 않은 인접 하위기술
- 지목 시점이 다른 기술 간 비교 (2018 vs 2020 foundational vs 2021 BCI)

**(3) 비교국가 오염 (SUTVA)**
- 통제가 전 세계 대상 license requirement였다면, 한국·일본·대만·독일 연구자와 기업도 같은 신호에 반응했을 수 있다.
- 미국은 통제 주체이고 동시에 CHIPS Act 등 자체 정책 변화가 있었으므로 **대조군으로 적합한지** 별도로 평가하라.
- 오염이 β를 어느 방향으로 편향시키는지 서술하라.

**(4) 교란이 변하는 차원과 FE 흡수 여부**
- country×time FE는 중국 전체 충격을 제거하고, technology×time FE는 세계 공통 기술 추세를 제거한다.
- 그러나 **중국 × 특정 기술 × 시점(c×k×t)** 차원에서 변하는 교란은 **어떤 FE 조합으로도 흡수되지 않는다.** 이는 treatment와 같은 차원이기 때문이다.
  - 예: Made in China 2025 중점 분야, Big Fund, 중국의 기술별 육성정책
- 이 교란은 섹션 4의 중국 정책 데이터셋으로 직접 다뤄라. 예:
  - 중국 정책 노출을 기술×시점 변수로 만들어 함께 추정
  - 2018-11 이전에 중국 전략기술이 아니었던 하위기술만으로 추정 (섹션 4-3 목록)
  - 미국 신호와 중국 정책 발표가 시간적으로 떨어진 기술만으로 추정

## 6-2. Pure announcement period 설계
**China-binding restriction이 시작되는 시점부터 해당 technology cell을 censor하여, 실제 restriction이 없는 기간만으로 announcement effect를 식별**하는 방법을 검토하라.

다음을 명시적으로 다뤄라.

**(1) Censor 기준**
- censor는 legal control date가 아니라 **China-binding access restriction date**를 기준으로 한다.
- restriction intensity 0인 규칙은 censor 사유가 아니다.
- intensity 문턱값(1 이상 / 2 이상)에 따른 결과 차이를 비교하라.

**(2) 부분통제 시 censor 규칙**
하위 ECCN 일부만 통제된 경우의 대안을 비교하라.
- family 전체 censor
- 통제된 subcategory만 censor
- 통제 비중과 intensity를 연속변수로 처리

**(3) censoring이 유발하는 selection**
일찍 통제된 기술이 표본에서 빠지면, 남은 표본은 "늦게 통제되었거나 끝까지 통제되지 않은 기술"이 된다. 이는 섹션 8의 eventually-controlled selection 문제와 동일한 구조이므로 연결하여 평가하라.

**(4) 식별가정과 약점**
이 방법의 식별가정과 약점을 냉정하게 평가하라.

## 6-3. Outcome별 시점 매핑
outcome마다 의사결정 시점과 관측 시점이 다르다. outcome별로 다음을 정리하고, **outcome별로 가능한 패널 빈도**를 정하라. 일괄적으로 quarter나 year를 적용하지 마라.

| 항목 | 정리할 내용 |
|---|---|
| 의사결정 시점 | 예: NSFC 신청서 제출, VC 투자 결정, 특허 출원 |
| 관측 가능한 날짜 변수 | 해당 데이터에 실제로 기록된 날짜 |
| 신호 이후 첫 반영 가능 시점 | 예: NSFC는 일반적으로 연 1회 사이클(봄 접수, 여름 발표)이므로 2018-11 신호의 첫 반영은 2019년 사이클일 가능성이 높다. 정확한 일정은 검증하라. |
| 공개 지연 | 예: 특허는 priority date 기준이며 출원 후 공개까지 약 18개월 |

## 6-4. 추정과 추론
- **count outcome:** log(1+y) 대신 PPML 등 count 모형의 사용 여부를 검토하라.
- **클러스터 수 문제:** family 단위면 treated cell이 14개(× 중국 1개국) 수준이라 통상적인 clustered SE를 신뢰하기 어렵다. 다음 대안을 비교하라.
  - ANPRM 하위기술 단위로 내리기
  - randomization inference / permutation test
  - wild cluster bootstrap
- **post-treatment controls**를 넣지 않도록 통제변수 선택 원칙을 명시하라.
- **Multiple testing:** primary outcome과 primary specification을 사전에 지정하라 (Gate 4). secondary outcome이나 technology-level heterogeneity를 여러 개 보고할 경우 FDR(q-value) 등 적절한 multiple-testing adjustment를 함께 보고하는 계획을 세워라.
- **최소탐지효과(MDE):** main regression 전에 실제 treatment cluster 수와 pre-period 분산으로 MDE를 계산하는 계획을 세워라. 이 단계에서 실제 데이터가 없으면 계산식, 필요한 입력값, 그리고 합리적 범위의 시나리오별 MDE를 제시하라. 현실적인 효과 크기를 검출할 power가 없다면 causal design을 과장하지 말고 descriptive/case-study design으로 전환할 것을 명시하라.

---

# 7. Announcement와 Implementation의 분해

$$
Y=\beta_A\,AnnouncementExposure+\sum_{j}\beta_{I,j}\,ActualControl^{(intensity=j)}+FE+\epsilon
$$

- $\beta_A$: China-binding restriction 이전의 anticipatory response
- $\beta_{I,j}$: intensity $j$의 restriction 이후 additional effect

이 구조로 **announcement → partial implementation → severe implementation**을 분해할 수 있는지 검토하라.

treatment timing과 eventual-control selection이 endogenous하므로 단순 비교가 왜 위험한지 설명하라. 그리고 다음 중 어떤 방법이 가장 적절한지, 이 연구의 **treated unit 수와 timing 구조**를 고려해 논의하라.
- stacked event study
- matched technology
- synthetic control
- continuous exposure
- pre-trend matching
- Sun-Abraham
- Callaway-Sant'Anna
- imputation estimator
- randomization inference
- permutation test

---

# 8. "Eventually controlled vs never controlled"를 조심해서 다뤄라

미국이 어떤 기술을 실제로 통제할지 여부 자체가 endogenous할 가능성이 높다. 중국의 해당 기술 성과가 통제 결정에 영향을 줬을 가능성(reverse causality)도 있다.

따라서 다음을 지켜라.
- eventually controlled vs never controlled의 차이를 곧바로 causal effect라고 주장하지 마라.
- 이 구분을 persistence, heterogeneity, descriptive evidence 정도로 사용할 수 있는지 검토하라.
- 더 강한 identification이 가능하다면 제시하라.
- 섹션 2-4의 **신호 신뢰도 하락** 가능성이 이 비교의 해석을 어떻게 바꾸는지도 논의하라.

**3회차 종료:** 섹션 11–12까지 마친 뒤 산출물을 저장하고, 로그를 갱신하고, 대화창에 보고한 뒤 멈춰라.

---

# 9. Outcome variable과 데이터 (특허에만 의존하지 마라)

기존 literature가 patent count에 매우 집중되어 있으므로, 본 연구는 **"announcement → capital/research reallocation"**을 먼저 보고 싶다. 각 outcome의 장단점을 평가하고, 실제 데이터 확보 가능성을 **0-2의 확인 수준과 함께** 확인하라.

## A. 중국 VC / startup investment
후보 데이터:
- IT桔子
- CVSource / Zero2IPO
- PitchBook
- Crunchbase
- Refinitiv VentureXpert / LSEG
- CSMAR PE/VC database

각각에 대해 다음을 적어라.
- 실제 접근 URL
- 유료/무료
- 학교 구독 가능성 ("확인 필요" 표시)
- 제공 변수
- 중국 deal의 historical coverage
- API/download 여부
- firm description / industry / investment amount / funding date 제공 여부

특히 **technology-quarter VC investment**를 구축할 수 있는지 확인하라.

## B. 중국 정부 연구자금 (NSFC 중심)
필요 변수:
- project title
- abstract/keywords
- funding year
- grant amount
- institution
- PI
- research field (申请代码)

NSFC 공식 포털에서 실제로 공개되는 정보를 확인하고, 다음을 적어라.
- 공식 사이트 URL
- 검색 메뉴
- 다운로드 가능 여부
- API 유무
- bulk data 확보 가능 여부
- scraping 필요 여부와 이용약관상 제약
- 금액 공개 여부
- historical coverage
- **연간 신청·발표 일정**

NSFC 외에 확보 가능한 중국 정부의 기술별 보조금·연구지원 데이터가 있다면 제안하라.

## C. 학술논문
OpenAlex, Dimensions, Web of Science, Scopus를 비교하라.

OpenAlex에 대해서는 **현재 기준 이용조건**(API key 필요 여부, 요청 한도, 비용)을 확인하고, 다음 항목을 실제 API/query 수준으로 설명하라.
- API endpoint
- institution country filtering
- topic filtering
- publication date
- citations
- international collaboration
- funder/grant data

목표 변수:

$$
ChinaPapers_{technology,t},\quad USChinaCollaboration_{technology,t}
$$

## D. 특허
PATSTAT, Google Patents Public Data, Lens, CNIPA를 비교하라.

**PATSTAT을 사용한다면** 다음을 설명하라.
- EPO account 생성 절차
- PATSTAT Global / TIP 접근
- 필요한 table과 field 이름
- application date / earliest priority date
- applicant country
- IPC/CPC
- citations
- patent family
- 각각을 어디서 받는지

**Google Patents Public Data를 사용한다면** 다음을 확인하라.
- BigQuery dataset 이름
- 필요한 fields
- embeddings 존재 여부와 필드명
- 비용 발생 구조 (무료 한도, 스캔량 기준 과금)

**중국 특허의 특수성**도 논의하라. 실용신안 포함 여부, 보조금 유도 저품질 출원 문제가 있으므로 다음 지표를 함께 검토하라.
- invention patent only
- 해외 동시출원 family
- 심사 통과 여부

## E. 상장기업 R&D
CSMAR / WIND / CNRDS / CNINFO를 비교하라.

CSMAR에서 실제 필요한 database/table을 확인하라. 다음 각 변수의 데이터베이스 위치나 product name을 가능한 한 구체적으로 적어라. **확인하지 못한 table명은 미확인으로 두어라.**
- R&D expense
- R&D personnel
- sales
- assets
- government subsidy
- ownership
- industry
- stock returns

학교 구독이 없을 경우를 대비해 **CNINFO annual report를 이용하는 fallback**도 설계하라.

## F. Outcome selection rule (Gate 4)
A–E의 평가를 마친 뒤, **실제 treatment 결과를 보기 전에** 각 outcome을 다음 기준으로 평가하라.
1. announcement에 대한 반응 속도 (6-3의 시점 매핑 기준)
2. 연구·자본 배분과의 직접성
3. coverage
4. technology classification 정확도
5. 데이터 접근 가능성
6. 예상 표본 크기와 MDE (6-4 기준)

평가 결과로 **primary outcome 1개와 secondary outcome 1–2개를 선택하고 freeze**하라.
- 선택 근거와 평가 표를 `outcome_freeze.md`에 기록하라.
- freeze 이후 **결과의 유의성에 따라 primary outcome을 변경하지 마라.** 데이터 접근 실패 등으로 불가피하게 바꿔야 하면 사유를 기록하고, 변경 전후를 모두 보고하라.
- 나머지 outcome은 long-run corroborating 또는 exploratory로 분류하라.

---

# 10. 기술분류 crosswalk

2018 ANPRM의 기술문구를 다음에 연결해야 한다.
- IPC
- CPC
- OpenAlex topics
- startup industry descriptions
- NSFC project text (중국어)

## 10-1. Reproducible pipeline
다음 단계를 포함한 pipeline을 제안하라.
1. ANPRM 14개 기술군과 subcategories 추출 (섹션 3·4 데이터셋과 동일 ID 체계 사용)
2. WIPO IPC/CPC definitions 확보
3. keyword dictionary 작성 (영어·중국어)
4. sentence embedding 생성
   - **다국어 모델 후보**를 제안하라 (중국어 NSFC 텍스트와 영어 정의를 같은 공간에 놓아야 하므로).
5. cosine similarity로 candidate codes 생성
6. manual validation
   - 검증 표본 크기
   - 2인 코딩 가능 여부
   - precision/recall 보고
7. **outcome 데이터를 보기 전에** crosswalk와 treatment 정의를 freeze
   - 버전과 날짜를 기록하라.
   - 가능하면 pre-analysis plan으로 문서화하라.

## 10-2. 추가 검토 사항
- 결과를 본 뒤 treatment technology를 조정하는 **p-hacking 위험**과 이를 막는 절차
- 대조 기술(섹션 6-1(2))도 **같은 pipeline으로 사전에 정의**해야 한다는 점
- **similarity threshold** 선택에 대한 robustness

---

# 11. Confounders

다음 동시정책과 이벤트를 고려하라.
- Made in China 2025
- U.S.-China trade war
- Section 301 tariffs
- ZTE 제재 (2018), Huawei Entity List (2019) 및 FDPR
- Chinese industrial subsidies
- semiconductor Big Fund
- COVID-19
- AI boom
- CHIPS Act
- Biden 2022 semiconductor controls
- Chinese retaliatory export controls (2020 수출통제법 포함)
- Chinese semiconductor equipment investment
- global semiconductor cycle
- 중국의 기술별 육성정책 (BCI 포함)

각 confounder에 대해 다음을 표로 정리하고 `confounders.csv`로 저장하라.
- 변하는 차원: `c×t / k×t / c×k×t`
- 어떤 FE로 흡수되는지, 또는 흡수되지 않는지
- 흡수되지 않는다면 어떤 robustness design으로 다룰지 (중국 정책 교란은 섹션 4 데이터셋 활용)

**c×k×t 교란을 FE로 통제된다고 쓰지 마라.**

---

# 12. Announcement effect의 식별문제를 공격하라

다음 반론을 심각하게 검토하라.

- **반론 1.** 미국이 future-control candidate로 지목한 기술은 애초에 향후 중요해질 기술이었다. 따라서 중국 연구 증가는 announcement가 아니라 global technological trend 때문일 수 있다.
- **반론 2.** 중국은 이미 해당 기술을 국가전략으로 지정하고 있었다. (섹션 4 데이터셋으로 정면 대응)
- **반론 3.** 2018년은 미중 무역전쟁 전체가 시작된 해다.
- **반론 4.** 연구자와 기업이 실제 ANPRM을 알고 행동했다고 어떻게 알 수 있는가?
- **반론 5.** 중국 연구 증가가 미국 발표에 대한 반응이 아니라, 동시에 이루어진 중국 정부정책 때문일 수 있다.
- **반론 6.** 비교국가도 같은 신호에 반응했다면 DDD는 효과를 과소추정하거나 왜곡한다.
- **반론 7.** 기대는 ANPRM 이전(ECRA 논의, ZTE 제재)부터 형성되었을 수 있으므로 announcement date 설정이 자의적이다. (Gate 2 결과와 연결)

각 반론에 대해 가능한 empirical test를 제안하라. 예:
- pretrend
- placebo announcement date
- unaffected technologies
- other-country comparison
- official Chinese policy-document text
- media coverage intensity
- Baidu index
- Chinese government document mentions
- public-comment salience
- event-specific news coverage
- 대체 announcement date에 대한 sensitivity
- 중국 전략기술 지정 이력이 없는 하위기술만의 표본

결과는 `part8_threats.md`에 심각도 순으로 정리하라.

---

# 13. Salience / awareness mechanism

"ANPRM이 발표되었다"는 것만으로 중국 기업이 이를 실제 인지했다고 가정하는 것은 약할 수 있다. 다음 자료에서 해당 미국 규제 발표에 대한 관심 증가를 측정할 수 있는지 검토하라.
- 중국 언론 보도
- 정부 문건
- 기업 annual report
- earnings calls / 投资者关系 기록
- Baidu search index
- WeChat / media archive
- policy database
- 중국 학술논문의 언급

각 소스에 대해 다음을 정리하라.
- 접근 가능성 (0-2 기준 확인 수준 포함)
- 기술별로 salience를 측정할 수 있는지
- Gate 2의 예비 지표를 보강하거나 뒤집을 수 있는지

이를 통해 다음 메커니즘을 보완할 수 있는지 검토하라.

$$
Announcement \rightarrow Awareness \rightarrow Investment
$$

---

# 14. BCI case study

Brain-Computer Interface는 2018 ANPRM에서 후보 기술로 언급되었고, 2021년 BIS가 다시 BCI 관련 ANPRM을 발표했다. 따라서 다음과 같은 repeated-treatment 구조를 만들 수 있는지 확인하라.

$$
2018\ \text{broad signal},\quad 2021\ \text{technology-specific signal}
$$

## 14-1. 분석 가능성
BCI 관련 다음 데이터가 2018과 2021에 각각 어떻게 반응하는지 분석할 수 있는지 검토하라.
- 중국 NSFC projects
- papers
- patents
- VC investment

## 14-2. 주의할 점
- BCI가 이미 중국 자체 정책으로 빠르게 성장한 분야라는 점을 반드시 고려하라. 섹션 4 데이터셋의 BCI 관련 정책·국가 프로젝트 날짜와 미국 신호 시점이 겹치는지 확인하라.
- BCI 분야의 규모(연간 건수)가 통계적 검정에 충분한지 확인하라.

**4회차 종료:** Gate 4(outcome freeze)를 수행한 뒤 산출물을 저장하고, 로그를 갱신하고, 대화창에 보고한 뒤 멈춰라.

---

# 15. Trump 2기 extension (범위 제한)

## 15-1. 위상과 범위
- 0-7에 따라 Trump 2기는 **motivation과 optional extension**이다. main identification에 쓰지 마라.
- 이 회차에서는 **핵심 사건 15개 이내**로 범위를 제한하라. 세부 규칙 변경을 모두 나열하지 말고, event study 후보가 될 수 있는 사건 위주로 정리하라.
- Trump 2기는 장기 특허효과를 보기엔 아직 너무 짧다. 따라서 high-frequency response만 검토하라.
  - Chinese semiconductor / GPU firm stock returns
  - VC announcements
  - analyst reports
  - corporate disclosure
  - policy text

## 15-2. 조치 유형별 분류
조치를 다음 세 유형으로 **분리하여** 정리하라. 관세와 수출통제를 같은 정책으로 취급하지 마라.

**(a) 수출통제 조치**
- NVIDIA H20 중국 수출 license requirement 부과와 이후 relaxation
- H200 / AMD MI325X 등 관련 정책과 license review policy 변경
- Entity List 확대
- affiliate rule (50% rule) 도입과 그 이후 유예·변경 상태
- semiconductor manufacturing equipment controls
- AI Diffusion Rule 철회 또는 대체

**(b) 무역조치**
- Section 232 semiconductor investigation
- semiconductor tariffs
- 대중 일반관세
- technology-specific tariff

**(c) 조건부 접근·협상형 조치**
- 수익공유 조건부 수출허가
- 정상회담 합의에 따른 유예 등
- 이런 조치의 **법적 근거와 성격** (규칙인지, 개별 허가인지, 행정적 발표인지)

## 15-3. 사건별 정리 항목
각 사건에 대해 다음을 기록하라.
- 발표일과 시각 (중국 시장 개장 기준으로 event day 0을 정할 수 있도록)
- 법적 효력 발생일
- 법적 근거와 문서 번호
- restriction intensity (섹션 3-4 기준)
- 사전 보도·유출 여부 (사전 정보 반영)
- event contamination과 concurrent news
- likely treated firms
- market expectation
- as-of 상태

정책 목록은 `policy_events_trump2.csv`, event study 평가는 `event_study_candidates.csv`로 저장하라.

## 15-4. Trump 2기의 특징
다음 가설을 간단히 검토하라.

> Trump 2기는 "완전한 차단"보다 license, conditional access, bargaining, policy reversal을 더 많이 사용하고 있는가?

그리고 이 정책변화가 기존 연구의 다음 논점과 연결되는지 검토하라.
- export controls may induce Chinese indigenous innovation
- U.S. suppliers may lose revenue and R&D capacity
- complete denial may accelerate substitution
- partial access may preserve dependence on U.S. technology ecosystem

**단, 정책당국이 특정 학술논문을 보고 정책을 바꿨다는 직접 증거가 없으면 그렇게 주장하지 마라.**

---

# 16. 연구설계 후보 3개

Gate 1–4의 결과를 반영하여 서로 다른 난이도의 연구설계 3개를 제안하라.
- **Design A — 가장 강한 causal identification:** 데이터 요구량이 높더라도 인과식별이 가장 강한 설계
- **Design B — 한 학기 안에 가장 현실적인 설계:** 무료 또는 일반적으로 접근 가능한 데이터 위주
- **Design C — 참신성이 가장 높은 high-risk/high-reward 설계**

각 설계마다 다음을 제시하라.
- research question
- sample
- treatment (Gate 2 결과 반영)
- control (기술과 국가 각각)
- outcome (Gate 4의 primary/secondary 사용)
- regression
- identifying assumption
- main threat
- placebo
- robustness
- inference 방법과 multiple-testing 처리
- MDE 또는 power 평가
- expected contribution
- exact data source
- 예상 데이터 구축 난이도와 소요 기간

---

# 17. Referee-style rejection report

처음 제안한 설계를 옹호하지 말고, 경제학·금융·혁신 분야 상위저널 referee처럼 공격하라. 최소한 다음을 검토하라.
- novelty가 정말 있는가?
- 이미 같은 질문을 한 논문이 있는가?
- **2018-11 ANPRM이 정말 새로운 정보충격인가, 아니면 예상된 사건인가?**
- treatment가 endogenous한가?
- announcement와 actual implementation을 정말 분리할 수 있는가? (부분통제, legal vs China-binding 구분 포함)
- censoring이 selection을 만들지 않는가?
- parallel trends가 설득력 있는가?
- 대조 기술과 비교국가가 정말 untreated인가?
- technology classification이 researcher discretion에 너무 의존하는가?
- outcome이 실제 innovation인지 단순 activity인지?
- primary outcome 선택이 사후적이지 않은가?
- 중국 산업정책(c×k×t 교란)과 구분 가능한가?
- post-treatment controls를 넣고 있지는 않은가?
- 클러스터 수가 적은 상황에서 standard error와 inference가 적절한가?
- multiple testing이 통제되었는가?
- sample size와 statistical power(MDE)는 충분한가?
- external validity가 있는가?

그리고 **Reject / R&R / Accept 가능성**을 솔직하게 평가하라. 그 criticism을 반영해서 최종 research design을 한 번 더 수정하라.

---

# 18. 최종 산출물

## 18-1. 보고서 구성

**Part I. Executive summary** (최대 2페이지)
- 가장 추천하는 research question
- Gate 1–4의 판정 결과와 근거
- identification intuition
- 필요한 데이터
- 가장 큰 위험

**Part II. Literature review**
- 가장 가까운 논문을 중심으로 상세하게
- 검색 프로토콜과 saturation 결과 요약

**Part III. Regulatory and policy timeline**
- 미국 신호 연쇄와 세 층위 기술별 규제 이력 (legal vs China-binding, intensity 포함)
- 중국 정책 timeline과 overlap
- Trump 2기는 별도 절로, 간략하게

**Part IV. Research gap**
- 기존 연구가 무엇을 답했고 무엇을 답하지 못했는지

**Part V. Three candidate empirical designs**
- 3개 비교

**Part VI. Preferred research design**
- 회귀식과 변수 구축까지 상세하게
- outcome별 시점 매핑과 primary outcome freeze 포함

**Part VII. Data acquisition manual**
각 데이터별로 다음을 반드시 포함하라.
- 사이트 이름
- URL
- 가입 필요 여부
- 유료 여부
- 메뉴/path
- API endpoint
- 다운로드 형식
- 필요한 table/fields
- 예상 데이터량
- Python/R로 받을 수 있는지
- 확인 수준

"PATSTAT을 사용하면 된다" 정도로 끝내지 말고, **어떤 계정을 만들고, 어느 페이지에 들어가고, 어떤 dataset/table/field를 받아야 하는지** 수준까지 작성하라. 확인하지 못한 부분은 미확인으로 표시하라.

**Part VIII. Identification threats and robustness**
- 심각도 순으로 정리하라.
- 상세 내용은 섹션 11–12의 산출물을 참조하라.

**Part IX. Referee report**
- 최대한 비판적으로

**Part X. Revised final proposal**
- referee criticism 반영 후 최종 연구계획
- 첫 4주 작업 순서 포함

## 18-2. 별도 파일
- `literature_table.csv`
- `search_log.csv`
- `regulatory_dataset.csv` (세 층위, intensity 포함)
- `china_policy_dataset.csv`
- `gate_2_3_assessment.md`
- `confounders.csv`
- `outcome_freeze.md`
- `policy_events_trump2.csv`
- `event_study_candidates.csv`
- `progress_log.md` (최종 상태)

---

# 19. 연구 태도에 대한 규칙

1. **내가 원하는 결과를 찾아주려고 하지 마라.** 내 아이디어를 살리는 것보다 먼저 깨 보는 것이 우선이다.
2. novelty가 없으면 없다고 말하라.
3. 데이터 확보가 현실적으로 불가능하면 그렇게 말하라.
4. 논문의 결론과 식별전략을 직접 확인하지 않고 abstract만 보고 과장하지 마라. 확인 수준을 항상 표시하라.
5. 정책문서는 반드시 BIS / Federal Register / USTR / White House 등 1차 자료를 우선하라. 중국 정책은 중국 정부 공식 문건을 우선하라.
6. 2018 ANPRM을 actual export-control implementation이라고 부르지 마라.
7. 2018-11 ANPRM을 Gate 2 검증 없이 T=0으로 고정하지 마라.
8. legal control date와 China-binding access restriction date를 혼동하지 마라.
9. tariff와 export control을 동일한 정책으로 취급하지 마라.
10. Trump 1기, Biden기, Trump 2기를 명확히 분리하라.
11. patent application / priority / publication / grant date를 혼동하지 마라.
12. correlation과 causal inference를 구분하라.
13. citation count를 곧바로 기술력이라고 해석하지 마라.
14. Entity List designation의 endogeneity를 항상 고려하라.
15. "China innovation increased"와 "China caught up technologically"를 구분하라.
16. 모든 핵심 사실과 데이터 소스에는 링크 또는 citation을 붙여라.
17. 가능한 경우 DOI, working-paper URL, Federal Register document number, docket number를 제공하라. 확인하지 못한 식별자는 만들어 내지 마라.
18. 문헌이나 정책을 "전부" 찾았다고 주장하지 마라. 검색 프로토콜 기준으로만 완전성을 서술하라.
19. c×k×t 차원의 교란을 fixed effect로 통제되었다고 서술하지 마라.
20. 결과를 본 뒤 treatment 기술, 대조 기술, primary outcome의 정의를 바꾸지 마라. 바꿔야 한다면 사유와 변경 전후 결과를 모두 보고하라.
21. power가 부족하면 causal claim을 과장하지 말고 그렇게 말하라.

---

# 최종 목표

내가 이 연구를 통해 알고 싶은 것은 단순히 "수출통제가 중국의 혁신을 촉진했는가?"가 아니다. 궁극적인 질문은 다음과 같다.

> **미국이 기술접근을 실제로 차단하기도 전에, "앞으로 이 기술을 차단할 수 있다"는 신호 자체가 중국의 자본과 연구역량을 해당 기술로 이동시키는가?**

그리고 만약 그렇다면:

> **기존 연구에서 관찰된 '수출통제 이후 중국 혁신 증가' 중 일부는 실제 공급제약의 결과가 아니라 anticipatory response였던 것은 아닌가?**

이 질문이 기존 문헌과 실제로 차별화되는지, 2018 ANPRM이 정말 정보충격인지, 데이터 구조상 식별이 가능한지를 순서대로 냉정하게 확인한 뒤, 살아남은 범위 안에서 가장 강한 연구설계를 제시하라.
