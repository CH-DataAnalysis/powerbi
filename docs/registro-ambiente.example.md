# Registro operacional — modelo para preenchimento

Copie este arquivo para `docs/operacao-local/ambiente.md` ou para o repositório operacional corporativo. A pasta local está ignorada no Git. Os campos abaixo não representam configuração já executada. Preencha com evidências reais antes de usar o registro para publicar ou recuperar um ambiente. Não inclua senhas/tokens.

## Ambiente e responsáveis

| Campo | Valor confirmado |
|---|---|
| Ambiente (desenvolvimento/homologação/produção) | |
| Responsável pelo BI e substituto | |
| Responsável pelas fontes/Redshift/PostgreSQL | |
| Responsável pelo gateway/serviço | |
| Aprovador dos indicadores e do acesso | |
| Workspace de publicação (nome/ID) | |
| Modelo e relatório (nomes/IDs) | |
| Aplicativo/consumidores dependentes | |
| Versão do Power BI Desktop | |
| Capacidade/licença aplicável | |
| Commit/tag implantado e data/hora | |
| Commit/tag anterior homologado | |

## Conexões e atualização

| Campo | Valor confirmado |
|---|---|
| `cliente` | |
| `PastaArquivos` e caminho visto pelo gateway | |
| `RangeStart`/`RangeEnd` usados na homologação | |
| Gateway, host/nós e proprietário | |
| Conexões de arquivos e identidade com leitura | |
| Conexões Redshift/PostgreSQL e referência ao cofre de credenciais | |
| Dataflow de autorização e responsável pela atualização | |
| Agenda, fuso, dependências e prazo de conclusão | |
| Destinatários das notificações de falha | |
| Última atualização bem-sucedida e evidência | |

## Controle dos oito arquivos

Para cada arquivo de `docs/contratos-arquivos.md` (a partir da raiz do projeto), registre origem autorizada, responsável, versão/data, período coberto, periodicidade e localização da cópia anterior. Não registre apenas o nome da pasta: o rollback precisa identificar o conjunto exato utilizado.

| Arquivo | Origem/responsável | Versão e período | Periodicidade | Cópia anterior |
|---|---|---|---|---|
| cadastro_fornecedor.csv | | | | |
| geolocalizacao.csv | | | | |
| lat_long.csv | | | | |
| parceiros_pbm_padrao.csv | | | | |
| logos.xlsx | | | | |
| despesas_rel_pai_analit.xlsx | | | | |
| despesas_rel_pai_sint.xlsx | | | | |
| plano_de_contas.xlsx | | | | |

## Evidências da homologação

| Cenário/medida | Cliente/loja/período/identidade | Referência e esperado | Observado/diferença | Tolerância/aprovador | Resultado/evidência |
|---|---|---|---|---|---|
| Vendas/compras/estoque | | | | | |
| Ticket/margem/percentuais | | | | | |
| Atualização e fronteiras incrementais | | | | | |
| Navegação/bookmarks/tooltips | | | | | |
| RLS: quatro funções e usuário sem autorização | | | | | |
| Tempo de atualização/páginas principais | | | | | |

## Publicação ou rollback

| Campo | Registro |
|---|---|
| Ação, motivo/incidente e responsável | |
| Versão anterior → versão implantada | |
| Início/fim e indisponibilidade | |
| Parâmetros/conexões/RLS conferidos | |
| Resultado da atualização após a ação | |
| Teste como consumidor e página inicial | |
| Agenda reativada e aprovador | |
