CREATE MATERIALIZED VIEW associacao.mv_performance_vendedores_bi_estrategico_{cliente}
DISTSTYLE KEY
DISTKEY(cnpj)
SORTKEY(cnpj, mes, cod_vendedor_ivend)
AS
WITH d_cadastro_loja AS (
	SELECT num_cnpj, codigo_rede, sistema
	FROM associacao.dimensao_cadastro_lojas
	WHERE ( '{campo_filtro}' = 'associacao' AND codigo_rede::VARCHAR IN ({valores}) )
        OR 
        ( '{campo_filtro}' = 'num_cnpj' AND num_cnpj IN ({valores}) )
),
vendas_unificadas AS (
	SELECT v.associacao, v.num_cnpj, v.dat_emissao, v.num_nota, v.cod_reduzido,
		v.cod_vendedor_ivend, v.cod_vendedor_cvend, v.nom_vendedor_ivend,
		v.vlr_total, v.tip_venda, v.vlr_custo, v.vlr_custo_aquisicao, v.qtd_produto,
		'TRIER' AS sistema
	FROM associacao.vendas v
	WHERE v.{campo_filtro} IN ({valores})
		AND v.flg_excluido_item IS NOT TRUE
		AND v.flg_excluido_nota IS NOT TRUE
		AND v.dat_emissao >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '24 months'
		AND v.dat_emissao <= CURRENT_DATE

	UNION ALL
	
	SELECT CAST(dl.codigo_rede AS INTEGER) AS associacao, vc.num_cnpj, vc.dat_emissao, vc.num_nota, vc.cod_reduzido,
		vc.cod_vendedor_ivend, vc.cod_vendedor_cvend, vc.nom_vendedor_ivend,
		vc.vlr_total, vc.tip_venda, vc.vlr_custo, vc.vlr_custo_aquisicao, vc.qtd_produto,
		'TRIER CLOUD' AS sistema
	FROM cloud.vendas_cloud  vc
	INNER JOIN d_cadastro_loja dl ON vc.num_cnpj = dl.num_cnpj
	WHERE  vc.dat_emissao >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '24 months'
		AND vc.dat_emissao <= CURRENT_DATE
		
	UNION ALL

	SELECT CAST(dl.codigo_rede AS INTEGER) AS associacao, vp.num_cnpj, vp.dat_emissao, vp.num_nota, vp.cod_reduzido,
		vp.cod_vendedor_ivend, vp.cod_vendedor_cvend, vp.nom_vendedor_ivend,
		vp.vlr_total, 
		CASE
            WHEN TRIM(UPPER(vp.tip_venda)) = 'VENDAS' THEN 'V'
            WHEN TRIM(UPPER(vp.tip_venda)) IN ('DEVOLUCAO', 'DEVOLUÇÃO') THEN 'D'
            WHEN TRIM(UPPER(vp.tip_venda)) = 'CANCELADA' THEN 'C'
            ELSE vp.tip_venda
			END AS tip_venda, vp.vlr_custo, vp.vlr_custo_aquisicao, vp.qtd_produto,
		dl.sistema
	FROM associacao.vendas_parceiros vp
	INNER JOIN d_cadastro_loja dl ON vp.num_cnpj = dl.num_cnpj
	WHERE vp.flg_excluido_item IS NOT TRUE
		AND vp.flg_excluido_nota IS NOT TRUE
		AND vp.dat_emissao >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '24 months'
		AND vp.dat_emissao <= CURRENT_DATE
),
vendas_base AS (
    SELECT
        v.associacao,
        v.num_cnpj,
        v.dat_emissao,
        v.num_nota,
        v.cod_reduzido,
        v.cod_vendedor_ivend,
        v.cod_vendedor_cvend,
        v.nom_vendedor_ivend,
        v.vlr_total,
        v.tip_venda,
        DATE_TRUNC('month', v.dat_emissao) AS mes,
        COALESCE(v.cod_vendedor_ivend, v.cod_vendedor_cvend) AS cod_vendedor,
		CASE
            WHEN v.vlr_custo_aquisicao IS NULL THEN v.vlr_total - (v.vlr_custo * v.qtd_produto)
            ELSE v.vlr_total - v.vlr_custo_aquisicao
        END AS lucro_nota
    FROM vendas_unificadas v
),
cupons_detalhes AS (
    SELECT
        num_cnpj,
        DATE_TRUNC('month', dat_emissao) AS mes,
        num_nota,
        COUNT(*) AS qtd_itens_nota,
        MAX(COALESCE(cod_vendedor_ivend, cod_vendedor_cvend)) AS cod_vendedor,
        SUM(vlr_total) AS vlr_total_nota  -- se vlr_total for linha; caso já seja cupom, usar MAX
    FROM vendas_base
    GROUP BY num_cnpj, DATE_TRUNC('month', dat_emissao), num_nota
),
cupons_liquidos_cte AS (
    SELECT
        num_cnpj,
        cod_vendedor_ivend,
        mes,
        SUM(sinal) AS cupons_liquidos
    FROM (
        SELECT
            num_cnpj,
            mes,
            num_nota,
            MAX(cod_vendedor) AS cod_vendedor_ivend,
            MAX(
                CASE
                    WHEN tip_venda = 'V' THEN 1
                    WHEN tip_venda = 'D' THEN -1
                END
            ) AS sinal
        FROM vendas_base
        GROUP BY num_cnpj, mes, num_nota
    ) x
    WHERE cod_vendedor_ivend IS NOT NULL
    GROUP BY num_cnpj, mes, cod_vendedor_ivend
),
cupons_unico_item AS (
    SELECT
        d.num_cnpj,
        d.cod_vendedor,
        d.mes,
        SUM(
            CASE 
                WHEN b.tip_venda = 'V' THEN 1
                WHEN b.tip_venda = 'D' THEN -1
                ELSE 0
            END
        ) AS cupons_unico_item,
        SUM(
            CASE 
                WHEN b.tip_venda = 'V' THEN d.vlr_total_nota
                WHEN b.tip_venda = 'D' THEN -d.vlr_total_nota
                ELSE 0
            END
        ) AS vlr_cupons_unico_item
    FROM cupons_detalhes d
    INNER JOIN vendas_base b
        ON b.num_cnpj = d.num_cnpj
        AND b.num_nota = d.num_nota
        AND b.dat_emissao >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '24 months'
        AND b.dat_emissao <= CURRENT_DATE
    WHERE d.qtd_itens_nota = 1
    GROUP BY d.num_cnpj, d.cod_vendedor, d.mes
),
total_itens_vendidos AS (
    SELECT
        num_cnpj,
        cod_vendedor,
        mes,
        COUNT(*) AS total_itens_vendidos
    FROM vendas_base
    GROUP BY num_cnpj, cod_vendedor, mes
),
base_mensal AS (
    SELECT
        v.associacao,
        v.num_cnpj,
        v.cod_vendedor AS cod_vendedor_ivend,
        MAX(v.nom_vendedor_ivend) AS nom_vendedor_ivend,
        v.mes,
        NULLIF(MAX(c.cupons_liquidos), 0) AS qtd_atendimento,
        MAX(COALESCE(cui.cupons_unico_item, 0)) AS qtd_cupons_um_item,
        MAX(COALESCE(tiv.total_itens_vendidos, 0)) AS total_itens_vendidos,
        SUM(v.vlr_total) / NULLIF(MAX(c.cupons_liquidos), 0) AS ticket_medio,
        ROUND(
            MAX(COALESCE(tiv.total_itens_vendidos, 0))::NUMERIC / NULLIF(MAX(c.cupons_liquidos), 0),
            2
        ) AS media_itens,
        SUM(v.vlr_total - v.lucro_nota) AS lucro,
        SUM(v.vlr_total) AS total_vendas,
        MAX(COALESCE(cui.vlr_cupons_unico_item, 0)) AS vlr_cupons_um_item
    FROM vendas_base v
    LEFT JOIN cupons_liquidos_cte c
        ON c.num_cnpj = v.num_cnpj
        AND c.cod_vendedor_ivend = v.cod_vendedor
        AND c.mes = v.mes
    LEFT JOIN cupons_unico_item cui
        ON cui.num_cnpj = v.num_cnpj
        AND cui.cod_vendedor = v.cod_vendedor
        AND cui.mes = v.mes
    LEFT JOIN total_itens_vendidos tiv
        ON tiv.num_cnpj = v.num_cnpj
        AND tiv.cod_vendedor = v.cod_vendedor
        AND tiv.mes = v.mes
    GROUP BY
        v.associacao,
        v.num_cnpj,
        v.cod_vendedor,
        v.mes
),
score_competitivo AS (
    SELECT
        b.associacao AS cod_associacao,
        b.num_cnpj AS cnpj,
        b.cod_vendedor_ivend,
        b.nom_vendedor_ivend,
        TO_CHAR(b.mes, 'YYYY-MM') AS mes,
        b.total_vendas,
        b.qtd_atendimento,
        b.total_itens_vendidos,
        b.qtd_cupons_um_item,            
        b.vlr_cupons_um_item,            
        b.ticket_medio,
        b.media_itens,
        b.lucro,
        (b.lucro / NULLIF(b.total_vendas, 0)) * 100 AS lucratividade,
        COUNT(*) OVER (PARTITION BY b.num_cnpj, b.mes) AS total_vendedores_loja,
        PERCENT_RANK() OVER (
            PARTITION BY b.num_cnpj, b.mes
            ORDER BY b.qtd_atendimento
        ) * 100 AS score_atendimento,
        PERCENT_RANK() OVER (
            PARTITION BY b.num_cnpj, b.mes
            ORDER BY b.ticket_medio
        ) * 100 AS score_ticket_medio,
        PERCENT_RANK() OVER (
            PARTITION BY b.num_cnpj, b.mes
            ORDER BY b.media_itens
        ) * 100 AS score_media_itens,
        PERCENT_RANK() OVER (
            PARTITION BY b.num_cnpj, b.mes
            ORDER BY b.lucro
        ) * 100 AS score_lucro
    FROM base_mensal b
),
score_ajustado AS (
    SELECT
        sc.cod_associacao,
        sc.cnpj,
        sc.cod_vendedor_ivend,
        sc.nom_vendedor_ivend,
        sc.mes,
        sc.total_vendas,
        sc.qtd_atendimento,
        sc.qtd_cupons_um_item,           
        sc.vlr_cupons_um_item,           
        sc.total_itens_vendidos,
        sc.ticket_medio,
        sc.media_itens,
        sc.lucro,
        sc.lucratividade,
        sc.total_vendedores_loja,
        sc.score_atendimento::DECIMAL(15,2) AS score_atendimento,
        sc.score_lucro::DECIMAL(15,2) AS score_lucro,
        CASE
            WHEN sc.qtd_atendimento < 10 THEN 0
            WHEN sc.qtd_atendimento < 30 THEN sc.score_ticket_medio * (sc.qtd_atendimento::NUMERIC / 30)
            ELSE sc.score_ticket_medio
        END::DECIMAL(15,2) AS score_ticket_medio,
        CASE
            WHEN sc.qtd_atendimento < 10 THEN 0
            WHEN sc.qtd_atendimento < 30 THEN sc.score_media_itens * (sc.qtd_atendimento::NUMERIC / 30)
            ELSE sc.score_media_itens
        END::DECIMAL(15,2) AS score_media_itens
    FROM score_competitivo sc
),
score_finalizado AS (
    SELECT
        sa.*,
        LEAST(
            sa.score_atendimento,
            sa.score_ticket_medio,
            sa.score_media_itens,
            sa.score_lucro
        ) AS pior_score,
        CASE
            WHEN sa.qtd_atendimento < 30 THEN 0
            ELSE ROUND(
                sa.score_atendimento * 0.30 +
                sa.score_ticket_medio * 0.25 +
                sa.score_media_itens * 0.20 +
                sa.score_lucro * 0.25,
                2
            )
        END AS score_final
    FROM score_ajustado sa
)
SELECT
    sf.cod_associacao,
    sf.cnpj,
    sf.cod_vendedor_ivend,
    sf.nom_vendedor_ivend,
    sf.mes,
    sf.total_vendas,
    sf.qtd_atendimento,
    sf.qtd_cupons_um_item,          
    sf.vlr_cupons_um_item,          
    sf.total_itens_vendidos,
    sf.ticket_medio,
    sf.media_itens,
    sf.lucro,
    sf.lucratividade,
    sf.total_vendedores_loja,
    sf.score_atendimento,
    sf.score_lucro,
    sf.score_ticket_medio,
    sf.score_media_itens,
    sf.pior_score,
    sf.score_final,
    ROW_NUMBER() OVER (
        PARTITION BY sf.cnpj, sf.mes
        ORDER BY
            CASE WHEN sf.qtd_atendimento < 30 THEN 2 ELSE 1 END,
            sf.score_final DESC NULLS LAST,
            sf.total_vendas DESC
    ) AS ranking_vendedor,
    CASE
        WHEN sf.qtd_atendimento < 30 THEN 'Baixa Amostra'
        WHEN sf.score_final < 40 THEN 'Precisa Melhorar'
        WHEN sf.score_final < 60 THEN 'Regular'
        WHEN sf.score_final < 80 THEN 'Bom'
        ELSE 'Excelente'
    END AS classificacao_performance,
    CASE
        WHEN sf.qtd_atendimento < 30 THEN 'Baixa Amostra'
        WHEN sf.pior_score = sf.score_lucro THEN 'Lucro'
        WHEN sf.pior_score = sf.score_ticket_medio THEN 'Ticket'
        WHEN sf.pior_score = sf.score_media_itens THEN 'Itens'
        WHEN sf.pior_score = sf.score_atendimento THEN 'Atendimentos'
        ELSE 'Atendimentos'
    END AS indicador_critico,
    CASE
        WHEN sf.qtd_atendimento < 30 THEN '• Baixa Amostra'
        WHEN sf.pior_score = sf.score_lucro THEN
			'• Evitar descontos fora da política para proteger a margem
			• Oferecer genéricos e similares com maior rentabilidade
			• Sugerir produtos de marca própria sempre que possível
			• Explicar ao cliente o custo-benefício do produto sem reduzir preço
			• Analisar mix de produtos e identificar itens com maior margem potencial
			• Incentivar programas de fidelidade para aumentar recompra
			• Treinar argumentação de valor sem ceder desconto
			• Monitorar margens por categoria e ajustar estratégias'
        WHEN sf.pior_score = sf.score_ticket_medio THEN
			'• Incentivar compra de medicamentos de uso contínuo em embalagens maiores
			• Combinar higiene e beleza com medicamentos
			• Criar kits promocionais estratégicos
			• Definir meta mínima de ticket por atendimento
			• Sugerir produtos premium e complementares
			• Estimular vendas digitais (WhatsApp, online)
			• Acompanhar ticket médio diariamente'
        WHEN sf.pior_score = sf.score_media_itens THEN
			'• Sempre oferecer produtos complementares
			• Utilizar kits prontos para elevar itens por venda
			• Estabelecer meta mínima de 2 itens por atendimento
			• Incentivar segunda unidade com desconto estratégico
			• Monitorar mix e destacar produtos de maior giro
			• Treinar sugestão natural de produtos'
        ELSE
			'• Realizar abordagem ativa no balcão e telefone
			• Definir meta mínima de atendimentos por turno
			• Garantir aproveitamento total do fluxo de clientes
			• Contato proativo com clientes recorrentes
			• Monitorar tempo e qualidade do atendimento
			• Utilizar indicadores de conversão para ajustes'
    END AS plano_acao
FROM score_finalizado sf
;