from __future__ import annotations

from dataclasses import dataclass
from typing import List

from coastalExtractor.models.semantic_models import (
    Section,
    SemanticTable,
    SemanticList,
    Caption,
    SemanticEntity,
)


@dataclass
class DocumentStatistics:

    pages: int = 0

    sections: int = 0

    tables: int = 0

    lists: int = 0

    captions: int = 0

    entities: int = 0

    words: int = 0

    characters: int = 0

    average_words_per_section: float = 0.0


class StatisticsAnalyzer:

    """
    Generates statistics describing the document.
    """

    def analyze(

        self,

        page_count: int,

        sections: List[Section],

        tables: List[SemanticTable],

        lists: List[SemanticList],

        captions: List[Caption],

        entities: List[SemanticEntity],

    ) -> DocumentStatistics:

        stats = DocumentStatistics()

        stats.pages = page_count

        stats.sections = len(sections)

        stats.tables = len(tables)

        stats.lists = len(lists)

        stats.captions = len(captions)

        stats.entities = len(entities)

        total_words = 0

        total_characters = 0

        for section in sections:

            for paragraph in section.paragraphs:

                total_words += len(

                    paragraph.text.split()

                )

                total_characters += len(

                    paragraph.text

                )

        stats.words = total_words

        stats.characters = total_characters

        if stats.sections:

            stats.average_words_per_section = round(

                total_words / stats.sections,

                2

            )

        return stats