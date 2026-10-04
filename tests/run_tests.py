#!/usr/bin/env python3
"""Runs skill_check.py over the fixtures and checks the results. Standard library only.  python3 tests/run_tests.py"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK, FX = os.path.join(ROOT, "skill_check.py"), os.path.join(ROOT, "fixtures")
EXPECT = {  # fixture: (errors, minimum warnings, text that must appear, rule id that must appear)
    "good-skill": (0, 0, None, None),
    "bad-yaml-colon": (1, 0, "unquoted ': '", "SC002"),
    "coupled-skill": (0, 6, "WebFetch", "SC010"),
    "broken-links": (2, 1, "broken link", "SC015"),
}
bad = 0
def run(args): return subprocess.run([sys.executable, CHECK] + args, capture_output=True, text=True)
for name, (errs, warns, text, rid) in EXPECT.items():
    r = run([os.path.join(FX, name, "SKILL.md"), "--json"])
    s = json.loads(r.stdout)["skills"][0]; blob = json.dumps(s)
    ok = len(s["errors"]) == errs and len(s["warnings"]) >= warns and (text is None or text in blob) and (rid is None or f"[{rid}]" in blob) and r.returncode == (1 if errs else 0)
    print(("PASS " if ok else "FAIL ") + f"{name}: {len(s['errors'])} error(s), {len(s['warnings'])} warning(s), exit {r.returncode}")
    bad += not ok
r = run([os.path.join(FX, "coupled-skill", "SKILL.md"), "--strict"]); ok = r.returncode == 1
print(("PASS " if ok else "FAIL ") + "--strict makes warnings fail the run"); bad += not ok
r = run([os.path.join(FX, "bad-yaml-colon", "SKILL.md"), "--ignore", "SC002,SC013"]); ok = r.returncode == 0 and "[SC002]" not in r.stdout
print(("PASS " if ok else "FAIL ") + "--ignore SC002,SC013 removes those rules and the error"); bad += not ok
r = run([FX]); ok = r.returncode == 2 and "no SKILL.md found" in r.stdout
print(("PASS " if ok else "FAIL ") + "a folder with .skill-check-ignore is skipped"); bad += not ok
sys.exit(1 if bad else 0)
