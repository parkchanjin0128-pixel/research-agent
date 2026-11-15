import sys, os; sys.argv=[sys.argv[0], "fig"]; sys.path.insert(0, "/home/claude/work/build")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, math
from scipy import stats
import figures as F
d=pd.read_csv("out/event_responses.csv",encoding="utf-8-sig"); d["day"]=pd.to_datetime(d["date"])
E=d[d.type=="ESC"]; D=d[d.type=="DEESC"]; I=d[d.type=="IMPL"]
def desc(x,name):
    x=np.asarray(x,float); n=len(x); k=int((x>0).sum())
    print(f"{name}: n={n} mean={x.mean():.3f} median={np.median(x):.3f} t={x.mean()/(x.std(ddof=1)/math.sqrt(n)):.2f} pos={k}/{n} sign_p={stats.binomtest(k,n,0.5).pvalue:.3f} wilcoxon_p={stats.wilcoxon(x).pvalue:.3f}")
desc(E.z,"ESC all"); desc(E[E.id!="E07"].z,"ESC excl E07(혼합)"); desc(E[(E.id!="E07")&(E.closed!=True)].z,"ESC excl E07, open only")
desc(D.z,"DEESC all"); desc(D[D.id!="D03"].z,"DEESC excl D03"); desc(I.z,"IMPL")
ex=E[E.outcome.isin(["EXECUTED","EXECUTED_PARTIAL"])&(E.id!="E07")].z; nx=E[E.outcome=="NOT_EXECUTED"].z
print("exec(excl E07) mean",round(ex.mean(),3),len(ex),"| notexec mean",round(nx.mean(),3),len(nx),"| MWU p",round(stats.mannwhitneyu(ex,nx).pvalue,3))
Es=E[E.id!="E07"].sort_values("day"); h=len(Es)//2
print("early/late excl E07:",round(Es.z.iloc[:h].mean(),3),round(Es.z.iloc[h:].mean(),3),"MWU p",round(stats.mannwhitneyu(Es.z.iloc[:h],Es.z.iloc[h:]).pvalue,3), "| spearman(z, time) all", [round(v,3) for v in stats.spearmanr(E.day.map(pd.Timestamp.toordinal),E.z)])
print("ESC S&P 30분 수익률(%) 하락=+ : median", round(E.ret_mkt.median(),3), "open-only median", round(E[E.closed!=True].ret_mkt.median(),3), "| 통화 median", round(E.ret_fx.median(),3))
print("DEESC S&P median", round(D.ret_mkt.median(),3), "| IMPL S&P median", round(I.ret_mkt.median(),3))
# 그림 1: 사건별 z (시간순)
fig,ax=plt.subplots(figsize=(5.6,2.9)); F.hgrid(ax); ax.axhline(0,color=F.INK,lw=0.6)
ax.axhspan(-1.96,1.96,color="#F1F4F8",lw=0)
sty={"EXECUTED":(F.NAVY,"o","실행"),"EXECUTED_PARTIAL":(F.GRAY,"s","부분 실행"),"NOT_EXECUTED":(F.RED,"x","미실행")}
for k,(c,m,l) in sty.items():
    s=E[E.outcome==k]; ax.scatter(s.day,s.z,color=c,marker=m,s=26,zorder=3,label=l)
for _,r in E.iterrows():
    if abs(r.z)>2.2: ax.annotate({"E07":"4/9 (유예와 같은 게시물)","E15":"10/10 대중 위협","E01":"콜롬비아","E09":"EU 50%"}.get(r.id,r.id),(r.day,r.z),xytext=(6,0),textcoords="offset points",fontsize=7.8,va="center",color="#55606e")
import matplotlib.dates as md
ax.xaxis.set_major_locator(md.MonthLocator(bymonth=[1,4,7,10])); ax.xaxis.set_major_formatter(md.DateFormatter("%y.%m"))
ax.set_ylabel("표준화 반응 z (위험회피 방향 = +)"); ax.legend(loc="lower right",ncol=3,handletextpad=0.2,columnspacing=0.8); ax.set_ylim(-5.6,6.6)
F.save(fig,"res_esc_scatter")
# 그림 2: 유형별 평균 z와 사건별 점
fig,ax=plt.subplots(figsize=(4.3,2.8)); F.hgrid(ax); ax.axhline(0,color=F.INK,lw=0.6)
groups=[("강화 위협\n(n=%d)"%len(E),E.z,F.NAVY),("완화·철회\n(n=%d)"%len(D),D.z,F.GRAY),("예정 발효\n(n=%d)"%len(I),I.z,F.LIGHT)]
rng=np.random.default_rng(1)
for i,(lab,x,c) in enumerate(groups):
    x=np.asarray(x,float); ax.scatter(i+rng.uniform(-0.13,0.13,len(x)),x,s=12,color=c,alpha=0.9,zorder=3)
    m=np.median(x); ax.plot([i-0.25,i+0.25],[m,m],color=F.RED,lw=1.6,zorder=4); ax.text(i+0.29,m,"중앙값 "+F.fmt(m),fontsize=8,va="center",color=F.RED)
ax.set_xticks(range(3),[g[0] for g in groups]); ax.tick_params(axis="x",length=0); ax.set_xlim(-0.5,2.9); ax.set_ylabel("표준화 반응 z"); ax.set_ylim(-5.6,6.6)
F.save(fig,"res_groups")
# 그림 3: 10/10 분 단위
fx=pd.read_pickle("work/fx_min.pkl")
t0=pd.Timestamp("2025-10-10 14:57",tz="UTC")
fig,ax=plt.subplots(figsize=(4.3,2.6)); F.hgrid(ax)
for inst,c,l,sg in (("USA500IDXUSD",F.NAVY,"S&P 500",1),("USDCNH",F.RED,"USD/CNH",1)):
    s=fx[(fx.inst==inst)&(fx.ts>=t0-pd.Timedelta(minutes=30))&(fx.ts<=t0+pd.Timedelta(minutes=60))].set_index("ts")["close"]
    b=s[s.index<t0].iloc[-1]; ax.plot((s.index-t0).total_seconds()/60,(s/b-1)*100,color=c,lw=1.1,label=l)
ax.axvline(0,color=F.INK,lw=0.8,ls=(0,(4,2))); ax.axhline(0,color=F.INK,lw=0.4); ax.set_xlabel("10:57 ET 게시 기준 경과 시간 (분)"); ax.set_ylabel("게시 직전 대비 (%)"); ax.legend(loc="lower left")
F.save(fig,"res_oct10_min")
