"""
merger.py

Merge multiple Candidate objects into one
canonical candidate.
"""

from copy import deepcopy

from src.models import Candidate
from src.utils import (
    merge_string_lists,
    merge_dict_list,
    read_json
)


class CandidateMerger:

    def __init__(self):

        config = read_json("config/merge_rules.json")

        self.priority = config.get(
            "priority",
            [
                "Recruiter CSV",
                "Resume",
                "GitHub"
            ]
        )

    def priority_score(self, source):

        try:
            return self.priority.index(source)
        except ValueError:
            return len(self.priority)

    def merge(self, candidates):

        merged = Candidate()

        source_map = {}

        for candidate in sorted(
            candidates,
            key=lambda c: self.priority_score(c.source)
        ):

            if not merged.candidate_id:
                merged.candidate_id = candidate.candidate_id

            if not merged.full_name and candidate.full_name:

                merged.full_name = candidate.full_name

                source_map["full_name"] = candidate.source

            if not merged.headline and candidate.headline:

                merged.headline = candidate.headline

                source_map["headline"] = candidate.source

            merged.emails = merge_string_lists(
                merged.emails,
                candidate.emails
            )

            merged.phones = merge_string_lists(
                merged.phones,
                candidate.phones
            )

            merged.skills = merge_dict_list(
                merged.skills + deepcopy(candidate.skills),
                "name"
            )

            merged.education = merge_dict_list(
                merged.education + deepcopy(candidate.education),
                "institution"
            )

            merged.experience.extend(
                deepcopy(candidate.experience)
            )

            merged.projects.extend(
                deepcopy(candidate.projects)
            )

            for key, value in candidate.links.items():

                if value and not merged.links.get(key):

                    merged.links[key] = value

            # Store ALL provenance
            for field, info in candidate.provenance.items():

                if field not in merged.provenance:

                    merged.provenance[field] = []

                merged.provenance[field].append(info)

        # Decision Trace
        for field, history in merged.provenance.items():

            merged.decision_trace.append({

                "field": field,

                "selected_source": history[0]["source"],

                "candidate_sources": [

                    h["source"]

                    for h in history

                ],

                "reason": "Highest priority source selected"

            })

        return merged