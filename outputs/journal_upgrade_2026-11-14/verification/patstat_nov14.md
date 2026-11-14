# Nov14 PATSTAT 독립 검증

판정: 수송 무결성·기록된 집계의 산술은 재현된다. 현재 자료로 비교기술의 충분한 지원, B 공통지지, 2017 당시 기업/국가 명의 또는 인과효과는 확인되지 않는다. 독립 SQL의 원DB 반환을 기다리는 중이며, 생산자 SQL 실행을 그대로 독립 원DB검증이라고 부르지 않는다.

## 수행 범위와 무결성

생산 코드는 실행·import하지 않고 CSV와 raw JSON을 직접 읽었다. UI는 생산자 전용으로 유지했다. 독립 쿼리는 법인/IPC CSV에서 다시 만들고 인용의 문헌 경로와 출원 경로를 나눈 뒤 window 순위로 family pair를 선택한다. 실제 실행은 로그인된 TIP을 제어하는 생산자에게 요청했다.

| 입력 | bytes | SHA256 | b64 압축 해제 |
|---|---:|---|---|
| patstat\pre_matrix_raw.json | 17096 | `906bfa2016ff84ce4162fcd8b4f8fc00e9a0aa6b42ffeb0b0ce6cd22e457a8a0` | 완전 동일 |
| patstat\firm_dose_raw.json | 9415 | `994f5ab0432637c9b29a7aca7068b60648685afb8e6d10a0f024111994051392` | 완전 동일 |

템플릿의 일곱 테이블 placeholder를 실제 dataset으로 치환한 support/dose/overlap SQL 해시와 raw 기록 일치: True. 일관성 점검: `{"support_keys_unique": true, "support_first_between_0_and_total": true, "tech_pair_counts_consistent": true, "firm_pair_counts_consistent": true, "APP_not_larger_than_ALL": true}`.

## 사전 지원과 B 공통지지

사전 2010–2015 × CN/DE/JP/KR/US 30칸을 구성하고 raw에 없는 칸을 0으로 보충했다. source 미상이나 pair0를 B=0으로 바꾸지는 않았다.

| 단위 | 분류 | 최소 family | 0인 칸 | 5 미만 칸 | 모든 칸 ≥5 |
|---|---|---:|---:|---:|---|
| N01 | nonlisted | 1 | 0 | 11 | 미달 |
| N02 | nonlisted | 0 | 11 | 25 | 미달 |
| N03 | nonlisted | 1 | 0 | 14 | 미달 |
| N04 | nonlisted | 0 | 4 | 21 | 미달 |
| N05 | nonlisted | 0 | 18 | 27 | 미달 |
| N06 | nonlisted | 0 | 2 | 16 | 미달 |
| N07 | nonlisted | 0 | 24 | 30 | 미달 |
| N08 | nonlisted | 0 | 28 | 30 | 미달 |
| N09 | nonlisted | 0 | 18 | 30 | 미달 |
| N10 | nonlisted | 0 | 2 | 15 | 미달 |
| N11 | nonlisted | 0 | 7 | 22 | 미달 |
| N12 | nonlisted | 0 | 4 | 17 | 미달 |
| P03 | positive | 0 | 3 | 15 | 미달 |
| P04 | positive | 26 | 0 | 0 | 통과 |
| P05 | positive | 0 | 2 | 11 | 미달 |
| P06 | positive | 4 | 0 | 1 | 미달 |
| P_ADDITIVE_UNION | positive | 0 | 16 | 20 | 미달 |
| P_NEURAL_GENETIC_UNION | positive | 0 | 2 | 14 | 미달 |

통과는 ['P04']뿐이다. known_pairs≥20인 ALL에서 지목 B 범위 0.302824004–0.538461538, 비지목 0.017857143–0.134146341로 점추정 구간이 겹치지 않는다. 이 20쌍 기준은 추가 정밀도 진단이며 확증 cutoff가 아니다. 미상 나라에 관한 조건부 구간은 넓게 겹칠 수 있으므로 진실한 B도 겹치지 않는다는 결론은 아니다.

