# 사용자 승인 한정 보완 대응

- **MDR-01** 이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다. 근거는 main_design.md 및 실행 부록 고정 부분에 있다. 이전 해시와 정확한 수정 차이를 확인한다.
- **MDR-02** 이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다. 근거는 main_design.md 및 실행 부록 고정 부분에 있다. 이전 해시와 정확한 수정 차이를 확인한다.
- **MDR-03** 허용 가능한 날짜·거래 범위에 따라 적격 여부가 달라지는 경우는 입력 대기, 범위 전체에서 분리 불가일 때 해상도상 무분리로 기록하도록 한 문장을 추가했다. 근거는 outputs/round_03/main_design_execution_revision_nov09.md §2 미·중 달력상 꺾임에 있다. 날짜 구간이 월말을 걸쳐 중간월이 생길 수도 있는 사례, 확정된 겹침, 확정된 공통 중간월을 새 독립 검증과 심사에서 확인한다.
- **MDR-04** 이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다. 근거는 main_design.md 및 실행 부록 고정 부분에 있다. 이전 해시와 정확한 수정 차이를 확인한다.
- **MDR-05** 이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다. 근거는 main_design.md 및 실행 부록 고정 부분에 있다. 이전 해시와 정확한 수정 차이를 확인한다.

```json
{
  "phase": "revision",
  "unit_id": "main_design",
  "review_path": "outputs/reviews/internal/main_design_r2_nov09_referee.md",
  "review_sha256": "a2d558a93d80956b4a953663eb9ed3e0e4d0cdcab54951090ed4cadafb477c1c",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "MDR-01",
      "response": "이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다.",
      "location": "main_design.md 및 실행 부록 고정 부분",
      "verification_plan": "이전 해시와 정확한 수정 차이를 확인한다."
    },
    {
      "finding_id": "MDR-02",
      "response": "이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다.",
      "location": "main_design.md 및 실행 부록 고정 부분",
      "verification_plan": "이전 해시와 정확한 수정 차이를 확인한다."
    },
    {
      "finding_id": "MDR-03",
      "response": "허용 가능한 날짜·거래 범위에 따라 적격 여부가 달라지는 경우는 입력 대기, 범위 전체에서 분리 불가일 때 해상도상 무분리로 기록하도록 한 문장을 추가했다.",
      "location": "outputs/round_03/main_design_execution_revision_nov09.md §2 미·중 달력상 꺾임",
      "verification_plan": "날짜 구간이 월말을 걸쳐 중간월이 생길 수도 있는 사례, 확정된 겹침, 확정된 공통 중간월을 새 독립 검증과 심사에서 확인한다."
    },
    {
      "finding_id": "MDR-04",
      "response": "이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다.",
      "location": "main_design.md 및 실행 부록 고정 부분",
      "verification_plan": "이전 해시와 정확한 수정 차이를 확인한다."
    },
    {
      "finding_id": "MDR-05",
      "response": "이전 독립 심사에서 확인된 해당 명세를 그대로 보존했다.",
      "location": "main_design.md 및 실행 부록 고정 부분",
      "verification_plan": "이전 해시와 정확한 수정 차이를 확인한다."
    }
  ]
}
```
