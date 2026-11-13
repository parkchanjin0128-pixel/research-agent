"""Primary dated-event evidence, not a legal cutoff or causal-effect audit."""
from pathlib import Path
import urllib.request,hashlib,json,csv,re,concurrent.futures,logging
logging.getLogger('pypdf').setLevel(logging.ERROR)
from html.parser import HTMLParser
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;RAW=HERE/'sources';RAW.mkdir(exist_ok=True)
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[];self.skip=0
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style'):self.skip+=1
 def handle_endtag(self,tag):
  if tag in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,s):
  if not self.skip:self.parts.append(s)
def textof(b):
 try:s=b.decode('utf-8')
 except UnicodeDecodeError:s=b.decode('gb18030',errors='replace')
 h=Text();h.feed(s);return re.sub(r'\s+',' ',' '.join(h.parts))
sources={
 'zte_on':'https://www.govinfo.gov/content/pkg/FR-2018-04-23/html/2018-08354.htm',
 'zte_off':'https://www.govinfo.gov/content/pkg/FR-2018-07-23/html/2018-15633.htm',
 'tariff1':'https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/june/ustr-issues-tariffs-chinese-products',
 'tariff2':'https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/august/ustr-finalizes-second-tranche',
 'tariff3':'https://ustr.gov/about-us/policy-offices/press-office/press-releases/2018/september/ustr-finalizes-tariffs-200',
 'huawei_el':'https://www.govinfo.gov/content/pkg/FR-2019-05-21/html/2019-10616.htm',
 'fdpr_may':'https://www.govinfo.gov/content/pkg/FR-2020-05-19/html/2020-10856.htm',
 'fdpr_aug':'https://www.govinfo.gov/content/pkg/FR-2020-08-20/html/2020-18213.htm',
 'jinhua':'https://www.govinfo.gov/content/pkg/FR-2018-10-30/html/2018-23693.htm',
 'doj':'https://www.justice.gov/archives/opa/speech/attorney-general-jeff-sessions-announces-new-initiative-combat-chinese-economic-espionage',
 'anprm':'https://www.govinfo.gov/content/pkg/FR-2018-11-19/html/2018-25221.htm',
 'house':'https://www.govinfo.gov/content/pkg/CREC-2018-06-26/html/CREC-2018-06-26-pt1-PgH5674-4.htm',
 'ecra':'https://www.govinfo.gov/content/pkg/PLAW-115publ232/html/PLAW-115publ232.htm',
 'diux':'https://www.govexec.com/media/diux_chinatechnologytransferstudy_jan_2018_%281%29.pdf',
 'china35_editor':'https://kunlunce.com/ssjj/fl1/2018-08-08/127123.html',
 'china35_hearing':'https://www.govinfo.gov/content/pkg/CHRG-117shrg47983/pdf/CHRG-117shrg47983.pdf',
 'nsfc':'https://fuwu.most.gov.cn/html/tztg/kjjhyjf/20181205/2960.html'
}
def fetch(kv):
 k,u=kv;p=RAW/(k+('.pdf' if '.pdf' in u else '.html'))
 try:
  if p.exists():b=p.read_bytes();http=200;retrieval='existing local bytes from this producer'
  else:
   with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research evidence audit'}),timeout=45) as r:b=r.read();http=r.status
   p.write_bytes(b);retrieval='fresh HTTPS'
  sha=hashlib.sha256(b).hexdigest()
  if p.suffix=='.pdf':
   if not b.startswith(b'%PDF'):raise ValueError('not PDF bytes')
   from pypdf import PdfReader
   reader=PdfReader(p);pages=[x.extract_text() or '' for x in reader.pages]
   t='\n'.join(pages);(RAW/(k+'.pages.json')).write_text(json.dumps(pages,ensure_ascii=False),encoding='utf-8')
  else:t=textof(b);pages=[]
  (RAW/(k+'.txt')).write_text(t,encoding='utf-8')
  return k,{'url':u,'http':http,'sha256':sha,'bytes':len(b),'local':str(p.relative_to(HERE)).replace('\\','/'),'method':retrieval,'pdf_pages':len(pages),'text':t}
 except Exception as e:return k,{'url':u,'error':str(e),'text':''}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:found=dict(pool.map(fetch,sources.items()))
