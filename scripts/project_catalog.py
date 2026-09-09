"""Generate repository documentation from PBIR/TMDL, using only the standard library.

This is an inventory parser for the indentation used by this project, not a TMDL
compiler. Expressions are copied, never evaluated or certified as correct.
"""
import argparse
import json
import re
import subprocess
import textwrap
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return path.read_text(encoding='utf-8-sig')


def unquote(value):
    value = value.strip()
    return value[1:-1].replace("''", "'") if value.startswith("'") and value.endswith("'") else value


def parse_measures(text):
    lines = text.splitlines()
    result = []
    for i, line in enumerate(lines):
        match = re.match(r'^\tmeasure (.+?)\s*=\s*(.*)$', line)
        if not match:
            continue
        expression = [match[2]] if match[2] else []
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or lines[j].startswith('\t\t\t')):
            expression.append(lines[j][3:] if lines[j].startswith('\t\t\t') else '')
            j += 1
        body = '\n'.join(expression).strip()
        if body.startswith('```') and body.endswith('```'):
            body = body[3:-3].strip()
        body = textwrap.dedent(body)
        metadata = []
        while j < len(lines) and not re.match(r'^\t\S', lines[j]):
            metadata.append(lines[j])
            j += 1
        fmt = re.search(r'^\t\tformatString: (.*)$', '\n'.join(metadata), re.M)
        result.append({'name': unquote(match[1]), 'expression': body,
                       'format': fmt[1] if fmt else '', 'line': i + 1})
    return result


def external_contract(text):
    if 'File.Contents(' not in text:
        return None
    match = re.search(r'File\.Contents\(PastaArquivos & "\\([^"\\]+)"\)', text)
    if not match:
        raise ValueError('File.Contents deve usar PastaArquivos & "\\arquivo"')
    source = text[text.index('\tpartition '):]
    headers = list(dict.fromkeys(re.findall(r'\{"([^"\n]+)",\s*(?:type \w+|Int64.Type|Currency.Type)\}', source)))
    # Include imported columns not covered by type conversions, excluding names
    # created by a later rename (which are not headers in the original file).
    renamed = set()
    for line in source.splitlines():
        if 'Table.RenameColumns(' in line:
            renamed.update(re.findall(r'\{"[^"]+",\s*"([^"]+)"\}', line))
    imported = re.findall(r'^\t\tsourceColumn: ([^\[\r\n]+)$', text, re.M)
    headers = list(dict.fromkeys(headers + [h for h in imported if h not in renamed]))
    sheet = re.search(r'Item="([^"]+)",\s*Kind="Sheet"', source)
    columns = re.search(r'Columns=(\d+)', source)
    quote_style = re.search(r'QuoteStyle=QuoteStyle\.(\w+)', source)
    return {'table': unquote(text.splitlines()[0].removeprefix('table ')),
            'file': match[1], 'sheet': sheet[1] if sheet else None,
            'headers': headers, 'csv_columns': int(columns[1]) if columns else None,
            'quote_style': quote_style[1] if quote_style else None}


def locations(root):
    reports = list(root.glob('*.Report'))
    models = list(root.glob('*.SemanticModel'))
    if len(reports) != 1 or len(models) != 1:
        raise ValueError('Esperado um diretorio .Report e um .SemanticModel')
    return reports[0], models[0]


def cell(value):
    return str(value).replace('|', '\\|').replace('\n', ' ').replace('[', '\\[').replace(']', '\\]')


