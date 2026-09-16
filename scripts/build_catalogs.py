"""Atualiza catálogos estáticos a partir de data/*.json. Python 3, sem dependências.

Páginas narrativas são editadas diretamente; somente blocos delimitados por
comentários 'catalog' e páginas listadas em write_page são gerados aqui.
"""
from pathlib import Path
from html import escape as esc
from html.parser import HTMLParser
from urllib.parse import quote
import json, re, unicodedata

ROOT = Path(__file__).resolve().parents[1]
BASE = '/bonfim-capoeira-acervo/'
ORIGIN = 'https://ricardoralves.github.io'
DATA = {p.stem:json.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'data').glob('*.json')}
ROWS = {k:v['rows'] for k,v in DATA.items() if 'rows' in v}
SOURCES = {r[0]:r for r in ROWS['sources']}
PEOPLE = {r[0]:r for r in ROWS['people']}

def e(value): return esc(str(value or ''), quote=True)
def slug(value): return re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',value).encode('ascii','ignore').decode().lower()).strip('-')
def clean(value):
    text=str(value or '')
    for a,b in [('NÃO CONFIRMADOS','ainda não confirmados'),('NÃO CONFIRMADAS','ainda não confirmadas'),('NÃO CONFIRMADO','ainda não confirmado'),('NÃO CONFIRMADA','ainda não confirmada'),('PROVÁVEL','provável'),('CONFIRMADA','documentada'),('CONFIRMADO','documentado'),('CONFIRMADAS','documentadas')]: text=text.replace(a,b)
    return text
def a(path,label,cls='text-link'): return f'<a class="{cls}" href="{BASE}{path}">{e(label)}</a>'
def external(url,label):
    if not str(url).startswith(('https://','http://')): return e(label)
    return f'<a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)} ↗</a>'
def p(text): return '<p>'+e(clean(text))+'</p>'
def section(title,body,id=''): return f'<section class="wrap section research-section"'+(f' id="{id}"' if id else '')+f'><h2>{title}</h2>{body}</section>'
def refs(value):
    links=[]
    # Expand document ranges without truncating S100–S120.
    value=re.sub(r'A(\d{2})[–-]A(\d{2})',lambda m:','.join(f'A{i:02}' for i in range(int(m[1]),int(m[2])+1)),str(value))
    for code in dict.fromkeys(re.findall(r'\b(?:S\d{2,3}|A\d{2}|R01)\b',value)):
        if code in SOURCES: links.append(a('fontes/#'+code, SOURCES[code][1]))
        elif code.startswith('A'): links.append(a('acervo/documentos/'+code.lower()+'/', 'Documento '+code))
        elif code=='R01': links.append(a('fontes/#R01','Relato de alunos'))
    for codes in re.findall(r'IG\s+([\w,-]+)',value):
        for code in codes.split(','):
            if re.fullmatch(r'[A-Za-z0-9_-]{5,}',code):links.append(external('https://www.instagram.com/p/'+code+'/','Publicação individual do grupo'))
    return '<details class="source-details"><summary>Fontes e contexto</summary><div class="source-links">'+''.join(links)+'</div></details>' if links else ''

def place_path(r):
    if r[0]=='N02': return 'jundiai/'
    if r[0]=='N13': return 'cidades/jaboticabal/corrego-rico/'
    if r[0] in ['N21','N22','N23']: return 'cidades/#'+r[0]
    return 'cidades/'+slug(r[1])+'/'

def related(value):
    links=[]
    for r in ROWS['places']:
        pattern=r'\b'+re.escape(r[1])+r'\b'
        if r[1]=='Registro':pattern=r'\bRegistro(?=$|[,;/·])'
        if re.search(pattern,value) and r[0] not in ['N13']: links.append(a(place_path(r),r[1]))
    for term,path,label in [('Kauê','jundiai/mestre-kaue/','Mestre Kauê'),('Zula','cidades/sao-paulo/aroeira/','Zula / Aroeira'),('Sereia','acervo/pessoas/#P006','Mestra Sereia'),('Reginaldo','mestre-reginaldo/','Mestre Régis')]:
        if term in value: links.append(a(path,label))
    return '<nav class="related-links" aria-label="Conteúdos relacionados">'+''.join(dict.fromkeys(links))+'</nav>' if links else ''

