from __future__ import annotations

import time
from typing import List

import fitz

# ============================================================
# Stage 2
# ============================================================

from coastalExtractor import intelligence
from coastalExtractor.analyzer.document_analyzer import (
    DocumentAnalyzer as Stage2Analyzer
)

# ============================================================
# Intelligence
# ============================================================

from coastalExtractor.intelligence.analyzers.metadata_extractor import (
    MetadataExtractor
)

from coastalExtractor.intelligence.analyzers.document_classifier import (
    DocumentClassifier
)

from coastalExtractor.intelligence.analyzers.table_analyzer import (
    TableAnalyzer
)

from coastalExtractor.intelligence.detectors.caption_detector import (
    CaptionDetector
)

from coastalExtractor.intelligence.detectors.key_value_detector import (
    KeyValueDetector
)

from coastalExtractor.intelligence.detectors.list_detector import (
    ListDetector
)

from coastalExtractor.intelligence.semantic.semantic_labeler import (
    SemanticLabeler
)

from coastalExtractor.intelligence.utils.hierarchy import (
    HierarchyBuilder
)

# ============================================================
# Models
# ============================================================

from coastalExtractor.models.document_intelligence import (
    DocumentIntelligence
)

from coastalExtractor.models.semantic_models import (
    Heading,
    Section,
    SemanticTable,
    SemanticList,
    Caption,
    KeyValuePair
)
from coastalExtractor.intelligence.analyzers.keyword_extractor import (
    KeywordExtractor
)

from coastalExtractor.intelligence.analyzers.section_summarizer import (
    SectionSummarizer
)

from coastalExtractor.intelligence.analyzers.statistics_analyzer import (
    StatisticsAnalyzer
)

from coastalExtractor.intelligence.analyzers.topic_analyzer import (
    TopicAnalyzer
)

from coastalExtractor.intelligence.detectors.entity_detector import (
    EntityDetector
)

from coastalExtractor.intelligence.detectors.reference_detector import (
    ReferenceDetector
)

from coastalExtractor.intelligence.exporters.json_exporter import (
    JsonExporter
)

from coastalExtractor.intelligence.exporters.database_exporter import (
    DatabaseExporter
)

from coastalExtractor.intelligence.utils.relationship_builder import (
    RelationshipBuilder
)

from coastalExtractor.intelligence.report_generator import (
    ReportGenerator
)

