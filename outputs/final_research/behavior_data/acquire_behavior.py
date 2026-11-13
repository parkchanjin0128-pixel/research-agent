"""Bounded official-data pilot. No account, purchase, or message submission.
Run with bundled Python. Outputs are approval/public-notice outcomes, NOT applications.
"""
from pathlib import Path
import urllib.request, hashlib, json, datetime, re, csv, subprocess
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parent
RAW=ROOT/'raw'; RAW.mkdir(exist_ok=True,parents=True)
SOURCES=[
 dict(id='nsfc_life_key_2017',year=2017,type='nsfc_award',url='https://www.nsfc.gov.cn/p1/2853/3102/72662.html'),
 dict(id='nsfc_life_key_2018',year=2018,type='nsfc_award',url='https://www.nsfc.gov.cn/p1/2853/3102/72653.html'),
 dict(id='nsfc_life_key_2019',year=2019,type='nsfc_award',url='https://www.nsfc.gov.cn/p1/2853/3102/72645.html'),
 dict(id='rd_hpc_2018',year=2018,type='rd_proposed_award',url='https://www.htrdc.com/gjszx/u/cms/gjszx/201809/06203731l9zx.pdf'),
 dict(id='rd_transformative_2019',year=2019,type='rd_proposed_award',url='https://service.most.gov.cn/u/cms/static/201912/13182523l275.pdf'),
 dict(id='rd_transformative_2017',year=2017,type='rd_proposed_award',url='https://service.most.gov.cn/u/cms/static/201805/04191201qlc0.pdf'),
]
class Parser(HTMLParser):
 def __init__(self):
  super().__init__(); self.rows=[]; self.row=None; self.cell=None; self.all=[]
 def handle_starttag(self,tag,attrs):
  if tag=='tr': self.row=[]
  if tag in ('td','th'): self.cell=[]
 def handle_data(self,data):
  self.all.append(data)
  if self.cell is not None: self.cell.append(data)
 def handle_endtag(self,tag):
  if tag in ('td','th') and self.cell is not None:
   if self.row is not None: self.row.append(re.sub(r'\s+',' ',''.join(self.cell)).strip())
   self.cell=None
  if tag=='tr' and self.row is not None:
   self.rows.append(self.row); self.row=None

def download(s):
 suffix='.pdf' if s['url'].endswith('.pdf') else '.html'
 p=RAW/(s['id']+suffix)
 if not p.exists():
  req=urllib.request.Request(s['url'],headers={'User-Agent':'Mozilla/5.0 (public research data pilot)'})
  try:
   with urllib.request.urlopen(req,timeout=25) as r:
    data=r.read(); final=r.url; ctype=r.headers.get('Content-Type','')
   s['download_method']='urllib'
  except Exception:
   # Windows network proxy/OS certificate trust is available to PowerShell.
   # All URLs/paths come from the fixed source list, quoted as PowerShell literals.
   quote=lambda x: "'"+str(x).replace("'","''")+"'"
   subprocess.run(['pwsh','-NoProfile','-Command',f'Invoke-WebRequest -Uri {quote(s["url"])} -OutFile {quote(p)} -TimeoutSec 25'],check=True,capture_output=True)
   data=p.read_bytes(); final=s['url']; ctype='downloaded by PowerShell Invoke-WebRequest'
   s['download_method']='PowerShell Invoke-WebRequest with OS trust'
  p.write_bytes(data)
 else: data=p.read_bytes(); final=s['url']; ctype='cached'
 s.update(local=str(p.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),final_url=final,content_type=ctype,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 return p,data

def write_csv(name,records):
 if records:
  with (ROOT/name).open('w',encoding='utf-8-sig',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(records[0])); w.writeheader(); w.writerows(records)

def main():
 records=[]; rd=[]; meta=[]
 for s in SOURCES:
  s=dict(s)
  try:
   p,data=download(s)
   if s['type']=='nsfc_award':
    html=data.decode('utf-8-sig',errors='replace'); par=Parser(); par.feed(html)
    text=' '.join(par.all); date=re.search(r'日期[：:]\s*(\d{4}-\d{2}-\d{2})',text)
    s['page_date']=date.group(1) if date else ''
    out=[]
    for row in par.rows:
     if len(row)>=6 and row[0].strip().isdigit() and re.fullmatch(r'\d{8,12}',row[1].strip()):
      amount=re.sub(r'[,，\s]','',row[-1])
      if not re.fullmatch(r'\d+(\.\d+)?',amount): raise ValueError(f'Unexpected amount {row}')
      # PI names are deliberately omitted from the derived dataset.
      out.append(dict(source_id=s['id'],program='NSFC life sciences key projects',allocation_year=s['year'],row_number=int(row[0]),project_id=row[1],id_type='科学部编号; not validated as NSFC approval number',title=row[2],field='生命科学部;重点项目',organization=row[-2],amount_cny_10000=float(amount),amount_type='approved_direct_cost',page_publication_date=s['page_date'],application_date='',approval_date='',decision_clock='award year only; page date is retrospective disclosure',source_url=s['url']))
    if not out: raise ValueError('No valid table records extracted')
    assert sorted(x['row_number'] for x in out)==list(range(1,len(out)+1))
    assert len({x['project_id'] for x in out})==len(out)
    s['rows']=len(out); s['amount_cny_10000']=sum(x['amount_cny_10000'] for x in out); records+=out
    (RAW/(s['id']+'_text.txt')).write_text(text,encoding='utf-8')
   else:
    import pdfplumber
    with pdfplumber.open(p) as pdf:
     txt='\n\n'.join(page.extract_text() or '' for page in pdf.pages)
     tables=[page.extract_tables() for page in pdf.pages]
    (RAW/(s['id']+'_text.txt')).write_text(txt,encoding='utf-8')
    (RAW/(s['id']+'_tables.json')).write_text(json.dumps(tables,ensure_ascii=False,indent=2),encoding='utf-8')
    out=[]
    for page in tables:
     for table in page:
      for row in table:
       if len(row)>=5 and str(row[0]).strip().isdigit() and re.fullmatch(r'20\d\dYF[A-Z]\d+',str(row[1]).strip()):
        clean=lambda x: str(x or '').replace('\n','').strip()
        has_amount=len(row)==7
        out.append(dict(source_id=s['id'],program='National key R&D proposed awards',allocation_year=s['year'],row_number=int(row[0]),project_id=clean(row[1]),id_type='项目编号',title=clean(row[2]),field='高性能计算' if s['id']=='rd_hpc_2018' else '变革性技术关键科学问题',organization=clean(row[3]),amount_cny_10000=float(clean(row[5])) if has_amount else '',amount_type='proposed_central_fiscal_funding' if has_amount else 'not_reported',duration_years=float(clean(row[-1]).replace('年','')),page_publication_date='',application_date='',approval_date='',decision_clock='proposed-award list year; PDF has no verified exact disclosure/application/approval date',source_url=s['url']))
    if not out: raise ValueError('No PDF project rows')
    assert sorted(x['row_number'] for x in out)==list(range(1,len(out)+1))
    s['rows']=len(out); s['amount_cny_10000']=sum(x['amount_cny_10000'] for x in out if x['amount_cny_10000']!='') if any(x['amount_cny_10000']!='' for x in out) else None
    rd+=out
    s['pdf_extracted']=True
   s['status']='downloaded_and_extracted'
  except Exception as e:
   s['status']='failed'; s['error']=str(e)
  meta.append(s)
 (ROOT/'sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 write_csv('nsfc_approved_records.csv',records)
 write_csv('national_rd_proposed_records.csv',rd)
 print(json.dumps(meta,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
