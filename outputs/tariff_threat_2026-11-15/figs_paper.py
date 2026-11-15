import sys; sys.argv=[sys.argv[0],"fig"]; sys.path.insert(0,"/home/claude/work/build")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import figures as F
# 1 결말별 반응
d=pd.read_csv("out/interp_esc.csv"); d=d[d.id!="E07"]
lab={"NEGO":"협상 타결","CONC":"상대 양보","EXEC":"실제 실행","UNIL":"일방 보류·소멸"}
fig,ax=plt.subplots(figsize=(4.8,2.7)); F.hgrid(ax); ax.axhline(0,color=F.INK,lw=0.6); rng=np.random.default_rng(2)
for i,k in enumerate(lab):
    x=d[d.reason==k].z.values; ax.scatter(i+rng.uniform(-0.12,0.12,len(x)),x,s=16,color=F.NAVY,zorder=3)
    ax.plot([i-0.25,i+0.25],[x.mean()]*2,color=F.RED,lw=1.6,zorder=4); ax.text(i+0.28,x.mean(),F.fmt(x.mean()),fontsize=8,color=F.RED,va="center")
ax.set_xticks(range(4),["%s\n(n=%d)"%(v,(d.reason==k).sum()) for k,v in lab.items()]); ax.tick_params(axis="x",length=0); ax.set_ylabel("표준화 반응 z"); ax.set_xlim(-0.5,3.7)
F.save(fig,"int_reason")
# 2 예측시장 보정
a=pd.read_csv("out/pm_calibration.csv")
fig,ax=plt.subplots(figsize=(4.6,2.9)); F.hgrid(ax)
ax.plot([0,1],[0,1],color=F.GRAY,lw=0.8,ls="--")
rng=np.random.default_rng(3); ax.scatter(a.p,a.y+rng.uniform(-0.035,0.035,len(a)),s=16,color=F.LIGHT,edgecolor=F.NAVY,lw=0.6,zorder=3,label="계약 32건 (실행=1, 미실행=0)")
a["bin"]=pd.cut(a.p,[0,0.3,0.6,1]); g=a.groupby("bin",observed=True).agg(p=("p","mean"),y=("y","mean"),n=("y","size"))
ax.plot(g.p,g.y,"-o",color=F.RED,lw=1.4,ms=5,zorder=4,label="구간 평균 실행 비율")
for _,r in g.iterrows(): ax.annotate("n=%d"%r.n,(r.p,r.y),xytext=(6,-10),textcoords="offset points",fontsize=7.8,color=F.RED)
ax.set_xlabel("상장 12–36시간 뒤 가격 (시장이 매긴 실행 확률)"); ax.set_ylabel("실제 실행 여부"); ax.set_xlim(0,1); ax.set_ylim(-0.1,1.1); ax.legend(loc="center right",fontsize=7.6)
F.save(fig,"pm_calib")
# 3 사건 시점 확률 변화
b=pd.read_csv("out/pm_event_jumps.csv"); b=b[~((b.id=="E06")&(b.p_before>0.99))&(b.q!="US x China tariff agreement by November 10?")]
nm={"E02":["2/27 대중 +10% 예고 (대중 인상)","2/27 멕·캐 강행 예고 (캐나다 발효)"],"E03":["3/11 캐나다 철강 50%"],"E06":["4/7 대중 +50% (100% 도달)"],"E14b":["9/25 의약품 100%"],"E15":["10/10 대중 위협 (세율 100–150%)"],"D03":["4/9 90일 유예 (4월 중 대폭 인하)"],"D04":["5/25 EU 50% 연기"],"D06":["7/30 한국 합의 (25% 발효)"],"D08":["1/21 그린란드 철회"]}
cnt={}; labs=[]
for _,r in b.iterrows(): k=cnt.get(r.id,0); labs.append(nm[r.id][k]); cnt[r.id]=k+1
b["lab"]=labs; b=b.iloc[::-1].reset_index(drop=True)
fig,ax=plt.subplots(figsize=(5.8,3.1)); ax.grid(axis="x",color="#E3E7EC",lw=0.6); ax.set_axisbelow(True)
for i,r in b.iterrows():
    c=F.RED if r.dp>0 else F.NAVY
    ax.annotate("",xy=(r.p_3h,i),xytext=(r.p_before,i),arrowprops=dict(arrowstyle="-|>",color=c,lw=1.3,mutation_scale=9))
    ax.scatter([r.p_before],[i],s=14,color="white",edgecolor=c,zorder=3)
    ax.text(1.03,i,"계약 결과: "+("예" if r.final==1 else "아니오"),fontsize=7.6,va="center",color="#55606e")
ax.set_yticks(range(len(b)),b.lab,fontsize=8); ax.set_xlim(0,1.22); ax.set_xticks([0,0.25,0.5,0.75,1]); ax.set_xlabel("계약 가격: 게시 10분 전 → 3시간 뒤")
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="y",length=0)
F.save(fig,"pm_jumps")
# 4 수출통제 상대수익
x=pd.read_csv("out/xc_responses.csv"); x=x[(x.type!="MIXED")].copy(); x["sp"]=x.cn1-x.us1; x=x.reset_index(drop=True)
fig,ax=plt.subplots(figsize=(5.8,2.8)); F.hgrid(ax); ax.axhline(0,color=F.INK,lw=0.6)
col=[F.RED if t=="ESC" else F.NAVY for t in x.type]; ax.bar(range(len(x)),x.sp,color=col,width=0.62,zorder=3)
ax.set_xticks(range(len(x)),[pd.Timestamp(v).strftime("%y.%m") for v in x.date],fontsize=7.6,rotation=45); ax.set_ylabel("중국 대체 − 미국 공급사 초과수익 (%p)")
ax.axvline(2.5,color=F.GRAY,lw=0.8,ls=":"); ax.text(2.6,ax.get_ylim()[1]*0.9,"2025년 이후",fontsize=8,color="#55606e")
from matplotlib.patches import Patch; ax.legend(handles=[Patch(color=F.RED,label="통제 강화"),Patch(color=F.NAVY,label="완화·번복")],loc="lower left",fontsize=7.8,ncol=2)
F.save(fig,"xc_spread")
