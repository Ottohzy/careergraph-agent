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