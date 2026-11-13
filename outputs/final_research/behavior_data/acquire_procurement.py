"""Three official procurement notices. Stores factual excerpts, no personal contacts.
University notices are public procurement selection outcomes; no cash-flow inference.
"""
from acquire_behavior import ROOT, RAW, Parser, write_csv
import urllib.request, subprocess, json, re, hashlib, datetime

SOURCES=[
 dict(id='szu_gpu_2018',url='https://bidding.szu.edu.cn/info/1022/20188.htm',title='GPU集群加速卡采购',organization='深圳大学',supplier='北京西普阳光教育科技股份有限公司',project_id='',field='GPU/计算基础设施'),
 dict(id='njust_hpc_jan2019',url='https://zbpt.njust.edu.cn/cjgg/5723.jhtml',title='高性能计算硬件系统采购项目',organization='南京理工大学',supplier='南京杰世欣计算机科技有限公司',project_id='ZZ0266-G18HZ0422/TC189JAWE',field='高性能计算硬件/模拟仿真'),
 dict(id='njust_hpc_mar2019',url='https://zbpt.njust.edu.cn/cjgg/5853.jhtml',title='高性能计算机集群采购项目',organization='南京理工大学',supplier='南京信同诚信息技术有限公司',project_id='ZZ0313-G18HZ0588/TC199J0C2',field='高性能计算集群/科研基础设施'),
]

def fetch(url):
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as r:
   data=r.read()
  return data.decode('utf-8-sig'), 'urllib; decoded UTF-8'
 except Exception:
  literal="'"+url.replace("'","''")+"'"
  result=subprocess.run(['pwsh','-NoProfile','-Command',f'[Console]::OutputEncoding=[Text.UTF8Encoding]::new();[Console]::Write((Invoke-WebRequest -Uri {literal} -TimeoutSec 25).Content)'],check=True,capture_output=True)
  return result.stdout.decode('utf-8-sig'), 'Invoke-WebRequest; Content returned as UTF-8 text'

def capture(pattern,text):
 m=re.search(pattern,text)
 if not m: raise ValueError(f'Expected field absent: {pattern}')
 return m

def main():
 out=[]; meta=[]; lineitems=[]
 for s in SOURCES:
  s=dict(s)
  try:
   html,method=fetch(s['url'])
   parser=Parser(); parser.feed(html); compact=re.sub(r'\s+','',''.join(parser.all))
   assert s['title'] in compact and s['supplier'] in compact
   snippets=[s['title'],s['supplier']]
   row=dict(source_id=s['id'],project_id=s['project_id'],title=s['title'],field=s['field'],organization=s['organization'],supplier=s['supplier'])
   if s['id'].startswith('szu'):
    publication=capture(r'2018/12/11\d{2}:\d{2}:\d{2}',compact).group(0)
    decision=capture(r'定标时间[：:]2018年12月7日',compact).group(0)
    amount=capture(r'中标金额[：:]人民币([\d,.]+)元',compact)
    budget=capture(r'预算金额[：:]人民币([\d,.]+)元',compact)
    row.update(publication_date='2018-12-11',solicitation_date='',decision_date='2018-12-07',decision_date_label='定标时间',award_notice_date='',amount_cny=float(amount.group(1).replace(',','')),budget_cny=float(budget.group(1).replace(',','')),decision_clock='explicit supplier-selection date; initial research/procurement decision date unknown')
    snippets += [publication,decision,amount.group(0),budget.group(0)]
   else:
    publication=capture(r'发布日期[：:](\d{4}-\d{2}-\d{2})',compact)
    solicitation=capture(r'招标公告日期[：:](\d{4})年(\d{2})月(\d{2})日',compact)
    award=capture(r'中标公告日期[：:](\d{4})年(\d{2})月(\d{2})日',compact)
    amount=capture(r'中标价格[：:]([\d,.]+)万元',compact)
    to_date=lambda m:'-'.join(m.groups())
    row.update(publication_date=publication.group(1),solicitation_date=to_date(solicitation),decision_date='',decision_date_label='',award_notice_date=to_date(award),amount_cny=float(amount.group(1).replace(',',''))*10000,budget_cny='',decision_clock='explicit solicitation and award-notice dates; supplier-selection day and initial project choice not reported')
    snippets += [publication.group(0),solicitation.group(0),award.group(0),amount.group(0),s['project_id']]
   row.update(amount_type='selected supplier award amount; not paid expenditure',source_url=s['url'])
   if s['id'].startswith('njust'):
    assert len(parser.rows)==51
    # Both notices report 17 specification rows, 17 quantity rows, 17 unit-price rows.
    (RAW/(s['id']+'_equipment_tables.json')).write_text(json.dumps(parser.rows,ensure_ascii=False,indent=2),encoding='utf-8')
    for i in range(17):
     spec,qty,price=parser.rows[i],parser.rows[i+17],parser.rows[i+34]
     assert spec[:-1]==qty[:-1]==price[:-1]
     item=dict(source_id=s['id'],item_number=i+1,item_name=' / '.join(spec[:-1]),specification_verbatim=spec[-1],quantity_verbatim=qty[-1],unit_price_verbatim=price[-1],source_url=s['url'])
     quantity=re.match(r'([\d.]+)',qty[-1]);unit=re.match(r'([\d.]+)万元',price[-1])
     item.update(quantity_numeric=float(quantity.group(1)) if quantity else '',unit_price_cny=float(unit.group(1))*10000 if unit else '')
     lineitems.append(item)
    row['equipment_detail_status']='17 equipment/service specification, quantity, and unit-price rows extracted'
   else:row['equipment_detail_status']='GPU model, number of cards, and manufacturer not reported in this notice'
   # No raw HTML/contact sections retained for these contact-heavy procurement pages.
   evidence='\n'.join(snippets)+'\n'
   name=s['id']+'_factual_excerpt.txt'; (RAW/name).write_text(evidence,encoding='utf-8')
   s.update(status='downloaded_and_extracted',method=method,html_text_sha256=hashlib.sha256(html.encode('utf-8')).hexdigest(),retained_evidence='raw/'+name,evidence_sha256=hashlib.sha256(evidence.encode('utf-8')).hexdigest(),retention='factual excerpts only; personal names/contact blocks excluded',retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
   out.append(row)
  except Exception as e:
   s.update(status='failed',error=str(e))
  meta.append(s)
 write_csv('procurement_records.csv',out)
 write_csv('procurement_lineitems.csv',lineitems)
 (ROOT/'procurement_sources.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'sources':meta,'records':out},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
