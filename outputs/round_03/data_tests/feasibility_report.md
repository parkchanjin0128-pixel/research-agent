# 3회차 특허 자료 접근 점검 — Google Patents와 EPO TIP

수정 생산자 `/root/data_r1_producer_nov11` · 2026-11-11 KST · 검토 기준 `b282c5b428c9c318c194e2faee4293053c6165c2` · 단위 `data_feasibility`. 원 생산: 2026-11-08, `/root/patent_metadata_nov08`, 기준 `a812bc6748d06b39e397290f37204bf91a628fb9`. [3회차 C절](../../../prompts/round_03.md) · [1주 계획](../one_week_plan_2026-11-08.md) · [원 보고서 독립 검증](../verification_data_feasibility_nov09.md) · [심사 DF-R01–03](../../reviews/round_03_internal_review_2.md).

**판정: 부분 진행.** Google Patents 공개 문서의 필드와 절차는 확인되었다. 11월 9일 EPO TIP 생산 기록은 별도 경로에서 PATSTAT Global 연결, 명시 열 및 두 후보 조인의 구문이 작동했음을 보여 준다. 두 검사 모두 데이터 행을 반환하지 않도록 설계되었다. Google Patents BigQuery의 두 dry run은 각각 미실행이며, 두 후보의 실제 사전 관측 가능성, 표본 포괄성, 기술별 dose와 지지 범위, 제한 전 분석창과 MDE는 미확인이다. 이번 수정은 기존 증거와 판정 규칙을 문서화한 생산자 대응이다. DF-R01–03은 독립 재검증 및 재심사 전까지 open이다.

## 두 접근 경로의 확인 범위와 재개 조건 (DF-R01)