def record(id,title,body,city='',kind='',date='',search=''):
    return f'<article class="catalog-record" id="{e(id)}" data-record data-city="{e(city)}" data-kind="{e(kind)}" data-date="{e(date)}" data-search="{e(search or title)}"><p class="record-type">{e(kind)}</p><h3>{title}</h3>{body}</article>'

def catalog(items, cities=(), kinds=(), decades=False):
    def select(name,label,opts): return f'<label>{label}<select name="{name}"><option value="">Todos</option>'+''.join(f'<option>{e(x)}</option>' for x in sorted(set(opts)) if x)+ '</select></label>'
    controls='<label>Pesquisar neste catálogo<input name="q" type="search" placeholder="Nome, lugar, assunto…" autocomplete="off"></label>'
    if cities: controls+=select('city','Localidade',cities)
    if kinds: controls+=select('kind','Tipo de registro',kinds)
    if decades: controls+=select('decade','Década',[str(i) for i in range(1950,2030,10)])
    return '<div class="catalog" data-catalog><form class="catalog-controls" role="search">'+controls+'<button type="reset">Limpar filtros</button></form><p class="catalog-count" role="status" aria-live="polite">'+str(len(items))+' registros</p><p class="catalog-empty" hidden>Nenhum registro encontrado. Experimente outro termo ou limpe os filtros.</p><div class="catalog-records">'+''.join(items)+'</div><noscript>Todos os registros estão disponíveis nesta página. Os filtros precisam de JavaScript.</noscript></div>'

def shell(path,title,lead,body,active='acervo'):
    source=(ROOT/'index.html').read_text(encoding='utf-8')
    head=source.split('<main id="conteudo">')[0]
    footer=source.split('</main>')[1]
    head=re.sub(r'<title>.*?</title>',f'<title>{e(title)} | Bonfim Capoeira</title>',head)
    head=re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*',lambda m:m[1]+e(lead),head)
    head=re.sub(r'(<meta property="og:title" content=")[^"]*',lambda m:m[1]+e(title+' | Bonfim Capoeira'),head)
    head=re.sub(r'(<(?:link rel="canonical" href|meta property="og:url" content)=")[^"]*',lambda m:m[1]+ORIGIN+BASE+path+'/',head)
    head=re.sub(r' aria-current="page"','',head)
    head=head.replace(f'href="{BASE}{active}/"',f'href="{BASE}{active}/" aria-current="page"',1)
    head=re.sub(r'<body class="[^"]*"','<body class="page-'+active+'"',head)
    return head+f'<main id="conteudo"><div class="wrap breadcrumb">{a("","Início")} / {a(active+"/",dict(historia="História",acervo="Acervo",cidades="Cidades",jundiai="Jundiaí").get(active,active))}</div><header class="page-heading wrap"><p class="eyebrow">Memória do Bonfim</p><h1>{e(title)}</h1><p class="lead">{e(lead)}</p></header>'+body+'</main>'+footer

def write_page(path,title,lead,body,active='acervo'):
    file=ROOT/path/'index.html'; file.parent.mkdir(parents=True,exist_ok=True)
    file.write_text(shell(path,title,lead,body,active),encoding='utf-8',newline='\n')

def block(path,key,html):
    f=ROOT/path/'index.html' if path else ROOT/'index.html'
    text=f.read_text(encoding='utf-8'); start=f'<!-- catalog:{key} -->'; end=f'<!-- /catalog:{key} -->'
    replacement=start+'\n'+html+'\n'+end
    pattern=re.escape(start)+'.*?'+re.escape(end)
    if start in text: text=re.sub(pattern,lambda m:replacement,text,flags=re.S)
    else: text=text.replace('</main>',replacement+'</main>')
    f.write_text(text,encoding='utf-8',newline='\n')

