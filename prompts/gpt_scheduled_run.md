# GPT 예약 실행 지시문 (ChatGPT/Codex scheduled task에 그대로 붙여넣기)

```
이 작업은 예약 실행이다. 사용자는 지켜보고 있지 않다.

1. 연구 repo의 최신 상태를 가져와라 (git pull).
2. state/turn.md를 읽어라.
   - next가 codex가 아니면 아무것도 하지 말고 "차례 아님"으로 종료하라.
   - lock이 claude이고 6시간이 지나지 않았으면 종료하라.
3. next가 codex이면 turn.md를 lock: codex, lock_since: 현재시각으로 바꾸고 커밋·push하라. push가 거절되면 pull 후 2번부터 다시 하라.
4. AGENTS.md를 따라 작업하라.
   - 시작 시 state/user_inbox.md의 새 지시를 확인하고 decision_log.md에 반영하라.
   - outputs/reviews/에 Claude 리뷰가 새로 있으면 blocker와 major부터 반영하라.
   - 현재 회차는 turn.md의 round와 prompts/round_XX.md를 따른다. 다음 회차 지시문이 없으면 docs/master_prompt.md의 회차표를 바탕으로 prompts/round_XX.md를 작성하라.
5. 사용량 한도로 언제든 중단될 수 있다. 작은 작업 단위가 끝날 때마다 progress_log.md를 갱신하고 커밋·push하라.
   - 커밋 메시지 형식: "rXX: <무엇>"
6. 종료 시 state/turn.md의 전환 규칙에 따라 next를 정하고 lock: none으로 바꿔 커밋·push하라.
   - Gate, freeze, 질문 변경, 비용 작업에서는 반드시 next: user로 멈춰라.
7. 사용자에게 보고가 필요하면(next: user) 보고 내용을 outputs/round_XX/report_to_user.md에 쓰고 결과에도 요약하라.
```
