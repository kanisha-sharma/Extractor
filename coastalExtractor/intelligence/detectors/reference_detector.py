from __future__ import annotations

import re

from dataclasses import dataclass
from typing import List


@dataclass
class Reference:

    text: str

    reference_type: str

    target: str

    page: int

    confidence: float = 1.0


class ReferenceDetector:

    """
    Detects references inside documents.

    Examples

    See Table 4

    Refer Section 3

    Appendix A

    Annex II

    Figure 12

    Chapter 5
    """

    PATTERNS = {

        "TABLE":

        re.compile(

            r"(Table\s+\d+[A-Za-z\-]*)",

            re.IGNORECASE

        ),

        "FIGURE":

        re.compile(

            r"(Figure\s+\d+[A-Za-z\-]*)",

            re.IGNORECASE

        ),

        "SECTION":

        re.compile(

            r"(Section\s+\d+(\.\d+)*)",

            re.IGNORECASE

        ),

        "CHAPTER":

        re.compile(

            r"(Chapter\s+\d+)",

            re.IGNORECASE

        ),

        "ANNEX":

        re.compile(

            r"(Annex\s+[A-Z0-9IVX]+)",

            re.IGNORECASE

        ),

        "APPENDIX":

        re.compile(

            r"(Appendix\s+[A-Z0-9IVX]+)",

            re.IGNORECASE

        )

    }

    def detect(

        self,

        pages: List[List[str]]

    ) -> List[Reference]:

        references = []

        for page_number, lines in enumerate(

            pages,

            start=1

        ):

            for line in lines:

                for ref_type, pattern in self.PATTERNS.items():

                    for match in pattern.findall(line):

                        if isinstance(match, tuple):

                            value = match[0]

                        else:

                            value = match

                        references.append(

                            Reference(

                                text=value,

                                reference_type=ref_type,

                                target=value,

                                page=page_number,

                                confidence=0.95

                            )

                        )

        return references