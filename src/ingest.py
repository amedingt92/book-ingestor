import re

"""Handles loading and basic cleaning of raw book text from Project Gutenberg or similar sources."""

def load_book(filepath: str) -> str:
    """Read a plain text book and return its full contents as a string."""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def clean_gutenberg_text(text: str) -> str:
    """Extracts and returns the main body of the book, skipping TOC and extras."""
    # Normalize line endings
    text = text.replace("\r\n", "\n")

    # Isolate between START and END markers
    match = re.search(
        r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*(.*)\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        body = match.group(2).strip()
    else:
        print("⚠️ Warning: Could not find START/END markers. Using raw text.")
        body = text.strip()

    # Skip ETYMOLOGY, EXTRACTS, CONTENTS, etc. — go to first CHAPTER
    chapter_start_match = re.search(r"(CHAPTER\s+1[\.:]?\s+.+)", body, re.IGNORECASE)
    if chapter_start_match:
        body = body[chapter_start_match.start():]
    else:
        print("⚠️ Warning: Could not find actual Chapter 1 start.")

    return body



