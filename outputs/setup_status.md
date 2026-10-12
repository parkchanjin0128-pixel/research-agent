# Codex–Claude 연구 시스템 설정 결과

설정일: 2026-10-12 (KST)

공유 저장소: https://github.com/parkchanjin0128-pixel/research-agent

## 적용된 구성

| 항목 | 상태 |
|---|---|
| Codex 예약 | 활성화, 현재 대화에서 5시간 간격 |
| 예약 ID | research-agent-claude |
| Claude 예약 | 사용자 화면의 2시간 간격 예약을 전제로 연결. Codex에서 스케줄러나 실제 실행은 확인하지 못함 |
| 역할 | Codex 생산·내부 독립 검증/심사 → Claude 교차 모델 심사 → Codex 수정 |
| 현재 차례 | round 03 / next codex / lock none / Claude 심사 0회 |
| 기존 산출물 | 18개 이관, 최초 원본 SHA-256 일치 확인 |
| 3회차 | 미완료 상태 유지. 조사 메모·공개 원문 출처 목록 인계 |
| 원격 쓰기 | 실제 커밋·push 및 원격 HEAD 일치 확인 |
| 동시 쓰기 | 먼저 잠금 커밋을 push한 실행만 작업. 다른 차례/잠금이면 종료 |
| 중단 조건 | 신규 Gate 채택·불가역 freeze·질문 변경·비용 작업·해결 못한 blocker를 사용자에게 올림 |
| 독립 심사 | 역할별 다른 에이전트, Claude 재심 최대 2회 |

## 검증

- 초기 산출물 18개의 바이트 해시 확인.
- 상태 파서의 빈 timestamp 처리 확인.
- 임시 Git 원격에서 잘못된 차례 건너뛰기, 잠금 push, 두 번째 checkout의 잠금 존중, reviewer의 잠금 존중, 미커밋 파일 보존을 테스트했다.
- 실제 원격 차례 점유 테스트 커밋: `01142a9753122b650924c1d61512701701a77a40`.
- 설정 점검 후 잠금을 해제하고 next codex로 복구했다. 이 테스트를 연구 실행이나 Claude 심사 완료로 계산하지 않았다.

## 사용자가 알아둘 점

PC와 Codex 앱이 실행 중이어야 로컬 연구 예약이 저장소에 접근해 작업할 수 있다. 예약은 현재 대화 모델 설정을 따른다. 특정 모델로 실행됐다고 별도 확인한 것은 아니다.

Claude의 2시간 예약은 새로 만들거나 수정하지 않았다. 기존 예약이 같은 저장소의 최신 state/turn.md와 CLAUDE_REVIEWER.md를 읽는 구조를 유지했다. 첫 Claude 리뷰 커밋이 생겨야 실제 양방향 작동이 확인된다.

현재 저장소는 공개다. 연구 산출물/출처 목록을 올렸으며 제공받은 논문 PDF와 전문 텍스트, 인증정보는 올리지 않았다. 논문은 로컬 캐시와 공개 출처에서 확인한다.

다음 작업은 3회차 위협 강도 설계의 완성·독립 검증·내부 심사다. 이미 승인한 Gate 2·3 실패와 연구질문 유지에 대해 재승인을 요구하지 않는다. 새 결정이 필요하면 먼저 검토 결과와 선택지를 만들어 보고한다.

운영 안내: [GitHub OPERATIONS](https://github.com/parkchanjin0128-pixel/research-agent/blob/main/docs/OPERATIONS.md)

공식 예약 문서: [OpenAI 예약 작업 안내](https://learn.chatgpt.com/docs/automations?surface=app)
