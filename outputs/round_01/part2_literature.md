# Part II. 문헌 검토 — 1회차 완료본

기준일: **2026-10-12**. 사용자가 제공한 8파일을 검사했으며 고유 논문은 7편이다. 두 SSRN5373282 파일은 SHA256이 동일하다. L13과 L14 검토본은 모두 **June 2026**이다. L14의 종전 서지상 2025-11-30 날짜를 제공 원문의 버전으로 대체한다. 수령 내역은 `pdf_receipt_log.csv`에 기록했다.

**Gate 1: 부분적으로 답변됨.** ANPRM 이후 중국 특허의 변화, 실제 제재 뒤 연구투입·자본배분·기술방향 전환은 이미 연구되었다. 확인한 문헌 중 **무제한 공식신호→실제 제한 이전 구간→비특허 연구·자본 배분→기술 비교**를 함께 식별한 연구는 확인하지 못했다. 이는 검색·접근 범위에 한정된 판정이며 보편적인 선행연구 부재의 증명은 아니다.

문헌표는 33편, 확인 수준은 **전문 확인12 / WP PDF 확인12 / abstract만9**다. 이 중 L23은 WP 표지·초록만 확인했으므로 원문 상세검토 편수에 넣지 않는다. 가까운 14편은 **L01·L02·L03·L04·L06·L07·L08·L09·L10·L12·L13·L14·L26·L27**이며 모두 원문 기준 상세검토했다. L11·L15·L28은 추가 상세검토다. L15는 저자의 인용 보류 요청이 있는 예비자료로 최종 논문 인용에 사용하지 않는다.

논문의 정책 설명은 **2차 자료**이며 법적 효력 검증과 별개다. 데이터 필드·접근권은 아직 제공기관에서 검증하지 않았다. KAIST는 모두 **구독 여부 확인 필요**다.

## 1. 검색 프로토콜과 종료 범위

영어·중국어 질의, OpenAlex/Crossref, SSRN·RePEc·NBER 및 공식 저널의 발견·추적 기록은 `search_log.csv`에 남겼다. 최초 탐색 뒤 검색어 계획을 작성했으므로 모든 질의가 사전등록되었다고 주장하지 않는다. Scholar/CNKI 직접 통합검색의 접근 실패와 일부 초기 hit/screen 집계 미비는 그대로 기록한다. 일반 검색엔진의 site: 검색은 해당 DB 내부 검색과 구별한다.

Kang et al. backward search는 Crossref 참고문헌50개·RePEc 매칭42개에서 출발했고, OpenAlex forward search의 당시 인용문헌12개 제목을 확인했다. 일반 OpenAlex 첫50건, ANPRM44건 중 첫25건을 screening했다. 제공 원문의 참고문헌과 새 문헌들은 기존 기록과 대조했으나 모든 참고문헌의 전문까지 검토한 것은 아니다.

이번 마무리 검색은 두 소규모 라운드에 각각 영어·중국어 질의 1개를 사용했다. 반환 결과는 1라운드17+15건, 2라운드10+14건이며 각각 제목·요약을 screening했다. 기존 L01/L12, 법률·정책해설, 다른 ANPRM, 비관련 특허연구가 주로 검색되어 **두 라운드 신규 직접 실증문헌은 0편**이었다. 검색엔진 전체 hit 수가 아니라 반환건수다. 질의별 제목은 내부 audit에 보존했다.

**Saturation은 전체 프로토콜 차원에서 여전히 입증되지 않았다.** 위 제한된 후속검색의 0건과 전체 DB 포화를 혼동하지 않는다. 정밀도가 낮은 질의, OpenAlex 미열람 잔여분, 접근 불가 DB와 미확보 원문이 남아 있다. 사용자의 이번 확보 범위를 반영하여 이 한계를 명시한 상태로 1회차를 종료한다. 종료 요건은 포화 달성이 아니라 수행한 프로토콜과 포화 여부의 정직한 보고다.

