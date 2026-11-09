# EPO TIP 실제 PATSTAT Global 연결 점검 · 2026-11-09 KST

생산 `/root` · 20:38–20:40 KST · 기준 GitHub `47f513f97d608b34fe2dbda435a5abca9eb484cb` · [선행 접근 점검](patstat_tip_access_nov09.md) · [재현 코드](patstat_tip_live_schema_probe.py)

**판정: 로그인된 EPO TIP의 PATSTAT Global 실데이터 연결과 스키마 확인 성공.** 사용자가 로그인한 EPO 작업공간에서 공식 Python 연결 `PatstatClient(env='PROD')`와 표준 SQL을 사용했다. 생산 데이터 연결에서 아래 9개 테이블의 명시 열만 요청하는 `WHERE FALSE` 쿼리가 모두 오류 없이 0행으로 끝났다. 별도로 `INFORMATION_SCHEMA.COLUMNS`에서 요청한 33/33개 테이블–열 조합과 데이터 타입을 확인했다. 0행은 검사용 SQL 조건의 결과이며 자료 건수나 관측 가능성을 뜻하지 않는다. [EPO TIP 공식 예제](https://tip.epo.org/hub/docs/patstat/notebooks/PATSTAT-Primer.html) · [공식 API 설명](https://tip.epo.org/hub/docs/patstat/api/patstat.html)

| 테이블 | 확인한 필드 |
|---|---|
| TLS201_APPLN | 출원 ID·관할·유형, 출원일, 최초 관련 출원일, 최초 공개일, DOCDB 패밀리 ID |
| TLS206_PERSON · TLS207_PERS_APPLN · TLS227_PERS_PUBLN | 당사자 ID·국가, 출원/공개 연결, 출원인 순번 |
| TLS209_APPLN_IPC · TLS224_APPLN_CPC · TLS225_DOCDB_FAM_CPC | 출원·패밀리 분류와 CPC 적용일·버전 |
| TLS211_PAT_PUBLN · TLS212_CITATION | 공개 ID·날짜, 인용 출처, 피인용 공개·출원·비특허문헌 연결키 |

33개 필드 유형은 `INT64` 18, `STRING` 9, `DATE` 6개다. 데이터베이스 연결은 제공자의 생산용 별칭이며 배포 판본을 표시하지 않는다. 출원·공개 테이블의 `INFORMATION_SCHEMA.TABLE_OPTIONS`에서 설명·태그를 조회했지만 명시적인 연도·계절 판본명을 확인하지 못했다. EPO 공개 페이지에 최신 사전이 있다는 이유만으로 실제 연결이 그 판본이라고 간주하지 않는다. [EPO 판본 목록](https://www.epo.org/en/about-us/observatory-patents-and-technology/observatory-tools/patstat/latest)

TIP의 실행 화면은 최근 7일 다운로드 한도 **10 GiB**, BigQuery 연산 한도 **1,000 slot-hours**, 작업공간 디스크 **30 GB**를 표시했다. 점검 후에도 계기판 표시 정밀도에서 다운로드 0 및 0.0 slot-hours였다. 이는 이 환경의 한도 표시이며 개별 작업의 비용·바이트 영수증은 아니다. 별도 Google Cloud 프로젝트·과금 계정·유료 API·키는 사용하지 않았다. 원자료를 조회, 다운로드, GitHub에 게시하지 않았다. 화면의 다운로드 상한은 재배포 권한과 별개다. TIP 데이터 외부 반출 조건과 표본의 실제 포괄성은 미검증이다. [EPO 무료 TIP 안내](https://www.epo.org/en/searching-for-patents/data/technology-intelligence-platform)

**재현 및 다음 단계.** EPO 작업공간에 `research_patstat_schema_check_2026-11-09.ipynb`를 저장했다. 계정별 URL과 원자료는 공유하지 않는다. 같은 EPO 환경에서 재현 코드의 두 셀을 순서대로 실행할 수 있다. 다음은 공개 범위와 고정 판본을 확인한 뒤, 2013–17 사전 미국 의존도 후보의 인용·패밀리 연결을 결과행 없는 쿼리로 점검하는 것이다. 실제 dose 표본 및 출원·연구·자본 배분 결과의 열람·집계는 별도 범위 확인 후 진행한다. 앞선 Google Patents의 별도 BigQuery 접근·두 dry run, 적격 기술별 제한 전 관측창, 시장 반응 및 검정력은 이 점검의 범위가 아니다. 이 메모는 생산 기록이며 독립 검증·심사와 Gate 판정은 대기다.
