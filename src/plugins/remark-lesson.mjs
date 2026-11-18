// Turns the special fenced blocks used by the upstream lessons into HTML:
//   ```math      -> KaTeX (rendered at build time, no client JS needed)
//   ```figure    -> <div class="lesson-figure" data-figure="..."> hydrated by lesson-figures.js
//   ```mermaid   -> <pre class="mermaid"> rendered in the browser by the bundled Mermaid
// Inline $...$ and $$...$$ math (parsed by remark-math) is rendered with KaTeX too.
//
// It also rewrites relative links and images, which upstream writes relative to
// phases/<phase>/<lesson>/docs/en.md, so the Markdown files can stay untouched:
//   ../assets/x.svg                    -> <base>lesson-files/<phase>/<lesson>/assets/x.svg
//   ../../../<phase>/<lesson>/docs/en.md -> <base><lang>/<phase>/<lesson>/
//   anything else inside the repo        -> the file on GitHub at the imported commit
import path from 'node:path';
import katex from 'katex';
import { visit } from 'unist-util-visit';

const UPSTREAM = 'https://github.com/rohitg00/ai-engineering-from-scratch/blob';

// Real HTML tags lessons may use. Anything else that looks like a tag (upstream prose has
// "<image A>", "<box>", "<person>", "<doc>") is shown as text instead of becoming markup.
const HTML_TAGS = new Set(
  ('a abbr b bdi bdo blockquote br caption cite code col colgroup dd del details dfn div dl dt em figcaption figure ' +
    'h1 h2 h3 h4 h5 h6 hr i img ins kbd li mark ol p picture pre q s samp section small source span strong sub summary ' +
    'sup svg table tbody td tfoot th thead time tr u ul var video audio track iframe center font').split(' '),
);

const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function renderMath(tex, displayMode) {
  return katex.renderToString(tex, { displayMode, throwOnError: false, strict: 'ignore', output: 'html' });
}

// src/content/docs/<lang>/<phase>/<lesson>.md -> { lang, phase, lesson }
function lessonOf(file) {
  const m = (file || '').replace(/\\/g, '/').match(/content\/docs\/(en|th)\/(\d\d-[^/]+)\/(\d\d-[^/]+)\.mdx?$/);
  return m ? { lang: m[1], phase: m[2], lesson: m[3] } : null;
}

function rewrite(url, ctx, { base, commit }) {
  if (!url || /^(?:[a-z][a-z0-9+.-]*:|#|\/)/i.test(url)) return url; // absolute, anchor or site-rooted
  const [pathPart, hash = ''] = url.split('#');
  const from = `phases/${ctx.phase}/${ctx.lesson}/docs`;
  const target = path.posix.normalize(path.posix.join(from, pathPart));
  const anchor = hash ? `#${hash}` : '';
  let m = target.match(/^phases\/(\d\d-[^/]+)\/(\d\d-[^/]+)\/?(?:docs\/en\.md)?$/);
  if (m) return `${base}${ctx.lang}/${m[1]}/${m[2]}/${anchor}`;
  m = target.match(/^phases\/(\d\d-[^/]+)\/(\d\d-[^/]+)\/(assets|code|outputs)\/(.+)$/);
  if (m) return `${base}lesson-files/${m[1]}/${m[2]}/${m[3]}/${m[4]}${anchor}`;
  if (!target.startsWith('..')) return `${UPSTREAM}/${commit || 'main'}/${target}${anchor}`;
  return url;
}

export default function remarkLesson(options = {}) {
  const base = (options.base || '/').replace(/\/?$/, '/');
  return (tree, file) => {
    const ctx = lessonOf(file?.path || file?.history?.[0]);
    const commit = file?.data?.astro?.frontmatter?.upstream_commit;
    visit(tree, (node, index, parent) => {
      if (ctx && (node.type === 'image' || node.type === 'link')) {
        node.url = rewrite(node.url, ctx, { base, commit });
        return;
      }
      if (!parent || index === undefined) return;
      let html = null;
      if (node.type === 'code' && node.lang === 'math') {
        html = `<div class="math-display">${renderMath(node.value, true)}</div>`;
      } else if (node.type === 'code' && node.lang === 'figure') {
        const name = node.value.trim().split(/\s+/)[0];
        html = `<div class="lesson-figure" data-figure="${escapeHtml(node.value.trim())}" data-figure-id="${escapeHtml(name)}"></div>`;
      } else if (node.type === 'code' && node.lang === 'mermaid') {
        html = `<div class="mermaid-wrap"><pre class="mermaid" data-src="${escapeHtml(node.value)}">${escapeHtml(node.value)}</pre></div>`;
      } else if (node.type === 'math') {
        html = `<div class="math-display">${renderMath(node.value, true)}</div>`;
      } else if (node.type === 'inlineMath') {
        html = renderMath(node.value, false);
      } else if (node.type === 'html') {
        const tag = node.value.match(/^<\/?([A-Za-z][\w-]*)/);
        if (tag && !HTML_TAGS.has(tag[1].toLowerCase())) {
          parent.children[index] = { type: 'text', value: node.value };
          return;
        }
        if (ctx && /<img\s/i.test(node.value)) {
          node.value = node.value.replace(/(<img\s[^>]*src=")([^"]+)(")/gi, (_, a, src, b) => a + rewrite(src, ctx, { base, commit }) + b);
        }
      }
      if (html !== null) {
        parent.children[index] = { type: 'html', value: html };
      }
    });
  };
}
