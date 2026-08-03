import argparse
import logging
from pathlib import Path
from typing import Any

from careergraph.config_loader import (
    load_skill_aliases,
    load_skill_catalog,
)
from careergraph.data_loader import (
    get_candidate_skills,
    load_candidate_profile,
    load_jd_text,
)
from careergraph.jd_extractor import extract_skills
from careergraph.matcher import match_skills
from careergraph.normalizer import normalize_skills
from careergraph.reporter import format_analysis_report
from careergraph.scorer import calculate_match_rate
from careergraph.schema import Analysis, Job
from careergraph.api import app


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


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Analyze the skill match between a candidate "
            "and a job description."
        ),
    )

    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path(
            "data/candidate_profile.json"
        ),
        help=(
            "Path to the candidate profile JSON file. "
            "Default: data/candidate_profile.json"
        ),
    )

    parser.add_argument(
        "--jd",
        type=Path,
        default=Path(
            "data/job_description.txt"
        ),
        help=(
            "Path to the job description text file. "
            "Default: data/job_description.txt"
        ),
    )

    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path(
            "data/skill_catalog.json"
        ),
        help=(
            "Path to the skill catalog JSON file. "
            "Default: data/skill_catalog.json"
        ),
    )

    parser.add_argument(
        "--aliases",
        type=Path,
        default=Path(
            "data/skill_aliases.json"
        ),
        help=(
            "Path to the skill aliases JSON file. "
            "Default: data/skill_aliases.json"
        ),
    )

    return parser.parse_args()


def run_analysis(
    candidate_path: str | Path,
    jd_path: str | Path,
    catalog_path: str | Path,
    aliases_path: str | Path,
) -> dict[str, Any]:
    """
    Run the complete CareerGraph analysis workflow.
    """
    # 1. 读取候选人资料
    candidate_profile = load_candidate_profile(
        candidate_path
    )

    # 2. 获取候选人技能
    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    # 3. 读取 JD
    jd_text = load_jd_text(
        jd_path
    )

    job_title = next(
        (
            line.strip()
            for line in jd_text.splitlines()
            if line.strip()
        ),
        "Untitled Job",
    )

    job = Job(
        job_id=Path(jd_path).stem or "job",
        title=job_title,
        raw_text=jd_text,
    )

    # 4. 加载技能目录
    skill_catalog = load_skill_catalog(
        catalog_path
    )

    # 5. 加载技能别名
    skill_aliases = load_skill_aliases(
        aliases_path
    )

    logger.info(
        "Loaded %d skills from the skill catalog.",
        len(skill_catalog),
    )

    # 6. 抽取 JD 技能
    job_skills = extract_skills(
        jd_text=jd_text,
        aliases=skill_aliases,
    )

    # 7. 获取必需技能
    required_skills = normalize_skills(
        [
            skill.name
            for skill in job_skills
            if skill.required
        ]
    )

    # 8. 匹配技能
    matched_skills, missing_skills = match_skills(
        required_skills=required_skills,
        candidate_skills=candidate_skills,
    )

    # 9. 计算覆盖率
    match_rate = calculate_match_rate(
        required_skills=required_skills,
        matched_skills=matched_skills,
    )

    candidate_name = candidate_profile.get(
        "name",
        "Unknown candidate",
    )

    candidate_id = candidate_profile.get(
        "candidate_id",
    )

    if not isinstance(candidate_id, str) or not candidate_id.strip():
        raise ValueError(
            "Candidate profile must include a valid candidate_id."
        )

    analysis = Analysis(
        analysis_id=(
            f"{candidate_id}-{job.job_id}"
        ),
        job_id=job.job_id,
        candidate_id=candidate_id,
        required_skills=sorted(required_skills),
        matched_skills=sorted(matched_skills),
        missing_skills=sorted(missing_skills),
        match_rate=match_rate,
    )

    return {
        "candidate_id": candidate_id,
        "job_id": job.job_id,
        "analysis_id": analysis.analysis_id,
        "candidate_name": candidate_name,
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_rate": analysis.match_rate,
    }


def main() -> None:
    """
    Parse CLI arguments, run analysis,
    and print the final report.
    """
    args = parse_args()

    logger.info(
        "CareerGraph analysis started."
    )

    try:
        result = run_analysis(
            candidate_path=args.candidate,
            jd_path=args.jd,
            catalog_path=args.catalog,
            aliases_path=args.aliases,
        )

        report = format_analysis_report(
            candidate_name=result["candidate_name"],
            required_skills=result["required_skills"],
            candidate_skills=result["candidate_skills"],
            matched_skills=result["matched_skills"],
            missing_skills=result["missing_skills"],
            match_rate=result["match_rate"],
        )

        print()
        print(report)

    except FileNotFoundError as error:
        logger.error(
            "Input file not found: %s",
            error,
        )

    except ValueError as error:
        logger.error(
            "Invalid input data: %s",
            error,
        )

    except TypeError as error:
        logger.error(
            "Invalid data type: %s",
            error,
        )

    else:
        logger.info(
            "CareerGraph analysis completed successfully."
        )


if __name__ == "__main__":
    main()