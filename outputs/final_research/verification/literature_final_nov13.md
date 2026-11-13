# 문헌 새 사실 독립 검증 - 2026-11-13

판정: **verified - 지정 범위에 한정**. 현재 `pdf_audit.md/json`, `report_main.md` §2.1 및 새 참고문헌의 핵심4편·Chen 서지 관련 26개 검증항목은 실제 제공 PDF와 부합한다. 원고 전체 승인, 분석코드 재현 또는 최초성 증명은 아니다.

- verifier: `/root/nov13_literature_final_verify`; producer: `/root/nov13_pdf_literature`.
- 확인일: 2026-11-13; 기록시각: 2026-11-13 12:59:22 UTC.
- 독립성: 현재 생산물을 주장 식별용으로 읽은 뒤 실제 Downloads PDF를 pypdf 6.6.0으로 새로 열었다. 이전/현재 referee나 verifier 판단을 증거로 사용하지 않았다. `user_pdf_inventory.json`은 locator·재고 목록 용도뿐이다.
- 허용 쓰기: 본 MD/JSON과 추출 코드 1개. 원고·ledger·상태파일을 변경하지 않았다.

## 핵심 판정과 강한 반례

1. Gao 제공본은 June 2026·85쪽이며 CSL 복수명단에 등재된 해외 고객과 연결된 미국 공급자 연구다. 2001–2021, 등재연도별 stacked DID 및 코호트 등재연도 포함 Post는 원문과 일치한다. 과거 HTML403·전문미확보 기록은 현재 로컬 원문 접근의 제약이 아니다. 이번에 현재 웹접근을 시험한 것은 아니다.
2. Zhang의 IPC3는 등재 직전 5년 최다특허 분야다. 2010–2022 분석창의 121=28+93과 2023까지의 34를 구분하는 서술은 맞다. 동시기 USPTO 특허 수 공변량과 2010–2017 분야 간 인용 네트워크는 서로 다르며, 미국기원 인용비중 처치가 아니다.
3. **Liu 원문의 시계 불일치가 실제로 확인된다.** 식25 설명(PDF24쪽)은 해당 IPC 최초 등재 뒤 출원, 표1 주석(43쪽)은 공급자 첫 중국 고객 등재 뒤 출원이다. Ts·Tk도 구분된다(21–22쪽). 실제 코딩의 동일성이나 차이를 이 문구만으로 확정할 수 없다. 현재 원고가 이 불일치를 보존한 것은 타당하다.
4. **He 원문에도 t=0 표현 차이가 있다.** PDF1쪽은 등재 당해연도와 그 이후로 설명하지만 5쪽·표1은 following-year 표현이고 식2 사건시간은 등재연도에 맞춘다. 실제 코드의 당해연도 포함 여부는 미확정이다. 표7의 ratio는 기업 특허 중 미국특허를 인용하는 특허 비율이다. 이를 본 연구의 개별 인용링크 미국비중과 동일 측정으로 합치면 반박된다. 현재 원고는 그 동일성을 주장하지 않는다.
5. He의 자본·인력 근거는 KZ·cashhold·학력별 직원구성이다. 개별 자금이체나 근로자 이동의 직접 추적이라는 외삽을 하지 않아야 한다. 집단 전체 혁신효과의 비유의는 영효과의 증명이 아니다.

현재 지정된 새 사실에 직접적인 `contradicted` 항목은 없다. 별도 경계검사에는 잘못된 측정 동일성 1개 `contradicted`, 실제 코딩·현 웹접근·전체 문헌 최초성 등 4개 `unverifiable`을 기록했다. 이들은 현재 원고가 주장한 사실을 오류로 세는 항목이 아니다.

## 실제 원문 신원과 locator

아래 실제 증거는 사용자 제공 Downloads 원본을 로컬로 연 것이다. 비공개 절대경로는 공개형식에 적지 않는다. 웹 URL은 찾아가기 위한 locator이며 온라인 원문 접근 성공의 증거와 분리한다. 쪽수는 표지를 포함한 1기준 PDF 쪽수다.

