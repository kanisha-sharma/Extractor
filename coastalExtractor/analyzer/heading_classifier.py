from typing import List

from coastalExtractor.analyzer.font_analyzer import TextSpan
from coastalExtractor.analyzer.layout_analyzer import LayoutSpan
from coastalExtractor.analyzer.confidence_scorer import ConfidenceScorer
from coastalExtractor.models.heading import Heading


class HeadingClassifier:

    def __init__(
        self,
        font_spans: List[TextSpan],
        layout_spans: List[LayoutSpan]
    ):

        self.font_spans = font_spans

        self.layout_lookup = {
            (layout.page, layout.text): layout
            for layout in layout_spans
        }

    def classify(self) -> List[Heading]:

        headings: List[Heading] = []

        if not self.font_spans:
            return headings

        average_font = (
            sum(span.font_size for span in self.font_spans)
            / len(self.font_spans)
        )

        scorer = ConfidenceScorer(
            average_font
        )

        for span in self.font_spans:

            layout = self.layout_lookup.get(
                (span.page, span.text)
            )

            if layout is None:
                continue

            confidence = scorer.score(
                span,
                layout
            )

            if confidence < 0.50:
                continue

            headings.append(

                Heading(

                    text=span.text,

                    page=span.page,

                    level=self.detect_level(
                        span.text
                    ),

                    confidence=confidence,

                    font_size=span.font_size,

                    is_bold=span.is_bold,

                    is_centered=layout.is_centered,

                    x0=span.x0,
                    y0=span.y0,
                    x1=span.x1,
                    y1=span.y1

                )

            )

        headings.sort(
            key=lambda h: (
                h.page,
                h.y0
            )
        )

        return headings

    def detect_level(self, text: str) -> int:

        text = text.strip()

        upper = text.upper()

        if upper.startswith("CHAPTER"):
            return 1

        if upper.startswith("SECTION"):
            return 1

        if upper.startswith("APPENDIX"):
            return 1

        if upper.startswith("ANNEX"):
            return 1

        if "." in text:

            dots = text.count(".")

            if dots == 1:
                return 2

            if dots == 2:
                return 3

            return 4

        if len(text) >= 2 and text[:2].isdigit():
            return 2

        return 2