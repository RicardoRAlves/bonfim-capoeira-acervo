# Bonfim Capoeira Acervo

Acervo histórico da Associação Nosso Senhor do Bonfim, publicado no GitHub Pages em
https://ricardoralves.github.io/bonfim-capoeira-acervo/.

O site é estático: HTML, CSS e JavaScript, sem servidor de aplicação ou dependências
de instalação. As páginas já geradas ficam versionadas e funcionam sem executar Python.

## Atualização de setembro de 2026

Consulte [o relatório de revisão](docs/REVISAO-2026-09.md) para a comparação editorial,
novas rotas, fontes, direitos e validações. Jundiaí continua sendo a única cidade no
menu principal. São Paulo reúne dois núcleos distintos, Aroeira/Zula e Mestre Marcão.

## Manutenção

- `data/*.json`: catálogo estruturado, com colunas e linhas da pesquisa revisada.
  `research.json` registra a procedência e os hashes dos arquivos utilizados.
- Páginas narrativas: editar o HTML correspondente, preservando as fontes.
- `scripts/build_catalogs.py`: gera as páginas de catálogo e os trechos delimitados
  por `<!-- catalog:... -->`. Não editar manualmente esses trechos.
- `assets/research.js` e `assets/research.css`: busca, filtros e extensões do visual.
  O índice da busca é produzido a partir do texto editorial final, incluindo ressalvas.

Após alterar dados ou texto:

```sh
python scripts/build_catalogs.py
python scripts/check_site.py
node --check assets/research.js
```

Python 3 usa somente a biblioteca padrão. Para revisão local, sirva a pasta que
contém este repositório e abra `/bonfim-capoeira-acervo/`; esse prefixo é necessário
para reproduzir os caminhos do GitHub Pages. Exemplo, a partir da pasta pai:

```sh
python -m http.server 8765
```

O workflow de validação verifica geração reproduzível, navegação e sintaxe. O
workflow de publicação existente continua restrito a `main` ou execução manual;
um Pull Request não publica o site. A revisão de setembro deve ser aprovada antes
de qualquer merge.

## Uso de mídia

Fotografias, cartazes, digitalizações e capa do disco com autorização pendente são
descritos e ligados às fontes, sem cópia pública neste conjunto. Os originais de
pesquisa não são distribuídos no repositório. Incorporar uma mídia futuramente
exige registrar crédito, licença/autorização e eventuais condições de uso.
