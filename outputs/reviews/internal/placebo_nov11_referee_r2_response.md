# 내부 심사 첫 수정 대응 — placebo_crosswalk

[독립 심사](placebo_nov11_referee_r1.md) · 원문 SHA256 `048155b24cc81051006bb807df83a1cf1cfeb82e9262c8783cf6ae5615130d4d` · 작성자 `/root`

2차 수정은 남은 PCX-02에 한정한다. 주설계와 비교 명세의 공통 범위는 결과 없는 고정 기대값으로 대조했고, 별도 Pool C는 주설계의 적용 범위 밖이며 월말 경계는 두 해석을 보존했다. 실제 입력·효과는 열람하지 않았다.

- **PCX-01**: 재심에서 해소된 정확점 투영과 기존 WLS를 유지했다. placebo_crosswalk.md §§2–3, 기존 placebo_crosswalk_synthetic_nov11.py 기존 합성 검사를 그대로 실행해 회귀 여부 확인.
- **PCX-02**: 공통 달력 기대 라벨 20례와 양 팔·거래 교집합, 입력 대기/빈 창, 사유 보존과 계산 순서를 고정 검사에 넣었다. Pool C는 별도 민감도이고 두 경계 집합을 병기했다. placebo_crosswalk.md §3 실행 안내, placebo_crosswalk_calendar_synthetic_nov11.py 별도 verifier가 두 문서의 공통 입력/기대값 및 20개 분기와 두 Pool C 출력을 독립 재현.
- **PCX-03**: 해소된 검증·훈련 분리 명세를 유지하고, 달력 고정 검사에 사전창의 경계만 포함했다. placebo_crosswalk.md §4, 신규 코드 pre-window 검사 훈련·위약 연산자 및 실제 추론 정의가 바뀌지 않았는지 대조.
- **PCX-04**: 공유 전이 명세와 기존 반례를 변경하지 않았다. placebo_crosswalk.md §4, 기존 합성 검사 기존 공유 전이 검사를 재실행하고 실제 오염 범위는 미확인 유지.
- **PCX-05**: 양 팔의 동일 정보시점·판본·분모 규칙을 변경하지 않았다. placebo_crosswalk.md §1 기존 명세·자료 미확인 상태 보존을 대조.

```json
{
  "phase": "revision",
  "unit_id": "placebo_crosswalk",
  "review_path": "outputs/reviews/internal/placebo_nov11_referee_r1.md",
  "review_sha256": "048155b24cc81051006bb807df83a1cf1cfeb82e9262c8783cf6ae5615130d4d",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "PCX-01",
      "response": "재심에서 해소된 정확점 투영과 기존 WLS를 유지했다.",
      "location": "placebo_crosswalk.md §§2–3, 기존 placebo_crosswalk_synthetic_nov11.py",
      "verification_plan": "기존 합성 검사를 그대로 실행해 회귀 여부 확인."
    },
    {
      "finding_id": "PCX-02",
      "response": "공통 달력 기대 라벨 20례와 양 팔·거래 교집합, 입력 대기/빈 창, 사유 보존과 계산 순서를 고정 검사에 넣었다. Pool C는 별도 민감도이고 두 경계 집합을 병기했다.",
      "location": "placebo_crosswalk.md §3 실행 안내, placebo_crosswalk_calendar_synthetic_nov11.py",
      "verification_plan": "별도 verifier가 두 문서의 공통 입력/기대값 및 20개 분기와 두 Pool C 출력을 독립 재현."
    },
    {
      "finding_id": "PCX-03",
      "response": "해소된 검증·훈련 분리 명세를 유지하고, 달력 고정 검사에 사전창의 경계만 포함했다.",
      "location": "placebo_crosswalk.md §4, 신규 코드 pre-window 검사",
      "verification_plan": "훈련·위약 연산자 및 실제 추론 정의가 바뀌지 않았는지 대조."
    },
    {
      "finding_id": "PCX-04",
      "response": "공유 전이 명세와 기존 반례를 변경하지 않았다.",
      "location": "placebo_crosswalk.md §4, 기존 합성 검사",
      "verification_plan": "기존 공유 전이 검사를 재실행하고 실제 오염 범위는 미확인 유지."
    },
    {
      "finding_id": "PCX-05",
      "response": "양 팔의 동일 정보시점·판본·분모 규칙을 변경하지 않았다.",
      "location": "placebo_crosswalk.md §1",
      "verification_plan": "기존 명세·자료 미확인 상태 보존을 대조."
    }
  ]
}
```
