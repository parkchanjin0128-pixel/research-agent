# 연구 발표 자료 사용 안내

2026년 11월 12일 작성. 11월 13일 자료 준비, 11월 16일 월요일 30분 이상 발표 기준이다.

## 먼저 볼 자료

- deliverables/연구보고서.pdf — 18쪽. 초록·목차·실제 분석·방법·한계·참고문헌을 포함한다.
- deliverables/발표자료.pptx — 본문 30장과 부록 5장. 권장 발표시간 33분 55초. 네이티브 도표 6개와 내장 데이터가 있어 편집할 수 있다.
- deliverables/발표자료.pdf — 최종 PPTX를 다시 불러와 렌더한 35쪽 화면용 PDF다. 본문은 이미지로 들어 있다.
- deliverables/발표원고.md, 발표목차.md, 예상질문답변.md — 리허설과 질의응답에 사용한다.
- deliverables/연구보고서_편집용.docx — 텍스트 편집용 참고본이다. PDF를 정본으로 사용하고 Word에서 편집한 뒤 페이지 구성을 확인한다.

## 새로 실행한 분석

공식 NBS·MOST·MOF 공보의 2013–2020년 R&D 지출을 수집하고 증가율·비중·수행주체별 변화를 계산했다. 원문 수치와 독립 재계산을 대조했다.

EPO TIP PATSTAT에서 넓은 IPC 다섯 분류의 중국 주소가 식별된 패밀리를 분류별 200개씩 실제 표집했다. 전체 인용과 any-APP 인용쌍의 미국 주소 분수비중, 국가미상과 관청·주소 연결을 집계했다. 1,000은 분류×패밀리 관측이며 고유 패밀리 수와 다를 수 있다.

정책의 인과효과는 아직 추정되지 않았다. 이번 발표는 실제 공식통계와 특허 측정의 진단, 식별 설계 및 반례를 다룬다. 특허 파일럿은 최종 ANPRM 기술분류나 엄격한 당시 정보집합의 dose로 동결되지 않았다.

## 재현

- data/official_rd_series.json, official_rd_derived.json — 공식 원자료·계산 결과
- data/patstat_pilot_final.json, patstat_pilot_final.csv — 정제 후 최종 집계와 정의
- data/patstat_pilot_notebook.ipynb — 실행 출력이 저장된 실제 노트북
- scripts/compute_official_rd.py — 공식 통계 산술 재현
- scripts/extract_patstat_pilot.py — 저장 노트북에서 최종 출력 추출과 파생 통계 재현
- scripts/patstat_executed_cells.py — TIP에서 실행한 SQL 포함 코드. 서버 재실행에는 EPO TIP 환경과 접근권한이 필요하다.
- references/ — 문헌 14편의 서지와 원문 확인 범위
- review/ — 독립 검증·내용 심사·PDF 시각 검수 기록

초기 공백 미정리 인용 출력은 최종 분석에서 제외했다. 최종 JSON과 CSV는 국가 문자열의 공백을 정리한 출력만 사용한다.

PowerPoint 파일은 패키지·레이아웃·도표 데이터·재불러오기 렌더를 검증했다. PowerPoint 앱에서 직접 열어 편집하는 검증은 수행하지 않았다.

모든 데이터는 연구 범위와 출처의 한계를 보고서와 함께 사용한다. 결과가 알려진 국가만의 분모에 조건부라는 점, 같은 패밀리가 분류 사이에 중복될 수 있다는 점을 발표에서도 유지한다.
