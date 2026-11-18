# SanskritLens: Linguistic Methodology & Theoretical Framework

**Indian Knowledge Systems (IKS) &bull; Computational Linguistics**  
*Project Title:* Sanskrit Text Tokenisation and Word-Frequency Analysis Platform  
*Platform Name:* SanskritLens (संस्कृतलेन्स)

---

## 1. Introduction and Academic Rationale

Sanskrit is an inflected, synthetic language with a rich morphological structure, extensive nominal compounding (*samāsa*), and euphonic combination (*sandhi*). As the medium of Indian Knowledge Systems (IKS)—encompassing philosophical treatises (*Darśanas*), sciences (*Śāstras*), astronomical works (*Jyotiṣa*), medical texts (*Āyurveda*), and poetry (*Kāvya*)—digital text analysis of Sanskrit offers unprecedented avenues for textual criticism, lexical profiling, and digital humanities scholarship.

Traditional Sanskrit analysis relies upon formal generative grammar, codified principally by Pāṇini in the *Aṣṭādhyāyī*. When developing computational tools for Sanskrit text analysis, computer scientists must balance computational tractability with linguistic fidelity.

SanskritLens is specifically engineered to provide transparent, reproducible, and mathematically rigorous tokenisation and frequency statistics on digital Sanskrit texts without making unsubstantiated claims regarding automated morphological decomposition.

---

## 2. Orthographic Tokenisation vs. Morphological Segmentation

A central methodological consideration in Sanskrit computational linguistics is the distinction between an **orthographic token** and a **grammatical word (pada)**.

### 2.1 The Nature of Sandhi (सन्धि)
In continuous Sanskrit speech and writing, contiguous phonetic segments combine across word boundaries (*saṃhitā*):
$$\text{ततः} + \text{अब्रवीत्} \longrightarrow \text{ततोऽब्रवीत्}$$
$$\text{विद्या} + \text{आलयः} \longrightarrow \text{विद्यालयः}$$

In printed editions and manuscripts, sandhi often produces single orthographic strings that merge multiple lexical items. Recovering the underlying words (*padaccheda*) requires context-sensitive morphological disambiguation and lexical lookups.

### 2.2 The Nature of Samasa (समास)
Sanskrit generates complex nominal compounds without spaces:
$$\text{प्रवरनृपमुकुटमणिकिरणमञ्जरीचर्चितचरणयुगलः}$$
While conceptually consisting of multiple substantives, adjectives, and genitive relations, the compound functions as a single compound lexical unit.

### 2.3 Methodological Commitment of SanskritLens
SanskritLens adopts **surface orthographic tokenisation** as its foundational unit of analysis:
1. **Preservation of Surface Forms:** Tokens represent orthographic words as written in the selected digital edition.
2. **Transparent Boundaries:** Dandas (।), double dandas (॥), commas, quotes, and punctuation are cleanly disengaged from lexical tokens.
3. **Academic Conservatism:** The application does **not** simulate automated sandhi splitting or compound decomposition without validated morphological engines. This prevents fabricated lexical analyses and preserves reproducible empirical integrity.

---

## 3. Unicode Normalisation & Devanagari Encoding

Devanagari text in digital environments can suffer from encoding variability due to different input methods, font-encoding legacies, and Unicode representation forms.

### 3.1 Normalisation Form C (NFC)
Unicode allows certain characters to be represented as precomposed characters or decomposed sequences (base letter + combining mark). SanskritLens applies **NFC (Canonical Decomposition followed by Canonical Composition)** uniformly:
- Unifies combining matras with base consonants into standardized composite glyphs.
- Eliminates duplicate entries in frequency counters caused solely by distinct Unicode byte sequences for the identical grapheme.

