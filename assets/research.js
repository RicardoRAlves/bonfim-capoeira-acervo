'use strict';
(() => {
 const fold = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('pt-BR');
 const params = new URLSearchParams(location.search);
 document.querySelectorAll('[data-catalog]').forEach(scope => {
  const form = scope.querySelector('form');
  const records = [...scope.querySelectorAll('[data-record]')];
  const count = scope.querySelector('.catalog-count');
  const empty = scope.querySelector('.catalog-empty');
  if (params.has('q')) form.elements.q.value = params.get('q');
  function apply() {
   const terms = fold(form.elements.q.value.trim()).split(/\s+/).filter(Boolean);
   const city = fold(form.elements.city?.value);
   const kind = form.elements.kind?.value || '';
   const decade = form.elements.decade?.value || '';
   let visible = 0;
   records.forEach(row => {
    const searchable = fold(row.dataset.search + ' ' + row.textContent);
    const years = (row.dataset.date || '').match(/(?:19|20)\d{2}/g) || [];
    const match = terms.every(t => searchable.includes(t)) && (!city || fold(row.dataset.city).includes(city)) && (!kind || row.dataset.kind === kind) && (!decade || years.some(y => Math.floor(Number(y)/10)*10 === Number(decade)));
    row.hidden = !match;
    if (match) visible++;
   });
   count.textContent = `${visible} de ${records.length} registros`;
   empty.hidden = visible > 0;
  }
  form.addEventListener('submit', event => {event.preventDefault(); apply();});
  form.addEventListener('input', apply);
  form.addEventListener('change', apply);
  form.addEventListener('reset', event => {
   event.preventDefault();
   [...form.elements].forEach(field => {if (field.matches('input,select')) field.value = '';});
   apply();
  });
  apply();
  const anchor = decodeURIComponent(location.hash.slice(1));
  const target = anchor && document.getElementById(anchor);
  if (target && scope.contains(target) && target.hidden) {
   [...form.elements].forEach(field => {if (field.matches('input,select')) field.value = '';});
   apply();
  }
 });
 const searchForm = document.querySelector('#site-search');
 if (!searchForm) return;
 const input = searchForm.elements.q;
 const status = document.querySelector('#search-status');
 const results = document.querySelector('#search-results');
 let indexPromise;
 let request = 0;
 const script = [...document.scripts].find(s => s.src && new URL(s.src).pathname.endsWith('/research.js'));
 async function search(event) {
  event?.preventDefault();
  const current = ++request;
  const q = input.value.trim();
  const url = new URL(location.href);
  if(q) url.searchParams.set('q', q); else url.searchParams.delete('q');
  history.replaceState(null, '', url);
  results.replaceChildren();
  if (!q) {status.textContent='Digite um nome, lugar ou assunto para começar.'; return;}
  status.textContent='Buscando no acervo…';
  try {
   indexPromise ||= fetch(new URL('search-index.json', script.src), {cache:'no-cache'}).then(response => {
    if (!response.ok) throw new Error('Index unavailable');
    return response.json();
   }).then(async manifest => {
    const parts=await Promise.all(manifest.files.map(name => fetch(new URL(name,script.src),{cache:'no-cache'}).then(response=>{
     if(!response.ok) throw new Error('Search part unavailable');
     return response.json();
    })));
    return parts.flat();
   });
   const index = await indexPromise;
   if(current !== request) return;
   const terms = fold(q).split(/\s+/).filter(Boolean);
   const matches = index.filter(row => terms.every(term => fold(row.title+' '+row.text).includes(term)));
   matches.sort((a,b) => Number(fold(b.title).includes(fold(q))) - Number(fold(a.title).includes(fold(q))));
   const unique = [...new Map(matches.map(row => [row.url,row])).values()];
   status.textContent = `${unique.length} resultados para “${q}”.`;
   if(!unique.length) status.textContent+=' Experimente outro termo, como Jundiaí, Zula ou batizado.';
   unique.slice(0,100).forEach(row => {
    const li=document.createElement('li'); const link=document.createElement('a'); const text=document.createElement('p');
    link.href=row.url; link.textContent=row.title;
    const offset=Math.max(0,fold(row.text).indexOf(terms[0])-70);
    text.textContent=(offset ? '…' : '')+row.text.slice(offset,offset+230)+'…';
    li.append(link,text);results.append(li);
   });
   if(unique.length>100) status.textContent+=' Mostrando os primeiros 100; acrescente termos para refinar.';
  } catch(error) {
   indexPromise=undefined;
   if(current===request) status.textContent='Não foi possível carregar a busca. Tente novamente ou use os índices do Acervo.';
  }
 }
 input.value=params.get('q') || '';
 searchForm.addEventListener('submit', search);
 search();
})();
