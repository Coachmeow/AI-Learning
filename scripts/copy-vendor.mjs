#!/usr/bin/env node
// Copy Pyodide (Python compiled to WebAssembly) into public/ so code runs offline,
// and fetch the extra Python packages lessons import in the browser (numpy).
//
// The npm package ships the Python core only. Packages come from the Pyodide CDN
// (one small file each, checked against the sha256 in pyodide-lock.json). If the CDN
// is unreachable, the full Pyodide release on GitHub is streamed and only the needed
// files are extracted (needs curl + tar). Set PYODIDE_PACKAGES_DIR to copy them from
// a local folder instead.
import { execFileSync } from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const from = path.join(root, 'node_modules', 'pyodide');
const to = path.join(root, 'public', 'vendor', 'pyodide');
const files = ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json'];
const PACKAGES = ['numpy'];

fs.mkdirSync(to, { recursive: true });
for (const f of files) {
  const a = path.join(from, f);
  const b = path.join(to, f);
  if (!fs.existsSync(a)) throw new Error(`missing ${a}; run npm install`);
  if (fs.existsSync(b) && fs.statSync(b).size === fs.statSync(a).size) continue;
  fs.copyFileSync(a, b);
}
console.log('pyodide core copied to public/vendor/pyodide');

const version = JSON.parse(fs.readFileSync(path.join(from, 'package.json'), 'utf8')).version;
const lock = JSON.parse(fs.readFileSync(path.join(from, 'pyodide-lock.json'), 'utf8'));
const sha256 = (buf) => crypto.createHash('sha256').update(buf).digest('hex');

// The packages plus everything they depend on.
const needed = new Map();
const add = (name) => {
  const pkg = lock.packages[name];
  if (!pkg || needed.has(name)) return;
  needed.set(name, pkg);
  (pkg.depends || []).forEach(add);
};
PACKAGES.forEach(add);

const ok = (pkg) => {
  const file = path.join(to, pkg.file_name);
  return fs.existsSync(file) && sha256(fs.readFileSync(file)) === pkg.sha256;
};
let missing = [...needed.values()].filter((p) => !ok(p));

const localDir = process.env.PYODIDE_PACKAGES_DIR;
if (missing.length && localDir) {
  for (const pkg of missing) {
    const src = path.join(localDir, pkg.file_name);
    if (fs.existsSync(src)) fs.copyFileSync(src, path.join(to, pkg.file_name));
  }
  missing = missing.filter((p) => !ok(p));
}

for (const pkg of missing) {
  try {
    const res = await fetch(`https://cdn.jsdelivr.net/pyodide/v${version}/full/${pkg.file_name}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    if (sha256(buf) !== pkg.sha256) throw new Error('checksum mismatch');
    fs.writeFileSync(path.join(to, pkg.file_name), buf);
  } catch (err) {
    console.warn(`could not download ${pkg.file_name} from the Pyodide CDN (${err.message})`);
  }
}
missing = missing.filter((p) => !ok(p));

if (missing.length && process.platform !== 'win32') {
  console.log('trying the Pyodide release on GitHub (streams ~340 MB, keeps only what is needed)...');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pyodide-'));
  const url = `https://github.com/pyodide/pyodide/releases/download/${version}/pyodide-${version}.tar.bz2`;
  const patterns = missing.map((p) => `'*/${p.file_name}'`).join(' ');
  try {
    execFileSync('sh', ['-c', `curl -sfL '${url}' | tar -xjf - -C '${tmp}' --wildcards ${patterns}`], { stdio: 'inherit' });
    for (const pkg of missing) {
      const src = path.join(tmp, 'pyodide', pkg.file_name);
      if (fs.existsSync(src)) fs.copyFileSync(src, path.join(to, pkg.file_name));
    }
  } catch (err) {
    console.warn(`GitHub release download failed (${err.message})`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  missing = missing.filter((p) => !ok(p));
}

if (missing.length) {
  console.warn(
    `WARNING: ${missing.map((p) => p.file_name).join(', ')} not available. ` +
      'Lessons that import these packages cannot run in the browser until you build once while online.',
  );
} else {
  console.log(`python packages ready: ${[...needed.keys()].join(', ')}`);
}
