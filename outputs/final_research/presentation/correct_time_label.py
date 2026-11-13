from pathlib import Path

root = Path(__file__).resolve().parent
content = root / 'content.mjs'
text = content.read_text(encoding='utf-8')
assert text.count('본문은 약 37분이며,') == 1
content.write_text(text.replace('본문은 약 37분이며,','본문 권장시간은 38분 45초이며,'),encoding='utf-8')
builder = root / 'build_deck.mjs'
text = builder.read_text(encoding='utf-8')
text = text.replace('deliverables/최종_연구발표_문헌보완.pptx','deliverables/최종_연구발표_시간정정.pptx').replace('validation_문헌보완.json','validation_시간정정.json')
builder.write_text(text,encoding='utf-8')
verification = (root / 'verify_notes_revision.py').read_text(encoding='utf-8')
verification = verification.replace("old = root / 'deliverables' / '최종_연구발표.pptx'", "old = root / 'deliverables' / '최종_연구발표_문헌보완.pptx'")
verification = verification.replace("new = root / 'deliverables' / '최종_연구발표_문헌보완.pptx'", "new = root / 'deliverables' / '최종_연구발표_시간정정.pptx'")
verification = verification.replace('notes_revision_before.json','time_revision_before.json').replace('notes_revision_verification.json','time_revision_verification.json')
verification = verification.replace("notes_ok = {}", "notes_ok = {}")
verification = verification.replace("for n in [13,14,24]:", "text = z.read('ppt/notesSlides/notesSlide1.xml').decode('utf-8')\n        notes_ok['1_발표시간'] = '본문 권장시간은 38분 45초' in text and '약 37분' not in text\n        for n in [13,14,24]:")
verification = verification.replace("'판정': '노트·근거 개정, 화면 본문 유지'", "'판정': '첫 장 발표시간 문구 정정, 화면 본문 유지'")
(root / 'verify_time_revision.py').write_text(verification,encoding='utf-8')
print('첫 장 원문과 새 시간정정 산출물 경로 설정')
