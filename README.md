# Connect Hub — Power BI

Projeto de Business Intelligence para acompanhamento comercial e operacional de redes de farmácias. Reúne análises de vendas, compras, estoque, performance, captação e sugestões de compra e transferência em um relatório Power BI versionado em PBIP.

## Visão geral

```text
Connect Hub.pbip                    Entrada do projeto
Connect Hub.Report/                Relatório PBIR: páginas, visuais, bookmarks e recursos
Connect Hub.SemanticModel/         Modelo TMDL: consultas, medidas, relações e RLS
mv_performance_vendedores_bi_estrategico.sql
docs/                            Instalação, operação, indicadores e catálogos
scripts/                         Geração de catálogos e validação estática
tests/                           Testes das ferramentas
.github/workflows/validate.yml    Verificações em push e pull request
```

O Git registra os artefatos com `Connect HUB`; este checkout Windows apresenta `Connect Hub`. Use Windows para abrir e validar o PBIP, como no workflow de CI. Não renomeie somente uma das pastas sem ajustar as referências.

O [inventário gerado](docs/inventario.md) contém as quantidades atuais de páginas, visuais, bookmarks, tabelas, colunas, medidas e relacionamentos, os parâmetros e o catálogo numerado das páginas. Ele substitui a lista do README de referência, que incluía páginas ausentes deste projeto.

## Requisitos

- Windows e Power BI Desktop com suporte a PBIP, PBIR e TMDL. Se a instalação exigir habilitar recursos de visualização, siga a documentação da versão instalada. A edição otimizada para Report Server não suporta PBIP. [Documentação Microsoft](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview).
- Git para obter o projeto e executar a geração de catálogos.
- Python 3.13 para as ferramentas de verificação; não há pacotes adicionais a instalar.
- Acesso autorizado às fontes Redshift, PostgreSQL, dataflow e aos oito arquivos externos.
- Para atualização no serviço: conexões, credenciais e gateway apropriados ao ambiente.

## Como abrir e configurar

1. Clone `https://github.com/CH-DataAnalysis/powerbi.git` e entre na pasta do repositório.
2. **Antes de executar o Power BI, rode o script de implantação das views** no banco de destino, configurado para o cliente desejado. Confirme que a execução terminou com sucesso e criou as views com os nomes e a estrutura esperados pelas consultas. O identificador usado na implantação deve ser o mesmo do parâmetro `cliente` no modelo.
3. **Disponibilize os oito arquivos base localmente em `C:\PowerBI`**, conforme [Fontes e instalação](docs/fontes-e-instalacao.md), preservando nomes de arquivos, abas e cabeçalhos. Se os arquivos estiverem em `data-local/`, copie os oito arquivos necessários para `C:\PowerBI`.
4. Após preparar as views e os arquivos, abra `Connect Hub.pbip` no Power BI Desktop.
5. Em **Transformar dados → Gerenciar parâmetros**, configure `cliente`, mantenha `PastaArquivos = C:\PowerBI` e revise `RangeStart` e `RangeEnd`.
6. Configure as credenciais em **Configurações da fonte de dados**, atualize e execute a [homologação](docs/manutencao-e-validacao.md).

O script completo de implantação das views deve ser obtido com o responsável pelo ambiente. O SQL de performance dos vendedores incluído neste repositório cobre somente essa view; não substitui a implantação de todas as fontes do modelo.

`PastaArquivos` tem padrão `C:\PowerBI`, sem barra final. As oito consultas de arquivos usam esse parâmetro. Para outro computador, altere-o uma vez, mantendo os nomes de arquivo e de aba exigidos pelos [contratos](docs/contratos-arquivos.md).

## Fontes e parâmetros

| Fonte | Uso |
|---|---|
| Amazon Redshift | Views analíticas por `cliente`, cadastro GCP e dados de clientes |
| PostgreSQL | Cadastro de lojas |
| Power Platform Dataflows | Entidade `Portal Authorization` usada no controle de acesso |
| Excel e CSV | Despesas, plano de contas, logos, fornecedores, geografia e parceiros PBM |
| DAX | Calendários, medidas, classificações e tabelas auxiliares |

| Parâmetro | Finalidade |
|---|---|
| `cliente` | Sufixo das consultas `NomeTabela`; não substitui RLS |
| `PastaArquivos` | Pasta comum dos oito arquivos locais, sem barra final |
| `RangeStart` | Limite inicial inclusivo do recorte de desenvolvimento |
| `RangeEnd` | Limite final exclusivo do recorte de desenvolvimento |

