#!/usr/bin/env python3
"""중국 상장사 분기 손익(연구개발비·매출): akshare(동방재부). 반도체 국산 대체 기업과 비교 기업."""
import os, sys, time
import pandas as pd, akshare as ak
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_raw", "cn_rd"); os.makedirs(OUT, exist_ok=True)
SEMI = ["SH688981","SZ002371","SH688012","SH688256","SH688041","SH603501","SH688008","SZ301269","SH688120","SH688072",
        "SH603986","SH600584","SH688126","SH688396","SZ300661","SH688200","SH688082","SZ300604","SZ002156","SH688347"]
CTRL = ["SZ000333","SH600690","SZ000651","SH600276","SZ300760","SZ002594","SZ300750","SH601012","SH600031","SH600309",
        "SZ002475","SZ300124","SH600406","SZ002241","SH600438","SZ300274","SH601100","SZ002460","SH603259","SZ300015"]
rows = []
for grp, syms in (("semi", SEMI), ("ctrl", CTRL)):
    for s in syms:
        df = None
        for attempt in range(3):
            try:
                df = ak.stock_profit_sheet_by_report_em(symbol=s); break
            except Exception as e:
                err = repr(e)[:120]; time.sleep(3)
        if df is None or len(df) == 0:
            print("FAIL", s, err, flush=True); continue
        keep = [c for c in ["SECUCODE","SECURITY_NAME_ABBR","REPORT_DATE","REPORT_TYPE","TOTAL_OPERATE_INCOME","OPERATE_INCOME","RESEARCH_EXPENSE","NETPROFIT"] if c in df.columns]
        d = df[keep].copy(); d["grp"] = grp; d["sym"] = s; rows.append(d)
        print("ok", s, len(d), flush=True); time.sleep(0.8)
if rows: pd.concat(rows, ignore_index=True).to_csv(os.path.join(OUT, "profit_sheets.csv"), index=False)
print("done", len(rows))
