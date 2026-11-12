# 실증 수치 독립 검증 기록

검증자 `/root/nov12_empirical_verify`, 검증일 2026-11-12 (Asia/Seoul). Producer의 데이터·코드는 수정하지 않았다. 이 파일만 검증 산출물로 작성했다. 문헌·발표 본문 작성은 하지 않았다.

## Claim별 판정

| Claim | 판정 | 근거와 범위 |
|---|---|---|
| 2017/2018/2019 공보의 총 R&D·기초연구·수행부문 금액, 보고 성장률·비중·당초 GDP 집약도 | verified | 공식 원문 문단과 전사값 대조. 2019 NBS HTML은 fetch timeout이므로 MOST의 동일 공동공보 PDF 사용. |
| 2013~2020 전체 8개년 전사값 | verified | 각 공식 공보를 직접 열어 12개 numeric fields, 총 96개 값을 별도 전사한 뒤 독립 Python Decimal로 input JSON과 대조. |
| 기초연구 비중 2017 5.5407%, 2018 5.5412%, 2019 6.0315%; 변화 2018 약 +0.0005%p, 2019 +0.4903%p | verified | 아래 독립 계산. 공보의 반올림 비중은 5.5→5.5→6.0%. |
| 2018에 기초연구 증가율이 즉시 가속하지 않았고 2019 상승이 두드러진다 | verified | 공보 증가율 2017 18.5%, 2018 11.8%, 2019 22.5%; 구성비도 일치. 기술적 관측에 한정. |
| 2019 대학·정부연구기관 증가율이 기업보다 높다 | verified | MOST PDF p.1: 23.2%, 14.5%, 11.1%. 기업 수행비중 77.4→76.4%, 대학 7.4→8.1%. |
| 2020 기초연구 성장률 9.8%, 계산 비중 6.0140% | verified | 2020 NBS 공보 및 독립 계산. |
| 기간 평균 및 2013~2017 로그추세 외삽 수치 | verified | Decimal 산술과 NumPy least-squares로 별도 계산; 아래 실행 결과 참조. |
| GDP 공표·개정판본 구분 | verified | 2015 공보 revision table 2013 2.01→1.99, 2014 2.05→2.02; 2016 주석 2015 2.06; 2018 주석 2017 2.15; 2019 PDF 주석 2018 2.14; 2020 주석 2019 2.24. 최초 2013 2.08과 개정표의 과거값 2.01을 구분한 설명 적절. |
| 2015 문서일/웹 공개일은 2016-11-10/11 | verified | NBS 본문 날짜와 게시 header에서 독립 확인. |
| 2018/2019/2020 조사방법 문구가 다르다 | verified | 2018 대중형 서비스업, 2019 규모이하 공업기업 표본추계, 2020 규모이하 공업·서비스업 표본추계. 문구 차이만으로 실질 시계열 단절을 확정할 수 없음. |
| 수출통제가 증가·재배분을 유발했다; 사전 대응·민간기업 반응을 식별했다 | unverifiable | 8개 국가 연간 집계, 통제집단·소유형태·노출도·연중 사건순서 없음. Producer도 이런 인과 주장을 하지 않는 것으로 확인. |
| PATSTAT 수치·코드 | unverifiable / deferred | Parent의 명시적 대기 지시로 검증하지 않았으며 verified 범위에 포함하지 않음. |
| 전사·계산에서 발견된 모순 | contradicted 항목 없음 | 아래 해시 버전과 실제 확인 범위에 한함. |

## 공식 원문 재접근

검증자가 직접 연 원문이다. 각 공보 I장의 총액·활동유형·수행주체 문단과 날짜·주석을 대조했다. PDF는 p.1 수치, p.2 GDP 주석, p.5 조사방법을 확인했다.

