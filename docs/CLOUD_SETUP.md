> 2026-11-13 최신 직접 사용자 지시: 연구용 예약을 모두 중지하고 현재 세션에서 연구를 마무리한다. Work 웹·로컬 연구예약은 PAUSED, GitHub Research cloud loop는 disabled_manually를 직접 확인했다. 아래 클라우드 예약 중심 절차는 과거 운영 이력이며 새 사용자 요청 없이 재개하지 않는다. 검증·심사·질문·Gate 권한은 유지한다. 현재 상태와 실제 증거: outputs/final_research/automation_status_nov13.json, STATUS.json.

# 구독 클라우드 실행 — PC·API 없이 진행

2026-11-02 사용자 요청에 따라 Claude 인계를 종료하고 Codex 내부 독립 검증·심사로 전환한다. 실행 방식은 기존 **ChatGPT Work 웹 5시간 예약 + GitHub 플러그인**을 유지한다. PC 로컬 checkout에 의존하지 않는다. OpenAI API 키, 유료 연구 workflow, 추가 크레딧 구매를 사용하지 않으며 구독 한도는 적용된다.

## 예약과 실제 검증 범위

- 저장소: [parkchanjin0128-pixel/research-agent](https://github.com/parkchanjin0128-pixel/research-agent).
- 예약: `research-agent Codex 자체 검증`, ID `6acc7ad834008191b7a20e074815c60b`, 기존 설정 주기 5시간.
- 실행 대화: [GitHub 쓰기 테스트](https://chatgpt.com/c/6acc7a3b-c160-83e8-9d79-55067baa2f13).
- 2026-10-12 일반 웹 쓰기/재조회 테스트: [d058930](https://github.com/parkchanjin0128-pixel/research-agent/commit/d05893031cb5e7c526f59875c6d9cec07520bc2b).
- 같은 날 예약 실행 쓰기/재조회 테스트: [b59fb69](https://github.com/parkchanjin0128-pixel/research-agent/commit/b59fb696bcd9b041e92d757ffb6d152e2f8ad5f6).
- 전환 전 2026-11-02 점검에서 웹 실행의 main 조건부 발행이 자동 승인 검토의 “변경 권한 미확인 / 기본 브랜치 변경 권한 미확인” 사유로 거절된 기록과 예약 중단 기록을 확인했다. 과거 쓰기 테스트 성공은 현재 정상 가동의 증거가 아니다.
- 로컬 `research-agent-claude` 예약은 PAUSED, API `research-cloud.yml`은 disabled 상태를 유지한다. 이를 이번 해결책으로 재활성화하지 않는다.

이 문서나 저장소 프롬프트 변경만으로 실제 웹 예약이 갱신·재개되었다고 간주하지 않는다. 전환 후 예약의 저장 지시문·활성 상태·최근 실행과 새 원격 checkpoint를 별도로 확인해야 한다.

## 새 실행 절차

예약의 본문은 [prompts/work_web_scheduled_run.md](../prompts/work_web_scheduled_run.md)의 현재 지시를 따라야 한다. 매 실행 main의 최신 HEAD에 고정해 turn·queue·운영 지침을 읽는다. Codex가 production → verification → review → revision을 관리하고 실제 Gate/freeze 결정만 사용자에게 올린다. Claude 참여·응답·토큰을 필요로 하지 않는다.

약 8분의 작은 단위로 원격 checkpoint를 남기며, 규제 감사뿐 아니라 독립적인 문헌·설계·정책·inference/MDE 단위를 공정하게 진행한다. 작성자와 다른 fresh verifier 및 새 referee의 실제 보고서와 provenance를 남긴다. [INTERNAL_REVIEW.md](INTERNAL_REVIEW.md)의 독립성·수정 한도·완료 규칙을 따른다.

## 승인 범위와 발행

사용자는 연구의 계속 진행과 Codex 단독 운영 구조 변경을 요청했다. 그 범위에서 이 저장소 main에 현재 회차 연구 산출물과 허용된 운영상태를 조건부 발행한다. 정기 연구 실행의 허용 파일은 현재 회차 outputs, reviews, progress_log와 turn/queue/claims/threat/decision 상태다. charter, 사용자 지시 원문, 과거 회차 원본, workflow·보안 설정을 임의 변경하지 않는다. 운영 시스템의 향후 확장·비용 발생·새 Gate/freeze는 별도 규칙을 따른다.

웹 예약은 고유 run_id와 시작 HEAD를 기록하고 선점 잠금 없이 별도 사본에서 작업한다. checkpoint 직전에 최신 HEAD·차례·잠금이 시작 조건과 일치할 때만 산출물·진행 로그·queue·turn을 하나의 커밋으로 조건부 발행한다. 커밋 SHA와 파일을 재조회한다. 구독 한도가 작업 중에 끊겨도 다음 예약은 마지막 발행본에서 재개하며, 한도에 도달하기 전에 저장하지 못한 작업은 유실될 수 있다.

프롬프트의 승인 범위는 자동 승인 검토를 무효화하지 않는다. 동일 동작이 다시 거절되면 거절 동작·사유를 숨기지 않고 기록한다. 권한을 임의 확장하거나 API·다른 계정·다른 발행 경로로 우회하지 않는다. 안전하게 보존 가능한 미발행 산출물을 남기고 사용자 조치가 필요한 경우만 알린다.

## 중단과 복구

차례가 codex가 아니면 쓰기 없이 종료한다. 다른 run_id의 잠금은 실행 종료를 확인하기 전까지 해제하지 않는다. 단순 시간 경과나 같은 actor 이름은 복구 근거가 아니다. 충돌한 변경은 허용된 recovery 브랜치 또는 다운로드 가능한 파일로 보존하고 저장 여부를 확인한다. 승인 거절을 우회하는 발행은 하지 않는다.

구독 한도·원문 접근·GitHub 쓰기 실패를 구분한다. 공개 저장소는 출처와 검증 기록을 보존하고, 로컬 원문 PDF는 별도로 유지한다. 필요한 원문 목록을 따로 남긴다. 11월 8일 요청에 따라 매 실행마다 작업, 증거, 저장 상태, 다음 단계를 예약 대화에서 보고한다.

공식 제품 안내: [예약 실행](https://learn.chatgpt.com/docs/automations), [구독 인증](https://learn.chatgpt.com/docs/auth), [subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).

