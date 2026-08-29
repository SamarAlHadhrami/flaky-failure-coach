# tests/test_real_regression.py
#
# Purpose: Demonstrates a REAL (non-flaky) regression test — one that fails
# consistently on every run because of a genuine bug in the source code.
#
# Why it always fails:
#   - The specification says members get 10% off, so a $100 item should cost
#     $90.00 after the discount.
#   - calculate_discount in src/app.py mistakenly multiplies by 0.99 instead
#     of 0.90, so it returns $99.00.
#   - The assertion below checks for the *correct* value ($90.00), so it will
#     fail every single run until the bug in app.py is fixed.
#
# This is the kind of failure a developer should fix immediately; it is not
# a flaky test — the result is 100% reproducible.

import sys
import os

# Allow imports from the project root so `src.app` resolves correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.app import calculate_discount


def test_calculate_discount_for_member():
    """A member buying a $100 item should pay $90.00 (10% discount).

    This test ALWAYS FAILS because the current code applies only 1% off
    (returning $99.00).  Fix the bug in src/app.py to make it pass.
    """
    price = 100.00
    discounted = calculate_discount(price, is_member=True)

    # Correct expectation: 10% off → $90.00
    assert discounted == 90.00, (
        f"Expected $90.00 for a member discount of 10%, but got ${discounted:.2f}. "
        "The code is applying the wrong discount rate."
    )
