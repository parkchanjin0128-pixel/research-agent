# Threat Register

## 사용 규칙
- 위협은 삭제하지 않는다. status와 대응만 갱신한다.
- 갱신할 때는 날짜와 근거 파일을 함께 적는다.
- referee는 새 위협을 **추가**할 수 있다. status를 `addressed`로 바꾸는 것은 referee가 다음 심사에서 확인한 뒤에만 가능하다.

## 분류 기준
- **severity**
  - `critical`: 해결하지 못하면 announcement effect 주장이 불가능하다.
  - `major`: 해석이나 크기를 크게 왜곡한다.
  - `minor`: robustness 수준의 문제다.
- **dimension:** 교란이 변하는 차원
  - `c×t`: 국가 × 시점
  - `k×t`: 기술 × 시점
  - `c×k×t`: 국가 × 기술 × 시점
  - `firm`: 기업 단위
  - `design`: 설계 자체의 문제
- **status:** `open` / `in-progress` / `addressed` / `accepted-limitation`

---

| ID | 위협 | severity | dimension | status | 현재 대응 또는 계획 | 출처 |
|---|---|---|---|---|---|---|
| T01 | 2018-11 ANPRM은 단일 정보충격이 아니다 (선행 신호: 2018-01 DIUx 보고서, 2018-04 ZTE, 2018-06 하원 기록, 2018-08 ECRA) | critical | design | in-progress | T=0을 두지 않고 신호 연쇄에 대한 동적 $\beta_\tau$를 추정한다. 시장반응 first stage로 신호 가중치를 정한다 | Gate 2 |
| T02 | untreated 또는 later-signaled 비교 기술이 없다 (47개 전부 2018년 지목) | critical | design | in-progress | 연속 dose $B_k$를 쓴다. strong parallel trends 가정(CGBS 2024)을 명시하고 dose 구간별로 검정한다 | Gate 3 조건 2 |
| T03 | 중국의 기술별 산업정책이 같은 기술에 겹친다 (family 11/14, 하위기술 17/47) | critical | c×k×t | in-progress | (a) CNPolicy_kt 통제, (b) 중국 정책 시점 대비 dose별 꺾임 시점 검정, (c) 중국 정책 미대응 30개 하위기술 표본, (d) 기술 내부 기업 비교 | Gate 3 조건 3 |
| T04 | 추격 수렴: 미국이 지배하는 분야에서 중국은 신호와 무관하게 빨리 성장한다. dose와 상관되어 $\beta$가 기계적으로 양수가 된다 | critical | c×k×t | open | B_k가 비슷한 비지목 기술 placebo를 쓰고, $\beta_{listed}-\beta_{nonlisted}$를 추정한다. 2018년 이전 dose별 pre-trend를 확인한다 | 설계 검토 |
| T05 | 동시기 실제 제한 1: Huawei Entity List (2019-05)와 이후 FDPR. 고dose 분야에 영향이 집중된다 | critical | c×k×t / firm | open | 가장 깨끗한 창(2018-11 ~ 2019-05)을 분리한다. k별 Entity List 기업 특허 비중을 통제한다. 기업 단위 분석에서 EL 기업과 계열사를 제외한다 | 설계 검토 |
| T06 | 동시기 실제 제한 2: ZTE denial order (2018-04 부과, 2018-07 해제) | major | firm / c×k×t | open | 통신·반도체 노출도를 통제한다. 2018년 상반기를 사전 기간에서 제외하는 robustness를 본다 | 설계 검토 |
| T07 | 동시기 무역조치: Section 301 관세 List 1–3 (2018-07 ~ 09), MIC2025 수혜 품목 겨냥 | major | c×k×t | open | 기술 k별 관세 노출도를 HS 매핑으로 측정해 통제한다 | 설계 검토 |
| T08 | 미 법무부 China Initiative (2018-11-01). 논문과 미중 공동연구 outcome을 교란한다 | major | c×k×t | open | 공동연구 outcome은 secondary로 강등한다. 학계 노출도를 통제한다 | 설계 검토 |
| T09 | 科技日报 35개 "卡脖子" 기술 연재 (2018). 중국 측의 동시 신호다 | major | c×k×t | open | 날짜와 목록을 확인한 뒤, 경로(mediator)로 볼지 교란으로 볼지 **사전에** 정하고 두 해석을 모두 보고한다 | 설계 검토 |
| T10 | 비교국가 오염: 전 세계 대상 license requirement 때문에 다른 나라도 반응했을 수 있다 | major | c×k×t | open | 편향 방향을 서술한다(대체로 0 쪽 감쇠). 국가별 위협 강도 가중치를 검토한다 | Gate 3, 3-6 |
| T11 | 수준 효과는 식별되지 않는다 (상대효과만 식별) | major | design | accepted-limitation | charter 3절대로 "강도 0 = 반응 0" 가정을 명시한 back-of-envelope 계산만 한다 | 설계 검토 |
| T12 | 미확인 41행: China-binding restriction 여부를 모른다 | major | design | open | "미통제(확인)"와 "미확인"으로 구분한다. 미통제 가정과 제외 두 경우로 bound를 보고한다 | Gate 3 조건 1 |
| T13 | dose 측정 오차와 crosswalk 재량 (p-hacking 위험) | major | design | open | pipeline을 사전 freeze한다. dose 정의 3종으로 robustness를 본다. similarity threshold 민감도를 보고한다 | 10절 |
| T14 | 클러스터 수 부족과 공통 규칙에 묶인 품목 때문에 유효 cluster 수가 불명확하다 | major | design | open | B_k 재배정 randomization inference, wild cluster bootstrap, 규칙 단위 clustering을 비교한다 | Gate 3 조건 4 |
| T15 | 검정력 부족 | major | design | open | MDE를 사전 계산한다. MDE가 과대하면 descriptive 설계로 전환한다 | 6-4 |
| T16 | censoring이 selection을 만든다 (일찍 통제된 기술이 표본에서 빠짐) | minor | design | open | 8절과 연결해 평가한다. 6행뿐이라 영향은 제한적일 수 있다 | 6-2 |
| T17 | outcome 선택의 사후성과 multiple testing | major | design | open | Gate 4에서 primary outcome을 freeze한다. FDR q-value를 보고한다 | 9-F |
| T18 | 신호의 내생성: 미국의 관심이 중국의 기술 진전에 반응해 높아졌을 수 있다 (역인과) | major | k×t / c×k×t | open | 신호의 **시점**은 ECRA 절차 일정에서 나온다고 보고, 기술 간 차이는 사전 고정된 B_k에서 얻는다. 텍스트 기반 신호 강도 S_kt는 secondary로만 쓴다 | 설계 검토 |
| T19 | Kang et al. (2025 JIMF) 등 가장 가까운 연구가 dose나 의존도를 이미 썼을 가능성 (novelty 위협) | major | design | open | 3회차에서 원문으로 Gate 1을 재확인한다 | 문헌 |
| T20 | NSFC 2019 면상항목 분류신청·분류평가 시범에 F04(반도체)·F05(광학) 포함: 고dose 분야의 2019 선정 결과가 심사제도 변화로 바뀔 수 있음. 공개자료는 선정과제라 선정 시점(2019 여름, Huawei 이후) 오염도 있음 | major | c×k×t | open | F04/F05 별도 처리·제외 사전 규칙; 학과별 신청 건수 통계 확보 여부 확인 | Claude precheck 1 CR3 (2026-10-12) |
| T21 | 가장 깨끗한 창(2018-12~2019-04)이 5개월뿐 → 연 단위 outcome으로 announcement 구간 식별 불가, 검정력 부족 위험 | critical | design | open | 월별 priority date 특허·월별 VC로 MDE 선계산; 포기기준 4 우선 점검 | Claude precheck 1 CR4 (2026-10-12) |
| T22 | Gate 2 근거 C001(2018-06 하원 기록 4/14 family 선행 지목)이 인용 링크로 검증되지 않음 | major | design | open | 실제 페이지 재출처 또는 근거 철회 후 다른 선행 신호로 Gate 2 재진술 | Claude precheck 1 CR1 (2026-10-12) |
