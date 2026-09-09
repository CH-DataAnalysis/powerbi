# Fontes e instalação

## Preparar um ambiente

O clone contém definições do relatório/modelo, não os dados necessários para atualizar. Obtenha acesso às fontes antes de executar a atualização completa. Registre a instalação usando [registro-ambiente.example.md](registro-ambiente.example.md); não preencha senhas nesse documento.

1. Instale Power BI Desktop compatível com PBIP/PBIR/TMDL no Windows e Git. Instale Python 3.13 se for executar as verificações.
2. **Antes de executar o Power BI, rode o script de implantação das views** no banco de destino, com o identificador e os filtros do cliente desejado. Obtenha esse script com o responsável pelo ambiente e confirme a conclusão sem erros, os nomes das views e a estrutura exigida pelas consultas. O `cliente` usado na implantação deve coincidir com o parâmetro do modelo. O SQL de performance dos vendedores presente no repositório cobre apenas essa view, não a implantação completa.
3. Solicite ao responsável atual pelo Connect Hub uma cópia aprovada dos oito arquivos abaixo, ou exportações equivalentes dos sistemas de origem com os mesmos contratos. O repositório não contém um endereço de download oficial nem a rotina que produz esses arquivos; não os substitua por arquivos vazios.
4. **Coloque os oito arquivos localmente em `C:\PowerBI`**, preservando nomes de arquivos, abas e cabeçalhos. Se estiverem em `data-local/`, copie os oito arquivos necessários para essa pasta antes de abrir o projeto.
5. Execute `python scripts/validate_project.py --data-dir "C:\PowerBI"` para conferir a estrutura dos arquivos. Esse comando não cria views nem altera parâmetros do modelo.
6. Após preparar as views e os arquivos, abra `Connect Hub.pbip` no Power BI Desktop. Em **Transformar dados → Gerenciar parâmetros**, mantenha `PastaArquivos = C:\PowerBI`, sem barra final.
7. Configure `cliente` e uma janela pequena de desenvolvimento com `RangeStart < RangeEnd`. Configure as credenciais das fontes, aplique as alterações e atualize.
8. Faça a conferência funcional em [Manutenção e validação](manutencao-e-validacao.md), antes da publicação.

## Arquivos obrigatórios

As responsabilidades abaixo são uma distribuição operacional sugerida, não nomes de responsáveis já confirmados. Registre o proprietário efetivo, a origem autorizada e a periodicidade de entrega de cada arquivo no registro do ambiente.

| Arquivo | Uso no modelo | Equipe a consultar para obtenção |
|---|---|---|
| `cadastro_fornecedor.csv` | Identificação de fornecedores por CNPJ | Cadastro/compras ou mantenedor do BI |
| `geolocalizacao.csv` | Dimensão geográfica | Dados/BI |
| `lat_long.csv` | Referência de CEP | Dados/BI |
| `parceiros_pbm_padrao.csv` | Padronização de parceiros PBM | Comercial/cadastro ou BI |
| `logos.xlsx` | Rede e URL do logo | Responsável pelo cadastro de redes/BI |
| `despesas_rel_pai_analit.xlsx` | Despesas e indicadores analíticos | Financeiro/controladoria |
| `despesas_rel_pai_sint.xlsx` | Valores a pagar/pagos por mês | Financeiro/controladoria |
| `plano_de_contas.xlsx` | Códigos e descrições das contas | Financeiro/controladoria |

Os [contratos gerados](contratos-arquivos.md) especificam abas, cabeçalhos, delimitador e quantidade de colunas dos CSV. Campos removidos no fim da consulta podem continuar obrigatórios na etapa de conversão de tipos. Não renomeie `despesas_rel_pai_analit-1768488` na planilha sem alterar a consulta correspondente.

Para cada entrega, registre data/hora, período coberto, origem, responsável e identificação da versão do arquivo. Substitua os arquivos fora da janela de atualização para evitar leitura durante a cópia. Retenha o conjunto anterior em armazenamento operacional controlado para rollback. Os dados não devem ser adicionados ao Git; `data-local/` é uma opção local já ignorada.

