"""Bounded official archive inventory probe, fixed protocol before inventory reads.
No effects estimated. At most 40 archive page fetches; details handled separately.
"""
from acquire_behavior import ROOT, RAW, write_csv, Parser
from acquire_procurement import fetch
import json,re,hashlib,datetime
from urllib.parse import urljoin
from html import unescape

KEYWORDS=r'GPU|图形加速|深度学习|人工智能|高性能计算|计算集群|超算|加速卡|计算服务器|服务器集群'
PERIOD=('2016-01-01','2019-12-31')
SZU_PATHS=['cggg/zbcg/xnjzcg.htm','cggg/zbcg/zfjzcg.htm','cjjg/zbjggs/xnjzcg.htm','cjjg/zbjggs/zfjzcg.htm','cjjg/dbgs1.htm']
def protocol():
 p=dict(frozen_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),institutions=['深圳大学','南京理工大学'],period=PERIOD,title_screen_regex=KEYWORDS,case_origin='Three notices selected by exploratory web searches for GPU/high-performance-computing in 2017-2019; two institutions, not a random or exhaustive sample',archive_sampling='SZU fixed public procurement categories, parse entire embedded datanews arrays; NJUST two announcement categories, archive endpoints and date-directed binary search followed by bounded page inventory',max_archive_fetches=40,max_detail_fetches=10,denominator='current archive listings only, NOT verified complete original procurement population; deleted notices, separate channels, small purchases and external procurement can be missing',no_clean_window_claim=True)
 path=ROOT/'archive_protocol.json'
 if not path.exists():path.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')

cache={}; logs=[]
def get(url,label):
 if url in cache:return cache[url]
 if len(logs)>=40:raise RuntimeError('40 archive document cap')
 try:
  h,m=fetch(url)
  # archive indexes contain titles/dates/URLs, no need to retain contact-heavy footers
  rawname='archive_'+re.sub(r'[^a-zA-Z0-9_-]','_',label)+'.txt'
  arr=re.search(r'var\s+datanews\s*=\s*(\[.*?\]);',h,re.S)
  records=[]
  if arr:
   data=json.loads(arr.group(1)); retained=arr.group(1)
   for d in data:
    records.append(dict(institution='深圳大学',category=label,date=d.get('showDate','').replace('/','-'),title=d.get('showTitle','').strip(),url=urljoin(url,d.get('url',{}).get('asString','')),archive_url=url))
  else:
   retained=[]
   for dd in re.findall(r'<dd\b[^>]*>(.*?)</dd>',h,re.S|re.I):
    a=re.search(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',dd,re.S|re.I)
    date=re.search(r'\d{4}-\d{2}-\d{2}',dd)
    if a and date:
     p=Parser();p.feed(a.group(2)); title=unescape(''.join(p.all)).strip()
     records.append(dict(institution='南京理工大学',category=label.split('_')[0],date=date.group(0),title=title,url=urljoin(url,a.group(1)).replace('http://zbpt.njust.edu.cn:80','https://zbpt.njust.edu.cn'),archive_url=url))
     retained.append(dict(date=date.group(0),title=title,original_href=a.group(1)))
   retained=json.dumps(retained,ensure_ascii=False)
  (RAW/rawname).write_text(retained,encoding='utf-8')
  pages=re.search(r'(\d+)/(\d+)页',h)
  rec=dict(url=url,label=label,status='success',rows=len(records),minimum_date=min([r['date'] for r in records],default=''),maximum_date=max([r['date'] for r in records],default=''),page_count=int(pages.group(2)) if pages else None,html_text_sha256=hashlib.sha256(h.encode('utf-8')).hexdigest(),retained='raw/'+rawname,method=m)
  result=(records,rec)
 except Exception as e:
  rec=dict(url=url,label=label,status='failed',error=str(e));result=([],rec)
 logs.append(rec);cache[url]=result
 return result

def main():
 protocol(); allrows=[]
 for path in SZU_PATHS:
  r,m=get('https://bidding.szu.edu.cn/'+path,'szu_'+path.replace('/','_'));allrows+=r
 # Date-directed index probing does not read selected outcome amounts.
 for cat in ['cgxx','cjgg']:
  base='https://zbpt.njust.edu.cn/'+cat+'/'
  first,meta=get(base+'index.jhtml',cat+'_1');allrows+=first
  total=meta.get('page_count') or 1
  tail,mt=get(base+f'index_{total}.jhtml',cat+'_'+str(total));allrows+=tail
  # Establish a page near 2019-12-31 with a bounded binary date search.
  lo,hi=1,total
  while hi-lo>1 and len(logs)<30:
   mid=(lo+hi)//2;rr,mm=get(base+f'index_{mid}.jhtml',cat+'_'+str(mid));allrows+=rr
   if not rr:break
   if mm['minimum_date']>'2019-12-31':lo=mid
   else:hi=mid
  # Inspect a small contiguous historical block; do not label it a census.
  for page in range(max(1,hi-1),min(total,hi+6)+1):
   if len(logs)>=40:break
   rr,mm=get(base+('index.jhtml' if page==1 else f'index_{page}.jhtml'),cat+'_'+str(page));allrows+=rr
 unique={}
 for r in allrows:unique[(r['category'],r['url'])]=r
 allrows=list(unique.values())
 inperiod=[r for r in allrows if PERIOD[0]<=r['date']<=PERIOD[1]]
 candidates=[r for r in inperiod if re.search(KEYWORDS,r['title'],re.I)]
 write_csv('archive_all_listed_records.csv',allrows)
 write_csv('archive_2016_2019_inventory.csv',inperiod)
 write_csv('archive_keyword_candidates.csv',candidates)
 summary=dict(fetched_archive_documents=len(logs),listed_unique_category_url_pairs=len(allrows),within_period=len(inperiod),title_keyword_candidates=len(candidates),coverage_by_year={str(y):sum(r['date'].startswith(str(y)) for r in inperiod) for y in range(2016,2020)},candidate_coverage_by_year={str(y):sum(r['date'].startswith(str(y)) for r in candidates) for y in range(2016,2020)},full_original_population_verified=False,logs=logs)
 (ROOT/'archive_probe_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in summary.items() if k!='logs'},ensure_ascii=False,indent=2))
 print(json.dumps(candidates,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
