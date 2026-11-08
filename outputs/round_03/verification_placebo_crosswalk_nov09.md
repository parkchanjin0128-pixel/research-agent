# Round 03 — 비지목 placebo·crosswalk 독립 검증

- 단위: `placebo_crosswalk` · 단계: verification · 검증자: `/root/placebo_verifier_nov09_fresh` · 생산자: `/root/placebo_design_producer_nov09`와 별개. 고정 큐의 이 단위에는 이전 verifier/referee 판단 기록이 없다.
- 검증일: 2026-11-08 UTC / 2026-11-09 KST. 고정 커밋: [`7c2157cf5b775d38512f3df17d52dd52037e0b91`][commit]. 이 보고서의 저장 예정 경로: `outputs/round_03/verification_placebo_crosswalk_nov09.md`.
- 대상: [`outputs/round_03/placebo_crosswalk.md`][artifact]. GitHub 원시 바이트(18,558바이트)의 SHA256은 `fd254a54695de30dd2b1e406b637c350383577622451c6b01ec474d206b154f0`이고 [작업 큐][queue]의 해당 단위와 정확히 일치한다. Git blob SHA는 `c14af4a69a45bb1db4a8832df528dbe41187a1dd`다.

**사실 검증 판정: `not_applicable` (새 외부 사실 0건).** 이 파일의 추가 내용은 향후 감사·측정·추정의 후보 규칙과 조건부 대수다. 특정 기술의 지목·미지목 또는 미제한 여부, 정책·규제의 구속일, 비교국의 노출 상태, 자료 접근·분류 성능, 실제 분자·분모나 분석 가능한 월, 효과 또는 검정력을 확정한 문장이 없다. 2013–17, 2013–16, 2018-12–2019-04, 임계값 및 국가 목록은 사전 기준·민감도·감사 대상으로만 읽힌다. ANPRM과 비교 텍스트의 형태 차이는 측정 결과가 아닌 눈가림 설계의 위험이다. 미국을 정책 주체로 취급하는 것은 기존 질문과 §6-1(3)의 범위이며, 각국의 반응 방향은 조건부 설명이다. 도입부의 작업 범위 표시는 생산자의 기록이고, 검증자는 자기 검증 작업에서 배분 outcome을 열람·집계하지 않았다. N/A를 자료나 식별의 검증, 혹은 심사 통과로 쓰지 않는다.

| 문서 위치 | 고정 출처 및 정확한 위치 | 확인과 한계 |
| --- | --- | --- |
| §1: 동일 매핑·사전 dose | [헌장][charter] §§2–4, [회차 지시][round] B1·B4, [원 지시][master] §10, [주간 계획][week] 직접 지시 3번 | 같은 분류 깊이·동일 후보 생성/수동 판정과 누락·분모 규칙, 사전 cutoff와 과거 판본을 제안한다. 두 사람 코딩·확률 검증 표본·precision/recall 및 threshold 민감도는 절차다. 실제 분류 판본·다국어 모델·검증 표본 크기·라벨·오차 추정과 사용 가능 범위는 명세·검증 대상이다. 회차 B1의 ECRA 원문 주장 C003은 이 파일에 제기되지 않았다. |
| §§2–3: 풀과 달력 | [원 지시][master] §6-1(2)–(4), [주간 계획][week] 직접 지시 3번 및 제한 전 창과 비교, [헌장][charter] §§2–4 | 세 대조 풀을 후보로 나눈다. 비지목의 신호일을 만들어내지 않고 같은 달력을 쓰며, 후속 지목은 그 이전 선행 신호·제한의 부재를 보장하지 않는다. 2018-12–2019-04를 확인된 깨끗한 창이나 확정 cutoff로 쓰지 않는다. 자료 부족과 감사로 확인한 빈 창을 구분한다. |
| §4: censor·비교국·선행 정책 | [원 지시][master] §§6-1(3)–(4), 6-2, [회차 지시][round] B4·B9, [2회차 규제 코딩 기준][coding] 날짜·intensity 절, [위협 등록부][threats] T02/T03/T04/T05/T09/T10/T12/T13/T16/T18 | legal과 China-binding을 분리하고 확인된 intensity 0을 censor하지 않으며, ≥1/≥2 및 부분통제·표본 선택을 별개로 점검하자는 후보 규칙이다. [규제표][reg] 1행의 식별자·날짜 열과 [창 감사][audit] 1행의 `NOT clean window` 표기를 확인했다. 이는 데이터 구조 대조에 한하며 규제 행의 진위나 미제한 사실을 확인하지 않았다. |
| §§3–4: 월 기울기·위약·단위 | [헌장][charter] §4, [회차 지시][round] B4, [주간 계획][week] 직접 지시 3번, [내부 리뷰 4][review4] IMDE-01/04 | 짝지은 달력, 기준 정규화, 반사실 편향 대조의 단위를 검토했다. IMDE-01/04의 해결 판정, 실제 동시구간, SESOI·MDE 평가 및 인과 해석은 이번 범위 밖이다. |

