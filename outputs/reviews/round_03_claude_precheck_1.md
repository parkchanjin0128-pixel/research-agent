# Round 03 — Claude 교차 모델 사전점검 1

- 작성: Claude (claude-opus-5-5), 2026-10-12 KST
- 계기: 사용자 직접 요청 ("코덱스가 진행한 부분까지 검토"). AGENTS.md 11절에 근거한다.
- **정식 회차 심사가 아니다.** `reviews_this_round`를 올리지 않고, `turn.md`도 바꾸지 않는다.
- 범위
  - 1·2회차 이관본: `part4_gap_novelty.md`, `gate_2_3_assessment.md`, `regulatory_coding_rules.md`, `progress_log.md`
  - 3회차 인계 메모: `outputs/round_03/resume_notes.md`
  - 운영 변경: workflow, `cloud_control.py`, AGENTS.md 11–12절, `turn.md` 규칙
- 3회차 주설계 문서(`main_design.md`)는 아직 없으므로 설계 자체는 심사하지 않았다.

## 판정

**Major revision 수준의 지적 4건.** 운영 구조에는 blocker가 없다.

1·2회차 작업의 원문 대조와 미확인 처리 방식은 우수하다. 미확인을 0으로 쓰지 않았고, family 전체에 단일 날짜를 복사하지 않았으며, 2019-05 관세 인상을 고려해 창을 좁혔다.

문제는 세 가지다.
1. Gate 2의 핵심 근거 하나가 인용 링크로 검증되지 않는다.
2. dose 설계의 novelty 근거가 인계 메모의 Kang et al. 발견으로 약해졌다.
3. 가장 깨끗한 창이 5개월로 줄면서 사용 가능한 outcome과 검정력이 크게 제약된다.

## 지적

| ID | severity | 위치 | 문제 | 해결책 |
|---|---|---|---|---|
| CR1 | major | `gate_2_3_assessment.md` Gate 2 표 1행, claims C001 | 아래 "CR1 상세" 참조 | 해당 문단이 있는 실제 granule·페이지를 찾아 원문을 인용하라. 찾지 못하면 C001을 근거에서 내리고, Gate 2는 다른 근거(ECRA 조문 자체, FIRRMA 2017, DIUx 2018-01 보고서의 실제 내용)로 재진술하라. Gate 2 결론이 바뀔 가능성은 낮지만, "4/14 family 선행 지목"이라는 정량 표현은 현재 근거가 없다. |
| CR2 | major | `resume_notes.md` Kang et al. 항목, threat T19 | 아래 "CR2 상세" 참조 | novelty 주장을 "제한 전 구간의 월 단위 분해 + 비특허 연구·자본 outcome + 신호 연쇄 시점"으로 한정하라. dose는 식별 도구일 뿐 기여로 쓰지 마라. Kang et al. 표본을 2019년 이전 월별 priority date로 재분해할 수 있는지(`part4` 4절 우선순위 1)가 이 연구의 차별점을 직접 보여주는 핵심 작업이다. |
| CR3 | major | `resume_notes.md` 창 정의, NSFC | 아래 "CR3 상세" 참조 | (a) NSFC는 "신청 단계 반응"과 "선정 단계"를 분리할 수 없다는 한계를 명시하라. (b) F04/F05를 별도 처리하거나 제외하는 사전 규칙을 정하라. (c) 신청 건수 통계(학부·학과별 신청 수)가 공개되는지 확인하라. NSFC 연차보고에 학과별 신청·자금 건수가 있을 가능성이 있다(미확인). 공개된다면 선정 오염 없이 신청 반응을 볼 수 있다. |
| CR4 | major | 3회차 설계 전반 | 5개월 창에 하위기술 47개 수준의 단위로는 MDE가 클 가능성이 높다. 창 밖의 2019-05 이후 구간은 Huawei와 관세 인상으로 오염된다. | 설계 전에 월별 priority date 특허, 월별 VC 각각의 MDE 시나리오를 계산하라. 포기 기준 4(MDE 과대)를 가장 먼저 점검할 항목으로 올려라. |
| CR5 | minor | 41행 재분류 | 전체 2018–2026 상태 감사는 큰 작업이고, 가장 깨끗한 창 estimand에는 필요 없다. | 1차 작업을 "2018-11-19 ~ 2019-04-30 사이 China-binding restriction이 생긴 하위기술이 있는가"로 좁혀라. 이 기간의 EAR 개정 FR 문서는 수가 적다. 전체 상태 감사는 implementation·persistence 분석용 2차 작업으로 미뤄라. |
| CR6 | minor | charter 4절 표현 (사용자 결정 사항) | 인계 메모의 CGBS·RI 지적에 동의한다. $B_k$는 처치량이라기보다 위협 노출에 따른 효과 이질성(effect modifier)에 가깝다. 사전 배정 메커니즘이 없으므로 $B_k$ 재배정 RI는 진단적 placebo이고, 정확한 randomization p-value가 아니다. | 설계 문서에서 "dose"를 "threat-exposure heterogeneity"로 서술하라. 기울기를 인과 dose-response로 읽으려면 strong parallel trends가 필요하다고 명시하라. charter 문구 변경은 사용자 결정 사항이므로 **제안**으로만 남긴다. |
| CR7 | minor | 운영 | AGENTS.md, `decision_log.md`, `progress_log.md`에 CRLF와 LF 줄바꿈이 섞여 있다. 그래서 diff가 파일 전체 변경처럼 보이고, append-only 감사가 어렵다. | `.gitattributes`에 `* text=auto eol=lf`를 추가하라. |

