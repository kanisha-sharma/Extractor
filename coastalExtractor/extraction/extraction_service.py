from __future__ import annotations


from typing import Optional


from coastalExtractor.extraction.section_catalog import (
    SectionCatalog
)

from coastalExtractor.extraction.section_selector import (
    SectionSelector
)

from coastalExtractor.extraction.section_extractor import (
    SectionExtractor
)

from coastalExtractor.extraction.extraction_response import (
    ExtractionResponse
)


from coastalExtractor.intelligence.document_analyzer import (
    DocumentIntelligenceAnalyzer
)



class ExtractionService:
    """
    Stage 4 Main Service

    Flow:

    PDF
     |
     ↓
    Stage 3 Intelligence
     |
     ↓
    Section Catalog
     |
     ↓
    User Selection
     |
     ↓
    Section Extraction
     |
     ↓
    Response
    """



    def __init__(
        self,
        pdf_path: str
    ):

        self.pdf_path = pdf_path


        self.analyzer = (
            DocumentIntelligenceAnalyzer(
                pdf_path
            )
        )


        self.catalog = SectionCatalog()

        self.selector = SectionSelector()

        self.extractor = SectionExtractor()


        self.intelligence = None



    # --------------------------------------------------
    # Load Stage 3 Intelligence
    # --------------------------------------------------

    def load_document(self):

        """
        Runs Stage 3 analysis once.
        """

        self.intelligence = (
            self.analyzer.analyze()
        )


        return self.intelligence



    # --------------------------------------------------
    # Section List For Frontend Dropdown
    # --------------------------------------------------

    def get_sections(
        self
    ):

        """
        Returns available sections
        for UI selection.
        """


        if self.intelligence is None:

            self.load_document()



        catalog = self.catalog.build(

            self.intelligence.sections

        )



        return [

            {

                "number": item.id,

                "title": item.title,

                "level": item.level,

                "page_start": item.page_start,

                "page_end": item.page_end,

                "parent": item.parent,

                "children": item.children

            }

            for item in catalog

        ]



    # --------------------------------------------------
    # Extract By Dropdown Number
    # --------------------------------------------------

    def extract_by_number(
        self,
        number: int
    ) -> Optional[ExtractionResponse]:

        """
        Extract section using
        displayed UI number.
        """


        if self.intelligence is None:

            self.load_document()



        section = (

            self.selector.select_by_number(

                self.intelligence.sections,

                number

            )

        )



        if section is None:

            return None



        content = (

            self.extractor.extract(

                section

            )

        )



        return ExtractionResponse.from_section(

            section,

            content

        )



    # --------------------------------------------------
    # Extract By Internal Section ID
    # --------------------------------------------------

    def extract_by_id(
        self,
        section_id: str
    ) -> Optional[ExtractionResponse]:

        """
        Extract section using
        internal section ID.
        """


        if self.intelligence is None:

            self.load_document()



        section = (

            self.selector.select_by_id(

                self.intelligence.sections,

                section_id

            )

        )



        if section is None:

            return None



        content = (

            self.extractor.extract(

                section

            )

        )



        return ExtractionResponse.from_section(

            section,

            content

        )



    # --------------------------------------------------
    # Extract By Section Title
    # --------------------------------------------------

    def extract_by_title(
        self,
        title: str
    ) -> Optional[ExtractionResponse]:

        """
        Extract section using title.

        Example:

        Coastal Shipping
        """



        if self.intelligence is None:

            self.load_document()



        section = (

            self.selector.select_by_title(

                self.intelligence.sections,

                title

            )

        )



        if section is None:

            return None



        content = (

            self.extractor.extract(

                section

            )

        )



        return ExtractionResponse.from_section(

            section,

            content

        )



    # --------------------------------------------------
    # Close Resources
    # --------------------------------------------------

    def close(
        self
    ):

        try:

            self.analyzer.close()


        except Exception:

            pass