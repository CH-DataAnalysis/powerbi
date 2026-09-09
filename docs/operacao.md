# Operação, publicação e rollback

Este documento define o procedimento. IDs do workspace de publicação, responsáveis, credenciais, agenda, capacidade e última versão implantada não foram confirmados no serviço. Registre os valores reais com o [modelo de registro de ambiente](registro-ambiente.example.md).

## Gateway e conexões

1. O administrador deve disponibilizar um gateway corporativo ativo em um host que alcance as fontes necessárias. Fontes que o serviço não consegue alcançar diretamente precisam de gateway. [Atualização de dados](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data).
2. Para `C:\PowerBI`, os arquivos precisam existir nesse caminho no host do gateway. Uma pasta no computador do desenvolvedor não fica automaticamente disponível ao serviço. Em cluster, garanta acesso equivalente em todos os nós. Uma pasta UNC pode centralizar o conjunto; configure permissões de leitura para a identidade usada na conexão.
3. Cadastre/mapeie as conexões de arquivos e bancos exigidas pelo modelo. Nomes de servidor e banco precisam coincidir com os usados pelo Desktop. [Configuração de fontes no gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-enterprise-manage-scheduled-refresh).
4. Associe o modelo publicado às conexões de gateway/nuvem, configure a autenticação do dataflow e revise os níveis de privacidade. Não presuma que Redshift/PostgreSQL são acessíveis pela nuvem sem verificar rede e políticas locais.
5. Confira `PastaArquivos` e `cliente` no ambiente de destino. Execute **Atualizar agora** e registre o resultado antes de habilitar uma agenda.

## Atualização incremental e dependências

| Tabela | Data de particionamento | Histórico | Janela incremental | Detecção de alteração |
|---|---|---|---|---|
| `mv_vendas_produtos` | `dat_emissao` | 2 anos | 15 dias | Máximo de `dat_atualiza` |
| `mv_compras_produtos` | `dat_entrada` | 2 anos | 30 dias | Máximo de `dat_atualiza` |

No Desktop, as consultas usam `data >= RangeStart` e `data < RangeEnd`. No serviço, a atualização incremental administra os limites das partições conforme a política; a primeira atualização após publicação prepara o histórico. A janela de desenvolvimento não é a agenda de produção. [Configuração incremental](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure).

As demais tabelas não declaram `refreshPolicy` neste projeto. Considere sua carga ao medir o tempo total. Não há rotina de agendamento das materialized views neste repositório: a equipe de dados precisa garantir que elas estejam atualizadas antes do modelo.

Ordem operacional:

1. Concluir cargas/atualizações das views no Redshift e a disponibilização dos cadastros.
2. Concluir a atualização de `Portal Authorization` no dataflow.
3. Disponibilizar o conjunto aprovado de CSV/Excel, fora de operações de cópia.
4. Atualizar o modelo semântico e conferir seu histórico de execução.
5. Conferir as datas de origem na página de captação e uma amostra dos indicadores.

Retificações mais antigas que as janelas de 15/30 dias exigem um procedimento específico para as partições afetadas ou uma recarga planejada. Não conclua que uma execução incremental bem-sucedida incorporou toda correção histórica.

## Agenda e monitoramento

O responsável pelo ambiente deve definir a frequência conforme a entrega das fontes e a capacidade disponível. Registre horário, fuso, dependências e prazo esperado de conclusão. Se a operação segue o horário de Brasília, selecione explicitamente o fuso correspondente e registre-o como `America/Sao_Paulo` na ficha operacional.

Configure os destinatários das notificações de falha no serviço. Após cada alteração de conexão, parâmetro ou política, execute uma atualização manual e examine o histórico antes de reativar o agendamento. Registre início/fim, status, mensagem de erro, quantidade de tentativas e responsável pela tratativa.

`reloadtime` usa `DateTime.LocalNow()` e registra a execução da consulta. Não comprova a data mais recente das vendas ou a conclusão de todas as fontes. Para frescor, confira também os campos de última coleta e datas máximas das tabelas relevantes.

## Publicar uma alteração

1. Identifique o commit/tag candidato e a última versão homologada. Preserve o pacote anterior e os registros de parâmetros/conexões/RLS para retorno. Não substitua arquivos de dados sem reter a versão anterior.
2. Execute os testes e o validador; regenere catálogos e revise o diff. Confirme que arquivos locais e PBIX não entraram na mudança.
3. Abra o PBIP no Desktop, confira parâmetros/fontes, atualize e conclua a [homologação](manutencao-e-validacao.md). Selecione a página de entrada desejada, salve e confira os metadados persistidos.
4. Publique primeiro no workspace de homologação definido no registro do ambiente. É possível publicar um PBIP pelo Desktop; esse fluxo usa um PBIX temporário para envio. [Publicação de projetos](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview).
5. No serviço, configure/mapeie conexões, credenciais e parâmetros. Confirme segurança e associação de usuários/grupos. Execute atualização e valide como consumidor.
6. Após aprovação registrada, publique no workspace de produção correto. Confirme a identidade dos itens que serão substituídos, o vínculo relatório/modelo e os consumidores dependentes antes de aceitar a substituição.
7. Confira novamente as conexões, RLS, atualização, página inicial e navegação. Se houver um aplicativo Power BI distribuído, atualize-o conforme o fluxo do ambiente e valide o acesso por ele.
8. Registre versão implantada, responsável, horário, IDs dos itens, evidências, agenda e versão anterior. Atualize o changelog somente com o estado efetivamente publicado.

O workflow deste repositório apenas valida. Não executa os passos de publicação, não implanta SQL e não configura o serviço.

## Rollback

Acione o retorno quando houver regressão de indicadores, acesso indevido, atualização indisponível ou navegação essencial quebrada, conforme decisão do responsável pela operação.

1. Registre o incidente e a versão atual. Se a execução estiver propagando dados incorretos, suspenda a agenda durante a recuperação; em incidente de acesso, o administrador deve conter a exposição no serviço.
2. Recupere a versão anteriormente homologada em uma pasta separada, usando seu commit/tag. Preserve a pasta de desenvolvimento atual; não use `git reset --hard` para recuperar uma publicação.
3. Restaure o conjunto anterior dos arquivos externos quando a regressão envolver dados auxiliares. Uma reversão Git não reverte arquivos externos, banco, materialized views ou dataflow.
4. Abra o PBIP anterior, configure os parâmetros/conexões registrados e confira compatibilidade com as fontes atuais. Para alteração de schema/view, coordene a restauração compatível com a equipe de dados antes da atualização.
5. Publique a versão anterior nos mesmos destinos previstos pelo plano de recuperação. Revise conexões, RLS e vínculo do relatório. Uma republicação pode exigir reconstrução do histórico incremental; dimensione o tempo e acompanhe a atualização.
6. Execute a conferência dos indicadores, acesso e navegação. Retome a agenda somente após uma atualização bem-sucedida e registre o resultado, a versão restaurada e o incidente.

O histórico Git recupera definições. A recuperação de dados, configurações do serviço e permissões depende das cópias e registros operacionais do ambiente.
