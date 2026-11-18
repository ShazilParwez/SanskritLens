"""Core Analysis Engine for SanskritLens.

Coordinates the complete Sanskrit NLP pipeline: normalisation, script detection,
tokenisation, frequency analysis, statistical calculations, section-wise analysis,
and comparative textual analysis.
"""

from __future__ import annotations
from typing import Any
import pandas as pd

from .preprocessing import normalize_sanskrit_text
from .script_detection import detect_script, ScriptDistribution
from .tokenizer import tokenize_sanskrit, segment_sentences
from .frequency import calculate_word_frequencies, get_unique_vocabulary
from .statistics import calculate_text_statistics, calculate_word_length_statistics
from .stopwords import get_stopwords_set


class AnalysisResult:
    """Container holding complete calculated results for a Sanskrit text."""

    def __init__(
        self,
        raw_text: str,
        normalized_text: str,
        script_info: ScriptDistribution,
        tokens: list[str],
        options: dict[str, Any],
        stats: dict[str, Any],
        frequency_df: pd.DataFrame,
        length_summary: dict[str, Any],
        length_df: pd.DataFrame,
        vocabulary_info: dict[str, Any],
    ) -> None:
        self.raw_text = raw_text
        self.normalized_text = normalized_text
        self.script_info = script_info
        self.tokens = tokens
        self.options = options
        self.stats = stats
        self.frequency_df = frequency_df
        self.length_summary = length_summary
        self.length_df = length_df
        self.vocabulary_info = vocabulary_info

    def to_dict(self) -> dict[str, Any]:
        """Convert analysis results into a JSON-serializable dictionary."""
        return {
            "metadata": {
                "total_characters": self.stats.get("total_characters", 0),
                "total_tokens": self.stats.get("total_tokens", 0),
                "unique_tokens": self.stats.get("unique_tokens", 0),
                "primary_script": self.script_info.get("primary_script", "Unknown"),
            },
            "configuration": self.options,
            "statistics": self.stats,
            "length_summary": self.length_summary,
            "top_20_frequencies": (
                self.frequency_df.head(20).to_dict(orient="records")
                if not self.frequency_df.empty
                else []
            ),
            "hapax_count": self.vocabulary_info.get("hapax_count", 0),
            "dis_count": self.vocabulary_info.get("dis_count", 0),
        }


def analyze_text(text: str, options: dict[str, Any] | None = None) -> AnalysisResult:
    """Execute the full SanskritLens NLP analysis pipeline on input text.

    Pipeline Steps:
    1. Unicode NFC normalisation & formatting preservation.
    2. Character block & script composition detection.
    3. Sanskrit-aware tokenisation using selected mode & filters.
    4. Frequency computation and deterministic ranking.
    5. Text, token length, and segment statistics calculation.
    6. Unique vocabulary, hapax, and dis legomena identification.

    Args:
        text: Input Sanskrit text string.
        options: Configuration dict for tokenisation modes and filters.

    Returns:
        AnalysisResult instance containing all calculated metrics.
    """
    opts = options.copy() if options else {}

    # 1. Normalise text
    normalized_text = normalize_sanskrit_text(text, preserve_newlines=True)

    # 2. Script detection
    script_info = detect_script(normalized_text)

    # Prepare stopwords if requested
    if opts.get("filter_stopwords", False):
        custom_stops = opts.get("custom_stopwords", [])
        opts["stopwords_set"] = get_stopwords_set(custom_stops)

    # 3. Tokenise
    tokens = tokenize_sanskrit(normalized_text, options=opts)

    # 4. Frequency analysis
    frequency_df = calculate_word_frequencies(tokens)

    # 5. Vocabulary metrics
    vocab_info = get_unique_vocabulary(tokens)

    # 6. Corpus and Length Statistics
    stats = calculate_text_statistics(normalized_text, tokens)
    length_summary, length_df = calculate_word_length_statistics(tokens)

    return AnalysisResult(
        raw_text=text,
        normalized_text=normalized_text,
        script_info=script_info,
        tokens=tokens,
        options=opts,
        stats=stats,
        frequency_df=frequency_df,
        length_summary=length_summary,
        length_df=length_df,
        vocabulary_info=vocab_info,
    )


