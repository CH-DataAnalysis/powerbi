# Catálogo técnico de medidas

Gerado por `python scripts/project_catalog.py`. Fórmulas extraídas do TMDL, sem execução DAX.

Nomes técnicos, formatos e fórmulas são a implementação atual, não uma homologação de negócio. Consulte [Indicadores](indicadores.md) para interpretação e critérios de conferência.

## calendario

### `dt_max`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/calendario.tmdl#L4)

Formato: `General Date`

```dax
MAX(calendario[Date])
```

## medidas_analise_mercado

### `_preco_medio_regiao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L4)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
IF(
    NOT(ISBLANK([*preco_medio_venda])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_preco_medio_municipio],
            Selecionado = "Microrregião", [_preco_medio_microrregiao],
            Selecionado = "Mesorregião", [_preco_medio_mesorregiao],
            Selecionado = "Estado", [_preco_medio_estado],
            BLANK()
        ),
    BLANK()
)
```

### `_preco_minimo_regiao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L25)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
IF(
    NOT(ISBLANK([*preco_medio_venda])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_preco_minimo_municipio],
            Selecionado = "Microrregião", [_preco_minimo_microrregiao],
            Selecionado = "Mesorregião", [_preco_minimo_mesorregiao],
            Selecionado = "Estado", [_preco_minimo_estado],
            BLANK()
        ),
    BLANK()
)
```

### `_preco_maximo_regiao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L46)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
IF(
    NOT(ISBLANK([*preco_medio_venda])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_preco_maximo_municipio],
            Selecionado = "Microrregião", [_preco_maximo_microrregiao],
            Selecionado = "Mesorregião", [_preco_maximo_mesorregiao],
            Selecionado = "Estado", [_preco_maximo_estado],
            BLANK()
        ),
    BLANK()
)
```

### `_var_preco_medio_regiao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L67)

Formato: `0.00%;-0.00%;0.00%`

```dax
IF(
    NOT(ISBLANK([*preco_medio_venda])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_var_preco_medio_municipio],
            Selecionado = "Microrregião", [_var_preco_medio_microrregiao],
            Selecionado = "Mesorregião", [_var_preco_medio_mesorregiao],
            Selecionado = "Estado", [_var_preco_medio_estado],
            BLANK()
        ),
    BLANK()
)
```

### `classificacao_precificacao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L86)

Formato: não declarado na medida.

```dax
VAR preco_medio_venda = [*preco_medio_venda]
VAR preco_medio_regiao_geral = [_preco_medio_regiao_geral]
VAR var_preco_medio_regiao_geral = [_var_preco_medio_regiao_geral]

RETURN
    IF(
        NOT ISBLANK(preco_medio_venda) &&
        NOT ISBLANK(preco_medio_regiao_geral) &&
        NOT ISBLANK(var_preco_medio_regiao_geral),
        SWITCH(
            TRUE(),
            var_preco_medio_regiao_geral < -0.10, "Abaixo do mercado",
            var_preco_medio_regiao_geral >= -0.10 && var_preco_medio_regiao_geral <= 0.10, "Na faixa competitiva",
            var_preco_medio_regiao_geral > 0.10, "Acima do mercado"
        )
    )
```

### `_numero_lojas_regiao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L106)

Formato: `#,0`

```dax
IF(
    NOT(ISBLANK([*preco_medio_venda])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_numero_lojas_municipio],
            Selecionado = "Microrregião", [_numero_lojas_microrregiao],
            Selecionado = "Mesorregião", [_numero_lojas_mesorregiao],
            Selecionado = "Estado", [_numero_lojas_estado],
            BLANK()
        ),
    BLANK()
)
```

### `qtd_produtos_faixa_normal`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L125)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral]
        ),
        [@classificacao] = "Na faixa competitiva"
    )
)
```

### `qtd_produtos_preco_competitivo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L139)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral]
        ),
        [@classificacao] = "Abaixo do mercado"
    )
)
```

### `qtd_produtos_avaliar_competitividade`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L153)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral]
        ),
        [@classificacao] = "Acima do mercado"
    )
)
```

### `qtd_total_produtos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L167)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral]
        ),
        [@classificacao] in {"abaixo do mercado","Na faixa competitiva","Acima do mercado"}
    )
)
```

### `%_qtd_produtos_preco_competitivo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L181)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([qtd_produtos_preco_competitivo], 0),
    [qtd_total_produtos],
    0
)
```

### `%_qtd_produtos_faixa_normal`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L191)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([qtd_produtos_faixa_normal], 0),
    [qtd_total_produtos],
    0
)
```

### `%_qtd_produtos_avaliar_competitividade`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L201)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([qtd_produtos_avaliar_competitividade], 0),
    [qtd_total_produtos],
    0
)
```

### `cor_fonte_classificacao_precificacao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L211)

Formato: não declarado na medida.

```dax
VAR preco_medio_venda = [*preco_medio_venda]
VAR preco_medio_regiao_geral = [_preco_medio_regiao_geral]
VAR var_preco_medio_regiao_geral = [_var_preco_medio_regiao_geral]

RETURN
    IF(
        NOT ISBLANK(preco_medio_venda) &&
        NOT ISBLANK(preco_medio_regiao_geral) &&
        NOT ISBLANK(var_preco_medio_regiao_geral),
        SWITCH(
            TRUE(),
            var_preco_medio_regiao_geral < -0.10, "#3c83f6",
            var_preco_medio_regiao_geral >= -0.10 && var_preco_medio_regiao_geral <= 0.10, "#16a249",
            var_preco_medio_regiao_geral > 0.10, "#f59f0a"
        )
    )
```

### `cor_fundo_classificacao_precificacao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L231)

Formato: não declarado na medida.

```dax
VAR preco_medio_venda = [*preco_medio_venda]
VAR preco_medio_regiao_geral = [_preco_medio_regiao_geral]
VAR var_preco_medio_regiao_geral = [_var_preco_medio_regiao_geral]

RETURN
    IF(
        NOT ISBLANK(preco_medio_venda) &&
        NOT ISBLANK(preco_medio_regiao_geral) &&
        NOT ISBLANK(var_preco_medio_regiao_geral),
        SWITCH(
            TRUE(),
            var_preco_medio_regiao_geral < -0.10, "#f5f8fb",
            var_preco_medio_regiao_geral >= -0.10 && var_preco_medio_regiao_geral <= 0.10, "#f5fbf8",
            var_preco_medio_regiao_geral > 0.10, "#faf9f6"
        )
    )
```

### `qtd_total_produtos_fora_da_faixa`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L251)

Formato: não declarado na medida.

```dax
VAR ForaFaixa =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Acima do mercado"}
        )
    )
VAR Total =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Na faixa competitiva", "Acima do mercado"}
        )
    )
RETURN
IF(
    ISBLANK(ForaFaixa) || ISBLANK(Total),
    "0 de 0",
    FORMAT(ForaFaixa, "#,##0") & " de " & FORMAT(Total, "#,##0")
)
```

### `qtd_produtos_acima_e_abaixo_da_faixa`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L283)

Formato: não declarado na medida.

```dax
VAR Acima =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral]
            ),
            [@classificacao] = "Acima do mercado"
        )
    )
VAR Abaixo =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral]
            ),
            [@classificacao] = "Abaixo do mercado"
        )
    )
RETURN
IF(
    ISBLANK(Acima) && ISBLANK(Abaixo),
    "0 acima, 0 abaixo",
    FORMAT(Acima, "#,##0") & " acima, " & FORMAT(Abaixo, "#,##0") & " abaixo"
)
```

### `_var_qtd_produtos_fora_da_faixa`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L313)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR ForaFaixa =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Acimado mercado"}
        )
    )
VAR Total =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Na faixa competitiva", "Acima do mercado"}
        )
    )
VAR Resultado = DIVIDE(ForaFaixa, Total, 0)
RETURN
IF(
    ISBLANK(Resultado) || Total = 0,
    "0.00",
    (Resultado)
)
```

### `_rank_vendas_regiao_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L345)

Formato: `#,0`

```dax
IF(
    NOT(ISBLANK([*preco_medio_venda])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_rank_vendas_municipio],
            Selecionado = "Microrregião", [_rank_vendas_microrregiao],
            Selecionado = "Mesorregião", [_rank_vendas_mesorregiao],
            Selecionado = "Estado", [_rank_vendas_estado],
            BLANK()
        ),
    BLANK()
)
```

### `_venda_liquida`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L364)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    --USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    --USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    --USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    --USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf])

)
```

### `_media_itens_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L386)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_mesorregiao[media_vendas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_numero_lojas_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L398)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_mesorregiao[numero_lojas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_maximo_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L412)

Formato: não declarado na medida.

```dax
CALCULATE(
    MAX(mv_analise_mercado_por_mesorregiao[preco_maximo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_medio_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L424)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_mesorregiao[preco_medio_simples]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_minimo_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L436)

Formato: não declarado na medida.

```dax
CALCULATE(
    MIN(mv_analise_mercado_por_mesorregiao[preco_minimo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_rank_vendas_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L449)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_mesorregiao[rank_qtd]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_mesorregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_por_mesorregiao[id_meso_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_meso_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_var_preco_medio_mesorregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L461)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [*preco_medio_venda]
VAR PrecoMercado = [_preco_medio_mesorregiao]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

### `_media_itens_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L476)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_microrregiao[media_vendas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_numero_lojas_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L488)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_microrregiao[numero_lojas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_maximo_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L500)

Formato: não declarado na medida.

```dax
CALCULATE(
    MAX(mv_analise_mercado_por_microrregiao[preco_maximo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_medio_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L512)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_microrregiao[preco_medio_simples]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_minimo_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L524)

Formato: não declarado na medida.

```dax
CALCULATE(
    MIN(mv_analise_mercado_por_microrregiao[preco_minimo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_rank_vendas_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L537)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_microrregiao[rank_qtd]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_microrregiao[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_por_microrregiao[id_micro_regiao]),
    USERELATIONSHIP(mv_vendas_produtos[id_micro_regiao],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_var_preco_medio_microrregiao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L549)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [*preco_medio_venda]
VAR PrecoMercado = [_preco_medio_microrregiao]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

### `_media_itens_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L564)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_municipio[media_vendas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_numero_lojas_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L576)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_municipio[numero_lojas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_maximo_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L588)

Formato: não declarado na medida.

```dax
CALCULATE(
    MAX(mv_analise_mercado_por_municipio[preco_maximo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_medio_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L600)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_municipio[preco_medio_simples]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_minimo_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L612)

Formato: não declarado na medida.

```dax
CALCULATE(
    MIN(mv_analise_mercado_por_municipio[preco_minimo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_rank_vendas_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L625)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_municipio[rank_qtd]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_municipio[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_por_municipio[id_municipio]),
    USERELATIONSHIP(mv_vendas_produtos[id_municipio],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_var_preco_medio_municipio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L637)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR PrecoVenda = [*preco_medio_venda]
VAR PrecoMercado = [_preco_medio_municipio]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

### `_media_itens_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L651)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_uf[media_vendas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_numero_lojas_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L665)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_uf[numero_lojas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_maximo_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L677)

Formato: não declarado na medida.

```dax
CALCULATE(
    MAX(mv_analise_mercado_por_uf[preco_maximo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_classificacao[id_regiao])    
)
```

### `_preco_medio_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L690)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_uf[preco_medio_simples]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_preco_minimo_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L704)

Formato: não declarado na medida.

```dax
CALCULATE(
    MIN(mv_analise_mercado_por_uf[preco_minimo]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_classificacao[id_regiao])
)
```

### `_rank_vendas_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L717)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_analise_mercado_por_uf[rank_qtd]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_analise_mercado_por_uf[cod_barra]),
    USERELATIONSHIP(mv_vendas_produtos[id_uf],mv_analise_mercado_por_uf[id_uf]),
    USERELATIONSHIP(mv_analise_mercado_classificacao[id_regiao],mv_vendas_produtos[id_uf])
)
```

### `_var_preco_medio_estado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado.tmdl#L729)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [*preco_medio_venda]
VAR PrecoMercado = [_preco_medio_estado]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

## medidas_analise_mercado_simulacao

### `_preco_medio_venda_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L4)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR preco_medio_original = [*preco_medio_venda]
VAR ajuste = [percentual_simulacao_selecionado]
RETURN
    preco_medio_original * (1 + (ajuste))
```

### `_var_preco_medio_regiao_geral_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L15)

Formato: `0.00%;-0.00%;0.00%`

```dax
IF(
    NOT(ISBLANK([_preco_medio_venda_simulacao])),
    VAR Selecionado = SELECTEDVALUE(medidas_analise_mercado[botao], "Município")
    RETURN
        SWITCH(
            TRUE(),
            Selecionado = "Município", [_var_preco_medio_municipio_simulacao],
            Selecionado = "Microrregião", [_var_preco_medio_microrregiao_simulacao],
            Selecionado = "Mesorregião", [_var_preco_medio_mesorregiao_simulacao],
            Selecionado = "Estado", [_var_preco_medio_estado_simulacao],
            BLANK()
        ),
    BLANK()
)
```

### `classificacao_precificacao_geral_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L34)

Formato: não declarado na medida.

```dax
VAR preco_medio_venda = [_preco_medio_venda_simulacao]
VAR preco_medio_regiao_geral = [_preco_medio_regiao_geral]
VAR var_preco_medio_regiao_geral_simulacao = [_var_preco_medio_regiao_geral_simulacao]

RETURN
    IF(
        NOT ISBLANK(preco_medio_venda) &&
        NOT ISBLANK(preco_medio_regiao_geral) &&
        NOT ISBLANK(var_preco_medio_regiao_geral_simulacao),
        SWITCH(
            TRUE(),
            var_preco_medio_regiao_geral_simulacao < -0.10, "Abaixo do mercado",
            var_preco_medio_regiao_geral_simulacao >= -0.10 && var_preco_medio_regiao_geral_simulacao <= 0.10, "Na faixa competitiva",
            var_preco_medio_regiao_geral_simulacao > 0.10, "Acima do mercado"
        )
    )
```

### `qtd_total_produtos_fora_da_faixa_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L54)

Formato: não declarado na medida.

```dax
VAR ForaFaixa =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral_simulacao]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Acima do mercado"}
        )
    )
VAR Total =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral_simulacao]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Na faixa competitiva", "Acima do mercado"}
        )
    )
RETURN
IF(
    ISBLANK(ForaFaixa) || ISBLANK(Total),
    "0 de 0",
    FORMAT(ForaFaixa, "#,##0") & " de " & FORMAT(Total, "#,##0")
)
```

### `qtd_total_produtos_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L84)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral_simulacao]
        ),
        [@classificacao] in {"abaixo do mercado","Na faixa competitiva","Acima do mercado"}
    )
)
```

### `qtd_produtos_preco_competitivo_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L98)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral_simulacao]
        ),
        [@classificacao] = "Abaixo do mercado"
    )
)
```

### `qtd_produtos_faixa_normal_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L112)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral_simulacao]
        ),
        [@classificacao] = "Na faixa competitiva"
    )
)
```

### `qtd_produtos_avaliar_competitividade_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L126)

Formato: `#,0`

```dax
COUNTROWS(
    FILTER(
        ADDCOLUMNS(
            VALUES(produto_gcp[cod_barra]),
            "@classificacao", [classificacao_precificacao_geral_simulacao]
        ),
        [@classificacao] = "Acima do mercado"
    )
)
```

### `qtd_produtos_acima_e_abaixo_da_faixa_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L140)

Formato: não declarado na medida.

