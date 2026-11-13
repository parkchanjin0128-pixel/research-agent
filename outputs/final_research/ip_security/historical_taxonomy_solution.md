# WIPO 원문으로 연결한 IPC 2017 의미 범주

2026-11-12, 독립 생산. 원문 8개 ZIP을 실제 내려받아 XML을 추출했다. 추정 URL만 나열한 것이 아니다. `source_manifest.json`에 각각 응답·크기·SHA256, ZIP member 이름을 기록했다. `extract_crosswalk.py`를 실행하면 **RCL76개 방향 edge**, 해당 **scheme106행**을 재현한다. 독립 특허분류 감사나 family 재집계를 완료한 것은 아니다.

## 확인된 연결

| 공식 개정 | 이전 코드·2017 의미 | 후속 코드 | 함의 |
|---|---|---|---|
| 2018.01→2019.01, F093 | G06F15/18: Learning machines; 컴퓨터의 경험에 따라 실행 중 프로그램이 바뀌는 것. 2017 스킴에서 실제 존재. | G06N20/00,20/10,20/20. 15/18 삭제, 20/00 default reclassification=Y. | 머신러닝이 2019년에 처음 존재한 것이 아니라 G06F에서 G06N으로 이동한 부분이 있음. |
| 같은 F093 | G06N99/00: 나머지 그룹에 제공되지 않은 subject matter. 2017 스킴에서 실제 존재. | G06N10/00,20/00,20/10,20/20,99/00. 99/00 scope changed, 잔존99/00가 default=Y. | 새20의 과거 source는 하나가 아님. 새20을 일괄15/18로 되돌리면 과잉확정. 옛99 전체를 ML이라고 부르면 quantum/잔여를 섞음. |
| 2019.01→2020.01, F097 | G06F17/20: Handling natural language data. 2017 스킴 실제 존재. | G06F40/00. | 옛17/20 하위 의미 집합을 새40계열에 연결하는 공식 근거. |
| 같은 F097 | 17/21 텍스트처리,17/22 코드에 의한 조작/기록,17/24 편집,17/25 자동 정렬,17/26 자동 줄바꿈,17/27 자동 분석,17/28 자연어 처리·번역. 모두2017존재. | 각각40/10계열;40/12계열·40/194·197;40/166…186;40/189;40/191;40/20…35;40/40…58. | NLP 전체와 일부 하위 의미는 과거17/20 또는 각 세부코드에 대응시킬 수 있음. 정확 edge는CSV/JSON을 사용. |

공식 원문:

- [2017 scheme ZIP](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20170101/MasterFiles/ipc_scheme_20170101.zip)
- [2018 scheme ZIP](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20180101/MasterFiles/ipc_scheme_20180101.zip), [2017→2018 RCL](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20180101/MasterFiles/ipc_concordancelist_20180101.zip)
- [2019 scheme ZIP](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20190101/MasterFiles/ipc_scheme_20190101.zip), [2018→2019 RCL](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20190101/MasterFiles/ipc_concordancelist_20190101.zip)
- [2020 scheme ZIP](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20200101/MasterFiles/ipc_scheme_20200101.zip), [2019→2020 RCL](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20200101/MasterFiles/ipc_concordancelist_20200101.zip)

## 2017 고정 의미로 실제 집계하는 방법

1. 정책 문구를 먼저 2017 의미로 고정한다. 예: 'ML 일반', '신경망', '자연어 번역'은 다른 집합이다. ANPRM이 NLP를 명시했다고 G06F40의 모든 텍스트 서식·버전제어가 같은 위협이라고 자동 판정하지 않는다.
2. 원자료가 가지고 있는 IPC 판본·classification value·분류 생성/갱신일을 확인한다. PATSTAT의 날짜 필터가 출원·공개일인지 분류시점인지 구별한다. 이미2017까지 공개된 문헌의 내용만으로 사전 지표를 만든다.
3. **NLP 의미:** 옛17/20 및 그 하위와 새40계열을 같은 의미집합의 후보로 연결한다. 분류 이력·내용으로 옛 코드와 후속 코드를 회수한 뒤, family×의미범주에서 union한다. 한 family가 옛/새를 모두 가졌다고 두 건으로 합산하지 않는다.
4. **ML 의미:** G06F15/18과 G06N99/00→G06N20의 many-to-many관계를 보존한다. 원 분류 이력이 없다면 새20에서의 각각 원천 비중은 RCL만으로 알 수 없다. (a) 공개 내용에 대한 고정 semantic rule로 ML를 재분류하거나 (b) 더 넓은 합동 범주 `옛G06F15/18 ∪ 옛G06N99/00` 및 후속 `G06N10 ∪ G06N20 ∪ G06N99`를 구성하는 대안이 있다. 후자는 ML 전용 범주가 아니므로 이름도 넓혀야 한다. 전체 후속기간의 추가개정도 연결해야 하며, 여기의2019/2020경계만으로2026판 closure가 완성되는 것은 아니다.
5. B의 분자/분모와 중국·비교국 outcome을 **같은 historical meaning map**으로 다시 계산한다. 새 코드의 포함/제외만 바꾼 불균등 표본을 비교하지 않는다. family 중복·의미범주 중첩은 사전규칙과 함께 공개한다.

## 무엇이 편향이고 무엇은 단순한 사후 측정인가

사후에 만들어진 코드로 과거 공개문헌을 일관되게 다시 분류하는 것은 회고적 measurement다. 라벨의 출현 연도만으로 미래정보 편향을 입증할 수 없다. 동일 내용의 문헌에 같은 규칙이 적용되고 정책 이후 outcome·처치노출 때문에 라벨 정확도/가용성이 달라지지 않는다면 사전 연결 proxy로 쓸 수 있다. 그러나 이를 당시 당국·연구자가 관측한 분류 또는 당시의 실제 통제범위라고 말하려면 별도 semantic·정보집합 근거가 필요하다.

반대로 정책/후속 기술성공에 의해 재분류의 강도나 포함 여부가 달라졌다면 label assignment의 내생성이 생길 수 있다. 이는 분류이력 또는 표본검사로 검증해야 할 가능성이지 여기서 확정한 사실은 아니다.

현재 파일럿은 모든 시기에 현행판 G06F/G06N을 쓰므로 **2019년의 기계적인 시계열 단절을 이미 관측했다고 주장할 수 없다.** 다만 G06F15/18이 G06N20으로 이동했다는 공식 기록은 현행 G06F/G06N 분할이2017분할과 다름을 확정한다. 현행 분류에 의한 상대기울기는 현행 의미집단의 진단일 수 있으나, 이를2017 고정 집단·당시 지목/비지목 대조로 바꾸어 해석할 수 없다. ML가 어느 비교셀에 들어가는지가 달라져 B·건수·중첩·표본선택이 달라질 수 있다는 구체적인 재집계 필요성이다.
