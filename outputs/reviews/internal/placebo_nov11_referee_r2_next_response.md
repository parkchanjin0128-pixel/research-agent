# 내부 심사 대응 — placebo_crosswalk

[독립 심사](placebo_nov11_referee_r2.md) · `/root` · 원문 SHA256 `cf95180f2736920e1bd73c4af26371eb56759ac726fc39cf7a111d1be0c619e4`

두 차례 수정 한도에 도달했고 PCX-02가 남았다. 고정 합성 입력의 재현 증거와 주설계 Pool A의 서술은 보존한다. 이 실행 코드와 Pool C 경계는 확정하지 않으며, 추가 수정이나 보류 뒤 독립 작업 재개를 사용자 결정으로 올린다. 기존 Gate, 연구질문, 자료 접근·효과·MDE 상태는 이 판단으로 바뀌지 않는다.

**결정 범위.** 권고안은 이 위약 달력 실행을 보류하고, 사용자가 승인한 범위에서 주설계·문헌·자료 접근·검정력 점검을 별도로 계속하는 것이다. 꼭 실행해야 하면 월 적격성 자체의 확실성과 제한 세부 상태를 분리하고, 시작·종료의 가능한 순서를 반영하는 테스트에 한해 별도 한 차례 수정 결정을 검토한다. 수정 한도 예외에는 정확한 대상, 전후 해시 및 현재 지적을 묶은 별도 승인이 필요하며 이 문서는 그 승인이 아니다.

- **PCX-01**: 정확점의 공통 비선형 경로와 기존 WLS의 구별을 유지한다. placebo_crosswalk.md §§2–3, 기존 합성 스크립트 자료·지지 검증은 범위 밖이며 기존 고정 회귀 사례만 재현 근거로 보존.
- **PCX-02**: 월 적격과 세부 라벨을 혼동한 반례 및 허용 순서 영역의 내부 시점 반례를 수용한다. 도구 사용 범위를 고정 예제 재현으로 제한하고, 후보 창 판정에 적용하지 않는다. 추가 수정은 사용자 결정 전 보류한다. placebo_crosswalk_calendar_synthetic_nov11.py classify_rule/audit_window; 독립 검증 및 현 심사 별도 수정 승인 시 가능한 모든 이력에서 구속인 경우, 적격 이력이 있는 경우, 불가능한 이력/감사 미완료를 분리하고 두 반례를 모두 고정 테스트한 뒤 새 verifier와 referee를 배정.
- **PCX-03**: 같은 연산자·훈련 분리·공동구간 명세를 후보로 유지한다. placebo_crosswalk.md §4 실제 결과·SESOI·검정력은 보류.
- **PCX-04**: 공유 전이 반례와 저노출·미확인 구분을 유지한다. placebo_crosswalk.md §4 및 기존 합성 스크립트 실제 오염·청정 비교국은 별도 원문과 자료 범위에서 확인.
- **PCX-05**: 같은 판본과 정보시점, 분모·팔별 감사의 명세를 유지한다. placebo_crosswalk.md §1 실제 자료 판본·커버리지·매핑 미확인은 상태에 남김.

```json
{
  "phase": "review",
  "unit_id": "placebo_crosswalk",
  "review_path": "outputs/reviews/internal/placebo_nov11_referee_r2.md",
  "review_sha256": "cf95180f2736920e1bd73c4af26371eb56759ac726fc39cf7a111d1be0c619e4",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "PCX-01",
      "response": "정확점의 공통 비선형 경로와 기존 WLS의 구별을 유지한다.",
      "location": "placebo_crosswalk.md §§2–3, 기존 합성 스크립트",
      "verification_plan": "자료·지지 검증은 범위 밖이며 기존 고정 회귀 사례만 재현 근거로 보존."
    },
    {
      "finding_id": "PCX-02",
      "response": "월 적격과 세부 라벨을 혼동한 반례 및 허용 순서 영역의 내부 시점 반례를 수용한다. 도구 사용 범위를 고정 예제 재현으로 제한하고, 후보 창 판정에 적용하지 않는다. 추가 수정은 사용자 결정 전 보류한다.",
      "location": "placebo_crosswalk_calendar_synthetic_nov11.py classify_rule/audit_window; 독립 검증 및 현 심사",
      "verification_plan": "별도 수정 승인 시 가능한 모든 이력에서 구속인 경우, 적격 이력이 있는 경우, 불가능한 이력/감사 미완료를 분리하고 두 반례를 모두 고정 테스트한 뒤 새 verifier와 referee를 배정."
    },
    {
      "finding_id": "PCX-03",
      "response": "같은 연산자·훈련 분리·공동구간 명세를 후보로 유지한다.",
      "location": "placebo_crosswalk.md §4",
      "verification_plan": "실제 결과·SESOI·검정력은 보류."
    },
    {
      "finding_id": "PCX-04",
      "response": "공유 전이 반례와 저노출·미확인 구분을 유지한다.",
      "location": "placebo_crosswalk.md §4 및 기존 합성 스크립트",
      "verification_plan": "실제 오염·청정 비교국은 별도 원문과 자료 범위에서 확인."
    },
    {
      "finding_id": "PCX-05",
      "response": "같은 판본과 정보시점, 분모·팔별 감사의 명세를 유지한다.",
      "location": "placebo_crosswalk.md §1",
      "verification_plan": "실제 자료 판본·커버리지·매핑 미확인은 상태에 남김."
    }
  ]
}
```
