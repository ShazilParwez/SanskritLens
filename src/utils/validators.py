"""Validation Utilities for SanskritLens.

Validates input lengths, script suitability, and processing options.
"""

from __future__ import annotations
from typing import Any


def validate_input_text(text: str, max_chars: int = 1_000_000) -> tuple[bool, str | None]:
    """Validate input text before initiating NLP analysis.

    Returns:
        (is_valid, error_message)
    """
    if not text or not text.strip():
        return False, "Input text is empty. Please enter, paste, or upload Sanskrit text."

    if len(text) > max_chars:
        return False, f"Input text exceeds the maximum character threshold ({max_chars:,} characters)."

    return True, None


def validate_options(options: dict[str, Any]) -> dict[str, Any]:
    """Ensure options dict contains sanitized, type-safe parameters."""
    opts = options.copy() if options else {}

    # Ensure mode is recognized
    mode = opts.get("mode", "standard")
    if mode not in ("standard", "normalised", "custom"):
        opts["mode"] = "standard"

    # Ensure min token length is valid positive integer
    min_len = opts.get("min_token_length", 1)
    try:
        min_len = max(1, int(min_len))
    except (ValueError, TypeError):
        min_len = 1
    opts["min_token_length"] = min_len

    return opts

