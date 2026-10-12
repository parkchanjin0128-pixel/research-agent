# Decision Log (append-only)

형식: `날짜 | 종류(Gate 판정 / 사용자 결정 / 제안 / 변경) | 내용 | 근거 파일`

---

- 2026-10-12 | Gate 판정 | **Gate 1 (Novelty): 부분적으로 답변됨.** | outputs/round_01/part4_gap_novelty.md

- 2026-10-12 | Gate 판정 | **Gate 2 (Announcement-date validity): 실패.** 2018-11-19 ANPRM을 단일 T=0으로 쓰는 근거가 부족하다. | outputs/round_02/gate_2_3_assessment.md
  - 2018-06-26 하원 기록에서 AI·로봇·바이오·첨단소재 등 최소 4/14 family가 이미 지목됐다.
  - ECRA가 8월에 먼저 제정됐다.
  - 보도량이 불연속적으로 증가했는지는 확인하지 못했다.

- 2026-10-12 | Gate 판정 | **Gate 3 (Identification feasibility): 기본 DDD 채택 중단.** | outputs/round_02/gate_2_3_assessment.md
  - 조건 1 (clean 기간): 부분 충족
  - 조건 2 (비교 기술): 심각하게 미충족. 47개 하위기술 전부가 2018년에 지목됐다.
  - 조건 3 (중국 정책 분리): 심각하게 미충족. 중국 선행정책과 family 11/14, 하위기술 17/47이 직접 대응한다.
  - 조건 4 (inference): 부분 충족
  - 47개 중 China-binding restriction이 확인된 것은 6행뿐이고 41행은 미확인이다.

- 2026-10-12 | 사용자 결정 | **연구질문을 유지한다.** 질문을 바꾸는 대안(기업 단위 시장반응을 주질문으로 삼는 설계 등)은 채택하지 않는다. | 대화 기록

- 2026-10-12 | 사용자 결정 | **연속 처치(dose) 설계를 3회차 주설계 후보로 검토한다.** 상세는 `prompts/round_03.md`를 따른다. | research_charter.md 4절
  - 위협 강도(B_k) × 신호 연쇄의 동적 경로
  - 비지목 placebo
  - 중국 정책 통제
  - 시장 반응 first stage
  - 기술 내부 메커니즘 검증

- 2026-10-12 | 사용자 결정 | **Announcement effect는 China-binding restriction 이전 구간의 강도별 차등 반응으로 정의한다.** 다음을 반드시 다룬다. | research_charter.md 2–3절
  - 동시기 실제 제한(ZTE, Section 301, Huawei Entity List)의 통제
  - 가장 깨끗한 창(2018-11 ~ 2019-05)의 분리

- 2026-10-12T10:06:00+09:00 | 사용자 지시 반영/설정 | 이 대화에서 Claude와 Codex 공동 연구 시스템 설정을 요청했다. 기존 교대 프로토콜을 사용하고 1·2회차 산출물을 이관했다. 3회차 조사 메모는 미완료이며 Gate 채택·freeze는 하지 않았다. | docs/OPERATIONS.md; state/import_manifest.json

- 2026-10-12 | 사용자 지시/구성 변경 | PC가 꺼져 있어도 자동 실행되도록 GitHub 설정을 요청함. 로컬 예약을 일시정지하고 GitHub 호스팅 연구 워크플로를 구성. OPENAI_API_KEY와 비용 활성화는 아직 없어 모델 호출 비활성. Gate/설계 승인과 무관한 실행 환경 변경이다. | docs/CLOUD_SETUP.md

- 2026-10-12 | 심사(사전점검) | Claude 교차 모델 사전점검 1: major 4(CR1 C001 재출처, CR2 novelty 근거 조정, CR3 NSFC 2019 F04/F05·선정 오염, CR4 5개월 창 검정력), minor 3. 운영 blocker 없음. 정식 회차 심사 아님(reviews_this_round 불변). | outputs/reviews/round_03_claude_precheck_1.md
