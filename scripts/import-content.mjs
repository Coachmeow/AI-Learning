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
const copyDir = (from, to) => {
  if (!fs.existsSync(from)) return 0;
  let n = 0;
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    const a = path.join(from, entry.name);
    const b = path.join(to, entry.name);
    if (entry.isDirectory()) n += copyDir(a, b);
    else if (entry.isFile() && !/\.(o|out|log|pyc)$/.test(entry.name)) {
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
  const files = copyDir(path.join(src, 'code'), path.join(root, 'public/lesson-files', phase, lesson, 'code')) +
    copyDir(path.join(src, 'outputs'), path.join(root, 'public/lesson-files', phase, lesson, 'outputs'));

  lock.lessons[key] = { source_hash: hash };
  console.log(`imported ${key} (${files} files)`);
}

// Interactive figure runtime (MIT, from the upstream site).
const figSrc = path.join(upstream, 'site', 'lesson-figures.js');
if (fs.existsSync(figSrc)) {
  write(
    path.join(root, 'public/vendor/figures/lesson-figures.js'),
    `/* From rohitg00/ai-engineering-from-scratch site/lesson-figures.js @ ${commit}\n   MIT License, Copyright (c) 2026 Rohit Ghumare. See NOTICE-UPSTREAM.md. */\n` +
      fs.readFileSync(figSrc, 'utf8'),
  );
}

const license = fs.readFileSync(path.join(upstream, 'LICENSE'), 'utf8');
write(
  path.join(root, 'NOTICE-UPSTREAM.md'),
  `# Upstream content notice\n\nLesson text, code, quizzes and interactive figures in this site come from\n[AI Engineering from Scratch](${lock.repo}) (commit \`${commit}\`), used under the MIT License below.\nThai translations, new quiz questions and hands-on exercises are added by this project.\n\n\`\`\`text\n${license.trim()}\n\`\`\`\n`,
);

lock.lessons = Object.fromEntries(Object.entries(lock.lessons).sort(([a], [b]) => a.localeCompare(b)));
write(lockFile, `${JSON.stringify(lock, null, 2)}\n`);
console.log(`done: ${targets.length} lesson(s) from ${commit.slice(0, 7)}`);