| ID | 원문 basename | 실제 SHA256 | 총쪽수 | 새로 읽은 쪽 |
|---|---|---|---:|---|
| gao | `ssrn-5373282.pdf` | `6ea4b904f0898bf22bf6ccb51900c384e1cefc1c02c62a9d1ca1e996b9d1c780` | 85 | 1, 12, 13, 14, 15, 16, 17, 19 |
| gao_duplicate | `ssrn-5373282 (1).pdf` | `6ea4b904f0898bf22bf6ccb51900c384e1cefc1c02c62a9d1ca1e996b9d1c780` | 85 | 신원·쪽수만 |
| zhang | `ssrn-6210408.pdf` | `10dbd3b0a4da72f8377da722622d174ef7b4170aacbf394b7bef9905b69a2c63` | 45 | 1, 9, 10, 11, 12, 21 |
| liu | `ssrn-7042518.pdf` | `a606a0a92a0a984b99ab78041c8ba24f74a6e3e5498aa3079131e1185f7423e2` | 63 | 1, 19, 21, 22, 23, 24, 43 |
| he | `1-s2.0-S0048733325001404-main.pdf` | `37866abeeb9c03e0b4f29e6a859a7faa30d7d37f6ba33d60ef47392b53243784` | 20 | 1, 5, 6, 7, 11, 12, 13 |
| chen | `1-s2.0-S0304387825001506-main.pdf` | `40db705d6546ddc7a1a04bf65cf3ed30062a1c62d9018c5619803cb79cea9fa1` | 16 | 1 |
| kang | `1-s2.0-S026156062400216X-main.pdf` | `17da67af637a63ce5ca6d5a2f2e1b0ff34f3b244bc2abff905daa740233b770c` | 24 | 신원·쪽수만 |
| shen | `1-s2.0-S1057521924004423-main.pdf` | `67e2ba8d9be6de7ef512cef5ed6dfd1e62494f4fa6035aaa619f3edd27c506c1` | 13 | 신원·쪽수만 |

8파일은 7고유문헌이다. Gao 두 파일은 실제 SHA256이 같으므로 한 편이다. Kang·Shen은 원문 신원과 쪽수만 재확인했다. 이번 보고서는 두 논문의 내용 확인을 과거 이력보다 상향하지 않는다.

| ID | 원문 locator | 실제 확인 범위 |
|---|---|---|
| gao | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5373282 | landing page not re-accessed; SSRN number supplied by basename |
| zhang | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6210408 | landing page not re-accessed; SSRN number supplied by basename |
| liu | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7042518 | landing page not re-accessed; SSRN number supplied by basename |
| he | https://doi.org/10.1016/j.respol.2025.105311 | DOI printed on PDF page 1; resolution not re-tested |
| chen | https://doi.org/10.1016/j.jdeveco.2025.103599 | DOI printed on PDF page 1; resolution not re-tested |

## 주장별 확인