### CR1 상세
- C001의 링크(`CREC-2018-06-26-pt1-PgH5674-4`)는 H.R. 5841의 **법안 본문** granule이다.
- Claude가 WebFetch로 확인한 범위(H5674–H5686)에는 "artificial intelligence", "robotics", "biotechnology", "advanced materials", "quantum"이라는 문자열이 없다. 발언자가 표시된 floor speech도 없다.
- 주장이 인용한 H5691은 이 granule 범위 밖으로 보인다.
- 따라서 **반증된 것은 아니지만, 인용 링크로는 검증할 수 없다.**

### CR2 상세
- 인계 메모에 따르면 Kang et al. §4.1의 treatment는 다음과 같다.
  - 2013–17 기간 14개 기술 관련 특허 비율이 상위 사분위(15.46%)인 집단을 처치, 비율 0인 집단을 대조로 둔다.
  - post 기간은 2019–22다.
- 또 §4.3은 1998–2017 중미 특허 stock 기준 상대적 기술역량으로 이질성을 이미 분석했다.
- 따라서 "미국 대비 위치·의존도에 따른 이질성"은 새롭지 않다.
- 반대로 차별점도 이 메모로 더 분명해졌다. Kang et al.은 2019–22를 통합하고 연 단위로 본다. 그래서 2019-05 이전 반응을 분리할 수 없다.

### CR3 상세
- 가장 깨끗한 창은 2018-12 ~ 2019-04로 좁혀졌다.
- 연 단위 outcome으로 이 창을 볼 수 있는 것은 NSFC 2019 신청뿐이다.
  - Claude 독립 확인: 신청 접수는 2019-03-01 ~ 03-20 16시 (MOST 전재 공고).
- 그러나 공개 자료는 **선정 과제**다. 선정은 2019년 여름, 즉 Huawei 지정 이후에 이루어진다.
- 같은 공고에 2019 면상항목의 분류 신청·분류 평가 시범 학과로 **F04(반도체 과학과 정보소자)와 F05(광학과 광전자학)**가 지정되어 있다.
  - 이 두 학과는 고dose 기술(microprocessor, 반도체)과 정확히 겹친다.
  - 2019년 이 분야의 선정 건수와 구성은 신호와 무관한 심사제도 변화로도 달라질 수 있다.

## 검증 결과 (claims ledger 반영)

| claim | 판정 | 내용 |
|---|---|---|
| C001 | unverifiable (cited link) | 위 CR1 |
| C011 | verified | 2019 NSFC 집중 접수 2019-03-01 ~ 03-20 16:00. 같은 공고에 F04·F05 분류 신청·평가 시범이 있음. https://fuwu.most.gov.cn/html/tztg/kjjhyjf/20181205/2960.html |

## 운영 점검 (blocker 없음)

- `research-cloud.yml`의 트리거는 cron과 `workflow_dispatch`뿐이다. public repo에서도 외부인이 API 키를 소모시킬 경로가 없다. `issue_comment`와 `pull_request_target` 트리거는 앞으로도 추가하지 마라.
- `cloud_control.py` publish allowlist는 다음으로 제한된다. 범위가 적절하다.
  - 현재 회차 outputs
  - `outputs/reviews/`
  - `outputs/progress_log.md`
  - `claims_ledger.csv`, `threat_register.md`, `decision_log.md`
- 시간만으로 오래된 lock을 덮어쓰지 않게 바꾼 규칙에 동의한다.
- **현재 상태:** `next: codex`인데 모델 호출은 비활성(API 키 없음)이고 로컬 예약은 일시정지됐다. 사용자가 실행 경로를 정하기 전까지 연구 루프는 멈춰 있다.

## Pre-mortem (지금 상태로 진행할 경우의 리젝 사유 3개)

1. "Announcement 효과라고 주장하지만 깨끗한 창이 5개월뿐이고, 그 창의 outcome은 대부분 연 단위다. 사실상 2019–22 통합 효과(Kang et al.와 동일)를 다른 방식으로 서술한 것이다."
2. "NSFC 2019 결과는 F04/F05 심사제도 개편과 Huawei 이후의 선정 결정으로 오염되어 있다."
3. "위협 강도 이질성은 Kang et al. §4.3에 이미 있다. 남은 기여가 불분명하다."
