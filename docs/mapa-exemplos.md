# Mapa dos exemplos de arquivos base

Levantamento de 2026-09-08, baseado nos 17 arquivos inseridos em `data-local/`, nas consultas TMDL e nos contratos gerados. Oito arquivos são fontes diretas do modelo; nove não têm referência de arquivo nas consultas atuais. Este documento especifica exemplos a criar, sem copiar os dados reais ou alterar as fontes.

## Exemplos necessários para o modelo atual

Destino proposto: `examples/arquivos-base/`. Usar os nomes originais, cabeçalhos completos e dados inteiramente fictícios. Os formatos, abas e todos os campos obrigatórios estão em [Contratos dos arquivos](contratos-arquivos.md).

| Exemplo | Estrutura obrigatória | Conteúdo mínimo sugerido |
|---|---|---|
| `cadastro_fornecedor.csv` | CSV UTF-8, vírgula; 3 colunas | 3 fornecedores fictícios, com identificadores numéricos distintos e nomes comerciais |
| `geolocalizacao.csv` | CSV UTF-8, vírgula; 32 colunas | 2 municípios com hierarquia geográfica coerente; documentar os campos de área/ponto e os que são descartados pela consulta |
| `lat_long.csv` | CSV UTF-8, vírgula; 4 colunas | 3 registros com `CEP_1`, `CEP_2`, `Latitude` e `Longitude`; preservar as quatro colunas mesmo que o modelo retenha apenas `CEP_1` |
| `parceiros_pbm_padrao.csv` | CSV UTF-8, vírgula; 3 colunas | 3 parceiros/programas fictícios com códigos distintos |
| `logos.xlsx` | Aba `Associação`; 2 colunas | 2 redes fictícias com `codigo_rede` e `link`; usar URLs demonstrativas claramente identificadas, sem prometer carregamento de imagem |
| `despesas_rel_pai_analit.xlsx` | Aba `despesas_rel_pai_analit-1768488`; 33 cabeçalhos exigidos | 2 filiais fictícias em 2 meses, com `num_cnpj`, datas e valores numéricos; incluir um caso com valores zero |
| `despesas_rel_pai_sint.xlsx` | Aba `despesas_rel_pai_sint`; 12 cabeçalhos exigidos | Mesmas filiais e meses do analítico, contas/subcontas coerentes e exemplos de valores pagos e a pagar |
| `plano_de_contas.xlsx` | Aba `Planilha1`; 4 colunas | 2 contas com subcontas; usar os mesmos códigos referenciados nas despesas sintéticas |

Os três exemplos financeiros devem ser produzidos juntos para manter coerência entre filiais, períodos e contas. Não presumir reconciliação automática: as regras de associação e os valores esperados precisam acompanhar os exemplos.

No XLSX de logos recebido há também a aba `Particular`, com `codigo_matriz` e `link`. A consulta atual lê somente `Associação`; a segunda aba não é necessária ao exemplo mínimo.

## Arquivos adicionais recebidos

Sem exemplo obrigatório para o modelo atual. A classificação abaixo não autoriza excluir os arquivos; eles podem ser úteis a outros projetos ou processos não presentes neste checkout.

| Arquivo | Evidência e tratamento proposto |
|---|---|
| `calendario.csv` | Sem referência de arquivo; `calendario` é uma tabela calculada em DAX. Não incluir no conjunto mínimo |
| `despesas_rel_pai_analit.csv` | Alternativa não consumida. Possui 32 cabeçalhos; falta `num_cnpj`, presente no XLSX de 33 colunas. Não é uma substituição direta |
| `despesas_rel_pai_sint.csv` | Alternativa não consumida; os 12 cabeçalhos correspondem aos do XLSX, mas o conector atual exige Excel e a aba indicada |
| `forma_pagto_padrao.csv` | Sem referência de arquivo. Antes de eventual integração, conferir serialização: a primeira linha lida como CSV resultou em um campo contendo `nom_condpag,forma_pagto_padrao` |
| `lat_long.txt` | Alternativa não consumida com os mesmos quatro cabeçalhos; o nome utilizado pela consulta é `lat_long.csv` |
| `parametro_rede.xlsx` | Aba `Sheet1`, 18 cabeçalhos de indicadores/parâmetros; sem referência de arquivo no modelo atual |
| `produto_gcp.csv` | Sem referência de arquivo; `produto_gcp` consulta `dimensao_cadastro_gcp` no Redshift. Um exemplo desse CSV não substitui a fonte do modelo |
| `smartped_26012026.xlsx` | Aba `Geral`, 10 cabeçalhos relacionados a pedidos; sem referência de arquivo no modelo atual |
| `usuario_logado.xlsx` | Aba `Planilha1`, cabeçalhos `usuario` e `cod_matriz`; sem referência de arquivo. A autorização atual usa o dataflow `Portal Authorization` e a identidade efetiva |

## Regras para criar os exemplos

1. Manter dados reais em `data-local/`, que está ignorada pelo Git. Criar arquivos fictícios novos em `examples/arquivos-base/`, sem reutilizar linhas reais.
2. Manter nomes de arquivo, abas e cabeçalhos exatos. Não adicionar uma linha de título antes do cabeçalho das fontes.
3. Preservar tipos e formatos compatíveis com as consultas: CSV UTF-8 com vírgula, datas e valores numéricos válidos, identificadores coerentes entre os arquivos. Não inserir rótulos como `EXEMPLO` em campos convertidos para número.
4. Incluir um README na pasta de exemplos com finalidade, cenário fictício, versão, relações entre os arquivos, valores esperados e limitações.
5. Validar o conjunto com `python scripts/validate_project.py --data-dir examples/arquivos-base` e conferir a importação no Power BI em um ambiente de teste.
6. Não apresentar os exemplos como uma demonstração completa offline: Redshift, PostgreSQL e dataflow continuam sendo dependências. Estes oito exemplos cobrem somente os arquivos locais.

## Validação dos arquivos recebidos

Executado: `python scripts/validate_project.py --data-dir data-local`.

Resultado: os oito arquivos exigidos estão presentes e passaram na conferência de abas, cabeçalhos e quantidade de colunas CSV. Os valores e tipos de todas as linhas, as relações entre os dados e a atualização real do Power BI não foram homologados.

`PastaArquivos` continua definido como `C:\PowerBI`. Inserir arquivos em `data-local/` não muda a origem do modelo. Para utilizá-los na atualização, configurar no Desktop a pasta absoluta `C:\Users\manutencao\Documents\Git\powerbi\data-local`, sem barra final. Este levantamento não alterou o parâmetro.
