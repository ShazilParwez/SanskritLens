"""Unit Tests for Sanskrit Tokenizer."""

import pytest
from src.nlp.tokenizer import tokenize_sanskrit, segment_sentences


def test_official_gita_verse_tokenization():
    """Verify official project test case:

    Input: धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।
    Expected: धर्मक्षेत्रे, कुरुक्षेत्रे, समवेता, युयुत्सवः (excluding danda).
    """
    input_text = "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।"
    tokens = tokenize_sanskrit(input_text)
    expected = ["धर्मक्षेत्रे", "कुरुक्षेत्रे", "समवेता", "युयुत्सवः"]
    assert tokens == expected
    assert "।" not in tokens


def test_double_danda_and_verse_numerals():
    """Verify that double danda and verse numbers are excluded from lexical tokens."""
    input_text = "गतासूनगतासूंश्च नानुशोचन्ति पण्डिताः॥ १॥"
    tokens = tokenize_sanskrit(input_text, options={"exclude_numerals": True})
    assert tokens == ["गतासूनगतासूंश्च", "नानुशोचन्ति", "पण्डिताः"]
    assert "॥" not in tokens
    assert "१" not in tokens


def test_avagraha_preservation():
    """Verify that avagraha (ऽ) is preserved within tokens (e.g. सोऽमृतत्वाय)."""
    input_text = "सोऽमृतत्वाय कल्पते।"
    tokens = tokenize_sanskrit(input_text)
    assert tokens == ["सोऽमृतत्वाय", "कल्पते"]
    assert "सोऽमृतत्वाय" in tokens


def test_compound_hyphen_tokenization():
    """Verify handling of hyphenated Sanskrit compounds."""
    input_text = "मित्र-भेद-शास्त्रम्"
    tokens = tokenize_sanskrit(input_text)
    assert tokens == ["मित्र-भेद-शास्त्रम्"]


def test_tokenization_modes():
    """Verify Mode A, Mode B, and Mode C tokenization configurations."""
    text = "रामः 123 Krishna! ॥ २॥"

    # Mode A (Standard): Numerals excluded by default for word frequency
    toks_a = tokenize_sanskrit(text, options={"mode": "standard"})
    assert "रामः" in toks_a
    assert "Krishna" in toks_a

    # Mode B (Normalised): Latin lowercased
    toks_b = tokenize_sanskrit(text, options={"mode": "normalised"})
    assert "krishna" in toks_b
    assert "123" not in toks_b

    # Mode C (Custom with min_length)
    toks_c = tokenize_sanskrit(
        "क च रामः",
        options={"mode": "custom", "min_token_length": 2},
    )
    assert "रामः" in toks_c
    assert "क" not in toks_c
    assert "च" not in toks_c


def test_sentence_verse_segmentation():
    """Verify segmentation by danda (।) and double danda (॥)."""
    text = "विद्या ददाति विनयं विनयाद्याति पात्रताम्। पात्रत्वाद्धनमाप्नोति धनाद्धर्मं ततः सुखम्॥"
    segments = segment_sentences(text)
    assert len(segments) == 2
    assert "विद्या ददाति विनयं विनयाद्याति पात्रताम्" in segments[0]
    assert "पात्रत्वाद्धनमाप्नोति धनाद्धर्मं ततः सुखम्" in segments[1]


def test_empty_and_whitespace_input():
    """Verify empty and whitespace inputs return empty list."""
    assert tokenize_sanskrit("") == []
    assert tokenize_sanskrit("   \n\t  ") == []
    assert tokenize_sanskrit("।।॥॥") == []

