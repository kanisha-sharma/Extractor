"""
Geometry utility functions used throughout the document extraction pipeline.

This module provides helper functions for:
- Bounding box calculations
- Distance measurements
- Intersection & overlap
- IoU calculations
- Block sorting
- Reading order helpers
"""

from __future__ import annotations

from math import sqrt
from typing import List, Tuple

BBox = Tuple[float, float, float, float]


# ==========================================================
# BASIC PROPERTIES
# ==========================================================

def width(box: BBox) -> float:
    return max(0.0, box[2] - box[0])


def height(box: BBox) -> float:
    return max(0.0, box[3] - box[1])


def area(box: BBox) -> float:
    return width(box) * height(box)


def center(box: BBox) -> Tuple[float, float]:
    return (
        (box[0] + box[2]) / 2,
        (box[1] + box[3]) / 2,
    )


# ==========================================================
# BOX RELATIONSHIPS
# ==========================================================

def intersects(a: BBox, b: BBox) -> bool:
    return not (
        a[2] <= b[0]
        or b[2] <= a[0]
        or a[3] <= b[1]
        or b[3] <= a[1]
    )


def contains(outer: BBox, inner: BBox) -> bool:
    return (
        outer[0] <= inner[0]
        and outer[1] <= inner[1]
        and outer[2] >= inner[2]
        and outer[3] >= inner[3]
    )


def intersection(a: BBox, b: BBox) -> BBox | None:

    if not intersects(a, b):
        return None

    return (
        max(a[0], b[0]),
        max(a[1], b[1]),
        min(a[2], b[2]),
        min(a[3], b[3]),
    )


def union(a: BBox, b: BBox) -> BBox:

    return (
        min(a[0], b[0]),
        min(a[1], b[1]),
        max(a[2], b[2]),
        max(a[3], b[3]),
    )


def merge_boxes(a: BBox, b: BBox) -> BBox:
    return union(a, b)


# ==========================================================
# OVERLAP
# ==========================================================

def overlap_area(a: BBox, b: BBox) -> float:

    inter = intersection(a, b)

    if inter is None:
        return 0.0

    return area(inter)


def overlap_ratio(a: BBox, b: BBox) -> float:

    oa = overlap_area(a, b)

    if oa == 0:
        return 0.0

    return oa / min(area(a), area(b))


def iou(a: BBox, b: BBox) -> float:

    inter = overlap_area(a, b)

    if inter == 0:
        return 0.0

    ua = area(a) + area(b) - inter

    if ua == 0:
        return 0.0

    return inter / ua


# ==========================================================
# DISTANCES
# ==========================================================

def horizontal_distance(a: BBox, b: BBox) -> float:

    if intersects(a, b):
        return 0.0

    if a[2] < b[0]:
        return b[0] - a[2]

    return a[0] - b[2]


def vertical_distance(a: BBox, b: BBox) -> float:

    if intersects(a, b):
        return 0.0

    if a[3] < b[1]:
        return b[1] - a[3]

    return a[1] - b[3]


def euclidean_distance(a: BBox, b: BBox) -> float:

    ax, ay = center(a)

    bx, by = center(b)

    return sqrt((ax - bx) ** 2 + (ay - by) ** 2)


# ==========================================================
# ALIGNMENT
# ==========================================================

def same_line(a: BBox, b: BBox, tolerance: float = 10) -> bool:

    ay = center(a)[1]

    by = center(b)[1]

    return abs(ay - by) <= tolerance


def same_column(a: BBox, b: BBox, tolerance: float = 25) -> bool:

    ax = center(a)[0]

    bx = center(b)[0]

    return abs(ax - bx) <= tolerance


# ==========================================================
# SORTING HELPERS
# ==========================================================

def sort_top_to_bottom(boxes: List[BBox]) -> List[BBox]:

    return sorted(boxes, key=lambda b: (b[1], b[0]))


def sort_left_to_right(boxes: List[BBox]) -> List[BBox]:

    return sorted(boxes, key=lambda b: (b[0], b[1]))


def reading_order_key(box: BBox):

    return (
        round(box[1] / 5),
        box[0],
    )


def sort_reading_order(boxes: List[BBox]) -> List[BBox]:

    return sorted(boxes, key=reading_order_key)


# ==========================================================
# MERGING
# ==========================================================

def should_merge(
    a: BBox,
    b: BBox,
    horizontal_gap: float = 20,
    vertical_gap: float = 8,
) -> bool:

    if same_line(a, b, vertical_gap):

        if horizontal_distance(a, b) <= horizontal_gap:

            return True

    return False


# ==========================================================
# PAGE HELPERS
# ==========================================================

def is_inside_page(box: BBox, page_width: float, page_height: float):

    return (
        box[0] >= 0
        and box[1] >= 0
        and box[2] <= page_width
        and box[3] <= page_height
    )


def normalize_bbox(
    box: BBox,
    page_width: float,
    page_height: float,
) -> Tuple[float, float, float, float]:

    return (
        box[0] / page_width,
        box[1] / page_height,
        box[2] / page_width,
        box[3] / page_height,
    )


def denormalize_bbox(
    box: BBox,
    page_width: float,
    page_height: float,
) -> BBox:

    return (
        box[0] * page_width,
        box[1] * page_height,
        box[2] * page_width,
        box[3] * page_height,
    )