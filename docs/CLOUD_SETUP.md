# PC 없이 실행하는 연구 시스템

2026-10-12 사용자 요청에 따라 로컬 예약 대신 GitHub 호스팅 Linux runner를 구성했다. 로컬 heartbeat는 PAUSED다. 이 문서가 이전 로컬 운영 안내보다 우선한다.

## 현재 상태

`.github/workflows/research-cloud.yml`이 GitHub 서버에서 매시간 17분에 준비 상태를 점검한다. 실제 연구는 마지막 클라우드 연구 시작에서 최소 5시간 경과, next=codex, lock=none일 때만 가능하다. 스케줄 지연 때문에 정확히 5시간마다 실행된다고 보장하지 않는다.

현재 OpenAI API secret이 없고 유료 자동 실행을 승인하지 않았으므로 연구 호출은 비활성 상태다. 점검 실행은 모델을 호출하지 않는다. **워크플로 배포/점검 성공과 AI 연구 실제 실행 성공을 구분한다.**

## 활성화에 필요한 마지막 설정

1. 사용자 소유 OpenAI API 프로젝트에서 키를 준비하고 예산/사용 제한을 설정한다. ChatGPT 구독 로그인을 GitHub Actions API 인증으로 대신하지 않는다.
2. GitHub 저장소 Settings → Secrets and variables → Actions → New repository secret에 `OPENAI_API_KEY`를 직접 등록한다. 키를 대화나 저장소 파일에 붙여넣지 않는다.
3. 별도 API 사용료를 수락한 뒤 repository **variable** `RESEARCH_AUTORUN`을 `true`로 설정한다. 키만 추가했다고 자동 과금이 시작되지 않도록 두 조건을 모두 확인한다.
4. Actions → Research cloud loop → Run workflow → mode `check`로 준비 상태를 확인하고, 연구를 실행하려면 mode `research`를 선택한다. 실제 모델 인증/호출 성공은 이 첫 유료 실행에서 확인한다.

Secret 설정: https://github.com/parkchanjin0128-pixel/research-agent/settings/secrets/actions

Variable 설정: https://github.com/parkchanjin0128-pixel/research-agent/settings/variables/actions

실행 이력: https://github.com/parkchanjin0128-pixel/research-agent/actions/workflows/research-cloud.yml

## 실행 과정

1. GitHub preflight: 가져오기·원본 파일/turn 검사·프로토콜 테스트. 키/승인/차례/간격 미충족이면 모델 실행 건너뛰기.
2. Codex 생산: 원격 잠금 커밋을 먼저 push한다. GPT-6 Astra high를 공식 Codex Action으로 호출한다. CLI 0.162.1, Action은 설정 시 확인한 commit SHA에 고정한다. 연구 Action 최대 40분이며 이 시간제한은 달러 비용 상한이 아니다.
3. 연구 agent에는 Git push 토큰을 환경변수로 전달하지 않는다. 산출물을 Actions artifact에 checkpoint로 남긴다.
4. 별도의 새 runner가 허용된 연구 파일만 검증해 커밋한다. charter/user_inbox/워크플로와 기존 회차 원본을 자동으로 덮어쓰지 않는다. 원격 HEAD가 바뀌면 강제 병합하지 않고 artifact를 보존한다.
5. Claude 심사 요건을 충족하면 next=claude. 진행 중이면 next=codex. 오류/사용자 결정이면 next=user. 잠금을 해제하고 커밋한다.

Claude는 사용자 화면에서 설정한 기존 2시간 클라우드 예약이 이 저장소를 읽는다는 전제다. 이 설정은 Claude API 키나 새 Claude 예약을 만들지 않는다. 첫 실제 Claude 리뷰 커밋으로 연결을 확인한다.

## 중단·복구와 자료 범위

- 자동 모델 호출 정지: `RESEARCH_AUTORUN=false`. 사용자 결정 대기: next=user. 현재 실행 중단은 Actions의 Cancel workflow로 한다.
- 강제 취소/runner 유실로 잠금이 남으면 `github_run_id`의 실행 종료를 확인한 뒤 복구한다. 여섯 시간이 지났다는 이유만으로 실행 중인 잠금을 훔치지 않는다.
- 모델 실행 오류 시 부분 checkpoint를 보존하고 next=user로 멈춘다. 네트워크 오류를 이유로 무한 유료 재시도하지 않는다.
- 현재 공개 저장소에 논문 PDF/전문/비밀정보는 없다. 클라우드는 로컬 Downloads를 읽을 수 없다. 공개 원문 접근 실패는 검증 한계로 남긴다.
- 공개 저장소에서 GitHub 일정 실행은 장기간 저장소 활동이 없으면 비활성화될 수 있고 실행 시각이 지연될 수 있다. Actions 실행 이력이 기준이다.

OpenAI 공식 문서: https://learn.chatgpt.com/docs/github-action

GitHub 일정 실행 문서: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
