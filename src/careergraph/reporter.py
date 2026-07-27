def format_skills(skills: set[str]) -> str:
    """
    Convert a skill set into a readable string.

    Return "None" when the skill set is empty.
    """
    if not skills:
        return "None"

    return ", ".join(sorted(skills))


def format_analysis_report(
    candidate_name: str,
    required_skills: set[str],
    candidate_skills: set[str],
    matched_skills: set[str],
    missing_skills: set[str],
    match_rate: float,
) -> str:
    """
    Format the CareerGraph analysis result
    as a readable text report.
    """
    lines = [
        "===== CareerGraph Analysis =====",
        f"Candidate: {candidate_name}",
        (
            "Required skills: "
            f"{format_skills(required_skills)}"
        ),
        (
            "Candidate skills: "
            f"{format_skills(candidate_skills)}"
        ),
        (
            "Matched skills: "
            f"{format_skills(matched_skills)}"
        ),
        (
            "Missing skills: "
            f"{format_skills(missing_skills)}"
        ),
        f"Match rate: {match_rate:.1%}",
    ]

    return "\n".join(lines)