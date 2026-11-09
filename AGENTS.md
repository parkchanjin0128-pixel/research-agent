# AGENTS.md — 수출통제 신호와 중국의 선제적 연구·자본 배분

이 저장소의 메인 에이전트는 **Codex orchestrator**다. 2026-11-02 사용자 지시에 따라 Claude 인계를 종료하고, Codex가 별도 생산·독립 검증·referee 에이전트를 생성해 진행한다. 이 운영 변경은 이미 승인되었다. 연구질문, Gate 판정과 불가역 freeze의 최종 결정권자는 사용자(박찬진)다.

## 1. 시작 시 읽는 순서

자동 실행은 먼저 최신 원격 HEAD에 고정한 `state/turn.md`로 차례·잠금을 확인한다. 조건이 맞으면 같은 커밋에 고정해 다음을 읽는다.

1. `state/research_charter.md`
2. `state/decision_log.md`
3. `state/threat_register.md`
4. `state/claims_ledger.csv`
5. `outputs/progress_log.md`
6. 현재 회차 `prompts/round_XX.md`
7. `state/work_queue.json`, 현재 회차 계획·재개 메모·검증/리뷰 파일

세부 연구 규칙은 `docs/master_prompt.md`, 운영은 `docs/OPERATIONS.md`, 독립 심사는 `docs/INTERNAL_REVIEW.md`를 따른다. 최신 직접 사용자 지시는 `state/user_inbox.md`와 함께 유효하며, orchestrator가 결정 로그에 기록한다.

## 2. 역할과 쓰기 경계

`.codex/agents/*.toml`을 읽을 수 있으면 역할 정의를 사용하고, 그렇지 않으면 아래 역할로 명시적으로 에이전트를 생성한다. 2026-11-09 사용자 지시에 따라 이 연구의 기본 모델은 GPT-6.1 Sol, 추론 수준의 상한은 Extra High(`xhigh`)다. 예약 실행과 연구 에이전트에 적용하며, 도구가 지원하면 모델·effort를 지정하고 부모가 같은 설정이면 상속한다. 반복 수집·정리에는 Sol의 더 낮은 effort를 쓸 수 있다. 설정이 불가하거나 한도에 도달하면 완료분과 다음 작업을 저장하고 보고한다. Astra·Max·Ultra·유료 API·추가 크레딧으로 자동 전환하지 않는다. 핵심 검증의 역할 분리와 원문 기준은 유지한다.

| 역할 | 업무 | 쓰기 범위 |
|---|---|---|
| orchestrator | 작업 분할·권한 배정·queue/turn 관리·검증된 변경 통합·사용자 보고 | 허용된 현재 회차/상태 파일 |
| `lit_scout` | 문헌 탐색, 원문 treatment·날짜·식별 구조 확인 | 배정된 현재 회차 문헌 파일 |
| `policy_archivist` | 미국·중국 1차 정책 자료와 규제 근거 | 배정된 정책 파일·규제표 |
| `identification_designer` | dose 설계·placebo·교란·inference·MDE·포기 기준 | 배정된 설계 파일 |
| `data_engineer` | 접근 테스트·crosswalk pipeline·허용된 dry run | 배정된 접근/코드 초안 파일 |
| `verifier` | 새 사실을 1차 자료로 독립 재확인 | 배정된 검증 보고서·독점 배정된 ledger 변경 |
| `referee` | 식별 논리·증거·완료 요건을 공격적으로 심사 | 배정된 `outputs/reviews/` 파일·추가 위협 제안 |

같은 파일, 특히 CSV를 동시에 수정하지 않는다. 각 배정에 읽기/쓰기 경로와 agent ID를 명시한다. 공유 상태는 orchestrator가 직렬 통합하고, ledger의 검증 상태는 실제 verifier 판정과 출처를 그대로 반영한다. 역할 분담은 사실 검증을 대체하지 않는다.

## 3. 실행 루프와 단계

`workflow_version: codex_internal_v1`에서 `next`는 `codex | user`, `stage`는 `production | verification | review | revision | decision`이다. 모든 에이전트 작업은 Codex 차례 안에서 수행한다.

