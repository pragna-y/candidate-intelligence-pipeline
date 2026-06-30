"""
confidence.py

Confidence Scoring Engine.
"""


class ConfidenceEngine:

    SOURCE_WEIGHT = {

        "Recruiter CSV": 1.00,

        "Resume": 0.90,

        "GitHub": 0.80

    }

    def calculate(self, candidate):

        confidence = {}

        for field, history in candidate.provenance.items():

            sources = [

                item["source"]

                for item in history

            ]

            base = max(

                self.SOURCE_WEIGHT.get(

                    source,

                    0.50

                )

                for source in sources

            )

            # Bonus if multiple sources agree

            if len(set(sources)) > 1:

                base += 0.05

            confidence[field] = round(

                min(base, 1.0),

                2

            )

        candidate.confidence = confidence

        if confidence:

            candidate.overall_confidence = round(

                sum(confidence.values())

                /

                len(confidence),

                2

            )

        return candidate