import pytest

from careergraph.matcher import match_skills


def test_match_skills_returns_matched_and_missing_sets():
    required_skills = {"python", "java", "sql"}
    candidate_skills = {"python", "aws", "sql"}

    matched_skills, missing_skills = match_skills(required_skills, candidate_skills)

    assert matched_skills == {"python", "sql"}
    assert missing_skills == {"java"}


def test_match_skills_returns_empty_sets_when_there_is_no_overlap():
    required_skills = {"python", "java"}
    candidate_skills = {"aws", "docker"}

    matched_skills, missing_skills = match_skills(required_skills, candidate_skills)

    assert matched_skills == set()
    assert missing_skills == {"python", "java"}

def test_match_skills_with_empty_required_skills():
    required_skills = set()
    candidate_skills = {"python", "java"}

    matched_skills, missing_skills = match_skills(required_skills, candidate_skills)

    assert matched_skills == set()
    assert missing_skills == set()

def test_match_skills_with_empty_candidate_skills():
    required_skills = {"python", "java"}
    candidate_skills = set()

    matched_skills, missing_skills = match_skills(required_skills, candidate_skills)

    assert matched_skills == set()
    assert missing_skills == {"python", "java"}

def test_match_skills_with_both_empty_sets():
    required_skills = set()
    candidate_skills = set()

    matched_skills, missing_skills = match_skills(required_skills, candidate_skills)

    assert matched_skills == set()
    assert missing_skills == set()

def test_match_skills_with_non_set_inputs():
    required_skills = ["python", "java"]  # This should be a set
    candidate_skills = {"python", "aws"}

    with pytest.raises(ValueError, match="Required skills must be provided as a set."):
        match_skills(required_skills, candidate_skills)

    required_skills = {"python", "java"}
    candidate_skills = ["python", "aws"]  # This should be a set

    with pytest.raises(ValueError, match="Candidate skills must be provided as a set."):
        match_skills(required_skills, candidate_skills)

def test_matcher_returns_intersection():
    required_skills = {"python", "java", "sql"}
    candidate_skills = {"python", "aws", "sql"}

    matched_skills, missing_skills = match_skills(required_skills, candidate_skills)

    assert matched_skills == {"python", "sql"}
    assert missing_skills == {"java"}
    