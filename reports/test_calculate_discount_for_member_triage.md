# Triage Report — `test_calculate_discount_for_member`

**Test:** `tests/test_real_regression.py::test_calculate_discount_for_member`  
**Date:** 2025-07-01

---

## 1. What happened

The test consistently fails because `calculate_discount()` in `src/app.py` applies a 1% discount (`price * 0.99`) instead of the specified 10% discount (`price * 0.90`), causing it to return `$99.00` when `$90.00` is expected.

---

## 2. Evidence

- **History (12 runs):** 9 passes, 3 fails — flip rate 9.1%, but the **last 3 runs are all failures**, indicating a regression that was introduced at some point and has stayed broken.
- **Error type:** `AssertionError` on every failing run — no network errors, no `KeyError`, no timeout signals.
- **Source code signal:** [`src/app.py:19`](../src/app.py) contains a documented typo — `return price * 0.99` should be `return price * 0.90`.
- **No flakiness signals:** No `time.sleep`, no `random`, no HTTP/network calls, no environment-variable lookups.

---

## 3. What it's calling it

**REAL BUG**

---

## 4. How confident

**HIGH** — Two independent signals agree: (a) consistent tail-end failures in run history, and (b) a clear, identifiable defect in the source code. No conflicting signals. *(Heuristic assessment, not scientific.)*

---

## 5. What to do next

**FIX** — Change `price * 0.99` to `price * 0.90` on line 19 of [`src/app.py`](../src/app.py). The fix is one character and the test will pass immediately. No quarantine needed.
