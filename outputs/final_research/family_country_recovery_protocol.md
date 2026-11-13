# 같은 family의 사전 주소 공보를 이용하는 별도 측정 파일럿

2026-11-12. 기존 월별 broad IPC 결과와 24세부그룹의 원문헌 dose를 이미 관측했다. 아래는 추가 탐색 측정이며 primary freeze나 확인표본을 뜻하지 않는다. 새로운 proxy 및 세부기술 outcome을 보기 전에 규칙을 적는다.

고정 source 표본은 앞선 24개 main group, 그룹당100개의 2013–2017 중국 주소 WO family다. 선택·hash·문헌시점·인용 pair를 그대로 유지한다. 각 target family에서 2017년 말까지 공개된 문헌 중 신청인 국가가 하나 이상 알려진 **가장 이른 문헌**을 고른다. 원래 피인용 공보의 신청인 국가를 그 나라로 대체했다고 하지 않고, target family의 사전 공개 applicant-country footprint라는 별도 구성개념으로 정의한다. ALL/APP source별 원래 대표 피인용 문헌도 보존한다.

각 source-target pair에 같은 새 family footprint를 붙이고, 관측 person목록의 known-country 미국분수와 unknown-person 조건부 하한·상한을 산출한다. 국가문헌이 없는 target family는 미상으로 남긴다. 결과는 원문헌 방식 대비 국가확인률·구간폭·분산·순위 안정성의 측정 진단이다. 주소가 다른 후속 법인, ownership 변경, 국제출원 선택, 판본·국가코드 오류, applicant 목록 자체 누락은 해소됐다고 주장하지 않는다.

쿼리는 기존 그룹을 최대20개씩 나눈다. EPO 무료 쿼터를 확인하고 비용이 생기는 외부 BigQuery 프로젝트를 연결하지 않는다. 새로운 post outcome 회귀는 이 단계에서 실행하지 않는다. 공개된 특허가 EAR상 통제될 접근과 동일하다는 가정도 별도 제도 검증 대상이다.
