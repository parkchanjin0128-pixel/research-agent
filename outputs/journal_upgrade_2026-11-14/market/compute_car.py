"""고정 표본·규칙에 따른 실제 일별 시장모형 CAR. 독립 검증 코드가 아니다."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json, hashlib
import numpy as np
import pandas as pd

BASE=Path(__file__).resolve().parent
FIRMS=pd.read_csv(BASE/'firm_universe.csv',keep_default_na=False)
BENCH={'US_ADR':'^GSPC','HK':'^HSI','A_SHANGHAI':'000001.SS','A_SHENZHEN':'399001.SZ'}
EVENTS=[
 {'event_id':'ZTE_APR16_AUX','signal_id':'ZTE_APRIL','date':'2018-04-16','clock':'earliest_public_day_not_established;auxiliary_calendar_date','source':'https://www.govinfo.gov/content/pkg/FR-2018-04-23/html/2018-08354.htm'},
 {'event_id':'ZTE_FR_APR23_AUX','signal_id':'ZTE_APRIL','date':'2018-04-23','clock':'FR_publication_not_independent_new_shock','source':'https://www.govinfo.gov/content/pkg/FR-2018-04-23/html/2018-08354.htm'},
 {'event_id':'HOUSE_JUN26','signal_id':'HOUSE','date':'2018-06-26','clock':'calendar_date;precise_information_clock_unresolved','source':'https://www.govinfo.gov/content/pkg/CREC-2018-06-26/html/CREC-2018-06-26-pt1-PgH5674-4.htm'},
 {'event_id':'ECRA_AUG13','signal_id':'ECRA','date':'2018-08-13','clock':'enactment_calendar_date;not_first_news;precise_information_clock_unresolved','source':'https://www.govinfo.gov/content/pkg/PLAW-115publ232/html/PLAW-115publ232.htm'},
 {'event_id':'ANPRM_NOV16_19','signal_id':'ANPRM','date':'2018-11-16','clock':'2018-11-16T08:45:00-05:00;21:45_Asia;one_event_not_two','source':'https://www.govinfo.gov/content/pkg/FR-2018-11-19/html/2018-25221.htm'},
]

def read_price(symbol):
 p=BASE/'raw'/('yahoo_'+symbol.replace('^','INDEX_')+'.json')
 obj=json.loads(p.read_text(encoding='utf-8'))['chart']['result'][0]
 dates=[datetime.fromtimestamp(t,ZoneInfo(obj['meta']['exchangeTimezoneName'])).date().isoformat() for t in obj['timestamp']]
 q=obj['indicators']['quote'][0]
 a=obj['indicators'].get('adjclose',[{}])[0].get('adjclose')
 if a is None: raise ValueError(f'adjusted close missing: {symbol}')
 d=pd.DataFrame({'date':dates,'close':q['close'],'adjusted_close':a,'volume':q.get('volume')})
 if d['date'].duplicated().any(): raise ValueError(f'duplicate date {symbol}')
 d=d.set_index('date').sort_index()
 d['symbol']=symbol
 return d,obj.get('events',{}),obj['meta']

def main():
 prices={}; qas=[]; actions=[]; rawrows=[]
 for sym in list(FIRMS['symbol'])+list(dict.fromkeys(BENCH.values())):
  d,events,meta=read_price(sym);prices[sym]=d;rawrows.append(d.reset_index())
  qas.append({'symbol':sym,'n_rows':len(d),'first_date':d.index.min(),'last_date':d.index.max(),'duplicate_dates':int(d.index.duplicated().sum()),'missing_adjusted_close':int(d.adjusted_close.isna().sum()),'nonpositive_adjusted_close':int((d.adjusted_close<=0).sum()),'zero_volume_rows':int((d.volume==0).sum()),'timezone':meta.get('exchangeTimezoneName'),'currency':meta.get('currency'),'provider_firstTradeDate_not_official_listing_date':meta.get('firstTradeDate')})
  for kind,evts in events.items():
   for key,v in evts.items():
    actions.append({'symbol':sym,'kind':kind,'date_local':datetime.fromtimestamp(v['date'],ZoneInfo(meta['exchangeTimezoneName'])).date().isoformat(),'provider_key':key,**v})
 pd.concat(rawrows,ignore_index=True).to_csv(BASE/'prices_2017_2019.csv',index=False)
 pd.DataFrame(qas).to_csv(BASE/'price_quality.csv',index=False)
 pd.DataFrame(actions).to_csv(BASE/'corporate_actions.csv',index=False)
 records=[];ar_records=[];clocks=[];missing=[]
 for firm in FIRMS.to_dict('records'):
  sym=firm['symbol']; market=firm['market'];b=BENCH[market]
  m=prices[b]['adjusted_close'];cal=m.index
  if market=='HK':
   # 2017-08-23은 지수null·양기업거래량0인 공급자 placeholder.
   # 시장전체의 비관측 행을 일별 거래세션으로 세지 않는다.
   peers=FIRMS.loc[FIRMS.market=='HK','symbol']
   all_zero=pd.concat([prices[s]['volume'].reindex(cal).eq(0) for s in peers],axis=1).all(axis=1)
   cal=cal[~(m.isna()&all_zero)]
   m=m.reindex(cal)
  stock=prices[sym].reindex(cal)
  # 거래중단·비거래 관측을 일수익률0으로 바꾸지 않음. 전후 양일가격 필요.
  valid=stock.adjusted_close.where((stock.adjusted_close>0)&(stock.volume>0))
  ri=valid.pct_change(fill_method=None)
  rm=m.where(m>0).pct_change(fill_method=None)
  for dt in cal[ri.isna() & (np.arange(len(cal))>0)]:
   missing.append({'symbol':sym,'date':dt,'close':stock.loc[dt,'close'],'adjusted_close':stock.loc[dt,'adjusted_close'],'volume':stock.loc[dt,'volume'],'reason':'missing_current_or_previous_valid_close_or_zero_volume'})
  for ev in EVENTS:
   requested='2018-11-19' if ev['signal_id']=='ANPRM' and market!='US_ADR' else ev['date']
   basepos=int(cal.searchsorted(requested))
   offsets=[0] if ev['signal_id']=='ANPRM' else [0,1]
   for shift in offsets:
    pos=basepos+shift;day0=cal[pos]
    version='primary_fixed_calendar' if shift==0 else 'next_session_clock_sensitivity'
    clocks.append({'symbol':sym,'market':market,'event_id':ev['event_id'],'signal_id':ev['signal_id'],'nominal_date':ev['date'],'day0':day0,'clock_version':version,'public_clock':ev['clock'],'source_url':ev['source']})
    estdates=cal[max(0,pos-250):pos-30]
    fit=pd.DataFrame({'ri':ri.reindex(estdates),'rm':rm.reindex(estdates)}).dropna()
    eligible=(pos>=250 and len(fit)>=180)
    alpha=beta=sigma=np.nan
    if eligible:
     X=np.column_stack([np.ones(len(fit)),fit.rm.to_numpy()]);y=fit.ri.to_numpy()
     alpha,beta=np.linalg.lstsq(X,y,rcond=None)[0]
     sigma=np.sqrt(np.square(y-X@np.array([alpha,beta])).sum()/(len(y)-2))
    for lo,hi,label in [(-1,1,'[-1,+1]'),(0,1,'[0,+1]')]:
     wd=cal[pos+lo:pos+hi+1]
     frame=pd.DataFrame({'ri':ri.reindex(wd),'rm':rm.reindex(wd)})
     status='ok' if eligible and len(wd)==hi-lo+1 and frame.notna().all().all() else ('insufficient_estimation' if not eligible else 'missing_window_return')
     ar=frame.ri-alpha-beta*frame.rm
     car=float(ar.sum()) if status=='ok' else np.nan
     records.append({'firm_id':firm['firm_id'],'symbol':sym,'market':market,'benchmark':b,'event_id':ev['event_id'],'signal_id':ev['signal_id'],'clock_version':version,'clock_status':ev['clock'],'day0':day0,'window':label,'window_start':wd.min(),'window_end':wd.max(),'estimation_start':estdates.min(),'estimation_end':estdates.max(),'expected_estimation_rows':len(estdates),'n_estimation':len(fit),'alpha':alpha,'beta':beta,'residual_sd':sigma,'CAR':car,'CAR_pct':car*100 if pd.notna(car) else np.nan,'status':status,'B_status':'awaiting_parent_2013_2017_mapping','interpretation':'descriptive_stock_response_not_allocation_effect'})
     for dt in wd:
      ar_records.append({'symbol':sym,'event_id':ev['event_id'],'clock_version':version,'window':label,'date':dt,'relative_day':int(cal.get_loc(dt))-pos,'stock_return':ri[dt],'benchmark_return':rm[dt],'expected_return':alpha+beta*rm[dt],'abnormal_return':ar[dt]})
 out=pd.DataFrame(records);out.to_csv(BASE/'firm_event_car.csv',index=False)
 pd.DataFrame(ar_records).to_csv(BASE/'daily_abnormal_returns.csv',index=False)
 pd.DataFrame(clocks).to_csv(BASE/'event_clock_mapping.csv',index=False)
 pd.DataFrame(missing).to_csv(BASE/'missing_or_suspended_days.csv',index=False)
 ok=out[(out.status=='ok')&(out.clock_version=='primary_fixed_calendar')]
 summary=ok.groupby(['event_id','signal_id','market','window'],sort=False).agg(n_firms=('symbol','size'),equal_weight_mean_CAR_pct=('CAR_pct','mean'),median_CAR_pct=('CAR_pct','median'),min_CAR_pct=('CAR_pct','min'),max_CAR_pct=('CAR_pct','max')).reset_index()
 summary.to_csv(BASE/'market_event_summary.csv',index=False)
 report={'producer':'/root/nov14_market_producer','independent_verification':False,'n_candidates':len(FIRMS),'n_downloaded_instruments':len(prices),'daily_price_rows':sum(len(x) for x in prices.values()),'primary_rows':int((out.clock_version=='primary_fixed_calendar').sum()),'all_CAR_rows':len(out),'status_counts':out.groupby(['clock_version','status']).size().to_dict().__str__(),'protocol_sha256':hashlib.sha256((BASE/'protocol_pre_returns.md').read_bytes()).hexdigest(),'B_received':False,'no_DIUX_daily_CAR':'public_release_day_only_month_known','ANPRM_count':'one event; US16 and Asia19; no separate FR19 shock'}
 (BASE/'computation_receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 print(summary.to_string(index=False))
if __name__=='__main__':main()
