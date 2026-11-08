# C028 — Part 744 UVL 원규칙 독립 검증

- 검증 시각: 2026-11-02 00:25 UTC (Asia/Seoul 09:25).
- 검증자: 별도 agent `/root/independent_verifier_probe` (`independent_verifier`). 원산출물의 작성자/claimant `/root/rule14610_checkpoint`와 다른 agent다. 작성자의 대화·추론은 전달받지 않았으며, 지정 산출물·상태와 직접 접근한 1차 원문을 대조했다.
- 입력: `outputs/round_03/part744_uvl_14610_source.md`, `state/research_charter.md`, `state/decision_log.md`, `state/threat_register.md`, `state/claims_ledger.csv`, `prompts/round_03.md`. `AGENTS.md`, `state/turn.md`, `outputs/progress_log.md`도 읽었다. 직접 지시된 Codex 생산·별도 verifier·별도 referee 운영을 적용했으며 Claude 호출이나 차례 대기는 하지 않았다.
- 등록 단위: 신규 C028 1건. 아래 원문 관측에 한정해 **verified**. 기존 claim을 재검증한 것으로 표시하지 않는다. 이 작업은 독립 검증 경로의 최소 시험이며 후보 설계·회차 전체 완료 판정이 아니다.

## 원문과 실제 접근