```dax
VAR Acima =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral_simulacao]
            ),
            [@classificacao] = "Acima do mercado"
        )
    )
VAR Abaixo =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral_simulacao]
            ),
            [@classificacao] = "Abaixo do mercado"
        )
    )
RETURN
IF(
    ISBLANK(Acima) && ISBLANK(Abaixo),
    "0 acima, 0 abaixo",
    FORMAT(Acima, "#,##0") & " acima, " & FORMAT(Abaixo, "#,##0") & " abaixo"
)
```

### `cor_fundo_classificacao_precificacao_geral_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L170)

Formato: não declarado na medida.

```dax
VAR preco_medio_venda = [_preco_medio_venda_simulacao]
VAR preco_medio_regiao_geral = [_preco_medio_regiao_geral]
VAR var_preco_medio_regiao_geral = [_var_preco_medio_regiao_geral_simulacao]

RETURN
    IF(
        NOT ISBLANK(preco_medio_venda) &&
        NOT ISBLANK(preco_medio_regiao_geral) &&
        NOT ISBLANK(var_preco_medio_regiao_geral),
        SWITCH(
            TRUE(),
            var_preco_medio_regiao_geral < -0.10, "#f5f8fb",
            var_preco_medio_regiao_geral >= -0.10 && var_preco_medio_regiao_geral <= 0.10, "#f5fbf8",
            var_preco_medio_regiao_geral > 0.10, "#faf9f6"
        )
    )
```

### `cor_fonte_classificacao_precificacao_geral_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L190)

Formato: não declarado na medida.

```dax
VAR preco_medio_venda = [_preco_medio_venda_simulacao]
VAR preco_medio_regiao_geral = [_preco_medio_regiao_geral]
VAR var_preco_medio_regiao_geral = [_var_preco_medio_regiao_geral_simulacao]

RETURN
    IF(
        NOT ISBLANK(preco_medio_venda) &&
        NOT ISBLANK(preco_medio_regiao_geral) &&
        NOT ISBLANK(var_preco_medio_regiao_geral),
        SWITCH(
            TRUE(),
            var_preco_medio_regiao_geral < -0.10, "#3c83f6",
            var_preco_medio_regiao_geral >= -0.10 && var_preco_medio_regiao_geral <= 0.10, "#16a249",
            var_preco_medio_regiao_geral > 0.10, "#f59f0a"
        )
    )
```

### `_var_qtd_produtos_fora_da_faixa_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L210)

Formato: não declarado na medida.

```dax
VAR ForaFaixa =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral_simulacao]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Acima do mercado"}
        )
    )
VAR Total =
    COUNTROWS(
        FILTER(
            ADDCOLUMNS(
                VALUES(produto_gcp[cod_barra]),
                "@classificacao", [classificacao_precificacao_geral_simulacao]
            ),
            [@classificacao] IN {"Abaixo do mercado", "Na faixa competitiva", "Acima do mercado"}
        )
    )
VAR Resultado = DIVIDE(ForaFaixa, Total, 0)
RETURN
IF(
    ISBLANK(Resultado) || Total = 0,
    "0.00%",
    FORMAT(Resultado, "0.00%")
)
```

### `%_qtd_produtos_avaliar_competitividade_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L241)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([qtd_produtos_avaliar_competitividade_simulacao], 0),
    [qtd_total_produtos_simulacao],
    0
)
```

### `%_qtd_produtos_faixa_normal_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L251)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([qtd_produtos_faixa_normal_simulacao], 0),
    [qtd_total_produtos_simulacao],
    0
)
```

### `%_qtd_produtos_preco_competitivo_simmulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L261)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([qtd_produtos_preco_competitivo_simulacao], 0),
    [qtd_total_produtos_simulacao],
    0
)
```

### `filtro_classificacao_precificacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L271)

Formato: `0`

```dax
VAR classificacao_selecionada = SELECTEDVALUE('classificacao_precificacao'[classificacao], "Todos")
VAR classificacao_precificacao = [_var_preco_medio_regiao_geral]
RETURN
SWITCH(
    TRUE(),
    classificacao_selecionada = "Todos", 1,
    classificacao_selecionada = "Abaixo do mercado" && classificacao_precificacao < -0.10, 1,
    classificacao_selecionada = "Faixa normal" && classificacao_precificacao >= -0.10 && classificacao_precificacao <= 0.10, 1,
    classificacao_selecionada = "Avaliar competitividade" && classificacao_precificacao > 0.10, 1
)
```

### `_var_preco_medio_mesorregiao_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L286)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [_preco_medio_venda_simulacao]
VAR PrecoMercado = [_preco_medio_mesorregiao]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

### `_var_preco_medio_microrregiao_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L301)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [_preco_medio_venda_simulacao]
VAR PrecoMercado = [_preco_medio_microrregiao]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

### `_var_preco_medio_municipio_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L316)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [_preco_medio_venda_simulacao]
VAR PrecoMercado = [_preco_medio_municipio]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

### `_var_preco_medio_estado_simulacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_analise_mercado_simulacao.tmdl#L331)

Formato: não declarado na medida.

```dax
VAR PrecoVenda = [_preco_medio_venda_simulacao]
VAR PrecoMercado = [_preco_medio_estado]

RETURN
IF(
    NOT ISBLANK(PrecoMercado),
    DIVIDE(PrecoVenda - PrecoMercado, PrecoMercado),
    BLANK()
)
```

## medidas_areas_da_farmacia

### `*%var_alimentos_bebidas_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L4)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*alimentos_bebidas_mes_atual] - [*alimentos_bebidas_mes_anterior]) / [*alimentos_bebidas_mes_anterior])
```

### `*%var_conveniencia_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L8)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*conveniencia_mes_atual] - [*conveniencia_mes_anterior]) / [*conveniencia_mes_anterior])
```

### `*%var_cuidado_infantil_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L12)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*cuidado_infantil_mes_atual] - [*cuidado_infantil_mes_anterior]) / [*cuidado_infantil_mes_anterior])
```

### `*%var_cuidados_ao_paciente_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L16)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*cuidados_ao_paciente_mes_atual] - [*cuidados_ao_paciente_mes_anterior]) / [*cuidados_ao_paciente_mes_anterior])
```

### `*%var_dermocosmeticos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L20)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*dermocosmeticos_mes_atual] - [*dermocosmeticos_mes_anterior]) / [*dermocosmeticos_mes_anterior])
```

### `*%var_higiene_pessoal_perfumaria_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L24)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*higiene_pessoal_perfumaria_mes_atual] - [*higiene_pessoal_perfumaria_mes_anterior]) / [*higiene_pessoal_perfumaria_mes_anterior])
```

### `*%var_nutricosmeticos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L28)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*nutricosmeticos_mes_atual] - [*nutricosmeticos_mes_anterior]) / [*nutricosmeticos_mes_anterior])
```

### `*%var_otc_mip_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L32)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*otc_mip_mes_atual] - [*otc_mip_mes_anterior]) / [*otc_mip_mes_anterior])
```

### `*%var_prescricao_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L36)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*prescricao_mes_atual] - [*prescricao_mes_anterior]) / [*prescricao_mes_anterior])
```

### `*%var_saude_sexual_masculina_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L40)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*saude_sexual_masculina_mes_atual] - [*saude_sexual_masculina_mes_anterior]) / [*saude_sexual_masculina_mes_anterior])
```

### `*%var_tratamento_dermatologicos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L44)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*tratamento_dermatologicos_mes_atual] - [*tratamento_dermatologicos_mes_anterior]) / [*tratamento_dermatologicos_mes_anterior])
```

### `*alimentos_bebidas`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L48)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "ALIMENTOS E BEBIDAS"
    )
)
```

### `*alimentos_bebidas_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L62)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "ALIMENTOS E BEBIDAS")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*alimentos_bebidas_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L82)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX ( calendario[Date] )
VAR DataMesAnterior =
    EDATE ( DataAtual, -1 )
-- Último dia carregado do mês atual
VAR DataLimiteMesAtual =
    CALCULATE (
        MAX ( mv_vendas_produtos[dat_emissao] ),
        USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
        USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        FILTER (
            ALL ( calendario ),
            calendario[ano_mes_numero] = MAX ( calendario[ano_mes_numero] )
        )
    )
-- Último dia do calendário no mês atual
VAR UltimoDiaMesAtual =
    CALCULATE (
        MAX ( calendario[Date] ),
        FILTER (
            ALL ( calendario ),
            calendario[ano_mes_numero] = MAX ( calendario[ano_mes_numero] )
        )
    )
-- Definição de até qual dia usar no mês anterior
VAR DiaLimiteMesAnterior =
    IF (
        DataLimiteMesAtual = UltimoDiaMesAtual,
        DAY ( EOMONTH ( DataMesAnterior, 0 ) ), -- mês fechado → usa último dia real
        DAY ( DataLimiteMesAtual )             -- mês aberto → usa mesmo dia limite
    )
RETURN
    CALCULATE (
        SUM ( mv_vendas_produtos[vlr_total_venda] ),
        USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
        USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        KEEPFILTERS ( produto_gcp[area_farmacia] = "ALIMENTOS E BEBIDAS" ),
        FILTER (
            ALL ( calendario ),
            calendario[Date] >= DATE ( YEAR ( DataMesAnterior ), MONTH ( DataMesAnterior ), 1 )
                && calendario[Date] <= DATE ( YEAR ( DataMesAnterior ), MONTH ( DataMesAnterior ), DiaLimiteMesAnterior )
        )
    )
```

### `*alimentos_bebidas_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L133)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*alimentos_bebidas],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*conveniencia`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L146)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "CONVENIÊNCIA"
    )
)
```

### `*conveniencia_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L160)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "CONVENIÊNCIA")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*conveniencia_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L180)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*conveniencia],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*conveniencia_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L227)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*conveniencia],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*cuidado_infantil`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L240)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "CUIDADO BEBÊ/INFANTIL"
    )
)
```

### `*cuidado_infantil_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L254)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "CUIDADO BEBÊ/INFANTIL")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*cuidado_infantil_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L274)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*cuidado_infantil],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*cuidado_infantil_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L321)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*cuidado_infantil],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*cuidados_ao_paciente`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L334)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "CUIDADOS AO PACIENTE"
    )
)
```

### `*cuidados_ao_paciente_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L348)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "CUIDADOS AO PACIENTE")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*cuidados_ao_paciente_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L368)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*cuidados_ao_paciente],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*cuidados_ao_paciente_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L415)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*cuidados_ao_paciente],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*dermocosmeticos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L428)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "DERMOCOSMETICOS"
    )
)
```

### `*dermocosmeticos_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L442)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "DERMOCOSMETICOS")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*dermocosmeticos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L462)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*dermocosmeticos],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*dermocosmeticos_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L509)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*dermocosmeticos],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*higiene_pessoal_perfumaria`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L522)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "HIGIENE PESSOAL, PERFUMARIA E COSMÉTICOS"
    )
)
```

### `*higiene_pessoal_perfumaria_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L536)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "HIGIENE PESSOAL, PERFUMARIA E COSMÉTICOS")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*higiene_pessoal_perfumaria_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L556)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*higiene_pessoal_perfumaria],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*higiene_pessoal_perfumaria_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L603)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*higiene_pessoal_perfumaria],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*nutricosmeticos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L616)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "NUTRICOSMÉTICOS"
    )
)
```

### `*nutricosmeticos_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L630)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "NUTRICOSMÉTICOS")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*nutricosmeticos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L650)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*nutricosmeticos],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*nutricosmeticos_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L697)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*nutricosmeticos],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*otc_mip`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L710)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "OTC"
    )
)
```

### `*otc_mip_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L724)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "OTC")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*otc_mip_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L744)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*otc_mip],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*otc_mip_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L791)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*otc_mip],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*prescricao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L804)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "PRESCRIÇÃO"
    )
)
```

### `*prescricao_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L818)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "PRESCRIÇÃO")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*prescricao_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L838)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*prescricao],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*prescricao_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L885)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*prescricao],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*saude_sexual_masculina`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L898)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "SAÚDE SEXUAL E SAÚDE MASCULINA"
    )
)
```

### `*saude_sexual_masculina_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L912)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "SAÚDE SEXUAL E SAÚDE MASCULINA")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*saude_sexual_masculina_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L932)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*saude_sexual_masculina],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*saude_sexual_masculina_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L979)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*saude_sexual_masculina],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*tratamento_dermatologicos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L992)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE( 
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "TRATAMENTOS DERMATOLÓGICOS"
    )
)
```

### `*tratamento_dermatologicos_%`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L1006)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    FILTER(produto_gcp, produto_gcp[area_farmacia] = "TRATAMENTOS DERMATOLÓGICOS")
    ),
    CALCULATE(
    SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])

    )
)
```

### `*tratamento_dermatologicos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L1026)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP ( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    [*tratamento_dermatologicos],
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*tratamento_dermatologicos_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_areas_da_farmacia.tmdl#L1073)

Formato: não declarado na medida.

```dax
CALCULATE(
    [*tratamento_dermatologicos],
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

## medidas_performance_vendedor

### `filtro_classificacao_performance_vendedor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_performance_vendedor.tmdl#L4)

Formato: `0`

```dax
VAR classificacao_selecionada = SELECTEDVALUE('classificacao_performance_vendedor'[classificacao], "Todos")
VAR classificacao_geral = [_score_final]
RETURN
SWITCH(
    TRUE(),
    classificacao_selecionada = "Todos", 1,
    classificacao_selecionada = "1 - Ruim" && classificacao_geral >= 0 && classificacao_geral < 40, 1,
    classificacao_selecionada = "3 - Regular" && classificacao_geral >= 40 && classificacao_geral < 60, 1,
    classificacao_selecionada = "2 - Bom" && classificacao_geral >= 60 && classificacao_geral < 80, 1,
    classificacao_selecionada = "4 - Excelente" && classificacao_geral >= 80 && classificacao_geral <= 100, 1,
    0
)
```

## medidas_prospeccao_vendas_clientes

### `pvc_frequencia`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L4)

Formato: não declarado na medida.

```dax
VAR QtdCompras =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    )
VAR MesesAtivos =
    CALCULATE(
        DISTINCTCOUNT(calendario[ano_mes_numero]),
        DATESBETWEEN(
            calendario[Date],
            MINX(ALLSELECTED(calendario), calendario[Date]),
            MAXX(ALLSELECTED(calendario), calendario[Date])
        )
    )
RETURN
DIVIDE(QtdCompras, MesesAtivos,0)
```

### `pvc_meses_analisados`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L28)

Formato: `0`

```dax
VAR MesesAtivos =
    CALCULATE(
        DISTINCTCOUNT(calendario[ano_mes_numero]),
        DATESBETWEEN(
            calendario[Date],
            MINX(ALLSELECTED(calendario), calendario[Date]),
            MAXX(ALLSELECTED(calendario), calendario[Date])
        )
    )
RETURN
MesesAtivos
```

### `pvc_meses_com_compras`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L44)

Formato: `0`

```dax
VAR MesesComCompra =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[AnoMes]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    )
RETURN
    MesesComCompra
```

### `pvc_meses_com_compras_pct`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L58)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR MesesComCompra =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[AnoMes]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])

    )
VAR MesesAtivos =
    CALCULATE(
        DISTINCTCOUNT(calendario[ano_mes_numero]),
        DATESBETWEEN(
            calendario[Date],
            MINX(ALLSELECTED(calendario), calendario[Date]),
            MAXX(ALLSELECTED(calendario), calendario[Date])
        )
    )
RETURN
DIVIDE(MesesComCompra, MesesAtivos, 0)
```

### `pvc_ticket_medio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L84)