| 보고연도 | 공식 원문 | 공개일 |
|---|---|---|
| 2013 | [NBS 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902123.html) | 2014-10-23 |
| 2014 | [NBS 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902124.html) | 2015-11-23 |
| 2015 | [NBS 공보](https://www.stats.gov.cn/sj/zxfb/202302/t20230203_1899323.html) | 2016-11-11 |
| 2016 | [NBS 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902126.html) | 2017-10-10 |
| 2017 | [NBS 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902127.html) | 2018-10-09 |
| 2018 | [NBS 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902128.html) | 2019-08-30 |
| 2019 | [MOST 공동공보 PDF](https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/kjtjbg/kjtj2020/202009/P020200917363989375844.pdf) | 2020-08-27 |
| 2020 | [NBS 공보](https://www.stats.gov.cn/sj/tjgb/rdpcgb/qgkjjftrtjgb/202302/t20230206_1902130.html) | 2021-09-22 |

## 한계

- 아래 해시 버전만 검증했다. 원문 서버의 raw HTML/PDF bytes를 로컬 보존·해시하지 않았으므로 해시는 로컬 검증 대상 파일의 해시다.
- 원문 공표치 전사와 산술을 검증했으며 공식 통계 자체의 조사오차·개정 적절성·불변가격 계열을 검증한 것은 아니다. 최신 GDP 판본의 일관된 intensity series 재구축도 하지 않았다.
- 반올림된 명목 수준에서 전년비를 계산했으므로 공보의 한 자리 보고율과 작은 차이는 허용된다. 2018 비중 변화 약 +0.00055%p는 반올림 금액에서 나온 값으로, 그 정밀도에서 경제적 증가가 관측됐다고 해석하면 안 된다.
- 과거 공보의 조사설계 비교성 전체 감사 및 다른 국가·산업·기업 데이터 대조는 범위 밖이다. 국가 집계에서 특정 산업·민간자본·선제 대응으로 확장할 수 없다.
- 최초 producer 재실행은 시스템 temp의 sandbox PermissionError로 실패했다. 독립 산술 검증은 그 전에 통과했으며 재실행은 workspace `.build` 임시 폴더로 이동했다.

## 독립 계산·코드 실행 결과

Python 3.12.14, NumPy 2.3.5. Producer import 없이 독립 inline Python. 원문 별도 전사 96개 numeric fields exact equality PASS; 연간 136개 field comparisons (year/null 포함) PASS; 기간 평균 9개 PASS. Decimal 40자리 정밀도로 증가율 100×(당해−전년)/전년, 비중 100×기초/총액, %p 차이를 계산했다.

| 연도 | 총 R&D YoY (%) | 기초 YoY (%) | 기초 비중 (%) | 비중 변화 (%p) |
|---|---:|---:|---:|---:|
| 2017 | 12.307437152 | 18.544173047 | 5.540693282 | +0.291501807 |
| 2018 | 11.767512396 | 11.778575090 | 5.541241698 | +0.000548415 |
| 2019 | 12.530300489 | 22.487160675 | 6.031539587 | +0.490297890 |
| 2020 | 10.158691450 | 9.838274933 | 6.013995761 | -0.017543826 |

기간 단순평균 (CAGR 아님):

- `pre_2018_growth_years_2014_2017`: total 10.419411018%, basic 15.180637027%, share change 0.213951198%p.
- `2018_2019_growth_years`: total 12.148906443%, basic 17.132867882%, share change 0.245423152%p.
- `post_2018_growth_year_2019_only`: total 12.530300489%, basic 22.487160675%, share change 0.490297890%p.

NumPy `linalg.lstsq`의 독립 로그추세 외삽(actual/prediction−1):

- `rd_total_100m_rmb` 2018: +2.431007933%.
- `rd_total_100m_rmb` 2019: +4.522067449%.
- `rd_total_100m_rmb` 2020: +4.408011999%.
- `basic_research_100m_rmb` 2018: -1.364237121%.
- `basic_research_100m_rmb` 2019: +4.805691509%.
- `basic_research_100m_rmb` 2020: -0.138412993%.

Producer 별도 재실행 exit 0; stderr ''; 구조·값 완전 일치 PASS; byte-for-byte 일치 True; rerun SHA-256 `00266ad2e8550329c1ab174fc557473a71f555356fdeef0efcc119380a94270d`. 임시 실행 폴더 자동 정리, 원본 4개 파일 해시 불변 PASS. 산식 비교 허용오차 rel 1e-12, abs 1e-10; prediction abs 1e-8.

```text
2017: total YoY 12.307%; basic YoY 18.544%; basic share 5.5407%; share change 0.2915 pp
2018: total YoY 11.768%; basic YoY 11.779%; basic share 5.5412%; share change 0.0005 pp
2019: total YoY 12.530%; basic YoY 22.487%; basic share 6.0315%; share change 0.4903 pp
2020: total YoY 10.159%; basic YoY 9.838%; basic share 6.0140%; share change -0.0175 pp
Wrote package-root/.build\nbs_verifier_htcn_vru\official_rd_derived.json
DESCRIPTIVE ONLY: no causal identification.
```

## 검사 파일 SHA-256

- `data/official_rd_series.json`: `95764a713dd5eebb9909ed42fa6bbd7a01196770f5410057fa868a5637fa290c`
- `data/official_rd_derived.json`: `00266ad2e8550329c1ab174fc557473a71f555356fdeef0efcc119380a94270d`
- `scripts/compute_official_rd.py`: `a29a6b56d0ddefce0629c17b90750fef3ee2927c428fa60437803b0837e5c14a`
- `empirical_sources.md`: `a2b09d275ff9907badc2bca8c6a15baf082a1280e6ee18a7d7ca4fa83587c5e6`

## PATSTAT 최종본 추가 audit (2026-11-12)

이 절은 **저장 notebook 실행출력 audit와 SQL 정적구조 검증**이다. 검증자는 TIP에 로그인하거나 SQL을 서버에서 재실행하지 않았다. 같은 계정의 실접근과 UI 실행은 parent만 진행했다. 따라서 서버 데이터의 진실성·완전성까지 독립 실접근으로 재확인했다는 뜻은 아니다. 앞 절의 PATSTAT deferred 상태는 이 절에 기재한 범위만큼 갱신된다. 초기 untrimmed 집계 파일은 계산 입력으로 사용하지 않았다.

### Claim 판정

| Claim | 상태 | 근거 |
|---|---|---|
| 최종 JSON raw는 저장 notebook의 trimmed 실행출력이다 | verified (artifact audit) | 별도 JSONDecoder로 두 marker 출력 독립 추출, JSON raw와 완전 일치; notebook SHA-256 일치. |
| 실행코드 3개 이상 보존 | verified | notebook cell 4/5/6/7의 4개 코드와 executed_cells 파일 완전 일치. 각 cell execution_count와 output 존재 확인. 최종 분석용은 trimmed cell 6/7 두 쿼리이며 앞 두 셀은 이전 진단 기록. |
| 최종 percentages·totals·ranks·CSV | verified | 독립 Decimal로 20개 비율, 4개 합계, 2개 순위와 CSV 전체 필드 대조. 아래 실행 결과 참조. |
| 최종 추출에 초기 untrimmed 수치가 섞이지 않음 | verified | extractor는 두 TRIMMED marker만 JSON에 넣음. code archive에는 이전 코드도 남지만 최종 raw는 trimmed만 포함. |
| causal effect 또는 중국 전체·민간기업 대표성 | unverifiable | 전후 결과나 통제집단 없는 pre-2018 linkage sample. 아래 selection·주소 누락·중복·현재판 한계. |
| 정확한 PATSTAT release와 2017 당시 이용 가능했던 데이터 상태 | unverifiable | PROD가 제공하는 현재 dataset을 호출하며 release label 미해결. 날짜 제한은 publication/event date를 제한하지만 현재판의 정정·IPC·주소·가족구성 소급변경은 배제하지 못함. |
| 산술·추출 모순 | contradicted 항목 없음 | 위 한정범위 및 아래 해시 버전에 한함. |

### SQL에서 확인한 분석 단위·선택·분모

- Eligible은 PI, 유효 DOCDB family, earliest filing 2013~2017, earliest publication 2017-12-31 이하, 5개 IPC 네 자리 중 하나를 만족하는 application에서 **TRIM한 CN applicant address**를 찾은 class-family다. 국적·발명자 국적·중국 특허청 출원과 다르다. 가족의 어떤 구성원에 조건이 있으면 포함하므로 전체 가족이 중국 기업 소유라는 뜻도 아니다.
- Class마다 FAMILY의 FARM_FINGERPRINT 정렬 상위 200개를 선택한다. 동일 class-family를 DISTINCT로 먼저 압축한다. Hash 정렬은 고정된 편의표본 규칙이며 모집단 추론·독립 무작위추출 설계를 검증하지 않았다. Hash collision의 동률에 별도 family 정렬키가 없으므로 극히 드문 동률까지 완전히 결정적이라고 보장할 수 없다. Class별 표본분율도 다르다.
- 표본 가족의 **모든 application**으로 확장하여 2017년까지 공개된 publications의 patent citations를 찾는다. 이 확장에는 처음 eligible 조건을 만족한 중국주소 application 이외의 가족구성원도 포함된다. NPL 인용과 cited application-only reference는 포함되지 않으며 동일가족 인용을 제외한다.
- Source class-family/target-family별 한 쌍으로 축약하므로 원문헌·공개공보 중복은 쌍 내에서 제거된다. Class 간에는 동일 source family와 target edge가 재등장할 수 있고, 합계 1,000은 고유 가족 1,000개를 뜻하지 않는다. 9,525도 class-specific pair observations다.
- 국가 가중은 target 쌍의 **가장 이른 cited publication**(target_date, cited_pat_publn_id 순)의 알려진 applicant **person_id 수**를 분모로 하고 US person_id 수를 분자로 한다. 이는 나라별 동일 가중이나 인용기업·가족별 전체 applicant 주소를 통합한 가중이 아니다. applicant identity 정제 및 법인 중복은 person_id 수준에서만 통제된다.
- `any_app`은 class/source-family/target-family의 어느 citation-origin row라도 APP면 1이다. Window MAX를 QUALIFY 이전 계산하므로 가장 이른 publication만 APP여야 하는 조건은 아니다. APP subset의 국가는 여전히 가장 이른 cited publication에서 가져오므로 APP 인용이 실제 가리킨 publication의 국가와 다를 수 있다.
- `all_us_pct`는 모든 pair가 아닌 **국가가 알려진 pair**에 대한 US fractional share다. `app_us_pct`는 APP-origin인 동시에 국가가 알려진 pair만 분모다. 국가가 하나라도 알려졌으면 부분 주소누락은 그 pair의 분모에 반영되지 않는다. Missing pair 비율은 38.9~47.3%로 커서 complete-case selection을 무시할 수 없다. 인용 없는 표본 가족 3~10개도 edge-based share에는 기여하지 않는다. 이것을 국가적 기술의존도·전체 인용 중 미국 비율로 표기하면 과장이다.
- Coverage의 `cn_office_cn_address_families`는 같은 application에서 CN office와 CN address가 함께 있는지의 family-level MAX다. 다른 가족구성원에서 각각 조건을 만족하는 family-set 교집합과 다르다. 0/1이라는 수치로 두 family집합의 교집합이 거의 없다고 결론내릴 수 없다. 그럼에도 표본의 CN주소 eligible 370~18,974와 CN-office 7,973~234,987의 큰 차이 및 주소 누락은 selection 경고 신호다.
- Extractor는 저장 출력만 읽고 SQL 재실행은 하지 않는다. Marker가 여러 번 있으면 마지막 발견값이 덮어쓰며 현재 script 자체는 execution_count, 유일 class 5개, release label, SQL-source/output 일치까지 강제하지 않는다. 이번 audit에서는 현 notebook의 실행기록·class uniqueness·코드/출력 일치를 별도로 확인했다. SQL 서버 syntax와 실제 row-level join 결과는 독립 서버 재실행이 없어 미검증이다.

### 독립 계산 표

US 열은 known-country pair 분모이며 APP 열은 applicant-known pair 분모다.

| IPC | 전체 US (%) | APP US (%) | 국가 미상 pair (%) | 인용 없는 sample family |
|---|---:|---:|---:|---:|
| C12N | 42.101446 | 47.237443 | 45.543585 | 10 |
| G01S | 44.343814 | 43.932292 | 46.305645 | 10 |
| G06F | 48.380731 | 39.031298 | 47.331461 | 3 |
| G06N | 58.228730 | 54.791667 | 45.340314 | 9 |
| H01L | 21.325210 | 15.658174 | 38.876700 | 8 |

Coverage 진단은 입력 범위의 주소 누락을 보여주며 CN office 표본으로 일반화할 근거가 되지 않는다.

| IPC | eligible 중 sample (%) | 전체 중 CN주소 (%) | 전체 중 known주소 없는 가족 (%) | 같은 application CN office+주소 가족 |
|---|---:|---:|---:|---:|
| C12N | 12.747 | 1.821 | 61.530 | 0 |
| G01S | 29.762 | 1.584 | 51.070 | 0 |
| G06F | 1.054 | 4.135 | 52.534 | 1 |
| G06N | 54.054 | 2.145 | 45.154 | 0 |
| H01L | 3.343 | 3.601 | 44.994 | 0 |

### 실행·해시 기록

- Python 3.12.14. 독립 Decimal 정밀도 45자리. 비율 비교 rel 1e-12, abs 1e-10.
- Notebook SHA-256 `48e897195bd333ede8ea3d8a5a5283e7b7adb4b0415d809082ac041ddf16348c`: final JSON의 notebook_sha256와 일치 PASS.
- 실행 cell(index, execution_count, output 수): `[(4, 2, 1), (5, 3, 1), (6, 4, 1), (7, 5, 1)]`.
- CSV 105개 필드 일치; raw→rows 두 source join 일치; 20개 비율·4개 합계·2개 ranks·수치범위 및 eligible=cn_address consistency PASS.
- 합계: class-family 1,000; family-pair 9,525; known-country pair 5,288; APP pair 943. Class overlap에 유의.
- Python syntax compile 두 스크립트 PASS. Extractor를 workspace 임시 복사본에서 실행: exit 0, stderr ''. 최종 JSON·CSV·executed_cells의 byte-for-byte 재현 `{'data/patstat_pilot_final.json': True, 'data/patstat_pilot_final.csv': True, 'scripts/patstat_executed_cells.py': True}`. 임시 폴더 정리 후 원본 네 파일 해시 불변 PASS.

- `data/patstat_pilot_final.json`: `a7bdad74f705feb9fb2ffb809e6903b124f4f4a0dd82aac171dc6995eac3532c`
- `data/patstat_pilot_final.csv`: `22fb063cb77e906b274e22fbc15221782a68ca8ad351a4ce12c60bced49a45fa`
- `scripts/patstat_executed_cells.py`: `cdb137663e1a4a97fd8d198d70a5dfb2eec4ead0629b2d24cd4b8cdafe352fd3`
- `scripts/extract_patstat_pilot.py`: `85761fd636e47046c5f32047f7c5b9a18982773f664b24183b5dd571458ce302`
