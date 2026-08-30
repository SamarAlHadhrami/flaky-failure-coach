# Triage Report — `tests/test_external_dependency.py::test_payment_gateway_call`

> Generated: 2025-05-19 | Heuristic analysis only — not a scientific determination.

---

## 1. What happened

The test intermittently raises `ConnectionError` with no code changes between runs, because it calls an unmocked payment-gateway helper that uses `random.random()` to simulate a ~30 % connection failure rate.

---

## 2. Evidence

| Signal | Detail |
|---|---|
| **History** | 12 runs total — 8 passes, 4 fails. Flip-rate: **72.7 %**. Pattern: alternating pass/fail with no consistent "all-pass then all-fail" breakpoint. |
| **Error type** | Every failure is a `ConnectionError` — no `AssertionError`, no `KeyError`, no environment variable missing. |
| **Code — `random.random()`** | [`call_payment_gateway()`](../tests/test_external_dependency.py#L19) raises `ConnectionError` whenever `random.random() < 0.30`. |
| **Code — network call** | Function is named and documented as an HTTP call to a payment gateway; failure is connection-based, not timing-based (no `time.sleep`). |
| **No code-change correlation** | Failures are spread across 10 days with no cluster after a commit. |

---

## 3. What it's calling it

**EXTERNAL DEPENDENCY** — intermittent failure tied to a (simulated) network call that is not mocked at the HTTP layer.

---

## 4. How confident

**HIGH** — two independent signals agree:
1. Mixed pass/fail history with a consistent `ConnectionError` error type points squarely to an unreliable external call.
2. The source confirms an unmocked probabilistic network simulation (`random.random()`).

> This is a heuristic assessment, not a scientific one.

---

## 5. What to do next

**FIX** (preferred) — mock the payment gateway at the HTTP layer (e.g. `unittest.mock.patch` or `responses` library) so the test controls the response and cannot be affected by real or simulated network conditions.

**QUARANTINE** (interim) — if a mock cannot be added immediately, mark the test with `@pytest.mark.xfail(strict=False, reason="payment gateway flaky — pending mock")` to stop it from blocking CI while the fix is in progress.