| ID | 대상·주장 | 판정 | 원문 위치·관찰 |
|---|---|---|---|
| V01 | 8개 제공파일은 7고유문헌이며 Gao 두 파일은 동일하다. | verified | gao/gao_duplicate PDF 파일 전체 해시·쪽수: 독립 SHA256 계산에서 두 Gao 파일의 해시가 동일하다. 모든 파일의 실제 쪽수도 새로 계산했다. |
| G01 | Gao, Shroff, Zhang 원고는 June 2026, 85쪽이다. | verified | gao PDF 1: 표지의 저자·제목·Current draft: June 2026 및 pypdf 85쪽을 확인. 웹 수정일을 원고일로 대체하지 않는다. |
| G02 | 처치는 중국 Entity List만이 아니라 CSL에 통합된 여러 미국 수출명단에 등재된 해외 고객과 연결된 미국 공급자다. | verified | gao PDF 15, 16, 17: CSL은 Commerce·State·Treasury 명단 통합이라고 설명. 공급망 연결은 제재 전에 존재해야 한다. PDF17쪽은 중국 외 Venezuela·Russia·Iran 등의 고객을 명시한다. |
| G03 | 미국 상장 공급자를 2001–2021년 자료로 분석한다. | verified | gao PDF 13, 16, 17: PDF13쪽은 U.S. listed company, 16쪽은 2001 시작·2021 종료, 17쪽은 제한 조건과 코호트 적층 후 표본을 설명한다. |
| G04 | 복수 고객·명단·자회사 등재는 최초 시점으로 연결한다. | verified | gao PDF 13, 15, 16: 각주12의 복수 고객 최초 연도, 15–16쪽의 복수 명단·자회사 최초 등재 및 같은 국가 복수 고객의 최초 blacklist date를 확인한다. |
| G05 | 등재연도별 stacked DID이며 Post는 코호트 등재연도 포함 회계연도다. | verified | gao PDF 12, 13: 식1은 firm·year·cohort 지표. Post는 코호트 사건연도 이상; 나중 처치되는 통제기업은 자기 등재연도 전 회계연도까지만 사용한다. |
| G06 | R&D/매출·연구직원·연구채용·이탈과 특허/영업비밀을 구분하며 초록 수치는 저자 보고치다. | verified | gao PDF 1, 14, 15: 초록의 13.8%·13.9%·24%·36%와 PDF14–15쪽의 R&D intensity 및 연구인력 관련 정의를 확인. 독립 재추정은 하지 않았다. |
| G07 | 확인한 주명세는 등재연도 전후로, 별도 예고일–시행일 사이 효과의 독립 명세로 해석하지 않는다. | verified | gao PDF 12, 13, 19: 식1의 연도 사건시계와 PDF19쪽 사건연구 설명에 기초한 제한적 독해다. 논문 전체 및 전체 문헌에 예고효과가 전혀 없다는 판정은 아니다. |
| Z01 | Zhang, Canlei Liu, Runjuan Liu 제공본은 February 2026 원고다. | verified | zhang PDF 1: 표지의 저자·제목·February 2026을 직접 확인한다. |
| Z02 | 등재 직전 5년 특허가 가장 많았던 IPC3를 기업의 주기술로 정한다. | verified | zhang PDF 9: §2.3의 baseline primary technology field 정의를 직접 확인한다. |
| Z03 | 2010–2022 분석창에는 121분야 중 처치 28·비처치 93이며 2023 포함 34와 구분한다. | verified | zhang PDF 9, 10: PDF9쪽은 2010–2023의 121·34, PDF10쪽은 분석창 2010–2022와 각주12의 28·93을 명시한다. |
| Z04 | 주처치는 해당 분야 첫 등재연도부터의 노출이다. | verified | zhang PDF 9, 10, 11: 식1의 sanction은 해당 연도까지 분야가 노출되었으면 1이고 첫 기업 designation 시점으로 결정한다. G06 첫 노출 2019 예시도 확인한다. |
| Z05 | 동시기 USPTO 분야·연도 특허 수는 공변량이고 2010–2017 분야 간 인용은 별도 네트워크 가중치다. | verified | zhang PDF 11, 12, 21: PDF11–12쪽 X의 contemporaneous technological shock 통제와 PDF21쪽 식5·사전 citation flows를 확인. 미국기원 인용비중 처치와 동일하지 않다. |
| Z06 | 기술분야 혁신량·질 및 지식네트워크 파급은 이미 분석 대상이며 주명세는 등재연도 기준이다. | verified | zhang PDF 1, 10, 11, 21: 초록은 수량·질·일반성·독창성·하류 파급을, 식1은 연도 노출을 설명한다. 그 현상 자체의 최초성 주장은 배제할 수 있다. |
| L01 | Laura Xiaolei Liu, Hongxun Ruan, Yijing Zheng 제공본은 June 2026이다. | verified | liu PDF 1: 표지의 저자·제목·June, 2026을 확인한다. |
| L02 | TRS는 기존 공급망 경로의 후방 텍스트유사도 합을 대안 경로의 합으로 나눈 비율이다. | verified | liu PDF 21, 22, 23: §4.4·식20–24: 같은 IPC4 안에서 공급관계 안/밖의 특허를 구분하고 제목·초록 TF–BIDF 코사인 유사도를 합산한다. 미국특허 인용비중이 아니다. |
| L03 | 공급자 Ts·IPC Tk·식25와 표1의 Post 문구는 구분해야 한다. | verified | liu PDF 21, 22, 24, 43: Ts는 공급자의 첫 중국 고객 등재연도, Tk는 관련 노출 공급자 중 가장 이른 사건연도. PDF24쪽 식25 설명은 IPC 최초 등재 뒤 출원, PDF43쪽 표1 주석은 공급자 첫 고객 등재 뒤 출원이다. 문구 불일치가 실제로 있다. |
| L04 | 공개 PDF만으로 모든 구축 세부를 재현했다고 주장할 수 없다. | verified | liu PDF 19, 21, 22: 자료 구축 세부, 정확한 선택 임계값·처치 IPC 전체목록·정확한 rolling window는 저자 요청자료로 설명되어 있다. |
| L05 | 미국 공급자·중국 표적기업의 기술경로 전환은 이미 이 논문의 분석대상이다. | verified | liu PDF 1, 24, 43: 초록은 양쪽 기업의 incumbent에서 alternative로의 전환을 명시한다. 본문·표1은 등재 뒤 TRS 비교를 설명한다. 해당 현상 자체의 최초성 주장은 성립하지 않는다. |
| H01 | He·Lyu 출판본은 Research Policy 54 (2025),105311, DOI 10.1016/j.respol.2025.105311이다. | verified | he PDF 1: 표지에 저자·제목·권호·article number·DOI·온라인 13 August 2025가 모두 인쇄되어 있다. |
| H02 | 2010–2022,1,520기업·11,131기업연도이며 집단 내 비등재기업이 간접 처치군이다. | verified | he PDF 5, 6: 같은 최종지배주주 아래 2개 이상 상장사, baseline의 자회사·손자회사 등재 포함, 비등재 집단 통제군 및 최종 표본을 확인한다. |
| H03 | 미국특허 인용 관련 비중·미국 대 중국 인용성향을 실제 종속변수로 사용한다. | verified | he PDF 12: 표7의 ratio는 기업 특허 중 미국특허를 인용하는 특허 비율이며 ratio_inv는 발명특허 대응 변수다. 식3의 decoupling은 미국/중국 인용수를 각 특허청 등록건수로 정규화한 뒤 나눈다. 본 연구 B의 개별 인용링크 분모와 같다고 읽으면 안 된다. |
| H04 | 자본·인력 재배분을 논의하지만 표8은 KZ·현금보유·학력별 직원비중의 간접 근거다. | verified | he PDF 5, 12, 13: H3·H4는 명시적 재배분 가설. §6.1와 표8의 실제 outcome은 자금제약·cashhold와 네 학력 집단의 직원 구성이다. 개별 자금이체·근로자 이동 추적과 구분하는 현재 서술은 타당하다. |
| H05 | 집단 전체 혁신효과는 유의하지 않다는 보고다. | verified | he PDF 12, 13: §6.2와 표9의 group-level 결과 및 결론에서 전체 혁신향상 가설을 지지하지 않는다고 설명한다. 이는 영효과의 증명이 아니다. |
| H06 | 실제 코드의 등재 당해연도 포함 여부를 공개문구만으로 확정하지 않는다. | verified | he PDF 1, 5, 6, 7: PDF1쪽은 등재연도와 그 이후로 설명하지만 PDF5쪽·표1은 following-year 표현이다. 식2의 사건시간은 등재연도 기준이다. 내부 표현 차이 때문에 정확한 t=0 코딩은 미확정으로 유지해야 한다. |
| C01 | Chen·Gong·Li는 JDE178(2026),103599, 온라인 2025년이며 DOI는 10.1016/j.jdeveco.2025.103599다. | verified | chen PDF 1: 표지에 저자·정식 제목·권호연도·DOI·Available online 15 August 2025가 인쇄되어 있다. 초록은 Section301 관세와 VC를 설명하며 수출통제 접근차단으로 바꿔 쓰면 안 된다. |

