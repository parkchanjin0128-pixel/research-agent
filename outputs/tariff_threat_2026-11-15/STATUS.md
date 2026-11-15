# STATUS (갱신: 2차 실행, 2026-11-15 04시대 KST)

## 완료
- 레포 최신화(커밋 2dee771). `trump2/` 올라옴(시간별 OHLC, 후보 결과, 스크립트). **`data_raw/` 는 아직 없음.**
- 선행연구 확인:
  - Kalemli-Özcan, Soylu & Yildirim (NBER WP 34728): TiRADE(319개 시각 확인 사건→177 묶음), Bloomberg 분 단위, 창 15/30/60/120/240분, EUR/USD·ES·금리차. 위협 대 시행 구분 분석·시간에 따른 반응 변화·신뢰도 학습 검정 없음. 예측시장 미사용. 자료 공개 링크는 확인된 범위에서 없음(마지막 20k자 미열람).
  - Merendino & Monacelli (2026, Economic Policy 게재예정): 분기 BVAR + 관세 지속성에 대한 베이즈 학습 모형(S-TPU). 사건 단위 검정 아님. 이론적 근거로 인용 가능.
  - Lin, Sun & Yan (arXiv 2608.30522): LLM 에이전트 설문 실험, 시장가격 아님.
  → "미실행 기록에 따른 반응 감소 + 발효 시점 반응 증가 + 예측시장" 조합은 확인한 범위에서 비어 있음.
- 사건 패널 v1: `events_v1.csv` (57건: ESC 33, DEESC 13, IMPL 11; Tier A 41). ESC 결과: EXECUTED 7, PARTIAL 4, NOT_EXECUTED 21, UNRESOLVED 1. 생성 스크립트 `build_events.py`.
- 사전 분석 계획: `PAP_v1.md` (events 해시 포함).

## 미완료 / 다음 실행(2차)이 할 일
1. `git fetch` 후 `data_raw/` 확인. 있으면 디코딩(Yahoo JSON, Dukascopy .bi5 — LZMA, 레코드 구조·스케일을 알려진 환율 수준으로 검증), 결측일 목록.
2. 예측시장: 관세 계약 목록 → 사건 대응표를 가격 보기 전에 고정.
3. PAP 5절대로 MDE 먼저 계산·기록 → 사건별 반응 → placebo → 회귀 → 강건성. 스크립트화.
4. data_raw 가 없으면: 추정 코드 작성 + 합성 자료 검증, PMCCF/OMT 등 도입부 사실관계 원문 확인, 실패 설계 그림 재료(레포 `outputs/final_research/empirics/fake_event_windows.csv`, `outputs/identification_rescue_2026-11-12/`) 정리.
5. 사건 패널 보완 후보(토큰 여유 시, v2로): E19 시간대, IMPL 발효 시각 건별 확인, 2025-07 서한 시각, 2026년 사건(이란 거래국 관세 위협 등) 추가.

## 주의
- IEEPA 관세는 2026-02-20 대법원 판결로 무효(PPAI). 그 뒤 122조 10%(7/24 만료)→301조. 결과 코딩 규칙 3)에 따라 원 위협의 결과는 바꾸지 않았다.
- 10/10 분석의 원자료·코드는 `trump2/hourly_prices.csv`, `hourly_analysis.py` 에 있어 발표용 그림을 원자료로 다시 그릴 수 있다.

---
## 2차 실행(04:21) 추가
### 완료
- 레포 재확인: 커밋 2dee771 그대로. **`data_raw/` 여전히 없음** → 실제 가격으로는 아무것도 추정하지 않았다.
- `pipeline.py`: 디코더(Dukascopy .bi5 열 순서·스케일 자동 판별, Yahoo JSON), 신뢰도 변수, 사건 반응(시장 전체 + 대상 통화, 휴장 처리, 같은 요일·시각 placebo), 기울기 회귀(HC3, wild bootstrap, 순열), 수준·대비 검정(T1–T4), 강건성 14종. `python pipeline.py selftest` 통과(약 20초).
- 자체 점검에서 나온 설계 수정 → `PAP_v1.md` 의 "v1.1 추가" 절(가격 열람 전): 결과 변수에 시장 전체 반응 추가, 주 검정을 수준·대비 검정으로 변경, 기울기 회귀는 보조.
- 가격 없이 확인된 사실: 과거 위협의 실행률(C_all)은 0.50 → 0.31 사이에서 움직이고 2025년 내내 0.40–0.46 근처다. 단조 하락이 아니다. `fig/cred_path.pdf`.
- 도입부 사실관계: `notes_intro_facts.md` (PMCCF·SMCCF, Haddad–Moreira–Muir 원문 확인).

