# Documentação e operação do Connect Hub

Objetivo autorizado: adaptar README e changelog ao checkout e concluir os itens 3 e 6 da avaliação, sem commit ou publicação.

Abordagem: manter PBIP/PBIR/TMDL como fonte de verdade, preservar o padrão atual de fontes e adicionar ferramentas Python sem dependências externas. A documentação gerada deve detectar desatualização; a validação estática não substitui atualização e testes no Power BI.

- [x] Parametrizar as oito fontes File.Contents com `PastaArquivos`, mantendo `C:\PowerBI` como padrão.
- [x] Criar gerador de inventário de páginas, modelo, medidas e contratos dos arquivos externos.
- [x] Criar validador de referências, JSON, parâmetros, consultas por cliente, documentos gerados e fontes locais opcionais; testar casos válidos e falhas em diretórios temporários.
- [x] Adaptar README e changelog ao histórico Git real. Documentar instalação, obtenção dos arquivos, credenciais, gateway, atualização, indicadores, manutenção, homologação, publicação e rollback.
- [x] Adicionar CI no GitHub Actions para testes e validação estática, sem conexão às fontes e sem publicação.
- [x] Gerar catálogos, executar testes e validações, conferir diff e registrar limitações externas.

Validação: `python -m unittest discover -s tests -v`, `python scripts/validate_project.py`, `python scripts/validate_project.py --data-dir C:\PowerBI`, `git diff --check`. Não executar o SQL fornecido; não alterar DAX, RLS ou políticas incrementais.

Resultado local: 12 testes aprovados; validador est?tico e verifica??o dos oito arquivos externos aprovados; 557 links locais conferidos; revis?o independente conclu?da e caso de CSV com aspas corrigido. Nenhum commit, SQL ou publica??o executado. Gateway, credenciais, agenda e homologa??o de neg?cio no servi?o permanecem etapas externas documentadas.
