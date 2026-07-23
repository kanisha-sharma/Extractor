from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from coastalExtractor.models.semantic_models import (
    Section,
    Heading,
    SemanticTable,
    Caption,
    SemanticList,
    SemanticEntity,
)


@dataclass
class Relationship:

    source: str

    target: str

    relation: str


class RelationshipBuilder:

    """
    Creates semantic relationships between
    different document objects.
    """

    def build(

        self,

        sections: List[Section],

        headings: List[Heading],

        tables: List[SemanticTable],

        captions: List[Caption],

        lists: List[SemanticList],

        entities: List[SemanticEntity],

    ) -> List[Relationship]:

        relationships = []

        heading_lookup = {

            h.text.strip().lower(): h

            for h in headings

        }

        for section in sections:

            heading = heading_lookup.get(

                section.title.strip().lower()

            )

            if heading:

                relationships.append(

                    Relationship(

                        source=heading.id,

                        target=section.id,

                        relation="defines"

                    )

                )

        for table in tables:

            for section in sections:

                if section.page_start <= table.page <= section.page_end:

                    relationships.append(

                        Relationship(

                            source=section.id,

                            target=table.id,

                            relation="contains_table"

                        )

                    )

                    break

        for caption in captions:

            for table in tables:

                if (

                    caption.page == table.page

                    and caption.target_type.lower() == "table"

                ):

                    relationships.append(

                        Relationship(

                            source=caption.id,

                            target=table.id,

                            relation="describes"

                        )

                    )

        for semantic_list in lists:

            for section in sections:

                if section.page_start <= semantic_list.page <= section.page_end:

                    relationships.append(

                        Relationship(

                            source=section.id,

                            target=semantic_list.id,

                            relation="contains_list"

                        )

                    )

        for entity in entities:

            for section in sections:

                if section.page_start <= entity.page <= section.page_end:

                    relationships.append(

                        Relationship(

                            source=section.id,

                            target=entity.text,

                            relation="mentions"

                        )

                    )

        return relationships