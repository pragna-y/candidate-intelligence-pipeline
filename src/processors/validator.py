"""
validator.py

Validates the merged candidate profile.
"""

import re


EMAIL_PATTERN = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


class CandidateValidator:

    MIN_CONFIDENCE = 0.70

    def validate(self, candidate):

        errors = []
        warnings = []

        # -----------------------------
        # Required Fields
        # -----------------------------
        if not candidate.full_name:
            errors.append("Missing full name.")

        if not candidate.emails:
            warnings.append("Email not available.")

        if not candidate.phones:
            warnings.append("Phone not available.")

        # -----------------------------
        # Email Validation
        # -----------------------------
        for email in candidate.emails:

            if not re.match(
                EMAIL_PATTERN,
                email
            ):
                errors.append(
                    f"Invalid email: {email}"
                )

        # -----------------------------
        # Duplicate Skills
        # -----------------------------
        names = [

            skill["name"].lower()

            for skill in candidate.skills

        ]

        if len(names) != len(set(names)):
            warnings.append(
                "Duplicate skills detected."
            )

        # -----------------------------
        # Confidence
        # -----------------------------
        if (
            candidate.overall_confidence
            <
            self.MIN_CONFIDENCE
        ):
            warnings.append(
                "Overall confidence is low."
            )

        return {

            "valid": len(errors) == 0,

            "errors": errors,

            "warnings": warnings

        }