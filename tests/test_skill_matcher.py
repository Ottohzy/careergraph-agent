import pytest

from careergraph.skill_matcher import (find_missing_skills, calculate_match_rate, count_skills,normalize_skills, find_matched_skills)

def test_count_skills_normal_input():
    skills = ["Python", "Java", "Python", "C++", "java"]
    result = count_skills(skills)
    assert result == {"python": 2, "java": 2, "c++": 1}

def test_count_skills_ignore_case_and_spaces():
    skills = [" Python ", "java", "PYTHON", "C++", "java", "  c++  ", "  ", ""]
    result = count_skills(skills)
    assert result == {"python": 2, "java": 2, "c++": 2}

def test_count_skills_empty_input_and_only_spaces():
    skills = ["", "   ", "  "]
    result = count_skills(skills)
    assert result == {}
    assert count_skills([]) == {}

def test_find_missing_skills_normal_input():
    required_skills = ["JAVA", "Python", "C++"]
    candidate_skills = ["Python", "C++", "Git"]
    result = find_missing_skills(required_skills, candidate_skills)
    assert result == ["java"]

def test_find_missing_skills_ignores_case_and_spaces_and_use_required_skills_name():
    required_skills=[" JAVA ", "Py  T  hon", "c++"]
    candidate_skills=["C++", "git"]
    result = find_missing_skills(required_skills, candidate_skills)
    assert result == ["java", "py  t  hon"]

def test_find_missing_skills_empty_input_and_only_spaces():
    required_skills = ["", "   ", "  "]
    candidate_skills = ["Python", "C++"]
    result = find_missing_skills(required_skills, candidate_skills)
    assert result == []
    assert find_missing_skills([], candidate_skills) == []
    assert find_missing_skills(required_skills, []) == []

def test_find_missing_skills_no_missing_skills():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Python", "Java", "C++"]
    result = find_missing_skills(required_skills, candidate_skills)
    assert result == []

def test_missing_skills_with_duplicates_in_required_skills():
    required_skills = ["Python", "Java", "Python", "C++"]
    candidate_skills = []
    result = find_missing_skills(required_skills, candidate_skills)
    assert result == ["c++", "java", "python"]

def test_calculate_match_rate_normal_input():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Python", "C++"]
    result = calculate_match_rate(required_skills, candidate_skills)
    assert result == 2/3

def test_calculate_match_rate_with_empty_required_skills():
    required_skills = []
    candidate_skills = ["Python", "C++"]
    result = calculate_match_rate(required_skills, candidate_skills)
    assert result == 0.0

def test_calculate_match_rate_with_empty_candidate_skills():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = []
    result = calculate_match_rate(required_skills, candidate_skills)
    assert result == 0.0

def test_calculate_match_rate_with_no_missing_skills():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Python", "Java", "C++"]
    result = calculate_match_rate(required_skills, candidate_skills)
    assert result == 1.0

def test_calculate_match_rate_with_duplicates_in_required_skills():
    required_skills = ["Python", "Java", "Python", "C++"]
    candidate_skills = ["Python"]
    result = calculate_match_rate(required_skills, candidate_skills)
    assert result == 1/3
    
def test_calculate_match_rate_decimal_result():
    required_skills = ["Python", "C++", "JavaScript"]
    candidate_skills = ["Python", "C++"]
    result = calculate_match_rate(required_skills, candidate_skills)
    assert result == pytest.approx(2/3, rel=1e-9)

def test_normalize_skills_normal_input():
    skills = ["Python", "Java", "C++", "Python", "java"]
    result = normalize_skills(skills)
    assert result == {"python", "java", "c++"}

def test_normalize_skills_ignore_case_and_spaces():
    skills = [" Python ", "java", "PYTHON", "C++", "java", "  c++  ", "  ", ""]
    result = normalize_skills(skills)
    assert result == {"python", "java", "c++"}

def test_normalize_skills_empty_input_and_only_spaces():
    skills = ["", "   ", "  "]
    result = normalize_skills(skills)
    assert result == set()
    assert normalize_skills([]) == set()

def test_normalize_skills_with_duplicates():
    skills = ["Python", "Java", "Python", "C++"]
    result = normalize_skills(skills)
    assert result == {"python", "java", "c++"}
 
def test_normalize_skills_with_special_characters():
    skills = ["Python!", "Java@", "C++#", "Python$", "java%"]
    result = normalize_skills(skills)
    assert result == {"python!", "java@", "c++#", "python$", "java%"}

def test_normalize_skills_with_numbers():
    skills = ["Python3", "Java8", "C++11", "Python3", "java8"]
    result = normalize_skills(skills)
    assert result == {"python3", "java8", "c++11"}

def test_normalize_skills_with_mixed_characters():
    skills = ["Python3!", "Java8@", "C++11#", "Python3$", "java8%"]
    result = normalize_skills(skills)
    assert result == {"python3!", "java8@", "c++11#", "python3$", "java8%"}

def test_normalize_skills_with_unicode_characters():
    skills = ["Pythön", "Jävä", "C++", "Pythön", "jävä"]
    result = normalize_skills(skills)
    assert result == {"pythön", "jävä", "c++"}

def test_normalize_skills_with_leading_and_trailing_spaces():
    skills = ["  Python  ", "  Java", "C++  ", "  Python", "Java  "]
    result = normalize_skills(skills)
    assert result == {"python", "java", "c++"}

def test_find_matched_skills_with_normal_input():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Python", "C++", "Git"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++", "python"]

def test_find_matched_skills_with_no_matches():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Git", "Docker"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == []

def test_find_matched_skills_with_all_matches():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Python", "Java", "C++"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++", "java", "python"]

def test_find_matched_skills_with_duplicates_in_required_skills():
    required_skills = ["Python", "Java", "Python", "C++"]
    candidate_skills = ["Python", "C++"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++", "python"]

def test_find_matched_skills_with_duplicates_in_candidate_skills():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["Python", "C++", "Python"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++", "python"]

def test_find_matched_skills_with_empty_required_skills():
    required_skills = []
    candidate_skills = ["Python", "C++"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == []

def test_find_matched_skills_with_empty_candidate_skills():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = []
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == []

def test_find_matched_skills_with_empty_inputs():
    required_skills = []
    candidate_skills = []
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == []
def test_find_matched_skills_with_case_insensitivity():
    required_skills = ["Python", "Java", "C++"]
    candidate_skills = ["python", "c++"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++", "python"]

def test_find_matched_skills_with_spaces_in_skills():
    required_skills = [" Python ", " Java ", " C++ "]
    candidate_skills = ["python", "c++"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++", "python"]

def test_find_matched_skills_with_special_characters():
    required_skills = ["Python!", "Java@", "C++#"]
    candidate_skills = ["python!", "c++#"]
    result = find_matched_skills(required_skills, candidate_skills)
    assert result == ["c++#", "python!"]