## 실제 코딩·외삽 경계검사

| ID | 검사한 추가 단정 | 판정 | 이유 |
|---|---|---|---|
| B01 | Liu 식25와 표1에 실제 사용된 Post 코딩은 동일하다. | unverifiable | 공개문구는 서로 다른 사건시계를 쓴다. 공급자별 사건연도가 동일 IPC 최초연도와 늘 같은지, 실제 코드가 무엇인지 확인하지 않았다. 현재 원고는 동일 코딩을 단정하지 않으므로 현재 원고의 contradicted 사실은 아니다. |
| B02 | He·Lyu 실제 코드가 등재 당해연도를 포함한다/제외한다. | unverifiable | 당해 포함 표현과 following-year 표현이 공존한다. 코드를 재현하지 않아 둘 중 하나를 확정하지 않는다. |
| B03 | He 표7 ratio와 본 연구의 개별 인용링크 미국기원 비중 B는 같은 분모·같은 측정이다. | contradicted | 표7 ratio는 특허 중 미국특허를 인용하는 특허의 비율이고 B는 인용링크의 미국 비중이다. 동일 측정이라는 외삽은 반박된다. 현재 §2.1은 이 동일성을 주장하지 않는다. |
| B04 | 현재 SSRN HTML/PDF 접근도 2026-11-12와 마찬가지로 403이다. | unverifiable | 이번 확인은 실제 사용자 제공 PDF를 직접 읽은 로컬 접근이다. 웹을 다시 요청하지 않았다. 과거 실패 기록을 현 접근 상태로 승격할 수 없다. |
| B05 | 전체 문헌에서 신호–시행 분리와 사전 차단가능 투입별 배분반응 조합을 처음 연구했다. | unverifiable | 전체 문헌의 최초성 증명은 범위 밖이다. 이번 선택쪽 감사는 4개 주명세 독해와 Chen 서지만 뒷받침한다. |

