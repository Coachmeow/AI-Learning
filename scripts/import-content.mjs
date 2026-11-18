#!/usr/bin/env node
// Import lessons from the upstream course (rohitg00/ai-engineering-from-scratch, MIT).
//
//   node scripts/import-content.mjs --lesson 01-math-foundations/08-optimization
//   node scripts/import-content.mjs --phase 01-math-foundations
//   node scripts/import-content.mjs --all
//   options: --upstream <dir>   (default: .upstream/ai-engineering-from-scratch, see scripts/sync-upstream.mjs)
//
// What it writes (English is copied as-is, never edited by hand):
//   src/content/docs/en/<phase>/<lesson>.md     lesson text, H1 moved into frontmatter
//   src/data/upstream-quiz/<phase>/<lesson>.json original quiz
//   public/lesson-files/<phase>/<lesson>/        code/ and outputs/ for download
//   public/vendor/figures/lesson-figures.js      interactive figure runtime
//   upstream.lock.json, NOTICE-UPSTREAM.md
import { execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const all = (name) => args.flatMap((a, i) => (a === name ? [args[i + 1]] : []));

const upstream = path.resolve(root, opt('--upstream') || '.upstream/ai-engineering-from-scratch');
if (!fs.existsSync(path.join(upstream, 'phases'))) {
  console.error(`Upstream checkout not found at ${upstream}. Run: node scripts/sync-upstream.mjs`);
  process.exit(1);
}
const commit = execFileSync('git', ['-C', upstream, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();

const lessonDirs = (phase) =>
  fs
    .readdirSync(path.join(upstream, 'phases', phase))
    .filter((d) => /^\d\d-/.test(d) && fs.existsSync(path.join(upstream, 'phases', phase, d, 'docs', 'en.md')))
    .map((d) => `${phase}/${d}`);

let targets = all('--lesson');
for (const phase of all('--phase')) targets.push(...lessonDirs(phase));
if (args.includes('--all')) {
  for (const phase of fs.readdirSync(path.join(upstream, 'phases')).filter((d) => /^\d\d-/.test(d))) {
    targets.push(...lessonDirs(phase));
  }
}
targets = [...new Set(targets)];
if (!targets.length) {
  console.error('Nothing to import. Pass --lesson <phase/lesson>, --phase <phase> or --all.');
  process.exit(1);
}

const sha256 = (s) => crypto.createHash('sha256').update(s).digest('hex');
const q = (s) => JSON.stringify(s); // JSON strings are valid YAML double-quoted scalars
const write = (file, data) => {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, data);
};
const IMAGE = /\.(png|jpe?g|gif|svg|webp|avif)$/i;
const SKIP_DIRS = new Set(['node_modules', '__pycache__', 'target', '.venv', 'venv', '.git']);
const isBinary = (file) => {
  const fd = fs.openSync(file, 'r');
  const buf = Buffer.alloc(1024);
  const n = fs.readSync(fd, buf, 0, 1024, 0);
  fs.closeSync(fd);
  return buf.subarray(0, n).includes(0);
};
// Copies text files (and images), skipping build outputs and compiled binaries.
const copyDir = (from, to) => {
  if (!fs.existsSync(from)) return 0;
  let n = 0;
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const a = path.join(from, entry.name);
    const b = path.join(to, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) n += copyDir(a, b);
    } else if (entry.isFile() && !/\.(o|out|log|pyc|class|wasm|so|dylib|exe)$/i.test(entry.name) && (IMAGE.test(entry.name) || !isBinary(a))) {
      fs.mkdirSync(to, { recursive: true });
      fs.copyFileSync(a, b);
      n++;
    }
  }
  return n;
};

const lockFile = path.join(root, 'upstream.lock.json');
const lock = fs.existsSync(lockFile) ? JSON.parse(fs.readFileSync(lockFile, 'utf8')) : { lessons: {} };
lock.repo = 'https://github.com/rohitg00/ai-engineering-from-scratch';
lock.commit = commit;

