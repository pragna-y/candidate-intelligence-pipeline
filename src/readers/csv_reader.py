"""
csv_reader.py

Reads recruiter CSV into Candidate objects.
"""

import csv

from src.models import Candidate
from src.utils import generate_candidate_id
from src.logger import logger


class CSVReader:

    def read(self, filepath):

        candidates = []

        logger.info(
            f"Reading CSV: {filepath}"
        )

        with open(
            filepath,
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                candidate = Candidate()

                candidate.candidate_id = generate_candidate_id()

                candidate.source = "Recruiter CSV"
                candidate.metadata["resume_file"] = row.get(
                      "resume_file"
                      )
                candidate.metadata["github_file"] = row.get(
                    "github_file"
                    )

                candidate.full_name = row.get(
                    "full_name"
                )

                email = row.get("email")

                if email:
                    candidate.emails.append(email)

                phone = row.get("phone")

                if phone:
                    candidate.phones.append(phone)

                skills = row.get(
                    "skills",
                    ""
                )

                for skill in skills.split(","):

                    skill = skill.strip()

                    if skill:

                        candidate.skills.append({

                            "name": skill,

                            "confidence": 1.0,

                            "sources": [
                                "Recruiter CSV"
                            ]

                        })

                candidate.provenance = {

                    "full_name": {
                        "source": "Recruiter CSV",
                        "method": "Direct"
                    },

                    "email": {
                        "source": "Recruiter CSV",
                        "method": "Direct"
                    },

                    "phone": {
                        "source": "Recruiter CSV",
                        "method": "Direct"
                    }

                }

                candidates.append(candidate)

        logger.info(
            f"{len(candidates)} candidates loaded."
        )

        return candidates