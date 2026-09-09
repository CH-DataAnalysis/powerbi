# Contratos dos arquivos externos

Gerado do Power Query/TMDL. Lista campos exigidos pela importação, inclusive campos removidos depois. Não contém dados de clientes.

Obtenção, responsabilidades e atualização: [Fontes e instalação](fontes-e-instalacao.md). Validação opcional: `python scripts/validate_project.py --data-dir C:\PowerBI`.

## cadastro_fornecedor.csv

Tabela: `cadastro_fornecedor`.

CSV UTF-8, separador vírgula, 3 colunas, QuoteStyle.Csv. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`cnpj_fornecedor`, `nome_fornecedor`, `nome_comercial`

## despesas_rel_pai_analit.xlsx

Tabela: `despesas_rel_pai_analit-1768488`.

Aba obrigatória: `despesas_rel_pai_analit-1768488`. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`mes`, `dinheiro`, `cheque`, `cartao`, `crediario`, `convenio`, `venda_extraida_sistema_operacional`, `desconto_concedido`, `despesas_com_pagamento_de_mercadorias`, `valor_juros`, `produtos_vencidos`, `reembolso_fcia_popular`, `num_clientes_atendidos`, `estoque_preco_venda`, `venda_delivery`, `contas_pagar_fornec_aberto`, `unidades_vendidas`, `num_colaboradores`, `m2_area_venda`, `valor_propagados`, `valor_genericos`, `valor_similares`, `valor_perfumarias`, `outros_valores`, `valor_sem_classificacao`, `qtd_propagados`, `qtd_genericos`, `qtd_similares`, `qtd_perfumarias`, `qtd_outros`, `qtd_sem_classificacao`, `cod_filial`, `num_cnpj`

## despesas_rel_pai_sint.xlsx

Tabela: `despesas_rel_pai_sint`.

Aba obrigatória: `despesas_rel_pai_sint`. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`mes`, `valor_pagar`, `valor_pago`, `cod_filial`, `num_cnpj`, `codigo_referencia`, `cod_contasint`, `num_mascara`, `cod_despesa`, `descricao_despesa`, `sub_descricao_despesa`, `nom_contafb`

## geolocalizacao.csv

Tabela: `geolocalizacao`.

CSV UTF-8, separador vírgula, 32 colunas, QuoteStyle.None. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`Pais_Cod`, `Regiao_Cod`, `UF_Cod`, `Meso_Cod`, `Micro_Cod`, `Municipio_Cod`, `Municipio`, `Micro_Regiao`, `Meso_Regiao`, `UF_Sigla`, `UF_Nome`, `Regiao_Sigla`, `Regiao_Nome`, `Pais_Nome`, `Municipio_Area`, `Municipio_Ponto`, `Municipio_Area_Alta_Qualidade`, `Micro_Regiao_Area`, `Micro_Regiao_Ponto`, `Micro_Regiao_Area_Alta_Qualidade`, `Meso_Regiao_Area`, `Meso_Regiao_Ponto`, `Meso_Regiao_Area_Alta_Qualidade`, `UF_Area`, `UF_Ponto`, `UF_Area_Alta_Qualidade`, `Regiao_Area`, `Regiao_Ponto`, `Regiao_Area_Alta_Qualidade`, `Pais_Area`, `Pais_Ponto`, `Pais_Area_Alta_Qualidade`

## lat_long.csv

Tabela: `lat_long`.

CSV UTF-8, separador vírgula, 4 colunas, QuoteStyle.None. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`CEP_1`, `CEP_2`, `Latitude`, `Longitude`

## logos.xlsx

Tabela: `logo_associacao`.

Aba obrigatória: `Associação`. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`codigo_rede`, `link`

## parceiros_pbm_padrao.csv

Tabela: `parceiros_pbm_padrao`.

CSV UTF-8, separador vírgula, 3 colunas, QuoteStyle.None. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`cod_parceiro`, `parceiro_pbm`, `Programa`

## plano_de_contas.xlsx

Tabela: `plano_de_contas`.

Aba obrigatória: `Planilha1`. Cabeçalhos na primeira linha.

Cabeçalhos exigidos:

`codigo`, `descricao`, `subcodigo`, `subdescricao`
