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

- 2026-10-12 | 최신 사용자 지시/운영 변경 | API 및 추가 과금 없이 구독 클라우드 실행을 요청했다. 유료 research-cloud.yml은 GitHub 서버에서 비활성화했고 로컬 예약은 PAUSED를 유지한다. Work 웹 일반 쓰기 d058930 및 예약 쓰기 b59fb69를 원격에서 검증했다. 5시간 웹 예약으로 전환하며 연구질문·Gate·turn은 변경하지 않는다. | docs/CLOUD_SETUP.md; prompts/work_web_scheduled_run.md

- 2026-10-13 | 운영 복구 | 구독 한도 중단 후 남은 Codex 잠금을 웹 실행 종료 확인 후 해제. 최소 작업 단위로 예약을 축소. 연구질문·Gate·정식 리뷰 횟수 불변. | outputs/progress_log.md

- 2026-10-20T09:20:16Z | 직접 사용자 지시/운영 복구 승인 | 사용자가 “이쪽에서 계속 진행이 안되는데 해결해”라고 요청. 2026-10-13 구독 한도 중단 후 잔여 잠금의 사용자 승인 복구를 수행한다. 독립적인 실행 종료 조회는 불가하며 자동 만료로 처리한 것이 아니다. next=codex, round=03, stage=production, lock=none으로 재개 가능 상태를 복원. 미발행 연구·검증은 완료로 인정하지 않으며 필요시 재생산. 연구질문·Gate·예약·권한 불변. | state/turn.md; outputs/progress_log.md
