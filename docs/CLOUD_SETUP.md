# 구독으로 PC 없이 실행하는 연구 시스템

2026-10-12 최신 사용자 지시: OpenAI API와 별도 과금을 사용하지 않는다. ChatGPT Work 웹 예약과 연결된 GitHub 플러그인을 사용한다. 구독 사용량 제한은 적용되며 추가 크레딧을 구매하지 않는다.

## 검증 상태

- Work 웹 GitHub 플러그인 설치 및 기존 OAuth 연결 확인.
- 일반 Work 웹 대화에서 파일 생성·main 커밋·재조회 성공. 독립적으로 GitHub 원격 내용과 SHA를 확인했다.
- 테스트 커밋: https://github.com/parkchanjin0128-pixel/research-agent/commit/d05893031cb5e7c526f59875c6d9cec07520bc2b
- 파일: outputs/setup/work_web_write_probe.md. 연구 상태는 변경하지 않았다.
- 웹 예약 research-agent 구독 클라우드, ID 6acc7ad834008191b7a20e074815c60b를 생성했다. UI에서 실행 위치 클라우드·5시간 간격을 확인했다. 예약 실행의 파일 생성·재조회에 성공했고 원격 커밋을 독립 확인했다: https://github.com/parkchanjin0128-pixel/research-agent/commit/b59fb696bcd9b041e92d757ffb6d152e2f8ad5f6
- 예약 검증 후 실제 연구 프롬프트 적용을 진행한다. 일반 쓰기 및 예약 쓰기 검증은 연구 회차 완료나 정기 실행의 무한 가용성을 보장하지 않는다.
- 기존 GitHub Actions research-cloud.yml은 서버에서 disabled_manually로 확인했다. OpenAI API 키는 등록하지 않았다. 코드 보존은 실행 승인이나 활성화가 아니다.
- 기존 로컬 research-agent-claude 예약은 PAUSED다.

## 운영 기준

웹 예약은 로컬 checkout을 유지하지 않으므로 GitHub main을 상태의 원본으로 사용한다. main HEAD를 먼저 읽고 그 커밋에 고정한 turn을 검사한다. GitHub의 조건부 ref 갱신으로 잠금을 점유하고 자신의 run_id와 최신 HEAD를 재확인해 산출물·진행 로그·turn을 원자적으로 발행한다. 조건부 갱신이 지원되지 않으면 연구를 시작하지 않는다. 상세 웹 지시문은 prompts/work_web_scheduled_run.md다.

Codex 생산 → 독립 검증·내부 referee → Claude 교차 심사 → Codex 수정 순서를 유지한다. 상세 연구는 prompts/round_03.md, 현재 상태는 state/turn.md 및 outputs/progress_log.md를 따른다. 기존 Gate 2·3 실패 수용과 dose 검토는 승인된 사항이다. 신규 Gate 채택·불가역 freeze는 사용자 결정 대상이다.

Claude가 커밋한 outputs/reviews/round_03_claude_precheck_1.md를 확인했다. 이는 직접 사용자 요청으로 수행한 사전점검이며 Claude 정기 예약의 무인 실행 성공을 뜻하지 않는다. 해당 리뷰는 정식 리뷰 횟수를 증가시키지 않는다.

공개 저장소에 사용자 PDF 전문이나 인증정보를 올리지 않는다. 웹 실행은 PC Downloads 파일을 읽을 수 없다. 원문 접근 실패는 미확인으로 남기고 필요한 원문 목록을 따로 작성한다.

## 중단과 복구

차례가 codex가 아니면 Codex 예약은 쓰기 없이 종료한다. 잠금이 있으면 실행 식별자와 링크로 실제 종료 여부를 확인한다. 시간 경과만으로 다른 실행의 잠금을 훔치지 않는다. 확인할 수 없으면 복구 필요를 알린다. 충돌한 산출물은 recovery/work-<run_id> 브랜치 또는 대화 다운로드 파일로 보존하고 실제 저장을 검증한다. 구독 한도에 도달하면 API로 우회하지 않는다.

예약 자체는 ChatGPT 웹의 예약 화면에서 관리한다. 이 문서나 GitHub 파일만 변경해서 웹 예약이 생성되었다고 간주하지 않는다. 과거 유료 Actions 및 로컬 실행은 새 사용자 지시 없이 재활성화하지 않는다.

공식 예약 문서: https://learn.chatgpt.com/docs/automations

구독 인증 안내: https://learn.chatgpt.com/docs/auth
