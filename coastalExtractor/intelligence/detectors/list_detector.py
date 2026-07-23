from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class ListItem:

    page: int

    level: int

    marker: str

    text: str

    ordered: bool


class ListDetector:

    """
    Detects:
    • Bullet Lists
    • Numbered Lists
    • Alphabetic Lists
    • Roman Lists
    """

    BULLET_PATTERN = re.compile(
        r"^(\u2022|\-|\*|●|▪|■|○)\s+(.*)"
    )

    NUMBER_PATTERN = re.compile(
        r"^(\d+[\.\)])\s+(.*)"
    )

    LETTER_PATTERN = re.compile(
        r"^([A-Za-z][\.\)])\s+(.*)"
    )

    ROMAN_PATTERN = re.compile(
        r"^([ivxlcdmIVXLCDM]+[\.\)])\s+(.*)"
    )

    def detect(
        self,
        pages: List[List[str]]
    ) -> List[ListItem]:

        items: List[ListItem] = []

        for page_number, lines in enumerate(pages, start=1):

            for line in lines:

                line = line.strip()

                result = self.__parse(line)

                if result is None:
                    continue

                marker, text, ordered = result

                level = self.__indentation_level(line)

                items.append(

                    ListItem(

                        page=page_number,

                        level=level,

                        marker=marker,

                        text=text,

                        ordered=ordered

                    )

                )

        return items

    def __parse(self, line):

        match = self.BULLET_PATTERN.match(line)

        if match:

            return (

                match.group(1),

                match.group(2),

                False

            )

        match = self.NUMBER_PATTERN.match(line)

        if match:

            return (

                match.group(1),

                match.group(2),

                True

            )

        match = self.LETTER_PATTERN.match(line)

        if match:

            return (

                match.group(1),

                match.group(2),

                True

            )

        match = self.ROMAN_PATTERN.match(line)

        if match:

            return (

                match.group(1),

                match.group(2),

                True

            )

        return None

    @staticmethod
    def __indentation_level(line: str) -> int:

        spaces = len(line) - len(line.lstrip())

        return spaces // 4