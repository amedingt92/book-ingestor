"""Handles loading and basic cleaning of raw book text from Project Gutenberg or similar sources."""

def load_book(filepath: str) -> str:
    """Read a plain text book and return its full contents as a string."""
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def clean_gutenberg_text(text: str) -> str:
    lines = text.splitlines()
    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if "*** START OF THIS PROJECT GUTENBERG EBOOK" in line:
            start_idx = i + 1  # Skip the line itself
        elif "*** END OF THIS PROJECT GUTENBERG EBOOK" in line:
            end_idx = i  # Stop before this line
            break

    body_lines = lines[start_idx:end_idx]
    cleaned = "\n".join(body_lines).strip()
    return cleaned

