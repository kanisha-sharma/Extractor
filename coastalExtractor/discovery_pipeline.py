from sqlalchemy.orm import Session

from coastalExtractor.analyzer.document_analyzer import DocumentAnalyzer
from coastalExtractor.discovery_service import DiscoveryService


class DiscoveryPipeline:

    def __init__(
        self,
        pdf_path: str,
        document_id: int,
        db: Session
    ):

        self.pdf_path = pdf_path

        self.document_id = document_id

        self.db = db

    def run(self):

        analyzer = DocumentAnalyzer(

            self.pdf_path

        )

        result = analyzer.analyze()

        analyzer.close()

        DiscoveryService(

            self.db

        ).save_sections(

            self.document_id,

            result["sections"]

        )

        return result