"""Trusted GitHub Actions controller. Model never receives a Git write credential."""
import base64
import datetime as dt
import io
import json
import os
from pathlib import Path, PurePosixPath
import sys
import urllib.request
import zipfile
from claim_turn import acquire, fields, git, set_fields

ROOT=Path(__file__).resolve().parents[1]
NOW=lambda: dt.datetime.now(dt.timezone.utc)


def output(key,value):
    if os.getenv('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'],'a',encoding='utf-8') as f:
            f.write(f'{key}={value}\n')


def summary(text):
    print(text)
    if os.getenv('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f:
            f.write(text+'\n')


def api(path):
    req=urllib.request.Request('https://api.github.com/'+path,headers={
        'Authorization':'Bearer '+os.environ['GH_TOKEN'],
        'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'})
    return json.load(urllib.request.urlopen(req,timeout=30))


def auth_git():
    # Ephemeral process configuration, not .git/config or an agent-visible file.
    encoded=base64.b64encode(('x-access-token:'+os.environ['GH_TOKEN']).encode()).decode()
    os.environ.update(GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
                      GIT_CONFIG_VALUE_0='AUTHORIZATION: basic '+encoded)
    git(ROOT,'config','user.name','github-actions[bot]')
    git(ROOT,'config','user.email','41898282+github-actions[bot]@users.noreply.github.com')


def preflight():
    state=fields((ROOT/'state/turn.md').read_text(encoding='utf-8'))
    reasons=[]
    if os.getenv('RESEARCH_AUTORUN','').lower()!='true': reasons.append('RESEARCH_AUTORUN is not true: paid research is disabled')
    if os.getenv('HAS_OPENAI_KEY','').lower()!='true': reasons.append('OPENAI_API_KEY repository secret is missing')
    if os.getenv('REQUEST_MODE')=='check': reasons.append('Check-only request: no model invocation')
    if state.get('next')!='codex': reasons.append('Waiting for '+state.get('next','unknown'))
    if state.get('lock')!='none': reasons.append('Existing lock: '+state.get('lock','unknown')+'; inspect owning run before recovery')
    stamp=state.get('cloud_last_started')
    if stamp and (NOW()-dt.datetime.fromisoformat(stamp)).total_seconds()<5*3600:
        reasons.append('Less than five hours since the last cloud research start')
    ready=not reasons
    output('run',str(ready).lower())
    summary('## Cloud readiness\n'+('\n'.join('- '+x for x in reasons) if reasons else '- Ready for research')+
            '\n\nThis preflight did not call OpenAI. The runner is hosted by GitHub, independent of the user PC.')


def claim():
    auth_git()
    result=acquire(ROOT,'codex',{'cloud_last_started':NOW().isoformat(timespec='seconds'),
                               'github_run_id':os.environ['GITHUB_RUN_ID']})
    output('acquired',str(result['status']=='acquired').lower())
    if result['status']=='acquired':
        output('claim_sha',result['commit']);output('run_id',result['run_id'])
        (ROOT/'.local').mkdir(exist_ok=True)
    summary(json.dumps(result))


def safe_artifact_files(raw):
    data={}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if sum(x.file_size for x in archive.infolist())>100_000_000:
            raise ValueError('Checkpoint too large')
        for item in archive.infolist():
            name=item.filename
            path=PurePosixPath(name)
            if item.is_dir(): continue
            if path.is_absolute() or '..' in path.parts or '\\' in name:
                raise ValueError('Unsafe artifact path')
            if item.file_size>20_000_000: raise ValueError('File too large')
            if (item.external_attr>>16)&0o170000==0o120000: raise ValueError('Symlink in artifact')
            data[name]=archive.read(item)
    return data


def download_checkpoint():
    repo=os.environ['GITHUB_REPOSITORY']; run=os.environ['GITHUB_RUN_ID']
    records=api(f'repos/{repo}/actions/runs/{run}/artifacts')['artifacts']
    record=next((x for x in records if x['name']=='research-checkpoint-'+run and not x['expired']),None)
    if not record: return None
    # Obtain a temporary signed download URL without forwarding the GitHub token to blob storage.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs): return None
    req=urllib.request.Request(record['archive_download_url'],headers={'Authorization':'Bearer '+os.environ['GH_TOKEN']})
    try:
        response=urllib.request.build_opener(NoRedirect).open(req,timeout=30)
        raw=response.read()
    except urllib.error.HTTPError as exc:
        if exc.code!=302: raise
        location=exc.headers['Location']
        if not location.startswith('https://'): raise ValueError('Non-HTTPS artifact redirect')
        raw=urllib.request.urlopen(location,timeout=60).read()
    return safe_artifact_files(raw)


def publish():
    auth_git()
    expected=os.environ['EXPECTED_CLAIM_SHA']; run_id=os.environ['EXPECTED_RUN_ID']
    git(ROOT,'fetch','origin','main')
    if git(ROOT,'rev-parse','origin/main')!=expected or git(ROOT,'rev-parse','HEAD')!=expected:
        raise RuntimeError('Remote changed during research; checkpoint retained, no overwrite attempted')
    turnpath=ROOT/'state/turn.md'; text=turnpath.read_text(encoding='utf-8'); state=fields(text)
    if state.get('lock')!='codex' or state.get('run_id')!=run_id:
        raise RuntimeError('Lease owner changed; cannot publish or release it')
    checkpoint=download_checkpoint()
    result={'next':'user','stage':'decision','summary':'Cloud run failed or produced no checkpoint; inspect Actions before retrying.'}
    modified=[]
    round_dir='outputs/round_'+state['round']+'/'
    allowed_state={'state/claims_ledger.csv','state/threat_register.md','state/decision_log.md'}
    if checkpoint:
        for name,content in checkpoint.items():
            if name=='.local/cloud_result.json': continue
            if (ROOT/name).is_file() and (ROOT/name).read_bytes()==content:
                continue  # Preserved baseline files include .gitkeep placeholders.
            allowed=name.startswith(round_dir) or name.startswith('outputs/reviews/') or name=='outputs/progress_log.md' or name in allowed_state
            if not allowed:
                if not (ROOT/name).is_file() or (ROOT/name).read_bytes()!=content:
                    raise ValueError('Out-of-scope change: '+name)
                continue
            if PurePosixPath(name).suffix.lower() not in {'.md','.csv','.json','.txt','.sql','.py'}:
                raise ValueError('Unexpected output type: '+name)
            if name=='state/decision_log.md':
                old=(ROOT/name).read_text(encoding='utf-8').replace('\r\n','\n')
                new=content.decode('utf-8').replace('\r\n','\n')
                if not new.startswith(old): raise ValueError('Decision log must be append-only')
            dest=ROOT/name; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(content);modified.append(name)
        if os.environ.get('PRODUCE_RESULT')=='success' and '.local/cloud_result.json' in checkpoint:
            proposed=json.loads(checkpoint['.local/cloud_result.json'])
            pairs={'codex':{'production','revision'},'claude':{'claude_review'},'user':{'decision'}}
            if proposed.get('next') not in pairs or proposed.get('stage') not in pairs[proposed['next']]:
                raise ValueError('Invalid requested transition')
            if not isinstance(proposed.get('summary'),str): raise ValueError('Missing summary')
            result=proposed
    if result['next']=='claude':
        mandatory=['verification_report.md']
        if state['round']=='03': mandatory+=['main_design.md','plan.md','regulatory_dataset.csv','concurrent_events.csv','signal_chain.csv','novelty_recheck.md','precedents_table.md','confounders.csv','threats_tests.md']
        missing=[x for x in mandatory if not (ROOT/round_dir/x).is_file()]
        reviews=list((ROOT/'outputs/reviews').glob('round_'+state['round']+'_review_*.md'))
        if missing or not reviews:
            result={'next':'codex','stage':'production','summary':'Handoff incomplete; finish required deliverables and independent internal review.'}
    if int(state.get('reviews_this_round','0'))>=2:
        result={'next':'user','stage':'decision','summary':'Two Claude reviews reached; user decision required.'}
    note=' '.join(result['summary'].split())[:700]
    turnpath.write_text(set_fields(text,{'next':result['next'],'stage':result['stage'],'lock':'none',
        'lock_since':'','run_id':'','updated_by':'github-actions','updated_at':NOW().isoformat(timespec='seconds'),
        'note':note}),encoding='utf-8',newline='\n')
    receipt=ROOT/round_dir/('cloud_run_'+os.environ['GITHUB_RUN_ID']+'.md')
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text('# Cloud run checkpoint\n\n'+note+'\n\nNext: '+result['next']+'\n',encoding='utf-8')
    git(ROOT,'add','--',*modified,'state/turn.md',str(receipt.relative_to(ROOT)))
    git(ROOT,'commit','-m','r'+state['round']+': publish cloud research checkpoint')
    git(ROOT,'push','origin','HEAD:main')
    summary('## Research checkpoint published\n\n'+note+'\n\nNext: '+result['next'])


if __name__=='__main__':
    {'preflight':preflight,'claim':claim,'publish':publish}[sys.argv[1]]()
