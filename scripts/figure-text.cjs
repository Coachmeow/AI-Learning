// List the English text inside the interactive figures of the given lessons, so it can be
// translated in src/data/figure-i18n.th.json. Needs the built site served at http://127.0.0.1:4321.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  const out = {};
  for (const key of process.argv.slice(2)) {
    await p.goto(`http://127.0.0.1:4321/en/${key}/`, { waitUntil: 'load' });
    await p.waitForTimeout(800);
    const grab = () => p.evaluate(() => {
      const seen = new Set();
      document.querySelectorAll('.lesson-figure').forEach((host) => {
        const w = document.createTreeWalker(host, NodeFilter.SHOW_TEXT);
        for (let n = w.nextNode(); n; n = w.nextNode()) {
          const t = (n.nodeValue || '').trim();
          if (t && /[A-Za-z]{2}/.test(t)) seen.add(t);
        }
        host.querySelectorAll('[aria-label],[title]').forEach((el) => {
          for (const a of ['aria-label', 'title']) {
            const v = el.getAttribute(a);
            if (v && /[A-Za-z]{2}/.test(v)) seen.add(v.trim());
          }
        });
      });
      return [...seen];
    });
    const first = await grab();
    const ctrls = await p.$$('.lesson-figure button, .lesson-figure [role=button]');
    for (const c of ctrls.slice(0, 12)) {
      try { await c.click({ timeout: 1000 }); await p.waitForTimeout(250); } catch { /* not clickable */ }
    }
    const after = await grab();
    out[key] = [...new Set([...first, ...after])];
  }
  console.log(JSON.stringify(out, null, 1));
  await b.close();
})();
