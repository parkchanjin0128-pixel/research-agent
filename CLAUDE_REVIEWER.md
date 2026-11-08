# Claude 연구 역할 종료 — 2026-11-02

사용자가 Claude의 다른 작업과 구독 사용량을 위해 이 연구의 Claude 참여를 종료했다. 이 파일은 **retired 안내**이며 Claude에게 실행·검증·심사·저장 권한이나 예약 지시를 부여하지 않는다. 이 프로젝트는 Codex가 별도 생산자·verifier·referee를 생성해 수행한다. 현재 규칙은 [AGENTS.md](AGENTS.md)와 [docs/INTERNAL_REVIEW.md](docs/INTERNAL_REVIEW.md)다.

과거 Claude 리뷰·response·claims ledger의 출처와 `verified_by=claude` 이력은 보존한다. `outputs/reviews/round_03_claude_precheck_1.md`는 당시 사용자 요청으로 작성된 사전점검이며 정식 내부 리뷰 횟수에 포함하지 않는다. 다음 미해결 지적은 내부 queue와 referee가 계속 추적한다.

| 역사 ID | 이관할 문제 |
|---|---|
| CR1 | C001 하원 신호의 원문 재출처·인용 범위 |
| CR2 | 가장 가까운 연구와 novelty의 원문 비교 |
| CR3 | NSFC 2019 F04/F05 제도 변화·선정 시점의 오염 |
| CR4 | 실제 제한 이전 짧은 창의 빈도·검정력 |

이를 종료·해결된 이슈로 바꾸지 않는다. 새 정식 리뷰는 `round_XX_internal_review_N.md`로 구분하고 실제 별도 심사를 수행한 뒤에만 카운트를 늘린다. 과거 절차는 Git 이력에서 확인할 수 있다. Claude의 다른 프로젝트·예약·설정은 변경하지 않는다.
