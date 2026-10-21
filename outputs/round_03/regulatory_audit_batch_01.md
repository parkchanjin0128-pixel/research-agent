# 좁은 규제 감사 01 — Biotechnology 최초 3행

생산일 2026-10-21; 생산자 별도 policy_archivist narrow_audit_batch1. 독립 verifier·referee 미실시. 현재 구독 상속 모델 사용; 권장 모델 별도 강제 지정 미적용.

고정 입력: parkchanjin0128-pixel/research-agent@6f6c2eac3919f4def5adc45a6f6dd7550fb09c5a의 outputs/round_02/regulatory_dataset.csv, outputs/round_02/regulatory_coding_rules.md, outputs/reviews/round_03_claude_precheck_1.md(CR5). 원본 round 02는 변경하지 않는다.

질문: 2018-11-19~2019-04-30 사이 해당 중국행 거래에 새 China-binding restriction이 생겼는가? 아래는 감사 작업목록이며 통제 판정이나 freeze가 아니다.

| node_id | technology description | 원본 연결 | baseline ECCN 탐색 후보(확정 아님) | 경계 | 결과 |
|---|---|---|---|---|---|
| F01-S01 | Nanobiology | 없음 | 1C351·1C353·1C354; 1E001; 장비 2B352·2E001 | 나노 규모만으로 매핑 금지. 실제 물질·유전요소·장비와 통제 목록·성능요건의 좁은 교집합 특정 | 미확인 |
| F01-S02 | Synthetic biology | R10 | 1C353; 관련 물질 1C351·1C354; 1E001; 장비 2B352·2E001 | 특정 병원성·독소 요건 확인. R10의 2021년 SW 사건 소급 금지. 당시 2B352.j 문구 별도 확인 | 미확인 |
| F01-S03 | Genomic and genetic engineering | R10 | 1C353; 관련 물질 1C351·1C354; 1E001; 장비 2B352·2E001 | 일반 유전공학과 특정 통제 유전요소·변형생물 분리. 장비·기술 별도 검토 | 미확인 |

후보 목록은 확정 매핑·전수 목록이 아니다. 날짜·강도·당시 미통제 여부는 세 행 모두 미확인 유지. 새 매칭 미발견을 0으로 바꾸지 않는다.

## 역사적 원문 일부 확인 — 생산 관측, 독립 검증 대기

GovInfo 2018 CFR Title 15 Vol.2, 2018-01-01 edition, Part774 Supplement No.1, ECCN 1C353: 인쇄면816–817(PDF58–59쪽), License Requirements / Items a–b / Technical Notes1–4.

https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/pdf/CFR-2018-title15-vol2-part774.pdf

생산자는 특정 병원성 관련 서열·독소 암호화 서열을 가진 유전요소·유전자변형생물이라는 한계, 유전요소 정의에 화학적 합성이 포함됨, CB Column1·AT Column1 표기를 확인했다. F01-S02·S03의 좁은 부분에 기존 통제가 있었을 가능성을 조사할 근거다. 전체 하위기술 통제 또는 중국 순증 제한으로 판정하지 않는다.

이 판본은 2018-01-01 기준이다. 2018-11-19 직전 상태와 연결하는 개정 이력 미검토. 2026 현행규정을 역사적 증거로 사용하지 않았다.

## 필요한 원본 및 다음 작업

1. 기준선 연결: 위 후보 ECCN 전체 문구·주석·정의와 2018-01-02~2018-11-18 해당 조항 개정 FR 원문·정정·효력일. 2019 CFR·LSA는 개정 발견용이며 11월19일 상태와 동일시 금지.
2. 창 안 변경: 2018-11-19~2019-04-30 EAR 개정 원문. Parts734·736·738·740·742·744·774의 관련 변경 및 창 이전 발표/창 안 효력 사건 포함.
3. 중국 적용: 당시 Part738 Country Chart, Part740 예외·국가군, §742.2 등 심사정책의 날짜별 연결.
4. 거래 제한: 당시 Part744 생물·화학무기 최종용도 및 Entity List 관련 사용자 조치. 특정 사용자 제한을 기술 전체로 전파하지 않는다.
5. 행별 적용 품목·SW·기술, 기존/추가 의무, 효력일, 중국 범위, 예외·심사·locator가 모인 뒤 날짜·강도를 판정한다.

완료는 세 행 작업목록과 1C353의 일부 역사적 원문 확인까지다. 기준선 개정 연결·후보 전체·창 안 FR 전수·중국 차트/예외/심사/사용자 이력은 미완료. 다음 최소 단위는 별도 verifier의 해당 1C353 구간 확인과 claims 등록이다. 이어 기준선 개정 연결을 수행한다. 원문 전문 저장 없음.
