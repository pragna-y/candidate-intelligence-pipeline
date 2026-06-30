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

        # -----------------------------
        # Basic Information
        # -----------------------------

        candidate.full_name = (
            data.get("name")
            or data.get("full_name")
        )

        candidate.headline = data.get("bio")

        location = data.get("location")

        if location:
            candidate.location["city"] = location

        candidate.links["github"] = data.get(
            "html_url"
        )

        # -----------------------------
        # Skills from skills[]
        # -----------------------------

        skills = data.get("skills", [])

        for skill in skills:

            candidate.skills.append({

                "name": skill,

                "confidence": 0.90,

                "sources": [
                    "GitHub"
                ]

            })

        # -----------------------------
        # Primary Language
        # -----------------------------

        language = data.get("language")

        if language:

            already_exists = any(
                s["name"].lower() == language.lower()
                for s in candidate.skills
            )

            if not already_exists:

                candidate.skills.append({

                    "name": language,

                    "confidence": 0.85,

                    "sources": [
                        "GitHub"
                    ]

                })

        # -----------------------------
        # Email (if available)
        # -----------------------------

        email = data.get("email")

        if email:
            candidate.emails.append(email)

        # -----------------------------
        # Provenance
        # -----------------------------

        candidate.provenance = {

            "full_name": {
                "source": "GitHub",
                "method": "Direct"
            },

            "headline": {
                "source": "GitHub",
                "method": "Direct"
            },

           "skills": [
        {
            "source": "GitHub",
            "method": "Profile"
        }
    ]

        }

        logger.info(
            "GitHub profile loaded."
        )

        return candidate