기술 dose raw에 N05/N07/N08 행이 없다. source_families가 없는 단위를 최종ns에서 만들지 않기 때문이다. B=0으로 복구하면 안 된다. 월별 패널을 만들 때도 0과 주소·분류 미상은 구별해야 한다.

## 기업 B의 독립 산술

각 수치는 네 ADR의 확인된 법인부분집합에 관한 것이다. 기업집단 전체의 기술손실이나 미국기술 사용의 진실값이 아니다. B_known=known_us_mass/known_pairs, 조건부 [lo,hi]=[mass/pairs,(mass+pairs-known_pairs)/pairs]. known_pairs=0이면 B_known은 미상, pairs=0이면 구간도 미상이다.

| 명의 범위 | origin | source family | pair | 나라 확인 pair | B_known | 조건부 [lo,hi] |
|---|---|---:|---:|---:|---:|---|
| BABA_group | ALL | 8187 | 56449 | 24324 | 0.523218 | [0.225456,0.794553] |
| BABA_group | APP | 8187 | 3924 | 2962 | 0.693507 | [0.523488,0.768646] |
| BABA_issuer | ALL | 8183 | 56347 | 24239 | 0.523506 | [0.225198,0.795025] |
| BABA_issuer | APP | 8183 | 3924 | 2962 | 0.693507 | [0.523488,0.768646] |
| BIDU_group | ALL | 3189 | 19283 | 5954 | 0.416350 | [0.128556,0.819787] |
| BIDU_group | APP | 3189 | 165 | 89 | 0.453184 | [0.244444,0.705051] |
| JD_group | ALL | 1795 | 9106 | 2464 | 0.391234 | [0.105864,0.835273] |
| JD_group | APP | 1795 | 9 | 4 | 0.750000 | [0.333333,0.888889] |
| NTES_group | ALL | 727 | 3866 | 1017 | 0.359390 | [0.094542,0.831480] |
| NTES_group | APP | 727 | 0 | 0 | 미상 | 미상 |
| NTES_issuer | ALL | 2 | 40 | 30 | 0.516667 | [0.387500,0.637500] |
| NTES_issuer | APP | 2 | 0 | 0 | 미상 | 미상 |

BIDU/JD issuer 행은 원raw에서 아예 없으므로 issuer에 source가 없었다는 해석은 독립SQL에서 확인할 예정이다. NTES APP의 0 pair는 미국 의존도 0이 아니라 측정 불가다.

## 코드·원문 감사에서 남은 핵심 제약

