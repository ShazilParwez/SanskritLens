"""SanskritLens NLP Package.

Provides Sanskrit text preprocessing, script detection, tokenisation,
stopwords, frequency calculations, linguistic statistics, and analysis pipelines.
"""

from .preprocessing import normalize_sanskrit_text, clean_whitespace, remove_vedic_accents
from .script_detection import detect_script, ScriptDistribution
from .tokenizer import tokenize_sanskrit, segment_sentences
from .stopwords import get_default_stopwords, get_stopwords_set
from .frequency import (
    calculate_word_frequencies,
    get_unique_vocabulary,
    search_word_frequency,
)
from .statistics import calculate_text_statistics, calculate_word_length_statistics
from .analysis import analyze_text, analyze_sections, compare_texts, AnalysisResult

__all__ = [
    "normalize_sanskrit_text",
    "clean_whitespace",
    "remove_vedic_accents",
    "detect_script",
    "ScriptDistribution",
    "tokenize_sanskrit",
    "segment_sentences",
    "get_default_stopwords",
    "get_stopwords_set",
    "calculate_word_frequencies",
    "get_unique_vocabulary",
    "search_word_frequency",
    "calculate_text_statistics",
    "calculate_word_length_statistics",
    "analyze_text",
    "analyze_sections",
    "compare_texts",
    "AnalysisResult",
]

