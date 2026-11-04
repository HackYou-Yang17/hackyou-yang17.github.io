// Phone menu: the ☰ button opens and closes the nav list
const burger=document.querySelector('.burger'),menu=document.querySelector('.nav ul');
if(burger)burger.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
// Footer year updates itself
document.querySelectorAll('.year').forEach(e=>e.textContent=new Date().getFullYear());
// Lightbox: any image with data-zoom opens full size when clicked
const box=document.createElement('div');box.className='lightbox';box.innerHTML='<img alt="">';document.body.appendChild(box);
document.querySelectorAll('img[data-zoom]').forEach(img=>img.addEventListener('click',()=>{box.firstChild.src=img.src;box.firstChild.alt=img.alt;box.classList.add('open')}));
box.addEventListener('click',()=>box.classList.remove('open'));
document.addEventListener('keydown',e=>{if(e.key==='Escape')box.classList.remove('open')});
// Opening a link like cooking.html#recipe-2 also opens that recipe
function openHash(){const d=location.hash&&document.querySelector(location.hash);if(d&&d.tagName==='DETAILS')d.open=true}
openHash();window.addEventListener('hashchange',openHash);
// Sliders: arrows move one image, the counter follows scrolling and swiping
document.querySelectorAll('[data-slider]').forEach(sl=>{const tr=sl.querySelector('.slides'),n=tr.children.length,ct=sl.querySelector('.slider-count'),[pv,nx]=sl.querySelectorAll('[data-step]');
const at=()=>Math.round(tr.scrollLeft/(tr.clientWidth+16)),upd=()=>{const i=at();ct.textContent=(i+1)+' / '+n;pv.disabled=i===0;nx.disabled=i===n-1};
sl.querySelectorAll('[data-step]').forEach(b=>b.addEventListener('click',()=>tr.scrollTo({left:(at()+ +b.dataset.step)*(tr.clientWidth+16)})));tr.addEventListener('scroll',upd);upd()});