Formato: não declarado na medida.

```dax
VAR TotalVendas =
    CALCULATE(
        SUM(mv_vendas_produtos[vlr_total_venda]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    )
VAR TotalAtendimentos =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente]) 
    )
RETURN
DIVIDE(TotalVendas, TotalAtendimentos, 0)
```

### `pvc_qtd_clientes`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L107)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT(mv_vendas_produtos[cod_cliente]),
USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `_frequencia`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L118)

Formato: não declarado na medida.

```dax
VAR QtdCompras =
    CALCULATE(
        DISTINCTCOUNT( mv_vendas_produtos[id_atendimento] ),
        USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
        USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )
    )
VAR Clientes =
    CALCULATE(
        DISTINCTCOUNT( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] )
    )
VAR MesesAtivos =
    CALCULATE(
        DISTINCTCOUNT( calendario[ano_mes_numero] ),
        DATESBETWEEN(
            calendario[Date],
            MINX( ALLSELECTED(calendario), calendario[Date] ),
            MAXX( ALLSELECTED(calendario), calendario[Date] )
        )
    )
RETURN
DIVIDE( DIVIDE(QtdCompras, Clientes, 0), MesesAtivos, 0 )
```

### `_clientes_retidos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L147)

Formato: `0`

```dax
VAR MesAtual =
    MAX( calendario[ano_mes_numero] )
VAR MesAnterior =
    MesAtual - 1
VAR ClientesPeriodoAtual =
    CALCULATETABLE(
        VALUES( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] ),
        calendario[ano_mes_numero] = MesAtual
    )
VAR ClientesPeriodoAnterior =
    CALCULATETABLE(
        VALUES( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] ),
        calendario[ano_mes_numero] = MesAnterior
    )
RETURN
COUNTROWS( INTERSECT( ClientesPeriodoAtual, ClientesPeriodoAnterior ) )
```

### `_taxa_retencao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L172)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [_clientes_retidos],
    CALCULATE(
        DISTINCTCOUNT( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
        USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )
    ),
    0
)
```

### `_clientes_recorrentes`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L187)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT( mv_vendas_produtos[cod_cliente] ),
    FILTER(
        VALUES( mv_vendas_produtos[cod_cliente] ),
        CALCULATE(
            COUNTROWS( mv_vendas_produtos ),
            USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )
        ) > 1
    )
)
```

### `_%clientes_recorrentes`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L204)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [_clientes_recorrentes],
    CALCULATE(
        DISTINCTCOUNT( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
        USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )
    ),
    0
)
```

### `_relacionamento_medio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L219)

Formato: não declarado na medida.

```dax
AVERAGEX(
    VALUES( mv_vendas_produtos[cod_cliente] ),
    DATEDIFF(
        CALCULATE(
            MIN( mv_vendas_produtos[dat_emissao] ),
            USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )
        ),
        CALCULATE(
            MAX( mv_vendas_produtos[dat_emissao] ),
            USERELATIONSHIP( calendario[Date], mv_vendas_produtos[dat_emissao] ),
            USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )
        ),
        MONTH
    )
)
```

### `_clientes_novos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L243)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_vendas_produtos[cod_cliente]),
    FILTER(
        VALUES(mv_vendas_produtos[cod_cliente]),
        CALCULATE(
            COUNTROWS(mv_vendas_produtos),
            USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
            USERELATIONSHIP( produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado] ),
            USERELATIONSHIP( mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente] )            
        ) = 1
    )
)
```

### `_clientes_retidos_mes`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L261)

Formato: `0`

```dax
VAR MesAtual =
    SELECTEDVALUE ( calendario[ano_mes_numero] )
VAR MesAnterior =
    MesAtual - 1
VAR ClientesAtual =
    CALCULATETABLE (
        VALUES ( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        FILTER ( ALL ( calendario ), calendario[ano_mes_numero] = MesAtual )
    )
VAR ClientesAnterior =
    CALCULATETABLE (
        VALUES ( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        FILTER ( ALL ( calendario ), calendario[ano_mes_numero] = MesAnterior )
    )
RETURN
COUNTROWS ( INTERSECT ( ClientesAtual, ClientesAnterior ) )
```

### `__clientes_retidos_mes`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/medidas_prospeccao_vendas_clientes.tmdl#L284)

Formato: `0`

```dax
VAR MesAtual = MAX ( calendario[ano_mes_numero] )
VAR MesAnterior = MesAtual - 1
VAR ClientesPeriodo =
    CALCULATETABLE (
        VALUES ( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        FILTER ( ALL ( calendario ), calendario[ano_mes_numero] = MesAtual )
    )
VAR ClientesPeriodoAnterior =
    CALCULATETABLE (
        VALUES ( mv_vendas_produtos[cod_cliente] ),
        USERELATIONSHIP ( calendario[Date], mv_vendas_produtos[dat_emissao] ),
        FILTER ( ALL ( calendario ), calendario[ano_mes_numero] = MesAnterior )
    )
RETURN
COUNTROWS ( INTERSECT ( ClientesPeriodo, ClientesPeriodoAnterior ) )
```

## metricas_vendas1item

### `Cor_%_Cupons_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/metricas_vendas1item.tmdl#L4)

Formato: não declarado na medida.

```dax
VAR Indice =
    mv_vendas_produtos[**%_Cupons_1_Item]

RETURN
    SWITCH(
        TRUE(),
        Indice >= 0.80, "#fc282f",   -- Emergencial
        Indice >= 0.50, "#f87171",   -- Crítico
        Indice >= 0.20, "#fcba03",   -- Atenção
        "#00689F"                    -- Normal
    )
```

### `Cor_%LucroPerdido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/metricas_vendas1item.tmdl#L19)

Formato: não declarado na medida.

```dax
VAR Valor =
    [***%LucroPerdido]

RETURN
    IF(
        Valor < 0,
        "#C00000",
        "#008000"
    )
```

## mv_compras_produtos

### `**%var_sku_compra_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L41)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE([**sku_compra_ano_atual] - [**sku_compra_ano_anterior],[**sku_compra_ano_anterior],0)
```

### `**%var_sku_compra_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L45)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([**sku_compra_mes_atual] - [**sku_compra_mes_anterior]) / [**sku_compra_mes_anterior])
```

### `**sku_compra_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L49)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    DISTINCTCOUNT(mv_compras_produtos[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada]),    
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `**sku_compra_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L76)

Formato: `0`

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    DISTINCTCOUNT(mv_compras_produtos[cod_barra]),
    REMOVEFILTERS(calendario),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada]),
    calendario[ano] = AnoAtual
)
```

### `**sku_compra_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L92)

Formato: `0`

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_dados_vendas_compras[dat_emissao]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    DISTINCTCOUNT(mv_compras_produtos[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `**sku_compra_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L138)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_compras_produtos[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada]),    
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*%valor_total_descto`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L153)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
DIVIDE(
SUM('mv_compras_produtos'[vlr_total_descto]), sum(mv_compras_produtos[vlr_total_compra_bruta])),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*qtd_produto_compra`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L164)

Formato: `#,0`

```dax
CALCULATE(
SUM('mv_compras_produtos'[qtd_produto_compra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_descto`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L173)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_descto]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_despesas_acessorias`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L184)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_despacess]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_icms_retido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L195)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_icmsret]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_nfe`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L206)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_nfe]), 0),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado])
)
```

### `filtro_alerta_desconto_compra`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L217)

Formato: `0`

```dax
VAR alertaselecionado = SELECTEDVALUE('alerta_desconto_compra'[alerta], "Todos")
VAR desconto = [*%valor_total_descto]
RETURN
SWITCH(
    TRUE(),
    alertaselecionado = "Todos", 1,
    alertaselecionado = "> que 10%" && desconto > 0.1, 1,
	alertaselecionado = "> que 20%" && desconto > 0.2, 1,
	alertaselecionado = "> que 30%" && desconto > 0.3, 1,
	alertaselecionado = "> que 40%" && desconto > 0.4, 1,
	alertaselecionado = "> que 50%" && desconto > 0.5, 1,
    0
)
```

### `*valor_total_produto`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L235)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_compra_bruta]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_frete`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L246)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_frete]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_ipi`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L257)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_ipi]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_seguro`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L268)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_seguro]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*valor_total_icms`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L279)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    COALESCE(SUM(mv_compras_produtos[vlr_total_icms]), 0),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*sku_compra`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L290)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_compras_produtos[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*preco_medio_custo_aq`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L299)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
COALESCE(
    CALCULATE(
        AVERAGE(mv_compras_produtos[cmv_compras]),
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_compras_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_compras_produtos[dat_entrada]
        )
    ),
    0
)
```

### `*maior_preco_custo_aq`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L320)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
COALESCE(
    CALCULATE(
        MAX(mv_compras_produtos[cmv_compras]),
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_compras_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_compras_produtos[dat_entrada]
        )
    ),
    0
)
```

### `cmv_compras_medio_teste`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L341)

Formato: não declarado na medida.

```dax
COALESCE(
    CALCULATE(
        AVERAGE(mv_compras_produtos[cmv_compras]),
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_compras_produtos[cod_barra_tratado]
        )
    ),
    0
)
```

### `*qtd_laboratorio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L357)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_compras_produtos[nom_laborat]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*qtd_fornecedor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L366)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(cadastro_fornecedor[nome_comercial]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_compras_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_compras_produtos[dat_entrada])
)
```

### `*%participacao_compra`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_compras_produtos.tmdl#L375)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR _total =
    CALCULATE(
        [*valor_total_nfe],

        ALLSELECTED(tabela_cadastro_lojas[nome_rede]),
        ALLSELECTED(tabela_cadastro_lojas[nome_loja]),

        ALLSELECTED(produto_gcp[laboratorio]),
        ALLSELECTED(mv_compras_produtos[nom_laborat]),

        ALLSELECTED(cadastro_fornecedor[nome_comercial]),
        ALLSELECTED(mv_compras_produtos[nom_fornec]),

        ALLSELECTED(produto_gcp[area_farmacia]),
        ALLSELECTED(produto_gcp[grupo_fcia]),
        ALLSELECTED(produto_gcp[nome_subgrupo]),
        ALLSELECTED(produto_gcp[nome_categoria]),

        ALLSELECTED(produto_gcp[produto_cod_barras]),
        ALLSELECTED(mv_compras_produtos[produto_cod_barras_farmacia]),

        ALLSELECTED(produto_gcp[classe_terapeutica]),
        ALLSELECTED(produto_gcp[principio_ativo]),

        ALLSELECTED(mv_compras_produtos[num_nota])
    )

RETURN
    DIVIDE(
        [*valor_total_nfe],
        _total
    )
```

## mv_controle_coleta_farmacias

### `*qtd_cnpjs_controle_coleta`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_controle_coleta_farmacias.tmdl#L4)

Formato: `#,0`

```dax
DISTINCTCOUNT(mv_controle_coleta_farmacias[num_cnpj])
```

### `*qtd_cnpjs_captacao_ok`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_controle_coleta_farmacias.tmdl#L8)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_controle_coleta_farmacias[num_cnpj]),
    FILTER(
        mv_controle_coleta_farmacias, mv_controle_coleta_farmacias[status_venda] = "CAPTAÇÃO OK"
    )
)
```

### `*qtd_cnpjs_captacao_problema`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_controle_coleta_farmacias.tmdl#L19)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_controle_coleta_farmacias[num_cnpj]),
    FILTER(
        mv_controle_coleta_farmacias, mv_controle_coleta_farmacias[status_venda] = "CAPTAÇÃO APRESENTANDO PROBLEMA"
    )
)
```

### `*%var_qtd_cnpjs_captacao_ok`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_controle_coleta_farmacias.tmdl#L30)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
        mv_controle_coleta_farmacias[*qtd_cnpjs_captacao_ok],
        mv_controle_coleta_farmacias[*qtd_cnpjs_controle_coleta]
    )
```

### `*%var_qtd_cnpjs_captacao_problema`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_controle_coleta_farmacias.tmdl#L40)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
        mv_controle_coleta_farmacias[*qtd_cnpjs_captacao_problema],
        mv_controle_coleta_farmacias[*qtd_cnpjs_controle_coleta]
    )
```

## mv_curva_abc_90_dias

### `*skus_estoque`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L4)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_curva_abc_90_dias[cod_barra]),
    filter(mv_curva_abc_90_dias, mv_curva_abc_90_dias[qtd_estoque] > 0)
 )
```

### `*qtd_produtos_risco_ruptura`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L12)

Formato: `#,0`

```dax
COALESCE(
    CALCULATE(
        DISTINCTCOUNT(mv_curva_abc_90_dias[cod_barra]),
        mv_curva_abc_90_dias[status_produto] = "Risco de ruptura",
        mv_curva_abc_90_dias[qtd_estoque] > 0
    ),
    0
)
```

### `*qtd_produtos_estoque_parado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L25)

Formato: `#,0`

```dax
COALESCE(
    CALCULATE(
        DISTINCTCOUNT(mv_curva_abc_90_dias[cod_barra]),
        mv_curva_abc_90_dias[status_produto] = "Estoque parado",
        mv_curva_abc_90_dias[qtd_estoque] > 0
    ),
    0
)
```

### `*qtd_produtos_cobertura_alta`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L38)

Formato: `#,0`

```dax
COALESCE(
    CALCULATE(
        DISTINCTCOUNT(mv_curva_abc_90_dias[cod_barra]),
        mv_curva_abc_90_dias[status_produto] = "Cobertura muito alta",
        mv_curva_abc_90_dias[qtd_estoque] > 0
    ),
    0
)
```

### `*qtd_estoque_curva_abc`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L51)

Formato: `#,0`

```dax
SUM(mv_curva_abc_90_dias[qtd_estoque])
```

### `*skus_estoque_curva_abc`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L55)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_curva_abc_90_dias[cod_barra]),
    filter(mv_curva_abc_90_dias, mv_curva_abc_90_dias[qtd_estoque] > 0)
 )
```

### `*vlr_total_curva_abc`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L63)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
SUM(mv_curva_abc_90_dias[vlr_total])
```

### `*qtd_total_curva_abc`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_curva_abc_90_dias.tmdl#L69)

Formato: `#,0`

```dax
SUM(mv_curva_abc_90_dias[qtd_total])
```

## mv_dados_vendas_compras

### `*venda_liquida_mes_atual_`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L4)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_total_venda]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*venda_liquida_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L18)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataInicioMesAnterior =
    EOMONTH(UltimaDataMesAtual, -2) + 1

VAR DataFimMesAnterior =
    MIN(
        EOMONTH(UltimaDataMesAtual, -1),
        DATE(
            YEAR(EOMONTH(UltimaDataMesAtual, -1)),
            MONTH(EOMONTH(UltimaDataMesAtual, -1)),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_venda]),
    calendario[Date] >= DataInicioMesAnterior &&
    calendario[Date] <= DataFimMesAnterior
)
```

### `*%var_venda_liquida_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L57)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[*venda_liquida_mes_atual_] - mv_dados_vendas_compras[*venda_liquida_mes_anterior],
     mv_dados_vendas_compras[*venda_liquida_mes_anterior],
    0
    )
```

### `*qtd_atendimentos_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L67)

Formato: `#,0`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[qtd_atendimento]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*qtd_atendimentos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L79)

Formato: `0`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataInicioMesAnterior =
    EOMONTH(UltimaDataMesAtual, -2) + 1

