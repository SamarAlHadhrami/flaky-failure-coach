# Timing Comparison: Manual vs Bob-Assisted Triage

> These are real, manually measured timings, not estimates.

## Results by Test Case

| Test | Manual (baseline) | Bob-assisted | Bob faster by |
|---|---|---|---|
| Flaky test | 54.03s | 48.00s | 6.03s |
| Real regression | 53.86s | 51.35s | 2.51s |
| Environment failure | 54.85s | 42.08s | 12.77s |
| External dependency | 50.47s | 42.00s | 8.47s |
| Insufficient evidence | 46.70s | 40.00s | 6.70s |

## Summary

Bob was faster on **every single test case**.

- **Average manual time:** 51.98s
- **Average Bob-assisted time:** 44.69s
- **Overall improvement:** ~14.0% faster with Bob-assisted triage
