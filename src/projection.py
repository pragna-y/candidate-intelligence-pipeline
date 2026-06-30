"""
projection.py

Projects Candidate into configurable JSON.
"""

from dataclasses import asdict

from src.utils import (

    read_json,

    safe_get

)


class ProjectionEngine:

    def __init__(self):

        config = read_json(

            "config/projection.json"

        )

        self.fields = config["fields"]

    def project(self, candidate):

        data = asdict(candidate)

        output = {}

        for field in self.fields:

            value = safe_get(

                data,

                field["path"]

            )

            if value is None:

                value = field.get(

                    "default"

                )

            output[

                field["output"]

            ] = value

        return output