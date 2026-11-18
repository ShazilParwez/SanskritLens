"""Methodology, Academic Context, and IKS Relevance Page for SanskritLens."""

from __future__ import annotations
import streamlit as st


def render_methodology_page() -> None:
    """Render comprehensive computational linguistics methodology and IKS relevance."""
    st.markdown(
        """
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">
                Computational Linguistics &bullet; Indian Knowledge Systems
            </div>
            <h2 style="color: #1E1B4B; margin-top: 0.1rem; margin-bottom: 0.2rem;">Methodology, Formalisms & Academic Notes</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Formal technical specification of the SanskritLens NLP processing pipeline, counting conventions, statistical equations, and linguistic scope.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Accordion Sections for Academic Review
    with st.expander("1. 🏛️ Relevance to Indian Knowledge Systems (IKS)", expanded=True):
        st.markdown(
            """
            The Indian Knowledge Systems (IKS) domain encompasses millennia of philosophical, scientific, 
            mathematical, and literary treatises composed in classical and Vedic Sanskrit. 
            Traditional Sanskrit scholarship relies heavily on rigorous linguistic models, most notably 
            the formal generative grammar of Pāṇini (*Aṣṭādhyāyī*).

            **How Computational Text Analytics Serves IKS:**
            - **Digital Preservation & Corpus Profiling:** Enables researchers to quantitatively assess vocabulary richness, lexical diversity, and authorship characteristics across diverse digital recensions.
            - **Lexical Pattern Discovery:** Uncovers recurring philosophical terms (e.g., *ātman*, *prakṛti*, *dharma*) and identifies hapax legomena representing specialized terminology or intricate compounds.
            - **Stylistic & Chronological Studies:** Measures Type-Token Ratios (TTR) and vocabulary overlap to assist comparative textual criticism between classical narrative prose and Vedic poetic meters.
            - **Reproducible Empirical Humanities:** Provides transparent, reproducible computational statistics that complement traditional textual hermeneutics.
            """
        )

    with st.expander("2. 📜 Unicode NFC Normalisation & Devanagari Script Handling", expanded=False):
        st.markdown(
            """
            Devanagari characters in digital text can be encoded in multiple Unicode equivalent sequences:
            
            1. **NFC (Canonical Decomposition followed by Canonical Composition):** 
               Combines base consonants and dependent vowel signs (*mātrās*) into standardized composite characters. 
               SanskritLens applies NFC normalisation uniformly before any tokenisation.
            2. **Preservation of Diacritical Marks:**
               - *Matras* (ा, ि, ी, ु, ू, ृ, ॄ, ॢ, ॣ, े, ै, ो, ौ)
               - *Virama / Halant* (् : U+094D)
               - *Anusvara* (ं : U+0902) & *Visarga* (ः : U+0903)
               - *Chandrabindu* (ँ : U+0901)
               - *Avagraha* (ऽ : U+093D)
               - *Vedic Svara Marks* (udātta, anudātta, svarita: U+0951-U+0954, U+1CD0-U+1CFF)
            3. **BOM & Whitespace Sanitation:**
               Strips UTF-8 Byte Order Marks (`\\ufeff`), normalises non-breaking spaces (NBSP: `\\u00a0`), 
               and collapses redundant whitespace without altering lexical integrity.
            """
        )

    with st.expander("3. 🔍 Orthographic Tokenisation vs Morphological Segmentation (Sandhi & Samasa)", expanded=False):
        st.markdown(
            """
            #### Critical Linguistic Boundary: Orthographic Unit vs Grammatical Lemma
            In modern English NLP, whitespace frequently delimits grammatical words. In Sanskrit, however:
            
            1. **Sandhi (सन्धि - Euphonic Combination):**
               Phonetic fusion between contiguous words fuses their orthographic representation.
               For example:
               $$\\text{ततो} + \\text{अब्रवीत्} \\longrightarrow \\text{ततोऽब्रवीत्}$$
               $$\\text{विद्या} + \\text{आलयः} \\longrightarrow \\text{विद्यालयः}$$
               A whitespace-based tokenizer cannot recover underlying component words without an extensive 
               morphological analyzer and disambiguation engine.
            2. **Samasa (समास - Nominal Compounds):**
               Sanskrit freely forms extensive nominal compounds (e.g., *rāja-puruṣaḥ*, *pīta-ambaraḥ*) that 
               appear as single surface orthographic tokens.

            **Methodological Principle in SanskritLens:**
            - **Unit of Analysis:** Surface orthographic tokens.
            - **Academic Integrity:** The platform explicitly **does not** claim to decompose sandhi or segment compounds automatically. 
              Claiming full sandhi resolution without verified linguistic morphology would risk academic inaccuracy.
            - Punctuation (danda ।, double danda ॥, commas, quotation marks) is cleanly disengaged from lexical tokens.
            """
        )

    with st.expander("4. 📐 Mathematical Formulations & Statistical Definitions", expanded=False):
        st.markdown(
            r"""
            #### 1. Type-Token Ratio (TTR)
            Measures lexical diversity:
            $$TTR = \frac{V}{N}$$
            where $V$ is the number of distinct vocabulary types (Unique Tokens), and $N$ is the total token count.

            #### 2. Average Token Length
            $$\text{Average Length} = \frac{1}{N} \sum_{i=1}^{N} \text{len}(t_i)$$
            **Counting Convention:** Length is strictly measured in **Unicode Code Points**. 
            In Devanagari, a code point is not equivalent to a phonetic akṣara (syllable). 
            For instance, the akṣara 'क्षि' comprises 4 code points: $\text{क} + \text{्} + \text{ष} + \text{ि}$.

            #### 3. Hapax Legomena & Dis Legomena
            - **Hapax Legomena ($H_1$):** Tokens occurring with frequency $f = 1$.
              $$\text{Hapax Share} = \frac{| \{ t \in V : f(t) = 1 \} |}{V} \times 100$$
            - **Dis Legomena ($H_2$):** Tokens occurring with frequency $f = 2$.

            #### 4. Jaccard Vocabulary Similarity
            For two texts with unique vocabulary sets $A$ and $B$:
            $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
            $J(A, B)$ quantifies surface lexical overlap on a scale from $0.0$ to $1.0$.

            #### 5. Zipf's Law Exploration
            Zipf's empirical law states that frequency $f$ of a token is inversely proportional to its rank $r$:
            $$f(r) \propto \frac{1}{r^s}$$
            SanskritLens displays empirical frequencies against $f(1)/r$ on logarithmic scales for exploratory inspection.
            """
        )

    with st.expander("5. 🛡️ Data Privacy & Offline Execution Guarantee", expanded=False):
        st.markdown(
            """
            - **Complete Offline Operation:** SanskritLens executes entirely on the local runtime environment.
            - **Zero External Network Dependencies:** No user-uploaded texts or direct input strings are transmitted to remote cloud APIs or third-party servers.
            - **Volatile Session State:** Uploaded files and texts reside purely in volatile memory during the active Streamlit session and are discarded upon session termination.
            """
        )

    with st.expander("6. 🛠️ Technology Stack & System Architecture", expanded=False):
        st.markdown(
            """
            - **Programming Language:** Python 3.11+
            - **Web Application Framework:** Streamlit
            - **Data Manipulation & Tabular Processing:** Pandas & NumPy
            - **Interactive Visualisation Engine:** Plotly Graph Objects & Express
            - **Static & PDF Report Generation:** Matplotlib & ReportLab
            - **Unicode Processing:** Python standard library `unicodedata` (NFC) & `re`
            - **Test Harness:** pytest automated testing suite
            """
        )

