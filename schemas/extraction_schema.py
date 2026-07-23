from pydantic import BaseModel

from typing import List, Dict, Any



class SectionOption(BaseModel):

    number: int

    section_id: str

    title: str

    page_start: int

    page_end: int



class SectionCatalogResponse(BaseModel):

    document_id: int

    sections: List[SectionOption]



class ExtractionMetadata(BaseModel):

    paragraphs: int = 0

    tables: int = 0

    lists: int = 0

    captions: int = 0



class SectionExtractionResponse(BaseModel):

    section_id: str

    title: str

    page_start: int

    page_end: int

    content: Dict[str, Any]

    metadata: ExtractionMetadata