from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, List



@dataclass
class ExtractionResponse:
    """
    Stage 4 response model.

    Final output returned after
    target section extraction.
    """


    section_id: str

    title: str

    page_start: int

    page_end: int


    content: Dict[str, Any] = field(
        default_factory=dict
    )


    metadata: Dict[str, Any] = field(
        default_factory=dict
    )



    def to_dict(self):

        return {


            "section_id":

                self.section_id,


            "title":

                self.title,


            "page_start":

                self.page_start,


            "page_end":

                self.page_end,


            "content":

                self.content,


            "metadata":

                self.metadata

        }



    @classmethod
    def from_section(
        cls,
        section,
        extracted_content
    ):

        return cls(

            section_id=section.id,

            title=section.title,

            page_start=section.page_start,

            page_end=section.page_end,


            content=extracted_content,


            metadata={

                "tables":

                    len(section.tables),


                "paragraphs":

                    len(section.paragraphs),


                "lists":

                    len(section.lists),


                "captions":

                    len(section.captions)

            }

        )