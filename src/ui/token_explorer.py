"""Token Explorer and Inspection Interface for SanskritLens."""

from __future__ import annotations
import streamlit as st
import pandas as pd
from ..nlp.frequency import search_word_frequency
from ..utils.exporters import export_to_csv


def render_token_explorer() -> None:
    """Render the interactive, searchable, and sortable token explorer table and inspector."""
    result = st.session_state.get("analysis_result")

    if result is None:
        st.warning("⚠️ No active analysis found. Please run an analysis on the Text Input page first.")
        if st.button("👉 Go to Text Input Studio", type="primary"):
            st.session_state["current_page"] = "Input"
            st.rerun()
        return

    freq_df = result.frequency_df
    total_tokens = result.stats.get("total_tokens", 0)

    st.markdown(
        """
        <div style="margin-bottom: 1.2rem;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">
                Lexical Inspection Studio
            </div>
            <h2 style="color: #1E1B4B; margin-top: 0.1rem; margin-bottom: 0.2rem;">Sanskrit Token Explorer</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Search, filter, and inspect orthographic tokens, their frequencies, ranks, and Unicode compositions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if freq_df.empty:
        st.info("No tokens found in the active text.")
        return

    # Two column layout: Left = Search & Filter Table, Right = Individual Token Inspector
    col_table, col_inspect = st.columns([3, 2])

    with col_table:
        st.markdown("### 🔍 Filter & Search Lexicon")

        # Search Query
        search_query = st.text_input(
            "Search Sanskrit Token (Devanagari):",
            placeholder="Search for a word (e.g., धर्म, देह, न, आत्मा)...",
        ).strip()

        # Filters in collapsible expander
        with st.expander("⚙️ Refine Table Filters", expanded=False):
            max_freq = int(freq_df["Frequency"].max()) if not freq_df.empty else 1
            min_freq_val, max_freq_val = st.slider(
                "Filter by Frequency Range:",
                min_value=1,
                max_value=max_freq,
                value=(1, max_freq),
            )

            sort_by = st.selectbox(
                "Sort Results By:",
                options=[
                    "Frequency (Highest to Lowest)",
                    "Frequency (Lowest to Highest)",
                    "Token (Alphabetical / Unicode)",
                    "Token Length (Descending)",
                ],
            )

        # Apply Filters
        filtered_df = freq_df.copy()

        if search_query:
            filtered_df = filtered_df[
                filtered_df["Token"].str.contains(search_query, regex=False, na=False)
            ]

        filtered_df = filtered_df[
            (filtered_df["Frequency"] >= min_freq_val)
            & (filtered_df["Frequency"] <= max_freq_val)
        ]

        # Apply Sorting
        if sort_by == "Frequency (Highest to Lowest)":
            filtered_df = filtered_df.sort_values(by=["Frequency", "Token"], ascending=[False, True])
        elif sort_by == "Frequency (Lowest to Highest)":
            filtered_df = filtered_df.sort_values(by=["Frequency", "Token"], ascending=[True, True])
        elif sort_by == "Token (Alphabetical / Unicode)":
            filtered_df = filtered_df.sort_values(by="Token", ascending=True)
        elif sort_by == "Token Length (Descending)":
            filtered_df["Length"] = filtered_df["Token"].apply(len)
            filtered_df = filtered_df.sort_values(by="Length", ascending=False)

        st.caption(f"Showing **{len(filtered_df):,}** of **{len(freq_df):,}** unique vocabulary tokens.")

        # Interactive Streamlit Dataframe
        display_cols = ["Rank", "Token", "Frequency", "Percentage", "Cumulative_Percentage"]
        if "Length" in filtered_df.columns:
            display_cols.append("Length")

        st.dataframe(
            filtered_df[display_cols],
            use_container_width=True,
            height=420,
            column_config={
                "Rank": st.column_config.NumberColumn("Rank", format="%d"),
                "Token": st.column_config.TextColumn("Sanskrit Token"),
                "Frequency": st.column_config.NumberColumn("Frequency", format="%d"),
                "Percentage": st.column_config.NumberColumn("Share (%)", format="%.2f%%"),
                "Cumulative_Percentage": st.column_config.NumberColumn("Cumulative (%)", format="%.2f%%"),
            },
        )

        # Download button for filtered table
        csv_bytes = export_to_csv(filtered_df[display_cols], include_bom=True)
        st.download_button(
            "📥 Download Filtered Vocabulary (CSV)",
            data=csv_bytes,
            file_name="sanskritlens_filtered_tokens.csv",
            mime="text/csv",
        )

    # INDIVIDUAL TOKEN INSPECTOR (RIGHT COLUMN)
    with col_inspect:
        st.markdown("### 🔬 Individual Token Inspector")
        st.markdown("Select or type an exact Sanskrit token to inspect its detailed corpus profile:")

        token_to_inspect = st.selectbox(
            "Select from Vocabulary:",
            options=freq_df["Token"].tolist(),
            index=0 if not freq_df.empty else None,
        )

        manual_inspect = st.text_input("Or enter exact token to inspect:", value="").strip()
        target_token = manual_inspect if manual_inspect else token_to_inspect

        if target_token:
            inspect_info = search_word_frequency(freq_df, target_token, total_tokens)

            if inspect_info:
                st.markdown(
                    f"""
                    <div style="background-color: #FAF8F5; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1.2rem; margin-top: 0.5rem;">
                        <div style="font-size: 0.8rem; color: #B45309; font-weight: 600; text-transform: uppercase;">Orthographic Token</div>
                        <h2 style="font-family: 'Noto Sans Devanagari', serif; color: #1E1B4B; margin: 0.2rem 0 0.8rem 0;">{target_token}</h2>
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                            <tr style="border-bottom: 1px solid #E2E8F0;">
                                <td style="padding: 6px 0; color: #64748B;">Corpus Rank</td>
                                <td style="padding: 6px 0; font-weight: 700; color: #1E1B4B; text-align: right;">#{inspect_info['rank']}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #E2E8F0;">
                                <td style="padding: 6px 0; color: #64748B;">Occurrence Count</td>
                                <td style="padding: 6px 0; font-weight: 700; color: #B45309; text-align: right;">{inspect_info['frequency']} times</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #E2E8F0;">
                                <td style="padding: 6px 0; color: #64748B;">Corpus Share</td>
                                <td style="padding: 6px 0; font-weight: 700; color: #1E1B4B; text-align: right;">{inspect_info['percentage']:.3f}%</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #E2E8F0;">
                                <td style="padding: 6px 0; color: #64748B;">Relative Frequency</td>
                                <td style="padding: 6px 0; font-weight: 700; color: #0F766E; text-align: right;">{inspect_info['per_thousand']} per 1,000 tokens</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #E2E8F0;">
                                <td style="padding: 6px 0; color: #64748B;">Code Point Length</td>
                                <td style="padding: 6px 0; font-weight: 700; color: #1E1B4B; text-align: right;">{len(target_token)} Unicode code points</td>
                            </tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Unicode Code Point Decomposition
                with st.expander("🔤 Unicode Code Point Breakdown", expanded=False):
                    cps = [f"U+{ord(c):04X} ({c})" for c in target_token]
                    st.code("\n".join(cps), language="text")
                    st.caption("Each code point represents an individual Unicode entity (consonant, matra, or halant).")
            else:
                st.warning(f"Token '{target_token}' was not found in the current corpus.")

