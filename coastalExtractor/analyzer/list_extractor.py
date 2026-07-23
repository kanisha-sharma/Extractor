from __future__ import annotations

"""
Stage 2 List Extractor

Detects

• Bulleted lists

• Numbered lists

• Alphabetic lists

• Roman numeral lists
"""

import re

from dataclasses import dataclass

from typing import List

from coastalExtractor.analyzer.font_analyzer import TextSpan


@dataclass
class ListItem:

    page: int

    text: str

    level: int

    marker: str


@dataclass
class SemanticList:

    id: int

    page: int

    list_type: str

    items: List[ListItem]


class ListExtractor:

    BULLET_PATTERN = r"^[•●▪■◆○◦-]"

    NUMBER_PATTERN = r"^\d+[.)]"

    ALPHA_PATTERN = r"^[a-zA-Z][.)]"

    ROMAN_PATTERN = r"^(i|ii|iii|iv|v|vi|vii|viii|ix|x)[.)]"

    def extract(

        self,

        spans: List[TextSpan]

    ) -> List[SemanticList]:

        lists = []

        current = []

        list_id = 1

        current_type = None

        current_page = None

        for span in spans:

            detected = self.__detect(

                span.text

            )

            if detected is None:

                if current:

                    lists.append(

                        SemanticList(

                            id=list_id,

                            page=current_page,

                            list_type=current_type,

                            items=current

                        )

                    )

                    list_id += 1

                    current = []

                    current_type = None

                continue

            marker, list_type = detected

            if current_page is None:

                current_page = span.page

                current_type = list_type

            current.append(

                ListItem(

                    page=span.page,

                    text=span.text,

                    level=0,

                    marker=marker

                )

            )

        if current:

            lists.append(

                SemanticList(

                    id=list_id,

                    page=current_page,

                    list_type=current_type,

                    items=current

                )

            )

        return lists

    def __detect(

        self,

        text: str

    ):

        value = text.strip()

        if re.match(self.BULLET_PATTERN, value):

            return value[0], "bullet"

        if re.match(self.NUMBER_PATTERN, value):

            return value.split()[0], "number"

        if re.match(self.ALPHA_PATTERN, value):

            return value.split()[0], "alpha"

        if re.match(self.ROMAN_PATTERN, value.lower()):

            return value.split()[0], "roman"

        return None

    def statistics(

        self,

        semantic_lists: List[SemanticList]

    ):

        total_items = sum(

            len(lst.items)

            for lst in semantic_lists

        )

        return {

            "lists": len(semantic_lists),

            "items": total_items

        }