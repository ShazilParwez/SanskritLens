# SanskritLens (संस्कृतलेन्स)
### Sanskrit Text Tokenisation and Word-Frequency Analysis Platform
**Academic Domain:** Indian Knowledge Systems (IKS) &bull; Computational Linguistics  
**Official Project Title:** Sanskrit Text Tokenisation and Word-Frequency Analysis Tool  
**Platform Version:** 1.0.0 (Production Release)

---

## 1. Project Introduction

**SanskritLens** is a dedicated, locally executable computational linguistics platform engineered to perform Devanagari character normalisation, Sanskrit-aware word tokenisation, frequency ranking, and lexical diversity analytics on classical and Vedic Sanskrit literature.

Developed under the **Indian Knowledge Systems (IKS)** research domain, SanskritLens replaces generic, English-centric tokenizers with a linguistically informed NLP pipeline that respects Devanagari Unicode characteristics—such as dependent vowel signs (*mātrās*), *virāma/halanta*, *anusvāra*, *visarga*, *candrabindu*, *avagraha*, and verse punctuation (*daṇḍas*).

The application is built with a refined, scholarly user interface in Streamlit, powered by Pandas and Plotly, and operates completely offline with zero dependency on external paid APIs or cloud servers.

---

## 2. Problem Statement

Sanskrit texts are preserved in extensive digital repositories (such as GRETIL, Muktabodha, and Sanskrit Documents). However, extracting quantitative lexical patterns from these texts presents unique computational hurdles:
1. **Script Complexity:** Devanagari encodes vowel signs and consonant conjuncts using complex combining Unicode code points that generic whitespace tokenizers often corrupt.
2. **Verse Orthography:** Classical Sanskrit poetry uses single (*।*) and double (*॥*) dandas as hemistich and verse boundaries, which traditional Western tokenizers often treat as unknown symbols or attach to trailing words.
3. **Encoding Discrepancies:** Variations in Unicode representations (NFD vs. NFC) and Byte Order Marks (BOM) produce inconsistent frequency counts for identical Sanskrit words.
4. **Sandhi and Compounding:** The continuous euphonic fusion of words (*sandhi*) and extensive nominal compounds (*samāsa*) mean that whitespace tokens do not directly correspond to grammatical words (*padas*). Tools that make unrealistic claims about automatic morphological decomposition frequently fabricate inaccurate linguistic results.

---

## 3. Project Objectives

1. **Digital Preprocessing:** Implement Unicode Normalisation Form C (NFC), BOM stripping, and whitespace sanitation.
2. **Script Composition Detection:** Quantify character block distributions (Devanagari, Latin, numerals, punctuation).
3. **Sanskrit-Aware Tokenisation:** Accurately extract orthographic word tokens while preserving combining ligatures and disengaging verse boundaries.
4. **Word-Frequency Computation:** Calculate token frequencies, percentages, ranks, and cumulative distributions.
5. **Vocabulary Diversity Metrics:** Identify Type-Token Ratio (TTR), Hapax Legomena (single-occurrence words), and Dis Legomena.
6. **Token Length Analysis:** Compute length distributions, means, medians, and extremes in Unicode code points.
7. **Empirical Visualisation:** Render responsive horizontal bar charts, frequency spectrums, donut charts, Pareto distributions, and Zipf rank-frequency curves.
8. **Multi-Format Export:** Export verified UTF-8 with BOM CSV files, structured JSON datasets, plain text summaries, and PDF reports.
9. **Academic Transparency:** Transparently document the boundary between orthographic tokenisation and morphological segmentation.

---

## 4. Indian Knowledge Systems (IKS) Relevance

Classical Sanskrit literature represents one of humanity's most comprehensive intellectual archives. Traditional scholarship in *Vyākaraṇa* (grammar), *Nyāya* (logic), *Mīmāṃsā* (hermeneutics), and *Kāvya* (poetics) values precise lexical rigor.

SanskritLens contributes to the IKS domain by:
- **Corpus Profiling:** Quantifying lexical density across recensions of foundational works (e.g., the *Bhagavad Gītā*, *Upaniṣads*, and classical didactic anthologies).
- **Stylistic Exploration:** Helping scholars explore vocabulary recurrence and rare lexemes (*hapax legomena*) that signal specialized philosophical terminology or complex compounds.
- **Comparative Hermeneutics:** Providing set-theoretic vocabulary overlap (Jaccard similarity) between classical philosophical schools.
- **Educational Empowerment:** Providing students with an intuitive, scholarly interface to explore the vocabulary of classical Sanskrit literature.

---

## 5. Technology Stack

- **Core Language:** Python 3.11+
- **Web Application Interface:** Streamlit (with customized scholarly CSS and typography)
- **Data Manipulation & Tabular Engine:** Pandas & NumPy
- **Interactive Visualisation:** Plotly (Graph Objects & Express)
- **Static Graphics & PDF Report Generation:** Matplotlib & ReportLab (with Devanagari font embedding)
- **NLP & Unicode Algorithms:** Python standard library `unicodedata`, `re`, and `collections.Counter`
- **Automated Testing Suite:** pytest

