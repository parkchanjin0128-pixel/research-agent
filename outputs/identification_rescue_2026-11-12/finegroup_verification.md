# 새 fine-group dose 독립 집계 검산

2026-11-12. **집계 산술과 정적 측정범위 검토는 통과했다. 독립 PATSTAT DB 재실행은 하지 않았다.** 이 단위는 새 원시 집계 검산이며 기존 referee 수정판 재검증과 별개다. 원시 pair/person 자료·정확한 서버 실행 SQL을 재조회하거나 표본 family overlap을 감사한 결과가 아니다.

입력 raw는 52,728 bytes, SHA256 `6f4c983b54e3f092798f6c6024dbb94c2d5f39fc6b53978d24a4546bedfceabf`로 전달받은 값과 일치했다. producer 실행시각은 `2026-11-12T13:49:22.524011+00:00`이며 저장된 script hash는 실행 출처 메타일 뿐 독립 재실행 증거로 취급하지 않았다. 읽은 6개 입력의 hash와 48행별 검산은 동명 JSON에 보존했다. 작성 파일은 이 보고서와 동명 JSON뿐이다.

## 재현한 산술

| 항목 | ALL | APP |
|---|---:|---:|
| main-group 행 | 24 | 24 |
| 표본 group-family memberships | 2,400 | 같은 2,400 |
| raw patent-document references | 11,644 | 869 |
| valid patent-document references | 10,877 | 866 |
| cited-family pairs | 10,747 | 765 |
| country가 하나 이상 알려진 pairs | 4,659 | 726 |
| 위 known-pair 비율 | 43.3516% | 94.9020% |
| 유효 pair를 낸 source-family memberships | 2,382 | 72 |
| 신청인 목록 부재 pairs | 265 | 9 |
| 기재 person 중 미상국가를 포함한 pairs | 5,870 | 38 |
| pairs <20인 그룹 | 0/24 | 18/24 |
| source families <10인 그룹 | 0/24 | 22/24 |
| lower/upper가 정의된 그룹 | 24/24 | 21/24 |
| known-only 점이 정의된 그룹 | 24/24 | 17/24 |

각 그룹은 100 family를 표집했다. 동일 family가 복수 그룹에 포함될 수 있으므로 2,400은 고유 family 수가 아니다. origin 두 행은 동일 표본을 반복 보고하므로 4,800개의 독립 family로 합산하면 안 된다. pair·person 총합 역시 그룹 중첩을 제거한 전체 고유 수가 아니다. 알려진 국가 pair와 미상국가를 포함한 pair는 부분적으로 겹칠 수 있어 위 두 계수를 배타적 분류로 합산하지 않는다.

48행 모두 lower/upper sum을 전체 유효 pair 수로 나눈 평균과 저장된 B가 허용오차 1e-12 이내로 같았다. US≤known≤listed persons, cited-family pairs≤valid documents≤raw documents, source-family 수≤sample 수 및 pair 수, null 처리와 origin별 count nesting도 통과했다. **pair 원자료가 없어 U/N 및 (U+N−K)/N을 pair별로 재계산하거나 known-only 평균 U/K를 person 총합으로 검증하지는 못했다.** person 합계의 비율은 pair별 비율의 평균과 다르다.

APP에 pair가 없는 `G06F21/`, `H01L23/`, `H01L27/`는 lower/upper와 known-only 모두 NULL이다. 이를 B=0으로 바꾸면 안 된다. 추가로 `G06F19/`, `H01L21/`, `H01L29/`, `H01L33/`는 pair는 있으나 known-country pair가 0이어서 bounds는 [0,1], known-only는 NULL이다. 따라서 APP의 bounds 21개와 known-only 점 17개를 구별해야 한다. 알려진 국가 비율이 높아도 18개 그룹의 pair<20, 22개 그룹의 source-family<10이라는 희소성은 해결되지 않는다.

## 경계와 순위 해석

ALL 그룹별 upper−lower의 중앙값은 **0.6087820261554358**이다. ALL 24개 marginal interval의 공통 교집합은 **[0.37701504844361994, 0.6310570644940348]**이다. 하한 최대는 G06F15/, 상한 최소는 C12N9/이다.

이는 각 그룹의 개별 구간이 공통 영역을 갖는다는 산술 사실이다. 동일 unknown person 또는 대표공보가 여러 pair·그룹에 공유될 수 있다. 따라서 모든 그룹 값을 동시에 같게 만드는 하나의 공동 국가배정이 존재한다고 증명한 결과가 아니다. joint feasibility를 계산하지 않았다. 이 marginal interval만의 비교에서 엄격히 분리되는 ALL 그룹쌍은 0개이므로 여기서 dose 순위를 확정할 수 없다. 공동 제약이 추가되면 얻을 수 있는 순위 정보까지 없다고 증명한 것은 아니다. known-only 점의 순위를 전체 dose의 확정 순위로 승격하면 안 된다.

