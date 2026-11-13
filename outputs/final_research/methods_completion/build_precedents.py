from pathlib import Path
import json, hashlib, datetime
BASE = Path(__file__).resolve().parent
SRC = BASE / 'sources'
rows = [
{
'id':'handley2017',
'citation':'Handley, Kyle, and Nuno Limão (2017), Policy Uncertainty, Trade, and Welfare: Theory and Evidence for China and the United States, AER 107(9), 2731–2783.',
'doi':'10.1257/aer.20141419',
'primary_url':'https://terpconnect.umd.edu/~limao/aer_final.pdf',
'version':'저자 공개 학술지 출판본. 인쇄 p = PDF p + 2730.',
'read_scope':'§II.A–D 핵심 식·자료·시점·강건성, 인쇄 pp.2744–2750 / PDF pp.14–20; 식(11), Table 2. 구조모형 전체 증명·온라인부록의 수치 재현은 하지 않음.',
'unit_outcome':'HS6 산업별 2000–2005년 대미 수출액 로그변화. 기준 표본은 양년 모두 무역이 있는 산업; 수출 진입·업그레이드는 모형 경로이며 중국 연구투입을 직접 관찰한 회귀가 아님.',
'exposure':'2000년 column-2/MFN 관세의 iceberg-factor 비율. 기본 OLS의 잠재이윤손실은 1−(τ2V/τ1V)^(-3). 실제 부과된 추가 관세량이나 무작위 배정 dose가 아님.',
'event_dates':'2000년 10월 PNTR 법률 통과(중국 WTO 가입 조건부), 2001-12-11 WTO 가입, 2002-01-01 미국 PNTR 발효. 연간 패널에서 높은 TPU 산업의 차등 성장이 유의해지는 시기는 2002년.',
'counterfactual':'식(11): Δln R_V = f(τ2V/τ1V,γ)+bτΔlnτ_V+bdΔlnD_V+b+e_V. 낮은 잠재손실 산업과의 성장 차이; 보완 비교는 중국의 EU·일본 수출, 다른 국가의 대미 수출·대만. 정보변화가 없을 경우 잠재손실과 상관된 잔여 차등 성장 부재가 필요.',
'assumptions':'관세·운송비·부문충격을 조건화한 뒤 누락된 산업별 수요·공급 변화가 잠재손실과 동행하지 않아야 함. 이론적 수치해석은 무역·진입·불확실성 함수 가정 추가. 다른 목적지 비교는 목적지 공통 공급충격만 제거함.',
'announcement_implementation':'불확실성 제거와 거의 불변인 적용관세를 구분하지만 2000년 법률발표~2002년 발효 사이의 순수 발표효과를 따로 추정하지 않음. 2000–05 장기차분을 제한 전 창의 추정으로 부르면 오류.',
'mapping':'사전 잠재손실의 관측 가능한 경제적 정의, 함수형태 점검, 목적지·원산지 placebo를 옮길 수 있음.',
'nontransfer':'불확실성 해소의 수출 반응을 접근차단 위협의 R&D 증가 부호로 전이할 수 없음. 관세손실 공식·구조 파라미터도 특허인용/미국 의존도 B_k에 자동 적용되지 않음.',
'locators':[
 {'claim':'식별식 및 조건','printed_pages':'2744','pdf_pages':[14],'section':'II.A','equations':['11']},
 {'claim':'노출·정책 시점','printed_pages':'2745','pdf_pages':[15],'section':'II.B–C'},
 {'claim':'변환 노출와 OLS','printed_pages':'2748','pdf_pages':[18],'section':'II.C','tables':['2']},
 {'claim':'교란·pretrend·연별 시점','printed_pages':'2749–2750','pdf_pages':[19,20],'section':'II.D'}],
'open_issues':[],
'assessment':'잠재손실 이질성의 직접 선례; 제한 전 발표효과의 직접 추정 선례는 아님.'
},
{
'id':'blume2013',
'citation':'Blume-Kohout, Margaret E., and Neeraj Sood (2013), Market Size and Innovation: Effects of Medicare Part D on Pharmaceutical Research and Development, Journal of Public Economics 97, 327–336.',
'doi':'10.1016/j.jpubeco.2012.10.003',
'primary_url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3711884/',
'version':'PMC의 저자 accepted manuscript. 말미 publisher disclaimer는 copyediting/typesetting 이전임을 명시. 출판본 페이지 327–336을 HTML 위치로 역산하지 않음. PDF 요청은 challenge HTML, EuropePMC PDF는403; PDF 쪽수 미확인.',
'read_scope':'공개 HTML 전문의 §§2.1–2.4·3.1–3.2, 식(1)–(3), Tables 2–3, 각주7 및 publisher disclaimer를 직접 읽음. 논문·표의 구조 확인 완료; 정확한 원코드 재현은 아래 불일치 때문에 보류.',
'unit_outcome':'49개 약물 치료군×1998–2010 연도별 전임상 및 단계별 임상시험 진입 건수(Pharmaprojects). 금전적 R&D 지출액과 구분.',
'exposure':'MEPS 2004–05 처방전 중 Medicare 가입자 처방의 조사 가중 비중. 2006년 Part D 시행 전이나 2003년 입법 후 측정. 입법 이전에 고정된 B의 선례로 쓰면 안 됨.',
'event_dates':'2003년 MMA 입법, 2004–05 저자 명명상 anticipatory 구간, 2006–07 시행 직후, 2008–10 지연 반응. 각주7: 2004년6월부터 할인카드가 약값 본인부담을 15–20% 낮춤. 읽은 본문은 입법·전면시행의 월일을 제공하지 않음.',
'counterfactual':'§3.2·식(3): 치료군 고정효과의 지수형 조건부 평균, Medicare 비중×시기, 치료군별 선형 추세, 예측 시장규모·NIH R&D 시차. 낮은 Medicare 비중 치료군의 자체추세 대비 변화가 비교 기준; 치료군 수준 군집 표준오차.',
'assumptions':'고령화·공공연구·자체추세를 조건화한 뒤 Medicare 비중과 함께 움직이는 다른 치료군별 충격이 없어야 함. 저자 자료설명은 정책시점과 노출 모두에 상관된 보고누락이 없어야 한다고 명시. 사전 시행 비중도 입법 후 반응에서 완전히 자유롭다고 보장하지 못함.',
'announcement_implementation':'별도 시기 계수는 있지만 2004–05에 실제 할인 혜택이 존재하므로 모든 실제효과와 분리된 순수 정보창은 아님. 시행 이후 계수에는 수요·현금흐름·기대 경로가 함께 들어갈 수 있음.',
'mapping':'연구 파이프라인의 빠른 투입지표, 사전 노출×신호/시행 구간, 기초연구비·예측 수요 교란 점검이 유용함.',
'nontransfer':'입법 후 측정 비중, 부분실행이 있는 anticipatory 창, 의약수요 확대의 부호를 본 연구의 2013–17 B·China-binding 이전창에 그대로 옮길 수 없음.',
'locators':[
 {'claim':'노출의2004–05 측정','printed_pages':None,'pdf_pages':None,'section':'2.2','html_anchor':'#S4'},
 {'claim':'표본·보고누락·자료기간','printed_pages':None,'pdf_pages':None,'section':'2.1'},
 {'claim':'기대시장·NIH 통제','printed_pages':None,'pdf_pages':None,'section':'2.3–2.4','equations':['1']},
 {'claim':'시기별회귀·추론','printed_pages':None,'pdf_pages':None,'section':'3.2','equations':['3'],'tables':['2','3']},
 {'claim':'부분혜택·판본','printed_pages':None,'pdf_pages':None,'section':'Footnotes','html_anchors':['#FN7','#FN8']}],
'open_issues':['PMC 식(3) m벡터 첫 행은 Year>2003인데 나머지 2004–05·2006–07·2008–10 더미와 중복됨. 본문은2003년 별도 반응을 말하고 Tables2–3도2003행을 보고함. 본 표는 후자의 시기별 비교 구조를 기술했으며 표기오류를 임의 교정하거나 정확설계를 재현했다고 주장하지 않음. 출판본/replication code 대조 필요.'],
'assessment':'발표/시행 분기와 연속 노출의 가까운 선례이나 순수신호창 및 엄격한 정책이전 노출의 선례는 아님.'
},
{
'id':'moser2012',
'citation':'Moser, Petra, and Alessandra Voena (2012), Compulsory Licensing: Evidence from the Trading with the Enemy Act, AER 102(1), 396–427.',
'doi':'10.1257/aer.102.1.396',
'primary_url':'https://www.petramoser.net/uploads/6/9/4/2/69429445/moservoena12_aer.pdf',
'version':'저자 공개 출판본. 본문 인쇄 p = PDF p +395; 공개파일38쪽 중 학술지 본문은32쪽. 뒤의6쪽을 본문 인쇄쪽으로 계산하지 않음.',
'read_scope':'§II.A, §III 도입·강도 확장, §III.D 및 서론의 시점·선택 논의. 인쇄pp.397–401·404·406·413–414 / PDFpp.2–6·9·11·18–19 중심. 전체 부록 재현 없음.',
'unit_outcome':'USPTO 화학 subclass×연도, 미국 발명자에게 부여된 특허 건수, 1875–1939. 19개 main class·7,248 subclass 중336개 실제 라이선스 노출. 특허 부여시점을 연구투입·출원시점과 구분.',
'exposure':'적어도1개 라이선스 수령 여부, 실제 라이선스 특허 수, 그 특허들의 합산 잔여권리기간. 선택적 실제 이용량임. 별도 ITT는 라이선스 가능 적국특허 수, IV는 그 가용량으로 실제 이용량을 도구화.',
'event_dates':'1917-10-06 TWEA 통과, 1918년 휴전 전후 몰수권 확대, 1919년 라이선스 개시. 실증 postTWEA=1918년 이후. 라이선스는1919–26, 대부분1919–22; 정확한 개별 라이선스 날짜는 불가용이라고 명시.',
'counterfactual':'§III의 무번호식: Patents_ct = α0+β′TREAT_c×post_t+γZ_ct+연도FE+subclassFE+ε_ct. 미수령 subclass와 수령 subclass 변화 비교; Z는 외국인특허. §III.D의 무번호 ITT·2단계식으로 가용 특허와 선택 이용량을 분리.',
'assumptions':'미국기업의 실제 라이선스 선택 내생성을 저자가 인정. 산업 공통·subclass 고정요인 외 차등충격이 없어야 함. IV는 관련성뿐 아니라 가용 적국특허가 실제 라이선스 외 경로로 미국 발명을 늘리지 않는 배제제약 필요. 외국인특허 통제가 모든 기술충격을 없애지는 않음.',
'announcement_implementation':'분석대상은 실제 접근 허용 이후 효과이며1917법률발표와1919이용 전 창을 분리하지 않음. 연도별 특허 부여 반응의 시차는 있음.',
'mapping':'기술군 비교, 가용자원과 실제선택 분리, 강도·잔여가치의 구분, 외국 발명자 placebo가 유용함.',
'nontransfer':'사후 라이선스 수를 사전 위협 B와 동일시할 수 없음. 접근을 열어준 학습효과를 접근차단 전 기대효과로 전이할 수 없음. 적국특허 IV의 배제제약도 미국특허인용·수입비중 도구에 승계되지 않음.',
'locators':[
 {'claim':'정책 및 특허부여 자료','printed_pages':'397–398','pdf_pages':[2,3],'section':'Introduction'},
 {'claim':'라이선스 시점의 한계','printed_pages':'401','pdf_pages':[6],'section':'II.A'},
 {'claim':'기본식·강도','printed_pages':'404,406','pdf_pages':[9,11],'section':'III','equations':['unnumbered baseline']},
 {'claim':'선택·ITT·IV·배제제약','printed_pages':'413–414','pdf_pages':[18,19],'section':'III.D','equations':['unnumbered ITT','unnumbered first and second stage']}],
'open_issues':[],
'assessment':'실제 접근 확대 및 선택적 강도의 선례; 제한 전 발표효과의 직접 선례는 아님.'
},
{
'id':'finkelstein2004',
'citation':'Finkelstein, Amy (2004), Static and Dynamic Effects of Health Policy: Evidence from the Vaccine Industry, Quarterly Journal of Economics 119(2), 527–564.',
'doi':'10.1162/0033553041382166',
'primary_url':'https://economics.mit.edu/sites/default/files/2022-08/Static%20and%20Dynamic%20Effects%20of%20Health%20Policy-Eviden.pdf',
'version':'MIT 저자 페이지의 학술지 출판본. 인쇄 p = PDF p+526. NBER w9460 초기판과 혼합하지 않음.',
'read_scope':'§II–III의 정책선정·식(1)·비교군, §IV의식(2)·pretrend 해석 및 Appendix1 정책 시점. 인쇄pp.535–540·543–545·558–560 / PDFpp.9–14·17–19·32–34. 전체 후생계산 재현 없음.',
'unit_outcome':'질병×연도별 새 백신 임상시험 건수(1983–99)가 주결과. 전임상·특허·승인은 별도 단계 지표. 여섯 영향 질병군의 기존 백신 개선 유인에 대한 분석.',
'exposure':'주처치는 질병별 정책 적용 ADOPT(이진값). 미국의 HepB 권고, flu 보장, VICF liability 감소. 연속 사전 위협량의 주회귀가 아님; 기대수입으로 환산한 보완분석은 별도.',
'event_dates':'HepB 보편영아접종권고1991, Medicare flu 보장1993년5월, VICF 1986 발표·1988 시행. p537 각주5: 첫 완전 노출연도를 쓰되 VICF는 기대가 알려진 1987부터 ADOPT. flu/HepB도 달력연도와 최초완전노출연도 구분.',
'counterfactual':'식(1): Newtrials_it=α_i+γ_t+λADOPT_it+ε_it. 비대상 질병군의 같은 기간 변화와 비교. 대안대조군은 전체임상26, 초기임상7, 기존승인7, 기술잠재력9개 질병. 식(2)는정책 상대기간 구간화, 기준은정책 전 1–3년.',
'assumptions':'정책이 기술 기회 확대에 반응해 도입되지 않아야 하고, 정책이 없었다면 질병별 임상 추세가 비교 가능해야 함. 대상 질병 증가가 대조 질병 연구를 밀어내면 비교가 오염됨. 저자는pretrend·질적정책경위를 근거로 논의하며, 무작위성의 증명은 아님.',
'announcement_implementation':'VICF의 발표/시행 차이는 인식하나1987 이후를 하나의 노출로 포함. 시행 추가효과와 기대효과를 별개로 추정하지 않음. 저자의 ‘정책전 무기대’ 논의는 발표/채택 이전을 뜻하며 시행 이전무기대와 동일하지 않음.',
'mapping':'질병/기술별 비교군의 잠재력 정합성, R&D단계별 지연, crowd-out 점검을 옮길 수 있음.',
'nontransfer':'의약산업 자금·피험자 공급이 충분해 crowd-out이 작다는 판단은 중국 연구자·자본 재배분 연구에 자동 전이 불가. 기대를 포함한 ADOPT를 순수 발표효과 계수라 부를 수 없음.',
'locators':[
 {'claim':'정책과내생성','printed_pages':'535–536','pdf_pages':[9,10],'section':'II'},
 {'claim':'기본식·VICF 예외','printed_pages':'537','pdf_pages':[11],'section':'III.B','equations':['1'],'footnotes':['5']},
 {'claim':'비교군·crowd-out','printed_pages':'539–540','pdf_pages':[13,14],'section':'III.B'},
 {'claim':'동학·가정','printed_pages':'543–545','pdf_pages':[17,18,19],'section':'IV','equations':['2'],'figures':['III']},
 {'claim':'세부정책 시점·정보','printed_pages':'558–560','pdf_pages':[32,33,34],'section':'Appendix 1'}],
'open_issues':[],
'assessment':'기대이익과 연구 파이프라인의 직접 선례; 발표/시행 별도계수나 연속dose의 직접 선례는 아님.'
},
{
'id':'malani2015',
'citation':'Malani, Anup, and Julian Reif (2015), Interpreting pre-trends as anticipation: Impact on estimated treatment effects from tort reform, Journal of Public Economics 124, 1–17.',
'doi':'10.1016/j.jpubeco.2015.01.001',
'primary_url':'https://julianreif.com/research/reif.jpube.2015.anticipation.pdf',
'version':'저자 공개 2015-02-09 원고 50쪽. 원고 인쇄번호=PDF쪽수; 학술지 1–17쪽과 일치하지 않음. 출판판본과 식번호·문언의 완전 동일성은 미대조.',
'read_scope':'원고 §1·§2.2–2.3·§3.1과§4.1–4.4 중심, 식(1),(4)–(8),(9)–(11), pp.6·11–17·19–29. 원고 조건·응용을 읽었으나 모든 proof/Appendix 재현은 하지 않음.',
'unit_outcome':'1980–2001년 주×의사 전문과목×연도별 인구당 의사수 로그. 징벌적 손해배상 상한은 주×연도 이진처치. 전체 산업 대상 개혁을 주분석에 쓰고 의료전용 대상 주는 보완 제외.',
'exposure':'현재 상한 d_st, 미래 최초채택 더미 D_s,t+j, 혹은 미래 의사공급을 포함한 기대모형. 예측치와 실현치를 구별하는 방법론이며 연속 사전노출 기울기를 추정하지 않음.',
'event_dates':'표본의 채택은 1984–98년에 분산. 공통 공식 정보충격일은 없음. 예: PA 1997-01-25 채택, 1993–96 신문 논의는 예견 가능성의 보조증거. 기본 moving-window는 논문이 정의한 채택 전 5년과 이후 4년의 9년창.',
'counterfactual':'채택주와 미채택주의 내부변화 비교, 주×전문과목·전문과목×연도 FE, 선택 명세의 주추세. 식(1): y_t=λ0d_t+Σ_j≥1 λ_j E_t[d_t+j]+e_t. 응용 식(10)은 유한 lead 더미, 식(11)은 y_ist=θy_is,t+1+βd_st+δd_s,t+1+FE/추세+w.',
'assumptions':'개혁 채택의 외생성은 별도 핵심가정. 유한 lead 모형은 완전예견과 S기 이후 기대효과 부재를 가정. 지수모형은 기대형성·할인함수·오차/예측오차 직교조건이 필요. outcome lead/lag IV에는 제한적 시계열상관·말기조건·배제제약이 필요하며 일반적으로 유효하지 않음.',
'announcement_implementation':'시행 전 반응이 예견과 일치할 수 있음을 보이지만 pretrend 자체로 예견을 입증하지 않는다고 명시. 시행 후 효과에도 미래 정책 지속 기대가 들어가므로 전부를 현재 실행효과로 읽을 수 없음. 실제 정책신호의 날짜별 감축형 효과와 동일한 estimand는 아님.',
'mapping':'신호 전 내생추세와 신호 후 기대반응의 구별, 기대를 포함한 총효과와 현재 시행 추가효과의 구별이 핵심.',
'nontransfer':'미국 개혁의 광범위 적용 논거는 선택적으로 지목된 중국 기술의 외생성을 보장하지 않음. 연구역량의 관성·반복신호에서는 outcome lead IV가 배제제약을 위반할 수 있어 그대로 차용 불가. 관측 신호일이 있다면 해당 신호와 제한일로 창을 명시해야 함.',
'locators':[
 {'claim':'기대모형·효과정의','printed_pages':'원고6–8','pdf_pages':[6,7,8],'section':'1','equations':['1']},
 {'claim':'할인·기대·오차조건','printed_pages':'원고11–17','pdf_pages':[11,12,15,16,17],'section':'2.2–3.1','equations':['4','5','6','7','8']},
 {'claim':'lead IV 반례','printed_pages':'원고19','pdf_pages':[19],'section':'3.2'},
 {'claim':'외생성·예견보조증거·시점','printed_pages':'원고22–27','pdf_pages':[22,23,24,25,26,27],'section':'4.3–4.4'},
 {'claim':'응용식과가정','printed_pages':'원고28–29','pdf_pages':[28,29],'section':'4.4','equations':['9','10','11']}],
'open_issues':['출판본 전문과의 판본 대조는 미실시. 모든 식/쪽수는 명시한 2015-02-09 저자원고에만 귀속.'],
'assessment':'예견을 허용하는 효과정의의 핵심 선례. pretrend의 인과적 면책이나 신호처치 외생성의 증거는 아님.'
}
]
for r in rows:
 r['status']='producer_primary_read_completed'
 r['independent_verification_status']='pending'
 r['producer_agent']='/root/nov13_precedent_completion'
 r['interpretation_note']='원문서술의요약과본연구전이판단은구별함. assumptions와nontransfer에는생산자의식별논리해석이포함됨.'
