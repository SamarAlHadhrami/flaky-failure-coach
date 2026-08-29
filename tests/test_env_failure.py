# tests/test_env_failure.py
#
# Purpose: Demonstrates an ENVIRONMENT-DEPENDENT test — one that fails when a
# required environment variable is absent and passes once it is set.
#
# How to reproduce each outcome:
#   Fail  → run pytest normally (DEMO_API_KEY is not set in your shell)
#   Pass  → set the variable first, e.g.:
#             $env:DEMO_API_KEY = "my-secret-key"   # PowerShell
#             export DEMO_API_KEY=my-secret-key      # bash / zsh
#           then re-run pytest.
#
# Real-world relevance:
#   Many CI pipelines fail because secrets or configuration values are
#   missing from the build environment.  This test makes that failure mode
#   explicit and provides a clear error message instead of a cryptic
#   KeyError or AttributeError buried in application code.

import os
import pytest


def test_requires_api_key():
    """Fails with a descriptive error when DEMO_API_KEY is not set.

    Passes as soon as the environment variable is exported in the shell (or
    injected by a CI secrets manager) before running pytest.
    """
    api_key = os.environ.get("DEMO_API_KEY")

    if api_key is None:
        pytest.fail(
            "Environment variable DEMO_API_KEY is not set. "
            "Export it before running this test:\n"
            "  PowerShell : $env:DEMO_API_KEY = 'my-secret-key'\n"
            "  bash/zsh   : export DEMO_API_KEY=my-secret-key"
        )

    # If we reach this point the key is present; verify it is non-empty
    assert api_key.strip(), "DEMO_API_KEY is set but contains only whitespace"

    # Simulate using the key to authenticate against an API
    assert len(api_key) >= 8, (
        f"DEMO_API_KEY looks too short ({len(api_key)} chars); "
        "a real key should be at least 8 characters."
    )
