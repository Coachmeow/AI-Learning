/* Runs Python with Pyodide inside a (module) Web Worker so the page never freezes.
   Messages in:  { id, type: 'init' | 'run' | 'check', base, ns?, code?, user?, tests? }
   Messages out: { id, ok, out?, error?, result? } */
let ready = null;
const namespaces = {};

function init(base) {
  if (!ready) {
    ready = (async () => {
      const { loadPyodide } = await import(base + 'vendor/pyodide/pyodide.mjs');
      const py = await loadPyodide({ indexURL: base + 'vendor/pyodide/' });
      const harness = await (await fetch(base + 'py/harness.py')).text();
      py.FS.writeFile('/home/pyodide/harness.py', harness);
      py.runPython("import sys; sys.path.insert(0, '/home/pyodide')");
      return py;
    })();
    ready.catch(() => {
      ready = null;
    });
  }
  return ready;
}

function getNs(py, name) {
  if (!namespaces[name]) {
    const d = py.globals.get('dict')();
    d.set('__name__', '__main__');
    namespaces[name] = d;
  }
  return namespaces[name];
}

self.onmessage = async (e) => {
  const msg = e.data;
  let py;
  try {
    py = await init(msg.base);
  } catch (err) {
    self.postMessage({ id: msg.id, ok: false, error: String(err && err.message ? err.message : err) });
    return;
  }
  if (msg.type === 'init') {
    self.postMessage({ id: msg.id, ok: true });
    return;
  }
  const out = [];
  py.setStdout({ batched: (s) => out.push(s) });
  py.setStderr({ batched: (s) => out.push(s) });
  try {
    if (msg.type === 'run') {
      await py.runPythonAsync(msg.code, { globals: getNs(py, msg.ns || 'page') });
      self.postMessage({ id: msg.id, ok: true, out: out.join('\n') });
    } else if (msg.type === 'check') {
      const harness = py.pyimport('harness');
      const json = harness.run_checks_json(msg.user, msg.tests);
      harness.destroy();
      self.postMessage({ id: msg.id, ok: true, out: out.join('\n'), result: JSON.parse(json) });
    }
  } catch (err) {
    let text = String(err && err.message ? err.message : err);
    // Keep the useful tail of a Python traceback.
    const lines = text.trim().split('\n');
    const start = lines.findIndex((l) => l.includes('File "<exec>"'));
    if (start > 0) text = ['Traceback (most recent call last):', ...lines.slice(start)].join('\n');
    self.postMessage({ id: msg.id, ok: false, out: out.join('\n'), error: text });
  }
};