VAR DataFimMesAnterior =
    MIN(
        EOMONTH(UltimaDataMesAtual, -1),
        DATE(
            YEAR(EOMONTH(UltimaDataMesAtual, -1)),
            MONTH(EOMONTH(UltimaDataMesAtual, -1)),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[qtd_atendimento]),
    calendario[Date] >= DataInicioMesAnterior &&
    calendario[Date] <= DataFimMesAnterior
)
```

### `*%var_qtd_atendimentos_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L115)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[*qtd_atendimentos_mes_atual] - mv_dados_vendas_compras[*qtd_atendimentos_mes_anterior],
    mv_dados_vendas_compras[*qtd_atendimentos_mes_anterior],
    0
)
```

### `*ticket_medio_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L125)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
mv_dados_vendas_compras[*venda_liquida_mes_atual_] / mv_dados_vendas_compras[*qtd_atendimentos_mes_atual]
```

### `*ticket_medio_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L131)

Formato: não declarado na medida.

```dax
mv_dados_vendas_compras[*venda_liquida_mes_anterior] / mv_dados_vendas_compras[*qtd_atendimentos_mes_anterior]
```

### `*%var_ticket_medio_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L136)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[*ticket_medio_mes_atual] - mv_dados_vendas_compras[*ticket_medio_mes_anterior] ,
     mv_dados_vendas_compras[*ticket_medio_mes_anterior],
     0
     )
```

### `*cmv_aquisicao_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L145)

Formato: não declarado na medida.

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_custo_aquisicao]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*cmv_aquisicao_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L158)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_dados_vendas_compras[dat_emissao]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `*%cmv_liquido_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L205)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(
    SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
    SUM(mv_dados_vendas_compras[vlr_total_venda])
),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*%cmv_liquido_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L220)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataInicioMesAnterior =
    EOMONTH(UltimaDataMesAtual, -2) + 1

VAR DataFimMesAnterior =
    MIN(
        EOMONTH(UltimaDataMesAtual, -1),
        DATE(
            YEAR(EOMONTH(UltimaDataMesAtual, -1)),
            MONTH(EOMONTH(UltimaDataMesAtual, -1)),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    DIVIDE(
        SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
        SUM(mv_dados_vendas_compras[vlr_total_venda])
    ),
    calendario[Date] >= DataInicioMesAnterior &&
    calendario[Date] <= DataFimMesAnterior
)
```

### `*%var_%cmv_liquido_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L257)

Formato: `0.00%;-0.00%;0.00%`

```dax
((mv_dados_vendas_compras[*%cmv_liquido_mes_atual] - mv_dados_vendas_compras[*%cmv_liquido_mes_anterior]) / mv_dados_vendas_compras[*%cmv_liquido_mes_anterior])
```

### `*venda_liquida`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L261)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
SUM(mv_dados_vendas_compras[vlr_total_venda])
```

### `**valor_total_nfe_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L267)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_total_nfe]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `**valor_total_nfe_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L281)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_dados_vendas_compras[dat_emissao]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_nfe]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `**%var_valor_total_nfe_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L328)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[**valor_total_nfe_mes_atual] - mv_dados_vendas_compras[**valor_total_nfe_mes_anterior],
    mv_dados_vendas_compras[**valor_total_nfe_mes_anterior],
    0
)
```

### `**valor_total_descto_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L338)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `**valor_total_descto_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L352)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_dados_vendas_compras[dat_emissao]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_descto]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `**%var_valor_total_descto_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L399)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[**valor_total_descto_mes_atual] - mv_dados_vendas_compras[**valor_total_descto_mes_anterior],
    mv_dados_vendas_compras[**valor_total_descto_mes_anterior],
    0
)
```

### `**%valor_total_descto_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L409)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]), sum(mv_dados_vendas_compras[vlr_total_compra_bruta])
),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `**%valor_total_descto_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L423)

Formato: `0%;-0%;0%`

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_dados_vendas_compras[dat_emissao]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    DIVIDE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]), sum(mv_dados_vendas_compras[vlr_total_compra_bruta])
),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `**%var_%valor_total_descto_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L471)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[**%valor_total_descto_mes_atual] - mv_dados_vendas_compras[**%valor_total_descto_mes_anterior],
    mv_dados_vendas_compras[**%valor_total_descto_mes_anterior],
    0
)
```

### `**qtd_produto_compra_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L481)

Formato: `#,0`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[qtd_produto_compra]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `**qtd_produto_compra_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L493)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR DataMesAnterior =
    EDATE(DataAtual, -1)

VAR DiaLimiteMesAnterior =
    VAR DataLimiteMesAtual =
        CALCULATE(
            MAX(mv_dados_vendas_compras[dat_emissao]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    VAR UltimoDiaMesAtual =
        CALCULATE(
            MAX(calendario[Date]),
            FILTER(
                ALL(calendario),
                calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
            )
        )
    RETURN
        IF(
            DataLimiteMesAtual = UltimoDiaMesAtual,
            31,
            DAY(DataLimiteMesAtual)
        )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[qtd_produto_compra]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), 1) &&
        calendario[Date] <= DATE(YEAR(DataMesAnterior), MONTH(DataMesAnterior), DiaLimiteMesAnterior)
    )
)
```

### `**%var_qtd_produto_compra_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L540)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    mv_dados_vendas_compras[**qtd_produto_compra_mes_atual] - mv_dados_vendas_compras[**qtd_produto_compra_mes_anterior],
    mv_dados_vendas_compras[**qtd_produto_compra_mes_anterior],
    0
)
```

### `*venda_liquida_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L550)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_total_venda]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*venda_liquida_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L564)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataBaseAnoAnterior =
    EDATE(UltimaDataMesAtual, -12)

VAR DataInicio =
    EOMONTH(DataBaseAnoAnterior, -1) + 1

VAR DataFim =
    MIN(
        EOMONTH(DataBaseAnoAnterior, 0),
        DATE(
            YEAR(DataBaseAnoAnterior),
            MONTH(DataBaseAnoAnterior),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_venda]),
    calendario[Date] >= DataInicio &&
    calendario[Date] <= DataFim
)
```

### `*%var_venda_liquida_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L603)

Formato: `0.00%;-0.00%;0.00%`

```dax
COALESCE(
    DIVIDE(
        mv_dados_vendas_compras[*venda_liquida_ano_atual]
        - mv_dados_vendas_compras[*venda_liquida_ano_anterior],
        mv_dados_vendas_compras[*venda_liquida_ano_anterior],
        0
    ),
0)
```

### `*qtd_atendimentos_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L616)

Formato: não declarado na medida.

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[qtd_atendimento]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*qtd_atendimentos_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L629)

Formato: `0`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataBaseAnoAnterior =
    EDATE(UltimaDataMesAtual, -12)

VAR DataInicio =
    EOMONTH(DataBaseAnoAnterior, -1) + 1

VAR DataFim =
    MIN(
        EOMONTH(DataBaseAnoAnterior, 0),
        DATE(
            YEAR(DataBaseAnoAnterior),
            MONTH(DataBaseAnoAnterior),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[qtd_atendimento]),
    calendario[Date] >= DataInicio &&
    calendario[Date] <= DataFim
)
```

### `*%var_qtd_atendimentos_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L666)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE (
    mv_dados_vendas_compras[*qtd_atendimentos_ano_atual] - mv_dados_vendas_compras[*qtd_atendimentos_ano_anterior],
    mv_dados_vendas_compras[*qtd_atendimentos_ano_anterior],
    0
)
```

### `*ticket_medio_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L676)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
mv_dados_vendas_compras[*venda_liquida_mes_atual_] / mv_dados_vendas_compras[*qtd_atendimentos_mes_atual]
```

### `*ticket_medio_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L682)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
mv_dados_vendas_compras[*venda_liquida_ano_anterior] / mv_dados_vendas_compras[*qtd_atendimentos_ano_anterior]
```

### `*%var_ticket_medio_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L688)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE (
    [*ticket_medio_ano_atual] - [*ticket_medio_ano_anterior],
    [*ticket_medio_ano_anterior],
    0
)
```

### `*cmv_aquisicao_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L698)

Formato: não declarado na medida.

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
    REMOVEFILTERS(calendario),
    calendario[ano] = AnoAtual
)
```

### `*cmv_aquisicao_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L713)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `*%cmv_liquido_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L738)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(
    SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
    SUM(mv_dados_vendas_compras[vlr_total_venda])
),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*%cmv_liquido_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L753)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataBaseAnoAnterior =
    EDATE(UltimaDataMesAtual, -12)

VAR DataInicio =
    EOMONTH(DataBaseAnoAnterior, -1) + 1

VAR DataFim =
    MIN(
        EOMONTH(DataBaseAnoAnterior, 0),
        DATE(
            YEAR(DataBaseAnoAnterior),
            MONTH(DataBaseAnoAnterior),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    DIVIDE(
        SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
        SUM(mv_dados_vendas_compras[vlr_total_venda])
    ),
    calendario[Date] >= DataInicio &&
    calendario[Date] <= DataFim
)
```

### `*%var_%cmv_liquido_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L793)

Formato: `0.00%;-0.00%;0.00%`

```dax
COALESCE(
    DIVIDE(
        mv_dados_vendas_compras[*%cmv_liquido_ano_atual]
        - mv_dados_vendas_compras[*%cmv_liquido_ano_anterior],
        mv_dados_vendas_compras[*%cmv_liquido_ano_anterior],
        0
    ),
0)
```

### `*desconto_venda_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L806)

Formato: não declarado na medida.

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_descto]),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*desconto_venda_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L819)

Formato: não declarado na medida.

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataInicioMesAnterior =
    EOMONTH(UltimaDataMesAtual, -2) + 1

VAR DataFimMesAnterior =
    MIN(
        EOMONTH(UltimaDataMesAtual, -1),
        DATE(
            YEAR(EOMONTH(UltimaDataMesAtual, -1)),
            MONTH(EOMONTH(UltimaDataMesAtual, -1)),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_descto]),
    calendario[Date] >= DataInicioMesAnterior &&
    calendario[Date] <= DataFimMesAnterior
)
```

### `*desconto_venda_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L854)

Formato: não declarado na medida.

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_descto]),
    REMOVEFILTERS(calendario),
    calendario[ano] = AnoAtual
)
```

### `*desconto_venda_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L869)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_descto]),
    REMOVEFILTERS(calendario), -- remove todos os filtros da tabela calendário
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `*%desconto_venda_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L894)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(SUM(mv_dados_vendas_compras[vlr_descto]),sum(mv_dados_vendas_compras[vlr_total_venda_bruta])),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

### `*%desconto_venda_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L906)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataInicioMesAnterior =
    EOMONTH(UltimaDataMesAtual, -2) + 1

VAR DataFimMesAnterior =
    MIN(
        EOMONTH(UltimaDataMesAtual, -1),
        DATE(
            YEAR(EOMONTH(UltimaDataMesAtual, -1)),
            MONTH(EOMONTH(UltimaDataMesAtual, -1)),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    DIVIDE(
        SUM(mv_dados_vendas_compras[vlr_descto]),
        SUM(mv_dados_vendas_compras[vlr_total_venda_bruta])
    ),
    calendario[Date] >= DataInicioMesAnterior &&
    calendario[Date] <= DataFimMesAnterior
)
```

### `*%var_%desconto_venda_mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L943)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [*%desconto_venda_mes_atual] - [*%desconto_venda_mes_anterior],
    [*%desconto_venda_mes_anterior],
    0
)
```

### `**%valor_total_descto_ano_atual_linhadotempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L953)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])
RETURN
CALCULATE(
    DIVIDE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]), sum(mv_dados_vendas_compras[vlr_total_compra_bruta])
),
   calendario[ano] = AnoAtual
)
```

### `*%desconto_venda_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L967)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataBaseAnoAnterior =
    EDATE(UltimaDataMesAtual, -12)

VAR DataInicio =
    EOMONTH(DataBaseAnoAnterior, -1) + 1

VAR DataFim =
    MIN(
        EOMONTH(DataBaseAnoAnterior, 0),
        DATE(
            YEAR(DataBaseAnoAnterior),
            MONTH(DataBaseAnoAnterior),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    DIVIDE(
        SUM(mv_dados_vendas_compras[vlr_descto]),
        SUM(mv_dados_vendas_compras[vlr_total_venda_bruta])
    ),
    calendario[Date] >= DataInicio &&
    calendario[Date] <= DataFim
)
```

### `*%var_%desconto_venda_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1007)

Formato: `0.00%;-0.00%;0.00%`

```dax
COALESCE(
    DIVIDE(
        mv_dados_vendas_compras[*%desconto_venda_ano_atual]
        - mv_dados_vendas_compras[*%desconto_venda_ano_anterior],
        mv_dados_vendas_compras[*%desconto_venda_ano_anterior],
        0
    ),
0)
```

### `**%var_qtd_produto_compra_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1020)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [**qtd_produto_compra_ano_atual] - [**qtd_produto_compra_ano_anterior],
     [**qtd_produto_compra_ano_anterior],
     0
     )
```

### `**%valor_total_descto_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1030)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    DIVIDE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]), sum(mv_dados_vendas_compras[vlr_total_compra_bruta])
),
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `**%valor_total_descto_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1056)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    DIVIDE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]), sum(mv_dados_vendas_compras[vlr_total_compra_bruta])
),
    REMOVEFILTERS(calendario),
    calendario[ano] = AnoAtual
)
```

### `**%var_%valor_total_desconto_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1072)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [**%valor_total_descto_ano_atual] - [**%valor_total_descto_ano_anterior],
    [**%valor_total_descto_ano_anterior],
    0
)
```

### `**%var_valor_total_descto_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1082)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [**valor_total_descto_ano_atual] - [**valor_total_descto_ano_anterior],
     [**valor_total_descto_ano_anterior],
     0
     )
```

### `**%var_valor_total_nfe_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1092)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [**valor_total_nfe_ano_atual] - [*valor_total_nfe_ano_anterior],
     [*valor_total_nfe_ano_anterior],
     0
     )
```

### `**qtd_produto_compra_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1102)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    SUM('mv_dados_vendas_compras'[qtd_produto_compra]),
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `**qtd_produto_compra_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1127)

Formato: não declarado na medida.

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM('mv_dados_vendas_compras'[qtd_produto_compra]),
    REMOVEFILTERS(calendario),
    calendario[ano] = AnoAtual
)
```

### `**valor_total_descto_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1142)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_descto]),
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `**valor_total_nfe_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1167)

Formato: não declarado na medida.

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_nfe]),
    REMOVEFILTERS(calendario),
    calendario[ano] = AnoAtual
)
```

### `**valor_total_descto_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1182)

Formato: não declarado na medida.

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_descto]),
    REMOVEFILTERS(calendario),
    calendario[ano] = AnoAtual
)
```

### `*valor_total_nfe_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1197)

Formato: não declarado na medida.

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_nfe]),
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `*%crescimento_mensal_vendas_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1222)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*venda_liquida_ano_atual_linha_do_tempo] - [*venda_liquida_ano_anterior_linha_do_tempo]) / [*venda_liquida_ano_anterior_linha_do_tempo])
```

### `*venda_liquida_ano_anterior_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1226)

Formato: não declarado na medida.

```dax
VAR DataAtualLinha = MAX('calendario'[Date]) 
VAR AnoAnterior = YEAR(DataAtualLinha) - 1 
VAR MesAtual = MONTH(DataAtualLinha) 
VAR DataInicialMesAnoAnterior = DATE(AnoAnterior, MesAtual, 1)
VAR DataFinalMesAnoAnterior = CALCULATE( MAX('calendario'[Date]), 'calendario'[ano] = AnoAnterior, 'calendario'[mes] = MesAtual ) 
RETURN 
CALCULATE( SUM(mv_dados_vendas_compras[vlr_total_venda]), 'calendario'[Date] >= DataInicialMesAnoAnterior, 'calendario'[Date] <= DataFinalMesAnoAnterior )
```

