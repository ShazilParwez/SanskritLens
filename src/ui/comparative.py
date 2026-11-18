"""Comparative Text Analysis and Section-Wise Breakdown for SanskritLens."""

from __future__ import annotations
import streamlit as st
import plotly.graph_objects as go
from ..nlp.analysis import analyze_sections, compare_texts
from ..nlp.tokenizer import tokenize_sanskrit
from ..utils.file_handler import load_sample_metadata, load_sample_text_by_id


def render_comparative_page() -> None:
    """Render section-wise decomposition and cross-text comparative linguistics."""
    result = st.session_state.get("analysis_result")

    st.markdown(
        """
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">
                Advanced Corpus Exploration
            </div>
            <h2 style="color: #1E1B4B; margin-top: 0.1rem; margin-bottom: 0.2rem;">Section-Wise & Comparative Analysis</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Examine lexical distribution across narrative sections or conduct set-theoretic comparative vocabulary analysis across two Sanskrit works.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_sections, tab_compare = st.tabs(["📑 Section-Wise Analysis", "⚖️ Cross-Text Comparative Analysis"])

    # 1. SECTION-WISE BREAKDOWN
    with tab_sections:
        if result is None:
            st.info("Please analyze a Sanskrit text first on the Text Input page.")
        else:
            active_text = result.raw_text
            st.markdown("### 📊 Lexical Density Across Discourse Units")

            sec_mode = st.radio(
                "Segment Text By:",
                options=["verse", "paragraph", "line"],
                format_func=lambda x: {
                    "verse": "Verse / Danda Units (।, ॥)",
                    "paragraph": "Paragraphs (Double Newline)",
                    "line": "Lines (Single Newline)",
                }[x],
                horizontal=True,
            )

            sec_df = analyze_sections(active_text, section_type=sec_mode, options=result.options)

            if sec_df.empty:
                st.warning("No sections could be delineated from the text.")
            else:
                # Plotly Chart: Token Count & TTR trend across sections
                fig_sec = go.Figure()
                fig_sec.add_trace(
                    go.Bar(
                        x=sec_df["Section"],
                        y=sec_df["Tokens"],
                        name="Token Count",
                        marker=dict(color="#CBD5E1"),
                    )
                )
                fig_sec.add_trace(
                    go.Scatter(
                        x=sec_df["Section"],
                        y=sec_df["TTR"],
                        name="Type-Token Ratio (TTR)",
                        yaxis="y2",
                        mode="lines+markers",
                        line=dict(color="#B45309", width=2),
                    )
                )
                fig_sec.update_layout(
                    title=f"Vocabulary Distribution across {len(sec_df)} Sections",
                    xaxis=dict(title="Section"),
                    yaxis=dict(title="Tokens per Section"),
                    yaxis2=dict(
                        title="TTR (Lexical Richness)",
                        overlaying="y",
                        side="right",
                        range=[0, 1.1],
                        showgrid=False,
                    ),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    plot_bgcolor="#FFFFFF",
                    paper_bgcolor="rgba(0,0,0,0)",
                    height=360,
                )
                st.plotly_chart(fig_sec, use_container_width=True)

                st.markdown("#### Section Details")
                st.dataframe(
                    sec_df,
                    use_container_width=True,
                    height=280,
                    column_config={
                        "Section": st.column_config.TextColumn("Section"),
                        "Snippet": st.column_config.TextColumn("Text Excerpt", width="large"),
                        "Tokens": st.column_config.NumberColumn("Tokens", format="%d"),
                        "Unique_Tokens": st.column_config.NumberColumn("Unique", format="%d"),
                        "TTR": st.column_config.NumberColumn("TTR", format="%.3f"),
                    },
                )

    # 2. COMPARATIVE TEXT ANALYSIS
    with tab_compare:
        st.markdown("### ⚖️ Cross-Text Vocabulary Overlap (Jaccard Index)")
        st.markdown(
            "Compare the lexical composition of two texts using set-theoretic overlap and Jaccard similarity: "
            r"$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$."
        )

        samples = load_sample_metadata()
        sample_map = {s["id"]: s["english_title"] for s in samples}

        col_in_a, col_in_b = st.columns(2)

        with col_in_a:
            st.markdown("#### Text A (Primary)")
            if result is not None:
                name_a = st.text_input("Label for Text A:", value="Text A (Workspace)").strip()
                tokens_a = result.tokens
                st.caption(f"Using active workspace tokens: **{len(tokens_a):,} tokens**.")
            else:
                sel_a = st.selectbox("Select Sample A:", options=list(sample_map.keys()), index=0, key="sel_comp_a")
                text_a_raw, _ = load_sample_text_by_id(sel_a)
                name_a = sample_map.get(sel_a, "Text A")
                tokens_a = tokenize_sanskrit(text_a_raw)

        with col_in_b:
            st.markdown("#### Text B (Comparison)")
            sel_b = st.selectbox(
                "Select Sample B:",
                options=list(sample_map.keys()),
                index=1 if len(sample_map) > 1 else 0,
                key="sel_comp_b",
            )
            text_b_raw, _ = load_sample_text_by_id(sel_b)
            name_b = st.text_input("Label for Text B:", value=sample_map.get(sel_b, "Text B")).strip()

            custom_b = st.text_area("Or paste custom Sanskrit text for Text B:", height=100, placeholder="Paste Sanskrit text for comparison...")
            if custom_b.strip():
                tokens_b = tokenize_sanskrit(custom_b)
                st.caption(f"Using pasted text: **{len(tokens_b):,} tokens**.")
            else:
                tokens_b = tokenize_sanskrit(text_b_raw)
                st.caption(f"Using sample text: **{len(tokens_b):,} tokens**.")

        if st.button("🔬 Execute Comparative Text Overlap Analysis", type="primary"):
            comp = compare_texts(tokens_a, tokens_b, name_a=name_a, name_b=name_b)

            st.markdown("---")
            st.markdown("#### 📊 Comparative Metric Summary")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric(f"Tokens ({name_a})", f"{comp['total_a']:,}", f"Vocab: {comp['unique_a']:,}")
            m2.metric(f"Tokens ({name_b})", f"{comp['total_b']:,}", f"Vocab: {comp['unique_b']:,}")
            m3.metric("Shared Vocabulary", f"{comp['common_count']:,} tokens", help="|A ∩ B|")
            m4.metric("Jaccard Similarity", f"{comp['jaccard_percentage']}%", help=f"Index: {comp['jaccard_similarity']}")

            st.markdown("<br>", unsafe_allow_html=True)

            # Venn / Donut overlap visual
            fig_jaccard = go.Figure(
                go.Pie(
                    labels=[f"Unique to {name_a}", "Shared Vocabulary", f"Unique to {name_b}"],
                    values=[len(comp["unique_to_a"]), comp["common_count"], len(comp["unique_to_b"])],
                    hole=0.55,
                    marker=dict(colors=["#B45309", "#0F766E", "#1E1B4B"]),
                    textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>Words: %{value}<br>Proportion: %{percent}<extra></extra>",
                )
            )
            fig_jaccard.update_layout(
                title=f"Vocabulary Overlap Breakdown: {name_a} vs {name_b}",
                height=340,
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_jaccard, use_container_width=True)

            # Shared Vocabulary Table
            shared_df = comp["shared_df"]
            if not shared_df.empty:
                st.markdown(f"#### 📜 Common Vocabulary Tokens ({len(shared_df):,} Shared Items)")
                st.dataframe(
                    shared_df,
                    use_container_width=True,
                    height=300,
                )

            st.info(
                "**Linguistic Overlap Caveat:** Jaccard similarity measures surface orthographic token intersection. "
                "In Sanskrit, high overlap may be driven by ubiquitous particles (च, अपि, एव) or shared philosophical vocabulary (e.g. आत्मा, देह). "
                "It represents lexical sharing, not theological or semantic identity.",
                icon="ℹ️",
            )

