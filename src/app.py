# src/app.py
#
# Purpose: Application logic module for the pytest demo.
#
# This module contains a calculate_discount function with a deliberate bug:
# members should receive a 10% discount (multiplier 0.90), but the code
# mistakenly applies only a 1% discount (multiplier 0.99).
# This causes test_real_regression.py to fail consistently every run.


def calculate_discount(price: float, is_member: bool) -> float:
    """Return the discounted price for a given customer.

    Members are *intended* to receive 10% off, but due to a typo the
    multiplier is 0.99 (1% off) instead of the correct 0.90 (10% off).
    """
    if is_member:
        # BUG: should be 0.90 to give 10% off; 0.99 only gives 1% off
        return price * 0.99
    return price