for (const key of targets) {
  const [phase, lesson] = key.split('/');
  const src = path.join(upstream, 'phases', phase, lesson);
  const raw = fs.readFileSync(path.join(src, 'docs', 'en.md'), 'utf8');
  const lines = raw.split('\n');
  const h1 = lines.findIndex((l) => /^#\s+/.test(l));
  const title = h1 >= 0 ? lines[h1].replace(/^#\s+/, '').trim() : lesson;
  const body = h1 >= 0 ? [...lines.slice(0, h1), ...lines.slice(h1 + 1)].join('\n').replace(/^\s*\n/, '') : raw;
  const quote = body.split('\n').find((l) => l.startsWith('> '));
  const order = parseInt(lesson.slice(0, 2), 10);
  const hash = sha256(raw);

  const front = [
    '---',
    `title: ${q(title)}`,
    quote ? `description: ${q(quote.slice(2).trim())}` : null,
    'sidebar:',
    `  label: ${q(`${lesson.slice(0, 2)} · ${title}`)}`,
    `  order: ${order}`,
    `upstream_path: ${q(`phases/${phase}/${lesson}`)}`,
    `upstream_commit: ${q(commit)}`,
    `source_hash: ${q(hash)}`,
    '---',
    '',
  ]
    .filter((l) => l !== null)
    .join('\n');
  write(path.join(root, 'src/content/docs/en', phase, `${lesson}.md`), `${front}${body}`);

  if (fs.existsSync(path.join(src, 'quiz.json'))) {
    write(path.join(root, 'src/data/upstream-quiz', phase, `${lesson}.json`), fs.readFileSync(path.join(src, 'quiz.json'), 'utf8'));
  }
  const filesDir = path.join(root, 'public/lesson-files', phase, lesson);
  const files =
    copyDir(path.join(src, 'code'), path.join(filesDir, 'code')) +
    copyDir(path.join(src, 'outputs'), path.join(filesDir, 'outputs')) +
    copyDir(path.join(src, 'assets'), path.join(filesDir, 'assets'));

  lock.lessons[key] = { source_hash: hash };
  console.log(`imported ${key} (${files} files)`);
}

// Interactive figures (MIT, from the upstream site): the runtime, every provider file
// (figures*.js) and a manifest saying which provider defines which figure.
const siteDir = path.join(upstream, 'site');
const figOut = path.join(root, 'public/vendor/figures');
const header = (f) => `/* From rohitg00/ai-engineering-from-scratch site/${f} @ ${commit}\n   MIT License, Copyright (c) 2026 Rohit Ghumare. See NOTICE-UPSTREAM.md. */\n`;
if (fs.existsSync(path.join(siteDir, 'lesson-figures.js'))) {
  const runtime = fs.readFileSync(path.join(siteDir, 'lesson-figures.js'), 'utf8');
  write(path.join(figOut, 'lesson-figures.js'), header('lesson-figures.js') + runtime);

  // Same provider order as the upstream build (later registrations override earlier ones).
  const buildJs = fs.readFileSync(path.join(siteDir, 'build.js'), 'utf8');
  const baseOrder = [...(buildJs.match(/const FIGURE_PROVIDER_ORDER = \[([\s\S]*?)\];/)?.[1] ?? '').matchAll(/'([^']+)'/g)].map((m) => m[1]);
  const extra = fs
    .readdirSync(siteDir)
    .filter((f) => /^figures(?:-[a-z0-9-]+)?\.js$/i.test(f) && !baseOrder.includes(f))
    .sort();
  const order = [...baseOrder, ...extra].filter((f) => fs.existsSync(path.join(siteDir, f)));
  const sources = new Map(order.map((f) => [f, fs.readFileSync(path.join(siteDir, f), 'utf8')]));
  for (const [f, s] of sources) write(path.join(figOut, f), header(f) + s);

  // Figure ids used by every upstream lesson (not only the imported ones, so later imports just work).
  const used = new Set();
  for (const phase of fs.readdirSync(path.join(upstream, 'phases')).filter((d) => /^\d\d-/.test(d))) {
    for (const key of lessonDirs(phase)) {
      const md = fs.readFileSync(path.join(upstream, 'phases', key, 'docs', 'en.md'), 'utf8');
      for (const m of md.matchAll(/```figure\s*\r?\n([\s\S]*?)```/g)) used.add(m[1].trim().split(/\s+/)[0]);
    }
  }
  const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const providers = {};
  const missing = [];
  for (const id of [...used].sort()) {
    const re = new RegExp(`['"]${esc(id)}['"]`);
    const list = order.filter((f) => re.test(sources.get(f)));
    if (list.length) providers[id] = list;
    else if (!re.test(runtime)) missing.push(id);
  }
  if (missing.length) console.warn(`figures with no provider: ${missing.join(', ')}`);
  const versions = Object.fromEntries(order.map((f) => [f, sha256(sources.get(f)).slice(0, 12)]));
  write(
    path.join(figOut, 'figure-manifest.js'),
    `// Generated by scripts/import-content.mjs. Provider paths resolve next to this file.\n(function () {\n` +
      `  var dir = document.currentScript.src.replace(/[^/]*$/, '');\n` +
      `  var order = ${JSON.stringify(order)};\n  var versions = ${JSON.stringify(versions)};\n  var byFigure = ${JSON.stringify(providers)};\n` +
      `  var abs = function (f) { return dir + f; };\n` +
      `  window.AIFS_FIGURE_PROVIDER_ORDER = order.map(abs);\n` +
      `  window.AIFS_FIGURE_PROVIDER_VERSIONS = {};\n  order.forEach(function (f) { window.AIFS_FIGURE_PROVIDER_VERSIONS[abs(f)] = versions[f]; });\n` +
      `  window.AIFS_FIGURE_PROVIDERS = {};\n  Object.keys(byFigure).forEach(function (id) { window.AIFS_FIGURE_PROVIDERS[id] = byFigure[id].map(abs); });\n})();\n`,
  );
  console.log(`figures: ${order.length} provider files, ${Object.keys(providers).length} routed figure ids`);
}

const license = fs.readFileSync(path.join(upstream, 'LICENSE'), 'utf8');
write(
  path.join(root, 'NOTICE-UPSTREAM.md'),
  `# Upstream content notice\n\nLesson text, code, quizzes and interactive figures in this site come from\n[AI Engineering from Scratch](${lock.repo}) (commit \`${commit}\`), used under the MIT License below.\nThai translations, new quiz questions and hands-on exercises are added by this project.\n\n\`\`\`text\n${license.trim()}\n\`\`\`\n`,
);

lock.lessons = Object.fromEntries(Object.entries(lock.lessons).sort(([a], [b]) => a.localeCompare(b)));
write(lockFile, `${JSON.stringify(lock, null, 2)}\n`);
console.log(`done: ${targets.length} lesson(s) from ${commit.slice(0, 7)}`);
