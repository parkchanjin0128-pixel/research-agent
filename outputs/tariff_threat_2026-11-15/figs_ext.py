import sys; sys.argv=[sys.argv[0],"fig"]; sys.path.insert(0,"/home/claude/work/build")
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
import figures as F
q=pd.read_csv("out/rd_quarterly.csv"); q=q[q.q>="2019Q3"].reset_index(drop=True)
fig,ax=plt.subplots(figsize=(5.8,2.8)); F.hgrid(ax); ax.axhline(0,color=F.INK,lw=0.6)
x=np.arange(len(q)); ax.plot(x,q.semi,color=F.RED,lw=1.5,label="반도체 국산 대체 20개사"); ax.plot(x,q.ctrl,color=F.NAVY,lw=1.5,label="비교 기업 20개사")
for lab,qq in [("2022.10 통제","2022Q4"),("2025 예고·번복 국면","2025Q1")]:
    i=q.index[q.q==qq][0]; ax.axvline(i,color=F.GRAY,lw=0.8,ls=":"); ax.text(i+0.2,ax.get_ylim()[1]*0.93,lab,fontsize=7.8,color="#55606e")
ax.set_xticks(x[::2],[s[2:4]+"."+s[-1]+"Q" for s in q.q[::2]],fontsize=7.4,rotation=45); ax.set_ylabel("연구개발비 전년 동기 대비 증가율 (%)"); ax.legend(loc="lower left",fontsize=7.8)
F.save(fig,"rd_growth")
if os.path.exists("out/t1_responses.csv"):
    a=pd.read_csv("out/t1_responses.csv"); a=a[a.win==30]; b=pd.read_csv("out/event_responses.csv")
    g=[("1기 강화 위협",a[a.type=="ESC"].z.dropna(),F.GRAY),("2기 강화 위협",b[b.type=="ESC"].z.dropna(),F.NAVY),("1기 철회",a[a.type=="DEESC"].z.dropna(),F.GRAY),("2기 철회",b[b.type=="DEESC"].z.dropna(),F.NAVY)]
    fig,ax=plt.subplots(figsize=(5.2,2.8)); F.hgrid(ax); ax.axhline(0,color=F.INK,lw=0.6); rng=np.random.default_rng(4)
    for i,(l,z,c) in enumerate(g):
        ax.scatter(i+rng.uniform(-0.12,0.12,len(z)),z,s=14,color=c,zorder=3); m=np.median(z); ax.plot([i-0.25,i+0.25],[m,m],color=F.RED,lw=1.6,zorder=4); ax.text(i+0.28,m,F.fmt(m),fontsize=8,color=F.RED,va="center")
    ax.set_xticks(range(4),["%s\n(n=%d)"%(l,len(z)) for l,z,_ in g]); ax.tick_params(axis="x",length=0); ax.set_yscale("symlog",linthresh=2); ax.set_yticks([-5,-2,-1,0,1,2,5,10,25],["−5","−2","−1","0","1","2","5","10","25"]); ax.set_ylabel("표준화 반응 z (2 초과는 로그 눈금)"); ax.set_xlim(-0.5,3.8)
    F.save(fig,"t1_compare")
