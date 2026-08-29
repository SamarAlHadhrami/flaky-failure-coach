# Triage Report: `tests/test_env_failure.py::test_requires_api_key`

_Generated: 2025-05-18_

---

## 1. What happened

The test has failed every single run (12/12) because the required environment variable `DEMO_API_KEY` is never set in the execution environment.

---

## 2. Evidence

| Signal | Detail |
|---|---|
| **History** | 12 runs, 0 passes, 12 fails — flip rate 0.0% |
| **Error type** | `EnvMissing` on every run (consistent, not random) |
| **Code** | `os.environ.get("DEMO_API_KEY")` → calls `pytest.fail()` explicitly when the var is `None` |
| **No timing code** | No `time.sleep`, no `random` — not a timing/flakiness issue |
| **No network calls** | No HTTP/socket usage — not an external dependency issue |
| **Date range** | 2025-05-07 → 2025-05-18: failure predates any recent code changes in the test itself |

---

## 3. What it's calling it

**ENVIRONMENT PROBLEM**

Consistent failure caused by a missing required environment variable (`DEMO_API_KEY`) that has never been injected into the CI/test environment.

---

## 4. How confident

**HIGH** — Two independent signals agree: (a) 100% consistent `EnvMissing` failure across 12 runs with zero passes, and (b) the test source directly and explicitly fails on `os.environ.get("DEMO_API_KEY") is None`. There is no ambiguity.

_Note: This is a heuristic classification, not a scientific determination._

---

## 5. What to do next

**ESCALATE** to the team/CI owner responsible for secrets management.

- Add `DEMO_API_KEY` as a CI secret in the pipeline (GitHub Actions: `Settings → Secrets`, Jenkins: credentials store, etc.).
- Ensure the secret is injected as an environment variable before the pytest step runs.
- Do **not** quarantine or skip this test — it is correctly written and will pass once the environment is fixed.
- Optionally, mark the test with `@pytest.mark.skipif(os.environ.get("DEMO_API_KEY") is None, reason="DEMO_API_KEY not set")` as a temporary measure to unblock CI, but treat that as a short-term workaround only.
