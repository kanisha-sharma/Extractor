from __future__ import annotations

from typing import List, Optional

from coastalExtractor.models.semantic_models import Section


class SectionSelector:
    """
    Stage 4 - Section Selection Layer

    Selects a target section from Stage 3
    DocumentIntelligence output.
    """


    def select_by_number(
        self,
        sections: List[Section],
        number: int
    ) -> Optional[Section]:

        """
        Select section using displayed number.

        Example:
        User selects:
        3

        Returns:
        sections[2]
        """

        if number <= 0:
            return None

        index = number - 1

        if index >= len(sections):
            return None

        return sections[index]


    def select_by_id(
        self,
        sections: List[Section],
        section_id: str
    ) -> Optional[Section]:

        """
        Select section using internal ID.

        Example:
        S3
        """

        for section in sections:

            if section.id == section_id:

                return section

        return None



    def select_by_title(
        self,
        sections: List[Section],
        title: str
    ) -> Optional[Section]:

        """
        Select section using heading/title.
        """

        title = title.strip().lower()


        for section in sections:

            if section.title.lower() == title:

                return section


        return None



    def search(
        self,
        sections: List[Section],
        keyword: str
    ) -> List[Section]:

        """
        Search sections.

        Example:
        keyword="coastal"

        Returns:

        Coastal Shipping
        Coastal Regulations
        """

        keyword = keyword.lower()


        results = []


        for section in sections:

            if keyword in section.title.lower():

                results.append(section)


        return results



    def available_sections(
        self,
        sections: List[Section]
    ) -> List[dict]:

        """
        Creates frontend-friendly section list.

        Used for dropdown/buttons.
        """

        output = []


        for index, section in enumerate(
            sections,
            start=1
        ):

            output.append(

                {
                    "number": index,
                    "id": section.id,
                    "title": section.title,
                    "page_start": section.page_start,
                    "page_end": section.page_end
                }

            )


        return output

