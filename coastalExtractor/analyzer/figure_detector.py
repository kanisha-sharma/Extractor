from __future__ import annotations

"""
Stage 2 Figure Detector

Associates extracted images with nearby captions to create
logical figures.

Example:

    Figure 2 : Coastal Shipping Route

        [ Image ]

becomes one Figure object.
"""

from dataclasses import dataclass
from typing import List, Optional

from coastalExtractor.analyzer.image_extractor import (
    ExtractedImage
)


@dataclass
class Figure:

    id: int

    page: int

    title: Optional[str]

    image: ExtractedImage

    confidence: float = 1.0


class FigureDetector:

    """
    Detects figures from extracted images.

    Caption association will be improved once
    caption_extractor.py is integrated.
    """

    def detect(
        self,
        images: List[ExtractedImage],
        captions=None
    ) -> List[Figure]:

        figures = []

        figure_id = 1

        for image in images:

            caption = self.__find_caption(
                image,
                captions
            )

            figures.append(

                Figure(

                    id=figure_id,

                    page=image.page,

                    title=caption,

                    image=image,

                    confidence=self.__confidence(
                        image,
                        caption
                    )

                )

            )

            figure_id += 1

        return figures

    # --------------------------------------------------

    def __find_caption(

        self,

        image: ExtractedImage,

        captions

    ) -> Optional[str]:

        if not captions:

            return None

        candidates = [

            caption

            for caption in captions

            if caption.page == image.page

        ]

        if not candidates:

            return None

        nearest = None

        distance = float("inf")

        for caption in candidates:

            if not hasattr(caption, "bbox"):

                continue

            d = abs(

                caption.bbox.y1 -

                image.y1

            )

            if d < distance:

                distance = d

                nearest = caption

        if nearest:

            return nearest.text

        return None

    # --------------------------------------------------

    def __confidence(

        self,

        image: ExtractedImage,

        caption

    ) -> float:

        score = 0.70

        if caption:

            score += 0.20

        if image.width > 150:

            score += 0.05

        if image.height > 150:

            score += 0.05

        return min(score, 1.0)

    # --------------------------------------------------

    def figures_on_page(

        self,

        figures: List[Figure],

        page: int

    ) -> List[Figure]:

        return [

            figure

            for figure in figures

            if figure.page == page

        ]

    # --------------------------------------------------

    def statistics(

        self,

        figures: List[Figure]

    ) -> dict:

        titled = len(

            [

                figure

                for figure in figures

                if figure.title

            ]

        )

        untitled = len(figures) - titled

        return {

            "total_figures": len(figures),

            "titled_figures": titled,

            "untitled_figures": untitled

        }

    # --------------------------------------------------

    def print_summary(

        self,

        figures: List[Figure]

    ):

        stats = self.statistics(figures)

        print()

        print("=" * 60)

        print("FIGURE DETECTOR SUMMARY")

        print("=" * 60)

        print(

            f"Figures          : {stats['total_figures']}"

        )

        print(

            f"With Caption     : {stats['titled_figures']}"

        )

        print(

            f"No Caption       : {stats['untitled_figures']}"

        )

        print("=" * 60)