## SQL 분모와 범위

정적 SQL은 동일 CN 주소·main-group을 가진 eligible WO application의 pre-publication에서 출발한다. target은 다른 양의 DOCDB family의 pre-cutoff 공보이며 origin×source family×target family당 대표 target 공보 하나를 고른다. APP는 APP 링크 안에서 별도로 대표 공보를 정하므로 ALL이 택한 비APP 문헌의 주소를 APP에 붙이는 문제를 피한다. B는 **전체 유효 citation-family pair를 같은 가중으로 평균**한 값이다. source-family 같은 가중 평균, person-pooled 비율, 전체 family의 미국 기술의존도와 동일하지 않다.

신청인 수 N은 양의 person ID를 중복 제거하고 비양수·누락 ID는 신청인 sequence slot으로 세는 기록상 목록 크기다. K는 두 대문자 국가코드에서 XX/ZZ/WO/EP/AP/EA/OA/GC/IB를 제외한 기록상 known 수, U는 US 수다. 모든 두 글자 국가코드를 실제 ISO 유효 코드로 검증한 것은 아니다. N>0일 때 [U/N,(U+N−K)/N], N=0일 때 [0,1]이라는 규칙은 문서와 코드가 일치한다. known-only는 K>0 pair만의 U/K 평균이다.

이 bounds는 관측된 신청인 목록과 known-country가 맞다는 조건 아래 미상국가의 배정만 바꾼 측정 경계다. **누락된 신청인 자체, 잘못된 person/country 매칭, 오기, family·IPC 오류, 사후 갱신된 주소·origin, 표본오차, 인과효과를 포괄하지 않는다.** 목록 전체 부재에 [0,1]을 주어도 부분적으로 누락된 신청인 수까지 복구되는 것은 아니다.

## 선택 지원과 역사적 시간

raw·저장된 선택목록·24개 지원행·dose 그룹 집합은 일치한다. 각 지원행의 25개 국가×연도 셀, CN 총합·양수 관측연도수·관측연도의 최소값을 재계산했다. 24개 모두 CN pre2013–17 총합≥100 및 2013/14/15 각각≥5를 만족하고, 네 donor가 2013–15 매년≥5인 그룹은 20개다. dose의 eligible 수는 각 CN pre 총합과 일치한다. 이 검산은 모든 eligible 그룹을 빠짐없이 선택했는지의 독립 DB 확인은 아니다.

별도 전체 pre 진단의 2017 earliest-filing memberships 합계는 1, 관측 main group도 1이다. 선택된 24개 지원표에서도 2017 CN 합계는 1이다. 이 진단을 전제로 2017에 ≥5가 필요한 최초 strict 5년 규칙은 어떤 그룹도 만족할 수 없다. 빈 strict 결과를 혁신 부재로 읽으면 안 된다. mature 규칙의 24개는 후속 탐색 모집단이며 최초 strict 규칙 통과로 바꿀 수 없다. selected subset의 연도합(4,674/4,784/6,724/3,430/1)은 전체 진단의 연도합과 혼동하지 않는다.

[WIPO PCT Article21](https://www.wipo.int/en/web/pct-system/texts/articles/a21) 본문 21(2)(a)는 예외를 전제로 우선일 후 통상 18개월 공개를 규정하고 21(2)(b)는 조기공개 신청을 둔다. 이는 2017 earliest filing과 2017 own-publication cutoff의 강한 절단과 정합적이다. 모든 누락 family의 개별 원인을 입증하지는 않는다.

[WIPO 공식 IPC 2024.01 G06 PDF](https://www.wipo.int/ipc/itos4ipc/ITSupport_and_download_area/20240101/pdf/scheme/full_ipc/en/g06.pdf)의 **p14 G06F40/00 [2020.01] 및 p22 G06N20/00 [2019.01]를 직접 본문으로 확인**했다. 원 경고문에 링크된 WIPO HTML은 검색색인에서는 같은 표지가 확인됐지만 직접 open 파서가 빈 표만 반환해 공식 PDF로 교차 확인했다. 출원·공개일 필터만으로 현재 세부 IPC가 2017년 당시 존재한 동일 분류였다고 볼 수 없다. 현재판을 이용한 회고적 기술분류라는 경고는 타당하다. 과거판·revision concordance와 재분류 이력의 별도 감사를 수행하지 않았다.

**판정:** 전달된 새 raw의 주장된 주요 산술은 재현됐다. 사전등록, 정책 지목 crosswalk, 공동 국가배정 가능성, 순위 식별, 인과식별, 독립 DB 재현이 통과했다는 판정은 아니다.
