"""File Input, Encoding, and Sample Data Management Module for SanskritLens.

Handles safe UTF-8 decoding, UTF-8 BOM handling, file size validation,
and loading of vetted public-domain Sanskrit sample corpora.
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

# Maximum upload limit: 10 MB (safe for browser and memory)
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLES_DIR = DATA_DIR / "samples"
METADATA_FILE = DATA_DIR / "metadata" / "sample_metadata.json"


def load_sample_metadata() -> list[dict[str, Any]]:
    """Load metadata catalog for all bundled Sanskrit sample texts.

    Returns:
        List of sample text metadata dicts.
    """
    if not METADATA_FILE.exists():
        return []

    try:
        with open(METADATA_FILE, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("samples", [])
    except Exception:
        return []


def load_sample_text_by_id(sample_id: str) -> tuple[str, dict[str, Any] | None]:
    """Load raw text and metadata for a selected sample ID.

    Returns:
        Tuple of (text_content, metadata_dict)
    """
    samples = load_sample_metadata()
    for s in samples:
        if s.get("id") == sample_id:
            filename = s.get("filename")
            file_path = SAMPLES_DIR / filename
            if file_path.exists():
                with open(file_path, mode="r", encoding="utf-8") as f:
                    content = f.read()
                return content, s
            return "", s
    return "", None


def read_uploaded_file(uploaded_file: Any) -> tuple[str, str | None]:
    """Safely decode and validate an uploaded Streamlit file buffer.

    Requirements:
    - UTF-8 decoding with fallback for UTF-8-sig (BOM).
    - File size validation.
    - Informative encoding and size error reporting.

    Returns:
        Tuple of (decoded_text, error_message). If error_message is not None, reading failed.
    """
    if uploaded_file is None:
        return "", "No file was uploaded."

    # Validate file size
    size = getattr(uploaded_file, "size", None)
    if size is not None and size > MAX_FILE_SIZE_BYTES:
        mb = round(MAX_FILE_SIZE_BYTES / (1024 * 1024))
        return "", f"File exceeds the maximum permitted size limit ({mb} MB)."

    try:
        raw_bytes = uploaded_file.read()
    except Exception as e:
        return "", f"Failed to read file buffer: {e}"

    if not raw_bytes:
        return "", "The uploaded file is empty (0 bytes)."

    # Decode UTF-8 (handling BOM)
    try:
        # utf-8-sig strips BOM if present
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            # Fallback to UTF-16 in case user exported from legacy Windows notepad
            text = raw_bytes.decode("utf-16")
        except Exception:
            return (
                "",
                "Encoding Error: The uploaded file is not a valid UTF-8 text file. "
                "Please save the text with UTF-8 encoding and try again.",
            )

    if not text.strip():
        return "", "The uploaded file contains only whitespace."

    return text, None

