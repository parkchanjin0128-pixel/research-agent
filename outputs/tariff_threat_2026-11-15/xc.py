import glob,gzip,json,os,numpy as np,pandas as pd
R='/home/claude/parkchanjin0128-pixel/research-agent/data_raw/yahoo'
def load(sym):
    f=os.path.join(R,sym.replace('^','_')+'_1d.json.gz'); r=json.loads(gzip.open(f).read())['chart']['result'][0]
    tz=r['meta']['exchangeTimezoneName']; q=r['indicators']['quote'][0]
    s=pd.Series(q['close'],index=pd.to_datetime(r['timestamp'],unit='s',utc=True).tz_convert(tz).normalize().tz_localize(None)).dropna()
    return s[~s.index.duplicated(keep='last')]
CN=["0981.HK","1347.HK","688981.SS","002371.SZ","688012.SS","688256.SS","688041.SS","603501.SS","688008.SS","301269.SZ","688120.SS","688072.SS"]
US=["NVDA","AMD","AMAT","LRCX","KLAC","SNPS","CDNS","MU","QCOM","INTC"]
def basket(syms):
    r=pd.concat([100*np.log(load(s)).diff() for s in syms],axis=1); r.columns=syms; return r
cn=basket(CN); us=basket(US); b_cn=100*np.log(load("000300.SS")).diff(); b_hk=100*np.log(load("^HSI")).diff(); b_us=100*np.log(load("SPY")).diff()
print(cn.notna().sum().to_dict())
# 본토 종목은 CSI300, 홍콩 종목은 HSI 대비 초과수익 → 동일가중
ex_cn=pd.concat([cn[c]-(b_hk if c.endswith('.HK') else b_cn).reindex(cn.index) for c in CN],axis=1).mean(axis=1,skipna=True)
ex_us=us.sub(b_us.reindex(us.index),axis=0).mean(axis=1)
ev=pd.read_csv('events_xc_v1.csv'); rows=[]
def resp(ex,day,shift,k):
    i=ex.index.searchsorted(pd.Timestamp(day))+shift
    if i+k>len(ex): return np.nan,np.nan,None
    sd=ex.iloc[max(0,i-250):i].std(); v=ex.iloc[i:i+k].sum(); return v, v/(sd*np.sqrt(k)), ex.index[i].date()
for _,e in ev.iterrows():
    # 미국: 장 마감 후면 다음 거래일. 중국: 미국 뉴스는 항상 다음 아시아 세션
    u1,uz1,ud=resp(ex_us,e.news_date,int(e.after_us_close),1); u3,uz3,_=resp(ex_us,e.news_date,int(e.after_us_close),3)
    c1,cz1,cd=resp(ex_cn,e.news_date,1,1); c3,cz3,_=resp(ex_cn,e.news_date,1,3)
    rows.append(dict(id=e.id,date=e.news_date,type=e.type,outcome=e.outcome,cn1=c1,cn_z1=cz1,cn3=c3,cn_z3=cz3,us1=u1,us_z1=uz1,us3=u3,us_z3=uz3,cn_day=cd,us_day=ud,measure=e.measure[:22]))
d=pd.DataFrame(rows); d.to_csv('out/xc_responses.csv',index=False)
pd.set_option('display.width',250); print(d.round(2).to_string())
g=d[d.type!='MIXED'].groupby('type')[['cn1','cn_z1','cn3','cn_z3','us1','us_z1','us3','us_z3']].agg(['mean','count']).round(2); print(g.T)
x=d[d.type=='ESC']; print('ESC cn>0:',(x.cn1>0).sum(),'/',x.cn1.notna().sum(),' us<0:',(x.us1<0).sum()); x=d[d.type=='DEESC']; print('DEESC cn<0:',(x.cn1<0).sum(),'/',x.cn1.notna().sum(),' us>0:',(x.us1>0).sum())