class DocumentIntelligenceAnalyzer:

    """
    Stage 3 Pipeline

    Converts Stage 2 output into semantic document
    intelligence.
    """

    def __init__(self, pdf_path: str):

        self.pdf_path = pdf_path

        self.document = fitz.open(pdf_path)

        self.stage2 = Stage2Analyzer(pdf_path)

        self.metadata_extractor = MetadataExtractor(
            self.document
        )

        self.classifier = DocumentClassifier()

        self.table_analyzer = TableAnalyzer()

        self.caption_detector = CaptionDetector()

        self.list_detector = ListDetector()

        self.keyvalue_detector = KeyValueDetector()

        self.semantic_labeler = SemanticLabeler()

        self.hierarchy_builder = HierarchyBuilder()

        # ==========================
        # Advanced Stage 3
        # ==========================

        self.keyword_extractor = KeywordExtractor()

        self.section_summarizer = SectionSummarizer()

        self.statistics_analyzer = StatisticsAnalyzer()

        self.topic_analyzer = TopicAnalyzer()

        self.entity_detector = EntityDetector()

        self.reference_detector = ReferenceDetector()

        self.relationship_builder = RelationshipBuilder()

        self.json_exporter = JsonExporter()

        self.database_exporter = DatabaseExporter()

        self.report_generator = ReportGenerator()

    # ---------------------------------------------------------

    def analyze(self) -> DocumentIntelligence:

        start_time = time.time()

        intelligence = DocumentIntelligence()

        # =====================================================
        # Stage 2
        # =====================================================

        stage2 = self.stage2.analyze()

        # =====================================================
        # Metadata
        # =====================================================

        metadata = self.metadata_extractor.extract()

        intelligence.metadata.title = metadata.title
        intelligence.metadata.author = metadata.author
        intelligence.metadata.subject = metadata.subject
        intelligence.metadata.language = metadata.language
        intelligence.metadata.creation_date = metadata.creation_date
        intelligence.metadata.modified_date = metadata.modification_date
        intelligence.metadata.page_count = metadata.page_count
        intelligence.metadata.producer = metadata.producer
        intelligence.metadata.keywords = metadata.keywords

        pages = [
            page.get_text("text").splitlines()
            for page in self.document
        ]

        intelligence.keywords = self.keyword_extractor.extract(
            pages
        )

        # =====================================================
        # Headings
        # =====================================================

        for index, heading in enumerate(
            stage2.get("headings", []),
            start=1
        ):

            intelligence.headings.append(

                Heading(

                    id=f"H{index}",

                    text=heading.text,

                    level=heading.level,

                    page=heading.page,

                    confidence=heading.confidence

                )

            )

        # =====================================================
        # Sections
        # =====================================================

        for index, section in enumerate(
            stage2.get("sections", []),
            start=1
        ):

            intelligence.sections.append(

                Section(

                    id=f"S{index}",

                    title=section.title,

                    level=section.level,

                    page_start=section.start_page,

                    page_end=section.end_page

                )

            )

        intelligence.sections = self.hierarchy_builder.build(

            intelligence.sections

        )

        # =====================================================
        # Reading Order
        # =====================================================

        if "reading_order" in stage2:

            intelligence.reading_order = [

                block.text

                if hasattr(block, "text")

                else str(block)

                for block in stage2["reading_order"]

            ]

        else:

            intelligence.reading_order = [

                heading.text

                for heading in intelligence.headings

            ]
        
        intelligence.topics = self.topic_analyzer.analyze(
            intelligence.keywords
        )

        # =====================================================
        # Captions
        # =====================================================

        if "captions" in stage2:

            for cap in stage2["captions"]:

                intelligence.captions.append(

                    Caption(

                        id=str(cap.id),

                        text=cap.text,

                        page=cap.page,

                        target_type=cap.caption_type,

                        target_id=(
                            str(cap.target_id)
                            if cap.target_id is not None
                            else None
                        )

                    )

                )

        else:

            captions: List[Caption] = self.caption_detector.detect(

                self.document

            )

            intelligence.captions.extend(

                captions

            )

        # =====================================================
        # Lists
        # =====================================================

        if "lists" in stage2:

            intelligence.lists.extend(

                stage2["lists"]

            )

        else:

            semantic_lists: List[SemanticList] = self.list_detector.detect(

                self.document

            )

            intelligence.lists.extend(

                semantic_lists

            )

        # =====================================================
        # Key Values
        # =====================================================

        key_values: List[KeyValuePair] = self.keyvalue_detector.detect(

            self.document

        )

        intelligence.key_values.extend(

            key_values

        )

        # =====================================================
        # Tables
        # =====================================================

        semantic_tables: List[SemanticTable] = []

        if "tables" in stage2:

            semantic_tables = self.table_analyzer.analyze(

                stage2["tables"],

                intelligence.captions

            )

            semantic_tables = self.table_analyzer.merge_tables(

                semantic_tables

            )

            semantic_tables = self.table_analyzer.remove_empty_tables(

                semantic_tables

            )

            intelligence.tables.extend(

                semantic_tables

            )

        # =====================================================
        # Semantic Entity Extraction
        # =====================================================

        intelligence.entities = self.entity_detector.detect(
            pages
        )

        #References
        intelligence.references = self.reference_detector.detect(
            pages
        )

        # =====================================================
        # Link Headings to Sections
        # =====================================================

        heading_lookup = {

            heading.text.strip().lower(): heading

            for heading in intelligence.headings

        }

        for section in intelligence.sections:

            heading = heading_lookup.get(

                section.title.strip().lower()

            )

            if heading is not None:

                section.heading = heading

        # =====================================================
        # Assign Tables to Sections
        # =====================================================

        for table in intelligence.tables:

            for section in intelligence.sections:

                if (

                    section.page_start

                    <= table.page

                    <= section.page_end

                ):

                    section.tables.append(

                        table

                    )

                    break

        # =====================================================
        # Assign Lists to Sections
        # =====================================================

        for semantic_list in intelligence.lists:

            for section in intelligence.sections:

                if (

                    section.page_start

                    <= semantic_list.page

                    <= section.page_end

                ):

                    section.lists.append(

                        semantic_list

                    )

                    break

        # =====================================================
        # Assign Captions to Sections
        # =====================================================

        for caption in intelligence.captions:

            for section in intelligence.sections:

                if (

                    section.page_start

                    <= caption.page

                    <= section.page_end

                ):

                    section.captions.append(

                        caption

                    )

                    break
        
        # =====================================================
        # Relationships
        # =====================================================

        # =====================================================
        # Relationships
        # =====================================================

        intelligence.relationships = (
            self.relationship_builder.build(
                intelligence.sections,
                intelligence.headings,
                intelligence.tables,
                intelligence.captions,
                intelligence.lists,
                intelligence.entities,
            )
        )

        # =====================================================
        # Classification
        # =====================================================

        document_text = "\n".join(
            heading.text for heading in intelligence.headings
        )

        intelligence.classification = self.classifier.classify(
            document_text
        )

        # =====================================================
        # Statistics
        # =====================================================

        intelligence.statistics = (
            self.statistics_analyzer.analyze(
                intelligence.metadata.page_count,
                intelligence.sections,
                intelligence.tables,
                intelligence.lists,
                intelligence.captions,
                intelligence.entities,
            )
        )

        # =====================================================
        # Section Summaries
        # =====================================================

        intelligence.section_summaries = (
            self.section_summarizer.summarize(
                intelligence.sections
            )
        )

        # =====================================================
        # Processing Statistics
        # =====================================================

        intelligence.processing_time = (

            time.time() - start_time

        )

        return intelligence

    # ---------------------------------------------------------
    # Convenience Helpers
    # ---------------------------------------------------------

    def summary(self):

        """
        Returns a lightweight summary without exposing
        the complete intelligence object.
        """

        result = self.analyze()

        return {

            "document_type":

                result.classification.document_type,

            "confidence":

                result.classification.confidence,

            "pages":

               result.metadata.page_count,

            "headings":

                len(result.headings),

            "sections":

                len(result.sections),

            "tables":

                len(result.tables),

            "captions":

                len(result.captions),

            "lists":

                len(result.lists),

            "key_values":

                len(result.key_values),

            "entities":

                len(result.entities),

            "processing_time":

                round(

                    result.processing_time,

                    3

                )

        }

    #JSON Exporter 
    def export_json(self, output_path):

        self.json_exporter.export(

            self.analyze(),

            output_path

        )

    #Export to Database
    def export_database(self, db):

        self.database_exporter.export(

            self.analyze(),

            db

        )

    #Generate report
    def generate_report(self):

        return self.report_generator.generate(

            self.analyze()

        )

    # ---------------------------------------------------------
    # Close Resources
    # ---------------------------------------------------------

    def close(self):

        """
        Close all open resources.
        """

        try:
            self.stage2.close()
        except Exception:
            pass

        try:
            self.document.close()
        except Exception:
            pass

    # ---------------------------------------------------------

    def __enter__(self):

        return self

    # ---------------------------------------------------------

    def __exit__(

        self,

        exc_type,

        exc_val,

        exc_tb

    ):

        self.close()