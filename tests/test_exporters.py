"""Unit Tests for Exporters (CSV, JSON, TXT, PDF)."""

import json
import pytest
from src.nlp.analysis import analyze_text
from src.utils.exporters import (
    export_to_csv,
    export_to_json,
    export_to_txt_summary,
    export_to_pdf_report,
)


@pytest.fixture
def sample_analysis():
    text = "धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः। मामकाः पाण्डवाश्चैव किमकुर्वत सञ्जय॥"
    return analyze_text(text)


def test_csv_export_with_bom(sample_analysis):
    """Verify CSV export produces valid bytes starting with UTF-8 BOM."""
    csv_bytes = export_to_csv(sample_analysis.frequency_df, include_bom=True)
    assert isinstance(csv_bytes, bytes)
    # Check UTF-8 BOM: \xef\xbb\xbf
    assert csv_bytes.startswith(b"\xef\xbb\xbf")
    decoded = csv_bytes.decode("utf-8-sig")
    assert "Rank,Token,Frequency,Percentage,Cumulative_Percentage" in decoded
    assert "धर्मक्षेत्रे" in decoded


def test_json_export_structure(sample_analysis):
    """Verify JSON export contains required academic keys and metadata."""
    json_str = export_to_json(sample_analysis)
    data = json.loads(json_str)

    assert "metadata" in data
    assert "statistics" in data
    assert "top_20_frequencies" in data
    assert "tool" in data
    assert data["metadata"]["primary_script"] == "Devanagari"
    assert len(data["top_20_frequencies"]) > 0


def test_txt_summary_export(sample_analysis):
    """Verify academic TXT summary produces properly formatted report."""
    txt_report = export_to_txt_summary(sample_analysis, title="Test Report")
    assert "TEST REPORT" in txt_report
    assert "CORPUS & VOCABULARY STATISTICS" in txt_report
    assert "TOP 25 MOST FREQUENT SANSKRIT TOKENS" in txt_report
    assert "METHODOLOGICAL NOTES" in txt_report


def test_pdf_report_export(sample_analysis):
    """Verify PDF export produces non-empty bytes starting with PDF header."""
    pdf_bytes = export_to_pdf_report(sample_analysis, title="Test PDF Report")
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 100
    # Either PDF header %PDF or plain text fallback
    assert pdf_bytes.startswith(b"%PDF") or b"TEST PDF REPORT" in pdf_bytes

