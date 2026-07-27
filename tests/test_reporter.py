from careergraph.reporter import (
    format_analysis_report,
    format_skills,
)


def test_format_skills_returns_sorted_string():
    skills = {
        "sql",
        "python",
        "docker",
    }

    result = format_skills(skills)

    assert result == "docker, python, sql"


def test_format_skills_returns_none_for_empty_set():
    result = format_skills(set())

    assert result == "None"


def test_format_analysis_report_contains_candidate_name():
    report = format_analysis_report(
        candidate_name="Zhengrong",
        required_skills={"python", "sql"},
        candidate_skills={"python"},
        matched_skills={"python"},
        missing_skills={"sql"},
        match_rate=0.5,
    )

    assert "Candidate: Zhengrong" in report


def test_format_analysis_report_contains_match_rate():
    report = format_analysis_report(
        candidate_name="Zhengrong",
        required_skills={"python", "sql"},
        candidate_skills={"python"},
        matched_skills={"python"},
        missing_skills={"sql"},
        match_rate=0.5,
    )

    assert "Match rate: 50.0%" in report


def test_format_analysis_report_handles_empty_skills():
    report = format_analysis_report(
        candidate_name="Zhengrong",
        required_skills=set(),
        candidate_skills=set(),
        matched_skills=set(),
        missing_skills=set(),
        match_rate=0.0,
    )

    assert "Required skills: None" in report
    assert "Candidate skills: None" in report
    assert "Matched skills: None" in report
    assert "Missing skills: None" in report