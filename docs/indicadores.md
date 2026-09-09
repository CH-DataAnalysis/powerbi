# Dicionário dos indicadores

Este documento descreve a implementação observada, não redefine regras de negócio. As fórmulas completas de todas as medidas, seus formatos e links ao TMDL estão no [catálogo técnico](catalogo-medidas.md), gerado automaticamente. Use o nome técnico exato para distinguir medidas com rótulos semelhantes.

## Indicadores principais

| Indicador | Tabela e medida | Implementação atual e unidade | Conferência necessária |
|---|---|---|---|
| Venda líquida | `mv_vendas_produtos[**venda_liquida]` | Soma de `vlr_total_venda`, com relações de produto, data e cliente ativadas na medida; valor monetário | Confirmar tratamento de devoluções/cancelamentos na view e comparar mesmo recorte |
| Quantidade vendida | `mv_vendas_produtos[*qtd_produto_venda]` | Soma de `qtd_produto_venda`; quantidade | Conferir sinais das devoluções e filtros de produto/data/cliente |
| Atendimentos líquidos | `mv_vendas_produtos[*qtd_atendimento_venda]` | Distintos `id_atendimento` com `tip_venda = V`, menos distintos com `tip_venda = D` | Conferir unicidade por loja e tratamento de devoluções |
| Ticket médio | `mv_vendas_produtos[*ticket_medio_atual_h]` | Soma das vendas dividida pelo total distinto de `id_atendimento`; `DIVIDE` retorna zero se necessário | O denominador não é a subtração V − D da medida de atendimentos líquidos |
| Margem de lucro bruta | `mv_vendas_produtos[*%margem_lucro_bruta]` | (Soma das vendas − soma de `vlr_custo_aquisicao`) / soma das vendas; percentual | Usa divisão direta; testar venda zero, devoluções e custo ausente |
| Desconto de venda | `mv_vendas_produtos[*valor_desconto_venda]` | Soma de `vlr_descto`, com relações de produto/data ativadas; valor monetário | Conferir a base de incidência antes de comparar com medidas percentuais |
| Nível de serviço | `mv_estoque[*nivel_servico]` | (`*qtd_produto_geral` − `*qtd_produto_com_ruptura_geral`) / `*qtd_produto_geral`; proporção | Consultar as medidas componentes para a população de produtos; testar denominador zero |
| Score final dos vendedores | `mv_performance_vendedores[_score_final]` | Média de `score_final`, com relação de mês ativada | Conferir a escala/regra da view e evitar supor ponderação por vendas |
| Ticket na performance dos vendedores | `mv_performance_vendedores[_ticket_medio]` | Soma da coluna `ticket_medio`, com relação de mês ativada | Não equivale necessariamente ao ticket global calculado como total de vendas / total de atendimentos |

Essas diferenças são relevantes para a comparação de páginas: medidas com nomes próximos podem usar tabelas, granularidades e denominadores distintos. A documentação não corrigiu essas fórmulas.

## Demais famílias

| Família | Fonte principal para consultar no catálogo/modelo | Interpretação e cuidado |
|---|---|---|
| Compras | `mv_compras_produtos` e `metricas_compras` | Separar valor de NF-e, compra bruta, descontos, despesas e quantidade; usar `dat_entrada` |
| Evolução de vendas/compras | `mv_dados_vendas_compras` e medidas das tabelas de fatos | Conferir se o período é fechado, mês corrente ou recorte selecionado; totais agregados podem diferir das medidas detalhadas |
| Curva ABC | `mv_curva_abc_90_dias` | Classificação e dados da view de 90 dias; conferir a data de corte na fonte |
| Estoque parado | `mv_produtos_com_estoque_sem_vendas_mais_de_90_dias` | Universo de produtos definido na view; conferir última venda/compra e data do estoque |
| Sugestões de compra/transferência | `mv_sugestao_compras`, `mv_sugestao_transferencia_filiais` | Estimativas e sugestões; validar preço, demanda e estoque usados na origem |
| Performance de loja | `mv_performance_loja` | Conferir componentes, pesos e classificação da origem antes de homologar o score |
| Captação | `mv_controle_coleta_farmacias` | Últimos registros de coleta; diferenciar falha de captação de ausência real de movimento |
| Áreas da farmácia e PBM | `medidas_areas_da_farmacia`, `mv_vendas_produtos`, `parceiros_pbm_padrao` | Conferir classificação de produtos e cadastro dos parceiros |
| Mercado e prospecção | `medidas_analise_mercado`, `medidas_prospeccao_vendas_clientes` | Há medidas no modelo; a presença de medidas não comprova uma página funcional correspondente neste relatório |

## Como homologar ou alterar um indicador

1. Identifique a medida usada pelo visual e sua fórmula no catálogo. Registre tabela, medida, página, unidade e filtros.
2. Identifique a granularidade da fonte, a data utilizada, os relacionamentos ativados e a população incluída/excluída.
3. Defina uma referência aprovada com o mesmo recorte; compare totais, denominadores e tratamento de zero/vazio/devoluções.
4. Registre esperado, observado, diferença, tolerância aprovada e decisão em uma cópia do [registro operacional](registro-ambiente.example.md).
5. Ao alterar a regra, atualize este dicionário, regenere o catálogo e registre a mudança no changelog. Homologue novamente as páginas consumidoras.

As regras de cálculo das views não estão integralmente versionadas. O SQL fornecido cobre a view de performance dos vendedores; a linhagem e as regras das demais dependem da equipe responsável pelo banco.
