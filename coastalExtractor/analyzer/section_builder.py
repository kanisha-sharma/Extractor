from typing import List

from coastalExtractor.models.section import Section
from coastalExtractor.models.heading import Heading


class SectionBuilder:

    def __init__(self, headings: List[Heading], total_pages: int):

        self.headings = sorted(
            headings,
            key=lambda h: (
                h.page,
                h.y0
            )
        )

        self.total_pages = total_pages

    def build(self) -> List[Section]:

        if len(self.headings) == 0:
            return []

        sections = []

        stack = []

        for index, heading in enumerate(self.headings):

            if index == len(self.headings) - 1:

                end_page = self.total_pages

            else:

                end_page = self.headings[index + 1].page

            section = Section(

                title=heading.text,

                level=heading.level,

                start_page=heading.page,

                end_page=end_page,

                confidence=heading.confidence

            )

            while stack and stack[-1].level >= section.level:

                stack.pop()

            if stack:

                stack[-1].add_child(section)

            else:

                sections.append(section)

            stack.append(section)

        return sections