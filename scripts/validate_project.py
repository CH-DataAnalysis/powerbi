"""Static PBIP checks. Optional external-file checks never connect to databases."""
import argparse
import csv
import json
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from project_catalog import ROOT, read, render, locations


def check_project_paths(root):
    errors = []
    projects = list(root.glob('*.pbip'))
    if len(projects) != 1:
        return ['Esperado exatamente um PBIP.']
    try:
        for artifact in json.loads(read(projects[0]))['artifacts']:
            report = (root/artifact['report']['path']).resolve()
            report.relative_to(root.resolve())
            definition = report/'definition.pbir'
            model = (report/json.loads(read(definition))['datasetReference']['byPath']['path']).resolve()
            model.relative_to(root.resolve())
            if not (model/'definition.pbism').is_file():
                errors.append('Modelo referenciado sem definition.pbism.')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'Referencia PBIP/PBIR invalida: {exc}')
    return errors


def check_generated(root, outputs):
    return [f'Documento desatualizado: {name}; execute python scripts/project_catalog.py'
            for name, content in outputs.items()
            if not (root/name).is_file() or read(root/name) != content]


def xlsx_headers(path, sheet):
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    relns = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
    with zipfile.ZipFile(path) as z:
        workbook = ET.fromstring(z.read('xl/workbook.xml'))
        entry = next((e for e in workbook.findall('s:sheets/s:sheet', ns) if e.get('name') == sheet), None)
        if entry is None:
            raise ValueError(f'Aba ausente: {sheet}')
        rels = ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        target = next(e.get('Target') for e in rels if e.get('Id') == entry.get(relns))
        member = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/' + target)
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            with z.open('xl/sharedStrings.xml') as stream:
                for _, elem in ET.iterparse(stream, events=('end',)):
                    if elem.tag == f'{{{ns["s"]}}}si':
                        strings.append(''.join(elem.itertext()))
                        elem.clear()
        with z.open(member) as stream:
            for _, elem in ET.iterparse(stream, events=('end',)):
                if elem.tag != f'{{{ns["s"]}}}row':
                    continue
                headers = []
                for c in elem.findall('s:c', ns):
                    value = c.findtext('s:v', '', ns)
                    if c.get('t') == 's':
                        value = strings[int(value)]
                    elif c.get('t') == 'inlineStr':
                        value = ''.join(c.find('s:is', ns).itertext())
                    headers.append(value)
                return headers
    return []


def check_external_files(folder, contracts):
    errors = []
    for contract in contracts:
        path = folder/contract['file']
        try:
            if path.suffix.lower() == '.csv':
                with path.open(encoding='utf-8-sig', newline='') as stream:
                    # M QuoteStyle.None changes line-break handling, not whether
                    # field quotes are recognized (that is controlled by CsvStyle).
                    lines = [stream.readline()] if contract.get('quote_style') == 'None' else stream
                    headers = next(csv.reader(lines, delimiter=','), [])
                if len(headers) != contract['csv_columns']:
                    errors.append(f'{path.name}: quantidade de colunas diferente do contrato.')
            else:
                headers = xlsx_headers(path, contract['sheet'])
            missing = set(contract['headers']) - set(headers)
            if missing:
                errors.append(f'{path.name}: cabecalhos ausentes: {", ".join(sorted(missing))}')
        except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError, KeyError, StopIteration, IndexError, csv.Error) as exc:
            errors.append(f'{path.name}: {exc}')
    return errors


def validate(root):
    errors = check_project_paths(root)
    report, model = locations(root)
    for base in (report, model):
        for path in base.rglob('*'):
            if path.suffix in ('.json', '.pbir', '.pbism') or path.name == '.platform':
                try:
                    json.loads(read(path))
                except (OSError, ValueError) as exc:
                    errors.append(f'JSON invalido: {path.relative_to(root)}: {exc}')
    try:
        page_meta = json.loads(read(report/'definition/pages/pages.json'))
        page_names = {json.loads(read(p))['name'] for p in (report/'definition/pages').glob('*/page.json')}
        order = page_meta['pageOrder']
        if set(order) != page_names or len(order) != len(page_names):
            errors.append('pageOrder possui paginas ausentes, duplicadas ou nao catalogadas.')
        if page_meta.get('activePageName') not in page_names:
            errors.append('Pagina ativa inexistente.')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(f'Metadados de paginas invalidos: {exc}')
    definition = model/'definition'
    expressions = read(definition/'expressions.tmdl')
    for name in ('cliente', 'PastaArquivos', 'RangeStart', 'RangeEnd'):
        if not re.search(rf'^expression {name} = .+IsParameterQuery=true', expressions, re.M):
            errors.append(f'Parametro ausente ou sem metadados: {name}')
    try:
        dates = []
        for name in ('RangeStart', 'RangeEnd'):
            value = re.search(rf'^expression {name} = #datetime\(([^)]+)\)', expressions, re.M)
            dates.append(datetime(*(int(v.strip()) for v in value[1].split(','))))
        if dates[0] >= dates[1]:
            errors.append('RangeStart deve ser anterior a RangeEnd.')
    except (ValueError, TypeError) as exc:
        errors.append(f'Parametros de data invalidos: {exc}')
    refs = re.findall(r'^ref table (.+)$', read(definition/'model.tmdl'), re.M)
    table_names = {read(p).splitlines()[0].removeprefix('table ') for p in (definition/'tables').glob('*.tmdl')}
    if set(refs) != table_names:
        errors.append('Referencias ref table divergentes das tabelas TMDL.')
    for path in (definition/'tables').glob('*.tmdl'):
        text = read(path)
        for line in text.splitlines():
            if 'NomeTabela =' in line and not re.search(r'&\s*(Text.From\(cliente\)|cliente)\s*,', line.split('//')[0]):
                errors.append(f'{path.name}: NomeTabela nao usa cliente.')
            if 'File.Contents(' in line and not re.search(r'File\.Contents\(PastaArquivos & "\\[^"\\]+"\)', line):
                errors.append(f'{path.name}: arquivo externo nao usa PastaArquivos.')
        if '\trefreshPolicy' in text:
            names = re.findall(r'NomeTabela = (.+)', text)
            if len(names) != 2 or names[0] != names[1]:
                errors.append(f'{path.name}: fontes incremental/importacao divergentes.')
            if text.count('>= RangeStart') != 2 or text.count('< RangeEnd') != 2:
                errors.append(f'{path.name}: conferir limites de data da politica e particao.')
    try:
        errors.extend(check_generated(root, render(root)))
    except (OSError, ValueError, KeyError) as exc:
        errors.append(f'Falha no inventario: {exc}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, help='Check presence, sheet names and headers of the eight external files.')
    args = parser.parse_args()
    try:
        errors = validate(ROOT)
        if args.data_dir:
            contracts = json.loads(read(ROOT/'docs/contratos-arquivos.json'))
            errors.extend(check_external_files(args.data_dir, contracts))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print('ERRO:', error)
    if errors:
        return 1
    print('OK: referencias, JSON, paginas, parametros, fontes e documentacao gerada.')
    if args.data_dir:
        print('OK: arquivos externos, abas e cabecalhos. Valores e tipos das linhas nao foram validados.')
    print('Nao executa M/DAX, nao valida schemas oficiais nem atualiza dados no Power BI.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
