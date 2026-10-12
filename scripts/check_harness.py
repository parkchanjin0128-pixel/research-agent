import hashlib
import json
from pathlib import Path
from claim_turn import fields

root=Path(__file__).resolve().parents[1]
required=['AGENTS.md','CLAUDE_REVIEWER.md','docs/OPERATIONS.md',
          'prompts/round_03.md','prompts/gpt_scheduled_run.md',
          'outputs/progress_log.md','outputs/round_03/resume_notes.md']
errors=[f'Missing {p}' for p in required if not (root/p).is_file()]
manifest=json.loads((root/'state/import_manifest.json').read_text(encoding='utf-8'))
for row in manifest['files']:
    p=root/row['path']
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
        errors.append('Import mismatch: '+row['path'])
state=fields((root/'state/turn.md').read_text(encoding='utf-8'))
if state.get('next') not in ['codex','claude','user']: errors.append('Invalid next')
if state.get('lock') not in ['codex','claude','none']: errors.append('Invalid lock')
if not 0<=int(state.get('reviews_this_round','-1'))<=2: errors.append('Invalid review count')
print(json.dumps({'ok':not errors,'imported_files':len(manifest['files']),
                  'turn':state,'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
