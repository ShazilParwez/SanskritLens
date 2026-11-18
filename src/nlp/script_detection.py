"""Script Detection Module for SanskritLens.

Analyzes character distribution across Unicode blocks to detect Devanagari,
Latin (transliteration), numerals, punctuation, and mixed scripts.
"""

from __future__ import annotations
import unicodedata
from typing import TypedDict


class ScriptDistribution(TypedDict):
    devanagari_count: int
    devanagari_pct: float
    latin_count: int
    latin_pct: float
    digit_devanagari_count: int
    digit_latin_count: int
    digits_total_count: int
    digits_pct: float
    sanskrit_punct_count: int
    general_punct_count: int
    punct_total_count: int
    punct_pct: float
    whitespace_count: int
    whitespace_pct: float
    other_count: int
    other_pct: float
    total_characters: int
    primary_script: str
    is_primarily_devanagari: bool
    warning: str | None


def detect_script(text: str) -> ScriptDistribution:
    """Analyze character composition of text to identify scripts and Unicode blocks.

    Distinguishes:
    - Devanagari letters, matras, virama, anusvara, visarga (U+0900-U+097F, U+A8E0-U+A8FF, U+1CD0-U+1CFF)
    - Latin letters (A-Z, a-z, and extended Latin diacritics used in IAST like ā, ī, ū, ṛ, ṝ, ḷ, ṃ, ḥ, ṅ, ñ, ṭ, ḍ, ṇ, ś, ṣ)
    - Devanagari numerals (०-९)
    - Western numerals (0-9)
    - Sanskrit punctuation (।, ॥)
    - General punctuation and symbols
    - Whitespace and other characters

    Returns:
        ScriptDistribution dictionary containing counts, percentages, primary script,
        and helpful linguistic advisory messages.
    """
    total = len(text)
    if total == 0:
        return {
            "devanagari_count": 0,
            "devanagari_pct": 0.0,
            "latin_count": 0,
            "latin_pct": 0.0,
            "digit_devanagari_count": 0,
            "digit_latin_count": 0,
            "digits_total_count": 0,
            "digits_pct": 0.0,
            "sanskrit_punct_count": 0,
            "general_punct_count": 0,
            "punct_total_count": 0,
            "punct_pct": 0.0,
            "whitespace_count": 0,
            "whitespace_pct": 0.0,
            "other_count": 0,
            "other_pct": 0.0,
            "total_characters": 0,
            "primary_script": "Empty",
            "is_primarily_devanagari": False,
            "warning": "Input text is empty.",
        }

    devanagari_count = 0
    latin_count = 0
    digit_devanagari = 0
    digit_latin = 0
    sanskrit_punct = 0
    general_punct = 0
    whitespace_count = 0
    other_count = 0

    for char in text:
        cp = ord(char)
        cat = unicodedata.category(char)

        if char.isspace():
            whitespace_count += 1
        elif char in ("\u0964", "\u0965"):  # Danda or Double Danda
            sanskrit_punct += 1
        elif 0x0966 <= cp <= 0x096F:  # Devanagari digits
            digit_devanagari += 1
        elif (
            0x0900 <= cp <= 0x097F
            or 0xA8E0 <= cp <= 0xA8FF
            or 0x1CD0 <= cp <= 0x1CFF
            or char in ("\u200C", "\u200D")
        ):
            devanagari_count += 1
        elif ("A" <= char <= "Z") or ("a" <= char <= "z") or (
            0x00C0 <= cp <= 0x024F or 0x1E00 <= cp <= 0x1EFF
        ):  # Latin and Latin Extended (including IAST)
            latin_count += 1
        elif "0" <= char <= "9":
            digit_latin += 1
        elif cat.startswith("P") or cat.startswith("S"):
            general_punct += 1
        else:
            other_count += 1

    digits_total = digit_devanagari + digit_latin
    punct_total = sanskrit_punct + general_punct

    # Calculate percentages
    dev_pct = round((devanagari_count / total) * 100, 2)
    latin_pct = round((latin_count / total) * 100, 2)
    digits_pct = round((digits_total / total) * 100, 2)
    punct_pct = round((punct_total / total) * 100, 2)
    ws_pct = round((whitespace_count / total) * 100, 2)
    other_pct = round((other_count / total) * 100, 2)

    # Effective content characters excluding whitespace and punctuation
    content_chars = devanagari_count + latin_count + digits_total + other_count

    warning = None
    if content_chars == 0:
        primary_script = "Punctuation/Whitespace Only"
        is_primarily_devanagari = False
        warning = "The text contains only whitespace or punctuation marks."
    else:
        dev_content_ratio = devanagari_count / content_chars
        latin_content_ratio = latin_count / content_chars

        if dev_content_ratio >= 0.70:
            primary_script = "Devanagari"
            is_primarily_devanagari = True
            if latin_count > 0:
                warning = f"Notice: Text is predominantly Devanagari ({dev_pct}%), with {latin_count} Latin character(s) present."
        elif latin_content_ratio >= 0.70:
            primary_script = "Latin (Possible Transliteration / IAST)"
            is_primarily_devanagari = False
            warning = (
                f"Warning: Text appears to be in Latin script ({latin_pct}%), such as IAST or Romanized Sanskrit. "
                "SanskritLens is optimized for native Devanagari script. Standard Sanskrit tokenisation operates best on Devanagari."
            )
        elif devanagari_count > 0 and latin_count > 0:
            primary_script = "Mixed (Devanagari & Latin)"
            is_primarily_devanagari = False
            warning = (
                f"Notice: Mixed script detected ({devanagari_count} Devanagari vs {latin_count} Latin characters). "
                "Both scripts will be analyzed, but Devanagari linguistic patterns are prioritized."
            )
        elif digits_total > content_chars * 0.5:
            primary_script = "Numerals"
            is_primarily_devanagari = False
            warning = "Notice: The text consists predominantly of numbers."
        else:
            primary_script = "Other / Non-Devanagari"
            is_primarily_devanagari = False
            warning = "Notice: Non-Devanagari script detected."

    return {
        "devanagari_count": devanagari_count,
        "devanagari_pct": dev_pct,
        "latin_count": latin_count,
        "latin_pct": latin_pct,
        "digit_devanagari_count": digit_devanagari,
        "digit_latin_count": digit_latin,
        "digits_total_count": digits_total,
        "digits_pct": digits_pct,
        "sanskrit_punct_count": sanskrit_punct,
        "general_punct_count": general_punct,
        "punct_total_count": punct_total,
        "punct_pct": punct_pct,
        "whitespace_count": whitespace_count,
        "whitespace_pct": ws_pct,
        "other_count": other_count,
        "other_pct": other_pct,
        "total_characters": total,
        "primary_script": primary_script,
        "is_primarily_devanagari": is_primarily_devanagari,
        "warning": warning,
    }

