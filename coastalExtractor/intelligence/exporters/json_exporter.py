from __future__ import annotations

import json
import os

from dataclasses import asdict

from coastalExtractor.models.document_intelligence import (
    DocumentIntelligence
)


class JsonExporter:

    """
    Exports Document Intelligence into JSON.
    """

    def export(

        self,

        intelligence: DocumentIntelligence,

        output_path: str

    ) -> str:

        os.makedirs(

            os.path.dirname(output_path),

            exist_ok=True

        )

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                asdict(intelligence),

                f,

                indent=4,

                ensure_ascii=False

            )

        return output_path

    def export_string(

        self,

        intelligence: DocumentIntelligence

    ) -> str:

        return json.dumps(

            asdict(intelligence),

            indent=4,

            ensure_ascii=False

        )