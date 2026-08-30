# src/feature_flags.py
#
# Purpose: Feature-flag helper — recently added to support gradual rollout of
# new product features.  All flags default to enabled so the module works
# out-of-the-box without external configuration.


FEATURES = {
    "new_checkout_summary": True,   # show itemised summary on checkout screen
}


def is_enabled(feature: str) -> bool:
    """Return True if the named feature flag is enabled, False otherwise.

    Unknown feature names return False rather than raising, so callers can
    safely check for features that may not exist in older deployments.
    """
    return FEATURES.get(feature, False)


def get_checkout_summary(items: list[dict]) -> dict:
    """Return a checkout summary for the given list of items.

    Each item dict must have 'name' (str) and 'price' (float) keys.
    This function was added alongside the 'new_checkout_summary' feature flag.
    """
    total = sum(item["price"] for item in items)
    return {
        "item_count": len(items),
        "total": round(total, 2),
        "currency": "USD",
    }