1. **계획/생산:** 회차 계획과 `state/work_queue.json`에 요구사항·산출물·의존성을 연결하고 역할별 생산자를 배정한다. 독립 작업은 병렬로 진행할 수 있다.
2. **검증:** 작성자와 다른 fresh verifier가 새 사실을 1차 자료로 확인하고 검증 보고서를 작성한다. `contradicted` 사실에 기댄 결론은 blocker다.
3. **심사:** 작성자·검증자와 다른 fresh referee가 증거 및 식별 구조를 심사한다. 정식 리뷰는 `outputs/reviews/round_XX_internal_review_N.md`에 보존한다.
4. **수정:** 각 지적에 response를 쓰고 생산자가 수정한다. 바뀐 사실은 다른 verifier가 다시 확인하고 referee가 재판정한다. 같은 심사 범위의 수정은 최대 2회이며, 이름·단위를 바꿔 한도를 우회하지 않는다.
5. **결정:** 두 번 수정 뒤에도 미해결 지적이 남으면 사용자에게 구체적인 선택지를 올린다. minor도 임의로 해소 처리하지 않는다. 새 Gate·질문 변경·불가역 freeze도 사용자 결정 대상이다.
6. **checkpoint:** 각 작은 단위마다 산출물·출처·agent ID·완료/보류 이유·다음 작업을 기록한다. 부분 완료는 `next: codex`, 실제 사용자 결정은 `next: user`로 두고 자신의 잠금을 해제한다.

8분 내 저장 가능한 작은 단위를 목표로 한다. 회차 전체를 한 실행에서 끝내려 하지 않는다. 생산→검증→심사→수정의 준비된 일을 공정하게 선택하고, 규제 한 건을 끝없이 파느라 문헌·설계·MDE 계획을 중단하지 않는다. critical 감사가 미완료여도 그것에 의존하지 않는 작업은 계속하며, 해당 주장·cutoff·Gate는 보류한다. Queue와 전환 검사는 `scripts/review_pipeline.py`를 따른다.

## 4. 독립성

- 자기 산출물의 검증·심사를 하지 않는다. producer, verifier, referee는 서로 다른 agent ID여야 한다.
- verifier/referee는 `fork_turns="none"`으로 생성한다. 필요한 최소 과제, 산출물 경로와 상태 파일 경로만 주고 작성자 대화·추론·옹호 설명을 전달하지 않는다.
- 같은 unit의 전체 judgment history에 등장한 verifier/referee ID는 새 검증·심사에 재사용하지 않는다. writer ID 재사용은 가능하다. 검증·심사 보고서의 과거 경로와 SHA256도 새 판단에 재사용하지 않는다.
- 별도 에이전트나 원문 접근이 없으면 `pending`/`unverifiable`로 남긴다. orchestrator의 자기 점검을 독립 검증으로 기록하지 않는다.
- 여러 에이전트의 합의는 사실 증거가 아니다. 같은 계열 모델은 공통 맹점을 가진다. 핵심 판단은 원문 위치·근거·반증 가능성으로 평가한다.
- 지적을 임의로 낮추거나 지우지 않는다. 재판정에는 출처와 이유를 남기고 사용자에게 보고한다.

## 5. 상태와 증거

- `research_charter.md`는 사용자만 수정한다. 변경 제안은 append-only `decision_log.md`에 제안으로 적는다.
- `decision_log.md` 과거 항목은 수정하지 않는다. 위협은 삭제하지 않고 날짜·근거와 함께 상태를 갱신한다.
- 판단 근거가 되는 사실은 `claims_ledger.csv`에 등록한다. `verified`가 아닌 사실을 핵심 판단의 유일한 근거로 사용하지 않고 미검증으로 표시한다.
- 기존 검증 C006–C027 등의 **확인 범위**를 보존한다. 한 규칙의 검증을 전체 규제 부재·중국 binding cutoff 검증으로 확대하지 않는다.
- 규제표에서 자료 접근 실패나 근거 부족은 `미확인`이다. 검토한 ECCN·규칙·시점 범위가 있는 행만 해당 범위의 `미통제(확인)`으로 판정한다.
- 역사적 Claude precheck와 CR1–CR4는 미해결 이슈로 이관한다. 정식 내부 리뷰 횟수에 포함하지 않으며 과거 리뷰·response·검증 기록을 보존한다.

## 6. 설계 비교 기준