1. **원 source의 시점 불일치:** TLS207는 최신 Latin-name 공보의 인명을 application에 연결한다. source공개일≤2017만으로 주소·법인명이 2017 공보 당시 것임을 보장하지 못한다. TLS227 공보별 명의로 새 감도를 준비했다. [EPO catalog](https://link.epo.org/web/observatory-tools/patstat/en-data-catalog-patsat-global-autumn-2026.pdf), p57.

2. **재분류:** TLS209는 모든 공보의 IPC를 병합하고 최신 버전을 쓴다. 2017 alias crosswalk는 2017 당시의 실제 분류 부착정보까지 복원하지 않는다. 같은 원문 p58.

3. **country bounds의 범위:** 일부 출원인의 나라가 비어도 다른 출원인의 나라 하나라도 있으면 known pair다. 따라서 위 구간은 모든 결측국가의 무조건 상하한이 아니다. distinct 나라를 동등 가중하므로 사람 수 가중도, 소유권·국적 가중도 아니다. target 해석은 TLS227 공보 명의에 한한다. 같은 원문 p78 및 dose.sql target_country.

4. **인용 선택·배제:** source-target DOCDB family별 중복 제거와 자기 family 배제는 코드에 명시된다. target은 유효 공개일≤2017 중 가장 이른 문헌·최소id다. APP은 어느 qualifying 문헌에서라도 APP이면 포함되지만 target문헌은 ALL과 공통 선택한다. cited_publn_id가 양수면 그 문헌만 허용한다. 문헌 id가 없을 때만 cited_appln으로 후보를 확장한다. targetfamily 미상·target 미연결·기한 밖·NPL은 남은 pair 분모와 위 bounds에서 제외된다. 배제된 인용의 양은 현재 집계가 제공하지 않는다.

5. **정보 가용 시점:** APP은 출원인이 도입한 인용이고 ALL은 심사·검색 등의 origin도 섞는다. source공보의 공개일만으로 인용이 실제 2017까지 공개·적재됐다고 확정할 수 없다. 공식 [EPO 인용 workflow 변경](https://www.epo.org/en/searching-for-patents/helpful-resources/patent-knowledge-news/improved-availability-citations)도 공보와 인용 가용 시점의 차이를 보여준다.

6. **법인 지도는 부분집합:** Baidu Note1에는 미포함 BaiduPay가 있고, JD Note1·NetEase Note1·Alibaba Exhibit8.1에도 지도 밖의 법인이 있다. 본 검증에서 확인한 매핑 명칭/관계는 대체로 제시 원문과 맞는다. BABA Cloud VIE와 Zhejiang Cloud WFOE는 다른 이름이다. VIE 계약연결을 issuer 지분소유로 바꾸면 안 된다. 2017년말(Alibaba는3월말)의 법인관계는 2013–17년 내내 해당 관계였다는 증거가 아니다.

7. **분모의 차이:** 기술 B는 CN 주소 WO, 기업 B는 해당 이름의 모든 관청 출원이다. 두 수치를 하나의 동일 B로 취급하거나 4기업 회귀를 확증으로 해석할 수 없다.

8. **패널·공통지지·인과성:** 공통지지 실패와 기술별 빈약한 지원은 실제 자료의 제약이다. 다른 cutoff나 추정법 명칭으로 해결됐다고 판정하지 않는다. 기술 간 양 팔 중첩은 raw overlap에 실제 존재하며 full JSON에 보존했다.

## 원문과 독립 실행 증거

공식 catalog 원본: `verification/patstat_sources/epo_patstat_global_2026b_catalog.pdf`, SHA256 `88b27d3026dbe10bad4f9f3bb34196de59b1ce5c9e60d206e8bff45e280712f0`. 발췌 완전 페이지 텍스트: `verification/patstat_sources/catalog_relevant_pages.txt`. 공식문서2026b를 읽었다는 것과 쿼리dataset의release확정은 다르다. actual schema/provenance 반환은 아직 로컬에 없다.

독립 쿼리 원본: `verification/build_independent_patstat_sql.py`; `verification/independent_queries.json` SHA256 `23555b95229607da1c529291cadf62dd58e404e3748528946e90b7ff793b5895`; 원판과 별도인 역사공보source 감도는 `verification/independent_historical_queries.json` SHA256 `4293261a8ba0988f1457a258c270ef1cffc93c45aad16e58904126069aaab79a`. 두 번들의 b64를 로그인 TIP으로 전송해 실행할 수 있다.

- [Baidu 2017 Form20F](https://www.sec.gov/Archives/edgar/data/1329099/000119312518084050/d480652d20f.htm): Note1 F9, browser lines4806-4814; BaiduPay demonstrates incomplete subset
- [Alibaba 2017 Exhibit8.1](https://www.sec.gov/Archives/edgar/data/1577552/000104746917004019/a2231121zex-8_1.htm): significant subsidiaries AND consolidated entities, as of March31 2017; list longer than mapped subset
- [Alibaba 2017 Form20F](https://www.sec.gov/Archives/edgar/data/1577552/000104746917004019/a2231121z20-f.htm): Item4C, browser lines3333,3353: Cloud VIE distinct from Zhejiang Cloud WFOE
- [JD 2017 Form20F](https://www.sec.gov/Archives/edgar/data/1549802/000110465918027777/a18-5116_120f.htm): Note1 F12, browser lines6126-6142;100% subsidiaries; list contains omitted firms
- [NetEase 2017 Form20F](https://www.sec.gov/Archives/edgar/data/1110646/000110465918025392/a18-5396_120f.htm): Note1 F7, browser lines5230-5248; omitted Youdao Information; VIE language ppF9-10

현재 판정은 집계·산술 검증 완료, 독립 원DB 반환 대조 대기다. post패널/IP5 대안 및 TLS227 historical-source 생산결과는 도착 후 추가 기록한다.

<!-- NEW_RETURNS -->

## 추가 회수자료 검증

새 파일 `patstat\historical_source_and_ip5_raw.json`: 3320 bytes, SHA256 `e7c1aa0d8a34c949fb28cf822f556c051b12006d43abf54c44a0100e6644b02c`, b64 해제 byte 동일=True.

생산자의 TLS227 source 감도는 기술 30행이 원판과 수치상 완전히 같다. 기업은 BABA group/issuer, BIDU group, JD group에서 달라진다. 이는 역사 명의 선택의 중요성을 실제로 보이며 원판도 역사 명의였다는 증거가 아니다. 실제 SQL 해시와 로컬 원문 대응은 JSON에 별도 기록했다. Windows파일의 CRLF byte해시와 LF로 정규화한 실행SQL문자열의 UTF8해시는 별개로 기록했다.

EARLIEST_PUBLN_DATE는 application의 최초공개일이다(catalogp159). 원dose의source는 그날짜2013–17인 출원을 가진 family합집합이며 family첫공개cohort라고 부르면 안 된다. 반면 새IP5SQL은 family전체 MIN을 실제 구했다. 사전support·postpanel의국가연결은여전히TLS207latest이므로 과거공보당시국가로도지원결과가같다는검증은별도다.

| IP5 유사부분집합 단위 | family | 나라 확인 | B_known | 조건부 [lo,hi] |
|---|---:|---:|---:|---|
| N01 | 754 | 617 | 0.093733 | [0.076702,0.258400] |
| N02 | 190 | 170 | 0.117647 | [0.105263,0.210526] |
| N03 | 459 | 404 | 0.128713 | [0.113290,0.233115] |
| N04 | 207 | 165 | 0.175758 | [0.140097,0.342995] |
| N05 | 139 | 114 | 0.166667 | [0.136691,0.316547] |
| N06 | 492 | 417 | 0.231415 | [0.196138,0.348577] |
| N07 | 44 | 36 | 0.152778 | [0.125000,0.306818] |
| N08 | 22 | 18 | 0.055556 | [0.045455,0.227273] |
| N09 | 47 | 34 | 0.294118 | [0.212766,0.489362] |
| N10 | 315 | 268 | 0.223259 | [0.189947,0.339153] |
| N11 | 247 | 202 | 0.121287 | [0.099190,0.281377] |
| N12 | 549 | 442 | 0.143665 | [0.115665,0.310565] |
| P03 | 1687 | 1480 | 0.423164 | [0.371241,0.493944] |
| P04 | 15687 | 13665 | 0.205263 | [0.178805,0.307702] |
| P05 | 617 | 535 | 0.278816 | [0.241761,0.374662] |
| P06 | 2878 | 2450 | 0.332143 | [0.282748,0.431463] |
| P_ADDITIVE_UNION | 3183 | 2814 | 0.410211 | [0.362656,0.478584] |
| P_NEURAL_GENETIC_UNION | 1030 | 894 | 0.495433 | [0.430016,0.562055] |

대안의 점 B 범위는 지목 [0.205262837,0.495432513], 비지목 [0.055555556,0.294117647], 교집합 [0.205262837,0.294117647]. 이는 IP5 유사 포트폴리오의 일부 공통 범위이며 원 인용 B의 공통지지 실패를 자동 해결하지 않는다. 지원조건 P04만 통과라는 자료제약도 바뀌지 않는다.

[OECD 2019 Innovative outputs](https://www.oecd.org/en/publications/measuring-the-digital-transformation_9789264311992-en/full-report/component-42.html)의 정의는 2관청 이상 출원 + 최소1관청이IP5다. 같은 페이지 figure 주석은 applicant residence의 fractional count다. 따라서 지정 출처를 inventor 기준이라고 서술하면 부정확하다. [OECD 2024 Annex C](https://www.oecd.org/en/publications/promoting-the-growth-of-the-semiconductor-ecosystem-in-the-philippines_01497fea-en/full-report/notes-on-patent-data_f8ed0fa4.html)도 같은2관청/IP5 정의를 확인한다. 본 집계는 WO를 제외한 national/regional관청·2017까지공개조건·DOCDBfamily·distinct applicantcountry가중 등에서 지정 OECD그림과 다르다.
