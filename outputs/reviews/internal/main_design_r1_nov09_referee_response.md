# 주설계 재심 대응

- **MDR-01** 같은 주 추정량과 합성 검산을 유지한다. 위치는 main_design.md §§2–4이다. WLS 대조와 기준 월을 확인한다.
- **MDR-02** 기존 주 분석용 양 팔 달력의 적격 규칙을 유지한다. 위치는 main_design_execution_revision_nov09.md §1이다. 주 창과 별도 국소 달력 적용의 경계를 확인한다.
- **MDR-03** 국소 전후 비교에 별도 마스크를 도입하고 날짜 불확실성과 다른 사건 상태를 명시한다. 위치는 main_design_execution_revision_nov09.md §2 미·중 달력상 꺾임이다. 합성 사례에서 최초 미국 신호 전 월을 복원하고, 불명·겹침·보강 해상도 조건과 주 추정량 불변을 확인한다.
- **MDR-04** 기존 위협표와 중단 기준을 유지한다. 위치는 main_design_execution_revision_nov09.md §§3–4이다. 다섯 기준의 입력 대기와 실패 구분을 확인한다.
- **MDR-05** 기존 절편·정규화·인용 수정을 유지한다. 위치는 main_design.md §§2·4·5이다. 고친 문구가 유지되는지 확인한다.

```json
{
  "phase": "review",
  "unit_id": "main_design",
  "review_path": "outputs/reviews/internal/main_design_r1_nov09_referee.md",
  "review_sha256": "c5a3173eff0eef1cf75b7a36f6da8560d0435ce5583d3dcb0d34af3d80f15f42",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "MDR-01",
      "response": "같은 주 추정량과 합성 검산을 유지한다.",
      "location": "main_design.md §§2–4",
      "verification_plan": "WLS 대조와 기준 월을 확인한다."
    },
    {
      "finding_id": "MDR-02",
      "response": "기존 주 분석용 양 팔 달력의 적격 규칙을 유지한다.",
      "location": "main_design_execution_revision_nov09.md §1",
      "verification_plan": "주 창과 별도 국소 달력 적용의 경계를 확인한다."
    },
    {
      "finding_id": "MDR-03",
      "response": "국소 전후 비교에 별도 마스크를 도입하고 날짜 불확실성과 다른 사건 상태를 명시한다.",
      "location": "main_design_execution_revision_nov09.md §2 미·중 달력상 꺾임",
      "verification_plan": "합성 사례에서 최초 미국 신호 전 월을 복원하고, 불명·겹침·보강 해상도 조건과 주 추정량 불변을 확인한다."
    },
    {
      "finding_id": "MDR-04",
      "response": "기존 위협표와 중단 기준을 유지한다.",
      "location": "main_design_execution_revision_nov09.md §§3–4",
      "verification_plan": "다섯 기준의 입력 대기와 실패 구분을 확인한다."
    },
    {
      "finding_id": "MDR-05",
      "response": "기존 절편·정규화·인용 수정을 유지한다.",
      "location": "main_design.md §§2·4·5",
      "verification_plan": "고친 문구가 유지되는지 확인한다."
    }
  ]
}
```