def analyze_sections(
    text: str,
    section_type: str = "verse",
    options: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Analyze vocabulary across text sections (verses, paragraphs, or danda lines).

    Args:
        text: Input text string.
        section_type: 'verse' (double danda / danda), 'paragraph' (double newline), or 'line'.
        options: Tokenisation options.

    Returns:
        pd.DataFrame summarizing section number, snippet, token count, unique tokens, and TTR.
    """
    if not text or not text.strip():
        return pd.DataFrame(
            columns=["Section", "Snippet", "Tokens", "Unique_Tokens", "TTR"]
        )

    norm_text = normalize_sanskrit_text(text, preserve_newlines=True)

    if section_type == "paragraph":
        raw_sections = [p.strip() for p in norm_text.split("\n\n") if p.strip()]
    elif section_type == "line":
        raw_sections = [l.strip() for l in norm_text.split("\n") if l.strip()]
    else:  # default 'verse'
        raw_sections = segment_sentences(norm_text)

    rows = []
    for idx, sec in enumerate(raw_sections, start=1):
        sec_tokens = tokenize_sanskrit(sec, options=options)
        tot_tok = len(sec_tokens)
        uniq_tok = len(set(sec_tokens))
        sec_ttr = round(uniq_tok / tot_tok, 3) if tot_tok > 0 else 0.0

        # Create brief snippet
        snippet = sec.replace("\n", " ")
        if len(snippet) > 60:
            snippet = snippet[:57] + "..."

        rows.append(
            {
                "Section": f"Section {idx}",
                "Snippet": snippet,
                "Tokens": tot_tok,
                "Unique_Tokens": uniq_tok,
                "TTR": sec_ttr,
            }
        )

    return pd.DataFrame(rows)


def compare_texts(
    tokens_a: list[str],
    tokens_b: list[str],
    name_a: str = "Text 1",
    name_b: str = "Text 2",
) -> dict[str, Any]:
    """Perform comparative lexical analysis and vocabulary overlap between two texts.

    Calculates:
    - Total tokens and unique vocabulary for each text.
    - Type-Token Ratios (TTR).
    - Common vocabulary set (intersection: A ∩ B).
    - Tokens unique to Text A (A \\ B).
    - Tokens unique to Text B (B \\ A).
    - Jaccard Similarity: J(A, B) = |A ∩ B| / |A ∪ B|
    - Comparative frequency DataFrame for shared tokens.

    Linguistic Note:
    Jaccard similarity measures orthographic lexical overlap between surface word tokens.
    It does not measure semantic similarity, thematic alignment, or underlying grammatical meaning.
    """
    set_a = set(tokens_a)
    set_b = set(tokens_b)

    total_a = len(tokens_a)
    total_b = len(tokens_b)

    uniq_a = len(set_a)
    uniq_b = len(set_b)

    ttr_a = round(uniq_a / total_a, 4) if total_a > 0 else 0.0
    ttr_b = round(uniq_b / total_b, 4) if total_b > 0 else 0.0

    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)

    common_count = len(intersection)
    union_count = len(union)

    jaccard_similarity = (
        round(common_count / union_count, 4) if union_count > 0 else 0.0
    )

    unique_to_a = sorted(list(set_a - set_b))
    unique_to_b = sorted(list(set_b - set_a))
    common_tokens = sorted(list(intersection))

    # Frequency comparison of shared tokens
    from collections import Counter

    count_a = Counter(tokens_a)
    count_b = Counter(tokens_b)

    shared_rows = []
    for tok in common_tokens:
        f_a = count_a[tok]
        f_b = count_b[tok]
        pct_a = round((f_a / total_a) * 100, 2) if total_a > 0 else 0.0
        pct_b = round((f_b / total_b) * 100, 2) if total_b > 0 else 0.0
        shared_rows.append(
            {
                "Token": tok,
                f"Freq ({name_a})": f_a,
                f"% ({name_a})": pct_a,
                f"Freq ({name_b})": f_b,
                f"% ({name_b})": pct_b,
                "Total_Combined": f_a + f_b,
            }
        )

    # Sort shared tokens by combined frequency descending
    shared_df = pd.DataFrame(shared_rows)
    if not shared_df.empty:
        shared_df = shared_df.sort_values(
            by=["Total_Combined", "Token"], ascending=[False, True]
        ).reset_index(drop=True)

    return {
        "name_a": name_a,
        "name_b": name_b,
        "total_a": total_a,
        "total_b": total_b,
        "unique_a": uniq_a,
        "unique_b": uniq_b,
        "ttr_a": ttr_a,
        "ttr_b": ttr_b,
        "common_count": common_count,
        "union_count": union_count,
        "jaccard_similarity": jaccard_similarity,
        "jaccard_percentage": round(jaccard_similarity * 100, 2),
        "unique_to_a": unique_to_a,
        "unique_to_b": unique_to_b,
        "common_tokens": common_tokens,
        "shared_df": shared_df,
    }

