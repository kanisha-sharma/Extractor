from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ClassificationResult:

    document_type: str

    confidence: float


class DocumentClassifier:

    """
    Rule-based document classifier.

    Can later be replaced by an ML model.
    """

    KEYWORDS = {

        "invoice": [
            "invoice",
            "bill",
            "gst",
            "tax invoice",
        ],

        "report": [
            "abstract",
            "executive summary",
            "conclusion",
        ],

        "manual": [
            "chapter",
            "appendix",
            "revision",
        ],

        "form": [
            "date",
            "name",
            "signature",
        ],

        "contract": [
            "agreement",
            "party",
            "witness",
            "terms",
        ],

        "imo_document": [
            "imo",
            "maritime",
            "msc",
            "solas",
            "circular",
        ]
    }

    def classify(self, text: str) -> ClassificationResult:

        lower = text.lower()

        best_type = "unknown"

        best_score = 0

        for doc_type, keywords in self.KEYWORDS.items():

            score = 0

            for keyword in keywords:

                if keyword in lower:

                    score += 1

            if score > best_score:

                best_score = score

                best_type = doc_type

        confidence = 0.0

        if best_score > 0:

            confidence = min(best_score / 5, 1.0)

        return ClassificationResult(

            document_type=best_type,

            confidence=confidence

        )

    def classify_pages(self, pages: List[str]) -> ClassificationResult:

        return self.classify(

            "\n".join(pages)

        )