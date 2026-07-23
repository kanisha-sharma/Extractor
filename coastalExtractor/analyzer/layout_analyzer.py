from dataclasses import dataclass
from typing import List

import fitz


@dataclass
class LayoutSpan:

    text: str

    page: int

    x0: float
    y0: float
    x1: float
    y1: float

    width: float
    height: float

    page_width: float
    page_height: float

    left_margin: float
    right_margin: float

    center_x: float

    is_centered: bool
    is_left_aligned: bool
    is_right_aligned: bool

    block_number: int
    line_number: int
    span_number: int

    column_index: int = 0

    whitespace_above: float = 0.0
    whitespace_below: float = 0.0


class LayoutAnalyzer:

    def __init__(self, document: fitz.Document):

        self.document = document

    def analyze(self) -> List[LayoutSpan]:

        layout_spans: List[LayoutSpan] = []

        for page_number, page in enumerate(self.document, start=1):

            page_width = page.rect.width
            page_height = page.rect.height

            page_dict = page.get_text("dict")

            previous_bottom = None

            line_counter = 0

            for block_index, block in enumerate(page_dict.get("blocks", [])):

                if "lines" not in block:
                    continue

                for line in block["lines"]:

                    line_counter += 1

                    for span_index, span in enumerate(line["spans"]):

                        text = span["text"].strip()

                        if not text:
                            continue

                        x0, y0, x1, y1 = span["bbox"]

                        width = x1 - x0
                        height = y1 - y0

                        center_x = (x0 + x1) / 2

                        left_margin = x0
                        right_margin = page_width - x1

                        tolerance = page_width * 0.05

                        is_centered = (
                            abs(center_x - page_width / 2)
                            <= tolerance
                        )

                        is_left_aligned = (
                            left_margin <= tolerance
                        )

                        is_right_aligned = (
                            right_margin <= tolerance
                        )

                        whitespace_above = 0

                        if previous_bottom is not None:

                            whitespace_above = max(
                                0,
                                y0 - previous_bottom
                            )

                        previous_bottom = y1

                        if center_x < page_width * 0.45:

                            column = 0

                        elif center_x > page_width * 0.55:

                            column = 1

                        else:

                            column = 0

                        layout_spans.append(

                            LayoutSpan(

                                text=text,

                                page=page_number,

                                x0=x0,
                                y0=y0,
                                x1=x1,
                                y1=y1,

                                width=width,
                                height=height,

                                page_width=page_width,
                                page_height=page_height,

                                left_margin=left_margin,
                                right_margin=right_margin,

                                center_x=center_x,

                                is_centered=is_centered,

                                is_left_aligned=is_left_aligned,

                                is_right_aligned=is_right_aligned,

                                block_number=block_index,

                                line_number=line_counter,

                                span_number=span_index,

                                column_index=column,

                                whitespace_above=whitespace_above

                            )

                        )

        self.__calculate_bottom_whitespace(
            layout_spans
        )

        return layout_spans

    def __calculate_bottom_whitespace(

        self,

        spans: List[LayoutSpan]

    ):

        for index in range(len(spans) - 1):

            current = spans[index]

            nxt = spans[index + 1]

            if current.page != nxt.page:

                current.whitespace_below = 0

                continue

            current.whitespace_below = max(

                0,

                nxt.y0 - current.y1

            )

        if spans:

            spans[-1].whitespace_below = 0