# 연구 생산 실행 — 지금 수행

이 메시지는 이미 생성된 예약이 호출한 이번 1회 실행의 작업 지시다. 예약 생성·갱신·설정 확인 요청이 아니다. 지금 아래 1단계부터 GitHub를 읽고 조건이 맞으면 실제 연구와 커밋을 수행하라. 과거 연결 테스트에 한정했던 '연구하지 말라/파일 하나만 생성' 지시는 종료되었다. 이번 실행에는 아래 범위의 연구 및 상태 갱신이 승인되어 있다. 예약 확인만 하고 끝내지 말고 실제 차례를 검사하라.

GitHub 플러그인으로 parkchanjin0128-pixel/research-agent의 최신 main을 읽고 Codex 생산 역할을 이어간다. PC의 로컬 폴더에 의존하지 않는다. OpenAI API 키, 유료 API, 추가 크레딧 구매, GitHub 유료 연구 workflow 실행은 사용하지 않는다. 구독 한도에 도달하면 멈추고 알린다.

1. main HEAD H를 먼저 기록한 뒤 정확히 그 immutable commit H에서 state/turn.md를 읽는다. next가 codex가 아니면 변경 없이 조용히 종료한다. 잠금이 있으면 해당 run_id와 실행 링크의 실제 실행 상태를 확인한다. 진행 중이면 쓰기 없이 종료한다. 종료가 확인되지 않거나 중단된 잠금이면 복구 필요를 알리고 임의 해제하지 않는다. 시간 경과만으로 잠금을 해제하지 않는다.
2. 잠금이 없으면 고유 run_id와 확인 가능한 예약 실행/대화 링크를 기록한다. turn의 lock=codex, lock_since, run_id를 변경하고 H를 parent로 한 커밋을 만든다. update_ref의 expected_sha=H 또는 동등한 원격 조건부 갱신으로 점유한다. 충돌하면 기존 스냅샷을 버리고 1단계부터 다시 읽는다. 이 기능이 없으면 안전한 점유가 불가능하다고 보고하고 작업을 시작하지 않는다. 강제 push는 금지한다.
3. AGENTS.md, state/research_charter.md, state/decision_log.md, state/threat_register.md, state/claims_ledger.csv, outputs/progress_log.md, state/user_inbox.md와 해당 prompts/round_XX.md를 읽는다. round 03은 outputs/round_03/resume_notes.md, sources_manifest.json, outputs/reviews/round_03_claude_precheck_1.md도 읽는다. 메모는 검증된 근거가 아니다. 최신 직접 사용자 지시가 우선한다.
4. 기존 Gate 2·3 실패 수용, 연구질문 유지, dose 설계 후보 검토는 이미 승인되었다. 규제 미통제 확인/미확인 분리부터 연속 처치 식별, 원문 검증, placebo, 중국 정책, announcement effect 전후 구간, 실제 제한, MDE 및 포기 기준까지 prompts/round_03.md의 요구를 수행한다. 설계 채택이나 불가역 freeze는 구체적인 결과를 마련한 뒤 사용자에게 넘긴다.
5. AGENTS.md에 따라 생산·독립 verifier·referee를 별도 에이전트로 수행한다. 도구가 지원하지 않으면 독립 검증 완료로 표시하지 않는다. 작성자의 추론을 검증자에게 전달하지 않는다. 자료가 없으면 필요한 원문 목록과 접근 실패를 기록한다. PC Downloads 파일을 볼 수 있다고 가정하지 않고 공개 저장소에 논문 전문을 올리지 않는다.
6. 한 실행에서 45분 이내의 작은 작업 묶음을 목표로 하되 작은 단위 완료마다 원격 checkpoint를 만든다. outputs의 현재 회차, 진행 로그, 허용된 상태 파일만 변경한다. 기존 round_01/02 원본, charter, user_inbox, workflow, 비밀정보는 수정하지 않는다. 다중 파일은 하나의 tree/commit으로 구성한다. 발행 직전 최신 HEAD P를 읽고 P에 고정해 자신의 run_id/lock과 변경 대상 파일을 재확인한 뒤 parent=P, expected_sha=P로 조건부 갱신한다. 충돌 시 강제로 덮어쓰지 않는다. 미발행 산출물·base SHA·run_id는 recovery/work-<run_id> 새 브랜치에 보존하고 실제 ref를 조회해 확인한다. 그것도 불가능하면 대화의 다운로드 가능한 파일로 보존하고 링크를 보고한다. 영속 저장이 확인되지 않으면 저장 완료라고 하지 않는다.
7. 부분 작업이면 next=codex, lock=none으로 해제한다. 산출물·독립 검증·내부 referee가 실제 완료되면 next=claude, stage=claude_review, lock=none으로 넘긴다. Claude 심사 후 수정도 최대 2회다. 새 Gate 채택/질문 변경/freeze 또는 실제 해결 불가 장애는 next=user로 기록한다. 진행 로그와 turn은 원자적으로 함께 발행한다.
8. 변경 없는 차례 확인은 알리지 않는다. 회차 완료, 새로운 장애, 사용자 결정이 필요한 경우에만 근거 파일과 커밋 링크를 알린다. 원격 커밋과 재조회 확인 없이 저장 완료라고 주장하지 않는다. 이 예약은 지속적인 연구 루프이므로 단일 실행이나 회차가 완료됐다고 임의로 비활성화하지 않는다. next=user 또는 claude여도 예약을 그대로 두고 차례만 확인한다. 예약이나 권한을 임의로 추가·확장하지 않는다.