def render(root):
    report, model = locations(root)
    tables = sorted((model/'definition/tables').glob('*.tmdl'), key=lambda p: p.name.casefold())
    # Git preserves casing that Windows Explorer may display differently.
    tracked = subprocess.run(['git', 'ls-files'], cwd=root, capture_output=True, text=True,
                             encoding='utf-8', check=True).stdout.splitlines()
    casing = {p.casefold(): p for p in tracked}

    def source_link(path, line=None):
        rel = path.relative_to(root).as_posix()
        rel = casing.get(rel.casefold(), rel)
        return '../' + quote(rel) + (f'#L{line}' if line else '')

    metadata = json.loads(read(report/'definition/pages/pages.json'))
    pages = {json.loads(read(p))['name']: (p, json.loads(read(p)))
             for p in (report/'definition/pages').glob('*/page.json')}
    measures = {p: parse_measures(read(p)) for p in tables}
    reltext = read(model/'definition/relationships.tmdl')
    counts = {
        'Páginas': len(pages),
        'Visuais (inclui elementos decorativos e grupos)': len(list((report/'definition/pages').glob('*/visuals/*/visual.json'))),
        'Bookmarks': len(list((report/'definition/bookmarks').glob('*.bookmark.json'))),
        'Tabelas': len(tables),
        'Colunas (inclui calculadas e ocultas)': sum(len(re.findall(r'^\tcolumn ', read(p), re.M)) for p in tables),
        'Medidas': sum(map(len, measures.values())),
        'Relacionamentos': len(re.findall(r'^relationship ', reltext, re.M)),
        'Relacionamentos bidirecionais': reltext.count('crossFilteringBehavior: bothDirections'),
        'Relacionamentos inativos': reltext.count('isActive: false'),
        'Tabelas automáticas LocalDateTable': sum(p.name.startswith('LocalDateTable_') for p in tables),
        'Funções de RLS': len(list((model/'definition/roles').glob('*.tmdl'))),
    }
    inventory = ['# Inventário do projeto', '',
                 'Gerado por `python scripts/project_catalog.py`. Não editar manualmente.', '',
                 '| Item | Quantidade |', '|---|---:|']
    inventory += [f'| {k} | {v} |' for k, v in counts.items()]
    inventory += ['', '## Parâmetros versionados', '', '| Parâmetro | Expressão padrão |', '|---|---|']
    expressions = read(model/'definition/expressions.tmdl')
    for name, value in re.findall(r'^expression (\w+) = (.+?) meta ', expressions, re.M):
        inventory.append(f'| `{name}` | `{cell(value)}` |')
    inventory += ['', '## Páginas na ordem do relatório', '',
                  '“Ativa” registra a página salva no editor; não define uma página inicial validada no serviço. Ocultação não é controle de acesso.', '',
                  '| Ordem | Página | Visuais | Visibilidade | Ativa no editor |', '|---:|---|---:|---|---|']
    for i, name in enumerate(metadata['pageOrder'], 1):
        path, page = pages[name]
        visual_count = len(list((path.parent/'visuals').glob('*/visual.json')))
        visibility = 'Oculta' if page.get('visibility') == 'HiddenInViewMode' else 'Visível'
        inventory.append(f'| {i} | [{cell(page["displayName"])}]({source_link(path)}) | {visual_count} | {visibility} | {"Sim" if name == metadata.get("activePageName") else ""} |')
    inventory += ['', '## Tabelas do modelo', '', '| Tabela | Colunas | Medidas |', '|---|---:|---:|']
    dictionary = ['# Catálogo técnico de medidas', '',
                  'Gerado por `python scripts/project_catalog.py`. Fórmulas extraídas do TMDL, sem execução DAX.', '',
                  'Nomes técnicos, formatos e fórmulas são a implementação atual, não uma homologação de negócio. Consulte [Indicadores](indicadores.md) para interpretação e critérios de conferência.', '']
    for path in tables:
        text = read(path)
        name = unquote(text.splitlines()[0].removeprefix('table '))
        ncolumns = len(re.findall(r'^\tcolumn ', text, re.M))
        inventory.append(f'| [{cell(name)}]({source_link(path)}) | {ncolumns} | {len(measures[path])} |')
        if not measures[path]:
            continue
        dictionary += [f'## {name}', '']
        for m in measures[path]:
            dictionary += [f'### `{m["name"]}`', '', f'[Fonte TMDL]({source_link(path, m["line"])})', '',
                           f'Formato: `{m["format"]}`' if m['format'] else 'Formato: não declarado na medida.', '',
                           '```dax', m['expression'], '```', '']
    contracts = [external_contract(read(p)) for p in tables if 'File.Contents(' in read(p)]
    contract_doc = ['# Contratos dos arquivos externos', '',
                    'Gerado do Power Query/TMDL. Lista campos exigidos pela importação, inclusive campos removidos depois. Não contém dados de clientes.', '',
                    r'Obtenção, responsabilidades e atualização: [Fontes e instalação](fontes-e-instalacao.md). Validação opcional: `python scripts/validate_project.py --data-dir C:\PowerBI`.', '']
    for c in contracts:
        contract_doc += [f'## {c["file"]}', '', f'Tabela: `{c["table"]}`.', '',
                         f'Aba obrigatória: `{c["sheet"]}`. Cabeçalhos na primeira linha.' if c['sheet'] else f'CSV UTF-8, separador vírgula, {c["csv_columns"]} colunas, QuoteStyle.{c["quote_style"]}. Cabeçalhos na primeira linha.', '',
                         'Cabeçalhos exigidos:', '', ', '.join(f'`{h}`' for h in c['headers']), '']
    return {'docs/inventario.md': '\n'.join(inventory) + '\n',
            'docs/catalogo-medidas.md': '\n'.join(dictionary),
            'docs/contratos-arquivos.md': '\n'.join(contract_doc),
            'docs/contratos-arquivos.json': json.dumps(contracts, ensure_ascii=False, indent=2) + '\n'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated files are stale; do not write.')
    args = parser.parse_args()
    stale = []
    for relative, content in render(ROOT).items():
        path = ROOT/relative
        if args.check:
            if not path.exists() or read(path) != content:
                stale.append(relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8', newline='\n')
            print(relative)
    if stale:
        parser.exit(1, 'Documentos desatualizados: ' + ', '.join(stale) + '\n')


if __name__ == '__main__':
    main()
