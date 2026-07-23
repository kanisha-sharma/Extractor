from __future__ import annotations

from sqlalchemy.orm import Session

from coastalExtractor.models.document_intelligence import DocumentIntelligence


class DatabaseExporter:
    """
    Persists Stage 3 intelligence into the database.

    Currently implemented as a placeholder because the
    existing database schema stores only uploaded documents.
    This class can later be extended once semantic tables
    are added to the database.
    """

    def export(
        self,
        db: Session,
        intelligence: DocumentIntelligence,
        document_id: int,
    ) -> bool:

        # --------------------------------------------------
        # Future implementation:
        #
        # Store
        #   - Metadata
        #   - Sections
        #   - Tables
        #   - Entities
        #   - Key Values
        #   - Relationships
        #
        # into normalized PostgreSQL tables.
        # --------------------------------------------------

        db.commit()

        return True