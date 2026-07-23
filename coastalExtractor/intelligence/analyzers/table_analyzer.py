"""
Semantic Table Analyzer

Stage 3:
Converts raw extracted tables into semantic tables.
"""

from __future__ import annotations

from typing import List, Optional

from coastalExtractor.models.semantic_models import (
    SemanticTable,
    Caption,
)


class TableAnalyzer:

    """
    Performs semantic analysis on extracted tables.
    """

    def analyze(
        self,
        tables: List[SemanticTable],
        captions: List[Caption]
    ) -> List[SemanticTable]:

        analyzed_tables = []

        for table in tables:

            table.title = self.__find_caption(
                table,
                captions
            )

            table.headers = self.__detect_headers(
                table.rows
            )

            table.table_type = self.__classify_table(
                table
            )

            table.confidence = self.__confidence(
                table
            )

            analyzed_tables.append(table)

        return analyzed_tables

    def __find_caption(
        self,
        table: SemanticTable,
        captions: List[Caption]
    ) -> Optional[str]:

        candidates = [

            caption

            for caption in captions

            if (
                caption.page == table.page
                and
                caption.target_type.lower() == "table"
            )

        ]

        if not candidates:
            return table.title

        return candidates[0].text

    def __detect_headers(
        self,
        rows: List[List[str]]
    ) -> List[str]:

        if not rows:
            return []

        first_row = rows[0]

        score = 0

        cleaned_headers = []

        for value in first_row:

            if value is None:
                value = ""

            value = str(value).strip()

            cleaned_headers.append(value)

            if value:
                score += 1

        if score >= max(1, len(cleaned_headers) * 0.6):
            return cleaned_headers

        return []

    def __classify_table(
        self,
        table: SemanticTable
    ) -> str:

        title = (table.title or "").lower()

        if "schedule" in title:
            return "schedule"

        if "financial" in title:
            return "financial"

        if "summary" in title:
            return "summary"

        if "result" in title:
            return "results"

        if "comparison" in title:
            return "comparison"

        if "appendix" in title:
            return "appendix"

        headers = [

            str(h).lower()

            for h in table.headers

            if h is not None

        ]

        if "amount" in headers:

            return "financial"

        if "date" in headers:

            return "timeline"

        if "description" in headers:

            return "details"

        return "generic"

    def __confidence(
        self,
        table: SemanticTable
    ) -> float:

        score = 0.5

        if table.title:

            score += 0.15

        if table.headers:

            score += 0.15

        if len(table.rows) > 2:

            score += 0.10

        if len(table.rows) > 10:

            score += 0.05

        if table.table_type != "generic":

            score += 0.05

        return min(score, 1.0)

    def merge_tables(
        self,
        tables: List[SemanticTable]
    ) -> List[SemanticTable]:

        """
        Merge consecutive split tables.
        """

        if len(tables) <= 1:

            return tables

        merged = []

        current = tables[0]

        for nxt in tables[1:]:

            if (

                current.page + 1 == nxt.page

                and

                current.headers == nxt.headers

            ):

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

    def remove_empty_tables(
        self,
        tables: List[SemanticTable]
    ) -> List[SemanticTable]:

        cleaned = []

        for table in tables:

            if len(table.rows) == 0:

                continue

            cleaned.append(table)

        return cleaned

    def statistics(
        self,
        tables: List[SemanticTable]
    ) -> dict:

        return {

            "total_tables": len(tables),

            "financial_tables": len(

                [

                    t

                    for t in tables

                    if t.table_type == "financial"

                ]

            ),

            "generic_tables": len(

                [

                    t

                    for t in tables

                    if t.table_type == "generic"

                ]

            ),

            "average_rows": (

                sum(

                    len(t.rows)

                    for t in tables

                ) / len(tables)

            ) if tables else 0

        }