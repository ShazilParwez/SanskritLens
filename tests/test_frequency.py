"""Unit Tests for Word Frequency Analysis."""

import pytest
import pandas as pd
from src.nlp.frequency import (
    calculate_word_frequencies,
    get_unique_vocabulary,
    search_word_frequency,
)


def test_official_frequency_test_case():
    """Verify official project test case:

    Input: रामः रामः कृष्णः सीता रामः
    Expected:
    रामः = 3
    कृष्णः = 1
    सीता = 1
    """
    tokens = ["रामः", "रामः", "कृष्णः", "सीता", "रामः"]
    df = calculate_word_frequencies(tokens)

    # Convert to dict for direct comparison
    freq_map = dict(zip(df["Token"], df["Frequency"]))
    assert freq_map["रामः"] == 3
    assert freq_map["कृष्णः"] == 1
    assert freq_map["सीता"] == 1

    # Check rank ordering
    assert df.iloc[0]["Token"] == "रामः"
    assert df.iloc[0]["Frequency"] == 3
    assert df.iloc[0]["Rank"] == 1

    # Check cumulative percentage reaches 100%
    assert df.iloc[-1]["Cumulative_Percentage"] == 100.0


def test_secondary_deterministic_sort():
    """Verify that when frequencies tie, words are sorted alphabetically by Unicode."""
    tokens = ["सीता", "कृष्णः"]  # both freq = 1
    df = calculate_word_frequencies(tokens)
    # कृष्णः comes before सीता in Unicode order
    assert df.iloc[0]["Token"] == "कृष्णः"
    assert df.iloc[1]["Token"] == "सीता"


def test_unique_vocabulary_and_hapax():
    """Verify hapax legomena and dis legomena counting."""
    tokens = ["रामः", "रामः", "कृष्णः", "सीता", "सीता", "अर्जुनः"]
    # रामः=2 (dis), कृष्णः=1 (hapax), सीता=2 (dis), अर्जुनः=1 (hapax)
    vocab = get_unique_vocabulary(tokens)

    assert vocab["unique_count"] == 4
    assert vocab["hapax_count"] == 2
    assert "कृष्णः" in vocab["hapax_tokens"]
    assert "अर्जुनः" in vocab["hapax_tokens"]
    assert vocab["dis_count"] == 2
    assert "रामः" in vocab["dis_tokens"]
    assert "सीता" in vocab["dis_tokens"]


def test_word_frequency_search():
    """Verify searching for specific tokens."""
    tokens = ["धर्मः", "सत्यम्", "धर्मः", "शान्तिः"]
    df = calculate_word_frequencies(tokens)

    match = search_word_frequency(df, "धर्मः", total_tokens=len(tokens))
    assert match is not None
    assert match["token"] == "धर्मः"
    assert match["frequency"] == 2
    assert match["rank"] == 1
    assert match["percentage"] == 50.0
    assert match["per_thousand"] == 500.0

    not_found = search_word_frequency(df, "माया", total_tokens=len(tokens))
    assert not_found is None


def test_empty_tokens_frequency():
    """Verify empty token input produces empty DataFrame."""
    df = calculate_word_frequencies([])
    assert df.empty
    assert list(df.columns) == ["Rank", "Token", "Frequency", "Percentage", "Cumulative_Percentage"]

