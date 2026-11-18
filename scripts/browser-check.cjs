// Browser check for Thai lesson pages (needs a built site served at http://127.0.0.1:4321,
// e.g. `npm run build && npm run preview -- --port 4321`, and Playwright with Chromium).
// For each lesson: banner, figures, Mermaid, every quiz level answered correctly, and every
// exercise solution checked in Pyodide. Usage: node scripts/browser-check.cjs <phase>/<lesson> ...
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = require('path').resolve(__dirname, '..');
const ORIGIN = process.env.ORIGIN || 'http://127.0.0.1:4321';
const BASE = process.env.BASE || '/';

(async () => {
  const b = await chromium.launch(process.env.HTTPS_PROXY && ORIGIN.startsWith('https') ? { proxy: { server: process.env.HTTPS_PROXY } } : {});
  for (const key of process.argv.slice(2)) {
    const ctx = await b.newContext();
    const p = await ctx.newPage();
    const errors = [];
    p.on('pageerror', (e) => errors.push(e.message));
    await p.goto(`${ORIGIN}${BASE}th/${key}/`, { waitUntil: 'load' });
    await p.waitForFunction(() => [...document.querySelectorAll('pre.mermaid')].every((m) => m.querySelector('svg')), null, { timeout: 30000 }).catch(() => {});
    const page = await p.evaluate(() => ({
      banner: document.querySelector('.ail-banner')?.textContent.trim().slice(0, 40),
      figures: `${[...document.querySelectorAll('.lesson-figure')].filter((f) => f.children.length).length}/${document.querySelectorAll('.lesson-figure').length}`,
      mermaid: `${document.querySelectorAll('pre.mermaid svg').length}/${document.querySelectorAll('pre.mermaid').length}`,
      english: [...document.querySelectorAll('.sl-markdown-content > p')].filter((x) => !/[฀-๿]/.test(x.textContent) && x.textContent.length > 80).length,
    }));

    // Quiz: answer each level correctly using the Thai text of the right option.
    const quiz = JSON.parse(fs.readFileSync(path.join(ROOT, 'src/data/quizzes', key + '.json'), 'utf8'));
    const quizRes = [];
    const root = p.locator('.ail-assess');
    for (const level of ['easy', 'medium', 'hard']) {
      await root.locator('.ail-tab[data-tab="quiz"]').click();
      await root.locator('.ail-pill').nth(['easy', 'medium', 'hard'].indexOf(level)).click();
      let score = 0;
      for (let i = 0; i < 5; i++) {
        const qText = (await root.locator('.ail-question').textContent()).trim();
        const q = quiz.questions.find((x) => x.difficulty === level && qText.startsWith(x.question.th.replace(/`/g, "").slice(0, 25)));
        if (!q) { quizRes.push(`${level}: question not found: ${qText.slice(0, 40)}`); break; }
        const right = q.options[q.answer].th;
        const opts = root.locator('.ail-opt');
        const n = await opts.count();
        for (let j = 0; j < n; j++) {
          const t = (await opts.nth(j).textContent()).trim();
          const norm = (x) => x.replace(/[`\s]/g, ""); if (norm(t.slice(1)) === norm(right)) { await opts.nth(j).click(); break; }
        }
        if (await root.locator('.ail-feedback .ail-ok').count()) score++;
        await root.locator('.ail-actions .ail-btn.primary').click();
      }
      quizRes.push(`${level} ${score}/5`);
    }

    // Exercises: paste the solution, check, expect every check to pass.
    const exRes = [];
    for (const level of ['easy', 'medium', 'hard']) {
      const dir = path.join(ROOT, 'src/data/exercises', key, level);
      if (!fs.existsSync(dir)) continue;
      await root.locator('.ail-tab[data-tab="code"]').click();
      await root.locator('.ail-pill').nth(['easy', 'medium', 'hard'].indexOf(level)).click();
      const editor = root.locator('.cm-content');
      await editor.waitFor({ timeout: 20000 });
      await editor.click();
      await p.keyboard.press('Control+A');
      await p.keyboard.press('Delete');
      await p.keyboard.insertText(fs.readFileSync(path.join(dir, 'solution.py'), 'utf8'));
      await root.locator('[data-panel="code"] .ail-actions .ail-btn.primary').click();
      await root.locator('.ail-results:not([hidden])').waitFor({ timeout: 120000 });
      await p.waitForFunction(() => !document.querySelector('.ail-spin'), null, { timeout: 120000 });
      const txt = (await root.locator('.ail-results').textContent()).trim();
      exRes.push(`${level}: ${(await root.locator('.ail-results .ail-ok').count()) ? 'PASS' : 'FAIL ' + txt.slice(0, 150)}`);
    }
    console.log(`${key}\n  page ${JSON.stringify(page)}\n  quiz ${quizRes.join(', ')}\n  code ${exRes.join(' | ')}\n  errors ${errors.length ? errors.slice(0, 3) : 0}`);
    await ctx.close();
  }
  await b.close();
})();
