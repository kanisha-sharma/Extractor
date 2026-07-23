from dataclasses import dataclass


@dataclass
class Heading:

    text: str

    page: int

    level: int

    confidence: float

    font_size: float

    is_bold: bool

    is_centered: bool

    x0: float = 0
    y0: float = 0
    x1: float = 0
    y1: float = 0