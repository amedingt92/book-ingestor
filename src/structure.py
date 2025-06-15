import re
from typing import List, Tuple


def clean_gutenberg_text(text: str) -> str:
    """Removes Project Gutenberg license boilerplate and returns clean book content."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = text.find(start_marker)
    if start_idx != -1:
        text = text[start_idx + len(start_marker):]

    end_idx = text.find(end_marker)
    if end_idx != -1:
        text = text[:end_idx]

    return text.strip()


def roman_to_int(roman: str) -> int:
    roman = roman.upper()
    roman_numerals = {
        'M': 1000, 'CM': 900, 'D': 500, 'CD': 400,
        'C': 100,  'XC': 90,  'L': 50,  'XL': 40,
        'X': 10,   'IX': 9,   'V': 5,   'IV': 4, 'I': 1
    }

    i = 0
    result = 0
    while i < len(roman):
        if i + 1 < len(roman) and roman[i:i+2] in roman_numerals:
            result += roman_numerals[roman[i:i+2]]
            i += 2
        else:
            result += roman_numerals.get(roman[i], 0)
            i += 1
    return result


def split_by_letter_number(text: str) -> list[dict]:
    """Splits the text into 'Letter <N>' epistolary chapters, skipping TOC."""

    # Match 'CONTENTS' heading (assumes all caps on its own line)
    toc_match = re.search(r'^\s*CONTENTS\s*$', text, re.MULTILINE)

    # Match all 'Letter <number>' lines
    pattern = re.compile(r'^\s*(Letter\s+\d+)\s*$', re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))

    # If TOC and at least 2 'Letter' headers are found
    if toc_match and len(matches) > 1:
        # Find the first 'Letter 1' that comes AFTER the TOC
        for match in matches:
            if match.start() > toc_match.end() and match.group(1).strip().lower() == "letter 1":
                text = text[match.start():]
                break

    # Recompute matches from updated text
    matches = list(pattern.finditer(text))
    chapters = []

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = match.group(1).strip()
        content = text[start:end].strip()
        chapters.append({
            "title": title,
            "content": content
        })

    return chapters


def detect_book_structure(text: str) -> str:
    # Detect letter-number format first (more specific)
    if re.search(r'^\s*Letter\s+\d+\s*$', text, re.IGNORECASE | re.MULTILINE):
        return "letter_number"
    
    # Then multi-tier like PART I
    elif re.search(r'^\s*PART\s+[IVXLC]+\s*$', text, re.IGNORECASE | re.MULTILINE):
        return "multi_tier"
    
    # Then numbered chapters like "Chapter 1"
    elif re.search(r'^\s*Chapter\s+\d+', text, re.IGNORECASE | re.MULTILINE):
        return "chapter_number"
    
    # Then fallback to roman numeral format
    elif re.search(r'^\s*[IVXLC]+\.\s+', text, re.MULTILINE):
        return "roman_numeral"
    
    else:
        return "unknown"


def split_major_sections(text: str) -> list[Tuple[str, str]]:
    pattern = re.compile(r'^\s*(PART\s+[IVXLC]+)\s*$', re.IGNORECASE | re.MULTILINE)
    matches = list(pattern.finditer(text))
    parts = []

    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(text)
        part_title = match.group(1).strip()
        part_content = text[start:end].strip()
        parts.append((part_title, part_content))

    return parts


def split_minor_sections(section_text: str) -> list[dict]:
    chapter_pattern = re.compile(r'^\s*Chapter\s+(\d+)\.?\s+(.*)', re.IGNORECASE | re.MULTILINE)
    lines = section_text.splitlines()
    chapters = []
    current_title = None
    current_lines = []

    for line in lines:
        match = chapter_pattern.match(line)
        if match:
            if current_title:
                chapters.append({
                    "title": current_title,
                    "content": "\n".join(current_lines).strip()
                })
            current_title = match.group(2).strip()
            current_lines = []
        elif current_title:
            current_lines.append(line)

    if current_title and current_lines:
        chapters.append({
            "title": current_title,
            "content": "\n".join(current_lines).strip()
        })

    return chapters


def split_by_chapter_format(text: str, format_type: str) -> list[dict]:
    chapters = []
    current_title = None
    current_lines = []

    if format_type == "roman_numeral":
        pattern = re.compile(r'^\s*([IVXLC]+)\.\s+(.*)', re.IGNORECASE)
    elif format_type == "chapter_number":
        pattern = re.compile(r'^\s*Chapter\s+\d+[:.]?\s+(.*)', re.IGNORECASE)
    else:
        return []

    lines = text.splitlines()

    for line in lines:
        match = pattern.match(line)
        if match:
            title = match.group(2).strip() if format_type == "roman_numeral" else match.group(1).strip()

            # Avoid TOC duplicates
            if any(ch["title"].lower() == title.lower() for ch in chapters):
                continue

            if current_title:
                chapters.append({
                    "title": current_title,
                    "content": "\n".join(current_lines).strip()
                })

            current_title = title
            current_lines = []
        elif current_title:
            current_lines.append(line)

    if current_title and current_lines:
        chapters.append({
            "title": current_title,
            "content": "\n".join(current_lines).strip()
        })

    return chapters


def split_epistolary_letters(text: str) -> list[dict]:
    """Splits 'Letter N' sections (e.g., Frankenstein) while skipping TOC entries."""

    # Skip content before the actual body of the book (e.g., after 'CONTENTS' marker)
    toc_match = re.search(r'^\s*CONTENTS\s*$', text, re.MULTILINE)
    if toc_match:
        text = text[toc_match.end():]

    # Now match actual letter sections in the book
    pattern = re.compile(r'^\s*Letter\s+(\d+)\s*$', re.MULTILINE)
    matches = list(pattern.finditer(text))

    chapters = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = f"Letter {match.group(1)}"
        content = text[start:end].strip()

        chapters.append({
            "title": title,
            "content": content
        })

    return chapters


def split_into_chapters(text: str) -> list[dict]:
    structure = detect_book_structure(text)

    if structure == "multi_tier":
        sections = split_major_sections(text)
        all_chapters = []
        for part_title, part_text in sections:
            chapters = split_minor_sections(part_text)
            for chap in chapters:
                chap["part"] = part_title
                all_chapters.append(chap)
        return all_chapters

    elif structure in {"roman_numeral", "chapter_number"}:
        return split_by_chapter_format(text, structure)

    elif structure == "letter_number":
        return split_by_letter_number(text)

    else:
        return []

