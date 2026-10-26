# C027 — 2019년 4월 LSA 독립 검증
- 역할: 별도 independent verifier. 기준 H=6f6e4f1cebea65fc083bd66c2d5334db694aae59; 점유 P=2ffe1ea3e3b4830e4ef23b79a4489324599c5de7; run=work-20261026T001540Z-8452e4ab-324b-4767-b538-41c1b77f1361.
- 대상: outputs/round_03/part738_lsa_2019_april_source.md. 작성자 추론·대화를 별도로 전달받지 않았으며 지정 산출물·상태 파일과 원문을 독립 대조했다.
- 판정: verified 1 / contradicted 0 / unverifiable 0. 한정 색인 관측만 검증한다.

## 원문·정확한 위치
공식 https://www.govinfo.gov/content/pkg/LSA-2019-04/pdf/LSA-2019-04.pdf 를 직접 다운로드했다. SHA256 f45766e2e82d228baeeb0a3ab7803cac5765d9937c6523e3cf3aac56a70ff65b.
1. PDF1 표지: Title 1–16의 변경 포괄기간은 2019-01-02~2019-04-30.
2. 인쇄2/PDF2: 월간 CFR→FR amendatory action finding aid이며 title/chapter/part/section별 색인, 제안규칙은 해당 title 끝에 별도 열거. 83 FR=2018, 84 FR=2019; Titles1–16 연간호는12월호.
3. 인쇄20/PDF20 왼쪽 아래 Title15 제목부터 오른쪽 중간 Title16 제목 직전까지가 이 호 Title15 전체. 왼쪽 아래 ChapterVII(Parts700–799) 마지막 항목은744 authority citation revised—14610; 오른쪽 맨 위로 이어지는 항목은744 Supplement No.6 amended—14610. 오른쪽 중간 Proposed Rules에는774—8485,801—11256,930—8628. 이 연속 Title15 범위에서 Part738 또는 그 Supplement No.1 항목을 관측하지 못했다. 텍스트와20쪽 렌더링을 직접 시각 대조했다.

## 해석 범위와 미완료
이 관측은 연구창2018-11-19~2019-04-30 중2019 구간의 해당 LSA 색인에 한정된다. 2018-11-19~12-31은 이 호 포괄기간 밖이다. 색인 항목 미관측을 전체 EAR 무변경·실제 제한 부재·China 접근 가능·China cutoff 확정으로 확대하지 않는다. 744 원규칙84FR14610과774 제안84FR8485의 원문 내용·효력일은 이번 검증에서 열람하지 않았다. 기존 연결표 자체 검증·전체 이력 완결성·1C353 적용성·기술매핑·창 안 순증 제한·MDE·내부 referee·회차 전체는 미완료다. 세 바이오행·41행·T12·Gate·질문·freeze는 바꾸지 않았다.

## 접근 기록
PDF 스킬 적용. 공식 PDF curl·pdftotext(1–2쪽과20쪽)·pdftoppm20쪽·이미지 시각대조 성공, 원문 접근 실패 없음. GitHub 최초 인자 누락 호출들은 schema 확인 후 수정 성공. 신규 보고 경로404는 부재 확인이며 원문 접근 장애가 아니다. 필수자료 일괄출력 잘림은 필요한 파일 재출력으로 보완했다. 원문 전문은 저장소에 복제하지 않았다.
다음 최소 생산: 84FR14610의 Part744 변경 원규칙 한 건을 좁힌 창 감사와 연결하되 Part738 변경 또는 China-binding 제한으로 미리 분류하지 않는다.
