# 내부 심사 첫 수정 대응 — placebo_crosswalk

[독립 심사](placebo_nov11_referee.md) · 원문 SHA256 `afd2386e62c2b8fa3f40220658db76490cab67048f2f92855b9a9362c02b3061` · 작성자 `/root`

합성 점검은 실행했으며 실제 결과·매핑·창·검정력은 확인하지 않았다. 기존 주설계의 WLS를 유지한다. 아래는 작성자 대응이며, 해결 여부는 fresh verifier와 fresh referee가 판정한다.

- **PCX-01**: 두 팔의 정확한 공통 dose 분포에서 층별 차이를 투영하는 별도 진단, 10%p 지지, rank·집중 기준을 명세했다. placebo_crosswalk.md §§2–3; 합성 점검 독립적으로 X² 반례와 한 팔 3/7 가산 및 지지 실패를 재현.
- **PCX-02**: 동일 달력과 고정 위험집합 교집합에 월 경계·직접조치·미확인 및 처치 후 선별 규칙을 추가했다. placebo_crosswalk.md §3.1–4 월 시작·종료 경계와 한 팔의 부분 제한을 독립 판정.
- **PCX-03**: 훈련·검증월을 분리하고 같은 연산자 및 중심화·studentize한 공동 95% 구간을 지정했다. placebo_crosswalk.md §4 훈련·검증·위약 달력 비중첩과 동일 연산자·공동 추론 대상을 점검.
- **PCX-04**: 양 팔·국가의 전이 경로와 미상, 저노출 적격, 공유 오염의 상대 반응 보정식을 명세했다. placebo_crosswalk.md §4 양 팔·비교국의 공유 전이; 합성 점검 공유 오염이 제외·가짜 처리에서 드러나지 않는 예와 보정식을 재현.
- **PCX-05**: 양 팔의 동일 사전 판본·이용 가능일·분모 및 잠금 후 독립 표본감사를 명세했다. placebo_crosswalk.md §1 사전 측정 잠금과 팔별 감사 판본, 분류·언어·팔별 누락·정밀도 및 0과 미상을 구분하는지 점검.

```json
{
  "phase": "revision",
  "unit_id": "placebo_crosswalk",
  "review_path": "outputs/reviews/internal/placebo_nov11_referee.md",
  "review_sha256": "afd2386e62c2b8fa3f40220658db76490cab67048f2f92855b9a9362c02b3061",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "PCX-01",
      "response": "두 팔의 정확한 공통 dose 분포에서 층별 차이를 투영하는 별도 진단, 10%p 지지, rank·집중 기준을 명세했다.",
      "location": "placebo_crosswalk.md §§2–3; 합성 점검",
      "verification_plan": "독립적으로 X² 반례와 한 팔 3/7 가산 및 지지 실패를 재현."
    },
    {
      "finding_id": "PCX-02",
      "response": "동일 달력과 고정 위험집합 교집합에 월 경계·직접조치·미확인 및 처치 후 선별 규칙을 추가했다.",
      "location": "placebo_crosswalk.md §3.1–4",
      "verification_plan": "월 시작·종료 경계와 한 팔의 부분 제한을 독립 판정."
    },
    {
      "finding_id": "PCX-03",
      "response": "훈련·검증월을 분리하고 같은 연산자 및 중심화·studentize한 공동 95% 구간을 지정했다.",
      "location": "placebo_crosswalk.md §4 훈련·검증·위약",
      "verification_plan": "달력 비중첩과 동일 연산자·공동 추론 대상을 점검."
    },
    {
      "finding_id": "PCX-04",
      "response": "양 팔·국가의 전이 경로와 미상, 저노출 적격, 공유 오염의 상대 반응 보정식을 명세했다.",
      "location": "placebo_crosswalk.md §4 양 팔·비교국의 공유 전이; 합성 점검",
      "verification_plan": "공유 오염이 제외·가짜 처리에서 드러나지 않는 예와 보정식을 재현."
    },
    {
      "finding_id": "PCX-05",
      "response": "양 팔의 동일 사전 판본·이용 가능일·분모 및 잠금 후 독립 표본감사를 명세했다.",
      "location": "placebo_crosswalk.md §1 사전 측정 잠금과 팔별 감사",
      "verification_plan": "판본, 분류·언어·팔별 누락·정밀도 및 0과 미상을 구분하는지 점검."
    }
  ]
}
```
