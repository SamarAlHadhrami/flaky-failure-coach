# tests/test_misleading_naming.py
#
# Purpose: Demonstrates a MISLEADING test — one whose names suggest a timing
# or concurrency problem, but whose failure is caused by a simple, deterministic
# off-by-one logic bug with no randomness or sleeping involved.
#
# Why the names are misleading:
#   - The helper is called wait_for_queue_delay(), implying it blocks on time.
#   - Variables are named delay_budget, elapsed_slots, timeout_threshold — all
#     evocative of timing/concurrency diagnostics.
#   - A triage engineer unfamiliar with the code might immediately suspect a
#     race condition, slow CI runner, or network latency.
#
# Why the test ALWAYS fails (no timing involved):
#   - wait_for_queue_delay() iterates over range(n) and counts how many items
#     it processes, but uses `i` (0-based) instead of `i + 1`, so the returned
#     count is always one less than the number of items passed in.
#   - The assertion checks that all items were processed, so it fails every
#     single run with the same value — this is a pure off-by-one bug.
#
# There is no time.sleep, no random, no threading, no I/O anywhere in this
# file.  The failure is 100% reproducible and unrelated to timing.


QUEUE_TIMEOUT_MS = 500          # misleading: never actually used for sleeping
DEFAULT_DELAY_BUDGET = 10       # misleading: sounds like a timing budget


def wait_for_queue_delay(items: list[int]) -> int:
    """Process every item in the queue and return the count of processed items.

    The name implies a time-bound wait, but this function is synchronous and
    completes instantly.  It contains an off-by-one: it returns `i` at the
    end of the loop rather than `i + 1`, so the reported count is always one
    short of the actual number of items processed.
    """
    elapsed_slots = 0
    for i, _item in enumerate(items):
        elapsed_slots = i          # BUG: should be `i + 1`; last value is len-1

    if not items:
        return 0
    return elapsed_slots


def test_process_delayed_queue():
    """All queued items should be processed before the timeout budget expires.

    The variable names (delay_budget, timeout_threshold, elapsed_slots) look
    like a timing test, but the actual failure is a logic bug: the helper
    returns one fewer than the number of items it processed (off-by-one), so
    the assertion comparing processed count to queue length always fails.

    This test ALWAYS FAILS with the same AssertionError regardless of how many
    times it is run or how fast the machine is.  There is no sleep, no random,
    no I/O — the failure is purely deterministic.
    """
    delay_budget = DEFAULT_DELAY_BUDGET
    timeout_threshold = QUEUE_TIMEOUT_MS

    queued_items = list(range(delay_budget))          # [0, 1, 2, …, 9]
    expected_processed = len(queued_items)            # 10

    elapsed_slots = wait_for_queue_delay(queued_items)

    # elapsed_slots will be 9, not 10, due to the off-by-one in the helper.
    assert elapsed_slots == expected_processed, (
        f"Queue processing stalled before timeout ({timeout_threshold} ms budget): "
        f"expected {expected_processed} items processed, but only "
        f"{elapsed_slots} were recorded.  "
        f"(Hint: this looks like a timing issue but is actually an off-by-one "
        f"in wait_for_queue_delay — it returns `i` instead of `i + 1`.)"
    )
