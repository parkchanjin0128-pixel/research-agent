# 수출통제 신호 연구 — Codex 단독 연구·독립 심사

2026-11-02 사용자 지시에 따라 Claude 인계를 종료한다. **Codex orchestrator → 역할별 생산자 → 별도 독립 verifier → 새 referee → 수정(최대 2회) → 사용자 결정**으로 진행한다. 연구질문과 3회차 dose 설계 검토 범위는 그대로다.

실행 방식은 API 키·추가 과금 없는 **Work 웹 클라우드 5시간 예약**이다. PC가 켜져 있을 필요는 없다. 구독 사용량 제한은 적용된다. 유료 Actions는 비활성, 로컬 예약은 일시정지를 유지한다. 파일 변경만으로 실제 예약이 갱신됐다고 간주하지 않는다. 실제 실행·잠금·checkpoint는 원격 기록과 예약 UI에서 확인한다.

## 시작 경로

| 파일 | 용도 |
|---|---|
| [AGENTS.md](AGENTS.md) | 모든 역할의 권한·독립성·완료·결정 규칙 |
| [docs/INTERNAL_REVIEW.md](docs/INTERNAL_REVIEW.md) | fresh agent 검증·심사·response 프로토콜 |
| [docs/OPERATIONS.md](docs/OPERATIONS.md) | phase queue, 잠금, 저장·복구 |
| [docs/CLOUD_SETUP.md](docs/CLOUD_SETUP.md) | 구독 클라우드 설정과 실제 검증 범위 |
| [prompts/work_web_scheduled_run.md](prompts/work_web_scheduled_run.md) | 현재 예약이 매 실행 읽는 지시문 |
| [state/turn.md](state/turn.md), [state/work_queue.json](state/work_queue.json) | 실시간 차례·진행 단계·전체 작업 coverage |
| [prompts/round_03.md](prompts/round_03.md) | 3회차 과학적 요구사항과 필수 산출물 |
| [state/research_charter.md](state/research_charter.md) | 사용자가 결정하는 연구질문·주장 범위 |
| [state/claims_ledger.csv](state/claims_ledger.csv), [state/threat_register.md](state/threat_register.md) | 사실의 검증 범위·미해결 식별 위협 |
| [outputs/progress_log.md](outputs/progress_log.md) | 실제 완료·중단·다음 단위 |

1·2회차 이관과 웹 쓰기 테스트는 이미 수행한 과거 기록이다. 다시 업로드하거나 연구 시작을 재승인할 필요가 없다. 3회차는 진행 중이며, 일부 규제 사실 검증을 전체 회차 완료로 해석하지 않는다.

## 진행 방식

한 실행은 약 8분 안에 저장할 수 있는 작은 단위를 맡는다. queue의 생산·검증·심사·수정을 이어가며, 미완료 규제 감사와 독립적인 문헌·설계·MDE 계획도 진행한다. 미검증 주장과 unresolved blocker는 그대로 보존한다.

verifier/referee는 작성자와 다른 ID의 새 에이전트이며, 작성자 대화 없이 파일 경로와 상태만 받는다. 모델은 현재 구독의 상위 설정을 상속한다. 별도 에이전트가 불가능하면 독립 심사를 완료했다고 쓰지 않는다. 같은 모델 계열의 합의는 증거가 아니며 원문·추적 가능한 검증이 필요하다.

새 Gate 채택, 질문 변경, 불가역 freeze는 구체적인 산출물·검증·심사 결과를 갖춘 뒤 사용자에게 올린다. 이미 승인된 Gate 2·3 실패와 dose 후보 검토는 계속 수행한다.

## 역사 기록

[CLAUDE_REVIEWER.md](CLAUDE_REVIEWER.md)는 retired 안내다. 기존 Claude precheck와 CR1–CR4, 과거 검증 provenance는 보존하되 Claude 대기나 예약을 전제로 하지 않는다. 다른 Claude 작업은 이 프로젝트의 권한 범위 밖이다.

회차 완료는 필수 산출물·독립 검증·정식 리뷰·response를 확인해야 한다. 원격 쓰기 성공, 내부 합의, 단위 검증만으로는 완료나 Gate 통과를 선언할 수 없다.
