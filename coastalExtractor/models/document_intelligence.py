"""
Top-level Stage 3 document intelligence model.

This model aggregates all semantic information extracted
from the document after Stage 3 processing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .semantic_models import (
    Heading,
    Section,
    SemanticTable,
    Caption,
    SemanticList,
    KeyValuePair,
    DocumentMetadata,
    DocumentClassification,
    SemanticEntity,
)


@dataclass
class DocumentIntelligence:
    """
    Final output of Stage 3.
    """

    metadata: DocumentMetadata = field(default_factory=DocumentMetadata)

    classification: DocumentClassification = field(
        default_factory=lambda: DocumentClassification(
            document_type="Unknown",
            confidence=0.0,
            reason=""
        )
    )

    headings: List[Heading] = field(default_factory=list)

    sections: List[Section] = field(default_factory=list)

    tables: List[SemanticTable] = field(default_factory=list)

    captions: List[Caption] = field(default_factory=list)

    lists: List[SemanticList] = field(default_factory=list)

    key_values: List[KeyValuePair] = field(default_factory=list)

    entities: List[SemanticEntity] = field(default_factory=list)

    reading_order: List[str] = field(default_factory=list)

    processing_time: float = 0.0

    version: str = "3.0"

    def summary(self) -> dict:
        """
        Returns a concise summary of the extracted intelligence.
        """

        return {
            "document_type": self.classification.document_type,
            "pages": self.metadata.page_count,
            "headings": len(self.headings),
            "sections": len(self.sections),
            "tables": len(self.tables),
            "lists": len(self.lists),
            "captions": len(self.captions),
            "key_values": len(self.key_values),
            "entities": len(self.entities),
        }