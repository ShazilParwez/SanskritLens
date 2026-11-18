"""Unit Tests for Script Detection."""

import pytest
from src.nlp.script_detection import detect_script


def test_pure_devanagari_detection():
    """Verify detection of pure Devanagari Sanskrit text."""
    text = "अशोच्यानन्वशोचस्त्वं प्रज्ञावादांश्च भाषसे।"
    res = detect_script(text)
    assert res["primary_script"] == "Devanagari"
    assert res["is_primarily_devanagari"] is True
    assert res["devanagari_count"] > 0
    assert res["latin_count"] == 0


def test_latin_transliteration_detection():
    """Verify detection when user provides Latin script (IAST or English)."""
    text = "dharmakṣetre kurukṣetre samavetā yuyutsavaḥ"
    res = detect_script(text)
    assert "Latin" in res["primary_script"]
    assert res["is_primarily_devanagari"] is False
    assert res["warning"] is not None


def test_mixed_script_detection():
    """Verify detection of mixed Devanagari and Latin text."""
    text = "Gita Chapter 2: अशोच्यानन्वशोचस्त्वम्"
    res = detect_script(text)
    assert res["primary_script"] == "Mixed (Devanagari & Latin)"
    assert res["devanagari_count"] > 0
    assert res["latin_count"] > 0


def test_empty_text_script_detection():
    """Verify script detection handles empty and punctuation strings safely."""
    empty_res = detect_script("")
    assert empty_res["primary_script"] == "Empty"
    assert empty_res["total_characters"] == 0

    punct_res = detect_script("। ॥ , . ! ?")
    assert punct_res["primary_script"] == "Punctuation/Whitespace Only"

