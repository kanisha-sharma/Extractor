"""
Common heuristic functions used by the Stage 3 intelligence package.
"""

from __future__ import annotations

import re
from typing import Iterable

from coastalExtractor.models.semantic_models import Heading


class Heuristics:
    """
    Collection of reusable heuristic methods.
    """

    TABLE_PATTERN = re.compile(
        r"^table\s+\d+",
        re.IGNORECASE,
    )

    FIGURE_PATTERN = re.compile(
        r"^(figure|fig\.?)\s+\d+",
        re.IGNORECASE,
    )

    ANNEX_PATTERN = re.compile(
        r"^(annex|appendix)\b",
        re.IGNORECASE,
    )

    CHAPTER_PATTERN = re.compile(
        r"^chapter\b",
        re.IGNORECASE,
    )

    SECTION_PATTERN = re.compile(
        r"^\d+(\.\d+)*"
    )

    KEY_VALUE_PATTERN = re.compile(
        r"^[A-Za-z][A-Za-z0-9\s/_\-]{1,60}\s*[:=-]\s*.+$"
    )

    BULLET_PATTERN = re.compile(
        r"^(\u2022|\*|\-|●|▪|■)\s+"
    )

    NUMBERED_PATTERN = re.compile(
        r"^(\d+[\.\)]|[A-Za-z][\.\)]|[ivxlcdmIVXLCDM]+[\.\)])\s+"
    )

    @staticmethod
    def clean(text: str) -> str:

        return " ".join(text.strip().split())

    @classmethod
    def is_table_caption(cls, text: str) -> bool:

        return bool(cls.TABLE_PATTERN.match(cls.clean(text)))

    @classmethod
    def is_figure_caption(cls, text: str) -> bool:

        return bool(cls.FIGURE_PATTERN.match(cls.clean(text)))

    @classmethod
    def is_caption(cls, text: str) -> bool:

        return (
            cls.is_table_caption(text)
            or cls.is_figure_caption(text)
        )

    @classmethod
    def is_annex(cls, text: str) -> bool:

        return bool(cls.ANNEX_PATTERN.match(cls.clean(text)))

    @classmethod
    def is_chapter(cls, text: str) -> bool:

        return bool(cls.CHAPTER_PATTERN.match(cls.clean(text)))

    @classmethod
    def is_section_number(cls, text: str) -> bool:

        return bool(cls.SECTION_PATTERN.match(cls.clean(text)))

    @classmethod
    def is_key_value(cls, text: str) -> bool:

        return bool(cls.KEY_VALUE_PATTERN.match(text.strip()))

    @classmethod
    def is_list_item(cls, text: str) -> bool:

        text = text.strip()

        return (
            bool(cls.BULLET_PATTERN.match(text))
            or bool(cls.NUMBERED_PATTERN.match(text))
        )

    @staticmethod
    def heading_score(heading: Heading) -> float:
        """
        Computes a normalized heading score.
        """

        score = heading.confidence

        if getattr(heading, "is_bold", False):
            score += 0.10

        if getattr(heading, "is_centered", False):
            score += 0.10

        if getattr(heading, "font_size", 0) >= 16:
            score += 0.10

        return min(score, 1.0)

    @staticmethod
    def normalize_confidence(value: float) -> float:

        if value < 0:
            return 0.0

        if value > 1:
            return 1.0

        return value

    @staticmethod
    def average(values: Iterable[float]) -> float:

        values = list(values)

        if not values:
            return 0.0

        return sum(values) / len(values)

    @staticmethod
    def is_short_line(text: str) -> bool:

        return len(text.split()) <= 10

    @staticmethod
    def is_long_paragraph(text: str) -> bool:

        return len(text.split()) >= 30

    @staticmethod
    def confidence_from_matches(matches: int, total: int) -> float:

        if total <= 0:
            return 0.0

        return min(matches / total, 1.0)