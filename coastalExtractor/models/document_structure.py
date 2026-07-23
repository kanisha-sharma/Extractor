from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ==========================================================
# BASIC MODELS
# ==========================================================

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

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center(self):
        return (
            (self.x1 + self.x2) / 2,
            (self.y1 + self.y2) / 2,
        )


# ==========================================================
# FONT INFORMATION
# ==========================================================

@dataclass
class TextStyle:

    font_name: str = ""

    font_size: float = 0.0

    bold: bool = False

    italic: bool = False

    underline: bool = False

    color: str = "#000000"


# ==========================================================
# OCR WORD
# ==========================================================

@dataclass
class Word:

    text: str

    bbox: BoundingBox

    confidence: float = 1.0


# ==========================================================
# TEXT BLOCK
# ==========================================================

@dataclass
class TextBlock:

    id: int

    text: str

    page: int

    bbox: BoundingBox

    style: TextStyle = field(default_factory=TextStyle)

    words: List[Word] = field(default_factory=list)

    confidence: float = 1.0

    block_type: str = "text"

    reading_order: int = -1


# ==========================================================
# TABLE BLOCK
# ==========================================================

@dataclass
class TableBlock:

    id: int

    page: int

    bbox: BoundingBox

    rows: List[List[str]] = field(default_factory=list)

    title: Optional[str] = None

    confidence: float = 1.0


# ==========================================================
# IMAGE BLOCK
# ==========================================================

@dataclass
class ImageBlock:

    id: int

    page: int

    bbox: BoundingBox

    image_path: Optional[str] = None

    caption: Optional[str] = None


# ==========================================================
# PAGE LAYOUT
# ==========================================================

@dataclass
class PageLayout:

    page_number: int

    width: float

    height: float

    text_blocks: List[TextBlock] = field(default_factory=list)

    tables: List[TableBlock] = field(default_factory=list)

    images: List[ImageBlock] = field(default_factory=list)


# ==========================================================
# COMPLETE DOCUMENT LAYOUT
# ==========================================================

@dataclass
class DocumentLayout:

    filename: str

    total_pages: int

    pages: List[PageLayout] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)


# ==========================================================
# STAGE 2 PARAGRAPH
# ==========================================================

@dataclass
class Paragraph:

    text: str

    page: int


# ==========================================================
# TABLE REFERENCE
# ==========================================================

@dataclass
class TableReference:

    table_number: Optional[str]

    title: Optional[str]

    page: int

    table_id: Optional[int] = None


# ==========================================================
# FIGURE
# ==========================================================

@dataclass
class Figure:

    title: str

    page: int


# ==========================================================
# IMAGE REFERENCE
# ==========================================================

@dataclass
class ImageReference:

    page: int

    bbox: Tuple


# ==========================================================
# SECTION
# ==========================================================

@dataclass
class Section:

    title: str

    level: int

    start_page: int

    end_page: int

    confidence: float

    children: List["Section"] = field(default_factory=list)

    paragraphs: List[Paragraph] = field(default_factory=list)

    tables: List[TableReference] = field(default_factory=list)

    figures: List[Figure] = field(default_factory=list)

    images: List[ImageReference] = field(default_factory=list)

    def add_child(
        self,
        child: "Section"
    ) -> None:

        self.children.append(child)

    def add_paragraph(
        self,
        paragraph: Paragraph
    ) -> None:

        self.paragraphs.append(paragraph)

    def add_table(
        self,
        table: TableReference
    ) -> None:

        self.tables.append(table)

    def add_figure(
        self,
        figure: Figure
    ) -> None:

        self.figures.append(figure)

    def add_image(
        self,
        image: ImageReference
    ) -> None:

        self.images.append(image)

    @property
    def page_count(self) -> int:

        return self.end_page - self.start_page + 1

    @property
    def is_leaf(self) -> bool:

        return len(self.children) == 0

    @property
    def has_content(self) -> bool:

        return (
            bool(self.paragraphs)
            or bool(self.tables)
            or bool(self.figures)
            or bool(self.images)
        )


# ==========================================================
# COMPLETE DOCUMENT STRUCTURE
# ==========================================================

@dataclass
class DocumentStructure:

    filename: str

    total_pages: int

    sections: List[Section] = field(default_factory=list)

    layout: Optional[DocumentLayout] = None

    statistics: dict = field(default_factory=dict)

    validation: dict = field(default_factory=dict)