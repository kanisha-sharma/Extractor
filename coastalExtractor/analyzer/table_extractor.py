from __future__ import annotations

"""
Stage 2 Table Extractor

Responsible for:
    • Detecting tables
    • Extracting rows
    • Identifying headers
    • Creating SemanticTable objects
"""

from typing import List, Optional
from dataclasses import dataclass

import fitz

from coastalExtractor.models.semantic_models import (
    SemanticTable,
)


@dataclass
class TableCell:

    row: int

    column: int

    text: str

    bbox: tuple


@dataclass
class RawTable:

    page: int

    bbox: tuple

    cells: List[TableCell]

    rows: List[List[str]]

    confidence: float = 1.0


class TableExtractor:

    """
    Extracts tables using PyMuPDF.

    If no tables are detected the extractor simply
    returns an empty list.
    """

    def __init__(self, document: fitz.Document):

        self.document = document

    # --------------------------------------------------------

    def extract(self) -> List[SemanticTable]:

        semantic_tables: List[SemanticTable] = []

        table_id = 1

        for page_number, page in enumerate(self.document, start=1):

            raw_tables = self.__extract_page_tables(
                page_number,
                page
            )

            for raw in raw_tables:

                semantic_tables.append(

                    self.__convert_table(
                        raw,
                        table_id
                    )

                )

                table_id += 1

        return semantic_tables

    # --------------------------------------------------------

    def __extract_page_tables(
        self,
        page_number: int,
        page: fitz.Page
    ) -> List[RawTable]:

        tables = []

        try:

            finder = page.find_tables()

        except Exception:

            return tables

        if finder is None:

            return tables

        if not hasattr(finder, "tables"):

            return tables

        for table in finder.tables:

            rows = table.extract()

            if rows is None:

                continue

            cells = []

            for r, row in enumerate(rows):

                for c, value in enumerate(row):

                    if value is None:

                        value = ""

                    cells.append(

                        TableCell(

                            row=r,

                            column=c,

                            text=str(value).strip(),

                            bbox=(0, 0, 0, 0)

                        )

                    )

            bbox = getattr(
                table,
                "bbox",
                (0, 0, 0, 0)
            )

            tables.append(

                RawTable(

                    page=page_number,

                    bbox=bbox,

                    rows=rows,

                    cells=cells,

                    confidence=self.__table_confidence(rows)

                )

            )

        return tables

    # --------------------------------------------------------

    def __convert_table(
        self,
        table: RawTable,
        table_id: int
    ) -> SemanticTable:

        headers = self.__detect_headers(
            table.rows
        )

        return SemanticTable(

            id=f"T{table_id}",

            page=table.page,

            title=None,

            headers=headers,

            rows=table.rows,

            table_type=self.__classify_table(
                headers
            ),

            caption=None,

            confidence=table.confidence

        )

    # --------------------------------------------------------

    def __detect_headers(
        self,
        rows: List[List[str]]
    ) -> List[str]:

        if not rows:

            return []

        first = rows[0]

        filled = sum(

            1

            for cell in first

            if str(cell).strip()

        )

        if filled >= max(1, len(first) * 0.6):

            return [

                str(cell).strip()

                for cell in first

            ]

        return []
    
    # --------------------------------------------------------
    # Table Classification
    # --------------------------------------------------------

    def __classify_table(
        self,
        headers: List[str]
    ) -> str:

        if not headers:
            return "generic"

        header_text = " ".join(headers).lower()

        if "amount" in header_text:
            return "financial"

        if "date" in header_text:
            return "timeline"

        if "description" in header_text:
            return "details"

        if "item" in header_text:
            return "inventory"

        if "result" in header_text:
            return "results"

        if "parameter" in header_text:
            return "technical"

        return "generic"

    # --------------------------------------------------------
    # Confidence Score
    # --------------------------------------------------------

    def __table_confidence(
        self,
        rows: List[List[str]]
    ) -> float:

        if not rows:
            return 0.0

        score = 0.40

        if len(rows) >= 2:
            score += 0.15

        if len(rows) >= 5:
            score += 0.10

        if len(rows[0]) >= 2:
            score += 0.10

        non_empty = 0
        total = 0

        for row in rows:

            for cell in row:

                total += 1

                if str(cell).strip():
                    non_empty += 1

        if total:

            density = non_empty / total

            score += density * 0.20

        return min(score, 1.0)

    # --------------------------------------------------------
    # Remove Empty Tables
    # --------------------------------------------------------

    def remove_empty_tables(
        self,
        tables: List[SemanticTable]
    ) -> List[SemanticTable]:

        cleaned = []

        for table in tables:

            if len(table.rows) == 0:
                continue

            has_text = False

            for row in table.rows:

                for value in row:

                    if str(value).strip():

                        has_text = True
                        break

                if has_text:
                    break

            if has_text:

                cleaned.append(table)

        return cleaned

    # --------------------------------------------------------
    # Merge Split Tables
    # --------------------------------------------------------

    def merge_tables(
        self,
        tables: List[SemanticTable]
    ) -> List[SemanticTable]:

        if len(tables) <= 1:
            return tables

        merged = []

        current = tables[0]

        for nxt in tables[1:]:

            same_header = (

                current.headers == nxt.headers

            )

            consecutive = (

                current.page + 1 == nxt.page

            )

            if same_header and consecutive:

                current.rows.extend(

                    nxt.rows

                )

                current.confidence = max(

                    current.confidence,

                    nxt.confidence

                )

            else:

                merged.append(current)

                current = nxt

        merged.append(current)

        return merged

    # --------------------------------------------------------
    # Find Table By Page
    # --------------------------------------------------------

    def tables_on_page(
        self,
        tables: List[SemanticTable],
        page: int
    ) -> List[SemanticTable]:

        return [

            table

            for table in tables

            if table.page == page

        ]

    # --------------------------------------------------------
    # Find Largest Table
    # --------------------------------------------------------

    def largest_table(
        self,
        tables: List[SemanticTable]
    ) -> Optional[SemanticTable]:

        if not tables:

            return None

        return max(

            tables,

            key=lambda table: len(table.rows)

        )
    
    # --------------------------------------------------------
    # Table Statistics
    # --------------------------------------------------------

    def statistics(
        self,
        tables: List[SemanticTable]
    ) -> dict:

        if not tables:

            return {
                "total_tables": 0,
                "average_rows": 0,
                "average_columns": 0,
                "financial_tables": 0,
                "generic_tables": 0
            }

        total_rows = 0
        total_columns = 0

        financial = 0
        generic = 0

        for table in tables:

            total_rows += len(table.rows)

            if table.rows:

                total_columns += max(

                    len(row)

                    for row in table.rows

                )

            if table.table_type == "financial":

                financial += 1

            if table.table_type == "generic":

                generic += 1

        return {

            "total_tables": len(tables),

            "average_rows":

                total_rows / len(tables),

            "average_columns":

                total_columns / len(tables),

            "financial_tables":

                financial,

            "generic_tables":

                generic

        }

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    def validate_tables(
        self,
        tables: List[SemanticTable]
    ) -> List[SemanticTable]:

        valid = []

        for table in tables:

            if not table.rows:
                continue

            if len(table.rows) < 2:
                continue

            column_count = max(

                len(row)

                for row in table.rows

            )

            if column_count < 2:
                continue

            valid.append(table)

        return valid

    # --------------------------------------------------------
    # Print Summary
    # --------------------------------------------------------

    def print_summary(
        self,
        tables: List[SemanticTable]
    ) -> None:

        stats = self.statistics(tables)

        print()

        print("=" * 60)

        print("TABLE EXTRACTION SUMMARY")

        print("=" * 60)

        print(f"Tables              : {stats['total_tables']}")

        print(f"Average Rows        : {stats['average_rows']:.2f}")

        print(f"Average Columns     : {stats['average_columns']:.2f}")

        print(f"Financial Tables    : {stats['financial_tables']}")

        print(f"Generic Tables      : {stats['generic_tables']}")

        print("=" * 60)

    # --------------------------------------------------------
    # Public Convenience API
    # --------------------------------------------------------

    def extract_and_clean(self) -> List[SemanticTable]:

        tables = self.extract()

        tables = self.remove_empty_tables(tables)

        tables = self.merge_tables(tables)

        tables = self.validate_tables(tables)

        return tables