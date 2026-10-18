/* Shared by both sites. No requests, tracking, storage, or localhost probing. */
(() => {
  'use strict';
  const start = () => {
    if (window.top !== window.self || document.getElementById('psych-author-entry')) return;
    const meta = name => document.querySelector(`meta[name="psych-author-${name}"]`)?.content || '';
    const project = meta('project'), page = meta('page'), build = meta('build');
    if (!['handbook', 'guide'].includes(project) || !page.endsWith('.html')) return;
    const norm = text => text.replace(/\s+/g, ' ').trim();
    const node = (tag, text, cls = '') => { const e = document.createElement(tag); e.textContent = text; e.className = cls; return e; };
    const point = () => {
      const main = document.querySelector('main');
      const heads = [...(main?.querySelectorAll('h1[id],h2[id],h3[id],section[id]') || [])];
      const anchor = heads.filter(h => h.getBoundingClientRect().top <= 140).pop()?.id || '';
      const paragraphs = [...(main?.querySelectorAll('p,li') || [])].filter(p => !p.querySelector('p,li') && p.getBoundingClientRect().bottom > 140 && norm(p.textContent).length > 10);
      const quote = paragraphs.find(p => p.getBoundingClientRect().top < innerHeight)?.textContent || '';
      return {anchor, quote: norm(quote).slice(0, 120)};
    };
    const dock = node('div', '', 'psych-author-entry'); dock.id = 'psych-author-entry';
    const launch = node('a', '✎ 作者模式'); launch.href = '#'; launch.title = '在本机工作台打开当前章节和阅读位置';
    const help = node('button', '?'); help.type = 'button'; help.setAttribute('aria-label', '作者模式使用帮助');
    dock.append(launch, help); document.body.append(dock);
    const dialog = node('dialog', '', 'psych-author-help'); dialog.setAttribute('aria-labelledby', 'psych-author-help-title');
    const title = node('h2', '在本机继续编辑'); title.id = 'psych-author-help-title';
    const intro = node('p', '已安装工作台时，浏览器会询问是否打开应用。允许后，就会进入这一章的当前位置。');
    const hint = node('p', '没有打开？可以从桌面启动“心理学 AI 手册·作者工作台”，点击“从页面地址打开”，粘贴下面的地址。');
    const address = node('input'); address.readOnly = true; address.setAttribute('aria-label', '当前章节与位置地址');
    const copy = node('button', '复制当前位置'); copy.type = 'button';
    const retry = node('a', '打开工作台'); retry.className = 'psych-author-retry';
    const close = node('button', '继续阅读'); close.type = 'button';
    const status = node('p', '', 'psych-author-status'); status.setAttribute('role', 'status');
    const install = node('p', '这个入口供已在 Windows 电脑上安装工作台的作者使用。修改和批注先保存在那台电脑，下一轮更新再整合。');
    const instructions = node('a', '查看安装与使用说明'); instructions.href = 'https://github.com/How-Tze/psych-ai-research-handbook/tree/main/tools/author-workbench'; instructions.target = '_blank'; instructions.rel = 'noopener noreferrer';
    const buttons = node('div', '', 'psych-author-buttons'); buttons.append(retry, copy, close);
    dialog.append(title, intro, hint, address, buttons, status, install, instructions); document.body.append(dialog);
    const prepare = () => {
      const position = point();
      const uri = 'psychauthor://open?' + new URLSearchParams({project, page, build, ...position});
      launch.href = uri; retry.href = uri;
      const publicUrl = new URL(location.href); publicUrl.search = ''; publicUrl.hash = position.anchor;
      publicUrl.searchParams.set('aw-build', build);
      if (position.quote) publicUrl.searchParams.set('aw-quote', position.quote);
      address.value = publicUrl.href;
      status.textContent = '';
    };
    launch.addEventListener('click', () => { prepare(); dialog.showModal(); });
    help.addEventListener('click', () => { prepare(); dialog.showModal(); });
    close.addEventListener('click', () => dialog.close());
    copy.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(address.value); status.textContent = '已复制。在工作台中粘贴即可。'; }
      catch { address.focus(); address.select(); status.textContent = '请复制已选中的地址。'; }
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
