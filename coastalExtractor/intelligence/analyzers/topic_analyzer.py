from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
from typing import List


@dataclass
class Topic:

    name: str

    score: float

    keywords: List[str] = field(default_factory=list)


class TopicAnalyzer:

    """
    Groups document keywords into semantic topics.
    """

    TOPICS = {

        "Navigation": [

            "navigation",

            "route",

            "voyage",

            "channel",

            "pilot"

        ],

        "Coastal Shipping": [

            "coastal",

            "shipping",

            "cargo",

            "vessel",

            "operator"

        ],

        "Safety": [

            "safety",

            "solas",

            "fire",

            "emergency",

            "life"

        ],

        "Security": [

            "security",

            "isps",

            "piracy",

            "inspection"

        ],

        "Ports": [

            "port",

            "berth",

            "terminal",

            "jetty",

            "harbour"

        ],

        "Environment": [

            "marpol",

            "pollution",

            "waste",

            "emission",

            "ballast"

        ],

        "Regulations": [

            "imo",

            "circular",

            "resolution",

            "regulation",

            "guideline"

        ]

    }

    def analyze(

        self,

        keywords

    ) -> List[Topic]:

        scores: Dict[str, float] = {}

        matches: Dict[str, List[str]] = {}

        for topic, vocabulary in self.TOPICS.items():

            score = 0

            matched = []

            for keyword in keywords:

                word = keyword.word.lower()

                if word in vocabulary:

                    score += keyword.frequency

                    matched.append(word)

            if score > 0:

                scores[topic] = score

                matches[topic] = matched

        if not scores:

            return []

        maximum = max(scores.values())

        topics = []

        for topic in scores:

            topics.append(

                Topic(

                    name=topic,

                    score=round(

                        scores[topic] / maximum,

                        3

                    ),

                    keywords=sorted(

                        set(

                            matches[topic]

                        )

                    )

                )

            )

        topics.sort(

            key=lambda x: x.score,

            reverse=True

        )

        return topics