"""
quality_report.py

Creates a human-readable data quality report.
"""

from datetime import datetime


class QualityReport:

    def generate(

        self,

        candidate,

        validation

    ):

        report = []

        report.append("=" * 60)
        report.append("Candidate Transformation Report")
        report.append("=" * 60)

        report.append(
            f"Generated : {datetime.now()}"
        )

        report.append("")

        report.append(
            f"Candidate : {candidate.full_name}"
        )

        report.append(
            f"Confidence : {candidate.overall_confidence:.2f}"
        )

        report.append("")

        report.append("Sources Used")

        report.append("-" * 60)

        for field, history in candidate.provenance.items():

            report.append(

                f"{field:<15}"

                f"{', '.join([

                    h['source']

                    for h in history

                ])}"

            )

        report.append("")

        report.append("Warnings")

        report.append("-" * 60)

        if validation["warnings"]:

            report.extend(

                validation["warnings"]

            )

        else:

            report.append("None")

        report.append("")

        report.append("Errors")

        report.append("-" * 60)

        if validation["errors"]:

            report.extend(

                validation["errors"]

            )

        else:

            report.append("None")

        report.append("")

        report.append(

            "Validation : "

            +

            (

                "PASSED"

                if validation["valid"]

                else "FAILED"

            )

        )

        return "\n".join(report)