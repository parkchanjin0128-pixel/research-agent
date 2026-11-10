# 내부 심사 첫 수정 대응 — data_feasibility

[독립 심사](round_03_internal_review_2.md) · 원문 SHA256 `c192db894af688f26cc850175eb581e7d9aae6d76791c4321add041eb835ca70` · 작성자 `/root`

이번 수정은 기록된 근거와 판정 규칙을 정리했다. 새로운 실행·결과열람·반출을 하지 않았으며 DF-R01–03 종결은 독립 검증과 재심에서 결정한다. OA-02 반증을 그대로 유지했다.

- **DF-R01**: 이전 TIP 0행 검사·계기판과 Google BigQuery의 미실행·미산정 비용을 분리하고, 별도 실행 조건과 재개 표를 명시했다. feasibility_report.md ‘두 접근 경로의 확인 범위와 재개 조건’ 기존 TIP 메타데이터·조인 기록 대조. 승인 프로젝트와 고정 SQL의 dry run·바이트 및 비용 가정이 실제 확인될 때만 Google 상태 갱신.
- **DF-R02**: 인용과 IP5에 각각 코호트/이용 가능일, 미상, 귀속·중복·분모, 당시판과 범위, 재구성 proxy를 구분했다. feasibility_report.md ‘두 사전 dose 후보의 2017년 말 기준 판정’ 필드 출처 및 날짜 경계 판정 먼저 검증. 시점 복원·라이선스·당시판과 양 팔 표본이 승인될 때만 지지·손실을 실제 확인.
- **DF-R03**: IP5 제3장/제5장/부록의 장·절 명칭과 인쇄면·PDF 위치를 구분했다. feasibility_report.md ‘IP5 정의의 정확한 출처’ 공식 목차와 본문 인쇄 50·78·92쪽 및 귀속·중복 보조 위치 52·55·79쪽 대조.

```json
{
  "phase": "revision",
  "unit_id": "data_feasibility",
  "review_path": "outputs/reviews/round_03_internal_review_2.md",
  "review_sha256": "c192db894af688f26cc850175eb581e7d9aae6d76791c4321add041eb835ca70",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "DF-R01",
      "response": "이전 TIP 0행 검사·계기판과 Google BigQuery의 미실행·미산정 비용을 분리하고, 별도 실행 조건과 재개 표를 명시했다.",
      "location": "feasibility_report.md ‘두 접근 경로의 확인 범위와 재개 조건’",
      "verification_plan": "기존 TIP 메타데이터·조인 기록 대조. 승인 프로젝트와 고정 SQL의 dry run·바이트 및 비용 가정이 실제 확인될 때만 Google 상태 갱신."
    },
    {
      "finding_id": "DF-R02",
      "response": "인용과 IP5에 각각 코호트/이용 가능일, 미상, 귀속·중복·분모, 당시판과 범위, 재구성 proxy를 구분했다.",
      "location": "feasibility_report.md ‘두 사전 dose 후보의 2017년 말 기준 판정’",
      "verification_plan": "필드 출처 및 날짜 경계 판정 먼저 검증. 시점 복원·라이선스·당시판과 양 팔 표본이 승인될 때만 지지·손실을 실제 확인."
    },
    {
      "finding_id": "DF-R03",
      "response": "IP5 제3장/제5장/부록의 장·절 명칭과 인쇄면·PDF 위치를 구분했다.",
      "location": "feasibility_report.md ‘IP5 정의의 정확한 출처’",
      "verification_plan": "공식 목차와 본문 인쇄 50·78·92쪽 및 귀속·중복 보조 위치 52·55·79쪽 대조."
    }
  ]
}
```
