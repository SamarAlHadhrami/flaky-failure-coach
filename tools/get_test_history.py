#!/usr/bin/env python3
"""CLI tool to display test history stats from test_history.json."""

import argparse
import json
import sys
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent.parent / "test_history.json"


def compute_flip_rate(outcomes: list[str]) -> float:
    """Return the percentage of consecutive run-pairs where the result changed."""
    if len(outcomes) < 2:
        return 0.0
    flips = sum(1 for a, b in zip(outcomes, outcomes[1:]) if a != b)
    return flips / (len(outcomes) - 1) * 100


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Show test history stats from test_history.json"
    )
    parser.add_argument(
        "--test",
        required=True,
        metavar="TEST_PATH",
        help="Test key as it appears in test_history.json "
             "(e.g. tests/test_foo.py::test_bar)",
    )
    args = parser.parse_args()

    if not HISTORY_FILE.exists():
        print(f"Error: {HISTORY_FILE} not found.", file=sys.stderr)
        sys.exit(1)

    with HISTORY_FILE.open() as f:
        history: dict = json.load(f)

    if args.test not in history:
        print(f"Error: test '{args.test}' not found in history.", file=sys.stderr)
        sys.exit(1)

    runs = history[args.test]
    total_runs = len(runs)
    num_passes = sum(1 for r in runs if r["result"] == "pass")
    num_fails = total_runs - num_passes
    outcomes = [r["result"] for r in runs]
    flip_rate = compute_flip_rate(outcomes)

    print(f"Test:        {args.test}")
    print(f"Total runs:  {total_runs}")
    print(f"Passes:      {num_passes}")
    print(f"Fails:       {num_fails}")
    print(f"Flip rate:   {flip_rate:.1f}%")
    print()
    print("Last 5 outcomes:")
    for run in runs[-5:]:
        error = run["error_type"] if run["error_type"] is not None else "none"
        print(f"  [{run['result']:4}]  error_type: {error}")


if __name__ == "__main__":
    main()
