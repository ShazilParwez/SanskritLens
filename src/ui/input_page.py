"""Text Input and Ingestion Interface for SanskritLens."""

from __future__ import annotations
import streamlit as st
from ..utils.file_handler import load_sample_metadata, load_sample_text_by_id, read_uploaded_file
from ..utils.validators import validate_input_text
from ..nlp.analysis import analyze_text
from ..nlp.stopwords import get_default_stopwords


def render_input_page() -> None:
    """Render the multi-channel text input and configuration interface."""
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="color: #1E1B4B; margin-bottom: 0.2rem;">Text Ingestion & Analysis Configuration</h2>
            <p style="color: #64748B; font-size: 0.95rem;">
                Select a verified classical Sanskrit sample, upload a local document, or paste Sanskrit text directly.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state for working text if not present
    if "working_text" not in st.session_state:
        # Default with the first sample
        default_content, _ = load_sample_text_by_id("bhagavad_gita_ch2")
        st.session_state["working_text"] = default_content
        st.session_state["selected_sample_id"] = "bhagavad_gita_ch2"
        st.session_state["text_source_label"] = "Bhagavad Gita (Chapter 2 Excerpt)"

    # Tab selection for input channels
    tab_sample, tab_upload, tab_direct = st.tabs(
        ["📜 Built-in Classical Samples", "📁 Document Upload (.txt, .md)", "✍️ Direct Sanskrit Text Area"]
    )

    # 1. BUILT-IN SAMPLES TAB
    with tab_sample:
        samples = load_sample_metadata()
        sample_options = {s["id"]: f"{s['english_title']} — {s['title']}" for s in samples}

        current_id = st.session_state.get("selected_sample_id", "bhagavad_gita_ch2")
        if current_id not in sample_options:
            current_id = list(sample_options.keys())[0] if sample_options else None

        selected_id = st.selectbox(
            "Select Classical Sanskrit Corpus Sample:",
            options=list(sample_options.keys()),
            format_func=lambda x: sample_options[x],
            index=list(sample_options.keys()).index(current_id) if current_id else 0,
        )

        # Retrieve selected sample metadata
        selected_meta = next((s for s in samples if s["id"] == selected_id), None)
        if selected_meta:
            col_m1, col_m2 = st.columns([2, 1])
            with col_m1:
                st.markdown(f"**Work / Tradition:** {selected_meta.get('source_work')}")
                st.markdown(f"**Author / Attribution:** {selected_meta.get('author_tradition')}")
                st.markdown(f"**Description:** {selected_meta.get('description')}")
            with col_m2:
                st.markdown(f"**Section:** {selected_meta.get('chapter_section')}")
                st.markdown(f"**License:** `{selected_meta.get('license')}`")
                if selected_meta.get("source_url"):
                    st.markdown(f"**Source:** [Digital Archive]({selected_meta.get('source_url')})")

            if st.button("📥 Load This Sample Text", key="btn_load_sample"):
                text_content, _ = load_sample_text_by_id(selected_id)
                st.session_state["working_text"] = text_content
                st.session_state["selected_sample_id"] = selected_id
                st.session_state["text_source_label"] = selected_meta.get("english_title")
                # Immediately synchronize analysis result to prevent stale state
                st.session_state["analysis_result"] = analyze_text(
                    text_content,
                    options={
                        "mode": "standard",
                        "remove_punctuation": True,
                        "exclude_numerals": True,
                        "min_token_length": 1,
                        "filter_stopwords": False,
                    },
                )
                st.success(f"Loaded & Analyzed: {selected_meta.get('english_title')}")
                st.rerun()

    # 2. FILE UPLOAD TAB
    with tab_upload:
        st.markdown("Upload a UTF-8 encoded text or Markdown file containing Sanskrit literature:")
        uploaded_file = st.file_uploader(
            "Choose a file (.txt or .md):",
            type=["txt", "md"],
            help="Files up to 10 MB in UTF-8 format are supported.",
        )
        if uploaded_file is not None:
            text_content, err = read_uploaded_file(uploaded_file)
            if err:
                st.error(err)
            else:
                st.success(f"File '{uploaded_file.name}' decoded successfully ({len(text_content):,} characters).")
                if st.button("📥 Use Uploaded File", key="btn_use_upload"):
                    st.session_state["working_text"] = text_content
                    st.session_state["selected_sample_id"] = None
                    st.session_state["text_source_label"] = f"Uploaded File: {uploaded_file.name}"
                    st.session_state["analysis_result"] = analyze_text(
                        text_content,
                        options={
                            "mode": "standard",
                            "remove_punctuation": True,
                            "exclude_numerals": True,
                            "min_token_length": 1,
                            "filter_stopwords": False,
                        },
                    )
                    st.success(f"Loaded & Analyzed: {uploaded_file.name}")
                    st.rerun()

    # 3. DIRECT TEXT AREA TAB
    with tab_direct:
        current_text = st.session_state.get("working_text", "")
        pasted_text = st.text_area(
            "Type or paste Sanskrit Devanagari text:",
            value=current_text,
            height=200,
            placeholder="Type or paste Sanskrit text here (e.g., धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः।)...",
            key="direct_text_area",
        )
        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.caption(f"Character Count: **{len(pasted_text):,}** characters | Lines: **{len(pasted_text.splitlines()):,}**")
        with col_c2:
            if st.button("Update Working Text", key="btn_update_text"):
                st.session_state["working_text"] = pasted_text
                st.session_state["text_source_label"] = "User Direct Input"
                st.session_state["analysis_result"] = analyze_text(
                    pasted_text,
                    options={
                        "mode": "standard",
                        "remove_punctuation": True,
                        "exclude_numerals": True,
                        "min_token_length": 1,
                        "filter_stopwords": False,
                    },
                )
                st.success("Working text updated & analyzed.")
                st.rerun()

    st.markdown("---")

    # PREVIEW OF CURRENT WORKING TEXT
    active_text = st.session_state.get("working_text", "")
    source_label = st.session_state.get("text_source_label", "Active Workspace")

    st.markdown(f"### 📖 Active Text in Workspace: *{source_label}*")
    with st.expander("👁️ View / Inspect Active Text", expanded=False):
        st.text_area("Workspace Text Preview:", value=active_text, height=180, disabled=True)

    # ANALYSIS CONFIGURATION & TOKENISATION MODES
    st.markdown("### ⚙️ Tokenisation & Analysis Configuration")

    mode_choice = st.radio(
        "Select Tokenisation Mode:",
        options=["Mode A: Standard Tokenisation", "Mode B: Normalised Tokenisation", "Mode C: Custom Tokenisation"],
        index=0,
        horizontal=True,
        help="Mode A retains surface forms with punctuation stripped from lexical tokens. Mode B normalises numerals. Mode C offers granular filtering.",
    )

    # Initialize configuration parameters based on mode
    opts = {}
    if "Mode A" in mode_choice:
        opts = {
            "mode": "standard",
            "remove_punctuation": True,
            "exclude_numerals": True,
            "min_token_length": 1,
            "filter_stopwords": False,
            "lowercase_latin": False,
        }
        st.info("ℹ️ **Mode A (Standard):** Unicode NFC normalised, verse punctuation (।, ॥) separated from words, original orthographic Sanskrit forms retained.")
    elif "Mode B" in mode_choice:
        opts = {
            "mode": "normalised",
            "remove_punctuation": True,
            "exclude_numerals": True,
            "min_token_length": 1,
            "filter_stopwords": False,
            "lowercase_latin": True,
        }
        st.info("ℹ️ **Mode B (Normalised):** Standard tokenisation with standalone numerals excluded, punctuation stripped, and case normalisation for any Latin segments.")
    else:  # Mode C
        opts = {"mode": "custom"}
        c_cfg1, c_cfg2 = st.columns(2)
        with c_cfg1:
            opts["remove_punctuation"] = st.checkbox("Remove punctuation from word tokens", value=True)
            opts["exclude_numerals"] = st.checkbox("Exclude standalone numbers (०-९, 0-9)", value=True)
            opts["min_token_length"] = st.number_input("Minimum Token Length (Unicode Code Points):", min_value=1, max_value=20, value=1)
        with c_cfg2:
            opts["filter_stopwords"] = st.checkbox(
                "Enable illustrative Sanskrit stopword filtering",
                value=False,
                help="Sanskrit indeclinables (च, अपि, एव, तु, etc.) will be omitted from frequency tables.",
            )
            opts["lowercase_latin"] = st.checkbox("Lowercase Latin / Transliterated text", value=True)

        if opts["filter_stopwords"]:
            with st.expander("📝 Customise Sanskrit Stopword List", expanded=False):
                default_stops = get_default_stopwords()
                st.caption(f"Default list contains {len(default_stops)} common Sanskrit particles, pronouns, and indeclinables.")
                stopword_text = st.text_area(
                    "Edit comma-separated stopwords:",
                    value=", ".join(default_stops),
                    height=100,
                )
                custom_list = [w.strip() for w in stopword_text.split(",") if w.strip()]
                opts["custom_stopwords"] = custom_list

    st.markdown("<br>", unsafe_allow_html=True)

    # ANALYZE BUTTON
    col_run1, col_run2, col_run3 = st.columns([1, 2, 1])
    with col_run2:
        if st.button("🔬 Execute SanskritLens Analysis Pipeline", type="primary", use_container_width=True):
            is_valid, err_msg = validate_input_text(active_text)
            if not is_valid:
                st.error(err_msg)
            else:
                with st.spinner("Executing Sanskrit NLP pipeline (NFC normalisation, script check, tokenisation)..."):
                    result = analyze_text(active_text, options=opts)
                    st.session_state["analysis_result"] = result
                    st.session_state["current_page"] = "Dashboard"
                    st.success("Analysis complete! Navigating to Dashboard...")
                    st.rerun()

