"""Observable protocol boundaries; standard library only, no real remote/model."""
import copy
import contextlib
import io
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

import claim_turn
import review_pipeline as pipe
from test_support import test_temp_root


def fresh_unit(key='u'):
    return {'id': key, 'title': key, 'status': 'pending', 'phase': 'production',
            'priority': 10, 'dependencies': [], 'required_artifacts': ['outputs/'+key+'.md'],
            'producer_ids': [], 'artifacts': [], 'verification': None, 'review': None,
            'revision_count': 0, 'review_count': 0, 'history': [], 'last_touched': None}


def queue_for(*units):
    return {'schema_version': pipe.VERSION, 'round': '03', 'units': list(units)}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=test_temp_root())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'outputs').mkdir()
        (self.root/'state').mkdir()
        (self.root/'outputs/u.md').write_text('A narrow produced claim.', encoding='utf-8')
        self.queue = queue_for(fresh_unit())

    def produced(self, queue=None, agent='producer-session'):
        return pipe.advance(self.root, queue or self.queue, 'u',
                            {'phase': 'production', 'agent_id': agent, 'artifacts': ['outputs/u.md']})

    def verify_receipt(self, queue, actor=None, cycle=0):
        actor = actor or 'verifier-session-'+str(cycle)
        path = 'outputs/verify_'+str(cycle)+'.md'
        (self.root/path).write_text('Independent primary-source comparison for version '+str(cycle), encoding='utf-8')
        return {'phase': 'verification', 'agent_id': actor, 'report_path': path,
                'artifact_hashes': pipe.artifact_hashes(queue['units'][0]), 'verdict': 'verified',
                'source_checks': [{'claim': 'bounded fact', 'source': 'https://example.gov/rule', 'result': 'matched original text'}]}

    def verified(self, queue=None, cycle=0):
        queue = queue or self.produced()
        return pipe.advance(self.root, queue, 'u', self.verify_receipt(queue, cycle=cycle))

    def review_receipt(self, queue, fail=False, actor=None, cycle=0):
        actor = actor or 'referee-session-'+str(cycle)
        path = 'outputs/review_'+str(cycle)+'.md'
        (self.root/path).write_text('Separate referee report for version '+str(cycle), encoding='utf-8')
        receipt = {'phase': 'review', 'agent_id': actor, 'report_path': path,
                'artifact_hashes': pipe.artifact_hashes(queue['units'][0]),
                'verdict': 'reject' if fail else 'accept',
                'findings': [{'id': 'R1', 'severity': 'blocker', 'status': 'open', 'reason': 'Unresolved identification problem'}] if fail else []}
        return self.add_response(queue, receipt, receipt, 'outputs/review_'+str(cycle)+'_response.md')

    def add_response(self, queue, receipt, review, path):
        responses = [{'finding_id': f['id'], 'response': 'Explicitly address '+f['id'],
                      'location': 'outputs/u.md: limitations', 'verification_plan': 'New agent checks revised claim'} for f in review.get('findings', [])]
        body = {'unit_id': 'u', 'review_path': review['report_path'],
                'review_sha256': pipe.digest(self.root/review['report_path']),
                'author_id': 'orchestrator-session', 'phase': receipt['phase'], 'responses': responses,
                'no_findings_reason': 'All explicit completion criteria were checked; no findings remain.' if not responses else None}
        (self.root/path).write_text('# Response\n```json\n'+json.dumps(body)+'\n```\n', encoding='utf-8')
        receipt.update(response_path=path, response_sha256=pipe.digest(self.root/path))
        if receipt['phase'] == 'revision':
            receipt['responses'] = responses
        return receipt

    def revision_receipt(self, queue, cycle=0, actor='producer-session'):
        receipt = {'phase': 'revision', 'agent_id': actor, 'artifacts': ['outputs/u.md']}
        return self.add_response(queue, receipt, queue['units'][0]['review'], 'outputs/revision_'+str(cycle)+'_response.md')

    def test_distinct_agents_and_reports_complete_only_after_review(self):
        queue = self.verified()
        self.assertEqual(queue['units'][0]['status'], 'partial')
        queue = pipe.advance(self.root, queue, 'u', self.review_receipt(queue))
        self.assertEqual(queue['units'][0]['status'], 'complete')
        self.assertEqual(queue['units'][0]['review_count'], 1)
        self.assertFalse(pipe.validate(self.root, queue))
        self.assertEqual(self.queue['units'][0]['phase'], 'production')  # no in-place partial mutation

    def test_author_cannot_verify_own_artifact(self):
        queue = self.produced()
        with self.assertRaisesRegex(ValueError, 'producer'):
            pipe.advance(self.root, queue, 'u', self.verify_receipt(queue, actor='producer-session'))

    def test_verifier_cannot_referee_same_unit(self):
        queue = self.verified()
        with self.assertRaisesRegex(ValueError, 'fresh'):
            pipe.advance(self.root, queue, 'u', self.review_receipt(queue, actor='verifier-session-0'))

    def test_missing_artifact_and_missing_report_rejected(self):
        (self.root/'outputs/u.md').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            self.produced()
        (self.root/'outputs/u.md').write_text('source note', encoding='utf-8')
        queue = self.produced()
        receipt = self.verify_receipt(queue)
        (self.root/receipt['report_path']).unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            pipe.advance(self.root, queue, 'u', receipt)

    def test_role_label_and_reused_producer_report_rejected(self):
        with self.assertRaisesRegex(ValueError, 'actual distinct'):
            self.produced(agent='codex')
        queue = self.produced()
        receipt = self.verify_receipt(queue)
        receipt['report_path'] = 'outputs/u.md'
        with self.assertRaisesRegex(ValueError, 'producer artifact'):
            pipe.advance(self.root, queue, 'u', receipt)

    def test_changed_source_requires_new_revision_and_reverification(self):
        queue = self.produced()
        (self.root/'outputs/u.md').write_text('changed after production', encoding='utf-8')
        self.assertTrue(any('digest changed' in e for e in pipe.validate(self.root, queue)))
        with self.assertRaisesRegex(ValueError, 'digest changed'):
            pipe.advance(self.root, queue, 'u', self.verify_receipt(queue))

    def test_incomplete_source_check_and_wrong_digest_rejected(self):
        queue = self.produced()
        receipt = self.verify_receipt(queue)
        receipt['source_checks'] = []
        with self.assertRaisesRegex(ValueError, 'source checks'):
            pipe.advance(self.root, queue, 'u', receipt)
        receipt = self.verify_receipt(queue)
        receipt['artifact_hashes'] = {}
        with self.assertRaisesRegex(ValueError, 'exactly'):
            pipe.advance(self.root, queue, 'u', receipt)

    def two_revision_escalation(self):
        queue = self.verified()
        for cycle in range(3):
            queue = pipe.advance(self.root, queue, 'u', self.review_receipt(queue, fail=True, cycle=cycle))
            if cycle == 2:
                break
            self.assertEqual(queue['units'][0]['phase'], 'revision')
            (self.root/'outputs/u.md').write_text('revision '+str(cycle), encoding='utf-8')
            queue = pipe.advance(self.root, queue, 'u', self.revision_receipt(queue, cycle))
            queue = self.verified(queue, cycle=cycle+1)
        return queue

    def test_two_revisions_then_remaining_blocker_escalates(self):
        queue = self.two_revision_escalation()
        self.assertEqual(queue['units'][0]['revision_count'], 2)
        self.assertEqual(queue['units'][0]['review_count'], 3)
        self.assertEqual(queue['units'][0]['phase'], 'decision')
        self.assertEqual(queue['units'][0]['status'], 'escalated')

    def test_escalation_allows_only_the_recorded_user_scope(self):
        queue = self.two_revision_escalation()
        receipt = self.revision_receipt(queue, cycle=2)
        with self.assertRaisesRegex(ValueError, 'no implicit reopening'):
            pipe.advance(self.root, queue, 'u', receipt)
        path = 'outputs/u.md'
        old_hash = pipe.digest(self.root/path)
        (self.root/path).write_text('User-approved single clarification.', encoding='utf-8')
        new_hash = pipe.digest(self.root/path)
        approval_path = 'outputs/user_scope.json'
        decision = dict(decision='allow_one_scoped_revision', unit_id='u',
                        review_sha256=queue['units'][0]['review']['report_sha256'],
                        finding_id='R1', artifact_path=path, user_response='Approve this clarification',
                        before_sha256=old_hash, after_sha256=new_hash)
        (self.root/approval_path).write_text(json.dumps(decision), encoding='utf-8')
        receipt['user_revision_approval'] = dict(path=approval_path, sha256=pipe.digest(self.root/approval_path))
        (self.root/path).write_text('Unauthorized replacement.', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'one approved artifact change'):
            pipe.advance(self.root, queue, 'u', receipt)
        (self.root/path).write_text('User-approved single clarification.', encoding='utf-8')
        queue = pipe.advance(self.root, queue, 'u', receipt)
        self.assertEqual(queue['units'][0]['revision_count'], 3)
        self.assertEqual(queue['units'][0]['phase'], 'verification')
        queue = self.verified(queue, cycle=3)
        queue = pipe.advance(self.root, queue, 'u', self.review_receipt(queue, cycle=3))
        self.assertEqual(queue['units'][0]['status'], 'complete')
        self.assertFalse(pipe.validate(self.root, queue))

    def test_revision_must_answer_open_findings_and_cannot_be_referee(self):
        queue = self.verified()
        queue = pipe.advance(self.root, queue, 'u', self.review_receipt(queue, fail=True))
        receipt = self.revision_receipt(queue)
        receipt['responses'] = []
        with self.assertRaisesRegex(ValueError, 'disagree'):
            pipe.advance(self.root, queue, 'u', receipt)
        receipt = self.revision_receipt(queue, actor='referee-session-0')
        with self.assertRaisesRegex(ValueError, 'reviser'):
            pipe.advance(self.root, queue, 'u', receipt)

    def test_minor_revision_is_not_silently_complete(self):
        queue = self.verified()
        receipt = self.review_receipt(queue)
        receipt['verdict'] = 'minor_revision'
        receipt['findings'] = [{'id': 'M1', 'severity': 'minor', 'status': 'open', 'reason': 'Caveat must be stated explicitly'}]
        self.add_response(queue, receipt, receipt, 'outputs/minor_0_response.md')
        queue = pipe.advance(self.root, queue, 'u', receipt)
        self.assertEqual(queue['units'][0]['phase'], 'revision')
        self.assertEqual(queue['units'][0]['status'], 'partial')
        queue = pipe.advance(self.root, queue, 'u', self.revision_receipt(queue))
        queue = self.verified(queue, cycle=1)
        receipt = self.review_receipt(queue, cycle=1)
        receipt['findings'] = [{'id': 'M1', 'severity': 'minor', 'status': 'resolved', 'reason': 'Explicit caveat checked in revised artifact'}]
        self.add_response(queue, receipt, receipt, 'outputs/minor_1_response.md')
        queue = pipe.advance(self.root, queue, 'u', receipt)
        self.assertEqual(queue['units'][0]['status'], 'complete')

    def test_accept_with_open_minor_still_requires_response(self):
        queue = self.verified()
        receipt = self.review_receipt(queue)
        receipt['findings'] = [{'id': 'M1', 'severity': 'minor', 'status': 'open', 'reason': 'Missing limitation'}]
        self.add_response(queue, receipt, receipt, 'outputs/minor_response.md')
        queue = pipe.advance(self.root, queue, 'u', receipt)
        self.assertEqual(queue['units'][0]['phase'], 'revision')

    def test_revised_version_rejects_old_judge_path_and_content_separately(self):
        queue = self.verified()
        queue = pipe.advance(self.root, queue, 'u', self.review_receipt(queue, fail=True))
        (self.root/'outputs/u.md').write_text('version 2', encoding='utf-8')
        queue = pipe.advance(self.root, queue, 'u', self.revision_receipt(queue))
        old = queue['units'][0]['history'][1]
        receipt = self.verify_receipt(queue, cycle=1)
        for key in ('agent_id', 'report_path'):
            reused = copy.deepcopy(receipt); reused[key] = old[key]
            with self.assertRaisesRegex(ValueError, 'fresh'):
                pipe.advance(self.root, queue, 'u', reused)
        (self.root/receipt['report_path']).write_bytes((self.root/old['report_path']).read_bytes())
        with self.assertRaisesRegex(ValueError, 'fresh'):
            pipe.advance(self.root, queue, 'u', receipt)

    def test_review_cannot_complete_without_real_response_even_no_findings(self):
        queue = self.verified()
        receipt = self.review_receipt(queue)
        missing = copy.deepcopy(receipt); missing.pop('response_path')
        with self.assertRaisesRegex(ValueError, 'Artifact path'):
            pipe.advance(self.root, queue, 'u', missing)
        missing = copy.deepcopy(receipt); missing.pop('response_sha256')
        with self.assertRaisesRegex(ValueError, 'Response digest'):
            pipe.advance(self.root, queue, 'u', missing)
        target = self.root/receipt['response_path']
        body = json.loads(target.read_text().split('```json\n')[1].split('```')[0])
        body.pop('no_findings_reason')
        target.write_text('```json\n'+json.dumps(body)+'\n```\n', encoding='utf-8')
        receipt['response_sha256'] = pipe.digest(target)
        with self.assertRaisesRegex(ValueError, 'no-findings'):
            pipe.advance(self.root, queue, 'u', receipt)

    def test_response_current_review_digest_and_exact_finding_coverage(self):
        queue = self.verified()
        receipt = self.review_receipt(queue, fail=True)
        target = self.root/receipt['response_path']
        original = json.loads(target.read_text().split('```json\n')[1].split('```')[0])
        for key, value, message in [('review_sha256', 'old-review-hash', 'current review'), ('responses', [], 'every current review')]:
            body = copy.deepcopy(original); body[key] = value
            target.write_text('```json\n'+json.dumps(body)+'\n```\n', encoding='utf-8')
            receipt['response_sha256'] = pipe.digest(target)
            with self.assertRaisesRegex(ValueError, message):
                pipe.advance(self.root, queue, 'u', receipt)

    def test_provenance_history_cannot_omit_a_judgment(self):
        queue = self.verified()
        queue['units'][0]['history'].pop()
        self.assertTrue(any('history' in e for e in pipe.validate(self.root, queue)))
        queue = self.verified()
        queue['units'][0]['producer_ids'] = []
        self.assertTrue(any('provenance' in e for e in pipe.validate(self.root, queue)))

    def test_live_cli_rejects_reduced_round_queue(self):
        (self.root/'state/work_queue.json').write_text(json.dumps(self.queue), encoding='utf-8')
        (self.root/'state/turn.md').write_text('```\nworkflow_version: codex_internal_v1\nnext: codex\n```\n')
        for command in ('validate', 'advance'):
            output = io.StringIO()
            with patch.object(sys, 'argv', ['review_pipeline.py', command, '--repo', str(self.root)]), contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as failure:
                pipe.main()
            self.assertEqual(failure.exception.code, 1)
            self.assertIn('Required round03 work track missing', output.getvalue())

    def test_round_coverage_requires_all_artifacts_and_integration_dependencies(self):
        units = []
        for key, paths in pipe.ROUND03_REQUIREMENTS.items():
            unit = fresh_unit(key); unit['required_artifacts'] = list(paths); units.append(unit)
        units[-1]['dependencies'] = list(pipe.ROUND03_REQUIREMENTS)[:-1]
        queue = queue_for(*units)
        self.assertFalse(pipe.round_coverage_errors(queue))
        units[-1]['dependencies'] = []
        self.assertTrue(any('depend' in e for e in pipe.round_coverage_errors(queue)))
        units[0]['required_artifacts'] = []
        self.assertTrue(any('artifact' in e for e in pipe.round_coverage_errors(queue)))

    def test_blocked_audit_does_not_starve_independent_work(self):
        audit, literature, integrated = fresh_unit('audit'), fresh_unit('literature'), fresh_unit('integrated')
        audit['status'] = 'blocked'
        integrated['dependencies'] = ['audit', 'literature']
        queue = queue_for(audit, literature, integrated)
        self.assertEqual([u['id'] for u in pipe.plan(self.root, queue)], ['literature'])
        audit['status'] = 'partial'
        audit['last_touched'] = '2026-11-02T01:00:00+00:00'
        self.assertEqual(pipe.plan(self.root, queue, 1)[0]['id'], 'literature')

    def test_duplicate_ids_cycles_and_false_completion_rejected(self):
        self.assertTrue(pipe.validate(self.root, queue_for(fresh_unit(), fresh_unit())))
        a, b = fresh_unit('a'), fresh_unit('b')
        a['dependencies'], b['dependencies'] = ['b'], ['a']
        self.assertTrue(any('cycle' in e for e in pipe.validate(self.root, queue_for(a, b))))
        fake = fresh_unit(); fake['status'] = 'complete'
        self.assertTrue(pipe.validate(self.root, queue_for(fake)))

    def test_other_run_cannot_reuse_codex_lock(self):
        state = {'workflow_version': pipe.VERSION, 'next': 'codex', 'lock': 'codex', 'run_id': 'owner'}
        pipe.owned_lease(state, 'owner')
        for actor in ('different-run', 'none', ''):
            with self.assertRaisesRegex(ValueError, 'exact owned'):
                pipe.owned_lease(state, actor)

    def test_claude_v2_claim_is_noop_without_git(self):
        turn = '```\nworkflow_version: codex_internal_v1\nnext: codex\nlock: none\n```\n'
        (self.root/'state/turn.md').write_text(turn)
        with patch.object(claim_turn, 'git') as git:
            result = claim_turn.acquire(self.root, 'claude')
            git.assert_not_called()
        self.assertEqual(result['status'], 'skipped')
        self.assertIn('retired', result['reason'])
        self.assertEqual((self.root/'state/turn.md').read_text(), turn)

    def test_stale_lock_is_never_stolen(self):
        turn = '```\nworkflow_version: codex_internal_v1\nnext: codex\nround: 03\nstage: production\nactive_unit: u\nlock: codex\nlock_since: 2000-01-01T00:00:00+00:00\nrun_id: other-run\ninternal_review_count: 0\n```\n'
        (self.root/'state/turn.md').write_text(turn)
        (self.root/'state/work_queue.json').write_text(json.dumps(self.queue))
        def fake_git(root, *args):
            return 'main' if args[0] == 'branch' else '0' if args[0] == 'rev-list' else ''
        with patch.object(claim_turn, 'git', side_effect=fake_git) as git:
            result = claim_turn.acquire(self.root, 'codex')
        self.assertEqual(result['status'], 'skipped')
        self.assertIn('no theft', result['reason'])
        self.assertFalse(any(c.args[1] in {'add', 'commit', 'push'} for c in git.call_args_list))
        self.assertEqual((self.root/'state/turn.md').read_text(), turn)


if __name__ == '__main__':
    unittest.main()
