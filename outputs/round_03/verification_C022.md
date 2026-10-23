# C022 — 2018판 Part738 China 행 독립 검증

- 별도 verifier: verify_china_chart, 2026-10-23.
- 입력: immutable HEAD aa3ab2c94c7b1d8d12a9c21ad23a9c6e033b80e8의 AGENTS.md, state/claims_ledger.csv, outputs/round_03/part738_china_chart_source.md. 작성자 추론·대화 미전달.
- 결과: **verified1 / contradicted0 / unverifiable0**. 한정 관측 묶음 C022 기준. 기존 C001–C021 재판정 없음.
- 공식 원문: https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/pdf/CFR-2018-title15-vol2-part738.pdf

독립 다운로드·텍스트 추출 후 PDF8을 렌더링·회전하여 시각 대조했다. 총13쪽, 인쇄면260/PDF8의 running header는15CFR Ch.VII(1–1–18 Edition)이다. Chile 다음·Colombia 앞 China 행을 머리글과 정렬하여 첫 통제 열 CB1=X, 끝에서 두 번째 열 AT1=공란을 확인했다.

| 조문 | locator | 한정 확인 |
|---|---|---|
| §738.2(d)(2)(ii)(B) | 인쇄면255/PDF3 | Country Chart 열 및 Part742 요건·정책 연결 |
| §738.3(d) | 인쇄면257/PDF5 오른쪽 위 | X의 해당 통제사유·목적지 허가요건 |
| §738.4(a)(2)(ii)(A)–(B) | 인쇄면258/PDF6 왼쪽 | X의 허가요건·예외 검토, 공란의 특정 사유/목적지 한정 및 다른 EAR 요건 유보 |

접근 실패 없음: GitHub immutable 파일 읽기·공식 PDF web open·curl·pdftotext·렌더링 성공. 원문 전문 저장소 복제 없음.

**2018-01-01판 관측만 검증했다.** 2018-11월 직전 상태·후속 개정 이력·1C353 거래 전체 적용성 및 예외·창 안 순증 제한·하위기술 날짜와 강도·Gate/T12는 미검증 유지한다.

다음 최소 생산 단위(오케스트레이터): 공식2018 LSA의 Part738/동 Supplement 개정 참조와 포괄기간을 확인해 cutoff까지 필요한 원규칙 목록을 지정. 기존 기준선 연결표 자체의 독립 검증·전체 감사·설계·MDE·referee는 미완료.
