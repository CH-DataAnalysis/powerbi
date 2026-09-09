# Changelog

Alterações relevantes do Connect Hub. Entradas não publicadas não representam implantação no Power BI Service. O repositório não possui tags de versão na revisão de 2026-09-08; o histórico abaixo identifica commits existentes, sem presumir versões semânticas.

## Não publicado

### Adicionado

- Mapeamento dos exemplos necessários a partir dos 17 arquivos recebidos em `data-local`, distinguindo oito fontes do modelo e nove arquivos adicionais.
- Guias de instalação, obtenção das fontes, credenciais, gateway, atualização, publicação, rollback e homologação.
- Inventário gerado de páginas/modelo, catálogo técnico das medidas e contratos de cabeçalhos/abas dos oito arquivos externos.
- Dicionário dos indicadores principais e modelo de registro operacional por ambiente.
- Ferramentas Python sem dependências externas para gerar e verificar a documentação e validar metadados e arquivos locais.
- Testes das ferramentas e workflow GitHub Actions para validação estática, sem publicação.
- Documentação do SQL de performance dos vendedores fornecido junto com o README de referência.

### Alterado

- Preparação antes da execução do Power BI explicita a implantação das views por cliente e a disponibilização dos oito arquivos base em `C:\PowerBI`.
- README adaptado aos arquivos deste projeto; removidas páginas, números, parâmetros e referências de outro repositório.
- Histórico do changelog alinhado aos commits reais de `CH-DataAnalysis/powerbi`.
- Oito consultas CSV/Excel passam a usar `PastaArquivos`, com padrão `C:\PowerBI`, preservando arquivos, abas e transformações.
- `.gitignore` inclui caches Python, pasta de dados locais e registros operacionais preenchidos.

## 2026-09-08

### Corrigido

- [f503500](https://github.com/CH-DataAnalysis/powerbi/commit/f503500): consultas de compras e vendas usam o parâmetro `cliente` no nome da tabela, tanto na importação quanto na política incremental.
- [3aaa818](https://github.com/CH-DataAnalysis/powerbi/commit/3aaa818): referências PBIP/PBIR ajustadas às pastas do relatório e do modelo, removendo `Teste` dos caminhos.

## 2026-09-04

### Alterado

- [5e5036a](https://github.com/CH-DataAnalysis/powerbi/commit/5e5036a): atualização registrada com a mensagem `feat v.21`. Essa mensagem não representa uma tag de release; consulte o diff do commit para o detalhe das mudanças.

## 2026-08-26

### Adicionado

- [87c1db9](https://github.com/CH-DataAnalysis/powerbi/commit/87c1db9): primeiro commit deste repositório (`first commit`).

## Como manter

Registre alterações em **Não publicado** durante o desenvolvimento. Quando houver publicação confirmada, mova os itens para uma entrada com data e referência do commit/tag efetivamente implantado. Associe a evidência de homologação e o ambiente ao registro operacional; nunca registre uma publicação apenas porque os arquivos foram commitados.
