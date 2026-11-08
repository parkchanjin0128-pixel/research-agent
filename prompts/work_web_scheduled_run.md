# Codex 연구 예약 실행

이 예약의 이번 회차를 지금 수행한다. 대상은 GitHub의 parkchanjin0128-pixel/research-agent main이며, 마감은 2026-11-15 21:00 KST다. 구독 Work 웹에서 5시간마다 실행한다. PC 파일, Claude, 유료 API와 추가 크레딧은 사용하지 않는다. 이 프로젝트의 작업과 매 실행 보고는 사용자 요청으로 승인되어 있다.

1. GitHub 연결로 최신 main HEAD H를 확인하고 정확히 H에서 state/turn.md를 읽는다. next=user, 마감 경과 또는 기존 lock이 있으면 상태와 필요한 조치를 이번 실행 보고에 적고 쓰기 없이 종료한다. 타인의 lock은 나이만으로 해제하지 않는다. workflow_version=codex_internal_v1을 확인한다. 고유 UTC 시각+UUID run_id를 만든다. 이 예약의 실행 대화는 https://chatgpt.com/c/6acc7a3b-c160-83e8-9d79-55067baa2f13 이고 ID는 6acc7ad834008191b7a20e074815c60b다.

2. H의 AGENTS.md, docs/OPERATIONS.md, docs/INTERNAL_REVIEW.md를 읽는다. charter, decision_log, threat_register, claims_ledger, progress_log, prompts/round_03.md, state/work_queue.json, outputs/round_03/status_2026-11-08.md와 one_week_plan_2026-11-08.md 및 관련 최신 보고를 읽는다. 기존 Gate 2·3 실패를 수용하고 같은 연구질문의 dose 후보를 검토한다. 결과를 열기 전 데이터 접근, 공통 지지, 시점, 검정력과 포기 기준을 기록한다. 기존 Claude 사전검토 CR1–CR4와 모든 미확인 범위를 보존한다.

3. 이번 날짜 계획과 의존성에 맞는 작은 단위 하나를 약 8분 목표로 마치고 즉시 저장한다. 충분한 구독 여유가 있으면 최신 HEAD부터 다시 읽어 다음 독립 단위 하나를 수행한다. 규제 원문 수집만 반복하지 말고 문헌, 규제 행별 근거, B_k 및 placebo, 중국 정책, 데이터 및 MDE를 공정하게 전진시킨다. 별도 producer, fresh verifier, fresh referee를 실제로 생성하고 verifier/referee에 작성자 대화를 넘기지 않는다. 최대 활성 에이전트 2개. 역할별 산출물 경로, 실제 agent ID, SHA256, 1차 출처·정확한 위치와 판정, 현재 리뷰에 대응하는 response를 기록한다. 동일 단위의 판단자·보고서 경로/해시를 재사용하지 않는다. 해당 기능이나 원문에 접근할 수 없으면 보류하고 실제 실패를 기록한다. 승인·합의나 원문 한 건을 전체 회차 완료로 표시하지 않는다.

4. 웹 실행은 원격에 선점 잠금을 만들지 않는다. H를 기준으로 분리된 작업 사본에서 증거와 상태 변경안을 만든다. scripts/review_pipeline.py의 검증·의존성·필수 커버리지·수정 최대 2회 규칙을 따른다. 스크립트 실행이 불가능하면 규칙을 파일별로 점검하고 실행했다고 주장하지 않는다. 발행 직전 main이 여전히 H, next=codex, lock=none인 것을 확인한다. 산출물·append-only 진행 로그·queue·turn을 같은 tree/commit으로 묶고 parent=H, update_ref expected_sha=H, force=false로 조건부 발행한다. 허용 범위는 현재 회차 outputs/round_03/, outputs/reviews/, outputs/progress_log.md와 state/turn.md, work_queue.json, claims_ledger.csv, threat_register.md, decision_log.md다. 작업하지 않은 파일을 덮어쓰지 않는다. 새 Gate 채택, 연구질문 변경, 결과 접근·정의 freeze 및 유료 작업은 별도 사용자 결정 범위를 지킨다.

5. 발행 SHA·파일 재조회 후에만 저장 완료로 보고한다. 경쟁 실행이 H를 바꾸면 재적용·강제 갱신 없이 새 HEAD를 확인한다. 유효한 부분 결과는 충돌 사유, base SHA, run_id와 함께 허용된 recovery/work-<run_id> 또는 대화의 다운로드 가능한 파일에 보존한다. 원문 전문, 비밀정보와 사용자 로컬 경로를 공개 저장소에 기록하지 않는다. 자동 승인 거절은 우회하지 않고 거절된 동작·이유·실제 보존 위치를 기록한다.

6. 토큰 한도가 가까우면 가장 작은 검토 가능 단위부터 즉시 저장하고 남은 일과 파일을 남긴다. 강제 중단 시 다음 예약은 마지막으로 재조회된 main부터 재개한다. 한도 해제 뒤 같은 자료를 반복하지 않는다. 구독 제한 자체를 해제할 수 있다고 약속하지 않는다. 한도·접근 오류·사용자 차례를 이유로 예약을 임의 중지하지 않는다. 실제 마지막 결정은 기한 내 증거와 남은 한계를 담아 사용자가 할 수 있도록 정리한다.

7. **매 실행** 이 대화에 한국어 4줄을 남긴다. (1) 실행 시각 KST·작업 단위와 단계 (2) 이번에 한 일과 확인한 증거 (3) 저장된 커밋·파일 링크 또는 저장 실패 사유와 보존 위치 (4) 다음 실행의 한 가지 일 또는 필요한 결정. 잠금·한도·결정 대기로 변화가 없었던 실행도 이유를 적는다. 저장 성공 시 같은 정보를 outputs/progress_log.md에 append한다.
