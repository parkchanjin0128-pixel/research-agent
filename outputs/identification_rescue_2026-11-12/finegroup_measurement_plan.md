# WO 동일모집단 main-group 생산계획

2026-11-12. 기존 5 broad IPC의 월별 결과는 이미 관측된 뒤의 새 탐색 단계다. 이 규칙은 세부 main-group 월별 결과와 재측정 dose를 보기 전에 기록한다. 원 연구의 사전등록·식별 게이트 통과·독립 검증을 뜻하지 않는다. 이 문서와 `proposed_finegroup_queries.py`만 새로 작성하며 다른 원장·방법파일·실행파일은 변경하지 않는다.

1. 범위는 WO application, PI, 양의 DOCDB family, C12N/G01S/G06F/G06N/H01L의 IPC main group이다. 원문 기호에서 `^([A-H][0-9]{2}[A-Z][[:space:]]*[0-9]+/)`를 추출하고 `[[:space:]]+`를 제거한다. 이는 원래 `\s` 추출규칙과 같은 공백 정의를 POSIX 표기로 구현하여 UI 전송 시 이중 escape 위험을 줄인 것이다. 예: `G06F  17/30`→`G06F17/`. 이 범위는 검증된 ANPRM 지목/비지목 crosswalk가 아니다.
2. 먼저 **2013–2017 earliest filing 및 최초 publication<=2017-12-31**만 조회한다. 추가로 **그 WO application 자체의 TLS211 publication이 2017-12-31까지 존재**해야 한다. 국내 선행공보의 최초 공개일만으로 WO 국가주소·해당 공보가 당시 관측됐다고 하지 않는다. 같은 WO application에 IPC와 TLS207의 신청인 주소국가가 함께 존재해야 한다. 가족·main group·국가를 중복 제거하고 매칭된 WO applications 중 최소 earliest filing date로 연도를 정한다. 공동국가는 국가별 중복 허용한다. 이 기준도 현재판 IPC·주소가 실제 당시 판본과 같다는 보증은 아니다.
3. CN에서 pre family 총수>=100이고 2013·14·15·16·17 각각>=5인 모든 main group을 선택한다. 일부 연도 미관측을 MIN이 무시하지 않도록 관측연도수=5를 동시에 요구한다. 이 선택을 세부 결과 이전에 `SAVED_PROVISIONAL`로 저장·보존한다. 원 연구의 공식 주분석 동결(freeze) 상태를 변경하지 않는다.
4. **US/JP/KR/DE의 각 pre연도>=5는 선택규칙에 넣지 않는다.** 그룹×국가×연도 0을 포함한 지원 메타를 별도 출력한다. 모든 국가 교집합으로 표본을 고르면 중국의 기술범위가 국제적으로 성숙한 기술로 바뀌며 국가교체별 모집단도 달라질 수 있다. CN 기준 모집단을 유지하고 donor 희소성에 따른 분석가능 여부를 별도 보류한다. 지원된 하위표본 분석은 별도 estimand·pre-only mask를 명시한다.
5. 첫 실행은 pre-only metadata와 선택그룹뿐이다. 세부 outcome·회귀·dose 결과를 동시에 조회하지 않는다. 선택그룹수와 broadclass별 범위를 확인한 뒤 잠정 저장된 그룹목록을 dose query에 전달한다. 그룹당 최대100 family의 deterministic hash 표본으로 인용 탐색비용을 제한한다. 100 family는 precision을 보장하지 않는다. 조건을 만족하는 그룹이 0이면 그 실패를 저장하고 dose query를 실행하지 않는다. publication 지연으로 2017 지원이 부족한지와 regex 미매치는 별도 pre-only 진단으로 분리하며 임계값을 완화해 본 계획의 표본을 만들지 않는다. fully-mature pre2013–15 대안은 별도 후속 계획으로만 제안한다.

## 동일 WO 모집단 dose

