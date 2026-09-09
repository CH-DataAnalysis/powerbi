# Manutenção e validação

## Fluxo de alteração

1. Leia o [README](../README.md), o inventário e a documentação da área afetada. Registre qual indicador/fluxo muda, por quê e qual comportamento é esperado.
2. Confira `git status --short` e preserve alterações existentes. Evite editar TMDL/PBIR externamente enquanto o Desktop estiver aberto, pois ele pode sobrescrever os arquivos ao salvar.
3. Faça a alteração mínima. Em compras/vendas, mantenha sincronizados a partição de importação e `sourceExpression` da política incremental. Use `cliente` nos nomes de views específicas e `PastaArquivos` nas fontes locais.
4. Regenere os catálogos com `python scripts/project_catalog.py`; não edite manualmente inventário, catálogo de medidas ou contratos gerados.
5. Execute os checks abaixo e revise `git diff --check` e `git diff`, incluindo mudanças automáticas do Desktop.
6. Faça a homologação manual aplicável e documente evidências/pendências. Atualize `CHANGELOG.md` em **Não publicado**.
7. Encaminhe a mudança para revisão. Commit e publicação são ações separadas; a aprovação de metadados não certifica os números ou o ambiente publicado.

## Verificações automatizadas

```powershell
python -m unittest discover -s tests -v
python scripts/validate_project.py
python scripts/validate_project.py --data-dir "C:\PowerBI"
python scripts/project_catalog.py --check
git diff --check
```

| Verificação | Cobertura |
|---|---|
| Testes Python | Comportamento das ferramentas em arquivos temporários válidos/inválidos |
| Caminhos | PBIP → relatório → modelo e existência de `definition.pbism` |
| JSON | Leitura sintática de metadados; não é validação dos schemas oficiais |
| Estrutura | Tabelas referenciadas, ordem de páginas e página ativa |
| Configuração | Existência de parâmetros, intervalo de datas, `NomeTabela` por cliente e arquivos por `PastaArquivos` |
| Incremental | Correspondência do nome da fonte nas duas consultas e limites inclusivo/exclusivo |
| Documentação | Comparação dos catálogos/contratos persistidos com nova extração do código |
| Arquivos opcionais | Existência, aba XLSX, cabeçalhos e número de colunas CSV; sem validação dos valores de todas as linhas |

A CI usa Windows/Python 3.13 e roda em push, pull request e disparo manual após o workflow estar no repositório remoto. Não requer credenciais das fontes. O resultado local não comprova uma execução do GitHub Actions. A obrigatoriedade do check para merge depende de uma regra de proteção configurada pelo administrador do repositório.

## Homologação funcional e numérica

Escolha um cliente, uma loja e um período fechado com dados de referência aprovados. Registre os filtros exatos, identidade de teste, data da extração e versão do modelo. Compare com extração do sistema de origem ou relatório aprovado, usando o mesmo tratamento de devoluções, cancelamentos, datas e arredondamento.

| Cenário | Evidência e critério |
|---|---|
| Vendas, compras e estoque | Totais por loja/período coincidem com a referência; divergência explicada e aprovada antes de liberar |
| Ticket, margem e percentuais | Numerador/denominador correspondem à medida real; testar zero, vazio e devoluções |
| Filtro de período | Conferir limites inicial/final, virada de mês/ano e comparações com período anterior |
| Filtros combinados | Conferir loja, produto, fornecedor/categoria e totais após limpar filtros |
| Incremental | Conferir dados na fronteira das partições e uma correção dentro da janela, sem duplicação entre períodos |
| Cliente diferente | Conferir que todas as views parametrizadas mudaram e que não permaneceu histórico do cliente anterior |
| Navegação | Percorrer páginas analíticas do inventário pelos botões; conferir voltar, bookmarks, tooltips e limpeza de filtros |
| Sem dados | Verificar mensagem/estado do visual, cálculos vazios e ausência de valores enganosos |
| Desempenho | Medir duração da atualização e páginas principais no Performance Analyzer, com os mesmos filtros/ambiente antes e depois |

Não há limites de tempo ou tolerância de negócio aprovados no repositório. Registre-os com o responsável pelos indicadores; não trate diferença não investigada como aprovação automática. O catálogo DAX não executa essas comparações.

## Homologação de acesso

Use **Exibir como função** no Desktop e uma identidade efetiva de consumo no serviço. Confira não só os filtros de lojas, mas também fatos, totais, detalhes/exportações permitidas e logos. As restrições abaixo resumem as definições atuais, sem certificar sua propagação pelos relacionamentos.

| Função/cenário | Conferência |
|---|---|
| `Agafarma` | Rede 1 e exclusão do CNPJ explicitamente indicado no arquivo da função |
| `Asfar` | Redes 32, 66 e 156 conforme a função e o tratamento do cadastro |
| `Nossafarma - 23172` | Matriz 23172, contratos permitidos e logo esperado |
| `Dashpress` | Usuário autenticado, tag autorizada e restrições de contrato/CNPJ da função |
| Usuário sem autorização | Nenhum acesso indevido ao relatório/modelo ou a dados fora do escopo aprovado |
| Usuário com múltiplas autorizações | Conferir todas as lojas esperadas e ausência de acesso adicional; revisar o uso de `MAX(tagvalue)` na regra dinâmica |

No serviço, teste como Viewer/consumidor sujeito à RLS. Admin, Member e Contributor não são evidência válida de isolamento porque têm permissão de edição. [Documentação de RLS](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security).

## Evidências e limites

Use [registro-ambiente.example.md](registro-ambiente.example.md) para registrar responsável, execução, valores esperados/observados e decisão. Guarde dados de amostra, identidades e capturas em local operacional controlado; `docs/operacao-local/` está ignorado no Git.

Uma validação estática aprovada permite revisar os arquivos com mais confiança. A liberação no serviço ainda exige atualização real, conferência DAX/M, homologação funcional, atribuições de RLS e conectividade do gateway.
