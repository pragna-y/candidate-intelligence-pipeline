"""
logger.py

Central logging utility for the Candidate Transformer.
"""

import logging
from pathlib import Path


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "candidate_transformer.log"


def get_logger():

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    logger = logging.getLogger(
        "CandidateTransformer"
    )

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "[%(asctime)s] %(levelname)s : %(message)s",

        "%Y-%m-%d %H:%M:%S"

    )

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.addHandler(file_handler)

    return logger


logger = get_logger()