### 3.2 Diacritical and Sign Preservation
The normalisation pipeline strictly preserves:
- **Dependent Vowel Signs (Mātrās):** ा, ि, ी, ु, ू, ृ, ॄ, ॢ, ॣ, े, ै, ो, ौ
- **Virāma / Halanta (् : U+094D):** Marks consonant clusters and vowel omission.
- **Anusvāra (ं : U+0902) & Visarga (ः : U+0903):** Nasalization and post-vocalic voiceless aspirate.
- **Anunāsika / Candrabindu (ँ : U+0901):** True nasalized vowels.
- **Avagraha (ऽ : U+093D):** Denotes elision of initial 'a' after 'e' or 'o'.
- **Vedic Svara Accents (U+0951-U+0954, U+1CD0-U+1CFF):** Udātta, Anudātta, and Svarita tones.

---

## 4. Statistical Formulations and Quantitative Metrics

### 4.1 Type-Token Ratio (TTR)
$$\text{TTR} = \frac{V}{N}$$
where:
- $V = |\text{Unique Tokens}|$ (Vocabulary richness)
- $N = |\text{Total Tokens}|$ (Corpus volume)

A high TTR indicates lexical variation and minimal word repetition; a lower TTR indicates significant repetition of key vocabulary, verbs, and connective particles.

### 4.2 Average Word Length
$$\bar{L} = \frac{1}{N} \sum_{i=1}^{N} \text{len}(t_i)$$
**Measurement Unit:** Length is reported strictly in **Unicode Code Points**. In Devanagari, a code point does not correspond to an *akṣara* (syllable). For example, 'स्त्री' comprises 5 Unicode code points (स + ् + त + ् + र + ी). This convention is documented to avoid misrepresenting code points as syllable metrics.

### 4.3 Hapax and Dis Legomena
- **Hapax Legomena ($H_1$):** Tokens occurring with frequency $f(t) = 1$.
$$\% H_1 = \frac{| \{ t \in V : f(t) = 1 \} |}{V} \times 100$$
- **Dis Legomena ($H_2$):** Tokens occurring with frequency $f(t) = 2$.
$$\% H_2 = \frac{| \{ t \in V : f(t) = 2 \} |}{V} \times 100$$

### 4.4 Jaccard Vocabulary Similarity
For two texts with unique vocabulary sets $A$ and $B$:
$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
Measures the proportion of shared orthographic words relative to total unique vocabulary across both texts.

### 4.5 Zipf-like Distribution Exploration
Zipf's empirical law observes that word frequency $f$ tends to be inversely proportional to frequency rank $r$:
$$f(r) \propto \frac{1}{r^s}$$
SanskritLens plots empirical frequencies against rank on logarithmic scales, offering an empirical baseline $f(1)/r$ for linguistic exploration.

---

## 5. Sanskrit Stopwords: Grammatical Perspective

In English NLP, function words (such as 'the', 'is', 'at') are often pruned as "stopwords". In Sanskrit grammatical theory (*Vyākaraṇa*):
- **Avyayāni (अव्ययानि - Indeclinables):** Words like *ca* (च - and), *eva* (एव - indeed), *api* (अपि - also), *tu* (तु - but), and *iti* (इति - thus) govern logical relations, discourse framing, and philosophical qualifiers.
- **Nipātas (निपाताः):** Particles can serve as sentence connectives, emphatic operators, or meter fillers.

**SanskritLens Policy:**
Filtering stopwords in Sanskrit alters syntactic relations. Consequently, stopword filtering is **disabled by default**. When activated by the researcher, an illustrative, editable list is provided with clear academic disclosures.

---

## 6. Summary of Academic Limitations

1. **No Sandhi Disambiguation:** Surface orthographic tokens are preserved; sandhi is not split automatically.
2. **No Compound Decomposition:** Extended nominal compounds remain intact as single tokens.
3. **No Morphological Lemmatisation:** Inflected case forms (e.g., *rāmaḥ*, *rāmam*, *rāmeṇa*) are counted as distinct surface types.
4. **No Automated Semantic Interpretation:** Insights reflect quantitative lexical data without imposing theological translations.

