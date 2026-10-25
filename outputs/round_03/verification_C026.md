# C026 — 2019판 Part738 China 행 및 각주7 독립 검증

- verifier: independent_checkpoint_2019, 2026-10-25 UTC. 작성 역할과 다른 에이전트이며 작성자의 추론 과정은 전달받지 않았다.
- 입력 HEAD: c130b7834932060d26c9f3cdbe52301023098e87; run_id: work-20261025T141959Z-995edeb9-7763-49c5-b979-8b3edbad45b3.
- 검증 대상: outputs/round_03/part738_china_2019_source.md의 단일 2019판 원문 관측. verified 1 / contradicted 0 / unverifiable 0.

## 직접 확보와 위치

공식 원문: https://www.govinfo.gov/content/pkg/CFR-2019-title15-vol2/pdf/CFR-2019-title15-vol2-part738.pdf

curl 다운로드, pdftotext -layout 추출, PDF8·12의 pdftoppm 렌더링을 직접 확인했다. PDF13쪽, SHA256 951252555212f7b757f0f4e0b0a8d18a2eb77dcc7d06934b7de819dba84efb0a. 텍스트의 PDF1·3·5·7 등 running header는 1-1-19 Edition을 표시한다. 파일 제작일을 법적 효력일로 사용하지 않는다.

| 관측 | 독립 대조 결과 | locator |
|---|---|---|
| China CB1 | X 확인 | Supplement No.1, 인쇄275/PDF8, Chile 다음 Colombia 앞 China; 머리글 CB1과 정렬 |
| China AT1 | 공란 확인 | 같은 행, AT2 바로 앞 열과 정렬 |
| 각주7 | India 목적지 ECCN6A003.b.4.b·9A515.e의 RS column2 사유 허가가 여전히 필요하다는 문구 확인 | 인쇄279/PDF12 표 아래 각주7 |

표는 회전 배치되어 있다. X 개수 대신 국가명·열 머리글·직선 셀 경계를 대조했다. 각주7의 목적지는 India이며 China 예외라는 주장은 지지하지 않는다.

## 비교 범위와 한계

이번 China 두 셀 관측은 ledger C022의 2018판 기록과 일치한다. 2018 PDF를 이번에 새로 열람한 것은 아니므로 양 판본 전수 비교나 각주 문구 변화 전체의 독립 검증으로 세지 않는다. C025 원규칙과 2019 각주를 잇는 완결된 개정 이력도 검증하지 않았다.

2018-11-18·2019-04-30의 전체 규제 상태, 기간 중 무변경, 2019 창 내 개정, Part740/742·예외·최종용도/사용자 제한, 1C353 전체 적용성, 실제 접근 제한 날짜·강도·세 바이오 매핑은 미확인 유지한다. AT1 공란은 거래 전체의 미통제·무허가를 뜻하지 않는다. 연결표 자체 검증·전체 감사·MDE·회차 생산·내부 referee는 미완료이며 Gate·T12·41행·질문·freeze를 변경하지 않는다.

## 접근 기록과 다음 최소 단위

공식 PDF 직접 다운로드·텍스트 추출·8/12쪽 시각 확인 성공; 원문 접근 실패 없음. search-service open은 시도하지 않았다. 신규 보고 경로 조회404는 파일 부재 확인이다. PDF 전문·렌더링은 저장소에 올리지 않는다.

다음 생산은 공식 2019 LSA 중 좁힌 창2018-11-19~2019-04-30에 해당하는 Part738 및 Supplement 개정 참조·포괄기간 한 건을 확보하고 필요한 원규칙을 지정한다. 기간 중 변경 부재를 미리 결론내리지 않는다.
