# Round 03 — 추론·MDE 및 반증 계획 독립 검증

- 단위: `inference_mde_plan` · 실제 verifier: `/root/mde_verifier_nov09` · 생산자: `/root/mde_plan_producer_nov09`. 두 역할은 서로 다르며 고정 queue의 이 단위 이력에는 이전 verifier/referee 기록이 없다.
- 확인 기준: `a6569b89dacf91de4a0aa624bff6a081b166182b` · 확인일 2026-11-08 UTC(2026-11-09 KST) · 예정 보고서 경로 `outputs/round_03/verification_inference_mde_nov09.md`.
- 판정: **`verified` — 해당 버전의 예시 산술, 문헌의 좁은 기술적 인용 및 §12 대응 범위에 한정.** 설계 채택, 실제 검정력·관측창 검증, 반증 성공이나 Gate 판정이 아니다.

| 고정 커밋에서 읽은 경로 | 계산한 SHA-256 |
|---|---|
| `outputs/round_03/inference_mde_plan.md` | `8cb2252b7531ae4a80a6f082e257515e8c46cd7a13d49575d55ca7c15acaf0c9` |
| `outputs/round_03/threats_tests.md` | `8e8a078ea9007a3548fabedf44c28a0792da140ee4a9c3cb04149d7c02a650a8` |
| `AGENTS.md` | `e7bb717d23e8a37ae10d46e1d00fad8a650628cca4460a26d937f32c95254a5c` |
| `docs/INTERNAL_REVIEW.md` | `7a9710675548e804a473760d0d5244115d3ed281c789a27e10e1aec15116fadf` |
| `state/work_queue.json` | `c66eb9468613266f336789b9136e31f0c4dd045c3cdbc6ddd843e983db3a6adc` |

두 산출물은 UTF-8 원바이트의 Git blob SHA-1도 각각 `e57a8cd52dbb027e3369af4baaab691982ab30d8`, `83e765515d945758ad6914e1ae7b01bf6f538f3e`로 원격과 일치하고, 위 SHA-256은 queue 값과 일치한다.

## 산술 독립 재현

월별 공분산 행렬 `R_ij=ρ^|i-j|`의 모든 원소를 합산하고 `h²`로 나누어 평균의 상대 분산을 구했다. 기준과 관측창 평균 사이 공분산을 0으로 놓는 예시에서만 두 분산을 더한다. Student t 분위수는 SciPy로 별도 계산했다. 넓은 지지의 `A(m), A(12)`는 `0.322568, 0.1462585079`, `t(.9875,11)+t(.80,11)=3.468622661`; 좁은 지지는 `0.680000, 0.2813633741`, `t(.9875,5)+t(.80,5)=4.082925230`이다.

| 가정 | SE 재계산 | MDE 재계산 | 표의 반올림 |
|---|---:|---:|---:|
| 특허·넓음 | 0.790633930 | 2.742410764 | 0.791 / 2.74 |
| 특허·좁음 | 2.668559570 | 10.895529196 | 2.669 / 10.90 |
| VC·넓음 | 0.118595089 | 0.411361615 | 0.119 / 0.41 |
| VC·좁음 | 0.400283935 | 1.634329379 | 0.400 / 1.63 |

**verified.** 비율형 B의 0.10은 10%p이고 가상 규모 20건과 2건의 10%는 각각 2건과 0.2건/월이다. 0.2건/월을 고정 구성에서 5개월 합산하면 기술당 평균 1건이다. 제시된 t 분위수 합은 명시대로 근사다. 일반적으로 두 창이 상관되면 차이 분산에는 `−2Cov`가 추가되며, 실제 잔차화 설계의 분산은 이 예시 공식으로 검증하지 않았다.

## 원문 대조와 판정

