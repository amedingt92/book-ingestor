import sys
import os

# Dynamically add the src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import structure # type: ignore

def test_split_into_chapters_detects_multiple():
    sample_text = (
        "Chapter 1\nCall me Ishmael...\n"
        "Chapter 2\nSome years ago...\n"
        "Chapter 3\nWhenever I find myself..."
    )

    chapters = structure.split_into_chapters(sample_text)

    assert len(chapters) == 3
    assert chapters[0][0].lower().startswith("chapter 1")
    assert "ishmael" in chapters[0][1].lower()
    assert "some years ago" in chapters[1][1].lower()
