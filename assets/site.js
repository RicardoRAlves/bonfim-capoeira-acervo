'use strict';
const siteScript=[...document.scripts].find(script=>script.src.includes('/assets/site.js'));
const officialLogoUrl=siteScript?new URL('logo-bonfim.jpeg',siteScript.src).href:'/assets/logo-bonfim.jpeg';
const legacyBrandMark=document.querySelector('.brand-mark');
if(legacyBrandMark){
 const officialLogo=document.createElement('img');
 officialLogo.className='brand-logo';
 officialLogo.src=officialLogoUrl;
 officialLogo.alt='';
 officialLogo.width=56;
 officialLogo.height=56;
 legacyBrandMark.replaceWith(officialLogo);
}
document.querySelectorAll('link[rel~="icon"]').forEach(icon=>{icon.href=officialLogoUrl;icon.type='image/jpeg'});
const legacyLocation='Local não identificado';
const otherLocation='Outros';
const citySelect=document.querySelector('select[name="city"]');
const legacyLocationOption=citySelect?[...citySelect.options].find(option=>option.value===legacyLocation):null;
if(legacyLocationOption){
 legacyLocationOption.value=otherLocation;
 legacyLocationOption.textContent=otherLocation;
 citySelect.append(legacyLocationOption);
 document.querySelectorAll(`[data-city="${legacyLocation}"]`).forEach(item=>{
  item.dataset.city=otherLocation;
  if(item.dataset.search)item.dataset.search=item.dataset.search.replace(legacyLocation,otherLocation);
  item.querySelectorAll('[data-meta]').forEach(meta=>meta.dataset.meta=meta.dataset.meta.replace(legacyLocation,otherLocation));
  item.querySelectorAll('.tag').forEach(tag=>tag.textContent=tag.textContent.replace(legacyLocation,otherLocation));
 });
}
const menuButton=document.querySelector('.menu-toggle');
const nav=document.querySelector('#main-nav');
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('open')){nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.focus()}});
