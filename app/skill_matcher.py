def count_skills(skills: list[str]) -> dict[str, int]:
    """
    Count the occurrences of each skill in the provided list.

    Args:
        skills (list[str]): A list of skills

    Returns:
        dict[str, int]: A dictionary mapping each skill to its count.
    """
    result = {}

    for skill in skills:
        normalized_skill = skill.strip().lower()  # Normalize skill by stripping whitespace and converting to lowercase
        if normalized_skill == "":
            continue  # Skip empty skills

        if normalized_skill in result:
            result[normalized_skill] += 1

        else:
            result[normalized_skill] = 1

    return result


def find_missing_skills(required_skills : list[str], candidate_skills: list[str]) -> list[str]:
    """
    Find the skills that are required but missing from the candidate's skills."""
    normalized_required_skills = normalize_skills(required_skills)
    normalized_candidate_skills = normalize_skills(candidate_skills)
    missing_skills = normalized_required_skills - normalized_candidate_skills  # Set difference to find missing skills
    return sorted(missing_skills)  # Return the missing skills as a sorted list

def calculate_match_rate(required_skills:list[str],candidate_skills:list[str]) -> float:
    """
    Calculate the match rate between required skills and candidate skills.  """
    normalized_required_skills = set()
    for skill in required_skills:
        normalized_skill = skill.strip().lower()
        if normalized_skill != "":
            normalized_required_skills.add(normalized_skill)

    if len(normalized_required_skills) == 0:
        return 0.0  # Avoid division by zero if there are no required skills

    missing_skills = find_missing_skills(required_skills, candidate_skills)
    missing_count = len(missing_skills)
    required_count = len(normalized_required_skills)
    matched_count = required_count - missing_count
    return matched_count / required_count
    
def normalize_skills(skills: list[str]) -> set[str]:
    """
    Normalize a list of skills by stripping whitespace and converting to lowercase.

    Args:
        skills (list[str]): A list of skills
    Returns:
        set[str]: A set of normalized skills.
    """
    normalize_skills = set()

    for skill in skills:
        normalize_skill = skill.strip().lower()
        if normalize_skill != "":
            normalize_skills.add(normalize_skill)
    return normalize_skills

def find_matched_skills(required_skills: list[str], candidate_skills: list[str]) -> list[str]:
    """
    Find the skills that are required and present in the candidate's skills.

    Args:
        required_skills (list[str]): A list of required skills.
        candidate_skills (list[str]): A list of candidate skills.

    Returns:
        list[str]: A list of matched skills.
    """
    normalized_required_skills = normalize_skills(required_skills)
    normalized_candidate_skills = normalize_skills(candidate_skills)

    matched_skills = normalized_required_skills & normalized_candidate_skills  # Intersection of required and candidate skills
    return sorted(matched_skills)  






    