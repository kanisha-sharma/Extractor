import fitz

from coastalExtractor.analyzer.font_analyzer import FontAnalyzer
from coastalExtractor.analyzer.layout_analyzer import LayoutAnalyzer
from coastalExtractor.analyzer.toc_detector import TOCDetector
from coastalExtractor.analyzer.heading_classifier import HeadingClassifier
from coastalExtractor.analyzer.section_builder import SectionBuilder

from coastalExtractor.analyzer.paragraph_builder import ParagraphBuilder
from coastalExtractor.analyzer.reading_order_builder import ReadingOrderBuilder
from coastalExtractor.analyzer.table_extractor import TableExtractor
from coastalExtractor.analyzer.image_extractor import ImageExtractor
from coastalExtractor.analyzer.figure_detector import FigureDetector
from coastalExtractor.analyzer.caption_extractor import CaptionExtractor
from coastalExtractor.analyzer.list_extractor import ListExtractor
from coastalExtractor.analyzer.page_analyzer import PageAnalyzer
from coastalExtractor.analyzer.document_statistics import DocumentStatistics
from coastalExtractor.analyzer.structure_validator import StructureValidator
class DocumentAnalyzer:

    def __init__(self, pdf_path):

        self.pdf_path = pdf_path

        self.document = fitz.open(pdf_path)

    def analyze(self):

        total_pages = len(self.document)

        # -----------------------------------
        # Step 1
        # Try TOC
        # -----------------------------------

        toc = TOCDetector(

            self.document

        ).detect()

        # -----------------------------------
        # Step 2
        # Font Analysis
        # -----------------------------------

        font_spans = FontAnalyzer(

            self.document

        ).analyze()

        # -----------------------------------
        # Step 3
        # Layout Analysis
        # -----------------------------------

        layout_spans = LayoutAnalyzer(

            self.document

        ).analyze()

        # -----------------------------------
        # Step 4
        # Heading Detection
        # -----------------------------------

        headings = HeadingClassifier(

            font_spans,

            layout_spans

        ).classify()

        # -----------------------------------
        # Step 5
        # Merge TOC if available
        # -----------------------------------

        if toc:

            for heading in headings:

                for toc_heading in toc:

                    if heading.text.lower() == toc_heading["title"].lower():

                        heading.level = toc_heading["level"]

                        heading.confidence = 1.0

        # -----------------------------------
        # Step 6
        # Build hierarchy
        # -----------------------------------

        sections = SectionBuilder(

            headings,

            total_pages

        ).build()

        # -----------------------------------
        # Step 7
        # Reading Order
        # -----------------------------------

        reading_order = ReadingOrderBuilder().build(

            layout_spans

        )

        # -----------------------------------
        # Step 8
        # Paragraphs
        # -----------------------------------

        paragraphs = ParagraphBuilder().build(

            font_spans,

            layout_spans


        )

        # -----------------------------------
        # Step 9
        # Tables
        # -----------------------------------

        tables = TableExtractor(

            self.document

        ).extract()

        # -----------------------------------
        # Step 10
        # Images
        # -----------------------------------

        images = ImageExtractor(

            self.document

        ).extract()

        # -----------------------------------
        # Step 11
        # Captions
        # -----------------------------------

        captions = CaptionExtractor().extract(

            font_spans

        )

        # -----------------------------------
        # Step 12
        # Figures
        # -----------------------------------

        figures = FigureDetector().detect(

            images,

            captions

        )

        # -----------------------------------
        # Step 13
        # Lists
        # -----------------------------------

        lists = ListExtractor().extract(

            font_spans

        )

        # -----------------------------------
        # Step 14
        # Page Analysis
        # -----------------------------------

        pages = PageAnalyzer(

            self.document

        ).analyze(

            layout_spans

        )

        # -----------------------------------
        # Step 15
        # Statistics
        # -----------------------------------

        statistics = DocumentStatistics().build(

            font_spans,

            paragraphs,

            tables,

            images

        )

        # -----------------------------------
        # Step 16
        # Validation
        # -----------------------------------

        validation = StructureValidator().validate(

            headings,

            sections,

            paragraphs,

            tables,

            captions

        )

        return {

            "total_pages": total_pages,

            "toc": toc,

            "headings": headings,

            "sections": sections,

            "paragraphs": paragraphs,

            "tables": tables,

            "captions": captions,

            "figures": figures,

            "images": images,

            "lists": lists,

            "reading_order": reading_order,

            "layout": layout_spans,

            "fonts": font_spans,

            "pages": pages,

            "statistics": statistics,

            "validation": validation

        }

    def close(self):

        self.document.close()