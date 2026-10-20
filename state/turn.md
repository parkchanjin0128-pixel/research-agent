# Turn

이 파일은 누가 다음 작업을 할 차례인지 정한다. 모든 자동 실행은 시작할 때 이 파일을 먼저 읽고, 자기 차례가 아니면 아무것도 하지 않고 종료한다.

```
next: codex
round: 03
stage: production
lock: none
lock_since: none
reviews_this_round: 0
updated_by: codex
updated_at: 2026-10-20T14:18:45Z
note: C006 최초 Entity List 규칙 날짜·서지 독립 검증 저장. 다음은 후속 TGL 원문 한 건 생산. 전체 round 03 및 referee 미완료.
run_id: none
run_started_at: none
run_url: https://chatgpt.com/c/6acc7a3b-c160-83e8-9d79-55067baa2f13
automation_id: 6acc7ad834008191b7a20e074815c60b
```

## 필드 정의
- **next:** 다음 차례. 셋 중 하나다.
  - `codex`: GPT 생산 담당
  - `claude`: 교차 모델 심사 담당
  - `user`: 사용자 결정 대기
- **stage:** 현재 단계. `setup` / `production` / `claude_review` / `revision` / `decision`
- **lock:** 작업 중인 주체(`codex` 또는 `claude`). 작업하지 않을 때는 `none`
  - 6시간이 지난 lock은 복구 점검 대상으로 본다. 소유 실행이 종료됐는지 확인한 뒤 해제하고 로그에 남긴다. 시간만으로 덮어쓰지 않는다.
- **reviews_this_round:** 이번 회차에 Claude가 심사한 횟수. 2에 도달하면 다음 전환은 무조건 `user`다.

## 전환 규칙

| 현재 next | 끝난 작업 | 다음 next |
|---|---|---|
| codex | 회차 생산과 내부 referee 완료 | claude |
| codex | Claude 지적 반영 수정 완료 | claude (reviews_this_round < 2) / user (= 2) |
| codex | Gate, freeze, 질문 변경, 비용 작업을 만남 | user |
| claude | 심사 완료, blocker 없음 | codex. 다음 회차로 진행 가능. 단, 다음 회차가 Gate로 끝나면 그 Gate에서 멈춘다 |
| claude | 심사 완료, blocker 있음 | codex (수정) / user (reviews_this_round = 2) |
| claude | 기존 Gate 판정의 근거 사실이 contradicted로 판정됨 | user |
| user | 결정을 `state/user_inbox.md`에 기록 | codex |
