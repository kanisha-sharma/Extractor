from __future__ import annotations

import re

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Entity:

    text: str

    entity_type: str

    page: int

    confidence: float = 1.0

    attributes: Dict = field(default_factory=dict)


class EntityDetector:

    """
    Detects semantic entities from document text.

    Supported entities:

    • IMO References
    • Circulars
    • SOLAS
    • MARPOL
    • ISPS
    • Ports
    • Countries
    • Ship Names
    • GT
    • DWT
    • TEU
    • Dates
    • Percentages
    """

    IMO_PATTERN = re.compile(
        r"\b(?:MSC|MEPC|RES|SN|A)\.?[A-Z0-9\/().-]+\b",
        re.IGNORECASE
    )

    GT_PATTERN = re.compile(
        r"\b\d+(?:,\d+)?\s*GT\b",
        re.IGNORECASE
    )

    DWT_PATTERN = re.compile(
        r"\b\d+(?:,\d+)?\s*DWT\b",
        re.IGNORECASE
    )

    TEU_PATTERN = re.compile(
        r"\b\d+(?:,\d+)?\s*TEU\b",
        re.IGNORECASE
    )

    PERCENT_PATTERN = re.compile(
        r"\b\d+(?:\.\d+)?\s*%",
        re.IGNORECASE
    )

    DATE_PATTERN = re.compile(

        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"

        r"|"

        r"\b\d{1,2}\s"

        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"

        r"[a-z]*"

        r"\s\d{4}\b",

        re.IGNORECASE

    )

    PORTS = {

        "mumbai",
        "cochin",
        "kochi",
        "chennai",
        "kandla",
        "vizag",
        "paradip",
        "haldia",
        "tuticorin",
        "ennore",
        "mormugao"

    }

    COUNTRIES = {

        "india",
        "singapore",
        "japan",
        "china",
        "uae",
        "usa",
        "uk",
        "australia"

    }

    REGULATIONS = {

        "imo",
        "solas",
        "marpol",
        "isps",
        "stcw",
        "load line",
        "colreg"

    }

    SHIP_PATTERN = re.compile(

        r"\b(?:MV|M\.V\.|MT|M/T|SS|FV)\s+[A-Z][A-Za-z0-9\- ]+",

        re.IGNORECASE

    )

    def detect(

        self,

        pages: List[List[str]]

    ) -> List[Entity]:

        entities: List[Entity] = []

        for page_number, lines in enumerate(

            pages,

            start=1

        ):

            for line in lines:

                entities.extend(

                    self.__extract(

                        line,

                        page_number

                    )

                )

        return entities

    def __extract(

        self,

        text: str,

        page: int

    ) -> List[Entity]:

        results: List[Entity] = []

        lower = text.lower()

        for match in self.IMO_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "IMO_REFERENCE",

                    page,

                    0.98

                )

            )

        for match in self.GT_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "GROSS_TONNAGE",

                    page,

                    0.99

                )

            )

        for match in self.DWT_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "DEADWEIGHT",

                    page,

                    0.99

                )

            )

        for match in self.TEU_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "TEU",

                    page,

                    0.99

                )

            )

        for match in self.DATE_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "DATE",

                    page,

                    0.95

                )

            )

        for match in self.PERCENT_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "PERCENTAGE",

                    page,

                    0.95

                )

            )

        for match in self.SHIP_PATTERN.findall(text):

            results.append(

                Entity(

                    match,

                    "SHIP",

                    page,

                    0.95

                )

            )

        for regulation in self.REGULATIONS:

            if regulation in lower:

                results.append(

                    Entity(

                        regulation,

                        "REGULATION",

                        page,

                        0.90

                    )

                )

        for port in self.PORTS:

            if port in lower:

                results.append(

                    Entity(

                        port.title(),

                        "PORT",

                        page,

                        0.90

                    )

                )

        for country in self.COUNTRIES:

            if country in lower:

                results.append(

                    Entity(

                        country.title(),

                        "COUNTRY",

                        page,

                        0.90

                    )

                )

        return results