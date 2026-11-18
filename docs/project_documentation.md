# SanskritLens: Technical Architecture & System Documentation

**Official Project Title:** Sanskrit Text Tokenisation and Word-Frequency Analysis Tool  
**Platform Name:** SanskritLens (संस्कृतलेन्स)  
**Domain:** Indian Knowledge Systems (IKS) &bull; Computational Linguistics  
**Software Version:** 1.0.0

---

## 1. System Architecture Overview

SanskritLens follows a decoupled, modular architectural model designed for high maintainability, clear separation of concerns, and local execution.

```
                     ┌──────────────────────────┐
                     │   Streamlit Web UI       │
                     │  (app.py / src/ui/)      │
                     └─────────────┬────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
     ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
     │   NLP Engine    │  │  Visualisation  │  │ Utility Services│
     │  (src/nlp/)     │  │ (src/vis/)      │  │ (src/utils/)    │
     └────────┬────────┘  └────────┬────────┘  └────────┬────────┘
              │                    │                    │
              ▼                    ▼                    ▼
     - Preprocessing      - Plotly Bar / Hist  - File Handling
     - Script Detection   - Donut & Pareto     - CSV with BOM
     - Tokenizer Modes    - Rank-Zipf Curves   - JSON & TXT
     - Frequency & Stats  - Matplotlib Static  - PDF ReportLab
```

---

## 2. Directory Layout and File Responsibilities

```
sanskritlens/
├── app.py                      # Main application entry point & page router
├── requirements.txt            # Pinned dependencies for local execution
├── README.md                   # Comprehensive user and evaluator manual
├── .gitignore                  # Git exclusions for venv, cache, and bytecode
├── .streamlit/
│   └── config.toml             # Theme palette & server configuration
│
├── data/
│   ├── samples/                # Public-domain classical Sanskrit texts
│   │   ├── bhagavad_gita_sample.txt
│   │   ├── upanishad_sample.txt
│   │   ├── subhashita_sample.txt
│   │   └── panchatantra_sample.txt
│   └── metadata/
│       └── sample_metadata.json # Provenance, licensing, and textual attribution
│
├── src/
│   ├── __init__.py
│   ├── nlp/                    # Intellectual core: Sanskrit NLP modules
│   │   ├── __init__.py
│   │   ├── preprocessing.py    # NFC normalisation, BOM strip, whitespace clean
│   │   ├── script_detection.py # Unicode block distribution & script detection
│   │   ├── tokenizer.py        # Devanagari regex tokenizer & verse segmenter
│   │   ├── stopwords.py        # Configurable Sanskrit avyaya/particle catalog
│   │   ├── statistics.py       # TTR, length distributions, segment metrics
│   │   ├── frequency.py        # Counter, ranking, hapax & dis legomena
│   │   └── analysis.py         # Pipeline orchestrator & comparative engine
│   │
│   ├── visualization/          # Publication-grade chart generation
│   │   ├── __init__.py
│   │   └── charts.py           # Plotly interactive & Matplotlib figures
│   │
│   ├── utils/                  # File I/O, validation, and multi-format exporters
│   │   ├── __init__.py
│   │   ├── file_handler.py     # Safe UTF-8 decoding & sample corpus loader
│   │   ├── validators.py       # Text length & configuration validation
│   │   └── exporters.py        # CSV (UTF-8 BOM), JSON, TXT, and PDF builders
│   │
│   └── ui/                     # User interface views
│       ├── __init__.py
│       ├── home.py             # Academic landing page & features
│       ├── input_page.py       # Sample selector, file uploader, direct text area
│       ├── dashboard.py        # KPI cards, Plotly charts, export buttons
│       ├── token_explorer.py   # Interactive searchable table & token inspector
│       ├── insights.py         # Algorithmically computed linguistic findings
│       ├── comparative.py      # Section analysis & cross-text Jaccard overlap
│       └── methodology.py      # Formal academic documentation & citations
│
├── tests/                      # Automated test suite (pytest)
│   ├── __init__.py
│   ├── test_preprocessing.py   # NFC, BOM, whitespace, diacritics tests
│   ├── test_tokenizer.py       # Verse tokenisation, modes, dandas, avagraha
│   ├── test_frequency.py       # Frequencies, ranks, cumulative %, search
│   ├── test_statistics.py      # TTR, average/median length, segment counts
│   ├── test_script_detection.py# Devanagari, Latin, Mixed, empty script tests
│   ├── test_exporters.py       # CSV with BOM, JSON schema, TXT, PDF tests
│   └── test_edge_cases.py      # Punctuation-only, numerals, stress tests
│
└── docs/                       # Academic and architectural papers
    ├── methodology.md          # Theoretical linguistic framework
    └── project_documentation.md# Technical specification & API reference
```

---

## 3. Data Processing Pipeline Specification

```
Raw Input Text
      ↓
[ normalize_sanskrit_text ]   --> Unicode NFC, BOM removal, NBSP resolution
      ↓
[ detect_script ]             --> Unicode block percentages & script advice
      ↓
[ tokenize_sanskrit ]         --> Punctuation detachment, Devanagari grapheme preservation
      ↓
[ calculate_word_frequencies] --> Counter, deterministic secondary tie-breaking
      ↓
[ calculate_text_statistics ] --> TTR, length distributions, verse segment metrics
      ↓
[ AnalysisResult Object ]     --> Passed to Dashboard, Explorer, Insights, Exporters
```

---

## 4. API Reference

### `src.nlp.preprocessing`
- `normalize_sanskrit_text(text: str, preserve_newlines: bool = True) -> str`
- `clean_whitespace(text: str) -> str`
- `remove_vedic_accents(text: str) -> str`

### `src.nlp.script_detection`
- `detect_script(text: str) -> ScriptDistribution`

### `src.nlp.tokenizer`
- `tokenize_sanskrit(text: str, options: dict = None) -> list[str]`
- `segment_sentences(text: str) -> list[str]`

### `src.nlp.frequency`
- `calculate_word_frequencies(tokens: list[str]) -> pd.DataFrame`
- `get_unique_vocabulary(tokens: list[str]) -> dict[str, Any]`
- `search_word_frequency(freq_df: pd.DataFrame, query: str, total_tokens: int) -> dict`

### `src.nlp.statistics`
- `calculate_text_statistics(text: str, tokens: list[str]) -> dict[str, Any]`
- `calculate_word_length_statistics(tokens: list[str]) -> tuple[dict, pd.DataFrame]`

### `src.nlp.analysis`
- `analyze_text(text: str, options: dict = None) -> AnalysisResult`
- `analyze_sections(text: str, section_type: str = "verse", options: dict = None) -> pd.DataFrame`
- `compare_texts(tokens_a: list[str], tokens_b: list[str], name_a: str, name_b: str) -> dict`

### `src.utils.exporters`
- `export_to_csv(freq_df: pd.DataFrame, include_bom: bool = True) -> bytes`
- `export_to_json(analysis_result: AnalysisResult) -> str`
- `export_to_txt_summary(analysis_result: AnalysisResult, title: str) -> str`
- `export_to_pdf_report(analysis_result: AnalysisResult, title: str) -> bytes`

---

## 5. Automated Test Suite Verification

The test harness uses `pytest` and verifies 36 automated unit and integration tests across 7 test modules:

```powershell
sanskritlens\.venv\Scripts\pytest -q sanskritlens\tests
# Output:
# ....................................                                     [100%]
# 36 passed in 1.31s
```

All Unicode normalization invariants, tokenisation constraints, frequency counts, edge cases, and exporter payloads pass with zero failures.

