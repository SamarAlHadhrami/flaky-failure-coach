# tests/test_flaky_timing.py
#
# Purpose: Demonstrates a FLAKY test — one that fails non-deterministically
# without any code changes between runs.
#
# How the flakiness works:
#   - time.sleep(0.1) simulates the latency of an external API call.
#   - random.random() produces a float in [0.0, 1.0) on every run.
#   - When the value is below 0.40 (≈ 40% of runs) a TimeoutError is raised,
#     mimicking an unreliable network or slow third-party service.
#   - The remaining ≈ 60% of runs the test passes with no code changes.
#
# This pattern is a classic source of CI noise: the test result depends on
# runtime randomness rather than the correctness of the code under test.

import random
import time

import pytest


def simulate_api_call() -> dict:
    """Pretend to call an external API that occasionally times out."""
    time.sleep(0.1)  # simulate network latency

    # Randomly decide whether the "API" responds in time
    if random.random() < 0.40:
        raise TimeoutError("API did not respond within the allowed window")

    return {"status": "ok", "data": 42}


def test_intermittent_api_call():
    """Passes ~60 % of the time; fails with TimeoutError ~40 % of the time.

    No code changes are required to observe both outcomes — just re-run the
    test suite a few times.
    """
    result = simulate_api_call()
    assert result["status"] == "ok"
    assert result["data"] == 42
