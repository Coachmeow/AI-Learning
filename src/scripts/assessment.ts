// "Check your understanding": multiple-choice quiz and hands-on exercises, each with difficulty levels.
import { checkCode } from './py-runner';

type Level = 'easy' | 'medium' | 'hard';
type Question = {
  id: string;
  difficulty: Level;
  origin: 'upstream' | 'new';
  question: string;
  code?: string;
  options: string[];
  answer: number;
  explanation: string;
};
type Exercise = {
  title: string;
  minutes: number;
  prompt: string;
  hints: string[];
  starter: string;
  solution: string;
  tests: string;
};
type CheckResult = { id: string; title: { th: string; en: string }; hidden: boolean; ok: boolean; th?: string; en?: string };
type Data = {
  lesson: string;
  lang: 'th' | 'en';
  ui: Record<string, any>;
  quiz: Question[];
  exercises: Partial<Record<Level, Exercise>>;
};

const LEVELS: Level[] = ['easy', 'medium', 'hard'];
const PASS = 0.7;
const STORE = 'ail-progress-v1';

const fmt = (s: string, vars: Record<string, string | number>) => s.replace(/\{(\w+)\}/g, (_, k) => String(vars[k] ?? ''));
const shuffle = <T>(a: T[]) => {
  const b = a.slice();
  for (let i = b.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [b[i], b[j]] = [b[j], b[i]];
  }
  return b;
};

// replaceChildren() would print "null" for skipped parts, so drop them first.
const put = (el: Element, ...kids: (Node | string | null | false | undefined)[]) =>
  el.replaceChildren(...(kids.filter(Boolean) as (Node | string)[]));

function h(tag: string, attrs: Record<string, any> = {}, kids: (Node | string | null | false)[] = []) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === false || v == null) continue;
    if (k === 'class') el.className = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const c of kids) if (c) el.append(c);
  return el;
}

// Light inline formatting for prompts and hints: `code` and **bold**.
const escapeHtml = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const inline = (s: string) =>
  escapeHtml(s)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

const ICON_OK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--ail-ok)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>';
const ICON_FAIL = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--ail-warn)" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M9 9l6 6M15 9l-6 6"/></svg>';
const ICON_LOCK = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>';

function loadStore(): Record<string, any> {
  try {
    return JSON.parse(localStorage.getItem(STORE) || '{}');
  } catch {
    return {};
  }
}
function saveStore(s: Record<string, any>) {
  try {
    localStorage.setItem(STORE, JSON.stringify(s));
  } catch {
    /* private mode: progress just isn't kept */
  }
}

