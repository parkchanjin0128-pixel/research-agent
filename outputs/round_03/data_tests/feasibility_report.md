# 3회차 자료 접근 점검 — Google Patents 공개 문서

2026-11-08 · 생산자 `/root/patent_metadata_nov08` · 기준 커밋 `a812bc6748d06b39e397290f37204bf91a628fb9` · 범위: `data_feasibility`의 특허 메타데이터 한 단위. [3회차 C절](../../../prompts/round_03.md) · [1주 계획](../one_week_plan_2026-11-08.md).

**판정: 부분 진행.** `patents-public-data.patents.publications`의 공개 설명과 문서상 후보 필드를 확인했다. 현재 테이블의 스키마·리전·갱신일, 이 실행의 접근권한, 2013–17 표본 품질, 두 dose SQL의 예상 스캔량과 실행 비용은 미확인이다. 기존 사용 승인된 BigQuery 실행 프로젝트가 주어지지 않았고 이 환경에서 `bq` 및 `gcloud`가 PATH에 없었다. 실제 IAM 거부를 관측한 것은 아니다. 계정이나 자격증명을 찾지 않았고 로그인, 과금 설정, 메타데이터 API 호출, dry run, 실제 쿼리, 특허 레코드·배분 outcome 열람 및 집계를 수행하지 않았다. 이 점검에서 발생한 BigQuery 비용은 0이며, 향후 쿼리 비용은 미산정이다. 독립 검증과 심사는 대기다.

## 문서에서 확인한 범위

