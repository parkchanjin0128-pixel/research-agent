from pathlib import Path
import hashlib, json, zipfile, sys
import xml.etree.ElementTree as ET
from pypdf import PdfReader

root = Path(__file__).resolve().parent
build = root / '.build'
old = root / 'deliverables' / '최종_연구발표.pptx'
new = root / 'deliverables' / '최종_연구발표_문헌보완.pptx'
pdf = root / 'deliverables' / '최종_연구발표.pdf'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def package_snapshot(p):
    with zipfile.ZipFile(p) as z:
        visible = {n: sha(z.read(n)) for n in z.namelist() if n.startswith('ppt/') and '/notes' not in n and not n.startswith('ppt/notes') and not n.endswith('.rels')}
        return visible

def normalized_slides(p):
    result = {}
    with zipfile.ZipFile(p) as z:
        for n in z.namelist():
            if not (n.startswith('ppt/slides/slide') and n.endswith('.xml')):
                continue
            tree = ET.fromstring(z.read(n))
            rel_name = str(Path(n).parent / '_rels' / (Path(n).name + '.rels')).replace('\\','/')
            rels = {}
            if rel_name in z.namelist():
                rels = {rel.attrib['Id']: rel.attrib.get('Target','') for rel in ET.fromstring(z.read(rel_name))}
            for parent in tree.iter():
                for key,value in list(parent.attrib.items()):
                    if key.startswith('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'):
                        parent.attrib[key] = rels.get(value,value)
                for child in list(parent):
                    if child.tag.rsplit('}',1)[-1] == 'creationId':
                        parent.remove(child)
            result[n] = sha(ET.tostring(tree))
    return result

if sys.argv[1] == 'before':
    data = {'old_pptx_sha256': sha(old.read_bytes()), 'pdf_sha256': sha(pdf.read_bytes()), 'visible_parts': package_snapshot(old), 'png': {p.name: sha(p.read_bytes()) for p in (build / 'previews').glob('*.png')}}
    (build / 'notes_revision_before.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print('기존 본문·차트·렌더·PDF 해시 보존')
else:
    before = json.loads((build / 'notes_revision_before.json').read_text(encoding='utf-8'))
    current = package_snapshot(new)
    slide_keys = [n for n in before['visible_parts'] if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
    chart_keys = [n for n in before['visible_parts'] if '/charts/' in n and n.endswith('.xml')]
    png = {p.name: sha(p.read_bytes()) for p in (build / 'previews').glob('*.png')}
    notes_ok = {}
    with zipfile.ZipFile(new) as z:
        for n in [13,14,24]:
            text = z.read(f'ppt/notesSlides/notesSlide{n}.xml').decode('utf-8')
            notes_ok[str(n)] = all(x in text for x in ['200개', 'any-APP', '재추정하지'])
        for n in [4,37]:
            text = z.read(f'ppt/notesSlides/notesSlide{n}.xml').decode('utf-8')
            notes_ok[str(n)] = all(x in text for x in ['85쪽', '6210408', '7042518', 'KZ'])
    result = {
        '판정': '노트·근거 개정, 화면 본문 유지',
        'old_pptx_sha256': before['old_pptx_sha256'],
        'new_pptx_sha256': sha(new.read_bytes()),
        '본문_slide_xml_원시해시동일': len(slide_keys)==38 and all(current.get(n)==before['visible_parts'][n] for n in slide_keys),
        '추적ID및관계ID_정규화후_본문38장_XML동일': len(slide_keys)==38 and normalized_slides(old)==normalized_slides(new),
        'native_chart_xml_7개_동일': len(chart_keys)==7 and all(current.get(n)==before['visible_parts'][n] for n in chart_keys),
        '렌더38장_해시동일': len(png)==38 and png==before['png'],
        '기존_nativePDF_해시동일': sha(pdf.read_bytes())==before['pdf_sha256'],
        'PDF페이지': len(PdfReader(str(pdf)).pages),
        '필수노트반영': notes_ok,
        'PDF처리': '무작위 creationId를 제외하고 관계ID를 동일 연결대상으로 정규화한 본문·차트 XML 및 38장 렌더 해시 동일이므로 기존 native PDF 유지. GUI/COM 재호출 없음.',
    }
    result['통과'] = all([result['추적ID및관계ID_정규화후_본문38장_XML동일'],result['native_chart_xml_7개_동일'],result['렌더38장_해시동일'],result['기존_nativePDF_해시동일'],all(notes_ok.values()),result['PDF페이지']==38])
    (build / 'notes_revision_verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not result['통과']:
        raise SystemExit(1)
