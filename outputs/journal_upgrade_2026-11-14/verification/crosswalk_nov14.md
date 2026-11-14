# 2026-11-14 crosswalk 독립 검증

검증자 `/root/nov14_crosswalk_verifier`. 생산자·root와 다른 fresh ID이며 이 unit의 과거 판단을 재사용하지 않았다. 공식 파일을 새로 내려받고 생산코드를 import/실행하지 않는 별도 파서로 재계산했다. 생산자 자체검사는 독립 증거로 쓰지 않았다. 결과·B·특허건수는 읽지 않았다. 유료 API·예약·다른 UI를 사용하지 않았고 producer 파일은 수정하지 않았다.

## 판정

**309→348 exact-code 연결과 24개 기술영역 후보 라벨은 제한된 의미에서 지지된다. 이 표만으로 식별에 유효한 비노출 대조군은 확립되지 않는다.** protocol의 “같은 계층”은 현재 표에서 충족되지 않는다. 판정은 분류입력의 사실 검증이며 인과설계·Gate·불가역 freeze 승인 또는 referee accept가 아니다.

직접 공식 IPC–ANPRM 대응표가 존재한다는 주장은 하지 않는다. `positive`는 ANPRM에 열거된 기술영역의 후보라는 연구자 의미추론이고, `nonlisted`는 공정의 분류상 본체가 열거기술 자체가 아니라는 판단이다. 어느 쪽도 개별 특허의 신기술성·새 규제대상·실제 접근차단을 뜻하지 않는다. [ANPRM 83 FR 58201–58202](https://www.govinfo.gov/content/pkg/FR-2018-11-19/html/2018-25221.htm)의 Representative Technology Categories (2),(9), Emerging Technologies 앞 문단을 대조했다.

## 실제 재현한 범위

| 항목 | 독립 재계산 | producer와 차이 |
|---|---:|---:|
| 선택 그룹 / 라벨 | 24 / positive12·nonlisted12 | 0 |
| IPC2017 canonical membership | 309 | 0 |
| canonical×연도×alias | 3,255 | 0 |
| 그룹×code의 2017–26 exact union | 348 | 0 |
| RCL 경로 | 48 | 0 |
| 각 판본 선택그룹 사이 exact-code 중첩 | 0 | 0 |
| 선택그룹 직전 closure 밖 source의 공식RCL incoming | 0 | 0 |
| CSV union과 SQL CTE membership | 348 | 0 |

WIPO scheme10개(2017–26)·연간 RCL9개(2018–26)를 각각 HTTP200으로 새로 받았다. 19개 영어 XML 해시가 producer가 참조한 원문과 모두 같았다. 단순 합계 대조에 그치지 않고 canonical/alias/union/edge의 **집합 대칭차가 모두 공집합**임을 확인했다. 각 연도의 forward closure가 같은 root의 당해 공식 하위트리와 정확히 같고, 348개의 판본 없는 코드가 다른 확인판본에서 선택 root 밖의 의미로 나타나는 사례도 없었다.

48은 서로 다른 “기술 48개”가 아니다. F130(2020) 5경로와 F141(2023) 43경로로서 **9개 source record에서 source code를 유지하는 Y경로9개와 새 target의 N경로39개**다. `default=N`을 버리면 세분 코드를 놓친다. `incoming0`은 2017–26의 선택그룹 연결에 관한 좁은 공식 RCL 검사다. WIPO는 RCL을 연속 판본 사이에서 범위가 실질적으로 바뀐 곳의 대응으로 설명하며, 개별 문헌에 실제 재분류가 모두 반영되었다는 보증으로 설명하지 않는다. [WIPO IPC FAQ, RCL·판본·재분류 설명](https://www.wipo.int/en/web/classification-ipc/faq).

## 24개 의미 판단

아래 2017→union 수는 분류코드 membership 수이며 특허·성과 건수가 아니다. 모든 root의 공식 제목과 상위문맥을 확인하고, 아래 예외가 있는 하위제목을 별도 점검했다. 모든309개 leaf 내용에 대해 개별 특허를 읽었다는 뜻은 아니다. 공식 XML locator는 JSON에 보존했다.

| ID | IPC2017 root | 기술 본체 | ANPRM locator | 2017→union |
|---|---|---|---|---:|
| P01 | G06N3/02 | 신경망 모델 | (2)(i) | 7→33 |
| P02 | G06N3/12 | 유전모델 컴퓨터 | (2)(ii) | 1→3 |
| P03 | G06N5/00 | 지식기반 모델·표현·추론 | (2)(v) | 3→11 |
| P04 | G06T7/00 | 영상 분석 | (2)(iv) | 66→66 |
| P05 | G10L13/00 | 음성 합성·문자→음성 | (2)(vi) | 10→10 |
| P06 | G10L15/00 | 음성 인식 | (2)(vi) | 28→28 |
| P07 | B33Y10/00 | 적층제조 공정 | (9) | 1→1 |
| P08 | B33Y30/00 | 적층제조 장치·부속 | (9) | 1→1 |
| P09 | B33Y40/00 | 적층제조 보조작업·설비 | (9) | 1→3 |
| P10 | B33Y50/00 | 적층제조 데이터·제어 | (9) | 2→2 |
| P11 | B33Y70/00 | 적층제조 전용 재료 | (9) | 1→2 |
| P12 | B33Y80/00 | 적층제조 제품 | (9) | 1→1 |
| N01 | B21B1/00 | 금속 압연 | 해당 없음 | 30→30 |
| N02 | B21C1/00 | 금속 인발 | 해당 없음 | 19→19 |
| N03 | B21D5/00 | 판금 직선 굽힘 | 해당 없음 | 10→10 |
| N04 | B21D7/00 | 봉·형재·관 굽힘 | 해당 없음 | 14→14 |
| N05 | B23B1/00 | 선삭 방법 | 해당 없음 | 1→1 |
| N06 | B23C3/00 | 특정 가공물의 밀링 | 해당 없음 | 22→22 |
| N07 | B23D1/00 | 수평 직선 평삭·형삭 | 해당 없음 | 16→16 |
| N08 | B23D5/00 | 비직선 평삭·형삭 | 해당 없음 | 3→3 |
| N09 | B23D15/00 | 평행날 전단 | 해당 없음 | 8→8 |
| N10 | B23D45/00 | 원형톱·마찰톱 절삭 | 해당 없음 | 14→14 |
| N11 | B24B5/00 | 회전면 연삭 | 해당 없음 | 30→30 |
| N12 | B24B7/00 | 평면 연삭·유리 연마 | 해당 없음 | 20→20 |

P01/P02는 명시된 신경망·유전계산과 직접 대응한다. P03 지식기반 모델/표현/추론을 전문가시스템 계열로 연결하는 것은 의미추론이며 모든 항목이 완성된 전문가시스템이라는 일대일 대응은 아니다. P04 영상분석은 컴퓨터비전의 유효한 기술영역 후보지만 고전적인 분할·정합·기하분석도 포함한다. P05/P06도 공고의 음성 생성/인식 예시에 맞지만 AI 방식만을 골라낸 표본은 아니다. 따라서 positive 전체를 “새로운 AI 통제 기술”로 확대하면 안 된다.

비지목12개에서 **공정 본체를 직접 열거기술로 재분류할 근거는 발견하지 못했다.** 다만 N04의 프로그램제어(B21D7/12), N07/N08의 복사장치 제어, N06의 터빈날개 가공(B23C3/18)은 최종용도·공분류를 확인할 지점이다. 터빈날개 가공 전체를 극초음속 추진으로 바꾸거나 일반 프로그램제어를 AI로 간주하는 것도 원문보다 넓은 추론이다. N11은 비금속 물품, N12는 세라믹·유리·목재·플라스틱 하위도 포함한다. 이들은 금속만의 대조군이 아니다. 산업·시장·정책 노출이 같거나 없는지는 이 분류표로 확인되지 않는다.

## B33Y·확장·병합의 정확한 해석

[공식 IPC2017 scheme](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20170101/MasterFiles/ipc_scheme_20170101.zip)의 `ipcEntry kind=n symbol=B33Y` 노트는 공정·재료와 무관한 적층제조 범위, 다른 분류와 결합한 검색, 의무 보충분류, first-position 비배치, 다중 aspect 분류를 명시한다. 따라서 P07–P12는 동일 family에 붙는 보완적인 분류가 될 수 있다. 여섯을 독립 실험처럼 더하거나 firstIPC 감소를 기술쇠퇴로 읽으면 안 된다. 합집합에서 family 중복을 한 번 세는 규칙은 타당하다.

그러나 selected6 union은 B33Y 전체가 아니다. 모든 확인판본에서 `B33Y99/00`가 추가된다. 따라서 잔여그룹을 임의로 nonlisted에 넣거나 subclass prefix가 완전히 같은 정의라고 말할 수 없다. 이 누락은 현재 문서가 전수 AM 표본이 아니라고 밝힌 범위 안에서는 알고 있는 제한이며 숨겨진 누락은 아니다.

P01/P02 union 역시 G06N3 전체와 같지 않다. 2017–22에는 `3/00`, 2023–26에는 `3/00,3/004,3/006,3/008`가 더해진다. 이들 생물모델·인공생명·집단행동/로봇 영역을 자동 비지목 또는 기존 union과 동등하다고 간주할 근거는 없다.

병합표를 그대로 적용하면 positive6·nonlisted12, 총18단위다. 신경망/유전계산은 서로 다른 ANPRM 세부항목인데 묶고, P05/P06은 같은 (2)(vi)인데 남겨 둔다. 이것이 잘못된 계산이라는 뜻은 아니지만 공식 정책충격의 독립 단위나 균일한 IPC 계층이라는 증거는 아니다. 새 병합은 원 exact union을 보존하는 명시적 분석 정의여야 한다.

## 과거시점 분류에 대한 반증 점검

B33Y의 공식2017 entry와 note의 edition은 `20150101`이다. 따라서 도입 이전 문헌의 현재 B33Y 배정은 당시 관찰 가능했던 분류라는 보장이 없다. WIPO FAQ 역시 재분류 지연을 설명한다. 2017–26 합집합이 과거 시점의 데이터 가용성을 복구하지는 않는다.

추가로 [공식2016 scheme](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20160101/MasterFiles/ipc_scheme_20160101.zip)과 [2016→2017 RCL](https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/20170101/MasterFiles/ipc_concordancelist_20170101.zip)을 새로 확인했다. G06T7은4→66코드로 세분되지만 **기존2016의4코드는 현재 union에 모두 남는다.** 그러므로 이 main-group 표본에서는 2017 세분화만을 이유로 구코드 누락이나 특허 증가가 발생했다고 단정할 수 없다. 남는 문제는 실제 DB의 분류배정시점·기관별 반영·도입 전 B33Y 가용성이다. 데이터가 없으므로 크기·방향은 판정하지 않는다.

## 남은 지적

**CW-N14-01 · major · open_protocol_deviation: 같은 IPC 계층 요건은 충족되지 않음.** 동일 파서는 검증됐지만 동등한 기술 크기·분류밀도·정책충격 단위는 성립하지 않는다. 24행 또는18단위의 균등 비교를 단일 계층 설계로 부를 수 없다.

필요한 조치: protocol 이탈을 명시하고 24행,18단위 및 정책문구/기술영역 단위의 역할을 결과와 무관하게 고정·공개한다. 의미를 넓히는 prefix 교체로 해결했다고 쓰지 않는다.

**CW-N14-02 · major · open_identification_dependency: 비지목 공정은 검증되지만 무노출·외생 대조군은 미확립.** 정확한 코드집합 중첩0/공식RCL incoming0은 family·기업의 양팔 노출과 정책파급을 배제하지 않는다. 시장·기술군 차이, 시기별 분류관행 차이를 해결하지 않는다.

필요한 조치: family 양팔·단위간 중첩, ALL/firstIPC 차이, 사전지원·추세·공통지지 및 기존정책 노출을 별도 확인할 때까지 관측 비교로만 해석한다. 이 검증은 결과/B/특허건수를 읽지 않았다.

**CW-N14-03 · major · open_measurement_dependency: 현행 분류의 과거 시점 해석은 복구되지 않음.** B33Y 도입 전 문헌·지연 재분류·기관별 분류가용성을 과거의 기술/시장 반응으로 읽으면 측정편향이 된다. 다만 G06T7의 2017 세분화 자체로 구코드 누락을 주장할 근거는 없다.

필요한 조치: 사용 DB의 IPC판본·분류시점·문헌공개시점·추가/발명정보·첫위치의 관측가능성을 명시하고 관측되지 않으면 retrospective 측정으로 제한한다.

**CW-N14-04 · minor · open_metadata_issue: 참조된 외부 주석이 적용 주석처럼 한 배열에 합쳐짐.** 원문복제 자체는 정확하고309/348 membership에는 영향이 없지만 모든 참조 대상의 subclass 규칙을 신경망에 상속되는 scope로 읽으면 안 된다.

필요한 조치: 단순 참조문맥과 실제 적용/상속 주석을 분리하고 관계를 표시한다. 전체 메타데이터를 적용 scope의 전수검증으로 부르지 않는다.

CW-N14-01은 protocol 적합성 지적, CW-N14-02/03은 식별·측정의 선행조건이며 현재 producer가 이미 유효한 인과대조군이라고 주장했다는 판정은 아니다. CW-N14-04는 membership 오류와 구분되는 metadata 문제다. 이들을 임의로 resolved 또는 N/A로 처리하지 않는다.

## 증거와 재현 파일

- `crosswalk_nov14.json`: 현재 판단·24개 semantic 판정·출처URL/locator/해시·producer입력 해시·finding.
- `crosswalk_nov14_aux/fresh_source_manifest.json`, `fresh_extra_source_manifest.json`: 새 공식 다운로드의 응답·ZIP member·SHA256.
- `crosswalk_nov14_aux/independent_recomputed.json`: 별도 파서의 전체 집합대조·선택코드·제목·노트.
- `crosswalk_nov14_aux/retrospective_check.json`, `sql_check.json`: 별도 반증·SQL 대조.
- `crosswalk_nov14_aux/official/`: 해당 원문 증거. 원문을 보고서에 장문 재게시하지 않았다.

공식 source XML/HTML SHA256:

| 자료 | SHA256 |
|---|---|
| 2017 scheme | `1f6df51bd1306090013d505bfd1523837745e3461fdb1044535950eeb2861935` |
| 2018 scheme | `186b3ef3e36f281afae44d98cac90d678208b19a307b29b7f153fb9792464617` |
| 2019 scheme | `f1610858fff74ba9aa0e49aa94b0885b4d10aaf70048c2e826f28fac4da4b8a4` |
| 2020 scheme | `f9dc1725e97b550638168bd8b3c5e873cd16aa82c7976b7330bcb57dd5c9f3bd` |
| 2023 scheme | `9004e0bf237615cb0a6aed104fb7514e741f7c8c3112456b8522417c3286b59d` |
| 2022 scheme | `f4fe95fc735b1dd7130c6b2f914b6f015bf398e013c696750b22c47df2b5d437` |
| 2021 scheme | `6e71dcf6041d988d2b7c83f17e2945af34f3b184b0e44954cb5e151269150d12` |
| 2024 scheme | `74e6187c64e80db451f3501f9ef3f09a3321b027e0ee69f185bf517206ea9a72` |
| 2018 concordancelist | `23b256b21b5fbfa107a3ac6df33a49db96da903c8413d34c0674f56ca0e20071` |
| 2019 concordancelist | `0d343942b6bbcd5a2c479c980c68084aebf7ed9aaa32bd41a204f2357b047968` |
| 2020 concordancelist | `9862fe61fe85be1071a990d2ade647f77857c24a75e75fd4c868d88355f8ad1a` |
| 2021 concordancelist | `8c03e51f2a7e14bafbc51e8299a1b9eca39b57df327004a9105a83b40ce405e6` |
| 2022 concordancelist | `ab4c37fe1c603035a0f774962b9044713b14694df664a3394714b847d0612e30` |
| 2026 scheme | `60abc42ec68c8c8ea789fa5698404fe893a0f9b79156b1d8f2d15318ef6904a3` |
| 2023 concordancelist | `c4fe3e9062f100ce784135e7f3330abd3ce7aa4d24e03cbfdcbbf6d296f8ae6e` |
| 2025 scheme | `57e524d64ba0a9a3a7f3d732629b9591ead63b95d1733132d1eaebdf9b4638d4` |
| 2024 concordancelist | `a2ec617703d16a94d728f81530178b733e5cbae86374e34dc53d3dae9855eccb` |
| 2025 concordancelist | `4a7ed826b7cc6593d9d38d3322c7ad2a25a83d075ab498d6f9d68cadda57d042` |
| 2026 concordancelist | `9c6184b39f954980a09336a3be9e334d3bfdc783b8a4aff0d95b211e68440b5e` |
|  ANPRM | `7d554564f90691598635e6691ba5777d7dcce1744756d535d471b2a20e167852` |
| 2016 scheme | `796d7f43ac0ebfac61b2313b577c2f31789f26f3307cfea1220d539a43faf994` |
| 2017 concordancelist | `088c10f014668a9d2367ec489d7dfd769b8b425da30dd0191332d089099f83c5` |
|  FAQ | `432130c9507dbc5822ef2ae168b55afcc705de602f5c13451567abf7967a729a` |

production의 “다른 파일 열람0”이라는 과거 실행행동 전체는 producer 자기보고만으로 독립확인하지 않았다. 현재 생산코드의 정적검사와 이 verifier 자신의 비열람 범위만 확인했다. 연구 전체 완료·유효한 인과효과·새 Gate는 판정하지 않는다.
