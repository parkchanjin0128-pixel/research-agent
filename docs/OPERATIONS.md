# 실제 운영 설정 — 2026-10-12

공유 원본: https://github.com/parkchanjin0128-pixel/research-agent (설정 시 공개 저장소).

Codex는 현재 대화에 연결된 로컬 예약 작업으로 5시간마다 최신 main을 확인한다. Claude는 사용자가 제공한 화면에 따르면 2시간마다 심사하도록 이미 설정되어 있다. Claude 스케줄러의 저장 상태/실제 실행은 Codex에서 직접 확인하지 못했다. 원격 리뷰 커밋이 생겨야 양방향 연결이 확인된다.

## 차례와 충돌 방지

1. 최신 main을 가져온 뒤 `state/turn.md`를 읽는다. 자신의 차례가 아니면 파일 변경 없이 종료한다.
2. Codex는 `python scripts/claim_turn.py --actor codex`로 차례를 점유한다. 로컬 변경, 원격 분기, 다른 lock, push 실패가 있으면 작업을 시작하지 않는다. 자동 force-push/reset/rebase는 금지한다.
3. Claude는 기존 예약 지시대로 lock 커밋을 먼저 push한다. push가 충돌하면 작업을 시작하지 말고 최신 turn을 다시 읽는다. lock: codex인 동안 심사 파일/공유 상태를 수정하지 않는다.
4. 작은 작업마다 산출물과 진행 로그를 저장한다. lock_since는 각 checkpoint에서 갱신한다. 중단 복구는 마지막 커밋에서 이어가며, 잠금만 만료되었다고 진행 중인 실행을 덮어쓰지 않는다.
5. 완료 시 산출물 커밋과 함께 lock을 none으로, next를 claude 또는 user로 바꾼다. Claude는 실제 심사 완료 후에만 reviews_this_round를 증가시킨다.
6. Claude 심사 최대 2회, 내부 referee 수정 왕복 최대 2회. 새 Gate 채택/불가역 freeze/연구질문 변경/유료 데이터 등은 사용자 결정 대기다. 이미 승인된 Gate 2·3 실패와 dose 후보 검토는 다시 승인받지 않는다.

## 실행 환경

로컬 예약 작업이 저장소를 읽고 push하려면 이 PC와 Codex 앱이 실행 중이어야 한다. Git Credential Manager의 기존 인증을 사용한다. 토큰은 저장소/프롬프트에 넣지 않는다. GitHub CLI 로그인 여부와 Git 인증은 별개다.

Codex 내부 역할은 AGENTS.md에 따라 별도 에이전트로 수행한다. 도구가 역할 파일을 자동으로 인식한다고 가정하지 말고 해당 TOML을 읽고 명시적으로 역할을 배정한다. 검증자와 referee는 작성자와 다른 에이전트이며 작성자 대화/추론을 전달하지 않는다. 생성 슬롯이 부족하면 순차적으로 실행한다. 별도 에이전트가 불가능하면 독립 검증 완료로 꾸미지 말고 제한을 기록한다.

현재 대화의 예약은 대화 모델 설정을 따른다. 역할 파일의 권장 모델은 실제 spawn 시 적용 가능 여부를 확인한다. 지정 모델이 없으면 조용히 대체하지 말고 기록한다.

## 자료

- 1·2회차 산출물은 outputs/round_01 및 round_02. 원본과의 바이트별 일치 여부는 state/import_manifest.json으로 확인한다.
- 기준 로그는 outputs/progress_log.md 하나다. 과거 로그의 '원문 대기'는 해제된 과거 상태이며 최신 머리말/항목이 우선한다.
- 3회차는 진행 중이다. outputs/round_03/resume_notes.md는 미심사 조사 메모이며 완료 산출물이 아니다.
- PDF/전문 텍스트는 업로드하지 않았다. 공개 출처와 해시는 sources_manifest.json에 있다. 로컬 자료 위치는 .local/source_paths.json에만 기록한다. Claude는 출처에서 원문에 접근하고, 접근 불가 항목을 미확인으로 남긴다.
- 연구 수치나 Gate 판정은 import 성공/스케줄 성공으로 검증된 것이 아니다.

## 일시정지/재개

작업 도중이 아닐 때 state/turn.md를 next: user로 바꾸면 두 에이전트가 새 연구를 시작하지 않는다. 현재 실행 중인 작업까지 멈추려면 해당 앱에서 실행을 중단한다. 예약 자체의 정지는 각 앱의 예약 화면에서 한다. 사용자 결정은 이 대화에 말해도 유효하며 Codex가 decision_log에 기록한다. user_inbox.md만 유효하다는 이전 문구가 직접 사용자 지시를 무효화하지 않는다.

공식 Codex 예약 문서: https://learn.chatgpt.com/docs/automations?surface=app