합성 검산만 수행했다.

1. **계수와 정규화.** 다른 두 하위항을 둔 선형 WLS에서, 중국−비교국의 비지목 dose 기울기는 $b_m$, 지목 기울기는 $b_m+d_m$이어서 차이는 $d_m$이다. 월별 $C D_m L$, $C D_m X$, $C D_m L X$의 각각의 전체 월 합은 시불변 $C L$, $C X$, $C L X$여서 $c\times k$ FE에 흡수된다. 고정 구성에서 경로별 기준월 하나를 제외하고 그 월 계수를 0으로 복원한 뒤 $R$의 평균을 빼면 기준월 선택에 불변인 대조가 된다. 중국과 비교국 2개, 기술 11개, $R=0,\ldots,11$, $W=12,13,14$의 결정론적 합성 패널에서 $c\times k,c\times t,k\times t$ FE와 세 상호작용을 함께 적합했다. $d_m$의 생성 기울기 0.5에서 제외 기준월 0과 6 모두 $\theta_y=3.75$, 선형 편향 투영 $0.5(13-5.5)=3.75$였다. $B$가 0–1 비율이면 $X=B/0.10$의 한 단위는 10%p다. 결과를 건수 **수준**으로 둔 WLS에서 $\theta_y$는 10%p당 기술·국가·월 건수의 차등 변화이고 월 누적값이나 로그 링크 계수가 아니다. PPML을 추후 쓰면 건수 해석에는 별도 예측값 대조가 필요하다.
2. **고정 가중치.** 합성 층×dose 셀 두 개의 기술 수를 지목 (3, 2), 비지목 (2, 4)로 두었다. 양쪽이 남은 셀에 $q_h$ 합 1을 부여하면 $q=(5/11,6/11)$이고, 각 셀·각 팔에서 기술 가중치 $q_h/n_{lh}$의 합이 동일하게 $q_h$였다. 기술 가중치를 월과 국가에 고정하고 비교국에 고정 국가 가중치를 부여했다. 같은 셀 질량이나 매칭 허용 거리만으로 실제 10%p 지지와 FE 조정 뒤의 순위가 보장되지는 않는다. 위 결과는 선형 대수 검산이며 실제 표본이나 지지를 검증하지 않았다.
3. **분모와 미상.** 같은 적격 모집단과 단위에서 $0\leq N\leq D$이고, $U$가 따로 계수한 국가 미상 가중치이며 $D+U>0$일 때만 $N/(D+U)$와 $(N+U)/(D+U)$가 해당 국가 귀속 극단이다. 합성 $N=2,D=10,U=5$에서 $B=1/5$, 극단은 $2/15$와 $7/15$다. 관측범위가 확인된 $N=0,D>0$에서만 관측 0이다. $D=0$인 관측 비율은 미정의다. $D=0,U>0$에서 $[0,1]$은 미상 가중치에 대한 시나리오일 뿐 관측 0이 아니며, $D+U=0$이면 그 구간도 계산할 수 없다. 이 식은 미관측 출원·인용·원천 자체에 대한 경계가 아니다.

