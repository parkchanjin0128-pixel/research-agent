import hashlib
import json
from pathlib import Path
import sys
import tomllib
from claim_turn import fields
from review_pipeline import VERSION, round_coverage_errors, validate

if __name__ == '__main__' and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

root=Path(__file__).resolve().parents[1]
required=['AGENTS.md','docs/OPERATIONS.md','docs/INTERNAL_REVIEW.md',
          'prompts/round_03.md','prompts/gpt_scheduled_run.md',
          'outputs/progress_log.md','outputs/round_03/resume_notes.md',
          'state/work_queue.json','scripts/review_pipeline.py']
errors=[f'Missing {p}' for p in required if not (root/p).is_file()]
manifest=json.loads((root/'state/import_manifest.json').read_text(encoding='utf-8'))
for row in manifest['files']:
    p=root/row['path']
    if row['path']=='outputs/progress_log.md':
        if not p.is_file(): errors.append('Missing active progress log')
        continue  # Mutable log; the original import digest is retained for historical provenance.
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:
        errors.append('Import mismatch: '+row['path'])
state=fields((root/'state/turn.md').read_text(encoding='utf-8'))
if state.get('workflow_version') != VERSION: errors.append('Unexpected workflow version')
try:
    queue=json.loads((root/'state/work_queue.json').read_text(encoding='utf-8'))
    errors.extend(validate(root,queue,state))
    errors.extend(round_coverage_errors(queue))
except (OSError,ValueError,TypeError,KeyError) as exc:
    errors.append('Invalid/missing work queue: '+str(exc))
try:
    if not 0<=int(state.get('reviews_this_round','-1'))<=2: errors.append('Invalid historical Claude review count')
except ValueError:
    errors.append('Invalid historical Claude review count')
roles={'data_engineer','identification_designer','lit_scout','policy_archivist','referee','verifier'}
for role in sorted(roles):
    path=root/'.codex/agents'/(role+'.toml')
    try:
        config=tomllib.loads(path.read_text(encoding='utf-8'))
        if config.get('name')!=role or any(not isinstance(config.get(k),str) or not config[k].strip() for k in ['description','developer_instructions']):
            errors.append('Incomplete custom agent config: '+role)
        if 'model' in config or 'model_reasoning_effort' in config:
            errors.append('Custom agent must inherit parent subscription model: '+role)
    except (OSError,tomllib.TOMLDecodeError) as exc:
        errors.append('Invalid custom agent '+role+': '+str(exc))
print(json.dumps({'ok':not errors,'imported_files':len(manifest['files']),
                  'turn':state,'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
