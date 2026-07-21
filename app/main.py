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
    missing_skills = []
    normalized_candidate_skills = []
    for candidate_skill in candidate_skills:
        normalized_candidate_skill = candidate_skill.strip().lower()
        if normalized_candidate_skill == "":
            continue
        else:
            normalized_candidate_skills.append(normalized_candidate_skill)
    
    added_skills = []
    for required_skill in required_skills:
        normalized_required_skill = required_skill.strip().lower()
        if normalized_required_skill == "":
            continue
        if (normalized_required_skill not in normalized_candidate_skills and normalized_required_skill not in added_skills):
            missing_skills.append(required_skill)
            added_skills.append(normalized_required_skill)
    
    return missing_skills

def calculate_match_rate(required_skills:list[str],candidate_skills:list[str]) -> float:
    """
    Calculate the match rate between required skills and candidate skills.  """
    #normalized_required_skills = set(skill.strip().lower() for skill in required_skills if skill.strip() != "")
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
    match_rate = 1 - missing_count / required_count
    return match_rate
    


        

    


    