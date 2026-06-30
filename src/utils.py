"""
utils.py

Common utility functions used throughout the project.
"""

import json
import uuid
from pathlib import Path


# ----------------------------------------------------
# File Utilities
# ----------------------------------------------------

def read_json(filepath):
    """
    Read a JSON file.
    """

    path = Path(filepath)

    if not path.exists():
        return None

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(filepath, data):
    """
    Write data to JSON.
    """

    path = Path(filepath)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def read_text(filepath):
    """
    Read text file.
    """

    path = Path(filepath)

    if not path.exists():
        return ""

    return path.read_text(
        encoding="utf-8",
        errors="ignore"
    )


# ----------------------------------------------------
# Candidate Utilities
# ----------------------------------------------------

def generate_candidate_id():
    """
    Generate unique candidate ID.
    """

    return f"CAND-{uuid.uuid4().hex[:8].upper()}"


# ----------------------------------------------------
# List Utilities
# ----------------------------------------------------

def unique_strings(values):
    """
    Remove duplicate strings.
    """

    seen = set()

    result = []

    for value in values:

        if not value:
            continue

        value = value.strip()

        if value.lower() not in seen:

            seen.add(value.lower())

            result.append(value)

    return result


def merge_string_lists(list1, list2):
    """
    Merge two string lists.
    """

    return unique_strings(list1 + list2)


def merge_dict_list(items, key):

    merged = {}

    for item in items:

        value = item.get(key)

        if not value:
            continue

        lookup = value.strip().lower()

        if lookup not in merged:

            merged[lookup] = item

        else:

            if item.get("confidence", 0) > merged[lookup].get("confidence", 0):

                merged[lookup] = item

    return list(merged.values())

# ----------------------------------------------------
# Nested Dictionary Utility
# ----------------------------------------------------

def safe_get(data, path, default=None):
    """
    Read nested dictionary using dot notation.

    Example:

    safe_get(candidate,"links.github")
    """

    current = data

    for part in path.split("."):

        if isinstance(current, dict):

            current = current.get(part)

        elif isinstance(current, list):

            try:

                current = current[int(part)]

            except:

                return default

        else:

            return default

        if current is None:
            return default

    return current