보류 후보 Ryan–Burman의 *Globalization, Primacy, and the US–China Tech War*는 공식 OUP 전문에서 역사적 문헌·정책기록 분석임을 확인했다. ANPRM의 제도적 배경에 유용하나 중국의 제한 전 자원배분에 대한 계량식별 연구로 세지 않는다([논문](https://doi.org/10.1093/cjip/poaf011)). *Reforming Export Control Regimes*는 RePEc 서지 확인까지이며 novelty 판정을 바꾸는 인과연구로 편입하지 않았다. ‘耐心资本…’ 후보의 공식 페이지 열람은 실패하여 0건 발견으로 처리하지 않았다.

## 2. 제공된 원문 7편의 상세검토

### L01. Kang, Yankun; Ma, Xin; Xie, Mi; Zhong, Ninghua (2025). Innovation’s false spring: U.S. export controls and Chinese patent quality. Journal of International Money and Finance 150, 103229.

**전문 확인** — [서지·원문 경로](https://www.sciencedirect.com/science/article/abs/pii/S026156062400216X).

- **표본:** 2014–2022; 3년 인용 표본 종료연도는 본문과 표 주석 불일치
- **처치와 시점:** 2013–2017 중국 발명특허 중 Patsnap ANPRM 관련 topic 비중이 큰 IPC main group
- **시간 코딩:** 2018-11-19를 사건으로 서술; 회귀 Post=t>2018, 즉 2019–2022. 발표/실제 제한 분리 없음
- **기술·자료 연결:** IPC main group 3,451개×9년=31,059; Ratio>15.46% 처리, Ratio=0 비교, 중간양수 노출 제외; IPC class 내 처리군 존재 조건. Appendix C topic list
- **식별:** IPC/year FE DID·PPML; IPC cluster; 일부 subclass trend. Table 3 중미 특허수·가치 비율 비교는 국가 DDD가 아님
- **결과변수:** 출원연도 기준 발명특허 수, 인용, 가치, grant rate; Table 4 Tianyancha 산업별 신규기업 등록(비특허 보조결과)
- **결과와 해석:** Table 1 PPML 선호계수 .1705는 약18.6% 출원 증가; 평균 인용 하락. 신규기업 진입의 유의한 증가 없음. SOE 특허 반응 큼; 실제 연구비·VC 증가 직접 추정 아님
- **남는 문제:** 2019–2022 평균효과에 발표와 후속 제한/정책이 혼재할 수 있음. 법적 하위기술별 censor 없음; 실제 제한된 특허의 포함 여부는 규제 crosswalk 전 미확인
- **근거 위치:** 사용자 PDF 24p: §3–4 pp5–10, Table1/3/4/5, Appendix A–C pp14–22; 아래 보고서 네 질문
- **재현성:** Appendix C topic list·노출구축 규칙 공개; Patsnap classifier·snapshot·정확한 IPC membership 및 공개 코드 패키지는 미확인

### L03. Chen, Y. Joy; Gong, Robin Kaiji; Li, Jinlin (2026). Industrial policy in a new era: Government venture capital in the US–China trade war. Journal of Development Economics 178, 103599.

**전문 확인** — [서지·원문 경로](https://www.sciencedirect.com/science/article/pii/S0304387825001506).

- **표본:** 기술통계2010Q1–2019Q4; 주 회귀2017Q1–2019Q4
- **처치와 시점:** 2016 대미 수출가중 관세노출이 제조업 산업 중앙값 이상인 high-TWE×정부 VC
- **시간 코딩:** Post≥2018Q3; VC–기업 분석은 2017Q1–2018Q2 대 2018Q3–2019Q4
- **기술·자료 연결:** HS6→ISIC Rev3→Rev4→CIC2017 2자리; high/low 이분법; 정부/SOE 최종LP지분≥20%
- **식별:** 펀드×산업군×분기 DID/DDD, 펀드–산업군 FE 및 분기 FE, 펀드 cluster; 기존 VC–기업 쌍 별도 분석
- **결과변수:** 주 결과는 분기 산업군 투자 여부(투자액 누락 때문에 금액 아님), 후속금융·IPO·출원분기 기준 최종등록특허
- **결과와 해석:** 정부 VC 투자는 대체로 유지, 민간 VC는 high-TWE에서 축소. 신규·후속 투자와 기존 포트폴리오 구분. 정부 VC의 절대 투자액 증가로 해석 불가
- **남는 문제:** 관세 시행 충격. ANPRM 독립처치 없음. 정부·민간 차이만으로 novelty 부족
- **근거 위치:** 사용자 PDF 16p: §3 pp3–8, Eqs2–5, Table4 pp9, §4.3 수출통제 교란 검토, p14 data availability
- **재현성:** 본문: 저자는 데이터 공유 권한 없음. 온라인 보충자료 존재는 명시되나 이번 제공 파일에는 별도 부록 없음

### L04. He, Yuhan; Lyu, Jinqiu (2025). Export controls and innovation transfer within Chinese business groups: Evidence from the U.S. entity list. Research Policy 54(9), 105311.

**전문 확인** — [서지·원문 경로](https://www.sciencedirect.com/science/article/pii/S0048733325001404).

- **표본:** 2010–2022; 1,520 상장기업, 11,131 기업연도
- **처치와 시점:** Entity List 직접노출 기업과 같은 최종지배자 집단의 비등재 기업; 무제재 집단 비교
- **시간 코딩:** §4.1/Table1은 등재 following year로 서술; 사건연도 포함 여부의 코드 검증은 미완료
- **기술·자료 연결:** CSMAR 최종지배자·지배구조 수작업 검증, Qichacha 자회사/손자회사 등재 매칭; incoPat 특허
- **식별:** 기업/year FE 시차 DID, BJS/CS/SA/stacked 방법 강건성; 직접 제재기업은 간접처리 표본과 구분
- **결과변수:** 출원수·발명출원·특허/R&D, KZ·현금비율·학력별 직원비율, 집단 총량
- **결과와 해석:** 비등재 동종/상류 집단기업 특허 증가, 집단 전체 혁신 증가 증거 없음. KZ·현금 및 학력구성 변화는 자원재배분의 간접 증거로 해석
- **남는 문제:** 실행 뒤 그룹 내 반응. Table8은 실제 기업 간 자금이체·개인별 인력이동 flow 직접 측정 아님
- **근거 위치:** 사용자 PDF20p: §4 pp5–7, Table3/4; §6.1·Table8 pp12–14, data availability p18
- **재현성:** Data will be made available on request. 공개 패키지 링크는 제공PDF에서 확인되지 않음

### L06. Shen, Haomin; Gao, Yuan; Cheng, Xiaoke; Wang, Qi (2024). The impact of the U.S. export controls on Chinese firms’ innovation: Evidence from Chinese high-tech firms. International Review of Financial Analysis 95, 103510.

**전문 확인** — [서지·원문 경로](https://www.sciencedirect.com/science/article/abs/pii/S1057521924004423).

- **표본:** 2007–2020; high-tech 상장기업 8,425 기업연도; DID 수입자료2007–2016
- **처치와 시점:** 기업/집단 또는 공급자 등재, 또는 연차보고서의 통제영향 문구; 직접·간접·인지 노출 혼합
- **시간 코딩:** 기본식 전기 Exp_Control; 강건성 DID Post≥2013(Obama 2기), ANPRM 기반 아님
- **기술·자료 연결:** NBS 첨단제조/서비스 산업; 연차보고서 Word2Vec 사전; CNRDS·CSMAR·Customs
- **식별:** 기본 산업/year FE+lagged exposure, firm cluster; PSM-DID는 2012→13 대미수입 감소로 Treat 선정하여 사후선택 우려
- **결과변수:** R&D비/총자산; ln(1+특허출원)
- **결과와 해석:** 노출과 R&D·출원 증가 관계, 수입경쟁·기술의존·금융제약/보조금 이질성. 본 설계의 순수 신호 인과효과와 구별
- **남는 문제:** 미실행 신호 아님; 사후 수입감소에 따른 처리집단 선택 및 혼합노출 때문에 설계를 그대로 차용하기 어려움
- **근거 위치:** 사용자 PDF13p: §4 pp3–4 Eq1; §5.3.1 p5 2013 PSM-DID
- **재현성:** 공개 replication package 미확인; 논문 데이터 설명 확인과 직접 데이터 접근은 구별

### L07. Zhang, Jing; Liu, Canlei; Liu, Runjuan (2026). The Dual Effects of Technology Decoupling: U.S. Export Controls and Innovation in China. SSRN 6210408, posted February 10; revised February 11.

**WP PDF 확인** — [서지·원문 경로](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6210408).

- **표본:** 2010–2022; 121 IPC3 중 28 처리/93 비교. 2023까지 세면34개라 표본과 구별
- **처치와 시점:** 등재기업의 등재 전5년 최다 출원 IPC3를 주기술로 정하고 기술 내 첫 등재부터 노출
- **시간 코딩:** IPC3 첫 Entity List 지정연도부터; 2018 ANPRM과 무관
- **기술·자료 연결:** Google Patents, 474/502 등재명칭 매칭, 집단자회사 통합; 다중IPC fractional patent count
- **식별:** 기술/year FE TWFE 및 IPC1 선형추세, USPTO 동기술 특허수 통제; 본문 robust SE, cluster 수준 명시 없음
- **결과변수:** 출원연도 특허수·인용·generality·originality; 신규/기존 출원자별 특허
- **결과와 해석:** 선호식 출원 약10.8% 증가, 질/일반성/독창성 하락. 신규와 기존 출원자 양쪽 증가하되 기존 비중 우세
- **남는 문제:** 기술 단위 DID와 특허 수량·질 괴리 자체는 선행; 실제등재 기반이며 순수공식신호구간 없음
- **근거 위치:** 사용자 WP45p(2026-02): PDF pp9–12 §2.3/Eq1; pp15–16 Table5 설명; §4
- **재현성:** 공개 코드/패키지 미확인; Google Patents 기반이라도 entity명칭매칭·기술처리목록 재구축 필요

### L13. Gao, Hao; Shroff, Nemit; Zhang, Pengdong (2026). Do U.S. Export Restrictions Hurt Domestic Innovation? SSRN 5373282. 검토본 표지 Current draft: June 2026.

**WP PDF 확인** — [서지·원문 경로](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5373282).

- **표본:** 2001–2021; 처리313기업5,041기업연도·대조287기업4,946기업연도; stacked98,042 관측치
- **처치와 시점:** CSL 외국 고객 제재에 노출된 미국 상장공급기업; 고객21개국, 중국만 아님
- **시간 코딩:** 고객 최초 blacklist 등재 회계연도부터. CSL 여러 목록/자회사 중 최초 날짜
- **기술·자료 연결:** Compustat segments+FactSet 고객관계, 이름 fuzzy/manual match; Lightcast 연구직; 특허 기술유사도
- **식별:** cohort별 전5년 특성 PSM+stacked DID; firm×cohort/year×cohort FE, firm cluster. later-treated는 자기처리 전까지만 비교
- **결과변수:** R&D/매출, Lightcast 연구직 수·채용·이탈, 특허출원·영업비밀 공시
- **결과와 해석:** 미국 공급자 R&D강도 및 연구직/채용 감소, 특허출원 감소·비밀보호 공시 증가. 해외고객 특허추격은 appropriation 경로와 일관적이나 직접 모방 입증과 구별
- **남는 문제:** 미국 공급자와 실제 제재 충격. 중국 공식신호의 제한 전 투입배분은 다루지 않음
- **근거 위치:** 사용자 WP85p 표지June2026; PDF pp12–17 연구설계·데이터; 온라인 부록도 파일 내 포함
- **재현성:** 85p 본문·온라인 부록 제공. FactSet/Compustat/Lightcast 접근 및 공개 코드 패키지는 미확인

### L14. Liu, Laura Xiaolei; Ruan, Hongxun; Zheng, Yijing (2026). Export Controls and Technological Redirection. SSRN 7042518. 검토본 June 2026.

**WP PDF 확인** — [서지·원문 경로](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7042518).

- **표본:** 등재자료1997–2023; 회귀표별 시작연도는 제공본문에서 명확히 확인하지 못함; 이를 회귀표본기간으로 대체하지 않음
- **처치와 시점:** Entity List 중국기업과 미국공급자; IPC4 핵심기술 최초 등재 노출
- **시간 코딩:** 기술방향 분석: IPC4 첫노출 후 출원연도; 기업 추가분석: 기업 최초노출 이후
- **기술·자료 연결:** Google Patents 제목·초록 TF–BIDF; 사전미국공급자 핵심IPC4, incumbent/alternative 특허 유사도 비율 TRS; 임계값/전체목록 저자요청
- **식별:** 특허단위 DID, 출원year/IPC4 FE, IPC4 cluster. 기업추가분석 PPML+Callaway–SantAnna. 동일IPC4 비노출기업 비교
- **결과변수:** TRS=incumbent backward similarity/alternative similarity(하락=대체방향), 특허가치; §6 grants/citations/equity-scaled patents·ROA
- **결과와 해석:** 중미 노출기업 특허의 대체경로 이동; 중국 특허확대·미국공급자 특허감소. §6 명칭 Real Allocation이나 중국결과는 연구비/인력 직접측정이 아님
- **남는 문제:** 연구방향 전환 자체도 선행. 최초 실제등재 기반이며 ANPRM 제한전 투입배분 식별 없음
- **근거 위치:** 사용자 WP63p 표지June2026; PDF pp19–24 §4–5 Eq20–25; pp31–34 §6 Eq27; Appendix B
- **재현성:** §4 처리IPC 전체목록·선정임계값·rolling window 상세는 authors upon request. 공개 패키지 미확인

## 3. L01 ANPRM 논문의 네 가지 필수 질문

| 질문 | 원문 판정 | 근거와 주의점 |
|---|---|---|
| 발표효과를 별도로 추정하는가? | **아니오. 연도별 2019–2022를 하나의 Post로 처리한다.** | §4.1 Eq1의 t>2018. 2018-11-19 직후 일·월·분기 변화나 발표→제한 전 구간을 별도 추정하지 않는다. |
| 이후 실제 제한된 하위기술의 포함·제외는? | **하위기술별 실제 제한일에 맞춘 제외·분리 규칙을 확인하지 못했다.** | §3–4 및 부록 A–C. 폭넓은 기술 topic을 포함하지만 어느 특허가 실제 법적 제한 대상인지는 ECCN crosswalk 전 미확인이다. 3년 인용의 종료연도 조정은 법적 censor가 아니다. |
| 국가·기술 비교집단은? | 중국 내 IPC main group의 고노출 대 영노출. 미국도 일부 비교에 사용. | 2013–17 topic 비중>15.46% 대 0, 중간 양수 제외. Table3의 중미 특허수·가치 비율 비교는 국가×기술×시간 DDD가 아니다. ‘비교국가가 전혀 없다’고 쓰지 않는다. |
| 특허의 어느 날짜를 쓰는가? | **출원/application·filing 연도** | §3.1, Table A2. 등록연도나 공개연도로 처치를 붙이지 않는다. 다만 인용분석은 등록된 특허로 제한(주13). 날짜 기준과 eventual-grant 표본선택은 별개다. |

Table4의 Tianyancha **신규기업 등록**은 비특허 보조 결과다. 그러므로 이 논문을 ‘특허 외 결과가 전혀 없다’고 분류하면 틀린다. 그러나 연구과제·연구비·VC·R&D 인력의 이동을 직접 측정하지는 않는다. Table5의 등록자본에 따른 기업규모 구분은 투자유입 측정이 아니다. 특허 grant를 정부 grant로 번역하지 않는다.

인용 결과의 재현성 문제도 있다. 본문 p5는 2020년 이후 출원을 제외한다고 설명하지만 Table1과 Fig1 주석은 2014–2020이라고 표시한다. **2019 종료인지 2020 포함인지 미해결**로 남긴다. PPML .1705의 지수변환은 약18.6%이며 118% 증가가 아니다. 공급제약·연구자금·국가정책의 기여 비중은 이 계수만으로 분해할 수 없다.

정책 서술의 오류 가능성과 추정 결과의 존재를 구별해야 한다. 이 논문을 ‘순수 실제 통제 효과’로 인용해서도 안 되고, 반대로 censor가 없다는 이유만으로 전 기간 효과가 순수 신호였다고 재해석해서도 안 된다.

L25는 ECRA 관련 연구라는 초록 정보만 확보했으며 **2018 ANPRM 기반인지 미확인**이다. 확인된 ANPRM 논문으로 올리거나 네 질문을 추정으로 채우지 않는다.

## 4. 이전 실행에서 검토한 원문: 기존 7편

### L02. Liu, Liu, Makarin & Wen (2025) — WP PDF 확인

[HBS WP 25-004, 2025-09-12 버전](https://www.hbs.edu/ris/Publication%20Files/25-004_ea198f96-5936-443e-b30c-55d8570a3900.pdf). PDF pp.9–15, Eq.(1)–(2), Table 2, Figure 3, Appendix B를 확인했다.

2006년 제안 목록 77개 HS6 품목 가운데 2007년 최종 포함된 59개 품목의 사전 수입기업을 처치군, 최종 제외된 18개 품목만 수입한 기업을 비교군으로 삼는다. 기본 표본은 2000–2013년(2010년 제외), R&D 자료는 2001–2013년 중 2004년 제외다. 기업 및 county×year 고정효과와 사전 특성×연도 통제를 사용한다. Post는 2007년부터, 기준연도는 2006년이다. ECCN→HS→산업 매핑과 별도의 IPC→ECCN LLM 분류가 있다.

Table 2의 저자 환산 효과는 R&D 49.1%, 특허출원 41.3% 증가다. 출원 연도의 발명·실용신안과 연구자 수를 관측한다. 따라서 ‘특허 대신 R&D를 본다’는 것만으로 차별화되지 않는다. 핵심적으로 **처치·비교군 모두 제안 단계에서 지목되었다**. 2006년을 기준으로 삼은 2007년 이후 차이는 제안 자체의 효과와 다르다. 다만 이것을 자동으로 순수 implementation increment라고 부를 수도 없다. 제안 강도·노출 차이를 확인해야 한다. 2014년 VAT 관계를 과거 표본에 연결하는 부분은 사후 생존·네트워크 선택에 유의할 필요가 있다. 공개 재현 패키지는 미확인이고 Customs/NBS/VAT 자료 접근이 필요하다.

### L08. Crosignani et al. (2025) — WP PDF 확인

[New York Fed Staff Report 1096, 2025-02 개정](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1096.pdf). 예전 제목인 *Geopolitical Risk and Decoupling*과 중복 계상하지 않았다. PDF pp.13–20, Eq.(1), footnote 11, §§5–6을 확인했다. 후속 학술지 버전은 별도 원문 미검토다.

중국 고객의 BIS 목록 편입과 미국 공급기업을 연결한다. 주가 표본은 2010–2022년 250개 사건·156개 공급기업, 기업연도 표본은 2007–2022년 655개 기업이다. 목록 발표일 CAR와 사건 전후 3년 stacked DID를 사용한다. 기업-cohort 및 cohort×산업×규모×연도 고정효과가 포함된다. 공급망 관계종료, 시장가치, 이익·고용·대출 등은 검토하지만 이를 중국 R&D 반응의 추정치로 읽으면 안 된다.

이 논문의 ‘announcement’는 고객 등재의 가치평가 반응이다. 실제 제한 없이 여러 해 지속되는 후보 지정과는 다르다. 연도 분석에서 고객 모기업의 첫 사건을 고르는 과정에 가장 부정적인 CAR를 이용하는 선택이 들어가므로 이 코딩을 기계적으로 복제하면 안 된다. FactSet 등 상용자료와 FR Y-14의 접근 제약도 재현에 중요하다. 공개 패키지 존재는 미확인이다.

### L09. Clayton et al. (2025) — WP PDF 확인

[Geoeconomic Pressure, NBER 34020](https://www.nber.org/system/files/working_papers/w34020/w34020.pdf). PDF pp.3–12와 기업 대응 분석을 검토했다. 2008–2025년 기업회의 자료와 애널리스트 보고서를 이용해 압박의 발신자·수신자·수단·대응을 LLM으로 분류한다. 중국 A주 기업회의 자료도 포함한다. 모델 교체 등에 대한 검증이 있지만, 이것이 공식 신호의 외생성을 보장하지는 않는다.

수출통제와 R&D 대응, 관세와 가격 대응의 연결이 나타나므로 ‘신호의 인식과 연구 대응을 텍스트로 측정한다’는 발상도 선행된다. 그러나 **R&D를 언급한 것과 실제 연구지출이 증가한 것은 다르다**. 위협과 실행을 별도 법적 구간으로 정한 기술 비교 실험도 아니다. 본 연구의 salience 측정 참고문헌으로 유용하되, 현재는 자료 접근·필드 검증을 하지 않았다. 2025 관련 내용은 문헌의 범위만 기록하며 Trump 2기 정책 조사는 수행하지 않았다.

### L10. Benguria et al. (2020 WP / 2022 학술지) — WP PDF 확인

[Anxiety or Pain?, NBER 27920](https://www.nber.org/system/files/working_papers/w27920/w27920.pdf). 검토 버전은 2020 WP이며 Eq.(4)–(5), Tables 8–9를 중심으로 읽었다. 연차보고서의 TPU, 사전 HS8 무역구성에 기초한 관세 노출, 상장기업 재무자료를 결합한다. 재무자료는 2016Q1–2019Q3, 핵심 TPU 변화는 2017Q4→2018Q4, R&D는 2017→2018 연간 변화다.

TPU 상승은 투자·R&D 감소와 관련된다. 따라서 위협이 반드시 혁신을 촉진한다는 방향 가정은 피해야 한다. 관세를 통제한 변화 회귀도 수출통제 신호의 독립적 인과효과와 같지 않다. 특히 2018년 연간 R&D는 11월 발표 이전 활동이 대부분일 수 있어 ANPRM 반응의 즉시 지표로 옮겨 쓰기 어렵다. 기업 텍스트의 내생성 문제도 남는다. 재현 패키지와 상용자료 이용권은 미확인이다.

### L11. Amiti, Kong & Weinstein (2020) — WP PDF 확인

[The Effect of the U.S.-China Trade War on U.S. Investment, NBER 27114](https://www.nber.org/system/files/working_papers/w27114/w27114.pdf). §§2–4 및 자료·사건선정 부분을 검토했다. 2016–2019년 주가와 2018–2019년 11개 무역정책 사건을 이용하고, 중국 관련 매출·수출입·간접 공급망 노출에 따른 차등 요인과 공통 요인을 구분한다.

발표일 주가의 정보를 투자식과 연결해 2020년 말까지 투자성장률이 1.9%p 낮아질 것으로 추정한다. 이는 관측된 중국 연구비 감소나 ANPRM의 무제한 구간 효과가 아니다. 주가 반응에는 향후 현금흐름·할인율·거시 충격이 함께 반영될 수 있다. ‘발표와 투자’라는 일반 조합은 새롭지 않으며, 중국의 실물 연구배분으로 넘어갈 때 별도의 측정 근거가 필요하다.

### L12. 刘斌·李秋静 (2023) — 전문 확인

[美国对华出口管制与中国企业创新, 财经研究 49(12), 19–33](https://qks.sufe.edu.cn/J/PDFFull/99ae5d0b-6da5-49c9-8d38-0aee538df987.pdf). 인쇄 pp.23–26, Eq.(1)–(3), Tables 1·3을 확인했다. 2013–2021년 16,018개 기업연도에서 산업별 누적 Entity List 기업 비율을 이용한다. GB2017 산업 중분류에 연결하며 ANPRM의 IPC 분류가 아니다. 발명특허 출원과 R&D/주영업수입을 각각 분석한다.

기업·연도 고정효과, IV, 2018년 산업강도×post2018 연속처치 DID를 제시한다. 특허출원 감소와 R&D 강도 증가가 동시에 나타난다. Table 3의 특허·R&D 결과를 보면 특허가 실제 연구활동과 다른 방향으로 움직일 수 있다는 점이 중요하다. 저자들은 주목·등재 위험을 줄이기 위한 출원 행동도 논의한다. 다만 예측된 제재를 사용하는 IV가 다른 산업별 변화와 독립인지에는 별도 논증이 필요하다. **2018 post를 사용한다는 이유만으로 ANPRM 연구로 분류할 수 없다.**

### L15. Bonnet, Ciani & Zaurino (2025) — WP PDF 확인, 인용 보류

[2025-06-16 학회 초안](https://fondazionemasi.it/public/masi/files/ITSG/Rimini2025/BonnetCianiZaurino.pdf)의 pp.1–4, 8–10과 추정 설명을 검토했다. 표지에 **“Preliminary, please do not cite”**가 있으므로 여기서는 탐색 기록으로만 남긴다. 최종 연구계획의 정식 인용 근거로 사용하기 전 후속 공개본을 찾아야 한다.

2017-01–2024-08 월별 무역, 반도체 생산사슬 33개 HS6, GTA 정책 파동을 이용한 DID/PPML 분석이다. 미국 칩 수출 감소와 제3국 일부 장비 수출 증가를 보고하며 비축 가능성을 논의한다. 그러나 재고·무역 증가는 연구비 배분이 아니며 비축 해석 자체가 독립적인 announcement effect 추정도 아니다. 제3국을 깨끗한 비교집단으로 가정하기 어렵다는 참고가 된다. 원고의 통제 날짜·법률 설명에는 독립 대조가 필요한 부분이 있어 다음 회차 규제 데이터에 그대로 옮기지 않는다.

## 5. 연구인력·혁신·금융의 보완 원문

### L26. Bao et al. (2025 CRC WP; 2026 SSRN 개정판 존재) — WP PDF 확인

[CRC TR 224 DP645 원문](https://www.crctr224.de/research/discussion-papers/archive/dp645)의 §§3–6, Tables 5·6·8·9, Appendix D를 확인했다. 검토본은 2025년 1월 원고/2월 시리즈이며, 제목이 달라진 2026 SSRN 본문은 읽지 않았다. **SSRN 7412595와는 다른 논문**이다.

2017–2020년 입시·채용자료에서 관세와 전공별 노동수요를 연결한다. HS→산업→미국 ACS 전공·직업별 고용비중→중국 전공 매핑을 사용한다. 입시는 전년 12월 관세, 채용은 월별 관세의 3개월 lag를 사용한다. Tables 5–6에는 Entity List 기업 수·자본·고용에 따른 대안 노출도 있다. 높은 노출과 STEM 입학점수·연구직 상대수요 증가를 보고한다.

따라서 **인재 배분·채용·정부지원·Baidu 인식**이라는 조합도 선행된다. 다만 입학점수는 지원 수요의 지표이지 실현된 연구인력 공급이 아니다. 미국의 전공-산업 구조를 중국에 적용하는 매핑도 별도 타당화가 필요하다. 채용 표본 종료가 본문 Table 9와 일부 Appendix D에서 다르므로 버전·표본을 구별해야 한다. 공식 무제한 신호 구간을 따로 식별하지 않아 Gate 1의 (a)·(b)는 충족하지 않는다.

### L27. Zhou, Chen & Tan (2026 권호; 2025-12-29 온라인) — 전문 확인

[공식 논문](https://www.mdpi.com/2071-1050/18/1/349), [확보한 공식 CDN PDF](https://mdpi-res.com/d_attachment/sustainability/sustainability-18-00349/article_deploy/sustainability-18-00349.pdf). pp.6–10, 12, 15–16, 20–21, 26을 검토했다. **ANPRM 연구가 아니라 Entity List 및 기업집단 연결 연구**다.

2015–2023년 제조업 2,891개 기업, 19,040개 기업연도에서 지정기업·연결 상장회사와 나머지를 비교한다. 특허는 출원연도로 집계하고 출원 후 18개월 내 등록비율을 질의 대리변수로 쓴다. TWFE 외 Sun–Abraham 결과도 제시한다. Table 3의 출원계수는 0.2466, 등록비율은 −0.0363이며 후자는 **3.63%p**다.

두 해석을 경계해야 한다. 첫째, 빠른 등록은 기술적 질뿐 아니라 행정 우선순위·조기심사 선택을 반영한다. 둘째, Table 11의 **특허 수/R&D 지출** 증가는 분모인 연구비 증가를 뜻하지 않는다. 별도로 연구인력 비중은 증가한다. 기업집단 연결 노출 역시 모든 계열사에 동일한 직접 법적 제한이 걸렸다는 증거가 아니다. 데이터 공개 문구는 제공기관 홈페이지를 나열한 것으로, 다운로드 가능한 분석자료·코드 패키지를 확인한 것은 아니다.

### L28. 马理·文程浩 (2026) — 전문 확인

[공식 논문 페이지](https://cjoe.cjoe.ac.cn/CN/10.12012/CJoE2024-0439). 인쇄 pp.231–236, 241–242의 표본·명세·결과를 검토했다. 2021Q1–2023Q3, 251개 기업(처치 61개·비교 190개)의 **주당 영업현금흐름**을 분석한다. 이는 연구비 배분 자체는 아니다. 제한기업 및 지배관계로 처치군을 구성하며 실제 제한이 없는 ANPRM 신호 연구가 아니다.

본문은 2022Q4 이전/2023Q1 이후, Table 1은 2022Q4 전후라는 시점 설명을 사용한다. 경계 분기의 코딩을 원자료에서 확인해야 한다. Table 3 열 3과 달리 열 4에 연도·분기 FE가 포함되며 계수는 −0.141(p=.030)이다. 이를 −14.1%의 효과로 해석해서는 안 된다. 타국 허가통계 IV에도 공통 정책·경기 충격의 배제제약이 필요하다.

재현 측면의 진전은 p.232 각주 1에 **데이터·코드 저장소 [DOI 10.57760/sciencedb.28963](https://doi.org/10.57760/sciencedb.28963)**가 명시되어 있다는 점이다. 저장소 직접 접속은 실패했으므로 파일·라이선스·실제 재현 가능성은 미확인이다. 이번 회차에서는 논문 저자의 정책 코딩만 검토했으며, 이를 법적 시행일로 승인하지 않았다.

## 6. 9개 문헌군의 범위 기록

| 문헌군 | 표에 기록한 문헌 | 해석상의 한계 |
|---|---|---|
| 1. Entity List/Huawei/ZTE/FDPR | L02, L04–L08, L12, L14, L25 | M&A·독립적인 ZTE/FDPR 효과 등 세부 범위의 검색 완결은 미충족 |
| 2. 2018 ANPRM | L01; L25 감사 후보; L16 분류 혼동 점검 | 확정된 기반 연구와 인접 문헌을 구분 |
| 3. announcement/anticipation | L02, L08, L09, L12, L15 | 주가 등재일·불확실성·무역비축을 순수 신호 효과와 혼동 금지 |
| 4. TPU와 R&D/innovation | L10, L17, L18 | 양·음의 반응 모두 보고; 공식 신호 정의와 다름 |
| 5. 관세 발표와 투자 | L03, L10, L11 | 발표와 시행 분리 정도는 논문별 상이 |
| 6. 다른 산업의 규제위협 | L19–L21, **3편으로 제한** | 일반적 ‘위협만으로 행동’ 주장의 선행성 |
| 7. 2022–2024 반도체 통제 | L15, L22 | 예비 초안과 비인과적 정책 분석; 강한 실증근거로 과장 금지 |
| 8. 2025–기준일 최신 문헌 | L09, L23, L24 | 문헌 기록만; 현행 정책 검증·조사 미착수 |
| 9. 미국 공급자 | L05, L08, L13, L14, L22 | 가치·매출·R&D·기술경로가 서로 다른 결과 |

인접 원문에서 특히 유용한 것은 [L19 규제위협 연구](https://findresearcher.sdu.dk/ws/files/174538156/201910_RTH_2_Oct_2019.pdf)의 위협 내생성 문제와 [L20 약가규제 연구](https://economics.mit.edu/research/publications/coordinating-lower-prices-pharmaceutical-pricing-under-political-pressure)의 미실행 개혁에 대한 행동이다. L19는 2010–2013년 가격민원에 예상 밖 열공급 고장을 IV로 사용하지만, 고장이 비용·평판에 직접 미칠 가능성은 비판적으로 검토할 수 있다. L20은 1993년 전후 규제취약성별 가격조정을 다루며 R&D의 인과효과 연구로 바꾸어 읽으면 안 된다.

[L22 CSIS 분석](https://www.csis.org/analysis/did-us-semiconductor-export-controls-harm-innovation)은 노출기업 R&D 감소를 발견하지 못한다. 다만 2024년 SOX 구성기업의 정규화 전후 비교이고 AI 성장·사후 표본선택이 섞일 수 있다. 저자는 **2022 통제의 특허효과는 공개지연 때문에 아직 분석할 수 없었다**고 밝힌다. 이 결과를 강한 반증으로 쓰지 않는다.

## 7. 종료 시 남긴 공백

L05·L25·L30·L31의 원문은 이번 확보 범위에 없으며 검증 수준을 올리지 않았다. L25의 ANPRM 처치 여부는 novelty 판정의 잔여 위험이다. 다만 사용자는 확보 가능한 전부를 제공했으므로 추가 제공 대기를 종료한다. `fulltext_request_list`는 재요청 목록이 아니라 **수령·잔여 공백 기록**으로 바꿨다.

L03의 온라인 보충자료, L01 Patsnap 분류모형·snapshot, L14 전체IPC·선정threshold·rolling-window 구현은 재현 단계의 미확인 항목이다. 데이터 제공기관별 접근권과 필드 검증은 4회차에서 수행한다. 논문이 데이터 출처를 적었다는 사실과 우리가 그 데이터를 확보했다는 사실은 다르다.
