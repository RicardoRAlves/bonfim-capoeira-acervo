'use strict';
const menuButton=document.querySelector('.menu-toggle');
const nav=document.querySelector('#main-nav');
menuButton?.addEventListener('click',()=>{const open=menuButton.getAttribute('aria-expanded')!=='true';menuButton.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('open')){nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.focus()}});
