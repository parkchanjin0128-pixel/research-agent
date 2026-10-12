# Research Charter (사용자만 수정)

최종 수정: 2026-10-12 (사용자 결정: 질문 유지, dose 설계를 주설계 후보로 채택)

## 1. 연구질문 (고정)

> 미국이 기술접근을 실제로 차단하기 전에, "앞으로 이 기술을 차단할 수 있다"는 공식 신호 자체가 중국의 자본과 연구역량을 해당 기술로 이동시키는가?

> 기존 연구가 관찰한 '수출통제 이후 중국 혁신 증가' 중 일부는 실제 공급제약이 아니라 anticipatory response였는가?

이 연구의 차별점은 **실제 제한 이전 구간의 announcement effect**다. 이 차별점이 사라지는 설계는 주설계가 될 수 없다.

## 2. 핵심 용어의 운영적 정의

- **신호(signal):** 미국 정부가 특정 기술을 향후 통제 후보로 공식 언급한 사건. 단일 날짜가 아니라 연쇄로 다룬다 (Gate 2 실패, decision_log 참조).
- **China-binding access restriction date:** 중국 측의 해당 기술 접근에 실질적인 추가 제한이 생긴 날. legal control date와 구분한다.
- **Announcement effect:** 첫 신호 이후, China-binding restriction 이전 구간에서 나타난 반응.
  - 현재 주설계에서는 **위협 강도(B_k)별 차등 반응**으로 식별한다.
- **Implementation effect:** China-binding restriction 이후 announcement effect를 넘어서는 추가 반응. 가능하면 restriction intensity별로 구분한다.
- **Persistence effect:** 추가 신호나 실제 통제 없이 반응이 유지되는지 여부.

## 3. 주장 가능 범위

**주장할 수 있는 것**
- 위협 강도가 높은 기술일수록 실제 제한 전에 연구·자본 배분이 더 증가했다 (상대효과, 강도 한 단위당 차등효과).

**가정을 명시해야만 주장할 수 있는 것**
- 수준 효과 ("신호가 중국 전체 투자를 X% 늘렸다"). "위협 강도 0 = 반응 0"이라는 외삽 가정이 필요하다.

**주장할 수 없는 것**
- ANPRM 단일 날짜의 효과
- 중국의 기술적 추격(catch-up) 자체
- 정책당국이 이 연구 결과를 근거로 정책을 바꿨다는 주장 (직접 증거가 없는 한)

## 4. 현재 주설계 후보 (2026-10-12 기준, 3회차에서 검증)

연속 처치(dose) 설계다.
- **Dose B_k:** 미국이 기술 k를 실제로 통제했을 때 중국이 입었을 잠재적 손실. 2013–2017 값으로 사전 고정한다.
- **추정 방식:** 신호 연쇄에 대한 동적 경로 $\beta_\tau$를 추정한다.
- **추격 수렴 대응:** 비지목 기술 placebo를 써서 $\beta_{listed}-\beta_{nonlisted}$를 추정한다.
- **선례:** Pierce & Schott 2016, Handley & Limão 2017, Blume-Kohout & Sood 2013, Moser & Voena 2012.

## 5. 사용자 조건

- 학부 연구, 한 학기
- 실행 환경: ChatGPT Work 또는 Codex
- 판단 회차에는 6 Astra high, 수집 회차에는 6.1 Sol
