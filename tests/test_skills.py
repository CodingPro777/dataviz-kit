import json
import py_compile
import subprocess
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILER = ROOT / "skills" / "data-report" / "scripts" / "profile_data.py"


def run_profile(path):
    result = subprocess.run(
        ["python3", str(PROFILER), str(path)],
        text=True,
        capture_output=True,
        check=False,
    )
    return result, json.loads(result.stdout) if result.returncode == 0 else None


def make_xlsx(path):
    files = {
        "[Content_Types].xml": """<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>""",
        "_rels/.rels": """<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>""",
        "xl/workbook.xml": """<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Sheet1" sheetId="1" r:id="rId1"/></sheets></workbook>""",
        "xl/_rels/workbook.xml.rels": """<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>""",
        "xl/worksheets/sheet1.xml": """<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>name</t></is></c><c r="B1" t="inlineStr"><is><t>score</t></is></c></row><row r="2"><c r="A2" t="inlineStr"><is><t>Alice</t></is></c><c r="B2"><v>10</v></c></row><row r="3"><c r="A3" t="inlineStr"><is><t>Bob</t></is></c><c r="B3"><v>20</v></c></row></sheetData></worksheet>""",
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)


class SkillTests(unittest.TestCase):
    def test_skill_frontmatter(self):
        for name in ("dataviz", "data-report"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\n"))
            frontmatter = text.split("---", 2)[1]
            self.assertRegex(frontmatter, rf'name:\s*["\']?{name}["\']?')
            self.assertIn("description:", frontmatter)

    def test_profiler_compiles(self):
        py_compile.compile(str(PROFILER), doraise=True)

    def test_csv_tsv_and_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixtures = {
                "sample.csv": "name,score\nAlice,10\nBob,20\n",
                "sample.tsv": "name\tscore\nAlice\t10\nBob\t20\n",
                "sample.json": '[{"name":"Alice","score":10},{"name":"Bob","score":20}]',
            }
            for filename, content in fixtures.items():
                path = root / filename
                path.write_text(content, encoding="utf-8")
                result, report = run_profile(path)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(report["row_count"], 2)
                self.assertEqual(report["columns"][1]["type"], "numeric")

    def test_xlsx(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.xlsx"
            make_xlsx(path)
            result, report = run_profile(path)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(report["row_count"], 2)
            self.assertEqual(report["columns"][1]["mean"], 15.0)

    def test_unsupported_input_fails_cleanly(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.xls"
            path.write_bytes(b"not an xls workbook")
            result, report = run_profile(path)
            self.assertEqual(result.returncode, 2)
            self.assertIsNone(report)
            self.assertIn("Unsupported input type", result.stderr)


if __name__ == "__main__":
    unittest.main()
