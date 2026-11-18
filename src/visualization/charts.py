"""Interactive and Statistical Data Visualisation Module for SanskritLens.

Produces scholarly, publication-quality Plotly interactive charts and Matplotlib figures
for Sanskrit text tokenisation, frequency distributions, vocabulary composition,
and Zipf-like rank-frequency analysis.
"""

from __future__ import annotations
import math
from pathlib import Path
from typing import Any
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Register bundled Noto Sans Devanagari font with Matplotlib if available
_bundled_font_path = Path(__file__).resolve().parent.parent.parent / "data" / "fonts" / "NotoSansDevanagari-Regular.ttf"
if _bundled_font_path.is_file():
    try:
        fm.fontManager.addfont(str(_bundled_font_path))
    except Exception:
        pass

# Scholarly Palette Definition
COLOR_PRIMARY = "#B45309"      # Warm antique saffron
COLOR_SECONDARY = "#1E1B4B"    # Deep scholarly indigo
COLOR_ACCENT = "#D97706"       # Golden ochre
COLOR_TEAL = "#0F766E"         # Vedic sage teal
COLOR_MUTED = "#64748B"        # Slate grey
COLOR_BG_CARD = "#FFFFFF"      # Crisp card background
COLOR_BG_LIGHT = "#FAF8F5"     # Warm parchment
FONT_FAMILY = "Noto Sans Devanagari, 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"


def _empty_figure(message: str = "No data available to display") -> go.Figure:
    """Create a graceful empty state figure for Plotly."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color=COLOR_MUTED, family=FONT_FAMILY),
    )
    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
    )
    return fig


def plot_top_frequencies(freq_df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Chart 1: Top N Most Frequent Tokens (Horizontal Bar Chart).

    Displays Sanskrit orthographic tokens with clear frequencies and percentages.
    Sorted with the highest frequency at the top.
    """
    if freq_df.empty:
        return _empty_figure("No word frequency data available.")

    subset = freq_df.head(top_n).copy()
    # Sort ascending for horizontal bar chart so highest appears at top
    subset = subset.sort_values(by="Frequency", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=subset["Frequency"],
            y=subset["Token"],
            orientation="h",
            marker=dict(
                color=subset["Frequency"],
                colorscale=[[0.0, "#FDE68A"], [0.5, "#D97706"], [1.0, "#9A3412"]],
                line=dict(color="#78350F", width=1),
            ),
            text=subset["Frequency"].apply(lambda v: f" {v}"),
            textposition="outside",
            hovertemplate=(
                "<b>Rank:</b> %{customdata[0]}<br>"
                "<b>Token:</b> %{y}<br>"
                "<b>Frequency:</b> %{x:,}<br>"
                "<b>Percentage:</b> %{customdata[1]:.2f}%<extra></extra>"
            ),
            customdata=subset[["Rank", "Percentage"]].values,
        )
    )

    fig.update_layout(
        title=dict(
            text=f"Top {len(subset)} Most Frequent Sanskrit Tokens",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        xaxis=dict(
            title="Frequency (Occurrences)",
            gridcolor="#E2E8F0",
            zerolinecolor="#CBD5E1",
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=13, family=FONT_FAMILY),
            automargin=True,
        ),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="rgba(0,0,0,0)",
        height=max(380, 24 * len(subset)),
        margin=dict(l=10, r=40, t=50, b=40),
    )
    return fig


