# Round 03 — 주설계 검증: 위협 강도(dose) 설계

## 전제
- Gate 2와 Gate 3는 실패로 판정됐다. 연구질문은 유지한다 (`state/decision_log.md`).
- 이번 회차의 목적은 `research_charter.md` 4절의 dose 설계가 **질문을 바꾸지 않고 announcement effect를 식별할 수 있는지**를 검증하고, 가능하면 설계를 확정 직전 단계까지 만드는 것이다.
- 기본 DDD를 전제하지 마라.

## 작업 분배와 순서

### A. 병렬 작업 1 (생산)

**A1. `policy_archivist`: 2회차 보완**
- 미확인 41행을 "미통제(확인)"와 "미확인"으로 구분하고, 판정 근거(검토한 ECCN·규칙)를 기록하라.
- `regulatory_dataset.csv`를 갱신하고, "지목됐으나 미통제" 집단의 규모를 보고하라.
- 동시기 실제 제한과 무역조치를 정리해 `concurrent_events.csv`로 저장하라.
  - ZTE denial order와 해제
  - Section 301 관세 List 1–3
  - Huawei Entity List와 FDPR
  - China Initiative
  - 科技日报 35개 卡脖子 연재: 날짜와 기술 목록 포함
- DIUx 보고서(2018-01)부터 2018-11 ANPRM까지의 신호 연쇄를 날짜·출처와 함께 갱신하라.

**A2. `lit_scout`: Gate 1 재확인과 선례 확인**
- dose 설계 기준으로 novelty를 재판정하라. 가장 가까운 연구의 원문에서 다음을 확인하라.
  - Kang, Ma, Xie & Zhong (2025, JIMF, "Innovation's false spring")
  - Shen et al. (2024, IRFA)
  - Liu, Ruan & Zheng (2025 WP)
  - He & Lyu (2025, Research Policy)
  - 확인 항목: treatment 정의, 날짜, 기술 의존도·노출도 사용 여부, 비교집단
- 선례 논문의 식별 구조를 원문으로 확인하고, 본 연구와의 대응 관계를 표로 정리하라.
  - Pierce & Schott (2016 AER)
  - Handley & Limão (2017 AER)
  - Blume-Kohout & Sood (2013 JPubE)
  - Moser & Voena (2012 AER)
  - Finkelstein (2004 QJE)
  - Malani & Reif (2015 JPubE)
  - Callaway, Goodman-Bacon & Sant'Anna (2024, continuous DiD)

### B. 설계 (A1·A2 결과를 받은 뒤)

**`identification_designer`: 주설계 작성**

1. **Dose B_k 정의:** 미국이 기술 k를 실제로 통제했을 때 중국의 잠재적 손실. 2013–2017 기준으로 사전 고정한다.
   - 후보 3종:
     - (i) 중국 출원인 특허 backward citation 중 미국 출원인 비중
     - (ii) k 분야 IP5 패밀리 중 미국 비중
     - (iii) 하드웨어는 HS 매핑 기준 대미 수입 의존도
   - ECRA 50 U.S.C. 4817(a)(2)(B)의 고려요소를 dose의 제도적 근거로 검토하라. 근거 사실은 C003으로, verifier 확인이 필요하다.
2. **식:**

   $Y_{ckt} = \alpha_{ck} + \delta_{ct} + \lambda_{kt} + \sum_\tau \beta_\tau (China_c \times B_k \times 1[t=\tau]) + \gamma (China_c \times CNPolicy_{kt}) + \text{동시기 사건 노출도 통제} + \epsilon$

   - 단일 T=0을 두지 마라. 신호 연쇄 중 어디서 꺾이는지를 추정하는 구조로 설계하라.
   - 첫 신호 이후의 변화는 anticipation으로 해석한다.
3. **Announcement effect 식별 조건**
   - $\beta_\tau$를 China-binding restriction 이전 구간과 이후 구간으로 분해하는 식을 작성하라.
   - 이 설계가 식별하는 것은 **강도별 차등 announcement effect**다. 수준 효과는 "강도 0 = 반응 0" 외삽 가정 하에서만 계산 가능함을 명시하라.
   - 가장 깨끗한 창(2018-11 ~ 2019-05 Huawei 지정 전)을 정의하고, 이 창을 관측할 수 있는 outcome을 평가하라.
   - 특히 NSFC 2019년도 신청 마감일이 이 창에 들어가는지 확인하라 (C011).
   - 기업 단위 분석에서 Entity List 기업과 계열사를 제외하는 사전 규칙을 정하라.
