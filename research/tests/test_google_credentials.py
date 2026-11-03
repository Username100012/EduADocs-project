"""Project credentials take precedence without printing or changing secrets."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import google_credentials as keys

class GoogleCredentialTests(unittest.TestCase):
    def test_local_google_then_local_gemini_then_environment(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(keys,'ROOT',Path(temp)), patch.dict(keys.os.environ,{'GOOGLE_API_KEY':'global-test','GEMINI_API_KEY':'global-alias'},clear=True):
            path=Path(temp)/'.env'
            self.assertEqual(keys.read_google_key(),('global-test','environment:GOOGLE_API_KEY'))
            path.write_text('GEMINI_API_KEY="project-alias"\n',encoding='utf-8')
            self.assertEqual(keys.read_google_key(),('project-alias','.env:GEMINI_API_KEY'))
            path.write_text('GOOGLE_API_KEY=project-test\nGEMINI_API_KEY=project-alias\n',encoding='utf-8')
            self.assertEqual(keys.read_google_key(),('project-test','.env:GOOGLE_API_KEY'))
            self.assertEqual(keys.os.getenv('GOOGLE_API_KEY'),'global-test')
            path.write_text('GOOGLE_API_KEY=\nGEMINI_API_KEY=\n',encoding='utf-8')
            self.assertEqual(keys.read_google_key(),('global-test','environment:GOOGLE_API_KEY'))
    def test_missing_credential_is_explicit(self):
        with tempfile.TemporaryDirectory() as temp,patch.object(keys,'ROOT',Path(temp)),patch.dict(keys.os.environ,{},clear=True):
            self.assertEqual(keys.read_google_key(),(None,'missing'))
