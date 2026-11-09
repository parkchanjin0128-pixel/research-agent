# 3회차 근접 문헌 1차 수정본 독립 재심 · 2026-11-09 KST

- 단위 `novelty_recheck` · 단계 `review` · 수정 1회차 재심. 심사자 `/root/nov9_novelty_referee`는 최초 생산자 `/root/november_first_source`, 수정자 `/root`, 현 판본 검증자 `/root/nov9_novelty_independent`, 이전 검증자 `/root/fast_novelty_verify` 및 이전 심사자 `/root/fast_novelty_referee`와 구별된다.
- **판정 `major_revision`.** 이전 지적 NR1과 NR2는 해소됐다. 새로 추가한 근접 문헌 중 He·Lyu의 기본 처치군 정의가 원문과 달라 실질적인 수정이 필요하다. Liu et al.의 식과 표 주석이 지칭하는 시점과 비교군도 분리해야 한다. 현재 두 산출물의 독립 검증은 `partially_verified`다. 판정은 이 문헌 단위의 1차 수정본에 적용한다.

## 확인한 판본과 범위

| 경로 | SHA-256 |
|---|---|
| `outputs/round_03/novelty_recheck.md` | `718f636ed9629821f840ad2f042d26a7fa96bb88a88cf07a21954fcb260230f3` |
| `outputs/round_03/literature_he_lyu_liu_versions_nov09.md` | `a3a92a95392529454d25bce8d8f56d4b9ec05c8e2f8732890f369910aa20767e` |
| `outputs/round_03/verification_novelty_revision_nov09.md` | `56178e09617e5f15b928546bff88addec7dcd41551205b0b42c0cd39b73930ac` |
| `outputs/reviews/internal/novelty_recheck_referee_1.md` | `91f9e72dd802be4f9eff738c083b564b08372722ca4fd4208b26e0e4bd7296b5` |
| `outputs/reviews/internal/novelty_recheck_referee_1_r1_response.md` | `ceb565efe385ae242c1b10ca49ae8893288b89e2ea6d1407e530625ed3f559b8` |

수정 산출물 두 편의 해시는 고정 작업 사본과 발행용 커밋 `60d1e988757bfb867d579582b78b95a4ddad046b`를 대상으로 한 검증 기록과 일치한다. Kang·Shen은 해당 검증 기록과 이전 보고서를 사용했다. He·Lyu 및 Liu June 2026은 제공 PDF의 해시를 다시 계산하고, 해당 PDF의 텍스트 사본에서 처치 정의와 표 주석을 대조했다. 연구헌장 §§1–4, 3회차 A2·B7 및 T19를 비교 범위에 적용했다. [현재 검증](../../round_03/verification_novelty_revision_nov09.md) · [최초 심사](novelty_recheck_referee_1.md) · [1차 수정 응답](novelty_recheck_referee_1_r1_response.md) · [연구헌장](../../../state/research_charter.md) · [3회차 요구사항](../../../prompts/round_03.md)

## 지적별 판정

| ID | 등급 | 위치 | 근거와 판정 | 해결책과 통과 기준 | 상태 |
|---|---|---|---|---|---|
| NR1 | minor | `novelty_recheck.md` 서두와 2026-11-09 후속 절 | 최초 생산 시점을 유지했다. 후속 절에서 Kang·Shen으로 한정한 원문 확인, 첫 심사 `minor_revision`, 당시 수정본 검증·재심 대기를 구분했고 검증과 심사 링크가 맞는다. | 당초 요구를 충족했다. 후속 판본의 검증·재심 상태는 날짜가 있는 별도 기록으로 연결할 수 있다. | `resolved` |
| NR2 | minor | `novelty_recheck.md` 2026-11-09 후속 비교 | Shen의 R&D/총자산은 기업 전체 연구투입이며 Kang의 신규 등록은 산업별 진입 수라고 명시했다. Kang의 기술별 특허와 사전 미·중 상대 특허 역량 층화도 보존했다. 기술별 연구·자본 배분의 사전 강도별 반응과 결과 단위를 구분했다. | 당초 요구를 충족했다. Shen §4.2.2·Tables 1·4와 Kang §4.4.2·Table 4 (3)의 비교다. | `resolved` |
| NR3 | major | `literature_he_lyu_liu_versions_nov09.md` He·Lyu 행 「처치와 비교」 | 현재 문장은 등재 기업 또는 그 자회사·손자회사를 직접 노출로 분류한다. §4.1 p. 5에서 실제 분석 단위는 상장기업이고 그 기업 자신, 자회사 또는 손자회사 중 하나가 등재되면 해당 상장기업을 직접 노출로 분류한다. 자체 명의 등재만 쓰는 명세는 강건성 검정이다. 현재의 「비등재 상장기업」도 자회사 등재로 직접 노출된 상장기업을 간접군에 넣는 것으로 읽힌다. 이 차이는 주요 선행연구의 직접·간접 노출군과 대조군 해석을 바꾼다. | 처치 대상을 해당 상장기업으로 명시한다. 간접군은 같은 최종 지배주주를 공유하는 집단의 직접 노출되지 않은 다른 상장기업, 대조군은 직접 노출 구성원이 없었던 집단의 상장기업으로 구분한다. Fig. 2는 세 집단의 구분, 식 (1)은 간접 처치 더미의 명세로 각각 설명한다. 사건 연도 포함 여부는 서론과 §4.1·Table 1의 표현 차이를 표시하고 코드 확인 전에는 유보한다. §4.1·Fig. 2·식 (1)과 수정 문장을 독립 재대조하면 통과한다. | `open` |
| NR4 | minor | `literature_he_lyu_liu_versions_nov09.md` Liu June 2026 행 「처치와 비교」 및 「시간·배분 측정」 | §5.1 식 (25) 본문은 IPC4 최초 관련 등재와 중국 고객이 없는 미국 기업 또는 미국 공급사가 없는 중국 기업을 쓴다고 서술한다. Table 1 주석은 공급사 첫 하류 중국 고객 등재, Table 4는 중국 기업 자체 등재연도 이후를 적는다. 양쪽 표 주석의 대조군은 동일 IPC4의 다른 자국 특허로 더 넓게 적혀 있다. 현재 문장은 식의 정의를 옮겼지만 실제 보고 계수의 구현상 한계를 밝히지 않았다. | 식의 정의와 Tables 1·4 주석의 문구를 각각 표기하고, 실제 표의 코호트 시계, 사건연도 내 출원 처리, 비교군 필터는 코드 또는 저자 확인 전까지 `unverifiable`로 둔다. 두 표가 등재를 사건으로 삼는다는 공통점과, 해당 식·표에 공식 기술 신호만의 사전 구간 계수가 없다는 제한된 결론을 보존한다. 식 (25)와 표 주석을 다시 대조해 문장별 범위가 분명하면 통과한다. | `open` |

