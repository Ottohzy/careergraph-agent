from careergraph.normalizer import normalize_skills
from careergraph.scorer import calculate_required_rate
from careergraph.matcher import match_skills

def analyze_skills(required_skills: list[str], candidate_skills: list[str]) -> dict:
    """
    Analyze the skills of a candidate against the required skills.

    Args:
        required_skills (list[str]): A list of required skills.
        candidate_skills (list[str]): A list of candidate skills.

    Returns:
        dict: A dictionary containing matched skills, missing skills, and match rate.
    """
    normalized_required_skills = normalize_skills(required_skills)
    normalized_candidate_skills = normalize_skills(candidate_skills)

    matched, missing = match_skills(normalized_required_skills, normalized_candidate_skills)
    match_rate = calculate_required_rate(matched, normalized_required_skills)

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "match_rate": match_rate
    }

results = analyze_skills(
    required_skills=["Python", "Data Analysis", "Machine Learning"],
    candidate_skills=["python", "data analysis", "communication"]
)

print(results)
