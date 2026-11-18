"""Sanskrit Preprocessing and Unicode Normalisation Module.

Handles Unicode NFC normalisation, BOM removal, whitespace cleanup,
and preservation of Devanagari characters, diacritics, and Sanskrit punctuation.
"""

from __future__ import annotations
import re
import unicodedata
from typing import Final

# Devanagari Unicode Blocks and Character Sets
# U+0900 - U+097F : Devanagari
# U+A8E0 - U+A8FF : Devanagari Extended
# U+1CD0 - U+1CFF : Vedic Extensions
# U+200C (ZWNJ), U+200D (ZWJ) : Zero-width joiner/non-joiner

DEVANAGARI_CHARS_REGEX: Final[str] = (
    r"[\u0900-\u097F\uA8E0-\uA8FF\u1CD0-\u1CFF\u200C\u200D]"
)

# Sanskrit Punctuation: Danda (।) and Double Danda (॥)
SANSKRIT_PUNCTUATION_REGEX: Final[str] = r"[\u0964\u0965]"

# Devanagari Numerals: ० to ९ (\u0966 to \u096F)
DEVANAGARI_DIGITS_REGEX: Final[str] = r"[\u0966-\u096F]"


def normalize_sanskrit_text(text: str, preserve_newlines: bool = True) -> str:
    """Apply Unicode NFC normalisation and clean formatting for Sanskrit text.

    Steps:
    1. Check for empty or None input.
    2. Strip UTF-8 Byte Order Mark (BOM: \\ufeff).
    3. Apply Unicode NFC (Canonical Decomposition, followed by Canonical Composition).
       NFC is crucial for Devanagari so that base consonants and combining matras
       form consistent, canonical Unicode representations.
    4. Replace non-breaking spaces and exotic Unicode whitespace with standard space.
    5. Clean redundant whitespace while preserving valid characters and newlines.
    6. Ensure Sanskrit punctuation (dandas) and diacritics are strictly preserved.

    Args:
        text: Raw Sanskrit string input.
        preserve_newlines: Whether to keep verse/paragraph newlines.

    Returns:
        Clean, NFC-normalised Sanskrit string.
    """
    if not text:
        return ""

    # 1. Remove UTF-8 Byte Order Mark (BOM)
    if text.startswith("\ufeff"):
        text = text[1:]
    text = text.replace("\ufeff", "")

    # 2. Unicode NFC Normalisation
    # NFC is the standard W3C and Unicode recommendation for Devanagari
    normalized = unicodedata.normalize("NFC", text)

    # If text is solely whitespace, return empty string
    if not normalized.strip():
        return ""

    # 3. Normalise special whitespace (NBSP, thin spaces, figure space, etc.)
    # \u00A0: No-break space
    # \u2007: Figure space
    # \u202F: Narrow no-break space
    # \u2009: Thin space
    # \u200B: Zero-width space (turn to standard space or strip)
    space_replacements = {
        "\u00a0": " ",
        "\u2007": " ",
        "\u202f": " ",
        "\u2009": " ",
        "\u200b": " ",
        "\r\n": "\n",
        "\r": "\n",
    }
    for old, new in space_replacements.items():
        normalized = normalized.replace(old, new)

    # 4. Standardise horizontal whitespace
    if preserve_newlines:
        # Collapse multiple horizontal spaces on each line
        lines = normalized.split("\n")
        cleaned_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in lines]
        # Preserve empty lines (paragraphs), but remove excessive blanks (more than 2 consecutive newlines)
        result = "\n".join(cleaned_lines)
        result = re.sub(r"\n{3,}", "\n\n", result)
    else:
        # Collapse all whitespace into single spaces
        result = re.sub(r"\s+", " ", normalized).strip()

    return result


def clean_whitespace(text: str) -> str:
    """Trim and collapse redundant whitespace inside text."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def remove_vedic_accents(text: str) -> str:
    """Optionally strip Vedic svara/accent marks if requested for secular comparison.

    Vedic accents include:
    - U+0951 : Devanagari Stress Sign Udatta
    - U+0952 : Devanagari Stress Sign Anudatta
    - U+0953, U+0954 : Grave and Acute accents
    - U+1CD0 to U+1CFF : Vedic Tone Marks
    """
    if not text:
        return ""
    # Strip combining marks used specifically for Vedic chanting
    text = re.sub(r"[\u0951-\u0954\u1CD0-\u1CFF]", "", text)
    return unicodedata.normalize("NFC", text)
