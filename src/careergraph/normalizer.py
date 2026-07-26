from fastapi import logger
import logging

logger = logging.getLogger(__name__)
def normalize_skills(skills: list[str]) -> set[str]:
    """
    Normalize a list of skills by stripping whitespace and converting to lowercase.

    Args:
        skills (list[str]): A list of skills
    Returns:
        set[str]: A set of normalized skills.
    """
    if not isinstance(skills, list):
        raise ValueError(
            "Skills must be provided as a list."
        )
    normalize_skills = set()



    for skill in skills:
        if not isinstance(skill, str):
            raise ValueError(
                "Each skill must be a string."
            )
        normalize_skill = skill.strip().lower()
        if normalize_skill != "":
            normalize_skills.add(normalize_skill)

    logger.debug("Normalized %s skills in to %s unique skills.", len(skills), len(normalize_skills))
    return normalize_skills