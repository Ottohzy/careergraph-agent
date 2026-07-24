import pytest
from careergraph.normalizer import normalize_skills

def test_normalize_skills_with_normal_input():
    skills = ["  Python  ", "  Java", "C++  ", "  Python", "Java  "]
    result = normalize_skills(skills)
    assert result == {"python", "java", "c++"}

def test_normalize_skills_with_empty_input():
    skills = []
    result = normalize_skills(skills)
    assert result == set()

def test_normalize_skills_with_only_spaces():
    skills = ["   ", "  ", " "]
    result = normalize_skills(skills)
    assert result == set()


def test_normalize_skills_deduplicates_and_normalizes_values():
    skills = [" Python ", "python", "  JAVA  ", "java", "   "]
    result = normalize_skills(skills)
    assert result == {"python", "java"}