### 3차 실행이 할 일 (순서대로)
1. `git fetch` → `data_raw/` 있으면: `python pipeline.py decode <레포>/data_raw` → `work/decode_report.json` 에서 환율 수준(fx_levels)이 상식적인지 확인(예: USDCNH≈7.1–7.3, USDJPY≈140–160) → `python pipeline.py run`.
   - MDE·사건 수를 먼저 기록하고 결과를 본다. T1–T4가 주 결과.
   - 예측시장: polymarket/events.jsonl.gz 에서 시한이 있는 위협(E09 EU 6/1, E15b 중국 11/1, E18 그린란드 2/1, B05 등)에 대응하는 계약을 문구로 먼저 고르고 나서 가격을 본다.
   - Tier B 일별 반응은 yahoo.parquet 의 1d 로 간단히.
2. `data_raw/` 가 없으면: 추정 없이 논문·발표자료를 "설계 + 사건 자료 + 실행률 사실 + 이전 설계의 실패 + 10/10 재분석(trump2 원자료)" 로 쓰고, 결과 절은 비워 둔 채 무엇이 필요한지 명시한다. 수치를 만들지 않는다.
3. 그림: 10/10 시간별 경로는 `trump2/hourly_prices.csv`(09:30–15:30 bar의 open/close) 로 원자료에서 다시 그린다. 실패 설계 그림은 논문에 적힌 수치(의존도 범위 0.303–0.538 대 0.018–0.134, 가짜 창 −1.133/−1.322/−1.101/−0.214 대 실제 −0.359)와 원본 월별 그림(fig4_theta_orig.png)을 쓴다.
4. 논문·발표자료 작성 지침은 3차 예약 지시문과 사용자 요청(발표 30–40분, 실패 과정의 스토리, PMCCF 등 발표효과 문헌 강조) 그대로.

---
## 3차 실행(09:22)
- `data_raw/` 여전히 없음(레포 커밋 2dee771). **추정하지 않았다.** 필요한 것: Codespace의 `data_raw/` 폴더를 커밋·푸시.
- 발표자료 v2(`deck_v2.pdf`, 본문 18장 + 부록 4장): 도입(PMCCF 등)·질문·첫 시도와 실패·두 번째 시도·현재 설계까지 완성. 결과 6장·강건성 2장은 자리만 표시.
- 논문은 쓰지 않았다(결과가 초록·서론·결론·제목을 정하므로 결과 없이 쓰면 다시 써야 함). 자료가 오면: decode → run → 결과 슬라이드·논문 작성.
- 10/10 시간별 경로는 trump2 원자료로 다시 계산(fig/oct10_path.pdf). 이전에 그림에서 읽은 값과 0.02%p 이내로 일치.
- 미확인: OMT·QE·포워드 가이던스 서지(기억 기준), E19 시간대, IMPL 발효 시각 건별, TiRADE 논문 마지막 20k자.

---
## 2026-11-15 11시대: 자료 도착, 추정 완료
- 레포 eb186b3 에 data_raw 도착(Yahoo 237, Dukascopy 42 zip, Polymarket 105 파일=수집 중간본). 디코딩 OK(1분봉 1,280만 행; 형식은 time, open, close, low, high, vol 확인).
- `python pipeline.py run` 결과: out/event_responses.csv, regressions.csv, contrasts.csv, run_log.txt. 보조 통계·그림: results_figs.py.
- 주 결과: ESC 평균 z=0.59(20건, 16건 +, 부호검정 p=0.012; 4/9 혼합 제외 0.87, t=2.64). 전후반 차이 없음(p=0.74). 실행 대 미실행 차이 없음(p=0.19). DEESC 평균 −0.91(t=−2.15). IMPL 평균 0.17(t=0.74). 기울기 회귀 전부 비유의, MDE 28.
- 발표자료 v3(deck_v3.pdf, 본문 23장+부록 5장)에 결과 반영.
- 남은 일: 논문 작성, 예측시장(수집 끝나면), Tier B 일별 반응, 실현 비율(v1.2, 탐색) 여부, OMT 등 서지 확인, 슬라이드 3~6pt 넘침 4곳.

