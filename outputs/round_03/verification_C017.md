# C017 — 2018판 ECCN 1C353 일부 구간 독립 검증

검증일: 2026-10-21. 별도 verifier verify_1c353; 생산자 narrow_audit_batch1와 다름. fork_turns=none, 작성자 대화·추론 미전달. 현재 구독 상속 모델 사용; 권장 역할 모델 별도 강제 지정 미적용.

입력: parkchanjin0128-pixel/research-agent@4b556ddf48c9b0d36bd02fe517de0af114928052의 AGENTS.md, state/claims_ledger.csv, outputs/round_03/regulatory_audit_batch_01.md. verifier가 직접 읽고 1차 원문을 별도 조회했다.

원문: https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/pdf/CFR-2018-title15-vol2-part774.pdf

## 한정 판정

C017 verified. 2018-01-01판 역사적 조문 관측만 검증했다.

- locator: 인쇄면816–817 / PDF58–59쪽, ECCN1C353 License Requirements, Items a–b, Technical Notes1–4. 독립 추출 텍스트 행6103–6192.
- CB Column1·AT Column1 표기, 특정 병원성 관련/독소 암호화 서열 조건과 유전요소 정의의 전체·일부 화학합성이 생산 관측과 일치.
- 백신 1C991 안내와 Technical Note2 예외도 있어 기술 일반 전체의 단일 통제 여부로 확대하지 않는다.
- PDF 텍스트 접근 성공. 두 면 screenshot 요청은 TimeoutError로 시각 확인 실패. 텍스트 대조를 시각 검증으로 보고하지 않는다.

## 미확인 범위

2018-11-19 직전까지의 개정 연결, 중국 Country Chart·예외·심사·최종사용자/용도 적용, F01-S01~S03 매핑 및 창 안 순증 제한은 검증하지 않았다. 세 행 날짜·강도·미통제 여부는 미확인 유지. 기존 Gate 근거 반증 없음.

이번 claim 단위 verified1 / contradicted0 / unverifiable0. 전체 규제 감사·내부 referee·round03 완료 아님. T12 등 상태 변경 없음.

다음 최소 생산 단위: 1C353의 2018-01-02~2018-11-18 개정 이력 연결 자료(공식 LSA/FR)를 확인하고, 확인한 변경·정정·효력일 또는 접근 실패를 기록. 단순 검색 미발견을 미통제 확인으로 쓰지 않는다.
