from __future__ import annotations

import re

from collections import Counter
from dataclasses import dataclass
from typing import List


@dataclass
class Keyword:

    word: str

    frequency: int

    score: float


class KeywordExtractor:

    """
    Extracts important keywords from document text.
    """

    STOPWORDS = {

        "the",
        "a",
        "an",
        "of",
        "for",
        "to",
        "and",
        "or",
        "is",
        "are",
        "was",
        "were",
        "on",
        "in",
        "with",
        "by",
        "this",
        "that",
        "these",
        "those",
        "be",
        "as",
        "at",
        "it",
        "from",
        "into",
        "shall",
        "may",
        "can",
        "must",
        "not"

    }

    TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9\-]+")

    def extract(

        self,

        pages: List[List[str]],

        top_n: int = 50

    ) -> List[Keyword]:

        counter = Counter()

        total_words = 0

        for lines in pages:

            for line in lines:

                tokens = self.TOKEN.findall(line.lower())

                for token in tokens:

                    if len(token) < 3:

                        continue

                    if token in self.STOPWORDS:

                        continue

                    counter[token] += 1

                    total_words += 1

        results: List[Keyword] = []

        for word, freq in counter.most_common(top_n):

            score = freq / max(total_words, 1)

            results.append(

                Keyword(

                    word=word,

                    frequency=freq,

                    score=round(score, 5)

                )

            )

        return results

    def as_dictionary(

        self,

        keywords: List[Keyword]

    ):

        return {

            keyword.word: keyword.frequency

            for keyword in keywords

        }

    def top_words(

        self,

        pages: List[List[str]],

        n: int = 10

    ) -> List[str]:

        return [

            keyword.word

            for keyword in self.extract(

                pages,

                top_n=n

            )

        ]