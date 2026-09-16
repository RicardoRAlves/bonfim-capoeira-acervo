# Revisão editorial e técnica — setembro de 2026

Atualização preparada em `research-update-2026-09` para revisão antes de merge.
O site publicado em `main` não foi alterado durante a preparação.

## Base e método de comparação

Foram examinados o site existente, seus 32 arquivos HTML, a arquitetura estática,
as 65 páginas de `Dossie_Bonfim_Revisado.pdf` e as 13 abas de
`Catalogos_Bonfim_Revisado.xlsx`. A versão revisada tem precedência editorial.
Os hashes dos dois arquivos estão em `data/research.json`.

As abas lidas foram Resumo, Núcleos, Mídias, Vídeos, Música, Cronologia, Pessoas,
Resultados, Fontes, Pistas, Índice Instagram, Divergências e Documentos. Os dados
foram cotejados com o texto e as seleções de registros já presentes no site. Não
se confundiu diferença de formatação de uma data com descoberta histórica.

| Área | Situação anterior | Tratamento nesta revisão |
|---|---|---|
| Navegação e identidade | Oito entradas principais, Jundiaí em destaque, paleta azul/amarela, mapa e tipografia próprios | Preservados. Novas rotas internas e busca no rodapé; nenhuma outra cidade no menu principal |
| História | Síntese e cronologia selecionada | Síntese preservada e ampliada; cronologia pesquisável com os 86 registros |
| Régis | Biografia, fundação e homenagem | Acrescentadas diferenças entre fontes, formação, memória autobiográfica, limites dos títulos e resultados; homenagem de 2012 contextualizada |
| Jundiaí | Formação local, espaços, equipe e registros selecionados | Documentos de 1994–2004, funções em 2001/2002, Sereia, ensino infantil, intercâmbios, endereços de épocas diferentes e alcance dos editais |
| Kauê | Informações distribuídas pela página de Jundiaí | Perfil próprio com formação, chegada em 1988, marco de 1990, ensino, música, alunos, esporte e divergências biográficas |
| São Paulo | Uma ficha territorial com referências aos dois mestres | Página reorganizada e duas páginas de núcleos, com locais distintos e sem endereço comum presumido |
| Cidades | Mapa e 20 fichas municipais | Mantidos; complementos históricos, frente distrital de Córrego Rico, três indícios e 22 pistas contextualizadas |
| Acervo | Galeria selecionada de reproduções | Porta de entrada para documentos, pessoas, registros visuais, resultados, cronologia e índice de publicações; referências preservadas sem reproduções pendentes |
| Documentos | Impressos não organizados em fichas próprias | 12 fichas, representando 10 peças; datas impressas, duplicatas, limites e relações com pessoas e eventos |
| Pessoas | Nomes distribuídos nas narrativas | Índice de 49 registros de pessoas ou conjuntos; funções e títulos datados pelas fontes |
| Vídeos | Seleção editorial de filmes e registros | Seleção preservada e catálogo dos 44 registros, com filtros e limites da identificação/visualização |
| Música | Álbum e 14 faixas | Preservados; créditos de plataforma separados da autoria de composição e da data de graduação; instrumentos e repertório contextualizados |
| Comunidade | Projetos e casos locais | Campanhas dos impressos, intercâmbio infantil de 2018, Jangadinha e relato de Risadinha; sem inventar números de arrecadação ou contratos |
| Fontes | Bibliografia e créditos selecionados | 120 fontes, R01, 21 divergências e fontes recolhíveis junto às histórias |

## Correções e distinções importantes

- **R01:** relato de alunos sem identificação nominal. A relação de Zula com Kauê,
  a residência de Zula na capital, os dois locais distintos e a formação de Marcão
  por Reginaldo são preservados como memória testemunhal. Não são apresentados
  como entrevistas independentes realizadas por esta pesquisa.
- **Marcão:** Mestre, formado por Reginaldo segundo R01. O perfil profissional
  informado pelo usuário foi incorporado à descrição mínima. Não foi confundido
  com Marcos Antônio de Lima, de Alpinópolis, nem teve identidade civil completada
  por inferência. A forma Henrri permanece vinculada à fonte histórica que a usa.
- **1997:** o impresso já emprega Mestre Kauê; não estabelece sua graduação naquele ano.
- **2002:** o documento identifica Carlos Alberto da Silva como presidente,
  Reginaldo como diretor geral e Helena R. da Silva como secretária executiva.
- **1999:** a edição de 23–29/10, a legenda de 23/10 e a fotografia marcada
  24/10/98 são distinguidas. Reutilização da fotografia é provável; não se inventa
  um 8º batizado confirmado.
- **Datas dos arquivos:** “Bonfim 1998” no nome não substitui a data impressa.
  A04/A05 são duas digitalizações do cartaz de 2004; A09/A12 são página e recorte.
- **Endereços:** Casa da Cultura, Clube São João, Esportiva e SESI são espaços
  históricos; 321/221 da Marechal Deodoro e Jardim Morumbi/Vila Municipal são
  referências que não foram artificialmente harmonizadas. Endereço histórico
  não foi convertido em recomendação atual de treino.
- **Território:** 24 fichas correspondem a 20 municípios brasileiros, uma frente
  distrital e três indícios. Não são 24 academias ativas. Uma visita, um evento ou
  um convidado de outro país não prova filial; ausência de atualização não prova encerramento.
- **Esporte:** 64 entradas não equivalem a 64 medalhas. Há colocações e resultados
  coletivos; declarações do grupo e resultados municipais/oficiais ficam separados.
- **Mídia:** 127 registros visuais não equivalem a 127 fotografias individuais;
  44 registros audiovisuais incluem canal e páginas de referência. A pesquisa não
  reivindica ter assistido integralmente a todos os vídeos.
