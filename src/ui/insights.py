"""Text Insights and Dynamic Observation Module for SanskritLens."""

from __future__ import annotations
import streamlit as st


def render_insights() -> None:
    """Render dynamically computed, data-driven observations from the analyzed Sanskrit text."""
    result = st.session_state.get("analysis_result")

    if result is None:
        st.warning("⚠️ No active analysis found. Please run an analysis on the Text Input page first.")
        if st.button("👉 Go to Text Input Studio", type="primary"):
            st.session_state["current_page"] = "Input"
            st.rerun()
        return

    stats = result.stats
    freq_df = result.frequency_df
    length_summary = result.length_summary
    source_label = st.session_state.get("text_source_label", "Analyzed Corpus")

    st.markdown(
        f"""
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">
                Computational Observations &bull; {source_label}
            </div>
            <h2 style="color: #1E1B4B; margin-top: 0.1rem; margin-bottom: 0.2rem;">Empirical Text Insights</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Quantitative linguistic observations derived algorithmically from word frequencies, distributions, and length patterns.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if freq_df.empty:
        st.info("Insufficient data to generate linguistic insights.")
        return

    total_tokens = stats.get("total_tokens", 0)
    unique_tokens = stats.get("unique_tokens", 0)
    ttr = stats.get("type_token_ratio", 0.0)
    hapax_count = stats.get("hapax_count", 0)
    hapax_pct = stats.get("hapax_percentage", 0.0)

    # 1. Lexical Dominance Observation
    top_row = freq_df.iloc[0]
    top_word = top_row["Token"]
    top_freq = int(top_row["Frequency"])
    top_pct = float(top_row["Percentage"])

    # 2. Cumulative Mass: Tokens required for 50% of the corpus
    half_mass_tokens = 0
    running_sum = 0
    target_50 = total_tokens * 0.5
    for _, r in freq_df.iterrows():
        running_sum += int(r["Frequency"])
        half_mass_tokens += 1
        if running_sum >= target_50:
            break

    half_mass_pct_vocab = (
        round((half_mass_tokens / unique_tokens) * 100, 1) if unique_tokens > 0 else 0.0
    )

    # 3. Dynamic insight cards
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border-left: 4px solid #B45309; border: 1px solid #E2E8F0; border-radius: 6px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                <h4 style="color: #B45309; margin: 0 0 0.4rem 0;">👑 Most Prevalent Lexical Item</h4>
                <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    The most frequently recurring orthographic token is <b>'{top_word}'</b>, occurring 
                    <b>{top_freq:,} times</b> and accounting for <b>{top_pct:.2f}%</b> of all token occurrences in this text.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border-left: 4px solid #0F766E; border: 1px solid #E2E8F0; border-radius: 6px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                <h4 style="color: #0F766E; margin: 0 0 0.4rem 0;">📚 Vocabulary Richness & Type-Token Ratio</h4>
                <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    The text exhibits a Type-Token Ratio (TTR) of <b>{ttr:.4f}</b> across <b>{total_tokens:,} tokens</b>, 
                    comprising <b>{unique_tokens:,} distinct orthographic word types</b>. 
                    {f"A TTR of {ttr:.2f} reflects high lexical variation characteristic of verse composition." if ttr > 0.6 else "A moderate TTR reflects significant thematic or particle repetition across discourse units."}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border-left: 4px solid #1E1B4B; border: 1px solid #E2E8F0; border-radius: 6px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                <h4 style="color: #1E1B4B; margin: 0 0 0.4rem 0;">⚖️ Lexical Concentration (Pareto Principle)</h4>
                <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    Just <b>{half_mass_tokens} distinct words</b> ({half_mass_pct_vocab}% of the unique vocabulary) 
                    constitute over <b>50% of the entire token volume</b>. 
                    This demonstrates significant vocabulary concentration in core nouns, verbs, and particles.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="background-color: #FFFFFF; border-left: 4px solid #D97706; border: 1px solid #E2E8F0; border-radius: 6px; padding: 1.1rem; margin-bottom: 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                <h4 style="color: #D97706; margin: 0 0 0.4rem 0;">🌱 Hapax Legomena (Single-Occurrence Lexemes)</h4>
                <p style="color: #334155; font-size: 0.92rem; line-height: 1.5; margin: 0;">
                    <b>{hapax_count:,} words ({hapax_pct:.1f}% of total vocabulary)</b> appear exactly once. 
                    In classical Sanskrit, high hapax frequencies often correspond to elaborate bahuvrīhi/tatpuruṣa compounds 
                    or specific inflected nominal and verbal paradigms.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Length & Morphological Structure Observations
    st.markdown("### 📏 Word Length & Structural Profiles")
    cl1, cl2, cl3 = st.columns(3)

    avg_len = length_summary.get("average_length", 0.0)
    longest_list = length_summary.get("longest_tokens", [])
    shortest_list = length_summary.get("shortest_tokens", [])

    cl1.metric("Mean Token Length", f"{avg_len:.2f} CPs", help="Unicode code points per token")
    cl2.metric("Median Token Length", f"{length_summary.get('median_length', 0):.1f} CPs")
    cl3.metric("Length Range", f"{length_summary.get('min_length', 0)} – {length_summary.get('max_length', 0)} CPs")

    st.markdown(
        f"""
        - **Shortest Tokens ({length_summary.get('min_length', 0)} CPs):** `{', '.join(shortest_list[:6])}`
        - **Longest Tokens ({length_summary.get('max_length', 0)} CPs):** `{', '.join(longest_list[:4])}`
        - **Segment Density:** The text contains **{stats.get('total_segments', 0):,} segments**, averaging **{stats.get('avg_tokens_per_segment', 0.0):.2f} tokens per segment**.
        """
    )

    st.info(
        "**Linguistic Integrity Reminder:** These computational observations describe empirical surface token patterns. "
        "They do not impute philosophical doctrines, theological assertions, or semantic translations. "
        "Computational linguistics provides structural evidence to support human scholars rather than replace them.",
        icon="⚖️",
    )