result={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'배정된미완료선례5편만보완. 기존Pierce–Schott/CGBS표를대체하거나검증완료로상향하지않음.','review_status':'independent_verification_and_referee_pending','rows':rows}
(BASE/'precedents.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# 미완료 방법론 선례 5편: 원문 보완표','',
'작성자: `/root/nov13_precedent_completion` (producer/lit_scout). 2026-11-13. **생산 완료, 독립 검증·referee 대기**. 기존 선례표·queue·Gate·원고는 수정하지 않았다. 원문 접근이나 핵심절 독해의 완료를 독립 검증 또는 전체 증명·부록 재현으로 표시하지 않는다.','',
'공통 결론: 연속 노출×시기 상호작용은 실험 배정이 아니다. 사전 지표 고정은 역인과를 줄이지만 정책 선택·기술별 동시충격을 제거하지 않는다. 본 연구의 목표는 사전 B_k에 따른 **실제 China-binding 제한 이전** 공식신호의 차등반응이다. 여기에 필요한 기술별 창·조건부 반사실·대조군 무오염은 각 선례에서 새로 충족해야 한다.','',
'아래 식은 식별구조를 읽기 위한 요약이다. 원문 기호·상세함수·추정코드를 완전히 전사한 재현 명세가 아니다. PDF쪽수는1부터 세고, 인쇄쪽수와 별도 표시한다. HTML에 PDF쪽수를 부여하지 않는다.','',
'| 논문 | 비교에서 얻는 것 | 발표/시행 분리의 한계 |','|---|---|---|']
for r in rows: md.append('| '+r['citation'].split('(')[0].strip()+' | '+r['assessment']+' | '+r['announcement_implementation']+' |')
for i,r in enumerate(rows,1):
 md += ['',f"## {i}. {r['id']}",'',r['citation']+f" [원문]({r['primary_url']}) · [출판서지](https://doi.org/{r['doi']})",'', '| 확인 항목 | 원문에서 확인한 내용과 전이 판단 |','|---|---|']
 for label,key in [('판본·쪽수','version'),('직접 확인 범위','read_scope'),('단위·결과','unit_outcome'),('처치·노출 측정시점','exposure'),('정보·실행 시점','event_dates'),('식·비교군·반사실','counterfactual'),('핵심 식별가정','assumptions'),('본 연구에 대응 가능한 부분','mapping'),('전이할 수 없는 부분','nontransfer')]:md.append('| '+label+' | '+r[key].replace('|','\\|')+' |')
 md += ['', '**원문 locator**','', '| 주장 | 인쇄쪽수 | 공개 PDF쪽수 | 절·식·표 |','|---|---|---|---|']
 for l in r['locators']:
  detail=l.get('section','')
  for k in ['equations','tables','figures','footnotes','html_anchors']:
   if l.get(k):detail+='; '+k+': '+', '.join(l[k])
  md.append('| '+l['claim']+' | '+str(l['printed_pages'] or '미부여/미확인')+' | '+(', '.join(map(str,l['pdf_pages'])) if l['pdf_pages'] else 'HTML, PDF 미확인')+' | '+detail+' |')
 if r['open_issues']:md+=['','**열린 한계**: '+' '.join(r['open_issues'])]