---

## 6. System Architecture

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

## 7. Project Directory Structure

```
sanskritlens/
├── app.py                      # Main application entry point & page router
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive user and evaluator manual
├── .gitignore                  # Git exclusions
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
│       └── sample_metadata.json # Complete metadata and licensing records
│
├── src/
│   ├── __init__.py
│   ├── nlp/                    # Sanskrit NLP core engine
│   │   ├── __init__.py
│   │   ├── preprocessing.py    # Unicode NFC normalisation & diacritics
│   │   ├── script_detection.py # Unicode block analysis & script identification
│   │   ├── tokenizer.py        # Devanagari tokenisation & verse segmentation
│   │   ├── stopwords.py        # Configurable Sanskrit particle catalog
│   │   ├── statistics.py       # TTR, length distributions, segment stats
│   │   ├── frequency.py        # Counter, ranking, hapax & dis legomena
│   │   └── analysis.py         # Pipeline coordinator & comparative engine
│   │
│   ├── visualization/          # Plotly interactive & static charts
│   │   ├── __init__.py
│   │   └── charts.py           # Publication-grade chart generation
│   │
│   ├── utils/                  # File I/O, validation, and multi-format exporters
│   │   ├── __init__.py
│   │   ├── file_handler.py     # Safe UTF-8 decoding & sample loader
│   │   ├── validators.py       # Input validation
│   │   └── exporters.py        # CSV (UTF-8 BOM), JSON, TXT, and PDF
│   │
│   └── ui/                     # Modular Streamlit views
│       ├── __init__.py
│       ├── home.py             # Academic landing page & features
│       ├── input_page.py       # Sample selector, file uploader, direct text
│       ├── dashboard.py        # KPI cards, Plotly charts, export buttons
│       ├── token_explorer.py   # Searchable table & individual token inspector
│       ├── insights.py         # Algorithmically computed linguistic findings
│       ├── comparative.py      # Section analysis & cross-text Jaccard overlap
│       └── methodology.py      # Academic documentation & citations
│
├── tests/                      # Automated test suite (pytest)
│   ├── __init__.py
│   ├── test_preprocessing.py   # Unicode normalisation tests
│   ├── test_tokenizer.py       # Tokenisation & verse tests
│   ├── test_frequency.py       # Frequency & ranking tests
│   ├── test_statistics.py      # TTR & length metrics tests
│   ├── test_script_detection.py# Script composition tests
│   ├── test_exporters.py       # Multi-format exporter tests
│   └── test_edge_cases.py      # Edge case & stress tests
│
└── docs/                       # Academic and architectural papers
    ├── methodology.md          # Theoretical linguistic framework
    └── project_documentation.md# Technical specification & API reference
```

---

## 8. Installation & Virtual Environment Setup

### 8.1 Windows

```powershell
# 1. Navigate to the project directory
cd sanskritlens

# 2. Create a clean virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```

### 8.2 Linux / macOS

```bash
# 1. Navigate to the project directory
cd sanskritlens

# 2. Create a clean virtual environment
python3 -m venv .venv

# 3. Activate the virtual environment
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## 9. Running the Application

Once the virtual environment is activated, launch the Streamlit web server:

```powershell
streamlit run app.py
```

The application will launch and open in your default web browser at `http://localhost:8501`.

---

## 10. Automated Testing Instructions

Run the automated test suite using `pytest`:

```powershell
pytest -q
```

### Verified Test Suite Output:
```
....................................                                     [100%]
36 passed in 1.31s
```
All 36 unit and integration tests across normalisation, tokenisation, frequency calculation, statistics, script detection, exporters, and edge cases pass with 100% success.

---

## 11. Core NLP Processing Pipeline

```
Raw Sanskrit Text
       ↓
[ normalize_sanskrit_text ]
  • Unicode Normalisation Form C (NFC)
  • UTF-8 Byte Order Mark (BOM) removal
  • Non-breaking space (NBSP) resolution
  • Diacritic & Sanskrit punctuation preservation
       ↓
[ detect_script ]
  • Devanagari, Latin (IAST), numeral, punctuation distribution
  • Primary script classification & informative advisories
       ↓
[ tokenize_sanskrit ]
  • Mode A (Standard): Retains orthographic forms, disengages dandas
  • Mode B (Normalised): Case normalisation for Latin, numerals filtered
  • Mode C (Custom): User-configured lengths, stopword filtering
       ↓
[ calculate_word_frequencies ]
  • collections.Counter with deterministic secondary Unicode sorting
  • Rank, occurrence frequency, percentage, cumulative percentage
       ↓
[ calculate_text_statistics ]
  • Type-Token Ratio (TTR)
  • Unicode code point length distributions (mean, median, min, max)
  • Verse/sentence segment counts & density
       ↓
[ AnalysisResult Object ]
  • Powers KPI Cards, Charts, Token Explorer, Insights, and Exporters
```

