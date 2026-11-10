# Round 03 독립 재심 — 비지목 기술 placebo·crosswalk 2차 수정

- 범위: `placebo_crosswalk`만 · 실제 referee: `/root/placebo_r2_referee_nov11` · 2026-11-10 UTC / 2026-11-11 KST.
- 고정 원격 판본: [`a90ffba43a9610b703871704c5f7bdfed3d712d1`](https://github.com/parkchanjin0128-pixel/research-agent/commit/a90ffba43a9610b703871704c5f7bdfed3d712d1) · 보고서 경로: `outputs/reviews/internal/placebo_nov11_referee_r2.md`.
- 원 생산자 `/root/placebo_design_producer_nov09`, 1차 수정 생산자 `/root/placebo_r1_producer_nov11`, 2차 대응 작성자 `/root`, 현 검증자 `/root/placebo_r2_verifier_nov11`, 직전 referee `/root/placebo_r1_referee_nov11`와 별개다. 작성자 대화·추론은 받지 않았다. 아래 고정 파일의 원시 바이트를 받아 Git blob ID를 대조하고 SHA-256을 계산했다.

**판정: `major_revision`.** PCX-01·03·04·05는 후보 명세의 범위에서 해결 상태를 유지한다. PCX-02는 1차 재심이 요구한 고정 사례를 실질적으로 보완했지만, 공통 풀 A의 빈 창 판정에 결과 없는 반례가 있어 열린다. 두 스크립트의 `python3 -B` 실행은 통과했다. 이는 제출된 사례의 통과이며, 실제 날짜·자료나 일반화한 달력 분기의 검증은 아니다. 별도 풀 C의 정확 월말 경계는 주설계 풀 A의 실패 근거가 아니다.

| ID | severity | 위치 (고정 줄) | 문제·증거와 통과 기준 | 상태 |
| --- | --- | --- | --- | --- |
| PCX-01 | major | CW 38–47, 56–66; PY 6–37, 48–75; V 18 | 같은 정확 dose 분포 투영과 기존 구간 WLS를 구분했다. 기존 합성 실행에서 공통 비선형 곡선 차이 0, 한 팔의 기울기 증분 3/7, 지지·입력·rank 분기를 재확인했다. 실제 지지·행공간·추론은 별도 확인이다. | resolved |
| PCX-02 | major | R1 14; RESP 5–8; CW 34, 36, 49–54, 68; MD 11–15, 19–37; CAL 86–101, 132–144, 152–347; V 19–43 | 같은 평가기로 문서 두 곳의 고정 기대값을 대조하는 20개 경계 사례와 교집합·사유·사전창·순서 검사는 통과했다. 아래 재실행에서 확인 탈락이 적격 가능으로 남았고, 별도 입력에서는 실제로 가능한 적격이 누락됐다. 달력 마스크가 주대조와 이후 지지·가중의 대상을 정하므로 주요 지적이다. 통과 기준은 결과 없는 고정 입력으로 **적격 가능성**과 **탈락 사유의 세부 확실성**을 분리하고, 가능한 시각과 출처별 사유를 보존해 두 문서의 기대 창 상태를 독립 재현하는 것이다. | open |
| PCX-03 | major | CW 72–84; MD 43; CAL 269–320; RESP 9 | 같은 연산자·고정 창·훈련 분리와 동시 95% 구간, 허용/반증/판별 불가가 명시됐다. 합성 검사는 사전창만 다루며 (W)에서만 생기는 교란이나 위약의 검정력을 확인하지 않았다. | resolved |
| PCX-04 | major | CW 86–90; PY 40–45, 76–89; RESP 10 | 저노출 적격과 미확인을 구분한다. 공유 전이 합성 반례는 통과했고 안정된 leave-out과 0인 비교국 위약이 오염 부재를 보장하지 않는다. 실제 경로·보정항의 근거는 미확인이다. | resolved |
| PCX-05 | minor | CW 9–26, 99; RESP 11 | 공통 사전 정보시점·당시판·확인된 양의 분모와 양 팔 독립 라벨/누락 감사를 유지했다. 실제 라벨·판본·분모의 비교 가능성은 미확인이다. | resolved |

**독립 재현과 적용 범위.** 1월을 `[a,b)`라 두고 12월은 지목 후 조건 위반, 2–4월은 확인 구속으로 탈락시키면, 한 비지목 거래의 구속 시작이 `a`부터 1월 15일 사이이고 종료 없이 지속하는 경우 가능한 시작일 전부가 1월과 겹친다. 고정 코드에 `Rule("jan_overlap", (a, MID))`를 넣어 `a`와 `MID`를 각각 정확한 시작일로 고정했을 때는 `binding_active`와 `mixed`로 각각 `confirmed_empty`였다. 둘을 하나의 불확실한 범위로 주자 `unknown`, 가능월 1월, `input_pending`이 나왔다(V 20, 24–40). **미상은 제한 형태의 세부 라벨이고 적격성은 확인 탈락**이다. 반대로 같은 고정 틀에서 시작 범위 `[a,b+2초]`, 종료 `b+1초`로 두면 `s<e`를 만족하는 `s=b`도 가능하다. 그런데 CAL 97–100이 부적합한 끝점 조합을 제거하고 내부의 가능한 `s=b`를 보지 않아 `binding_active/confirmed_empty`가 됐다. `s=b`만 정확히 주면 1월 적격이다. 이 경우에는 **적격 여부가 미상**이므로 `input_pending`이다. 이 두 사례는 같은 PCX-02의 문제이며 실제 연구월 판정이 아니다.

두 기대 열은 두 독립 구현이 아니다. CAL 63, 125–128, 174–175는 해제 이력을 입력 플래그로 받으며, 월별 삽입 사례(198–214, 304–306)는 월을 가로지르는 사건·이력의 일관성을 확인하지 않는다. CAL 323–347은 마스크→지지→가중 순서와 마스크 재개방 금지만 검사하며 실제 지지·가중 계산은 하지 않는다. CAL 3의 내부 source pin과 재심 SHA는 다르므로 아래 현재 해시로 확인 범위를 한정했다. 풀 C는 이미 감사된 세 사건 하한의 최솟값만 검사하며 선행 신호 검색 범위나 공통지지가 미확인일 때의 보류는 검증하지 않았다(CW 34; CAL 226–266). 합성에서 월말이 하한과 정확히 같을 때 `b<cutoff`는 12월만, `b≤cutoff`는 12·1월을 허용한다. 주설계의 `out_of_scope`는 풀 C를 적용하지 않는다는 표식이다.

**다음 결정.** 프로토콜 75·92행에 따라 두 차례 수정 뒤 남은 PCX-02를 `decision`으로 보내고 완료로 올리지 않는다. 권고는 풀 A의 두 문서 규칙을 **후보로 보존**, 합성 코드는 통과한 고정 사례에 한정하고 일반 달력 실행·승인을 보류하며, 별도 풀 C 민감도와 정확 월말 경계 선택은 미룬다는 것이다. 사용자가 여기서 더 진행하기를 원한다면 선택 범위는 결과에 접근하지 않는 달력 판정의 보완·독립 재검증으로 한정하고, 풀 C가 필요할 때만 두 경계 중 하나를 사전에 결정한다. 이는 연구 결론, 추정 실행, 규칙 채택 또는 freeze에 대한 요청이 아니다.

**범위 밖과 중단 기준.** 두 연산자는 10%p당 상대 월 건수 기울기의 창 간 변화다. 지목 수준효과·발표 당일 효과·중국 전체 반응·추가 시행효과는 식별하지 않는다. T02/T04/T18의 실제 dose 지지·정책조정 rank와 묶음, T10의 전이, T13의 매핑·당시판·분모/자료 커버리지, T05/T12/T16의 실제 신호·거래별 적용·잔존·청정 월 및 처치 후 선별, T03/T09의 중국 고유 기술×시점 교란은 미확인이다. 결과 귀속 시계, 1차 outcome, MDE·SESOI·추론의 크기·검정력, 문헌·독창성, 전체 회차·Gate는 심사하지 않았다. 실제 분석에서 (1) 양 팔 10%p 지지나 독립 묶음 부족, (2) 거래별 부분 제한·잔존 또는 미확인으로 공통 창 불성립, (3) 비교군 공유 전이 또는 중국 고유 추격·정책과의 분리 불가가 각각 인과 해석의 중단 사유가 될 수 있다. 실제 결과를 열람·집계하거나 규칙·원격 파일을 변경하지 않았다.

| 약어 / 고정 경로 | 원시 SHA-256 |
| --- | --- |
| CW `outputs/round_03/placebo_crosswalk.md` | `93772ce564fe7094d38097ee123edbdc5ddb0d9b35d40052967e2af56f4f63f3` |
| PY `outputs/round_03/placebo_crosswalk_synthetic_nov11.py` | `651d01325c00329c612e37b4c15fbddfd42b788383e6f563a708ce38e5e04a53` |
| CAL `outputs/round_03/placebo_crosswalk_calendar_synthetic_nov11.py` | `44f5ded87030433f6aeb2d90d16fa9a50c189aed577c9bb99833dce30911a719` |
| MD `outputs/round_03/main_design_execution_revision_nov09.md` | `6459028ebff8bb53ce4d61d9170011e8adc87b84acb3702f55279916aed3ae5d` |
| R1 `outputs/reviews/internal/placebo_nov11_referee_r1.md` | `048155b24cc81051006bb807df83a1cf1cfeb82e9262c8783cf6ae5615130d4d` |
| RESP `outputs/reviews/internal/placebo_nov11_referee_r2_response.md` | `e664367646f9d1c47991352075c4b7da525fba636b57b2752fbca2e92d66ed97` |
| V `outputs/round_03/verification_placebo_r2_nov11.md` | `b2b11b002da19114baadd29956a100e5679a4f0b98e86704171521169c7263e7` |
| 프로토콜 `docs/INTERNAL_REVIEW.md` | `cafb08f423c170f0c76646e32db364e1ee95a92dfbe809e690d9e73c0e3dc7b7` |

```json
{
  "verdict": "major_revision",
  "findings": [
    {"id":"PCX-01","severity":"major","status":"resolved","reason":"동일 정확점 분포의 별도 투영 및 기존 구간 WLS를 구분했고 기존 산술과 지지·rank 사례가 통과했다."},
    {"id":"PCX-02","severity":"major","status":"open","reason":"고정 사례는 통과했지만 확정 구속의 세부 라벨 미상에서 빈 창을 입력 대기로 오분류하고, 가능한 시각의 내부 해에서는 반대 오분류도 재현했다. 풀 C 정확 월말은 별도 보류다."},
    {"id":"PCX-03","severity":"major","status":"resolved","reason":"같은 연산자와 위약·lead 창, 훈련 분리, 동시 95% 구간과 판별 불가의 후보 명세를 유지했다."},
    {"id":"PCX-04","severity":"major","status":"resolved","reason":"저노출 적격과 미확인을 구별하고 공유 전이 반례 및 결과 단위 민감도를 보존했다."},
    {"id":"PCX-05","severity":"minor","status":"resolved","reason":"양 팔 공통 사전 정보시점과 당시판·분모, 잠금 후 독립 측정 감사를 명세했다."}
  ]
}
```
