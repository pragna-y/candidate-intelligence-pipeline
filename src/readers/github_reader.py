"""
github_reader.py

Reads GitHub profile JSON.
"""

from src.models import Candidate
from src.utils import (
    generate_candidate_id,
    read_json
)
from src.logger import logger


class GitHubReader:

    def read(self, filepath):

        logger.info(
            f"Reading GitHub: {filepath}"
        )

        data = read_json(filepath)

        if data is None:

            logger.error(
                "GitHub JSON not found."
            )

            return None

        candidate = Candidate()

        candidate.candidate_id = generate_candidate_id()

        candidate.source = "GitHub"

        candidate.full_name = data.get("name")

        candidate.headline = data.get("bio")

        location = data.get("location")

        if location:

            candidate.location["city"] = location

        candidate.links["github"] = data.get(
            "html_url"
        )

        language = data.get("language")

        if language:

            candidate.skills.append({

                "name": language,

                "confidence": 0.85,

                "sources": [
                    "GitHub"
                ]

            })

        candidate.provenance = {

            "full_name": {
                "source": "GitHub",
                "method": "Direct"
            },

            "headline": {
                "source": "GitHub",
                "method": "Direct"
            }

        }

        logger.info(
            "GitHub profile loaded."
        )

        return candidate