def timeline():
    cards=[]
    for r in ROWS['timeline']:
        id,date,exact,event,city,source,confidence=r
        if id=='T006': date='1979, segundo relato biográfico'; event='A Jundpedia situa o início com Reginaldo em 20/05/1979, mas apresenta idade incompatível com o nascimento informado. Ano provável; dia, mês e idade inicial não confirmados.'
        event=clean(event)
        if id in ['T061','T062','T063','T064','T065','T066','T067','T068','T070','T071','T074','T076']: city='Jundiaí'+(' · '+city if city!='Jundiaí' else '')
        if id in ['T072','T085']: city='São Paulo; Jundiaí'
        if id in ['T077','T079','T080','T081','T082','T083','T084','T086']: city='São Paulo · '+city
        years=re.findall(r'(?:19|20)\d{2}',date)
        kind='Publicação / registro' if re.search('publica|perfil|catálogo|dissertação|relato do encontro',event,re.I) else 'Acontecimento / memória'
        if re.search('anunci|convite|programação',event,re.I): kind='Anúncio'
        if id in ['T005','T006','T041','T064']: kind='Data divergente'
        body=p(event)+p(city)+refs(source)+related(event+' '+city)
        # Only use precision actually present in the displayed date. Undated
        # months/days sort after the dated entries of the same year.
        iso=re.match(r'^(\d{4})-(\d{2})(?:-(\d{2}))?',date)
        br=re.match(r'^(\d{2})/(\d{2})/(\d{4})$',date)
        sort_date=(min(years) if years else '9999')+'-99-99'
        if iso:sort_date=f'{iso[1]}-{iso[2]}-{iso[3] or "99"}'
        if br:sort_date=f'{br[3]}-{br[2]}-{br[1]}'
        cards.append((sort_date,id,record(id,e(date),body,city,kind,' '.join(years),event+' '+city+' '+date+' '+source)))
    cards.sort(key=lambda x:(x[0],x[1]))
    html=catalog([x[2] for x in cards],[r[1] for r in ROWS['places'] if r[0]!='N13'],['Publicação / registro','Acontecimento / memória','Anúncio','Data divergente'],True)
    write_page('historia/cronologia','Tempo de aprender e ensinar','86 marcos para percorrer a história. Anúncios, publicações e lembranças conservam suas próprias datas.',section('Encontre um período',p('O ano orienta a navegação; não preenche dias, meses ou graduações desconhecidos. Registros sobre um mesmo evento podem aparecer em mais de uma entrada, preservando o catálogo.')+html),'historia')

DOC_META={
 'A01':('11º batizado · 2002','T067',['P001','P005','P006','P007','P044','P046','P048']),
 'A02':('10º batizado · 2001','T066',['P001','P005','P006','P007','P044','P045','P046','P047','P048']),
 'A03':('6º batizado · 1997','T062',['P005']), 'A04':('13º batizado · 2004','T068',['P005']),
 'A05':('Outra digitalização do cartaz de 2004','T068',['P005']),
 'A06':('7º batizado · 1998','T063',['P005']), 'A07':('9º batizado · 2000','T065',['P005']),
 'A08':('3º batizado · 1994','T061',[]), 'A09':('Página Sociais · 1999','T064',[]),
 'A10':('Bastidores · 2002','',[]), 'A11':('A caminho da batalha · 2002','',[]),
 'A12':('Recorte da página Sociais · 1999','T064',[])}

