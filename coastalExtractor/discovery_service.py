from sqlalchemy.orm import Session

from database.crud import (
    create_section
)


class DiscoveryService:

    def __init__(self, db: Session):

        self.db = db

    def save_sections(
        self,
        document_id: int,
        sections
    ):

        saved_sections = []

        for section in sections:

            saved = self.__save_recursive(
                document_id=document_id,
                section=section
            )

            saved_sections.append(saved)

        return saved_sections

    def __save_recursive(
        self,
        document_id,
        section
    ):

        db_section = create_section(

            db=self.db,

            document_id=document_id,

            section_name=section.title,

            start_page=section.start_page,

            end_page=section.end_page

        )

        for child in section.children:

            self.__save_recursive(

                document_id,

                child

            )

        return db_section