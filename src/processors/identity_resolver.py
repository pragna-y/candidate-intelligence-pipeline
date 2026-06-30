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
    def score(

        cls,

        candidate1,

        candidate2

    ):

        score = 0

        if (

            candidate1.emails

            and

            candidate2.emails

        ):

            if (

                candidate1.emails[0]

                ==

                candidate2.emails[0]

            ):

                score += cls.EMAIL_WEIGHT

        if (

            candidate1.phones

            and

            candidate2.phones

        ):

            if (

                candidate1.phones[0]

                ==

                candidate2.phones[0]

            ):

                score += cls.PHONE_WEIGHT

        score += (

            cls.similarity(

                candidate1.full_name,

                candidate2.full_name

            )

            *

            cls.NAME_WEIGHT

        )

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