def documents():
    cards=[]
    for r in ROWS['documents']:
        id,file,date,desc,provenance,assessment,duplicate,availability,rights,confidence=r
        title,event,people=DOC_META[id]; path='acervo/documentos/'+id.lower()
        body=p(desc)+p(assessment)
        if duplicate: body+=p('Esta digitalização pertence à mesma peça documental de '+duplicate+'.')+a('acervo/documentos/'+duplicate.lower()+'/','Consultar a peça relacionada')
        if id in ['A09','A12']:
            body+=p('A edição é de 23–29/10/1999; a legenda menciona 23/10, enquanto a fotografia traz 24/10/98. O reaproveitamento da foto de 1998 é provável, mas não está demonstrado. Não identificamos esse registro como um 8º batizado confirmado.')+refs('A06')
        if id=='A01': body+=p('O cabeçalho informa fundação em 02/02/1990. Carlos Alberto da Silva aparece como presidente e organizador; Reginaldo Santana, diretor geral; Helena R. da Silva, secretária executiva. O corpo indica Jardim Morumbi, enquanto o carimbo usa Vila Municipal: as duas referências do documento foram preservadas.')
        if id=='A03': body+=p('A expressão Mestre Kauê já está impressa em outubro de 1997. Isso não estabelece a data em que recebeu a graduação.')
        if id=='A08': body+=p('O cartaz nomeia o grupo, mas não nomeia Kauê. A relação aqui documentada é com o batizado anunciado em Jundiaí.')
        body+='<dl class="record-meta"><dt>Arquivo recebido</dt><dd>'+e(file)+'</dd><dt>Procedência</dt><dd>'+e(provenance)+'</dd><dt>Acesso</dt><dd>Descrição da digitalização; sem URL pública do original.</dd><dt>Reprodução</dt><dd>Imagem não publicada: crédito e autorização ainda pendentes.</dd></dl>'
        if event: body+=a('historia/cronologia/#'+event,'Ver o marco na cronologia')
        if people: body+='<h3>Pessoas nomeadas no documento</h3><ul>'+''.join('<li>'+a('acervo/pessoas/#'+i,PEOPLE[i][2]+' · '+PEOPLE[i][1])+'</li>' for i in people)+'</ul>'
        body+=related('Jundiaí')+a('acervo/documentos/','Todos os documentos')
        write_page(path,title,'Uma leitura do acervo impresso de Jundiaí.',section('O que esta peça registra',body))
        kind='Duplicata / recorte' if duplicate else ('Contexto de imprensa' if id in ['A10','A11'] else 'Documento histórico')
        cards.append(record(id,a(path+'/',title),p(desc)+p(assessment),'Jundiaí',kind,date,desc+' '+assessment+' '+file+' '+id))
    write_page('acervo/documentos','Papéis que guardam a roda','12 digitalizações, correspondentes a 10 peças documentais. Convites, cartazes e jornais ajudam a contar a história de Jundiaí.',section('O acervo impresso',p('Os nomes dos arquivos foram preservados, mas a data impressa orienta a descrição. Convites comprovam a programação anunciada; presença, realização e arrecadação precisam de outros registros.')+catalog(cards,['Jundiaí'],['Documento histórico','Duplicata / recorte','Contexto de imprensa'])))

def people():
    cards=[]
    for r in ROWS['people']:
        id,name,nick,role,city,source=r
        if id=='P037': role+=' Em relato publicado em 30/11/2025, agradece aos mestres Zula e Kauê pela transmissão de conhecimentos; apresenta participação em projeto escolar e na Expo Internacional da Consciência Negra.'; source+=',S97'
        if id=='P038': role='Presente na equipe do Aroeira na consulta de 2026; pré-formatura noticiada em 2024 e crédito musical no catálogo do disco. O anúncio de maio de 2024 não fixa a data de graduação.'; source+=',S64,S102'
        if id=='P009': role+=' Uma publicação de janeiro de 2026 anuncia futura formatura; a realização não foi comprovada.'; source+=',S101'
        body=(p(name) if name not in ['NÃO CONFIRMADO',nick] else '')+p(role)+p(city)+refs(source)+related(nick+' '+city)
        if id=='P012': body+=a('cidades/sao-paulo/mestre-marcao/','Conheça o núcleo de Marcão')
        docids=[d for d,v in DOC_META.items() if id in v[2]]
        if docids: body+='<p>Nos documentos: '+ ' · '.join(a('acervo/documentos/'+d.lower()+'/',DOC_META[d][0]) for d in docids)+'</p>'
        cards.append(record(id,e(nick),body,city,'Pessoas e conjuntos','',name+' '+nick+' '+role+' '+city))
    write_page('acervo/pessoas','Pessoas que fazem a história','49 registros de pessoas ou conjuntos, com funções e títulos situados na época de cada fonte.',section('Vozes, ensino e convivência',p('Este índice não é uma diretoria nem uma árvore completa de formação. Relações de ensino, supervisão, parceria e participação são descritas separadamente.')+catalog(cards,[r[1] for r in ROWS['places'] if r[0]!='N13'])))

