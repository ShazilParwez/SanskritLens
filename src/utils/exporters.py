"""Export and Report Generation Module for SanskritLens.

Supports CSV (with UTF-8 BOM for Windows Excel compatibility),
structured JSON, plain text summary, and PDF report generation.
"""

from __future__ import annotations
import io
import json
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd


def export_to_csv(freq_df: pd.DataFrame, include_bom: bool = True) -> bytes:
    """Export token frequency table to CSV bytes with UTF-8 encoding.

    When include_bom is True, uses utf-8-sig so Windows Excel opens Devanagari
    characters correctly without font corruption.
    """
    encoding = "utf-8-sig" if include_bom else "utf-8"
    csv_str = freq_df.to_csv(index=False)
    return csv_str.encode(encoding)


def export_to_json(analysis_result: Any) -> str:
    """Export full analysis result, configuration, and vocabulary to formatted JSON."""
    data = analysis_result.to_dict()
    data["exported_at"] = datetime.now().isoformat()
    data["tool"] = "SanskritLens: Sanskrit Text Tokenisation & Word-Frequency Platform"
    data["methodology_version"] = "1.0.0 (Indian Knowledge Systems Edition)"
    return json.dumps(data, ensure_ascii=False, indent=2)


def export_to_txt_summary(analysis_result: Any, title: str = "SanskritLens Analysis Report") -> str:
    """Generate a clean, publication-grade academic text summary report."""
    stats = analysis_result.stats
    script_info = analysis_result.script_info
    freq_df = analysis_result.frequency_df
    opts = analysis_result.options
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "=" * 76,
        f"  {title.upper()}",
        "  Sanskrit Text Tokenisation and Word-Frequency Analysis Platform",
        "=" * 76,
        f"Generated At          : {now_str}",
        f"Primary Script        : {script_info.get('primary_script', 'Unknown')}",
        f"Tokenisation Mode     : {opts.get('mode', 'standard').capitalize()}",
        f"Punctuation Removed   : {opts.get('remove_punctuation', True)}",
        f"Numerals Excluded     : {opts.get('exclude_numerals', True)}",
        f"Stopword Filter Active: {opts.get('filter_stopwords', False)}",
        "-" * 76,
        "1. CORPUS & VOCABULARY STATISTICS",
        "-" * 76,
        f"Total Characters (raw)        : {stats.get('total_characters', 0):,}",
        f"Characters (no whitespace)    : {stats.get('chars_no_whitespace', 0):,}",
        f"Whitespace Characters         : {stats.get('total_whitespace', 0):,}",
        f"Punctuation Marks             : {stats.get('punctuation_count', 0):,}",
        f"Total Verse/Sentence Segments : {stats.get('total_segments', 0):,}",
        f"Total Orthographic Tokens     : {stats.get('total_tokens', 0):,}",
        f"Unique Orthographic Tokens    : {stats.get('unique_tokens', 0):,}",
        f"Type-Token Ratio (TTR)        : {stats.get('type_token_ratio', 0.0):.4f}",
        f"Average Token Length (CPs)    : {stats.get('average_token_length', 0.0):.2f} Unicode code points",
        f"Median Token Length (CPs)     : {stats.get('median_token_length', 0.0):.2f}",
        f"Min / Max Token Length (CPs)  : {stats.get('min_token_length', 0)} / {stats.get('max_token_length', 0)}",
        f"Hapax Legomena (Freq = 1)     : {stats.get('hapax_count', 0):,} ({stats.get('hapax_percentage', 0.0):.2f}% of vocabulary)",
        f"Dis Legomena (Freq = 2)       : {stats.get('dis_count', 0):,} ({stats.get('dis_percentage', 0.0):.2f}% of vocabulary)",
        f"Average Tokens / Segment      : {stats.get('avg_tokens_per_segment', 0.0):.2f}",
        "-" * 76,
        "2. TOP 25 MOST FREQUENT SANSKRIT TOKENS",
        "-" * 76,
        f"{'Rank':<6}{'Sanskrit Token':<28}{'Frequency':<12}{'Percentage':<14}{'Cumulative %':<14}",
        "-" * 76,
    ]

    top_tokens = freq_df.head(25)
    for _, row in top_tokens.iterrows():
        r = int(row["Rank"])
        w = str(row["Token"])
        f = int(row["Frequency"])
        p = f"{float(row['Percentage']):.2f}%"
        c = f"{float(row['Cumulative_Percentage']):.2f}%"
        lines.append(f"{r:<6}{w:<28}{f:<12}{p:<14}{c:<14}")

    lines.extend([
        "-" * 76,
        "3. METHODOLOGICAL NOTES & ACADEMIC LIMITATIONS",
        "-" * 76,
        "• Orthographic Tokenisation: Tokens represent surface orthographic units as",
        "  written in Devanagari script. Sandhi (euphonic combination) and Samasa",
        "  (nominal compounds) are preserved as written and are not mechanically",
        "  decomposed without morphological verification.",
        "• Token Length Unit: Length is measured in Unicode Code Points, not traditional",
        "  phonetic syllables (akṣaras) or morphemes.",
        "• IKS Domain Relevance: Computational word-frequency distributions assist in",
        "  lexical profiling, authorship attribution studies, and digital preservation.",
        "=" * 76,
    ])

    return "\n".join(lines)


