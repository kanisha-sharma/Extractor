from __future__ import annotations

"""
Stage 2 Caption Extractor

Detects captions for:
    • Figures
    • Tables
    • Charts
    • Plates
    • Diagrams
    • Images

Supports:
    • Figure 1
    • Figure 1:
    • Figure 1-
    • Figure 2A
    • Figure IV
    • Table 3
    • Table 5.1
    • Multi-line captions
"""

import re

from dataclasses import dataclass

from typing import List
from typing import Optional
from typing import Dict

from coastalExtractor.analyzer.font_analyzer import TextSpan


# ---------------------------------------------------------
# Caption Model
# ---------------------------------------------------------

@dataclass
class Caption:

    id: int

    page: int

    text: str

    caption_type: str

    number: Optional[str] = None

    target_id: Optional[int] = None

    position: str = "unknown"

    x0: float = 0

    y0: float = 0

    x1: float = 0

    y1: float = 0

    confidence: float = 1.0


# ---------------------------------------------------------
# Caption Extractor
# ---------------------------------------------------------

class CaptionExtractor:

    CAPTION_PATTERNS = [

        re.compile(
            r"^figure\s+([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        ),

        re.compile(
            r"^fig\.?\s*([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        ),

        re.compile(
            r"^table\s+([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        ),

        re.compile(
            r"^plate\s+([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        ),

        re.compile(
            r"^chart\s+([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        ),

        re.compile(
            r"^diagram\s+([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        ),

        re.compile(
            r"^image\s+([0-9IVXLCDM]+[A-Za-z]?([.-][0-9]+)?)[:.\-]?$",
            re.IGNORECASE
        )

    ]

    def extract(

        self,

        spans: List[TextSpan]

    ) -> List[Caption]:

        spans = sorted(

            spans,

            key=lambda s: (

                s.page,

                s.y0,

                s.x0

            )

        )

        captions: List[Caption] = []

        caption_id = 1

        index = 0

        while index < len(spans):

            span = spans[index]

            if not self.__is_caption_start(span.text):

                index += 1

                continue

            merged_text = span.text.strip()

            x0 = span.x0
            y0 = span.y0
            x1 = span.x1
            y1 = span.y1

            next_index = index + 1

            while next_index < len(spans):

                nxt = spans[next_index]

                if nxt.page != span.page:
                    break

                if nxt.y0 - y1 > 18:
                    break

                if self.__is_caption_start(nxt.text):
                    break

                merged_text += " " + nxt.text.strip()

                x0 = min(x0, nxt.x0)
                y0 = min(y0, nxt.y0)
                x1 = max(x1, nxt.x1)
                y1 = max(y1, nxt.y1)

                next_index += 1

            captions.append(

                Caption(

                    id=caption_id,

                    page=span.page,

                    text=merged_text,

                    caption_type=self.__caption_type(

                        merged_text

                    ),

                    number=self.__caption_number(

                        merged_text

                    ),

                    x0=x0,

                    y0=y0,

                    x1=x1,

                    y1=y1,

                    confidence=self.__confidence(

                        span,

                        merged_text

                    )

                )

            )

            caption_id += 1

            index = next_index

        return captions
    
    # ---------------------------------------------------------
    # Caption Detection
    # ---------------------------------------------------------

    def __is_caption_start(

        self,

        text: str

    ) -> bool:

        text = text.strip()

        if len(text) < 4:
            return False

        for pattern in self.CAPTION_PATTERNS:

            if pattern.match(text):

                return True

        return False


    def __caption_type(

        self,

        text: str

    ) -> str:

        text = text.lower()

        if text.startswith("table"):
            return "table"

        if text.startswith("fig"):
            return "figure"

        if text.startswith("figure"):
            return "figure"

        if text.startswith("image"):
            return "image"

        if text.startswith("plate"):
            return "plate"

        if text.startswith("chart"):
            return "chart"

        if text.startswith("diagram"):
            return "diagram"

        return "unknown"


    # ---------------------------------------------------------
    # Caption Number
    # ---------------------------------------------------------

    def __caption_number(

        self,

        text: str

    ) -> Optional[str]:

        for pattern in self.CAPTION_PATTERNS:

            match = pattern.match(

                text.strip()

            )

            if match:

                return match.group(1)

        return None


    # ---------------------------------------------------------
    # Confidence
    # ---------------------------------------------------------

    def __confidence(

        self,

        span: TextSpan,

        caption_text: str

    ) -> float:

        score = 0.60

        if span.is_bold:
            score += 0.10

        if span.is_italic:
            score += 0.05

        if 8 <= span.font_size <= 14:
            score += 0.10

        if len(caption_text) > 15:
            score += 0.05

        if len(caption_text) > 35:
            score += 0.05

        if self.__caption_number(caption_text):
            score += 0.05

        if ":" in caption_text:
            score += 0.03

        if "." in caption_text:
            score += 0.02

        return min(score, 1.0)


    # ---------------------------------------------------------
    # Link Captions
    # ---------------------------------------------------------

    def link_to_objects(

        self,

        captions: List[Caption],

        objects: List

    ) -> None:

        """
        Links captions with extracted
        figures/images/tables.
        """

        for caption in captions:

            nearest = None

            nearest_distance = float("inf")

            for obj in objects:

                if getattr(obj, "page", None) != caption.page:
                    continue

                if not hasattr(obj, "y0"):
                    continue

                distance = abs(obj.y0 - caption.y0)

                if distance < nearest_distance:

                    nearest = obj

                    nearest_distance = distance

            if nearest is None:
                continue

            caption.target_id = getattr(
                nearest,
                "id",
                None
            )

            if nearest.y0 > caption.y1:
                caption.position = "above"

            elif nearest.y1 < caption.y0:
                caption.position = "below"

            else:
                caption.position = "overlap"

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def captions_on_page(

        self,

        captions: List[Caption],

        page: int

    ) -> List[Caption]:

        return [

            caption

            for caption in captions

            if caption.page == page

        ]


    def get_table_captions(

        self,

        captions: List[Caption]

    ) -> List[Caption]:

        return [

            caption

            for caption in captions

            if caption.caption_type == "table"

        ]


    def get_figure_captions(

        self,

        captions: List[Caption]

    ) -> List[Caption]:

        return [

            caption

            for caption in captions

            if caption.caption_type == "figure"

        ]


    def remove_duplicates(

        self,

        captions: List[Caption]

    ) -> List[Caption]:

        unique: Dict[tuple, Caption] = {}

        for caption in captions:

            key = (

                caption.page,

                caption.text.strip().lower()

            )

            if key not in unique:

                unique[key] = caption

        return list(unique.values())


    def sort(

        self,

        captions: List[Caption]

    ) -> List[Caption]:

        return sorted(

            captions,

            key=lambda c: (

                c.page,

                c.y0,

                c.x0

            )

        )


    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    def statistics(

        self,

        captions: List[Caption]

    ) -> dict:

        figure_count = len(

            [

                c

                for c in captions

                if c.caption_type == "figure"

            ]

        )

        table_count = len(

            [

                c

                for c in captions

                if c.caption_type == "table"

            ]

        )

        linked = len(

            [

                c

                for c in captions

                if c.target_id is not None

            ]

        )

        average_confidence = (

            sum(

                c.confidence

                for c in captions

            ) / len(captions)

        ) if captions else 0.0

        return {

            "total_captions": len(captions),

            "figure_captions": figure_count,

            "table_captions": table_count,

            "linked_captions": linked,

            "average_confidence": round(
                average_confidence,
                3
            )

        }


    # ---------------------------------------------------------
    # Debug
    # ---------------------------------------------------------

    def print_summary(

        self,

        captions: List[Caption]

    ) -> None:

        stats = self.statistics(captions)

        print("\n========== Caption Summary ==========")

        for key, value in stats.items():

            print(f"{key}: {value}")

        print("=====================================\n")