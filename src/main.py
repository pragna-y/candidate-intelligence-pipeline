"""
main.py

Multi Candidate Candidate Transformer
"""

from pathlib import Path

from src.logger import logger

from src.readers.csv_reader import CSVReader
from src.readers.resume_reader import ResumeReader
from src.readers.github_reader import GitHubReader

from src.processors.extractor import ResumeExtractor
from src.processors.normalizer import CandidateNormalizer
from src.processors.identity_resolver import IdentityResolver
from src.processors.merger import CandidateMerger
from src.processors.confidence import ConfidenceEngine
from src.processors.validator import CandidateValidator
from src.processors.quality_report import QualityReport

from src.projection import ProjectionEngine
from src.exporter import Exporter


def process_candidate(csv_candidate):

    logger.info(f"Processing {csv_candidate.full_name}")

    resume_path = Path(
        "input/resumes",
        csv_candidate.metadata["resume_file"]
    )

    github_path = Path(
        "input/github",
        csv_candidate.metadata["github_file"]
    )

    resume_text = ResumeReader().read(resume_path)

    resume_candidate = ResumeExtractor(
        resume_text
    ).build_candidate()

    github_candidate = GitHubReader().read(
        github_path
    )

    csv_candidate = CandidateNormalizer.normalize(csv_candidate)
    resume_candidate = CandidateNormalizer.normalize(resume_candidate)
    github_candidate = CandidateNormalizer.normalize(github_candidate)

    candidates = [csv_candidate]

    if IdentityResolver.is_same(csv_candidate, resume_candidate):
        candidates.append(resume_candidate)

    if github_candidate and IdentityResolver.is_same(csv_candidate, github_candidate):
        candidates.append(github_candidate)

    merged = CandidateMerger().merge(candidates)

    merged = ConfidenceEngine().calculate(merged)

    validation = CandidateValidator().validate(merged)

    projected = ProjectionEngine().project(merged)

    report = QualityReport().generate(
        merged,
        validation
    )

    return (
        projected,
        merged.decision_trace,
        report,
        validation
    )


def main():

    logger.info("Pipeline Started")

    csv_candidates = CSVReader().read(
        "input/recruiter.csv"
    )

    exporter = Exporter()

    projected_candidates = []
    all_traces = []
    reports = []
    validations = []

    for csv_candidate in csv_candidates:

        projected, trace, report, validation = process_candidate(
            csv_candidate
        )

        projected_candidates.append(projected)

        all_traces.extend(trace)

        reports.append(report)

        validations.append(validation)

    exporter.export_candidates(projected_candidates)

    exporter.export_decision_trace(all_traces)

    exporter.export_quality_report(
        "\n\n".join(reports)
    )

    exporter.export_pipeline_summary(
        projected_candidates,
        validations
    )

    logger.info(
        f"{len(projected_candidates)} candidates processed."
    )

    logger.info("Pipeline Completed Successfully")


if __name__ == "__main__":
    main()