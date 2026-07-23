from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import fitz


@dataclass
class Metadata:

    title: Optional[str] = None

    author: Optional[str] = None

    subject: Optional[str] = None

    keywords: Optional[str] = None

    creator: Optional[str] = None

    producer: Optional[str] = None

    creation_date: Optional[str] = None

    modification_date: Optional[str] = None

    language: Optional[str] = None

    page_count: int = 0


class MetadataExtractor:

    def __init__(self, document: fitz.Document):

        self.document = document

    def extract(self) -> Metadata:

        pdf_metadata: Dict[str, Any] = self.document.metadata or {}

        return Metadata(

            title=self.__clean(pdf_metadata.get("title")),

            author=self.__clean(pdf_metadata.get("author")),

            subject=self.__clean(pdf_metadata.get("subject")),

            keywords=self.__clean(pdf_metadata.get("keywords")),

            creator=self.__clean(pdf_metadata.get("creator")),

            producer=self.__clean(pdf_metadata.get("producer")),

            creation_date=self.__clean(pdf_metadata.get("creationDate")),

            modification_date=self.__clean(pdf_metadata.get("modDate")),

            language=self.__detect_language(),

            page_count=len(self.document)

        )

    def to_dict(self) -> Dict[str, Any]:

        metadata = self.extract()

        return metadata.__dict__

    def __detect_language(self) -> Optional[str]:

        meta = self.document.metadata or {}

        language = meta.get("language")

        if language:
            return language

        return None

    @staticmethod
    def __clean(value):

        if value is None:
            return None

        value = str(value).strip()

        if value == "":
            return None

        return value