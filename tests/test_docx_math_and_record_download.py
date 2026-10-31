"""Regression tests for equations, nested lists, provenance and credential export."""
import io
import json
from pathlib import Path
import sys
import unittest
from zipfile import ZipFile
from xml.etree import ElementTree as ET
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from docx import Document
from exporters.markdown_docx import add_markdown_content
from application.record_download import execution_record_json
from processing import process_response
from processing.probability_example import BAD, GOOD, correct_known_probability_example

class ExportRegressionTests(unittest.TestCase):
    def test_native_math_with_fractions_and_multiline_display(self):
        d=Document()
        add_markdown_content(d, 'Probabilidade $P(\\text{par})=\\frac{3}{6}=\\frac{1}{2}$ e $50\\%$.\n\n$$x^2 +\ny_1$$')
        b=io.BytesIO();d.save(b)
        with ZipFile(io.BytesIO(b.getvalue())) as z:
            root=ET.fromstring(z.read('word/document.xml'))
        ns={'m':'http://schemas.openxmlformats.org/officeDocument/2006/math','w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        self.assertEqual(len(root.findall('.//m:oMath',ns)),3)
        self.assertEqual(len(root.findall('.//m:f',ns)),2)
        self.assertEqual(len(root.findall('.//m:sSup',ns)),1)
        self.assertNotIn('\\frac',ET.tostring(root,encoding='unicode'))

    def test_lists_preserve_depth_and_do_not_create_empty_paragraphs(self):
        d=Document();add_markdown_content(d,'# Avaliação\n\n- Critérios:\n  - Clareza\n  - Comparação\n- Encerramento\n')
        self.assertEqual([p.style.name for p in d.paragraphs],['Heading 1','List Bullet','List Bullet 2','List Bullet 2','List Bullet'])
        self.assertTrue(all(p.text for p in d.paragraphs))
        self.assertGreater(d.paragraphs[2].paragraph_format.left_indent,d.paragraphs[1].paragraph_format.left_indent)

    def test_escaped_currency_is_not_math(self):
        d=Document();add_markdown_content(d,r'Preço: R\$ 10,00.')
        self.assertEqual(len(d._element.findall('.//{http://schemas.openxmlformats.org/officeDocument/2006/math}oMath')),0)

    def test_credentials_redacted_recursively_without_removing_usage(self):
        secret='known-production-key'
        payload={'execution_id':'id','request':{'api_key':secret},'provider_response':{'raw_metadata':{'authorization':'Bearer abc','input_tokens':12}},'raw_response':secret+' '+('AIza'+'x'*35),'error':'https://example.test?api_key=another-secret&x=1'}
        output=execution_record_json(payload,secrets=[secret]);data=json.loads(output)
        self.assertNotIn(secret,output.decode());self.assertNotIn('another-secret',output.decode());self.assertNotIn('AIza',output.decode())
        self.assertEqual(data['provider_response']['raw_metadata']['input_tokens'],12)
        self.assertEqual(data['execution_id'],'id')

    def test_probability_correction_preserves_original_and_marks_change(self):
        raw='Como tarefa, lançar '+BAD+'.'
        result=correct_known_probability_example(process_response(raw))
        self.assertEqual(result.raw_content,raw)
        self.assertIn(GOOD,result.content)
        self.assertEqual(result.warnings,['probability_coin_die_example_corrected_v1'])

    def test_unrelated_probability_content_is_unchanged(self):
        raw='Uma face específica de um dado equilibrado tem probabilidade 1/6.'
        result=correct_known_probability_example(process_response(raw))
        self.assertEqual(result.content,raw);self.assertFalse(result.warnings)

if __name__=='__main__':unittest.main()
