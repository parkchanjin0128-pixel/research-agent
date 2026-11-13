# 선례 7편의 새 독립 원문 검증

판정: **verified - 수정된 지정 핵심절 범위**. 새5편과 보존된 기존2행의 원문을 각각 새로 읽었다. 7편의 핵심 식별구조·시점·가정과 본 연구 전이한계의 검증이며, 모든 증명·분석코드 재현 또는 A2/Gate 전체 완료 판정이 아니다.

verifier `/root/nov13_literature_final_verify`; 새5편 producer `/root/nov13_precedent_completion`; locator 수정자 `/root`. 실제 원문 PDF/HTML을 새 pypdf·BeautifulSoup 코드로 읽었고 생산자의 추출TXT·렌더이미지·과거판정으로 대체하지 않았다. 검증일2026-11-13, 기록시각13:17:07UTC.

## 확인 결과와 수정 이력

- Finkelstein:1986발표·1988효력인 VICF에 ADOPT를1987부터 주는 각주5를 확인했다. 기대시기를 포함한 처치이며 발표/시행의 별도효과 계수가 아니다.
- Blume:노출은2004–05 MEPS이므로2003입법 이전고정 지표가 아니다.2004할인카드 부분혜택과 식3의 더미중복도 확인했다. 순수신호창·정확한원코드재현으로 승격하지 않는다.
- Moser:실제 라이선스 선택과 ITT/IV의 가용자원을 구분한다. 원문의 정확한 Post는 after1918=1919부터다. IV배제제약은 현재B에 자동승계되지 않는다.
- Handley:기대정책확률과 상태별손실을 구조모형으로 연결하며 실증은 관세비율의 비선형 잠재손실이다. 확률×손실의 직관을 본 연구B의 금전손실로 대체할 근거는 아니다.
- Malani:선행추세가 anticipation의 증명이 아니라는 문장과 기대모형·lead IV의 제한을 확인했다. 사용한50쪽원고는2015-02-09판이며 실제출판판본 미대조를 유지한다.
- P&S와 CGBS:보존된2행을 과거검증으로 자동이월하지 않았다. P&S의1999gap·Post2001·상대효과/각주18·EU3중차분을 새로 확인했다. CGBS는 실제Feb2024표지·가정2–5·정리3.1–3.3이 맞고 현재NBER웹판과 동일성은 미확인이다.

**PF01(resolved)**: 초기 Blume의 §3.2 locator는 해당HTML에 없어 contradicted였다. root가 MD/JSON/manifest를 §3.1/#S8와 식3/#FD3로 수정했고 현재판을 원문 앵커와 독립 재대조했다. 원문SHA는 불변이다. 수정전3파일도 보존본의 실제SHA를 대조했다. 현재판에 미해결 contradicted항목은 없다. Moser1919부터 정밀화도 원문과 일치한다.

CGBS에서 SPT는 명칭상 강하더라도 PT4와 논리적으로 항상 포함관계인 것은 아니다(Remark3.2). 이 두 가정의 추가내용은 사전추세만으로 구별할 수 없다. 본 연구B는 처리dose가 아닌 사전특성·효과조절변수이므로 원문의 정리와 가중공식을 곧바로 β에 적용하지 않는 경계를 유지해야 한다.

## 실제 원문·판본·locator

모든 파일SHA와 PDF총쪽수는 새로 계산했다. 실제 내용 증거는 아래 로컬1차원문이며 URL은 원문locator다. 비공개 절대경로를 기록하지 않는다. PDF뷰어쪽과 인쇄쪽은 다르며 HTML에PDF쪽수를 부여하지 않는다.

