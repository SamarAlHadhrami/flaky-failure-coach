# Triage Report — `test_process_delayed_queue`

**File:** `tests/test_misleading_naming.py`
**Date:** 2026-08-30

---

## 1. What happened

`test_process_delayed_queue` has failed on every one of its 12 recorded runs with an identical `AssertionError: assert 9 == 10`, caused by a deterministic off-by-one bug in `wait_for_queue_delay()`.

---

## 2. Evidence

| Signal | Detail |
|--------|--------|
| **Flip rate** | 0 % — 0 passes / 12 fails; never passed once |
| **Error type** | `AssertionError` — same value every run (`9 == 10`) |
| **No timing code** | Zero `time.sleep`, `random`, `threading`, or I/O calls in the file |
| **Root cause in source** | `wait_for_queue_delay()` assigns `elapsed_slots = i` inside `enumerate(items)`, so the final value is `len(items) - 1` (i.e. 9 for a 10-item list), not `len(items)` |
| **Misleading names** | `wait_for_queue_delay`, `delay_budget`, `timeout_threshold`, `QUEUE_TIMEOUT_MS` all imply timing, but none of these values affect execution |
| **Assertion message** | Even the error string says *"looks like a timing issue but is actually an off-by-one"* |

---

## 3. Classification

**REAL BUG** — consistent pass-then-fail (here: never-passed) with a clear, identifiable logic defect and no intermittency whatsoever.

---

## 4. Confidence

**HIGH** — multiple independent signals agree:
- 0 % flip rate (no randomness)
- Same numeric mismatch on every run
- Off-by-one is directly visible in source (`elapsed_slots = i` instead of `i + 1`)
- No timing, network, or environment signals present

*(This is a heuristic assessment, not a scientific proof.)*

---

## 5. What to do next

**FIX** the off-by-one in [`wait_for_queue_delay()`](../tests/test_misleading_naming.py#L39):

```python
# Before (buggy)
elapsed_slots = i

# After (correct)
elapsed_slots = i + 1
```

The test assertion and all misleading variable names can remain unchanged — fixing the single line above makes the test pass deterministically.
