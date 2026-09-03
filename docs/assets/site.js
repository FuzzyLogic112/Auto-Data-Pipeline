/* Claude 红皮书 — 阅读进度、目录高亮、回到顶部 */
(() => {
  const progress = document.querySelector('.progress span');
  const backTop = document.querySelector('[data-back-top]');
  const tocPanel = document.querySelector('.toc-panel');
  const tocLinks = Array.from(document.querySelectorAll('.toc-link'));

  const idOf = (link) => decodeURIComponent(link.hash.slice(1));
  // 目录项和正文标题一一对应；找不到对应标题的条目直接丢掉
  const entries = tocLinks
    .map((link) => ({ link, heading: document.getElementById(idOf(link)) }))
    .filter((e) => e.heading);

  /* ---------- 窄屏折叠目录 ---------- */
  // HTML 里目录默认 open，所以没有 JS 也能读到。窄屏上把它折起来，
  // 免得几十条目录把正文顶到一屏之外。
  const BREAKPOINT = 980;
  let wasNarrow = null;
  function syncTocOpen() {
    if (!tocPanel) return;
    const narrow = window.innerWidth <= BREAKPOINT;
    if (narrow === wasNarrow) return; // 断点没跨过去，别覆盖用户自己的展开/收起
    wasNarrow = narrow;
    tocPanel.open = !narrow;
  }

  /* ---------- 当前章节 ---------- */
  let current = null;

  function activeIndex() {
    // 视口上方 1/4 处作为判定线：取最后一个已经越过这条线的标题。
    // 比 IntersectionObserver 的窄带可靠——直接跳转、带 hash 打开、
    // 滚到页面底部这几种情况都能正确高亮。
    const line = window.innerHeight * 0.25;
    let index = -1;
    for (let i = 0; i < entries.length; i += 1) {
      if (entries[i].heading.getBoundingClientRect().top <= line) index = i;
      else break;
    }
    // 滚到底了就把最后一条点亮，否则末尾几节永远高亮不到
    const atBottom =
      window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
    return atBottom ? entries.length - 1 : index;
  }

  function syncActive() {
    if (!entries.length) return;
    const index = activeIndex();
    const next = index >= 0 ? entries[index].link : null;
    if (next === current) return;
    if (current) current.classList.remove('is-active');
    current = next;
    if (!current) return;
    current.classList.add('is-active');

    // 侧边栏是可滚动的粘性列时，把当前条目带进视野
    if (tocPanel && tocPanel.scrollHeight > tocPanel.clientHeight) {
      const panelBox = tocPanel.getBoundingClientRect();
      const linkBox = current.getBoundingClientRect();
      if (linkBox.top < panelBox.top || linkBox.bottom > panelBox.bottom) {
        tocPanel.scrollTop += linkBox.top - panelBox.top - tocPanel.clientHeight / 3;
      }
    }
  }

  /* ---------- 进度条 / 回到顶部 ---------- */
  function syncProgress() {
    const top = window.scrollY || document.documentElement.scrollTop;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = `${(max > 0 ? Math.min(top / max, 1) : 0) * 100}%`;
    if (backTop) backTop.classList.toggle('is-visible', top > 600);
  }

  let ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      syncProgress();
      syncActive();
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', () => {
    syncTocOpen();
    onScroll();
  });
  if (tocPanel) tocPanel.addEventListener('toggle', syncActive);

  if (backTop) {
    backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  syncTocOpen();
  syncProgress();
  syncActive();
})();
