#!/usr/bin/env python3
"""Check Thai lessons and the bilingual quizzes against their English sources.

Lessons (src/content/docs/th/<phase>/<lesson>.md):
  - the English lesson exists and the upstream_* fields and source_hash match it
    (a different source_hash means the translation is stale: reported, not an error)
  - fenced blocks appear in the same order with the same language; every block except
    mermaid (whose labels are translated) and plain blocks with no language (often prose
    laid out as a diagram, which may be translated; listed as a note) is byte-identical
    to the English one
  - the same number of display-math blocks ($$ ... $$)

Quizzes (src/data/quizzes/<phase>/<lesson>.json):
  - 15 questions, 5 per level, unique ids, both languages filled in, answer in range
  - questions marked origin "upstream" match the upstream quiz word for word

Usage: python3 scripts/check-thai.py [path-filter]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "src" / "content" / "docs"
flt = sys.argv[1] if len(sys.argv) > 1 else ""
problems = []
notes = []

FENCE = re.compile(r"^(```+|~~~+)([^\n`]*)\n(.*?)^\1[ \t]*$", re.M | re.S)


def front(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    data = {}
    if m:
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            if not line.startswith(" ") and v.strip():
                data[k.strip()] = v.strip().strip('"')
    return data, text[m.end():] if m else text


def blocks(body):
    return [(m.group(2).strip().split(" ")[0], m.group(3)) for m in FENCE.finditer(body)]


def outside_fences(body):
    return FENCE.sub("", body)


lessons = 0
for th_file in sorted((DOCS / "th").glob("*/*.md")):
    rel = th_file.relative_to(DOCS / "th")
    if flt not in str(rel):
        continue
    lessons += 1
    en_file = DOCS / "en" / rel
    if not en_file.exists():
        problems.append(f"{rel}: no English lesson at {en_file.relative_to(ROOT)}")
        continue
    th_meta, th_body = front(th_file.read_text(encoding="utf-8"))
    en_meta, en_body = front(en_file.read_text(encoding="utf-8"))
    for key in ("upstream_path", "upstream_commit"):
        if th_meta.get(key) != en_meta.get(key):
            problems.append(f"{rel}: {key} differs from the English lesson")
    if th_meta.get("source_hash") != en_meta.get("source_hash"):
        notes.append(f"{rel}: translated from an older English version (source_hash differs)")
    if "title" not in th_meta or "label" not in th_file.read_text(encoding="utf-8").split("---")[1]:
        problems.append(f"{rel}: missing title or sidebar label")

    tb, eb = blocks(th_body), blocks(en_body)
    if [b[0] for b in tb] != [b[0] for b in eb]:
        problems.append(f"{rel}: fenced blocks differ in number or language: th {[b[0] for b in tb]} vs en {[b[0] for b in eb]}")
    else:
        for i, ((lang, t), (_, e)) in enumerate(zip(tb, eb)):
            if lang == "" and t != e:
                notes.append(f"{rel}: plain block {i + 1} is translated (check it is prose, not program output)")
            elif lang != "mermaid" and t != e:
                problems.append(f"{rel}: block {i + 1} ({lang or 'plain'}) is not identical to the English one")
    tm = outside_fences(th_body).count("$$")
    em = outside_fences(en_body).count("$$")
    if tm != em:
        problems.append(f"{rel}: {tm // 2} display-math blocks vs {em // 2} in English")


def filled(obj):
    return isinstance(obj, dict) and all(isinstance(obj.get(k), str) and obj[k].strip() for k in ("en", "th"))


quizzes = 0
for qfile in sorted((ROOT / "src" / "data" / "quizzes").glob("*/*.json")):
    rel = qfile.relative_to(ROOT / "src" / "data" / "quizzes")
    if flt not in str(rel):
        continue
    quizzes += 1
    data = json.loads(qfile.read_text(encoding="utf-8"))
    key = str(rel)[:-5]
    if data.get("lesson") != key:
        problems.append(f"quiz {rel}: 'lesson' should be {key}")
    en_meta, _ = front((DOCS / "en" / (key + ".md")).read_text(encoding="utf-8"))
    if data.get("source_hash") != en_meta.get("source_hash"):
        notes.append(f"quiz {rel}: written for an older English version (source_hash differs)")
    qs = data.get("questions", [])
    levels = {lvl: sum(q.get("difficulty") == lvl for q in qs) for lvl in ("easy", "medium", "hard")}
    if len(qs) != 15 or any(n != 5 for n in levels.values()):
        problems.append(f"quiz {rel}: needs 5 questions per level, has {levels} ({len(qs)} total)")
    ids = [q.get("id") for q in qs]
    if len(set(ids)) != len(ids):
        problems.append(f"quiz {rel}: duplicate ids")
    up_file = ROOT / "src" / "data" / "upstream-quiz" / rel
    upstream = json.loads(up_file.read_text(encoding="utf-8"))["questions"] if up_file.exists() else []
    for q in qs:
        qid = f"quiz {rel} {q.get('id')}"
        if not filled(q.get("question")) or not filled(q.get("explanation")):
            problems.append(f"{qid}: question and explanation need both en and th")
        opts = q.get("options", [])
        if len(opts) < 2 or not all(filled(o) for o in opts):
            problems.append(f"{qid}: needs at least 2 options, each with en and th")
        if not isinstance(q.get("answer"), int) or not 0 <= q["answer"] < len(opts):
            problems.append(f"{qid}: answer must be an option index")
        if q.get("origin") not in ("upstream", "new"):
            problems.append(f"{qid}: origin must be 'upstream' or 'new'")
        if q.get("origin") == "upstream":
            match = [u for u in upstream if u["question"] == q["question"]["en"]]
            if not match:
                problems.append(f"{qid}: marked upstream but the English question is not in the upstream quiz")
                continue
            u = match[0]
            if [o["en"] for o in opts] != u["options"] or q["answer"] != u["correct"] or q["explanation"]["en"] != u["explanation"]:
                problems.append(f"{qid}: options, answer or explanation differ from the upstream question")

for n in notes:
    print("note", n)
for p in problems:
    print("FAIL", p)
print(f"{lessons} Thai lesson(s) and {quizzes} quiz(zes) checked, {len(problems)} problem(s)")
sys.exit(1 if problems else 0)
