# 다음 회차 재개: 실제 자료 검증을 우선

최신 사용자 지시(2026-11-12): 가설 미검증 상태를 해소하도록 최근 방법론을 검토하고 실제 계량 검증을 진행한다. 이어서 계속 진행하라고 재지시했다. 기존 질문·Gate 유지, 유리한 결과를 찾는 사양선택 금지, 유료 API·구매 없음.

## 보존된 실측 결과

- EPO TIP 실제 panel: WO 포함 family, 신청인 국가주소, 5 IPC×5국×84개월, 2,100셀. raw JSON 및 SQL 보존, 전송해시 일치.
- ALL/APP 4국평균 대비 후보창 기울기 -0.080665/-0.049947. 이는 실제 제한 전 R&D/자본 효과가 아니라 최초출원 코호트별 국제특허 활동의 기술적 상대 기울기다.
- 독립 검산 465항목 일치. 원 쿼리를 DB에서 독립 재실행한 것은 아님. 원 가설은 계속 미식별.
- 독립 referee 초심은 revise-before-use/diagnostic-only. 3개 표현 수정은 반영했으나 마지막 재확인 도중 구독 사용 한도 오류로 종료했다(도구가 안내한 재개 시각 2026-11-13 02:17, 시간대는 오류문에 명시 안 됨). 판정을 accept로 올리지 않는다. 사용 범위 경고는 PDF/본문에 유지한다.

## 다음 작업

1. `overview.md`, `verification.md`, `referee.md`, `referee_response.md`를 읽고 **최신 overview에 대한 fresh 독립 referee 재확인**을 수행한다. 정식 주설계/원 가설 accept가 아니라 추가 진단의 표현·범위만 심사한다. 기존 원장 단위의 수정 회차를 초기화하지 않는다.
2. WO 국제출원 안에서 사전 B와 outcome 모집단을 맞춘다. 세부 기술은 기존 5 IPC 안의 IPC main group. 결과 확인 전 포함규칙과 결측·최소분모를 기록하고 사전 2013–2017 집계부터 확인한다. 현재 5 broad IPC의 post 결과를 이미 봤으므로 새로운 분석도 탐색이다. 확인표본이라고 부르지 않는다.
3. 연도별(2013–2019) 주소 커버리지, 표본수·기술 중복, 국가귀속·현재판 선택과 최초출원/PCT 시계 차이를 점검한다. CN관청을 중국국적·주소로 치환하지 않는다.
4. pre-only IPC 세부그룹 지원이 충분하면 그룹당 100개 family hash표집에서 국가 미상 person까지 포함한 인용 비중 경계와 ALL/APP를 계산한다. 현재 known-country 분모 비중은 엄격한 사전 잠재손실량으로 검증되지 않았다.
5. 비지목 placebo/실제 제한/중국정책 crosswalk·공통창 없이 국제특허 상대기울기를 순수 announcement effect로 승격하지 않는다. NSFC 신청과 승인, 기업 CAR와 연구배분을 구별한다.

## 후속 실측 갱신: 세부기술 dose까지 실행

위 2–4의 생산 작업 일부는 이어서 실행했다. strict5yr 지원은 0개였고 2017 cohort의 main-group-family 합1을 확인했다. 충분히 관측된 과거 지원을 따로 검사하는 잠정 규칙으로 24개 main group을 구성했고, 그룹당100 WO family에서 ALL/APP 인용을 실제 집계했다. `finegroup_progress.md`, `finegroup_pre_dose_raw.json`, `finegroup_measurement_diagnostics.json`을 먼저 읽어 같은 조회를 반복하지 않는다.

ALL10747쌍/국가알려진4659쌍, 국가미상person에 따른 개별구간 폭 중앙값60.9%p. APP765쌍/known726쌍이지만18/24기술쌍수<20,22/24sourcefamily<10. APP 경계는21그룹,known-only점은17그룹에만정의된다. ALL 개별구간의 공통부분은 공동assignment가능성·진짜B동일의 증거가 아니다. 세부기술 post outcome은 아직 조회하지 않았다.

또한 G06N20/와 G06F40/가 선정목록에 들어가며 WIPO 버전표지가 각각[2019.01]/[2020.01]이다. 당시정보의 crosswalk는 2017판과 revision concordance로 별도 감사해야 한다. 단순히 새로운코드를삭제해미래정보문제가해결됐다고하지않는다.

실행 후 다음 우선순위는 (a) 새 fine-dose 검산의 실제 파일/판정 확인, (b) 미상 target applicant 국가를 같은family의 사전공개다른공보로보완할 수 있는지 구성개념을명시한측정파일럿, (c) 사전 IPC taxonomy정합성, (d) 직접 행동결정 outcome접근이다. 인용point를확정하지않고24그룹post회귀부터실행하지않는다.

새 fine-dose 독립 검산도 완료되어 `finegroup_verification.md/json`이 존재한다. APP은 경계21/24와 known-only점17/24를 구분한다. WIPO 공식 스킴 PDF에서 두 IPC 버전표지와 PCT Article21을 독립 확인했다. (a)는 이 파일들의 범위를 읽는 단계이며 재실행을 무작정 반복할 필요는 없다. 기존 broad파일럿의 referee 재확인은 여전히 별도 대기다.

실행 가능한 독립 작업은 계속하고, 한도 재개가 실제 되지 않으면 성공했다고 보고하지 않는다. 복구 후 한국어로 실제 산출물·미해결·다음 행동을 보고한다.
