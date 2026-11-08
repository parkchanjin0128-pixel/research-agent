# 내부 심사 첫 수정 대응 — inference_mde_plan

기준: [독립 심사](round_03_internal_review_4.md) · SHA256 `2a7376b9d6492e30c8e5d6e5b1016ebbe29066b6bf060befd58607c7fe255255` · 작성자 `/root`.

첫 수정에 반영한 내용과 새 독립 검증 계획이다. 이전 심사의 IMDE-01–04가 해소됐다는 판정은 아니다. 실제 자료·적격 창·SESOI·MDE 및 Gate는 미확인 또는 별도 결정 상태다.

- **IMDE-01**: 동일 달력·가중치로 전체월을 자르고 고정 기준월에서 각 경로를 정규화했다. 지목−비지목 대조와 동일 단위 사전 위약 및 추세 투영의 계산, 반사실 가정과 미확인 규칙을 적었다. 위치: inference_mde_plan.md §추정량·짝 달력·반사실 1–4 및 포기 기준 2; threats_tests.md 반론 1·7 재확인: 합성 WLS에서 기준월 변경 불변성, 완전월 경계와 창·사전 추세 대조의 단위를 새 verifier가 대조한다.
- **IMDE-02**: 묶음과 가중치·꼬리·동점·해상도, Holm 전역/부분 귀무, 과대기각 선별과 독립 크기 보정·검증을 구분했다. 명목 크기를 검증하지 못한 사양의 MDE는 판정하지 않는다. 위치: inference_mde_plan.md §입력·추론·시뮬레이션 2–4 재확인: 가상 6묶음의 p값 하한 및 부분귀무 Holm 절차, 표본화와 실패 분모, 다중 모의 시나리오 판정을 독립 산술과 합성 자료로 확인한다.
- **IMDE-03**: 특허·VC별 입력과 승인 상태를 분리하고, 승인된 양의 SESOI에서 80% 동시구간으로 통과·부족·불확실을 나눴다. 방향별 보고·격자 경계·입력 대기와 확인된 적격 창 실패를 명시했다. 위치: inference_mde_plan.md §입력·추론·시뮬레이션 1·5, CR4 상태표 및 포기 기준 4·5; threats_tests.md CR4 재확인: 합성 경계 사례에서 80% 판정, 미도달·불확실 및 승인·입력 미확보를 실제 실패와 구분하는지 새 검증으로 확인한다.
- **IMDE-04**: 정책과 dose 연관을 지지 진단으로 분리하고 편향을 결과 단위로 환산한다. 인지 보강 근거와 비교국 교체의 안정·불안정·판별 불가 규칙을 명시했다. 위치: inference_mde_plan.md §사전 포기 기준 3; threats_tests.md 반론 2·4–6 재확인: 정책 민감도 단위 및 사전 가정, 동일 지지의 국가 교체와 인지 자료 상태에 따른 판정이 재현되는지 별도 확인한다.

```json
{
  "phase": "revision",
  "unit_id": "inference_mde_plan",
  "review_path": "outputs/reviews/round_03_internal_review_4.md",
  "review_sha256": "2a7376b9d6492e30c8e5d6e5b1016ebbe29066b6bf060befd58607c7fe255255",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "IMDE-01",
      "response": "동일 달력·가중치로 전체월을 자르고 고정 기준월에서 각 경로를 정규화했다. 지목−비지목 대조와 동일 단위 사전 위약 및 추세 투영의 계산, 반사실 가정과 미확인 규칙을 적었다.",
      "location": "inference_mde_plan.md §추정량·짝 달력·반사실 1–4 및 포기 기준 2; threats_tests.md 반론 1·7",
      "verification_plan": "합성 WLS에서 기준월 변경 불변성, 완전월 경계와 창·사전 추세 대조의 단위를 새 verifier가 대조한다."
    },
    {
      "finding_id": "IMDE-02",
      "response": "묶음과 가중치·꼬리·동점·해상도, Holm 전역/부분 귀무, 과대기각 선별과 독립 크기 보정·검증을 구분했다. 명목 크기를 검증하지 못한 사양의 MDE는 판정하지 않는다.",
      "location": "inference_mde_plan.md §입력·추론·시뮬레이션 2–4",
      "verification_plan": "가상 6묶음의 p값 하한 및 부분귀무 Holm 절차, 표본화와 실패 분모, 다중 모의 시나리오 판정을 독립 산술과 합성 자료로 확인한다."
    },
    {
      "finding_id": "IMDE-03",
      "response": "특허·VC별 입력과 승인 상태를 분리하고, 승인된 양의 SESOI에서 80% 동시구간으로 통과·부족·불확실을 나눴다. 방향별 보고·격자 경계·입력 대기와 확인된 적격 창 실패를 명시했다.",
      "location": "inference_mde_plan.md §입력·추론·시뮬레이션 1·5, CR4 상태표 및 포기 기준 4·5; threats_tests.md CR4",
      "verification_plan": "합성 경계 사례에서 80% 판정, 미도달·불확실 및 승인·입력 미확보를 실제 실패와 구분하는지 새 검증으로 확인한다."
    },
    {
      "finding_id": "IMDE-04",
      "response": "정책과 dose 연관을 지지 진단으로 분리하고 편향을 결과 단위로 환산한다. 인지 보강 근거와 비교국 교체의 안정·불안정·판별 불가 규칙을 명시했다.",
      "location": "inference_mde_plan.md §사전 포기 기준 3; threats_tests.md 반론 2·4–6",
      "verification_plan": "정책 민감도 단위 및 사전 가정, 동일 지지의 국가 교체와 인지 자료 상태에 따른 판정이 재현되는지 별도 확인한다."
    }
  ]
}
```
