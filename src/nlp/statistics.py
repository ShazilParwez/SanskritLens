"""Linguistic and Text Statistics Module for SanskritLens.

Computes text metrics, Type-Token Ratio (TTR), word length distributions,
and segment statistics with clear documentation of counting conventions.
"""

from __future__ import annotations
import statistics
import unicodedata
from typing import Any
import pandas as pd
from .frequency import get_unique_vocabulary
from .tokenizer import segment_sentences


def calculate_text_statistics(text: str, tokens: list[str]) -> dict[str, Any]:
    """Calculate comprehensive corpus and token statistics.

    Important Unit Convention Note:
    - Length metrics for Sanskrit words in this application are calculated based on
      Unicode Code Points (Python `len()`).
      In Devanagari orthography, a grapheme cluster or akṣara (syllable, e.g., 'कुरु' or 'क्षेत्रे')
      consists of multiple Unicode code points (consonant + virama + consonant + matra).
      These metrics strictly report Unicode code points and do NOT claim to represent
      traditional phonetic akṣara (syllable) counts.

    Returns:
        dict containing text metrics, vocabulary ratios, and length statistics.
    """
    total_characters = len(text)
    total_tokens = len(tokens)

    # Basic character counts
    chars_no_whitespace = sum(1 for c in text if not c.isspace())
    total_whitespace = sum(1 for c in text if c.isspace())

    # Count punctuation marks (Devanagari dandas + general punctuation)
    punctuation_count = sum(
        1
        for c in text
        if c in ("\u0964", "\u0965")
        or unicodedata.category(c).startswith("P")
        or unicodedata.category(c).startswith("S")
    )

    # Line counts
    total_lines = len(text.splitlines()) if text else 0

    # Verse / Sentence segments
    segments = segment_sentences(text)
    total_segments = len(segments)

    # Unique vocabulary
    vocab_info = get_unique_vocabulary(tokens)
    unique_tokens = vocab_info["unique_count"]

    # Type-Token Ratio (TTR)
    ttr = round(unique_tokens / total_tokens, 4) if total_tokens > 0 else 0.0

    # Token lengths (Unicode code points)
    if tokens:
        lengths = [len(t) for t in tokens]
        avg_len = round(sum(lengths) / total_tokens, 2)
        min_len = min(lengths)
        max_len = max(lengths)
        median_len = round(float(statistics.median(lengths)), 2)
    else:
        avg_len = 0.0
        min_len = 0
        max_len = 0
        median_len = 0.0

    # Segment token metrics
    tokens_per_segment: list[int] = []
    if segments:
        from .tokenizer import tokenize_sanskrit

        for seg in segments:
            seg_toks = tokenize_sanskrit(seg)
            tokens_per_segment.append(len(seg_toks))

        avg_seg_tokens = (
            round(sum(tokens_per_segment) / len(tokens_per_segment), 2)
            if tokens_per_segment
            else 0.0
        )
        min_seg_tokens = min(tokens_per_segment) if tokens_per_segment else 0
        max_seg_tokens = max(tokens_per_segment) if tokens_per_segment else 0
    else:
        avg_seg_tokens = 0.0
        min_seg_tokens = 0
        max_seg_tokens = 0

    return {
        "total_characters": total_characters,
        "chars_no_whitespace": chars_no_whitespace,
        "total_whitespace": total_whitespace,
        "punctuation_count": punctuation_count,
        "total_lines": total_lines,
        "total_segments": total_segments,
        "total_tokens": total_tokens,
        "unique_tokens": unique_tokens,
        "type_token_ratio": ttr,
        "average_token_length": avg_len,
        "min_token_length": min_len,
        "max_token_length": max_len,
        "median_token_length": median_len,
        "hapax_count": vocab_info["hapax_count"],
        "hapax_percentage": vocab_info["hapax_percentage"],
        "dis_count": vocab_info["dis_count"],
        "dis_percentage": vocab_info["dis_percentage"],
        "avg_tokens_per_segment": avg_seg_tokens,
        "min_tokens_per_segment": min_seg_tokens,
        "max_tokens_per_segment": max_seg_tokens,
    }


def calculate_word_length_statistics(tokens: list[str]) -> tuple[dict[str, Any], pd.DataFrame]:
    """Calculate token length frequencies and distribution.

    Returns:
        tuple of (summary_dict, length_distribution_dataframe)
    """
    if not tokens:
        empty_df = pd.DataFrame(
            columns=["Length", "Token_Count", "Percentage", "Examples"]
        )
        return (
            {
                "average_length": 0.0,
                "median_length": 0.0,
                "min_length": 0,
                "max_length": 0,
                "shortest_tokens": [],
                "longest_tokens": [],
            },
            empty_df,
        )

    lengths = [len(t) for t in tokens]
    total_tokens = len(tokens)
    avg_len = round(sum(lengths) / total_tokens, 2)
    median_len = round(float(statistics.median(lengths)), 2)
    min_len = min(lengths)
    max_len = max(lengths)

    # Group tokens by length
    length_groups: dict[int, list[str]] = {}
    for tok in tokens:
        l = len(tok)
        if l not in length_groups:
            length_groups[l] = []
        length_groups[l].append(tok)

    # Distinct shortest and longest token lists
    shortest_tokens = sorted(list(set(length_groups.get(min_len, []))))[:10]
    longest_tokens = sorted(list(set(length_groups.get(max_len, []))))[:10]

    rows = []
    for l in sorted(length_groups.keys()):
        toks = length_groups[l]
        count = len(toks)
        pct = round((count / total_tokens) * 100, 2)
        unique_examples = sorted(list(set(toks)))[:3]
        example_str = ", ".join(unique_examples)
        rows.append(
            {
                "Length": l,
                "Token_Count": count,
                "Percentage": pct,
                "Examples": example_str,
            }
        )

    dist_df = pd.DataFrame(rows)

    summary = {
        "average_length": avg_len,
        "median_length": median_len,
        "min_length": min_len,
        "max_length": max_len,
        "shortest_tokens": shortest_tokens,
        "longest_tokens": longest_tokens,
    }

    return summary, dist_df

