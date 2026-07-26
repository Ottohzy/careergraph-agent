import pytest
from careergraph.scorer import calculate_match_rate


def test_calculate_match_rate_returns_expected_ratio():
    matched_skills = {"python", "java"}
    required_skills = {"python", "java", "sql"}

    result = calculate_match_rate(matched_skills, required_skills)

    assert result == 2 / 3


def test_calculate_match_rate_returns_zero_for_empty_required_skills():
    matched_skills = {"python"}
    required_skills = set()

    result = calculate_match_rate(matched_skills, required_skills)

    assert result == 0.0

def test_calculate_match_rate_returns_zero_for_no_matched_skills():
    matched_skills = set()
    required_skills = {"python", "java"}

    result = calculate_match_rate(matched_skills, required_skills)

    assert result == 0.0

def test_calculate_match_rate_returns_one_for_all_matched_skills():
    matched_skills = {"python", "java"}
    required_skills = {"python", "java"}

    result = calculate_match_rate(matched_skills, required_skills)

    assert result == 1.0


