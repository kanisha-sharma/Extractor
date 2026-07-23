"""
Project-wide constants.

Changing values here affects the entire extraction pipeline.
"""

# ==========================================
# PDF
# ==========================================

MAX_TOC_SCAN_PAGES = 15

MIN_PAGE_NUMBER = 1


# ==========================================
# Heading Detection
# ==========================================

MIN_HEADING_FONT_SIZE = 11

HEADING_CONFIDENCE_THRESHOLD = 0.60

BOLD_SCORE = 0.25

FONT_SIZE_SCORE = 0.35

POSITION_SCORE = 0.20

CAPITALIZATION_SCORE = 0.20


# ==========================================
# Tables
# ==========================================

MIN_TABLE_LINES = 2

MIN_TABLE_COLUMNS = 2

TABLE_HEADER_THRESHOLD = 0.70

CELL_ALIGNMENT_TOLERANCE = 5


# ==========================================
# OCR
# ==========================================

OCR_CONFIDENCE_THRESHOLD = 0.50


# ==========================================
# Section Discovery
# ==========================================

MIN_SECTION_LENGTH = 1


# ==========================================
# Geometry
# ==========================================

OVERLAP_THRESHOLD = 0.40

LINE_ALIGNMENT_TOLERANCE = 3

BOX_MERGE_DISTANCE = 10


# ==========================================
# Text Cleaning
# ==========================================

REMOVE_MULTIPLE_SPACES = True

REMOVE_EMPTY_LINES = True

NORMALIZE_QUOTES = True