## 읽은 현재 산출물의 해시

| 현재 파일 | SHA256 |
|---|---|
| `outputs/final_research/literature/pdf_audit.md` | `bf9c1d3fc9e21306d6951d503631c908eff1bed9e6eff3d625778cf8c8ada463` |
| `outputs/final_research/literature/pdf_audit.json` | `266b6c90451c2f36c0564336caba446943e929af55964116795f285dcc66d1e0` |
| `outputs/final_research/report_main.md` | `342f989367535db5fe61a0bf91dd23c9f06b857475dfd0d138ccf7fa69cce7fb` |
| `outputs/final_research/literature/user_pdf_inventory.json` | `64791109b68880c313949281da193c1208413a776a74c5bc630a11571e11b713` |

추출 코드: `outputs/final_research/verification/verify_literature_final_nov13.py`; SHA256 `156a3fbdcfb104bc0d131b511b1a0bcb1ef52ec52637a093e40e2d7d41d002de`.

## 서지 확인과 한계

- Gao: Hao Gao, Nemit Shroff, Pengdong Zhang; *Do U.S. Export Restrictions Hurt Domestic Innovation?*; Current draft June 2026. 표지에서 확인한 원고일이며 SSRN 웹 수정일 검증이 아니다.
- Zhang: Jing Zhang, Canlei Liu, Runjuan Liu; *The Dual Effects of Technology Decoupling: U.S. Export Controls and Innovation in China*; February 2026.
- Liu: Laura Xiaolei Liu, Hongxun Ruan, Yijing Zheng; *Export Controls and Technological Redirection*; June 2026.
- He: Yuhan He, Jinqiu Lyu; *Export controls and innovation transfer within Chinese business groups: Evidence from the U.S. entity list*; Research Policy 54 (2025),105311; DOI 10.1016/j.respol.2025.105311; 온라인 2025-08-13. 모두 PDF1쪽.
- Chen: Y. Joy Chen, Robin Kaiji Gong, Jinlin Li; *Industrial policy in a new era: Government venture capital in the US–China trade war*; Journal of Development Economics 178 (2026),103599; DOI 10.1016/j.jdeveco.2025.103599; 온라인 2025-08-15. PDF1쪽 서지·초록만 이번 보조검증 범위다.

선택된 관련 쪽의 완전한 텍스트를 읽었고 원문 전체 텍스트 덤프나 PDF 복사본을 만들지 않았다. 분석코드·추정수치 재현, 저자 인과주장의 독립 검증, 모든 문헌 검색의 완전성·최초성 증명은 범위 밖이다. 등재연도는 논문의 사건시계이지 개별 거래의 실효 접근차단일을 확인한 판정이 아니다.

Ledger 통합 시 새 핵심4편의 지정 사실과 Chen 표지 서지에만 이 source check를 연결할 수 있다. 실제 Liu/He 코딩·현재 웹접근·전체 문헌 최초성·Kang/Shen 내용·원고 전체의 인과 결론을 verified로 올리지 않는다.