### `*venda_liquida_ano_atual_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1241)

Formato: não declarado na medida.

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_venda]),
    calendario[ano] = AnoAtual
)
```

### `*ticket_medio_ano_atual_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1255)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    DIVIDE([*venda_liquida], [*qtd_atendimentos]),
    calendario[ano] = AnoAtual
)
```

### `*ticket_medio_ano_anterior_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1271)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR DataAtualLinha = MAX('calendario'[Date]) 
VAR AnoAnterior = YEAR(DataAtualLinha) - 1 
VAR MesAtual = MONTH(DataAtualLinha) 
VAR DataInicialMesAnoAnterior = DATE(AnoAnterior, MesAtual, 1)
VAR DataFinalMesAnoAnterior = CALCULATE( MAX('calendario'[Date]), 'calendario'[ano] = AnoAnterior, 'calendario'[mes] = MesAtual ) 

RETURN
CALCULATE(
    DIVIDE([*venda_liquida], [*qtd_atendimentos]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DataInicialMesAnoAnterior &&
        calendario[Date] <= DataFinalMesAnoAnterior
    )
)
```

### `*%crescimento_mensal_ticket_medio_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1294)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*ticket_medio_ano_atual_linha_do_tempo] - [*ticket_medio_ano_anterior_linha_do_tempo]) / [*ticket_medio_ano_anterior_linha_do_tempo])
```

### `*qtd_atendimentos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1298)

Formato: `#,0`

```dax
SUM(mv_dados_vendas_compras[qtd_atendimento])
```

### `*valor_desconto_ano_anterior_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1302)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR DataAtualLinha = MAX('calendario'[Date]) 
VAR AnoAnterior = YEAR(DataAtualLinha) - 1 
VAR MesAtual = MONTH(DataAtualLinha) 
VAR DataInicialMesAnoAnterior = DATE(AnoAnterior, MesAtual, 1)
VAR DataFinalMesAnoAnterior = CALCULATE( MAX('calendario'[Date]), 'calendario'[ano] = AnoAnterior, 'calendario'[mes] = MesAtual ) 

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_descto]),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DataInicialMesAnoAnterior &&
        calendario[Date] <= DataFinalMesAnoAnterior
    )
)
```

### `*valor_desconto_ano_atual_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1326)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_descto]),
    calendario[ano] = AnoAtual
)
```

### `*%crescimento_descontos_linha_do_tempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1341)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [*valor_desconto_ano_atual_linha_do_tempo] - [*valor_desconto_ano_anterior_linha_do_tempo],
     [*valor_desconto_ano_atual_linha_do_tempo],
     0
     )
```

### `**%valor_total_descto_ano_anterior_linhadotempo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1351)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR DataAtualLinha = MAX('calendario'[Date]) 
VAR AnoAnterior = YEAR(DataAtualLinha) - 1 
VAR MesAtual = MONTH(DataAtualLinha) 
VAR DataInicialMesAnoAnterior = DATE(AnoAnterior, MesAtual, 1)
VAR DataFinalMesAnoAnterior = CALCULATE( MAX('calendario'[Date]), 'calendario'[ano] = AnoAnterior, 'calendario'[mes] = MesAtual ) 

RETURN
CALCULATE(
    DIVIDE(
    SUM('mv_dados_vendas_compras'[vlr_total_descto]), sum(mv_dados_vendas_compras[vlr_total_compra_bruta])
),
    FILTER(
        ALL(calendario),
        calendario[Date] >= DataInicialMesAnoAnterior &&
        calendario[Date] <= DataFinalMesAnoAnterior
    )
)
```

### `**%var_%descontos_ano_ano`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1382)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [**%valor_total_descto_ano_atual_linhadotempo] - [**%valor_total_descto_ano_anterior_linhadotempo],
    [**%valor_total_descto_ano_anterior_linhadotempo],
     0
     )
```

### `*%cmv_liquido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1392)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(
    SUM(mv_dados_vendas_compras[vlr_custo_aquisicao]),
    SUM(mv_dados_vendas_compras[vlr_total_venda])
))
```

### `*%desconto_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1402)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(SUM(mv_dados_vendas_compras[vlr_descto]),sum(mv_dados_vendas_compras[vlr_total_venda_bruta]))
)
```

### `*desconto_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1410)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_descto])
)
```

### `**ticket_medio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1420)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
mv_dados_vendas_compras[*venda_liquida] / mv_dados_vendas_compras[*qtd_atendimentos]
```

### `*cmv_aquisicao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1426)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM('mv_dados_vendas_compras'[vlr_custo_aquisicao])
)
```

### `venda_liquida_mes_anterior_corrigida`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1436)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR DataAtual =
    MAX(calendario[Date])

VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataInicioMesAnterior =
    EOMONTH(UltimaDataMesAtual, -2) + 1

VAR DataFimMesAnterior =
    MIN(
        EOMONTH(UltimaDataMesAtual, -1),
        DATE(
            YEAR(EOMONTH(UltimaDataMesAtual, -1)),
            MONTH(EOMONTH(UltimaDataMesAtual, -1)),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_venda]),
    calendario[Date] >= DataInicioMesAnterior &&
    calendario[Date] <= DataFimMesAnterior
)
```

### `*venda_liquida_mes_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1475)

Formato: não declarado na medida.

```dax
VAR UltimaDataMesAtual =
    CALCULATE(
        MAX(calendario[Date]),
        ALL(calendario),
        calendario[ano_mes_numero] = MAX(calendario[ano_mes_numero])
    )

VAR DiaAtual =
    DAY(UltimaDataMesAtual)

VAR DataBaseAnoAnterior =
    EDATE(UltimaDataMesAtual, -12)

VAR DataInicio =
    EOMONTH(DataBaseAnoAnterior, -1) + 1

VAR DataFim =
    MIN(
        EOMONTH(DataBaseAnoAnterior, 0),
        DATE(
            YEAR(DataBaseAnoAnterior),
            MONTH(DataBaseAnoAnterior),
            DiaAtual
        )
    )

RETURN
CALCULATE(
    SUM(mv_dados_vendas_compras[vlr_total_venda]),
    calendario[Date] >= DataInicio &&
    calendario[Date] <= DataFim
)
```

### `*%desconto_venda_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_dados_vendas_compras.tmdl#L1513)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(SUM(mv_dados_vendas_compras[vlr_descto]),sum(mv_dados_vendas_compras[vlr_total_venda_bruta])),
    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    )
)
```

## mv_estoque

### `*qtd_produto_estoque`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L4)

Formato: `#,0`

```dax
CALCULATE(
SUM('mv_estoque'[qtd_estoque]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*qtd_produto_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L13)

Formato: `#,0`

```dax
VAR Selecionado = SELECTEDVALUE(stock_out_botao_analise[botao], "1 Mês")
RETURN
SWITCH(
    TRUE(),
    Selecionado = "1 Mês", [*qtd_produto_1m],
    Selecionado = "3 Meses", [*qtd_produto_3m],
    Selecionado = "6 Meses", [*qtd_produto_6m],
    BLANK()
)
```

### `*qtd_vendida_1m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L27)

Formato: `0`

```dax
CALCULATE(
SUM('mv_estoque'[qtd_vendida_1m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*qtd_vendida_3m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L36)

Formato: `#,0`

```dax
CALCULATE(
SUM('mv_estoque'[qtd_vendida_3m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*qtd_vendida_6m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L45)

Formato: não declarado na medida.

```dax
CALCULATE(
SUM('mv_estoque'[qtd_vendida_6m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*valor_vendido_1m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L55)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM('mv_estoque'[valor_vendido_1m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*valor_vendido_3m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L66)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM('mv_estoque'[valor_vendido_3m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*valor_vendido_6m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L77)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM('mv_estoque'[valor_vendido_6m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*nivel_servico`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L88)

Formato: `0.0%;-0.0%;0.0%`

```dax
(([*qtd_produto_geral] - [*qtd_produto_com_ruptura_geral]) / [*qtd_produto_geral])
```

### `*perda_por_stockout_1m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L92)

Formato: não declarado na medida.

```dax
CALCULATE(
SUM('mv_estoque'[perda_stockout_1m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*perda_por_stockout_3m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L102)

Formato: não declarado na medida.

```dax
CALCULATE(
SUM('mv_estoque'[perda_stockout_3m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*perda_por_stockout_6m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L112)

Formato: não declarado na medida.

```dax
CALCULATE(
SUM('mv_estoque'[perda_stockout_6m]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda])
)
```

### `*perda_stockout_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L122)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR Selecionado = SELECTEDVALUE(stock_out_botao_analise[botao], "1 Mês")
RETURN
SWITCH(
    TRUE(),
    Selecionado = "1 Mês", [*perda_por_stockout_1m],
    Selecionado = "3 Meses", [*perda_por_stockout_3m],
    Selecionado = "6 Meses", [*perda_por_stockout_6m],
    BLANK()
)
```

### `*qtd_produto_1m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L138)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT('mv_estoque'[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda]),
    FILTER(mv_estoque, mv_estoque[*qtd_vendida_1m] > 0
    )
)
```

### `*qtd_produto_3m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L149)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT('mv_estoque'[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda]),
    FILTER(mv_estoque, mv_estoque[*qtd_vendida_3m] > 0
    )
)
```

### `*qtd_produto_6m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L160)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT('mv_estoque'[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda]),
    FILTER(mv_estoque, mv_estoque[*qtd_vendida_6m] > 0
    )
)
```

### `*qtd_produto_com_ruptura_1m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L171)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT('mv_estoque'[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda]),
    FILTER(
        mv_estoque, mv_estoque[em_ruptura_1m] = "Ruptura"
    )
)
```

### `*qtd_produto_com_ruptura_3m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L183)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT('mv_estoque'[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda]),
    FILTER(
        mv_estoque, mv_estoque[em_ruptura_3m] = "Ruptura"
    )
)
```

### `*qtd_produto_com_ruptura_6m`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L195)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT('mv_estoque'[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_estoque[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_estoque[ultima_venda]),
    FILTER(
        mv_estoque, mv_estoque[em_ruptura_6m] = "Ruptura"
    )
)
```

### `*qtd_produto_com_ruptura_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L207)

Formato: `#,0`

```dax
VAR Selecionado = SELECTEDVALUE(stock_out_botao_analise[botao], "1 Mês")
RETURN
SWITCH(
    TRUE(),
    Selecionado = "1 Mês", [*qtd_produto_com_ruptura_1m],
    Selecionado = "3 Meses", [*qtd_produto_com_ruptura_3m],
    Selecionado = "6 Meses", [*qtd_produto_com_ruptura_6m],
    BLANK()
)
```

### `*qtd_vendida_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L221)

Formato: `#,0`

```dax
VAR Selecionado = SELECTEDVALUE(stock_out_botao_analise[botao], "1 Mês")
RETURN
SWITCH(
    TRUE(),
    Selecionado = "1 Mês", [*qtd_vendida_1m],
    Selecionado = "3 Meses", [*qtd_vendida_3m],
    Selecionado = "6 Meses", [*qtd_vendida_6m],
    BLANK()
)
```

### `*valor_vendido_geral`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L235)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR Selecionado = SELECTEDVALUE(stock_out_botao_analise[botao], "1 Mês")
RETURN
SWITCH(
    TRUE(),
    Selecionado = "1 Mês", [*valor_vendido_1m],
    Selecionado = "3 Meses", [*valor_vendido_3m],
    Selecionado = "6 Meses", [*valor_vendido_6m],
    BLANK()
)
```

### `*nivel_servico_cor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_estoque.tmdl#L251)

Formato: não declarado na medida.

```dax
VAR ns = [*nivel_servico]
RETURN
    SWITCH (
        TRUE(),
        ns > 0.90, "#4CAF50",   -- verde
        ns > 0.80, "#FDD663",   -- amarelo
        ns <= 0.80, "#e8756f"   -- vermelho
    )
```

## mv_performance_loja

### `**score_final`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L4)

Formato: `#,0.00`

```dax
CALCULATE(
AVERAGE(mv_performance_loja[score_final]),
    USERELATIONSHIP(calendario[Date],mv_performance_loja[mes])
)
```

### `**classificacao_performance_loja`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L13)

Formato: não declarado na medida.

```dax
SWITCH(
    TRUE(),
    [**score_final] < 40, "Ruim",
    [**score_final] < 60, "Regular",
    [**score_final] < 80, "Bom",
    "Excelente"
)
```

### `***qtd_lojas_performance_bom`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L24)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_loja[num_cnpj]),
    USERELATIONSHIP(calendario[Date], mv_performance_loja[mes]),
    KEEPFILTERS(
        ADDCOLUMNS(
            VALUES(mv_performance_loja[num_cnpj]),
            "@classificacao", [**classificacao_performance_loja]
        )
    ),
    FILTER(
        VALUES(mv_performance_loja[num_cnpj]),
        [**classificacao_performance_loja] = "Bom"
    )
)
```

### `***qtd_lojas_performance_ruim`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L43)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_loja[num_cnpj]),
    USERELATIONSHIP(calendario[Date], mv_performance_loja[mes]),
    KEEPFILTERS(
        ADDCOLUMNS(
            VALUES(mv_performance_loja[num_cnpj]),
            "@classificacao", [**classificacao_performance_loja]
        )
    ),
    FILTER(
        VALUES(mv_performance_loja[num_cnpj]),
        [**classificacao_performance_loja] = "Ruim"
    )
)
```

### `***qtd_lojas_performance_regular`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L62)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_loja[num_cnpj]),
    USERELATIONSHIP(calendario[Date], mv_performance_loja[mes]),
    KEEPFILTERS(
        ADDCOLUMNS(
            VALUES(mv_performance_loja[num_cnpj]),
            "@classificacao", [**classificacao_performance_loja]
        )
    ),
    FILTER(
        VALUES(mv_performance_loja[num_cnpj]),
        [**classificacao_performance_loja] = "Regular"
    )
)
```

### `***qtd_lojas_performance_excelente`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L81)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_loja[num_cnpj]),
    USERELATIONSHIP(calendario[Date], mv_performance_loja[mes]),
    KEEPFILTERS(
        ADDCOLUMNS(
            VALUES(mv_performance_loja[num_cnpj]),
            "@classificacao", [**classificacao_performance_loja]
        )
    ),
    FILTER(
        VALUES(mv_performance_loja[num_cnpj]),
        [**classificacao_performance_loja] = "Excelente"
    )
)
```

### `%_qtd_lojas_performance_bom`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L100)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([***qtd_lojas_performance_bom], 0),
    [*qtd_total_lojas],
    0
)
```

### `*qtd_total_lojas`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L110)

Formato: `0`

```dax
CALCULATE(
DISTINCTCOUNT(mv_performance_loja[num_cnpj]),
    USERELATIONSHIP(calendario[Date],mv_performance_loja[mes])
)
```

### `%_qtd_lojas_performance_ruim`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L119)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([***qtd_lojas_performance_ruim], 0),
    [*qtd_total_lojas],
    0
)
```

### `%_qtd_lojas_performance_regular`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L129)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([***qtd_lojas_performance_regular], 0),
    [*qtd_total_lojas],
    0
)
```

### `%_qtd_lojas_performance_excelente`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L139)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([***qtd_lojas_performance_excelente], 0),
    [*qtd_total_lojas],
    0
)
```

