"""Analysis Dashboard Interface for SanskritLens."""

from __future__ import annotations
import streamlit as st
from ..visualization.charts import (
    plot_top_frequencies,
    plot_frequency_distribution,
    plot_word_length_distribution,
    plot_vocabulary_composition,
    plot_hapax_breakdown,
    plot_pareto_analysis,
    plot_frequency_rank_curve,
)
from ..utils.exporters import (
    export_to_csv,
    export_to_json,
    export_to_txt_summary,
    export_to_pdf_report,
)


def render_dashboard() -> None:
    """Render the primary analytical dashboard with KPI metrics and charts."""
    result = st.session_state.get("analysis_result")

    if result is None:
        st.warning("⚠️ No active analysis found. Please select or paste a Sanskrit text first.")
        if st.button("👉 Go to Text Input Studio", type="primary"):
            st.session_state["current_page"] = "Input"
            st.rerun()
        return

    stats = result.stats
    script_info = result.script_info
    freq_df = result.frequency_df
    length_df = result.length_df
    vocab_info = result.vocabulary_info

    # Header and Script Indicator
    source_label = st.session_state.get("text_source_label", "Analyzed Text")
    st.markdown(
        f"""
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">
                Analytical Dashboard &bull; {source_label}
            </div>
            <h2 style="color: #1E1B4B; margin-top: 0.1rem; margin-bottom: 0.2rem;">Sanskrit Lexical Analytics</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Script Detection Alert / Composition Notice
    if script_info.get("warning"):
        st.info(script_info["warning"], icon="ℹ️")

    # Script Distribution Quick Pills
    col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
    col_s1.metric("Primary Script", script_info.get("primary_script", "Unknown"))
    col_s2.metric("Devanagari Share", f"{script_info.get('devanagari_pct', 0.0)}%")
    col_s3.metric("Sanskrit Punctuation", f"{script_info.get('sanskrit_punct_count', 0)}")
    col_s4.metric("Numerals", f"{script_info.get('digits_total_count', 0)}")
    col_s5.metric("Total Characters", f"{stats.get('total_characters', 0):,}")

    st.markdown("---")

    # 1. SIX PRIMARY KPI METRIC CARDS
    st.markdown("### 📌 Key Corpus & Lexical Metrics")
    k1, k2, k3, k4, k5, k6 = st.columns(6)

    k1.metric(
        label="Total Tokens",
        value=f"{stats.get('total_tokens', 0):,}",
        help="Total orthographic word tokens after tokenisation & configured filtering.",
    )
    k2.metric(
        label="Unique Tokens",
        value=f"{stats.get('unique_tokens', 0):,}",
        help="Number of distinct orthographic word types.",
    )
    k3.metric(
        label="Type-Token Ratio",
        value=f"{stats.get('type_token_ratio', 0.0):.4f}",
        help="TTR = Unique Tokens / Total Tokens. Measures lexical diversity.",
    )
    k4.metric(
        label="Avg Token Length",
        value=f"{stats.get('average_token_length', 0.0):.2f}",
        help="Measured in Unicode code points per word token.",
    )
    k5.metric(
        label="Total Segments",
        value=f"{stats.get('total_segments', 0):,}",
        help="Sentence or verse segments delimited by danda (।), double danda (॥), or line breaks.",
    )
    k6.metric(
        label="Hapax Legomena",
        value=f"{stats.get('hapax_count', 0):,}",
        delta=f"{stats.get('hapax_percentage', 0.0):.1f}% of vocab",
        delta_color="off",
        help="Tokens occurring exactly once in the entire text.",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Top-N Chart Controls
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        st.markdown("### 📈 Visual Data Analytics")
    with col_ctrl2:
        top_n = st.slider(
            "Top N tokens to display:",
            min_value=5,
            max_value=min(50, max(5, len(freq_df))),
            value=min(15, len(freq_df)) if len(freq_df) > 0 else 10,
            step=5,
        )

    # 2. CHARTS GRID
    # Row 1: Top N Frequencies + Occurrence Spectrum
    c_r1_1, c_r1_2 = st.columns(2)
    with c_r1_1:
        fig_top = plot_top_frequencies(freq_df, top_n=top_n)
        st.plotly_chart(fig_top, use_container_width=True)
    with c_r1_2:
        fig_dist = plot_frequency_distribution(freq_df)
        st.plotly_chart(fig_dist, use_container_width=True)

    # Row 2: Word Length Distribution + Vocabulary Composition
    c_r2_1, c_r2_2 = st.columns(2)
    with c_r2_1:
        fig_len = plot_word_length_distribution(length_df)
        st.plotly_chart(fig_len, use_container_width=True)
    with c_r2_2:
        fig_comp = plot_vocabulary_composition(
            total_tokens=stats.get("total_tokens", 0),
            unique_tokens=stats.get("unique_tokens", 0),
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    # Row 3: Hapax Stratification + Pareto Analysis
    c_r3_1, c_r3_2 = st.columns(2)
    with c_r3_1:
        fig_hapax = plot_hapax_breakdown(vocab_info)
        st.plotly_chart(fig_hapax, use_container_width=True)
    with c_r3_2:
        fig_pareto = plot_pareto_analysis(freq_df, top_n=min(30, len(freq_df)))
        st.plotly_chart(fig_pareto, use_container_width=True)

    # Row 4: Zipf Rank-Frequency Curve
    st.markdown("#### 🔬 Rank-Frequency Distribution (Zipf's Law Exploration)")
    fig_zipf = plot_frequency_rank_curve(freq_df)
    st.plotly_chart(fig_zipf, use_container_width=True)
    st.caption(
        "**Note on Zipf Analysis:** Plotted on logarithmic axes. In natural languages, word frequencies often exhibit "
        "power-law decay roughly proportional to 1/rank. This chart enables empirical inspection without asserting unconditional conformity."
    )

    st.markdown("---")

    # 3. EXPORT FACILITY
    st.markdown("### 📥 Export & Download Results")
    st.markdown("Export the complete token frequencies, corpus metrics, and analysis configuration:")

    e1, e2, e3, e4 = st.columns(4)

    with e1:
        csv_bytes = export_to_csv(freq_df, include_bom=True)
        st.download_button(
            label="📊 Download CSV (UTF-8 BOM)",
            data=csv_bytes,
            file_name="sanskritlens_word_frequencies.csv",
            mime="text/csv",
            use_container_width=True,
            help="Excel-friendly CSV with Devanagari characters preserved via UTF-8-sig BOM.",
        )

    with e2:
        json_str = export_to_json(result)
        st.download_button(
            label="⚙️ Download JSON",
            data=json_str,
            file_name="sanskritlens_analysis.json",
            mime="application/json",
            use_container_width=True,
            help="Machine-readable structured JSON dataset with metadata and parameters.",
        )

    with e3:
        txt_str = export_to_txt_summary(result, title=f"SanskritLens Report: {source_label}")
        st.download_button(
            label="📄 Download TXT Summary",
            data=txt_str,
            file_name="sanskritlens_summary.txt",
            mime="text/plain",
            use_container_width=True,
            help="Human-readable academic text report.",
        )

    with e4:
        pdf_bytes = export_to_pdf_report(result, title=f"SanskritLens: {source_label}")
        st.download_button(
            label="📑 Download PDF Report",
            data=pdf_bytes,
            file_name="sanskritlens_report.pdf",
            mime="application/pdf",
            use_container_width=True,
            help="Formatted academic PDF report with metric tables.",
        )

