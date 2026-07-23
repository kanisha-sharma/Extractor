from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Any

from coastalExtractor.models.semantic_models import (
    Heading,
    Paragraph,
    SemanticTable,
    SemanticList,
    Caption,
    KeyValuePair,
    SemanticEntity,
)


@dataclass
class SectionStatistics:

    paragraph_count: int = 0

    table_count: int = 0

    image_count: int = 0

    list_count: int = 0

    caption_count: int = 0

    entity_count: int = 0

    key_value_count: int = 0

    word_count: int = 0


@dataclass
class TargetSection:

    """
    Final output of Stage 4.

    Represents one extracted document section.
    """

    title: str

    heading: Optional[Heading] = None

    start_page: int = 0

    end_page: int = 0

    paragraphs: List[Paragraph] = field(default_factory=list)

    tables: List[SemanticTable] = field(default_factory=list)

    images: List[Any] = field(default_factory=list)

    captions: List[Caption] = field(default_factory=list)

    lists: List[SemanticList] = field(default_factory=list)

    entities: List[SemanticEntity] = field(default_factory=list)

    key_values: List[KeyValuePair] = field(default_factory=list)

    references: List[Any] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    statistics: SectionStatistics = field(
        default_factory=SectionStatistics
    )

    confidence: float = 1.0

    extraction_time: float = 0.0