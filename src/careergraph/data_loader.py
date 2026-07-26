import logging
import json
from pathlib import Path
from typing import Any

from fastapi import logger

from careergraph.normalizer import normalize_skills

logger = logging.getLogger(__name__)



def load_candidate_profile(
    file_path: str | Path,
) -> dict[str, Any]:
    path = Path(file_path)

    logger.info(f"Loading candidate profile from %s", path)

    try:
        with path.open("r", encoding="utf-8") as file:
            profile = json.load(file)

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from %s: %s", path, e)
        raise ValueError("Invalid JSON format in candidate profile.")

    except FileNotFoundError:
        logger.error(f"File not found: %s", path)
        raise

    if not isinstance(profile, dict):
        logger.error("Candidate profile must be a dictionary: %s", path,)
        raise ValueError(
            "Candidate profile must be a JSON object."
        )

    logger.info(f"Candidate profile loaded successfully from %s", path)

    return profile


def get_candidate_skills(
    candidate_profile: dict[str, Any],
) -> set[str]:
    skills = candidate_profile.get("skills", [])

    if not isinstance(skills, list):
        logger.error("Candidate skills must be a list, received: %s", type(skills).__name__)
        raise ValueError(
            "Candidate skills must be a list."
        )

    normalized_skills = normalize_skills(skills)

    logger.info("Loaded %s candidate skills.", len(normalized_skills))

    return normalized_skills


def load_jd_text(
    file_path: str | Path,
) -> str:
    path = Path(file_path)

    logger.info(f"Loading job description from %s", path)

    try:
        jd_text = path.read_text(
            encoding="utf-8"
        ).strip()
    except FileNotFoundError:
        logger.error(f"File not found: %s", path)
        raise

    if not jd_text:
        logger.error(f"Job description from %s is empty.", path)
        raise ValueError(
            "Job description cannot be empty."
        )

    logger.info(f"Job description loaded successfully from %s", path)

    return jd_text
            