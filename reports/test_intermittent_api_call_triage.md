# Triage Report — `tests/test_flaky_timing.py::test_intermittent_api_call`

_Generated: 2025-05-18_

---

## 1. What happened

The test has been alternating between pass and fail across 12 CI runs with no code changes, always raising `TimeoutError` on failure.

---

## 2. Evidence

| Signal | Detail |
|--------|--------|
| **Run history** | 12 runs — 8 passes, 4 fails (flip-rate 72.7%); failures scattered across days, no "break point" |
| **Failure type** | Always `TimeoutError`; never an `AssertionError` or import error |
| **`time.sleep(0.1)`** | Explicit latency simulation in `simulate_api_call()` ([`tests/test_flaky_timing.py:24`](../tests/test_flaky_timing.py)) |
| **`random.random() < 0.40`** | Hard-coded 40% failure probability — outcome is non-deterministic by design ([`tests/test_flaky_timing.py:27`](../tests/test_flaky_timing.py)) |
| **No env vars / no real network** | No missing environment variables, no actual HTTP call — pure in-process randomness |

---

## 3. What it's calling it

**FLAKY** — mixed pass/fail history combined with explicit timing code (`time.sleep`) and a random-outcome trigger (`random.random()`). Matches table entry *(a)*: _mixed pass/fail history + timing code_.

---

## 4. How confident

**HIGH** — three independent signals converge on the same conclusion: the history pattern is non-monotonic, the source code contains deliberate randomness, and every failure carries the same `TimeoutError` consistent with a simulated timeout. _(This is a heuristic assessment, not a scientific proof.)_

---

## 5. What to do next

**QUARANTINE** this test immediately:

1. Add `@pytest.mark.skip(reason="flaky: intermittent TimeoutError — tracked in #<issue>")` or move it to a dedicated `flaky` suite so it no longer blocks CI.
2. Open a tracking issue noting the root cause: `simulate_api_call` uses `random.random()` to introduce artificial non-determinism. The fix is to either mock the randomness in the test (inject a seeded `random.Random`) or redesign the test to assert on the function's contract rather than its probabilistic timing behaviour.
3. Re-enable the test once a deterministic version is in place and verified green across ≥ 10 consecutive runs.
