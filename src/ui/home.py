"""Home and Overview Page for SanskritLens."""

from __future__ import annotations
import streamlit as st


def render_home_page() -> None:
    """Render the scholarly landing page for SanskritLens."""
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 1rem 1.5rem 1rem;">
            <div style="display: inline-block; background-color: #FEF3C7; color: #92400E; font-size: 0.85rem; font-weight: 600; padding: 0.25rem 0.8rem; border-radius: 9999px; border: 1px solid #FDE68A; margin-bottom: 0.8rem;">
                INDIAN KNOWLEDGE SYSTEMS (IKS) &bull; COMPUTATIONAL LINGUISTICS
            </div>
            <h1 style="font-family: 'Noto Sans Devanagari', 'Segoe UI', serif; color: #1E1B4B; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.2rem; letter-spacing: -0.5px;">
                संस्कृतलेन्स <span style="color: #B45309;">SanskritLens</span>
            </h1>
            <p style="color: #475569; font-size: 1.25rem; font-weight: 400; max-width: 720px; margin: 0 auto 1.5rem auto;">
                Explore Sanskrit Through Computational Linguistics.
            </p>
            <p style="color: #64748B; font-size: 0.95rem; max-width: 780px; margin: 0 auto 2rem auto; line-height: 1.6;">
                A rigorous, locally executable digital platform designed for Sanskrit scholars, linguists, 
                and IKS researchers to perform Devanagari-aware tokenisation, word-frequency ranking, 
                lexical diversity measurement, and interactive corpus analytics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action Banner
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button(
            "🚀 Start Text Analysis Now",
            type="primary",
            use_container_width=True,
            help="Navigate directly to the Text Input and Ingestion studio",
        ):
            st.session_state["current_page"] = "Input"
            st.rerun()

    st.markdown("---")

    # Three Core Pillars
    st.markdown("### 🏛️ Foundational Capabilities")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.25rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="color: #B45309; font-size: 1.5rem; margin-bottom: 0.5rem;">📜</div>
                <h4 style="color: #1E1B4B; margin-bottom: 0.4rem;">Devanagari Normalisation</h4>
                <p style="color: #475569; font-size: 0.88rem; line-height: 1.5;">
                    Applies strict Unicode NFC normalisation, strips UTF-8 BOMs, resolves whitespace variations, and meticulously preserves conjuncts, matras, halant, anusvara, and visarga.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.25rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="color: #0F766E; font-size: 1.5rem; margin-bottom: 0.5rem;">🔍</div>
                <h4 style="color: #1E1B4B; margin-bottom: 0.4rem;">Sanskrit-Aware Tokenisation</h4>
                <p style="color: #475569; font-size: 0.88rem; line-height: 1.5;">
                    Distinguishes lexical tokens from verse dandas (।, ॥) and punctuation without falsely segmenting internal combining ligatures. Preserves orthographic integrity.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            """
            <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.25rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="color: #1E1B4B; font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                <h4 style="color: #1E1B4B; margin-bottom: 0.4rem;">Empirical Visualisations</h4>
                <p style="color: #475569; font-size: 0.88rem; line-height: 1.5;">
                    Calculates Type-Token Ratios (TTR), Hapax Legomena, Pareto lexical concentration curves, and rank-frequency distributions rendered in responsive Plotly figures.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Academic Notice Card
    st.info(
        "**Academic Methodology Note:** In Sanskrit computational linguistics, a whitespace-delimited "
        "orthographic token is not identical to a morphological lemma or grammatical word. Due to sandhi (सन्धि) "
        "and compound formation (समास), surface tokens are preserved as the transparent unit of empirical analysis. "
        "SanskritLens explicitly reports calculated metrics without making unsubstantiated claims about automatic "
        "morphological segmentation.",
        icon="ℹ️",
    )

    # Overview of Features in 2 Columns
    col_feat1, col_feat2 = st.columns(2)

    with col_feat1:
        st.markdown("#### 📂 Supported Input Workflows")
        st.markdown(
            """
            - **Curated Classical Corpora**: Instant access to verified public-domain samples:
              - *Bhagavad Gita* (Chapter 2, Sankhya Yoga)
              - *Isha Upanishad* (Complete 18 verses)
              - *Subhashita Ratna Bhandagara* (Wisdom & Ethics anthologies)
              - *Panchatantra* (Kathāmukha narrative prose)
            - **Custom Text Upload**: Direct ingestion of `.txt` and `.md` files with automatic UTF-8 validation and BOM removal.
            - **Direct Sanskrit Input**: Live interactive workspace with real-time character counting.
            """
        )

    with col_feat2:
        st.markdown("#### 📥 Publication-Ready Exports")
        st.markdown(
            """
            - **UTF-8 with BOM CSV**: Ready for Excel, Google Sheets, or R without Devanagari character garbling.
            - **Structured JSON**: Complete analysis configuration, raw tokens, statistics, and top frequencies.
            - **Plain Text (TXT) Summary**: Formatted monograph-style academic summary.
            - **Academic PDF Report**: Formatted documentation featuring key metric tables and Devanagari font embedding.
            """
        )

