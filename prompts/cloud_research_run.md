# 비활성 API 컨트롤러 안내

현재 사용자는 API·추가 결제 없는 Work 웹 구독 클라우드 실행을 선택했다. 활성 예약은 prompts/work_web_scheduled_run.md를 따른다. research-cloud.yml은 비활성으로 유지하며 이 파일은 API 실행 승인이 아니다. 키 등록·API workflow 재활성화·유료 호출을 하지 않는다.

현재 workflow_version=codex_internal_v1에서는 API 컨트롤러가 flag·키 존재 여부와 무관하게 read-only skip해야 한다. 이 경로에서 잠금 점유·연구 에이전트 실행·파일 수정·publish·차례 전환을 하지 않는다. Codex 내부 생산·독립 검증·referee는 구독 Work 실행 안에서 수행한다.

잘못 호출된 경우 실제 skip 사유를 보고하고 현재 연구 상태를 유지한다. 자동 승인 거절·권한 실패를 API로 우회하지 않는다. 인증정보를 읽거나 출력하지 않는다. 과거 출력 schema에 따른 응답이 필요해도 연구·검증·원격 저장이 완료되었다고 주장하지 않는다.

다른 실행 방식을 검토하려면 사용자의 새 지시와 운영 코드·문서의 명시적 전환이 먼저 필요하다. 과거 Claude precheck·검증 provenance는 보존하지만 Claude 차례는 만들지 않는다. 연구질문·Gate·freeze 결정은 AGENTS.md에 따라 사용자에게 남긴다.