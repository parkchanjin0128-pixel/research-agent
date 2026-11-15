import pandas as pd, numpy as np, pickle
from scipy import stats
pd.set_option('display.width',250)
r=pd.read_csv('out/event_responses.csv'); e=pd.read_csv('events_v1.csv')
reason={ # 사후(post hoc) 분류: 가격과 무관하게 outcome_basis와 공개 보도로 코딩
'E01':'CONC','E03':'CONC','E04':'CONC','E17':'CONC',
'E09':'NEGO','E15':'NEGO','E15b':'NEGO','E18':'NEGO','B09':'NEGO',
'E05':'UNIL','E08':'UNIL','E13':'UNIL','E14a':'UNIL','E14b':'UNIL','E16':'UNIL','E19':'UNIL',
'B03':'UNIL','B05':'UNIL','B07':'UNIL','B10':'UNIL','B11':'UNIL'}
form={ # 미실행이 드러난 방식: EXPL=명시적 번복/합의 발표, SILENT=시한 경과·조용한 소멸
'E01':'EXPL','E03':'EXPL','E04':'SILENT','E17':'EXPL','E09':'EXPL','E15':'EXPL','E15b':'EXPL','E18':'EXPL','B09':'EXPL',
'E05':'SILENT','E08':'SILENT','E13':'SILENT','E14a':'EXPL','E14b':'EXPL','E16':'SILENT','E19':'SILENT',
'B03':'SILENT','B05':'EXPL','B07':'SILENT','B10':'SILENT','B11':'SILENT'}
e['reason']=e.id.map(reason); e['form']=e.id.map(form)
e[e.type=='ESC'][['id','reason','form']].to_csv('out/nonexec_reason.csv',index=False)
print(e[e.outcome=='NOT_EXECUTED'].groupby(['reason','form']).size().unstack(fill_value=0))
d=r[r.type=='ESC'].copy(); d['reason']=d.id.map(reason).fillna(d.outcome.str[:4]); d['form']=d.id.map(form)
d=d[d.z.notna()]
print(d[['id','date','outcome','reason','form','z','z_mkt','z_fx','ret_mkt','ret_fx','closed']].round(2).to_string())
print(d.groupby('reason').agg(n=('z','size'),z=('z','mean'),med=('z','median'),zm=('z_mkt','mean'),zf=('z_fx','mean'),rm=('ret_mkt','median')).round(2))
print(d[d.outcome=='NOT_EXECUTED'].groupby('form').agg(n=('z','size'),z=('z','mean'),med=('z','median')).round(2))
# 채널: 주식 vs 환율
for t in ['ESC','DEESC','IMPL']:
    x=r[r.type==t]; b=x.dropna(subset=['z_mkt','z_fx'])
    print(t,'z_mkt',round(x.z_mkt.mean(),2),x.z_mkt.notna().sum(),'z_fx',round(x.z_fx.mean(),2),x.z_fx.notna().sum(),'paired n',len(b),'corr',round(b.z_mkt.corr(b.z_fx),2))
# 지속성: 일별 S&P 누적 (사건 직전 종가 대비)
y=pickle.load(open('work/yahoo.pkl','rb'))
print(y.groupby(['sym','itv']).size().head(60))
from pipeline import perm_diff, load_events
a=d[d.reason.isin(['CONC','NEGO'])].z.values; b=d[d.reason=='UNIL'].z.values; c=d[(d.reason=='EXEC')&(d.id!='E07')].z.values
print('CONC+NEGO',a.mean().round(2),len(a),'UNIL',b.mean().round(2),len(b),'perm',perm_diff(a,b),'MWU',stats.mannwhitneyu(a,b).pvalue.round(3))
print('EXECexE07',c.mean().round(2),'vs UNIL MWU',stats.mannwhitneyu(c,b).pvalue.round(3),'| CONC+NEGO vs EXECexE07',stats.mannwhitneyu(a,c).pvalue.round(3))
x=d[d.outcome=='NOT_EXECUTED']; print('EXPL vs SILENT MWU',stats.mannwhitneyu(x[x.form=='EXPL'].z,x[x.form=='SILENT'].z).pvalue.round(3))
es=y[(y.sym=='ES_F')&(y.itv=='1h')].copy(); es['ts']=pd.to_datetime(es.ts,utc=True); es=es.sort_values('ts').set_index('ts').close
print(es.index[0],es.index[-1])
def px(t): 
    s=es[:t]; return s.iloc[-1] if len(s) else np.nan
d['t0']=pd.to_datetime(d.date+' '+d.time_et).dt.tz_localize('America/New_York').dt.tz_convert('UTC')
H={'2h':2,'1d':24,'3d':72,'5d':120,'10d':240}
for k,h in H.items():
    d[k]=[100*np.log(px(t+pd.Timedelta(hours=h+1))/px(t-pd.Timedelta(hours=1))) for t in d.t0]
d['m30']=-d.ret_mkt
print(d[['id','reason','m30']+list(H)].round(2).to_string())
g=d[d.id!='E07']
print(g.groupby('reason')[['m30']+list(H)].median().round(2)); print(g[['m30']+list(H)].agg(['median','mean']).round(2))
print(g.groupby('reason')[['m30']+list(H)].mean().round(2))
d.to_csv('out/interp_esc.csv',index=False)