## Bancos e dataflow

| Fonte | Configuração encontrada | Acesso necessário |
|---|---|---|
| Amazon Redshift | Servidor `bc-prod.c9lkmnbigxth.us-east-1.redshift.amazonaws.com:5439`; banco `business_connect`; schema `associacao` | Leitura das views/dimensões usadas pelo modelo e acesso de rede |
| PostgreSQL | Servidor `dbneo.triersistemas.com.br`; banco `trier` | Leitura das tabelas consultadas por `tabela_cadastro_lojas` |
| Power Platform Dataflows | Workspace `c94214dd-6a97-4463-91b8-62676740c2ac`; dataflow `258d0f79-7de4-443c-880b-883cd5892eee`; entidade `Portal Authorization` | Conta organizacional autorizada a ler a entidade |

Esses identificadores descrevem o código versionado. Não comprovam conectividade ou concessão de acesso. Solicite as credenciais pelo canal corporativo e configure-as nas conexões do Desktop e do serviço; não as inclua no TMDL, README ou workflow.

Os servidores/bancos e identificadores do dataflow continuam definidos nas consultas. Para migrá-los, revise todas as ocorrências, inclusive `sourceExpression` da política incremental e `source` da partição. `PastaArquivos` parametriza somente arquivos locais.

### Seleção por cliente

`cliente` é texto e compõe o sufixo de 13 nomes distintos de views; há 15 definições `NomeTabela` porque compras e vendas repetem a consulta na política incremental. Com `cliente = "26595"`, vendas consulta `mv_vendas_produtos_26595`, e compras consulta `mv_compras_produtos_26595`.

Performance de vendedores usa o prefixo específico `mv_performance_vendedores_bi_estrategico_`. Solicite à equipe de dados confirmação de existência e atualização das views para o cliente antes de trocar o parâmetro. `mv_dados_clientes` e `dimensao_cadastro_gcp` são fontes sem sufixo no código atual; não há evidência de variantes por cliente para elas. O parâmetro não filtra automaticamente todos os cadastros e não substitui as regras de acesso.

Trocar `cliente` em um modelo já publicado com partições históricas exige tratar a recarga completa do novo conjunto de dados. Não presuma que a janela incremental curta elimina dados do cliente anterior. Prefira homologar um modelo separado para o novo cliente e planejar sua publicação.

## Credenciais e privacidade

No Desktop, abra **Arquivo → Opções e configurações → Configurações da fonte de dados** e revise cada fonte. Use o método de autenticação autorizado pela organização para o conector. Ajuste os níveis de privacidade de acordo com a classificação real dos dados; não desative a proteção global para contornar um erro de combinação.

No serviço, confira **Configurações do modelo semântico → Conexões de gateway e nuvem / Credenciais da fonte de dados**, conforme a interface disponível. A credencial local do Desktop não comprova que o serviço consegue atualizar. Para arquivos em disco/rede, siga [Operação](operacao.md).

## Diagnóstico da instalação

| Sintoma | Conferência |
|---|---|
| PBIP não abre | Executar o validador; conferir caminhos relativos e suporte da versão do Desktop |
| Arquivo não encontrado | Conferir `PastaArquivos`, nomes e acesso da conta que executa a atualização |
| Aba/campo ausente | Comparar o arquivo recebido com os contratos; não remover etapas de transformação apenas para ocultar o erro |
| View não encontrada | Conferir `cliente`, prefixo específico e provisionamento no schema `associacao` |
| Dados recentes ausentes no Desktop | Conferir `RangeEnd`, que é exclusivo; o padrão versionado pode preceder a data atual |
| Desktop atualiza, serviço não | Conferir gateway, conexões, credenciais e caminho visto pelo host do gateway |
| Autorização do portal desatualizada | Conferir a atualização do dataflow antes da atualização do modelo |

Referências: [Projetos PBIP](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview), [fontes e gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-enterprise-manage-scheduled-refresh).
