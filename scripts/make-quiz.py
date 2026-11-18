#!/usr/bin/env python3
"""Build src/data/quizzes/<phase>/<lesson>.json from a short spec file.

Upstream questions are copied word for word from src/data/upstream-quiz (English text,
options, answer and explanation); the spec only adds the Thai. New questions carry both
languages. Upstream "pre" questions become easy and "post" questions medium unless the
spec says otherwise.

Spec (JSON):
{
  "lesson": "00-setup-and-tooling/01-dev-environment",
  "upstream": [
    {"n": 0, "id": "e1", "q": "Thai question", "o": ["Thai option", ...], "x": "Thai explanation"}
  ],
  "new": [
    {"id": "e3", "d": "easy", "q": ["English", "Thai"], "code": "optional code",
     "o": [["English", "Thai"], ...], "a": 0, "x": ["English", "Thai"]}
  ]
}

Usage: python3 scripts/make-quiz.py spec.json [more-specs.json ...]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEVEL = {"pre": "easy", "post": "medium"}
ORDER = {"easy": 0, "medium": 1, "hard": 2}


def pair(v):
    return {"en": v[0], "th": v[1]}


for spec_path in sys.argv[1:]:
    spec = json.loads(pathlib.Path(spec_path).read_text(encoding="utf-8"))
    key = spec["lesson"]
    upstream = json.loads((ROOT / "src/data/upstream-quiz" / f"{key}.json").read_text(encoding="utf-8"))["questions"]
    en_md = (ROOT / "src/content/docs/en" / f"{key}.md").read_text(encoding="utf-8")
    source_hash = re.search(r'^source_hash: "([0-9a-f]+)"', en_md, re.M).group(1)

    questions = []
    for s in spec.get("upstream", []):
        u = upstream[s["n"]]
        if len(s["o"]) != len(u["options"]):
            sys.exit(f"{key} {s['id']}: {len(s['o'])} Thai options for {len(u['options'])} upstream options")
        q = {
            "id": s["id"],
            "difficulty": s.get("d", LEVEL[u["stage"]]),
            "origin": "upstream",
            "question": {"en": u["question"], "th": s["q"]},
            "options": [{"en": en, "th": th} for en, th in zip(u["options"], s["o"])],
            "answer": u["correct"],
            "explanation": {"en": u["explanation"], "th": s["x"]},
        }
        if s.get("code"):
            q["code"] = s["code"]
        questions.append(q)
    for s in spec.get("new", []):
        q = {"id": s["id"], "difficulty": s["d"], "origin": "new", "question": pair(s["q"])}
        if s.get("code"):
            q["code"] = s["code"]
        q.update({"options": [pair(o) for o in s["o"]], "answer": s["a"], "explanation": pair(s["x"])})
        questions.append(q)
    questions.sort(key=lambda q: (ORDER[q["difficulty"]], q["id"]))

    out = ROOT / "src/data/quizzes" / f"{key}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"lesson": key, "source_hash": source_hash, "questions": questions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(questions)} questions)")
