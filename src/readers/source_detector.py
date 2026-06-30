"""
source_detector.py

Automatically detects the correct reader
based on file extension.
"""

from pathlib import Path

from src.logger import logger

from src.readers.csv_reader import CSVReader
from src.readers.resume_reader import ResumeReader
from src.readers.github_reader import GitHubReader


class SourceDetector:

    def __init__(self):

        self.readers = {

            ".csv": CSVReader(),

            ".txt": ResumeReader(),

            ".json": GitHubReader()

        }

    # -----------------------------------------

    def detect(self, filepath):

        extension = Path(filepath).suffix.lower()

        reader = self.readers.get(extension)

        if reader is None:

            logger.error(
                f"No reader found for {extension}"
            )

            return None

        logger.info(
            f"Detected {extension} source."
        )

        return reader

    # -----------------------------------------

    def load(self, filepath):

        reader = self.detect(filepath)

        if reader is None:

            return None

        return reader.read(filepath)