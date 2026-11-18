"""Word Frequency Analysis Module for SanskritLens.

Computes exact word frequencies, ranks, relative percentages, and cumulative distributions
using Python collections.Counter and Pandas DataFrames.
"""

from __future__ import annotations
from collections import Counter
from typing import Any
import pandas as pd


def calculate_word_frequencies(tokens: list[str]) -> pd.DataFrame:
    """Calculate frequencies, ranks, percentages, and cumulative percentages for tokens.

    Sorting Rules:
    - Primary sort: Descending frequency (most frequent first).
    - Secondary sort: Deterministic alphabetical order by Unicode code points.

    Returns:
        pd.DataFrame with columns:
        ['Rank', 'Token', 'Frequency', 'Percentage', 'Cumulative_Percentage']
    """
    if not tokens:
        return pd.DataFrame(
            columns=["Rank", "Token", "Frequency", "Percentage", "Cumulative_Percentage"]
        )

    total_tokens = len(tokens)
    counter = Counter(tokens)

    # Sort items deterministically: first by frequency DESC (-count), then by token ASC
    sorted_items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))

    ranks: list[int] = []
    word_list: list[str] = []
    freq_list: list[int] = []
    pct_list: list[float] = []
    cum_pct_list: list[float] = []

    running_cum_pct = 0.0
    for rank, (word, freq) in enumerate(sorted_items, start=1):
        pct = round((freq / total_tokens) * 100, 3)
        running_cum_pct = min(100.0, round(running_cum_pct + pct, 3))

        ranks.append(rank)
        word_list.append(word)
        freq_list.append(freq)
        pct_list.append(pct)
        cum_pct_list.append(running_cum_pct)

    # Ensure last element hits exactly 100.0 if not empty
    if cum_pct_list:
        cum_pct_list[-1] = 100.0

    df = pd.DataFrame(
        {
            "Rank": ranks,
            "Token": word_list,
            "Frequency": freq_list,
            "Percentage": pct_list,
            "Cumulative_Percentage": cum_pct_list,
        }
    )
    return df


def get_unique_vocabulary(tokens: list[str]) -> dict[str, Any]:
    """Calculate unique vocabulary metrics, including Hapax and Dis legomena.

    Definitions:
    - Hapax legomena: Tokens that appear exactly once in the entire corpus.
    - Dis legomena: Tokens that appear exactly twice in the corpus.

    Returns:
        dict containing unique count, lists of hapax/dis legomena, and percentages.
    """
    if not tokens:
        return {
            "unique_count": 0,
            "hapax_count": 0,
            "hapax_percentage": 0.0,
            "hapax_tokens": [],
            "dis_count": 0,
            "dis_percentage": 0.0,
            "dis_tokens": [],
            "all_unique_tokens": [],
        }

    counter = Counter(tokens)
    total_unique = len(counter)

    hapax_tokens = sorted([word for word, count in counter.items() if count == 1])
    dis_tokens = sorted([word for word, count in counter.items() if count == 2])

    hapax_count = len(hapax_tokens)
    dis_count = len(dis_tokens)

    hapax_pct = round((hapax_count / total_unique) * 100, 2) if total_unique > 0 else 0.0
    dis_pct = round((dis_count / total_unique) * 100, 2) if total_unique > 0 else 0.0

    return {
        "unique_count": total_unique,
        "hapax_count": hapax_count,
        "hapax_percentage": hapax_pct,
        "hapax_tokens": hapax_tokens,
        "dis_count": dis_count,
        "dis_percentage": dis_pct,
        "dis_tokens": dis_tokens,
        "all_unique_tokens": sorted(counter.keys()),
    }


def search_word_frequency(
    freq_df: pd.DataFrame,
    query_token: str,
    total_tokens: int,
) -> dict[str, Any] | None:
    """Perform exact search for a Sanskrit token in the frequency DataFrame.

    Returns token metrics or None if not found.
    """
    if freq_df.empty or not query_token:
        return None

    query_norm = query_token.strip()
    match = freq_df[freq_df["Token"] == query_norm]

    if match.empty:
        return None

    row = match.iloc[0]
    freq = int(row["Frequency"])
    rank = int(row["Rank"])
    pct = float(row["Percentage"])
    per_thousand = round((freq / total_tokens) * 1000, 2) if total_tokens > 0 else 0.0

    return {
        "token": query_norm,
        "rank": rank,
        "frequency": freq,
        "percentage": pct,
        "per_thousand": per_thousand,
        "total_tokens": total_tokens,
    }

