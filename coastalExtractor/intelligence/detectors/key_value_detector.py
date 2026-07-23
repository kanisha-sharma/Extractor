from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class KeyValue:

    key: str

    value: str

    page: int


class KeyValueDetector:

    """
    Detects key-value pairs like:

    IMO Number : 12345

    Name = ABC

    Port - Mumbai
    """

    SEPARATORS = [

        ":",

        "=",

        "-"

    ]

    def detect(
        self,
        document
    ) -> List[KeyValue]:

        pairs: List[KeyValue] = []

        for page_number, page in enumerate(document, start=1):

            text = page.get_text("text")

            lines = text.splitlines()

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                kv = self.__extract(line)

                if kv:

                    pairs.append(

                        KeyValue(

                            key=kv[0],

                            value=kv[1],

                            page=page_number

                        )

                    )

        return pairs

    def to_dictionary(

        self,

        pairs: List[KeyValue]

    ) -> Dict[str, str]:

        result = {}

        for pair in pairs:

            result[pair.key] = pair.value

        return result

    def __extract(

        self,

        line: str

    ):

        for separator in self.SEPARATORS:

            if separator in line:

                left, right = line.split(

                    separator,

                    1

                )

                key = left.strip()

                value = right.strip()

                if key and value:

                    return key, value

        return None