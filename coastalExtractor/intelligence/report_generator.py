from __future__ import annotations

from coastalExtractor.models.document_intelligence import (
    DocumentIntelligence
)


class ReportGenerator:

    """
    Generates a human-readable report
    from Document Intelligence.
    """

    def generate(

        self,

        intelligence: DocumentIntelligence

    ) -> str:

        lines = []

        lines.append("DOCUMENT INTELLIGENCE REPORT")
        lines.append("=" * 60)
        lines.append("")

        lines.append(
            f"Document Type : {intelligence.classification.document_type}"
        )

        lines.append(
            f"Confidence    : {intelligence.classification.confidence:.2f}"
        )

        lines.append(
            f"Pages         : {intelligence.metadata.page_count}"
        )

        lines.append("")

        lines.append(
            f"Sections      : {len(intelligence.sections)}"
        )

        lines.append(
            f"Headings      : {len(intelligence.headings)}"
        )

        lines.append(
            f"Tables        : {len(intelligence.tables)}"
        )

        lines.append(
            f"Captions      : {len(intelligence.captions)}"
        )

        lines.append(
            f"Lists         : {len(intelligence.lists)}"
        )

        lines.append(
            f"Key Values    : {len(intelligence.key_values)}"
        )

        lines.append(
            f"Entities      : {len(intelligence.entities)}"
        )

        lines.append("")
        lines.append("SECTION SUMMARY")
        lines.append("-" * 60)

        for section in intelligence.sections:

            lines.append(

                f"{section.title} "

                f"(Pages {section.page_start}-{section.page_end})"

            )

        lines.append("")
        lines.append("END OF REPORT")

        return "\n".join(lines)