| 확인 대상 | 직접 읽은 1차 자료 및 위치 | 관찰과 판정 |
|---|---|---|
| 불균형 묶음과 소수 처치묶음에서 표준 오차·wild bootstrap의 성능 문제 | [MacKinnon–Webb, Queen’s QED WP 1314, 저자 정정판 PDF](https://qed.econ.queensu.ca/pub/faculty/mackinnon/working-papers/qed_wp_1314.pdf), 2019-09-18 본문 Abstract, §2 단계 4–6, §4–5; [학술지 DOI 10.1002/jae.2508](https://onlinelibrary.wiley.com/doi/10.1002/jae.2508/full) | **verified.** 저자 모의실험에서 불균형 묶음의 CRVE 과대기각 문제와 처치묶음이 적을 때 wild bootstrap의 실패가 보고된다. §4의 연속 회귀변수 모의와 §5의 이진 처치 DiD 모의는 구별된다. 어느 쪽도 현재 연속 노출 설계의 실제 크기를 보장하지 않는다. |
| 묶음별 Rademacher 가중치와 Webb 가중치 민감도 | [MacKinnon–Webb WP 1314](https://qed.econ.queensu.ca/pub/faculty/mackinnon/working-papers/qed_wp_1314.pdf) §2 단계 4–6; [Webb, Queen’s QED WP 1315, 2014-11-13](https://econ.queensu.ca/working_papers/papers/qed_wp_1315.pdf), 식 (4)와 바로 뒤 문단, 모의결과 Table 2 | **verified.** 두 점 또는 여섯 점의 가중치 후보와 각각의 배정 수를 뒷받침한다. 두 점의 `2^G`는 벡터 수이며, 양측 부호 대칭과 동점 때문에 고유한 `abs(t)` 수는 더 적을 수 있다. 정확한 해상도·동점 처리와 성능은 실제 사양에서 점검할 항목이다. |
| 두 1차 후보에 Holm 가족 0.05를 쓰고 예시에서 후보별 0.025를 쓰는 구분 | [Holm (1979), Scandinavian Journal of Statistics 6:65–70, 원문 스캔](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf), §2, Scheme 1 및 Theorem 1, pp. 66–67 | **verified.** 정렬된 두 검정의 임계값은 0.025, 0.05이며 개별 p값의 유효성이 전제다. 고정 0.025는 예시의 보수적 임계값이다. 전역 영가설 모의만으로 일부 귀무가설이 참인 조합에서의 실제 가족 오류율까지 입증되지 않는다. |
| 원 반론 일곱 개와 반증표의 항목 대응 | [고정 커밋 `docs/master_prompt.md` §12](https://github.com/parkchanjin0128-pixel/research-agent/blob/a6569b89dacf91de4a0aa624bff6a081b166182b/docs/master_prompt.md) | **verified (범위 대응만).** 세계 기술 추세, 선행 중국전략, 무역전쟁, 인지, 동시 중국 정책, 비교국 반응, 선행 기대를 각각 찾았다. 각 위협이나 실제 노출의 해소는 검증하지 않았다. |

WP 1314의 문서 링크인 Queen’s 기관 소개 페이지는 직접 열기에서 시간 초과가 났으나, 저자 정정판 전체 PDF와 출판본 서지·요약으로 대체 확인했다. 정정판의 초록 앞 표기와 초록 아래 정정 고지에 따르면 일부 구판 모의의 상관 입력에 오류가 있었으므로 여기서는 정정판의 결론 범위만 채택했다.

## 제안과 실증 미확인 항목

- 공통지지·동일 crosswalk, 기술별 완전월, 양방향 80% 검정력, SESOI·0.5배 편향 허용치, 모의 반복 수, 0.065 상한, outcome·검정 가족은 사전 **제안**이다. 0.065 상한 선별은 5% 수준이 보장되었다는 뜻이 아니다. PPML의 `exp(θ)−1`도 명시한 로그 대조의 배율 변환이며 절대 건수 또는 일반 수준효과가 아니다.
- B 재배정은 확률적 배정 기제와 sharp null이 없는 한 진단용 placebo라는 제한을 유지한다. 블록의 실제 교환 가능성이나 모의 검정의 크기는 확인하지 않았다.
- 실제 중국 구속 cutoff·동시조치·월수, 날짜/공시 지연과 0·결측, 사전 규모·잔차와 독립 묶음, mapping 오차와 지지는 실증 입력이 없어 이 검증 범위 밖이다. CR1의 실제 granule·페이지, CR2의 가까운 논문 재현 가능성, CR3의 NSFC 커버리지와 CR4의 실제 MDE도 미해결이다. 자료·출처 확보는 각 담당 단위에서 별도로 한다.
- 새 ledger 상태 변경을 제안하지 않는다. 이 보고서는 T13–T17·T21의 진단 계획을 뒷받침하지만 위협을 해소하거나 기존 claim의 확인 범위를 넓히지 않는다. 배분 outcome을 열람하지 않았고 비용 발생 호출이나 원격 쓰기를 하지 않았다.
