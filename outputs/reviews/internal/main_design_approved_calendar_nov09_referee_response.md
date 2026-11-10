# 사용자 승인 한정 보완 재심 대응

- **MDR-01** 주 WLS 대조·반사실 추세 조건의 앞선 확인을 보존했다.
- **MDR-02** 주 관측창의 양 팔 거래·결정 시점 규칙의 앞선 확인을 보존했다.
- **MDR-03** 월말 경계의 입력 대기와 확인된 무분리·공통 중간월 분기를 재현해 마지막 계획 지적을 해소했다.
- **MDR-04** 위협표와 중단 기준, 추론·검정력 계획의 앞선 확인을 보존했다.
- **MDR-05** 정규화, 절편 및 인용 범위의 앞선 확인을 보존했다.

```json
{
  "phase": "review",
  "unit_id": "main_design",
  "review_path": "outputs/reviews/internal/main_design_approved_calendar_nov09_referee.md",
  "review_sha256": "9fe7c75da8d00a38026312fc0a225bc605efd1f2603c7226a85c62022038dfed",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "MDR-01",
      "response": "주 WLS 대조·반사실 추세 조건의 앞선 확인을 보존했다.",
      "location": "고정 주설계와 부록, 독립 심사 이력",
      "verification_plan": "실제 적격 창, 지지와 배분 자료는 별도 연구 단위에서 평가한다."
    },
    {
      "finding_id": "MDR-02",
      "response": "주 관측창의 양 팔 거래·결정 시점 규칙의 앞선 확인을 보존했다.",
      "location": "고정 주설계와 부록, 독립 심사 이력",
      "verification_plan": "실제 적격 창, 지지와 배분 자료는 별도 연구 단위에서 평가한다."
    },
    {
      "finding_id": "MDR-03",
      "response": "월말 경계의 입력 대기와 확인된 무분리·공통 중간월 분기를 재현해 마지막 계획 지적을 해소했다.",
      "location": "main_design_execution_revision_nov09.md §2 및 독립 검증·심사",
      "verification_plan": "실제 적격 창, 지지와 배분 자료는 별도 연구 단위에서 평가한다."
    },
    {
      "finding_id": "MDR-04",
      "response": "위협표와 중단 기준, 추론·검정력 계획의 앞선 확인을 보존했다.",
      "location": "고정 주설계와 부록, 독립 심사 이력",
      "verification_plan": "실제 적격 창, 지지와 배분 자료는 별도 연구 단위에서 평가한다."
    },
    {
      "finding_id": "MDR-05",
      "response": "정규화, 절편 및 인용 범위의 앞선 확인을 보존했다.",
      "location": "고정 주설계와 부록, 독립 심사 이력",
      "verification_plan": "실제 적격 창, 지지와 배분 자료는 별도 연구 단위에서 평가한다."
    }
  ]
}
```