[Kang 출판본 §§4.3–4.4, Tables 2·4](https://doi.org/10.1016/j.jimonfin.2024.103229) · [Shen 출판본 §§4.2·5, Tables 1·4](https://doi.org/10.1016/j.irfa.2024.103510) · [He·Lyu 출판본 §§4.1–4.2, pp. 5–6, Fig. 2 및 식 (1)](https://doi.org/10.1016/j.respol.2025.105311) · [Liu June 2026 §5.1 및 Tables 1·4, 인쇄 pp. 23·42·44](https://doi.org/10.2139/ssrn.7042518)

## 비교 결론의 범위

대조한 Kang·Shen·He·Lyu 출판본과 Liu June 2026 원고의 해당 명세에서는, 공식 기술 신호 이후부터 기술별 실질적인 중국 접근 제한 전까지를 별도 창으로 두고 사전 대미 잠재 손실 강도에 따른 기술 간 연구·자본 배분의 차등반응을 추정한 결과가 확인되지 않는다. Kang의 ANPRM 노출과 사전 기술역량 층화, Shen의 기업 R&D 및 대미 수입 관련 경로, He·Lyu의 집단 내 자원 이동 분석과 Table 6의 기술 M&A·양수 특허, Liu June 2026의 특허 방향 전환은 겹치는 선례다. 별도 ABFER 2025 원고는 등재 발표의 일별 주가 반응과 연간 혁신을 각각 연구한다. 두 Liu 문서 간 공식 판본 관계와 비교표의 구현 세부는 확인 범위 밖이다. T19는 대조한 명세 범위에서 근거가 좁혀졌으며 추가 문헌과 방법론 선례의 대조가 남아 있다. [He·Lyu Tables 6·8–9](https://doi.org/10.1016/j.respol.2025.105311) · [Liu ABFER 2025 원고](https://abfer.org/media/abfer-events-2025/posters/selected-papers/PS25065_Export-Restrictions-and-the-Ripple-Effect_Evidence-from-US-China-Trade-Networks.pdf) · [위협표](../../../state/threat_register.md)

B7에서 Kang의 연간 표·그림은 기술별 제한 전 추정치나 기존 PPML 추정치에 대한 그 구간의 기여분을 복원할 해상도를 갖추지 못했다. 창별 신규 계수의 계산에는 일자·IPC·Patsnap 토픽 분류 및 표본 규칙, 기술·거래별 실질 제한일과 창별 지지가 필요하다. 기존 PPML 효과의 기여분을 주장하려면 같은 표본과 모형에서 반사실 예측량 및 집계 기준도 정의해야 한다. 기간 길이만으로 기여분을 환산할 근거는 없다. [Kang 식 (1)·(3), Table 1 및 Fig. 1](https://doi.org/10.1016/j.jimonfin.2024.103229)

다음 재심은 NR3·NR4의 위치별 응답, 바뀐 두 산출물의 해시와 독립 검증, 수정 횟수의 기존 이력을 기준으로 한다. 이 단위에서 우선 막아야 할 오류는 직접 노출군의 방향 오기, Liu 회귀의 실제 구현 단정, 연간 결과의 사전 창 귀속이다. 실제 접근 제한일, 기술×시점 교란과 추격, 중국 정책, placebo, MDE 및 포기 기준은 별도 설계 단위의 검토 범위다.