| 경로 | 확인된 근거 | 미확인 및 다음 입력 |
|---|---|---|
| Google Patents 문서 | [Google Cloud 출시 공지](https://cloud.google.com/blog/topics/public-datasets/google-patents-public-datasets-connecting-public-paid-and-private-patent-data)의 공개 데이터 설명과 [Google 운영 예제 저장소](https://github.com/google/patents-public-data/blob/master/tables/dataset_Google%20Patents%20Public%20Datasets.md)의 첫 `patents-public-data:patents.publications` Stat 및 Schema. IFI CLAIMS가 제공하는 세계 특허공개 서지 및 미국 전문으로 소개된다. 문서의 통계 날짜는 2018-11-26이다. | 문서의 통계 날짜는 현행 갱신일이나 중국 출원·인용 완전성의 증거가 아니다. 현행 스키마·리전·갱신일·접근권한과 2013–17 표본 품질은 미확인이다. |
| Google Patents 실행·비용 | 원 생산 기록상 승인된 BigQuery 실행 프로젝트를 받지 못했고 당시 `bq`와 `gcloud`가 PATH에 없었다. IAM 거부를 관측한 것은 아니다. 자격증명 탐색, Google 로그인·과금 설정, 메타데이터 API 조회, 두 dry run, 실제 쿼리와 레코드 추출은 수행하지 않았다. 원 점검에 발생한 BigQuery 비용은 생산 기록상 0이다. | 승인된 실행 프로젝트·권한·실행 경로 필요. 현재 예상 처리 바이트와 실제 실행 예상 비용은 양 후보 모두 미산정이며, 원 점검 비용 0을 향후 실행 예상 비용으로 읽지 않는다. |
| EPO TIP PATSTAT Global 연결·열 | [11월 9일 스키마 생산 기록](patstat_tip_live_schema_2026-11-09.md) (기준 `47f513f97d608b34fe2dbda435a5abca9eb484cb`). 당시 로그인된 TIP에서 `PatstatClient(env='PROD')`로 명시 열의 `WHERE FALSE` 쿼리가 9개 테이블에서 오류 없이 0행을 반환했고, `INFORMATION_SCHEMA.COLUMNS`에서 요청한 33/33 열과 유형을 확인했다. 출원·공개, 당사자·국가, IPC/CPC 및 인용 연결키가 해당 범위다. | 0행은 조건의 결과다. 실제 원자료 건수나 결측률을 뜻하지 않는다. 생산 연결 별칭과 테이블 설명으로 정확한 배포 판본을 확인하지 못했다. |
| EPO TIP 두 후보 조인 | [11월 9일 조인 생산 기록](patstat_tip_dose_joins_2026-11-09.md) (기준 `037b2b488f30c74e4834c8990b8eddf41bedd166`). 출원인 후방 인용 및 IP5 패밀리 연결 SQL의 시작 CTE와 최종 SELECT에 `WHERE FALSE`를 적용해 두 쿼리 모두 오류 없이 0행을 반환했다. 해당 기록이 가리키는 노트북과 [재현 코드](patstat_tip_dose_join_probe.py)는 검증 출발점이다. | 구문·연결 증거만 있다. 조인 정확도, 사전 정보 복원, 실제 dose·분모 및 대표성, Google 테이블 권한·dry run·비용은 검증하지 못했다. |
| EPO TIP 한도·판본·라이선스 | 스키마 기록의 화면 표시: 최근 7일 다운로드 10 GiB, BigQuery 연산 1,000 slot-hours, 디스크 30 GB. 점검 뒤 표시 정밀도에서 다운로드 0 및 0.0 slot-hours였다. 별도 Google Cloud 프로젝트·과금 계정·유료 API·키를 사용하지 않았다. | 한도와 계기판은 개별 작업의 비용·바이트 영수증이나 반출·재배포 권한이 아니다. EPO의 실행일 판본 식별 및 동일 판본 고정 경로, TIP 웹 약관·플랫폼 전용 조건·[PATSTAT 벌크 라이선스 §1.1](https://www.epo.org/en/service-support/ordering/patstat-data-terms-and-conditions)의 적용 범위, 허용 집계와 반출·재배포 범위를 각각 문서화한다. 실제 표본 커버리지는 별도 승인 후 검증한다. |

Google 문서의 첫 Schema에는 `publication_number`, `application_number`, `country_code`, `family_id`, `publication_date`, `filing_date`, `priority_date`, `assignee_harmonized.country_code`, `ipc.code`, `cpc.code`와 반복 `citation`이 있다. 공개·출원·우선권 날짜는 별개이며 문서상 `priority_date`는 출원일로 대체될 수 있다. 관할과 권리자 국가는 별개이고, 조화된 권리자 국가를 출원 당시 출원인 주소·거주지나 국적으로 대체할 근거는 확인되지 않았다. 인용의 공개·출원번호, 출처와 비특허문헌 필드가 있다는 사실은 결측률, 중복 및 과거 가용성을 입증하지 않는다.

Google 경로는 승인된 실행 프로젝트와 주체가 확인되면 [`tables.get`](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get)으로 실제 스키마·리전·갱신일과 권한 결과만 기록한다. `tables.get`은 `bigquery.tables.get`을 요구하며 행을 읽지 않는다. [일반 쿼리의 권한](https://docs.cloud.google.com/bigquery/docs/running-queries#required_permissions)은 실행 프로젝트의 `bigquery.jobs.create`와 참조 테이블의 `bigquery.tables.getData`다. 스키마를 확인한 후 (i) 원천 출원·기술 → 인용 펼치기 → 피인용 공개/출원 연결 → 출원인 귀속, (ii) 최초 우선권 → 패밀리·관할/단계 → 기원·기술 귀속을 구현하는 두 읽기 전용 GoogleSQL을 각각 검토하고 판본·해시와 날짜 매개변수를 고정한다. 사전 시점 증거가 없는 필드는 아래 규칙에 따라 미확인으로 두며, 판정할 수 없는 항목을 임의 필드로 대체하지 않는다. 스캔 추정용 SQL에는 대상 열·조인·코호트 조건을 반영하고 TIP의 강제 0행 필터를 옮기지 않는다.

허용 경로에서만 `bq --project_id=PROJECT --location=LOCATION query --use_legacy_sql=false --dry_run` 또는 API `dryRun=true`로 검증한다. [공식 dry run 설명](https://docs.cloud.google.com/bigquery/docs/running-queries#dry-run)과 [공개 데이터셋의 비용·위치 안내](https://docs.cloud.google.com/bigquery/public-data)에 따라 dry run 자체의 무과금과 실제 실행의 추정 비용을 구분한다. 후보별로 SQL 버전·해시, 실행일과 리전, 결과 또는 오류, 예상 처리 바이트, 과금 방식·해당 리전 단가·무료 한도 적용 조건을 기록한다. 온디맨드일 때는 추정 바이트를 단가 단위로 변환하여 실제 실행 비용의 가정을 명시하며, 용량 과금에서는 스캔 바이트에 온디맨드 단가를 곱하지 않는다. (i) dry run·예상 처리 바이트·비용: **미실행·미확인·미산정**. (ii) dry run·예상 처리 바이트·비용: **미실행·미확인·미산정**. 경로가 없거나 오류가 나면 사유와 다음 필요 입력을 기록하고 DF-R01을 open으로 유지한다. 비용 추정을 위해 실제 쿼리로 전환하지 않는다.

## 두 사전 dose 후보의 2017년 말 기준 판정 (DF-R02)

코호트 편입일과 정보 관측 가능일을 별도 기록한다. 2013-01-01~2017-12-31 코호트에서 지표 구성에 필요한 사실마다 사건일, 최초로 그 사실을 확인할 수 있는 공개일, 당시 공개 문헌 또는 날짜가 고정된 출처·판본을 기록한다. 필요한 사실의 관측 가능일 중 가장 늦은 날이 2017-12-31 이하여야 엄격한 사전 후보에 포함한다. 이후 공개가 확인되면 사전 대상에서 제외하고, 날짜 또는 당시 판본 근거가 없으면 **`사전 관측 가능 미확인`**으로 표시한다. 미확인을 0 또는 비미국으로 채우지 않는다. 현재 판본의 소급 보강은 사건 날짜 필터를 통과할 수 있다. CPC 적용일·버전은 진단 자료이며 당시 분류의 증거로 단독 사용하지 않는다. 당시 문헌 또는 당시 발행 판본의 분류와 버전 고정 기술 crosswalk를 우선한다.

| 후보 | 코호트와 정보 관측 기준 | 연결·분모·귀속 규칙 후보 |
|---|---|---|
| (i) 중국 출원인의 후방 특허 인용 중 미국 출원인 비중 | 인용 원천의 최초 출원이 2013–17인 코호트. 인용을 실제 포함한 공개 문헌이나 당시 판본이 컷오프 이전에 있어야 한다. 원천의 최초 공개일 또는 피인용 문헌의 출원일만으로 해당 인용의 추가·공개 시점을 판정하지 않는다. 공개번호와 직접 출원번호 연결 모두 인용 자체의 사전 공개 증거와 피인용 대상 식별·국가 귀속의 사전 증거가 필요하다. | TIP에서는 `TLS212 → TLS211 → TLS201`과 `TLS227/206` 출원인 국가, `TLS209` 기술을 연결하는 경로를 점검했다. `CITN_ORIGIN='APP'`의 출원인 도입 인용을 우선 후보로 두고 심사관·기타·출처 불명은 따로 기록한다. 중국 주소의 출원인과 중국 관할 출원을 구별한다. 피인용 공개번호와 출원번호를 별도로 풀고, 단일 일치와 양쪽 일치만 확정 연결 후보로 삼는다. 다중 매치와 키 충돌을 별도 집계하고 자의적으로 선택하지 않는다. 동일 패밀리 내부 인용, 비특허·비특허문헌 경유 특허는 별도 범주로 둔다. 패밀리 쌍의 중복을 제거하고, 복수국 출원인은 동일한 분수 귀속 규칙으로 검토한다. 기술별 후보 분모는 적격 후방 특허 인용, 후보 분자는 미국 출원인 귀속분이다. 식별·국가가 불명인 적격 인용은 연결 가능한 분모와 별도로 남겨 포괄 분모의 하한·상한을 비교한다. |
| (ii) 기술별 IP5 패밀리의 미국 출원인 비중 | 같은 최초 우선권을 형성한 출원이 2013–17인 코호트. 5개 권역 각각의 적격 활동과 최초 우선권 연결이 실제로 컷오프 이전에 공개 근거로 확인되어야 한다. 최초 출원일이나 PCT 국제출원·지정일은 국내·지역 단계 진입일의 대체물이 아니다. 후기 해외 진입과 늦은 공개를 분리해 우측 절단을 표시한다. | TIP에서는 `TLS204` 우선권·`TLS201` 출원, DOCDB 패밀리, 관할, PCT 단계, 공개, 출원인 국가 및 IPC/CPC 버전을 연결하는 경로를 점검했다. 최초 우선권 단위와 DOCDB 패밀리의 대응 및 다중 우선권을 별도 검토한다. 실용신안 제외, EPC 국가 관청과 EPO를 포함한 유럽 권역, 일본·한국·중국·미국 각 권역을 적용한다. 동일 최초 우선권 단위를 기술 안에서 중복 제거하고 기술 다중 매핑은 사전 고정한 분수 규칙 등으로 검토한다. 기술별 후보 분모는 사전 확인된 5권역 패밀리, 후보 분자는 최초 우선권을 형성한 출원의 미국 출원인 거주지 귀속분이다. 국가는 USPTO 출원 여부나 국적으로 대체하지 않으며, 복수 출원인·국가 불명의 분수 귀속과 불명 분모를 별도로 검토한다. 공식 보고서의 첫 기재 출원인 또는 발명자 거주지 기원 규칙과 연구 후보의 출원인 분자는 같다고 가정하지 않는다. |

판본과 사용 범위가 확인된 뒤, 별도 승인된 사전 dose 표본에서만 동일 규칙으로 지목/비지목별 코호트·사전 공개 제한에 따른 손실, 날짜·귀속·인용 연결 불명, 기술 매핑률, 기술별 분모, dose 분산·중첩을 비교한다. FE 및 중국 기술정책 노출을 제거한 뒤의 변동과 독립 기술 클러스터 수도 그때 확인한다. 조인·분류·귀속 규칙과 최소 분모·매핑률·지지 범위는 결과 열람 전에 근거와 함께 제안한다. 엄격한 재현이 안 되면 관측기간을 맞춘 더 이른 종료의 성숙 코호트를 별도 민감도로 검토한다. 현 판본의 소급 자료나 단일 IP5 관할 기준은 명시적으로 다른 proxy로만 검토하며, 사전 규칙을 충족하지 못한 후보를 엄격한 dose로 채택하지 않는다. 두 proxy는 인용 연결과 국제 특허화라는 서로 다른 대상을 측정한다. 어느 쪽도 통제가 실제로 시행되었을 때 중국의 잠재 손실을 직접 관측하지 않는다.

## IP5 정의의 정확한 출처 (DF-R03)

*IP5 Statistics Report 2022* (USPTO 편집, 2023-11)의 [목차 PDF 7쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=7)과 본문을 구분한다.

- 제3장 *Worldwide Patenting Activity*, *Patent Families* 절 [인쇄 50쪽 / PDF 59쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=59): 최초 출원의 우선권과 공개 시차, Table 3. 같은 절 [인쇄 52쪽 / PDF 61쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=61)은 EPC 국가 관청 포함, [인쇄 55쪽 / PDF 64쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=64)의 Fig. 3.17은 우선권 형성 출원의 첫 기재 출원인 또는 발명자 거주지에 따른 기원 구분의 근거다.
- 제5장 *The IP5 Offices and the Patent Cooperation Treaty (PCT)*, *Patent Families and PCT* 절 [인쇄 78쪽 / PDF 87쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=87): 패밀리의 PCT 이용 정의와 Fig. 5.5. 이어지는 [인쇄 79쪽 / PDF 88쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=88)의 Fig. 5.6은 5개 권역 활동과 기원별 PCT 이용을 설명한다.
- Annex 2 *Definitions of terms and statistics on procedures*, *Patent Families* 항목 [인쇄 92쪽 / PDF 101쪽](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf#page=101): 같은 최초 우선권, 실용신안 제외, 다섯 권역 모두의 활동 증거. 하나의 IP5 관할에서 관측되는 패밀리와 다르다.

## 배분 outcome 접근과 판정의 경계

- [11월 9일 독립 접근 검증](../verification_outcome_access_nov09.md)의 **OA-02는 `contradicted`**다. NSFC 일반과제 표의 `受理申请`은 표에서 확인되는 연간 접수 집계로 기술한다. 전국 합계가 동시기 집중접수 보고의 초심 전 `接收` 건수와 일치하므로 초심 통과 신청 분모로 읽지 않는다. 사업·세부행의 포함·제외 규칙은 미확인이다. 연간 신청·승인 열과 직접비는 구분되지만 지급일·개별 제출일이나 월별 기술 패널을 확보한 것은 아니다. 별도로 그 검증에서 후보 창 밖 특허 한 건의 날짜 구분과 검색 서비스 한계를 확인했으며, 월×기술 모집단 포괄성이나 무료 일괄 추출을 입증하지 않았다.
- 2018-12~2019-04는 후보 창이다. 기술·거래별 최초 China-binding cutoff, 창에 걸쳐 남은 선행 조치, 신호 일시, 결정·출원·공개 시계를 별도로 확인해야 한다. 공개·등록월을 의사결정월로 대체하지 않고 연간 집계에서 제한 전 월별 계수를 식별하지 않는다. 비교국 포괄성도 미확인이다.
- MDE는 최소 실질 효과, 유효 클러스터 수, 잔차 dose 분산, 별도 허용된 사전 잔차 변동·시계열 상관 또는 외부 가정, 추론·다중검정 규칙으로 사전 시나리오를 정한 후 산정한다. 입력값 미확보로 수치는 미산정이다. 실제 제한 분리 불가, dose 지지 범위 부족·매핑 실패, placebo 후 선행 추세 잔존, 통제 후 dose와 중국 정책 구분 불가, 또는 MDE가 최소 실질 효과를 초과할 때는 사전 규칙에 따라 기술적 분석 전환을 검토한다. 자료·권한 미확보는 이 기준에 도달했다는 증거가 아니다.
- VC, NSFC, 논문, 상장기업 R&D, 시장 수익률·기업 기제, HS/무역 의존도와 crosswalk의 실제 분석 자료 및 특허 outcome의 가용성·공개 지연은 대기다. 이번 수정에서 원자료나 배분 outcome을 열람·추출·집계하지 않았다. Gate, freeze, crosswalk, treatment, primary outcome 및 신호 가중치 판정은 별도다.
