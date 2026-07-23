"""
Semantic models for Stage 3 - Document Intelligence.

These models represent the logical structure of a document after
layout analysis has been completed in Stage 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ----------------------------------------------------------------------
# Common Models
# ----------------------------------------------------------------------

@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        return self.x2 - self.x1

    @property
    def height(self) -> float:
        return self.y2 - self.y1


# ----------------------------------------------------------------------
# Heading
# ----------------------------------------------------------------------

@dataclass
class Heading:
    id: str
    text: str
    level: int
    page: int
    confidence: float = 1.0
    bbox: Optional[BoundingBox] = None


# ----------------------------------------------------------------------
# Paragraph
# ----------------------------------------------------------------------

@dataclass
class Paragraph:
    id: str
    text: str
    page: int
    bbox: Optional[BoundingBox] = None


# ----------------------------------------------------------------------
# Lists
# ----------------------------------------------------------------------

@dataclass
class ListItem:
    text: str
    level: int = 0


@dataclass
class SemanticList:
    id: str
    list_type: str        # bullet / numbered / alpha
    page: int
    items: List[ListItem] = field(default_factory=list)


# ----------------------------------------------------------------------
# Captions
# ----------------------------------------------------------------------

@dataclass
class Caption:
    id: str
    text: str
    page: int
    target_type: str      # image / table
    target_id: Optional[str] = None
    bbox: Optional[BoundingBox] = None


# ----------------------------------------------------------------------
# Tables
# ----------------------------------------------------------------------

@dataclass
class SemanticTable:
    id: str
    page: int
    title: Optional[str] = None
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)
    table_type: str = "generic"
    caption: Optional[str] = None
    confidence: float = 1.0


# ----------------------------------------------------------------------
# Key Value
# ----------------------------------------------------------------------

@dataclass
class KeyValuePair:
    key: str
    value: str
    page: int
    confidence: float = 1.0


# ----------------------------------------------------------------------
# Metadata
# ----------------------------------------------------------------------

@dataclass
class DocumentMetadata:
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    language: Optional[str] = None
    creation_date: Optional[str] = None
    modified_date: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    page_count: int = 0
    producer: Optional[str] = None


# ----------------------------------------------------------------------
# Classification
# ----------------------------------------------------------------------

@dataclass
class DocumentClassification:
    document_type: str
    confidence: float
    reason: str = ""


# ----------------------------------------------------------------------
# Section
# ----------------------------------------------------------------------

@dataclass
class Section:
    id: str

    title: str

    level: int

    page_start: int

    page_end: int

    heading: Optional[Heading] = None

    paragraphs: List[Paragraph] = field(default_factory=list)

    tables: List[SemanticTable] = field(default_factory=list)

    lists: List[SemanticList] = field(default_factory=list)

    captions: List[Caption] = field(default_factory=list)

    subsections: List["Section"] = field(default_factory=list)


# ----------------------------------------------------------------------
# Semantic Entity
# ----------------------------------------------------------------------

@dataclass
class SemanticEntity:
    entity_type: str
    text: str
    page: int
    confidence: float = 1.0
    attributes: Dict[str, Any] = field(default_factory=dict)