### `**classificacao_performance_loja_cor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L149)

Formato: não declarado na medida.

```dax
SWITCH(
    TRUE(),
    [**score_final] < 40, "#F28B82",
    [**score_final] < 60, "#FDD663",
    [**score_final] < 80, "#81C995",
    "#8AB4F8"
)
```

### `dica_acao_2`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L160)

Formato: não declarado na medida.

```dax
VAR classificacao = [**classificacao_performance_loja]
RETURN
SWITCH(
    classificacao,

	"Ruim",
	"
	• Revisar a política de descontos para evitar perdas de margem

	• Incentivar a venda de genéricos, similares e marca própria (maior rentabilidade)

	• Reforçar treinamento em argumentação de valor e custo-benefício

	• Oferecer kits atrativos (ex.: medicamento + vitamina, protetor solar + hidratante)

	• Estabelecer meta mínima de atendimentos por colaborador

	• Acompanhar de perto ticket médio, itens por venda e margem da loja
	",

	"Regular",
	"
	• Atuar de forma ativa na venda consultiva, sugerindo itens complementares que agreguem valor à compra do cliente e contribuam para o aumento do ticket médio

	• Sugerir a compra de uma versão mais completa ou maior do produto que o cliente está levando

	• Incentivar a escolha de genéricos ou similares que tragam maior lucro para a loja em comparação ao produto de referência

	• Definir metas de ticket médio e itens por cliente

	• Direcionar esforços para produtos de maior margem

	• Monitorar de perto concessão de descontos e impacto na rentabilidade
	",

	"Bom",
	"
	• Manter consistência nas boas práticas de abordagem ativa

	• Buscar pequenos ganhos de ticket médio sugerindo complementos úteis

	• Monitorar indicadores de margem e quantidade de itens vendidos

	• Oferecer ao cliente uma versão maior ou mais completa do produto que está comprando

	• Incentivar compartilhamento de boas práticas entre os vendedores
	",

	"Excelente",
	"
	• Reforçar a rotina que já gera alta performance

	• Reconhecer e valorizar publicamente os resultados da equipe

	• Estimular que vendedores de alta performance sejam multiplicadores de conhecimento

	• Investir em melhorias contínuas em atendimento, ticket médio, mix de produtos e margem

	• Criar desafios pontuais para manter o engajamento elevado
	",

	"Sem classificação definida"
)
```

### `**score_ticket`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L228)

Formato: não declarado na medida.

```dax
CALCULATE(
AVERAGE(mv_performance_loja[score_ticket_medio]),
    USERELATIONSHIP(calendario[Date],mv_performance_loja[mes])
)
```

### `**score_media_itens`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L238)

Formato: não declarado na medida.

```dax
CALCULATE(
AVERAGE(mv_performance_loja[score_media_itens]),
    USERELATIONSHIP(calendario[Date],mv_performance_loja[mes])
)
```

### `**score_lucro`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L248)

Formato: não declarado na medida.

```dax
CALCULATE(
AVERAGE(mv_performance_loja[score_lucro]),
    USERELATIONSHIP(calendario[Date],mv_performance_loja[mes])
)
```

### `**score_atendimento`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L258)

Formato: não declarado na medida.

```dax
CALCULATE(
AVERAGE(mv_performance_loja[score_atendimento]),
    USERELATIONSHIP(calendario[Date],mv_performance_loja[mes])
)
```

### `filtro_classificacao_performance_loja`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_loja.tmdl#L268)

Formato: `0`

```dax
VAR classificacao_selecionada = SELECTEDVALUE('classificacao_performance_vendedor'[classificacao], "Todos")
VAR classificacao_geral = [**score_final]
RETURN
SWITCH(
    TRUE(),
    classificacao_selecionada = "Todos", 1,
    classificacao_selecionada = "1 - Ruim" && classificacao_geral >= 0 && classificacao_geral < 40, 1,
    classificacao_selecionada = "3 - Regular" && classificacao_geral >= 40 && classificacao_geral < 60, 1,
    classificacao_selecionada = "2 - Bom" && classificacao_geral >= 60 && classificacao_geral < 80, 1,
    classificacao_selecionada = "4 - Excelente" && classificacao_geral >= 80 && classificacao_geral <= 100, 1,
    0
)
```

## mv_performance_vendedores

### `_qtd_vendedor_excelente`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L4)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_vendedores[cod_vendedor_ivend]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes]),
    FILTER(
        mv_performance_vendedores,
        mv_performance_vendedores[classificacao_performance] = "Excelente"
    )
)
```

### `_qtd_vendedor_bom`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L17)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_vendedores[cod_vendedor_ivend]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes]),
    FILTER(
        mv_performance_vendedores,
        mv_performance_vendedores[classificacao_performance] = "Bom"
    )
)
```

### `_qtd_vendedor_regular`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L30)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_vendedores[cod_vendedor_ivend]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes]),
    FILTER(
        mv_performance_vendedores,
        mv_performance_vendedores[classificacao_performance] = "Regular"
    )
)
```

### `_qtd_vendedor_precisa_melhorar`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L43)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_vendedores[cod_vendedor_ivend]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes]),
    mv_performance_vendedores[classificacao_performance] IN {
        "Precisa Melhorar",
        "Baixa Amostra"
    }
)
```

### `_score_final`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L56)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[score_final]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_classificacao_performance_cor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L66)

Formato: não declarado na medida.

```dax
SWITCH(
    TRUE(),
    [_score_final] < 40, "#F28B82",   -- vermelho suave
    [_score_final] < 60, "#FDD663",   -- amarelo suave
    [_score_final] < 80, "#81C995",   -- verde suave
    "#8AB4F8"                                -- azul suave
)
```

### `_score_atendimento`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L77)

Formato: `#,0.00`

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[score_atendimento]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_score_ticket_medio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L86)

Formato: `#,0.00`

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[score_ticket_medio]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_score_lucro`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L95)

Formato: `#,0.00`

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[score_lucro]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_score_media_itens`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L104)

Formato: `#,0.00`

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[score_media_itens]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_qtd_atendimento`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L113)

Formato: `#,0`

```dax
CALCULATE(
    SUM(mv_performance_vendedores[qtd_atendimento]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_media_itens`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L122)

Formato: não declarado na medida.

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[media_itens]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_lucro`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L132)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM(mv_performance_vendedores[lucro]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_total_vendas`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L143)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    AVERAGE(mv_performance_vendedores[total_vendas]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_ticket_medio`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L154)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM(mv_performance_vendedores[ticket_medio]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_score_medidas`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L165)

Formato: não declarado na medida.

```dax
"Score Ticket médio: " &[_score_ticket_medio]
    & UNICHAR(10) &
"Score Média de itens: " &[_score_media_itens]
    & UNICHAR(10) &
"Score Lucro: " &[_score_lucro]
    & UNICHAR(10) &
"Score Atendimentos: " &[_score_atendimento]
```

### `_%qtd_vendedores_excelente`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L176)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([_qtd_vendedor_excelente], 0),
    [_qtd_vendedor],
    0
)
```

### `_qtd_vendedor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L186)

Formato: `0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_performance_vendedores[cod_vendedor_ivend]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

### `_%qtd_vendedores_bom`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L195)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([_qtd_vendedor_bom], 0),
    [_qtd_vendedor],
    0
)
```

### `_%qtd_vendedores_regular`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L205)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([_qtd_vendedor_regular], 0),
    [_qtd_vendedor],
    0
)
```

### `_%qtd_vendedores_precisa_melhorar`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L215)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([_qtd_vendedor_precisa_melhorar], 0),
    [_qtd_vendedor],
    0
)
```

### `_%qtd_venda_1_item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L225)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    COALESCE([_qtd_cupon_1_item], 0),
    [_qtd_atendimento],
    0
)
```

### `_qtd_cupon_1_item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_performance_vendedores.tmdl#L235)

Formato: `0`

```dax
CALCULATE(
    SUM(mv_performance_vendedores[qtd_cupons_um_item]),
    USERELATIONSHIP(calendario[Date],mv_performance_vendedores[mes])
)
```

## mv_produtos_com_estoque_sem_vendas_mais_de_90_dias

### `*vlr_total_vendido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L4)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[vlr_total_vendido]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*vlr_total_lucro`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L14)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[vlr_total_lucro]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*qtd_total_vendida`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L24)

Formato: `#,0`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[qtd_total_vendida]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*qtd_total_estoque`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L32)

Formato: `#,0`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[qtd_total_estoque]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*qtd_total_comprada`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L40)

Formato: `#,0`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[qtd_total_comprada]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*vlr_total_comprado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L48)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[vlr_total_comprado]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*vlr_custo_estoque`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L58)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[vlr_custo_estoque]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*skus_prod_com_estoque`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L68)

Formato: `0`

```dax
CALCULATE(DISTINCTCOUNT(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*qtd_dias_sem_vendas`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L76)

Formato: `#,0`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[qtd_dias_sem_vendas]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

### `*faturamento_potencial`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_produtos_com_estoque_sem_vendas_mais_de_90_dias.tmdl#L84)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(SUM(mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[faturamento_potencial]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_produtos_com_estoque_sem_vendas_mais_de_90_dias[dat_ult_venda])
)
```

## mv_sugestao_compras

### `*qtd_compra_ultima_entrada`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L4)

Formato: `#,0`

```dax
CALCULATE(
SUM('mv_sugestao_compras'[qtd_compra_ultima_entrada]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_compras[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_sugestao_compras[data_ultima_entrada])
)
```

### `*qtd_estoque`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L13)

Formato: `#,0`

```dax
CALCULATE(
SUM('mv_sugestao_compras'[qtd_estoque]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_compras[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_sugestao_compras[data_ultima_entrada])
)
```

### `*%var_valor_atual_x_menor_valor`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L22)

Formato: `0.00%;-0.00%;0.00%`

```dax
(([*valor_ultima_entrada] - [*menor_valor_negociado]) / [*menor_valor_negociado])
```

### `*menor_valor_negociado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L26)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM('mv_sugestao_compras'[menor_valor_negociado]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_compras[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_sugestao_compras[data_ultima_entrada])
)
```

### `*potencial_economia`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L37)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
[*valor_ultima_entrada] - [*menor_valor_negociado]
```

### `*qtd_produtos`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L43)

Formato: `#,0`

```dax
CALCULATE(
DISTINCTCOUNT(mv_sugestao_compras[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_compras[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_sugestao_compras[data_ultima_entrada])
)
```

### `*qtd_produtos_acima_melhor_preco`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L52)

Formato: `#,0`

```dax
CALCULATE(
DISTINCTCOUNT(mv_sugestao_compras[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_compras[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_sugestao_compras[data_ultima_entrada]),
    FILTER(mv_sugestao_compras,mv_sugestao_compras[classificacao_valor] <> "Melhor preço")
)
```

### `cor_linha`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L62)

Formato: não declarado na medida.

```dax
VAR menor_valor_negociado = 'mv_sugestao_compras'[*menor_valor_negociado]
VAR valor_ultima_entrada = 'mv_sugestao_compras'[*valor_ultima_entrada]
VAR classificacao =
    SWITCH(
        TRUE(),
        menor_valor_negociado > 0 && ABS(valor_ultima_entrada - menor_valor_negociado) < 0.001, "Melhor preço",
        menor_valor_negociado > 0 && valor_ultima_entrada > 0 && valor_ultima_entrada <= menor_valor_negociado * 1.10, "Acima do menor",
        "Crítico + 10%"
    )
RETURN
SWITCH(
    TRUE(),
    classificacao = "Melhor preço", "#ECFDF5",       // Verde claro
    classificacao = "Acima do menor", "#FEF2F2",     // Vermelho claro
    classificacao = "Crítico + 10%", "#FEE2E2",      // Vermelho mais forte
    BLANK()
)
```

### `*valor_ultima_entrada`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L85)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM('mv_sugestao_compras'[valor_ultima_entrada]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_compras[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_sugestao_compras[data_ultima_entrada])
)
```

### `cor_fonte`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L96)

Formato: não declarado na medida.

```dax
VAR menor_valor_negociado = 'mv_sugestao_compras'[*menor_valor_negociado]
VAR valor_ultima_entrada = 'mv_sugestao_compras'[*valor_ultima_entrada]
VAR classificacao =
    SWITCH(
        TRUE(),
        menor_valor_negociado > 0 && ABS(valor_ultima_entrada - menor_valor_negociado) < 0.001, "Melhor preço",
        menor_valor_negociado > 0 && valor_ultima_entrada > 0 && valor_ultima_entrada <= menor_valor_negociado * 1.10, "Acima do menor",
        "Crítico + 10%"
    )
RETURN
SWITCH(
    TRUE(),
    classificacao = "Melhor preço", "#059669",       // Verde claro
    classificacao = "Acima do menor", "#DC2626",     // Vermelho claro
    classificacao = "Crítico + 10%", "#DC2626",      // Vermelho mais forte
    BLANK()
)
```

### `cor_fonte_status`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_compras.tmdl#L117)

Formato: não declarado na medida.

```dax
VAR menor_valor_negociado = 'mv_sugestao_compras'[*menor_valor_negociado]
VAR valor_ultima_entrada = 'mv_sugestao_compras'[*valor_ultima_entrada]
VAR classificacao =
    SWITCH(
        TRUE(),
        menor_valor_negociado > 0 && ABS(valor_ultima_entrada - menor_valor_negociado) < 0.001, "Melhor preço",
        menor_valor_negociado > 0 && valor_ultima_entrada > 0 && valor_ultima_entrada <= menor_valor_negociado * 1.10, "Acima do menor",
        "Crítico + 10%"
    )
RETURN
SWITCH(
    TRUE(),
    classificacao = "Melhor preço", "#ECFDF5",       // Verde claro
    classificacao = "Acima do menor", "#DC2626",     // Vermelho claro
    classificacao = "Crítico + 10%", "#DC2626",      // Vermelho mais forte
    BLANK()
)
```

## mv_sugestao_transferencia_filiais

### `*qtd_disponivel_origem`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L4)

Formato: `#,0`

```dax
CALCULATE(
    SUM(mv_sugestao_transferencia_filiais[qtd_disponivel_origem]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_transferencia_filiais[cod_barra_tratado])
)
```

### `*qtd_sugerida_transferencia`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L12)

Formato: `#,0`

```dax
CALCULATE(
    SUM(mv_sugestao_transferencia_filiais[qtd_sugerida_transferencia]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_transferencia_filiais[cod_barra_tratado])
)
```

### `*demanda_90d_destino`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L20)

Formato: `#,0`

```dax
CALCULATE(
    SUM(mv_sugestao_transferencia_filiais[demanda_90d_destino]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_transferencia_filiais[cod_barra_tratado])
)
```

### `*potencial_economia_total`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L28)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
    SUM(mv_sugestao_transferencia_filiais[potencial_economia_total]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_transferencia_filiais[cod_barra_tratado])
)
```

### `*skus_sugestao_transferencia`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L38)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_sugestao_transferencia_filiais[cod_barra_tratado]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_transferencia_filiais[cod_barra_tratado])
)
```

### `*dias_cobertura`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L46)

Formato: não declarado na medida.

```dax
CALCULATE(
    SUM(mv_sugestao_transferencia_filiais[dias_cobertura]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_sugestao_transferencia_filiais[cod_barra_tratado])
)
```

### `*perc_demanda_atendida_media`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_sugestao_transferencia_filiais.tmdl#L55)

Formato: `0.00%;-0.00%;0.00%`

```dax
AVERAGE(mv_sugestao_transferencia_filiais[*perc_demanda_atendida])
```