stamp=datetime.now(timezone.utc).isoformat()
(HERE/'source_manifest.json').write_text(json.dumps({'generated_utc':stamp,'producer':'/root','independent_verification':'pending','sources':{k:{x:v for x,v in r.items() if x!='text'} for k,r in found.items()}},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
records=[
 ('ZTE_ON','2018-04-15','2018-04-23','order immediate effect; publication differs','zte_on','April 2018 denial order; not all China technologies','2017 ZTE/affiliate pre-patent share and dated supply ties; keep denial spell separate'),
 ('ZTE_OFF','2018-07-13','2018-07-23','order immediate effect; publication differs','zte_off','Terminates specified April order; other EAR obligations persist','End ZTE denial spell; do not set all EAR exposure to zero'),
 ('301_LIST1','2018-07-06','2018-06-15','effective vs announcement','tariff1','US import duties on covered China-origin goods, initial25%','2017 CN exports to US by HTS line times rate; direction differs from CN imports from US'),
 ('301_LIST2','2018-08-23','2018-08-07','effective vs announcement','tariff2','initial25%,279 tariff lines in final release','same frozen trade-product-technology crosswalk; exclusions and concordance explicit'),
 ('301_LIST3','2018-09-24','2018-09-18','effective vs announcement','tariff3','initial10%; do not label planned Jan2019 increase as implemented','fixed2017 US export sales exposure, not hardware US input import proxy'),
 ('JINHUA_EL','2018-10-30','2018-10-30','effective and publication','jinhua','Entity/end-user restriction; not general memory ban','pre2018 Jinhua/affiliate patents/supply links; DRAM exclusion sensitivity'),
 ('CHINA_INITIATIVE','2018-11-01','2018-11-01','speech announcement; exact clock unconfirmed','doj','DOJ enforcement initiative, not new ECCN effective date','pre2018 US academic/collaboration and trade-secret exposure; do not interpret same-day CAR as pure export-control signal'),
 ('HUAWEI_EL','2019-05-16','2019-05-21','effective precedes publication','huawei_el','Listed parties and EAR-subject items; TGL/transition/actual licenses not collapsed','pre2018 Huawei/affiliate patents/supply links; dated exclusions and alternative cohorts'),
 ('HUAWEI_FDPR_MAY','2020-05-15','2020-05-19','effective precedes publication','fdpr_may','specified foreign-produced direct products and footnote1 knowledge/scope conditions','dated product-technology and transaction-role exposure; preserve savings clauses'),
 ('HUAWEI_FDPR_AUG','2020-08-17','2020-08-20','effective precedes publication','fdpr_aug','revised product and knowledge/party scope; not retroactive2018 law','separate rule spell; do not code all foreign hardware as controlled'),
 ('NSFC_2019_DEADLINE','2019-03-20','2018-12-05','16:00 centralized receipt deadline, not grant decision','nsfc','program-specific eligibility/window, F04/F05 pilot potential confound','applications with decision/application timestamps; annual awards alone cannot recover pre-Huawei choices')
]
fields=['event_id','effective_or_deadline_date','announcement_or_publication_date','date_definition','source_id','scope','pre_exposure_and_control','source_url','verification']
with (HERE/'concurrent_events.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fields);w.writeheader()
 for r in records:w.writerow(dict(zip(fields[:7],r))|{'source_url':sources[r[4]],'verification':'producer direct-source reading; fresh verifier pending'})
signals=[
 {'id':'DIUX','date_lower':'2018-01-01','date_upper':'2018-01-31','precision':'month only, cover date not exact public-release day','source_id':'diux','definition':'DIUx-authored report updated2016/2017 data; public copy on third-party host, not rule/blanketban'},
 {'id':'ZTE_APRIL','date_lower':'2018-04-15','date_upper':'2018-04-23','precision':'order effect and FR publication bound; earliest public news not established by this row','source_id':'zte_on','definition':'restriction and signal overlap; not clean announcement-only event'},
 {'id':'HOUSE','date_lower':'2018-06-26','date_upper':'2018-06-26','precision':'Congressional Record debate date','source_id':'house','definition':'H5691 Royce technology examples in legislative explanation; not BIS binding designation'},
 {'id':'ECRA','date_lower':'2018-08-13','date_upper':'2018-08-13','precision':'PublicLaw enactment','source_id':'ecra','definition':'identification framework; section1758 considerations are not a validated China loss formula'},
 {'id':'ANPRM','date_lower':'2018-11-16','date_upper':'2018-11-19','precision':'filed public inspection Nov16 08:45ET; publicationNov19; same event','source_id':'anprm','definition':'request for comments, not immediate general China technology prohibition'}
]
with (HERE/'signal_chain.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,list(signals[0])+['source_url']);w.writeheader();w.writerows([r|{'source_url':sources[r['source_id']]} for r in signals])
# Independently parse the editor list headings and the first following date.
t=found['china35_editor']['text'];matches=list(re.finditer(r'(?<!\d)(\d{1,2})\s*[、．]',t));articles=[]
for n,m in enumerate(matches):
 end=matches[n+1].start() if n+1<len(matches) else len(t);piece=t[m.end():end];d=re.search(r'[（(]\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日\s*[）)]',piece)
 if not d:continue
 title=re.sub(r'\s+',' ',piece[:piece.find('《')]).strip()[:80]
 articles.append({'article_number':int(m.group(1)),'date':f'2018-{int(d.group(1)):02d}-{int(d.group(2)):02d}','editor_technology':title,'date_evidence':'editor first-person list reprint; original newspaper page not independently opened','source_url':sources['china35_editor'],'locator':'numbered item '+m.group(1)})
assert len(articles)==35 and [x['article_number'] for x in articles]==list(range(1,36)),len(articles)
with (HERE/'china_35_articles.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,list(articles[0]));w.writeheader();w.writerows(articles)
needles={'zte_on':['effective immediately','15th day of April 2018'],'zte_off':['effective immediately','July 13, 2018'],'tariff1':['July 6, 2018'],'tariff2':['August 23'],'tariff3':['September 24, 2018'],'huawei_el':['May 16, 2019'],'fdpr_may':['effective May 15, 2020'],'fdpr_aug':['effective August 17, 2020'],'doj':['November 1, 2018'],'nsfc':['2019','16'],'anprm':['11-16-18','8:45 am'],'diux':['January 2018']}
checks={k:[{'phrase':v,'present':v.lower() in found[k]['text'].lower()} for v in vv] for k,vv in needles.items()}
summary={'producer':'/root','generated_utc':stamp,'event_rows':len(records),'signal_rows':len(signals),'article_rows':len(articles),'article_min':min(x['date'] for x in articles),'article_max':max(x['date'] for x in articles),'source_reads':{k:{x:v for x,v in r.items() if x in ('http','pdf_pages','error')} for k,r in found.items()},'literal_locator_checks':checks,'independent_verification':'pending','causal_or_clean_window_verified':False}
(HERE/'production_checks.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
