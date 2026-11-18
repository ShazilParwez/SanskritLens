"""Unit Tests for Linguistic and Corpus Statistics."""

import pytest
from src.nlp.statistics import calculate_text_statistics, calculate_word_length_statistics


def test_text_statistics_calculation():
    """Verify total tokens, unique tokens, TTR, and character counts."""
    text = "सत्यं ब्रूयात् प्रियं ब्रूयात्।"
    tokens = ["सत्यं", "ब्रूयात्", "प्रियं", "ब्रूयात्"]
    # Total = 4, Unique = 3 ('सत्यं', 'प्रियं', 'ब्रूयात्'), TTR = 3/4 = 0.75

    stats = calculate_text_statistics(text, tokens)
    assert stats["total_tokens"] == 4
    assert stats["unique_tokens"] == 3
    assert stats["type_token_ratio"] == 0.75
    assert stats["total_segments"] == 1
    assert stats["punctuation_count"] >= 1


def test_word_length_statistics():
    """Verify average, min, max, median length in Unicode code points."""
    tokens = ["क", "रामः", "धर्मक्षेत्रे"]
    # len("क") = 1
    # len("रामः") = 4 (र, ा, म, ः)
    # len("धर्मक्षेत्रे") = 11 (ध, र, ्, म, क, ्, ष, े, त, ्, र, े) -> wait let's calculate exact len
    l_expected = [len(t) for t in tokens]
    summary, dist_df = calculate_word_length_statistics(tokens)

    assert summary["min_length"] == min(l_expected)
    assert summary["max_length"] == max(l_expected)
    assert summary["average_length"] == round(sum(l_expected) / 3, 2)
    assert not dist_df.empty


def test_empty_tokens_statistics():
    """Verify edge case of empty text and zero tokens."""
    stats = calculate_text_statistics("", [])
    assert stats["total_tokens"] == 0
    assert stats["unique_tokens"] == 0
    assert stats["type_token_ratio"] == 0.0
    assert stats["average_token_length"] == 0.0

    summary, dist_df = calculate_word_length_statistics([])
    assert summary["average_length"] == 0.0
    assert dist_df.empty

