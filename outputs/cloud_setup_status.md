# PC 없이 실행하는 Codex–Claude 연구 설정

기준일: 2026-10-12. 로컬 예약은 일시정지했고 GitHub Actions 클라우드 구성으로 전환했다.

- 저장소: https://github.com/parkchanjin0128-pixel/research-agent
- 클라우드 워크플로: `.github/workflows/research-cloud.yml`
- GitHub 서버 점검 결과: **성공**. 상태 파서·자료 일치·잠금·checkpoint 저장 테스트를 통과했다.
- 실제 모델 실행: **아직 비활성**. 저장소에 OPENAI_API_KEY가 없으며 RESEARCH_AUTORUN=true도 설정하지 않았다. produce/publish job은 정상적으로 건너뛰었다.
- GitHub 매시간 점검, 실제 연구는 최소 5시간 간격. 실행 지연이 있을 수 있다.
- Codex 연구 → Claude 심사 → Codex 수정 흐름과 3회차 연구 지시를 유지한다. Claude 예약의 실제 실행은 첫 리뷰 커밋으로 확인해야 한다.

## 활성화 전 남은 사항

별도 OpenAI API 사용료 방식으로 진행할지 사용자 선택이 필요하다. API 방식이면 사용자가 아래 GitHub 설정에 키를 직접 등록하고 비용을 수락한 뒤 RESEARCH_AUTORUN=true로 설정한다. 키를 대화에 보내지 않는다. 코드·스케줄 배포 완료를 실제 AI 연구 가동 완료로 해석하면 안 된다.

- Secret: https://github.com/parkchanjin0128-pixel/research-agent/settings/secrets/actions
- Variable: https://github.com/parkchanjin0128-pixel/research-agent/settings/variables/actions
- 운영 안내: https://github.com/parkchanjin0128-pixel/research-agent/blob/main/docs/CLOUD_SETUP.md
- OpenAI 공식 안내: https://learn.chatgpt.com/docs/github-action

## 확인 범위

유료 모델 호출 및 실제 Claude 응답은 테스트하지 않았다. 공개 원문 외에 사용자 PC의 PDF는 클라우드에서 읽을 수 없다. 접근 실패를 미확인으로 기록하도록 했다.

별도 코드 검토에서 발견한 기존 placeholder 파일 처리와 보호된 CLI 인자 문제를 수정했다. 모델 API 키는 공식 Action의 보호된 프록시로 전달하고, Git 쓰기는 별도 runner가 허용된 연구 파일에만 수행하도록 구성했다.

클라우드 점검 실행: https://github.com/parkchanjin0128-pixel/research-agent/actions/runs/38191398585
