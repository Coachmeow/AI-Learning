// Turns the special fenced blocks used by the upstream lessons into HTML:
//   ```math      -> KaTeX (rendered at build time, no client JS needed)
//   ```figure    -> <div class="lesson-figure" data-figure="..."> hydrated by lesson-figures.js
//   ```mermaid   -> <pre class="mermaid"> rendered in the browser by the bundled Mermaid
// Inline $...$ and $$...$$ math (parsed by remark-math) is rendered with KaTeX too.
import katex from 'katex';
import { visit } from 'unist-util-visit';

const escapeHtml = (s) =>
  s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function renderMath(tex, displayMode) {
  return katex.renderToString(tex, { displayMode, throwOnError: false, strict: 'ignore', output: 'html' });
}

export default function remarkLesson() {
  return (tree) => {
    visit(tree, (node, index, parent) => {
      if (!parent || index === undefined) return;
      let html = null;
      if (node.type === 'code' && node.lang === 'math') {
        html = `<div class="math-display">${renderMath(node.value, true)}</div>`;
      } else if (node.type === 'code' && node.lang === 'figure') {
        const name = node.value.trim().split(/\s+/)[0];
        html = `<div class="lesson-figure" data-figure="${escapeHtml(name)}"></div>`;
      } else if (node.type === 'code' && node.lang === 'mermaid') {
        html = `<div class="mermaid-wrap"><pre class="mermaid" data-src="${escapeHtml(node.value)}">${escapeHtml(node.value)}</pre></div>`;
      } else if (node.type === 'math') {
        html = `<div class="math-display">${renderMath(node.value, true)}</div>`;
      } else if (node.type === 'inlineMath') {
        html = renderMath(node.value, false);
      }
      if (html !== null) {
        parent.children[index] = { type: 'html', value: html };
      }
    });
  };
}
