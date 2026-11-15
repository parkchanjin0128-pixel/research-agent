import sys, os; sys.argv=[sys.argv[0], "fig"]; sys.path.insert(0, "/home/claude/work/build")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import figures as F
from pipeline import load_events, credibility
os.makedirs("fig", exist_ok=True)
ev=load_events(); ev=pd.concat([ev, credibility(ev)],axis=1)
esc=ev[ev["type"]=="ESC"].sort_values("day")
# (1) 신뢰도 경로
fig,ax=plt.subplots(figsize=(5.4,2.9)); F.hgrid(ax)
col={"EXECUTED":F.NAVY,"EXECUTED_PARTIAL":F.GRAY,"NOT_EXECUTED":F.RED,"UNRESOLVED":"#cccccc"}
ax.step(esc["day"], esc["C_all"], where="post", color=F.INK, lw=1.0)
for k,lab in (("EXECUTED","실행"),("EXECUTED_PARTIAL","부분 실행"),("NOT_EXECUTED","미실행")):
    s=esc[esc["outcome"]==k]; ax.scatter(s["day"], s["C_all"], s=22, color=col[k], zorder=3, label=lab, marker={"EXECUTED":"o","EXECUTED_PARTIAL":"s","NOT_EXECUTED":"x"}[k])
ax.set_ylim(0.2,0.6); ax.set_ylabel("과거 위협의 실행률 (사후평균)"); ax.legend(loc="upper right", ncol=3, handletextpad=0.2, columnspacing=0.8)
import matplotlib.dates as md
ax.xaxis.set_major_locator(md.MonthLocator(bymonth=[1,4,7,10])); ax.xaxis.set_major_formatter(md.DateFormatter("%y.%m")); ax.tick_params(axis="x", labelsize=8.5); F.save(fig,"cred_path")
print(esc[["id","date","outcome","C_all","n_past"]].to_string(index=False))
# (2) 10월 10일 경로 — 원자료(trump2/hourly_prices.csv)
p=pd.read_csv("/home/claude/parkchanjin0128-pixel/research-agent/trump2/hourly_prices.csv",encoding="utf-8-sig")
d=p[(p["date"]=="2025-10-10")&(p["local_hm"]>="09:30")&(p["local_hm"]<"16:00")]
print(sorted(d["symbol"].unique()), d[d["symbol"]=="BIDU"][["local_hm","open","close"]].to_string(index=False))
