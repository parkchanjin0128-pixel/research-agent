# 운영 절차 — Codex 내부 독립 심사

2026-11-02 승인된 운영 구조다. 구독 Work 웹 5시간 예약에서 Codex가 생산·검증·심사·수정을 관리한다. 원격 원본은 [research-agent](https://github.com/parkchanjin0128-pixel/research-agent)의 main이다. 로컬 예약은 PAUSED, API 연구 workflow는 disabled 상태를 유지한다. Claude 인계는 하지 않는다.

## 상태와 작업 queue

`state/turn.md`의 `workflow_version`은 `codex_internal_v1`이다. `next`는 `codex | user`, `stage`는 `production | verification | review | revision | decision`, `lock`은 `none | codex`다. `active_unit`은 현재 queue 단위를 가리킨다. 실제 정식 내부 리뷰만 `internal_review_count`에 기록한다. 역사적인 `reviews_this_round`는 과거 Claude 횟수이며 새 심사 카운트로 재사용하지 않는다.

`state/work_queue.json`에는 전체 회차 요구사항의 단위별 phase/status, 의존성, 산출물 경로·해시와 작성자 ID, 검증·리뷰 receipt, 수정·리뷰 횟수와 history를 둔다. 필드와 전환 검사는 `scripts/review_pipeline.py --help` 및 현재 queue를 따른다. `validate`로 일관성을 확인하고 `plan`으로 준비된 다음 단위를 고른다. `advance`는 실제 산출물과 별도 agent provenance가 있어야 한다. 스크립트 통과는 원문 사실이나 과학적 타당성의 독립 검증을 대신하지 않는다.

한 실행은 약 8분 내 저장할 수 있는 단위를 목표로 한다. 활성 작업 subagent는 최대 2개로 제한하고 슬롯이 부족하면 순차 실행한다. 준비된 verification/review/revision을 방치하지 않되, 특정 critical 감사가 끝나지 않았다는 이유로 독립적인 생산 항목을 무기한 보류하지 않는다. 모든 3회차 항목이 queue에 나타나야 한다. 규제·문헌·식별·중국정책·메커니즘·inference/MDE·완료심사의 coverage를 checkpoint에서 확인한다.

의존성이 막힌 단위는 이유·필요 증거를 기록하고 독립 단위로 이동한다. 미검증 규제 범위를 확인된 cutoff로 쓰거나, 막힌 항목을 삭제해 회차 완료를 만들지 않는다. 최신 규제 checkpoint의 검증을 마치면 그 다음 규칙만 무한 추적하는 대신 다른 독립 설계·문헌 단위도 선택한다.

## 점유·발행

웹 예약은 고정된 HEAD에서 검토 가능한 단위를 작성한 다음, 그 HEAD의 `next: codex`, `lock: none`과 현재 원격 HEAD가 일치할 때만 산출물·진행 로그·queue·turn을 한 번에 조건부 발행한다. 작업 중 원격 잠금을 만들지 않아 한도 중단 후 다음 예약이 마지막 저장점에서 재개할 수 있다. 동시 실행이 먼저 저장하면 이번 저장은 실패하며 비교 후 이어간다. CLI의 소유 잠금 검사와 아래 선점 절차는 수동 로컬 실행에 적용한다.

1. 최신 main HEAD H와 정확히 H에 고정한 turn을 읽는다. `next`가 codex가 아니면 쓰기 없이 종료한다.
2. 기존 lock은 소유 실행의 종료 여부를 확인한다. 같은 actor라도 다른 run_id면 점유하지 않는다. 6시간 경과는 복구 점검 사유이지 자동 해제 권한이 아니다.
3. lock이 없으면 UTC 시각·고유 run_id·실행 링크로 점유 커밋을 만든다. parent=H, expected_sha=H의 조건부 ref 갱신으로만 main에 적용한다. 충돌 시 최신 상태부터 다시 읽는다. 조건부 갱신 기능이 없으면 연구를 시작하지 않는다.
4. 배정된 역할만 해당 파일을 수정한다. 같은 CSV나 공유 상태의 동시 수정을 금지한다. verifier/referee의 fresh 생성과 agent ID를 보고서에 기록한다. 같은 unit의 전체 judgment history에서 검증·심사 ID 및 보고서 경로/해시를 재사용하지 않는다. writer ID는 재사용할 수 있다.
5. checkpoint 시 최신 HEAD P와 P의 자신의 lock/run_id·변경 대상 파일을 확인한다. 산출물·진행 로그·queue·turn을 parent=P, expected_sha=P로 원자적 발행한다. 원격 SHA와 내용을 재조회해야 저장 완료다.
6. 부분 작업이면 `next: codex`, 단계·active_unit을 실제 다음 일로 맞추고 자신의 lock을 해제한다. 실제 사용자 결정이면 `stage: decision`, `next: user`로 둔다. Claude 차례는 생성하지 않는다.

force-push, reset, 임의 rebase로 충돌을 없애지 않는다. API 키·인증정보·논문 전문·로컬 절대 자료 경로는 공개 저장소에 올리지 않는다. `round_01/02` 원본과 charter를 보존한다.

## 검증·심사·완료

[INTERNAL_REVIEW.md](INTERNAL_REVIEW.md)의 작성자 분리, `fork_turns="none"`, 원문 재확인, response와 최대 2회 수정 규칙을 따른다. review/revision receipt에는 별도 orchestrator/생산자의 response_path·response_sha256과 현재 finding ID에 정확히 대응하는 JSON response가 필요하다. 계획 response를 해결 판정으로 쓰지 않고 revision마다 새 파일로 보존한다. 단위 완료는 현재 artifact의 verified(새 사실이 없을 때만 근거 있는 N/A), referee accept, 모든 finding resolved가 필요하다. minor_revision도 수정 대기이고 두 번 수정 뒤 미해결 지적은 minor를 포함해 decision이다. 단위 심사와 회차 전체 심사를 구분한다. CR1–CR4와 기존 미확인 claim은 새 queue로 이관하되 판정을 올리지 않는다.

새 Gate·질문 변경·freeze 결정 전까지 가능한 독립 조사와 심사를 진행한다. 해당 결정에 의존하지 않는 단위는 계속할 수 있다. 새 사용자 판단이 필요한 구체적인 결과가 마련되면 `next: user`다. 기존 승인 사항을 다시 승인받지 않는다.

## 중단과 복구

원격에 저장되지 않은 변경은 완료가 아니다. 충돌한 산출물·base SHA·run_id는 허용된 `recovery/work-<run_id>` 브랜치에 보존하고 ref를 재조회한다. 그것도 실패하면 대화의 다운로드 가능한 파일로 보존하고 실제 저장 위치를 알린다. 오래된 잠금은 소유 실행 종료가 확인된 뒤 복구 기록을 남기고 해제한다. 확인할 수 없으면 복구 필요를 알린다.

쓰기 권한 또는 자동 승인 검토가 거절되면 거절된 동작과 명시된 이유를 기록하고 가능한 조사·미발행 산출물을 보존한다. main 변경을 무작정 재시도하거나 권한을 임의 확장하지 않는다. 거절된 발행을 다른 경로로 우회하지 않는다. 구독 한도는 API·유료 workflow로 우회하지 않는다. 예약 자체는 자동으로 비활성화하지 않으며, 중단 상태가 생기면 실제 UI·최근 실행으로 확인한다.

11월 8일 사용자 요청에 따라 매 예약 실행에서 단계, 작업과 증거, 저장 상태와 링크, 다음 작업을 한국어로 보고한다. 변화가 없으면 그 이유를 보고한다. 저장한 실행의 기록은 진행 로그에 추가한다. 직접 대화에서 받은 사용자 지시는 결정 로그에 기록한다.

## 비활성 대체 실행

`prompts/gpt_scheduled_run.md`와 `prompts/cloud_research_run.md`는 비활성 로컬/API 환경의 호환 지침이다. 파일이 있다고 재활성화하지 않는다. 로컬 도구를 수동 사용하는 경우 `scripts/claim_turn.py --actor codex`의 최신 main/잠금 검사와 같은 v2 phase 절차를 따른다. API 컨트롤러 환경은 별도 사용자 지시 없이는 사용하지 않는다.
