const themeButton = document.querySelector('#theme');
function setTheme(dark) {
  document.body.classList.toggle('dark', dark);
  document.querySelectorAll('[data-dark-logo]').forEach(source => {
    source.media = dark ? 'screen' : 'not all';
  });
  themeButton.setAttribute('aria-label', dark ? '밝은 테마로 전환' : '어두운 테마로 전환');
  themeButton.setAttribute('aria-pressed', String(dark));
}
let savedTheme;
try { savedTheme = localStorage.getItem('portfolio-theme'); } catch {}
setTheme(savedTheme === 'dark');
themeButton.addEventListener('click', () => {
  const dark = !document.body.classList.contains('dark');
  setTheme(dark);
  try { localStorage.setItem('portfolio-theme', dark ? 'dark' : 'light'); } catch {}
});
const links = [...document.querySelectorAll('nav a')];
const observer = new IntersectionObserver(entries => {
  for (const entry of entries) {
    if (entry.isIntersecting) {
      links.forEach(link => {
        const active = link.hash === '#' + entry.target.id;
        link.classList.toggle('active', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
  }
}, { rootMargin: '-15% 0px -60% 0px' });
document.querySelectorAll('main section[id]').forEach(section => observer.observe(section));

const viewer = document.querySelector('#image-viewer');
const viewerImage = document.querySelector('#viewer-image');
document.querySelectorAll('[data-full-image]').forEach(button => {
  button.addEventListener('click', () => {
    viewerImage.src = button.dataset.fullImage;
    viewerImage.alt = button.dataset.caption;
    document.querySelector('#image-caption').textContent = button.dataset.caption;
    viewer.showModal();
    document.body.classList.add('image-viewer-open');
  });
});
document.querySelector('#close-viewer').addEventListener('click', () => viewer.close());
viewer.addEventListener('click', event => {
  const bounds = viewer.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom) viewer.close();
});
viewer.addEventListener('close', () => document.body.classList.remove('image-viewer-open'));

const printButton = document.querySelector('#print-portfolio');
printButton.addEventListener('click', async () => {
  printButton.disabled = true;
  const status = document.querySelector('#print-status');
  status.textContent = '이미지를 준비하고 있습니다…';
  try {
    if (viewer.open) viewer.close();
    document.querySelectorAll('img[loading="lazy"]').forEach(img => { img.loading = 'eager'; });
    await Promise.all([...document.querySelectorAll('main img')].map(img => img.decode().catch(() => {})));
    if (document.fonts) await document.fonts.ready;
    status.textContent = '인쇄 창에서 PDF로 저장을 선택하세요.';
    window.print();
  } finally {
    printButton.disabled = false;
  }
});
