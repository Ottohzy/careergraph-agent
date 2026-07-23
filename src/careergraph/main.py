from careergraph.data_loader import (
    get_candidate_skills,
    load_candidate_profile,
    load_jd_text,
)

from .skill_matcher import (
    find_missing_skills,
    calculate_match_rate,
    count_skills,
    normalize_skills,
    find_matched_skills,)




def main() -> None:
    candidate = load_candidate_profile(
        "data/candidate_profile.json"
    )

    candidate_skills = get_candidate_skills(candidate)

    jd_text = load_jd_text(
        "data/sample_jd.txt"
    )

    print(
        f"Candidate: {candidate.get('name', 'Unknown')}"
    )
    print(
        f"Candidate skills: {sorted(candidate_skills)}"
    )
    print("JD loaded successfully.")
    print(f"JD length: {len(jd_text)} characters")


if __name__ == "__main__":
    main()