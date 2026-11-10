# Round 03 — placebo·crosswalk R2 독립 검증

- 실제 독립 검증자: `/root/placebo_r2_verifier_nov11` · 2026-11-10 UTC / 2026-11-11 KST. 생산자·직전 verifier·referee와 별개이며 생산자 대화·추론을 열람하지 않았다.
- 저장소: `parkchanjin0128-pixel/research-agent` · 검증 판본 [`b8c66b26adc98ac6308af5b59556e15441292599`](https://github.com/parkchanjin0128-pixel/research-agent/commit/b8c66b26adc98ac6308af5b59556e15441292599). 아래 다섯 파일만 해당 커밋에서 원시 바이트로 읽었다. Git blob 해시도 응답의 blob ID와 대조했다.

| 약어 | 파일 | SHA-256 |
|---|---|---|
| CW | `outputs/round_03/placebo_crosswalk.md` | `93772ce564fe7094d38097ee123edbdc5ddb0d9b35d40052967e2af56f4f63f3` |
| PY | `outputs/round_03/placebo_crosswalk_synthetic_nov11.py` | `651d01325c00329c612e37b4c15fbddfd42b788383e6f563a708ce38e5e04a53` |
| CAL | `outputs/round_03/placebo_crosswalk_calendar_synthetic_nov11.py` | `44f5ded87030433f6aeb2d90d16fa9a50c189aed577c9bb99833dce30911a719` |
| MD | `outputs/round_03/main_design_execution_revision_nov09.md` | `6459028ebff8bb53ce4d61d9170011e8adc87b84acb3702f55279916aed3ae5d` |
| R1 | `outputs/reviews/internal/placebo_nov11_referee_r1.md` | `048155b24cc81051006bb807df83a1cf1cfeb82e9262c8783cf6ae5615130d4d` |

**판정: `partially_verified`.** 두 스크립트는 고정 해시에서 `python3 -B`로 통과했다. 제출된 공통 풀 A 경계 예와 독립 계산은 대체로 일치한다. 다만 확인된 제한의 세부 라벨만 불명인 경우를 적격 가능으로 잘못 남기는 반례가 있어 공통 달력의 빈 창 판정 전반을 검증 완료로 올리지 않는다. 풀 C의 두 판독은 재현됐으며, 정확한 경계 선택은 보류 상태다. 주설계 풀 A는 C 판정의 적용 범위 밖이다.

| claim | source (고정 줄) | result |
|---|---|---|
| 기존 산술과 전이 예제의 재현 | CW 38–45, 56–66, 84–88; PY 6–45, 48–90 | **확인.** 실행 통과. 가중 쌍별 차분으로 별도 계산한 기존 기울기 179/100·181/100, 공통 이차곡선 차이 0, 한 팔 가산 기울기 3/7이 일치했다. 지지 부재·입력 대기·rank·공유 전이 분기도 제출 실행에서 통과했다. |
| 같은 입력의 공통 완전월과 거래 교집합 | R1 14; CW 49–54, 68; MD 13–37; CAL 152–222 | **제출 사례 확인.** 양 문서의 기대 열을 한 평가기에 대조한 20개 합성 행이 통과했다. 독립 UTC 비교에서 월초 직전·정확히 월초·양쪽에 가능한 지목 신호는 각각 `eligible`·`outside_signal`·`unknown`. 월말 시작은 적격, 한 초 전 시작·월중 종료는 `mixed`, 월 전체 구속은 `binding_active`. 월말을 가르는 적용 가능성은 적격·비적격이 모두 가능하다. 다른 후보월이 확인 탈락이고 1월의 단일 거래만 차이를 만들면 청정은 `W={2019-01}`, 적격 가능성만 남으면 입력 대기, 확인 제한은 확인된 빈 창이다. 복수 사유 및 출처 표식도 보존된다. |
| 확인된 제한과 세부 상태의 미상을 구별 | CW 52–53; MD 13, 15; CAL 86–101, 132–144, 198–216 | **불일치.** 아래 반례에서 어떤 날짜를 택해도 구속이 1월에 겹친다. 제한의 세부 라벨만 `binding_active` 또는 `mixed`로 바뀐다. 따라서 두 문서상 1월도 확인 탈락이며, 나머지 월도 확인 탈락이면 `confirmed_empty`다. 제출 코드는 두 라벨을 `unknown`으로 합치고 1월을 `possible`에 넣어 `input_pending`으로 반환했다. |
| 같은 사전 기준과 고정 순서 | CW 36, 53, 72–81; MD 11, 15, 43; CAL 269–347 | **제출 사례 확인.** 최초 사건 하한이 2018-12-01이면 독립 월 순번으로 R=2017-12–2018-11, P=2017-10–11, Q=2016-10–2017-09, V=2016-10–2018-11. 하한이 직전 초까지 가능하면 각각 1개월 앞당겨진다. P의 확인 제한·Q의 미상 잔존은 제출 예에서 Q/P/V를 보류했다. 지지·가중은 호출 순서만 점검하고, 제거된 거래가 달력을 다시 열지 않는 것을 확인한다. |
| 풀 C 최초 사건 경계와 범위 | CW 34, 53, 68; MD 11; CAL 226–266 | **두 판독 확인·경계 미결.** 세 후보 중 최소 감사 하한을 쓰는 코드이며 각 유형이 가장 이른 경우를 대조한다. 2019-02-01 00:00 UTC의 한 초 전이면 12월만, 한 초 후면 12월·1월을 두 판독이 허용한다. 하한이 정확히 월말이면 엄격한 `b<cutoff`는 12월만, 반개구간의 `b≤cutoff`는 12월·1월을 허용한다. MD는 주설계 풀 A의 범위만 확인했으며, CAL의 `out_of_scope`는 범위 표식이다. |

재현 입력: 1월은 `[2019-01-01T00:00:00Z, 2019-02-01T00:00:00Z)`. 모든 고정 칸은 검증되었고 한 비지목 비교국 거래만 1월 1일 00:00부터 1월 15일 00:00 UTC 사이에 실제 구속이 시작돼 월말까지 지속된다. 12월은 지목 후 조건 위반, 2–4월은 같은 거래의 확인된 제한으로 탈락한다. CAL의 `CLEAN`을 바탕으로 2월 1일에 시작하는 고정 구속을 모든 월에 제공하고, 1월 그 거래에만 다음 규칙을 추가해도 결과는 같다.

```python
from dataclasses import replace
from runpy import run_path
f = run_path("outputs/round_03/placebo_crosswalk_calendar_synthetic_nov11.py")
a, b, mid = f["A"], f["B"], f["MID"]
rule = f["Rule"]
base = replace(f["CLEAN"], rules=(rule("feb_binding", (b, b)),))
jan = replace(base, rules=base.rules + (rule("jan_overlap", (a, mid)),))
overrides = {(i, f["N"]): base for i in f["W_CANDIDATES"]}
overrides[f["JAN"], f["N"]] = jan
rows, good, possible = f["audit_window"](f["W_CANDIDATES"], overrides, "W")
print(rows[f["JAN"]][f["N"]], good, tuple(map(f["key"], possible)),
      f["window_status"](good, possible))
# (('unknown', 'jan_overlap'),) () ('2019-01',) input_pending
# 문서상: 확인된 구속, 적격월·가능월 모두 없음 -> confirmed_empty
```

검증의 한계: CAL 63, 125–128의 기준 뒤 해제 이력은 입력 플래그로 주어져 기준창과 사건에서 도출되지는 않는다. CAL 198–214, 304–306의 일부 제한 예도 월별 삽입이라 시작·종료 이력의 월간 일관성을 검증하지 않는다. CAL 226–259는 C의 세 감사 하한이 주어진 경우만 실행하며 선행 신호 범위·공통지지 미확인 시 보류(CW 34)는 시험하지 않는다. CAL 3의 내부 source pin은 검증한 제출 커밋과 다르므로 이 보고는 위 다섯 파일의 현재 해시로만 범위를 고정한다. 실제 입력·시계·구속·청정 월·지지·효과, 크기·검정력, 인과 주장, 재심 적합성 및 전체 회차 판정은 검증하지 않았다. 실제 결과에 접근하거나 원격으로 쓰지 않았다.