주 판정 근거는 [GPO 공식 PDF](https://www.govinfo.gov/content/pkg/FR-2019-04-11/pdf/2019-07211.pdf)다. 웹 도구와 search-service가 각각 7쪽 PDF의 본문·페이지 표식을 반환했다. 검색 결과 요약이나 생산자 추출문에만 의존하지 않았다.

| 접근 | 실제 결과 |
|---|---|
| [생산자가 제시한 공식 HTML](https://www.govinfo.gov/content/pkg/FR-2019-04-11/html/2019-07211.htm) | 두 웹 도구의 open에서 접근 불가. 로컬 `curl.exe`는 호스트 DNS 해석 실패(exit 6). 생산자의 과거 접근 성공을 이번 검증의 성공으로 복사하지 않음. |
| 공식 govinfo PDF open | 성공. 인쇄 14608 / PDF 1쪽, 14609 / 2쪽, 14610 / 3쪽, 14614 / 7쪽의 관련 본문을 직접 대조. |
| [FederalRegister.gov 참고 XML판](https://www.federalregister.gov/documents/2019/04/11/2019-07211/revisions-to-the-unverified-list-uvl) | 본문 접근 성공. 사이트가 법적 공식판은 govinfo PDF라고 명시하므로 보조 확인에만 사용. |
| PDF screenshot | PDF 스킬을 읽고 위 네 페이지를 요청. 도구가 screenshot 참조/표시 마커만 반환했고 실제 이미지 데이터는 제공하지 않음. 따라서 시각 대조 성공으로 인정하지 않음. 표 전수 재계수·레이아웃 검증은 미수행. |

## 범위별 판정

| 검증 대상 | 판정 | 공식 PDF의 정확한 위치·확인 방법 |
|---|---|---|
| 제목, 기관, 유형, Part, docket, RIN, 문서번호, 게재·효력일 | verified | 인쇄 14608 / PDF 1쪽 머리말·BIS 구역·DATES: *Revisions to the Unverified List (UVL)*, BIS final rule, 15 CFR Part 744, Docket 190130021-9021-01, RIN 0694-AH73, 2019-04-11 효력. 14614 / PDF 7쪽 서명 아래 FR Doc. 2019-07211. 문서 시작·종료는 14608–14614이며 같은 PDF 양끝의 다른 기관 문서는 제외. 번호·날짜를 추정하지 않음. |
| Part 744 authority citation 재기재 | verified | 인쇄 14610 / PDF 3쪽 `PART 744—[AMENDED]`, 개정지시 1. 권한 인용 변경 자체를 기술별 통제 변경으로 번역하지 않음. |
| UVL 명단 변경 및 숫자 | verified (규칙이 명시한 숫자) | 인쇄 14609 / PDF 2쪽 Changes: 총 50 추가·10 삭제, China 37 추가·3 삭제, Hong Kong 6 추가 및 Ling Ao 기존 항목 주소 추가·오탈자 수정. 14610 / PDF 3쪽 개정지시 2(a)–(d), (f)–(g)가 China/Hong Kong 변경을 직접 명시. 총원은 요약문 수치의 존재를 확인한 것이며 표 전체 항목을 독립 재계수한 값이 아님. |
| license exception 이용 정지 및 UVL statement 요건 설명 | verified (이 규칙의 설명문) | 인쇄 14609 / PDF 2쪽 Background: §740.2(a)(17) 인용 문단과 §744.15(b) 인용 문단. UVL 당사자 관련 수출·재수출·국내이전의 예외 이용 정지, 별도 허가요건 없는 거래에 앞선 statement 취득·보관 설명 확인. 14608–14609 Background는 UVL과 Entity List를 구분. 해당 두 조문 당시 전문의 별도 대조는 미수행. |
| Savings Clause의 조건부 종전 취급 | verified (문언·조건 한정) | 인쇄 14609 / PDF 2쪽 Savings Clause. 기존 무허가 적격성, 실제 주문, 2019-04-11 당시 지정 운송단계 등의 조건과 May 13 문구를 확인. 모든 거래의 접근 차단일을 Apr 11 또는 May 13으로 고정할 근거는 아님. |

## 남는 불확실성과 사용 제한

1. Savings Clause는 먼저 `before May 13, 2019`라고 쓰고, 이어 `before midnight on May 13, 2019`라는 문구를 쓴다. 원산출물의 전자 요약은 원문에 있으나 정확한 마지막 허용 시각을 여기서 통일 해석하지 않는다. 경과조항 조건과 두 문구를 함께 보존해야 한다.
2. 개정지시 2(i)는 Malaysia에 단수 entry를 쓰지만 Changes는 Malaysia 2명을 설명하고 PDF 6쪽 표에도 두 항목이 있다. 생산자의 검증 대상 China/Hong Kong 수치와 총원 설명의 존재는 확인되지만, 전체 지시·표의 숫자가 완전히 정합하다고 확대하지 않는다. 전수 명단 감사는 남아 있다.
3. 이번 verified는 원규칙 1건의 명시 내용에만 적용한다. 실제 거래·대체조달·허가예외 사용, 기술 매핑, 기관 노출, China-binding 접근 제한의 날짜·강도는 **미검증**이다. Part 738 Country Chart 또는 ECCN 1C353 개정으로 분류하지 않는다.
4. 좁힌 2018-11-19–2019-04-30 창 안의 UVL 거래요건 변경을 조사할 단서는 있으나, 기간 전체의 추가 제한 부재·무변경·전체 이력 완결성을 증명하지 않는다. 41행·세 바이오 행·T12·기존 Gate·charter·freeze는 변경하지 않았다.
5. 생산자의 과거 다운로드 성공·오류 보완 등 실행 이력은 이번 1차 원문만으로 검증할 대상이 아니다. 이번 접근의 성공·실패를 위 표에 별도로 기록했다.

## 기록 결과

- 신규 ledger 판정: **verified 1 / contradicted 0 / unverifiable 0**. 이 집계는 C028의 한정 원문 관측 1건에 대한 것이며 위의 미검증 영역에 verified를 부여한 것이 아니다.
- 기존 ledger 행은 수정하지 않고 C028만 추가했다. 신규 검증보고 외의 연구·운영 파일, commit/push, 예약은 변경하지 않았다.
- 저장 확인: Python 실행 별칭이 시작되지 않아 첫 append 시도는 실행되지 않았다. PowerShell 기본 파일 API로 추가 후 기존 ledger 바이트가 그대로인 것과 27행→28행, C028 유일성을 확인했다.
- 별도 referee의 심사와 생산자의 후속 보완은 이 검증보고의 완료 범위 밖이다.
