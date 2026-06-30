"""
extractor.py

Extracts structured candidate data
from raw resume text.
"""

import re

from src.models import Candidate
from src.utils import generate_candidate_id


EMAIL_REGEX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_REGEX = r"(?:\+91[- ]?)?[6-9]\d{9}"

GITHUB_REGEX = r"https?://github\.com/[A-Za-z0-9_-]+"

LINKEDIN_REGEX = r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+"


KNOWN_SKILLS = [

    "Python",
    "Java",
    "SQL",
    "Docker",
    "AWS",
    "Git",
    "Linux",
    "React",
    "Node.js",
    "MongoDB",
    "MySQL"

]


class ResumeExtractor:

    def __init__(self, text):

        self.text = text

    # ---------------------------------

    def extract_name(self):

        for line in self.text.splitlines():

            line = line.strip()

            if line:

                return line

        return None

    # ---------------------------------

    def extract_email(self):

        match = re.search(
            EMAIL_REGEX,
            self.text
        )

        return match.group() if match else None

    # ---------------------------------

    def extract_phone(self):

        match = re.search(
            PHONE_REGEX,
            self.text
        )

        return match.group() if match else None

    # ---------------------------------

    def extract_skills(self):

        skills = []

        text = self.text.lower()

        for skill in KNOWN_SKILLS:

            if skill.lower() in text:

                skills.append({

                    "name": skill,

                    "confidence": 0.95,

                    "sources": [
                        "Resume"
                    ]

                })

        return skills

    # ---------------------------------

    def build_candidate(self):

        candidate = Candidate()

        candidate.candidate_id = generate_candidate_id()

        candidate.source = "Resume"

        candidate.full_name = self.extract_name()

        email = self.extract_email()

        if email:
            candidate.emails.append(email)

        phone = self.extract_phone()

        if phone:
            candidate.phones.append(phone)

        github = re.search(
            GITHUB_REGEX,
            self.text
        )

        if github:

            candidate.links["github"] = github.group()

        linkedin = re.search(
            LINKEDIN_REGEX,
            self.text
        )

        if linkedin:

            candidate.links["linkedin"] = linkedin.group()

        candidate.skills = self.extract_skills()

        candidate.provenance = {

            "full_name": {
                "source": "Resume",
                "method": "Text Extraction"
            },

            "email": {
                "source": "Resume",
                "method": "Regex"
            },

            "phone": {
                "source": "Resume",
                "method": "Regex"
            }

        }

        return candidate