| 항목 | 공개 출처와 위치 | 확인 범위와 한계 |
|---|---|---|
| 테이블과 제공 범위 | [Google Cloud 출시 공지](https://cloud.google.com/blog/topics/public-datasets/google-patents-public-datasets-connecting-public-paid-and-private-patent-data), 공개 데이터 설명 첫 부분. [Google 운영 예제 저장소의 테이블 문서](https://github.com/google/patents-public-data/blob/master/tables/dataset_Google%20Patents%20Public%20Datasets.md), 첫 `patents-public-data:patents.publications` 절의 Stat 및 Schema. | 제공자가 IFI CLAIMS인 세계 특허공개 서지 및 미국 전문 자료로 소개된다. 테이블 문서의 통계 날짜는 2018-11-26으로, 현재 갱신일이나 중국의 출원·인용 완전성의 근거로 사용하지 않는다. |
| 조인·날짜·국가 | 같은 문서의 첫 Schema에서 `publication_number`, `application_number`, `country_code`, `family_id`, `publication_date`, `filing_date`, `priority_date`, `assignee_harmonized.country_code` 항목. | 공개·출원·우선권 날짜는 서로 다르다. 문서상 `priority_date`에는 출원일 대체가 가능하다. 관할을 나타내는 문서의 국가 코드와 권리자 국가 필드를 구분한다. 조화된 권리자 필드가 출원 당시 출원인 국적·소재지를 정확히 재현하는지는 별도 확인이 필요하다. |
| 기술·인용 | 같은 Schema의 `ipc.code`, `cpc.code`, `citation` 및 하위 필드. | IPC/CPC와 인용 레코드가 문서화되어 있다. 인용 공개번호·출원번호의 누락, 비특허문헌, 출원인·심사관 등 인용 출처, 패밀리 중복, 과거 시점 가용 여부는 확인하지 못했다. |
| 권한·비용 | [BigQuery tables.get](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables/get), Method·HTTP request; [Run a query](https://docs.cloud.google.com/bigquery/docs/running-queries), Required permissions·Dry run; [BigQuery public datasets](https://docs.cloud.google.com/bigquery/public-data), Before you begin·Public dataset locations·Access public datasets. | `tables.get`은 테이블의 `bigquery.tables.get` 권한을 요구하며 레코드를 읽는 절차가 아니다. 일반 쿼리의 문서상 요건은 실행 프로젝트의 `bigquery.jobs.create`와 참조 테이블의 `bigquery.tables.getData`다. Dry run은 검증과 처리량 추정을 제공하고 과금되지 않는다. 공개 데이터라고 해서 실제 쿼리가 항상 무료이거나 이 환경에서 실행 가능한 것은 아니다. 이 테이블의 리전은 별도 메타데이터로 확인한다. |

## 2013–17 사전 dose 후보와 다음 실행

- **(i) 중국 출원인의 후방 특허인용 중 미국 출원인 비중.** 중국 쪽 출원인 귀속을 검증한 인용 원천을 기준으로 `citation`을 펼치고 인용 대상 공개번호로 연결한다. 출원번호 보조 연결은 다중 매치 규칙을 먼저 문서화한다. 중복 제거, 출원인·심사관 인용 분리, 다국적 공동출원, 미연결·국가 불명 인용의 분모 및 극단 가정 민감도를 지목·비지목 기술에 동일 적용한다. 2017년 말 이후 공개되거나 추가된 인용이 2013–17 의존도에 섞이는지 확인한다. 이를 배제할 정보가 부족하면 확인된 사전 공개분만 쓰는 방안의 선택 편의와, 사후 보강된 역사 자료를 쓰는 방안의 정보 누출을 각각 평가한다.
- **(ii) 기술별 IP5 패밀리의 미국 비중.** `family_id`, 관할, 우선권·출원 날짜, 출원인 귀속 후보, IPC/CPC를 사용한다. [IP5 Statistics Report 2022](https://www.cnipa.gov.cn/attach/0/0895b234b2a848a489050542f0908558.pdf) 제5장 *Patent Families* 및 Annex 2는 분모·출원 기원 정의의 비교 기준이다. 해당 통계의 IP5 패밀리 정의와 ‘IP5 관할 중 하나에 보이는 패밀리’, ‘미국 출원인 기원’과 ‘USPTO 출원’을 구분한다. 정확한 분모·분자, 국가 복수 귀속, 패밀리 중복 제거, 기술 다중매핑 및 사전 시점 기준을 정의하기 전에는 재현 가능하다고 판정하지 않는다. 사후 해외 확장이나 사후 분류 변경도 사전 지표에 섞일 수 있다.
- **재개 순서.** 이미 승인된 실행 프로젝트와 권한이 확인되면 테이블 메타데이터만 조회하여 실제 위치·스키마·갱신일과 접근 결과를 기록한다. 이후 후보별 컬럼·날짜·조인 구조를 반영한 읽기 전용 GoogleSQL을 검토하고 `bq --project_id=PROJECT --location=LOCATION query --use_legacy_sql=false --dry_run` 또는 API `dryRun=true`로만 검증한다. 쿼리 판본, 위치, 오류 또는 예상 처리 바이트와 단가 가정별 예상 비용을 따로 남긴다. 오류·경로 부재는 미실행/평가 불가로 기록한다. 비용 추정을 위해 실제 실행으로 전환하지 않는다.

## 배분 outcome 열람 전 제안할 판정 기준

| 항목 | 사전 점검과 아직 필요한 입력 |
|---|---|
| 시점과 오염 | 후보 월별 창은 2018-12~2019-04. 기술·거래별 최초 China-binding cutoff, 창 이전에 시작해 창에도 남은 조치, 신호 일시 및 데이터의 결정·출원·공개 시계를 확인한 후 적용한다. 특허의 공개월이나 등록월을 의사결정월로 대체하지 않는다. 날짜 분해가 안 되는 연간 집계로 제한 전 계수를 식별하지 않는다. |
| 지지 범위와 crosswalk | 같은 사전 자료·코드로 지목/비지목의 CPC/IPC→기술 매핑률, 국가·인용 연결 손실, 기술별 분모, dose 분산·중첩, FE 및 정책 노출 제거 후 변동과 독립 기술 클러스터 수를 확인할 계획이다. 최소 지지 범위·분모·매핑률과 출원인 귀속 규칙은 설계 담당자가 결과 열람 전에 근거와 함께 제안한다. 승인된 사전 dose 표본과 버전 고정 crosswalk가 필요하다. |
| 검정력과 포기 | 최소 실질 효과, 비교국·기술별 유효 클러스터 수, 잔차 dose 분산, 사전 기간에서 별도 허용된 잔차 변동·시계열 상관 또는 외부 가정, 추론·다중검정 규칙을 정해 MDE를 시나리오별로 계산한다. 수치 입력 미확보로 현재 MDE는 미산정이다. 실제 제한의 분리 불가, dose 지지 범위 부족/매핑 실패, placebo 후 선행 추세 잔존, 통제 후 dose–중국 정책 구분 불가, 또는 MDE가 최소 실질 효과보다 큰 경우에는 사전 규칙에 따라 기술적 분석 전환을 제안한다. 자료·권한 미확보는 이들 실패를 입증하지 않는다. |

VC, NSFC, 논문, 상장기업 R&D, 시장 수익률·기업 기제, HS/무역 의존도와 crosswalk의 실제 자료 접근은 각각 대기다. 특허 outcome으로서의 가용성·공개 지연도 대기다. 이번 작업은 Gate 변경이나 crosswalk·treatment·primary outcome·신호 가중치의 확정이 아니다.
