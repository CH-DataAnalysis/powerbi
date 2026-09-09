import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from project_catalog import parse_measures, external_contract
from validate_project import check_project_paths, check_external_files, check_generated


class ProjectToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_missing_report_reference_is_rejected(self):
        (self.root / 'Demo.pbip').write_text(json.dumps({
            'artifacts': [{'report': {'path': 'Missing.Report'}}]}))
        self.assertTrue(check_project_paths(self.root))

    def test_valid_project_and_model_paths(self):
        (self.root / 'Demo.Report').mkdir()
        (self.root / 'Demo.SemanticModel').mkdir()
        (self.root / 'Demo.pbip').write_text(json.dumps({
            'artifacts': [{'report': {'path': 'Demo.Report'}}]}))
        (self.root / 'Demo.Report/definition.pbir').write_text(json.dumps({
            'datasetReference': {'byPath': {'path': '../Demo.SemanticModel'}}}))
        (self.root / 'Demo.SemanticModel/definition.pbism').write_text('{}')
        self.assertEqual(check_project_paths(self.root), [])

    def test_invalid_project_json_is_reported(self):
        (self.root / 'Demo.pbip').write_text('{invalid')
        self.assertTrue(check_project_paths(self.root))

    def test_project_cannot_reference_outside_repository(self):
        (self.root / 'Demo.pbip').write_text(json.dumps({
            'artifacts': [{'report': {'path': '../Outside.Report'}}]}))
        self.assertTrue(check_project_paths(self.root))

    def test_csv_missing_headers_and_file(self):
        contract = [{'file': 'data.csv', 'headers': ['id', 'name'], 'sheet': None,
                     'csv_columns': 2, 'quote_style': 'Csv'}]
        self.assertTrue(check_external_files(self.root, contract))
        (self.root / 'data.csv').write_text('id,wrong\n1,test\n', encoding='utf-8')
        self.assertTrue(check_external_files(self.root, contract))
        (self.root / 'data.csv').write_text('id,name\n1,test\n', encoding='utf-8')
        self.assertEqual(check_external_files(self.root, contract), [])

    def test_stale_generated_document_is_rejected(self):
        (self.root / 'catalog.md').write_text('old', encoding='utf-8')
        self.assertTrue(check_generated(self.root, {'catalog.md': 'new'}))
        (self.root / 'catalog.md').write_text('new', encoding='utf-8')
        self.assertEqual(check_generated(self.root, {'catalog.md': 'new'}), [])

    def test_quote_style_none_still_accepts_quoted_csv_headers(self):
        (self.root / 'data.csv').write_text('"id","name"\n1,test\n', encoding='utf-8')
        contract = [{'file': 'data.csv', 'headers': ['id', 'name'], 'sheet': None,
                     'csv_columns': 2, 'quote_style': 'None'}]
        self.assertEqual(check_external_files(self.root, contract), [])

    def test_measure_expression_excludes_metadata(self):
        text = 'table Demo\n\tmeasure total =\n\t\t\tSUM(Demo[value])\n\t\tformatString: 0\n\t\tlineageTag: abc\n\n\tmeasure other = ```\n\t\t\t[total] * 2\n\t\t\t```\n\t\tformatString: 0\n'
        measures = parse_measures(text)
        self.assertEqual(len(measures), 2)
        self.assertEqual(measures[0]['expression'], 'SUM(Demo[value])')
        self.assertEqual(measures[1]['expression'], '[total] * 2')

    def test_contract_keeps_columns_removed_after_import(self):
        text = 'table Demo\n\tpartition Demo = m\n\t\tsource =\n\t\t\tCsv.Document(File.Contents(PastaArquivos & "\\data.csv"), [Columns=2, QuoteStyle=QuoteStyle.None])\n\t\t\tTable.TransformColumnTypes(x,{{"id", Int64.Type}, {"removed", type text}})\n'
        contract = external_contract(text)
        self.assertEqual(contract['headers'], ['id', 'removed'])
        self.assertEqual(contract['file'], 'data.csv')

    def test_xlsx_headers_and_missing_sheet(self):
        path = self.root / 'data.xlsx'
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr('xl/workbook.xml', '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Dados" r:id="rId1"/></sheets></workbook>')
            z.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/></Relationships>')
            z.writestr('xl/sharedStrings.xml', '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><si><t>id</t></si></sst>')
            z.writestr('xl/worksheets/sheet1.xml', '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="inlineStr"><is><t>name</t></is></c></row></sheetData></worksheet>')
        contract = [{'file': 'data.xlsx', 'headers': ['id', 'name'], 'sheet': 'Dados'}]
        self.assertEqual(check_external_files(self.root, contract), [])
        contract[0]['headers'].append('missing')
        self.assertTrue(check_external_files(self.root, contract))
        contract[0]['sheet'] = 'Absent'
        self.assertTrue(check_external_files(self.root, contract))

    def test_corrupt_xlsx_is_reported(self):
        (self.root / 'data.xlsx').write_text('not a workbook')
        self.assertTrue(check_external_files(self.root, [
            {'file': 'data.xlsx', 'headers': ['id'], 'sheet': 'Dados'}]))

    def test_contract_requires_untyped_imported_columns_but_not_renamed_output(self):
        text = 'table Demo\n\tcolumn renamed\n\t\tsourceColumn: renamed\n\tcolumn cnpj\n\t\tsourceColumn: cnpj\n\tpartition Demo = m\n\t\tsource =\n\t\t\tCsv.Document(File.Contents(PastaArquivos & "\\data.csv"), [Columns=2])\n\t\t\tTable.TransformColumnTypes(x,{{"original", Int64.Type}})\n\t\t\tTable.RenameColumns(x,{{"original", "renamed"}})\n'
        self.assertEqual(external_contract(text)['headers'], ['original', 'cnpj'])


if __name__ == '__main__':
    unittest.main()
