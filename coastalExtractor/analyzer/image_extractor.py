from __future__ import annotations

"""
Stage 2 Image Extractor

Extracts image locations from PDF pages.

This module only identifies images and their
positions. Image understanding is performed
during Stage 3.
"""

from dataclasses import dataclass
from typing import List, Optional

import fitz


@dataclass
class ExtractedImage:

    id: int

    page: int

    x0: float
    y0: float
    x1: float
    y1: float

    width: float
    height: float

    xref: int

    image_name: Optional[str] = None

    extension: Optional[str] = None

    confidence: float = 1.0


class ImageExtractor:

    """
    Extract images together with their locations.
    """

    def __init__(self, document: fitz.Document):

        self.document = document

    # --------------------------------------------------------

    def extract(self) -> List[ExtractedImage]:

        images = []

        image_id = 1

        for page_number, page in enumerate(self.document, start=1):

            image_list = page.get_images(full=True)

            for image in image_list:

                xref = image[0]

                try:

                    rects = page.get_image_rects(xref)

                except Exception:

                    rects = []

                if not rects:

                    continue

                for rect in rects:

                    images.append(

                        ExtractedImage(

                            id=image_id,

                            page=page_number,

                            x0=rect.x0,
                            y0=rect.y0,
                            x1=rect.x1,
                            y1=rect.y1,

                            width=rect.width,
                            height=rect.height,

                            xref=xref,

                            extension=self.__extension(
                                xref
                            )

                        )

                    )

                    image_id += 1

        return images

    # --------------------------------------------------------

    def __extension(
        self,
        xref: int
    ) -> Optional[str]:

        try:

            info = self.document.extract_image(xref)

            return info.get("ext")

        except Exception:

            return None

    # --------------------------------------------------------

    def large_images(
        self,
        images: List[ExtractedImage],
        minimum_area: float = 25000
    ) -> List[ExtractedImage]:

        result = []

        for image in images:

            if image.width * image.height >= minimum_area:

                result.append(image)

        return result

    # --------------------------------------------------------

    def images_on_page(
        self,
        images: List[ExtractedImage],
        page: int
    ) -> List[ExtractedImage]:

        return [

            image

            for image in images

            if image.page == page

        ]

    # --------------------------------------------------------

    def statistics(
        self,
        images: List[ExtractedImage]
    ) -> dict:

        if not images:

            return {

                "total_images": 0,

                "average_width": 0,

                "average_height": 0

            }

        avg_width = (

            sum(

                image.width

                for image in images

            ) / len(images)

        )

        avg_height = (

            sum(

                image.height

                for image in images

            ) / len(images)

        )

        return {

            "total_images": len(images),

            "average_width": avg_width,

            "average_height": avg_height

        }

    # --------------------------------------------------------

    def print_summary(
        self,
        images: List[ExtractedImage]
    ):

        stats = self.statistics(images)

        print()

        print("=" * 60)

        print("IMAGE EXTRACTION SUMMARY")

        print("=" * 60)

        print(

            f"Images : {stats['total_images']}"

        )

        print(

            f"Average Width : {stats['average_width']:.2f}"

        )

        print(

            f"Average Height : {stats['average_height']:.2f}"

        )

        print("=" * 60)