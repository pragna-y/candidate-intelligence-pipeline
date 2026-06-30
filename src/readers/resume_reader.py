"""
resume_reader.py

Reads raw resume text from a .txt file.
"""

from pathlib import Path

from src.logger import logger


class ResumeReader:

    def read(self, filepath):

        path = Path(filepath)

        logger.info(f"Reading Resume: {filepath}")

        if not path.exists():

            logger.error("Resume file not found.")

            return ""

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        logger.info("Resume loaded successfully.")

        return text