## mv_vendas_produtos

### `*venda_liquida_h`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L42)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])
)
```

### `*ticket_medio_atual_h`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L54)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR TotalVendas =
    CALCULATE(
        SUM(mv_vendas_produtos[vlr_total_venda]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
    )
VAR TotalAtendimentos =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
    )
RETURN
DIVIDE(TotalVendas, TotalAtendimentos, 0)
```

### `**venda_liquida`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L77)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM(mv_vendas_produtos[vlr_total_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `*%margem_lucro_bruta`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L89)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
((SUM(mv_vendas_produtos[vlr_total_venda]) - sum(mv_vendas_produtos[vlr_custo_aquisicao])) / SUM(mv_vendas_produtos[vlr_total_venda])),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `*%valor_total_descto_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L99)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
DIVIDE(
SUM('mv_vendas_produtos'[vlr_descto]), sum(mv_vendas_produtos[vlr_total_venda_bruta])),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `*lucro_bruto`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L111)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM(mv_vendas_produtos[vlr_total_venda]) - SUM(mv_vendas_produtos[vlr_custo_aquisicao]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])
)
```

### `*qtd_atendimento_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L123)

Formato: `#,0`

```dax
VAR QtdeVendas =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    )

VAR QtdeDevolucoes =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    )

RETURN
    QtdeVendas - QtdeDevolucoes
```

### `*qtd_produto_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L149)

Formato: `#,0`

```dax
CALCULATE(
SUM(mv_vendas_produtos[qtd_produto_venda]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `*sku_venda_ano_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L159)

Formato: `0`

```dax
VAR DataAtual =
    TODAY()

VAR AnoAnterior =
    YEAR(DataAtual) - 1

VAR DataInicialAnoAnterior =
    DATE(AnoAnterior, 1, 1)

VAR DataFinalAnoAnterior =
    DATE(AnoAnterior, MONTH(DataAtual), DAY(DataAtual))

RETURN
CALCULATE(
    DISTINCTCOUNT(mv_vendas_produtos[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),    
    REMOVEFILTERS(calendario),
    calendario[Date] >= DataInicialAnoAnterior &&
    calendario[Date] <= DataFinalAnoAnterior
)
```

### `*sku_venda_ano_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L186)

Formato: `0`

```dax
VAR AnoAtual =
    MAXX(ALL(calendario), calendario[ano])

RETURN
CALCULATE(
    DISTINCTCOUNT(mv_vendas_produtos[cod_barra]),
    REMOVEFILTERS(calendario),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    calendario[ano] = AnoAtual
)
```

### `*valor_custo_aquisicao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L202)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM(mv_vendas_produtos[vlr_custo_aquisicao]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])
)
```

### `*valor_desconto_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L213)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM(mv_vendas_produtos[vlr_descto]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])
)
```

### `filtro_alerta_desconto_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L224)

Formato: `0`

```dax
VAR alertaselecionado = SELECTEDVALUE('alerta_desconto_venda'[alerta], "Todos")
VAR desconto = [*%valor_total_descto_venda]
RETURN
SWITCH(
    TRUE(),
    alertaselecionado = "Todos", 1,
    alertaselecionado = "> que 10%" && desconto > 0.1, 1,
	alertaselecionado = "> que 20%" && desconto > 0.2, 1,
	alertaselecionado = "> que 30%" && desconto > 0.3, 1,
	alertaselecionado = "> que 40%" && desconto > 0.4, 1,
	alertaselecionado = "> que 50%" && desconto > 0.5, 1,
    0
)
```

### `filtro_alerta_margem_lucro_bruta`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L242)

Formato: `0`

```dax
VAR alertaselecionado = SELECTEDVALUE('alerta_margem_lucro_bruta'[alerta], "Todos")
VAR margem = [*%margem_lucro_bruta]
RETURN
SWITCH(
    TRUE(),
    alertaselecionado = "Todos", 1,
    alertaselecionado = "< que 0%" && margem < 0, 1,
    alertaselecionado = "< que 10%" && margem < 0.1, 1,
	alertaselecionado = "< que 20%" && margem < 0.2, 1,
	alertaselecionado = "< que 30%" && margem < 0.3, 1,
	alertaselecionado = "< que 40%" && margem < 0.4, 1,
	alertaselecionado = "< que 50%" && margem < 0.5, 1,
    alertaselecionado = "> que 50%" && margem > 0.5, 1,
    0
)
```

### `*%participacao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L262)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    CALCULATE(
        SUM(mv_vendas_produtos[vlr_total_venda]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao])
    ),
    CALCULATE(
        SUM(mv_vendas_produtos[vlr_total_venda]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        ALL(produto_gcp),
        ALL(calendario)
    )
)
```

### `filtro_alerta_margem_lucro_bruta_2`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L283)

Formato: `0`

```dax
VAR alertaselecionado = SELECTEDVALUE('alerta_margem_lucro_bruta_2'[alerta], "Todos")
VAR margem = [*%margem_lucro_bruta]
RETURN
SWITCH(
    TRUE(),
    alertaselecionado = "Todos", 1,
    alertaselecionado = "Margem negativa" && margem < 0, 1,
    alertaselecionado = "Margem positiva" && margem > 0, 1,
    0
)
```

### `**%cmv_liquido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L298)

Formato: `0.00%;-0.00%;0.00%`

```dax
CALCULATE(
    DIVIDE(
    SUM(mv_vendas_produtos[vlr_custo_aquisicao]),
    SUM(mv_vendas_produtos[vlr_total_venda])
),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `*media_itens`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L312)

Formato: não declarado na medida.

```dax
CALCULATE(
    DIVIDE(
        SUM(mv_vendas_produtos[qtd_produto_venda]),
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento])
    ),
    USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `*preco_medio_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L327)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
DIVIDE(
    CALCULATE(
        SUM(mv_vendas_produtos[vlr_total_venda]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    ),
    CALCULATE(
        SUM(mv_vendas_produtos[qtd_produto_venda]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente], mv_vendas_produtos[cod_cliente])
    )
)
```

### `**venda_bruta`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L350)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
CALCULATE(
SUM(mv_vendas_produtos[vlr_total_venda_bruta]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao]),
    USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
)
```

### `**Qtd_Cupons_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L362)

Formato: `#,0`

```dax
VAR CuponsVenda =
    CALCULATE(
        COUNTROWS(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        )
                ),
                [QtdTotal] = 1
            )
        ),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        COUNTROWS(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        )
                ),
                [QtdTotal] = 1
            )
        ),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `**%_Cupons_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L427)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE(
    [**Qtd_Cupons_1_Item],
    [**Qtd_Cupons],
    0
)
```

### `**Qtd_Cupons`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L437)

Formato: `0`

```dax
VAR CuponsVenda =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `*sku_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L480)

Formato: `#,0`

```dax
CALCULATE(
    DISTINCTCOUNT(mv_vendas_produtos[cod_barra]),
    USERELATIONSHIP(produto_gcp[cod_barra],mv_vendas_produtos[cod_barra_tratado]),
    USERELATIONSHIP(calendario[Date],mv_vendas_produtos[dat_emissao])
)
```

### `*%participacao_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L489)

Formato: `0.00%;-0.00%;0.00%`

```dax
VAR _total =
    CALCULATE(
        [*venda_liquida_h],

        ALLSELECTED(tabela_cadastro_lojas[nome_rede]),
        ALLSELECTED(tabela_cadastro_lojas[nome_loja]),

        ALLSELECTED(produto_gcp[laboratorio]),
        ALLSELECTED(mv_vendas_produtos[nom_laborat]),

        ALLSELECTED(produto_gcp[area_farmacia]),
        ALLSELECTED(produto_gcp[grupo_fcia]),

        ALLSELECTED(produto_gcp[nome_subgrupo]),
        ALLSELECTED(produto_gcp[nome_categoria]),

        ALLSELECTED(produto_gcp[produto_cod_barras]),
        ALLSELECTED(mv_vendas_produtos[produto_cod_barras_farmacia]),

        ALLSELECTED(produto_gcp[classe_terapeutica]),
        ALLSELECTED(produto_gcp[principio_ativo]),

        ALLSELECTED(mv_vendas_produtos[num_nota]),

        ALLSELECTED(mv_vendas_produtos[venda_delivery]),
        ALLSELECTED(mv_vendas_produtos[cod_nom_vendedor]),

        ALLSELECTED(geolocalizacao[Municipio]),
        ALLSELECTED(geolocalizacao[Micro_Regiao]),
        ALLSELECTED(geolocalizacao[Meso_Regiao])
    )

RETURN
    DIVIDE(
        [*venda_liquida_h],
        _total
    )
```

### `*maior_preco_venda`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L532)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
MAXX(
    CALCULATETABLE(
        mv_vendas_produtos,

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),

        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),

        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    ),

    DIVIDE(
        mv_vendas_produtos[vlr_total_venda],
        mv_vendas_produtos[qtd_produto_venda]
    )
)
```

### `***Gap_de_Ticket (R$)`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L565)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
[***Ticket_medio_mais1] - [***Ticket_medio_1_Item]
```

### `***Ticket_medio_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L574)

Formato: não declarado na medida.

```dax
DIVIDE ( [**Vlr_Vendas_1_Item], [**Qtd_Cupons_1_Item] )
```

### `**%_Cupon_1_Item_Mes_anterior`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L580)

Formato: não declarado na medida.

```dax
CALCULATE ( [**%_Cupons_1_Item], DATEADD ( calendario[Date], -1, MONTH ) )
```

### `**%_fisico_online`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L587)

Formato: `0.0000`

```dax
DIVIDE(
    [**Qtd_Cupon_ecommerce_mes_atual],
    [**Qtd_Cupon_balcao_mes_atual],
    0
)
```

### `**qtd_cupons_1_item_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L597)

Formato: `#,0`

```dax
VAR CuponsVenda =
    CALCULATE(
        COUNTROWS(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        )
                ),
                [QtdTotal] = 1
            )
        ),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        COUNTROWS(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        )
                ),
                [QtdTotal] = 1
            )
        ),
        mv_vendas_produtos[tip_venda] = "D",
        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `**Qtd_Cupons_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L673)

Formato: `#,0`

```dax
VAR CuponsVenda =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),        
        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `**Vlr_Vendas_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L725)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR Vendas_1_Item =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR Devolucoes_1_Item =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    Vendas_1_Item - Devolucoes_1_Item
```

### `**Vlr_Vendas_1_Item_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L803)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR Vendas_1_Item =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "V",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR Devolucoes_1_Item =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "D",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    Vendas_1_Item - Devolucoes_1_Item
```

### `**Vlr_Vendas_ecommerce_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L893)

Formato: não declarado na medida.

```dax
VAR Vendas_ecommerce =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "V",
        mv_vendas_produtos[flg_ecommerce] = "S",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR Devolucoes_Vendas_ecommerce =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "D",
        mv_vendas_produtos[flg_ecommerce] = "S",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    Vendas_ecommerce - Devolucoes_Vendas_ecommerce
```

### `**Vlr_Vendas_ecommerce_atual_voa`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L984)

Formato: não declarado na medida.

```dax
VAR Vendas_ecommerce =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 2
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "V",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR Devolucoes_Vendas_ecommerce =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 2
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "D",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    Vendas_ecommerce - Devolucoes_Vendas_ecommerce
```

### `**Vlr_Vendas_s/ecommerce_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1074)

Formato: não declarado na medida.

```dax
VAR Vendas_ecommerce =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "V",
        mv_vendas_produtos[flg_ecommerce] <> "S",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR Devolucoes_Vendas_ecommerce =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] = 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "D",
        mv_vendas_produtos[flg_ecommerce] <> "S",

        FILTER(
            ALL(calendario),
            calendario[ano_mes] = MAX(calendario[ano_mes])
        ),

        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    Vendas_ecommerce - Devolucoes_Vendas_ecommerce
```

### `**Qtd_Cupons_+1`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1165)

Formato: `#,0`

```dax
VAR CuponsVenda =
    CALCULATE(
        COUNTROWS(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        )
                ),
                [QtdTotal] > 1
            )
        ),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        COUNTROWS(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        )
                ),
                [QtdTotal] > 1
            )
        ),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `**Qtd_Cupon_balcao_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1230)

Formato: `0`

```dax
VAR CuponsVenda =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "V",
        mv_vendas_produtos[flg_ecommerce] <> "S",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "D",
        mv_vendas_produtos[flg_ecommerce] <> "S",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `**Qtd_Cupon_ecommerce_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1275)

Formato: `0`

```dax
VAR CuponsVenda =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "V",
        mv_vendas_produtos[flg_ecommerce] = "S",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR CuponsDevolucao =
    CALCULATE(
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento]),
        mv_vendas_produtos[tip_venda] = "D",
        mv_vendas_produtos[flg_ecommerce] = "S",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    CuponsVenda - CuponsDevolucao
```

### `*ticket_medio_1_item_atual_h`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1320)

Formato: não declarado na medida.

```dax
VAR TotalVendas =
    CALCULATE(
        [**Vlr_Vendas_1_Item_mes_atual],
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
    )
VAR TotalAtendimentos =
    CALCULATE(
        [**qtd_cupons_1_item_mes_atual],
        USERELATIONSHIP(calendario[Date], mv_vendas_produtos[dat_emissao]),
        USERELATIONSHIP(produto_gcp[cod_barra], mv_vendas_produtos[cod_barra_tratado]),
        USERELATIONSHIP(mv_dados_clientes[cod_cliente],mv_vendas_produtos[cod_cliente])
    )
RETURN
DIVIDE(TotalVendas, TotalAtendimentos, 0)
```

### `*media_itens_mes_atual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1342)

Formato: não declarado na medida.

```dax
CALCULATE(
    DIVIDE(
        SUM(mv_vendas_produtos[qtd_produto_venda]),
        DISTINCTCOUNT(mv_vendas_produtos[id_atendimento])
    ),

    FILTER(
        ALL(calendario),
        calendario[ano_mes] = MAX(calendario[ano_mes])
    ),

    USERELATIONSHIP(
        produto_gcp[cod_barra],
        mv_vendas_produtos[cod_barra_tratado]
    ),

    USERELATIONSHIP(
        calendario[Date],
        mv_vendas_produtos[dat_emissao]
    ),

    USERELATIONSHIP(
        mv_dados_clientes[cod_cliente],
        mv_vendas_produtos[cod_cliente]
    )
)
```

### `**Vlr_Vendas_mais1`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1375)

Formato: não declarado na medida.

```dax
VAR Vendas_mais1 =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] > 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "V",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

VAR Devolucoes_mais1 =
    CALCULATE(
        SUMX(
            FILTER(
                ADDCOLUMNS(
                    VALUES(mv_vendas_produtos[num_nota]),
                    "QtdTotal",
                        CALCULATE(
                            SUM(mv_vendas_produtos[qtd_produto_venda])
                        ),
                    "ValorVenda",
                        CALCULATE(
                            SUM(mv_vendas_produtos[vlr_total_venda])
                        )
                ),
                [QtdTotal] > 1
            ),
            [ValorVenda]
        ),
        mv_vendas_produtos[tip_venda] = "D",
        USERELATIONSHIP(
            produto_gcp[cod_barra],
            mv_vendas_produtos[cod_barra_tratado]
        ),
        USERELATIONSHIP(
            calendario[Date],
            mv_vendas_produtos[dat_emissao]
        ),
        USERELATIONSHIP(
            mv_dados_clientes[cod_cliente],
            mv_vendas_produtos[cod_cliente]
        )
    )

RETURN
    Vendas_mais1 - Devolucoes_mais1
```

