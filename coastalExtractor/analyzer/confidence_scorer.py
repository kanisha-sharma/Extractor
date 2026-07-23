import re
from string import punctuation

from sqlalchemy import text

from coastalExtractor.analyzer.font_analyzer import TextSpan
from coastalExtractor.analyzer.layout_analyzer import LayoutSpan


class ConfidenceScorer:

    def __init__(self, average_font_size: float):

        self.average_font_size = average_font_size

    def score(
        self,
        font: TextSpan,
        layout: LayoutSpan
    ) -> float:

        score = 0

        text = font.text.strip()

        # -------------------------------------------------
        # Font Size
        # -------------------------------------------------

        if font.font_size >= self.average_font_size + 4:
            score += 35

        elif font.font_size >= self.average_font_size + 2:
            score += 28

        elif font.font_size >= self.average_font_size + 1:
            score += 18

        # -------------------------------------------------
        # Bold
        # -------------------------------------------------

        if font.is_bold:
            score += 15

        # -------------------------------------------------
        # Center Alignment
        # -------------------------------------------------

        if layout.is_centered:
            score += 10

        # -------------------------------------------------
        # Whitespace
        # -------------------------------------------------

        if layout.whitespace_above >= 10:
            score += 10

        if layout.whitespace_below >= 8:
            score += 5

        # -------------------------------------------------
        # Uppercase
        # -------------------------------------------------

        if text.isupper():

            if len(text.split()) <= 8:
                score += 8
            else:
                score -= 5

        if font.is_italic:
            score -= 3

        if text.endswith(":"):
            score += 5

        if font.font_size < self.average_font_size - 1:
            score -= 10

        punctuation = text.count(".") + text.count(",")

        if punctuation >= 3:
            score -= 10

        if "http://" in text or "https://" in text:
            score -= 30

        if "@" in text:
            score -= 25

        if text.isdigit():
            score -= 40
        # -------------------------------------------------
        # Title Case
        # -------------------------------------------------

        if self.__is_title_case(text):
            score += 5

        # -------------------------------------------------
        # Numbered Heading
        # -------------------------------------------------

        if self.__looks_like_numbered_heading(text):
            score += 12

        # -------------------------------------------------
        # Short Heading
        # -------------------------------------------------

        word_count = len(text.split())

        if 1 <= word_count <= 10:
            score += 5

        # -------------------------------------------------
        # Ends with punctuation
        # -------------------------------------------------

        if text.endswith("."):
            score -= 15

        if text.endswith(","):
            score -= 10

        if text.endswith(";"):
            score -= 10

        # -------------------------------------------------
        # Very long lines are unlikely headings
        # -------------------------------------------------

        if len(text) > 120:
            score -= 20

        elif len(text) > 80:
            score -= 10

        # -------------------------------------------------
        # Top of page bonus
        # -------------------------------------------------

        if layout.y0 < layout.page_height * 0.20:
            score += 5

        # -------------------------------------------------
        # Left aligned headings are common
        # -------------------------------------------------

        if layout.is_left_aligned:
            score += 3

        score = max(0, score)

        return min(score / 100.0, 1.0)

    def __looks_like_numbered_heading(
        self,
        text: str
    ) -> bool:

        patterns = [

            r"^\d+$",
            r"^\d+\.$",
            r"^\d+\.\d+$",
            r"^\d+\.\d+\.\d+$",

            r"^[A-Z]\.$",

            r"^[IVXLCDM]+\.$",

            r"^CHAPTER",

            r"^SECTION",

            r"^APPENDIX",

            r"^ANNEX",

        ]

        upper = text.upper()

        for pattern in patterns:

            if re.match(pattern, upper):
                return True

        return False

    def __is_title_case(
        self,
        text: str
    ) -> bool:

        words = text.split()

        if not words:
            return False

        capitalized = 0

        for word in words:

            if word[:1].isupper():
                capitalized += 1

        return capitalized >= max(1, len(words) * 0.6)