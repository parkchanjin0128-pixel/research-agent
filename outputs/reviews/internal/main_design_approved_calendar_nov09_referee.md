# Round 03 — 주설계 MDR-03 승인 문구 독립 재심

2026-11-10 KST · `main_design` · referee `/root/r3_calendar_approved_referee` · 비교 기준 `6b1be7d3d58a8ef729b67e1d761d12aad1f85e9d`. [AGENTS §4](../../../AGENTS.md)에 따라 작성자 `/root`, 검증자 `/root/r3_calendar_approved_verify`, 이전 재심자와 별도로 심사했다.

**판정 `accept` — 주설계 계획의 MDR-01–05 모두 `resolved`.** 사용자 승인은 실행 부록 §2 46행의 MDR-03 상태 분류 한 문장에 한정됐다. 기준 부록의 SHA-256은 `a511bc25581bede17433e44dbbdda8778fe5ac968932120ec708da8ce59863d8`, 승인본은 `6459028ebff8bb53ce4d61d9170011e8adc87b84acb3702f55279916aed3ae5d`다. 삽입한 문장과 뒤 공백을 제거하면 기준 텍스트와 일치한다. §1 주 창 및 §2 고정 위험집합·가중·WLS·rank 조건은 그대로이며 주설계 본문도 기준 Git blob과 일치했다. 독립 검증 SHA-256은 `7325e84e4b75118c19427b2b704d3e122e2687d011604b945ba8e63c5e1f8347`이다. [승인 기록](../../round_03/main_design_calendar_user_approval_nov09.json) · [결정 메모](../../round_03/main_design_calendar_decision_nov09.md) · [한정 대응](main_design_r2_nov09_referee_scoped_response.md) · [실행 부록 §2](../../round_03/main_design_execution_revision_nov09.md#L46) · [독립 검증](../../round_03/verification_main_design_approved_calendar_nov09.md)

미국 사건을 11월 15일로 고정하고, 별도로 표시한 월 외에는 고정 감사와 가능한 대조의 rank가 충족된다고 가정했다. 완전월의 사전 `b_m ≤ e_lo`, 사후 `a_m > e_hi`, 비대상 사건 노출 상태 동일 조건을 독립 계산했다.

| 합성 중국 사건 또는 거래 조건 | 판정 근거 |
|---|---|
| 가능한 UTC 시각이 12월 31일 23:59:59–1월 1일 00:00:00 | 이른 끝점이면 12월 말이 사건보다 늦고, 늦은 끝점이면 12월 말이 사건과 같아 중간월이 된다. 거래 적용의 미확정으로 12월 적격이 달라지거나 가능한 이력마다 고를 달력이 다를 때도 **입력 대기**, 공동 보고 보류다. |
| 11월 20일 또는 12월 15일로 확정 | 같은 월과 인접월 각각에 중간 완전월이 없다. 확인된 범위의 모든 이력이 이처럼 중간월을 허용하지 않으면 **해상도상 무분리**다. |
| 다음 해 1월 15일로 확정 | 미국 10월→12월, 중국 12월→2월이다. 공통 중간월은 12월이며 비대상 사건의 상태는 각 대조에서 사전/사전, 사후/사후다. 감사와 rank 충족 가정에서 **공동 보고 가능**하다. |

따라서 §2의 새 분기를 포기 기준 3과 함께 적용할 때, 가능한 이력에 따라 판정이 달라지는 빈 달력은 입력 대기이고 범위 전체에서 확인된 부재는 해상도상 무분리다. 보고 가능한 국소 대조도 사건별 인과 분해에는 쓰이지 않는다. [2차 재심](main_design_r2_nov09_referee.md)

| 지적 | 등급 · 상태 | 근거 |
|---|---|---|
| MDR-01 | `critical` · `resolved` | 고정 WLS 대조와 같은 연산자의 반사실 조건 보존. |
| MDR-02 | `critical` · `resolved` | 양 팔의 주 창과 거래·결정일 적격 분기 보존. |
| MDR-03 | `major` · `resolved` | 별도 국소 달력에 입력 대기와 확인된 무분리의 분기가 명시됐고 세 합성 사례에서 판정이 갈린다. |
| MDR-04 | `major` · `resolved` | T01–T19 대응과 다섯 사전 포기 기준 보존. |
| MDR-05 | `minor` · `resolved` | 절편·기준월 해석과 인용 범위 수정 보존. |

심사 범위는 계획 문구다. 실제 사건 시각·거래 적용, 월 적격·rank, 배분 결과와 효과, 설계 채택, 회차 완료 및 Gate는 이 판정의 범위 밖이다.
