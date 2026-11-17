// Home page: fill in "continue where you left off", progress counts and the backup buttons
// from what this browser has stored (nothing leaves the browser).
const STORE_VISITS = 'ail-visits-v1';
const STORE_PROGRESS = 'ail-progress-v1';

type Visits = { seen: Record<string, number>; last: { key: string; title: string } | null };

const read = <T>(key: string, fallback: T): T => {
  try {
    return (JSON.parse(localStorage.getItem(key) || 'null') as T) ?? fallback;
  } catch {
    return fallback;
  }
};

const root = document.querySelector<HTMLElement>('.ail-home');
if (root) {
  const data = JSON.parse(document.getElementById('ail-home-data')!.textContent!) as {
    phaseKeys: Record<string, string[]>;
    base: string;
    lang: 'th' | 'en';
    imported: string;
    importFail: string;
  };
  const visits = read<Visits>(STORE_VISITS, { seen: {}, last: null });
  const progress = read<Record<string, { quiz?: Record<string, number>; ex?: Record<string, boolean> }>>(STORE_PROGRESS, {});
  const seen = visits.seen || {};

  const set = (sel: string, text: string) => {
    const el = root.querySelector(sel);
    if (el) el.textContent = text;
  };
  set('[data-stat="read"]', String(Object.keys(seen).length));
  let quiz = 0;
  let ex = 0;
  for (const p of Object.values(progress)) {
    quiz += Object.values(p.quiz || {}).filter((v) => v >= 0.7).length;
    ex += Object.values(p.ex || {}).filter(Boolean).length;
  }
  set('[data-stat="quiz"]', String(quiz));
  set('[data-stat="ex"]', String(ex));

  root.querySelectorAll<HTMLElement>('[data-phase]').forEach((card) => {
    const keys = data.phaseKeys[card.dataset.phase!] || [];
    const n = keys.filter((k) => seen[k]).length;
    const count = keys.length || 1;
    const bar = card.querySelector<HTMLElement>('[data-read-bar]');
    if (bar) bar.style.width = `${Math.round((n / count) * 100)}%`;
    const label = card.querySelector('[data-read-count]');
    if (label) label.textContent = String(n);
  });

  if (visits.last && /^\d\d-[^/]+\/\d\d-[^/]+$/.test(visits.last.key)) {
    const [phase, lesson] = visits.last.key.split('/');
    const n = parseInt(lesson.slice(0, 2), 10);
    set('[data-where]', data.lang === 'th' ? `Phase ${phase.slice(0, 2)} · บทที่ ${n}` : `Phase ${phase.slice(0, 2)} · Lesson ${n}`);
    set('[data-title]', visits.last.title);
    root.querySelector('[data-none]')?.remove();
    root.querySelector<HTMLAnchorElement>('[data-cont-link]')!.href = `${data.base}${data.lang}/${visits.last.key}/`;
  }

  // Backup: every key this site stores starts with "ail-".
  root.querySelector('[data-export]')?.addEventListener('click', () => {
    const all: Record<string, string> = {};
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i)!;
      if (k.startsWith('ail-')) all[k] = localStorage.getItem(k)!;
    }
    const blob = new Blob([JSON.stringify({ app: 'ai-learning', version: 1, exportedAt: new Date().toISOString(), data: all }, null, 2)], {
      type: 'application/json',
    });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `ai-learning-progress-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  });

  const msg = root.querySelector('[data-import-msg]');
  root.querySelector<HTMLInputElement>('[data-import]')?.addEventListener('change', async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    try {
      const parsed = JSON.parse(await file.text());
      if (parsed?.app !== 'ai-learning' || typeof parsed.data !== 'object') throw new Error('bad file');
      for (const [k, v] of Object.entries(parsed.data)) {
        if (k.startsWith('ail-') && typeof v === 'string') localStorage.setItem(k, v);
      }
      if (msg) msg.textContent = data.imported;
      setTimeout(() => location.reload(), 600);
    } catch {
      if (msg) msg.textContent = data.importFail;
    }
  });
}
