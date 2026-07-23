"""
Hierarchy utilities for Stage 3.

Builds and validates hierarchical relationships between
sections produced by the Stage 2 analyzer.
"""

from __future__ import annotations

from typing import List, Optional

from coastalExtractor.models.semantic_models import Section


class HierarchyBuilder:
    """
    Builds and validates semantic section hierarchies.
    """

    def build(self, sections: List[Section]) -> List[Section]:
        """
        Build parent-child hierarchy from a flat list of sections.
        """

        if not sections:
            return []

        sections = sorted(
            sections,
            key=lambda s: (
                s.page_start,
                s.level,
            ),
        )

        roots: List[Section] = []

        stack: List[Section] = []

        for section in sections:

            while stack and stack[-1].level >= section.level:
                stack.pop()

            if stack:
                stack[-1].subsections.append(section)
            else:
                roots.append(section)

            stack.append(section)

        return roots

    def flatten(self, sections: List[Section]) -> List[Section]:
        """
        Convert hierarchy into a flat list.
        """

        result: List[Section] = []

        def visit(section: Section):

            result.append(section)

            for child in section.subsections:

                visit(child)

        for section in sections:

            visit(section)

        return result

    def assign_page_ranges(self, sections: List[Section]) -> None:
        """
        Ensure every section has a valid page_end.
        """

        flat = self.flatten(sections)

        if not flat:
            return

        for index, section in enumerate(flat):

            if index == len(flat) - 1:
                continue

            next_section = flat[index + 1]

            if section.page_end < section.page_start:

                section.page_end = next_section.page_start

    def validate(self, sections: List[Section]) -> List[str]:
        """
        Validate hierarchy consistency.
        """

        errors: List[str] = []

        flat = self.flatten(sections)

        previous_level = None

        for section in flat:

            if section.level < 1:

                errors.append(
                    f"Invalid level in '{section.title}'"
                )

            if section.page_end < section.page_start:

                errors.append(
                    f"Invalid page range in '{section.title}'"
                )

            if (
                previous_level is not None
                and section.level > previous_level + 1
            ):

                errors.append(
                    f"Hierarchy jump detected near '{section.title}'"
                )

            previous_level = section.level

        return errors

    def find_parent(
        self,
        root_sections: List[Section],
        section_id: str,
    ) -> Optional[Section]:
        """
        Find the parent of a section.
        """

        def search(
            current: Section,
            parent: Optional[Section],
        ) -> Optional[Section]:

            if current.id == section_id:
                return parent

            for child in current.subsections:

                result = search(child, current)

                if result is not None:
                    return result

            return None

        for root in root_sections:

            result = search(root, None)

            if result is not None:
                return result

        return None

    def find_section(
        self,
        root_sections: List[Section],
        section_id: str,
    ) -> Optional[Section]:
        """
        Find a section by ID.
        """

        for section in self.flatten(root_sections):

            if section.id == section_id:

                return section

        return None

    def max_depth(
        self,
        sections: List[Section],
    ) -> int:
        """
        Calculate hierarchy depth.
        """

        def depth(section: Section) -> int:

            if not section.subsections:
                return 1

            return 1 + max(
                depth(child)
                for child in section.subsections
            )

        if not sections:
            return 0

        return max(
            depth(section)
            for section in sections
        )