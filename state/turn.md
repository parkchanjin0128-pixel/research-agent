# Turn

GitHub의 이 파일과 `state/work_queue.json`이 클라우드 실행의 지속 상태다. 현재 운영은 Codex 내부 생산·독립 검증·referee 방식이며 Claude는 claim/publish할 수 없다.

```
workflow_version: codex_internal_v1
next: codex
round: 03
stage: production
active_unit: concurrent_cn
lock: none
lock_since: none
reviews_this_round: 0
internal_review_count: 12
updated_by: codex
updated_at: 2026-11-10T15:35:08+00:00
note: C001은 Royce 의원의 입법 설명 중 기술 예시로 범위를 좁혀 확인. CR1의 H5691 위치 이의만 해소, 4/14 family 정량 매핑 및 정식 지목·대중 구속·최초 신호·효과 미입증. 기존 Gate와 concurrent_cn 전체 상태 유지.
run_id: none
run_started_at: none
run_url: https://chatgpt.com/c/6acc7a3b-c160-83e8-9d79-55067baa2f13
automation_id: 6acc7ad834008191b7a20e074815c60b
```

## 필드와 경계

- `next`: `codex` 또는 `user`. Claude 관련 이전 카운트·보고서는 이력이며 새 차례를 부여하지 않는다.
- `stage`: `production`, `verification`, `review`, `revision`, `decision`. 작은 작업 단위의 현재 단계이며 회차 전체 완료와 다르다.
- `active_unit`: 마지막 선택한 queue 단위. 다른 독립 ready 단위도 병렬 진행할 수 있다. 한 단위의 접근 실패로 모든 문헌·설계·MDE 계획을 중단하지 않는다.
- `lock`: `codex` 또는 `none`. 정확한 `run_id` 소유자만 checkpoint/publish/release한다. 같은 Codex의 다른 실행도 잠금을 재사용하지 않는다.
- 6시간 경과는 점검 사유다. 시간만으로 탈취·해제하지 않는다. 소유 실행 종료 및 후속 쓰기 부재를 확인하고 명시적 복구 이력을 남겨야 한다.
- `reviews_this_round`: 과거 Claude 심사 횟수로 보존한다. 새 내부 심사에 사용하지 않는다.
- `internal_review_count`: queue 단위별 `review_count`의 합. 단위별 수정은 최대 2회이며 그 뒤 검증 실패나 미해결 지적이 남으면 minor도 자동 해소하지 않고 `next: user`, `stage: decision`으로 올린다.

## 전환

`production → verification → review → complete` 또는 `review → revision → verification → review`를 단위별 저장한다. 작성/수정자, verifier, referee는 서로 다른 실제 agent/session ID여야 한다. 독립 verifier/referee는 작성자 대화·설득 설명을 물려받지 않는다. 현재 artifact SHA256·검증 보고서·심사 보고서·출처 확인/지적 필드가 없으면 완료 판정은 거부한다.

`scripts/review_pipeline.py validate`, `plan`, `advance`가 이 경계를 검사한다. `advance`는 정확한 소유 run ID를 요구하며 로컬 checkpoint만 쓴다. GitHub 발행은 기존 expected-head CAS 절차를 지킨다. Gate·dose/crosswalk freeze·질문 변경·과금은 기존 승인 경계이며 전체 queue 완료로 자동 승인되지 않는다.
