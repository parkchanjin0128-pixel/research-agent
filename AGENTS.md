# AGENTS.md — 수출통제 신호와 중국의 선제적 연구·자본 배분 연구 하네스

이 파일은 이 폴더에서 작업하는 모든 에이전트에게 적용된다. 메인 에이전트는 **orchestrator**다. 직접 모든 작업을 하지 말고, 아래 역할별 subagent에게 위임하고 결과를 통합하라.

연구 방향의 최종 결정권자는 **사용자(박찬진)**다. 에이전트는 대안을 비교하고 추천할 수 있지만, Gate 판정의 채택, 연구질문 변경, 되돌릴 수 없는 freeze는 사용자의 승인 없이 확정하지 않는다.

---

## 1. 작업 시작 시 반드시 읽을 파일 (순서대로)

1. `state/research_charter.md`: 고정된 연구질문과 주장 가능 범위
2. `state/decision_log.md`: 지금까지의 Gate 판정과 사용자 결정
3. `state/threat_register.md`: 알려진 식별 위협과 처리 상태
4. `state/claims_ledger.csv`: 설계 근거가 되는 사실과 검증 상태
5. `progress_log.md` (`outputs/` 아래에 있으면 그 파일)
6. 이번 회차 지시: `prompts/round_XX.md`
7. 세부 규칙이 필요하면 `docs/master_prompt.md` (원래 마스터 프롬프트, 특히 섹션 0과 19)

---

## 2. 역할

Codex에서는 `.codex/agents/<name>.toml`에 정의되어 있다. 정의 파일을 읽을 수 없는 환경(예: ChatGPT Work)에서는 아래 설명대로 subagent를 생성하라.

| 이름 | 하는 일 | 권장 모델 | 쓰기 권한 |
|---|---|---|---|
| `lit_scout` | 검색 프로토콜에 따른 문헌 탐색, 원문 확인, `literature_table.csv`와 `search_log.csv` 관리 | 6.1 Sol, high | outputs |
| `policy_archivist` | 미국·중국 정책의 1차 자료 수집, 규제·정책 데이터셋 관리 | 6.1 Sol, high | outputs |
| `identification_designer` | 식별전략·회귀식·추정 계획 설계, 대안 비교 | 6 Astra, high | outputs |
| `data_engineer` | 데이터 접근 실제 테스트(API 호출, BigQuery dry run), crosswalk pipeline | 6.1 Sol, medium | outputs |
| `verifier` | 새로 등장한 사실(날짜, 문서번호, 수치, 논문 내용)을 1차 자료로 독립 재확인 | 6.1 Sol, high | `state/claims_ledger.csv`만 |
| `referee` | 산출물을 상위 저널 referee처럼 공격하고 blocker를 지정 | 6 Astra, high | `outputs/reviews/`, `state/threat_register.md`(추가만) |

---

## 3. 회차 루프 (모든 회차 공통)

1. **계획:** orchestrator가 상태 파일과 `prompts/round_XX.md`를 읽고, 작업을 역할별로 나눈 계획을 `outputs/round_XX/plan.md`에 쓴다.
2. **생산:** 해당 역할(`lit_scout`, `policy_archivist`, `identification_designer`, `data_engineer`)이 산출물을 만든다. 서로 독립적인 작업은 병렬로 실행한다.
3. **검증:** `verifier`가 이번 회차에 새로 등장한 사실을 전부 `claims_ledger.csv`에 등록하고 독립적으로 재확인한다.
   - `contradicted`(반증됨) 판정이 나오면 그 사실에 기댄 판단은 즉시 blocker가 된다.
4. **심사:** `referee`가 산출물을 심사하고 `outputs/reviews/round_XX_review_N.md`를 쓴다.
5. **수정:** blocker와 major 지적에 대해 생산 역할이 수정한다.
   - designer와 referee 사이의 왕복은 **최대 2회**까지만 한다.
   - 그래도 blocker가 남으면 해결하려고 더 돌리지 말고 사용자에게 escalate한다.
6. **기록:** orchestrator가 다음을 갱신한다.
   - `state/decision_log.md`
   - `state/threat_register.md`
   - `progress_log.md`
7. **보고 후 멈춤:** 대화창에 보고하고 멈춘다(형식은 8절).

---

## 4. 독립성 규칙 (가장 중요)

- **자기 산출물을 자기가 심사하거나 검증하지 않는다.** 작성한 역할과 심사·검증하는 역할은 항상 다른 subagent여야 한다.
- `referee`와 `verifier`에게는 **산출물 파일 경로와 상태 파일만** 넘긴다. 작성자의 추론 과정, 대화 내용, "이 설계가 좋은 이유" 같은 설명은 넘기지 않는다.
- `referee`의 지적을 orchestrator가 임의로 "사소함"으로 낮추지 않는다. 등급을 낮추려면 근거를 리뷰 파일에 덧붙이고, 사용자 보고에 그 사실을 포함한다.
- 여러 subagent가 같은 결론에 도달했다는 사실을 독립적인 증거로 취급하지 않는다. 같은 모델은 같은 맹점을 공유한다.

