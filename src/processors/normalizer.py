"""
normalizer.py

Standardizes candidate information into a
consistent canonical format.
"""

import re

from src.models import Candidate
from src.utils import (
    unique_strings,
    merge_dict_list
)


class CandidateNormalizer:

    # -------------------------------------

    @staticmethod
    def normalize_name(name):

        if not name:
            return None

        return " ".join(

            word.capitalize()

            for word in name.strip().split()

        )

    # -------------------------------------

    @staticmethod
    def normalize_email(email):

        if not email:
            return None

        return email.strip().lower()

    # -------------------------------------

    @staticmethod
    def normalize_phone(phone):

        if not phone:
            return None

        digits = re.sub(r"\D", "", phone)

        if len(digits) == 10:

            return "+91" + digits

        if len(digits) == 12 and digits.startswith("91"):

            return "+" + digits

        return phone

    # -------------------------------------

    @staticmethod
    def normalize_skill(skill):

        aliases = {

            "python3": "Python",

            "python": "Python",

            "py": "Python",

            "js": "JavaScript",

            "node": "Node.js",

            "nodejs": "Node.js",

            "sql": "SQL",

            "mysql": "MySQL",

            "aws": "AWS"

        }

        name = skill["name"].lower()

        skill["name"] = aliases.get(
            name,
            skill["name"].title()
        )

        return skill

    # -------------------------------------

    @classmethod
    def normalize(cls, candidate: Candidate):

        candidate.full_name = cls.normalize_name(
            candidate.full_name
        )

        candidate.emails = unique_strings([

            cls.normalize_email(email)

            for email in candidate.emails

            if email

        ])

        candidate.phones = unique_strings([

            cls.normalize_phone(phone)

            for phone in candidate.phones

            if phone

        ])

        normalized = []

        for skill in candidate.skills:

            normalized.append(

                cls.normalize_skill(skill)

            )

        candidate.skills = merge_dict_list(

            normalized,

            "name"

        )

        return candidate