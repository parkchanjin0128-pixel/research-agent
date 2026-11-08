"""Acquire a research turn with a fast-forward Git push. No force/reset/rebase."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid


def git(root, *args):
    env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GCM_INTERACTIVE='never')
    p = subprocess.run(['git', '-c', 'credential.interactive=never', '-C', str(root), *args],
                       capture_output=True, text=True, encoding='utf-8', env=env)
    if p.returncode:
        raise RuntimeError('git ' + ' '.join(args) + ': ' + p.stderr.strip())
    return p.stdout.strip()


def fields(text):
    block = re.search(r'```\s*\n(.*?)```', text, re.S)
    if not block:
        raise ValueError('Missing turn state block')
    return dict(re.findall(r'^([a-z_]+):[ \t]*([^\n]*)', block.group(1), re.M))


def set_fields(text, updates):
    match = re.search(r'```\s*\n(.*?)```', text, re.S)
    if not match:
        raise ValueError('Missing turn state block')
    body = match.group(1)
    for name, value in updates.items():
        pattern = r'^' + re.escape(name) + r':[^\n]*'
        if re.search(pattern, body, re.M):
            body = re.sub(pattern, lambda _: name + ': ' + value, body, flags=re.M)
        else:
            body += name + ': ' + value + '\n'
    return text[:match.start(1)] + body + text[match.end(1):]


def acquire(root, actor, extra_fields=None):
    # Read-only early refusal means obsolete Claude schedulers cannot mutate v2.
    initial = fields((root/'state/turn.md').read_text(encoding='utf-8'))
    if initial.get('workflow_version') == 'codex_internal_v1' and actor != 'codex':
        return {'status': 'skipped', 'reason': 'Claude is retired from codex_internal_v1; no claim or publish is permitted'}
    if git(root, 'status', '--porcelain'):
        raise RuntimeError('Local changes exist; preserve and inspect them before claiming')
    if git(root, 'branch', '--show-current') != 'main':
        raise RuntimeError('Expected the dedicated main checkout')
    git(root, 'fetch', 'origin', 'main')
    if git(root, 'rev-list', '--count', 'origin/main..HEAD') != '0':
        raise RuntimeError('Local unpushed commits exist; reconcile explicitly, do not auto-rebase')
    git(root, 'merge', '--ff-only', 'origin/main')
    path = root/'state/turn.md'
    text = path.read_text(encoding='utf-8')
    state = fields(text)
    if state.get('workflow_version') == 'codex_internal_v1':
        if actor != 'codex':
            return {'status': 'skipped', 'reason': 'Claude is retired from codex_internal_v1; no claim or publish is permitted'}
        from review_pipeline import validate
        queue = json.loads((root/'state/work_queue.json').read_text(encoding='utf-8'))
        errors = validate(root, queue, state)
        if errors:
            raise RuntimeError('Invalid queue/turn: ' + '; '.join(errors))
    if state.get('lock') != 'none':
        stamp = state.get('lock_since', '')
        try:
            age = dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(stamp)
        except (ValueError, TypeError):
            raise RuntimeError('Locked turn has an invalid timestamp; inspect it without stealing the lock')
        if age.total_seconds() > 6*3600:
            return {'status': 'skipped', 'reason': 'Lock is older than six hours; no theft: confirm owning run ended and quiesced before explicit recovery', 'lock': state.get('lock'), 'run_id': state.get('run_id')}
    if state.get('next') != actor or state.get('lock') != 'none':
        return {'status':'skipped', 'next':state.get('next'), 'lock':state.get('lock')}
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    run_id = str(uuid.uuid4())
    updates={'lock':actor, 'lock_since':now, 'updated_at':now,
             'updated_by':actor, 'run_id':run_id}
    forbidden = {'workflow_version', 'next', 'stage', 'lock', 'lock_since', 'updated_at', 'updated_by', 'run_id'}
    if forbidden.intersection(extra_fields or {}):
        raise ValueError('Extra fields cannot override lease ownership or workflow state')
    updates.update(extra_fields or {})
    path.write_text(set_fields(text, updates), encoding='utf-8')
    git(root, 'add', '--', 'state/turn.md')
    git(root, 'commit', '-m', 'ops: claim '+actor+' turn '+run_id)
    # If another writer won, push fails: leave the commit intact and stop.
    git(root, 'push', 'origin', 'HEAD:main')
    return {'status':'acquired', 'actor':actor, 'run_id':run_id,
            'commit':git(root, 'rev-parse', 'HEAD')}


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser=argparse.ArgumentParser()
    parser.add_argument('--actor', choices=['codex','claude'], required=True)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    root=args.repo.resolve()
    # Excludes concurrent local invocations, including a second check in the same second.
    guard=root/'.git/research-claim.guard'
    try:
        fd=os.open(guard, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        print(json.dumps({'status':'skipped','reason':'local claim in progress'})); return
    try:
        os.close(fd)
        print(json.dumps(acquire(root,args.actor),ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({'status':'error','error':str(exc)},ensure_ascii=False))
        sys.exit(1)
    finally:
        guard.unlink(missing_ok=True)


if __name__=='__main__':
    main()
