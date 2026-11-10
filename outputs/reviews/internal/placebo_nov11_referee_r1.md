# Round 03 독립 재심 — 비지목 기술 placebo·crosswalk 1차 수정

- 단위: `placebo_crosswalk`만 · 1차 수정 재심 · 실제 referee: `/root/placebo_r1_referee_nov11` · 2026-11-10 UTC / 2026-11-11 KST.
- 고정 원격 판본: [`b8897c16f934af6b61a676c4b72532197af1b26c`](https://github.com/parkchanjin0128-pixel/research-agent/commit/b8897c16f934af6b61a676c4b72532197af1b26c). 보고서 경로: `outputs/reviews/internal/placebo_nov11_referee_r1.md`.
- 1차 수정 생산자 `/root/placebo_r1_producer_nov11`, 현 검증자 `/root/placebo_r1_verifier_nov11`, 직전 referee `/root/placebo_referee_nov11`, 수정 대응 작성자 `/root`와 별개다. 작성자 대화·추론은 받지 않았다. 아래 여섯 고정 파일만 읽었다.

**판정: `major_revision`.** PCX-01·03·04·05는 후보 설계 명세와 결과 없는 확인의 범위에서 해결됐다. PCX-02의 달력 규칙은 문서와 독립 예제에서 개선·확인됐지만, 완전월·거래별 교집합의 동일 판정을 재현할 고정 테스트가 제출되지 않았다. 이 마스크가 기준·발표 창과 이후 지지·가중의 대상을 모두 정하므로, 문서 예제만으로 기존 major 지적을 닫지 않는다. 현 독립 검증도 `partially_verified`이며 새 지적은 추가하지 않는다.

아래 위치는 모두 고정 판본의 줄 번호다. MD = `outputs/round_03/placebo_crosswalk.md`, PY = `outputs/round_03/placebo_crosswalk_synthetic_nov11.py`, R = `outputs/reviews/internal/placebo_nov11_referee.md`, RESP = `outputs/reviews/internal/placebo_nov11_referee_r1_response.md`, V = `outputs/round_03/verification_placebo_r1_nov11.md`. V가 인용한 주설계 실행 부록·MDE 문서는 그 검증 보고의 범위로만 참조했다.

| ID | severity | 위치 | 문제와 증거 | 해결 기준 또는 남은 시험 | 상태 |
| --- | --- | --- | --- | --- | --- |
| PCX-01 | major | R 11·17; RESP 22–25; MD §§2–3, 36–47·56–66; PY 6–37·48–75; V 18 | 정확층에서 양 팔의 정확한 유리수 dose 점과 10%p 지지쌍을 사용하고 동일 기준 분포에서 두 곡선을 투영한다. 고정 코드 실행에서 기존 기울기 179/100 대 181/100, 공통 이차곡선 차이 0, 한 팔만 가산한 기울기 3/7 복원, 지지 부재·감사 미완료·rank 실패 분기가 모두 통과했다. 기존 구간 WLS는 팔별 선형성에 기대는 다른 투영이며 공통 분포 효과로 읽지 않는다고 구별했다. | 기존 기준 충족. 정확점 분석은 사전 지정한 별도 민감도이며 WLS·MDE를 바꾸지 않는다. 실제 10%p 지지와 묶음 집중, 조정 대조의 행공간 및 추론은 승인 후 별도 확인한다. | resolved |
| PCX-02 | major | R 12; RESP 28–31; MD 34–36·49–54·92; PY 1–94, 특히 48–90; V 12·19–20·26 | 양 팔·모든 국가의 공유 완전월, 선행 조치와 잔존, C 풀 cutoff, 마스크→최종 지지→가중 및 처치 후 선별 한계는 명세됐다. V 19행의 독립 예제도 이를 지지한다. 하지만 제출 코드에는 날짜, 기간, 거래별 구속, 공통 마스크나 빈 창 분기를 받는 경로가 없다. 실행 성공은 그 판정들을 확인하지 않는다. R 12행의 ‘두 파일’은 crosswalk와 주설계 측 규칙의 동일 판정을 뜻하며 Python 구현 자체를 요구한 것으로 읽지 않는다. 현재 누락은 그 일치를 같은 입력과 기대값으로 재현할 고정 검증 자료다. | PY 또는 결과를 쓰지 않는 동등한 고정 fixture/테스트에 MD §3과 주설계 실행 규칙에 대조할 동일 입력·기대 라벨·월 집합을 넣는다. 신호 월초 직전/정확히 월초/월초를 가르는 미상, 구속 월말 정확히/월초 지속/월중 시작·종료/월말을 가르는 미상, 한 팔·한 거래의 부분 제한 및 기준 뒤 해제 이력, C 풀 최초 사건 경계, `R`/위약/lead 공유 사전 조건을 포함한다. 미확인 때문에 가능월이 남은 빈 교집합은 입력 대기, 매 후보월에 확인 위반이 있는 교집합은 확인된 빈 창이어야 한다. 같은 사례에서 사유 보존과 마스크→지지→가중 순서를 재현해 별도 verifier가 현재 해시로 확인하면 종결할 수 있다. | open |
| PCX-03 | major | R 13; RESP 34–37; MD §4, 70–82; V 21 | 공통 기술·국가·dose·정책과 연산자를 가짜 기준/창에도 적용하며, 달력 순번·연속월·학습 분리·계절 겹침·불충분 창 처리를 고정한다. 개별 lead 구간을 위약·편향 투영 구간으로 대체하지 않고 공통 draw의 동시 95% 가족으로 구분한다. 허용/반증/판별 불가가 별도이고 SESOI 미승인은 판별 불가다. | 기존 기준 충족. W에서만 생긴 추격·정책은 이 진단으로 배제되지 않는다. 실제 재표본 크기·해상도·검정력은 별도 MDE 검토다. | resolved |
| PCX-04 | major | R 14; RESP 40–43; MD §4, 84–88; PY 40–45·76–89; V 22 | 직접·1단계 경로와 필수 출처 커버리지로 저노출 후보를 제한하고 미확인을 구분한다. 공유 전이 합성에서 네 leave-out이 모두 1이고 비교국 내부 위약은 0이어도 보정 뒤 중국 지목 반응은 3이다. 같은 지지에서 대안·불확실성을 비교하고 독립 근거가 없으면 보정항을 0으로 두지 않는다. | 기존 기준 충족. 경로 감사와 오염 여부는 미판정이다. 청정 인과 대조가 불가하면 중단하고, 가정 없는 중국 지목 단독 반응을 주장하지 않는다. | resolved |
| PCX-05 | minor | R 15; RESP 46–49; MD §1, 9–26·97; V 23 | 공통 정보시점, 당시 공개·정정·판본, 후보 생성과 코더 훈련/보류 분리, 양 팔 링크 처리와 팔×원천×기술층별 잠금 후 오류·누락 감사가 재현 요건으로 명시됐다. 양의 확인 분모에서만 관측 0을 인정하고 비교 불능 층은 미상으로 둔다. | 기존 기준 충족. 실제 당시판 라벨·정밀도·분모·커버리지 및 최초 신호와의 순서는 입력 확인 때 별도 감사한다. | resolved |

**확인 방법과 범위.** 고정 원시 바이트의 해시를 직접 계산했고 두 산출물은 V 9–10행과 일치했다. `python3 -B placebo_crosswalk_synthetic_nov11.py`는 `PASS: nonlinear shared curve, one-arm increment, support/rank, shared spillover/unknown`을 출력했다. 소스와 AST에서 실행 함수가 `slope`, `common_law`, `contrast`, `classify_exposure`, `main`임을 확인해 달력 테스트의 부재를 별도로 점검했다. 절차상 해결과 실제 위협 해소를 구분한다. T02/T04/T18의 공통 dose 진단, T10의 전이 진단, T13의 측정 감사는 계획 단계다. T05/T12/T16의 실제 제한·청정 창과 처치 후 선별, T03/T09의 중국 고유 기술×시점 교란은 아직 검증되지 않았다. 두 연산자 모두 10%p당 상대적인 월 결과 건수 기울기 대조이며, 지목 수준효과·하루 발표 효과·중국 전체 또는 추가 시행효과를 식별하지 않는다. 문헌·novelty, 실제 기술 매핑·dose 지지·cutoff·청정 월·전이·outcome과 효과, MDE·SESOI·검정력, 전체 회차와 Gate/freeze는 이 판정에 포함하지 않는다. 결과 열람·집계 및 원격 쓰기는 하지 않았다.

**사전 중단 점검.** (1) 실제 정확점 지지·묶음이 부족하거나 기존 WLS와의 차이를 구별할 수 없는 경우, (2) 선행/부분 제한 또는 미확인 기록 때문에 공유 청정 창이 확정되지 않는 경우, (3) 비교군 공유 전이 또는 불정밀한 위약으로 상대 대조의 인과 해석을 뒷받침할 수 없는 경우를 각각 기록한다. 다음 단계는 남은 PCX-02만 2차 수정에서 결과 없는 고정 테스트로 보완하고 새 verifier와 새 referee를 배정하는 것이다. `docs/INTERNAL_REVIEW.md` 75·92행에 따라 2회 후에도 미해결이면 `decision`으로 보내며, 현 상태를 완료로 승격하지 않는다.

| 읽은 고정 경로 | 원시 내용 SHA256 |
| --- | --- |
| `outputs/round_03/placebo_crosswalk.md` | `30e9ee24b16467b48d151b9c3a3f4cc34558682b55d58d37e7a913e0c09bf035` |
| `outputs/round_03/placebo_crosswalk_synthetic_nov11.py` | `651d01325c00329c612e37b4c15fbddfd42b788383e6f563a708ce38e5e04a53` |
| `outputs/reviews/internal/placebo_nov11_referee.md` | `afd2386e62c2b8fa3f40220658db76490cab67048f2f92855b9a9362c02b3061` |
| `outputs/reviews/internal/placebo_nov11_referee_r1_response.md` | `c40ffd8a6188c9fe5507ef9fe1793fb0a0b7c60db3e27d79cb1b196bd2df40a7` |
| `outputs/round_03/verification_placebo_r1_nov11.md` | `b73aa15abe0c2de2ce5b8f8e1f348ff2ecb2c659e0b1094802dee8437756e792` |
| `docs/INTERNAL_REVIEW.md` | `cafb08f423c170f0c76646e32db364e1ee95a92dfbe809e690d9e73c0e3dc7b7` |

```json
{
  "verdict": "major_revision",
  "findings": [
    {"id":"PCX-01","severity":"major","status":"resolved","reason":"동일 정확점 분포 투영을 정의했고 공통 비선형 곡선의 0, 한 팔 증분 3/7 및 지지·rank 실패를 합성으로 재현했다. 기존 WLS와 별개다."},
    {"id":"PCX-02","severity":"major","status":"open","reason":"공유 달력 명세는 독립 예제와 일치하지만 동반 자료에서 경계·부분거래·빈 교집합과 감사 미완료 분기를 같은 입력으로 재현할 고정 테스트가 없다."},
    {"id":"PCX-03","severity":"major","status":"resolved","reason":"같은 위약·lead 연산자, 달력과 훈련 분리, 동시 95% 구간 및 허용·반증·판별 불가를 후보 명세에 고정했다."},
    {"id":"PCX-04","severity":"major","status":"resolved","reason":"저노출 적격과 미확인을 구별하고 공유 전이 반례와 상대 대조의 결과 단위 보정을 명세·합성으로 확인했다."},
    {"id":"PCX-05","severity":"minor","status":"resolved","reason":"양 팔 공통 사전 정보시점·당시판·분모와 잠금 후 독립 팔별 오류·누락 감사 규칙을 명세했다."}
  ]
}
```
