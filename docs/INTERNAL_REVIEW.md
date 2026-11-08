# 내부 독립 검증·심사 프로토콜

2026-11-02 사용자 지시에 따른 Codex 단독 운영이다. 작성자와 별도 verifier/referee를 생성하되 같은 계열 모델의 공통 맹점을 인정한다. 독립 agent의 수나 합의가 원문 증거를 대신하지 않는다.

## 1. 배정과 provenance

orchestrator는 단위마다 요구사항, 허용 쓰기 경로, producer ID, 산출물 경로·SHA256을 queue에 기록한다. 하나의 CSV는 한 역할만 독점 편집한다. 통합 시 다른 역할의 검증 상태를 임의로 올리지 않는다.

verifier는 producer와 다른 새 agent, referee는 producer·verifier와 다른 새 agent로 생성한다. 둘 다 `fork_turns="none"`을 사용한다. 역할 정의, 최소 과제, 읽을 산출물/상태 파일 경로, 허용 보고서 경로만 제공한다. 작성자의 대화·추론·옹호 메시지는 전달하지 않는다. 검증자는 원문을 직접 다시 확인한다.

같은 unit의 전체 judgment history를 조회해 과거 verifier/referee ID를 새 검증·심사에 재사용하지 않는다. writer ID의 재사용은 가능하다. 새 판단은 과거 report_path 또는 report_sha256을 재사용하지 않고 새 보고서·실제 agent provenance를 남긴다. 과거 보고서를 근거로 참조하는 것과 새 독립 검증을 수행하는 것을 구분한다.

예시 배정의 내용은 다음 범위로 제한한다.

- verifier: “이 경로의 주장과 상태 파일을 읽고 1차 자료로 재확인하라. 출처·정확한 위치·판정·한계를 지정된 보고서에 기록하라.”
- referee: “이 산출물·검증 보고서·charter·threat register·회차 요구사항을 읽고 식별과 증거를 비판하라. 지정된 리뷰에 지적과 해결 기준을 기록하라.”

현재 구독에서 사용할 수 있는 상위 모델/effort를 상속한다. 모델 이름을 바꾸는 것만으로 독립성이 생기지 않는다. 별도 agent가 불가능하면 자기 점검과 독립 검증을 구분하고 해당 phase를 보류한다.

## 2. 사실 검증 보고서

검증 보고서는 현재 회차의 `verification_<unit>.md` 등 지정 경로에 작성한다. 최소 내용은 다음과 같다.

1. 범위: unit ID, verifier의 실제 agent ID, 작성 시각, 읽은 파일·SHA256, producer ID와의 분리.
2. 주장별 원문 확인: claim ID/문장, 1차 자료 URL, 문서번호·판본·페이지/조항/표/단락, 접근일, 관찰한 근거.
3. `verified | contradicted | unverifiable` 판정, 확인 범위와 확인하지 못한 부분.
4. 기존 ledger 변경 제안과 영향을 받는 설계·위협.
5. 접근 실패와 필요한 원문 목록. 확인하지 못한 식별자를 추정하지 않는다.

`partially_verified`는 일부 주장만 확인된 보고서 전체 상태이며 개별 사실을 모두 verified로 바꾸지 않는다. 순수 형식 수정처럼 새 사실이 없는 단위만 `not_applicable`과 구체적인 `no_new_facts_reason`을 쓸 수 있다. 새 사실이 있는 설계·문헌·규제 단위의 검증을 생략하는 수단으로 사용하지 않는다.

규제 원문 한 건 검증은 “동시기 다른 실제 제한 없음”, 전체 41행 미통제, 기술별 China-binding cutoff 확인을 뜻하지 않는다. 필요한 ECCN·규칙·시간 범위를 행별로 명시한다. 기존 C006–C027의 좁은 확인 범위를 그대로 지킨다.

## 3. 정식 referee 보고서

파일명은 `outputs/reviews/round_XX_internal_review_N.md`다. 이전 리뷰를 덮어쓰지 않는다.

- 실제 referee ID와 생산·검증 agent ID 분리, 읽은 artifact SHA256.
- 심사 범위: 특정 단위 또는 회차 전체. 단위 심사를 전체 회차 승인으로 쓰지 않는다.
- 판정: `accept | minor_revision | major_revision | reject`, 근거. receipt와 같은 표준 값을 사용한다.
- 지적 표: `ID | severity | 위치 | 문제 | 증거 | 해결책/통과 기준 | 상태`.
- 질문 충실도, threat register의 critical·major별 해결/주장만/미해결 여부.
- 식별 변동과 estimand, c×k×t 교란, dose 강도별 효과와 수준 효과의 구분.
- 가장 가까운 원문 연구와 novelty, 시점·binding restriction·중국 정책·placebo·MDE·포기 기준의 충족 여부.
- 사전 반론·추가 확인, pre-mortem 리젝 사유 3개, 다음 phase 권고.

