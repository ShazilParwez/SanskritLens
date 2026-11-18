"""Sanskrit-Aware Word Tokenizer Module.

Performs robust, linguistically informed orthographic tokenisation for Sanskrit text.
Preserves Devanagari ligatures, matras, virama, anusvara, visarga, chandrabindu,
and Vedic accents, while cleanly separating punctuation and verse boundaries.
"""

from __future__ import annotations
import re
from typing import Any
from .preprocessing import normalize_sanskrit_text

# Devanagari Lexical Character Pattern
# Includes: Vowels, Consonants, Matras, Halant/Virama (\u094D), Anusvara (\u0902),
# Visarga (\u0903), Chandrabindu (\u0901), Avagraha (\u093D), Nukta (\u093C),
# Vedic Svara (\u0951-\u0954, \u1CD0-\u1CFF), Devanagari Extended (\uA8E0-\uA8FF),
# and Zero-Width joiners (\u200C, \u200D).
# Excludes: Dandas (\u0964, \u0965) and Numerals (\u0966-\u096F).
DEVANAGARI_WORD_CHARS = (
    r"[\u0900-\u0963\u0970-\u097F\uA8E0-\uA8FF\u1CD0-\u1CFF\u200C\u200D]"
)

# Latin word characters including IAST diacritics
LATIN_WORD_CHARS = r"[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]"

# Sanskrit and general punctuation
PUNCTUATION_PATTERN = re.compile(
    r"[\u0964\u0965\.,;:!\?\"'“”‘’—\-\(\)\[\]\{\}\<\>«»/\\\|`~@#\$%\^&\*_\+=]+"
)


def tokenize_sanskrit(
    text: str,
    options: dict[str, Any] | None = None,
) -> list[str]:
    """Tokenize Sanskrit text into a list of orthographic word tokens.

    Linguistic Scope & Methodology:
    - Preserves orthographic units (word tokens as written).
    - Accurately respects Devanagari grapheme clusters, preventing splits at matras or halant.
    - Excludes Sanskrit danda (।) and double danda (॥) from lexical tokens.
    - Supports three modes: 'standard', 'normalised', and 'custom'.

    Options dictionary may contain:
    - mode: 'standard' | 'normalised' | 'custom' (default: 'standard')
    - remove_punctuation: bool (default: True for lexical tokens)
    - exclude_numerals: bool (default: True in normalised/custom, False in standard)
    - min_token_length: int (default: 1)
    - filter_stopwords: bool (default: False)
    - stopwords_set: set[str] (optional custom stopwords)
    - lowercase_latin: bool (default: True for non-Devanagari characters)
    - strip_hyphens_at_linebreak: bool (default: True)

    Args:
        text: Input Sanskrit string.
        options: Configuration dictionary.

    Returns:
        List of Sanskrit word token strings.
    """
    if not text or not text.strip():
        return []

    opts = options or {}
    mode = opts.get("mode", "standard").lower()

    # Configure defaults based on mode
    if mode == "normalised":
        remove_punct = opts.get("remove_punctuation", True)
        exclude_nums = opts.get("exclude_numerals", True)
        min_len = opts.get("min_token_length", 1)
        filter_stops = opts.get("filter_stopwords", False)
        case_norm = opts.get("lowercase_latin", True)
    elif mode == "custom":
        remove_punct = opts.get("remove_punctuation", True)
        exclude_nums = opts.get("exclude_numerals", False)
        min_len = opts.get("min_token_length", 1)
        filter_stops = opts.get("filter_stopwords", False)
        case_norm = opts.get("lowercase_latin", False)
    else:  # standard
        remove_punct = opts.get("remove_punctuation", True)
        exclude_nums = opts.get("exclude_numerals", True)  # by default omit verse numbers from word counts
        min_len = opts.get("min_token_length", 1)
        filter_stops = opts.get("filter_stopwords", False)
        case_norm = opts.get("lowercase_latin", False)

    # 1. Unicode NFC Normalisation
    norm_text = normalize_sanskrit_text(text, preserve_newlines=True)

    # 2. Handle line-break hyphens common in printed verses (e.g., "कदाचि-\nन्नायं" -> "कदाचिन्नायं")
    if opts.get("strip_hyphens_at_linebreak", True):
        norm_text = re.sub(r"-\s*\n\s*", "", norm_text)

    # 3. Primary token extraction
    # Match Devanagari lexical tokens, Devanagari numerals, Latin words, or Western numbers
    # A Devanagari token may contain internal hyphens for compounds (e.g. मित्र-भेद)
    devanagari_token_pattern = (
        rf"{DEVANAGARI_WORD_CHARS}+(?:[-_]{DEVANAGARI_WORD_CHARS}+)*"
    )
    latin_token_pattern = rf"{LATIN_WORD_CHARS}+(?:[-_]{LATIN_WORD_CHARS}+)*"
    devanagari_num_pattern = r"[\u0966-\u096F]+"
    western_num_pattern = r"[0-9]+"

    if remove_punct:
        # Extract purely lexical and numeric tokens, bypassing standalone punctuation
        token_regex = re.compile(
            rf"({devanagari_token_pattern}|{latin_token_pattern}|{devanagari_num_pattern}|{western_num_pattern})"
        )
    else:
        # Include punctuation tokens as distinct items if requested
        punct_chars = r"[\u0964\u0965\.,;:!\?\"'“”‘’—\-\(\)\[\]\{\}\<\>/\\|`~@#\$%\^&\*_\+=]"
        token_regex = re.compile(
            rf"({devanagari_token_pattern}|{latin_token_pattern}|{devanagari_num_pattern}|{western_num_pattern}|{punct_chars})"
        )

    raw_tokens = token_regex.findall(norm_text)

    # 4. Token Filtering & Normalisation
    stopwords_set = opts.get("stopwords_set") or set()
    cleaned_tokens: list[str] = []

    dev_digits_re = re.compile(r"^[\u0966-\u096F]+$")
    west_digits_re = re.compile(r"^[0-9]+$")

    for tok in raw_tokens:
        tok = tok.strip()
        if not tok:
            continue

        # Case normalization for Latin scripts only
        if case_norm:
            tok = tok.lower()

        # Numerical filtering
        if exclude_nums:
            if dev_digits_re.match(tok) or west_digits_re.match(tok):
                continue

        # Minimum length filter (counting Unicode code points)
        if len(tok) < min_len:
            continue

        # Stopword filtering
        if filter_stops and stopwords_set:
            if tok in stopwords_set:
                continue

        cleaned_tokens.append(tok)

    return cleaned_tokens


def segment_sentences(text: str) -> list[str]:
    """Segment Sanskrit text into sentence, verse, or hemistich units.

    Recognises:
    - Sanskrit Double Danda (॥) : Full verse or discourse boundary.
    - Sanskrit Danda (।) : Hemistich (pāda / half-verse) or sentence boundary.
    - Western sentence terminators: '.', '!', '?'
    - Fallback: Newlines where punctuation is absent.

    Returns:
        List of non-empty segment strings.
    """
    if not text or not text.strip():
        return []

    norm_text = normalize_sanskrit_text(text, preserve_newlines=True)

    # Replace double danda, danda, and western terminators with a dedicated delimiter
    delimited = re.sub(r"[\u0965\u0964\r\n\?!]+", "\u2042", norm_text)

    # Split by delimiter
    segments = [s.strip() for s in delimited.split("\u2042") if s.strip()]
    return segments