def videos():
    cards=[]
    for r in ROWS['videos']:
        id,title,kind,city,date,platform,url,who,duration,verification,source,use,rights=r
        # Generic fields added in the research workbook do not identify participants.
        if id=='V034': who='Responsáveis não individualizados na descrição consultada.'
        if id=='V039': who='Participantes não individualizados na fonte.'
        if id=='V044': who='Crédito de catálogo: Mestre Zula; não estabelece autoria de composição.'
        body=p(date)+p(verification)+external(url,'Abrir '+('canal' if kind=='Canal' else 'publicação original'))
        body+='<details><summary>Ficha e alcance da leitura</summary>'+p('Pessoas / identificação: '+who)+p('Duração: '+duration)+p(rights)+refs(source)+'</details>'+related(title+' '+city)
        cards.append(record(id,e(title),body,city,platform,date,title+' '+city+' '+who+' '+verification))
    block('audiovisual','videos',section('Explore os 44 registros',p('O catálogo inclui vídeos, um canal, páginas históricas e uma página de filme. Títulos e legendas foram examinados em graus diferentes; não se trata de 44 vídeos assistidos integralmente. Publicação e filmagem podem ter datas distintas.')+catalog(cards,['Jundiaí','São Paulo','Passos','Iguape','Registro','Cananeia','Minas Gerais'],['YouTube','Instagram','Página externa']),'catalogo'))

def media():
    cards=[]
    for r in ROWS['media']:
        id,desc,kind,city,date,themes,who,source,url,original,quality,inspection,origin,permission,credit,use,access=r
        body=p(date)+external(url,'Consultar na fonte')+'<details><summary>Crédito, procedência e leitura</summary>'+p(credit)+p(inspection)+p('Identificação na fonte: '+who)+p('Direitos: '+permission)+refs(source)+'</details>'+related(desc+' '+city)
        cards.append(record(id,e(desc),body,city,kind,date,desc+' '+city+' '+themes+' '+who))
    write_page('acervo/registros-visuais','Olhares sobre o Bonfim','127 registros visuais localizados: fotografias, carrosséis e publicações, com acesso às fontes.',section('Explore os registros',p('Uma entrada de carrossel pode conter várias imagens. As mídias continuam nos locais de publicação; autoria e acesso público não equivalem a autorização de reprodução neste site.')+catalog(cards,[r[1] for r in ROWS['places'] if r[0]!='N13'],[r[2] for r in ROWS['media']])) )

def results():
    cards=[]
    for r in ROWS['results']:
        id,competition,year,city,athlete,category,result,source,confidence=r
        body=p(competition+' · '+str(year))+p(category+' — '+result)+refs(source)+related(city)
        cards.append(record(id,e(athlete),body,city,'Resultados','',competition+' '+str(year)+' '+athlete+' '+city+' '+category))
    write_page('acervo/resultados','O esporte na memória','64 registros de colocações e resultados coletivos, preservando competição, categoria, cidade e fonte.',section('Cada resultado tem seu contexto',p('Este número não equivale a 64 medalhas ou títulos. Há quartos lugares e entradas coletivas. Os 30 resultados de 2008–2011 são declarações do grupo; a equipe municipal de 2013 e a relação oficial do Mineiro de 2022 têm fontes próprias.')+catalog(cards,[r[3] for r in ROWS['results']])) )

