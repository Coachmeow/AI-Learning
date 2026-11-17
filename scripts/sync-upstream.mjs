#!/usr/bin/env node
// Fetch (or update) a light copy of the upstream course into .upstream/ (git-ignored).
// Only the folders the import needs are checked out, so it stays small.
//   node scripts/sync-upstream.mjs            # latest commit on main
//   node scripts/sync-upstream.mjs <commit>   # a specific commit
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const dir = path.join(root, '.upstream', 'ai-engineering-from-scratch');
const repo = 'https://github.com/rohitg00/ai-engineering-from-scratch.git';
const git = (...a) => execFileSync('git', a, { stdio: 'inherit' });

if (!fs.existsSync(path.join(dir, '.git'))) {
  fs.mkdirSync(path.dirname(dir), { recursive: true });
  git('clone', '--filter=blob:none', '--sparse', '--depth', '1', repo, dir);
  git('-C', dir, 'sparse-checkout', 'set', 'phases', 'practice', 'glossary', 'site/lesson-figures.js');
}
const ref = process.argv[2] || 'main';
git('-C', dir, 'fetch', '--depth', '1', 'origin', ref);
git('-C', dir, 'checkout', '--detach', 'FETCH_HEAD');
console.log(`upstream ready at ${dir}`);
