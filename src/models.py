"""
models.py

Canonical candidate model used throughout the project.
"""

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Candidate:
    """
    Canonical representation of a candidate.
    """

    candidate_id: str | None = None

    source: str | None = None

    full_name: str | None = None

    emails: list[str] = field(default_factory=list)

    phones: list[str] = field(default_factory=list)

    headline: str | None = None

    location: dict[str, Any] = field(default_factory=lambda: {
        "city": None,
        "region": None,
        "country": None
    })

    links: dict[str, Any] = field(default_factory=lambda: {
        "github": None,
        "linkedin": None,
        "portfolio": None
    })

    skills: list[dict] = field(default_factory=list)

    education: list[dict] = field(default_factory=list)

    experience: list[dict] = field(default_factory=list)

    projects: list[dict] = field(default_factory=list)

    provenance: dict = field(default_factory=dict)

    decision_trace: list[dict] = field(default_factory=list)

    confidence: dict = field(default_factory=dict)

    overall_confidence: float = 0.0

    warnings: list[str] = field(default_factory=list)

    metadata: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)