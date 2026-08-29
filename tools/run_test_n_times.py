#!/usr/bin/env python3
"""Run a pytest test N times and summarise pass/fail consistency."""

import argparse
import re
import subprocess
import sys


def extract_failure_message(output: str) -> str:
    """Pull the first 'FAILED' summary line, or the last 'E ' traceback line."""
    # Prefer the traceback "E  <msg>" lines — never truncated by pytest.
    # Use the first one (the exception type + message) when available.
    error_lines = re.findall(r"^E\s+(.+)$", output, re.MULTILINE)
    if error_lines:
        return error_lines[0].strip()

    # Fall back to the short summary line "FAILED ... - <msg>" (may be clipped)
    m = re.search(r"^FAILED .+ - (.+)$", output, re.MULTILINE)
    if m:
        return m.group(1).strip()

    return "(no message captured)"


def run_once(test_path: str) -> tuple[bool, str]:
    """Run pytest once. Returns (passed, failure_message)."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path, "-x", "--tb=short", "-q"],
        capture_output=True,
        text=True,
    )
    passed = result.returncode == 0
    message = "" if passed else extract_failure_message(result.stdout + result.stderr)
    return passed, message


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run a pytest test N times and summarise results."
    )
    parser.add_argument(
        "--test",
        required=True,
        metavar="TEST_PATH",
        help="Test path passed to pytest (e.g. tests/test_foo.py::test_bar)",
    )
    parser.add_argument(
        "--n",
        required=True,
        type=int,
        metavar="NUMBER",
        help="Number of times to run the test",
    )
    args = parser.parse_args()

    if args.n < 1:
        print("Error: --n must be at least 1.", file=sys.stderr)
        sys.exit(1)

    passes = 0
    failures = 0
    failure_messages: list[str] = []

    for i in range(1, args.n + 1):
        print(f"  Run {i}/{args.n} ...", end=" ", flush=True)
        passed, message = run_once(args.test)
        if passed:
            passes += 1
            print("PASS")
        else:
            failures += 1
            failure_messages.append(message)
            print(f"FAIL  ({message})")

    # ── Summary ──────────────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Test:    {args.test}")
    print(f"  Runs:    {args.n}")
    print(f"  Passed:  {passes}")
    print(f"  Failed:  {failures}")

    if failures == 0:
        print("  Consistency: all runs passed")
    else:
        unique_messages = set(failure_messages)
        if len(unique_messages) == 1:
            print(f"  Consistency: failures consistent - \"{failure_messages[0]}\"")
        else:
            print(f"  Consistency: failures VARIED across runs ({len(unique_messages)} distinct messages)")
            for msg in sorted(unique_messages):
                count = failure_messages.count(msg)
                print(f"    x{count}  {msg}")


if __name__ == "__main__":
    main()
