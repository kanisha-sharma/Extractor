from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Caption:

    text: str

    page: int

    caption_type: str

    number: str | None = None


class CaptionDetector:

    """
    Detects Figure, Table, Image, Diagram,
    Chart and Annex captions.
    """

    PATTERN = re.compile(

        r"^(Figure|Fig\.?|Table|Image|Diagram|Chart|Annex)\s*([A-Za-z0-9\-\.]*)[:\-]?\s*(.*)",

        re.IGNORECASE

    )

    def detect(self, pages: List[List[str]]) -> List[Caption]:

        captions = []

        for page_number, lines in enumerate(pages, start=1):

            for line in lines:

                line = line.strip()

                match = self.PATTERN.match(line)

                if not match:
                    continue

                caption_type = match.group(1)

                number = match.group(2).strip()

                remainder = match.group(3).strip()

                text = line

                if remainder:

                    text = f"{caption_type} {number} {remainder}".strip()

                captions.append(

                    Caption(

                        text=text,

                        page=page_number,

                        caption_type=caption_type,

                        number=number if number else None

                    )

                )

        return captions