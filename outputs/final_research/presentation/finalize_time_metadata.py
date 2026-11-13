from pathlib import Path
import json, hashlib, zipfile
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parent
deck = root / 'deliverables' / '최종_연구발표_시간정정.pptx'
prior = root / 'deliverables' / '최종_연구발표_문헌보완.pptx'
pdf = root / 'deliverables' / '최종_연구발표.pdf'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def note_texts(p):
    with zipfile.ZipFile(p) as z:
        return {n: ''.join(ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{n}.xml')).itertext()) for n in range(1,39)}

a, b = note_texts(prior), note_texts(deck)
changed = [n for n in a if a[n] != b[n]]
assert changed == [1], changed
assert b[1] == a[1].replace('본문은 약 37분이며,','본문 권장시간은 38분 45초이며,')
assert '약 37분' not in (root/'발표원고.md').read_text(encoding='utf-8')
assert '약 37분' not in (root/'content.mjs').read_text(encoding='utf-8')

record = root / '제작_확인기록.md'
block = f'''\n\n## 최종 발표시간 정정\n\n첫 장 발표자 노트·발표원고·본문 원천의 “본문 권장시간은 38분 45초”를 동기화했다. PPTX에서 텍스트가 바뀐 발표자 노트는 1장뿐이며, 나머지 37장 노트와 결론은 같다.\n\n최종 PPTX: `deliverables/최종_연구발표_시간정정.pptx`, {deck.stat().st_size:,}바이트, SHA256 `{sha(deck)}`. 기존 native PDF는 {pdf.stat().st_size:,}바이트, SHA256 `{sha(pdf)}`로 유지한다.\n\n`.build/time_revision_verification.json`에서 추적ID·관계ID를 정규화한 본문38장 XML, 차트7개 XML, PNG38장 해시의 동일성과 PDF38페이지·기존 PDF 해시 유지를 확인했다. `.build/validation_시간정정.json`은 패키지·레이아웃·차트·재import 검증 통과 기록이다. `verify_time_revision.py`와 `finalize_time_metadata.py`를 보존했다. 이번 정정에는 GUI/COM을 호출하지 않았다.\n'''
text = record.read_text(encoding='utf-8')
if '\n\n## 최종 발표시간 정정\n' in text:
    text = text.split('\n\n## 최종 발표시간 정정\n')[0]
record.write_text(text + block,encoding='utf-8')

manifest = json.loads((root/'presentation_manifest.json').read_text(encoding='utf-8'))
manifest['최종PPTX'] = 'deliverables/최종_연구발표_시간정정.pptx'
manifest['개정범위'] = '첫 장 발표시간을 38분45초로 동기화. 나머지37장 노트·화면본문·차트·기존PDF 동일.'
manifest['시간정정_검증'] = '.build/time_revision_verification.json'
manifest['텍스트변경_발표자노트'] = changed
paths = [manifest['최종PPTX']] + [x['경로'] for x in manifest['파일'] if not x['경로'].endswith('.pptx')]
manifest['파일'] = [{'경로':p,'바이트':(root/p).stat().st_size,'sha256':sha(root/p)} for p in paths]
(root/'presentation_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'최종PPTX':manifest['최종PPTX'],'바이트':deck.stat().st_size,'sha256':sha(deck),'변경노트':changed,'기존PDFsha256':sha(pdf),'확인':'다른37장노트·결론변경없음'},ensure_ascii=False,indent=2))
