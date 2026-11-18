"""Unit Tests for Sanskrit Preprocessing and Unicode Normalisation."""

import unicodedata
import pytest
from src.nlp.preprocessing import normalize_sanskrit_text, clean_whitespace, remove_vedic_accents


def test_nfc_normalization():
    """Verify that Devanagari text is normalized using Unicode NFC."""
    # Decomposed form (NFD): base consonant + separate combining sign
    raw = "क" + "\u093e"  # ka + aa matra in NFD
    norm = normalize_sanskrit_text(raw)
    assert unicodedata.is_normalized("NFC", norm)
    assert norm == "का"


def test_utf8_bom_removal():
    """Verify that leading UTF-8 Byte Order Mark (\ufeff) is stripped."""
    text_with_bom = "\ufeffधर्मक्षेत्रे कुरुक्षेत्रे"
    cleaned = normalize_sanskrit_text(text_with_bom)
    assert not cleaned.startswith("\ufeff")
    assert cleaned == "धर्मक्षेत्रे कुरुक्षेत्रे"


def test_nbsp_and_whitespace_cleaning():
    """Verify non-breaking spaces and redundant whitespace are cleaned."""
    text = "सत्यम्\u00a0ब्रूयात्    प्रियम्\u202fब्रूयात्"
    cleaned = normalize_sanskrit_text(text, preserve_newlines=False)
    assert cleaned == "सत्यम् ब्रूयात् प्रियम् ब्रूयात्"


def test_preservation_of_sanskrit_diacritics():
    """Ensure anusvara, visarga, chandrabindu, virama, and matras are preserved."""
    sample = "ॐ नमः शिवाय् हँसः क्रतो स्मरँ"
    norm = normalize_sanskrit_text(sample)
    assert "ः" in norm  # Visarga
    assert "्" in norm  # Virama
    assert "ँ" in norm  # Chandrabindu
    assert "ं" in norm or "ँ" in norm


def test_danda_preservation():
    """Ensure Sanskrit punctuation marks (। and ॥) are kept in normalized text."""
    sample = "अशोच्यानन्वशोचस्त्वं भाषसे। गतासूनगतासूंश्च नानुशोचन्ति पण्डिताः॥"
    norm = normalize_sanskrit_text(sample)
    assert "।" in norm
    assert "॥" in norm


def test_empty_and_whitespace_only():
    """Verify robust handling of empty and whitespace-only strings."""
    assert normalize_sanskrit_text("") == ""
    assert normalize_sanskrit_text("   \n\t  ") == ""
    assert normalize_sanskrit_text(None) == ""


def test_vedic_accent_removal():
    """Verify optional removal of Vedic svara accents."""
    vedic_text = "अ॒ग्निमी॑ळे"
    stripped = remove_vedic_accents(vedic_text)
    assert stripped == "अग्निमीळे"

