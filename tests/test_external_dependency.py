# tests/test_external_dependency.py
#
# Purpose: Demonstrates a FLAKY test caused by an unreliable external dependency
# — specifically, a payment gateway that drops connections intermittently.
#
# How the flakiness works:
#   - random.random() produces a float in [0.0, 1.0) on every run.
#   - When the value is below 0.30 (≈ 30% of runs) a ConnectionError is raised,
#     mimicking a payment gateway that refuses or drops the TCP connection.
#   - No time.sleep() is used — the failure mode is network/connection-specific,
#     not timing-specific, making it clearly distinct from test_flaky_timing.py.
#
# This pattern is common when tests depend on third-party payment providers
# (Stripe, PayPal, etc.) without proper mocking at the HTTP layer.

import random


def call_payment_gateway() -> dict:
    """Simulate an HTTP call to a payment gateway that fails ~30% of the time.

    The failure is a ConnectionError (e.g. the gateway refused the TCP
    connection or the socket was reset), not a timeout — there is no delay.
    """
    # Simulate an unreliable network connection to the payment provider.
    # No time.sleep: the failure is connection-based, not latency-based.
    if random.random() < 0.30:
        raise ConnectionError(
            "Payment gateway refused the connection (network error)"
        )

    return {"status": "success", "transaction_id": "txn_abc123", "amount": 99.99}


def test_payment_gateway_call():
    """Passes ~70% of the time; fails with ConnectionError ~30% of the time.

    Re-run the test suite multiple times without any code changes to observe
    both outcomes — the randomness comes from the simulated network, not logic.
    """
    result = call_payment_gateway()
    assert result["status"] == "success"
    assert "transaction_id" in result
