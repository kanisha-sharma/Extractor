from __future__ import annotations

"""
Stage 2 Page Analyzer

Extracts page-level layout information.

Detects:
    • page size
    • orientation
    • estimated columns
    • margins
    • text density
"""

from dataclasses import dataclass
from typing import List

import fitz

from coastalExtractor.analyzer.layout_analyzer import LayoutSpan


@dataclass
class PageInformation:

    page: int

    width: float
    height: float

    orientation: str

    columns: int

    left_margin: float
    right_margin: float

    top_margin: float
    bottom_margin: float

    text_blocks: int

    text_density: float


class PageAnalyzer:

    def __init__(

        self,

        document: fitz.Document

    ):

        self.document = document

    # ----------------------------------------------------

    def analyze(

        self,

        layout_spans: List[LayoutSpan]

    ) -> List[PageInformation]:

        pages = []

        grouped = {}

        for span in layout_spans:

            grouped.setdefault(

                span.page,

                []

            ).append(span)

        for page_number, page in enumerate(

            self.document,

            start=1

        ):

            spans = grouped.get(

                page_number,

                []

            )

            width = page.rect.width
            height = page.rect.height

            pages.append(

                PageInformation(

                    page=page_number,

                    width=width,

                    height=height,

                    orientation=self.__orientation(

                        width,

                        height

                    ),

                    columns=self.__columns(

                        spans,

                        width

                    ),

                    left_margin=self.__left_margin(

                        spans

                    ),

                    right_margin=self.__right_margin(

                        spans,

                        width

                    ),

                    top_margin=self.__top_margin(

                        spans

                    ),

                    bottom_margin=self.__bottom_margin(

                        spans,

                        height

                    ),

                    text_blocks=len(spans),

                    text_density=self.__density(

                        spans,

                        width,

                        height

                    )

                )

            )

        return pages

    # ----------------------------------------------------

    def __orientation(

        self,

        width,

        height

    ):

        return "landscape" if width > height else "portrait"

    # ----------------------------------------------------

    def __columns(

        self,

        spans,

        page_width

    ):

        if not spans:

            return 1

        midpoint = page_width / 2

        left = 0
        right = 0

        for span in spans:

            center = (

                span.x0 +

                span.x1

            ) / 2

            if center < midpoint:

                left += 1

            else:

                right += 1

        if left > 10 and right > 10:

            return 2

        return 1

    # ----------------------------------------------------

    def __left_margin(self, spans):

        if not spans:

            return 0

        return min(

            span.x0

            for span in spans

        )

    def __right_margin(

        self,

        spans,

        width

    ):

        if not spans:

            return width

        return width - max(

            span.x1

            for span in spans

        )

    def __top_margin(

        self,

        spans

    ):

        if not spans:

            return 0

        return min(

            span.y0

            for span in spans

        )

    def __bottom_margin(

        self,

        spans,

        height

    ):

        if not spans:

            return height

        return height - max(

            span.y1

            for span in spans

        )

    # ----------------------------------------------------

    def __density(

        self,

        spans,

        width,

        height

    ):

        if not spans:

            return 0

        area = width * height

        text_area = 0

        for span in spans:

            text_area += (

                span.width *

                span.height

            )

        return round(

            text_area / area,

            4

        )