// Main-thread side of the Pyodide worker: queues jobs and enforces time limits.
type Job = { id: number; resolve: (r: RunResult) => void; timer?: number };
export type RunResult = { ok: boolean; out?: string; error?: string; result?: any; timedOut?: boolean };

const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';
let worker: Worker | null = null;
let readyPromise: Promise<RunResult> | null = null;
let nextId = 1;
const jobs = new Map<number, Job>();

function spawn() {
  worker = new Worker(base + 'py-worker.js', { type: 'module' });
  worker.onmessage = (e: MessageEvent) => {
    const job = jobs.get(e.data.id);
    if (!job) return;
    if (job.timer) clearTimeout(job.timer);
    jobs.delete(e.data.id);
    job.resolve(e.data);
  };
  readyPromise = null;
}

function post(msg: Record<string, unknown>, timeoutMs?: number): Promise<RunResult> {
  if (!worker) spawn();
  const id = nextId++;
  return new Promise((resolve) => {
    const job: Job = { id, resolve };
    if (timeoutMs) {
      job.timer = window.setTimeout(() => {
        // A runaway loop: kill the worker; the next call starts a fresh one.
        worker?.terminate();
        worker = null;
        readyPromise = null;
        for (const [jid, j] of jobs) {
          if (j.timer) clearTimeout(j.timer);
          j.resolve({ ok: false, timedOut: true });
          jobs.delete(jid);
        }
      }, timeoutMs);
    }
    jobs.set(id, job);
    worker!.postMessage({ id, base, ...msg });
  });
}

export function isLoaded() {
  return readyPromise !== null;
}

export function ensureReady(): Promise<RunResult> {
  if (!worker) spawn();
  if (!readyPromise) {
    const p = post({ type: 'init' });
    readyPromise = p;
    p.then((r) => {
      if (!r.ok && readyPromise === p) readyPromise = null; // allow a retry
    });
  }
  return readyPromise;
}

export async function runCode(code: string, ns = 'page', timeoutMs = 20000) {
  const ready = await ensureReady();
  if (!ready.ok) return ready;
  return post({ type: 'run', code, ns }, timeoutMs);
}

export async function checkCode(user: string, tests: string, timeoutMs = 15000) {
  const ready = await ensureReady();
  if (!ready.ok) return ready;
  return post({ type: 'check', user, tests }, timeoutMs);
}
