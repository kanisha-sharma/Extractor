from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from coastalExtractor.analyzer.font_analyzer import TextSpan
from coastalExtractor.analyzer.layout_analyzer import LayoutSpan


@dataclass
class Paragraph:

    id: int

    page: int

    text: str

    spans: List[TextSpan] = field(default_factory=list)

    x0: float = 0
    y0: float = 0
    x1: float = 0
    y1: float = 0


class ParagraphBuilder:

    """
    Groups individual text spans into logical paragraphs.

    Paragraph boundaries are determined using:
        • page
        • block number
        • vertical spacing
        • column index
    """

    def build(
        self,
        font_spans: List[TextSpan],
        layout_spans: List[LayoutSpan]
    ) -> List[Paragraph]:

        paragraphs: List[Paragraph] = []

        if not font_spans or not layout_spans:
            return paragraphs

        layout_lookup = {

            (
                l.page,
                l.text,
                l.block_number,
                l.line_number,
                l.span_number
            ): l

            for l in layout_spans

        }

        current_spans: List[TextSpan] = []

        current_layouts: List[LayoutSpan] = []

        paragraph_id = 1

        previous_layout = None

        for span in font_spans:

            layout = self.__find_layout(
                span,
                layout_lookup
            )

            if layout is None:
                continue

            if previous_layout is None:

                current_spans.append(span)
                current_layouts.append(layout)

                previous_layout = layout

                continue

            if self.__new_paragraph(
                previous_layout,
                layout
            ):

                paragraphs.append(

                    self.__create_paragraph(
                        paragraph_id,
                        current_spans,
                        current_layouts
                    )

                )

                paragraph_id += 1

                current_spans = []
                current_layouts = []

            current_spans.append(span)
            current_layouts.append(layout)

            previous_layout = layout

        if current_spans:

            paragraphs.append(

                self.__create_paragraph(
                    paragraph_id,
                    current_spans,
                    current_layouts
                )

            )

        return paragraphs

    def __find_layout(
        self,
        span: TextSpan,
        lookup
    ):

        for key, value in lookup.items():

            if (
                key[0] == span.page
                and key[1] == span.text
            ):
                return value

        return None

    def __new_paragraph(
        self,
        previous: LayoutSpan,
        current: LayoutSpan
    ) -> bool:

        if previous.page != current.page:
            return True

        if previous.block_number != current.block_number:
            return True

        if previous.column_index != current.column_index:
            return True

        if current.whitespace_above > 12:
            return True

        return False

    def __create_paragraph(
        self,
        paragraph_id: int,
        spans: List[TextSpan],
        layouts: List[LayoutSpan]
    ) -> Paragraph:

        text = " ".join(

            span.text.strip()

            for span in spans

        ).strip()

        x0 = min(layout.x0 for layout in layouts)
        y0 = min(layout.y0 for layout in layouts)
        x1 = max(layout.x1 for layout in layouts)
        y1 = max(layout.y1 for layout in layouts)

        return Paragraph(

            id=paragraph_id,

            page=layouts[0].page,

            text=text,

            spans=list(spans),

            x0=x0,
            y0=y0,
            x1=x1,
            y1=y1

        )