function setup(root: HTMLElement) {
  const data: Data = JSON.parse(root.querySelector('.ail-data')!.textContent!);
  const t = data.ui;
  const lessonKey = data.lesson;
  const store = loadStore();
  const prog = (store[lessonKey] ||= { quiz: {}, ex: {} });
  const persist = () => {
    store[lessonKey] = prog;
    saveStore(store);
  };

  const tabs = root.querySelectorAll<HTMLButtonElement>('.ail-tab');
  const levelsBox = root.querySelector<HTMLElement>('.ail-levels')!;
  const quizPanel = root.querySelector<HTMLElement>('[data-panel="quiz"]')!;
  const codePanel = root.querySelector<HTMLElement>('[data-panel="code"]')!;
  const hasQuiz = data.quiz.length > 0;
  const hasEx = LEVELS.some((l) => data.exercises[l]);

  let tab: 'quiz' | 'code' = hasQuiz ? 'quiz' : 'code';
  let level: Level | 'mixed' = 'easy';

  /* ── Level pills ── */
  function renderLevels() {
    put(levelsBox, h('span', { class: 'ail-levels-label' }, [t.level]));
    const list: (Level | 'mixed')[] = tab === 'quiz' ? [...LEVELS.filter((l) => data.quiz.some((q) => q.difficulty === l)), 'mixed'] : LEVELS.filter((l) => data.exercises[l]);
    if (!list.includes(level)) level = list[0];
    for (const l of list) {
      const done = tab === 'quiz' ? l !== 'mixed' && (prog.quiz[l] ?? 0) >= PASS : prog.ex[l] === true;
      levelsBox.append(
        h('button', { type: 'button', class: 'ail-pill', 'aria-pressed': String(l === level), onclick: () => select(l) }, [
          t.levels[l],
          done ? h('span', { class: 'ail-badge', 'aria-label': t.exDone }, ['✓']) : null,
        ]),
      );
    }
  }
  function select(l: Level | 'mixed') {
    level = l;
    renderLevels();
    if (tab === 'quiz') startQuiz();
    else showExercise();
  }
  function setTab(next: 'quiz' | 'code') {
    tab = next;
    tabs.forEach((b) => b.setAttribute('aria-selected', String(b.dataset.tab === tab)));
    quizPanel.hidden = tab !== 'quiz';
    codePanel.hidden = tab !== 'code';
    renderLevels();
    if (tab === 'quiz') startQuiz();
    else showExercise();
  }
  tabs.forEach((b) => {
    if ((b.dataset.tab === 'quiz' && !hasQuiz) || (b.dataset.tab === 'code' && !hasEx)) b.hidden = true;
    b.addEventListener('click', () => setTab(b.dataset.tab as 'quiz' | 'code'));
  });

  /* ── Quiz ── */
  let run: { qs: (Question & { order: number[] })[]; idx: number; score: number; picked: number | null } | null = null;

  function startQuiz() {
    let pool: Question[];
    if (level === 'mixed') pool = LEVELS.flatMap((l) => shuffle(data.quiz.filter((q) => q.difficulty === l)).slice(0, 2));
    else pool = data.quiz.filter((q) => q.difficulty === level);
    run = { qs: shuffle(pool).map((q) => ({ ...q, order: shuffle(q.options.map((_, i) => i)) })), idx: 0, score: 0, picked: null };
    renderQuestion();
  }

  function renderQuestion() {
    if (!run) return;
    const q = run.qs[run.idx];
    const n = run.qs.length;
    const best = level === 'mixed' ? null : prog.quiz[level];
    const answered = run.picked !== null;
    const correctPos = q.order.indexOf(q.answer);
    const opts = q.order.map((orig, pos) => {
      let cls = 'ail-opt';
      if (answered) cls += orig === q.answer ? ' correct' : pos === run!.picked ? ' wrong' : ' dim';
      return h('button', { type: 'button', class: cls, disabled: answered, onclick: () => pick(pos) }, [
        h('span', { class: 'ail-letter' }, [t.letters[pos]]),
        h('span', {}, [q.options[orig]]),
      ]);
    });
    const ok = answered && run.picked === correctPos;
    put(quizPanel, 
      h('div', { class: 'ail-meta' }, [
        h('span', { class: 'ail-counter' }, [fmt(t.questionOf, { i: run.idx + 1, n })]),
        best != null ? h('span', { class: 'ail-muted' }, [`${t.best}: ${Math.round(best * 100)}%`]) : null,
      ]),
      h('div', { class: 'ail-progress' }, [h('i', { style: `width:${((run.idx + (answered ? 1 : 0)) / n) * 100}%` })]),
      h('p', { class: 'ail-question' }, [
        q.question,
        q.origin === 'upstream' ? h('span', { class: 'ail-origin', title: t.fromUpstream }, [t.fromUpstream]) : null,
      ]),
      q.code ? h('pre', { class: 'ail-code' }, [q.code]) : null,
      h('div', { class: 'ail-options' }, opts),
      answered
        ? h('div', { class: 'ail-feedback', role: 'status' }, [
            h('div', { class: ok ? 'ail-ok' : 'ail-warn' }, [ok ? t.correct : t.wrong]),
            h('div', {}, [q.explanation]),
          ])
        : null,
      answered
        ? h('div', { class: 'ail-actions' }, [
            h('button', { type: 'button', class: 'ail-btn primary', onclick: nextQuestion }, [run.idx + 1 < n ? t.next : t.finish]),
          ])
        : null,
    );
  }

  function pick(pos: number) {
    if (!run || run.picked !== null) return;
    run.picked = pos;
    const q = run.qs[run.idx];
    if (q.order[pos] === q.answer) run.score++;
    renderQuestion();
    quizPanel.querySelector<HTMLButtonElement>('.ail-actions .ail-btn')?.focus();
  }

  function nextQuestion() {
    if (!run) return;
    if (run.idx + 1 < run.qs.length) {
      run.idx++;
      run.picked = null;
      renderQuestion();
      quizPanel.querySelector<HTMLButtonElement>('.ail-opt')?.focus();
      return;
    }
    const pct = run.score / run.qs.length;
    if (level !== 'mixed') {
      prog.quiz[level] = Math.max(prog.quiz[level] ?? 0, pct);
      persist();
      renderLevels();
    }
    const passed = pct >= PASS;
    put(quizPanel, 
      h('div', { class: 'ail-muted' }, [`${t.resultTitle} · ${t.levels[level]}`]),
      h('div', { class: 'ail-score' }, [`${run.score} / ${run.qs.length}`]),
      h('div', { class: passed ? 'ail-ok' : 'ail-warn' }, [passed ? t.passed : t.notPassed]),
      h('div', { class: 'ail-actions' }, [h('button', { type: 'button', class: 'ail-btn primary', onclick: startQuiz }, [t.retry])]),
    );
  }

  /* ── Exercises ── */
  let editorMod: Promise<typeof import('./editor')> | null = null;
  const drafts: Partial<Record<Level, { get: () => string; set: (s: string) => void }>> = {};

  async function showExercise() {
    const l = level as Level;
    const ex = data.exercises[l];
    if (!ex) return;
    editorMod ||= import('./editor');
    const draftKey = `ail-draft:${lessonKey}:${l}`;
    let draft = ex.starter;
    try {
      draft = localStorage.getItem(draftKey) ?? ex.starter;
    } catch {
      /* ignore */
    }
    let attempts = 0;
    let hintShown = 0;

    const hintBox = h('div', { class: 'ail-hint', hidden: true });
    const results = h('div', { class: 'ail-results', hidden: true, role: 'status' });
    const solution = h('details', { class: 'ail-solution', hidden: true }, [
      h('summary', {}, [t.solutionTitle]),
      h('pre', { class: 'ail-code' }, [ex.solution]),
    ]);
    const editorHost = h('div');
    const checkBtn = h('button', { type: 'button', class: 'ail-btn primary' }, [t.exCheck]) as HTMLButtonElement;
    const hintBtn = h('button', { type: 'button', class: 'ail-btn' }, [t.exHint]) as HTMLButtonElement;
    const resetBtn = h('button', { type: 'button', class: 'ail-btn' }, [t.exReset]) as HTMLButtonElement;
    const solBtn = h('button', { type: 'button', class: 'ail-btn', disabled: !prog.ex[l] }, [prog.ex[l] ? t.exSolution : t.exSolutionLocked]) as HTMLButtonElement;

    put(codePanel, 
      h('div', { class: 'ail-ex-head' }, [
        h('h3', {}, [ex.title]),
        h('span', { class: 'ail-muted' }, [fmt(t.exMinutes, { m: ex.minutes })]),
        prog.ex[l] ? h('span', { class: 'ail-ok' }, [`✓ ${t.exDone}`]) : null,
      ]),
      h('p', { class: 'ail-ex-prompt', html: inline(ex.prompt) }),
      h('div', { class: 'ail-editor' }, [h('div', { class: 'ail-editor-bar' }, [h('span', {}, ['solution.py']), h('span', {}, [t.exEditable])]), editorHost]),
      h('div', { class: 'ail-actions' }, [checkBtn, hintBtn, resetBtn, solBtn]),
      hintBox,
      results,
      solution,
    );

    const { createEditor } = await editorMod;
    if (level !== l || tab !== 'code') return; // the learner switched away while loading
    let timer = 0;
    const editor = createEditor(editorHost, draft, (text) => {
      clearTimeout(timer);
      timer = window.setTimeout(() => {
        try {
          localStorage.setItem(draftKey, text);
        } catch {
          /* ignore */
        }
      }, 400);
    });
    drafts[l] = editor;

    hintBtn.addEventListener('click', () => {
      if (hintShown < ex.hints.length) hintShown++;
      hintBox.hidden = false;
      hintBox.innerHTML = ex.hints
        .slice(0, hintShown)
        .map((s, i) => `<div><b>${fmt(t.exHintN, { i: i + 1, n: ex.hints.length })}</b> ${inline(s)}</div>`)
        .join('');
      if (hintShown >= ex.hints.length) hintBtn.disabled = true;
    });
    resetBtn.addEventListener('click', () => editor.set(ex.starter));
    solBtn.addEventListener('click', () => {
      solution.hidden = false;
      (solution as HTMLDetailsElement).open = true;
    });

    checkBtn.addEventListener('click', async () => {
      checkBtn.disabled = true;
      checkBtn.replaceChildren(h('span', { class: 'ail-spin', 'aria-hidden': 'true' }), t.exChecking);
      const r = await checkCode(editor.get(), ex.tests);
      checkBtn.disabled = false;
      checkBtn.replaceChildren(t.exCheck);
      attempts++;
      results.hidden = false;
      if (r.timedOut) {
        put(results, h('div', { class: 'ail-warn' }, [fmt(t.timeout ?? 'Timed out', { s: 15 })]));
      } else if (!r.ok || r.result?.error) {
        put(results, h('div', { class: 'ail-warn' }, [t.exError]), h('pre', { class: 'ail-code' }, [r.result?.error || r.error || '']));
      } else {
        const list: CheckResult[] = r.result.results;
        const visible = list.filter((c) => !c.hidden);
        const hidden = list.filter((c) => c.hidden);
        const okVisible = visible.filter((c) => c.ok).length;
        const allVisible = okVisible === visible.length;
        const okHidden = hidden.filter((c) => c.ok).length;
        const allPass = allVisible && okHidden === hidden.length;
        const rows: Node[] = [h('div', { class: allPass ? 'ail-ok' : 'ail-warn' }, [allPass ? t.exAllPass : fmt(t.exSomeFail, { ok: okVisible + (allVisible ? okHidden : 0), n: visible.length + (allVisible ? hidden.length : 0) })])];
        for (const c of visible) {
          const msg = c.ok ? c.title[data.lang] : c[data.lang] || c.title[data.lang];
          rows.push(h('div', {}, [h('span', { html: c.ok ? ICON_OK : ICON_FAIL }), h('span', { class: c.ok ? '' : 'ail-warn-text' }, [c.ok ? msg : `${c.title[data.lang]}: ${msg}`])]));
        }
        if (hidden.length) {
          const txt = allVisible ? fmt(t.exHidden, { ok: okHidden, n: hidden.length }) : fmt(t.exHiddenWait, { n: hidden.length });
          rows.push(h('div', { class: 'ail-muted' }, [h('span', { html: allVisible ? (okHidden === hidden.length ? ICON_OK : ICON_FAIL) : ICON_LOCK }), h('span', {}, [txt])]));
        }
        put(results, ...rows);
        if (allPass) {
          prog.ex[l] = true;
          persist();
          renderLevels();
        }
      }
      if (prog.ex[l] || attempts >= 3) {
        solBtn.disabled = false;
        solBtn.textContent = t.exSolution;
      }
    });
  }

  setTab(tab);
}

document.querySelectorAll<HTMLElement>('.ail-assess').forEach(setup);
