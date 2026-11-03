"""Tests use constructed dummy secrets, never provider credentials."""
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
from check_publication import check

class PublicationChecks(unittest.TestCase):
    def test_detects_sensitive_json_fields_without_printing_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'MANIFEST_SHA256.json').write_text('{}')
            fake='synthetic-not-a-real-credential'
            (root/'example.json').write_text(json.dumps({'provider':{'api_key':fake}}))
            report=check(root)
            self.assertTrue(any(x['type']=='nonempty_credential_field' for x in report['findings']))
            self.assertNotIn(fake,json.dumps(report))

    def test_detects_known_secret_and_provider_pattern(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as envtmp:
            root=Path(tmp);(root/'MANIFEST_SHA256.json').write_text('{}')
            fake='AIza'+'x'*35
            (root/'log.txt').write_text(fake)
            env=Path(envtmp)/'.env';env.write_text('GOOGLE_API_KEY='+fake)
            report=check(root,env)
            self.assertEqual({x['type'] for x in report['findings']},{'google_api_key','known_local_secret'})
            self.assertNotIn(fake,json.dumps(report))

    def test_manifest_detects_content_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source.txt').write_bytes(b'original')
            (root/'MANIFEST_SHA256.json').write_text(json.dumps({'source.txt':{'sha256':sha256(b'original').hexdigest()}}))
            self.assertFalse(check(root)['original_snapshot_changed'])
            (root/'source.txt').write_bytes(b'changed')
            self.assertEqual(check(root)['original_snapshot_changed'],['source.txt'])

if __name__=='__main__':unittest.main()