def export_to_pdf_report(analysis_result: Any, title: str = "SanskritLens Analysis Report") -> bytes:
    """Generate a clean PDF report using ReportLab.

    If Devanagari TrueType font is available in the operating system, it is embedded;
    otherwise, fallback font is used with an explanatory note.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        # Fallback to plain text bytes wrapped if ReportLab unavailable
        return export_to_txt_summary(analysis_result, title).encode("utf-8")

    # Attempt to register Devanagari font (Windows Nirmala.ttc or Nirmala.ttf)
    font_name = "Helvetica"
    nirmala_path = Path("C:/Windows/Fonts/Nirmala.ttc")
    if nirmala_path.exists():
        try:
            pdfmetrics.registerFont(TTFont("NirmalaDevanagari", str(nirmala_path), subfontIndex=0))
            font_name = "NirmalaDevanagari"
        except Exception:
            font_name = "Helvetica"

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E1B4B"),
    )
    heading_style = ParagraphStyle(
        "DocHeading",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#B45309"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B"),
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph(title, title_style))
    story.append(
        Paragraph(
            "<b>Platform:</b> SanskritLens &nbsp;|&nbsp; <b>Domain:</b> Indian Knowledge Systems (IKS) &nbsp;|&nbsp; <b>Date:</b> "
            + datetime.now().strftime("%Y-%m-%d %H:%M"),
            body_style,
        )
    )
    story.append(Spacer(1, 12))

    # KPI Statistics Table
    stats = analysis_result.stats
    kpi_data = [
        ["Metric", "Value", "Metric", "Value"],
        ["Total Tokens", f"{stats.get('total_tokens', 0):,}", "Unique Tokens", f"{stats.get('unique_tokens', 0):,}"],
        ["Type-Token Ratio (TTR)", f"{stats.get('type_token_ratio', 0.0):.4f}", "Avg Token Length", f"{stats.get('average_token_length', 0.0):.2f} CPs"],
        ["Hapax Legomena", f"{stats.get('hapax_count', 0):,} ({stats.get('hapax_percentage', 0.0):.1f}%)", "Dis Legomena", f"{stats.get('dis_count', 0):,} ({stats.get('dis_percentage', 0.0):.1f}%)"],
        ["Sentence/Verse Segments", f"{stats.get('total_segments', 0):,}", "Punctuation Count", f"{stats.get('punctuation_count', 0):,}"],
    ]
    t = Table(kpi_data, colWidths=[130, 130, 130, 130])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E1B4B")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FAF8F5")),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                ("ALIGN", (3, 1), (3, -1), "RIGHT"),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 14))

    # Top 20 Frequencies Table
    story.append(Paragraph("Top 20 Most Frequent Sanskrit Tokens", heading_style))
    freq_df = analysis_result.frequency_df.head(20)

    table_data = [["Rank", "Sanskrit Token", "Frequency", "Share (%)", "Cumulative (%)"]]
    for _, r in freq_df.iterrows():
        table_data.append(
            [
                str(int(r["Rank"])),
                str(r["Token"]),
                str(int(r["Frequency"])),
                f"{float(r['Percentage']):.2f}%",
                f"{float(r['Cumulative_Percentage']):.2f}%",
            ]
        )

    freq_table = Table(table_data, colWidths=[50, 190, 80, 90, 110])
    freq_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#B45309")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("ALIGN", (2, 0), (-1, -1), "RIGHT"),
            ]
        )
    )
    story.append(freq_table)
    story.append(Spacer(1, 14))

    # Methodology Disclaimer
    story.append(Paragraph("Academic Methodology & Known Limitations", heading_style))
    disclaimer_text = (
        "<b>Orthographic Tokenisation Note:</b> In this analysis, tokens correspond to surface orthographic units "
        "written in Devanagari. Sandhi (euphonic changes) and Samasa (nominal compounds) are preserved as written. "
        "Token lengths are reported in Unicode Code Points rather than phonetic syllables (akṣaras). "
        "This tool serves as an analytical support framework for Indian Knowledge Systems (IKS) computational linguistics."
    )
    story.append(Paragraph(disclaimer_text, body_style))

    try:
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    except Exception:
        # Fallback to plain text bytes
        return export_to_txt_summary(analysis_result, title).encode("utf-8")

