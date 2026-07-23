import json
from pathlib import Path
from typing import Any

from careergraph.skill_matcher import normalize_skills


def load_candidate_profile(
    file_path: str | Path,
) -> dict[str, Any]:
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        profile = json.load(file)

    if not isinstance(profile, dict):
        raise ValueError(
            "Candidate profile must be a JSON object."
        )

    return profile


def get_candidate_skills(
    candidate_profile: dict[str, Any],
) -> set[str]:
    skills = candidate_profile.get("skills", [])

    if not isinstance(skills, list):
        raise ValueError(
            "Candidate skills must be a list."
        )

    return normalize_skills(skills)


def load_jd_text(
    file_path: str | Path,
) -> str:
    path = Path(file_path)

    jd_text = path.read_text(
        encoding="utf-8"
    ).strip()

    if not jd_text:
        raise ValueError(
            "Job description cannot be empty."
        )

    return jd_text