4. **추격 수렴 (T04):** B_k가 비슷한 비지목 기술 placebo의 사전 정의 규칙을 만들어라. crosswalk와 같은 pipeline을 쓰고, $\beta_{listed}-\beta_{nonlisted}$를 추정 대상으로 하는 식을 작성하라.
5. **중국 정책 (T03, T09):**
   - (a) CNPolicy_kt 통제
   - (b) 중국 정책 시점 대비 dose별 꺾임 시점 검정
   - (c) 중국 정책 미대응 하위기술 표본
   - (d) 卡脖子 연재를 경로로 볼지 교란으로 볼지 사전 규칙
6. **보강 설계**
   - (a) 신호 날짜별 중국 상장기업 초과수익률을 B_k로 정렬한 event study로 신호의 정보량을 측정한다. 그 가중치를 배분 outcome을 보기 전에 고정하는 절차를 설계하라.
   - (b) 중국만 표본으로, 같은 기술 안에서 사전 미국 의존도 차이를 이용하는 메커니즘 검증을 설계하라.
7. **기존 연구 재분해:** Kang et al. 등의 "2018 이후 증가" 추정치 중 실제 제한 이전 구간에서 나타난 비중을 재분해할 수 있는지 평가하라.
8. **나머지 3회차 작업**
   - 시점 매핑
   - inference: B_k 재배정 randomization inference, wild cluster bootstrap
   - MDE 계획
   - confounder 표
   - 반론 7개
9. **포기 기준 (사전 명시).** 다음 중 하나라도 해당하면 descriptive 설계로 전환한다.
   - B_k의 기술 간 변동이 부족하거나 crosswalk가 실패한다.
   - 2018년 이전 dose별 pre-trend가 비지목 placebo로 제거되지 않는다.
   - 지목 기술 안에서 B_k와 중국 정책 포괄 범위의 상관이 통제 후에도 강하다.
   - MDE가 현실적인 효과 크기보다 크다.
   - 동시기 실제 제한(T05)을 깨끗한 창으로도 분리할 수 없다.

### C. 실현 가능성 점검

**`data_engineer`**
- dose 후보 (i)과 (ii)를 Google Patents BigQuery로 측정할 수 있는지 **dry run**으로 확인하라. 스캔량과 비용을 보고하라.
- outcome 데이터는 집계하지 마라.

### D. 검증과 심사
1. `verifier`: A·B·C에 새로 등장한 사실을 전부 검증하라. 우선순위는 다음과 같다.
   - C001(6월 하원 기록)
   - C003(ECRA 조문)
   - C006–C011(동시기 사건 날짜)
2. `referee`: 주설계를 심사하라. 특히 다음 질문에 답하라.
   - (i) 이 설계가 정말 announcement effect를 식별하는가, 아니면 위협 강도와 상관된 다른 무언가를 식별하는가?
   - (ii) 추격 수렴과 Huawei 효과를 실제로 분리하는가?
3. 수정 왕복은 최대 2회. 남은 blocker는 사용자에게 escalate한다.

## 저장할 산출물 (`outputs/round_03/`)
- `plan.md`
- `regulatory_dataset.csv` (갱신본)
- `concurrent_events.csv`
- `signal_chain.csv`
- `novelty_recheck.md`
- `precedents_table.md`
- `main_design.md`: 식, 식별 변동 분해, 위협 대응표, 포기 기준
- `confounders.csv`
- `threats_tests.md`
- `data_tests/`
- `verification_report.md`
- `../reviews/round_03_review_*.md`

## 완료 기준
- Gate 1 재판정과 근거
- 주설계의 식, announcement/implementation 분해, 위협 대응표 (T01–T19 전부)
- 포기 기준 5개를 사전 명시
- verifier 보고서와 referee 리뷰 각 1회 이상
- 사용자 결정 사항 목록 (선택지와 추천 근거 포함)
