"""SanskritLens - Sanskrit Text Tokenisation and Word-Frequency Analysis Platform.

Main Streamlit Application Entrypoint.
Academic Project under the Indian Knowledge Systems (IKS) domain.
"""

from __future__ import annotations
import sys
from pathlib import Path

# Ensure root package directory is in sys.path
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st

from src.ui.home import render_home_page
from src.ui.input_page import render_input_page
from src.ui.dashboard import render_dashboard
from src.ui.token_explorer import render_token_explorer
from src.ui.insights import render_insights
from src.ui.comparative import render_comparative_page
from src.ui.methodology import render_methodology_page
from src.nlp.analysis import analyze_text
from src.utils.file_handler import load_sample_text_by_id

# Configure page layout and branding
st.set_page_config(
    page_title="SanskritLens | संस्कृतलेन्स",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Scholarly CSS Injection
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600;700;800&family=Noto+Serif+Devanagari:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', 'Noto Sans Devanagari', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Primary Container Polish */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Sidebar Aesthetic */
    [data-testid="stSidebar"] {
        background-color: #F8F5EE;
        border-right: 1px solid #E5DFD3;
    }

    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #1E1B4B !important;
        font-weight: 700 !important;
        font-family: 'Noto Sans Devanagari', 'Inter', sans-serif !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-weight: 600;
        border-radius: 6px 6px 0 0;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.15s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"

if "analysis_result" not in st.session_state:
    # Auto-initialize with Bhagavad Gita Chapter 2 sample
    sample_text, meta = load_sample_text_by_id("bhagavad_gita_ch2")
    if sample_text:
        st.session_state["working_text"] = sample_text
        st.session_state["selected_sample_id"] = "bhagavad_gita_ch2"
        st.session_state["text_source_label"] = (
            meta.get("english_title") if meta else "Bhagavad Gita (Sample)"
        )
        st.session_state["analysis_result"] = analyze_text(
            sample_text,
            options={
                "mode": "standard",
                "remove_punctuation": True,
                "exclude_numerals": True,
                "min_token_length": 1,
                "filter_stopwords": False,
            },
        )

# Sidebar Navigation
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #E2DCD0; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 2rem;">📜</span>
                <div>
                    <h3 style="color: #1E1B4B; margin: 0; font-size: 1.3rem; font-weight: 800; line-height: 1.1;">
                        SanskritLens
                    </h3>
                    <span style="color: #B45309; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.4px;">
                        संस्कृत-पद-विश्लेषणम्
                    </span>
                </div>
            </div>
            <p style="color: #64748B; font-size: 0.78rem; margin: 0.5rem 0 0 0; line-height: 1.3;">
                Indian Knowledge Systems (IKS)<br>Text Tokenisation & Lexical Analytics
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page_options = [
        "🏠 Home / Overview",
        "📥 Text Input & Ingestion",
        "📊 Analysis Dashboard",
        "🔍 Token Explorer",
        "💡 Empirical Insights",
        "⚖️ Section & Comparative",
        "📖 Methodology & About",
    ]

    page_map = {
        "🏠 Home / Overview": "Home",
        "📥 Text Input & Ingestion": "Input",
        "📊 Analysis Dashboard": "Dashboard",
        "🔍 Token Explorer": "Explorer",
        "💡 Empirical Insights": "Insights",
        "⚖️ Section & Comparative": "Comparative",
        "📖 Methodology & About": "Methodology",
    }
    reverse_map = {v: k for k, v in page_map.items()}

    current_selection = reverse_map.get(
        st.session_state["current_page"], page_options[0]
    )

    selected_nav = st.radio(
        "Navigation",
        options=page_options,
        index=page_options.index(current_selection),
        label_visibility="collapsed",
    )
    st.session_state["current_page"] = page_map[selected_nav]

    st.markdown("---")

    # Workspace Status Widget
    st.markdown("##### 📌 Workspace Status")
    res = st.session_state.get("analysis_result")
    src_label = st.session_state.get("text_source_label", "None")

    if res is not None:
        st.markdown(f"**Corpus:** *{src_label}*")
        st.caption(
            f"**{res.stats.get('total_tokens', 0):,}** tokens &bull; "
            f"**{res.stats.get('unique_tokens', 0):,}** unique &bull; "
            f"TTR **{res.stats.get('type_token_ratio', 0.0):.3f}**"
        )
    else:
        st.caption("No text currently analyzed.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background-color: #F1ECE1; border-radius: 6px; padding: 0.8rem; font-size: 0.75rem; color: #64748B; line-height: 1.4;">
            <b>🔒 100% Offline Execution</b><br>
            All Sanskrit tokenisation and frequency analytics run locally. No text is sent to cloud APIs.
        </div>
        """,
        unsafe_allow_html=True,
    )


# Page Routing
page = st.session_state.get("current_page", "Home")

if page == "Home":
    render_home_page()
elif page == "Input":
    render_input_page()
elif page == "Dashboard":
    render_dashboard()
elif page == "Explorer":
    render_token_explorer()
elif page == "Insights":
    render_insights()
elif page == "Comparative":
    render_comparative_page()
elif page == "Methodology":
    render_methodology_page()
else:
    render_home_page()