**원문 및 상태 후속:** 새 원문 사실, 모순, 접근 실패로 분류할 검증 대상 및 ledger 변경 제안은 없다. 향후 실제 판정에는 공식 신호·구속·직접 동시조치의 문서와 정확한 단락/적용 거래, 기술별 당시 분류·자료 공개일/정정 이력 및 국가 미상·분모 범위, 독립 검증 라벨과 비교국 적격성의 직접 확인이 필요하다. 연결된 과거 감사의 인용만으로 규제 부재를 인정하지 않는다. 위협 상태, Gate, freeze, 배분 결과 접근 및 별도 referee 판정은 변경하지 않았다.

고정 참조 파일 SHA256(규제표·창 감사는 헤더만 확인):

| 파일 | SHA256 |
| --- | --- |
| `state/work_queue.json` | `4e3849ef10b6c6d497fc11e20fbb68453ab4df9ab6532cfc171628ff0f49c0a9` |
| `state/research_charter.md` | `32225e9dbf67054f3ab8f7d3b45c0a83f7733b80db51c0c4f1e663654244a602` |
| `prompts/round_03.md` | `18c1ac4ae0cbd178e9f562b0282c2e562029a068280c93846fdd54a402b271af` |
| `docs/INTERNAL_REVIEW.md` | `7a9710675548e804a473760d0d5244115d3ed281c789a27e10e1aec15116fadf` |
| `docs/master_prompt.md` | `220cd3eefff6afc57b4eb8c8a017fa7b0f2e7f16ceda0348c098e30809e4948c` |
| `outputs/round_03/one_week_plan_2026-11-08.md` | `c6034141764f48a118944514e46ae48434d63cca28963e76f3d0f5002733ead9` |
| `state/threat_register.md` | `7d8cfa045194fe73a191bf77ec24c6f2dd4691b8347469075c16dc91391a7a09` |
| `outputs/round_03/inference_mde_plan.md` | `8cb2252b7531ae4a80a6f082e257515e8c46cd7a13d49575d55ca7c15acaf0c9` |
| `outputs/reviews/round_03_internal_review_4.md` | `2a7376b9d6492e30c8e5d6e5b1016ebbe29066b6bf060befd58607c7fe255255` |
| `outputs/round_02/regulatory_coding_rules.md` | `b429f3f4e1919200110f4d1ac328eea35a2c78e025eb5d853e6f9ba0c7de7de7` |
| `scripts/review_pipeline.py` | `cd9ad86c43cf9152a1c3833e8aec2433af19a36785be0f380d6172bc962681d0` |
| `AGENTS.md` | `e7bb717d23e8a37ae10d46e1d00fad8a650628cca4460a26d937f32c95254a5c` |

[commit]: https://github.com/parkchanjin0128-pixel/research-agent/commit/7c2157cf5b775d38512f3df17d52dd52037e0b91
[artifact]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/outputs/round_03/placebo_crosswalk.md
[queue]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/state/work_queue.json
[charter]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/state/research_charter.md
[round]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/prompts/round_03.md
[master]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/docs/master_prompt.md
[week]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/outputs/round_03/one_week_plan_2026-11-08.md
[threats]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/state/threat_register.md
[coding]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/outputs/round_02/regulatory_coding_rules.md
[reg]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/outputs/round_02/regulatory_dataset.csv#L1
[audit]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/outputs/round_02/announcement_window_audit.csv#L1
[review4]: https://github.com/parkchanjin0128-pixel/research-agent/blob/7c2157cf5b775d38512f3df17d52dd52037e0b91/outputs/reviews/round_03_internal_review_4.md
