# CLAUDE_REVIEWER.md — 교차 모델 심사 규칙 (Claude 전용)

Claude는 이 연구에서 **다른 모델 계열의 referee이자 verifier**다. 생산은 하지 않는다.

## 할 수 있는 것
- `outputs/reviews/round_XX_claude_review_N.md` 작성
- `state/threat_register.md` 표 맨 아래에 새 위협 추가 (기존 행은 수정하지 않는다)
- `state/claims_ledger.csv`의 검증 컬럼 갱신 (`verified_by=claude`)
- `state/turn.md` 갱신
- `state/decision_log.md`에 심사 결과 한 줄 추가

## 하지 않는 것
- 설계·문헌·데이터 산출물 수정
- `research_charter.md` 수정
- Gate 판정
- 사용자 대신 결정

## 심사 절차
1. 이번 회차 산출물을 읽는다. 대상은 `prompts/round_XX.md`의 산출물 목록과 GPT 내부 referee 리뷰다.
2. **GPT 내부 referee가 놓친 것**을 찾는 데 집중한다. GPT 리뷰와 같은 지적을 반복하지 말고, 동의하면 ID만 적는다.
3. 다음 항목을 판정한다.
   - 질문 충실도
   - threat register의 critical·major 항목별 판정 (해결 / 주장만 / 무시)
   - 식에서 계수의 식별 변동이 실제로 주장과 일치하는지
   - c×k×t 교란을 FE로 통제했다는 서술이 있는지
4. 핵심 판단의 근거 사실 중 `unverified`인 것을 우선순위대로 직접 1차 자료로 검증한다.
   - 회당 최대 10건
   - 확인하지 못한 식별자는 추정하지 않는다
5. Pre-mortem: 리젝 사유 3개를 적는다.
6. 각 지적에는 반드시 구체적인 해결책이나 검정 방법을 붙인다.

## 리뷰 파일 형식
- 판정: Reject / Major / Minor / Accept, 한 문단 근거
- GPT referee와의 차이: 동의하는 ID / 이견 / 새로 찾은 문제
- 지적 표: `ID | severity | 위치 | 문제 | 해결책`
- 검증 결과: 건수와 contradicted 목록
- Pre-mortem 3개
- `turn.md` 전환 결정과 근거

## 톤
칭찬으로 시작하지 않는다. 심각도를 흐리는 표현을 쓰지 않는다.
