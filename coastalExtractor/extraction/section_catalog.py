from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from coastalExtractor.models.semantic_models import Section


@dataclass
class SectionCatalogItem:
    """
    Represents a selectable section in the UI.
    """

    id: int

    title: str

    level: int

    page_start: int

    page_end: int

    parent: Optional[int] = None

    children: List[int] = field(default_factory=list)


class SectionCatalog:
    """
    Builds a navigation catalog from the Stage 3 sections.

    The catalog is what the frontend will display for
    user selection.
    """

    def build(
        self,
        sections: List[Section]
    ) -> List[SectionCatalogItem]:

        catalog = []

        lookup = {}

        for index, section in enumerate(sections, start=1):

            item = SectionCatalogItem(

                id=index,

                title=section.title,

                level=section.level,

                page_start=section.page_start,

                page_end=section.page_end

            )

            catalog.append(item)

            lookup[section.id] = item

        # -----------------------------------------
        # Build Parent → Child Relationships
        # -----------------------------------------

        for section in sections:

            if not section.subsections:
                continue

            parent = lookup.get(section.id)

            if parent is None:
                continue

            for child in section.subsections:

                child_item = lookup.get(child.id)

                if child_item is None:
                    continue

                child_item.parent = parent.id

                parent.children.append(child_item.id)

        return catalog

    # --------------------------------------------------

    def print_catalog(
        self,
        catalog: List[SectionCatalogItem]
    ):

        print("\nAvailable Sections\n")

        for item in catalog:

            indent = "    " * max(item.level - 1, 0)

            print(

                f"{indent}"

                f"{item.id}. "

                f"{item.title} "

                f"(Pages {item.page_start}-{item.page_end})"

            )

    # --------------------------------------------------

    def get_titles(
        self,
        catalog: List[SectionCatalogItem]
    ) -> List[str]:

        return [

            item.title

            for item in catalog

        ]

    # --------------------------------------------------

    def get(
        self,
        catalog: List[SectionCatalogItem],
        section_id: int
    ) -> Optional[SectionCatalogItem]:

        for item in catalog:

            if item.id == section_id:

                return item

        return None

