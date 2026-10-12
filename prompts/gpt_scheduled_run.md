# Codex 예약 실행 지시문

현재 대화에 연결된 로컬 연구 예약이다. 대상은 parkchanjin0128-pixel/research-agent 저장소다.

1. 로컬 checkout에서 docs/OPERATIONS.md와 scripts/claim_turn.py를 읽고 `python scripts/claim_turn.py --actor codex`를 실행한다. 최신 main을 가져오고 차례/잠금을 확인하는 단계다. skipped면 아무 파일도 수정하지 않고 종료한다. error면 연구를 시작하지 말고 오류를 보고한다. force-push, reset, 임의 rebase, 인증 정보 출력은 금지한다.
2. 점유 성공 시 AGENTS.md의 시작 파일, state/user_inbox.md, 현재 prompts/round_XX.md를 읽는다. round_03 시작이면 outputs/round_03/resume_notes.md와 .local/source_paths.json을 참고하되 메모를 검증된 사실로 승격하지 않는다. 사용자 최신 직접 지시가 로컬 문서보다 우선한다.
3. AGENTS.md의 역할별 독립 생산·검증·referee 순서를 수행한다. .codex/agents의 모델/역할 지시는 실제 subagent 생성 시 명시한다. verifier/referee는 작성자와 다른 에이전트이며 추론 이력을 전달하지 않는다. 역할별 쓰기 경로를 나누고 같은 CSV를 동시에 수정하지 않는다.
4. 원본 outputs/round_01, round_02는 보존하고 현재 회차 폴더에 갱신본을 쓴다. 미확인은 빈칸/미확인으로 남긴다. 자료 접근 실패를 무통제 확인으로 바꾸지 않는다. 유료 호출, 대량 스캔, 배분 outcome 열람 또는 사전 freeze 확정은 승인 범위 밖이다.
5. 한 번의 실행에서 한 회차 또는 기록 가능한 작은 작업 묶음만 수행한다. 45분 내 checkpoint를 목표로 한다. 남으면 next: codex로 유지하고 lock: none으로 해제해 이어받을 수 있게 한다. 변경 파일을 명시해서 stage하고 진행 로그/lock_since를 갱신하여 커밋·push한다. push 직전 원격 상태를 확인하고 충돌 시 강제 덮어쓰지 않는다. .local, PDF 원문, 비밀정보를 commit하지 않는다.
6. 현재 회차 산출물·독립 검증·내부 referee가 갖추어지면 next: claude, stage: claude_review, lock: none으로 넘긴다. 수정 재심도 최대 2회다. Gate 채택·질문 변경·불가역 freeze 등 실제 사용자 결정이 필요하면 구체적인 보고서를 만든 뒤 next: user로 멈춘다. 이미 승인된 Gate 2·3 실패와 dose 검토는 재승인 대상이 아니다. 결정 전 조사·검증을 중단할 이유로 사용하지 않는다.
7. outputs/progress_log.md와 state/turn.md를 함께 갱신한다. 다음 회차 진행 허용 여부와 미완료 항목을 정확히 기록한다. 변경 없는 차례 확인은 조용히 종료하며 새 blocker/사용자 결정 필요/회차 완료만 보고한다.
