#!/usr/bin/env node
// Copy Pyodide (Python compiled to WebAssembly) into public/ so code runs offline.
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const from = path.join(root, 'node_modules', 'pyodide');
const to = path.join(root, 'public', 'vendor', 'pyodide');
const files = ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json'];

fs.mkdirSync(to, { recursive: true });
for (const f of files) {
  const a = path.join(from, f);
  const b = path.join(to, f);
  if (!fs.existsSync(a)) throw new Error(`missing ${a}; run npm install`);
  const sa = fs.statSync(a);
  if (fs.existsSync(b) && fs.statSync(b).size === sa.size) continue;
  fs.copyFileSync(a, b);
}
console.log('pyodide copied to public/vendor/pyodide');
