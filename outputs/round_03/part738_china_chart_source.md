# Part738 China 행: 2018-01-01판 한정 생산 관측

policy_archivist, 2026-10-23 UTC. **독립 verifier 확인·referee 심사 전 미검증 생산물**. 고정 입력: repository HEAD `2433beed61cf6a16f9ade9bf5e59e3a49b2b3d72`의 AGENTS.md, prompts/round_03.md, outputs/round_03/1c353_baseline_connection.md. 신규 원문 실질 열람은 아래 공식 문서 한 판본에 한정했다.

원문: https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/pdf/CFR-2018-title15-vol2-part738.pdf

## 판본·셀 관측

문서 running header는 `15 CFR Ch. VII (1-1-18 Edition)`이다. 이는 2018-01-01판 관측이며 2018-11-18 기준선 인증이 아니다. PDF 총 13쪽 중 제8쪽(0-based index7), 인쇄면260, Supplement No.1 to Part738, China 행에서 다음을 관측했다.

| 열 | China 셀 | 정확한 위치 |
|---|---|---|
| CB Column1 (표 머리글 CB1) | X | 인쇄면260/PDF8, Countries 오른쪽 첫 통제 열 |
| AT Column1 (AT1) | 공란 | 같은 면·행, 오른쪽 끝 AT2 바로 앞 열 |

표는 PDF에서 옆으로 돌아가 있다. pdftoppm으로 PDF8을 PNG 렌더링한 뒤 머리글부터 China 행(Chile 다음, Colombia 앞)까지 눈으로 대조했다. CB1의 X와 AT1의 공란은 이 시각 정렬 확인 결과다. 평탄화된 X 개수만으로 열을 배정하지 않았다. 작업용 렌더링은 `/tmp/china738.png`이며 원문 전체를 산출물에 첨부하지 않는다.

## 같은 문서의 작동 규칙

| 조문 | locator | 한정 요지 |
|---|---|---|
| §738.2(d)(2)(ii)(B) | 인쇄면255/PDF3 | ECCN의 Country Chart 열 이름·번호로 해당 열을 찾으며 Part742에서 요건·정책을 검토하도록 안내한다. |
| §738.3(d), Cells | 인쇄면257/PDF5, 오른쪽 상단 | X는 해당 통제사유·목적지 조합의 허가요건을 표시한다. |
| §738.4(a)(2)(ii)(A) | 인쇄면258/PDF6, 왼쪽 | 해당 셀이 X이면 예외가 적용되지 않는 한 허가신청이 필요하다. 각 긍정 요건에 대한 예외 충족을 검토한다. |
| §738.4(a)(2)(ii)(B) | 인쇄면258/PDF6, 왼쪽 | X가 없다는 것은 그 특정 통제사유·목적지의 요건이 없다는 의미이며, 다른 EAR 요건에 관한 조건을 별도로 둔다. |

따라서 이번 조각은 이 판본에서 China-CB1은 X, China-AT1은 공란이라는 연결만 제공한다. 공란을 중국 거래 전체의 무허가·미통제로 확대하지 않는다. 1C353 품목·기술 적합성, Part740 예외·국가군, Part742 심사정책, 최종용도·최종사용자 및 이후 개정은 이번에 확인하지 않았다. 2018-11-18 기준선, 창 안 중국 접근의 추가 제한 여부, 세 하위기술 날짜·강도 판정은 미확인 유지다. Gate·freeze·T12·기존 ledger 상태는 변경하지 않는다.

## 접근 기록과 다음 최소 단위

2018 공식 URL은 web open 및 curl 다운로드 모두 성공했다. 2019 대체 판본은 열람하지 않았다. 원문 접근 실패 없음. 추출문과 PDF8 렌더링을 대조했다. 다음 작업은 독립 verifier가 위 단일 판본과 셀 정렬·조문 locator를 재확인하는 것이다. 그 뒤 cutoff까지의 Part738 변경 이력 연결은 별도 범위로 남는다.