단위 밖의 요건은 해당 범위 밖이라고 표시한다. 모든 필수 산출물의 회차 전체 심사는 별도로 수행한다. 지적이 하나도 없어도 완료 기준과 원문에 기반한 이유를 적는다.

## 4. Response와 수정 한도

orchestrator/생산자는 각 리뷰 옆 `round_XX_internal_review_N_response.md`를 작성한다. 각 finding ID에 반영 위치·내용·검증 계획 또는 반영하지 않는 근거를 대응시킨다. 미해결 상태를 삭제하지 않는다.

review와 revision receipt에는 `response_path`, `response_sha256`이 필수다. response 작성자는 실제 orchestrator/producer ID이며 같은 unit 전체 history의 verifier/referee와 달라야 한다. response 파일에는 아래 형식의 fenced `json` 블록을 정확히 하나 넣는다. `phase`는 현재 receipt와 같아야 하며 review checkpoint는 `review`, revision checkpoint는 `revision`이다. 예시의 ID·경로·해시는 실제 값으로 채운다.

```json
{
  "phase": "review",
  "unit_id": "실제 unit ID",
  "review_path": "해당 리뷰 경로",
  "review_sha256": "해당 리뷰의 실제 SHA256",
  "author_id": "실제 orchestrator 또는 producer agent ID",
  "responses": [
    {
      "finding_id": "해당 리뷰의 finding ID",
      "response": "반영 내용 또는 반영 예정 내용",
      "location": "수정 파일과 위치",
      "verification_plan": "독립 재검증 방법"
    }
  ]
}
```

반영하지 않는 항목은 `finding_id`, `response`, `not_adopted_reason`으로 기록한다. 현재 리뷰의 모든 finding ID와 responses를 누락·중복·추가 없이 정확히 대응시킨다. 지적이 없으면 `responses: []`와 구체적인 `no_findings_reason`을 넣는다. review advance 전에 미반영 계획을 response로 작성할 수 있으나 그 자체로 finding이 resolved가 되지 않는다. response 파일명은 항상 `_response.md`로 끝나야 한다. revision마다 `round_XX_internal_review_N_r1_response.md`처럼 새 파일을 만들고 과거 파일·해시를 보존한다.

동일 심사 범위의 수정은 최대 2회다. 수정 후 독립 verifier가 바뀐 주장과 현재 artifact를 확인하고, 별도 fresh referee가 다시 판정한다. 파일·unit 이름을 바꾸어 한도를 초기화하지 않는다. minor_revision도 수정 대기이며, 2회 후 미해결 지적이 남으면 `decision`으로 보내 사용자에게 선택지·근거·추천을 올린다. 사소하다는 이유로 자동 하향·해소 처리하지 않는다. 새로운 Gate 채택이나 freeze도 사용자가 결정한다.

역사적 Claude precheck CR1–CR4는 계속 추적하지만 정식 내부 리뷰 횟수에 포함하지 않는다. 기존 precheck·response·claims provenance는 보존한다. 새 내부 리뷰의 동의만으로 CR1–CR4를 해결했다고 표시하지 않는다.

## 5. Queue receipt와 상태 전환

실제 명세는 `state/work_queue.json`과 `scripts/review_pipeline.py --help`를 따른다. 핵심 필드는 다음과 같다.

| receipt | 필수 기록 |
|---|---|
| production | phase, 실제 agent_id, artifacts 경로 |
| revision | phase, 실제 agent_id, artifacts 경로, finding별 responses, response_path, response_sha256 |
| verification | phase, 실제 agent_id, report_path, 현재 artifact_hashes, verdict, source_checks(claim/source/result); N/A면 이유 |
| review | phase, 실제 agent_id, report_path, 현재 artifact_hashes, verdict, findings(id/severity/status/reason), response_path, response_sha256 |

스크립트는 보고서 해시와 agent 분리를 확인한다. hash는 실제 현재 파일에서 계산한다. 과거 보고서를 새 산출물에 재사용하거나 가상의 agent ID를 만들지 않는다. `advance --unit ID --receipt PATH --run-id RUN`는 자신의 실행 잠금이 있을 때만 수행한다. report/receipt 검사는 증거 내용의 진위를 보증하지 않는다.

단위의 `complete`는 현재 artifact가 독립 검증 `verified`(새 사실이 없는 경우만 근거 있는 N/A), referee `accept`, 모든 finding `resolved`일 때 가능하며 그 범위에 한정된다. minor/major/reject나 partially_verified를 완료로 통과시키지 않는다. 회차 완료는 전체 요구사항 coverage, 필수 산출물, 독립 검증, 전체 referee 리뷰/response 및 지적 해소 상태를 확인한 뒤에만 선언한다. 미완료 규제 감사가 있어도 독립 설계·문헌·MDE 계획은 계속하고, 그 감사에 의존하는 주장·cutoff·Gate만 보류한다.
