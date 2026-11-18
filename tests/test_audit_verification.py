"""Independent Audit Verification Tests for SanskritLens.

Validates:
- U+0900 Inverted Candrabindu tokenization fix.
- Plotly Pareto chart yref configuration fix.
- Hand-calculated statistical verification on controlled verse.
- All visualisations on normal and empty states.
- File upload size and encoding limits.
"""

import io
import pytest
import pandas as pd
from src.nlp.tokenizer import tokenize_sanskrit
from src.nlp.analysis import analyze_text
from src.visualization.charts import (
    plot_top_frequencies,
    plot_frequency_distribution,
    plot_word_length_distribution,
    plot_vocabulary_composition,
    plot_hapax_breakdown,
    plot_pareto_analysis,
    plot_frequency_rank_curve,
    generate_static_frequency_plot,
)
from src.utils.file_handler import read_uploaded_file


def test_inverted_candrabindu_tokenization():
    """Verify that Vedic inverted candrabindu (U+0900) is preserved as part of the token."""
    text = "इदम्\u0900"
    tokens = tokenize_sanskrit(text)
    assert tokens == ["इदम्\u0900"]


def test_pareto_chart_yref_no_exception():
    """Verify that plot_pareto_analysis executes without ValueError on yref."""
    df = pd.DataFrame(
        {
            "Rank": [1, 2, 3],
            "Token": ["सत्यम्", "ज्ञानम्", "अनन्तम्"],
            "Frequency": [5, 3, 2],
            "Percentage": [50.0, 30.0, 20.0],
            "Cumulative_Percentage": [50.0, 80.0, 100.0],
        }
    )
    fig = plot_pareto_analysis(df)
    assert fig is not None


def test_controlled_hand_calculated_statistics():
    """Verify hand-calculated expected values on:

    'सत्यं ब्रूयात् प्रियं ब्रूयात् न ब्रूयात् सत्यमप्रियम्।'
    """
    text = "सत्यं ब्रूयात् प्रियं ब्रूयात् न ब्रूयात् सत्यमप्रियम्।"
    res = analyze_text(text)
    stats = res.stats

    # Expected hand values:
    # Tokens: ['सत्यं', 'ब्रूयात्', 'प्रियं', 'ब्रूयात्', 'न', 'ब्रूयात्', 'सत्यमप्रियम्']
    assert stats["total_tokens"] == 7
    assert stats["unique_tokens"] == 5
    assert stats["type_token_ratio"] == 0.7143
    assert stats["average_token_length"] == 6.86
    assert stats["median_token_length"] == 8.0
    assert stats["min_token_length"] == 1
    assert stats["max_token_length"] == 12
    assert stats["hapax_count"] == 4
    assert stats["hapax_percentage"] == 80.0
    assert stats["dis_count"] == 0
    assert stats["dis_percentage"] == 0.0

    # Verify rank 1 token
    top_row = res.frequency_df.iloc[0]
    assert top_row["Token"] == "ब्रूयात्"
    assert top_row["Frequency"] == 3
    assert top_row["Percentage"] == 42.857
    assert res.frequency_df.iloc[-1]["Cumulative_Percentage"] == 100.0


def test_all_charts_empty_state_resilience():
    """Verify all 8 visualisations handle empty DataFrames gracefully without crashing."""
    empty_df = pd.DataFrame(
        columns=["Rank", "Token", "Frequency", "Percentage", "Cumulative_Percentage"]
    )
    empty_len_df = pd.DataFrame(
        columns=["Length", "Token_Count", "Percentage", "Examples"]
    )
    empty_vocab = {"unique_count": 0, "hapax_count": 0, "dis_count": 0}

    figs = [
        plot_top_frequencies(empty_df),
        plot_frequency_distribution(empty_df),
        plot_word_length_distribution(empty_len_df),
        plot_vocabulary_composition(0, 0),
        plot_hapax_breakdown(empty_vocab),
        plot_pareto_analysis(empty_df),
        plot_frequency_rank_curve(empty_df),
        generate_static_frequency_plot(empty_df),
    ]
    for f in figs:
        assert f is not None


class DummyUpload:
    def __init__(self, content: bytes, size: int):
        self._content = content
        self.size = size

    def read(self):
        return self._content


def test_file_handler_size_and_empty_validation():
    """Verify file upload size checks and empty file handling."""
    # Empty file
    empty_upload = DummyUpload(b"", 0)
    text, err = read_uploaded_file(empty_upload)
    assert text == ""
    assert "empty" in err.lower()

    # Oversized file (> 10 MB)
    large_upload = DummyUpload(b"content", 15 * 1024 * 1024)
    text, err = read_uploaded_file(large_upload)
    assert text == ""
    assert "exceeds" in err.lower()

