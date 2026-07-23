from __future__ import annotations

from typing import Optional, List

from coastalExtractor.models.semantic_models import Section


class SectionExtractor:
    """
    Stage 4 - Target Section Extraction

    Extracts selected section data
    from Stage 3 DocumentIntelligence.
    """

    def extract(
        self,
        section: Section
    ) -> dict:

        return {

            "section_id": section.id,

            "title": section.title,

            "level": section.level,

            "page_range": {

                "start": section.page_start,

                "end": section.page_end

            },


            "heading": self._extract_heading(
                section
            ),


            "paragraphs": self._extract_paragraphs(
                section
            ),


            "tables": self._extract_tables(
                section
            ),


            "lists": self._extract_lists(
                section
            ),


            "captions": self._extract_captions(
                section
            ),


            "subsections": [

                {

                    "id": sub.id,

                    "title": sub.title,

                    "page_start": sub.page_start,

                    "page_end": sub.page_end

                }

                for sub in section.subsections

            ]

        }


    # --------------------------------------------------
    # Heading
    # --------------------------------------------------

    def _extract_heading(
        self,
        section: Section
    ) -> Optional[dict]:

        if not section.heading:

            return None


        return {

            "id": section.heading.id,

            "text": section.heading.text,

            "level": section.heading.level,

            "page": section.heading.page

        }


    # --------------------------------------------------
    # Paragraphs
    # --------------------------------------------------

    def _extract_paragraphs(
        self,
        section: Section
    ) -> List[dict]:

        return [

            {

                "id": paragraph.id,

                "text": paragraph.text,

                "page": paragraph.page

            }

            for paragraph in section.paragraphs

        ]


    # --------------------------------------------------
    # Tables
    # --------------------------------------------------

    def _extract_tables(
        self,
        section: Section
    ) -> List[dict]:

        return [

            {

                "id": table.id,

                "page": table.page,

                "title": table.title,

                "headers": table.headers,

                "rows": table.rows,

                "table_type": table.table_type,

                "confidence": table.confidence

            }

            for table in section.tables

        ]


    # --------------------------------------------------
    # Lists
    # --------------------------------------------------

    def _extract_lists(
        self,
        section: Section
    ) -> List[dict]:

        return [

            {

                "id": semantic_list.id,

                "page": semantic_list.page,

                "type": semantic_list.list_type,

                "items": [

                    item.text

                    for item in semantic_list.items

                ]

            }

            for semantic_list in section.lists

        ]


    # --------------------------------------------------
    # Captions
    # --------------------------------------------------

    def _extract_captions(
        self,
        section: Section
    ) -> List[dict]:

        return [

            {

                "id": caption.id,

                "text": caption.text,

                "page": caption.page,

                "type": caption.target_type,

                "target_id": caption.target_id

            }

            for caption in section.captions

        ]