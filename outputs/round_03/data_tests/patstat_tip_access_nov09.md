# PATSTAT 무료 접근 경로 · 2026-11-09 KST

생산 `/root` · 문서와 비로그인 화면만 확인 · [기존 Google Patents 접근 점검](feasibility_report.md) · [NSFC·특허 단건 점검](../nov09_outcome_access_probe.md)

**새 경로.** 유럽특허청은 공식 웹 서비스 TIP에서 PATSTAT Global과 EP Register에 무료로 접속할 수 있다고 명시한다. 비로그인으로 공식 TIP 주소를 열면 EPO 계정 로그인 화면으로 이동했다. 신규 무료 계정 또는 기존 EPO 계정으로 접속하는 경로가 공식 안내에 있다. 별도 유료 PATSTAT Online과 조직의 심사를 거치는 원자료 일괄 배포는 이 점검 범위 밖이다. 실제 로그인 성공, 권한·판본, 쿼리/내보내기 한도, 분석 자료의 포괄성은 아직 미확인이다. [EPO PATSTAT 개요](https://www.epo.org/en/about-us/observatory-patents-and-technology/observatory-tools/patstat) · [TIP 공식 안내](https://www.epo.org/en/searching-for-patents/data/technology-intelligence-platform) · [접속 화면](https://tip.epo.org/) · [시작 가이드](https://link.epo.org/web/data/technology-intelligence-platform/en-TIP-getting-started.pdf)

| 연구 필요 | 공개 사전에서 확인한 구조와 주의점 |
|---|---|
| 출원 및 지식산출의 시간 | TLS201_APPLN의 출원일·최초 관련 출원일·DOCDB 패밀리, TLS211_PAT_PUBLN의 공개일. 최초 관련 출원일은 직접 연결된 우선권·국제출원 등도 포함한다. 날짜 미상 대체값, 가공된 출원, 출원관할·당사자 국가를 분리한다. 최초 출원은 관측 가능한 혁신 산출 대리변수이며 연구·투자 결정일이 아니다. |
| 출원인 국가와 분류 | TLS207_PERS_APPLN에서 `APPLT_SEQ_NR > 0`으로 출원인을 고르고 TLS206_PERSON의 `PERSON_CTRY_CODE`로 연결한다. 거주·주소 귀속을 국적 또는 최종 지배국으로 해석하지 않는다. 문헌별 출원인은 TLS227에 있다. IPC TLS209는 여러 공개문헌의 분류를 현행 분류 체계로 병합하고, CPC TLS224는 TLS225의 패밀리 분류에서 파생된다. 사후 분류 변화와 공동출원·국가 불명을 따로 검사한다. |
| 후방 특허 인용 | TLS212_CITATION의 인용 출처와 공개/출원 연결키를 검토한다. 카탈로그 §5.11에 따르면 `CITED_PAT_PUBLN_ID`와 `CITED_APPLN_ID`는 같은 인용의 동등 키가 아니다. 가공 공개 레코드와 비특허문헌에서 재추출한 특허 번호를 명시적으로 다룬다. DOCDB 패밀리 간 중복 제거와 미국 귀속 분모를 고정하기 전에는 B를 계산하지 않는다. |

근거는 [2025 가을 Global 데이터 사전](https://link.epo.org/web/business/patstat/en-data-catalog-patsat-global-autumn-2025.pdf) §§3.2, 5(TLS201·206·207·209·211·212·224·225·227), 6.16, 6.20, 6.46, 6.143. [EPO 최신 판본 목록](https://www.epo.org/en/about-us/observatory-patents-and-technology/observatory-tools/patstat/latest)은 2026년 가을 사전을 링크하지만 이번 조회는 PDF 시간 초과였다. TIP 내부의 실제 서비스 판본과 일치한다고 가정하지 않는다.

**첫 접속에서 할 일.** 작업공간의 PATSTAT Global 판본과 데이터베이스 연결 방법, 카탈로그·사용 제한·결과 반출 규칙을 기록한다. 별도 계정 정보는 작업 기록에 넣지 않는다. TIP SQL 연결이 허용되고 실제 스키마 이름이 확인되면 먼저 결과행을 반환하지 않는 `WHERE 1=0` 검사를 단계별로 시도한다. 예시는 [스키마 검사안](patstat_tip_schema_only.sql) 참조. SQL 판본·권한·오류 또는 빈 결과의 열 이름만 기록한다. 기술별·국가별·월별 특허 수, 개별 레코드, 의존도 수치와 배분 결과는 이 단계에서 열거나 집계하지 않는다. 이 경로가 성공해도 기존 BigQuery의 미실행 점검을 성공으로 바꾸지 않는다.

**다음 판단.** 분석에 필요한 국가 및 인용 연결의 누락, 비교국별 수록 해상도, 고정 판본의 재현성·반출 한도 검사는 실제 접근과 사전자료 검사 범위가 확인된 뒤 수행한다. 특허 시계는 신호 직후의 연구 투입·신청 시계와 다르므로, 특허 경로 성공이 NSFC 또는 투자 outcome의 가용성을 보장하지 않는다. 접근·결과 선택·Gate는 미확정이며 비용·결과 열람은 수행하지 않았다. 독립 검증 대기.
