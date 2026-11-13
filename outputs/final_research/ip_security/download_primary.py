import concurrent.futures, hashlib, json, pathlib, requests, zipfile
from bs4 import BeautifulSoup
BASE=pathlib.Path(__file__).resolve().parent
OUT=BASE/'sources'; OUT.mkdir(exist_ok=True)
jobs={}
for s in ['734-3','734-7','734-8','734-10','734-13','734-15','772-1']:
    jobs[f'cfr2018_{s}.xml']=f'https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-sec{s}.xml'
jobs['ecra2018.html']='https://www.govinfo.gov/content/pkg/PLAW-115publ232/html/PLAW-115publ232.htm'
jobs['anprm2018.html']='https://www.govinfo.gov/content/pkg/FR-2018-11-19/html/2018-25221.htm'
jobs['wipo_patents_faq.html']='https://www.wipo.int/en/web/patents/faq_patents'
jobs['gao_shroff_zhang_2026.html']='https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5373282'
jobs['coelli2025.html']='https://www.sciencedirect.com/science/article/pii/S0022199625001278'
jobs['crosignani2025.pdf']='https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1096.pdf'
jobs['liu2025.pdf']='https://www.hbs.edu/ris/Publication%20Files/25-004_ea198f96-5936-443e-b30c-55d8570a3900.pdf'
jobs['zhan_lee_gan2026.html']='https://www.eaerweb.org/selectArticleInfo.do?ano=JE0001_2026_v30n1_59&article_a_no=JE0001_2026_v30n1_59'
for y in ['20170101','20180101','20190101','20200101']:
    for kind in ['scheme','concordancelist']:
        name=f'ipc_{kind}_{y}.zip'
        jobs[name]=f'https://www.wipo.int/classifications/data/ipc/ITSupport_and_download_area/{y}/MasterFiles/{name}'
def download(job):
    name,url=job
    try:
        r=requests.get(url,timeout=45)
        record=dict(name=name,url=url,status=r.status_code,final_url=r.url,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
        if r.status_code==200 and '/error' not in r.url:
            (OUT/name).write_bytes(r.content)
            if name.endswith('.zip') and zipfile.is_zipfile(OUT/name):
                with zipfile.ZipFile(OUT/name) as z:
                    record['members']=z.namelist()
                    for member in z.namelist():
                        if member.lower().endswith('.xml') and ('en_' in member.lower() or 'concord' in member.lower()):
                            (OUT/(name[:-4]+'_'+pathlib.Path(member).name)).write_bytes(z.read(member))
            elif name.endswith(('.html','.xml')):
                (OUT/(name+'.txt')).write_text(BeautifulSoup(r.content,'html.parser').get_text(' ',strip=True),encoding='utf-8')
        return record
    except Exception as e:
        return dict(name=name,url=url,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    records=list(pool.map(download,jobs.items()))
manifest_path=BASE/'source_manifest.json'
prior=json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else []
merged={r['name']:r for r in prior}
merged.update({r['name']:r for r in records})
manifest_path.write_text(json.dumps(list(merged.values()),ensure_ascii=False,indent=2),encoding='utf-8')
for r in records: print(r['name'],r.get('status'),r.get('bytes'),r.get('error',''),r.get('members',''))
