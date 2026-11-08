# 비활성 로컬 실행 지침 — Codex 내부 심사 호환

현재 활성 실행 방식은 prompts/work_web_scheduled_run.md의 구독 Work 웹 클라우드다. 로컬 예약은 PAUSED로 유지한다. 이 파일을 읽었다는 이유로 로컬 예약을 만들거나 재개하지 않는다. 아래는 사용자가 로컬 실행을 명시적으로 선택한 경우의 호환 지침이다.

1. docs/OPERATIONS.md를 읽고 scripts/claim_turn.py --actor codex로 최신 main·차례·잠금을 확인한다. skipped면 파일 변경 없이 종료하고 error면 연구를 시작하지 않는다. force-push/reset/임의 rebase·인증정보 출력은 금지한다.
2. 점유 성공 후 AGENTS.md 시작 파일, state/user_inbox.md, 현재 prompts/round_XX.md, state/work_queue.json, docs/INTERNAL_REVIEW.md를 읽는다. 미심사 재개 메모를 검증 사실로 올리지 않는다. 최신 직접 사용자 지시도 유효하다.
3. 약8분의 작은 단위를 목표로 queue의 준비된 production/verification/review/revision을 공정하게 이어간다. 특정 critical 감사에 의존하지 않는 문헌·설계·MDE 계획을 계속한다. producer/verifier/referee는 다른 실제 agent ID로 배정한다. verifier/referee는 fork_turns="none"으로 생성하고 파일 경로·상태만 제공한다. 모델/effort는 구독 내 상위 설정을 상속한다.
4. 역할별 쓰기 경로를 분리하고 CSV를 동시 수정하지 않는다. 같은 unit의 전체 judgment history에서 검증·심사 ID와 보고서 경로/해시를 재사용하지 않는다(writer ID 재사용은 가능). 새 사실은 1차 자료로 독립 검증하고 report/receipt/현재 해시를 남긴다. review/revision receipt에는 response_path·response_sha256이 필수이며 response 파일에는 docs/INTERNAL_REVIEW.md의 JSON 계약에 따라 현 리뷰의 모든 finding ID를 정확히 대응시킨다. 작성자는 해당 verifier/referee와 다른 실제 orchestrator/producer다. 계획 response는 해결 판정이 아니며 revision마다 새 파일로 이력을 보존한다. 내부 리뷰·response를 보존하고 같은 심사 범위의 수정은 최대2회다. CR1–CR4, 과거 검증과 미확인 범위를 보존한다.
5. 허용된 현재 회차 outputs, reviews, progress_log, turn/queue/claims/threat/decision만 갱신한다. charter·과거 회차 원본·user_inbox·workflow·비밀정보·PDF 전문을 수정/게시하지 않는다. 유료 호출·추가 결제·배분 outcome 열람·불가역 freeze를 수행하지 않는다.
6. 명시된 파일만 저장하고 발행 전 최신 원격 상태와 자기 run_id를 확인한다. 충돌을 강제 덮어쓰지 않는다. 산출물·진행 로그·queue·turn을 함께 checkpoint하고 원격 SHA/내용을 재조회한다. 부분 작업은 next=codex, lock=none으로 두고 실제 다음 phase/active_unit을 기록한다. Claude 인계는 하지 않는다.
7. 새 Gate·질문 변경·freeze 또는 두 번 수정해도 남은 지적은 구체적 검증·리뷰 결과를 마련한 뒤 next=user, stage=decision으로 올린다. minor_revision도 수정 대기이며 완료는 verified(새 사실이 없을 때만 근거 있는 N/A)+referee accept+모든 finding resolved일 때만 가능하다. 기존 Gate2·3 실패·질문 유지·dose 검토·Codex 단독 전환은 재승인 대상이 아니다.
8. 자동 승인 거절이나 쓰기 실패를 숨기거나 우회하지 않는다. 거절 동작·사유·미발행 산출물 보존 위치를 보고한다. 변경 없는 차례 확인은 조용히 끝내고 새 장애·사용자 결정·회차 완료만 알린다. 독립 검증·전체 리뷰와 모든 필수 산출물 확인 전에는 회차 완료를 선언하지 않는다.
