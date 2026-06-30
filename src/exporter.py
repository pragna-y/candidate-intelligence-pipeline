"""
exporter.py

Exports all pipeline outputs.
"""

import json
from pathlib import Path


class Exporter:

    def __init__(self):

        self.output = Path("output")

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

    # -----------------------------------------
    # Export Final Candidate List
    # -----------------------------------------

    def export_candidates(self, candidates):

        with open(
            self.output / "all_candidates.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                candidates,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------------------
    # Export Decision Trace
    # -----------------------------------------

    def export_decision_trace(self, traces):

        with open(
            self.output / "decision_trace.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                traces,
                file,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------------------------
    # Export Quality Report
    # -----------------------------------------

    def export_quality_report(self, report):

        with open(
            self.output / "quality_report.txt",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(report)

    # -----------------------------------------
    # Export Pipeline Summary
    # -----------------------------------------

    def export_pipeline_summary(self, candidates, validations):

        summary = {
            "total_candidates": len(candidates),
            "processed_successfully": sum(
                1 for v in validations if v["valid"]
            ),
            "failed": sum(
                1 for v in validations if not v["valid"]
            ),
            "candidates": []
        }

        for candidate, validation in zip(candidates, validations):

            summary["candidates"].append({

                "candidate_id": candidate["candidate_id"],

                "name": candidate["name"],

                "confidence": candidate["confidence"],

                "status": (
                    "PASSED"
                    if validation["valid"]
                    else "FAILED"
                )

            })

        with open(
            self.output / "pipeline_summary.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False
            )