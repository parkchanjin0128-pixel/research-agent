# C028 / UVL 2019-07211 첫 수정판 독립 원문 검증

- 단위: `uvl_2019_14610`. 검증일: 2026-11-08 23:18 UTC / 2026-11-09 08:18 KST.
- 검증자: `/root/uvl_r1_verifier_nov09`. 최초 작성자 `/root/rule14610_checkpoint`, 수정 작성자 `/root/uvl_minor_revision_nov09`, 기존 검증자 `/root/independent_verifier_probe`, 기존 심사자 `/root/internal_referee_probe`와 다르다.
- 입력 커밋: `24f3fce145c9a155747a3e01e4f4368cfc441195`. 검증 대상은 [수정판 생산 메모](https://github.com/parkchanjin0128-pixel/research-agent/blob/24f3fce145c9a155747a3e01e4f4368cfc441195/outputs/round_03/part744_uvl_14610_source.md), SHA256 `028a9ed38fa3e41df933d4a027ca8aeed9b20b9ca42f800190017a6830c9fd50`이다. 받은 UTF-8 원본으로 직접 계산하여 queue 기록과 일치함을 확인했다.
- 판정: **verified**. 현재 수정판의 C028 한정 원규칙 관측과 수정판이 인용한 과거 단위 이력에 적용한다. 신규 referee 판정, 지적 종결, 단위 완료나 정식 3회차 심사 완료 판정은 이 보고서 범위 밖이다.

## 원규칙 직접 대조

2026-11-08 UTC에 [미국 GPO GovInfo 공식 PDF](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf)의 본문과 페이지 표식을 직접 확인했다. 아래 링크의 페이지 번호는 PDF 뷰어 기준이고, 인쇄 페이지도 병기했다.

| 대상 | 판정과 원문 위치 |
|---|---|
| C028: 문서 식별 및 날짜 | **verified.** [인쇄 14608 / PDF 1쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=1) 머리말·BIS 구역·DATES: BIS 최종규칙, 15 CFR Part 744, Docket 190130021-9021-01, RIN 0694-AH73, 2019-04-11 게재·효력. [인쇄 14614 / PDF 7쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=7) BIS 서명 아래 FR Doc. 2019-07211. 14610은 개정지시가 있는 인쇄면이며 문서 범위는 14608–14614다. |
| C028: 개정 범위와 숫자 | **verified.** [인쇄 14610 / PDF 3쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=3)의 PART 744 개정지시 1은 권한 인용 재기재, 2(a)–(p)는 Supplement No. 6 UVL 개정이다. 2(a)–(d), 2(f)–(g)는 China 37 추가·3 삭제, Hong Kong 6 추가·기존 1개 수정 지시를 명시한다. [인쇄 14608 / PDF 1쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=1) Summary 및 [인쇄 14609 / PDF 2쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=2) Changes에 총 50 추가·10 삭제·기존 1개 주소 추가가 명시된다. 규칙이 표명한 숫자를 확인했으며, 전수 재계수 값이 아니다. |
| C028: 거래 요건 | **verified.** [인쇄 14609 / PDF 2쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=2) Background의 §740.2(a)(17), §744.15(b) 인용 문단은 UVL 당사자가 포함된 수출·재수출·국내이전의 허가예외 이용 정지 및 별도 허가요건이 없는 경우 거래 전 UVL statement 취득·기록 보관을 설명한다. 인쇄 14608 Background의 §744.11 설명은 Entity List와 구별한다. 인용 조문의 당시 전문이나 후속 연혁은 별도 확인하지 않았다. |
| R1 / C028: Savings Clause | **verified.** [인쇄 14609 / PDF 2쪽, Savings Clause](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=2)에는 (1) 이 규칙으로 허가예외 적격성을 잃었거나 EAR §744.15 요건이 새로 적용되고, (2) 이전에는 무허가 수출·재수출·국내이전이 가능했으며, (3) 실제 주문에 따라 2019-04-11 현재 선적용 부두에 있거나 부선에 실렸거나 수출 운송수단에 적재되었거나 운송수단에 실려 수출항으로 이동 중이던 화물이라는 세 요건이 있다. 첫 문장의 `before May 13, 2019`는 해당 UVL 당사자에 대한 종전 허가예외 또는 무허가 취급의 문언이고, 둘째 문장의 `before midnight on May 13, 2019`는 그 시점 전까지 실제 수출·재수출·국내이전되지 않은 해당 물품에 §744.15를 적용한다는 문언이다. 수정판은 두 표현과 선적 요건을 보존했다. 정확한 마지막 허용 시각·시간대는 이 검증에서 정하지 않는다. |

## R2 문서 이력 대조

**verified.** 수정판의 첫 문단과 접근·후속 구역은 최초 생산 당시 검증·심사 미완료 기록을 과거 시점에 두고, 그 뒤의 [C028 독립 검증](https://github.com/parkchanjin0128-pixel/research-agent/blob/24f3fce145c9a155747a3e01e4f4368cfc441195/outputs/round_03/verification_C028.md)과 [단위 심사 1](https://github.com/parkchanjin0128-pixel/research-agent/blob/24f3fce145c9a155747a3e01e4f4368cfc441195/outputs/reviews/internal/uvl_2019_14610_referee_1.md)을 구분한다. 두 기록은 2026-11-02 UTC이고, C028은 원규칙 한 건에 한정되며 단위 심사는 minor 2건을 요구했다. [고정 queue](https://github.com/parkchanjin0128-pixel/research-agent/blob/24f3fce145c9a155747a3e01e4f4368cfc441195/state/work_queue.json)의 해당 단위는 `partial`, phase `verification`, 새 verification/review는 모두 null이다. revision 이력에 등록된 [실제 r1 대응 파일](https://github.com/parkchanjin0128-pixel/research-agent/blob/24f3fce145c9a155747a3e01e4f4368cfc441195/outputs/reviews/internal/uvl_2019_14610_referee_1_r1_response.md)도 대조했다. 이 문서 대조로 과거 다운로드·실행을 재현했다거나 주설계·연결표·MDE·정식 3회차 전체를 검증했다고 보지 않는다.

고정 입력 SHA256: `AGENTS.md` `e7bb717d23e8a37ae10d46e1d00fad8a650628cca4460a26d937f32c95254a5c`; `docs/INTERNAL_REVIEW.md` `7a9710675548e804a473760d0d5244115d3ed281c789a27e10e1aec15116fadf`; `state/work_queue.json` `f453de65281400aee6326ccefdab5375faf778c411d410c6232241125ed2cfc5`; `verification_C028.md` `19b826cdffae9922e543dfafc0bdd9f98001e51bf73924ab94734ba36f3df14c`; `uvl_2019_14610_referee_1.md` `f9f8f36bd0fef71ca3af14ccd4a64ebf32eb5d2f7195667f65bb43e072cda74e`; `uvl_2019_14610_referee_1_r1_response.md` `58e1a5895d4694138a1d3eb2809dee127d9c21deafb1d66099cfb8001ff59c00`.

## 적용 한계 및 ledger 제안

- [공식 GovInfo HTML](https://www.govinfo.gov/content/pkg/FR-2019-04-11/html/2019-07211.htm)은 이번 열기에서 접근되지 않았다. PDF 원문 텍스트 대조는 성공했다. [FederalRegister.gov XML 표시판](https://www.federalregister.gov/documents/2019/04/11/2019-07211/revisions-to-the-unverified-list-uvl)은 접근 가능했으며 공식판으로 간주하지 않았다. PDF 시각 대조와 명단 전수 재계수는 하지 않았다. Malaysia는 인쇄 14609 Changes에서 2명이고, 인쇄 14610 개정지시 2(i)는 단수이며, [인쇄 14613 / PDF 6쪽](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf#page=6) 텍스트에 두 항목이 있다. 전체 지시와 명단의 수치 정합성을 판정하지 않는다.
- 이 규칙은 Part 744 UVL 당사자 명단 변경의 조사 단서다. Part 738 Country Chart 또는 ECCN 1C353 개정으로 분류할 근거가 없으며, 2018-11-19~2019-04-30 전체의 추가 제한 부재나 완결성을 보여 주지 않는다. 실제 거래·허가예외 사용·대체조달·기술 매핑·기관 노출은 확인하지 않았다. 4월 11일 또는 5월 13일을 모든 거래의 단일 차단일로 적용하거나 41행·세 바이오 행의 China-binding 날짜·강도를 바꿀 근거가 없다.
- 기존 C028의 좁은 `verified` 범위를 유지할 것을 제안한다. 새 ledger 행·기존 행의 범위 확대, T12 해소, Gate 재판정, cutoff 또는 freeze를 제안하지 않는다. 별도 referee가 재판정한다.
