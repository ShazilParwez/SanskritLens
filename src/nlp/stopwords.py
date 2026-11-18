"""Sanskrit Stopwords and Filtering Module.

Provides a carefully curated, configurable collection of Sanskrit indeclinables (अव्यय),
pronouns, particles, and conjunctions.

IMPORTANT ACADEMIC DISCLAIMER:
In the Sanskrit grammatical tradition (Pāṇinian Vyākaraṇa), indeclinables (अव्ययानि)
and nipātas (निपाताः) often carry essential syntactic and semantic force (e.g., च, एव, अपि, न).
Unlike modern analytic languages like English, Sanskrit inflectional morphology means that
so-called 'stopwords' cannot be discarded without altering the syntactic structure.
Therefore, this list is provided strictly as an illustrative, configurable research tool
and is DISABLED by default in SanskritLens.
"""

from __future__ import annotations
from typing import Final

DEFAULT_SANSKRIT_STOPWORDS: Final[list[str]] = [
    # Conjunctions & Connective Particles
    "च",
    "अपि",
    "एव",
    "तु",
    "वा",
    "इति",
    "यथा",
    "तथा",
    "हि",
    "न",
    "मा",
    "सह",
    "विना",
    "किल",
    "खलु",
    "स्म",
    "अथ",
    "अतः",
    "ततः",
    "यतः",
    "कुतः",
    "चेत्",
    "यदि",
    "तर्हि",
    "उत",
    "किन्तु",
    "परम्",
    "ननु",
    # Pronouns & Pronominal Adjectives (Common cases)
    "सः",
    "सा",
    "तद्",
    "तत्",
    "ते",
    "तानि",
    "तम्",
    "तान्",
    "तस्य",
    "तस्मात्",
    "तस्मै",
    "तस्मिन्",
    "अयम्",
    "इयम्",
    "इदम्",
    "इमे",
    "एषः",
    "एषा",
    "एतत्",
    "एते",
    "एतद्",
    "कः",
    "का",
    "किम्",
    "के",
    "कस्मै",
    "कस्य",
    "यः",
    "या",
    "यत्",
    "ये",
    "यानि",
    "यस्य",
    "अहम्",
    "माम्",
    "मया",
    "मह्यम्",
    "मत्",
    "मम",
    "मयि",
    "वयम्",
    "अस्मान्",
    "अस्माकम्",
    "नः",
    "त्वम्",
    "त्वाम्",
    "त्वया",
    "तुभ्यम्",
    "त्वत्",
    "तव",
    "त्वयि",
    "यूयम्",
    "युष्माकम्",
    "वः",
    "सर्वः",
    "सर्वे",
    "सर्वाणि",
    "सर्वम्",
    # Adverbial & Spatial/Temporal Indeclinables
    "तत्र",
    "यत्र",
    "कुत्र",
    "सर्वत्र",
    "एकत्र",
    "अत्र",
    "तदा",
    "यदा",
    "कदा",
    "सदा",
    "सर्वदा",
    "एकदा",
    "अधुना",
    "इदानीम्",
    "पुनः",
    "पुरा",
    "बहिः",
    "अन्तः",
    "ऊर्ध्वम्",
    "अधः",
]


def get_default_stopwords() -> list[str]:
    """Return a copy of the default Sanskrit stopword list."""
    return list(DEFAULT_SANSKRIT_STOPWORDS)


def get_stopwords_set(custom_words: list[str] | set[str] | None = None) -> set[str]:
    """Return a unified set of normalized stopwords."""
    words = set(DEFAULT_SANSKRIT_STOPWORDS)
    if custom_words:
        words.update(w.strip() for w in custom_words if w.strip())
    return words