잠정 저장된 CN pre 모집단의 main-group×family를 대상으로 `FARM_FINGERPRINT('wo-main-v1|'+family)` 순서, family ID tie-break로 **그룹당 최대100 family**를 뽑는다. 부모그룹당 표본이 아니라 각 main group별 표본이다. 한 family는 여러 main group에 중복될 수 있으며 hash seed를 공유하므로 표본 간 독립을 가정하지 않는다. 동일 family가 여러 그룹에서 쓰인다는 점을 향후 추론·overlap 감사에 남긴다.

표본 family의 인용출처도 **CN 주소와 그 main group이 함께 확인된, pre-period own-publication 조건을 만족하는 WO application**으로만 한정한다. 국내·미국·다른 국가 family 구성원의 공보 인용으로 확대하지 않는다. 해당 WO application의 TLS211 공보 중 2017-12-31까지의 공보에서 TLS212 patent-publication 참조를 조회한다. target 공보도 2017-12-31 이전에 존재해야 하며 양의 다른 DOCDB family여야 한다. self-family 인용과 비특허문헌 참조는 제외한다. raw document reference 수와 유효 target document 수를 모두 출력해 링크·시간·self-family 제외에 따른 탈락을 알 수 있게 한다. 세부 탈락 원인별 분해는 이 1차 제안에 포함하지 않는다.

ALL과 APP를 별도 origin으로 만든다. APP는 `citn_origin='APP'`인 링크만 사용한다. 각 origin×source family×target family에서 실제 링크된 target 공보 중 가장 이른 날짜, 공보 ID 순으로 대표 공보 하나를 택한다. **APP의 주소를 ALL에서 선택한 비APP 문헌에 붙이지 않는다.** 대표공보 신청인은 TLS227 `applt_seq_nr>0`과 TLS206으로 연결한다. 이 주소는 target family 전체 발명자의 국적이나 미국 기술 공급원의 위치와 같지 않다.

## pair별 누락국가·person 불확실성

각 source–target family pair의 대표 target 공보에 기재된 신청인 수를 N, 그중 국가를 기록상 분류할 수 있는 수를 K, US 수를 U로 둔다. 양의 person ID는 중복 제거하고, person ID가 없거나 비양수인 신청인 행은 applicant sequence별 미상 slot으로 센다. 공백·비정상코드 및 XX/ZZ/WO/EP/AP/EA/OA/GC/IB는 미상으로 처리한다. 그 외 두 영문 대문자 코드는 기록된 국가코드로 인정한다. 이는 모든 국가코드의 정확성 감사가 아니다.

- N>0이면 pair의 미국 신청인 분율은 **[U/N, (U+N−K)/N]**로 보고한다. 미상 신청인을 모두 non-US 또는 US로 둘 때의 경계다.
- 신청인 목록 자체가 없으면 pair 경계는 **[0,1]**이다. 빈 목록을 미국0으로 확정하지 않는다.
- 동일 pair 분모로 lower/upper를 평균해 `b_pair_us_lower/upper`를 만든다. pair에 같은 가중을 주므로 이는 citation-pair 가중 지식연결 척도다. 특허 family마다 같은 가중을 준 척도와 다르다.
- 기존식 known-only 점은 K>0인 pair만 대상으로 U/K를 평균한 `b_pair_us_known_only`로 함께 출력한다. 국가정보가 있는 pair만의 조건부 척도이며 전체 pair 경계의 중앙값이나 최종 B가 아니다.
- APP에 유효 pair가 0이면 B는 NULL이다. 인용 없음·APP 없음·국가 미상을 B=0으로 대체하지 않는다. 미상국가 pair 수, 신청인 목록 부재 수, listed/known/US person 수를 함께 보고한다.

