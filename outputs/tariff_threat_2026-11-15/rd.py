import numpy as np,pandas as pd
from scipy import stats
d=pd.read_csv('/home/claude/parkchanjin0128-pixel/research-agent/data_raw/cn_rd/profit_sheets.csv')
d['q']=pd.PeriodIndex(pd.to_datetime(d.REPORT_DATE),freq='Q'); d=d[d.q>='2018Q1'].sort_values(['sym','q']).drop_duplicates(['sym','q'])
d['yr']=d.q.dt.year
for c,n in [('RESEARCH_EXPENSE','rd'),('TOTAL_OPERATE_INCOME','rev')]:
    prev=d.groupby(['sym','yr'])[c].shift(1); d[n]=np.where(d.q.dt.quarter==1,d[c],d[c]-prev)   # 누계 → 분기 흐름
d.loc[d.rd<=0,'rd']=np.nan; d.loc[d.rev<=0,'rev']=np.nan
d['lrd']=np.log(d.rd); d['g']=d.groupby('sym').lrd.diff(4)          # 전년 동기 대비 로그 증가율
d['rd4']=d.groupby('sym').rd.transform(lambda s:s.rolling(4).sum()); d['rev4']=d.groupby('sym').rev.transform(lambda s:s.rolling(4).sum()); d['int4']=100*d.rd4/d.rev4
d.to_csv('out/rd_panel.csv',index=False)
print('firms',d.groupby('grp').sym.nunique().to_dict(),'obs with g',d.g.notna().groupby(d.grp).sum().to_dict())
def per(q):
    return 'A 2019Q1–2022Q3' if q<=pd.Period('2022Q3') else ('B 2022Q4–2024Q4' if q<=pd.Period('2024Q4') else 'C 2025Q1–2026Q3')
x=d[d.g.notna()&(d.q>='2019Q1')].copy(); x['per']=x.q.map(per)
f=x.groupby(['grp','sym','per']).g.mean().unstack()          # 기업별 기간 평균 → 기업 단위 추론
print((100*f.groupby('grp').mean()).round(1)); print(f.notna().groupby('grp').sum())
for a,b in [('A 2019Q1–2022Q3','B 2022Q4–2024Q4'),('B 2022Q4–2024Q4','C 2025Q1–2026Q3'),('A 2019Q1–2022Q3','C 2025Q1–2026Q3')]:
    ch=(f[b]-f[a]).dropna(); s=ch[ch.index.get_level_values(0)=='semi']; c=ch[ch.index.get_level_values(0)=='ctrl']
    t=stats.ttest_ind(s,c,equal_var=False); print(a[:1],'→',b[:1],'DiD(semi−ctrl) %.1f%%p'%(100*(s.mean()-c.mean())),'n',len(s),len(c),'t %.2f p %.3f'%(t.statistic,t.pvalue),'MWU p %.3f'%stats.mannwhitneyu(s,c).pvalue)
# 분기별 차이 경로
gq=x.groupby(['q','grp']).g.agg(['mean','sem','count']).unstack(); diff=100*(gq['mean']['semi']-gq['mean']['ctrl']); se=100*np.sqrt(gq['sem']['semi']**2+gq['sem']['ctrl']**2)
pd.DataFrame({'q':diff.index.astype(str),'semi':100*gq['mean']['semi'].values,'ctrl':100*gq['mean']['ctrl'].values,'diff':diff.values,'se':se.values}).round(2).to_csv('out/rd_quarterly.csv',index=False)
print(pd.DataFrame({'semi':100*gq['mean']['semi'],'ctrl':100*gq['mean']['ctrl'],'diff':diff,'se':se}).round(1).to_string())
# 집약도
i=d[d.int4.notna()].groupby([d.q.dt.year,'grp']).int4.median().unstack(); print(i.round(1).T)
# 가짜 시점: 2020Q4를 '신호'로 놓았을 때 (2019Q1–2020Q3 대 2020Q4–2022Q3)
x2=x[x.q<=pd.Period('2022Q3')].copy(); x2['pp']=np.where(x2.q<=pd.Period('2020Q3'),'pre','post'); f2=x2.groupby(['grp','sym','pp']).g.mean().unstack(); ch=(f2['post']-f2['pre']).dropna()
s=ch[ch.index.get_level_values(0)=='semi']; c=ch[ch.index.get_level_values(0)=='ctrl']; print('가짜 시점 2020Q4 DiD %.1f%%p'%(100*(s.mean()-c.mean())),'p %.3f'%stats.ttest_ind(s,c,equal_var=False).pvalue,len(s),len(c))
