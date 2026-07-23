"""
Text utility functions used throughout the document extraction pipeline.
"""

from __future__ import annotations

import re
import unicodedata
from typing import List


# ==========================================================
# CLEANING
# ==========================================================

def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def remove_duplicate_spaces(text: str) -> str:
    return re.sub(r" +", " ", text)


def clean_text(text: str) -> str:
    text = normalize_unicode(text)
    text = text.replace("\xa0", " ")
    text = remove_duplicate_spaces(text)
    text = normalize_whitespace(text)
    return text.strip()


def remove_empty_lines(lines: List[str]) -> List[str]:
    return [line for line in lines if line.strip()]


def remove_page_numbers(lines: List[str]) -> List[str]:
    cleaned = []

    for line in lines:

        if re.fullmatch(r"\d+", line.strip()):
            continue

        if re.fullmatch(r"page\s+\d+", line.lower().strip()):
            continue

        cleaned.append(line)

    return cleaned


# ==========================================================
# TOKENIZATION
# ==========================================================

def tokenize(text: str):
    return re.findall(r"\w+", text.lower())


def word_count(text: str) -> int:
    return len(tokenize(text))


# ==========================================================
# CASE CHECKS
# ==========================================================

def is_all_caps(text: str) -> bool:

    letters = [c for c in text if c.isalpha()]

    if not letters:
        return False

    return all(c.isupper() for c in letters)


def is_title_case(text: str) -> bool:
    return text == text.title()


# ==========================================================
# NUMBERING
# ==========================================================

_ROMAN_PATTERN = re.compile(
    r"^(M{0,4}(CM|CD|D?C{0,3})"
    r"(XC|XL|L?X{0,3})"
    r"(IX|IV|V?I{0,3}))$",
    re.IGNORECASE,
)


def is_roman_numeral(text: str) -> bool:
    return bool(_ROMAN_PATTERN.fullmatch(text.strip()))


def starts_with_number(text: str) -> bool:
    return bool(
        re.match(
            r"^\d+(\.\d+)*",
            text.strip(),
        )
    )


def starts_with_letter(text: str) -> bool:
    return bool(
        re.match(
            r"^[A-Za-z]\.",
            text.strip(),
        )
    )


# ==========================================================
# BULLETS
# ==========================================================

_BULLET_PATTERN = re.compile(
    r"^(\u2022|\-|–|\*|●|▪|○|■)\s+"
)


def is_bullet(text: str) -> bool:
    return bool(_BULLET_PATTERN.match(text.strip()))


def remove_bullet(text: str) -> str:
    return _BULLET_PATTERN.sub("", text).strip()


# ==========================================================
# NUMBERED LISTS
# ==========================================================

_NUMBERED_LIST_PATTERN = re.compile(
    r"^(\d+[\.\)]|[A-Za-z][\.\)]|[ivxlcdm]+[\.\)])\s+",
    re.IGNORECASE,
)


def is_numbered_list(text: str) -> bool:
    return bool(_NUMBERED_LIST_PATTERN.match(text.strip()))


def remove_list_marker(text: str) -> str:
    return _NUMBERED_LIST_PATTERN.sub("", text).strip()


# ==========================================================
# CAPTION DETECTION
# ==========================================================

_CAPTION_PATTERN = re.compile(
    r"^(Figure|Fig\.?|Table|Image|Diagram|Chart|Annex)\s*[\dA-Za-z\-:]*",
    re.IGNORECASE,
)


def looks_like_caption(text: str) -> bool:
    return bool(_CAPTION_PATTERN.match(clean_text(text)))


# ==========================================================
# HEADING DETECTION
# ==========================================================

_HEADING_NUMBER_PATTERN = re.compile(
    r"^\d+(\.\d+)*\s+"
)


def heading_level(text: str) -> int:

    match = _HEADING_NUMBER_PATTERN.match(text.strip())

    if not match:
        return 1

    numbering = match.group().strip()

    return numbering.count(".") + 1


def looks_like_heading(text: str) -> bool:

    text = clean_text(text)

    if len(text) < 3:
        return False

    if len(text) > 150:
        return False

    if text.endswith("."):
        return False

    if is_all_caps(text):
        return True

    if starts_with_number(text):
        return True

    if is_title_case(text) and word_count(text) <= 12:
        return True

    return False


# ==========================================================
# FOOTER / HEADER DETECTION
# ==========================================================

def looks_like_page_header(text: str) -> bool:

    text = clean_text(text)

    if len(text) > 100:
        return False

    if "confidential" in text.lower():
        return True

    return False


def looks_like_page_footer(text: str) -> bool:

    text = clean_text(text)

    if re.fullmatch(r"\d+", text):
        return True

    if text.lower().startswith("page"):
        return True

    return False


# ==========================================================
# TEXT SIMILARITY
# ==========================================================

def normalized_text(text: str) -> str:

    text = clean_text(text)

    return text.lower()


def same_text(a: str, b: str) -> bool:

    return normalized_text(a) == normalized_text(b)