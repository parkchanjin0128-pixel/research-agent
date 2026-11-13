# 연구보고서 산출물

- `연구보고서_최종.pdf`: A4 한국어 보고서 22쪽. 제목·초록·클릭 가능한 목차·본문·수식·표·부록·문헌·페이지 번호를 포함한다.
- `연구보고서_원문.md`: 입력 보고서의 출력용 복사본. 원본은 수정하지 않았다. `原문`을 `원문`으로, 유니코드 긴 대시·음수기호를 ASCII 하이픈으로 표준화했다.
- `figures/`: 실제 보존 집계로 생성한 native-vector 개별 도표 6개와 PNG 미리보기.
- `build_report.py`: ReportLab 생성 코드. source의 수식을 다른 식으로 대체하는 hardcode 변환을 사용하지 않는다.
- `verify_report.py`: 원문 블록·표셀 포함 여부, 텍스트 안전영역, 현재 입력과 출력용 복사본 일치, 전체 페이지 렌더 여부 검사와 contact sheet 작성.
- `qa/`: 전체 22쪽 PNG, contact sheet, 확대 검토 화면, PDF 추출 텍스트, SHA256와 검토 결과.

입력 경로는 코드가 있는 디렉터리를 기준으로 기존 연구 작업의 상대경로를 사용한다. 번들 Python의 `reportlab`, `pypdf`, `pdfplumber`, `Pillow`와 Windows의 Malgun Gothic·SimSun·Segoe UI Symbol 글꼴이 필요하다. 렌더는 Poppler `pdftoppm`을 사용한다. Office COM과 GUI는 사용하지 않는다.

## 재생성

1. 번들 Python으로 `build_report.py`를 실행한다.
2. `pdftoppm -r 100 -png 연구보고서_최종.pdf qa/page`로 전체 페이지를 렌더한다.
3. 번들 Python으로 `verify_report.py`를 실행한다.
4. `qa/contactsheet.png`와 확대본에서 마지막 PDF의 레이아웃을 확인한다.

수치의 인과적 타당성에 대한 판정은 본문과 기존 연구 검증 기록을 따른다. 조판 QA는 학술 심사를 대체하지 않는다.
