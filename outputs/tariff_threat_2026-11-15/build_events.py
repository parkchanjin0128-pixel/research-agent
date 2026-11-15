"""사건 패널 v1 (가격 열람 전 고정). 시각 출처: American Presidency Project(APP)의 Truth Social 일별 기록
(페이지 주석 "Posting times are in Pacific time") → ET = PT + 3h. 날짜·결과 출처: PPAI/Thorn Run 'Tracking Tariffs
During Trump 2.0 — Summer 2026 Update'(PPAI), Reuters 연표(RTE 2026-02-23 게재본, REU)."""
import csv, hashlib
APP="https://www.presidency.ucsb.edu/documents/truth-social-posts-"
H=["id","tier","date","time_pt","time_et","weekday_note","type","target","fx","rate","deadline","text","ts_source","prior_viewed",
   "outcome","outcome_date","outcome_basis"]
R=[]
def a(*x): R.append(dict(zip(H,x)))
# ---- Tier A: 게시 시각 확인 (ESC=강화 위협/발표, DEESC=완화)
a("E01","A","2025-01-26","10:28","13:28","일요일(FX 휴장)","ESC","Colombia","","25→50%","","콜롬비아 전 수입품 25%, 1주 뒤 50%",APP+"january-26-2025","0","NOT_EXECUTED","2025-01-26","당일 철회(백악관 성명; 날짜는 일반 보도, 원문 미확인)")
a("E02","A","2025-02-27","05:46","08:46","","ESC","Mexico;Canada;China","USDMXN;USDCAD;USDCNH","25%;25%;+10%","2025-03-04","3/4 관세 예정대로, 중국 +10%",APP+"february-27-2025","0","EXECUTED","2025-03-04","PPAI,REU")
a("E03","A","2025-03-11","07:15","10:15","","ESC","Canada steel/aluminum","USDCAD","50%","2025-03-12","캐나다 철강·알루미늄 50%",APP+"march-11-2025","0","NOT_EXECUTED","2025-03-11","PPAI(당일 번복; 원자료 날짜 표기 05-11은 오기로 판단)")
a("E04","A","2025-03-13","04:58","07:58","","ESC","EU wine/spirits","EURUSD","200%","","EU 주류 200% 위협",APP+"march-13-2025","0","NOT_EXECUTED","2025-06-11","90일 규칙(시행 기록 없음)")
a("E05","A","2025-03-24","07:37","10:37","","ESC","Buyers of Venezuelan oil","","25%","2025-04-02","베네수엘라산 원유 구매국 25%",APP+"march-24-2025","0","NOT_EXECUTED","2025-04-02","PPAI(never imposed)")
a("E06","A","2025-04-07","08:14","11:14","","ESC","China","USDCNH","+50%","2025-04-09","중국이 4/8까지 철회 안 하면 +50%",APP+"april-7-2025","0","EXECUTED","2025-04-09","REU(104%→125%)")
a("E07","A","2025-04-09","10:18","13:18","","ESC","China","USDCNH","125%","2025-04-09","중국 125%로 인상(같은 게시물에 타국 90일 유예)",APP+"april-9-2025","0","EXECUTED","2025-04-09","REU")
a("E08","A","2025-05-04","16:18","19:18","일요일","ESC","Foreign films","","100%","","외국 제작 영화 100%",APP+"may-4-2025","0","NOT_EXECUTED","2025-08-02","90일 규칙(시행 기록 없음)")
a("E09","A","2025-05-23","04:43","07:43","","ESC","EU","EURUSD","50%","2025-06-01","EU 50%, 6/1부터 (04:19 PT 애플 25% 게시 직후)",APP+"may-23-2025","0","NOT_EXECUTED","2025-05-25","PPAI(7/9로 연기 후 15% 합의)")
a("E10","A","2025-05-30","16:16","19:16","금요일 장후","ESC","Steel/aluminum","","50%","2025-06-04","철강·알루미늄 50%, 6/4부터",APP+"may-30-2025","0","EXECUTED","2025-06-04","PPAI,REU")
a("E11","A","2025-07-09","17:29","20:29","","ESC","Copper","","50%","2025-08-01","구리 50%, 8/1부터",APP+"july-9-2025","0","EXECUTED_PARTIAL","2025-08-01","PPAI(품목별 차등 시행)")
a("E12","A","2025-07-30","05:09","08:09","","ESC","India","USDINR","25%+penalty","2025-08-01","인도 25%+벌칙, 8/1부터",APP+"july-30-2025","0","EXECUTED","2025-08-07","REU(8/6 추가 25% 명령, 8/7 발효)")
a("E13","A","2025-08-25","17:31","20:31","","ESC","Digital-tax countries","","","","디지털세 국가 추가 관세·칩 수출 제한 위협",APP+"august-25-2025","0","NOT_EXECUTED","2025-11-23","90일 규칙(시행 기록 없음)")
a("E14a","A","2025-09-25","15:51","18:51","","ESC","Heavy trucks","","25%","2025-10-01","대형 트럭 25%, 10/1부터",APP+"september-25-2025","0","NOT_EXECUTED","2025-10-01","PPAI(11/1로 연기 후 시행)")
a("E14b","A","2025-09-25","16:24","19:24","","ESC","Branded pharmaceuticals","","100%","2025-10-01","브랜드 의약품 100%, 10/1부터",APP+"september-25-2025","0","NOT_EXECUTED","2025-10-01","PPAI(보류; 2026-07-31 별도 시행)")
a("E15","A","2025-10-10","07:57","10:57","","ESC","China","USDCNH","대폭 인상","","대중 관세 대폭 인상 검토(선행 위협)",APP+"october-10-2025","1","NOT_EXECUTED","2025-11-01","PPAI(1년 연기)")
a("E15b","A","2025-10-10","13:50","16:50","장후","ESC","China","USDCNH","+100%","2025-11-01","11/1부터 +100%와 핵심 소프트웨어 통제",APP+"october-10-2025","1","NOT_EXECUTED","2025-11-01","PPAI(1년 연기)")
a("E16","A","2025-10-25","13:30","16:30","토요일","ESC","Canada","USDCAD","+10%","","캐나다 +10% (광고 문제)",APP+"october-25-2025","0","NOT_EXECUTED","2026-01-23","PPAI(mechanism unclear), 90일 규칙")
a("E17","A","2025-12-08","14:55","17:55","","ESC","Mexico","USDMXN","5%","","멕시코 5% (물 조약)",APP+"december-8-2025","0","NOT_EXECUTED","2025-12-12","PPAI(분쟁 해결로 철회)")
a("E18","A","2026-01-17","08:19","11:19","토요일","ESC","Denmark+7 European","EURUSD","10→25%","2026-02-01","그린란드 관련 유럽 8개국 10%, 이후 25%",APP+"january-17-2026","0","NOT_EXECUTED","2026-01-21","APP 2026-01-21 게시물(철회)")
a("E19","A","2026-02-21","7:59 AM(표기 형식 변경, 시간대 재확인 필요)","","토요일","ESC","Global","","10→15%","","전 세계 관세 10%→15%",APP+"february-21-2026","0","NOT_EXECUTED","2026-07-24","PPAI(no orders issued; 122조 만료)")
a("D01a","A","2025-02-03","07:41","10:41","","DEESC","Mexico","USDMXN","","","멕시코 관세 1개월 유예",APP+"february-3-2025","0","","","")
a("D01b","A","2025-02-03","13:57","16:57","","DEESC","Canada","USDCAD","","","캐나다 관세 30일 유예",APP+"february-3-2025","0","","","")
a("D02","A","2025-03-06","08:29","11:29","","DEESC","Mexico","USDMXN","","","멕시코 USMCA 품목 4/2까지 면제",APP+"march-6-2025","0","","","")
a("D03","A","2025-04-09","10:18","13:18","","DEESC","All except China","EURUSD;USDJPY;USDMXN;USDCAD","10%","","상호관세 90일 유예(같은 게시물에 중국 125%)",APP+"april-9-2025","0","","","")
a("D04","A","2025-05-25","15:15","18:15","일요일","DEESC","EU","EURUSD","","2025-07-09","EU 50% 시한 7/9로 연기",APP+"may-25-2025","0","","","")
a("D05","A","2025-06-11","05:04","08:04","","DEESC","China","USDCNH","","","미중 합의 완료 발표",APP+"june-11-2025","0","","","")
a("D06","A","2025-07-30","15:16","18:16","","DEESC","South Korea","","15%","","한국과 15% 합의",APP+"july-30-2025","0","","","")
a("D07","A","2025-10-12","09:43","12:43","일요일","DEESC","China","USDCNH","","","대중 완화성 게시",APP+"october-12-2025","1","","","")
a("D08","A","2026-01-21","11:27","14:27","","DEESC","Denmark+7 European","EURUSD","","","그린란드 관세 철회",APP+"january-21-2026","0","","","")
# ---- Tier B: 날짜만 확인 (시각 미확인 → 일별 창)
B=[("B01","2025-02-01","ESC","Mexico;Canada;China","USDMXN;USDCAD;USDCNH","25%;25%;10%","2025-02-04","행정명령(토요일)","EXECUTED_PARTIAL","2025-02-04","PPAI(중국만 발효, 멕·캐 유예)"),
("B02","2025-02-18","ESC","Autos; semis; pharma","","~25%","","발언","EXECUTED_PARTIAL","2025-04-03","PPAI(자동차만 4/3 발효)"),
("B03","2025-02-26","ESC","EU","EURUSD","25%","","발언","NOT_EXECUTED","2025-04-02","PPAI(4/2 상호관세 20%로 대체)"),
("B04","2025-03-26","ESC","Autos","","25%","2025-04-03","포고문","EXECUTED","2025-04-03","PPAI"),
("B05","2025-04-02","ESC","Global reciprocal","EURUSD;USDJPY;USDCNH","10%+","2025-04-09","로즈가든 발표(장 마감 후로 알려짐; 시각 미확인)","NOT_EXECUTED","2025-04-09","REU(발효 24시간 내 유예)"),
("B06","2025-07-07","ESC","14 countries incl. Japan, Korea","USDJPY","25–40%","2025-08-01","서한(이미지 게시라 시각 미확인)","EXECUTED_PARTIAL","2025-08-07","REU(다수 합의로 인하)"),
("B07","2025-07-08","ESC","Pharmaceuticals","","200%","","각료회의 발언","NOT_EXECUTED","2025-10-06","90일 규칙"),
("B08","2025-07-10","ESC","Canada","USDCAD","35%","2025-08-01","서한","EXECUTED","2025-08-01","PPAI"),
("B09","2025-07-12","ESC","Mexico;EU","USDMXN;EURUSD","30%","2025-08-01","서한(토요일)","NOT_EXECUTED","2025-07-31","PPAI(멕시코 90일 연기, EU 15% 합의)"),
("B10","2025-08-06","ESC","Semiconductors","","100%","","발언","NOT_EXECUTED","2025-11-04","90일 규칙(2026-01 일부 품목 25%)"),
("B11","2026-01-31","ESC","Canada","USDCAD","50%","","위협(게시물 텍스트 미확인)","NOT_EXECUTED","2026-05-01","90일 규칙; 2026-07 별도 338조 조치"),
("B12","2026-05-01","ESC","EU trucks","EURUSD","25%","","위협","UNRESOLVED","","PPAI"),
("B13","2025-05-12","DEESC","China","USDCNH","145→30%","","제네바 합의","","",""),
("B14","2025-07-27","DEESC","EU","EURUSD","15%","","미·EU 합의(일요일)","","",""),
("B15","2025-08-11","DEESC","China","USDCNH","","2025-11-10","휴전 90일 연장","","",""),
("B16","2025-10-30","DEESC","China","USDCNH","펜타닐 10%","","부산 합의","","","")]
for b in B: a(b[0],"B",b[1],"","","",b[2],b[3],b[4],b[5],b[6],b[7],"PPAI/REU","1" if b[1] in("2025-02-18","2025-08-06") else "0",b[8],b[9],b[10])
# ---- IMPL: 예정된 발효 시각(00:01 ET). 발효 자체가 '실행 확인' 정보인지 본다.
I=[("I01","2025-02-04","China 10%","USDCNH"),("I02","2025-03-04","Canada/Mexico 25%, China +10%","USDCAD;USDMXN;USDCNH"),
("I03","2025-03-12","Steel/aluminum 25%",""),("I04","2025-04-03","Autos 25%","USDJPY;EURUSD"),("I05","2025-04-09","Reciprocal country rates","EURUSD;USDJPY;USDCNH"),
("I06","2025-06-04","Steel/aluminum 50%",""),("I07","2025-08-01","Canada 35%; copper","USDCAD"),("I08","2025-08-07","Reciprocal rates on dozens of partners","EURUSD;USDJPY;USDINR"),
("I09","2025-10-14","Lumber 10%; China port fees","USDCAD;USDCNH"),("I10","2026-02-24","Section 122 global 10%","EURUSD;USDJPY"),("I11","2026-07-24","Section 301 forced-labor 10–12.5%","USDCAD;USDCNH")]
for i in I: a(i[0],"A","%s"%i[1],"21:01(전일)","00:01","예정 발효","IMPL",i[2],i[3],"","","발효 시각 00:01 ET(관보·명령상 통상 시각; 건별 재확인 필요)","PPAI/REU","0","","","")
with open("events_v1.csv","w",newline="",encoding="utf-8-sig") as f:
    w=csv.DictWriter(f,fieldnames=H); w.writeheader(); w.writerows(R)
print(len(R), {t:sum(r["type"]==t for r in R) for t in("ESC","DEESC","IMPL")}, "tierA", sum(r["tier"]=="A" for r in R))
esc=[r for r in R if r["type"]=="ESC"]
print("ESC outcomes", {o:sum(r["outcome"]==o for r in esc) for o in set(r["outcome"] for r in esc)})
print("sha256", hashlib.sha256(open("events_v1.csv","rb").read()).hexdigest())
