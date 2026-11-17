// Lesson page enhancements: interactive figures, Mermaid diagrams and "Run" buttons on Python code.
import { ensureReady, isLoaded, runCode } from './py-runner';
import figureTh from '../data/figure-i18n.th.json';

type Strings = Record<string, string>;
const content = document.querySelector<HTMLElement>('.sl-markdown-content');
const lang = document.documentElement.lang.startsWith('th') ? 'th' : 'en';
const ui: Strings = JSON.parse(document.getElementById('ail-ui')?.textContent || '{}');
const fmt = (s: string, vars: Record<string, string | number>) => s.replace(/\{(\w+)\}/g, (_, k) => String(vars[k] ?? ''));

/* ── Interactive figures ─────────────────────────────── */
function translateFigure(host: Element) {
  if (lang !== 'th') return;
  const exact = figureTh.exact as Strings;
  const patterns = (figureTh.patterns as [string, string][]).map(([re, to]) => [new RegExp(re), to] as const);
  const tr = (text: string) => {
    const t = text.trim();
    if (!t) return null;
    if (exact[t]) return text.replace(t, exact[t]);
    for (const [re, to] of patterns) if (re.test(t)) return text.replace(t, t.replace(re, to));
    return null;
  };
  const walker = document.createTreeWalker(host, NodeFilter.SHOW_TEXT);
  for (let n = walker.nextNode(); n; n = walker.nextNode()) {
    const next = tr(n.nodeValue || '');
    if (next !== null && next !== n.nodeValue) n.nodeValue = next;
  }
  host.querySelectorAll('[aria-label]').forEach((el) => {
    const next = tr(el.getAttribute('aria-label') || '');
    if (next !== null) el.setAttribute('aria-label', next);
  });
}

function mountFigures() {
  const w = window as any;
  if (!content || typeof w.mountLessonFigures !== 'function') return;
  w.mountLessonFigures(content);
  content.querySelectorAll('.lesson-figure').forEach((host) => {
    translateFigure(host);
    if (lang === 'th') {
      let busy = false;
      new MutationObserver(() => {
        if (busy) return;
        busy = true;
        translateFigure(host);
        busy = false;
      }).observe(host, { subtree: true, childList: true, characterData: true });
    }
  });
}

/* ── Mermaid ─────────────────────────────────────────── */
async function renderMermaid() {
  const nodes = [...document.querySelectorAll<HTMLElement>('pre.mermaid')];
  if (!nodes.length) return;
  const { default: mermaid } = await import('mermaid');
  const draw = async () => {
    const dark = document.documentElement.dataset.theme !== 'light';
    mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      theme: dark ? 'dark' : 'neutral',
      fontFamily: "'IBM Plex Sans Thai', system-ui, sans-serif",
    });
    for (const n of nodes) {
      n.removeAttribute('data-processed');
      n.textContent = n.dataset.src || '';
    }
    await mermaid.run({ nodes });
  };
  await draw();
  new MutationObserver(() => draw()).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
}

/* ── Run buttons ─────────────────────────────────────── */
const LOCAL_ONLY = /^\s*(?:import|from)\s+(torch|tensorflow|transformers|jax|sklearn|datasets|librosa|openai|anthropic|cv2|tiktoken)\b/m;
const ICON_PLAY = '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>';

type Block = { code: string; ran: boolean; out: HTMLPreElement; btn: HTMLButtonElement };

function setupRunButtons() {
  if (!content) return;
  const blocks: Block[] = [];
  content.querySelectorAll<HTMLElement>('.expressive-code').forEach((ec) => {
    const pre = ec.querySelector('pre[data-language="python"]');
    if (!pre) return;
    const lines = [...pre.querySelectorAll('.ec-line')].map((l) => l.textContent ?? '');
    const code = (lines.length ? lines : [pre.textContent ?? '']).join('\n');
    const box = document.createElement('div');
    box.className = 'ail-run not-content';
    const local = code.match(LOCAL_ONLY);
    if (local) {
      box.innerHTML = `<div class="ail-run-bar"><span class="ail-run-note">${fmt(ui.runNeedsLocal, { lib: local[1] })}</span></div>`;
      ec.after(box);
      return;
    }
    box.innerHTML = `<div class="ail-run-bar"><button type="button" class="ail-btn small primary">${ICON_PLAY}<span>${ui.run}</span></button><span class="ail-run-note">${ui.runNote}</span></div><pre class="ail-run-out" hidden></pre>`;
    ec.after(box);
    const block: Block = { code, ran: false, out: box.querySelector('pre')!, btn: box.querySelector('button')! };
    blocks.push(block);
    block.btn.addEventListener('click', () => runUpTo(blocks, blocks.indexOf(block)));
  });
}

let running = false;
async function runUpTo(blocks: Block[], index: number) {
  if (running) return;
  running = true;
  blocks.forEach((b) => (b.btn.disabled = true));
  const target = blocks[index];
  const label = target.btn.querySelector('span')!;
  try {
    if (!isLoaded()) {
      target.out.hidden = false;
      target.out.classList.remove('err');
      target.out.textContent = ui.loadingPython;
      const ready = await ensureReady();
      if (!ready.ok) {
        target.out.classList.add('err');
        target.out.textContent = ready.error || 'Python failed to load';
        return;
      }
    }
    // Notebook-style: earlier blocks on the page define what later ones use.
    for (let i = 0; i <= index; i++) {
      const b = blocks[i];
      if (b.ran && i !== index) continue;
      if (i === index) label.textContent = ui.running;
      const r = await runCode(b.code);
      b.out.hidden = false;
      b.out.classList.toggle('err', !r.ok);
      if (r.timedOut) {
        blocks.forEach((x) => (x.ran = false));
        b.out.textContent = fmt(ui.timeout, { s: 20 });
        break;
      }
      b.out.textContent = [r.out, r.error].filter(Boolean).join('\n') || ui.noOutput;
      if (!r.ok) break;
      b.ran = true;
      b.btn.querySelector('span')!.textContent = ui.runAgain;
    }
  } finally {
    if (!target.ran) label.textContent = ui.run;
    blocks.forEach((b) => (b.btn.disabled = false));
    running = false;
  }
}

mountFigures();
setupRunButtons();
renderMermaid();
