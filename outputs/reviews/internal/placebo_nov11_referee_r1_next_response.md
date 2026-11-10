# 내부 심사 대응 — placebo_crosswalk

[독립 심사](placebo_nov11_referee_r1.md) · `/root` · 원문 SHA256 `048155b24cc81051006bb807df83a1cf1cfeb82e9262c8783cf6ae5615130d4d`

현재 재심의 판정을 그대로 기록한다. 네 건은 후보 명세 수준에서 유지하고, 2차 수정은 PCX-02의 결과 없는 재현 자료만 대상으로 한다. 새로운 확정, 효과·MDE 검증 또는 데이터 열람은 포함하지 않는다.

- **PCX-01**: 후보 명세 수준 해소를 수용하고 공통 정확점 투영과 기존 WLS의 구별을 유지한다. placebo_crosswalk.md §§2–3 기존 합성 점검을 재실행하여 회귀를 확인; 실제 지지는 미확인으로 유지.
- **PCX-02**: 지적을 수용한다. 월초 신호, 월말 구속, 교차 미상, 한 거래 부분 제한, 이전 적용 잔존, C 풀 및 사전창 경계, 빈 창과 입력 대기를 고정 입력·기대값으로 재현한다. placebo_crosswalk.md §3 및 동반 결과 없는 fixture/검사 동일 입력으로 문서와 주설계 부록의 마스크 판정, 복수 사유 및 마스크→지지→가중을 fresh verifier가 확인.
- **PCX-03**: 해소 판정을 수용하고 동일 연산자·훈련 분리·공동구간을 유지한다. placebo_crosswalk.md §4 수정 범위 밖임을 대조; 실제 SE/SESOI·검정력은 보류.
- **PCX-04**: 해소 판정을 수용하고 공유 전이 반례와 미상 보정을 유지한다. placebo_crosswalk.md §4 및 기존 합성 검사 기존 공유 전이 테스트를 재실행; 실제 저노출은 미확인.
- **PCX-05**: 해소 판정을 수용하고 동일 판본·시점·팔별 감사 및 미상의 구분을 유지한다. placebo_crosswalk.md §1 수정 범위 밖임을 대조; 실제 자료 판본과 매핑은 미확인.

```json
{
  "phase": "review",
  "unit_id": "placebo_crosswalk",
  "review_path": "outputs/reviews/internal/placebo_nov11_referee_r1.md",
  "review_sha256": "048155b24cc81051006bb807df83a1cf1cfeb82e9262c8783cf6ae5615130d4d",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "PCX-01",
      "response": "후보 명세 수준 해소를 수용하고 공통 정확점 투영과 기존 WLS의 구별을 유지한다.",
      "location": "placebo_crosswalk.md §§2–3",
      "verification_plan": "기존 합성 점검을 재실행하여 회귀를 확인; 실제 지지는 미확인으로 유지."
    },
    {
      "finding_id": "PCX-02",
      "response": "지적을 수용한다. 월초 신호, 월말 구속, 교차 미상, 한 거래 부분 제한, 이전 적용 잔존, C 풀 및 사전창 경계, 빈 창과 입력 대기를 고정 입력·기대값으로 재현한다.",
      "location": "placebo_crosswalk.md §3 및 동반 결과 없는 fixture/검사",
      "verification_plan": "동일 입력으로 문서와 주설계 부록의 마스크 판정, 복수 사유 및 마스크→지지→가중을 fresh verifier가 확인."
    },
    {
      "finding_id": "PCX-03",
      "response": "해소 판정을 수용하고 동일 연산자·훈련 분리·공동구간을 유지한다.",
      "location": "placebo_crosswalk.md §4",
      "verification_plan": "수정 범위 밖임을 대조; 실제 SE/SESOI·검정력은 보류."
    },
    {
      "finding_id": "PCX-04",
      "response": "해소 판정을 수용하고 공유 전이 반례와 미상 보정을 유지한다.",
      "location": "placebo_crosswalk.md §4 및 기존 합성 검사",
      "verification_plan": "기존 공유 전이 테스트를 재실행; 실제 저노출은 미확인."
    },
    {
      "finding_id": "PCX-05",
      "response": "해소 판정을 수용하고 동일 판본·시점·팔별 감사 및 미상의 구분을 유지한다.",
      "location": "placebo_crosswalk.md §1",
      "verification_plan": "수정 범위 밖임을 대조; 실제 자료 판본과 매핑은 미확인."
    }
  ]
}
```