### `***Ticket_medio_mais1`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1452)

Formato: não declarado na medida.

```dax
DIVIDE ( [**Vlr_Vendas_mais1], [**Qtd_Cupons_+1] )
```

### `**Gap_Ticket_medio(%)`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1457)

Formato: não declarado na medida.

```dax
DIVIDE ( [***Gap_de_Ticket (R$)], [***Ticket_medio_1_Item] )
```

### `***Texto_Diferenca_Ticket_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1462)

Formato: não declarado na medida.

```dax
VAR QtdVendas =
    [**qtd_cupons_1_item]

VAR Ticket1Item =
    [***ticket_medio_1_item]

VAR TicketMais1 =
    [***ticket_medio_mais1]

VAR TextoQtdVendas =
    SWITCH(
        TRUE(),
        QtdVendas >= 1000000,
            FORMAT(QtdVendas / 1000000, "0.#") & " mi",
        QtdVendas >= 1000,
            FORMAT(QtdVendas / 1000, "0") & " mil",
        FORMAT(QtdVendas, "#,##0")
    )

RETURN
    TextoQtdVendas
        & " vendas × ("
        & FORMAT(TicketMais1, "R$ #,##0")
        & " − "
        & FORMAT(Ticket1Item, "R$ #,##0")
        & ") de diferença de ticket médio"
```

### `***Receita_Potencial_Perdida`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1492)

Formato: `"R$"\ #,0.00;-"R$"\ #,0.00;"R$"\ #,0.00`

```dax
VAR Gap = [***Gap_de_Ticket (R$)]
RETURN IF ( Gap > 0, Gap * [**Qtd_Cupons_1_Item], 0 )
```

### `***%LucroPerdido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1501)

Formato: `0.00%;-0.00%;0.00%`

```dax
DIVIDE ( [***Receita_Potencial_Perdida], [**venda_liquida] )*-1
```

### `***Tooltip_Cupons_1_Item`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1505)

Formato: não declarado na medida.

```dax
"
REGRAS DE CÁLCULO

• Cupons 1 Item
Quantidade de vendas que possuem exatamente 1 produto/item no cupom.

• % Cupons 1 Item
Percentual de cupons com exatamente 1 item em relação ao total de cupons.

• Ticket Médio 1 Item
Faturamento dos cupons com exatamente 1 item ÷ quantidade de cupons com 1 item.

• Ticket Médio +1 Item
Faturamento dos cupons com mais de 1 item ÷ quantidade de cupons com mais de 1 item.

• Diferença de Ticket Médio
Ticket Médio +1 Item − Ticket Médio 1 Item.

• Potencial
Quantidade de Cupons 1 Item × Diferença de Ticket Médio.

Quanto maior o % de Cupons 1 Item e a diferença de ticket médio,
maior o potencial de aumento do faturamento por meio da venda de itens adicionais.
"
```

### `***Texto_%LucroPerdido`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/mv_vendas_produtos.tmdl#L1533)

Formato: não declarado na medida.

```dax
VAR Valor =
    [***%LucroPerdido]

VAR Seta =
    IF(
        Valor < 0,
        UNICHAR(9660),
        UNICHAR(9650)
    )

VAR Descricao =
    IF(
        Valor < 0,
        "Perda de oportunidades",
        "Oportunidade"
    )

RETURN
    Seta
        & " "
        & FORMAT(ABS(Valor), "0.0%")
        & " "
        & Descricao
```

## plano_acao_vendedores

### `*gargalo_principal`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/plano_acao_vendedores.tmdl#L4)

Formato: não declarado na medida.

```dax
VAR t = [**ticket_score]
VAR i = [**itens_score]
VAR a = [**atendimentos_score]
VAR l = [**lucro_score]
VAR minv = MIN( MIN(t,i), MIN(a,l) )
RETURN
SWITCH(TRUE(),
    l = minv, "Lucro",
    t = minv, "Ticket",
    i = minv, "Itens",
    "Atendimentos"
)
```

### `*plano_acao_base`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/plano_acao_vendedores.tmdl#L20)

Formato: não declarado na medida.

```dax
VAR g = [*gargalo_principal]
RETURN
SWITCH(
    g,

    "Lucro",
    "
    • Evitar descontos fora da política para proteger a margem
    • Oferecer genéricos e similares com maior rentabilidade
    • Sugerir produtos de marca própria sempre que possível
    • Explicar ao cliente o custo-benefício do produto sem reduzir preço
    • Analisar mix de produtos e identificar itens com maior margem potencial
    • Incentivar o uso de programas de fidelidade para aumentar recompra
    • Treinar vendedores para argumentação de valor sem ceder descontos
    • Monitorar margens por categoria e ajustar estratégias de compra
    ",

    "Ticket",
    "
    • Incentivar compra de medicamentos de uso contínuo em embalagens maiores (30 dias ou mais)
    • Combinar produtos de higiene e beleza com medicamentos para aumentar ticket médio
    • Criar kits promocionais atrativos (ex.: remédio + vitamina, dermocosmético + protetor solar)
    • Definir meta de ticket médio por atendimento
    • Sugerir produtos premium ou complementares que aumentem valor agregado
    • Identificar oportunidades de venda digital (ex.: pedidos online, WhatsApp) para aumentar ticket
    • Realizar acompanhamento diário do ticket médio por loja e por vendedor
    ",

    "Itens",
    "
    • Sempre oferecer produtos complementares (vitaminas, hidratantes, protetor solar)
    • Utilizar kits prontos para aumentar quantidade de itens por venda
    • Estabelecer meta mínima de pelo menos 2 itens por atendimento
    • Incentivar promoções de segunda unidade com desconto estratégico
    • Monitorar mix de categorias e garantir que produtos de maior giro estejam destacados
    • Treinar vendedores para sugerir produtos de forma natural, sem pressionar o cliente
    ",

    "Atendimentos",
    "
    • Realizar abordagem ativa no balcão e por telefone
    • Estabelecer meta mínima de atendimentos por turno
    • Monitorar se o vendedor está aproveitando todo o fluxo de clientes
    • Incentivar contato proativo com clientes frequentes (ligação, WhatsApp, app, aniversariantes...)
    • Avaliar tempo de atendimento e qualidade do serviço
    • Implementar checklists de atendimento para garantir padrão de excelência
    • Utilizar indicadores de conversão (clientes atendidos x clientes que compram) para ajustes
    ",

    "Sem ponto de atenção relevante: manter acompanhamento normal"
)
```

### `*plano_acao_contextual`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/plano_acao_vendedores.tmdl#L76)

Formato: não declarado na medida.

```dax
VAR t = [**ticket_score]
VAR i = [**itens_score]
VAR a = [**atendimentos_score]
VAR l = [**lucro_score]
RETURN
SWITCH(TRUE(),
    l < 40 && t >= 60,
    "• Rever descontos dados em remédios de alto valor
• Incentivar substituição por similares/genéricos mais rentáveis
• Oferecer produtos de marca própria na finalização da venda",

    l < 40 && i >= 60,
    "• Orientar equipe a priorizar itens de maior margem (ex.: dermocosméticos, vitaminas)
• Montar kits onde o produto principal seja de boa rentabilidade
• Evitar foco apenas em itens populares de baixa margem",

    l < 40 && a >= 60,
    "• Monitorar descontos excessivos em vendas de alto volume
• Definir meta mínima de margem por atendimento
• Usar alerta no caixa para autorizar descontos acima do limite",

    BLANK()
)
```

### `*plano_acao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/plano_acao_vendedores.tmdl#L105)

Formato: não declarado na medida.

```dax
VAR base = [*plano_acao_base]
VAR ctx  = [*plano_acao_contextual]
RETURN
IF( NOT ISBLANK(ctx), ctx, base )
```

### `*resumo_acao`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/plano_acao_vendedores.tmdl#L113)

Formato: não declarado na medida.

```dax
VAR vend = SELECTEDVALUE( mv_vendas_produtos[cod_nom_vendedor], "Vendedor" )
VAR garg = [*gargalo_principal]
RETURN
vend & UNICHAR(10) & UNICHAR(10) & 
"Ponto de atenção: " & garg & UNICHAR(10) & UNICHAR(10) & 
"Ações recomendadas: " & UNICHAR(10) & [*plano_acao]
```

## plano_de_contas

### `valor_por_subcodigo`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/plano_de_contas.tmdl#L4)

Formato: não declarado na medida.

```dax
VAR _codigo    = SELECTEDVALUE(plano_de_contas[codigo])
VAR _subcodigo = SELECTEDVALUE(plano_de_contas[subcodigo])

RETURN
SWITCH(
    TRUE(),

    _codigo = "1.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[dinheiro]),0) +
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[cheque]),0) +
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[cartao]),0) +
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[crediario]),0) +
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[convenio]),0),

    _subcodigo = "1.1", COALESCE(SUM('despesas_rel_pai_analit-1768488'[dinheiro]),0),
    _subcodigo = "1.2", COALESCE(SUM('despesas_rel_pai_analit-1768488'[cheque]),0),
    _subcodigo = "1.3", COALESCE(SUM('despesas_rel_pai_analit-1768488'[cartao]),0),
    _subcodigo = "1.4", COALESCE(SUM('despesas_rel_pai_analit-1768488'[crediario]),0),
    _subcodigo = "1.5", COALESCE(SUM('despesas_rel_pai_analit-1768488'[convenio]),0),

    _codigo = "2.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[venda_extraida_sistema_operacional]),0),
    _subcodigo = "2.0", COALESCE(SUM('despesas_rel_pai_analit-1768488'[venda_extraida_sistema_operacional]),0),

    _codigo = "3.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[desconto_concedido]),0),
    _subcodigo = "3.0", COALESCE(SUM('despesas_rel_pai_analit-1768488'[desconto_concedido]),0),

    _codigo = "4.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "4.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "4.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "6.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[despesas_com_pagamento_de_mercadorias]),0) +
        100 +
        100 +
        100,

    _subcodigo = "6.1", COALESCE(SUM('despesas_rel_pai_analit-1768488'[despesas_com_pagamento_de_mercadorias]),0),
    _subcodigo = "6.2", 100,
    _subcodigo = "6.3", 100,
    _subcodigo = "6.4", 100,

    _codigo = "7.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "7.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "7.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "7.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "7.4", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "7.5", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "7.6", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "8.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "8.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "9.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "9.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "9.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "9.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "9.4", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "9.5", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "9.6", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "9.7", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "10.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "10.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "10.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "10.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "11.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "11.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "11.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "11.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "11.4", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "11.5", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "11.6", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "11.7", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "12.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "12.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "12.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "12.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "13.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "13.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "13.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "13.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "14.0" && ISBLANK(_subcodigo),
        100,                    --COALESCE(SUM('despesas_rel_pai_analit-1768488'[lucro]),0),
    _subcodigo = "14.0", 100,   --COALESCE(SUM('despesas_rel_pai_analit-1768488'[lucro]),0),

    _codigo = "15.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _subcodigo = "15.1", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "15.2", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "15.3", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "15.4", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "15.5", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),
    _subcodigo = "15.6", COALESCE(SUM('despesas_rel_pai_sint'[valor_pagar]),0),

    _codigo = "16.0" && ISBLANK(_subcodigo),
        COALESCE(SUM('despesas_rel_pai_analit-1768488'[reembolso_fcia_popular]),0),

    _subcodigo = "16.0", COALESCE(SUM('despesas_rel_pai_analit-1768488'[reembolso_fcia_popular]),0),

    _subcodigo = "17.1", COALESCE(SUM('despesas_rel_pai_analit-1768488'[num_clientes_atendidos]),0),
    _subcodigo = "17.3", COALESCE(SUM('despesas_rel_pai_analit-1768488'[estoque_preco_venda]),0),
    _subcodigo = "17.5", COALESCE(SUM('despesas_rel_pai_analit-1768488'[venda_delivery]),0),
    _subcodigo = "17.6", COALESCE(SUM('despesas_rel_pai_analit-1768488'[contas_pagar_fornec_aberto]),0),
    _subcodigo = "17.7", COALESCE(SUM('despesas_rel_pai_analit-1768488'[unidades_vendidas]),0),
    _subcodigo = "17.8", COALESCE(SUM('despesas_rel_pai_analit-1768488'[num_colaboradores]),0),
    _subcodigo = "17.9", COALESCE(SUM('despesas_rel_pai_analit-1768488'[m2_area_venda]),0),

    _subcodigo = "18.1", COALESCE(SUM('despesas_rel_pai_analit-1768488'[valor_propagados]),0),
    _subcodigo = "18.2", COALESCE(SUM('despesas_rel_pai_analit-1768488'[valor_genericos]),0),
    _subcodigo = "18.3", COALESCE(SUM('despesas_rel_pai_analit-1768488'[valor_similares]),0),
    _subcodigo = "18.4", COALESCE(SUM('despesas_rel_pai_analit-1768488'[valor_perfumarias]),0),
    _subcodigo = "18.5", COALESCE(SUM('despesas_rel_pai_analit-1768488'[outros_valores]),0),
    _subcodigo = "18.6", COALESCE(SUM('despesas_rel_pai_analit-1768488'[valor_sem_classificacao]),0),

    _subcodigo = "19.1", COALESCE(SUM('despesas_rel_pai_analit-1768488'[qtd_propagados]),0),
    _subcodigo = "19.2", COALESCE(SUM('despesas_rel_pai_analit-1768488'[qtd_genericos]),0),
    _subcodigo = "19.3", COALESCE(SUM('despesas_rel_pai_analit-1768488'[qtd_similares]),0),
    _subcodigo = "19.4", COALESCE(SUM('despesas_rel_pai_analit-1768488'[qtd_perfumarias]),0),
    _subcodigo = "19.5", COALESCE(SUM('despesas_rel_pai_analit-1768488'[qtd_outros]),0),
    _subcodigo = "19.6", COALESCE(SUM('despesas_rel_pai_analit-1768488'[qtd_sem_classificacao]),0),


    BLANK()
)
```

## portal_authorization

### `usuario_logado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/portal_authorization.tmdl#L4)

Formato: não declarado na medida.

```dax
USERPRINCIPALNAME()
```

### `tagvalue_logada`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/portal_authorization.tmdl#L7)

Formato: `0`

```dax
CALCULATE(
    MAX('portal_authorization'[tagvalue]),
    FILTER(
        'portal_authorization',
        'portal_authorization'[username] = [usuario_logado]
    )
)
```

## simulacao_precificacao_analise_mercado

### `percentual_simulacao_selecionado`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/simulacao_precificacao_analise_mercado.tmdl#L4)

Formato: não declarado na medida.

```dax
VAR classificacao_selecionada =
    SELECTEDVALUE(classificacao_precificacao[classificacao], "Todos")
VAR perc_simulacao_string = SELECTEDVALUE(simulacao_precificacao_analise_mercado[percentual], "0")
VAR perc_simulacao_number =
    VALUE(SUBSTITUTE(perc_simulacao_string, "%", ""))
RETURN
    SWITCH(
        TRUE(),
        classificacao_selecionada IN {"Avaliar competitividade"},
            -perc_simulacao_number,
        classificacao_selecionada IN {"Abaixo do mercado","Faixa normal","Todos"},
            perc_simulacao_number
    )
```

## tabela_cadastro_lojas

### `*qtd_cnpjs`

[Fonte TMDL](../Connect%20HUB.SemanticModel/definition/tables/tabela_cadastro_lojas.tmdl#L4)

Formato: `#,0`

```dax
DISTINCTCOUNT(tabela_cadastro_lojas[num_cnpj])
```