---

## 12. Mathematical Formulations & Statistical Formulas

### 12.1 Type-Token Ratio (TTR)
$$\text{TTR} = \frac{V}{N}$$
where $V$ is the number of distinct vocabulary types, and $N$ is the total token volume.

### 12.2 Average Token Length
$$\bar{L} = \frac{1}{N} \sum_{i=1}^{N} \text{len}(t_i)$$
*Important:* Length is measured strictly in **Unicode Code Points**. It is not claimed to represent traditional phonetic syllables (*akṣaras*).

### 12.3 Hapax & Dis Legomena
- **Hapax Legomena ($H_1$):** Words occurring with frequency $f = 1$.
- **Dis Legomena ($H_2$):** Words occurring with frequency $f = 2$.

### 12.4 Jaccard Similarity (Vocabulary Overlap)
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
Quantifies surface lexical overlap across two Sanskrit texts on a scale from $0.0$ to $1.0$.

### 12.5 Zipf's Law Exploration
$$f(r) \propto \frac{1}{r^s}$$
Evaluates the distribution of frequency against rank on logarithmic scales against an empirical reference slope.

---

## 13. Data Visualisations Included

1. **Top N Most Frequent Sanskrit Tokens:** Interactive horizontal bar chart displaying tokens, ranks, and exact percentages.
2. **Word Frequency Occurrence Spectrum:** Distribution histogram showing the number of words occurring at frequency tiers (1, 2, 3, 4, 5-9, 10-19, 20+).
3. **Word Length Distribution:** Histogram displaying token length frequencies measured in Unicode code points with mean and median indicators.
4. **Vocabulary Composition (Lexical Diversity):** Donut chart illustrating unique vocabulary types versus repeated token instances.
5. **Vocabulary Stratification:** Donut chart breaking down Hapax Legomena, Dis Legomena, and Higher Frequency items.
6. **Cumulative Frequency (Pareto Analysis):** Dual-axis bar and line chart illustrating lexical concentration and the 80% lexical mass threshold.
7. **Frequency Rank Curve (Zipf Analysis):** Log-log plot of empirical frequency vs. rank compared against a theoretical Zipf reference line.
8. **Section-Wise Distribution:** Dual-axis chart tracking token counts and lexical diversity (TTR) across text segments.
9. **Cross-Text Overlap Chart:** Proportional composition chart visualizing shared vocabulary vs. text-unique words.

---

## 14. Academic Integrity & Known Limitations

In compliance with rigorous IKS academic standards:
1. **Orthographic Boundaries:** Tokens represent surface orthographic units as written. The tokenizer preserves sandhi combinations and compound words (*samāsa*) without fabricating morphological segmentations.
2. **Length Measurement:** Length is reported in Unicode code points, not phonetic syllables (*akṣaras*).
3. **Stopword Policy:** Sanskrit indeclinables (*avyayas*) carry essential syntactic force. Filtering is optional and disabled by default.
4. **Descriptive Not Interpretative:** Computational observations report empirical metrics without claiming theological or philosophical interpretations.

---

## 15. Bundled Classical Corpora & Provenance

All bundled sample texts are drawn from verified public-domain editions of classical Sanskrit literature:
1. **Bhagavad Gītā (Chapter 2, Verses 11–25):** Samkhya Yoga philosophical discourse. Concordance with the Bhandarkar Oriental Research Institute (BORI) Critical Edition / Sanskrit Documents project.
2. **Īśāvāsya Upaniṣad (Verses 1–18):** Shukla Yajurveda Samhita (Adhyaya 40). Göttingen Register of Electronic Texts in Indian Languages (GRETIL).
3. **Subhāṣitaratnabhaṇḍāgāra (Selected Verses):** Classical didactic poetry on wisdom (*Vidyā*), effort (*Udyama*), and truth (*Satyam*). Nirnaya Sagar Press Edition (1911).
4. **Pañcatantra (Mitrabheda Kathāmukha):** Opening didactic fable prose by Pandit Vishnu Sharma. Kosegarten / Hertel Panchatantra Editions.

---

## 16. Future Scope

- Integration with rule-based Pāṇinian morphological analyzers (e.g., Sanskrit Heritage Site engine) for optional sandhi decomposition.
- Phonetic grapheme-cluster parser for computing true metrical syllable (*akṣara*) counts and poetic meters (*chandas*).
- Corpus-scale indexing across the complete Mahābhārata and Rāmāyaṇa recensions.

---

## 17. License

This project is licensed under the MIT License for educational, academic, and research applications. Classical Sanskrit texts included in the sample repository reside in the Public Domain.

