"""Edge Cases and Stress Testing for SanskritLens NLP Pipeline."""

import pytest
from src.nlp.analysis import analyze_text, compare_texts
from src.nlp.tokenizer import tokenize_sanskrit


def test_punctuation_only_text():
    """Verify handling of texts containing only dandas and punctuation."""
    text = "॥ । , . ! ? ; : - — \" ' ( ) [ ]"
    res = analyze_text(text)
    assert res.stats["total_tokens"] == 0
    assert res.stats["unique_tokens"] == 0
    assert res.frequency_df.empty


def test_numerals_only_text():
    """Verify handling of text with only numerals."""
    text = "१ २ ३ ४ ५ ६ ७ ८ ९ ० 123 456"
    res = analyze_text(text, options={"exclude_numerals": True})
    assert res.stats["total_tokens"] == 0
    assert res.stats["unique_tokens"] == 0


def test_repeated_tokens_stress():
    """Verify text with 10,000 repeated tokens does not crash or corrupt counts."""
    base = "शान्तिः " * 1000
    res = analyze_text(base)
    assert res.stats["total_tokens"] == 1000
    assert res.stats["unique_tokens"] == 1
    assert res.frequency_df.iloc[0]["Frequency"] == 1000
    assert res.frequency_df.iloc[0]["Percentage"] == 100.0


def test_mixed_scripts_in_analysis():
    """Verify mixed script analysis works gracefully."""
    text = "इदम् वाक्यम् contains English and numbers 108 ॥"
    res = analyze_text(text)
    assert res.stats["total_tokens"] > 0
    assert "इदम्" in res.tokens
    assert "वाक्यम्" in res.tokens
    assert "contains" in res.tokens
    assert res.script_info["primary_script"] == "Mixed (Devanagari & Latin)"


def test_comparative_identical_texts():
    """Verify Jaccard similarity is 1.0 (100%) for identical texts."""
    toks = ["सत्यम्", "ज्ञानम्", "अनन्तम्", "ब्रह्म"]
    comp = compare_texts(toks, toks, name_a="A", name_b="B")
    assert comp["jaccard_similarity"] == 1.0
    assert comp["jaccard_percentage"] == 100.0
    assert len(comp["unique_to_a"]) == 0
    assert len(comp["unique_to_b"]) == 0


def test_comparative_disjoint_texts():
    """Verify Jaccard similarity is 0.0 for completely disjoint vocabularies."""
    toks_a = ["रामः", "लक्ष्मणः", "सीता"]
    toks_b = ["कृष्णः", "बलरामः", "सुभद्रा"]
    comp = compare_texts(toks_a, toks_b, name_a="A", name_b="B")
    assert comp["jaccard_similarity"] == 0.0
    assert comp["common_count"] == 0

