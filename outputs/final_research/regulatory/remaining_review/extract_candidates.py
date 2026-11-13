from pathlib import Path
import xml.etree.ElementTree as ET
import re,json,hashlib

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[3]
SRC=BASE/'outputs/final_research/ip_security/sources/cfr2018_part774.xml'
root=ET.parse(SRC).getroot()
app=root.find('PART/APPENDIX')
nodes=list(app)
starts=[]
for j,n in enumerate(nodes):
    if n.tag=='FP' and n.get('SOURCE')=='FP-2':
        s=''.join(n.itertext()).strip()
        if re.match(r'^[0-9][A-E][0-9]{3}\b',s): starts.append((j,s[:5]))
targets=['2D001','4A004','4D001','4D994','4E001','5A001','5A002','5D001','5D002','7A005','7D003','7D004','9D103','1C351','1C353','1C991','3A001','3A991','2B007','6A006']
(OUT/'source_extracts').mkdir(parents=True,exist_ok=True)
manifest=[]
for k,(j,eccn) in enumerate(starts):
    if eccn not in targets: continue
    end=starts[k+1][0] if k+1<len(starts) else len(nodes)
    chunks=[]
    pages=set()
    for n in nodes[j:end]:
        chunks.append(re.sub(r'\s+',' ',''.join(n.itertext())).strip())
        pages.update(x.get('P') for x in n.iter('PRTPAGE'))
    text='\n'.join(chunks)+'\n'
    path=OUT/'source_extracts'/f'2018_{eccn}.txt'
    path.write_text(text,encoding='utf-8')
    manifest.append({'eccn':eccn,'file':str(path.relative_to(BASE)).replace('\\','/'),'source':'https://www.govinfo.gov/content/pkg/CFR-2018-title15-vol2/xml/CFR-2018-title15-vol2-part774.xml','source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'entry_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'page_markers_inside':sorted(pages),'scope':'기계추출 전문. 실제 검토는 행별 actual_scope 및 메모가 지정한 단락에 한정.'})
(OUT/'extract_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'extracted':len(manifest),'entries':[x['eccn'] for x in manifest]},ensure_ascii=False))