def sources():
    cards=[]
    for r in ROWS['sources']:
        id,title,author,published,access,url,use,limits=r
        body=p(author)+p('Publicação / atualização: '+published)+p('Acesso registrado na pesquisa: '+str(access))+p(use)+p('Alcance: '+clean(limits))
        if id=='S33': body+=p('A URL original retornou 404 na revisão. A referência histórica foi mantida para localização posterior; não há cópia pública neste site.')+'<details><summary>Endereço histórico indisponível</summary><code>'+e(url)+'</code></details>'
        else: body+=external(url,'Consultar fonte original')
        cards.append(record(id,e(title),body,'','Fonte pública','',id+' '+title+' '+author+' '+use))
    block('fontes','sources',section('120 fontes públicas',catalog(cards),'bibliografia'))
    oral=DATA['research']['oral_source']
    block('fontes','oral',section('A memória dos alunos',p(oral['account'])+p('Segundo relato de alunos, sem identificação nominal, encaminhado à pesquisa em setembro de 2026. A fonte testemunhal é preservada como parte da história. O vídeo institucional de 2018 documenta o intercâmbio entre as academias de Zula e Kauê; ele não substitui o relato sobre formação e locais distintos.')+p(oral['limits'])+refs('S110,S120')+'<p class="record-type">Referência de pesquisa: R01 · testemunhal · sem URL pública</p>','R01'))
    divs=[]
    for r in ROWS['divergences']:
        divs.append('<details id="'+r[0]+'"><summary>'+e(r[1])+'</summary>'+p(r[2])+p(r[3])+refs(r[4])+'</details>')
    block('fontes','divergences',section('Questões que continuam abertas',''.join(divs),'divergencias'))

def places():
    # Supplement the retained narrative instead of replacing correct histories.
    for r in ROWS['places']:
        id,city,state,country,responsible,status,basis,bond,confidence,history,location,contact,channels,source=r
        if id in ['N02','N03','N13','N21','N22','N23']: continue
        body=p(history)+p('Espaços registrados: '+location)+p('As referências acima pertencem à época das fontes e não constituem indicação de endereço atual de treino.')+refs(source)+related(city)
        body+='<nav class="related-links" aria-label="Explore esta localidade">'+a('historia/cronologia/?q='+quote(city),'Na cronologia')+a('acervo/pessoas/?q='+quote(city),'Pessoas relacionadas')+a('acervo/resultados/?q='+quote(city),'Resultados')+a('acervo/registros-visuais/?q='+quote(city),'Registros visuais')+'</nav>'
        block(place_path(r).rstrip('/'),'local-record',section('Memória dos espaços e do trabalho',body,'ficha'))
    district=next(r for r in ROWS['places'] if r[0]=='N13')
    write_page('cidades/jaboticabal/corrego-rico','Córrego Rico','Uma frente distrital de Jaboticabal, no mesmo município.',section('Oficinas e encontro de gerações',p(district[9])+p(district[10])+p('As oficinas são documentadas em julho de 2026. A notícia registra cerca de 150 participantes no batizado, sem confundir público do evento com alunos regulares.')+refs('S19')+a('cidades/jaboticabal/','Conheça Jaboticabal')),'cidades')
    block('cidades/jaboticabal','district',section('No distrito de Córrego Rico',a('cidades/jaboticabal/corrego-rico/','Conheça a frente distrital')))
    body=p('O inventário reúne 24 fichas: 20 municípios brasileiros com vínculos documentados, uma frente distrital de Jaboticabal e três localidades com indícios. A ficha de São Paulo abriga dois trabalhos distintos. Essa contagem não representa academias em funcionamento.')+a('cidades/jaboticabal/corrego-rico/','Frente distrital de Córrego Rico')
    for r in ROWS['places']:
        if r[0] in ['N21','N22','N23']: body+=record(r[0],e(r[1]),p(r[6])+p(r[9])+refs(r[13]),r[1],'Indício de núcleo')
    body+='<h3>Outras pistas territoriais</h3>'+p('Portugal e viagens a outros países não são tratados como filiais. Menções de convidados, locais de apresentações e nomes semelhantes também exigem confirmação individual.')
    for r in ROWS['leads']:
        body+='<details id="'+r[0]+'"><summary>'+e(r[1])+'</summary>'+p(r[2])+p(r[3])+'</details>'
    block('cidades','inventory',section('Além dos pontos do mapa',body,'em-investigacao'))

def instagram():
    cards=[]
    for r in ROWS['instagram']:
        id,url,items,scope,source=r
        cards.append(record(str(id),external(url,'Publicação '+str(id)),p('Itens relacionados: '+str(items))+p(scope)+refs(source),'Jundiaí','Índice de publicações','',str(items)+' '+str(id)))
    write_page('acervo/indice-instagram','Índice de publicações','122 entradas localizadas na pesquisa de Jundiaí, entre 2018 e 2026.',section('Caminhos para continuar a pesquisa',p('Este índice se sobrepõe parcialmente aos catálogos visual e audiovisual. Não certifica leitura integral de todos os vídeos, comentários ou imagens dos carrosséis.')+catalog(cards)))

