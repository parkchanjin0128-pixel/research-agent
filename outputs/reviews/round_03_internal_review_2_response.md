# 특허 자료 접근 심사 대응 · 계획

세 지적은 모두 열린 상태다. 아래 대응은 후속 작업이며, dry run 성공이나 단위 완료를 의미하지 않는다.

- **DF-R01:** 두 후보의 버전 고정 SQL 및 비용 산정 서식을 준비한다. 승인된 실행 프로젝트를 확보할 때까지 실제 처리량·비용을 미확인으로 둔다. 허용된 프로젝트의 tables.get 결과와 후보별 dry run 결과를 확인한다. 결과 조회와 비용 발생을 금지하고, 실패 시 open을 유지한다.
- **DF-R02:** 코호트일과 정보 공개·확정일을 구분한다. 인용과 다섯 관할 충족, 귀속 및 분류에 각각 관측가능일과 근거 버전이 없으면 미확인으로 둔다. 성숙 코호트와 별도 proxy는 강건성 후보로만 둔다. 공식 자료에서 시점 필드와 버전을 재확인한다. 승인된 사전 표본에 한해 정보 유입과 손실·지지 범위를 확인한다.
- **DF-R03:** IP5 제3장·제5장의 장 제목과 절 제목을 분리하고, 부록의 정의와 정확한 인쇄 쪽수를 인용한다. 다른 검증자가 공식 PDF 목차·본문·Annex 2를 재대조한다.

```json
{
  "phase": "review",
  "unit_id": "data_feasibility",
  "review_path": "outputs/reviews/round_03_internal_review_2.md",
  "review_sha256": "c192db894af688f26cc850175eb581e7d9aae6d76791c4321add041eb835ca70",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "DF-R01",
      "response": "두 후보의 버전 고정 SQL 및 비용 산정 서식을 준비한다. 승인된 실행 프로젝트를 확보할 때까지 실제 처리량·비용을 미확인으로 둔다.",
      "location": "feasibility_report.md: 접근 점검 및 재개 조건",
      "verification_plan": "허용된 프로젝트의 tables.get 결과와 후보별 dry run 결과를 확인한다. 결과 조회와 비용 발생을 금지하고, 실패 시 open을 유지한다."
    },
    {
      "finding_id": "DF-R02",
      "response": "코호트일과 정보 공개·확정일을 구분한다. 인용과 다섯 관할 충족, 귀속 및 분류에 각각 관측가능일과 근거 버전이 없으면 미확인으로 둔다. 성숙 코호트와 별도 proxy는 강건성 후보로만 둔다.",
      "location": "feasibility_report.md: 후보별 사전 정보 규칙",
      "verification_plan": "공식 자료에서 시점 필드와 버전을 재확인한다. 승인된 사전 표본에 한해 정보 유입과 손실·지지 범위를 확인한다."
    },
    {
      "finding_id": "DF-R03",
      "response": "IP5 제3장·제5장의 장 제목과 절 제목을 분리하고, 부록의 정의와 정확한 인쇄 쪽수를 인용한다.",
      "location": "feasibility_report.md: IP5 분모·귀속 근거",
      "verification_plan": "다른 검증자가 공식 PDF 목차·본문·Annex 2를 재대조한다."
    }
  ]
}
```
