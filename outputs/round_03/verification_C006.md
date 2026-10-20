# C006 독립 검증 — Huawei 최초 Entity List 규칙

- 검증일: 2026-10-20. 별도 에이전트: huawei_verifier_oct20 (생산자와 다름; fork_turns=none).
- 검증 입력: immutable commit f5cfb274799fcdd86c64225c48a8dc2f1a696b93의 AGENTS.md, state/claims_ledger.csv, state/research_charter.md, state/threat_register.md, outputs/round_03/huawei_entity_list_source_note.md. 작성자 대화·추론은 전달하지 않았다.
- 모델: 현재 구독 세션 상속 모델 사용; 역할 권장 모델을 별도로 강제 지정하지 않았다. 같은 모델의 공통 맹점 가능성은 독립 증거로 해소됐다고 보지 않는다.
- 1차 원문: https://www.govinfo.gov/content/pkg/FR-2019-05-21/html/2019-10616.htm
- 확인 수준: Federal Register 원문 직접 대조. 2019년 최초 규칙의 범위이며 2026년 현행상태 검증 아님.

## 별도 verifier 결과

| 항목 | 결과 및 locator |
|---|---|
| C006 날짜·서지 | verified: 효력일 2019-05-16; 게재일 2019-05-21; 84 FR 22961–22968; FR Doc.2019-10616. 머리말 및 DATES p.22961 |
| 대상 | 메모와 일치: Huawei와 26개 destination의 비미국 계열사 68개. SUMMARY p.22961; ERC Entity List Decision pp.22961–22962 |
| 범위·심사 | 메모와 일치: EAR 적용 품목 전체 허가요건·거부 추정·Savings Clause 외 예외 불가. ERC Entity List Decision p.22962 |
| 경과조치 | 메모와 일치: 2019-05-16 실제 외국 목적지 주문에 따라 운송수단으로 수출·재수출 항구로 이동 중인 적격 선적의 종전 자격 유지. Savings Clause p.22963. 모든 기존 주문으로 확대 해석 금지 |

원문 메모 추출표의 실질적 오류는 발견하지 않았다. 원래 C006의 복합 문구에서 EO 2019-05-15는 별도 원문을 확인하지 않아 검증 범위 밖으로 분리했다. 기존 문구는 아래 이력으로 보존하며 반증 판정이 아니다.

기존: Huawei Entity List 지정 2019-05 (EO 2019-05-15, EL 효력 2019-05-16 전후).
변경: 최초 Entity List 규칙의 효력일·게재일·서지로 한정. claims ledger의 새 문구만 verified.

## 완료 범위

- 이번 claim 단위 판정: verified 1; contradicted 0; unverifiable 0. EO·TGL·FDPR·실제 차단일은 이번 검증 범위 밖이며 검증 완료에 포함하지 않는다.
- T05는 open 유지. 날짜 검증이 교란 분리의 성공을 뜻하지 않는다. clean-window, 41행 분류, Gate, freeze 변경 없음.
- 내부 referee 미실시. 전체 round 03 독립 검증·회차 완료가 아님.
- 다음 단위: 최초 규칙 이후 임시일반허가(TGL) 원문 1건 생산. 기업별 실효 범위 변경을 확인한 뒤 FDPR은 별도로 감사.
