'use strict';
function closeMenu(){menuButton?.setAttribute('aria-expanded','false');nav?.classList.remove('open');}
nav?.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
document.addEventListener('click',event=>{if(!event.target.closest('.site-header'))closeMenu();});
const normalize=text=>text.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR');
document.querySelectorAll('.filter-scope').forEach(scope=>{
 const form=scope.querySelector('.filter-bar');if(!form)return;
 const items=[...scope.querySelectorAll('.filter-item')];
 const count=scope.querySelector('.result-count');const empty=scope.querySelector('.empty-state');
 function filter(){
  const query=normalize(form.elements.q.value.trim());const city=normalize(form.elements.city.value);const theme=form.elements.theme?.value||'';
  let visible=0;
  items.forEach(item=>{const match=normalize(item.dataset.search).includes(query)&&normalize(item.dataset.city).includes(city)&&(!theme||item.dataset.theme.split('|').includes(theme));item.hidden=!match;if(match)visible++;});
  count.textContent=`${visible} de ${items.length} registros`;empty.hidden=visible>0;
 }
 form.addEventListener('submit',event=>event.preventDefault());form.addEventListener('input',filter);form.addEventListener('change',filter);
 form.addEventListener('reset',event=>{event.preventDefault();form.elements.q.value='';form.elements.city.value='';if(form.elements.theme)form.elements.theme.value='';filter();});
 document.querySelectorAll('[data-state]').forEach(anchor=>anchor.addEventListener('click',()=>{form.elements.q.value='';form.elements.city.value=anchor.dataset.state;filter();}));
 filter();
});
if(!document.querySelector('.city-grid'))document.querySelectorAll('[data-state]').forEach(anchor=>{anchor.setAttribute('href',`/bonfim-capoeira-acervo/bonfim-capoeira-acervo/cidades/?estado=${anchor.dataset.state}#lista-cidades`);});
const initialState=new URLSearchParams(location.search).get('estado');
if(['MG','SP','PR'].includes(initialState)){const select=document.querySelector('.city-grid')?.closest('.filter-scope').querySelector('select[name="city"]');if(select){select.value=initialState;select.dispatchEvent(new Event('change',{bubbles:true}));}}
const dialog=document.querySelector('#lightbox');
let photos=[],photoIndex=0,lastPhoto;
function showPhoto(index){
 photoIndex=(index+photos.length)%photos.length;const anchor=photos[photoIndex];
 const photo=new Image();photo.src=anchor.href;photo.alt=anchor.dataset.title;
 dialog.querySelector('.lightbox-image').replaceChildren(photo);
 dialog.querySelector('#lightbox-title').textContent=anchor.dataset.title;
 dialog.querySelector('#lightbox-meta').textContent=anchor.dataset.meta;
 dialog.querySelector('#lightbox-credit').textContent=anchor.dataset.credit;
 dialog.querySelector('#lightbox-source').href=anchor.dataset.source;
 dialog.querySelector('#lightbox-count').textContent=`${photoIndex+1} / ${photos.length}`;
 dialog.querySelectorAll('[data-photo-step]').forEach(button=>button.disabled=photos.length<2);
}
document.querySelectorAll('.photo-open').forEach(anchor=>anchor.addEventListener('click',event=>{
 if(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||!dialog?.showModal)return;
 event.preventDefault();photos=[...document.querySelectorAll('.photo-open')].filter(a=>!a.closest('[hidden]'));lastPhoto=anchor;
 showPhoto(photos.indexOf(anchor));dialog.showModal();document.body.classList.add('no-scroll');dialog.querySelector('.close-dialog').focus();
}));
dialog?.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());
dialog?.addEventListener('close',()=>{document.body.classList.remove('no-scroll');lastPhoto?.focus();});
dialog?.addEventListener('click',event=>{if(event.target===dialog){const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();}});
dialog?.querySelectorAll('[data-photo-step]').forEach(button=>button.addEventListener('click',()=>showPhoto(photoIndex+Number(button.dataset.photoStep))));
dialog?.addEventListener('keydown',event=>{if(event.key==='ArrowRight'){event.preventDefault();showPhoto(photoIndex+1);}if(event.key==='ArrowLeft'){event.preventDefault();showPhoto(photoIndex-1);}});
document.querySelectorAll('button.video-load[data-video]').forEach(button=>button.addEventListener('click',()=>{
 const iframe=document.createElement('iframe');iframe.src=`https://www.youtube-nocookie.com/embed/${button.dataset.video}?autoplay=1`;
 iframe.title=button.dataset.title;iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';
 button.parentElement.replaceChildren(iframe);iframe.focus();
}));
