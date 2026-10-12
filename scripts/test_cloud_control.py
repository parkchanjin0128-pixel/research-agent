import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import cloud_control as cloud
from claim_turn import git, fields


class CloudTests(unittest.TestCase):
    def test_zip_rejects_traversal(self):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z: z.writestr('../escape.txt','bad')
        with self.assertRaises(ValueError): cloud.safe_artifact_files(data.getvalue())

    def test_zip_accepts_outputs(self):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z: z.writestr('outputs/round_03/test.md','ok')
        self.assertEqual(cloud.safe_artifact_files(data.getvalue())['outputs/round_03/test.md'],b'ok')

    def test_missing_key_never_enables_research(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'state').mkdir()
            (root/'state/turn.md').write_text('```\nnext: codex\nlock: none\n```')
            with patch.object(cloud,'ROOT',root), patch.dict(os.environ,{'RESEARCH_AUTORUN':'true','HAS_OPENAI_KEY':'false','REQUEST_MODE':'research'}), patch.object(cloud,'output') as out, contextlib.redirect_stdout(io.StringIO()):
                cloud.preflight(); out.assert_called_with('run','false')

    def test_checked_activation_enables_due_turn(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'state').mkdir()
            (root/'state/turn.md').write_text('```\nnext: codex\nlock: none\n```')
            with patch.object(cloud,'ROOT',root), patch.dict(os.environ,{'RESEARCH_AUTORUN':'true','HAS_OPENAI_KEY':'true','REQUEST_MODE':'research'}), patch.object(cloud,'output') as out, contextlib.redirect_stdout(io.StringIO()):
                cloud.preflight(); out.assert_called_with('run','true')

    def test_publish_checkpoint_and_reject_incomplete_review_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent=Path(tmp); remote=parent/'remote.git'; root=parent/'repo'
            git(parent,'init','--bare',str(remote));git(parent,'clone',str(remote),str(root))
            git(root,'checkout','-b','main');git(root,'config','user.name','Test');git(root,'config','user.email','test@example.invalid')
            (root/'state').mkdir()
            (root/'state/turn.md').write_text('```\nnext: codex\nround: 03\nstage: production\nlock: codex\nlock_since: 2026-10-12T00:00:00+00:00\nrun_id: lease\nreviews_this_round: 0\n```')
            git(root,'add','.');git(root,'commit','-m','test');git(root,'push','-u','origin','main')
            sha=git(root,'rev-parse','HEAD')
            payload={'outputs/round_03/draft.md':b'Partial research preserved.',
                     '.local/cloud_result.json':json.dumps({'next':'claude','stage':'claude_review','summary':'ready'}).encode()}
            env={'EXPECTED_CLAIM_SHA':sha,'EXPECTED_RUN_ID':'lease','PRODUCE_RESULT':'success','GITHUB_RUN_ID':'123'}
            with patch.object(cloud,'ROOT',root),patch.dict(os.environ,env),patch.object(cloud,'auth_git'),patch.object(cloud,'download_checkpoint',return_value=payload),patch.object(cloud,'summary'):
                cloud.publish()
            state=fields((root/'state/turn.md').read_text())
            self.assertEqual(state['next'],'codex');self.assertEqual(state['lock'],'none')
            self.assertEqual((root/'outputs/round_03/draft.md').read_bytes(),b'Partial research preserved.')
            self.assertNotEqual(git(root,'ls-remote','origin','refs/heads/main').split()[0],sha)


if __name__=='__main__': unittest.main()
