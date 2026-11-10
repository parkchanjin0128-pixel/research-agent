# 내부 심사 대응 — placebo_crosswalk

[독립 심사](placebo_nov11_referee.md) · `/root` · 원문 SHA256 `afd2386e62c2b8fa3f40220658db76490cab67048f2f92855b9a9362c02b3061`

심사 결과는 major_revision이다. 아래는 대응 계획이며 다섯 지적은 모두 열려 있다. 실제 공통지지·시점·효과는 확인하지 않았다.

- **PCX-01**: 공통 기준 분포에 두 조건부 경로를 동일 연산자로 투영하고 양 팔 지원이 비는 범위를 제외한다. placebo_crosswalk.md §§2–3 공통 비선형 X², 불균형 지지, rank 탈락을 각각 합성 재현한다.
- **PCX-02**: 주설계와 R/W 적격 달력을 맞추고 시각·직접 조치 잔존·미상·부분제한의 순서와 마스크를 명시한다. placebo_crosswalk.md §§3–4 양 팔 월 시작·끝 경계 및 고정 가중치가 같은 설계에서 일치하는지 확인한다.
- **PCX-03**: 학습기간과 겹치지 않는 사전 달력에서 본 대조와 같은 연산자로 위약·lead를 계산하고 허용·반증·판별 불가의 기준을 명시한다. placebo_crosswalk.md §§3–4 학습·검정 월 중복, 저검정력 및 사전 추세 위반 예를 각각 점검한다.
- **PCX-04**: 비교국·비지목 기술의 사전 노출 기준을 정하고 공통 오염이 배제되지 않으면 상대 대조로 해석 범위를 제한한다. placebo_crosswalk.md §§2·4 공통 오염을 심은 합성 패널에서 제외 진단의 실패와 해석 제한을 확인한다.
- **PCX-05**: 양 팔별 매핑 오차·분모·미상 규칙을 나란히 감사하고 공통 사전 정보 시점과 정확한 출처를 적는다. placebo_crosswalk.md §1 첫 적격 신호 뒤에 생긴 정보가 어느 팔에도 들어오지 않는지 확인한다.

```json
{
  "phase": "review",
  "unit_id": "placebo_crosswalk",
  "review_path": "outputs/reviews/internal/placebo_nov11_referee.md",
  "review_sha256": "afd2386e62c2b8fa3f40220658db76490cab67048f2f92855b9a9362c02b3061",
  "author_id": "/root",
  "responses": [
    {
      "finding_id": "PCX-01",
      "response": "공통 기준 분포에 두 조건부 경로를 동일 연산자로 투영하고 양 팔 지원이 비는 범위를 제외한다.",
      "location": "placebo_crosswalk.md §§2–3",
      "verification_plan": "공통 비선형 X², 불균형 지지, rank 탈락을 각각 합성 재현한다."
    },
    {
      "finding_id": "PCX-02",
      "response": "주설계와 R/W 적격 달력을 맞추고 시각·직접 조치 잔존·미상·부분제한의 순서와 마스크를 명시한다.",
      "location": "placebo_crosswalk.md §§3–4",
      "verification_plan": "양 팔 월 시작·끝 경계 및 고정 가중치가 같은 설계에서 일치하는지 확인한다."
    },
    {
      "finding_id": "PCX-03",
      "response": "학습기간과 겹치지 않는 사전 달력에서 본 대조와 같은 연산자로 위약·lead를 계산하고 허용·반증·판별 불가의 기준을 명시한다.",
      "location": "placebo_crosswalk.md §§3–4",
      "verification_plan": "학습·검정 월 중복, 저검정력 및 사전 추세 위반 예를 각각 점검한다."
    },
    {
      "finding_id": "PCX-04",
      "response": "비교국·비지목 기술의 사전 노출 기준을 정하고 공통 오염이 배제되지 않으면 상대 대조로 해석 범위를 제한한다.",
      "location": "placebo_crosswalk.md §§2·4",
      "verification_plan": "공통 오염을 심은 합성 패널에서 제외 진단의 실패와 해석 제한을 확인한다."
    },
    {
      "finding_id": "PCX-05",
      "response": "양 팔별 매핑 오차·분모·미상 규칙을 나란히 감사하고 공통 사전 정보 시점과 정확한 출처를 적는다.",
      "location": "placebo_crosswalk.md §1",
      "verification_plan": "첫 적격 신호 뒤에 생긴 정보가 어느 팔에도 들어오지 않는지 확인한다."
    }
  ]
}
```
