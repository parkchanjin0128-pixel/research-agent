"""Integration checks in a disposable local remote; never touches the real remote."""
from pathlib import Path
import subprocess, tempfile, sys, json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from claim_turn import fields
assert fields('```\nlock_since:\nreviews_this_round: 0\n```')['reviews_this_round']=='0'

script=Path(__file__).resolve().parent/'claim_turn.py'
def run(*args, cwd=None):
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,encoding='utf-8')
    if p.returncode: raise RuntimeError(p.stdout+p.stderr)
    return p.stdout.strip()

with tempfile.TemporaryDirectory(prefix='research_harness_test_') as tmp:
    base=Path(tmp); remote=base/'remote.git'; a=base/'a'; b=base/'b'
    run('git','init','--bare',str(remote))
    run('git','clone',str(remote),str(a))
    run('git','checkout','-b','main',cwd=a)
    run('git','config','user.name','Harness Test',cwd=a)
    run('git','config','user.email','test@example.invalid',cwd=a)
    (a/'state').mkdir()
    (a/'state/turn.md').write_text('# Turn\n```\nnext: codex\nround: 03\nstage: production\nlock: none\nlock_since:\nreviews_this_round: 0\n```\n',encoding='utf-8')
    run('git','add','state/turn.md',cwd=a); run('git','commit','-m','test init',cwd=a)
    run('git','push','-u','origin','main',cwd=a)
    run('git','clone','-b','main',str(remote),str(b))
    run('git','config','user.name','Harness Test',cwd=b)
    run('git','config','user.email','test@example.invalid',cwd=b)
    def claim(repo,actor): return json.loads(run(sys.executable,str(script),'--repo',str(repo),'--actor',actor).splitlines()[-1])
    assert claim(a,'claude')['status']=='skipped'
    first=claim(a,'codex'); assert first['status']=='acquired'
    assert claim(b,'codex')['status']=='skipped'
    assert claim(b,'claude')['status']=='skipped'
    (b/'uncommitted.txt').write_text('preserve me')
    p=subprocess.run([sys.executable,str(script),'--repo',str(b),'--actor','codex'],capture_output=True,text=True)
    assert p.returncode==1 and (b/'uncommitted.txt').read_text()=='preserve me'
    print(json.dumps({'passed':['wrong actor skips','claim pushes lock','second checkout respects remote lock','reviewer respects producer lock','dirty worktree preserved'],'count':5}))
