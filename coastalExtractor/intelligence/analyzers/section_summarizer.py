from __future__ import annotations

from dataclasses import dataclass
from typing import List

from coastalExtractor.models.semantic_models import Section


@dataclass
class SectionSummary:

    title: str

    page_start: int

    page_end: int

    summary: str


class SectionSummarizer:

    """
    Generates lightweight summaries for every section.
    """

    def summarize(

        self,

        sections: List[Section],

        max_sentences: int = 3

    ) -> List[SectionSummary]:

        results = []

        for section in sections:

            text = ""

            for paragraph in section.paragraphs:

                text += paragraph.text.strip()

                text += " "

            summary = self.__summarize(

                text,

                max_sentences

            )

            results.append(

                SectionSummary(

                    title=section.title,

                    page_start=section.page_start,

                    page_end=section.page_end,

                    summary=summary

                )

            )

        return results

    def __summarize(

        self,

        text: str,

        max_sentences: int

    ) -> str:

        text = text.strip()

        if not text:

            return ""

        sentences = [

            sentence.strip()

            for sentence in text.replace(

                "\n",

                " "

            ).split(".")

            if sentence.strip()

        ]

        if not sentences:

            return ""

        return ". ".join(

            sentences[:max_sentences]

        ) + "."