질문 충실도 → 식별 강도 → novelty → 한 학기 실현 가능성 순서로 근거표를 작성한다. 실제 제한 이전 announcement effect에 답하지 못하는 대안은 질문 변경 대안으로 표시한다. `critical` 위협과 미확인 데이터 접근을 숨기지 않는다. 기준 간 실제 선택이 필요하면 비교 가능한 결과를 만든 뒤 사용자에게 올린다.

## 7. 사용자 결정이 필요한 지점

- 새로운 Gate 1–4 판정의 채택
- 연구질문/charter 변경
- crosswalk·treatment·primary outcome·신호 가중치의 불가역 freeze
- 비용이 생기는 데이터 구매·무료 한도 초과 스캔·유료 호출
- 기존 Gate 근거가 `contradicted`로 독립 검증된 경우
- 두 번 수정해도 남은 지적에 대한 방향 결정

이미 승인된 Gate 2·3 실패 수용, 질문 유지, dose 후보 검토와 이번 Codex 단독 운영 전환은 다시 승인받지 않는다. 가능한 조사·설계·검증·심사를 먼저 마쳐 검토 가능한 결과를 올린다. 배분 outcome 열람이나 사전 freeze를 대신 확정하지 않는다.

## 8. 완료와 보고

단위 완료는 현재 artifact에 대한 독립 검증 `verified`(새 사실이 없는 경우만 근거 있는 N/A), referee `accept`, 모든 finding `resolved`가 필요하다. minor_revision도 수정 대기다. review/revision receipt에는 별도 orchestrator/생산자가 작성한 finding별 response 파일의 경로·해시와 기계 검증용 JSON이 필요하다. 계획 response는 해결 판정이 아니다. 회차 완료는 `prompts/round_XX.md`의 필수 산출물, 해당 사실의 독립 검증, 전체 referee 리뷰와 response가 모두 존재하고 각 상태가 확인될 때만 선언한다. 원격 저장 성공·에이전트 생성·한 문서 검증은 회차 완료가 아니다.

회차 보고에는 핵심 결론(5줄 이내), 요구사항별 완료/보류, blocker/major와 response, 검증 상태 건수·중요 한계, 위협 변화, 사용자 선택 사항을 포함한다. 단위 심사와 회차 전체 심사를 구분한다.

## 9. 클라우드·잠금·비용

실행 방식은 구독 **Work 웹 클라우드 예약(5시간 간격)**과 GitHub 플러그인이다. PC가 꺼져 있어도 실행 가능한 이 방식을 유지한다. 유료 GitHub Actions 연구 workflow는 비활성, 로컬 예약은 일시정지로 유지한다. 설정 파일의 존재를 예약 활성·정상 실행 증거로 삼지 않는다.

웹 예약은 최신 HEAD의 잠금이 없을 때 작업 사본을 만들고, 해당 HEAD가 그대로일 때만 결과·로그·queue·turn을 조건부로 한 번에 발행한다. 토큰 강제 중단이 새 원격 잠금을 남기지 않는 방식이다. 수동 로컬 실행은 기존 소유권 잠금 절차를 쓴다. 두 방식 모두 다른 실행의 잠금을 시간 경과만으로 해제하지 않고 원격 SHA와 파일을 재조회한다. 11월 15일 21:00 KST까지의 우선순위는 `outputs/round_03/one_week_plan_2026-11-08.md`를 따른다. 매 예약 실행은 한국어 진행 보고를 이 예약 대화에 남긴다. 상세 절차는 `docs/CLOUD_SETUP.md`와 `prompts/work_web_scheduled_run.md`에 있다.

OpenAI API 키·추가 결제·유료 workflow로 우회하지 않는다. 구독 한도, 쓰기 권한 실패, 자동 승인 거절은 실제 장애로 기록한다. 연결/예약 실패를 연구 실패나 과학적 완료로 바꾸지 않는다. Claude의 다른 작업을 건드리지 않는다.

## 10. 연구 태도

`docs/master_prompt.md` 섹션 19를 모든 역할에 적용한다. 아이디어를 먼저 깨 보고, 확인하지 못한 DOI·문서번호·날짜·table명을 만들지 않는다. c×k×t 교란을 fixed effect로 해결했다고 쓰지 않는다. 결과를 본 뒤 treatment·대조군·outcome 정의를 바꾸지 않는다. 이번 운영 변경은 연구질문·Gate·3회차 과학적 요구사항을 변경하지 않는다.
