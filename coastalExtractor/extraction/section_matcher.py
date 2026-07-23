from __future__ import annotations

from typing import List, Optional

from coastalExtractor.models.semantic_models import Section


class SectionMatcher:
    """
    Matches user selected section
    with Stage 3 detected sections.
    """

    def match(
        self,
        sections: List[Section],
        selected_id: str
    ) -> Optional[Section]:

        """
        Finds section using section id.

        Example:
        User selects:
            S3

        Returns:
            Section object
        """

        for section in sections:

            if section.id == selected_id:
                return section

            child = self.__search_children(
                section,
                selected_id
            )

            if child:
                return child

        return None


    def __search_children(
        self,
        section: Section,
        selected_id: str
    ) -> Optional[Section]:

        for child in section.subsections:

            if child.id == selected_id:
                return child

            result = self.__search_children(
                child,
                selected_id
            )

            if result:
                return result

        return None



    def validate_selection(
        self,
        sections: List[Section],
        selected_id: str
    ) -> bool:

        """
        Checks whether selected
        section exists.
        """

        return self.match(
            sections,
            selected_id
        ) is not None