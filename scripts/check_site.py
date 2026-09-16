"""Verificações estáticas de navegação, catálogos, acessibilidade básica e direitos."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
BASE='/bonfim-capoeira-acervo/'
errors=[]; pages={}; incoming={}; external=set()
NAV=['História','Mestre Régis','Jundiaí','Cidades','Acervo','Musicalidade','Vídeos','Comunidade']

class Page(HTMLParser):
    def __init__(self,path):
        super().__init__();self.path=path;self.ids=set();self.links=[];self.h1=0;self.nav=False;self.nav_text=[];self.in_nav_link=False;self.images=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if d.get('id'):
            if d['id'] in self.ids:errors.append(f'{self.path}: duplicate id {d["id"]}')
            self.ids.add(d['id'])
        if tag=='h1':self.h1+=1
        if tag=='nav' and d.get('id')=='main-nav':self.nav=True
        if tag=='a' and self.nav:self.in_nav_link=True
        if tag=='img':
            self.images+=1
            if 'alt' not in d:errors.append(f'{self.path}: image without alt')
            if re.search(r'/(?:M\d+|S26-|S76-|album.jpg)',d.get('src','')):errors.append(f'{self.path}: reproduction awaiting permission')
        for key in ['href','src']:
            if key in d:self.links.append(d[key])
        if 'srcset' in d:self.links.extend(x.strip().split()[0] for x in d['srcset'].split(','))
        if tag=='iframe' and not d.get('title'):errors.append(f'{self.path}: iframe without title')
    def handle_endtag(self,tag):
        if tag=='nav':self.nav=False
        if tag=='a':self.in_nav_link=False
    def handle_data(self,text):
        if self.nav and self.in_nav_link and text.strip():self.nav_text.append(text.strip())

for f in ROOT.rglob('*.html'):
    relative=f.relative_to(ROOT).as_posix();page=Page(relative);page.feed(f.read_text(encoding='utf-8'));pages[relative]=page
    if page.h1!=1:errors.append(f'{relative}: expected one h1, got {page.h1}')
    if page.nav_text!=NAV:errors.append(f'{relative}: navigation changed: {page.nav_text}')
    text=f.read_text(encoding='utf-8')
    if 'assets/research.js' not in text:errors.append(f'{relative}: missing research.js')
    if 'lang="pt-BR"' not in text:errors.append(f'{relative}: missing language')
for name,page in pages.items():
    for link in page.links:
        u=urlsplit(link)
        if u.scheme in ['http','https']:
            if '/p//' in link:errors.append(f'{name}: empty Instagram identifier: {link}')
            external.add(link);continue
        if u.scheme:continue
        if not u.path:target=ROOT/name
        elif u.path.startswith(BASE):target=ROOT/unquote(u.path[len(BASE):])
        elif u.path.startswith('/'):errors.append(f'{name}: URL outside Pages base: {link}');continue
        else:target=(ROOT/name).parent/unquote(u.path)
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{name}: missing {link}');continue
        relative=target.relative_to(ROOT).as_posix()
        if relative in pages:
            if relative!=name:incoming.setdefault(relative,set()).add(name)
            if u.fragment and unquote(u.fragment) not in pages[relative].ids:errors.append(f'{name}: missing anchor {link}')
for name in pages:
    if name not in ['index.html','404.html','404/index.html'] and not incoming.get(name):errors.append(f'Orphan: {name}')
expected={'places':24,'sources':120,'timeline':86,'people':49,'results':64,'media':127,'videos':44,'music':14,'instagram':122,'leads':22,'divergences':21,'documents':12}
for name,count in expected.items():
    data=json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))['rows']
    if len(data)!=count:errors.append(f'{name}: count {len(data)} != {count}')
    ids=[r[0] for r in data]
    if len(ids)!=len(set(ids)):errors.append(f'{name}: duplicate IDs')
docs=json.loads((ROOT/'data/documents.json').read_text(encoding='utf-8'))['rows']
if sum(not r[6] for r in docs)!=10:errors.append('Expected 10 unique documentary pieces')
for name,path in [('timeline','historia/cronologia/index.html'),('people','acervo/pessoas/index.html'),('videos','audiovisual/index.html'),('media','acervo/registros-visuais/index.html'),('results','acervo/resultados/index.html'),('sources','fontes/index.html')]:
    for row in json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))['rows']:
        if row[0] not in pages[path].ids:errors.append(f'{path}: record missing {row[0]}')
for path in ROOT.rglob('*'):
    if path.suffix in ['.mp3','.mp4','.wav']:errors.append(f'Rehosted audiovisual: {path}')
    if path.parent.name=='assets' and re.match(r'(?:M\d+.*\.webp|S26-.*\.webp|S76-.*\.webp|album\.jpg)$',path.name):errors.append(f'Pending reproduction included in deployment: {path.name}')
manifest=json.loads((ROOT/'assets/search-index.json').read_text(encoding='utf-8'))
index=[]
for name in manifest['files']:
    index.extend(json.loads((ROOT/'assets'/name).read_text(encoding='utf-8')))
by_url={r['url']:r for r in index}
kaue_start=by_url.get(BASE+'historia/cronologia/#T006',{})
if 'não confirmados' not in kaue_start.get('text',''):errors.append('Search loses caveat on Kauê starting date')
song=by_url.get(BASE+'audiovisual/#V044',{})
if 'Crédito de catálogo: Mestre Zula' not in song.get('text',''):errors.append('Search loses corrected musical identification')
for route in ['cidades/sao-paulo/aroeira/index.html','cidades/sao-paulo/mestre-marcao/index.html']:
    if 'fontes/#R01' not in (ROOT/route).read_text(encoding='utf-8'):errors.append(f'{route}: missing oral-source provenance')
report={'html_files':len(pages),'external_urls':len(external),'catalog_counts':expected,'errors':errors}
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(errors))
