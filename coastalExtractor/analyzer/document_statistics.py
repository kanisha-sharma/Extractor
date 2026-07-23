from __future__ import annotations

"""
Stage 2 Document Statistics

Computes useful statistics
used by Stage 3.
"""

from typing import List

from coastalExtractor.analyzer.font_analyzer import TextSpan
from coastalExtractor.analyzer.paragraph_builder import Paragraph
from coastalExtractor.analyzer.image_extractor import ExtractedImage
from coastalExtractor.models.semantic_models import SemanticTable


class DocumentStatistics:

    def build(

        self,

        font_spans: List[TextSpan],

        paragraphs: List[Paragraph],

        tables: List[SemanticTable],

        images: List[ExtractedImage]

    ) -> dict:

        return {

            "pages":

                len({

                    span.page

                    for span in font_spans

                }),

            "text_spans":

                len(font_spans),

            "paragraphs":

                len(paragraphs),

            "tables":

                len(tables),

            "images":

                len(images),

            "average_font":

                self.average_font(

                    font_spans

                ),

            "largest_font":

                self.largest_font(

                    font_spans

                ),

            "average_paragraph_length":

                self.average_paragraph(

                    paragraphs

                )

        }

    # ------------------------------------------

    def average_font(

        self,

        spans

    ):

        if not spans:

            return 0

        return round(

            sum(

                span.font_size

                for span in spans

            ) / len(spans),

            2

        )

    # ------------------------------------------

    def largest_font(

        self,

        spans

    ):

        if not spans:

            return 0

        return max(

            span.font_size

            for span in spans

        )

    # ------------------------------------------

    def average_paragraph(

        self,

        paragraphs

    ):

        if not paragraphs:

            return 0

        return round(

            sum(

                len(

                    paragraph.text

                )

                for paragraph in paragraphs

            ) / len(paragraphs),

            2

        )