Consulte os valores versionados no [inventário](docs/inventario.md). No Desktop, uma data fora do intervalo não é importada. No serviço, as partições incrementais seguem a política publicada. Vendas mantém dois anos e atualiza 15 dias; compras mantém dois anos e atualiza 30 dias. [Operação e atualização](docs/operacao.md).

## Relatório e indicadores

As páginas cobrem vendas gerenciais e detalhadas, curva ABC, PBM, crescimento, margem, descontos, performance de lojas e vendedores, áreas da farmácia, compras, sugestões, ruptura e captação. Há também páginas informativas e tooltips.

`Gerencial Vendas` é a única página marcada como visível. A página ativa salva no editor é um tooltip de classificação de mercado; confirme a página de entrada antes de publicar. Páginas ocultas não comprovam navegação funcional nem restringem acesso a dados.

- [Páginas e estrutura do modelo](docs/inventario.md).
- [Dicionário dos indicadores principais e critérios de comparação](docs/indicadores.md).
- [Catálogo completo das medidas, fórmulas DAX e fontes](docs/catalogo-medidas.md).

O catálogo técnico documenta o código atual. A conferência numérica e a aprovação das regras de negócio continuam sendo etapas de homologação.

## Segurança em nível de linha

O modelo possui as funções `Agafarma`, `Asfar`, `Dashpress` e `Nossafarma - 23172`. As definições estão na pasta `definition/roles` do modelo. A função `Dashpress` usa `USERPRINCIPALNAME()` por meio das medidas da tabela `portal_authorization`.

Teste cada função e a identidade efetiva de consumo conforme a [matriz de homologação](docs/manutencao-e-validacao.md). No serviço, usuários Admin, Member e Contributor não servem como prova de restrição RLS, pois possuem permissões de edição. [RLS na Microsoft](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security).

## Materialized view de performance dos vendedores

O [SQL fornecido](mv_performance_vendedores_bi_estrategico.sql) define a view `associacao.mv_performance_vendedores_bi_estrategico_{cliente}`. Combina vendas de Trier, Trier Cloud e parceiros, calcula agregações mensais por loja/vendedor e componentes de score. O filtro parte do início do mês de 24 meses atrás até a data corrente.

Os placeholders `{cliente}`, `{campo_filtro}` e `{valores}` dependem da implantação no banco. A equipe responsável pelo Redshift deve revisar a substituição e executar o script no ambiente adequado. As ferramentas deste repositório não executam SQL. Esse arquivo não contém o provisionamento de todas as demais views do modelo.

## Verificações e manutenção

Na raiz do projeto:

```powershell
python -m unittest discover -s tests -v
python scripts/validate_project.py
python scripts/validate_project.py --data-dir "C:\PowerBI"
```

Após mudanças no relatório, modelo ou consultas, regenere os catálogos e confira o diff:

```powershell
python scripts/project_catalog.py
python scripts/project_catalog.py --check
git diff --check
git diff
```

A CI executa testes e validação estática, sem credenciais nem acesso a fontes. Verifica JSON, caminhos PBIP/PBIR, referências de tabelas e páginas, parâmetros, uso de `cliente`, caminhos de arquivos, consistência das fontes incrementais e atualização dos catálogos. Não compila TMDL, executa M/DAX, valida valores de negócio ou publica o relatório.

O modo `--data-dir` confere existência, abas e cabeçalhos dos arquivos. Não copia dados para o repositório nem verifica todos os valores/tipos das linhas.

## Documentação operacional

| Documento | Conteúdo |
|---|---|
| [Fontes e instalação](docs/fontes-e-instalacao.md) | Obtenção dos arquivos, contratos, parâmetros, bancos e credenciais |
| [Mapa de exemplos](docs/mapa-exemplos.md) | Oito exemplos necessários e classificação dos arquivos adicionais recebidos |
| [Operação](docs/operacao.md) | Gateway, agendamento, monitoramento, publicação e rollback |
| [Manutenção e validação](docs/manutencao-e-validacao.md) | Fluxo de alterações, escopo dos checks e homologação funcional/RLS |
| [Registro de ambiente](docs/registro-ambiente.example.md) | Modelo para registrar responsáveis, conexões e evidências reais |
| [Changelog](CHANGELOG.md) | Alterações e histórico confirmado deste repositório |

Arquivos PBIX, caches, dados locais, credenciais e registros operacionais preenchidos ficam fora do Git. A documentação não implica que o gateway, o agendamento ou uma publicação tenham sido configurados no serviço.
