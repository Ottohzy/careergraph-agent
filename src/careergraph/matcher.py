import logging

logger = logging.getLogger(__name__)

def match_skills(required_skills: set[str], candidate_skills: set[str]) -> tuple[set[str], set[str]]:
    """
    Match the required skills with the candidate's skills.

    Args:
        required_skills (set[str]): A set of required skills.
        candidate_skills (set[str]): A set of candidate skills.

    Returns:
        tuple[set[str], set[str]]: A tuple containing two sets:
            - matched_skills: The skills that are both required and present in the candidate's skills.
            - missing_skills: The skills that are required but not present in the candidate's skills.
    """
    if not isinstance(required_skills, set):
        raise ValueError(
            "Required skills must be provided as a set."
        )
    if not isinstance(candidate_skills, set):
        raise ValueError(
            "Candidate skills must be provided as a set."
        )
    matched_skills = required_skills & candidate_skills  # Intersection of required and candidate skills
    missing_skills = required_skills - candidate_skills  # Skills that are required but not present in candidate's skills

    logger.debug("Matched %s skills and found %s missing skills.", len(matched_skills), len(missing_skills))
    return matched_skills, missing_skills
