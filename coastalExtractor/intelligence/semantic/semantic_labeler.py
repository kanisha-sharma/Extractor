from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class SemanticLabel:

    text: str

    page: int

    label: str

    confidence: float


class SemanticLabeler:

    """
    Assigns semantic labels to text.

    These labels enrich the output of the
    existing analyzer package.
    """

    TITLE = "TITLE"

    HEADING = "HEADING"

    PARAGRAPH = "PARAGRAPH"

    TABLE_CAPTION = "TABLE_CAPTION"

    FIGURE_CAPTION = "FIGURE_CAPTION"

    FOOTER = "FOOTER"

    HEADER = "HEADER"

    LIST_ITEM = "LIST_ITEM"

    UNKNOWN = "UNKNOWN"

    def label(
        self,
        pages: List[List[str]]
    ) -> List[SemanticLabel]:

        labels = []

        for page_number, lines in enumerate(pages, start=1):

            for index, line in enumerate(lines):

                label, confidence = self.__classify(

                    line,

                    index

                )

                labels.append(

                    SemanticLabel(

                        text=line,

                        page=page_number,

                        label=label,

                        confidence=confidence

                    )

                )

        return labels

    def __classify(

        self,

        text: str,

        line_index: int

    ):

        value = text.strip()

        upper = value.upper()

        if line_index == 0 and len(value) < 120:

            return self.TITLE, 0.95

        if upper.startswith("TABLE"):

            return self.TABLE_CAPTION, 0.95

        if upper.startswith("FIGURE"):

            return self.FIGURE_CAPTION, 0.95

        if upper.startswith("FIG."):

            return self.FIGURE_CAPTION, 0.95

        if value.startswith("•"):

            return self.LIST_ITEM, 0.90

        if value.startswith("- "):

            return self.LIST_ITEM, 0.90

        if value.isupper() and len(value) < 100:

            return self.HEADING, 0.90

        if len(value.split()) > 6:

            return self.PARAGRAPH, 0.80

        return self.UNKNOWN, 0.50