import re
from typing import List, Tuple

def split_into_chapters(text: str) -> List[Tuple[str, str]]:
    """
    Splits a book's full text into chapters based on common header patterns.

    Returns:
        A list of tuples: (chapter_title, chapter_content)
    """
    chapters = []
    pattern = r"(Chapter\s+\d+[\s\S]*?)(?=Chapter\s+\d+|$)"

    matches = re.finditer(pattern, text, flags=re.IGNORECASE)

    for match in matches:
        chunk = match.group(1).strip()
        lines = chunk.splitlines()
        title = lines[0].strip()
        content = "\n".join(lines[1:]).strip()
        chapters.append((title, content))

    return chapters
