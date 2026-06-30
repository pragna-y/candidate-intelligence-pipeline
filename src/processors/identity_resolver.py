"""
identity_resolver.py

Checks whether multiple records
belong to the same candidate.
"""

from difflib import SequenceMatcher


class IdentityResolver:

    EMAIL_WEIGHT = 0.50

    PHONE_WEIGHT = 0.30

    NAME_WEIGHT = 0.20

    THRESHOLD = 0.70

    # ---------------------------------

    @staticmethod
    def similarity(a, b):

        if not a or not b:

            return 0

        return SequenceMatcher(

            None,

            a.lower(),

            b.lower()

        ).ratio()

    # ---------------------------------

    @classmethod
    def score(cls, candidate1, candidate2):
        score = 0.0

        # Email
        if candidate1.emails and candidate2.emails:
         if candidate1.emails[0].lower() == candidate2.emails[0].lower():
            score += cls.EMAIL_WEIGHT

        # Phone
        if candidate1.phones and candidate2.phones:
         if candidate1.phones[0] == candidate2.phones[0]:
            score += cls.PHONE_WEIGHT

        # Name
        name_similarity = cls.similarity(
        candidate1.full_name,
        candidate2.full_name
    )

        score += name_similarity * cls.NAME_WEIGHT

    # GitHub profiles usually don't expose email/phone.
    # If names are almost identical and one record has a GitHub link,
    # allow the match.

        if (
         name_similarity >= 0.95
         and (
            candidate1.links.get("github")
            or candidate2.links.get("github")
         )
    ):
         score = max(score, cls.THRESHOLD)

        return round(score, 2)

    # ---------------------------------

    @classmethod
    def is_same(

        cls,

        candidate1,

        candidate2

    ):

        return (

            cls.score(

                candidate1,

                candidate2

            )

            >=

            cls.THRESHOLD

        )