이 경계는 **관측된 신청인 목록과 알려진 국가코드가 맞다는 조건하에, 미상국가만에 대한 측정 경계**다. 누락된 신청인 자체, 잘못된 person 매칭, 오기 국가, family 연결·IPC 오분류, 2017년 이후 소급 수정된 주소·인용 origin은 포괄하지 않는다. 따라서 이 경계를 전체 dose 불확실성의 보장범위나 효과의 인과경계라고 부르지 않는다. sample100의 표본오차도 포함하지 않는다.

## 시간·비용·추론의 제한

own WO 공보의 cutoff는 당시 공보 존재를 확인하지만 현재판 TLS207/TLS206 주소·TLS209 분류·TLS212 인용링크가 당시와 동일했음을 보증하지 않는다. 2017년 출원은 cutoff까지 공개된 사례만 포함되어 코호트 선택이 강하다. 향후 monthly outcome에서 2021년 publication cutoff를 쓰면 최근출원 지연은 완화하지만 pre-only selected cohort와 publication maturity가 다르다. 이를 동일한 완전 모집단이라고 표현하지 않는다. 그룹 범위는 이 단계의 잠정 선택으로 유지하되 시점별 eligible-publication 정의와 outcome의 대응을 별도로 기록해야 한다.

`run_finegroup_dose`는 명시적 호출에만 실행되며 한 query에 최대20그룹·최대2000 source family로 확장을 제한한다. batch별 query hash·그룹목록·집계를 출력한다. 이것은 BigQuery **scan bytes/slot-hours의 엄밀한 상한이 아니다**. 라이브러리에서 확인되지 않은 maximum-bytes 옵션은 넣지 않았다. pre-only query의 작업량과 서버 표시를 먼저 확인하고 batch를 한 번씩 실행·저장하며 비정상비용이면 중단한다. 전체 월별 outcome은 이 생산코드에서 조회하지 않는다.

세부 main group의 수가 늘어도 독립 정책충격이나 독립 기술군의 수가 자동으로 늘지 않는다. broad class5개 안의 그룹 중첩·공통수요·특허 공유를 남겨두므로 단순히 main-group cluster 수를 늘려 유의성을 얻었다고 해석하지 않는다. 이후 실제 finegroup panel은 별도 새 분석·검증자가 검사하며, 기존 `analyze_monthly.py`의 음의 점추정은 최종 결론으로 승격하지 않는다.

현재 파일은 제안 코드이며 EPO 서버에서 아직 실행·검증되지 않았다. 로컬 Python 문법과 문자열/규칙의 정적 검산만 수행하며 query 실행·비용·서버 SQL 구문 검증을 완료했다고 하지 않는다.

## 별도 성숙 코호트 지원 규칙의 생산 지원

상위 작업에서 strict5yr 선택이 비었고 pre-only CN 지원 메타가 2013년44그룹/4,790 memberships, 2014년44/4,949, 2015년48/7,001, 2016년45/3,605, 2017년1/1이었다는 진행 결과를 전달받았다. 이는 본 작성자가 독립 재실행한 결과가 아니다. 2017 own-publication cutoff와 공개시차가 강한 선택을 만든다는 진단에 따라 상위 작업이 `finegroup_mature_rule.md`에 별도 탐색규칙을 기록했다.

이에 기존 strict5yr SQL을 그대로 보존하면서 `run_mature_finegroup_pre()`를 추가했다. **CN의 총2013–17>=100은 유지하되 2013/14/15 각각>=5만 요구**하며 2016/17은 필터가 아니라 지원 메타로 남긴다. 이는 세부 결과에 앞선 후속 탐색이며 최초 계획이 통과했다고 바꾸는 행위가 아니다. 반환 객체에 rule ID·rows·selected_groups를 묶고 dose 함수의 `selection` 인수로 넘겨 strict 선택과 섞지 않는다. `run_mature_finegroup_pre()`도 기본 자동실행하지 않는다. 실행자는 먼저 그 출력과 그룹목록을 저장하고 나서 dose를 명시 호출한다. 독립 검증은 대기 상태다.
