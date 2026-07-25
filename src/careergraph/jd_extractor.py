from careergraph.models import JobSkill


PREFERRED_MARKERS = {
    "preferred",
    "nice to have",
    "a plus",
    "bonus",
    "优先",
    "加分项",
    "最好具备",
}


def is_preferred_line(line: str) -> bool:
    normalized_line = line.lower()

    return any(
        marker in normalized_line
        for marker in PREFERRED_MARKERS
    )


def find_skills_in_line(
    line: str,
    aliases: dict[str, str],
) -> set[str]:
    normalized_line = line.lower()
    matched_skills = set()

    for alias, canonical_name in aliases.items():
        if alias.lower() in normalized_line:
            matched_skills.add(canonical_name)

    return matched_skills


def extract_skills(
    jd_text: str,
    aliases: dict[str, str],
) -> list[JobSkill]:
    skill_status: dict[str, bool] = {}

    for line in jd_text.splitlines():
        if not line.strip():
            continue

        required = not is_preferred_line(line)
        matched_skills = find_skills_in_line(line, aliases)

        for skill_name in matched_skills:
            if skill_name not in skill_status:
                skill_status[skill_name] = required
            elif required:
                skill_status[skill_name] = True

    return [
        JobSkill(name=name, required=required)
        for name, required in skill_status.items()
    ]