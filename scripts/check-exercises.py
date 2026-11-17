#!/usr/bin/env python3
"""Validate every hands-on exercise with the same checker the browser uses.

For each src/data/exercises/<phase>/<lesson>/<level>/:
  - solution.py must pass every check (visible and hidden)
  - starter.py must fail at least one check (otherwise the exercise is already solved)
  - every mutants/*.py (deliberately wrong answers) must fail at least one check

Usage: python3 scripts/check-exercises.py [path-filter]
"""
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("harness", ROOT / "public" / "py" / "harness.py")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)

flt = sys.argv[1] if len(sys.argv) > 1 else ""
problems = 0
count = 0


def summary(res):
    if "error" in res:
        return False, "error: " + res["error"].splitlines()[-1]
    fails = [r for r in res["results"] if not r["ok"]]
    return not fails, ", ".join(f'{r["id"]}: {r["en"]}' for r in fails)


for level_dir in sorted((ROOT / "src" / "data" / "exercises").glob("*/*/*")):
    if not (level_dir / "tests.py").exists() or flt not in str(level_dir):
        continue
    count += 1
    tests = (level_dir / "tests.py").read_text(encoding="utf-8")
    name = level_dir.relative_to(ROOT / "src" / "data" / "exercises")

    ok, why = summary(harness.run_checks((level_dir / "solution.py").read_text(encoding="utf-8"), tests))
    if not ok:
        problems += 1
        print(f"FAIL {name}: solution does not pass -> {why}")

    ok, _ = summary(harness.run_checks((level_dir / "starter.py").read_text(encoding="utf-8"), tests))
    if ok:
        problems += 1
        print(f"FAIL {name}: starter already passes every check")

    for mutant in sorted((level_dir / "mutants").glob("*.py")):
        ok, why = summary(harness.run_checks(mutant.read_text(encoding="utf-8"), tests))
        if ok:
            problems += 1
            print(f"FAIL {name}: mutant {mutant.name} is not caught")
        else:
            print(f"  ok {name}: mutant {mutant.name} caught ({why[:90]})")

print(f"{count} exercise(s) checked, {problems} problem(s)")
sys.exit(1 if problems else 0)