| ID | 실제 원문 | SHA256 | 총PDF쪽 | 새로읽은 locator |
|---|---|---|---:|---|
| handley2017 | `handley2017.pdf` [원문](https://terpconnect.umd.edu/~limao/aer_final.pdf) | `98b3005722eec1447e490ca9046b3e061e2d9a13626e45e8049574bdba9b0e7b` | 53 | 1, 8, 9, 14, 15, 18, 19, 20; printed = PDF + 2730 |
| blume2013 | `blume2013.html` [원문](https://pmc.ncbi.nlm.nih.gov/articles/PMC3711884/) | `a6ce1190fb21630d730fa73396e51c126e42903b706d8f33d4f0809ba269f34b` | HTML | #S3, #S4, #S5, #S6, #S7, #S8, #FD3, #FN7, #FN8, #T2, #T3; No PDF or printed-page numbers assigned to this HTML |
| moser2012 | `moser2012.pdf` [원문](https://www.petramoser.net/uploads/6/9/4/2/69429445/moservoena12_aer.pdf) | `9247d072afc15c293b95e4ff78ab4fda486fb9cea76fdb4736a9803e814b6967` | 38 | 1, 2, 3, 6, 9, 11, 18, 19, 32, 33; printed = PDF +395 for article pages1–32; last6 pages are cited-by material |
| finkelstein2004 | `finkelstein2004.pdf` [원문](https://economics.mit.edu/sites/default/files/2022-08/Static%20and%20Dynamic%20Effects%20of%20Health%20Policy-Eviden.pdf) | `8da7f0ff0aab81bde63e5ff8f6c01d5714e6b67f4e4845d760d2cc58a0c26f65` | 38 | 1, 9, 10, 11, 13, 14, 17, 18, 32, 33, 34, 38; printed = PDF +526 |
| malani2015 | `malani2015.pdf` [원문](https://julianreif.com/research/reif.jpube.2015.anticipation.pdf) | `b3952074d41d4929b983dc3b1aa0f9691c46bbcf468007b398ce2e6ae6c813f5` | 50 | 1, 6, 11, 12, 15, 16, 17, 19, 22, 23, 24, 25, 26, 27, 28, 29; manuscript printed number = PDF page |
| pierce2016 | `pierce2016.pdf` [원문](https://www.justinrpierce.com/index_files/pierce_schott_aer_2016.pdf) | `396e697e96562110eb74575464cb8b738270a512a9db9fd81dde37ed55f63864` | 42 | 1, 5, 6, 7, 10, 11, 13, 14, 16, 17; printed = PDF +1631 for journal article pages |
| cgbs2024 | `cgbs2024.pdf` [원문](https://www.nber.org/system/files/working_papers/w32117/w32117.pdf) | `462516203de4c056de9638393de63e0622d489e29be790e375d2fc0da29d5906` | 61 | 1, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20; body printed = PDF −2 |

Malani는저자원고, Blume는accepted manuscript다. Moser38쪽 중 학술지본문은32쪽이고 뒤6쪽은 cited-by자료다. CGBS의로컬파일은61쪽·표지Feb2024다. 현재NBERURL은이번직접요청403이었다. P&S저자URL은이번웹도구에서42쪽PDF로열렸지만 로컬파일과바이트동일성까지비교한것은아니다.

## 주장별 판정

| ID | 원문위치 | 핵심주장 | 판정 | 본연구대응·한계 |
|---|---|---|---|---|
| P01 handley2017 | PDF8–9,14–15,18; printed2738–2739,2744–2745,2748, eqs2,11;Table2 | 무역 불확실성은 미래 정책 전환확률과 상태별 비용·이윤에 대한 기대를 모형화한다. 실증 잠재손실은 tariff iceberg 비율의 비선형 변환1−(τ2/τ1)^−3이며 2000–2005 수출 로그변화의 식11에 들어간다. | verified | B를 곧바로 확률×직접차단비용으로 읽거나 R&D의 부호·단위로 전이할 수 없다. 확률×비용은 직관 요약이며 원문의 정확 함수가 단순 NTRgap 곱이라는 뜻은 아니다. |
| P02 handley2017 | PDF15,19–20; printed2745,2749–2750 | 2000PNTR 입법은 WTO가입 조건부,2001-12-11가입·2002-01-01발효다. 높은 TPU 산업의 차등성장이 유의해지는 연도는2002이며 baseline은2000–2005 장기차분이다. | verified | 이 장기차분을2000–2002의 순수 발표효과로 읽을 수 없다. 비교목적지는 목적지 공통 공급충격을 점검하지만 임의의 중국×기술×시간 교란을 제거하지 않는다. |
| P03 blume2013 | HTML§2.1#S3,§2.2#S4 | 49치료군×1998–2010 파이프라인 진입건수를 사용하며 MedicareShare는 MEPS2004–05 처방전의 조사 가중 Medicare 비중이다. | verified | 2006 시행 전 측정이지만2003 입법 후이므로 엄격한 입법 이전 고정노출 선례가 아니다. |
| P04 blume2013 | HTML§3.1#S8,footnote7#FN7,Tables2–3 | 2003,2004–05,2006–07,2008–10을 나눠 분석한다. 각주7은2004년6월부터 Medicare 할인카드가 본인부담을15–20% 낮췄다고 설명한다. | verified | 2004–05는 저자가 anticipatory라 불러도 모든 실제 혜택이 없는 순수신호창은 아니다. |
| P05 blume2013 | HTML§3.1#S8,eq3#FD3,Tables2–3 | 식3 m벡터의 첫행 Year>2003은 뒤의 세 구간더미 합과 겹치지만 표는2003계수를 따로 보고한다. | verified | 주어진 HTML표기 그대로면 열종속이다. 출판본/원코드 대조 없이 Year=2003으로 고쳐 정확한 재현이라고 할 수 없다. 현재 표가 모호함을 보존한 것은 맞다. |
| P06 blume2013 | HTML headings and #S8/#FD3, corrected current3artifacts | 식3·Tables2–3의 현재 locator는 §3.1/#S8와 #FD3가 맞으며 §3.2는 이 HTML에 없다. | verified | 초기 locator 오류를 발견했고 root 수정 후 현재 MD/JSON/manifest의 해당 위치를 독립 재확인했다. findingPF01은resolved다. |
| P07 moser2012 | PDF2–3,6,9,11; printed397–398,401,404,406 | 처치는 실제 라이선스 여부·수·합산잔여수명이며 outcome은 미국발명자 특허 부여건수다. 19main classes·7,248subclasses중336이 실제노출이다. | verified | 선택된 사후 이용량을 사전 미국의존도B와 같게 볼 수 없다. 특허부여와 실제 연구선택 시점도 다르다. |
| P08 moser2012 | PDF2–3,6,9; printed397–398,401,404 | TWEA는1917-10-06, 체계적 라이선스는1919부터다. baseline postTWEA는 after1918, 즉1919년부터이며 정확한 개별 라이선스 부여일은 불가용하다. | verified | 현재판의1919부터 정밀화는 원문과 일치한다. 예고와실제이용전창을 따로식별한 선례가 아니다. |
| P09 moser2012 | PDF18–19; printed413–414,§III.D | 선택 내생성을 인정하며 ITT는 라이선스 가능한 적국특허 수다. IV는 가용특허 수로 실제 라이선스 수를 도구화한다. | verified | IV배제제약은 미라이선스 가용특허가 직접 국내발명을 늘리지 않는다는 것이다. 이를 현 연구의 미국인용·수입비중 도구의 타당성으로 승계할 수 없다. |
| P10 finkelstein2004 | PDF10–11,13; printed536–537,539,eq1 | 주결과는 질병×연도 새백신 임상시험 진입이며 ADOPT는 질병별 정책 이진노출이다. 질병·연도FE로 대상/대조질병 변화를 비교한다. | verified | 연속 사전 위협량의 주회귀가 아니며 연구 파이프라인 단계를 구분해야 한다. |
| P11 finkelstein2004 | PDF9,11fn5,32–34; printed535,537fn5,558–560 | VICF1986발표·1988효력에도 ADOPT는 기대가 알려진 첫 완전연도1987부터다. HepB1991권고·flu1993년5월보장도 확인된다. | verified | VICF효과에 기대시기를 포함하지만 발표효과와 시행추가효과를 별도계수로 분리한 것으로 말할 수 없다. |
| P12 finkelstein2004 | PDF9–10,13–14,17–18; printed535–536,539–540,543–544 | 정책선정의 기술변화 내생성, 대조질병의 잠재력·다른대조군, crowd-out 우려를 명시한다. 식2는 상대기간구간이며 기준은정책전1–3년이다. | verified | 해당 의약환경에서 crowd-out이 작다는 판단을 중국 연구자·자본 재배분으로 전이할 수 없다. 사전추세가 외생성의 증명은 아니다. |
| P13 malani2015 | PDF1 and manuscript page numbering | 사용 원문은 February9,2015 저자원고50쪽이다. | verified | 실제 Journal of Public Economics 출판본과 문언·식번호 동일성은 미대조로 유지한다. 원고쪽을 학술지1–17쪽으로 부르면 안 된다. |
| P14 malani2015 | PDF6,11–12;eqs1,4–5 | 현재 처치와 미래 처치기대를 함께 놓고 ex-post효과도 현재1기효과와 지속기대효과로 구분한다. | verified | 시행후 총효과를 전부 현재 실행효과로, 선행반응을 무조건 내생성으로 읽으면 안 된다. |
| P15 malani2015 | PDF15–17,19,28–29;eqs6–11 | 유한lead모형은 완전예견과 S기이후효과없음을 요구한다. 지수기대모형의 outcomelead/lag IV는 제한적 시계열상관·말기조건·직교가 필요하다. p19는 outcome관성이 lead IV를 무효로 만들 수 있음을 보인다. | verified | 기대모형의 식과 가정은 source에서 확인했지만 해당IV가 본 연구에 유효하다고 검증한 것은 아니다. |
| P16 malani2015 | PDF22–29;§4.3–4.4 | 원문은 pretrend가 anticipation의 증명이 아니라고 명시한다. 개혁채택외생성을 별도 가정하고 PA1997-01-25와1993–96신문기사를 예견가능성 보조근거로 쓴다. | verified | 고정된 공식신호일과 실제 제한일로 나눈 본 연구의 효과정의와 동일하지 않다. |
| P17 pierce2016 | PDF1,5–7;printed1632,1636–1638,eq1 | 1999NTRgap은 비NTR−NTR 관세이며2000입법으로 미래 인상가능성을 제거했다.2001년12월효력·2002-01-01시행 시계를 구분한다. | verified | 기존 두행의 이 사실을 과거판정으로 이월하지 않고 실제 원문에서 새로 읽었다. |
| P18 pierce2016 | PDF10–11;printed1641–1642,eq2,Table1,fn18 | 기본Post는2001부터이고 계수는 산업간 상대 log고용변화다. 분위수대비와 가상0gap 대비환산은 상대치이며 각주18은 전체고용감소 몫을 식별하지 못한다고 설명한다. | verified | 통합Post를 시행전 순수신호효과로 보거나0gap의무반응을 자동 가정하면 안 된다. |
| P19 pierce2016 | PDF13–14,16–17;printed1644–1645,1647–1648,eqs3–4 | 연별NTRgap 상호작용과 US대EU의3중차분을 사용하며 식4는 country×year,country×industry,industry×year FE를 둔다. | verified | 이 FE구조가 현 연구의 임의 중국×기술×시간 충격을 해결한다는 선례는 아니다. |
| P20 cgbs2024 | PDF1,10,12–17,19–20;printed8,10–15,17–18 | 표지NBER32117·February2024·61쪽, 가정2–5와 정리3.1–3.3·Remark3.1 번호가 실제로 맞다. | verified | 현재 NBERURL은 이번웹요청에서403이었다. 현재웹판이 로컬2024파일과 같거나 다르다고 확정하지 않는다. |
| P21 cgbs2024 | PDF12–14;printed10–12,Assumptions2–4,Theorems3.1–3.2 | 첫기간무처치·무선행반응과 실제D=0집단이 있는 기본설정이다. 일반PT아래 ATT(d|d)는 식별되나 강도집단차이는 causal response와 selection항을 합친다. | verified | 본 연구B는 실제처치dose가 아니라 사전특성이므로 해당정리를 β에 직접적용할 수 없다. |
| P22 cgbs2024 | PDF15–17;printed13–15,Assumption5,Theorem3.3,Remarks3.1–3.2 | SPT5는treated potential outcomes를 제한해 ATE·ACR를 식별하며, untreated가 없을 때 최소dose대비도 추가가정이 필요하다. | verified | 일반PT와SPT는 보통의 강도표현과 달리 논리적으로 항상포함관계가 아니라고 Remark3.2가 명시한다. 사전추세로두가정을구별할수없음도p14에명시된다. |
| P23 cgbs2024 | PDF19–20;printed17–18,Theorem3.4discussion | TWFE의 가중·선별항 문제와 선형관측관계만으로 causal response가 복구되지 않음을 설명한다. | verified | 정리3.4의 정확가중공식을 국가×기술×시간인 본설계로 직접이식하지 않는 현재 역사표의 경계는 맞다. |

## 확인하지 못한 추가 단정

| ID | 판정 | 주장과한계 |
|---|---|---|
| PB01 | unverifiable | Blume accepted-manuscript eq3 reproduces exact author implementation. Year>2003 overlaps the other3perioddummies; exact code/final typesetting comparison not done. Limitation retained. |
| PB02 | unverifiable | Malani2015 author manuscript and final journal publication have identical expressions/page numbers. Only dated50-page manuscript was inspected; final version comparison not done. |
| PB03 | unverifiable | Current NBER32117 remote PDF is the same February2024 bytes as the cached source. Current direct web request403. Cached actualcover/assumption numbers are verified; remoteversion unknown. |
| PB04 | unverifiable | All original empirical identification assumptions hold, or these precedents identify the current China signal effect. This work verifies what the original core models do and logical transfer limits, not truth of their counterfactual assumptions or current causal identification. |

## 현재 검증대상 해시

| 파일 | SHA256 |
|---|---|
| `outputs/final_research/methods_completion/precedents.md` | `95722975a499151b1531640121d7eb51d62ae510610668fea6b59f05169b30bd` |
| `outputs/final_research/methods_completion/precedents.json` | `fe6347732384929ed4dab2de8b944e084033329327cc652fd0f8c4b859916fff` |
| `outputs/final_research/methods_completion/source_manifest.json` | `c2dedbe78c26eb378bd9e54467efef5a6603563d3de5c45d0fae31486e1a46c9` |
| `outputs/final_research/methods_completion/existing_two_precedents_history.md` | `15799a6469e8ac877ba1747c1753b839120fc325d716a5a0a42dadfb111a81e2` |
| `outputs/final_research/methods_completion/locator_correction_nov13.json` | `4db284aab8c81f484ee49e7cfedffd007bbe74355e240d8c7ddafd420ed7fd1f` |

독립추출코드: `outputs/final_research/verification/verify_precedents_final_nov13.py`, SHA256 `fd6ab7d99b717d7d105d6bb714dcd2489331cffbbc442b29cf56d435544e8d55`.

새5편 생산물의 독립검증대기 문구와 기존2행history의 나머지5편대기 문구는 각각 저장당시 상태다. 이 보고서의 새판정으로 과거문구를 소급해독립검증완료였다고 바꾸지 않는다. 현원고·데이터·ledger·상태파일은 변경하지 않았다.