---

## 5. 상태 파일 규칙

- `research_charter.md`: 사용자만 수정한다. 에이전트는 변경을 **제안**만 할 수 있고, 제안은 `decision_log.md`에 "제안" 항목으로 기록한다.
- `decision_log.md`: 추가만 가능하다(append-only). 과거 항목을 수정하지 않는다.
- `threat_register.md`: 위협을 삭제하지 않는다. status와 대응만 갱신하며, 갱신할 때마다 날짜와 근거 파일을 함께 적는다.
- `claims_ledger.csv`: 설계나 Gate 판정의 근거가 되는 사실은 전부 등록한다.
  - `verified` 상태가 아닌 사실은 핵심 판단의 **유일한** 근거로 쓸 수 없다.
  - 그런 사실을 쓸 때는 "미검증 근거"로 표시한다.

---

## 6. "최적 방향" 판정 기준

대안 연구설계를 비교할 때는 아래 순서로 평가하고, 평가 근거를 표로 남겨라.

1. **질문 충실도:** charter의 연구질문, 특히 실제 제한 이전의 announcement effect에 답하는가? 이 기준을 통과하지 못한 설계는 순위에 올리지 않고 "질문 변경 대안"으로 따로 분류한다.
2. **식별 강도:** threat register의 `critical` 위협을 몇 개, 어떻게 해결하는가? 해결하지 못한 critical 위협을 명시한다.
3. **Novelty:** 가장 가까운 기존 연구와 어디가 다른가? 근거 논문의 확인 수준을 함께 적는다.
4. **실현 가능성:** 한 학기 안에, 확인된 데이터 접근 경로로 가능한가?

기준끼리 충돌하면 결정하지 말고 사용자에게 선택지를 제시하라. 예를 들어 질문 충실도는 높지만 식별이 약한 설계와, 그 반대인 설계가 맞설 때다.

---

## 7. 반드시 멈추고 사용자에게 물어야 하는 경우

- Gate 판정 (Gate 1–4)
- 연구질문 또는 charter 변경 제안
- 되돌리기 어려운 freeze: crosswalk 정의, treatment 정의, primary outcome, 신호 가중치
- 비용이 발생하는 작업: 유료 데이터 구매, 무료 한도를 넘는 BigQuery 스캔, 대량 API 호출
- verifier가 기존 Gate 판정의 근거 사실을 `contradicted`로 판정한 경우

---

## 8. 회차 종료 보고 형식

1. 이번 회차 핵심 결론 (5줄 이내)
2. 완료 기준 충족 여부 (항목별)
3. referee의 blocker와 major 지적, 그리고 각각의 처리 상태
4. verifier 결과 요약 (verified, contradicted, unverifiable 건수와 중요 항목)
5. threat register 변화 (새로 추가된 위협, status가 바뀐 위협)
6. 사용자가 결정하거나 확인해야 할 사항 (선택지와 각각의 추천 근거)

---

## 9. 자동 실행과 차례 규칙

이 repo는 GPT(생산)와 Claude(교차 모델 심사)가 예약 실행으로 번갈아 작업한다.

- 모든 실행은 `state/turn.md`를 먼저 읽는다. 자기 차례가 아니면 아무것도 하지 않고 종료한다.
- 작업을 시작하면 lock을 걸고 커밋·push한다. 끝나면 lock을 풀고 전환 규칙에 따라 next를 정한다.
- 사용량 한도로 언제든 중단될 수 있다. 작은 작업 단위마다 커밋·push한다. 중단된 실행은 다음 실행이 `progress_log.md`에서 이어받는다.
- Claude의 리뷰(`outputs/reviews/*_claude_review_*.md`)는 GPT 내부 referee와 같은 권위를 가진다. blocker는 반영하거나, 반영하지 않는 근거를 리뷰 파일 옆 `*_response.md`에 적는다.
- 사용자의 지시는 `state/user_inbox.md`로만 들어온다.
- GPT 예약 실행의 지시문은 `prompts/gpt_scheduled_run.md`, Claude의 규칙은 `CLAUDE_REVIEWER.md`에 있다.

---

## 10. 연구 태도

`docs/master_prompt.md` 섹션 19의 규칙 21개를 모든 역할에 적용한다. 특히 다음 규칙을 지켜라.

- 사용자가 원하는 결과를 찾아주려고 하지 마라. 아이디어를 살리기 전에 먼저 깨 보아라.
- 확인하지 못한 식별자(DOI, Federal Register 번호, 날짜, table명)를 만들어 내지 마라.
- c×k×t 차원의 교란을 fixed effect로 통제했다고 서술하지 마라.
- 결과를 본 뒤에 treatment, 대조군, outcome 정의를 바꾸지 마라.
