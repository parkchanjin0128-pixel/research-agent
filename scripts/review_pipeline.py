"""Codex-only research-unit checkpoints; no model call, Git write, or truth promotion.

An agent identity is an auditable session/subagent id, not a role name. Receipts
document provenance; they do not authenticate it. The orchestrator must create
separate, context-isolated agents and verify the ids against the run record.
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

from claim_turn import fields, set_fields

VERSION = 'codex_internal_v1'
PHASES = {'production', 'verification', 'review', 'revision', 'decision'}
STATUSES = {'pending', 'partial', 'blocked', 'complete', 'escalated'}
ROOT = Path(__file__).resolve().parents[1]
ROUND03_REQUIREMENTS = {
    'uvl_2019_14610': ['outputs/round_03/part744_uvl_14610_source.md'],
    'regulatory_audit_41': ['outputs/round_03/regulatory_dataset.csv'],
    'novelty_recheck': ['outputs/round_03/novelty_recheck.md'],
    'precedents': ['outputs/round_03/precedents_table.md'],
    'main_design': ['outputs/round_03/main_design.md'],
    'concurrent_cn': ['outputs/round_03/concurrent_events.csv', 'outputs/round_03/signal_chain.csv', 'outputs/round_03/confounders.csv'],
    'placebo_crosswalk': ['outputs/round_03/placebo_crosswalk.md'],
    'inference_mde_plan': ['outputs/round_03/inference_mde_plan.md', 'outputs/round_03/threats_tests.md'],
    'data_feasibility': ['outputs/round_03/data_tests/feasibility_report.md'],
    'round03_integration': ['outputs/round_03/plan.md', 'outputs/round_03/verification_report.md'],
}


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def output_path(root, value):
    if not isinstance(value, str):
        raise ValueError('Artifact path must be a string')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '\\' in value or not value.startswith('outputs/'):
        raise ValueError('Artifact/report must be a repository-relative outputs/ path')
    target = root.joinpath(*path.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('Artifact resolves outside repository')
    if not target.is_file() or not target.stat().st_size:
        raise ValueError('Missing or empty artifact/report: ' + value)
    return target


def identity(value):
    if not isinstance(value, str) or not value.strip() or value in {'codex', 'claude', 'verifier', 'referee', 'orchestrator', 'unknown', 'none'}:
        raise ValueError('Use an actual distinct agent/session id, not a role label')
    return value


def artifact_hashes(unit):
    return {row['path']: row['sha256'] for row in unit.get('artifacts', [])}


def check_response(root, unit, receipt, review):
    path = receipt.get('response_path')
    target = output_path(root, path)
    if not path.endswith('_response.md') or path in artifact_hashes(unit) or path == review.get('report_path'):
        raise ValueError('Response must be a separate *_response.md artifact')
    if receipt.get('response_sha256') != digest(target):
        raise ValueError('Response digest missing or stale')
    blocks = re.findall(r'```json\s*\n(.*?)```', target.read_text(encoding='utf-8'), re.S)
    if len(blocks) != 1:
        raise ValueError('Response needs exactly one structured JSON block')
    body = json.loads(blocks[0])
    actor = identity(body.get('author_id'))
    judges = {r.get('agent_id') for r in unit.get('history', []) if r.get('phase') in {'verification', 'review'}}
    judges |= {review.get('agent_id'), (unit.get('verification') or {}).get('agent_id')}
    if actor in judges:
        raise ValueError('Response must be authored by orchestrator/producer, not a verifier/referee')
    if body.get('unit_id') != unit['id'] or body.get('review_path') != review.get('report_path') or body.get('review_sha256') != review.get('report_sha256'):
        raise ValueError('Response does not identify this unit/current review digest')
    if body.get('phase') != receipt.get('phase'):
        raise ValueError('Response phase does not match this review/revision checkpoint')
    responses = body.get('responses')
    if not isinstance(responses, list):
        raise ValueError('Response needs an explicit responses list')
    expected = {f['id'] for f in review.get('findings', [])}
    ids = [r.get('finding_id') for r in responses if isinstance(r, dict)]
    if len(ids) != len(responses) or len(set(ids)) != len(ids) or set(ids) != expected:
        raise ValueError('Response must cover every current review finding exactly once')
    for row in responses:
        if not row.get('response') or not (row.get('location') and row.get('verification_plan') or row.get('not_adopted_reason')):
            raise ValueError('Each response needs content and location/verification_plan or not_adopted_reason')
    if not expected and not body.get('no_findings_reason'):
        raise ValueError('No-findings review still needs an explicit reasoned no-findings response')
    if 'responses' in receipt and receipt['responses'] != responses:
        raise ValueError('Receipt responses disagree with the actual response file')
    return body


def check_history(root, unit):
    history = unit.get('history')
    if not isinstance(history, list):
        raise ValueError('Unit needs durable phase history')
    writers, judges, report_paths, report_hashes, response_authors = set(), set(), set(), set(), set()
    response_paths, response_hashes = set(), set()
    last_verification = last_review = None
    expected_phase = 'production'
    for row in history:
        phase = row.get('phase')
        if phase != expected_phase:
            raise ValueError('History omits or reorders required production/verification/review/revision phases')
        actor = identity(row.get('agent_id'))
        if phase in {'production', 'revision'}:
            writers.add(actor)
            if phase == 'revision':
                if not last_review:
                    raise ValueError('Revision history lacks its preceding review')
                body = check_response(root, unit, row, last_review)
                response_authors.add(body['author_id'])
            expected_phase = 'verification'
        elif phase in {'verification', 'review'}:
            report = output_path(root, row.get('report_path'))
            checksum = row.get('report_sha256')
            if not checksum or digest(report) != checksum:
                raise ValueError('Historical judgment report missing, changed, or unhashed')
            if actor in judges or row['report_path'] in report_paths or checksum in report_hashes:
                raise ValueError('Every verification/referee cycle needs a fresh agent, report path and report digest')
            judges.add(actor); report_paths.add(row['report_path']); report_hashes.add(checksum)
            if phase == 'verification':
                last_verification = row
                expected_phase = 'review'
            else:
                if not last_verification:
                    raise ValueError('Review history lacks its preceding verification')
                body = check_response(root, unit, row, row)
                response_authors.add(body['author_id'])
                last_review = row
                accepted = row.get('verdict') == 'accept' and not any(f.get('status') == 'open' for f in row.get('findings', [])) and last_verification.get('verdict') in {'verified', 'not_applicable'}
                expected_phase = 'complete' if accepted else 'revision'
        else:
            raise ValueError('Unsupported history phase')
        if phase in {'review', 'revision'}:
            if row['response_path'] in response_paths or row['response_sha256'] in response_hashes:
                raise ValueError('Every review/revision needs a fresh response path and content digest')
            response_paths.add(row['response_path']); response_hashes.add(row['response_sha256'])
    if writers != set(unit.get('producer_ids', [])) or writers & judges or response_authors & judges:
        raise ValueError('Producer/response/judgment provenance is missing or roles overlap')
    if sum(r['phase'] == 'revision' for r in history) != unit.get('revision_count') or sum(r['phase'] == 'review' for r in history) != unit.get('review_count'):
        raise ValueError('History cannot omit/reset revision or review counts')
    for kind in ('verification', 'review'):
        current = unit.get(kind)
        if current and not any({k: v for k, v in r.items() if k != 'recorded_at'} == current for r in history if r['phase'] == kind):
            raise ValueError('Current '+kind+' receipt is missing from durable history')
    expected = 'complete' if unit.get('status') == 'complete' else 'revision' if unit.get('status') == 'escalated' else unit.get('phase')
    if expected_phase != expected:
        raise ValueError('Current phase/status disagrees with durable phase history')


def ensure_fresh_judgment(unit, receipt):
    for old in unit.get('history', []):
        if old.get('phase') in {'verification', 'review'} and any(receipt.get(key) == old.get(key) for key in ('agent_id', 'report_path', 'report_sha256')):
            raise ValueError('New judgment requires a fresh agent id, report path, and report content digest')


def check_receipt(root, unit, receipt, kind):
    identity(receipt.get('agent_id'))
    if receipt['agent_id'] in unit.get('producer_ids', []):
        raise ValueError(kind + ' cannot be performed by any producer/reviser of this unit')
    if kind == 'review' and receipt['agent_id'] == (unit.get('verification') or {}).get('agent_id'):
        raise ValueError('Referee and verifier must be different agents')
    other_role = 'verification' if kind == 'review' else 'review'
    if receipt['agent_id'] in {r.get('agent_id') for r in unit.get('history', []) if r.get('phase') == other_role}:
        raise ValueError('Verifier/referee roles cannot be reused by the same agent across revisions')
    report = output_path(root, receipt.get('report_path'))
    if receipt['report_path'] in artifact_hashes(unit):
        raise ValueError('Independent report cannot be the producer artifact itself')
    if kind == 'review' and receipt['report_path'] == (unit.get('verification') or {}).get('report_path'):
        raise ValueError('Verifier/referee must save separate reports')
    if receipt.get('report_sha256') != digest(report):
        raise ValueError(kind + ' report digest missing or stale')
    if receipt.get('artifact_hashes') != artifact_hashes(unit) or not unit.get('artifacts'):
        raise ValueError(kind + ' must cover exactly the current artifact digests')
    if kind == 'verification':
        if receipt.get('verdict') not in {'verified', 'partially_verified', 'contradicted', 'unverifiable', 'not_applicable'}:
            raise ValueError('Missing verification verdict')
        checks = receipt.get('source_checks')
        if not isinstance(checks, list) or not checks:
            raise ValueError('Verification needs explicit independent source checks (or a reasoned no-new-facts entry)')
        if any(not isinstance(c, dict) or not c.get('claim') or not c.get('source') or not c.get('result') for c in checks):
            raise ValueError('Each source check needs claim, source, and result')
        if receipt.get('verdict') == 'not_applicable' and not receipt.get('no_new_facts_reason'):
            raise ValueError('No-new-facts verification needs a reason')
    else:
        if receipt.get('verdict') not in {'accept', 'minor_revision', 'major_revision', 'reject'}:
            raise ValueError('Missing review verdict')
        if not isinstance(receipt.get('findings'), list):
            raise ValueError('Review needs an explicit findings list, including an empty one')
        for finding in receipt['findings']:
            if not isinstance(finding, dict) or not finding.get('id') or finding.get('severity') not in {'critical', 'blocker', 'major', 'minor'} or finding.get('status') not in {'open', 'resolved'} or not finding.get('reason'):
                raise ValueError('Review findings need id, severity, status, and reason')
        check_response(root, unit, receipt, receipt)


def unit_errors(root, unit, allow_changed_artifacts=False):
    errors = []
    try:
        if unit.get('status') not in STATUSES or unit.get('phase') not in PHASES:
            raise ValueError('Invalid status/phase')
        if unit['status'] == 'complete' and unit['phase'] != 'review':
            raise ValueError('Completed unit must have reached independent review')
        if unit['status'] == 'escalated' and unit['phase'] != 'decision':
            raise ValueError('Escalated unit must await a user decision')
        required = unit.get('required_artifacts')
        if not isinstance(required, list) or not required or any(not isinstance(p, str) or not p.startswith('outputs/') for p in required):
            raise ValueError('Unit needs explicit required artifact paths')
        if unit.get('revision_count', -1) not in {0, 1, 2} or not isinstance(unit.get('review_count'), int) or unit['review_count'] < 0:
            raise ValueError('Invalid review/revision count')
        producers = unit.get('producer_ids')
        if not isinstance(producers, list) or len(producers) != len(set(producers)):
            raise ValueError('Invalid producer_ids')
        for actor in producers:
            identity(actor)
        check_history(root, unit)
        for row in unit.get('artifacts', []):
            if row.get('author_id') not in producers:
                raise ValueError('Artifact author missing from producer provenance')
            if not allow_changed_artifacts and digest(output_path(root, row.get('path'))) != row.get('sha256'):
                raise ValueError('Artifact digest changed without production/revision receipt')
        if unit['phase'] in {'verification', 'review'} or unit['status'] == 'complete':
            if not unit.get('artifacts') or not producers:
                raise ValueError('Phase requires a produced artifact and author identity')
            paths = artifact_hashes(unit)
            if not set(unit.get('required_artifacts', [])).issubset(paths):
                raise ValueError('Production receipt does not cover required unit artifacts')
        if unit['phase'] == 'review' or unit['status'] == 'complete':
            check_receipt(root, unit, unit.get('verification') or {}, 'verification')
        if unit['status'] == 'complete':
            check_receipt(root, unit, unit.get('review') or {}, 'review')
            if unit['verification']['verdict'] not in {'verified', 'not_applicable'}:
                raise ValueError('Unresolved factual verification cannot complete a unit')
            review = unit['review']
            if review['verdict'] != 'accept' or any(f['status'] == 'open' for f in review['findings']):
                raise ValueError('Only an explicit accept with every finding resolved can complete a unit')
    except (ValueError, TypeError, KeyError) as exc:
        errors.append(str(exc))
    return errors


def validate(root, queue, state=None, revising_unit=None):
    errors = []
    if queue.get('schema_version') != VERSION or queue.get('round') != '03':
        errors.append('Unsupported queue version/round')
    units = queue.get('units')
    if not isinstance(units, list) or not units:
        return errors + ['Queue requires nonempty units']
    ids = [u.get('id') for u in units]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        errors.append('Unit ids must be nonempty and unique')
    lookup = {u.get('id'): u for u in units}
    for unit in units:
        errors += [str(unit.get('id')) + ': ' + e for e in unit_errors(root, unit, unit.get('id') == revising_unit and unit.get('phase') == 'revision')]
        deps = unit.get('dependencies')
        if not isinstance(deps, list) or any(d not in lookup or d == unit.get('id') for d in deps):
            errors.append(str(unit.get('id')) + ': Invalid dependencies')
        if unit.get('status') == 'complete' and any(lookup.get(d, {}).get('status') != 'complete' for d in deps or []):
            errors.append(str(unit.get('id')) + ': Complete unit has unfinished dependencies')
    def visit(key, trail):
        if key in trail:
            raise ValueError('Dependency cycle: ' + ' -> '.join(trail + [key]))
        for dep in lookup.get(key, {}).get('dependencies', []):
            if dep in lookup:
                visit(dep, trail + [key])
    try:
        for key in lookup:
            visit(key, [])
    except ValueError as exc:
        errors.append(str(exc))
    if state is not None:
        if state.get('workflow_version') != VERSION or state.get('next') not in {'codex', 'user'} or state.get('stage') not in PHASES or state.get('lock') not in {'codex', 'none'}:
            errors.append('Invalid Codex-only turn state')
        if state.get('round') != queue.get('round'):
            errors.append('Turn/queue round mismatch')
        if state.get('active_unit') not in lookup and state.get('active_unit') != 'none':
            errors.append('Unknown active_unit')
        try:
            if int(state.get('internal_review_count', '-1')) != sum(u.get('review_count', 0) for u in units):
                errors.append('internal_review_count disagrees with unit review counts')
        except ValueError:
            errors.append('Invalid internal_review_count')
    return errors


def round_coverage_errors(queue):
    """Live CLI/terminal guard, separate from small pure-function unit fixtures."""
    if queue.get('round') != '03':
        return ['Required round coverage is not configured for this round']
    lookup = {u.get('id'): u for u in queue.get('units', []) if isinstance(u, dict)}
    errors = []
    for key, paths in ROUND03_REQUIREMENTS.items():
        unit = lookup.get(key)
        if not unit:
            errors.append('Required round03 work track missing: '+key)
        elif not set(paths).issubset(unit.get('required_artifacts', [])):
            errors.append('Required round03 artifact coverage missing: '+key)
    integrated = lookup.get('round03_integration')
    if integrated and not (set(ROUND03_REQUIREMENTS)-{'round03_integration'}).issubset(integrated.get('dependencies', [])):
        errors.append('Round03 integration must depend on every required work track')
    return errors


def plan(root, queue, limit=3):
    if limit < 1:
        raise ValueError('Plan limit must be positive')
    errors = validate(root, queue)
    if errors:
        raise ValueError('; '.join(errors))
    lookup = {u['id']: u for u in queue['units']}
    ready = [u for u in queue['units'] if u['status'] in {'pending', 'partial'} and u['phase'] != 'decision' and all(lookup[d]['status'] == 'complete' for d in u['dependencies'])]
    # Oldest touched first prevents the regulatory audit monopolizing each run.
    ready.sort(key=lambda u: (u.get('last_touched') or '', u.get('priority', 50), u['id']))
    return [{'id': u['id'], 'phase': u['phase'], 'title': u['title']} for u in ready[:limit]]


def advance(root, queue, unit_id, receipt):
    """Return a new queue; caller validates an owned lease and CAS-publishes it."""
    errors = validate(root, queue, revising_unit=unit_id)
    if errors:
        raise ValueError('; '.join(errors))
    result = copy.deepcopy(queue)
    unit = next((u for u in result['units'] if u['id'] == unit_id), None)
    if not unit:
        raise ValueError('Unknown unit')
    if unit['status'] in {'complete', 'blocked', 'escalated'}:
        raise ValueError('Unit is not runnable; no implicit reopening or unblock')
    phase = unit['phase']
    if receipt.get('phase') != phase:
        raise ValueError('Receipt phase differs from queued phase')
    actor = identity(receipt.get('agent_id'))
    lookup = {u['id']: u for u in queue['units']}
    if any(lookup[d]['status'] != 'complete' for d in unit['dependencies']):
        raise ValueError('Unit dependencies are not complete')
    if phase in {'production', 'revision'}:
        paths = receipt.get('artifacts')
        if not isinstance(paths, list) or not paths or not set(unit.get('required_artifacts', [])).issubset(paths):
            raise ValueError('Production/revision must supply all required artifact paths')
        judged = {r.get('agent_id') for r in unit.get('history', []) if r.get('phase') in {'verification', 'review'}}
        if actor in judged | {(unit.get('verification') or {}).get('agent_id'), (unit.get('review') or {}).get('agent_id')}:
            raise ValueError('A verifier/referee cannot become the reviser of the unit it judged')
        if phase == 'revision':
            if unit['revision_count'] >= 2:
                raise ValueError('Two revision cycles exhausted; user decision required')
            response = check_response(root, unit, receipt, unit.get('review') or {})
            if not isinstance(receipt.get('responses'), list) or receipt['responses'] != response['responses']:
                raise ValueError('Revision needs the actual response file finding-response list')
            open_ids = {f['id'] for f in (unit.get('review') or {}).get('findings', []) if f['status'] == 'open'}
            if not open_ids.issubset({r.get('finding_id') for r in receipt['responses'] if isinstance(r, dict) and r.get('response')}):
                raise ValueError('Revision must respond to every open review finding')
            unit['revision_count'] += 1
        if actor not in unit['producer_ids']:
            unit['producer_ids'].append(actor)
        unit['artifacts'] = [{'path': p, 'sha256': digest(output_path(root, p)), 'author_id': actor} for p in paths]
        unit['verification'] = None
        unit['review'] = None
        unit['phase'] = 'verification'
        unit['status'] = 'partial'
    elif phase == 'verification':
        record = copy.deepcopy(receipt)
        record['report_sha256'] = digest(output_path(root, record.get('report_path')))
        ensure_fresh_judgment(unit, record)
        check_receipt(root, unit, record, 'verification')
        unit['verification'] = record
        # Even failed facts reach an independent referee; never auto-promote claims.
        unit['phase'] = 'review'
    elif phase == 'review':
        record = copy.deepcopy(receipt)
        record['report_sha256'] = digest(output_path(root, record.get('report_path')))
        ensure_fresh_judgment(unit, record)
        check_receipt(root, unit, record, 'review')
        unit['review'] = record
        unit['review_count'] += 1
        unresolved = any(f['status'] == 'open' for f in record['findings'])
        failed = unresolved or record['verdict'] != 'accept' or unit['verification']['verdict'] not in {'verified', 'not_applicable'}
        if failed and unit['revision_count'] >= 2:
            unit.update(status='escalated', phase='decision')
        elif failed:
            unit.update(status='partial', phase='revision')
        else:
            unit.update(status='complete', phase='review')
    else:
        raise ValueError('Decision is a user boundary, not an agent-completable phase')
    unit['last_touched'] = now()
    recorded = record if phase in {'verification', 'review'} else receipt
    unit.setdefault('history', []).append(dict(recorded, recorded_at=unit['last_touched']))
    result['updated_at'] = now()
    errors = validate(root, result)
    if errors:
        raise ValueError('; '.join(errors))
    return result


def owned_lease(state, run_id):
    if state.get('workflow_version') != VERSION or state.get('next') != 'codex' or state.get('lock') != 'codex' or not run_id or run_id in {'none', ''} or state.get('run_id') != run_id:
        raise ValueError('An exact owned Codex run_id is required; never reuse another run lock')


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'plan', 'advance'])
    parser.add_argument('--repo', type=Path, default=ROOT)
    parser.add_argument('--unit')
    parser.add_argument('--receipt', type=Path, help='JSON with phase, actual agent_id, and artifacts or report/verdict; no secrets')
    parser.add_argument('--run-id', help='Exact current lease owner, required for advance')
    parser.add_argument('--limit', type=int, default=3)
    args = parser.parse_args()
    root = args.repo.resolve()
    path = root/'state/work_queue.json'
    queue = json.loads(path.read_text(encoding='utf-8'))
    turnpath = root/'state/turn.md'
    text = turnpath.read_text(encoding='utf-8')
    state = fields(text)
    coverage_errors = round_coverage_errors(queue)
    if coverage_errors:
        print(json.dumps({'ok': False, 'errors': coverage_errors}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    if args.command == 'validate':
        errors = validate(root, queue, state)
        print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False, indent=2))
        raise SystemExit(bool(errors))
    if args.command == 'plan':
        print(json.dumps({'ready': plan(root, queue, args.limit)}, ensure_ascii=False, indent=2))
        return
    owned_lease(state, args.run_id)
    receipt = json.loads(args.receipt.read_text(encoding='utf-8')) if args.receipt else {}
    queue = advance(root, queue, args.unit, receipt)
    unit = next(u for u in queue['units'] if u['id'] == args.unit)
    updates = {'active_unit': unit['id'], 'stage': unit['phase'], 'internal_review_count': str(sum(u['review_count'] for u in queue['units'])), 'updated_at': now(), 'updated_by': 'codex'}
    if unit['status'] == 'escalated':
        updates.update(next='user', stage='decision', note='Unit '+unit['id']+': two revisions exhausted; unresolved review/factual issues require user decision.')
    else:
        ready = plan(root, queue, 1)
        if ready:
            updates.update(active_unit=ready[0]['id'], stage=ready[0]['phase'])
        elif all(u['status'] == 'complete' for u in queue['units']):
            updates.update(next='user', stage='decision', active_unit='none', note='Required research units independently checked/reviewed. Gate/freeze/next-round decision still belongs to user.')
    # Files are a local checkpoint only. The caller publishes with exact-head CAS.
    path.write_text(json.dumps(queue, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    turnpath.write_text(set_fields(text, updates), encoding='utf-8')
    print(json.dumps({'unit': unit['id'], 'status': unit['status'], 'phase': unit['phase'], 'next': updates.get('next', state['next'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
