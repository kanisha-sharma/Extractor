from dataclasses import dataclass
from typing import List

import fitz


@dataclass
class TextSpan:
    text: str

    page: int

    x0: float
    y0: float
    x1: float
    y1: float

    font: str
    font_size: float

    is_bold: bool
    is_italic: bool

    color: int
    flags: int


class FontAnalyzer:

    def __init__(self, document: fitz.Document):
        """
        Parameters
        ----------
        document : fitz.Document
            Already opened PDF document.
        """
        self.document = document

    def analyze(self) -> List[TextSpan]:

        spans: List[TextSpan] = []

        for page_number, page in enumerate(self.document, start=1):

            page_dict = page.get_text("dict")

            for block in page_dict.get("blocks", []):

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    for span in line["spans"]:

                        text = span["text"].strip()

                        if text == "":
                            continue

                        font_name = span.get("font", "")

                        font_lower = font_name.lower()

                        flags = span.get("flags", 0)

                        is_bold = (
                            "bold" in font_lower
                            or (flags & 16) != 0
                        )

                        is_italic = (
                            "italic" in font_lower
                            or "oblique" in font_lower
                        )

                        bbox = span["bbox"]

                        spans.append(

                            TextSpan(

                                text=text,

                                page=page_number,

                                x0=bbox[0],
                                y0=bbox[1],
                                x1=bbox[2],
                                y1=bbox[3],

                                font=font_name,

                                font_size=span.get("size", 0),

                                is_bold=is_bold,

                                is_italic=is_italic,

                                color=span.get("color", 0),

                                flags=flags

                            )

                        )

        return spans