## 2026-11-15 해석 분석 (사후·탐색, interp.py → out/nonexec_reason.csv, out/interp_esc.csv)
- 미실행 21건 사유: CONC 4 / NEGO 5 / UNIL 12; 형태 EXPL 11 / SILENT 10. 법원 사유는 위협 단계에 없음.
- ESC z: NEGO 1.88(4) CONC 1.15(4) EXEC 0.57(5, E07 제외) UNIL 0.26(6). CONC+NEGO vs UNIL perm p=0.16, MWU 0.18. EXPL 1.39(9) vs SILENT 0.23(5), MWU 0.11.
- 채널: ESC z_mkt 0.43 / z_fx 1.17; DEESC z_mkt -1.63 / z_fx -0.10; IMPL 0.43 / -0.08.
- 지속성(ES 1h, 추세 미조정, E07 제외 중앙값): 30분 -0.11%, 1일 0.00, 3일 +0.34, 10일 +0.50.
- 주의: UNIL은 품목 관세가 많아 지수·환율이 맞는 측정 도구가 아닐 수 있음(섹터 ETF로 확인 필요). yahoo 1d는 2018년부터 있음(1기 일별 비교 가능).
- 다음: 해석 슬라이드(deck_v4) → 논문.
- 11/15: deck_v4(해석 3장+결론 개정), events_xc_v1.csv(17건), collect_xc.py 전달, PAPER_FRAME.md 작성. 품목 관세: 구리 선물 +12.4%(7/8), XPH +2.0% 초과(9/26) → 지수 무반응은 측정 도구 문제 일부.
- 11/15: GitHub push 권한 확보. 브랜치 claude/xc-collect + Actions(collect-xc.yml)로 수집 자동화 성공(70/70). 로컬 클론 /home/claude/parkchanjin0128-pixel/research-agent 가 해당 브랜치.
- 7절 1차(xc.py → out/xc_responses.csv, 일별, 동일가중 초과수익): ESC 10건 CN 대체 +0.95%(z 0.17), US 공급사 −0.57%(z −0.35); DEESC 6건 CN −0.86%, US +1.14%. 유의하지 않음. 2022–24 규칙 3건은 CN 하락(−1.9%), 2025년 이후 ESC 7건은 CN 상승, 번복 X09·X13·X14는 CN 하락. 사후 관찰. X07·X08·X16·X17 날짜 원문 확인 필요.
- 11/15 12:20: 예측시장 병렬 수집 완료(collect_pm_fast.py, Actions). Polymarket 1026/1080 시장, 86만 포인트. Kalshi는 로그 참조. 브랜치 claude/xc-collect.
- 11/15 오후: 예측시장 분석(pm.py, pm2.py → out/pm_calibration.csv, pm_event_jumps.csv), 수출통제 X17 날짜 정정(11/9→9/23) 후 재추정, 그림 4종(figs_paper.py), 논문 v1(paper/paper.tex, 18쪽), 발표자료 v5(34쪽) 완성. 남은 것: Kalemli-Özcan·Merendino 논문 정식 제목 확인, E19 시간대, 품목 관세의 품목별 가격 반응, 2018–19 비교.
- 11/15: 발표자료 v6(키워드 제목+핵심 문장 줄, 계층 재설계, 넘침 0), 발표 대본(Docs, 40분) 작성.
- 11/15 오후: 1기(2018–19) 트윗 위협 12건 비교(t1.py), 중국 상장사 R&D 패널(rd.py) 추가. 논문 v3(22쪽), 디자인 수정 전달서 작성.