- **Busca:** indexa o texto editorial final. Conserva a ressalva sobre 1979 e a
  identificação musical de Zula, em vez de reapresentar campos genéricos do catálogo.

## Rotas novas e arquitetura

Foram acrescentadas 23 páginas, mantendo as URLs existentes:

- `/jundiai/mestre-kaue/`
- `/cidades/sao-paulo/aroeira/`
- `/cidades/sao-paulo/mestre-marcao/`
- `/cidades/jaboticabal/corrego-rico/`
- `/historia/cronologia/`
- `/acervo/busca/`
- `/acervo/documentos/` e suas 12 fichas, de `a01/` a `a12/`
- `/acervo/pessoas/`
- `/acervo/registros-visuais/`
- `/acervo/resultados/`
- `/acervo/indice-instagram/`

Cada caminho acima usa o prefixo de publicação `/bonfim-capoeira-acervo`.
O resultado contém 55 arquivos HTML: 54 páginas `index.html` e a página de erro
`404.html`. O mapa continua destacando 20 municípios, com explicação do alcance.
Documentos, pessoas, cidades, cronologia e fontes passam a ter ligações contextuais.

Não foi adotado framework, banco de dados ou novo serviço de hospedagem. Os dados
estruturados alimentam um gerador Python sem dependências. As páginas narrativas
continuam editáveis em HTML; somente os blocos marcados e as páginas de catálogo
são gerados. JavaScript acrescenta filtros e busca; os registros permanecem
legíveis sem ele. O sitemap foi atualizado.

## Materiais não republicados e pendências

Foram retiradas desta versão 166 cópias locais de fotografias, variantes de tamanho
e capa do disco cuja autorização estava pendente na documentação anterior. As
referências, descrições e créditos continuam disponíveis. Os arquivos originais
do usuário não foram alterados; o histórico Git também não foi reescrito.

As 12 digitalizações não foram copiadas para o repositório: suas fichas descrevem
o conteúdo, a procedência, duplicatas e limites. Não foram hospedados áudio,
filme completo ou gravações de terceiros. Permanecem links às plataformas e
incorporações oficiais já existentes. Miniaturas remotas do YouTube acompanham
esses acessos; não foram baixadas como novo acervo fotográfico.

Continuam pendentes:

- Ano/local de nascimento e idade inicial de Kauê; as versões não coincidem.
- Fundação geral em 1977, 1978 ou 1979; 1978 é predominante, sem apagar as demais.
- Datas documentais das graduações de Kauê, Sereia, Zula e Marcão, quando não demonstradas.
- Endereço atual, início do núcleo e graduação de Marcão; endereço atual do Aroeira.
- Realização das formaturas anunciadas e datas de filmagem diferentes da publicação.
- Identificação completa de participantes, autores, fotógrafos e compositores.
- Certificação oficial de Ponto de Cultura e atos de concessão de prêmios do Aroeira.
- Pagamentos/execução dos projetos: seleção ou habilitação em edital não comprovam repasse.
- Autorizações de reprodução, especialmente imagens de crianças.
- Indícios territoriais e alegações de atuação internacional sem sede demonstrada.

## Verificação realizada

- Validação de todos os 55 HTML: links internos e fragmentos, prefixo do Pages,
  arquivos referenciados, páginas órfãs, IDs repetidos, menu exato, idioma,
  um título principal por página, textos alternativos e títulos de iframes.
- Contagens e IDs dos 12 catálogos de dados; 12 digitalizações/10 peças; presença
  de R01 nos dois núcleos; ressalvas essenciais também no índice de busca.
- Navegação real nas 54 páginas `index.html`, em 1440 × 1000 e 320 × 740 pixels:
  sem largura excedente, imagens quebradas detectadas ou erros/avisos de console.
  Inspeções visuais adicionais da home, perfil de Kauê e acervo em desktop e celular.
- Menu móvel abre/fecha e responde a Escape. Corrigidos títulos que escapavam da
  tela no desenho anterior e a largura dos cartões comunitários.
- Filtro combinado da cronologia (batizado + Jundiaí + anos 1990: quatro registros),
  estado vazio e restauração dos 86 registros. Filtro de SP: 12 dos 20 municípios;
  busca por Zula: São Paulo; limpeza: 20 municípios.
- Busca geral por Marcão, Zula e termo inexistente; destinos de registros com âncoras.
- Sintaxe dos três arquivos JavaScript e geração reproduzível dos catálogos.
- Verificação HTTP dos endereços externos: 355 URLs finais; 353 responderam 200
  por HEAD ou GET. Cultura Viva retornou 403 e Circuito Serras de Ibitipoca, 406;
  mantidos como limitação de acesso automático, não como prova de desaparecimento.
  HTTP 200 não comprova conteúdo integral acessível: redes sociais podem exigir login.
- Removidos links individuais de Instagram gerados a partir de separadores/códigos
  vazios. S33, já registrado como indisponível na pesquisa, conserva o endereço
  histórico em texto e sua ressalva, sem prometer acesso funcional.
- O botão de vídeo cria iframe oficial com título e link alternativo preservado.
  O player externo ficou vazio no navegador de teste; reprodução efetiva não foi
  comprovada neste ambiente. O acesso direto ao YouTube permanece disponível.

O workflow de validação do PR não publica o site. O workflow de GitHub Pages
permanece restrito a `main` ou acionamento manual. Esta proposta não faz merge.

## Próximas etapas opcionais

Recolher autorizações e créditos das mídias, registrar depoimentos consentidos
com datas, confirmar os endereços dos núcleos e localizar atas/diplomas/encartes.
Essas contribuições podem enriquecer as fichas existentes sem mudar o menu principal.