def plot_frequency_distribution(freq_df: pd.DataFrame) -> go.Figure:
    """Chart 2: Word Frequency Distribution (Histogram of Occurrence Frequencies).

    Shows how many unique words occur at various frequency thresholds.
    """
    if freq_df.empty:
        return _empty_figure("No token frequency distribution available.")

    # Frequency binning: 1, 2, 3, 4, 5-9, 10-19, 20+
    freqs = freq_df["Frequency"].tolist()

    bins = {
        "1 (Hapax)": 0,
        "2 (Dis)": 0,
        "3": 0,
        "4": 0,
        "5 - 9": 0,
        "10 - 19": 0,
        "20+": 0,
    }

    for f in freqs:
        if f == 1:
            bins["1 (Hapax)"] += 1
        elif f == 2:
            bins["2 (Dis)"] += 1
        elif f == 3:
            bins["3"] += 1
        elif f == 4:
            bins["4"] += 1
        elif 5 <= f <= 9:
            bins["5 - 9"] += 1
        elif 10 <= f <= 19:
            bins["10 - 19"] += 1
        else:
            bins["20+"] += 1

    # Filter out empty tail bins if small dataset
    active_bins = {k: v for k, v in bins.items() if v > 0 or k in ("1 (Hapax)", "2 (Dis)", "3")}

    fig = go.Figure(
        go.Bar(
            x=list(active_bins.keys()),
            y=list(active_bins.values()),
            marker=dict(
                color=COLOR_TEAL,
                line=dict(color="#042F2E", width=1),
            ),
            text=list(active_bins.values()),
            textposition="outside",
            hovertemplate="<b>Frequency Range:</b> %{x}<br><b>Unique Words:</b> %{y}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="Token Frequency Occurrence Spectrum",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        xaxis=dict(title="Occurrence Count", gridcolor="#E2E8F0"),
        yaxis=dict(title="Number of Unique Words", gridcolor="#E2E8F0"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=30, r=30, t=50, b=40),
    )
    return fig


def plot_word_length_distribution(length_df: pd.DataFrame) -> go.Figure:
    """Chart 3: Word Length Distribution.

    Displays distribution of token lengths (counted in Unicode code points).
    """
    if length_df.empty:
        return _empty_figure("No word length data available.")

    fig = go.Figure(
        go.Bar(
            x=length_df["Length"],
            y=length_df["Token_Count"],
            marker=dict(
                color=COLOR_ACCENT,
                line=dict(color="#78350F", width=1),
            ),
            text=length_df["Token_Count"],
            textposition="outside",
            hovertemplate=(
                "<b>Length:</b> %{x} Unicode code points<br>"
                "<b>Token Count:</b> %{y}<br>"
                "<b>Percentage:</b> %{customdata[0]:.2f}%<br>"
                "<b>Examples:</b> %{customdata[1]}<extra></extra>"
            ),
            customdata=length_df[["Percentage", "Examples"]].values,
        )
    )

    fig.update_layout(
        title=dict(
            text="Token Length Distribution (Unicode Code Points)",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        xaxis=dict(title="Token Length (Unicode Code Points)", dtick=1, gridcolor="#E2E8F0"),
        yaxis=dict(title="Total Tokens", gridcolor="#E2E8F0"),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="rgba(0,0,0,0)",
        height=380,
        margin=dict(l=30, r=30, t=50, b=40),
    )
    return fig


def plot_vocabulary_composition(total_tokens: int, unique_tokens: int) -> go.Figure:
    """Chart 4: Vocabulary Composition (Donut Chart).

    Visualizes unique tokens versus repeated token occurrences.
    """
    if total_tokens == 0:
        return _empty_figure("No tokens available for composition.")

    repeated_tokens = max(0, total_tokens - unique_tokens)

    labels = ["Unique Tokens (Vocabulary Types)", "Repeated Token Occurrences"]
    values = [unique_tokens, repeated_tokens]
    colors = [COLOR_PRIMARY, "#CBD5E1"]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="Lexical Diversity: Type vs Repetition",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        paper_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=50, b=40),
    )
    return fig


def plot_hapax_breakdown(vocab_info: dict[str, Any]) -> go.Figure:
    """Chart 5: Hapax Legomena Breakdown.

    Shows proportion of Hapax Legomena (freq=1), Dis Legomena (freq=2),
    and Multi-occurrence tokens across unique vocabulary.
    """
    unique_count = vocab_info.get("unique_count", 0)
    if unique_count == 0:
        return _empty_figure("No vocabulary data available.")

    hapax = vocab_info.get("hapax_count", 0)
    dis = vocab_info.get("dis_count", 0)
    multi = max(0, unique_count - hapax - dis)

    labels = [
        "Hapax Legomena (Freq = 1)",
        "Dis Legomena (Freq = 2)",
        "Frequent Lexemes (Freq ≥ 3)",
    ]
    values = [hapax, dis, multi]
    colors = ["#D97706", "#0F766E", "#1E1B4B"]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=colors, line=dict(color="#FFFFFF", width=2)),
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Words: %{value}<br>Share of Vocabulary: %{percent}<extra></extra>",
        )
    )

    fig.update_layout(
        title=dict(
            text="Vocabulary Stratification (Hapax & Dis Legomena)",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=50, b=30),
    )
    return fig