md += ['', '## 검토 수령과 범위','',
'5편 모두 직접 원문에서 핵심 식·노출·비교·시점을 확인했다. Handley/Moser/Finkelstein은 공개 출판본, Malani는 날짜가 표시된 저자원고, Blume는 NIH 공개 accepted manuscript다. Blume 식(3) 표기의 모순과 부분혜택, Malani 판본 차이는 남겨 두었다. 이를 “정확한 코드 재현 5/5” 또는 “독립검증 5/5”로 집계하면 안 된다. 원문파일의SHA256·다운로드실패·독해범위는 [source_manifest.json](source_manifest.json), 구조화 표는 [precedents.json](precedents.json)에 있다.','',
'독립 검증자는 특히 (i) Finkelstein p537 fn5의1987 coding, (ii) Blume §§2.2·3.2·각주7과식(3) 모순, (iii) Moser p414의IV배제제약, (iv) Malani 원고p29의응용식과가정을 다시 확인해야 한다. 그 전까지 어떤행도 verified로 올리지 않는다.']
(BASE/'precedents.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
manifest=json.loads((BASE/'source_manifest.json').read_text(encoding='utf-8'))
for r in rows:
 rec=next((x for x in manifest['sources'] if x['id']==r['id']),None)
 if not rec:
  rec={'id':r['id'],'url':r['primary_url'],'acquisition':'copied_existing_primary_cache','original_local_path':'work/stage3/blume2013.html','path':str(SRC/'blume2013.html'),'pdf_pages':None};manifest['sources'].append(rec)
 rec.update({'version':r['version'],'read_scope':r['read_scope'],'locators':r['locators'],'full_proof_appendix_reproduction':False,'independent_verification_status':'pending','sha256':hashlib.sha256(Path(rec['path']).read_bytes()).hexdigest()})
 if r['id']=='blume2013':
  rec['access_attempts']=[{'url':'https://pmc.ncbi.nlm.nih.gov/articles/PMC3711884/pdf/nihms419385.pdf','http_status':200,'body_type':'text/html challenge; not PDF','accepted_as_source_pdf':False},{'url':'https://europepmc.org/articles/PMC3711884?pdf=render','http_status':403,'accepted_as_source_pdf':False}]
  rec['open_issues']=r['open_issues']
 manifest['source_extraction_code']='extract_sources.py'
 manifest['table_generation_code']='build_precedents.py'
 manifest['scope']='author/publisher/NIH primary fulltexts; core identification pages actually read; not all appendices/proofs'
manifest['artifacts']=[{'path':str(BASE/name),'sha256':hashlib.sha256((BASE/name).read_bytes()).hexdigest()} for name in ['precedents.md','precedents.json','extract_sources.py','build_precedents.py']]
(BASE/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Wrote',len(rows),'rows; all independent verification pending')
