# PATSTAT 사전 대미 의존도 후보의 연결 검사

2026-11-09 KST · 생산 `/root` · 원격 기준 `037b2b488f30c74e4834c8990b8eddf41bedd166` · [기존 실접근 기록](patstat_tip_live_schema_2026-11-09.md)

로그인된 EPO TIP에서 생산 환경 `PatstatClient(env='PROD')`으로 아래 두 표준 SQL을 실행했다. 두 쿼리 모두 시작 CTE와 최종 쿼리에 `WHERE FALSE`를 두었다. 두 연결 모두 오류 없이 0행을 반환했고, TIP의 `research_patstat_schema_check_2026-11-09.ipynb` 세 번째 셀에 실행 결과를 저장했다. 이 검사는 스키마·조인 구문·접근만 확인한다. [실행 코드](patstat_tip_dose_join_probe.py) · [EPO SQL 안내서 §5](https://link.epo.org/web/patstat/new-to-patstat/en-Quick-start-guide-to-PATSTAT-SQL.pdf#page=21)

| 후보 | 연결 검사 | 측정 전에 검토할 기준 |
|---|---|---|
| 중국 출원인의 후방 특허 인용 중 미국 출원인 비중 | **통과.** `TLS212`의 인용 출처 → 인용한 `TLS211` 공개 → `TLS201` 출원·패밀리 → `TLS227/206` 출원인 국가 및 `TLS209` 분류. 피인용 공개번호 경로와 직접 피인용 출원번호 경로를 별도로 해석하고 국가 필드를 연결했다. | `CITN_ORIGIN='APP'`는 출원인이 도입한 인용을 뜻한다. 신청인이 중국 주소로 잡힌 것과 중국 특허청 출원은 구분한다. 2013–17에 최초 출원한 관측과 2017-12-31까지 실제 공개된 인용 기록의 교집합을 사전 정보 후보로 삼는다. 직접 출원번호 경로에는 해당 인용의 공개 증거가 따로 필요하다. 출원인 국가 불명, 가공·미연결 대상, 비특허 및 비특허문헌에서 추출한 특허, 동일 패밀리와 양 키 충돌을 별도 분모로 기록한다. 패밀리 쌍을 중복 제거하고 복수 출원인 국가를 분수 귀속하는 규칙이 필요하다. [PATSTAT Global 2025 가을 §§5.11, 6.24](https://link.epo.org/web/business/patstat/en-data-catalog-patsat-global-autumn-2025.pdf) |
| IP5 패밀리에서 미국 출원인 비중 | **통과.** `TLS204` 우선권 연결·`TLS201` 최초 관련 출원과 같은 DOCDB 패밀리의 출원관할 → 출원인 국가, PCT 단계 플래그, 공개일, IPC/CPC·버전을 연결했다. | IP5 2022 공식 보고서 Annex 2의 패밀리는 같은 최초 우선권에 연결되며 실용신안을 제외하고 **5개 권역 모두**에 출원 활동이 있어야 한다. 단일 IP5 관할 출원은 그 조건을 충족하지 않는다. 유럽 권역, 최초 우선권 단위와 DOCDB 단순 패밀리의 대응, PCT 국내·지역단계의 진입일과 일반 출원일 차이, 국가 귀속을 검증해야 한다. 2017년 말 기준으로 이후의 해외 진입을 배제하면 후기 코호트가 불리하다. 공통 관측기간을 확보한 이른 코호트의 민감도와 전 코호트의 우측 절단을 구분한다. 후보 분모와 미국 출원인 귀속 방식은 미확정이다. [IP5 Statistics Report 2022 Chapter 3 및 Annex 2](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=102) |

2017년까지의 날짜로 필터해도 현재 판본에서 소급 보강된 분류와 인용은 남을 수 있다. CPC 적용일·버전은 진단에 쓸 수 있으나 그 열만으로 당시 이용 가능했던 분류를 복원했다고 간주할 수 없다. 2017년까지 확인되는 발행 판본 또는 문헌상의 분류를 우선 검토하고, 불가능하면 현재 판본의 역사 자료를 사용했다는 점과 사후 갱신 민감도를 따로 보고한다. 2017년 말 공개 제한으로 생기는 최근 출원 표본의 누락도 품질 점검 대상이다.

EPO는 `PROD`를 전체 생산 환경으로 안내하고 PATSTAT이 반기별 갱신된다고 설명한다. 앞서 본 연결 별칭과 이번 연결 성공으로는 2026-11-09 실행에 연결된 정확한 배포판을 식별할 수 없다. 해당 날짜의 판본과 이후 같은 판본으로 연결하는 방법은 EPO의 확인이 필요하다. TIP 웹 약관, 플랫폼 안의 전용 조건 및 PATSTAT 벌크 라이선스의 적용 범위를 구분한다. 다음 재현 단계는 실제 판본을 식별하고 허용되는 집계표와 반출 범위를 문서화하는 것이다. 이번 검사에는 특허 기록, 기술별 분모나 dose, 배분 결과, 사용자 계정 정보의 조회·반출이 포함되지 않았다. Google Patents의 별도 dry run은 미실행 상태다. [EPO TIP 기술 소개 p.4](https://epn.epo.org/sites/default/files/2025-04/250122_-_it-cooperation_-_v1.pdf#page=4) · [EPO TIP 공개 안내](https://www.epo.org/en/searching-for-patents/data/technology-intelligence-platform) · [PATSTAT 벌크 라이선스 §1.1](https://www.epo.org/en/service-support/ordering/patstat-data-terms-and-conditions)
