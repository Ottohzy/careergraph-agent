import logging
from pathlib import Path

from careergraph.normalizer import normalize_skills
from careergraph.config_loader import (
    load_skill_aliases,
    load_skill_catalog,
)
from careergraph.data_loader import (
    get_candidate_skills,
    load_candidate_profile,
    load_jd_text,
)
from careergraph.matcher import match_skills
from careergraph.jd_extractor import extract_skills
from careergraph.scorer import calculate_match_rate


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(name)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


DATA_DIR = Path("data")

CANDIDATE_PROFILE_PATH = (
    DATA_DIR / "candidate_profile.json"
)

JD_PATH = (
    DATA_DIR / "job_description.txt"
)

SKILL_CATALOG_PATH = (
    DATA_DIR / "skill_catalog.json"
)

SKILL_ALIASES_PATH = (
    DATA_DIR / "skill_aliases.json"
)


def format_skills(skills: set[str]) -> str:
    """
    Convert a skill set into a readable string.
    """
    if not skills:
        return "None"

    return ", ".join(sorted(skills))


def print_analysis_result(
    candidate_name: str,
    required_skills: set[str],
    candidate_skills: set[str],
    matched_skills: set[str],
    missing_skills: set[str],
    match_rate: float,
) -> None:
    """
    Print the final skill matching result.
    """
    print()
    print("===== CareerGraph Analysis =====")
    print(f"Candidate: {candidate_name}")

    print(
        "Required skills:",
        format_skills(required_skills),
    )

    print(
        "Candidate skills:",
        format_skills(candidate_skills),
    )

    print(
        "Matched skills:",
        format_skills(matched_skills),
    )

    print(
        "Missing skills:",
        format_skills(missing_skills),
    )

    print(f"Match rate: {match_rate:.1%}")


def main() -> None:
    logger.info(
        "CareerGraph analysis started."
    )

    # 1. 读取 candidate profile
    candidate_profile = load_candidate_profile(
        CANDIDATE_PROFILE_PATH
    )

    # 2. 获取并标准化候选人技能
    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    # 3. 读取 JD
    jd_text = load_jd_text(
        JD_PATH
    )

    # 4. 加载技能 catalog
    skill_catalog = load_skill_catalog(
        SKILL_CATALOG_PATH
    )

    # 5. 加载技能 aliases
    skill_aliases = load_skill_aliases(
        SKILL_ALIASES_PATH
    )

    # 6. 从 JD 中抽取岗位要求技能
    job_skills = extract_skills(
        jd_text=jd_text,
        aliases=skill_aliases,
    )
    
    # Convert JobSkill objects to a set of required skill names
    required_skills = normalize_skills([
    skill.name
    for skill in job_skills
    if skill.required
    ])

    # 7. 匹配技能
    matched_skills, missing_skills = match_skills(
        required_skills=required_skills,
        candidate_skills=candidate_skills,
    )

    # 8. 计算技能覆盖率
    match_rate = calculate_match_rate(
        required_skills=required_skills,
        matched_skills=matched_skills,
    )

    # 9. 输出结果
    candidate_name = candidate_profile.get(
        "name",
        "Unknown candidate",
    )

    print_analysis_result(
        candidate_name=candidate_name,
        required_skills=required_skills,
        candidate_skills=candidate_skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        match_rate=match_rate,
    )

    logger.info(
        "CareerGraph analysis completed successfully."
    )


if __name__ == "__main__":
    main()