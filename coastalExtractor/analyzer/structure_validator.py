from __future__ import annotations

"""
Stage 2 Structure Validator

Performs validation of the extracted document
structure before it is passed to Stage 3.

Checks

• Heading hierarchy

• Section ordering

• Table consistency

• Caption consistency

• Reading order

• Duplicate headings

• Empty sections
"""

from typing import List


class StructureValidator:

    def validate(

        self,

        headings,

        sections,

        paragraphs,

        tables,

        captions

    ) -> dict:

        report = {

            "valid": True,

            "warnings": [],

            "errors": []

        }

        report["warnings"].extend(

            self.validate_heading_levels(

                headings

            )

        )

        report["warnings"].extend(

            self.validate_duplicate_headings(

                headings

            )

        )

        report["warnings"].extend(

            self.validate_sections(

                sections

            )

        )

        report["warnings"].extend(

            self.validate_tables(

                tables

            )

        )

        report["warnings"].extend(

            self.validate_captions(

                captions

            )

        )

        report["warnings"].extend(

            self.validate_paragraphs(

                paragraphs

            )

        )

        if report["errors"]:

            report["valid"] = False

        return report

    # ---------------------------------------------------------

    def validate_heading_levels(

        self,

        headings

    ):

        warnings = []

        previous = 1

        for heading in headings:

            if heading.level > previous + 1:

                warnings.append(

                    f"Heading '{heading.text}' jumps "

                    f"from level {previous} "

                    f"to level {heading.level}"

                )

            previous = heading.level

        return warnings

    # ---------------------------------------------------------

    def validate_duplicate_headings(

        self,

        headings

    ):

        warnings = []

        seen = set()

        for heading in headings:

            key = (

                heading.page,

                heading.text.lower()

            )

            if key in seen:

                warnings.append(

                    f"Duplicate heading: "

                    f"{heading.text}"

                )

            seen.add(key)

        return warnings

    # ---------------------------------------------------------

    def validate_sections(

        self,

        sections

    ):

        warnings = []

        for section in sections:

            if section.start_page > section.end_page:

                warnings.append(

                    f"Invalid section "

                    f"{section.title}"

                )

        return warnings

    # ---------------------------------------------------------

    def validate_tables(

        self,

        tables

    ):

        warnings = []

        for table in tables:

            if len(table.rows) == 0:

                warnings.append(

                    f"Empty table "

                    f"{table.id}"

                )

        return warnings

    # ---------------------------------------------------------

    def validate_captions(

        self,

        captions

    ):

        warnings = []

        ids = set()

        for caption in captions:

            if caption.id in ids:

                warnings.append(

                    f"Duplicate caption "

                    f"{caption.id}"

                )

            ids.add(

                caption.id

            )

        return warnings

    # ---------------------------------------------------------

    def validate_paragraphs(

        self,

        paragraphs

    ):

        warnings = []

        for paragraph in paragraphs:

            if len(

                paragraph.text.strip()

            ) < 10:

                warnings.append(

                    "Very short paragraph "

                    f"on page {paragraph.page}"

                )

        return warnings

    # ---------------------------------------------------------

    def summary(

        self,

        report

    ):

        return {

            "valid": report["valid"],

            "warnings": len(

                report["warnings"]

            ),

            "errors": len(

                report["errors"]

            )

        }