import csv,json,pathlib
from lxml import etree
BASE=pathlib.Path(__file__).resolve().parent
S=BASE/'sources'
def sym(s):
    return f'{s[:4]} {int(s[4:8])}/{s[8:10]}' if s.endswith('0000') else s
def title(n):
    # Read the entry's own text body; do not fold child IPC entries into its title.
    own=n.xpath('./*[local-name()="textBody"]')
    return ' '.join(' '.join(own[0].itertext()).split()) if own else ''
schemes={}
for y in ['20170101','20180101','20190101','20200101']:
    t=etree.parse(str(S/f'ipc_scheme_{y}_EN_ipc_scheme_{y}.xml'))
    schemes[y]={n.get('symbol'):n for n in t.xpath('//*[@symbol]')}
edges=[]; excerpts=[]
for y in ['20180101','20190101','20200101']:
    t=etree.parse(str(S/f'ipc_concordancelist_{y}_ipc_concordancelist_{y}.xml'))
    old=t.getroot().get('from-version')
    for n in t.getroot():
        targets=list(n)
        if not any(x.get('to-symbol','').startswith(('G06N0020','G06F0040')) for x in targets): continue
        excerpts.append(etree.tostring(n,encoding='unicode',pretty_print=True))
        for to in targets:
            a=n.get('from-symbol'); b=to.get('to-symbol')
            edges.append(dict(from_version=old,to_version=y,project=n.get('revision-project'),from_symbol=a,from_display=sym(a),from_modification=n.get('modification'),to_symbol=b,to_display=sym(b),to_modification=to.get('modification'),default_reclassification=to.get('default-reclassification'),from_title=title(schemes[old][a]) if a in schemes[old] else '',to_title=title(schemes[y][b]) if b in schemes[y] else '',from_exists_in_2017=a in schemes['20170101']))
with (BASE/'historical_crosswalk_edges.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=list(edges[0]));w.writeheader();w.writerows(edges)
(BASE/'historical_crosswalk_edges.json').write_text(json.dumps(edges,ensure_ascii=False,indent=2),encoding='utf-8')
(BASE/'rcl_exact_extracts.xml.txt').write_text('\n'.join(excerpts),encoding='utf-8')
symbols=sorted({r['from_symbol'] for r in edges}|{r['to_symbol'] for r in edges})
scheme_rows=[]
for y,d in schemes.items():
    for s in symbols:
        n=d.get(s)
        if n is not None:
            scheme_rows.append(dict(version=y,symbol=s,display=sym(s),kind=n.get('kind'),edition=n.get('edition'),own_title=title(n)))
(BASE/'historical_scheme_rows.json').write_text(json.dumps(scheme_rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('RCL edges',len(edges),'scheme rows',len(scheme_rows))
for r in edges:
    print(r['from_version'],r['from_display'],'->',r['to_display'],r['project'],r['default_reclassification'])
