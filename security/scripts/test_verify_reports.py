import json
import tempfile
import unittest
from pathlib import Path
from verify_reports import EXPECTED, verify

class ReportCompletenessTest(unittest.TestCase):
    def make_reports(self, root):
        for name, kind in EXPECTED.items():
            data = [] if kind is list else {}
            if name.startswith('zap-'): data = {'site': [{'@name': 'http://localhost'}]}
            elif name.startswith('trivy-'): data = {'Results': []}
            elif name in ('semgrep.json', 'bandit.json'): data = {'results': []}
            elif name.startswith('pip-audit'): data = {'dependencies': []}
            (root / name).write_text(json.dumps(data))

    def test_complete_empty_findings_are_valid(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); self.make_reports(root)
            self.assertEqual(verify(root), [])

    def test_missing_corrupt_duplicate_and_unscanned_reports_block(self):
        for change in ('missing', 'corrupt', 'duplicate', 'unscanned'):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as d:
                root=Path(d); self.make_reports(root)
                p=root/'zap-api.json'
                if change == 'missing': p.unlink()
                elif change == 'corrupt': p.write_text('{')
                elif change == 'unscanned': p.write_text('{"site": []}')
                else:
                    (root/'duplicate').mkdir();(root/'duplicate'/p.name).write_text(p.read_text())
                self.assertTrue(verify(root))

if __name__ == '__main__': unittest.main()
