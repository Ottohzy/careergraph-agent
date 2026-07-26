import logging

logger = logging.getLogger(__name__)
def calculate_match_rate(matched_skills: set[str], required_skills: set[str]) -> float:
    """
    Calculate the match rate based on matched skills and required skills.

    Args:
        matched_skills (set[str]): A set of matched skills.
        required_skills (set[str]): A set of required skills.

    Returns:
        float: The match rate as a float value.
    """
    if len(required_skills) == 0:
        logger.warning("Required skills set is empty. Returning 0.0 to avoid division by zero.")
        return 0.0  # Avoid division by zero if there are no required skills

    matched_count = len(matched_skills)
    required_count = len(required_skills)
    

    return matched_count / required_count