---
name: flaky-triage
description: >-
  Investigates a failing pytest test using history, logs, and code to classify
  it as flaky, a real bug, an environment problem, or an external dependency
  issue, then recommends a next action.
---

When the user reports a failing test (by name, or by pasting a failure log), do the following in order:
1. Identify the exact test name and file path.
2. Run: python tools/get_test_history.py --test <full_test_path> — and read the flip-rate and recent outcomes.
3. Read the test's source code and the most recent failure log.
4. Look for signals: time.sleep or random (timing), network/HTTP calls (external dependency), missing env vars / KeyError (environment), plain AssertionError with no other pattern (regression).
5. If the flip-rate is between 20% and 70% and there is no clear regression signal, run: python tools/run_test_n_times.py --test <full_test_path> --n 5 — and use the result as a tie-breaker.
6. Classify using exactly this table: (a) mixed pass/fail history + timing code = FLAKY, recommend QUARANTINE. (b) consistent pass-then-fail after a code change = REAL BUG, recommend FIX. (c) consistent failure from a missing env var = ENVIRONMENT PROBLEM, recommend ESCALATE. (d) intermittent failure tied to a network call = EXTERNAL DEPENDENCY, recommend FIX or QUARANTINE. (e) too little history to tell = NOT ENOUGH INFO, recommend ESCALATE.
7. Assign confidence: HIGH if 2+ signals agree, MEDIUM if 1 clear signal, LOW if signals disagree. State clearly this is heuristic, not scientific.
8. Write a markdown report to reports/<test_name>_triage.md with exactly 5 short parts: (1) What happened — one sentence, (2) Evidence — the history + code clues used, (3) What it's calling it — from the table above, (4) How confident — high/medium/low, (5) What to do next — fix/rerun/quarantine/escalate.
9. Show the same 5-part summary in chat as well.
