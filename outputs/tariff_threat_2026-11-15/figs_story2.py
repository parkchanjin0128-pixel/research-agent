import sys, os; sys.argv=[sys.argv[0], "fig"]; sys.path.insert(0, "/home/claude/work/build")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import figures as F
REPO="/home/claude/parkchanjin0128-pixel/research-agent/"
# (a) 10월 10일 경로 — 원자료
p=pd.read_csv(REPO+"trump2/hourly_prices.csv",encoding="utf-8-sig")
d=p[(p["date"]=="2025-10-10")&(p["local_hm"]>="09:30")&(p["local_hm"]<"16:00")]
def path(sym):
    g=d[d["symbol"]==sym].sort_values("local_hm"); return (g["close"].to_numpy()/g["open"].iloc[0]-1)*100
adr=np.mean([path(s) for s in ("BIDU","BABA","JD","NTES")],axis=0); spx=path("^GSPC")
F.PATH_ADR=[round(float(v),3) for v in adr]; F.PATH_SPX=[round(float(v),3) for v in spx]
print("ADR4",F.PATH_ADR); print("SPX",F.PATH_SPX)
F.fig_path("oct10_path",(4.1,2.45))
# (b) 의존도 범위가 겹치지 않는다 (논문 7.4절 수치)
fig,ax=plt.subplots(figsize=(3.9,1.9))
for y,(lo,hi,lab,c) in enumerate([(0.018,0.134,"비지목 4기술",F.GRAY),(0.303,0.538,"지목 6기술",F.NAVY)]):
    ax.plot([lo,hi],[y,y],lw=7,color=c,solid_capstyle="butt"); ax.text(hi+0.012,y,f"{lo:.3f}–{hi:.3f}",va="center",fontsize=8.5)
ax.set_yticks([0,1],["비지목 4기술","지목 6기술"]); ax.set_ylim(-0.6,1.6); ax.set_xlim(0,0.72)
ax.axvspan(0.134,0.303,color="#F3E6E8",lw=0); ax.text(0.2185,1.42,"겹치는 구간 없음",ha="center",fontsize=8.3,color=F.RED)
ax.set_xlabel("사전 미국 인용 비중 (중국 출원의 미국 문헌 인용)"); ax.spines["left"].set_visible(False); ax.tick_params(axis="y",length=0)
F.save(fig,"dose_ranges")
# (c) 가짜 시점 대조 (논문 7.4절 수치)
fig,ax=plt.subplots(figsize=(3.9,2.3)); F.hgrid(ax)
lab=["2013.12","2014.12","2015.12","2016.12","2018.12\n(실제)"]; v=[-1.133,-1.322,-1.101,-0.214,-0.3586]
ax.bar(range(5),v,0.55,color=[F.LIGHT]*4+[F.RED])
for i,x in enumerate(v): ax.text(i,x-0.04,F.fmt(x),ha="center",va="top",fontsize=8.3)
ax.axhline(0,color=F.INK,lw=0.6); ax.set_xticks(range(5),lab); ax.tick_params(axis="x",length=0); ax.spines["bottom"].set_visible(False)
ax.set_ylim(-1.65,0.15); ax.set_ylabel("지목−비지목 차등 기울기"); ax.set_xlabel("5개월 창의 시작 시점 (공통 점범위 표본)")
F.save(fig,"fake_windows")
# (d) 강화 위협의 결과 구성
ev=pd.read_csv("events_v1.csv",encoding="utf-8-sig"); e=ev[ev["type"]=="ESC"]
print(e["outcome"].value_counts().to_dict(), "| 시한 명시", int((e["deadline"].fillna("")!="").sum()), "/", len(e))
