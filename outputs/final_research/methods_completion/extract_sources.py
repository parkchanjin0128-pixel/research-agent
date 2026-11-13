from pathlib import Path
import shutil, requests, hashlib, json, datetime
import fitz
from bs4 import BeautifulSoup
base=Path('outputs/final_research/methods_completion'); src=base/'sources'
records=[]
for key,url in [('handley2017','https://terpconnect.umd.edu/~limao/aer_final.pdf'),('moser2012','https://www.petramoser.net/uploads/6/9/4/2/69429445/moservoena12_aer.pdf'),('malani2015','https://julianreif.com/research/reif.jpube.2015.anticipation.pdf')]:
    path=src/(key+'.pdf'); shutil.copyfile(Path('work/stage3')/(key+'.pdf'),path)
    records.append({'id':key,'url':url,'acquisition':'copied_existing_primary_cache','original_local_path':str(Path('work/stage3')/(key+'.pdf')),'path':str(path)})
for key,url in [('finkelstein2004','https://economics.mit.edu/sites/default/files/2022-08/Static%20and%20Dynamic%20Effects%20of%20Health%20Policy-Eviden.pdf'),('blume2013','https://pmc.ncbi.nlm.nih.gov/articles/PMC3711884/pdf/nihms419385.pdf')]:
    response=requests.get(url,timeout=50); path=src/(key+'.pdf')
    if response.ok and response.content.startswith(b'%PDF'):
        path.write_bytes(response.content); records.append({'id':key,'url':url,'acquisition':'downloaded_primary','path':str(path)})
    else:
        print(key,'DOWNLOAD_FAILED',response.status_code,response.headers.get('Content-Type'),len(response.content))
for key in ['blume2013']:
    for ext in ['html','txt']: shutil.copyfile(Path('work/stage3')/(key+'.'+ext),src/(key+'.'+ext))
for rec in records:
    p=Path(rec['path']); rec['sha256']=hashlib.sha256(p.read_bytes()).hexdigest(); doc=fitz.open(p); rec['pdf_pages']=len(doc)
    (src/(rec['id']+'.txt')).write_text('\n'.join('[PDF PAGE %d]\n%s'%(i+1,page.get_text()) for i,page in enumerate(doc)),encoding='utf-8')
(base/'source_manifest.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'producer':'/root/nov13_precedent_completion','verification_status':'pending_independent_verification','sources':records},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(records,indent=2))
