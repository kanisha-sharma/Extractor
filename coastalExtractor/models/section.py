from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .document_structure import (
    Paragraph,
    TableReference,
    Figure,
    ImageReference,
)


@dataclass
class Section:
    """
    Represents a logical document section.

    This model intentionally maintains only a downward hierarchy
    (children) to avoid circular references during serialization.
    """

    title: str

    level: int

    start_page: int

    end_page: int

    confidence: float = 1.0

    children: List["Section"] = field(default_factory=list)

    paragraphs: List[Paragraph] = field(default_factory=list)

    tables: List[TableReference] = field(default_factory=list)

    figures: List[Figure] = field(default_factory=list)

    images: List[ImageReference] = field(default_factory=list)

    def add_child(self, child: "Section") -> None:
        """
        Add a child section.

        No parent reference is stored to avoid circular references.
        """
        self.children.append(child)

    def add_paragraph(self, paragraph: Paragraph) -> None:
        self.paragraphs.append(paragraph)

    def add_table(self, table: TableReference) -> None:
        self.tables.append(table)

    def add_figure(self, figure: Figure) -> None:
        self.figures.append(figure)

    def add_image(self, image: ImageReference) -> None:
        self.images.append(image)

    @property
    def page_count(self) -> int:
        return self.end_page - self.start_page + 1

    @property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @property
    def has_content(self) -> bool:
        return any([
            self.paragraphs,
            self.tables,
            self.figures,
            self.images
        ])