class TextReader(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style']: self.skip+=1
    def handle_endtag(self,tag):
        if tag in ['script','style']: self.skip=max(0,self.skip-1)
    def handle_data(self,text):
        if not self.skip:self.parts.append(text)

class RecordReader(TextReader):
    """Index the final editorial text, including corrections absent from raw data."""
    def __init__(self):
        super().__init__(); self.records=[]; self.current=None; self.heading=False
    def handle_starttag(self,tag,attrs):
        super().handle_starttag(tag,attrs)
        attrs=dict(attrs)
        if tag=='article' and 'data-record' in attrs:
            self.current={'id':attrs['id'],'title':[],'text':[]}
        if tag=='h3' and self.current is not None:self.heading=True
    def handle_endtag(self,tag):
        super().handle_endtag(tag)
        if tag=='h3':self.heading=False
        if tag=='article' and self.current is not None:
            self.records.append(self.current);self.current=None
    def handle_data(self,text):
        super().handle_data(text)
        if self.current is not None and not self.skip:
            self.current['text'].append(text)
            if self.heading:self.current['title'].append(text)

def search():
    items=[]
    for f in sorted(ROOT.rglob('index.html')):
        route=f.parent.relative_to(ROOT).as_posix()
        if route in ['404','acervo/busca']: continue
        text=f.read_text(encoding='utf-8')
        title=re.search('<title>(.*?)</title>',text).group(1).split(' | ')[0]
        main=text.split('<main id="conteudo">')[1].split('</main>')[0]
        reader=RecordReader();reader.feed(main)
        url=BASE+('' if route=='.' else route+'/')
        items.append({'title':title,'url':url,'text':' '.join(reader.parts)})
        for record in reader.records:
            items.append({'title':' '.join(record['title']),'url':url+'#'+record['id'],'text':' '.join(record['text'])})
    # Keep each static search file small enough for individual content review.
    chunks=[]; chunk=[]; size=2
    for item in items:
        item_size=len(json.dumps(item,ensure_ascii=False).encode('utf-8'))+1
        if chunk and size+item_size>80000:chunks.append(chunk);chunk=[];size=2
        chunk.append(item);size+=item_size
    if chunk:chunks.append(chunk)
    files=[]
    for number,chunk in enumerate(chunks,1):
        name=f'search-part-{number:02}.json';files.append(name)
        (ROOT/'assets'/name).write_text(json.dumps(chunk,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    for stale in (ROOT/'assets').glob('search-part-*.json'):
        if stale.name not in files:stale.unlink()
    (ROOT/'assets/search-index.json').write_text(json.dumps({'files':files},ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
    write_page('acervo/busca','Encontre uma história','Pesquise nomes, lugares, documentos, eventos e vídeos do acervo.',section('O que você procura?','<form id="site-search" role="search"><label for="archive-query">Buscar em todo o acervo</label><div class="search-line"><input id="archive-query" name="q" type="search" placeholder="Experimente Zula ou Kauê" autocomplete="off"><button>Buscar</button></div></form><p id="search-status" role="status" aria-live="polite"></p><ol id="search-results" class="search-results"></ol><noscript>Use os índices de '+a('acervo/pessoas/','pessoas')+', '+a('historia/cronologia/','cronologia')+' e '+a('acervo/documentos/','documentos')+'. A busca geral precisa de JavaScript.</noscript>'))

def sitemap():
    paths=sorted(p.parent.relative_to(ROOT).as_posix() for p in ROOT.rglob('index.html') if p.parent.name!='404')
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+BASE+('' if x=='.' else x+'/')+'</loc></url>' for x in paths)+'</urlset>\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    timeline(); documents(); people(); videos(); media(); results(); sources(); places(); instagram(); search(); sitemap()
    print('Catálogos, relações, índice de busca e sitemap atualizados.')
