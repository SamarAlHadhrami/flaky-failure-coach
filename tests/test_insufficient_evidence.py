# tests/test_insufficient_evidence.py
#
# Purpose: Demonstrates a test with INSUFFICIENT HISTORY to judge its
# reliability — it covers a brand-new feature that was just merged and has
# only been run a handful of times.
#
# Why this scenario matters:
#   - The flaky-failure coach classifies failures partly on run history.
#   - When a test is new, there is no historical baseline: we cannot tell
#     whether one failure means "genuinely flaky" or "real regression" because
#     we simply haven't accumulated enough data points yet.
#   - The correct recommendation is: "collect more runs before drawing
#     conclusions" — not to quarantine or fix immediately.
#
# The feature under test (get_checkout_summary / is_enabled) is correct and
# fully deterministic.  This test will pass on every run; it is not flaky.
# The "insufficient evidence" label applies to the *history* context, not to
# any fault in the code.

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.feature_flags import get_checkout_summary, is_enabled


def test_new_feature_check():
    """Verify the new checkout-summary feature flag and its summary helper.

    This test was added alongside the feature itself and has very few runs
    in the history store — not enough to classify any failure as flaky vs.
    a real regression.  The code is correct; the test always passes.
    """
    # The feature flag should be enabled by default
    assert is_enabled("new_checkout_summary") is True

    # The summary helper should correctly aggregate a small basket
    items = [
        {"name": "Widget A", "price": 9.99},
        {"name": "Widget B", "price": 4.50},
        {"name": "Widget C", "price": 15.00},
    ]
    summary = get_checkout_summary(items)

    assert summary["item_count"] == 3
    assert summary["total"] == 29.49
    assert summary["currency"] == "USD"