def plot_pareto_analysis(freq_df: pd.DataFrame, top_n: int = 30) -> go.Figure:
    """Chart 6: Cumulative Frequency / Pareto Analysis.

    Dual-axis chart illustrating token frequency bars alongside cumulative percentage curve.
    Highlights lexical concentration (e.g., Pareto 80/20 threshold).
    """
    if freq_df.empty:
        return _empty_figure("No frequency data for Pareto analysis.")

    subset = freq_df.head(top_n).copy()

    fig = go.Figure()

    # Individual Token Frequency Bar
    fig.add_trace(
        go.Bar(
            x=subset["Rank"],
            y=subset["Frequency"],
            name="Token Frequency",
            marker=dict(color="#CBD5E1"),
            hovertemplate="<b>Rank %{x}:</b> %{customdata} (%{y} occurrences)<extra></extra>",
            customdata=subset["Token"],
        )
    )

    # Cumulative Percentage Line
    fig.add_trace(
        go.Scatter(
            x=subset["Rank"],
            y=subset["Cumulative_Percentage"],
            name="Cumulative %",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color=COLOR_PRIMARY, width=2.5),
            marker=dict(size=5, color="#78350F"),
            hovertemplate="<b>Cumulative:</b> %{y:.2f}%<extra></extra>",
        )
    )

    # 80% reference horizontal line
    fig.add_hline(
        y=80,
        yref="y2",
        line_dash="dot",
        line_color="#EF4444",
        annotation_text="80% Lexical Mass",
        annotation_position="top right",
        annotation_font=dict(size=11, color="#EF4444"),
    )

    fig.update_layout(
        title=dict(
            text=f"Pareto Lexical Concentration (Top {len(subset)} Tokens)",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        xaxis=dict(title="Token Rank (Ordered by Frequency)", gridcolor="#F1F5F9"),
        yaxis=dict(title="Individual Token Frequency", gridcolor="#E2E8F0"),
        yaxis2=dict(
            title="Cumulative Percentage (%)",
            overlaying="y",
            side="right",
            range=[0, 105],
            showgrid=False,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=40, r=40, t=60, b=40),
    )
    return fig


def plot_frequency_rank_curve(freq_df: pd.DataFrame) -> go.Figure:
    """Chart 7: Frequency vs. Rank Analysis (Zipf-like distribution exploration).

    Plots token rank against frequency on log-log and linear scales.
    Conservative presentation: explores empirical distribution without unsubstantiated claims.
    """
    if freq_df.empty:
        return _empty_figure("No data available for rank-frequency analysis.")

    df = freq_df.copy()

    fig = go.Figure()

    # Empirical data curve
    fig.add_trace(
        go.Scatter(
            x=df["Rank"],
            y=df["Frequency"],
            mode="lines+markers",
            name="Empirical Word Frequency",
            line=dict(color=COLOR_SECONDARY, width=2),
            marker=dict(size=4, color=COLOR_PRIMARY),
            hovertemplate="<b>Rank:</b> %{x}<br><b>Token:</b> %{customdata}<br><b>Frequency:</b> %{y}<extra></extra>",
            customdata=df["Token"],
        )
    )

    # Theoretical Zipf reference curve f(r) = f(1) / r
    if len(df) > 1 and df["Frequency"].iloc[0] > 0:
        f1 = df["Frequency"].iloc[0]
        zipf_y = [round(f1 / r, 2) for r in df["Rank"]]
        fig.add_trace(
            go.Scatter(
                x=df["Rank"],
                y=zipf_y,
                mode="lines",
                name="Zipf Reference Slope [ f(1)/r ]",
                line=dict(color="#94A3B8", width=1.5, dash="dash"),
                hovertemplate="<b>Theoretical Zipf:</b> %{y:.2f}<extra></extra>",
            )
        )

    fig.update_layout(
        title=dict(
            text="Word Frequency vs. Rank Curve (Zipf Analysis Exploration)",
            font=dict(size=16, family=FONT_FAMILY, color=COLOR_SECONDARY),
        ),
        xaxis=dict(
            title="Rank (Logarithmic Scale)",
            type="log",
            gridcolor="#E2E8F0",
        ),
        yaxis=dict(
            title="Frequency (Logarithmic Scale)",
            type="log",
            gridcolor="#E2E8F0",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=40, r=30, t=60, b=40),
    )
    return fig


def generate_static_frequency_plot(freq_df: pd.DataFrame, top_n: int = 15) -> plt.Figure:
    """Generate static Matplotlib bar chart for downloadable figure or PDF inclusion."""
    # Ensure Devanagari font is prioritized on Windows/Linux environments
    plt.rcParams["font.sans-serif"] = [
        "Nirmala UI",
        "Nirmala Text",
        "Mangal",
        "Noto Sans Devanagari",
        "Segoe UI",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False

    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
    if freq_df.empty:
        ax.text(0.5, 0.5, "No data available", ha="center", va="center")
        return fig

    subset = freq_df.head(top_n).sort_values(by="Frequency", ascending=True)
    y_pos = range(len(subset))

    bars = ax.barh(y_pos, subset["Frequency"], color="#B45309", edgecolor="#78350F", height=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(subset["Token"])
    ax.set_xlabel("Frequency (Occurrences)")
    ax.set_title(f"Top {len(subset)} Most Frequent Sanskrit Tokens", color="#1E1B4B", fontsize=12, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.1, bar.get_y() + bar.get_height() / 2, f"{int(w)}", va="center", ha="left", fontsize=9)

    plt.tight_layout()
    return fig

