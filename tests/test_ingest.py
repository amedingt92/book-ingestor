import sys
import os

# Dynamically add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import ingest # type: ignore

def test_load_book(tmp_path):
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Test content.")
    assert ingest.load_book(str(test_file)) == "Test content."

def test_clean_gutenberg_text_strips_wrappers():
    mock_text = (
        "Header junk\n"
        "*** START OF THIS PROJECT GUTENBERG EBOOK MOBY DICK ***\n"
        "Call me Ishmael...\n"
        "*** END OF THIS PROJECT GUTENBERG EBOOK MOBY DICK ***\n"
        "Footer junk"
    )
    cleaned = ingest.clean_gutenberg_text(mock_text)
    assert "Call me Ishmael" in cleaned
    assert "***" not in cleaned
    assert "Header" not in cleaned
    assert "Footer" not in cleaned

def test_clean_gutenberg_text_returns_full_when_no_markers():
    raw_text = "This is a short story without any Gutenberg markers."
    cleaned = ingest.clean_gutenberg_text(raw_text)
    assert cleaned == raw_text
