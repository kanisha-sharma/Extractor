from __future__ import annotations

from dataclasses import dataclass
from typing import List

from coastalExtractor.analyzer.paragraph_builder import Paragraph


@dataclass
class ReadingElement:
    """
    Represents one element in the document reading sequence.
    """

    order: int

    page: int

    element_type: str

    content: Paragraph


class ReadingOrderBuilder:
    """
    Determines the logical reading order of paragraphs.

    Supports:
    - Single-column PDFs
    - Two-column PDFs
    - Multi-page documents

    (Can later be extended for complex magazine layouts.)
    """

    def build(
        self,
        paragraphs: List[Paragraph]
    ) -> List[ReadingElement]:

        if not paragraphs:
            return []

        pages = {}

        for paragraph in paragraphs:

            pages.setdefault(
                paragraph.page,
                []
            ).append(paragraph)

        ordered: List[ReadingElement] = []

        order = 1

        for page_number in sorted(pages.keys()):

            page_paragraphs = pages[page_number]

            if self.__is_two_column(page_paragraphs):

                ordered_paragraphs = self.__two_column_order(
                    page_paragraphs
                )

            else:

                ordered_paragraphs = sorted(
                    page_paragraphs,
                    key=lambda p: (
                        p.y0,
                        p.x0
                    )
                )

            for paragraph in ordered_paragraphs:

                ordered.append(

                    ReadingElement(

                        order=order,

                        page=paragraph.page,

                        element_type="paragraph",

                        content=paragraph

                    )

                )

                order += 1

        return ordered

    # -----------------------------------------------------

    def __is_two_column(
        self,
        paragraphs: List[Paragraph]
    ) -> bool:

        if len(paragraphs) < 6:
            return False

        centers = [

            (paragraph.x0 + paragraph.x1) / 2

            for paragraph in paragraphs

        ]

        page_width = max(

            paragraph.x1

            for paragraph in paragraphs

        )

        midpoint = page_width / 2

        left = sum(

            1

            for center in centers

            if center < midpoint

        )

        right = len(centers) - left

        return left >= 2 and right >= 2

    # -----------------------------------------------------

    def __two_column_order(
        self,
        paragraphs: List[Paragraph]
    ) -> List[Paragraph]:

        page_width = max(

            paragraph.x1

            for paragraph in paragraphs

        )

        midpoint = page_width / 2

        left_column = []

        right_column = []

        for paragraph in paragraphs:

            center = (

                paragraph.x0 + paragraph.x1

            ) / 2

            if center < midpoint:

                left_column.append(paragraph)

            else:

                right_column.append(paragraph)

        left_column.sort(

            key=lambda p: (
                p.y0,
                p.x0
            )

        )

        right_column.sort(

            key=lambda p: (
                p.y0,
                p.x0
            )

        )

        return left_column + right_column

    # -----------------------------------------------------

    def reading_text(
        self,
        ordered: List[ReadingElement]
    ) -> str:

        lines = []

        for element in ordered:

            if element.element_type == "paragraph":

                lines.append(

                    element.content.text

                )

        return "\n\n".join(lines)

    # -----------------------------------------------------

    def statistics(
        self,
        ordered: List[ReadingElement]
    ) -> dict:

        pages = {

            element.page

            for element in ordered

        }

        return {

            "pages": len(pages),

            "elements": len(ordered),

            "paragraphs": len(

                [

                    element

                    for element in ordered

                    if element.element_type == "paragraph"

                ]

            )

        }