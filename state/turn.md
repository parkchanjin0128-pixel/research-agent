# Turn

이 파일은 누가 다음 작업을 할 차례인지 정한다. 모든 자동 실행은 시작할 때 이 파일을 먼저 읽고, 자기 차례가 아니면 아무것도 하지 않고 종료한다.

```
next: user
round: 03
stage: setup
lock: none
lock_since:
reviews_this_round: 0
updated_by: claude
updated_at: 2026-10-12T09:45+09:00
note: GPT Work의 1·2회차 산출물을 outputs/round_01, outputs/round_02에 올린 뒤 next를 codex로 바꿔라.
```

## 필드 정의
- **next:** 다음 차례. 셋 중 하나다.
  - `codex`: GPT 생산 담당
  - `claude`: 교차 모델 심사 담당
  - `user`: 사용자 결정 대기
- **stage:** 현재 단계. `setup` / `production` / `claude_review` / `revision` / `decision`
- **lock:** 작업 중인 주체(`codex` 또는 `claude`). 작업하지 않을 때는 `none`
  - 6시간이 지난 lock은 만료된 것으로 본다. 덮어쓰고 로그에 남겨라.
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
